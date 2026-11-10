"""Read-only PDF inventory and cover contact sheets for a reversible naming audit."""
import argparse
import hashlib
import json
import re
from pathlib import Path
import pymupdf
from PIL import Image, ImageDraw

parser=argparse.ArgumentParser()
parser.add_argument('folder',type=Path)
parser.add_argument('--output',type=Path,required=True)
args=parser.parse_args()
args.output.mkdir(parents=True,exist_ok=True)
rows=[]
sheet=None
for i,path in enumerate(sorted(args.folder.glob('*.pdf')),1):
    with pymupdf.open(path) as doc:
        first='\n'.join(page.get_text() for page in list(doc)[:2])
        hits=[]
        for n,page in enumerate(doc,1):
            for line in page.get_text().splitlines():
                if re.search(r'calendario|20(?:20|21|22|23|24|25|26)|primera sesi|segunda sesi',line,re.I):
                    hits.append({'page':n,'text':line[:200]})
        row={'id':i,'original':path.name,'pages':len(doc),'bytes':path.stat().st_size,
             'sha256':hashlib.file_digest(path.open('rb'),'sha256').hexdigest(),
             'first_text':first[:4500],'hits':hits[:40],'metadata':doc.metadata}
        rows.append(row)
        pix=doc[0].get_pixmap(matrix=pymupdf.Matrix(.9,.9),alpha=False)
        cover=Image.frombytes('RGB',(pix.width,pix.height),pix.samples)
        cover.save(args.output/f'cover-{i:02}.png')
        cover.thumbnail((340,485))
        pos=(i-1)%12
        if pos==0:sheet=Image.new('RGB',(1440,1560),'#dce0e4')
        x=(pos%4)*360+10;y=(pos//4)*520+25
        sheet.paste(cover,(x,y))
        ImageDraw.Draw(sheet).text((x,y-19),f'{i:02} | {len(doc)} pages',fill='black')
        if pos==11 or i==len(list(args.folder.glob('*.pdf'))):sheet.save(args.output/f'sheet-{(i-1)//12+1}.png')
        print(json.dumps({'id':i,'name':path.name,'pages':len(doc),'text':first[:500],'hits':hits[:5]},ensure_ascii=True),flush=True)
(args.output/'inventory.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
