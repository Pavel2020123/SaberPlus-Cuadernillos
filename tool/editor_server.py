"""Loopback-only editorial tool. No connection to SaberPlus student services."""
import argparse
import base64
import copy
import io
import json
import mimetypes
import secrets
import threading
import uuid
import tempfile
from collections import OrderedDict
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit, unquote
from PIL import Image, UnidentifiedImageError
import pymupdf
from editor_model import ROOT, AREAS, SESSIONS, CATALOG, new_project, demo_project, validate_project, inspect_project_import
from editor_pdf import generate, preview_project

DATA=ROOT/'data'
STATE=DATA/'project.json'
TOKEN=secrets.token_urlsafe(32)
LOCK=threading.RLock()
RENDER_LOCK=threading.Lock()
PREVIEWS=OrderedDict()
PREVIEW_LOCK=threading.Lock()
Image.MAX_IMAGE_PIXELS=20_000_000


def load():
    return json.loads(STATE.read_text(encoding='utf-8')) if STATE.exists() else new_project()


def save(project, expected):
    with LOCK:
        old=load()
        if type(expected) is not int or expected!=old['revision']:
            raise FileExistsError('El proyecto cambió en otra ventana. Recarga antes de guardar; exporta tu JSON si necesitas conservar esta edición.')
        validate_project(project)
        DATA.mkdir(exist_ok=True)
        if STATE.exists():
            backups=DATA/'backups'
            backups.mkdir(exist_ok=True)
            (backups/(datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S')+'-'+uuid.uuid4().hex[:8]+'.json')).write_bytes(STATE.read_bytes())
        result=copy.deepcopy(project)
        result['revision']=old['revision']+1
        temp=DATA/'project.pending.json'
        temp.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
        temp.replace(STATE)
        return result


class Handler(BaseHTTPRequestHandler):
    def response(self, value, status=200):
        raw=json.dumps(value,ensure_ascii=False).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type','application/json; charset=utf-8')
        self.send_header('Content-Length',str(len(raw)))
        self.send_header('Cache-Control','no-store')
        self.send_header('X-Content-Type-Options','nosniff')
        self.end_headers()
        self.wfile.write(raw)

    def trusted(self):
        host=self.headers.get('Host','')
        return host in (f'127.0.0.1:{self.server.server_port}',f'localhost:{self.server.server_port}')

    def do_GET(self):
        if not self.trusted():
            return self.response({'error':'Host no permitido.'},403)
        path=unquote(urlsplit(self.path).path)
        if path=='/api/bootstrap':
            return self.response({'project':load(),'catalog':CATALOG,'areas':AREAS,'sessions':SESSIONS,'token':TOKEN,
                                  'isolated':DATA.resolve()!=(ROOT/'data').resolve()})
        if path.startswith('/previews/'):
            parts=path.strip('/').split('/')
            if len(parts)!=3 or not parts[2].endswith('.png'):
                return self.response({'error':'Vista previa no encontrada.'},404)
            with PREVIEW_LOCK:
                pdf=PREVIEWS.get(parts[1])
            try:
                number=int(parts[2][:-4])
                with pymupdf.open(stream=pdf,filetype='pdf') as doc:
                    if not pdf or not 1<=number<=len(doc):
                        raise ValueError('Página no disponible.')
                    raw=doc[number-1].get_pixmap(matrix=pymupdf.Matrix(1.5,1.5),alpha=False).tobytes('png')
            except (ValueError,TypeError,pymupdf.EmptyFileError,pymupdf.FileDataError):
                return self.response({'error':'La vista previa caducó. Pulsa Actualizar.'},404)
            self.send_response(200)
            self.send_header('Content-Type','image/png')
            self.send_header('Content-Length',str(len(raw)))
            self.send_header('Cache-Control','no-store')
            self.end_headers()
            return self.wfile.write(raw)
        if path in ('/','/app.js','/style.css','/live.css'):
            target=ROOT/'tool/editor_web'/('index.html' if path=='/' else path[1:])
        elif path.startswith('/assets/uploads/'):
            target=(ROOT/path[1:]).resolve()
            if not target.is_relative_to((ROOT/'assets/uploads').resolve()):
                return self.response({'error':'Ruta inválida.'},403)
        elif path.startswith('/exports/'):
            target=(ROOT/'output/editor'/path.removeprefix('/exports/')).resolve()
            if not target.is_relative_to((ROOT/'output/editor').resolve()):
                return self.response({'error':'Ruta inválida.'},403)
            if target.suffix not in ('.pdf','.json'):
                return self.response({'error':'Archivo no disponible.'},404)
        else:
            return self.response({'error':'No encontrado.'},404)
        if not target.is_file():
            return self.response({'error':'No encontrado.'},404)
        raw=target.read_bytes()
        self.send_response(200)
        self.send_header('Content-Type',mimetypes.guess_type(str(target))[0] or 'application/octet-stream')
        self.send_header('Content-Length',str(len(raw)))
        self.send_header('Cache-Control','no-store')
        self.send_header('X-Content-Type-Options','nosniff')
        self.end_headers()
        self.wfile.write(raw)

    def do_POST(self):
        origin=self.headers.get('Origin')
        if not self.trusted() or self.headers.get('X-Local-Token')!=TOKEN or (origin and origin not in (f'http://127.0.0.1:{self.server.server_port}',f'http://localhost:{self.server.server_port}')):
            return self.response({'error':'Petición local no autorizada. Recarga el editor.'},403)
        try:
            size=int(self.headers.get('Content-Length','0'))
            if not 0<size<=8*1024*1024:
                raise ValueError('Petición demasiado grande.')
            payload=json.loads(self.rfile.read(size))
            if not isinstance(payload,dict):
                raise ValueError('Formato de petición inválido.')
            if self.path=='/api/preview':
                project,notes=preview_project(payload['project'])
                with RENDER_LOCK, tempfile.TemporaryDirectory(prefix='saberplus-preview-') as folder:
                    result=generate(project,Path(folder),preview=True)
                    raw=(Path(folder)/'cuadernillo.pdf').read_bytes()
                job=uuid.uuid4().hex
                with PREVIEW_LOCK:
                    PREVIEWS[job]=raw
                    while len(PREVIEWS)>6:
                        PREVIEWS.popitem(last=False)
                with pymupdf.open(stream=raw,filetype='pdf') as doc:
                    pages=len(doc)
                return self.response({'id':job,'pages':pages,'page_map':result['page_map'],
                    'warnings':notes+result['warnings']})
            if self.path=='/api/import-check':
                return self.response(inspect_project_import(payload.get('project')))
            if self.path=='/api/save':
                project=save(payload['project'],payload.get('revision'))
                return self.response({'project':project,'warnings':validate_project(project)})
            if self.path=='/api/demo':
                project=save(demo_project(),payload.get('revision'))
                return self.response({'project':project,'warnings':validate_project(project)})
            if self.path=='/api/upload':
                raw=base64.b64decode(payload.get('data',''),validate=True)
                if not raw or len(raw)>5*1024*1024:
                    raise ValueError('La imagen debe pesar como máximo 5 MiB.')
                with Image.open(io.BytesIO(raw)) as img:
                    fmt=img.format
                    if fmt not in ('PNG','JPEG','WEBP') or getattr(img,'n_frames',1)!=1 or img.width*img.height>20_000_000:
                        raise ValueError('Usa PNG, JPG o WEBP estático, hasta 20 megapíxeles.')
                    img.verify()
                extension={'PNG':'png','JPEG':'jpg','WEBP':'webp'}[fmt]
                path=ROOT/'assets/uploads'/(uuid.uuid4().hex+'.'+extension)
                path.parent.mkdir(exist_ok=True,parents=True)
                path.write_bytes(raw)
                return self.response({'path':path.relative_to(ROOT).as_posix()})
            if self.path=='/api/generate':
                with LOCK:
                    project=load()
                    if payload.get('revision')!=project['revision']:
                        raise FileExistsError('Guarda o recarga el proyecto antes de generar.')
                    job=uuid.uuid4().hex
                    with RENDER_LOCK:
                        result=generate(project,ROOT/'output/editor'/job)
                return self.response({**result,'student':f'/exports/{job}/cuadernillo.pdf','solved':f'/exports/{job}/cuadernillo_resuelto.pdf',
                    'teacher':f'/exports/{job}/clave_docente.pdf','review':f'/exports/{job}/guia_docente.pdf','project':f'/exports/{job}/proyecto.json'})
            return self.response({'error':'No encontrado.'},404)
        except FileExistsError as exc:
            return self.response({'error':str(exc)},409)
        except (ValueError,KeyError,TypeError,UnidentifiedImageError,Image.DecompressionBombError) as exc:
            return self.response({'error':str(exc)},400)
        except Exception:
            import traceback
            traceback.print_exc()
            return self.response({'error':'No se pudo completar la operación. El servicio conserva el proyecto guardado; revisa el registro local.'},500)


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--port',type=int,default=4185)
    parser.add_argument('--data-dir',type=Path,help='Carpeta independiente para proyecto y respaldos; por defecto data/.')
    args=parser.parse_args()
    if args.data_dir:
        DATA=args.data_dir.resolve()
        STATE=DATA/'project.json'
    print(f'Editor local: http://127.0.0.1:{args.port}',flush=True)
    ThreadingHTTPServer(('127.0.0.1',args.port),Handler).serve_forever()
