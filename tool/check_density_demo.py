"""Generate isolated proof from saved content, never change the editor state."""
import json
import argparse
from pathlib import Path
import pymupdf
from editor_model import ROOT
from editor_pdf import generate

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,default=ROOT/'tmp/pdfs/ajuste-densidad')
    args=parser.parse_args()
    source=ROOT/'tmp/pdfs/tamanos-imagenes-20261110/datos_editor_prueba/project.json'
    project=json.loads(source.read_text(encoding='utf-8'))
    out=args.output
    result=generate(project,out)
    assert len(set(result['page_map'].values()))==1, result['page_map']
    with pymupdf.open(out/'cuadernillo.pdf') as doc:
        page=doc[next(iter(result['page_map'].values()))-1]
        page.get_pixmap(matrix=pymupdf.Matrix(1.8,1.8)).save(out/'preguntas.png')
        text=page.get_text()
        assert 'G = 2I' not in text
        for block in page.get_text('dict')['blocks']:
            if block['type']==0:
                assert 0 <= block['bbox'][0] < block['bbox'][2] <= page.rect.width
                assert 0 <= block['bbox'][1] < block['bbox'][3] <= page.rect.height
    print(json.dumps(result,ensure_ascii=True))
