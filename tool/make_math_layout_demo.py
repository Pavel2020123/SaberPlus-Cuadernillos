"""Authorized isolated math/grid fixture and two read-only USB reference renders."""
import json
from io import BytesIO
from pathlib import Path
from unittest.mock import patch
from PIL import Image as PILImage,ImageDraw
import pymupdf
from reportlab.platypus import Image
from editor_model import ROOT,new_project,blank_assessment
from editor_pdf import generate

OUT=ROOT/'tmp/pdfs/ecuaciones-maquetacion'

def fixture_picture(path,width,max_height=100,**kwargs):
    image=PILImage.new('RGB',(600,300),'white');d=ImageDraw.Draw(image)
    d.line((45,20,45,250,570,250),fill='black',width=4)
    for i,height in enumerate((70,120,95,160)):
        d.rectangle((90+i*110,250-height,135+i*110,250),fill='#777777')
    buffer=BytesIO();image.save(buffer,format='PNG');buffer.seek(0)
    result=Image(buffer)
    scale=min(width/600,max_height/300,1)
    result.drawWidth=600*scale;result.drawHeight=300*scale
    return result

def build():
    project=new_project();project.update(code='QA-MATH',time='Demostración técnica')
    formulas=[r'\(\frac{3}{4}+\frac{1}{2}\)',r'\(\sqrt{x^2+y^2}\)',
              r'\(a_{n+1}=2a_n\)',r'\(\sum_{k=1}^{n}k\)']
    for number in range(1,6):
        q=dict(id='math-fixture-'+str(number),area='mathematics',part=0,order=number,
            layout='columns' if number in (1,2,4) else 'full',included=True,context=None,
            topic='Demostración técnica',subtopic='No pertenece al banco',
            introduction='Muestra de composición; no es una pregunta para estudiantes.',
            stem=r'Compara \(\frac{1}{\sqrt{x_1^2+1}}\) con \(a_n=a_1r^{n-1}\).',
            options=[dict(text=formula) for formula in formulas],correct='B',
            explanation=r'Comprobación tipográfica: \(\sqrt[3]{8}=2\), \(\alpha\leq\beta\) y \(x_{n+1}\).',
            assessment=blank_assessment('mathematics'))
        if number==3:
            q.update(options_layout='grid2',stem='Opciones gráficas A/B en la primera fila y C/D en la segunda.')
            for option in q['options']:option['image']='assets/uploads/'+'a'*32+'.png'
        if number==2:
            q['column_break_before']=True
        if number==4:
            q['stem']=r'Sucesión: \(a_n=\frac{n(n+1)}{2}\).'+('\nPaso: conservar la relación entre términos.'*7)
        if number==5:
            q.update(page_break_before=True,stem=r'Fórmula en línea separada:\[\frac{-b+\sqrt{b^2-4ac}}{2a}\]Luego continúa el texto sin superponerse.')
        project['questions'].append(q)
    with patch('editor_pdf.picture',side_effect=fixture_picture):
        result=generate(project,OUT)
    for name in ('cuadernillo','cuadernillo_resuelto','clave_docente'):
        with pymupdf.open(OUT/(name+'.pdf')) as doc:
            for n,page in enumerate(doc):
                page.get_pixmap(matrix=pymupdf.Matrix(1.4,1.4)).save(OUT/f'{name}-{n+1}.png')
    catalogue=json.loads((ROOT/'output/cotejo_30/indice_editorial.json').read_text(encoding='utf-8'))
    ref=next(q for q in catalogue if q['catalog_id']=='USB-1c6462bf5377-Q021')
    if not Path(ref['source_path']).is_file():
        print('USB reference unavailable; not inspected.')
    else:
        with pymupdf.open(ref['source_path']) as doc:
            for number in (2,11):
                doc[number-1].get_pixmap(matrix=pymupdf.Matrix(1.4,1.4)).save(OUT/f'referencia-pagina-{number}.png')
        (OUT/'referencia.json').write_text(json.dumps({'source':ref['source_path'],'pages':[2,11]},ensure_ascii=False),encoding='utf-8')
    print(json.dumps(result,ensure_ascii=True))

if __name__=='__main__':build()
