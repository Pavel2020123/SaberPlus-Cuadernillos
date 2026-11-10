"""Read-only page comparison. Similarity is never authority to delete a variant."""
import argparse
import json
from datetime import datetime
import pymupdf
from PIL import Image,ImageChops
import usb_pdf_catalog as catalog

parser=argparse.ArgumentParser()
parser.add_argument('left')
parser.add_argument('right')
args=parser.parse_args()
with catalog.db() as conn:
    def get(ident):
        row=conn.execute('SELECT * FROM files WHERE id=?',(ident,)).fetchone()
        if not row:raise ValueError('Unknown catalog ID')
        visited=set()
        while row['duplicate_of'] and row['status']=='eliminado_duplicado':
            if row['id'] in visited:raise ValueError('Invalid duplicate chain')
            visited.add(row['id']);row=conn.execute('SELECT * FROM files WHERE id=?',(row['duplicate_of'],)).fetchone()
        return row
    left,right=get(args.left),get(args.right)
    lp,rp=catalog.safe(catalog.ROOT/left['current_path']),catalog.safe(catalog.ROOT/right['current_path'])
    if catalog.digest(lp)!=left['sha256'] or catalog.digest(rp)!=right['sha256']:raise ValueError('Files changed since inventory')
    folder=catalog.AUDIT/'comparaciones'/(args.left+'__'+args.right);folder.mkdir(exist_ok=True,parents=True)
    result={'left':args.left,'right':args.right,'canonical_left':left['id'],'canonical_right':right['id'],
            'binary_identical':left['sha256']==right['sha256'],'review_status':'comparacion_automatica_no_semantica',
            'warning':'Paginas fisicas, no numeros de pregunta. OCR, anotaciones, escala y escaneo pueden cambiar la imagen. No se borra por similitud.', 'pages':[]}
    with pymupdf.open(lp) as ld,pymupdf.open(rp) as rd:
        result.update(left_pages=len(ld),right_pages=len(rd))
        saved=0
        for n in range(max(len(ld),len(rd))):
            row={'pdf_page':n+1}
            if n>=len(ld) or n>=len(rd):row['comparison']='pagina_sin_pareja'
            else:
                def render(page):
                    scale=800/page.rect.width
                    pix=page.get_pixmap(matrix=pymupdf.Matrix(scale,scale),colorspace=pymupdf.csGRAY,alpha=False)
                    return Image.frombytes('L',(pix.width,pix.height),pix.samples)
                a,b=render(ld[n]),render(rd[n])
                if a.size!=b.size:row['comparison']='proporcion_distinta'
                else:
                    hist=ImageChops.difference(a,b).histogram();total=a.width*a.height
                    row['equal_pixels']=hist[0]/total
                    row['pixels_difference_over_12']=sum(hist[13:])/total
                    row['comparison']='render_identico' if hist[0]==total else 'render_distinto'
                if row['comparison']!='render_identico' and saved<6:
                    pair=Image.new('RGB',(a.width+b.width,max(a.height,b.height)),'white');pair.paste(a,(0,0));pair.paste(b,(a.width,0));pair.save(folder/f'pagina-{n+1:03d}.png');saved+=1
            result['pages'].append(row)
    target=folder/'comparacion.json';target.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    conn.execute('INSERT INTO actions VALUES(?,?,?,?)',(datetime.now().isoformat(),'automatic_visual_comparison',args.left,json.dumps({'right':args.right,'path':str(target)},ensure_ascii=False)));conn.commit()
    print(json.dumps({'binary_identical':result['binary_identical'],'left_pages':result['left_pages'],'right_pages':result['right_pages'],
         'identical_render_pages':sum(p['comparison']=='render_identico' for p in result['pages']),
         'different_or_unmatched_pages':sum(p['comparison']!='render_identico' for p in result['pages']),'report':str(target)},ensure_ascii=True))
