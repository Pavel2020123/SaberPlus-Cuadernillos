"""Three public outputs share layout and keys; student output stays unanswered."""
import copy
import tempfile
import unittest
from pathlib import Path
import pymupdf
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
            return [d for d in page.get_drawings() if 12<=d['rect'].width<=14 and 12<=d['rect'].height<=14
                    and (d.get('fill') is not None and max(d['fill'])<.5)==filled]
        with pymupdf.open(self.out/'cuadernillo.pdf') as student,pymupdf.open(self.out/'clave_docente.pdf') as key:
            sheet=student[-1]
            self.assertTrue(bubbles(sheet,False))
            self.assertFalse(bubbles(sheet,True))
            marked=sum(len(bubbles(page,True)) for page in key)
            self.assertEqual(marked,len(selected_questions(self.project)))

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
        with pymupdf.open(self.out/'cuadernillo_resuelto.pdf') as solved:
            marks=[d for d in solved[number].get_drawings() if d.get('fill') and max(d['fill'])<.5 and 12<=d['rect'].width<=14]
            self.assertGreaterEqual(len(marks),3)


if __name__=='__main__':unittest.main()
