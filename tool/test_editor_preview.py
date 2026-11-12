"""Preview must use real PDF layout, tolerate unfinished items and never persist edits."""
import copy
import json
import tempfile
import threading
import unittest
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from http.server import ThreadingHTTPServer
from unittest.mock import patch
import pymupdf
import editor_server as server
from editor_model import demo_project,new_project,blank_assessment
from editor_pdf import preview_project,generate


class PreviewTests(unittest.TestCase):
    def test_placeholders_leave_original_unchanged(self):
        p=demo_project();p['questions'][4]['stem']='';p['questions'][4]['options'][0]['text']=''
        original=copy.deepcopy(p)
        draft,notes=preview_project(p)
        self.assertEqual(p,original)
        self.assertTrue(notes)
        self.assertIn('pendiente',draft['questions'][4]['stem'])

    def test_empty_project_gets_only_ephemeral_placeholder(self):
        p=new_project();draft,notes=preview_project(p)
        self.assertEqual(p['questions'],[])
        self.assertEqual(len(draft['questions']),1)
        self.assertTrue(notes)

    def test_map_points_to_numbered_question_and_no_keys(self):
        p=demo_project();p['session']='second';draft,_=preview_project(p)
        with tempfile.TemporaryDirectory() as folder:
            result=generate(draft,folder,preview=True)
            with pymupdf.open(Path(folder)/'cuadernillo.pdf') as doc:
                text=''.join(page.get_text() for page in doc)
                for q in p['questions']:
                    if q['area']=='reading':continue
                    self.assertIn(q['id'],result['page_map'])
                    self.assertGreaterEqual(result['page_map'][q['id']],3)
                self.assertNotIn('Clave ',text)
                self.assertNotIn('Solo vista previa; sin clave',text)
                self.assertIn('Palabras',text)
            self.assertFalse((Path(folder)/'guia_docente.pdf').exists())


class PreviewHTTPTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp=tempfile.TemporaryDirectory()
        cls.old_data,cls.old_state=server.DATA,server.STATE
        server.DATA=Path(cls.temp.name);server.STATE=server.DATA/'project.json'
        cls.http=ThreadingHTTPServer(('127.0.0.1',0),server.Handler)
        cls.thread=threading.Thread(target=cls.http.serve_forever,daemon=True);cls.thread.start()
        cls.url=f'http://127.0.0.1:{cls.http.server_port}'

    @classmethod
    def tearDownClass(cls):
        cls.http.shutdown();cls.http.server_close();cls.thread.join()
        server.DATA,server.STATE=cls.old_data,cls.old_state
        cls.temp.cleanup()

    def post(self,path,payload,token=server.TOKEN):
        req=Request(self.url+path,data=json.dumps(payload).encode(),headers={'Content-Type':'application/json','X-Local-Token':token})
        with urlopen(req) as response:return json.load(response)

    def test_preview_png_and_no_disk_save(self):
        result=self.post('/api/preview',{'project':new_project()})
        self.assertFalse(server.STATE.exists())
        with urlopen(self.url+f'/previews/{result["id"]}/3.png') as response:
            self.assertEqual(response.headers['Content-Type'],'image/png')
            self.assertTrue(response.read().startswith(b'\x89PNG'))

    def test_preview_requires_local_token(self):
        with self.assertRaises(HTTPError) as error:self.post('/api/preview',{'project':new_project()},token='bad')
        self.assertEqual(error.exception.code,403)

    def test_math_preview_uses_same_pdf_engine_without_saving(self):
        project=demo_project()
        q=next(q for q in project['questions'] if q['area']=='mathematics')
        q['stem']=r'Calcula \(\frac{1}{\sqrt{x_1^2+1}}\).'
        result=self.post('/api/preview',{'project':project})
        self.assertFalse(server.STATE.exists())
        raw=server.PREVIEWS[result['id']]
        with pymupdf.open(stream=raw,filetype='pdf') as doc:
            page=doc[result['page_map'][q['id']]-1]
            self.assertGreater(len(page.get_drawings()),0)
        with urlopen(self.url+f'/previews/{result["id"]}/{result["page_map"][q["id"]]}.png') as response:
            self.assertTrue(response.read().startswith(b'\x89PNG'))

    def test_invalid_math_is_400_not_saved_or_reported_as_success(self):
        project=demo_project()
        next(q for q in project['questions'] if q['area']=='mathematics')['stem']=r'\(\frac{a}\)'
        with self.assertRaises(HTTPError) as error:
            self.post('/api/preview',{'project':project})
        self.assertEqual(error.exception.code,400)
        self.assertFalse(server.STATE.exists())

    def test_live_assets_available(self):
        with urlopen(self.url+'/live.css') as response:self.assertEqual(response.status,200)

    def test_generate_endpoint_returns_three_downloadable_pdfs(self):
        p=demo_project()
        with patch.object(server,'load',return_value=p),patch.object(server,'ROOT',Path(self.temp.name)):
            result=self.post('/api/generate',{'revision':p['revision']})
            for key in ('student','solved','teacher'):
                with urlopen(self.url+result[key]) as response:
                    self.assertTrue(response.read().startswith(b'%PDF'))
            self.assertNotEqual(result['student'],result['solved'])

    def test_missing_preview_page_has_clear_404(self):
        with self.assertRaises(HTTPError) as error:urlopen(self.url+'/previews/missing/1.png')
        self.assertEqual(error.exception.code,404)

    def test_unfinished_gap_does_not_save_or_crash(self):
        p=demo_project();p['session']='second'
        next(q for q in p['questions'] if q.get('part')==4)['slot']='not-in-text'
        with self.assertRaises(HTTPError) as error:self.post('/api/preview',{'project':p})
        self.assertEqual(error.exception.code,400)
        self.assertFalse(server.STATE.exists())


if __name__=='__main__':unittest.main()
