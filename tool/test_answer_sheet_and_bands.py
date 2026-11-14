"""Answer sheet: one row per question, readable A-G rows; context members share balanced bands."""
import copy
import re
import tempfile
import unittest
from pathlib import Path
import pymupdf
from editor_model import demo_project,selected_questions
from editor_pdf import generate,letters_for,AREAS


class AnswerSheetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp=tempfile.TemporaryDirectory()
        cls.project=demo_project();cls.project['session']='second'
        cls.out=Path(cls.temp.name)
        cls.result=generate(cls.project,cls.out)
        cls.selected=selected_questions(cls.project)

    @classmethod
    def tearDownClass(cls):cls.temp.cleanup()

    def test_one_row_per_question_with_brand_header_and_no_university(self):
        with pymupdf.open(self.out/'cuadernillo.pdf') as student:
            sheet=student[-1];text=sheet.get_text()
            self.assertIn('SABERPLUS',text)
            self.assertIn(f'PRUEBA DE {len(self.selected)} PREGUNTAS',text)
            self.assertIn('NOMBRE Y APELLIDO',text)
            self.assertIn('IDENTIFICACIÓN',text)
            self.assertNotIn('UNIVERSIDAD',text.upper())
            numbers=[int(n) for n in re.findall(r'(?m)^(\d+)\.$',text)]
            self.assertEqual(sorted(numbers),list(range(1,len(self.selected)+1)))

    def test_watermark_is_not_text(self):
        with pymupdf.open(self.out/'cuadernillo.pdf') as student:
            words=[w[4] for w in student[-1].get_text('words')]
            self.assertNotIn('S',words)

    def test_bubbles_do_not_overlap_and_letters_match_key(self):
        with pymupdf.open(self.out/'clave_docente.pdf') as key:
            circles=[d['rect'] for d in key[0].get_drawings() if d['items'] and d['items'][0][0]=='c'
                     and 10<=d['rect'].width<=12.5]
            expected=sum(len(letters_for(q)) for q in self.selected)
            self.assertGreaterEqual(len(circles),expected)
            for i,a in enumerate(circles):
                for b in circles[i+1:]:
                    inter=a&b
                    self.assertFalse(inter.width>0.4 and inter.height>0.4,(a,b))

    def test_context_members_in_columns_join_balanced_band(self):
        project=demo_project();project['session']='first';project['column_flow']='balanced'
        members=[q for q in selected_questions(project) if q.get('context')=='ctx-reading']
        self.assertEqual(len(members),2)
        for q in members:
            q['layout']='columns';q['options_layout']='vertical'
        with tempfile.TemporaryDirectory() as folder:
            result=generate(project,Path(folder),preview=True)
            self.assertEqual(result['page_map'][members[0]['id']],result['page_map'][members[1]['id']])
            with pymupdf.open(Path(folder)/'cuadernillo.pdf') as doc:
                page=doc[result['page_map'][members[0]['id']]-1]
                x=[page.search_for(q['stem'][:25])[0].x0 for q in members]
            # Left and right columns, not both stacked on the left.
            self.assertGreater(x[1]-x[0],150)


if __name__=='__main__':
    unittest.main()
