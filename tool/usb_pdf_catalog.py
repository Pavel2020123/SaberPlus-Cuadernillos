"""Resumable local PDF audit. No cloud calls, no access outside one allowed USB folder.

States distinguish extraction from semantic review. Only byte-identical files can be
removed, after a full binary comparison and a recoverable deletion manifest.
"""
import argparse
import csv
import ctypes
import hashlib
import html
import json
import os
import re
import shutil
import sqlite3
import subprocess
import sys
import time
from collections import Counter,defaultdict
from datetime import datetime
from contextlib import closing
from pathlib import Path
import pymupdf

SOURCE=Path(__file__).resolve().parent
ROOT=Path('E:/Icfes_SaberPlus')
AUDIT=ROOT/'_SaberPlus_catalogo'


def candidates(text):
    """Unverified question starts. Never use this index alone to delete a PDF."""
    found=[]
    for match in re.finditer(r'(?m)^\s*(\d{1,3}|I)[.)]\s+([^\n]{12,})',text):
        number=1 if match[1]=='I' else int(match[1])
        if 1<=number<=250:
            found.append({'number':number,'excerpt':match[2][:220]})
    return found


def emit(**data):
    print(json.dumps(data,ensure_ascii=True),flush=True)


def digest(path):
    with path.open('rb') as stream:return hashlib.file_digest(stream,'sha256').hexdigest()


def safe(path):
    path=Path(path).resolve()
    if not path.is_relative_to(ROOT.resolve()) or path==ROOT.resolve():
        raise ValueError('Path outside the authorized PDF folder')
    return path


def relative(path):return safe(path).relative_to(ROOT.resolve()).as_posix()


def serial():
    number=ctypes.c_ulong();label=ctypes.create_unicode_buffer(260)
    if not ctypes.windll.kernel32.GetVolumeInformationW('E:\\',label,len(label),ctypes.byref(number),None,None,None,0):
        raise OSError('USB is not available')
    if label.value.upper()!='PAVEL':raise ValueError('E: is no longer PAVEL; stop')
    return str(number.value)


def db():
    AUDIT.mkdir(exist_ok=True)
    marker=AUDIT/'identidad.json'
    number=serial()
    if marker.exists():
        if json.loads(marker.read_text(encoding='utf-8'))['serial']!=number:raise ValueError('USB identity changed')
    else:marker.write_text(json.dumps({'label':'PAVEL','serial':number,'root':str(ROOT)},indent=2),encoding='utf-8')
    conn=sqlite3.connect(AUDIT/'catalogo.sqlite',timeout=30)
    conn.row_factory=sqlite3.Row
    conn.execute('PRAGMA journal_mode=WAL')
    conn.executescript('''
    CREATE TABLE IF NOT EXISTS files(id TEXT PRIMARY KEY, original_path TEXT UNIQUE,current_path TEXT,
      bytes INTEGER,mtime_ns INTEGER,priority INTEGER,priority_reason TEXT,sha256 TEXT,
      pages INTEGER,text_pages INTEGER,scanned_pages INTEGER,status TEXT DEFAULT 'inventariado',error TEXT,
      duplicate_of TEXT,review_status TEXT DEFAULT 'pendiente',review_json TEXT,updated_at TEXT);
    CREATE TABLE IF NOT EXISTS pages(file_id TEXT,page INTEGER,text TEXT,source TEXT,chars INTEGER,
      normalized_sha256 TEXT,PRIMARY KEY(file_id,page));
    CREATE TABLE IF NOT EXISTS actions(time TEXT,kind TEXT,file_id TEXT,details TEXT);
    ''')
    return conn


def priority(path):
    text=path.as_posix().lower()
    years=re.findall(r'(?<!\d)(20(?:1[4-9]|2[0-6]))(?!\d)',text)
    if years:return 10000+int(max(years)),'Por ano (solo prioridad; no fecha confirmada)'
    if 'lyon' in text or 'leon' in text or 'león' in text:return 9000,'Grupo Lyon'
    match=re.search(r'(?:s11[- _]*|^)([a-z])(?:1|2)?(?:\b|[ _])',path.stem.lower())
    if 'entren' in text or match:
        letter=ord(match[1])-97 if match else 0
        return 7000+letter,'Serie por letra; editorial pendiente de confirmar'
    return 1000,'Otros materiales'


