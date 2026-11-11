"""Read-only regressions: no saved project, PDFs, uploads or screenshots are created."""
import copy
import unittest
from unittest.mock import Mock, patch
from reportlab.platypus import Spacer
from editor_model import demo_project, validate_project
from editor_pdf import Interior, H, BOTTOM, matching_descriptions, BubbleRow


class IntegrityTests(unittest.TestCase):
    def test_export_requires_exactly_one_allowed_answer_letter(self):
        for value in ('',None,'AB','BCD','A ','a',[],False,1):
            with self.subTest(value=value):
                project=demo_project()
                project['questions'][0]['correct']=value
                with self.assertRaisesRegex(ValueError,'clave válida'):
                    validate_project(project,exporting=True)

    def test_missing_answer_remains_saveable_as_draft(self):
        project=demo_project()
        project['questions'][0]['correct']=''
        validate_project(project,exporting=False)

    def test_order_types_rejected_without_changing_project(self):
        for value in ('1', None, -1, 1.5, True):
            with self.subTest(value=value):
                project = demo_project()
                project['questions'][0]['order'] = value
                original = copy.deepcopy(project)
                with self.assertRaisesRegex(ValueError, 'entero no negativo'):
                    validate_project(project)
                self.assertEqual(project, original)

    def test_duplicate_order_warns_in_draft_and_blocks_export(self):
        project = demo_project()
        first, second = project['questions'][:2]
        second['order'] = first['order']
        self.assertTrue(any('orden repetido' in w for w in validate_project(project)))
        with self.assertRaisesRegex(ValueError, 'orden repetido'):
            validate_project(project, exporting=True)

    def test_same_order_in_different_areas_is_allowed(self):
        project = demo_project()
        project['questions'][2]['order'] = project['questions'][0]['order']
        validate_project(project, exporting=True)

    def test_missing_topics_warn_without_inventing_classification(self):
        project = demo_project()
        project['questions'][0]['topic'] = ''
        original = copy.deepcopy(project)
        notes = validate_project(project, exporting=True)
        self.assertTrue(any('falta tema y subtema' in note for note in notes))
        self.assertEqual(project, original)

    def test_gap_question_image_is_not_discarded(self):
        project = demo_project()
        book = Interior.__new__(Interior)
        for part in (4, 7):
            question = next(q for q in project['questions'] if q['area'] == 'english' and q['part'] == part)
            question['image'] = 'assets/uploads/placeholder.png'
            with patch('editor_pdf.picture', return_value=Spacer(1, 70)) as picture:
                flows, _, compact = book.question_flows(question, 1)
                self.assertFalse(compact)
                picture.assert_called_once()
                self.assertGreater(book.question_height(question, 1), 70)

    def test_shared_context_reserves_actual_question_height(self):
        book = Interior.__new__(Interior)
        book.question_height = Mock(return_value=310)
        book.full = Mock()
        flows = [Spacer(1, 70)]
        question = {'id': 'first'}
        book.shared_context(flows, question, 8)
        book.full.assert_called_once_with(flows, True, reserve=324)

    def test_matching_image_and_answer_bubble_are_both_preserved(self):
        question = {'id': 'match', 'stem': 'Description', 'correct': 'G',
                    'image': 'assets/uploads/placeholder.png'}
        with patch('editor_pdf.picture', return_value=Spacer(1, 70)) as picture:
            flows = matching_descriptions(object(), [question], {'match': 12})
        picture.assert_called_once()
        rows = [flow for flow in flows if isinstance(flow, BubbleRow)]
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0].answer, 'G')

    def test_oversized_context_and_question_fail_before_drawing(self):
        book = Interior.__new__(Interior)
        book.question_height = Mock(return_value=400)
        book.full = Mock()
        with self.assertRaisesRegex(ValueError, 'primera pregunta no caben juntos'):
            book.shared_context([Spacer(1, H-83-BOTTOM-300)], {'id': 'first'}, 1)
        book.full.assert_not_called()

    def test_resolved_appendix_header_and_notice(self):
        book = Interior.__new__(Interior)
        book.c = Mock()
        book.project = {'code': 'SP-TEST', 'session': 'second'}
        book.page, book.open, book.area, book.resolved = 9, False, '', True
        book.newpage('RESPUESTAS EXPLICADAS')
        right_text = [call.args[-1] for call in book.c.drawRightString.call_args_list]
        self.assertIn('SP-TEST · RESUELTO', right_text)
        self.assertNotIn('SP-TEST · BORRADOR', right_text)
        self.assertTrue(any('COMPARTIR DESPUES' in call.args[-1]
                            for call in book.c.drawString.call_args_list))


if __name__ == '__main__':
    unittest.main()
