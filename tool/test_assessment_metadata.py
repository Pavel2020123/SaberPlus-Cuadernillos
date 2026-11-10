import copy
import json
from pathlib import Path
import unittest
from generate_booklet_template import validate_bank


class AssessmentTests(unittest.TestCase):
    def setUp(self):
        self.bank = json.loads(Path(__file__).with_name('booklet_competency_sample.json').read_text(encoding='utf-8'))

    def test_sample_validates_with_explicit_pending(self):
        qs = validate_bank(self.bank)
        self.assertEqual(sum(q['assessment']['status'] == 'proposed' for q in qs), 14)
        self.assertEqual(sum(q['assessment']['status'] == 'unclassified' for q in qs), 8)

    def test_legacy_bank_remains_valid(self):
        bank = json.loads(Path(__file__).with_name('booklet_template_bank.json').read_text(encoding='utf-8'))
        self.assertEqual(len(validate_bank(bank)), 22)

    def reject(self):
        with self.assertRaises(ValueError):
            validate_bank(self.bank)

    def test_cross_area_rejected(self):
        self.bank['reading']['questions'][0]['assessment']['area'] = 'science'
        self.reject()

    def test_claim_must_belong_to_competency(self):
        self.bank['mathematics'][1]['assessment']['claim'] = '3'
        self.reject()

    def test_evidence_must_belong_to_claim(self):
        self.bank['mathematics'][1]['assessment']['evidence'] = '1.1'
        self.reject()

    def test_reading_process_must_match_claim(self):
        self.bank['reading']['questions'][0]['assessment']['process'] = 'critical'
        self.reject()

    def test_english_part_must_match_format(self):
        self.bank['english']['notice']['assessment']['part'] = 6
        self.reject()

    def test_english_cannot_inherit_claims(self):
        self.bank['english']['notice']['assessment']['claim'] = '1'
        self.reject()

    def test_review_requires_responsible_date(self):
        self.bank['mathematics'][1]['assessment']['status'] = 'reviewed'
        self.reject()

    def test_valid_review(self):
        a = self.bank['mathematics'][1]['assessment']
        a.update(status='reviewed', reviewer='Docente de prueba', reviewed_at='2026-10-28')
        self.assertEqual(len(validate_bank(self.bank)), 22)

    def test_pending_has_no_active_labels(self):
        self.bank['science'][0]['assessment']['competency'] = 'explanation'
        self.reject()

    def test_unknown_framework_rejected(self):
        self.bank['assessment_framework'] = 'unknown'
        self.reject()

    def test_validator_does_not_mutate_bank(self):
        before = copy.deepcopy(self.bank)
        validate_bank(self.bank)
        self.assertEqual(before, self.bank)


if __name__ == '__main__':
    unittest.main()
