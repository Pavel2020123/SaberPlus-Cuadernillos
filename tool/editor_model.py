"""Independent local editorial project, not student or official-result storage."""
import copy
import json
import re
from pathlib import Path
from assessment_metadata import CATALOG, validate_assessments

ROOT = Path(__file__).resolve().parents[1]
AREAS = {key: item['label'] for key, item in CATALOG['areas'].items()}
SESSIONS = {'first': ['mathematics', 'reading', 'social', 'science'],
            'second': ['social', 'mathematics', 'science', 'english']}
ID = re.compile(r'^[A-Za-z0-9_-]{1,80}$')
DEFAULT_RANGE_HEADING = 'RESPONDA LAS PREGUNTAS {{desde}} A {{hasta}} DE ACUERDO CON LA SIGUIENTE INFORMACIÓN'


def range_heading(template, first, last):
    """Resolve actual selected numbers, never numbers manually stored on an item."""
    if not template or not template.strip():
        template = (DEFAULT_RANGE_HEADING if first != last else
                    'RESPONDA LA PREGUNTA {{desde}} DE ACUERDO CON LA SIGUIENTE INFORMACIÓN')
    for key, value in {'desde': first, 'hasta': last, 'cantidad': last-first+1}.items():
        template = template.replace('{{'+key+'}}', str(value))
    return template


def new_project():
    return {'schema': 1, 'revision': 0, 'code': 'SP-001', 'session': 'first', 'time': '',
            'targets': {key: None for key in AREAS}, 'area_headers': {}, 'contexts': [], 'questions': []}


def blank_assessment(area):
    return {'framework': CATALOG['id'], 'area': area, 'status': 'unclassified',
            'competency': None, 'process': None, 'claim': None, 'evidence': None,
            'component': None, 'part': None, 'rationale': '', 'reviewer': None, 'reviewed_at': None}


def selected_questions(project):
    result = []
    # Groups stay contiguous; area/English-part ordering is never randomized.
    for area in SESSIONS[project['session']]:
        items = [q for q in project['questions'] if q['area'] == area and q.get('included', True)]
        items.sort(key=lambda q: (q.get('part', 0) if area == 'english' else 0, q.get('order', 0)))
        groups = {}
        for q in items:
            groups.setdefault(q.get('context') or q['id'], []).append(q)
        for group in groups.values():
            result.extend(group)
    return result


