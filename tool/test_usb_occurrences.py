import json
import unittest
from usb_export_question_reviews import collect_occurrences


class FakeConnection:
    def __init__(self, ref):
        self.row = dict(id='source', pages=5, current_path='source.pdf',
                        sha256='hash', review_json=json.dumps({
                            'batch': dict(file_id='source', items=[],
                                          duplicate_occurrences=[ref])}))

    def execute(self, _query):
        return [self.row]


class OccurrenceTests(unittest.TestCase):
    def ref(self, **changes):
        return dict(dict(question=3, page=2, canonical_file_id='canonical',
                         canonical_question=7, exact_content=True), **changes)

    def test_reference_does_not_copy_question(self):
        items = [dict(file_id='canonical', question=7)]
        refs = collect_occurrences(FakeConnection(self.ref()), items)
        self.assertEqual(len(items), 1)
        self.assertEqual(refs[0]['question'], 3)
        self.assertEqual(refs[0]['source_sha256'], 'hash')

    def test_similarity_is_not_exact_identity(self):
        with self.assertRaises(ValueError):
            collect_occurrences(FakeConnection(self.ref(exact_content=False)),
                                [dict(file_id='canonical', question=7)])

    def test_missing_target_rejected(self):
        with self.assertRaises(ValueError):
            collect_occurrences(FakeConnection(self.ref()), [])

    def test_page_outside_pdf_rejected(self):
        with self.assertRaises(ValueError):
            collect_occurrences(FakeConnection(self.ref(page=6)),
                                [dict(file_id='canonical', question=7)])


if __name__ == '__main__':
    unittest.main()
