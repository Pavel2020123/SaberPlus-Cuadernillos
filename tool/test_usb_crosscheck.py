import copy
import unittest
from usb_crosscheck_decisions import resolve, transform
from usb_export_question_reviews import item_area


class CrosscheckTests(unittest.TestCase):
    def test_resolve_chain(self):
        self.assertEqual(resolve(('c', 1), {('c', 1): ('b', 2), ('b', 2): ('a', 3)}), ('a', 3))

    def test_cycle_rejected(self):
        with self.assertRaises(ValueError):
            resolve(('a', 1), {('a', 1): ('b', 2), ('b', 2): ('a', 1)})

    def test_preserves_marks_and_redirects_previous_references(self):
        reviews = {'a': {'b': {'file_id': 'a', 'items': [{'question': 1, 'page': 2}]}},
                   'b': {'b': {'file_id': 'b', 'items': [{'question': 2, 'page': 3, 'observed_highlight': 'C'}]}},
                   'c': {'b': {'file_id': 'c', 'duplicate_occurrences': [
                       {'question': 8, 'page': 4, 'canonical_file_id': 'b', 'canonical_question': 2}]}}}
        archive = transform(reviews, {('b', 2): ('a', 1)}, {('b', 2): 'visual evidence'})
        self.assertEqual(len(archive), 1)
        self.assertEqual(archive[0]['item']['observed_highlight'], 'C')
        self.assertEqual(reviews['b']['b']['items'], [])
        self.assertEqual(reviews['b']['b']['duplicate_occurrences'][0]['source_observed_highlight'], 'C')
        self.assertEqual(reviews['c']['b']['duplicate_occurrences'][0]['canonical_file_id'], 'a')
        self.assertEqual(reviews['c']['b']['duplicate_occurrences'][0]['canonical_page'], 2)

    def test_unknown_target_rejected_before_mutation(self):
        reviews = {'a': {'b': {'file_id': 'a', 'items': [{'question': 1, 'page': 2}]}}}
        old = copy.deepcopy(reviews)
        with self.assertRaises(ValueError):
            transform(reviews, {('a', 1): ('missing', 2)}, {('a', 1): 'x'})
        self.assertEqual(reviews, old)

    def test_mixed_batch_uses_section_area(self):
        review = {'s': {'structure': {'sections': [
            {'area': 'Sociales', 'questions': [1, 25]},
            {'area': 'Matemáticas', 'questions': [26, 50]}]}}}
        self.assertEqual(item_area(review, {'question': 27}, {'area': 'Sociales y Matemáticas'}), 'Matemáticas')

    def test_individual_area_takes_precedence(self):
        self.assertEqual(item_area({}, {'area': 'Inglés', 'question': 1}, {}), 'Inglés')

    def test_old_schema_fallback(self):
        self.assertEqual(item_area({}, {'question': 1}, {'area': 'Matematicas'}), 'Matematicas')


if __name__ == '__main__':
    unittest.main()
