"""Conversation prompts stay opposite A-C choices, with one shared example."""
import copy
import tempfile
import unittest
from pathlib import Path
import pymupdf
from editor_model import demo_project,validate_project
from editor_pdf import generate


class DialogueLayoutTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp=tempfile.TemporaryDirectory();cls.folder=Path(cls.temp.name)
        p=demo_project();p['session']='second'
        base=next(q for q in p['questions'] if q['area']=='english' and q['part']==3)
        cid='ctx-dialogue-test'
        p['contexts']=[dict(id=cid,area='english',part=3,title='',layout='full',dialogue_layout='paired',
                            instructions='Complete the conversations.',text='',words=[],
                            example='How are things? A. Not bad. B. Too long. C. Nothing else. Respuesta: A.')]
        p['questions']=[]
        for i,(stem,key) in enumerate([('Why are they hiding?','B'),('This film is about a family.','A')],1):
            q=copy.deepcopy(base)
            q.update(id='q-dialogue-'+str(i),context=cid,order=i,stem=stem,introduction='',image=None,
                     layout='full',options=[{'text':'Is it good?'},{'text':'I have no idea.'},{'text':'Come here!'}],correct=key)
            p['questions'].append(q)
        cls.before=copy.deepcopy(p);cls.project=p;cls.result=generate(p,cls.folder)

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_prompts_once_and_options_to_the_right(self):
        with pymupdf.open(self.folder/'cuadernillo.pdf') as doc:
            page=doc[self.result['page_map']['q-dialogue-1']-1]
            text=page.get_text()
            self.assertEqual(text.count('PARTE 3'),1)
            self.assertEqual(text.count('Why are they hiding?'),1)
            prompt=page.search_for('Why are they hiding?')[0]
            options=[rect for rect in page.search_for('A. Is it good?') if rect.y0>prompt.y0-4]
            self.assertTrue(options)
            self.assertGreater(options[0].x0,prompt.x1)
            circles=[d for d in page.get_drawings() if abs(d['rect'].width-13)<.1 and abs(d['rect'].height-13)<.1]
            self.assertEqual(circles,[])
        self.assertEqual(self.project,self.before)

    def test_solved_highlights_two_scored_answers(self):
        with pymupdf.open(self.folder/'cuadernillo_resuelto.pdf') as doc:
            page=doc[self.result['page_map']['q-dialogue-1']-1]
            marks=[d for d in page.get_drawings() if d.get('fill') and d['fill'][0]>.9 and .8<d['fill'][1]<1 and d['fill'][2]<.6]
            self.assertEqual(len(marks),2)
            self.assertTrue(page.get_textbox(marks[0]['rect']).strip().startswith('B.'))
            self.assertTrue(page.get_textbox(marks[1]['rect']).strip().startswith('A.'))

    def test_pair_layout_is_only_for_part_three(self):
        p=copy.deepcopy(self.project);p['contexts'][0]['part']=2
        with self.assertRaisesRegex(ValueError,'conversaciones'):
            validate_project(p)


if __name__=='__main__':
    unittest.main()
