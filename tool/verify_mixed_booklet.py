"""Authorized isolated mixed-flow copy and visual review artifacts."""
import hashlib
import json
from pathlib import Path
import pymupdf
from PIL import Image,ImageDraw
from editor_model import ROOT,selected_questions
from editor_pdf import generate

SOURCE=ROOT/'tmp/pdfs/tamanos-imagenes-20261110/datos_editor_prueba/project.json'
BASE=Path(r'C:\Users\LENOVO 14ALC6\Desktop\SP-001-matematicas-corregido.json')
OUT=ROOT/'tmp/pdfs/flujo-mixto'

def main():
    hashes={p:hashlib.sha256(p.read_bytes()).hexdigest() for p in (SOURCE,BASE)}
    project=json.loads(BASE.read_text(encoding='utf-8'))
    project['column_flow']='balanced'
    full={1,2,5,8,15,25}
    selected=selected_questions(project)
    assert len(selected)==25
    changes=[]
    for n,q in enumerate(selected,1):
        layout='full' if n in full else 'columns'
        if q['layout']!=layout:
            changes.append({'number':n,'id':q['id'],'from':q['layout'],'to':layout})
        q['layout']=layout
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/'SP-001-flujo-mixto.json').write_text(json.dumps(project,ensure_ascii=False,indent=2),encoding='utf-8')
    (OUT/'cambios-distribucion.json').write_text(json.dumps(changes,ensure_ascii=False,indent=2),encoding='utf-8')
    result=generate(project,OUT)
    pictures=[]
    for name in ('cuadernillo','cuadernillo_resuelto','clave_docente'):
        with pymupdf.open(OUT/(name+'.pdf')) as doc:
            for n,page in enumerate(doc,1):
                path=OUT/f'{name}-{n:02}.png'
                page.get_pixmap(matrix=pymupdf.Matrix(1.25,1.25)).save(path)
                pictures.append((name,n,path))
    for offset in range(0,len(pictures),8):
        sheet=Image.new('RGB',(1400,2080),'#e4e8eb');draw=ImageDraw.Draw(sheet)
        for k,(name,n,path) in enumerate(pictures[offset:offset+8]):
            x=k%2*700;y=k//2*520
            with Image.open(path) as im:
                im.thumbnail((680,485));sheet.paste(im,(x+(700-im.width)//2,y+25))
            draw.text((x+10,y+5),f'{name} - {n}',fill='black')
        sheet.save(OUT/f'contacto-{offset//8+1}.png')
    with pymupdf.open(OUT/'clave_docente.pdf') as doc:
        actual=[page.get_textbox(d['rect']).strip() for page in doc for d in page.get_drawings()
                if 12<=d['rect'].width<=14 and 12<=d['rect'].height<=14 and d.get('fill') and max(d['fill'])<.5]
        assert actual==[q['correct'] for q in selected]
    for p,h in hashes.items():
        assert hashlib.sha256(p.read_bytes()).hexdigest()==h
    (OUT/'resultado.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(result,ensure_ascii=True))

if __name__=='__main__':main()
