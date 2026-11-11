"""Emit a reviewable, key-free usage manifest from one editor project."""
import argparse
import hashlib
import json
import re
import sys
import unicodedata
from pathlib import Path
from editor_model import selected_questions


def normalized(value):
    return re.sub(r'\s+', ' ', unicodedata.normalize('NFKC', str(value or '')).casefold()).strip()


def signature(question):
    parts = [question.get('introduction'), question.get('stem')]
    parts += [option.get('text') for option in question.get('options', [])]
    return hashlib.sha256('\n'.join(normalized(part) for part in parts).encode('utf-8')).hexdigest()


def records(project, session):
    selected = selected_questions(project)
    return [{
        'simulacro': project['code'],
        'sesion': session,
        'area': q['area'],
        'numero_actual': number,
        'editor_id': q['id'],
        'catalog_id': q.get('catalog_id') or None,
        'estado': 'usada_fuente_pendiente' if not q.get('catalog_id') else 'usada',
        'tema': q.get('topic', ''),
        'inicio': (q.get('introduction') or '')[:180],
        'enunciado': (q.get('stem') or '')[:240],
        'huella_texto': signature(q),
    } for number, q in enumerate(selected, 1)]


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('project', type=Path)
    parser.add_argument('--session', choices=['primera', 'segunda'], required=True)
    args = parser.parse_args()
    project = json.loads(args.project.read_text(encoding='utf-8'))
    print(json.dumps({
        'schema': 1,
        'scope': 'uso_global_entre_simulacros',
        'nota': 'La huella detecta texto normalizado igual; las variantes de escaneo requieren cotejo visual.',
        'preguntas': records(project, args.session),
    }, ensure_ascii=False, indent=2))
