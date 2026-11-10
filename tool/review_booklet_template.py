"""Render sample PDFs and source contact sheets for visual inspection."""
from pathlib import Path
import pymupdf
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
TMP = ROOT / 'tmp' / 'pdfs'
TMP.mkdir(parents=True, exist_ok=True)

for source in (ROOT / 'output' / 'pdf').glob('SaberPlus_*.pdf'):
    doc = pymupdf.open(source)
    images = []
    for i, page in enumerate(doc):
        pix = page.get_pixmap(matrix=pymupdf.Matrix(1.3, 1.3), alpha=False)
        image = Image.frombytes('RGB', (pix.width, pix.height), pix.samples)
        image.save(TMP / f'{source.stem}-{i+1}.png')
        thumb = image.copy()
        thumb.thumbnail((390, 552))
        images.append(thumb)
        # All searchable text must remain inside the printable page.
        for block in page.get_text('blocks'):
            if block[0] < 0 or block[1] < 0 or block[2] > page.rect.width + 1 or block[3] > page.rect.height + 1:
                raise ValueError(f'Clipped text in {source.name} page {i+1}')
    sheet = Image.new('RGB', (780, ((len(images)+1)//2)*580), '#cccccc')
    draw = ImageDraw.Draw(sheet)
    for i, image in enumerate(images):
        x, y = (i % 2)*390, (i//2)*580
        sheet.paste(image, (x, y+20))
        draw.text((x+5, y+3), f'Page {i+1}', fill='black')
    sheet.save(TMP / f'{source.stem}-contact.png')
    print(source.name, 'pages', len(doc), 'text bounds OK')

source_root = ROOT / 'references'
names = [
    'ilide.info-primera-sesion-2024-pr_f438466ae203447ffcdf35590111cac4.pdf',
    'ilide.info-primera-sesion-cal-b-2026-filtrado-2026-pr_2fcf46852d51c481b999345c6ad534da.pdf',
    'ilide.info-pruebas-icfes-2020-pdf-pr_17efc2b821b09f8cf24a71860a7445fd.pdf',
    'ilide.info-pruebas-icfes-2024-1-primera-sesion-pr_b3d4072692f6650fc13436c591c0356e.pdf',
    'ilide.info-r-primera-sesion-1-pr_a7afe8f84c2e938dde1bb06695c50100.pdf',
    'ilide.info-segunda-sesion-cal-b-2026-icfes-filtrado-a-detalle-pr_c9736c67614b3b8103566afc14361871.pdf',
    'ilide.info-segunda-sesion-del-icfes-agosto-2025-con-respuestas-pr_9903cf68260b3837b4ea4a83d27b1000.pdf',
    'S11-M 2DA SESIÓN.pdf', 'S11-O Segunda sesión Completo.pdf', 'S11-P s2.pdf',
    'S11-R s2.pdf', 'S11-S s2.pdf', 'S11-T s2.pdf',
]
for batch in range(2):
    selected = names[batch*7:(batch+1)*7]
    sheet = Image.new('RGB', (len(selected)*250, 1050), 'white')
    draw = ImageDraw.Draw(sheet)
    for i, name in enumerate(selected):
        doc = pymupdf.open(source_root / name)
        for row, idx in enumerate([0, min(2, len(doc)-1), max(0, len(doc)-5)]):
            pix = doc[idx].get_pixmap(matrix=pymupdf.Matrix(.4, .4), alpha=False)
            im = Image.frombytes('RGB', (pix.width, pix.height), pix.samples)
            im.thumbnail((245, 315))
            x, y = i*250, row*350
            sheet.paste(im, (x, y+25))
            draw.text((x+3, y+3), f'{batch*7+i+1} | p.{idx+1}', fill='black')
    sheet.save(TMP / f'references-{batch+1}.png')
print('Rendered source samples from all 13 supplied PDFs; no source content exported.')
