"""Read-only PDF audit; only writes authorized PNGs and report under tmp/pdfs."""
import json
import re
from pathlib import Path
import pymupdf
from PIL import Image,ImageDraw
from editor_model import ROOT

SOURCE=Path(r'C:\Users\LENOVO 14ALC6\Desktop\fotos para los cuadernillos\Nueva carpeta')
OUT=ROOT/'tmp/pdfs/revision-cuadernillo-actual'

def audit():
    OUT.mkdir(parents=True,exist_ok=True)
    report={};pictures=[]
    for name in ('cuadernillo','cuadernillo_resuelto','clave_docente'):
        with pymupdf.open(SOURCE/(name+'.pdf')) as doc:
            report[name]={'pages':len(doc),'out_of_bounds':[],'page_content':[]}
            for n,page in enumerate(doc,1):
                path=OUT/f'{name}-{n:02}.png'
                page.get_pixmap(matrix=pymupdf.Matrix(1.25,1.25)).save(path)
                pictures.append((name,n,path))
                blocks=page.get_text('blocks')
                for b in blocks:
                    if b[0]<0 or b[1]<0 or b[2]>page.rect.width+.2 or b[3]>page.rect.height+.2:
                        report[name]['out_of_bounds'].append({'page':n,'bbox':b[:4],'text':b[4][:90]})
                report[name]['page_content'].append({'page':n,'text':page.get_text(),
                    'images':[{'bbox':i['bbox'],'digest':i['digest'].hex()} for i in page.get_image_info(hashes=True)]})
    for offset in range(0,len(pictures),8):
        sheet=Image.new('RGB',(1100,1640),'#e4e8eb');draw=ImageDraw.Draw(sheet)
        for k,(name,n,path) in enumerate(pictures[offset:offset+8]):
            x=(k%2)*550;y=(k//2)*410
            with Image.open(path) as image:
                image.thumbnail((535,380))
                sheet.paste(image,(x+(550-image.width)//2,y+25))
            draw.text((x+10,y+5),f'{name} - pagina {n}',fill='black')
        sheet.save(OUT/f'contacto-{offset//8+1}.png')
    with pymupdf.open(SOURCE/'clave_docente.pdf') as key:
        answers=[]
        for page in key:
            for d in page.get_drawings():
                r=d['rect'];fill=d.get('fill')
                if 12<=r.width<=14 and 12<=r.height<=14 and fill and max(fill)<.5:
                    answers.append(page.get_textbox(r).strip())
        report['key_letters']=answers
    text=''.join(p['text'] for p in report['cuadernillo_resuelto']['page_content'][18:])
    report['explanation_headers']=re.findall(r'Pregunta (\d+) · Matemáticas · Respuesta([^\n]*)',text)
    (OUT/'informe.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'pages':{k:v['pages'] for k,v in report.items() if isinstance(v,dict)},
        'key_letters':answers,'explanation_headers':report['explanation_headers'],
        'out_of_bounds':{k:v['out_of_bounds'] for k,v in report.items() if isinstance(v,dict)}},ensure_ascii=True))

if __name__=='__main__':audit()
