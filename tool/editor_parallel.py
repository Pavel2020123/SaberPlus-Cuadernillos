"""Run an independent local editor without changing the main editor's state."""
import argparse
from html import escape
import json
from pathlib import Path
from urllib.parse import urlsplit
import re

import editor_server as server


def workspace_directory(name, port):
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]{0,63}', name):
        raise ValueError('Usa un nombre de espacio con letras, números, guiones o guiones bajos.')
    if type(port) is not int or not 1024 <= port <= 65535:
        raise ValueError('El puerto debe estar entre 1024 y 65535.')
    base = (server.ROOT / 'data/parallel').resolve()
    target = (base / f'{name}-{port}').resolve()
    if not target.is_relative_to(base):
        raise ValueError('El espacio debe permanecer dentro de data/parallel.')
    return target


def initialize_workspace(data, template):
    """Create an empty project once; reopening never replaces saved work."""
    state = data / 'project.json'
    if state.exists():
        project = json.loads(state.read_text(encoding='utf-8'))
        server.validate_project(project)
        return project
    project = json.loads(Path(template).read_text(encoding='utf-8'))
    if project.get('questions') or project.get('contexts'):
        raise ValueError('El proyecto inicial debe estar vacío; usa planning/starter_projects.')
    server.validate_project(project)
    project['revision'] = 0
    data.mkdir(parents=True, exist_ok=True)
    with state.open('x', encoding='utf-8') as output:
        json.dump(project, output, ensure_ascii=False, indent=2)
        output.write('\n')
    return project


def parallel_page(label):
    html = (server.ROOT / 'tool/editor_web/index.html').read_text(encoding='utf-8')
    banner = ('<section class="card" aria-label="Tu espacio de trabajo paralelo" '
              'style="border:2px solid #375d83;background:#edf4fb">'
              '<p class="eyebrow">TU ESPACIO · EDICIÓN PARALELA</p>'
              f'<h2>{escape(label)}</h2>'
              '<p>Las preguntas de esta ventana se guardan aparte del cuadernillo principal. '
              'Elige otra área para avanzar mientras se prepara Matemáticas en la otra ventana.</p>'
              '<p>Al terminar, guarda y descarga tu proyecto JSON. Después integraremos sus preguntas '
              'en el cuadernillo principal.</p></section>')
    html = html.replace('<title>SaberPlus · Editor de cuadernillos</title>',
                        '<title>SaberPlus · Tu trabajo paralelo</title>', 1)
    return html.replace('<main>', '<main>' + banner, 1).encode('utf-8')


class ParallelHandler(server.Handler):
    def do_GET(self):
        if not self.trusted():
            return self.response({'error': 'Host no permitido.'}, 403)
        if urlsplit(self.path).path != '/':
            return super().do_GET()
        raw = parallel_page(self.server.workspace_label)
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', str(len(raw)))
        self.send_header('Cache-Control', 'no-store')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.end_headers()
        self.wfile.write(raw)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port', type=int, default=4186)
    parser.add_argument('--workspace', default='SP-003-usuario')
    parser.add_argument('--template', type=Path,
                        default=server.ROOT / 'planning/starter_projects/SP-003-primera.json')
    args = parser.parse_args()
    data = workspace_directory(args.workspace, args.port)
    # Different ports always have different data directories. Bind first so a
    # second process cannot open the same workspace while its port is occupied.
    with server.ThreadingHTTPServer(('127.0.0.1', args.port), ParallelHandler) as http:
        initialize_workspace(data, args.template)
        server.DATA, server.STATE = data, data / 'project.json'
        http.workspace_label = args.workspace
        print(f'Tu editor paralelo: http://127.0.0.1:{args.port}', flush=True)
        print(f'Proyecto independiente: {server.STATE}', flush=True)
        http.serve_forever()


if __name__ == '__main__':
    main()
