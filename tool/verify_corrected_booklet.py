"""Generate/review the explicitly approved copy, never import or save it live."""
import json
import hashlib
from pathlib import Path
import pymupdf
from PIL import Image,ImageDraw
from editor_model import ROOT,selected_questions
from editor_pdf import generate

SOURCE=ROOT/'tmp/pdfs/tamanos-imagenes-20261110/datos_editor_prueba/project.json'
COPY=Path(r'C:\Users\LENOVO 14ALC6\Desktop\SP-001-matematicas-corregido.json')
OUT=ROOT/'tmp/pdfs/cuadernillo-corregido'

if __name__=='__main__':
    before=hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    project=json.loads(COPY.read_text(encoding='utf-8'))
    selected=selected_questions(project)
    assert len(project['questions'])==26 and len(selected)==25
    result=generate(project,OUT)
    pictures=[]
    for name in ('cuadernillo','cuadernillo_resuelto','clave_docente'):
        with pymupdf.open(OUT/(name+'.pdf')) as doc:
            for number,page in enumerate(doc,1):
                path=OUT/f'{name}-{number:02}.png'
                page.get_pixmap(matrix=pymupdf.Matrix(1.25,1.25)).save(path)
                pictures.append((name,number,path))
    for offset in range(0,len(pictures),8):
        sheet=Image.new('RGB',(1100,1640),'#e4e8eb');draw=ImageDraw.Draw(sheet)
        for k,(name,n,path) in enumerate(pictures[offset:offset+8]):
            x=k%2*550;y=k//2*410
            with Image.open(path) as image:
                image.thumbnail((535,380));sheet.paste(image,(x+(550-image.width)//2,y+25))
            draw.text((x+10,y+5),f'{name} - pagina {n}',fill='black')
        sheet.save(OUT/f'contacto-{offset//8+1}.png')
    with pymupdf.open(OUT/'clave_docente.pdf') as doc:
        actual=[page.get_textbox(d['rect']).strip() for page in doc for d in page.get_drawings()
                if 12<=d['rect'].width<=14 and 12<=d['rect'].height<=14 and d.get('fill') and max(d['fill'])<.5]
        assert actual==[q['correct'] for q in selected]
    with pymupdf.open(OUT/'cuadernillo.pdf') as doc:
        assert ' Copiar' not in ''.join(p.get_text() for p in doc)
        assert 'Deja el campo Introducción vacío' not in ''.join(p.get_text() for p in doc)
    assert before==hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    print(json.dumps(result,ensure_ascii=True))
