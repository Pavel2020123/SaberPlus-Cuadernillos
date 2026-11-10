"""Area changes and group instructions must follow the selected question order."""
import tempfile
import unittest
from pathlib import Path
import pymupdf
from editor_model import demo_project,range_heading,validate_project,selected_questions
from editor_pdf import generate


class HeadingTests(unittest.TestCase):
    def test_range_tokens_and_singular_default(self):
        self.assertEqual(range_heading('Del {{desde}} al {{hasta}}: {{cantidad}} ítems',3,5),'Del 3 al 5: 3 ítems')
        self.assertIn('LA PREGUNTA 4',range_heading('',4,4))
        self.assertNotIn('4 A 4',range_heading('',4,4))

    def test_unknown_heading_token_is_rejected(self):
        p=demo_project();p['contexts'][0]['range_heading']='Responda {{h1}}'
        with self.assertRaisesRegex(ValueError,'desde'):validate_project(p)

    def test_long_area_title_rejected(self):
        p=demo_project();p['area_headers']={'mathematics':{'title':'x'*121}}
        with self.assertRaisesRegex(ValueError,'120'):validate_project(p)

    def test_legacy_project_without_area_headers_stays_valid(self):
        p=demo_project();p.pop('area_headers',None)
        validate_project(p,exporting=True)

    def test_real_pdf_group_range_changes_after_excluding_question(self):
        p=demo_project()
        p['area_headers']={'reading':{'title':'COMPRENSIÓN Y LECTURA','instructions':'Esta sección reúne {{cantidad}} preguntas, desde {{desde}} hasta {{hasta}}.'}}
        ctx=next(c for c in p['contexts'] if c['id']=='ctx-reading')
        ctx['range_heading']='Responda del {{desde}} al {{hasta}} según el texto de referencia.'
        ctx['source']='Texto original de demostración editorial.'
        next(q for q in p['questions'] if q['id']=='q-demo-7')['included']=False
        selected=selected_questions(p);numbers={q['id']:i for i,q in enumerate(selected,1)}
        with tempfile.TemporaryDirectory() as folder:
            result=generate(p,folder,preview=True)
            with pymupdf.open(Path(folder)/'cuadernillo.pdf') as pdf:
                page=pdf[result['page_map']['q-demo-1']-1]
                text=page.get_text()
                self.assertIn('COMPRENSIÓN Y LECTURA',text)
                self.assertIn('desde 3 hasta 4',text)
                self.assertIn('Responda del 3 al 4',text)
                self.assertIn('Fuente: Texto original',text)
                self.assertEqual(numbers['q-demo-1'],3)
                math_page=result['page_map']['q-demo-5']
                self.assertLess(math_page,result['page_map']['q-demo-1'])
                self.assertNotIn('COMPRENSIÓN Y LECTURA',pdf[math_page-1].get_text())
                math_text=pdf[math_page-1].get_text()
                self.assertEqual(math_text.count('MATEMÁTICAS'),1)
                self.assertNotIn('3 preguntas',math_text)


if __name__=='__main__':unittest.main()
