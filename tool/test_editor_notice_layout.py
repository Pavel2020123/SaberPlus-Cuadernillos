"""Notice examples and scored answers stay separate in paired English layouts."""
import copy
import tempfile
import unittest
from pathlib import Path
import pymupdf
from editor_model import demo_project,validate_project
from editor_pdf import generate


class NoticeLayoutTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp=tempfile.TemporaryDirectory()
        cls.folder=Path(cls.temp.name)
        project=demo_project();project['session']='second'
        base=next(q for q in project['questions'] if q['area']=='english' and q['part']==2)
        ctx=copy.deepcopy(next(c for c in project['contexts'] if c['id']==base['context']))
        ctx.update(notice_layout='paired',example_notice='Food for your pet',
                   example_options=['in a shop','in a lift','in a hospital'],example_answer='A',
                   range_heading='RESPONDA LAS PREGUNTAS {{desde}} A {{hasta}}',instructions='Where can you see these notices?')
        questions=[]
        for i,(text,answer) in enumerate([('Return your glasses here','B'),('Small pets can play here','C')],1):
            q=copy.deepcopy(base)
            q.update(id='q-notice-'+str(i),order=i,stem=text,introduction='',image=None,
                     options=[{'text':'in a restaurant'},{'text':'in a cinema'},{'text':'in a park'}],
                     correct=answer,layout='full',notice_style='dark' if i==1 else 'light')
            questions.append(q)
        project['questions']=questions;project['contexts']=[ctx]
        cls.project=project;cls.before=copy.deepcopy(project)
        cls.result=generate(project,cls.folder)

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_one_part_heading_and_scored_items_printed_once(self):
        with pymupdf.open(self.folder/'cuadernillo.pdf') as doc:
            page=doc[self.result['page_map']['q-notice-1']-1]
            text=page.get_text()
            self.assertEqual(text.count('PARTE 2'),1)
            self.assertEqual(text.count('Return your glasses here'),1)
            self.assertEqual(text.count('Small pets can play here'),1)
            self.assertEqual(self.result['page_map']['q-notice-1'],self.result['page_map']['q-notice-2'])
        self.assertEqual(self.project,self.before)

    def test_only_worked_example_has_circles_in_question_page(self):
        with pymupdf.open(self.folder/'cuadernillo.pdf') as doc:
            page=doc[self.result['page_map']['q-notice-1']-1]
            circles=[d for d in page.get_drawings() if abs(d['rect'].width-16)<.1 and abs(d['rect'].height-16)<.1]
            self.assertEqual(len(circles),3)
            marked=[d for d in circles if d.get('fill') and max(d['fill'])<.8]
            self.assertEqual(len(marked),1)
            self.assertEqual(page.get_textbox(marked[0]['rect']).strip(),'A')
            inline_sheet_circles=[d for d in page.get_drawings() if abs(d['rect'].width-13)<.1 and abs(d['rect'].height-13)<.1]
            self.assertEqual(inline_sheet_circles,[])

    def test_solved_marks_scored_options_not_example(self):
        with pymupdf.open(self.folder/'cuadernillo_resuelto.pdf') as doc:
            page=doc[self.result['page_map']['q-notice-1']-1]
            marks=[d for d in page.get_drawings() if d.get('fill') and d['fill'][0]>.9 and .8<d['fill'][1]<1 and d['fill'][2]<.6]
            self.assertEqual(len(marks),2)
            self.assertTrue(page.get_textbox(marks[0]['rect']).strip().startswith('B.'))
            self.assertTrue(page.get_textbox(marks[1]['rect']).strip().startswith('C.'))

    def test_incomplete_example_rejected(self):
        p=copy.deepcopy(self.project)
        p['contexts'][0]['example_answer']='H'
        with self.assertRaisesRegex(ValueError,'ejemplo de avisos'):
            validate_project(p,exporting=True)


if __name__=='__main__':
    unittest.main()
