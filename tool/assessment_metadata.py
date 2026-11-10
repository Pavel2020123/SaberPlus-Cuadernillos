"""Versioned pedagogical metadata; never converts practice scores to official levels."""
import json
from datetime import date
from pathlib import Path

CATALOG = json.loads(Path(__file__).with_name('assessment_catalog.json').read_text(encoding='utf-8'))
PARTS = {11: 1, 12: 1, 13: 1, 14: 2, 15: 3, 16: 4, 17: 4, 18: 5, 19: 5, 20: 6, 21: 7, 22: 7}


def expected_area(number):
    if number <= 2:
        return 'reading'
    if number <= 4:
        return 'social'
    if number <= 7:
        return 'mathematics'
    if number <= 10:
        return 'science'
    return 'english'


def validate_assessments(bank, questions, area_by_number=None, parts_by_number=None):
    enabled = bank.get('assessment_framework')
    if enabled is None:
        if any('assessment' in q for q in questions):
            raise ValueError('Los metadatos requieren assessment_framework.')
        return  # Legacy banks stay readable, not implicitly classified.
    if enabled != CATALOG['id']:
        raise ValueError('Catálogo de evaluación desconocido.')
    errors = []
    for q in questions:
        a = q.get('assessment')
        prefix = f'Pregunta {q["n"]}'
        if not isinstance(a, dict):
            errors.append(prefix + ': falta assessment.')
            continue
        area_id = area_by_number[q['n']] if area_by_number is not None else expected_area(q['n'])
        if a.get('area') != area_id or a.get('framework') != enabled:
            errors.append(prefix + ': área o versión no corresponde al bloque.')
            continue
        status = a.get('status')
        if status not in ('unclassified', 'proposed', 'reviewed'):
            errors.append(prefix + ': estado de revisión inválido.')
        area = CATALOG['areas'][area_id]
        competency = a.get('competency')
        claim, evidence = a.get('claim'), a.get('evidence')
        process, component, part = a.get('process'), a.get('component'), a.get('part')
        if status == 'unclassified':
            if any(v is not None for v in (competency, claim, evidence, process, component, part)):
                errors.append(prefix + ': sin clasificar no puede tener asignaciones activas.')
            continue
        if competency not in area['competencies']:
            errors.append(prefix + ': competencia ajena al área o inexistente.')
            continue
        if not isinstance(a.get('rationale'), str) or not a['rationale'].strip():
            errors.append(prefix + ': falta justificar la clasificación.')
        if status == 'reviewed':
            if not isinstance(a.get('reviewer'), str) or not a['reviewer'].strip():
                errors.append(prefix + ': una revisión necesita responsable.')
            try:
                date.fromisoformat(a.get('reviewed_at', ''))
            except (TypeError, ValueError):
                errors.append(prefix + ': fecha de revisión inválida; usar AAAA-MM-DD.')
            if area_id != 'english' and evidence is None:
                errors.append(prefix + ': una clasificación revisada requiere evidencia registrada.')
        if area_id == 'english':
            expected_part = parts_by_number.get(q['n']) if parts_by_number is not None else PARTS.get(q['n'])
            if type(part) is not int or part != expected_part:
                errors.append(prefix + ': parte de inglés no corresponde al formato.')
            if claim is not None or evidence is not None or process is not None or component is not None:
                errors.append(prefix + ': inglés no usa el desglose de afirmaciones de otras áreas.')
        else:
            if claim not in area['competencies'][competency]['claims']:
                errors.append(prefix + ': afirmación no pertenece a la competencia.')
            elif evidence is not None and evidence not in area['claims'][claim]['evidence']:
                errors.append(prefix + ': evidencia no registrada para esa afirmación.')
            if area_id == 'reading':
                if process not in area['processes'] or area['processes'][process]['claim'] != claim:
                    errors.append(prefix + ': proceso de lectura y afirmación incompatibles.')
            elif process is not None:
                errors.append(prefix + ': proceso de lectura fuera de lectura.')
            if area_id == 'science':
                if component not in area['components']:
                    errors.append(prefix + ': falta componente válido de ciencias.')
            elif component is not None:
                errors.append(prefix + ': componente de ciencias fuera de ciencias.')
            if part is not None:
                errors.append(prefix + ': parte de inglés fuera de inglés.')
    if errors:
        raise ValueError('Clasificación de evaluación inválida:\n' + '\n'.join(errors))


def append_teacher_pages(book, bank, questions):
    if bank.get('assessment_framework') is None:
        return
    from generate_booklet_template import W, M
    counts = {s: sum(q['assessment']['status'] == s for q in questions)
              for s in ('unclassified', 'proposed', 'reviewed')}
    for start in range(0, len(questions), 8):
        y = book.start('Clasificación pedagógica - revisión')
        y = book.p(f'Sin clasificar: {counts["unclassified"]}. Propuestas: {counts["proposed"]}. '
                   f'Revisadas: {counts["reviewed"]}. No es un informe de resultados del estudiante.', y, size=9)
        y = book.p('Fuente: guía Saber 11 2026-2. Competencias y afirmaciones no equivalen a niveles '
                   'de desempeño. Las propuestas necesitan revisión docente.', y, size=9)
        rows = [['N.º', 'Área', 'Clasificación', 'Estado']]
        for q in questions[start:start+8]:
            a = q['assessment']
            area = CATALOG['areas'][a['area']]
            description = 'Pendiente de clasificación docente.'
            if a['status'] != 'unclassified':
                description = area['competencies'][a['competency']]['label']
                if a.get('process'):
                    description += '. Proceso: ' + area['processes'][a['process']]['label']
                if a.get('claim'):
                    description += '. Afirmación ' + a['claim']
                if a.get('evidence'):
                    description += '; evidencia ' + a['evidence']
                if a.get('part'):
                    description += f'. Parte {a["part"]}: ' + area['parts'][str(a['part'])]
                description += '. Motivo: ' + a['rationale']
            label = {'unclassified': 'Sin clasificar', 'proposed': 'Propuesta', 'reviewed': 'Revisada'}[a['status']]
            rows.append([q['n'], area['label'], description, label])
        book.table(rows, y, [30, 75, W-2*M-175, 70])