def inventory(conn):
    count,total=0,0
    for base,dirs,names in os.walk(ROOT,followlinks=False):
        dirs[:]=[d for d in dirs if not d.startswith('_SaberPlus') and not Path(base,d).is_symlink()
                 and not (Path(base,d).stat().st_file_attributes & 1024)]
        for name in names:
            if not name.lower().endswith('.pdf'):continue
            path=safe(Path(base,name));rel=relative(path);stat=path.stat()
            existing=conn.execute('SELECT id FROM files WHERE current_path=? OR original_path=?',(rel,rel)).fetchone()
            if not existing:
                ident='USB-'+hashlib.sha256(rel.encode('utf-8')).hexdigest()[:12]
                rank,reason=priority(Path(rel))
                conn.execute('INSERT INTO files(id,original_path,current_path,bytes,mtime_ns,priority,priority_reason) VALUES(?,?,?,?,?,?,?)',
                             (ident,rel,rel,stat.st_size,stat.st_mtime_ns,rank,reason))
            count+=1;total+=stat.st_size
    conn.commit();emit(stage='inventory',files=count,bytes=total)


def scan(conn,limit):
    rows=conn.execute("SELECT * FROM files WHERE status IN ('inventariado','error') ORDER BY priority DESC,original_path LIMIT ?",(limit,)).fetchall()
    for index,row in enumerate(rows,1):
        path=safe(ROOT/row['current_path'])
        try:
            before=path.stat();sha=digest(path)
            text_pages,scan_pages=0,0
            with pymupdf.open(path) as doc:
                count=len(doc)
                if doc.needs_pass:raise ValueError('PDF protegido con clave')
                for n,page in enumerate(doc,1):
                    text=page.get_text(sort=True)
                    chars=len(re.sub(r'\s','',text))
                    source='embedded' if chars>=80 else 'needs_ocr'
                    if source=='embedded':text_pages+=1
                    else:scan_pages+=1
                    normalized=re.sub(r'\s+',' ',text).strip()
                    conn.execute('INSERT OR REPLACE INTO pages VALUES(?,?,?,?,?,?)',(row['id'],n,text,source,chars,hashlib.sha256(normalized.encode()).hexdigest() if chars>=80 else None))
            after=path.stat()
            if (before.st_size,before.st_mtime_ns)!=(after.st_size,after.st_mtime_ns):raise ValueError('PDF cambio durante la lectura')
            conn.execute('UPDATE files SET sha256=?,pages=?,text_pages=?,scanned_pages=?,status=?,error=NULL,updated_at=? WHERE id=?',
                         (sha,count,text_pages,scan_pages,'extraido_texto' if not scan_pages else 'requiere_ocr',datetime.now().isoformat(),row['id']))
            conn.commit();emit(stage='scan',id=row['id'],name=path.name,pages=count,embedded=text_pages,needs_ocr=scan_pages)
        except Exception as exc:
            conn.rollback()
            conn.execute('UPDATE files SET status=?,error=?,updated_at=? WHERE id=?',('error',str(exc),datetime.now().isoformat(),row['id']))
            conn.commit();emit(stage='error',id=row['id'],error=str(exc))
        if index%20==0:report(conn)
    report(conn)


