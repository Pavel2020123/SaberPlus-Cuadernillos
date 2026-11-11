"""Append saved editor questions to the shared usage manifest; reject exact reuse."""
import argparse
import json
import os
import tempfile
from pathlib import Path
from export_used_questions import records


def merge(ledger, project, session):
    current = list(ledger['preguntas'])
    by_owner = {(r['simulacro'], r['sesion'], r['editor_id']): r for r in current}
    incoming = records(project, session)
    for item in incoming:
        key = (item['simulacro'], item['sesion'], item['editor_id'])
        old = by_owner.get(key)
        if old:
            if not item['catalog_id']:
                item['catalog_id'] = old.get('catalog_id')
                if item['catalog_id']:
                    item['estado'] = 'usada'
            current[current.index(old)] = item
            by_owner[key] = item
        else:
            current.append(item)
            by_owner[key] = item
    clashes = []
    for i, left in enumerate(current):
        for right in current[i + 1:]:
            if (left['simulacro'], left['sesion'], left['editor_id']) == (right['simulacro'], right['sesion'], right['editor_id']):
                continue
            reasons = []
            if left.get('catalog_id') and left['catalog_id'] == right.get('catalog_id'):
                reasons.append('mismo código de catálogo')
            if left.get('huella_texto') and left['huella_texto'] == right.get('huella_texto'):
                reasons.append('mismo texto normalizado')
            if reasons:
                clashes.append((left, right, ', '.join(reasons)))
    return current, clashes


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('project', type=Path, help='JSON guardado del editor')
    parser.add_argument('--session', choices=['primera', 'segunda'], required=True)
    parser.add_argument('--ledger', type=Path, default=Path(__file__).resolve().parents[1] / 'planning/PREGUNTAS_USADAS_GLOBAL.json')
    parser.add_argument('--check-only', action='store_true')
    args = parser.parse_args()
    project = json.loads(args.project.read_text(encoding='utf-8'))
    expected = 'first' if args.session == 'primera' else 'second'
    if project['session'] != expected:
        parser.error('La sesión indicada no coincide con el proyecto.')
    ledger = json.loads(args.ledger.read_text(encoding='utf-8'))
    updated, clashes = merge(ledger, project, args.session)
    if clashes:
        for left, right, reason in clashes:
            print(f'REPETIDA: {left["simulacro"]}/{left["sesion"]}/{left["numero_actual"]} y '
                  f'{right["simulacro"]}/{right["sesion"]}/{right["numero_actual"]}: {reason}')
        raise SystemExit(2)
    print(f'Sin repeticiones exactas detectadas. Registro: {len(updated)} preguntas.')
    if args.check_only:
        return
    ledger['preguntas'] = updated
    payload = json.dumps(ledger, ensure_ascii=False, indent=2) + '\n'
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=args.ledger.parent, prefix='.uso-global-', suffix='.tmp', delete=False) as temp:
        temp.write(payload)
        temporary = Path(temp.name)
    try:
        os.replace(temporary, args.ledger)
    finally:
        temporary.unlink(missing_ok=True)


if __name__ == '__main__':
    main()
