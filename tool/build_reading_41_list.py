"""Reproduce the inspected 41-item Reading shortlist from the USB catalog."""
import collections
import json
from pathlib import Path

from editor_model import ROOT

CATALOG = ROOT / 'output/cotejo_30/indice_editorial.json'
OUTPUT = ROOT / 'planning/SP001_S1_LECTURA_41.md'
GROUPS = [
    ('USB-04dc5257ed8b', 30, 31),
    ('USB-a170782eadcb', 27, 30),
    ('USB-d4e43db6988a', 26, 30),
    ('USB-04dc5257ed8b', 26, 29),
    ('USB-a170782eadcb', 33, 34),
    ('USB-d4e43db6988a', 60, 64),
    ('USB-04dc5257ed8b', 23, 25),
    ('USB-a170782eadcb', 64, 65),
    ('USB-d4e43db6988a', 52, 53),
    ('USB-04dc5257ed8b', 35, 36),
    ('USB-a170782eadcb', 54, 54),
    ('USB-d4e43db6988a', 65, 66),
    ('USB-04dc5257ed8b', 41, 42),
    ('USB-04dc5257ed8b', 43, 45),
    ('USB-04dc5257ed8b', 52, 53),
]
SOURCES = {
    'USB-04dc5257ed8b': '2026 calendario por confirmar · Castillo San Felipe',
    'USB-a170782eadcb': '2025-2 AAA1',
    'USB-d4e43db6988a': '2026 calendario B · Cóndor Andino',
}


def process(q):
    label = (q.get('competency_proposal') or '').lower()
    if 'identif' in label:
        return 'Información local'
    if 'comprend' in label:
        return 'Sentido global'
    if 'reflex' in label:
        return 'Reflexión/evaluación'
    raise ValueError('Competencia por cotejar: ' + q['catalog_id'])


def select(catalog):
    by_id = {(q['file_id'], q['question']): q for q in catalog if 'lectura' in (q.get('area') or '').lower()}
    result = [by_id[(file_id, number)] for file_id, first, last in GROUPS for number in range(first, last + 1)]
    counts = collections.Counter(map(process, result))
    if len(result) != 41 or counts != {'Información local': 10, 'Sentido global': 17, 'Reflexión/evaluación': 14}:
        raise ValueError('La lista ya no cumple 41 y la distribución 10/17/14.')
    if any(q.get('alert') or not q.get('answer_proposal') or q.get('cross_source_key_conflict') for q in result):
        raise ValueError('Hay una alerta o clave no resuelta en la lista.')
    selected = {(q['file_id'], q['question']) for q in result}
    if any((e['file_id'], e['question']) in selected for q in result for e in q.get('additional_source_evidence', [])):
        raise ValueError('Hay apariciones exactas duplicadas entre las elegidas.')
    return result, counts


def render(items):
    lines = [
        '# SP-001 · Primera sesión · 41 candidatas de Lectura crítica',
        '',
        'Estado: selección editorial propuesta, no cargada ni marcada como usada. Numeración prevista: 26–66, después de las 25 de Matemáticas. Metas: información local 10, sentido global 17, reflexión/evaluación 14. Son procesos/objetivos de una competencia lectora, no tres competencias oficiales.',
        '',
        'Se inspeccionaron las páginas físicas pertinentes de tres PDF escaneados. Las clasificaciones y claves son propuestas del catálogo que deben verificarse al transcribir. En las 41 fichas no hay alertas de clave, claves vacías, conflictos documentados de clave ni apariciones exactas repetidas dentro de esta selección. Aún hay cotejos de posibles variantes pendientes: esta lista no certifica unicidad absoluta.',
        '',
        '| N.º SP-001 | Código | Fuente · página física / pregunta original | Lectura compartida | Proceso | Tarea resumida | Clave propuesta |',
        '| ---: | --- | --- | --- | --- | --- | :---: |',
    ]
    for number, q in enumerate(items, 26):
        lines.append(f"| {number} | `{q['catalog_id']}` | {SOURCES[q['file_id']]} · {q['physical_page']}/{q['question']} | {q.get('context_id') or '—'} | {process(q)} | {q['topic'].replace('|', '/')} | {q['answer_proposal']} |")
    lines += [
        '',
        '## Montaje por bloques',
        '',
        'Crear una lectura/contexto por cada cambio de nombre en «Lectura compartida». Mantener juntas las preguntas y usar `{{desde}}`/`{{hasta}}` en el encabezado. Aunque se seleccionen solo algunas preguntas originales, conservar el texto o la infografía completos. «Petrícor» y el cómic de «filosofía» necesitan imágenes legibles; no copiar encabezados, marcas ni resaltados del PDF fuente.',
        '',
        'Las primeras cinco coinciden con `planning/SP001_S1_LECTURA_CANDIDATAS_05.md`. El registro global aún contiene solamente las 25 de Matemáticas; actualizarlo cuando estas candidatas estén cargadas y guardadas.',
        '',
        '## Páginas inspeccionadas',
        '',
        '- `USB-04dc5257ed8b`: 8, 9, 10, 12, 15, 16 y 18.',
        '- `USB-a170782eadcb`: 6, 7, 10 y 12.',
        '- `USB-d4e43db6988a`: 10, 11, 18, 19, 22 y 23.',
        '',
        'Los originales están en `E:\\Icfes_SaberPlus\\Revisados - Lote 30\\`. Buscar cada código exacto en `output/cotejo_30/INDICE.html` y revisar sus variantes documentadas antes de reservar.',
    ]
    return '\n'.join(lines) + '\n'


if __name__ == '__main__':
    items, counts = select(json.loads(CATALOG.read_text(encoding='utf-8')))
    OUTPUT.write_text(render(items), encoding='utf-8')
    print(f'41 candidatas: {dict(counts)} · {OUTPUT}')