def ocr(conn,limit):
    rows=conn.execute("SELECT * FROM files WHERE status='requiere_ocr' AND duplicate_of IS NULL ORDER BY priority DESC,original_path LIMIT ?",(limit,)).fetchall()
    for row in rows:
        # Names may be reviewed between documents; do not use a stale queued path.
        row=conn.execute('SELECT * FROM files WHERE id=?',(row['id'],)).fetchone()
        if row['duplicate_of'] or row['status']!='requiere_ocr':continue
        path=safe(ROOT/row['current_path']);folder=AUDIT/'trabajo_ocr'/row['id'];folder.mkdir(parents=True,exist_ok=True)
        output=folder/'ocr.jsonl'
        try:
            if digest(path)!=row['sha256']:raise ValueError('El PDF cambio desde el inventario')
            pending=[r['page'] for r in conn.execute("SELECT page FROM pages WHERE file_id=? AND source='needs_ocr' ORDER BY page",(row['id'],))]
            with pymupdf.open(path) as doc:
                for n in pending:
                    dest=folder/f'{n:04d}.png'
                    if not dest.exists():
                        page=doc[n-1];scale=min(1.9,3800/max(page.rect.width,page.rect.height))
                        page.get_pixmap(matrix=pymupdf.Matrix(scale,scale),alpha=False).save(dest)
            emit(stage='ocr_start',id=row['id'],name=path.name,pages=len(pending))
            result=subprocess.run(['powershell.exe','-NoProfile','-File',str(SOURCE/'usb_native_ocr.ps1'),'-InputFolder',str(folder),'-OutputFile',str(output)],capture_output=True,text=True,encoding='utf-8',errors='replace')
            if result.returncode:raise RuntimeError(result.stderr[-1200:])
            if output.exists():
                for line in output.read_text(encoding='utf-8-sig').splitlines():
                    item=json.loads(line)
                    if item.get('error'):continue
                    text=item['text'];chars=len(re.sub(r'\s','',text));normalized=re.sub(r'\s+',' ',text).strip()
                    conn.execute('UPDATE pages SET text=?,source=?,chars=?,normalized_sha256=? WHERE file_id=? AND page=?',
                                 (text,'windows_ocr' if chars>=80 else 'ocr_poco_texto',chars,hashlib.sha256(normalized.encode()).hexdigest(),row['id'],item['page']))
            remaining=conn.execute("SELECT COUNT(*) FROM pages WHERE file_id=? AND source='needs_ocr'",(row['id'],)).fetchone()[0]
            alerts=conn.execute("SELECT COUNT(*) FROM pages WHERE file_id=? AND source='ocr_poco_texto'",(row['id'],)).fetchone()[0]
            state='requiere_ocr' if remaining else 'extraido_ocr_con_alertas' if alerts else 'extraido_ocr'
            conn.execute('UPDATE files SET status=?,updated_at=? WHERE id=?',(state,datetime.now().isoformat(),row['id']))
            conn.commit()
            # Delete only generated PNGs under this exact work folder, never source PDFs.
            for image in folder.glob('*.png'):
                if safe(image).parent==folder.resolve():image.unlink()
            emit(stage='ocr_complete',id=row['id'],remaining=remaining)
        except Exception as exc:
            conn.rollback();emit(stage='ocr_error',id=row['id'],error=str(exc))
            conn.execute('UPDATE files SET error=? WHERE id=?',(str(exc),row['id']));conn.commit()
        report(conn)


def identical(a,b):
    if a.stat().st_size!=b.stat().st_size:return False
    with a.open('rb') as left,b.open('rb') as right:
        while True:
            x,y=left.read(2*1024*1024),right.read(2*1024*1024)
            if x!=y:return False
            if not x:return True


def dedup(conn,apply=False):
    groups=defaultdict(list)
    for row in conn.execute("SELECT * FROM files WHERE sha256 IS NOT NULL AND duplicate_of IS NULL AND status!='eliminado_duplicado'"):
        groups[row['sha256']].append(dict(row))
    actions=[]
    for sha,rows in groups.items():
        if len(rows)<2:continue
        rows.sort(key=lambda r:(r['review_status']=='pendiente',-r['priority'],not Path(r['current_path']).name.startswith('ICFES_'),len(r['current_path']),r['current_path']))
        keep=rows[0];keep_path=safe(ROOT/keep['current_path'])
        for duplicate in rows[1:]:
            duplicate_path=safe(ROOT/duplicate['current_path'])
            keep_stat=keep_path.stat();dup_stat=duplicate_path.stat()
            if keep_path==duplicate_path:raise ValueError('Cannot remove canonical file')
            if digest(keep_path)!=sha or digest(duplicate_path)!=sha or not identical(keep_path,duplicate_path):
                raise ValueError('Binary identity verification failed; no deletion')
            item={'duplicate_id':duplicate['id'],'removed_path':duplicate['current_path'],'kept_id':keep['id'],'kept_path':keep['current_path'],'sha256':sha,'bytes':duplicate['bytes']}
            actions.append(item)
            if apply:
                if keep_path.stat().st_mtime_ns!=keep_stat.st_mtime_ns or duplicate_path.stat().st_mtime_ns!=dup_stat.st_mtime_ns:
                    raise ValueError('File changed during duplicate verification; stop')
                # Persist recovery mapping BEFORE removal. Restoring is a byte-for-byte copy of keeper.
                with (AUDIT/'duplicados_eliminados.jsonl').open('a',encoding='utf-8') as f:
                    f.write(json.dumps(item,ensure_ascii=False)+'\n');f.flush();os.fsync(f.fileno())
                duplicate_path.unlink()
                conn.execute('UPDATE files SET status=?,duplicate_of=?,updated_at=? WHERE id=?',('eliminado_duplicado',keep['id'],datetime.now().isoformat(),duplicate['id']))
                conn.execute('INSERT INTO actions VALUES(?,?,?,?)',(datetime.now().isoformat(),'remove_exact_duplicate',duplicate['id'],json.dumps(item,ensure_ascii=False)))
                conn.commit();emit(stage='duplicate_removed',id=duplicate['id'],kept=keep['id'],bytes=duplicate['bytes'])
    (AUDIT/'plan_duplicados_exactos.json').write_text(json.dumps(actions,ensure_ascii=False,indent=2),encoding='utf-8')
    emit(stage='dedup',apply=apply,duplicates=len(actions),bytes=sum(a['bytes'] for a in actions))
    report(conn)


