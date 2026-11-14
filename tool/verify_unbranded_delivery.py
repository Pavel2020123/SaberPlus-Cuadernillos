from pathlib import Path
import json,re,hashlib,sys,ast
import pymupdf as fitz
from PIL import Image,ImageDraw
root=Path.cwd();src=Path.home()/'Desktop/SaberPlus - Cuadernillos SP001-SP003';dst=Path.home()/'Desktop/Cuadernillos SP001-SP003 - Sin marca'
sys.path.insert(0,str(root/'tool'))
from editor_model import selected_questions
total=0
for f in dst.rglob('proyecto.json'):
 a=json.loads((src/f.relative_to(dst)).read_text(encoding='utf8'));b=json.loads(f.read_text(encoding='utf8'))
 assert a['questions']==b['questions'] and a['contexts']==b['contexts'],f
 total+=len(selected_questions(b))
for f in dst.rglob('*.py'):ast.parse(f.read_text(encoding='utf8'))
# Replace the empty mascot panel with a neutral typographic cover.
for f in dst.rglob('*.pdf'):
 d=fitz.open(f)
 if 'SIMULACRO' not in d[0].get_text():d.close();continue
 pg=d[0];box=fitz.Rect(82,205,513,391)
 pg.add_redact_annot(box,fill=(1,1,1));pg.apply_redactions(images=0,graphics=0)
 count=120 if 'PRIMERA' in pg.get_text() else 134
 pg.insert_textbox(fitz.Rect(82,260,513,315),'CUADERNILLO DE PRÁCTICA',fontname='hebo',fontsize=20,color=(.09,.15,.22),align=1)
 pg.insert_textbox(fitz.Rect(82,307,513,345),f'{count} PREGUNTAS',fontname='helv',fontsize=13,color=(.32,.38,.45),align=1)
 t=f.with_suffix('.final.pdf');d.save(t,garbage=4,deflate=True);d.close();t.replace(f)
qa=root/'tmp/pdfs/sin_marca';qa.mkdir(parents=True,exist_ok=True)
sheet=Image.new('RGB',(1500,1760),'#cccccc');draw=ImageDraw.Draw(sheet);idx=0
for code in ('SP001','SP002','SP003'):
 for ses in sorted((dst/code).iterdir()):
  f=ses/'01 - Cuadernillo.pdf';d=fitz.open(f)
  for page in (0,len(d)-1):
   pix=d[page].get_pixmap(matrix=fitz.Matrix(.57,.57));im=Image.frombytes('RGB',(pix.width,pix.height),pix.samples)
   x=idx%4*375;y=idx//4*585;sheet.paste(im,(x,y+20));draw.text((x,y),f'{code} {ses.name} p{page+1}',fill='black');idx+=1
  d.close()
sheet.save(qa/'portadas_y_hojas.jpg')
for f in dst.rglob('*.pdf'):
 d=fitz.open(f)
 for p in d:
  assert not re.search(r'saber\s*plus',p.get_text(),re.I)
  assert not any(s['text'].strip() in ('S+','S','+') and s['bbox'][1]>p.rect.height-55 for b in p.get_text('dict')['blocks'] if 'lines' in b for l in b['lines'] for s in l['spans'])
 d.close()
for f in list(dst.rglob('*')):
 if f.is_file() and f.name.upper()=='SABI_GENERACION.md':f.unlink()
def digest(f):
 with f.open('rb') as stream:return hashlib.file_digest(stream,'sha256').hexdigest()
manifest={f.relative_to(dst).as_posix():digest(f) for f in dst.rglob('*') if f.is_file() and f.name!='MANIFIESTO_SHA256.json'}
(dst/'MANIFIESTO_SHA256.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8')
assert all(digest(dst/name)==value for name,value in manifest.items())
print(json.dumps({'preguntas_conservadas':total,'pdf':len(list(dst.rglob('*.pdf'))),'archivos_verificados':len(manifest),'fallas':0}))
