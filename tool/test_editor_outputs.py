"""Three public outputs share layout and keys; student output stays unanswered."""
import copy
import tempfile
import unittest
import io
from pathlib import Path
from unittest.mock import patch
import pymupdf
from PIL import Image as PillowImage
from reportlab.platypus import Image as PdfImage
from editor_model import demo_project,selected_questions
from editor_pdf import generate,letters_for


class OutputTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp=tempfile.TemporaryDirectory()
        cls.out=Path(cls.temp.name)
        cls.project=demo_project();cls.project['session']='second'
        cls.original=copy.deepcopy(cls.project)
        cls.result=generate(cls.project,cls.out)

    @classmethod
    def tearDownClass(cls):cls.temp.cleanup()

    def test_three_files_and_no_mutation(self):
        for key in ('student','solved','teacher'):
            self.assertTrue((self.out/self.result[key]).is_file())
        self.assertEqual(self.project,self.original)

    def test_same_questions_and_explanations_only_in_solved_appendix(self):
        with pymupdf.open(self.out/'cuadernillo.pdf') as student,pymupdf.open(self.out/'cuadernillo_resuelto.pdf') as solved:
            self.assertGreater(len(solved),len(student))
            for i,page in enumerate(student):
                student_lines=page.get_text().splitlines()
                solved_lines=solved[i].get_text().splitlines()
                for line in student_lines:
                    if line=='CUADERNILLO DEL ESTUDIANTE' or line.endswith(' · BORRADOR'):continue
                    self.assertIn(line,solved_lines)
            appendix=''.join(solved[i].get_text() for i in range(len(student),len(solved)))
            self.assertIn('RESPUESTAS EXPLICADAS',appendix)
            self.assertIn('Pregunta 20',appendix)
            text=''.join(page.get_text() for page in student)
            self.assertNotIn('RESPUESTAS EXPLICADAS',text)
            self.assertNotIn('Respuesta A',text)
            self.assertNotIn('(A)',text)
            self.assertIn('CUADERNILLO RESUELTO',solved[0].get_text())

    def test_circles_empty_for_student_filled_for_teacher(self):
        def bubbles(page,filled):
            # The 13 pt sample circle in the marking-example box is not an answer bubble (real ones are 11-12 pt).
            return [d for d in page.get_drawings() if 10<=d['rect'].width<=12.5 and 10<=d['rect'].height<=12.5 and d['items'][0][0]=='c'
                    and (d.get('fill') is not None and max(d['fill'])<.5)==filled]
        with pymupdf.open(self.out/'cuadernillo.pdf') as student,pymupdf.open(self.out/'clave_docente.pdf') as key:
            sheet=student[-1]
            self.assertTrue(bubbles(sheet,False))
            self.assertFalse(bubbles(sheet,True))
            marked=sum(len(bubbles(page,True)) for page in key)
            self.assertEqual(marked,len(selected_questions(self.project)))
            actual=[page.get_textbox(mark['rect']).strip()
                    for page in key for mark in bubbles(page,True)]
            self.assertEqual(actual,[q['correct'] for q in selected_questions(self.project)])

    def test_normal_and_gap_options_are_highlighted_only_in_solved(self):
        for qid in ('q-demo-3','q-demo-16','q-demo-21'):
            page_number=self.result['page_map'][qid]-1
            with pymupdf.open(self.out/'cuadernillo.pdf') as student,pymupdf.open(self.out/'cuadernillo_resuelto.pdf') as solved:
                def yellow(page):return [d for d in page.get_drawings() if d.get('fill') and d['fill'][0]>.9 and .8<d['fill'][1]<1 and d['fill'][2]<.6]
                self.assertFalse(yellow(student[page_number]))
                self.assertTrue(yellow(solved[page_number]))

    def test_matching_marks_and_available_letters(self):
        selected=selected_questions(self.project)
        self.assertEqual(letters_for(next(q for q in selected if q.get('part')==1)),'ABCDEFG')
        self.assertEqual(letters_for(next(q for q in selected if q.get('part')==2)),'ABC')
        self.assertEqual(letters_for(next(q for q in selected if q.get('part')==6)),'ABCD')
        number=self.result['page_map']['q-demo-11']-1
        with pymupdf.open(self.out/'cuadernillo.pdf') as student,pymupdf.open(self.out/'cuadernillo_resuelto.pdf') as solved:
            inline_circles=[d for d in student[number].get_drawings() if 12<=d['rect'].width<=14 and 12<=d['rect'].height<=14]
            self.assertEqual(inline_circles,[])
            marks=[d for d in solved[number].get_drawings() if d.get('fill') and d['fill'][0]>.9 and .8<d['fill'][1]<1 and d['fill'][2]<.6]
            self.assertGreaterEqual(len(marks),3)

    def test_appendix_keeps_resolved_header_and_notice(self):
        with pymupdf.open(self.out/'cuadernillo.pdf') as student,pymupdf.open(self.out/'cuadernillo_resuelto.pdf') as solved:
            for page in list(solved)[len(student):]:
                text=page.get_text()
                self.assertIn('SP-001 · RESUELTO',text)
                self.assertIn('COMPARTIR DESPUES',text)
                self.assertNotIn('SP-001 · BORRADOR',text)

    def test_special_format_images_and_image_option_highlight(self):
        project=copy.deepcopy(self.project)
        path='assets/uploads/'+('a'*32)+'.png'
        by_id={q['id']:q for q in project['questions']}
        for qid in ('q-demo-11','q-demo-16','q-demo-21'):
            by_id[qid]['image']=path
        question=by_id['q-demo-3']
        question['options']['ABCD'.index(question['correct'])]={'image':path}
        def fixture_picture(*args, **kwargs):
            image=io.BytesIO()
            PillowImage.new('RGB',(40,30),'#345678').save(image,format='PNG')
            image.seek(0)
            return PdfImage(image,width=40,height=30)
        with tempfile.TemporaryDirectory() as folder,patch('editor_pdf.picture',side_effect=fixture_picture):
            result=generate(project,folder)
            with pymupdf.open(Path(folder)/'cuadernillo.pdf') as student,pymupdf.open(Path(folder)/'cuadernillo_resuelto.pdf') as solved:
                for qid in ('q-demo-11','q-demo-16','q-demo-21','q-demo-3'):
                    page=result['page_map'][qid]-1
                    self.assertTrue(student[page].get_image_info(),qid)
                    self.assertTrue(solved[page].get_image_info(),qid)
                for qid in ('q-demo-16','q-demo-21'):
                    selected=selected_questions(project)
                    number=next(i for i,q in enumerate(selected,1) if q['id']==qid)
                    page=result['page_map'][qid]-1
                    self.assertIn(f'Choose the word for space {number}.',student[page].get_text())
                    self.assertNotIn('{{numero}}',student[page].get_text())
                page=result['page_map']['q-demo-3']-1
                images=solved[page].get_image_info()
                highlights=[d['rect'] for d in solved[page].get_drawings()
                            if d.get('fill') and d['fill'][0]>.9 and .8<d['fill'][1]<1 and d['fill'][2]<.6]
                self.assertTrue(any(rect.contains(pymupdf.Rect(image['bbox']))
                                    for rect in highlights for image in images))

    def test_long_context_and_first_question_remain_together(self):
        project=copy.deepcopy(self.project)
        question=next(q for q in project['questions'] if q['id']=='q-demo-5')
        context=next(c for c in project['contexts'] if c['id']==question['context'])
        context.update(title='Context QA continuity',text='\n'.join(['Context line']*18))
        context.pop('table',None)
        question['stem']='\n'.join(['Question line']*20)
        with tempfile.TemporaryDirectory() as folder:
            result=generate(project,folder)
            with pymupdf.open(Path(folder)/'cuadernillo.pdf') as doc:
                context_pages=[i+1 for i,page in enumerate(doc) if page.search_for('Context QA continuity')]
                self.assertEqual(context_pages,[result['page_map'][question['id']]])
                self.assertIn('Question line',doc[context_pages[0]-1].get_text())

    def test_long_context_and_question_are_preserved_on_separate_pages(self):
        project=copy.deepcopy(self.project)
        question=next(q for q in project['questions'] if q['id']=='q-demo-5')
        context=next(c for c in project['contexts'] if c['id']==question['context'])
        context['text']='\n'.join(['Context line']*30)
        context.pop('table',None)
        question['stem']='\n'.join(['Question line']*20)
        with tempfile.TemporaryDirectory() as folder:
            result=generate(project,folder)
            with pymupdf.open(Path(folder)/'cuadernillo.pdf') as doc:
                reading=[i+1 for i,page in enumerate(doc) if 'Context line' in page.get_text()]
                self.assertEqual(len(reading),1)
                self.assertEqual(doc[reading[0]-1].get_text().count('Context line'),30)
                question_page=result['page_map'][question['id']]
                self.assertGreater(question_page,reading[0])
                self.assertEqual(doc[question_page-1].get_text().count('Question line'),20)


if __name__=='__main__':unittest.main()