def restore(conn,ident):
    row=conn.execute('SELECT * FROM files WHERE id=?',(ident,)).fetchone()
    if not row or row['status']!='eliminado_duplicado':raise ValueError('ID is not a removed exact duplicate')
    keep=conn.execute('SELECT * FROM files WHERE id=?',(row['duplicate_of'],)).fetchone()
    visited={ident}
    while keep and keep['status']=='eliminado_duplicado':
        if keep['id'] in visited:raise ValueError('Invalid duplicate chain')
        visited.add(keep['id'])
        keep=conn.execute('SELECT * FROM files WHERE id=?',(keep['duplicate_of'],)).fetchone()
    if not keep:raise ValueError('Canonical record missing; stop')
    source=safe(ROOT/keep['current_path']);target=safe(ROOT/row['current_path'])
    if target.exists():raise FileExistsError('Do not overwrite a file to restore a duplicate')
    if digest(source)!=row['sha256']:raise ValueError('Canonical file changed; stop')
    target.parent.mkdir(parents=True,exist_ok=True)
    shutil.copy2(source,target)
    if digest(target)!=row['sha256']:raise ValueError('Restored content did not match')
    conn.execute('UPDATE files SET status=? WHERE id=?',('restaurado_duplicado',ident))
    conn.execute('INSERT INTO actions VALUES(?,?,?,?)',(datetime.now().isoformat(),'restore_exact_duplicate',ident,row['current_path']))
    conn.commit();report(conn);emit(stage='restored',id=ident)


def review(conn,path):
    data=json.loads(Path(path).read_text(encoding='utf-8'))
    for item in data:
        row=conn.execute('SELECT * FROM files WHERE id=?',(item['id'],)).fetchone()
        if not row or row['duplicate_of']:raise ValueError('Review needs an existing retained file')
        actual=safe(ROOT/row['current_path'])
        if digest(actual)!=row['sha256']:raise ValueError('File changed since review')
        if item.get('rename'):
            name=item['rename']
            if Path(name).name!=name or not name.lower().endswith('.pdf'):raise ValueError('Invalid reviewed filename')
            target=safe(actual.with_name(name))
            if target.exists() and target!=actual:raise FileExistsError('Never overwrite another variant')
            if target!=actual:
                log={'time':datetime.now().isoformat(),'id':item['id'],'old_path':row['current_path'],'new_path':relative(target),'sha256':row['sha256']}
                with (AUDIT/'renombrados.jsonl').open('a',encoding='utf-8') as f:f.write(json.dumps(log,ensure_ascii=False)+'\n')
                actual.rename(target)
                conn.execute('UPDATE files SET current_path=? WHERE id=?',(relative(target),item['id']))
        conn.execute('UPDATE files SET review_status=?,review_json=?,updated_at=? WHERE id=?',
                     (item['status'],json.dumps(item,ensure_ascii=False),datetime.now().isoformat(),item['id']))
        conn.commit();emit(stage='review_saved',id=item['id'],status=item['status'])
    report(conn)


