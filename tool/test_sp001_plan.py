"""Coverage planning checks; never generate PDFs or mutate editorial projects."""
import json
import unittest
from collections import Counter
from pathlib import Path
from assessment_metadata import CATALOG
from editor_model import SESSIONS

PLAN = Path(__file__).resolve().parents[1]/'planning/SP001_MATRIZ_COBERTURA.json'


class CoveragePlanTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.plan = json.loads(PLAN.read_text(encoding='utf-8'))
        cls.slots = cls.plan['slots']

    def test_total_and_session_area_counts(self):
        self.assertEqual(len(self.slots),254)
        self.assertEqual(Counter(s['session'] for s in self.slots),{'first':120,'second':134})
        self.assertEqual(Counter((s['session'],s['area']) for s in self.slots),{
            ('first','mathematics'):25,('first','reading'):41,('first','social'):25,('first','science'):29,
            ('second','social'):25,('second','mathematics'):25,('second','science'):29,('second','english'):55})

    def test_unique_stable_ids_and_session_numbering(self):
        self.assertEqual(len({s['slot_id'] for s in self.slots}),254)
        for session,total in [('first',120),('second',134)]:
            numbers=[s['provisional_number'] for s in self.slots if s['session']==session]
            self.assertEqual(numbers,list(range(1,total+1)))

    def test_area_order_matches_current_editor_profile(self):
        self.assertEqual(self.plan['area_order'],SESSIONS)
        for session,areas in SESSIONS.items():
            sequence=list(dict.fromkeys(s['area'] for s in self.slots if s['session']==session))
            self.assertEqual(sequence,areas)

    def test_global_cognitive_targets(self):
        expected={
            'mathematics':{'interpretation':17,'execution':22,'argumentation':11},
            'reading':{'local':10,'relational':17,'critical':14},
            'social':{'social_thinking':15,'perspectives':20,'systems':15},
            'science':{'knowledge':18,'explanation':17,'inquiry':23},
        }
        for area,counts in expected.items():
            key='process' if area=='reading' else 'competency'
            self.assertEqual(Counter(s['target'][key] for s in self.slots if s['area']==area),counts)

    def test_per_session_targets_match_declared_quotas(self):
        components=['biological','physical','chemical','cts']
        for session,areas in self.plan['quotas'].items():
            for area,quotas in areas.items():
                slots=[s for s in self.slots if s['session']==session and s['area']==area]
                for key,count in quotas.items():
                    if area=='science':
                        actual=Counter(s['target']['component'] for s in slots if s['target']['competency']==key)
                        self.assertEqual([actual[c] for c in components],count)
                    else:
                        field='part' if area=='english' else 'process' if area=='reading' else 'competency'
                        self.assertEqual(sum(str(s['target'][field])==key for s in slots),count)

    def test_science_joint_matrix_and_component_totals(self):
        components=['biological','physical','chemical','cts']
        for competency,counts in [('knowledge',[6,5,5,2]),('explanation',[5,5,5,2]),('inquiry',[7,7,7,2])]:
            actual=Counter(s['target']['component'] for s in self.slots
                           if s['area']=='science' and s['target']['competency']==competency)
            self.assertEqual([actual[c] for c in components],counts)
        self.assertEqual(Counter(s['target']['component'] for s in self.slots if s['area']=='science'),
                         {'biological':18,'physical':17,'chemical':17,'cts':6})

    def test_english_parts_counts_and_order(self):
        english=[s for s in self.slots if s['area']=='english']
        self.assertEqual(Counter(s['target']['part'] for s in english),{1:5,2:6,3:6,4:10,5:9,6:6,7:13})
        parts=[s['target']['part'] for s in english]
        self.assertEqual(parts,sorted(parts))
        self.assertEqual([s['provisional_number'] for s in english],list(range(80,135)))
        self.assertTrue(any('adaptacion' in note.lower() for note in self.plan['notes']))

    def test_catalog_targets_do_not_invent_item_classifications(self):
        for slot in self.slots:
            area=slot['area']; target=slot['target']; catalog=CATALOG['areas'][area]
            self.assertIn(target['competency'],catalog['competencies'])
            if area=='reading':
                self.assertEqual(target['competency'],'reading')
                self.assertIn(target['process'],catalog['processes'])
            else:
                self.assertIsNone(target['process'])
            if area=='science':
                self.assertIn(target['component'],catalog['components'])
            else:
                self.assertIsNone(target['component'])
            if area=='english':
                self.assertIn(str(target['part']),catalog['parts'])
            else:
                self.assertIsNone(target['part'])
            self.assertNotIn('assessment',slot)
            self.assertNotIn('reviewer',target)
            self.assertNotIn('evidence',target)

    def test_assignment_ids_cannot_repeat_between_slots(self):
        assigned=[s['question_id'] for s in self.slots if s['question_id'] is not None]
        self.assertEqual(len(assigned),len(set(assigned)),
                         'Un mismo ID canonico no puede ocupar dos puestos del simulacro.')

    def test_plan_is_not_an_importable_editor_project(self):
        self.assertEqual(self.plan['kind'],'editorial_coverage_plan_not_editor_project')
        self.assertNotIn('schema',self.plan)
        self.assertNotIn('questions',self.plan)
        self.assertEqual(self.plan['reference']['framework'],CATALOG['id'])
        self.assertFalse(self.plan['scope']['auxiliary_questionnaires'])
        self.assertEqual(self.plan['scope']['minutes_per_session'],270)

    def test_question_policy_is_source_pdfs_only(self):
        self.assertEqual(self.plan['question_policy'],'source_pdf_only_no_new_or_rewritten_questions')
        self.assertFalse(self.plan['new_question_proposals_allowed'])


if __name__ == '__main__':
    unittest.main()
