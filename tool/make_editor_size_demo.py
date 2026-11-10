"""Original three-question image-sizing demo; never opens the normal saved project.

Creates full outputs plus a three-page comparison of their relevant pages.
--serve uses a separate state file on loopback, not data/project.json.
"""
import argparse
import json
import uuid
from pathlib import Path

import pymupdf
from PIL import Image, ImageDraw, ImageFont

from editor_model import ROOT, new_project, blank_assessment
from editor_pdf import generate, picture, CW

DEFAULT_OUT = ROOT/'tmp/pdfs/tamanos-imagenes-20261110'


def font(size):
    path = Path('C:/Windows/Fonts/arial.ttf')
    return ImageFont.truetype(str(path), size) if path.exists() else ImageFont.load_default(size=size)


def make_images():
    """Draw new original educational diagrams, not edited third-party pictures."""
    uploads = ROOT/'assets/uploads'
    uploads.mkdir(parents=True, exist_ok=True)
    results = []
    for kind, size in [('horizontal', (1200, 320)), ('cuadrada', (600, 600)), ('vertical', (360, 1000))]:
        image = Image.new('RGB', size, 'white')
        draw = ImageDraw.Draw(image)
        if kind == 'horizontal':
            draw.text((30, 18), 'Estudiantes por grupo', font=font(54), fill='black')
            draw.text((30, 115), 'A', font=font(54), fill='black')
            draw.text((30, 220), 'B', font=font(54), fill='black')
            draw.rectangle((110, 110, 710, 180), fill='#c1c7ce', outline='black', width=4)
            draw.rectangle((110, 215, 1010, 285), fill='#c1c7ce', outline='black', width=4)
            draw.text((735, 115), '20', font=font(54), fill='black')
            draw.text((1030, 220), '30', font=font(54), fill='black')
        elif kind == 'cuadrada':
            draw.rectangle((115, 180, 475, 420), fill='#e6e8eb', outline='black', width=5)
            draw.text((225, 95), '6 cm', font=font(48), fill='black')
            draw.text((35, 265), '4', font=font(48), fill='black')
            draw.text((20, 320), 'cm', font=font(38), fill='black')
            draw.text((125, 465), 'No esta a escala', font=font(34), fill='black')
        else:
            draw.text((42, 25), 'Nivel del agua', font=font(36), fill='black')
            draw.rectangle((170, 140, 275, 900), fill='white', outline='black', width=5)
            draw.rectangle((174, 444, 271, 896), fill='#c1c7ce')
            for value in range(0, 101, 20):
                y = 900-value*7.6
                draw.line((142, y, 290, y), fill='black', width=4)
                draw.text((35, y-24), str(value), font=font(45), fill='black')
            draw.text((80, 935), 'Litros', font=font(40), fill='black')
        relative = 'assets/uploads/'+uuid.uuid4().hex+'.png'
        image.save(ROOT/relative)
        results.append({'kind': kind, 'size': list(size), 'image': relative,
                        'source': 'Diagrama original SaberPlus para prueba editorial; no validado.'})
    return results


def make_project(images):
    project = new_project()
    project.update(code='SP-IMG-01', time='15 minutos')
    project['targets']['mathematics'] = 3
    samples = [
        ('Lectura de graficas', 'Suma de frecuencias',
         'La grafica muestra los estudiantes de dos grupos. ¿Cuantos estudiantes hay en total?',
         ['50', '10', '30', '60'], 'A', 'Se suman 20 y 30: en total hay 50 estudiantes.'),
        ('Medicion', 'Area de rectangulos',
         'El rectangulo tiene las medidas indicadas. ¿Cual es su area?',
         ['20 cm2', '10 cm2', '24 cm2', '48 cm2'], 'C', 'El area es base por altura: 6 por 4 = 24 cm2.'),
        ('Lectura de escalas', 'Interpretacion de niveles',
         'Observa el nivel sombreado del recipiente. ¿Cuantos litros contiene?',
         ['40 litros', '60 litros', '80 litros', '100 litros'], 'B',
         'La parte sombreada alcanza la marca de 60 litros.'),
    ]
    for index, (topic, subtopic, stem, options, correct, explanation) in enumerate(samples):
        project['questions'].append({
            'id': 'q-size-'+str(index+1), 'area': 'mathematics', 'part': 0, 'order': index+1,
            'topic': topic, 'subtopic': subtopic, 'stem': stem,
            'options': [{'text': value} for value in options], 'correct': correct,
            'explanation': explanation, 'layout': 'columns' if index != 1 else 'boxed',
            'included': True, 'context': None, 'image': images[index]['image'],
            'assessment': blank_assessment('mathematics'),
        })
    return project


