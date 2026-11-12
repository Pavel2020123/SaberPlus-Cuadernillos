"""Build an independent SP-002 review project from the protected 120-item pilot.

The reviewed replacement manifest is intentionally separate from the original
pilot. This script verifies original PDF hashes and known code conflicts before
writing inside output/pilots/sp002-final-revisado only.
"""
import copy
import hashlib
import json
import re
import shutil
import subprocess
import sys
import uuid
from pathlib import Path

import pymupdf

from editor_model import ROOT, validate_project
from import_booklet_questions import equivalent_codes, region_rect, source_path


BASE = ROOT / 'output/pilots/sp002-ciencias-manual'
DEST = ROOT / 'output/pilots/sp002-final-revisado'
COLLECTION = Path('D:/Icfes_SaberPlus')
POSITIONS = {
    92: 'USB-2722e7c48dfd-Q049',
    93: 'USB-524d98b0a234-Q058',
    98: 'USB-7882c8f9ae2f-Q063',
    99: 'USB-77cc8ac26d2c-Q098',
    104: 'USB-2722e7c48dfd-Q052',
    105: 'USB-7882c8f9ae2f-Q066',
    108: 'USB-77cc8ac26d2c-Q086',
    109: 'USB-7882c8f9ae2f-Q078',
    110: 'USB-7882c8f9ae2f-Q061',
    111: 'USB-e4489f150183-Q061',
    112: 'USB-e4489f150183-Q048',
    113: 'USB-77cc8ac26d2c-Q087',
    114: 'USB-2722e7c48dfd-Q050',
    116: 'USB-2722e7c48dfd-Q055',
    119: 'USB-524d98b0a234-Q072',
    120: 'USB-77cc8ac26d2c-Q088',
}


def git_text(ref, path):
    return subprocess.check_output(['git', 'show', f'{ref}:{path}'], cwd=ROOT).decode('utf-8-sig')


def referenced_assets(project):
    paths = set()
    for obj in project['contexts'] + project['questions']:
        if obj.get('image'):
            paths.add(obj['image'])
    for q in project['questions']:
        paths.update(o['image'] for o in q['options'] if o.get('image'))
    return paths


