import copy
import unittest

from editor_model import blank_assessment, new_project, validate_project
from sync_used_questions import merge, remaining_reservations


def project(code, question_id, catalog_id=''):
    data = new_project()
    data['code'] = code
    data['questions'] = [{
        'id': question_id, 'area': 'mathematics', 'part': 0, 'order': 1,
        'topic': 'Tema', 'subtopic': 'Subtema', 'introduction': 'Datos',
        'stem': 'Pregunta idéntica', 'options': [{'text': str(i)} for i in range(4)],
        'correct': 'A', 'explanation': 'Razón', 'layout': 'columns',
        'included': True, 'context': None, 'catalog_id': catalog_id,
        'assessment': blank_assessment('mathematics'),
    }]
    return data


class UsageRegistryTests(unittest.TestCase):
    def test_same_question_in_two_simulacros_is_rejected(self):
        first = project('SP-001', 'q-a')
        ledger = {'preguntas': []}
        ledger['preguntas'], _ = merge(ledger, first, 'primera')
        _, clashes = merge(ledger, project('SP-002', 'q-b'), 'primera')
        self.assertIn('mismo texto normalizado', clashes[0][2])

    def test_same_editor_record_updates_without_freeing_prior_usage(self):
        original = project('SP-001', 'q-a')
        existing, _ = merge({'preguntas': []}, original, 'primera')
        updated = copy.deepcopy(original)
        updated['questions'][0]['catalog_id'] = 'USB-123456789abc-Q001'
        records, clashes = merge({'preguntas': existing}, updated, 'primera')
        self.assertFalse(clashes)
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]['catalog_id'], 'USB-123456789abc-Q001')
        updated['questions'][0]['included'] = False
        records, clashes = merge({'preguntas': records}, updated, 'primera')
        self.assertEqual(len(records), 1)

    def test_catalog_code_format_is_checked(self):
        item = project('SP-002', 'q-a', 'USB-123456789abc-Q001')
        validate_project(item)
        item['questions'][0]['catalog_id'] = 'Q1'
        with self.assertRaisesRegex(ValueError, 'código de catálogo'):
            validate_project(item)

    def test_same_catalog_code_blocks_changed_text(self):
        first = project('SP-001', 'q-a', 'USB-123456789abc-Q001')
        existing, _ = merge({'preguntas': []}, first, 'primera')
        second = project('SP-003', 'q-c', 'USB-123456789abc-Q001')
        second['questions'][0]['stem'] = 'Texto distinto'
        _, clashes = merge({'preguntas': existing}, second, 'primera')
        self.assertIn('mismo código de catálogo', clashes[0][2])

    def test_reservation_blocks_other_simulacro_but_not_owner(self):
        code = 'USB-123456789abc-Q002'
        ledger = {'preguntas': [], 'reservas': [{
            'simulacro': 'SP-001', 'sesion': 'primera', 'numero_actual': 42,
            'catalog_id': code,
        }]}
        _, clashes = merge(ledger, project('SP-002', 'q-b', code), 'primera')
        self.assertIn('código reservado', clashes[0][2])
        _, clashes = merge(ledger, project('SP-001', 'q-a', code), 'primera')
        self.assertFalse(clashes)

    def test_loaded_question_clears_only_its_own_reservation(self):
        code = 'USB-123456789abc-Q002'
        ledger = {'preguntas': [], 'reservas': [
            {'simulacro': 'SP-001', 'catalog_id': code},
            {'simulacro': 'SP-002', 'catalog_id': 'USB-123456789abc-Q003'},
        ]}
        used, clashes = merge(ledger, project('SP-001', 'q-a', code), 'primera')
        self.assertFalse(clashes)
        self.assertEqual(remaining_reservations(ledger, used), [ledger['reservas'][1]])


if __name__ == '__main__':
    unittest.main()
