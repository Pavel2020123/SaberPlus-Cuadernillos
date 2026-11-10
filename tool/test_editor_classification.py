"""Editorial classification does not require or claim teacher validation."""
import copy
import unittest
from unittest.mock import patch
from assessment_metadata import STATUS_LABELS, append_teacher_pages
from editor_model import demo_project, validate_project, blank_assessment


class EditorialClassificationTests(unittest.TestCase):
    def test_competency_only_editorial_classification_is_valid(self):
        project=demo_project()
        question=next(q for q in project['questions'] if q['area']=='mathematics')
        question['assessment']={**blank_assessment('mathematics'),
            'status':'proposed','competency':'execution',
            'rationale':'Aplica el cálculo de la media aritmética.'}
        before=copy.deepcopy(project)
        validate_project(project,exporting=True)
        self.assertEqual(before,project)

    def test_evidence_without_claim_still_fails(self):
        project=demo_project()
        question=next(q for q in project['questions'] if q['area']=='mathematics')
        question['assessment']={**blank_assessment('mathematics'),
            'status':'proposed','competency':'execution','evidence':'2.1',
            'rationale':'No inventar una afirmación a partir de la evidencia.'}
        with self.assertRaisesRegex(ValueError,'antes de indicar evidencia'):
            validate_project(project,exporting=True)

    def test_complete_editorial_classification_exports_without_reviewer(self):
        project=demo_project()
        for question in project['questions']:
            if question['area']=='mathematics':
                question['assessment']={**blank_assessment('mathematics'),
                    'status':'proposed','competency':'interpretation','claim':'1','evidence':'1.1',
                    'rationale':'Clasificación editorial de prueba, no validación docente.'}
                self.assertIsNone(question['assessment']['reviewer'])
                self.assertIsNone(question['assessment']['reviewed_at'])
        original=copy.deepcopy(project)
        notes=validate_project(project,exporting=True)
        self.assertEqual(project,original)
        self.assertFalse(any('pendientes de revisión' in note for note in notes))

    def test_unclassified_warning_is_not_a_teacher_requirement(self):
        project=demo_project()
        project['questions'][0]['assessment']=blank_assessment('reading')
        notes=validate_project(project,exporting=True)
        self.assertIn('Hay preguntas sin clasificación por competencia.',notes)
        self.assertFalse(any('docente' in note.lower() for note in notes))

    def test_invalid_editorial_mapping_still_fails(self):
        project=demo_project()
        question=next(q for q in project['questions'] if q['area']=='mathematics')
        question['assessment']={**blank_assessment('mathematics'),
            'status':'proposed','competency':'interpretation','claim':'3','evidence':'3.1',
            'rationale':'No debe aceptar una afirmación ajena a esta competencia.'}
        with self.assertRaisesRegex(ValueError,'afirmación no pertenece'):
            validate_project(project,exporting=True)

    def test_editorial_label_does_not_claim_review(self):
        self.assertEqual(STATUS_LABELS['proposed'],'Clasificación editorial SaberPlus')
        self.assertNotIn('revisada',STATUS_LABELS['proposed'].lower())

    def test_auxiliary_guide_uses_editorial_language_without_creating_pdf(self):
        class Book:
            def __init__(self):self.text=[];self.rows=[]
            def start(self,text):self.text.append(text);return 700
            def p(self,text,y,size):self.text.append(text);return y-20
            def table(self,rows,*args):self.rows.extend(rows)
        book=Book()
        question=demo_project()['questions'][0]
        question={**question,'n':1}
        with patch.dict(question['assessment'],status='proposed'):
            append_teacher_pages(book,{'assessment_framework':question['assessment']['framework']},[question])
        self.assertIn('Clasificación editorial SaberPlus',book.text)
        self.assertNotIn('necesitan revisión docente',' '.join(book.text))
        self.assertEqual(book.rows[1][-1],'Clasificación editorial SaberPlus')


if __name__=='__main__':unittest.main()