def validate_project(project, exporting=False):
    if isinstance(project,dict) and project.get('column_flow','sequential') not in ('sequential','balanced','adaptive'):
        raise ValueError('Modo de columnas desconocido.')
    if not isinstance(project, dict) or project.get('schema') != 1:
        raise ValueError('Formato de proyecto desconocido.')
    if project.get('session') not in SESSIONS:
        raise ValueError('Selecciona primera o segunda sesión.')
    headers = project.get('area_headers', {})
    if not isinstance(headers, dict) or any(key not in AREAS for key in headers):
        raise ValueError('Los encabezados deben pertenecer a áreas conocidas.')
    for header in headers.values():
        if not isinstance(header, dict):
            raise ValueError('Encabezado de área inválido.')
        for key, limit in [('title',120),('instructions',1500)]:
            value = header.get(key, '')
            if not isinstance(value, str) or len(value)>limit:
                raise ValueError(f'Encabezado: {key} debe ser texto de hasta {limit} caracteres.')
    if not re.fullmatch(r'[A-Za-z0-9_-]{1,32}', str(project.get('code', ''))):
        raise ValueError('El código admite letras, números y guiones, hasta 32 caracteres.')
    if not isinstance(project.get('targets'), dict):
        raise ValueError('Faltan las cantidades previstas.')
    for area in AREAS:
        value = project['targets'].get(area)
        if value is not None and (type(value) is not int or not 0 <= value <= 300):
            raise ValueError('La cantidad prevista debe ser un entero entre 0 y 300 o quedar vacía.')
    contexts, questions = project.get('contexts'), project.get('questions')
    if not isinstance(contexts, list) or not isinstance(questions, list) or len(questions) > 500:
        raise ValueError('Se admiten hasta 500 preguntas en el banco local.')
    ids = set()
    for item in contexts + questions:
        if not isinstance(item, dict) or not ID.fullmatch(str(item.get('id', ''))) or item['id'] in ids:
            raise ValueError('Hay identificadores ausentes, inválidos o repetidos.')
        ids.add(item['id'])
        if item.get('area') not in AREAS:
            raise ValueError('Área desconocida.')
        for key, value in item.items():
            if isinstance(value, str) and len(value) > 30000:
                raise ValueError(f'El campo {key} es demasiado extenso.')
        options = item.get('options', [])
        if not isinstance(options, list):
            raise ValueError('Las opciones deben ser una lista.')
        for image in [item.get('image')] + [o.get('image') for o in options if isinstance(o, dict)]:
            if image and not re.fullmatch(r'assets/uploads/[a-f0-9]{32}\.(png|jpg|webp)', image):
                raise ValueError('Usa una imagen cargada desde el editor.')
    by_id = {ctx['id']: ctx for ctx in contexts}
    for ctx in contexts:
        if ctx.get('layout', 'full') not in ('full', 'side_by_side'):
            raise ValueError('Distribución de lectura compartida desconocida.')
        if ctx.get('layout') == 'side_by_side' and ctx['area'] == 'english':
            raise ValueError('La lectura en columna izquierda no se aplica a Inglés.')
        heading = ctx.get('range_heading', '')
        if not isinstance(heading, str) or len(heading)>600:
            raise ValueError('La indicación del grupo admite hasta 600 caracteres.')
        unknown = set(re.findall(r'\{\{([^{}]+)\}\}', heading))-{'desde','hasta','cantidad'}
        if unknown:
            raise ValueError('En la indicación usa solo {{desde}}, {{hasta}} o {{cantidad}}. Los huecos {{h1}} pertenecen al texto.')
        if not isinstance(ctx.get('source',''), str) or len(ctx.get('source',''))>1500:
            raise ValueError('La fuente del contexto admite hasta 1500 caracteres.')
        if ctx.get('notice_layout'):
            if ctx['area']!='english' or ctx.get('part')!=2 or ctx['notice_layout']!='paired':
                raise ValueError('La composición de avisos corresponde a Inglés, parte 2.')
            choices=ctx.get('example_options',[])
            if (not isinstance(ctx.get('example_notice'),str) or not ctx['example_notice'].strip()
                    or not isinstance(choices,list) or len(choices)!=3
                    or any(not isinstance(value,str) or not value.strip() for value in choices)
                    or ctx.get('example_answer') not in ('A','B','C')):
                raise ValueError('El ejemplo de avisos necesita su texto, tres opciones y una clave A-C.')
        if ctx.get('dialogue_layout'):
            if ctx['area']!='english' or ctx.get('part')!=3 or ctx['dialogue_layout']!='paired':
                raise ValueError('La composición de conversaciones corresponde a Inglés, parte 3.')
    for q in questions:
        catalog_id = q.get('catalog_id', '')
        if catalog_id is None:
            catalog_id = ''
        if not isinstance(catalog_id, str) or (catalog_id and not re.fullmatch(r'USB-[a-f0-9]{12}-Q[0-9]{3}(?:\.[1-9][0-9]*)?', catalog_id)):
            raise ValueError(f'Pregunta {q["id"]}: el código de catálogo debe tener formato USB-xxxxxxxxxxxx-Q001, con sufijo opcional de examen como .1 o .2.')
        if q.get('options_layout','vertical') not in ('vertical','grid2'):
            raise ValueError('Distribución de opciones desconocida.')
        if 'page_break_before' in q and type(q['page_break_before']) is not bool:
            raise ValueError('El salto de página debe ser una casilla activada o desactivada.')
        if 'column_break_before' in q and type(q['column_break_before']) is not bool:
            raise ValueError('El salto de columna debe ser una casilla activada o desactivada.')
        if q.get('column_break_before') and q.get('layout')=='full':
            raise ValueError('El salto a columna derecha requiere una pregunta en dos columnas.')
        if 'image_width' in q and (type(q['image_width']) not in (int,float) or not 40 <= q['image_width'] <= 500):
            raise ValueError('El ancho máximo de imagen debe estar entre 40 y 500 puntos.')
        if 'image_height' in q and (type(q['image_height']) not in (int,float) or not 40 <= q['image_height'] <= 240):
            raise ValueError('La altura máxima de imagen debe estar entre 40 y 240 puntos.')
        if 'option_image_height' in q and (type(q['option_image_height']) not in (int,float) or not 40 <= q['option_image_height'] <= 240):
            raise ValueError('El alto máximo de las imágenes de las opciones debe estar entre 40 y 240 puntos.')
        if type(q.get('order', 0)) is not int or q.get('order', 0) < 0:
            raise ValueError(f'Pregunta {q["id"]}: el orden debe ser un entero no negativo.')
        for field in ('topic', 'subtopic', 'introduction'):
            if not isinstance(q.get(field, ''), str):
                raise ValueError(f'Pregunta {q["id"]}: {field} debe ser texto.')
        ctx = by_id.get(q.get('context'))
        if ctx and ctx.get('layout') == 'side_by_side' and q.get('layout') == 'full':
            raise ValueError('Las preguntas junto a una lectura deben usar distribución en columnas.')
        if q.get('context') and (not ctx or ctx['area'] != q['area']):
            raise ValueError('El contexto debe existir y pertenecer al área de la pregunta.')
        if q.get('layout') not in ('columns', 'boxed', 'full'):
            raise ValueError('Distribución de pregunta desconocida.')
        if q['area'] == 'english' and (type(q.get('part')) is not int or not 1 <= q['part'] <= 7):
            raise ValueError('Inglés necesita una parte entre 1 y 7.')
        if ctx and q['area'] == 'english' and ctx.get('part') != q['part']:
            raise ValueError('La parte de inglés debe coincidir con el contexto.')
        if not isinstance(q.get('options'), list) or any(not isinstance(o, dict) for o in q['options']):
            raise ValueError('Las opciones deben ser objetos de texto e imagen.')
    # Validate actual area/part instead of assuming numbers from the old sample.
    mapped = []
    for n, q in enumerate(questions, 1):
        item = copy.deepcopy(q)
        item['n'] = n
        mapped.append(item)
    validate_assessments({'assessment_framework': CATALOG['id']}, mapped,
                         {i+1: q['area'] for i, q in enumerate(questions)},
                         {i+1: q.get('part') for i, q in enumerate(questions)})
    active = selected_questions(project)
    warnings = []
    orders = set()
    for q in active:
        key = (q['area'], q.get('part', 0) if q['area'] == 'english' else 0, q.get('order', 0))
        if key in orders:
            message = f'Pregunta {q["id"]}: orden repetido dentro del área / parte. Asigna un orden distinto.'
            if exporting:
                raise ValueError(message)
            warnings.append(message)
        orders.add(key)
        missing = [label for field, label in [('topic', 'tema'), ('subtopic', 'subtema')]
                   if not q.get(field, '').strip()]
        if missing:
            warnings.append(f'Pregunta {q["id"]}: falta {" y ".join(missing)}; clasificación temática pendiente.')
    for area in SESSIONS[project['session']]:
        count = sum(q['area'] == area for q in active)
        target = project['targets'].get(area)
        if not count:
            warnings.append(f'{AREAS[area]}: todavía no hay preguntas seleccionadas.')
        if target is not None and target != count:
            warnings.append(f'{AREAS[area]}: seleccionadas {count}; previstas {target}.')
    if not project.get('time'):
        warnings.append('Tiempo de aplicación sin configurar.')
    if any(q['assessment']['status'] == 'unclassified' for q in active):
        warnings.append('Hay preguntas sin clasificación por competencia.')
    if exporting:
        if not active:
            raise ValueError('Selecciona al menos una pregunta de esta sesión.')
        for q in active:
            title = f'Pregunta {q["id"]}'
            if not q.get('stem', '').strip():
                raise ValueError(title + ': falta el enunciado.')
            matching = q['area'] == 'english' and q['part'] == 1
            ctx = by_id.get(q.get('context'))
            if matching:
                words = ctx.get('words', []) if ctx else []
                if len(words) != 7 or any(not str(w).strip() for w in words) or len(set(words)) != 7:
                    raise ValueError(title + ': vocabulario requiere contexto con siete palabras A-G distintas.')
                letters = 'ABCDEFG'
            else:
                count = 3 if q['area'] == 'english' and q['part'] in (2, 3, 4, 5) else 4
                if len(q['options']) != count or any(not o.get('text', '').strip() and not o.get('image') for o in q['options']):
                    raise ValueError(title + f': completa sus {count} opciones con texto o imagen.')
                letters = 'ABCD'[:count]
            if not isinstance(q.get('correct'),str) or len(q['correct'])!=1 or q['correct'] not in letters:
                raise ValueError(title + ': selecciona una clave válida.')
            if not q.get('explanation', '').strip():
                raise ValueError(title + ': falta la explicación para el docente.')
            if q['area'] == 'english' and q['part'] in (4, 5, 6, 7) and not ctx:
                raise ValueError(title + ': esta parte necesita un contexto compartido.')
            if q['area'] == 'english' and q['part'] in (4, 7):
                slot = q.get('slot', '')
                if not re.fullmatch(r'[A-Za-z0-9_-]{1,20}', slot) or ctx['text'].count('{{'+slot+'}}') != 1:
                    raise ValueError(title + ': el hueco debe aparecer exactamente una vez en el contexto, por ejemplo {{h1}}.')
        for ctx in contexts:
            members = [q for q in active if q.get('context') == ctx['id']]
            if ctx.get('part') in (4, 7) and members:
                slots = [q.get('slot') for q in members]
                if len(slots) != len(set(slots)):
                    raise ValueError('Dos preguntas usan el mismo hueco del contexto.')
                if set(re.findall(r'\{\{([^{}]+)\}\}', ctx.get('text', ''))) != set(slots):
                    raise ValueError('Hay huecos sin pregunta seleccionada o preguntas sin hueco en un contexto.')
    return warnings


