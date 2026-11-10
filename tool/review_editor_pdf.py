"""Render every exported page and produce inspection sheets; no source PDFs changed."""
import argparse
from pathlib import Path
import pymupdf
from PIL import Image, ImageOps, ImageDraw

parser=argparse.ArgumentParser()
parser.add_argument('folder',type=Path)
args=parser.parse_args()
dest=Path('tmp/pdfs')/('editor-'+args.folder.name)
dest.mkdir(parents=True,exist_ok=True)
for name in ('cuadernillo','cuadernillo_resuelto','clave_docente','guia_docente'):
    if not (args.folder/(name+'.pdf')).exists():
        continue  # Live previews deliberately never generate the teacher key.
    with pymupdf.open(args.folder/(name+'.pdf')) as doc:
        for start in range(0,len(doc),6):
            sheet=Image.new('RGB',(1140,1700),'#dce0e4')
            draw=ImageDraw.Draw(sheet)
            for index in range(start,min(start+6,len(doc))):
                page=doc[index]
                pix=page.get_pixmap(matrix=pymupdf.Matrix(1.35,1.35),alpha=False)
                image=Image.frombytes('RGB',[pix.width,pix.height],pix.samples)
                image.save(dest/f'{name}-{index+1:02}.png')
                image.thumbnail((550,780))
                x=(index-start)%2*570+10;y=(index-start)//2*565+22
                # Three rows with a readable thumbnail of each whole page.
                image.thumbnail((390,535))
                sheet.paste(image,(x+75,y))
                draw.text((x,y-15),f'{name} {index+1}',fill='black')
            sheet.save(dest/f'{name}-sheet-{start//6+1}.png')
    print(name,len(doc) if not doc.is_closed else 'rendered')
