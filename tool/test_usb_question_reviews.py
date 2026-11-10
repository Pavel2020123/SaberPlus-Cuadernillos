import json
import unittest
from usb_export_question_reviews import collect, review_html


class FakeConnection:
    def __init__(self, review):
        self.row = {'id': 'USB-fixture', 'current_path': 'fixture.pdf',
                    'original_path': 'original.pdf', 'sha256': 'fixture-hash',
                    'pages': 2, 'review_json': json.dumps(review)}

    def execute(self, _query):
        return [self.row]


def batch(question=1, page=1):
    return {'file_id': 'USB-fixture', 'scope': 'Test only', 'area': 'Matematicas',
            'items': [{'question': question, 'page': page, 'topic': '<unsafe>',
                       'competency_proposal': 'Argumentacion', 'answer_proposal': 'C',
                       'observed_highlight': 'A', 'reason': 'Independent reasoning'}]}


class QuestionReviewTests(unittest.TestCase):
    def test_handwriting_remains_separate_from_highlight_and_key(self):
        data = batch()
        data['items'][0]['observed_annotation'] = {
            'value': 'B', 'type': 'letra manuscrita', 'provenance': 'desconocida'}
        item = collect(FakeConnection({'one': data}))[0]
        self.assertEqual(item['answer_proposal'], 'C')
        self.assertEqual(item['observed_highlight'], 'A')
        self.assertEqual(item['annotation_value'], 'B')
        self.assertEqual(item['annotation_vs_proposal'], 'discrepa_de_propuesta')

    def test_ambiguous_handwriting_does_not_become_single_key(self):
        data = batch()
        data['items'][0]['observed_annotation'] = {'value': 'B/C', 'type': 'trazo dudoso'}
        item = collect(FakeConnection({'one': data}))[0]
        self.assertEqual(item['answer_proposal'], 'C')
        self.assertEqual(item['annotation_vs_proposal'], 'anotacion_no_univoca_o_clave_sin_cerrar')

    def test_highlight_never_overwrites_reasoned_key(self):
        item = collect(FakeConnection({'one': batch()}))[0]
        self.assertEqual(item['answer_proposal'], 'C')
        self.assertEqual(item['observed_highlight'], 'A')
        self.assertEqual(item['highlight_vs_proposal'], 'discrepa_de_propuesta')

    def test_repeated_number_in_separate_batches_rejected(self):
        with self.assertRaisesRegex(ValueError, 'Duplicate manual review'):
            collect(FakeConnection({'one': batch(), 'two': batch()}))

    def test_out_of_range_page_rejected(self):
        with self.assertRaisesRegex(ValueError, 'Invalid physical page'):
            collect(FakeConnection({'one': batch(page=3)}))

    def test_batch_attached_to_wrong_source_rejected(self):
        other = batch()
        other['file_id'] = 'USB-other'
        with self.assertRaisesRegex(ValueError, 'wrong source'):
            collect(FakeConnection({'one': other}))

    def test_html_escapes_source_text_and_preserves_warning(self):
        items = collect(FakeConnection({'one': batch()}))
        summary = {'academic_items_initially_reviewed': 1, 'excluded_self_report_items': 0,
                   'files_with_manual_question_reviews': 1, 'retained_files': 399}
        output = review_html(items, summary)
        self.assertIn('&lt;unsafe&gt;', output)
        self.assertNotIn('<unsafe>', output)
        self.assertIn('NO esta terminada', output)
        self.assertIn('fixture.pdf#page=1', output)


if __name__ == '__main__':
    unittest.main()
