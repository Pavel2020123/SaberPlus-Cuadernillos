"""Verify flow order without generating PDFs or loading user images."""
import unittest
from unittest.mock import patch
from editor_pdf import Interior, matching_descriptions


class QuestionImageOrderTests(unittest.TestCase):
    def question(self):
        return dict(id='q1', area='mathematics', part=0, layout='columns',
                    introduction='Observe la gráfica.', stem='¿Qué tendencia tiene?',
                    image='unused', options=[dict(text='A')], correct='A')

    def test_introduction_image_question_options(self):
        book=object.__new__(Interior)
        with patch('editor_pdf.picture', return_value='IMAGE'):
            flows, _, _=book.question_flows(self.question(), 7)
        # The number is a bold hanging label, not part of the paragraph text.
        self.assertEqual((getattr(flows[0],'bulletText',None) or ''), '7.')
        self.assertEqual(flows[0].getPlainText(), 'Observe la gráfica.')
        self.assertEqual(flows[2], 'IMAGE')
        self.assertEqual(flows[4].getPlainText(), '¿Qué tendencia tiene?')

    def test_legacy_image_stem_moves_below_image_without_text_loss(self):
        question=self.question(); question.pop('introduction')
        with patch('editor_pdf.picture', return_value='IMAGE'):
            flows, _, _=Interior.question_flows(object.__new__(Interior), question, 7)
        self.assertEqual((getattr(flows[0],'bulletText',None) or ''), '7.')
        self.assertEqual(flows[2], 'IMAGE')
        self.assertEqual(flows[4].getPlainText(), question['stem'])

    def test_legacy_text_only_keeps_number_and_stem_together(self):
        question=self.question(); question.pop('introduction');question.pop('image')
        flows, _, _=Interior.question_flows(object.__new__(Interior), question, 7)
        self.assertEqual(getattr(flows[0],'bulletText',None), '7.')
        self.assertEqual(flows[0].getPlainText(), '¿Qué tendencia tiene?')

    def test_matching_uses_same_order(self):
        with patch('editor_pdf.picture', return_value='IMAGE'):
            flows=matching_descriptions(None,[self.question()],{'q1':7})
        self.assertEqual(flows[2].getPlainText(), '7. Observe la gráfica.')
        self.assertEqual(flows[4], 'IMAGE')
        self.assertEqual(flows[6].getPlainText(), '¿Qué tendencia tiene?')


if __name__=='__main__':unittest.main()