def main():
    base_raw = (BASE / 'project.json').read_bytes()
    progress = json.loads((DEST / 'substitution-progress.json').read_text(encoding='utf-8'))
    if hashlib.sha256(base_raw).hexdigest() != progress['base_sha256']:
        raise ValueError('El proyecto original cambió desde la copia de seguridad.')
    backups = [folder for folder in (ROOT / 'output/pilots/backups').glob('sp002-ciencias-manual-*')
               if (folder / 'backup-manifest.json').is_file()
               and json.loads((folder / 'backup-manifest.json').read_text(encoding='utf-8'))['project_sha256'] == progress['base_sha256']]
    if not backups:
        raise ValueError('No existe el respaldo independiente verificado del proyecto base.')
    backup = sorted(backups)[-1]
    project = json.loads(base_raw)
    entries = json.loads((DEST / 'substitutions.json').read_text(encoding='utf-8'))
    by_code = {row['new_code']: row['question'] for row in entries}
    if len(by_code) != 16 or set(by_code) != set(POSITIONS.values()):
        raise ValueError('Se necesitan exactamente 16 reemplazos distintos y documentados.')
    catalog = json.loads((ROOT / 'output/cotejo_30/indice_editorial.json').read_text(encoding='utf-8'))
    archive = json.loads((ROOT / 'output/cotejo_30/archivo_fichas_consolidadas.json').read_text(encoding='utf-8'))
    catalog_by_code = {row['catalog_id']: row for row in catalog}
    expand = equivalent_codes(catalog, archive)
    registry = json.loads(git_text('origin/main', 'planning/PREGUNTAS_USADAS_GLOBAL.json'))
    occupied = {row.get('catalog_id') for row in registry['preguntas'] + registry['reservas'] if row.get('catalog_id')}
    occupied.update(re.findall(r'USB-[a-f0-9]{12}-Q\d{3}', git_text('origin/trabajo/sp-003', 'planning/reservas/SP-003.md')))
    occupied.update(re.findall(r'USB-[a-f0-9]{12}-Q\d{3}', git_text('origin/trabajo/sp-003', 'planning/SP003_S1_CIENCIAS_CODIGOS.txt')))
    pending = json.loads((ROOT / 'output/cotejo_30/cotejos_pendientes.json').read_text(encoding='utf-8'))
    adjacent = {}
    for pair in pending:
        a = f'{pair["left"][0]}-Q{pair["left"][1]:03d}'
        b = f'{pair["right"][0]}-Q{pair["right"][1]:03d}'
        adjacent.setdefault(a, set()).add(b)
        adjacent.setdefault(b, set()).add(a)
    kept = {q.get('catalog_id') for n, q in enumerate(project['questions'], 1) if n not in POSITIONS and q.get('catalog_id')}
    for code in by_code:
        if (expand(code) | adjacent.get(code, set())) & (occupied | kept | (set(by_code) - {code})):
            raise ValueError('Equivalencia o cotejo pendiente con código ocupado: ' + code)
    docs = {}
    new_assets = {}
    substitutions = []
    for position, code in POSITIONS.items():
        item = by_code[code]
        source = catalog_by_code[code]
        if source['physical_page'] != item['page'] or source['area_normalized'] != 'Ciencias naturales':
            raise ValueError('Fuente o página incompatible: ' + code)
        fid = source['file_id']
        if fid not in docs:
            path = source_path(source, COLLECTION)
            docs[fid] = (path, pymupdf.open(path))
        source_file, doc = docs[fid]
        old = project['questions'][position - 1]
        question = {
            'id': 'q-' + str(uuid.uuid5(uuid.NAMESPACE_URL, 'sp002-first-session-' + code)),
            'area': 'science', 'part': 0, 'order': old['order'],
            'topic': item['topic'], 'subtopic': item['subtopic'],
            'stem': item['stem'],
            'options': [{'text': text} for text in item['options']],
            'correct': item['correct'], 'explanation': item['explanation'],
            'layout': 'full', 'included': True, 'context': None, 'slot': '',
            'assessment': {
                'framework': 'icfes-guia-2026-2', 'area': 'science', 'status': 'proposed',
                'competency': item['competency'], 'process': None,
                'claim': item['claim'], 'evidence': None,
                'component': item['component'], 'part': None,
                'rationale': item['rationale'], 'reviewer': None, 'reviewed_at': None,
            },
            'option_drafts': {}, 'catalog_id': code,
        }
        if item.get('introduction'):
            question['introduction'] = item['introduction']
        for asset in item['assets']:
            if asset['kind'] != 'question':
                raise ValueError('Tipo de recorte no soportado.')
            page = doc[item['page'] - 1]
            rect = region_rect(page, asset['region'])
            raw = page.get_pixmap(matrix=pymupdf.Matrix(3, 3), clip=rect, alpha=False).tobytes('png')
            name = 'assets/uploads/' + hashlib.sha256(raw).hexdigest()[:32] + '.png'
            question['image'] = name
            question['image_height'] = 360 if code == 'USB-e4489f150183-Q048' else (190 if code == 'USB-7882c8f9ae2f-Q078' else 145)
            new_assets[name] = raw
        project['questions'][position - 1] = question
        substitutions.append({
            'position': position, 'old_code': old['catalog_id'], 'new_code': code,
            'reason': next(row['reason'] for row in progress['conflicts'] if row['position'] == position),
            'source_pdf': source_file.name, 'source_sha256': source['source_sha256'],
            'physical_page': item['page'], 'original_question': source['question'],
            'answer_verified': item['correct'], 'status': 'proposal_for_editorial_review',
            'pending_unoccupied_equivalences': sorted(adjacent.get(code, set())),
            'question': item,
        })
    # Two inherited questions had complete content but no editorial classification.
    project['questions'][3]['assessment'].update(
        status='proposed', competency='interpretation', claim='1',
        rationale='Relaciona los valores de dos tablas con su representación en gráficas de barras.')
    project['questions'][32]['assessment'].update(
        status='proposed', competency='reading', process='local', claim='1',
        rationale='Identifica una paráfrasis fiel de una afirmación localizada en el texto.')
    project['revision'] = 1
    warnings = validate_project(project, exporting=True)
    if len(project['questions']) != 120:
        raise ValueError('La cantidad final no es 120.')
    for path in referenced_assets(project):
        target = DEST / path
        target.parent.mkdir(parents=True, exist_ok=True)
        if path in new_assets:
            target.write_bytes(new_assets[path])
            # The editor's existing asset route and PDF renderer use ROOT/assets/uploads.
            shared = ROOT / path
            shared.parent.mkdir(parents=True, exist_ok=True)
            if shared.exists() and shared.read_bytes() != new_assets[path]:
                raise ValueError('Colisión de nombre en recursos del editor: ' + path)
            if not shared.exists():
                shared.write_bytes(new_assets[path])
        else:
            source = backup / path
            if not source.is_file():
                raise FileNotFoundError(source)
            shutil.copy2(source, target)
    (DEST / 'project.json').write_text(json.dumps(project, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    (DEST / 'substitutions.json').write_text(json.dumps(substitutions, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    progress['state'] = 'independent_project_built_pdf_pending'
    for row in progress['conflicts']:
        row['new_code'] = POSITIONS[row['position']]
        row['status'] = 'proposal_for_editorial_review'
    (DEST / 'substitution-progress.json').write_text(json.dumps(progress, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('project', DEST / 'project.json')
    print('questions', len(project['questions']), 'assets', len(referenced_assets(project)), 'warnings', warnings)


if __name__ == '__main__':
    main()
