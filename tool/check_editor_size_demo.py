"""HTTP smoke checks restricted to the isolated SP-IMG-01 demo on port 4186.

Does not automate a browser or open the normal saved project.
"""
import base64
import copy
import io
import json
from urllib.error import HTTPError
from urllib.request import Request, urlopen

import pymupdf
from PIL import Image
from editor_model import ROOT
from editor_pdf import picture, CW
from make_editor_size_demo import DEFAULT_OUT


def check():
    url = 'http://127.0.0.1:4186'
    with urlopen(url+'/') as response:
        assert response.status == 200
    with urlopen(url+'/api/bootstrap') as response:
        bootstrap = json.load(response)
    project = bootstrap['project']
    assert project['code'] == 'SP-IMG-01', 'No es la instancia de prueba: no se escribira nada.'
    assert {q['id'] for q in project['questions']} == {'q-size-1', 'q-size-2', 'q-size-3'}
    project = copy.deepcopy(project)
    revision = project['revision']

    def post(route, payload, expected_status=200):
        request = Request(url+'/api/'+route, data=json.dumps(payload).encode(),
                          headers={'Content-Type': 'application/json',
                                   'X-Local-Token': bootstrap['token']})
        try:
            response = urlopen(request)
        except HTTPError as error:
            with error:
                body = json.load(error)
                assert error.code == expected_status, body
                return body
        with response:
            assert response.status == expected_status
            return json.load(response)

    images = []
    for question in project['questions']:
        raw = (ROOT/question['image']).read_bytes()
        with Image.open(io.BytesIO(raw)) as source:
            original_size = source.size
        uploaded = post('upload', {'data': base64.b64encode(raw).decode()})['path']
        question['image'] = uploaded
        with Image.open(ROOT/uploaded) as stored:
            assert stored.size == original_size
        fitted = picture(uploaded, CW-18)
        assert abs(fitted.drawWidth/fitted.drawHeight-original_size[0]/original_size[1]) < 1e-9
        images.append({'pixels': list(original_size), 'pdf_points': [fitted.drawWidth, fitted.drawHeight]})
    post('upload', {'data': base64.b64encode(b'not an image').decode()}, 400)
    preview = post('preview', {'project': project})
    assert len(set(preview['page_map'].values())) == 1
    with urlopen(url+f'/previews/{preview["id"]}/{preview["page_map"]["q-size-1"]}.png') as response:
        assert response.read().startswith(b'\x89PNG')
    saved = post('save', {'project': project, 'revision': revision})['project']
    post('save', {'project': project, 'revision': revision}, 409)
    result = post('generate', {'revision': saved['revision']})
    documents = {}
    for name in ('student', 'solved', 'teacher'):
        with urlopen(url+result[name]) as response:
            raw = response.read()
        assert raw.startswith(b'%PDF')
        documents[name] = pymupdf.open(stream=raw, filetype='pdf')
    try:
        student_text = ''.join(page.get_text() for page in documents['student'])
        assert all(q['explanation'] not in student_text for q in project['questions'])
        assert 'RESPUESTAS EXPLICADAS' not in student_text
        solved_text = ''.join(page.get_text() for page in documents['solved'])
        assert all(q['explanation'] in solved_text for q in project['questions'])
        marked = [page.get_textbox(shape['rect']).strip()
                  for page in documents['teacher'] for shape in page.get_drawings()
                  if shape.get('fill') and max(shape['fill']) < .5
                  and 12 <= shape['rect'].width <= 14 and 12 <= shape['rect'].height <= 14]
        assert marked == ['A', 'C', 'B'], marked
        report = {'method': 'HTTP local; no equivale a una prueba interactiva en navegador',
                  'images': images, 'available_outputs': list(documents),
                  'pages': {name: len(doc) for name, doc in documents.items()},
                  'teacher_answers': marked, 'invalid_image_rejected': True,
                  'stale_save_rejected': True, 'preview_png_ok': True}
    finally:
        for doc in documents.values():
            doc.close()
    (DEFAULT_OUT/'comprobacion_http.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(report, ensure_ascii=True, indent=2))


if __name__ == '__main__':
    check()
