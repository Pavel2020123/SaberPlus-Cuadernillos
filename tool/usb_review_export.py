"""Create small on-USB visual previews and page evidence for a specific catalog ID."""
import argparse
import json
import pymupdf
from PIL import Image,ImageDraw
import usb_pdf_catalog as catalog

parser=argparse.ArgumentParser()
parser.add_argument('id')
args=parser.parse_args()
with catalog.db() as conn:
    row=conn.execute('SELECT * FROM files WHERE id=?',(args.id,)).fetchone()
    if not row:raise ValueError('ID not in catalog')
    output=catalog.AUDIT/'revision_visual'/row['id'];output.mkdir(parents=True,exist_ok=True)
    with pymupdf.open(catalog.safe(catalog.ROOT/row['current_path'])) as doc:
        sheet=None
        for index,page in enumerate(doc):
            pix=page.get_pixmap(matrix=pymupdf.Matrix(.9,.9),alpha=False)
            im=Image.frombytes('RGB',(pix.width,pix.height),pix.samples)
            if index in (0,len(doc)-1):im.save(output/f'pagina-{index+1:03d}.png')
            im.thumbnail((340,480));pos=index%12
            if pos==0:sheet=Image.new('RGB',(1440,1560),'#dde2e7')
            x=(pos%4)*360+10;y=(pos//4)*520+25
            sheet.paste(im,(x,y));ImageDraw.Draw(sheet).text((x,y-18),f'Pagina {index+1}',fill='black')
            if pos==11 or index==len(doc)-1:sheet.save(output/f'hoja-{index//12+1}.png')
    for p in conn.execute('SELECT * FROM pages WHERE file_id=? ORDER BY page',(row['id'],)):
        print(json.dumps({'page':p['page'],'method':p['source'],'text_start':p['text'][:270],
            'question_starts':catalog.candidates(p['text'])},ensure_ascii=True))
