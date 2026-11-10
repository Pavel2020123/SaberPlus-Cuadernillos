"""Render selected candidate page pairs for visual comparison, without editing PDFs."""
import json
import sys
from pathlib import Path
import pymupdf
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'output' / 'cotejo_30'
items = json.loads((OUT / 'fichas_academicas.json').read_text(encoding='utf-8'))
lookup = {(i['file_id'], i['question']): i for i in items}
pairs = json.loads((OUT / 'candidatos.json').read_text(encoding='utf-8'))
for arg in sys.argv[1:]:
    index = int(arg)
    pair = pairs[index-1]
    a, b = (lookup[tuple(pair[k])] for k in ('left', 'right'))
    images = []
    for item in (a, b):
        with pymupdf.open(item['source_path']) as doc:
            page = doc[item['physical_page']-1]
            pix = page.get_pixmap(matrix=pymupdf.Matrix(950/page.rect.width, 950/page.rect.width), alpha=False)
            im = Image.frombytes('RGB', (pix.width, pix.height), pix.samples)
            images.append(im)
    sheet = Image.new('RGB', (1900, max(i.height for i in images)+50), 'white')
    draw = ImageDraw.Draw(sheet)
    for n, (im, item) in enumerate(zip(images, (a, b))):
        sheet.paste(im, (950*n, 50))
        draw.text((950*n+10, 10), f"Pair {index} {item['file_id']} q{item['question']} page {item['physical_page']}", fill='black')
    target = OUT / f'pair-{index:04d}.png'
    sheet.save(target)
    print(target)