def demo_project():
    """Import original demonstration items without student/result data."""
    old = json.loads((ROOT/'tool/booklet_competency_sample.json').read_text(encoding='utf-8'))
    p = new_project()
    from generate_booklet_template import all_questions
    contexts = [
        {'id': 'ctx-reading', 'area': 'reading', 'title': old['reading']['title'], 'text': old['reading']['text']},
        {'id': 'ctx-table', 'area': 'mathematics', 'title': 'Préstamos de libros', 'table': 'Día;Lunes;Martes;Miércoles;Jueves\nPréstamos;20;30;10;40'},
        {'id': 'ctx-en-2', 'area': 'english', 'part': 2, 'title': 'Notice', 'text': 'PLEASE RETURN BOOKS TO THE DESK AFTER USE'},
    ]
    e = old['english']
    for part, key, title in [(1, None, 'School'), (4, 'grammarText', 'A class garden'),
                              (5, 'literalText', 'Reading club'), (6, 'inferenceText', 'Messages and study'),
                              (7, 'lexicalText', 'Seed exchange')]:
        text = e.get(key, '') if key else ''
        text = re.sub(r'\((\d+)\)\s*\{\{\1\}\}', lambda m: '{{h'+m[1]+'}}', text)
        contexts.append({'id': f'ctx-en-{part}', 'area': 'english', 'part': part, 'title': title,
                         'text': text, 'words': e['words'] if part == 1 else [], 'instructions': ''})
    for q in all_questions(old):
        a = copy.deepcopy(q['assessment'])
        part = a.get('part') or (1 if 11 <= q['n'] <= 13 else 0)
        context = 'ctx-reading' if q['n'] <= 2 else 'ctx-table' if q['n'] == 5 else f'ctx-en-{part}' if part in (1,2,4,5,6,7) else None
        stem = q['stem']
        if a['area'] == 'english' and part in (4, 7):
            stem = re.sub(r'\bspace\s+\d+', 'space {{numero}}', stem)
        p['questions'].append({'id': f'q-demo-{q["n"]}', 'area': a['area'], 'part': part,
                              'order': q['n'], 'topic': q['topic'], 'subtopic': '', 'stem': stem,
                              'options': [{'text': t} for t in q.get('options', [])], 'correct': q['answer'],
                              'explanation': q['why'], 'layout': 'boxed' if q['n'] % 2 else 'columns',
                              'included': True, 'context': context, 'slot': f'h{q["n"]}', 'assessment': a})
    p['contexts'] = contexts
    return p
