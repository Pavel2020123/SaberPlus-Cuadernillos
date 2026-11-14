from pathlib import Path
import json,re,shutil,hashlib
import pymupdf as fitz
root=Path.cwd();desktop=Path.home()/'Desktop';src=desktop/'SaberPlus - Cuadernillos SP001-SP003';dst=desktop/'Cuadernillos SP001-SP003 - Sin marca'
assert src.is_dir() and not dst.exists(),'Conservar cualquier entrega previa; no sobrescribir'
shutil.copytree(src,dst)
stats=[]
for file in sorted(dst.rglob('*.pdf')):
 d=fitz.open(file);changes=0;images=0;oldpages=len(d)
 for pg in d:
  text=pg.get_text()
  # The only cover/instruction illustrations are the branded mascot.
  mascot=('SIMULACRO' in text and 'DATOS DEL ESTUDIANTE' in text) or 'Antes de comenzar' in text
  sheet=('HOJA DE RESPUESTAS' in text or 'CLAVE DE RESPUESTAS' in text) and 'TIPO DE MARCACIONES' in text or ('USO EXCLUSIVO DEL DOCENTE' in text)
  if mascot or sheet:
   for im in pg.get_images(full=True):
    boxes=pg.get_image_rects(im[0])
    if mascot or any(abs(b.width-380)<2 and abs(b.height-430)<2 for b in boxes):
     pg.delete_image(im[0]);images+=1
  for block in pg.get_text('dict')['blocks']:
   if 'lines' not in block:continue
   for line in block['lines']:
    for span in line['spans']:
     s=span['text'];box=fitz.Rect(span['bbox']);replacement=None
     if re.search(r'saber\s*plus',s,re.I):
      replacement=re.sub(r'saber\s*plus','equipo editorial',s,flags=re.I) if 'interna de' in s else ''
     elif box.y0>pg.rect.height-55 and s.strip() in ('S+','S','+'):
      replacement=''
     if replacement is not None:
      pg.add_redact_annot(box,fill=(1,1,1));changes+=1
      # Body text is retained with neutral wording at the same font size.
      if replacement:pg._neutral_replacements=getattr(pg,'_neutral_replacements',[])+[(box,span,replacement)]
  additions=getattr(pg,'_neutral_replacements',[])
  pg.apply_redactions(images=0,graphics=0)
  for box,span,value in additions:
   size=span['size'];width=fitz.get_text_length(value,fontname='helv',fontsize=size)
   if width>box.width:size*=box.width/width
   pg.insert_text((box.x0,span['origin'][1]),value,fontname='helv',fontsize=size,color=(0.1,0.15,0.2))
 d.set_metadata({key:re.sub(r'saber\s*plus','',value,flags=re.I) if isinstance(value,str) else value for key,value in d.metadata.items()})
 temp=file.with_suffix('.neutral.pdf');d.save(temp,garbage=4,deflate=True);d.close();temp.replace(file)
 with fitz.open(file) as check:
  assert len(check)==oldpages
  assert all(not re.search(r'saber\s*plus',p.get_text(),re.I) for p in check)
 stats.append({'archivo':file.relative_to(dst).as_posix(),'paginas':oldpages,'marcas_texto_retiradas':changes,'imagenes_marca_retiradas':images})
 print(file.relative_to(dst),changes,images,flush=True)
# Neutralize the included regeneration engines; preserve all question assets.
for f in dst.rglob('*'):
 if not f.is_file() or f.suffix.lower() not in ('.py','.json','.md','.txt','.toml','.csv'):continue
 if f.name=='MANIFIESTO_SHA256.json':continue
 text=f.read_text(encoding='utf-8-sig')
 if f.name=='editor_pdf.py':
  text=text.replace('def watermark_image():','def watermark_image():\n    return None')
  text=text.replace("c.drawRightString(W-M, 25, 'S+')","pass # Neutral footer")
  text=text.replace("c.drawString(M, H-32, 'SaberPlus')","pass # Neutral header")
  text=text.replace("top-21,'SABERPLUS'","top-21,'RESPUESTAS'")
 if f.name=='preview_editorial_cover.py':
  text=re.sub(r'(def mascot\([^\n]+\):)',r'\1\n    return',text)
  text=text.replace("p('SaberPlus',M,H-30,220,21,True)","pass # Neutral header")
  text=text.replace("c.drawString(W-M-45,19,'S')","pass").replace("c.drawString(W-M-33,27,'+')","pass")
 text=re.sub(r'saber\s*plus','Material de práctica',text,flags=re.I)
 f.write_text(text,encoding='utf8')
# Mascot files are solely cover resources; disable those references before excluding them.
for f in dst.rglob('editorial_cover_config.json'):
 p=json.loads(f.read_text(encoding='utf8'));p.pop('cover_image',None);p.pop('instructions_image',None);f.write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding='utf8')
# The neutral cover function ignores its image arguments; keep config keys safe for callers.
for f in dst.rglob('editorial_cover_config.json'):
 p=json.loads(f.read_text(encoding='utf8'));p['cover_image']='';p['instructions_image']='';f.write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding='utf8')
for f in list(dst.rglob('*')):
 if f.is_file() and f.name.lower().startswith('sabi') and f.suffix.lower() in ('.png','.jpg','.jpeg'):
  f.unlink()
(dst/'LEEME.txt').write_text('CUADERNILLOS SP001-SP003 — EDICIÓN SIN MARCA\n\nPDF organizados por simulacro y sesión. JSON, imágenes de preguntas y motor en ZZ_Informacion_JSON_e_imagenes. Se retiraron la marca, la mascota y las marcas de agua. Se conservan las preguntas, opciones, claves, numeración y páginas. Material de práctica; no es una prueba oficial. Las claves y explicaciones son para el profesor.\n',encoding='utf8')
(dst/'REVISION_SIN_MARCA.json').write_text(json.dumps(stats,ensure_ascii=False,indent=2),encoding='utf8')
def digest(p):
 with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
manifest={f.relative_to(dst).as_posix():digest(f) for f in dst.rglob('*') if f.is_file() and f.name!='MANIFIESTO_SHA256.json'}
(dst/'MANIFIESTO_SHA256.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8')
assert len(stats)==30
print('TERMINADO',dst,len(manifest),flush=True)
