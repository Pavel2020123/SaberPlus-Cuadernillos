"""Regressions for separate English parts and four-choice cloze readings."""
import tempfile
import unittest
from pathlib import Path
import pymupdf
from editor_model import demo_project,selected_questions
from editor_pdf import generate,Interior,cloze_flows

class UniformEnglishTests(unittest.TestCase):
    def test_parts_never_share_a_page_when_requested(self):
        p=demo_project();p['session']='second';p['questions']=[q for q in p['questions'] if q['area']=='english'];p['english_separate_parts']=True
        with tempfile.TemporaryDirectory() as folder:
            result=generate(p,folder,preview=True);owners={}
            for q in selected_questions(p):
                page=result['page_map'][q['id']]
                if page in owners:self.assertEqual(owners[page],q['part'])
                owners[page]=q['part']

    def test_part_seven_keeps_four_options_and_its_heading(self):
        q={'id':'english-four','stem':'Complete','slot':'gap','correct':'D','options':[{'text':t} for t in ('firstchoice','secondchoice','thirdchoice','fourthchoice')]}
        ctx={'part':7,'title':'Reading','text':'The answer is {{gap}}.','range_heading':'Preguntas {{desde}} a {{hasta}}','instructions':'Choose a word.','example_options':['one','two','three','four'],'use_reading_panel':True}
        with tempfile.TemporaryDirectory() as folder:
            file=Path(folder)/'test.pdf';book=Interior(str(file),demo_project());book.newpage();book.full(cloze_flows(book,ctx,[q],{q['id']:132}));book.c.save()
            with pymupdf.open(file) as pdf:
                text=''.join(pg.get_text() for pg in pdf)
                self.assertIn('PARTE 7',text);self.assertNotIn('PARTE 4',text)
                for option in q['options']:self.assertIn(option['text'],text)
            self.assertEqual(len(book.answer_marks),1)

if __name__=='__main__':unittest.main()
