"""Original one-page layout exercise, isolated from the user's saved project."""
import hashlib
import json
from pathlib import Path

import pymupdf
from reportlab.pdfgen import canvas
from reportlab.lib import colors

from editor_model import new_project, blank_assessment, validate_project
from editor_pdf import generate

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'output' / 'pdf'
TMP = ROOT / 'tmp' / 'pdfs' / 'pagina_prueba_20261031'


def main():
    TMP.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    saved = ROOT / 'data' / 'project.json'
    before = saved.read_bytes()
    # Own diagram: labelled bars keep the information usable in grayscale.
    chart = TMP / 'grafica_original.pdf'
    c = canvas.Canvas(str(chart), pagesize=(1000, 270))
    c.setFillColor(colors.white)
    c.rect(0, 0, 1000, 270, fill=1, stroke=0)
    c.setStrokeColor(colors.HexColor('#d9dde1'))
    for value in (0, 20, 40, 60):
        y = 46+value*2.6
        c.line(90, y, 960, y)
        c.setFillColor(colors.HexColor('#48515a'))
        c.setFont('Helvetica', 16)
        c.drawRightString(76, y-5, str(value))
    c.setFont('Helvetica', 17)
    c.drawString(26, 244, 'Entradas vendidas')
    for x, day, value in zip((200, 410, 620, 830), ('Lunes', 'Martes', 'Miércoles', 'Jueves'), (40, 55, 45, 60)):
        height = value*2.6
        c.setFillColor(colors.HexColor('#74808b'))
        c.roundRect(x-42, 46, 84, height, 3, fill=1, stroke=0)
        c.setFillColor(colors.HexColor('#17263a'))
        c.setFont('Helvetica-Bold', 19)
        c.drawCentredString(x, 54+height, str(value))
        c.setFont('Helvetica', 17)
        c.drawCentredString(x, 20, day)
    c.save()
    with pymupdf.open(chart) as doc:
        png = doc[0].get_pixmap(matrix=pymupdf.Matrix(1.3, 1.3), alpha=False).tobytes('png')
    asset = ROOT / 'assets' / 'uploads' / (hashlib.md5(png).hexdigest()+'.png')
    asset.parent.mkdir(parents=True, exist_ok=True)
    if not asset.exists():
        asset.write_bytes(png)
    p = new_project()
    p['area_headers'] = {'mathematics': {'title': 'MATEMÁTICAS', 'instructions': ''}}
    p['contexts'] = [{
        'id': 'ctx-feria-demo-20261031', 'area': 'mathematics',
        'range_heading': 'RESPONDA LAS PREGUNTAS {{desde}} A {{hasta}} DE ACUERDO CON LA SIGUIENTE INFORMACIÓN',
        'title': 'Una feria para compartir historias',
        'text': 'Un colegio organizó una feria de lectura. La gráfica muestra las entradas vendidas durante cuatro días. Cada entrada costó $4.000 y no hubo descuentos.',
        'image': asset.relative_to(ROOT).as_posix(),
        'source': 'Elaboración original SaberPlus. Datos ficticios para esta prueba de diseño.'}]
    questions = [
        ('¿En qué día se vendieron más entradas?', ['Lunes.', 'Martes.', 'Miércoles.', 'Jueves.'], 'D',
         'Jueves registra 60 entradas, más que lunes (40), martes (55) y miércoles (45).', 'interpretation', 'Lectura de gráficas'),
        ('¿Cuántas entradas se vendieron en total durante los cuatro días?', ['145 entradas.', '155 entradas.', '200 entradas.', '220 entradas.'], 'C',
         'Se suman los cuatro registros: 40 + 55 + 45 + 60 = 200 entradas.', 'execution', 'Operaciones con datos'),
        ('¿Qué porcentaje del total de entradas se vendió el jueves?', ['20 %.', '25 %.', '30 %.', '60 %.'], 'C',
         'El total es 200. Las 60 entradas del jueves representan 60/200 × 100 = 30 %.', 'execution', 'Porcentajes'),
        ('¿Cuánto dinero se recaudó por la venta de entradas durante los cuatro días?', ['$200.000.', '$800.000.', '$600.000.', '$240.000.'], 'B',
         'Se vendieron 200 entradas a $4.000: 200 × 4.000 = $800.000.', 'execution', 'Cálculo de ingresos'),
        ('Una estudiante afirma: «El promedio fue de 50 entradas diarias; por eso, cada día se vendieron 50». ¿Es correcta su conclusión?',
         ['No; el promedio no exige que los cuatro registros sean iguales.', 'Sí; un promedio siempre coincide con cada registro.', 'Sí; la gráfica muestra 50 entradas en los cuatro días.', 'No; para calcular un promedio se usa solo el mayor registro.'], 'A',
         'El promedio es 200/4 = 50, pero los registros son 40, 55, 45 y 60. La media no implica igualdad de los datos.', 'argumentation', 'Interpretación del promedio'),
        ('Si el lunes se hubieran vendido un 25 % más de entradas, ¿cuántas entradas se habrían vendido ese día?',
         ['10 entradas.', '45 entradas.', '65 entradas.', '50 entradas.'], 'D',
         'El 25 % de 40 es 10. El nuevo total sería 40 + 10 = 50 entradas.', 'execution', 'Incrementos porcentuales'),
    ]
    # Keep readable type and the argumentation item; the sixth item would spill.
    questions = questions[:5]
    for n, (stem, options, key, reason, competency, topic) in enumerate(questions, 1):
        assessment = blank_assessment('mathematics')
        assessment.update(status='proposed', competency=competency,
                          claim={'interpretation': '1', 'execution': '2', 'argumentation': '3'}[competency],
                          rationale='Propuesta original para revisar el diseño; clasificación pendiente de revisión docente.')
        p['questions'].append({'id': f'q-feria-demo-{n}', 'area': 'mathematics', 'part': 0, 'order': n,
                               'topic': topic, 'subtopic': '', 'stem': stem,
                               'options': [{'text': text} for text in options], 'correct': key,
                               'explanation': reason, 'layout': 'columns', 'included': True,
                               'context': p['contexts'][0]['id'], 'slot': '', 'assessment': assessment})
    validate_project(p, exporting=True)
    result = generate(p, TMP / 'render', preview=True)
    content_pages = sorted(set(result['page_map'].values()))
    if len(content_pages) != 1:
        raise ValueError(f'Demo must fit exactly one content page, got {content_pages}')
    target = OUT / 'SaberPlus_prueba_una_pagina_SP-001.pdf'
    with pymupdf.open(TMP/'render'/'cuadernillo.pdf') as source:
        page_number = content_pages[0]-1
        with pymupdf.open() as out:
            out.insert_pdf(source, from_page=page_number, to_page=page_number)
            out.set_metadata({'title': 'SaberPlus SP-001 · Prueba de una página', 'author': 'SaberPlus',
                              'subject': 'Contenido original de demostración; no es una prueba oficial ni un simulacro completo.'})
            out.save(target)
    with pymupdf.open(target) as doc:
        assert len(doc) == 1
        text = doc[0].get_text()
        assert 'RESPUESTAS EXPLICADAS' not in text
        assert all(q['stem'][:20] in text.replace('\n', ' ') for q in p['questions'])
        assert all(36 <= block[0] < block[2] <= doc[0].rect.width-30 for block in doc[0].get_text('blocks'))
        doc[0].get_pixmap(matrix=pymupdf.Matrix(1.6, 1.6), alpha=False).save(TMP/'pagina.png')
    (OUT/'SaberPlus_prueba_una_pagina_SP-001.proyecto.json').write_text(json.dumps(p, ensure_ascii=False, indent=2), encoding='utf-8')
    (OUT/'SaberPlus_prueba_una_pagina_SP-001.clave.json').write_text(json.dumps([
        {'number': n, 'correct': q['correct'], 'explanation': q['explanation'], 'assessment': q['assessment']}
        for n, q in enumerate(p['questions'], 1)], ensure_ascii=False, indent=2), encoding='utf-8')
    assert saved.read_bytes() == before, 'User saved project must not change'
    print(json.dumps({'pdf': str(target), 'page_count': 1, 'questions': len(p['questions']),
                      'original_content': True, 'saved_project_unchanged': True, 'warnings': result['warnings']}, ensure_ascii=True))


if __name__ == '__main__':
    main()