def report(conn):
    rows=[dict(r) for r in conn.execute('SELECT * FROM files ORDER BY priority DESC,original_path')]
    if not rows:return
    with (AUDIT/'inventario.csv').open('w',encoding='utf-8-sig',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter=';');writer.writeheader();writer.writerows(rows)
    counts=Counter(r['status'] for r in rows)
    (AUDIT/'resumen.json').write_text(json.dumps({'files':len(rows),'statuses':dict(counts),'reviewed':dict(Counter(r['review_status'] for r in rows)),
        'pages':sum(r['pages'] or 0 for r in rows),'bytes_original':sum(r['bytes'] for r in rows)},ensure_ascii=False,indent=2),encoding='utf-8')
    esc=html.escape
    table=[]
    ficha=AUDIT/'fichas';ficha.mkdir(exist_ok=True)
    for r in rows:
        info=json.loads(r['review_json']) if r['review_json'] else {}
        file_rows=conn.execute('SELECT page,source,chars,text FROM pages WHERE file_id=? ORDER BY page',(r['id'],)).fetchall()
        text=[f'# {r["id"]}',f'\nOriginal: {r["original_path"]}',f'\nActual: {r["current_path"]}',f'\nEstado tecnico: {r["status"]}. Revision: {r["review_status"]}.',
              f'\nPaginas: {r["pages"] or "pendiente"}. SHA-256: {r["sha256"] or "pendiente"}.',
              '\nEl texto OCR puede tener errores. Un nombre o una extraccion no prueba autenticidad, equivalencia de preguntas ni revision pedagogica.',
              '\n## Revision documentada\n',json.dumps(info,ensure_ascii=False,indent=2) if info else 'Pendiente de revision visual y de preguntas.',
              '\n## Extraccion por pagina\n','Pagina | Metodo | Caracteres\n--- | --- | ---']
        text.extend(f'{p["page"]} | {p["source"]} | {p["chars"]}' for p in file_rows)
        text += ['\n## Posibles enunciados detectados (sin verificacion)\n',
                 'El OCR puede omitir numeros o mezclar columnas. Estos recortes no certifican el total ni equivalencia entre preguntas.']
        for p in file_rows:
            for item in candidates(p['text']):
                text.append(f'- Pagina {p["page"]}, posible pregunta {item["number"]}: {item["excerpt"]}')
        (ficha/(r['id']+'.md')).write_text('\n'.join(text),encoding='utf-8')
        table.append('<tr>'+''.join(f'<td>{esc(str(v))}</td>' for v in (r['id'],r['priority_reason'],r['current_path'],r['pages'] or '',r['status'],r['review_status'],r['duplicate_of'] or ''))+f'<td><a href="fichas/{r["id"]}.md">Ficha</a></td></tr>')
    content='<!doctype html><html lang="es"><meta charset="utf-8"><title>Catalogo PDF SaberPlus</title><style>body{font:14px Segoe UI,sans-serif;margin:30px;color:#17263a}table{border-collapse:collapse;width:100%}td,th{border:1px solid #ccd4dd;padding:8px;text-align:left}th{background:#edf1f4}h1{font-size:26px}</style><h1>Catalogo PDF · USB PAVEL</h1>'
    content+=f'<p>{len(rows)} archivos registrados. {sum(r["pages"] or 0 for r in rows)} paginas inventariadas.</p><p>Inventario y OCR NO equivalen a preguntas leidas. No se borran documentos por similitud.</p><p>Estados: {esc(str(dict(counts)))}</p>'
    if (AUDIT/'preguntas_revisadas'/'INDICE.html').exists():
        content+='<p><a href="preguntas_revisadas/INDICE.html">Abrir documentacion manual de preguntas y alertas</a> (no confundir con extraccion OCR).</p>'
    content+='<table><tr><th>ID</th><th>Prioridad</th><th>Archivo</th><th>Paginas</th><th>Estado tecnico</th><th>Revision</th><th>Duplicado de</th><th>Detalle</th></tr>'+''.join(table)+'</table></html>'
    (AUDIT/'INDICE.html').write_text(content,encoding='utf-8')


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('mode',choices=['inventory','scan','ocr','report','dedup','review','restore'])
    parser.add_argument('--limit',type=int,default=10000)
    parser.add_argument('--apply',action='store_true')
    parser.add_argument('--review-file',type=Path)
    parser.add_argument('--duplicate-id')
    args=parser.parse_args()
    with closing(db()) as conn:
        if args.mode=='inventory':inventory(conn);report(conn)
        elif args.mode=='scan':scan(conn,args.limit)
        elif args.mode=='ocr':ocr(conn,args.limit)
        elif args.mode=='dedup':dedup(conn,args.apply)
        elif args.mode=='review':review(conn,args.review_file)
        elif args.mode=='restore':restore(conn,args.duplicate_id)
        else:report(conn)


if __name__=='__main__':main()