def build(out):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    snapshot = out/'proyecto.json'
    manifest = out/'imagenes_prueba.json'
    if snapshot.exists() and manifest.exists():
        # Reuse only this demo's snapshot; the live QA state is kept separately.
        project = json.loads(snapshot.read_text(encoding='utf-8'))
        images = json.loads(manifest.read_text(encoding='utf-8'))
    elif snapshot.exists() or manifest.exists():
        raise ValueError('La carpeta de prueba esta incompleta. Elige otra con --output.')
    else:
        images = make_images()
        project = make_project(images)
        manifest.write_text(json.dumps(images, ensure_ascii=False, indent=2), encoding='utf-8')
    result = generate(project, out)
    pages = set(result['page_map'].values())
    if len(pages) != 1:
        raise ValueError('La comparacion requiere que las tres preguntas quepan en una pagina.')
    question_page = next(iter(pages))-1
    comparison = pymupdf.open()
    files = [('cuadernillo.pdf', question_page, 'muestra_estudiante.pdf'),
             ('cuadernillo_resuelto.pdf', question_page, 'muestra_resuelto.pdf'),
             ('clave_docente.pdf', 0, 'muestra_clave_docente.pdf')]
    for name, page, excerpt in files:
        with pymupdf.open(out/name) as original, pymupdf.open() as extract:
            extract.insert_pdf(original, from_page=page, to_page=page)
            extract.set_metadata({'title': 'SaberPlus - Extracto de prueba de imagenes'})
            extract.save(out/excerpt)
            comparison.insert_pdf(extract)
    comparison.set_metadata({'title': 'SaberPlus - Comparacion de tres salidas'})
    comparison.save(out/'comparacion_tres_paginas.pdf')
    comparison.close()
    for name in ['comparacion_tres_paginas', 'cuadernillo_resuelto']:
        with pymupdf.open(out/(name+'.pdf')) as doc:
            for index, page in enumerate(doc):
                page.get_pixmap(matrix=pymupdf.Matrix(1.5, 1.5), alpha=False).save(out/f'{name}-{index+1}.png')
    for item in images:
        scaled = picture(item['image'], CW-18)
        ratio = item['size'][0]/item['size'][1]
        assert abs(scaled.drawWidth/scaled.drawHeight-ratio) < 1e-9
        assert scaled.drawWidth <= CW-18 and scaled.drawHeight <= 190
    print('Tres proporciones conservadas; comparacion de 3 paginas: '+str(out/'comparacion_tres_paginas.pdf'), flush=True)
    return project


def serve(project, out, port):
    import editor_server as server
    data = Path(out)/'datos_editor_prueba'
    data.mkdir(exist_ok=True)
    server.DATA, server.STATE = data, data/'project.json'
    if not server.STATE.exists():
        server.STATE.write_text(json.dumps(project, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'Editor con datos de prueba separados: http://127.0.0.1:{port}', flush=True)
    server.ThreadingHTTPServer(('127.0.0.1', port), server.Handler).serve_forever()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=DEFAULT_OUT)
    parser.add_argument('--serve', action='store_true')
    parser.add_argument('--port', type=int, default=4186)
    args = parser.parse_args()
    demo = build(args.output)
    if args.serve:
        serve(demo, args.output, args.port)
