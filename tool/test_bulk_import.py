"""Regression checks for the independent, reviewed PDF import pilot."""
import copy
import json
import unittest
from pathlib import Path

import pymupdf

from editor_model import inspect_project_import, selected_questions, validate_project
from import_booklet_questions import build_import, coordination_inputs, equivalent_codes, source_path


ROOT=Path(__file__).resolve().parents[1]


class BulkImportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base=json.loads((ROOT/'data/project.json').read_text(encoding='utf-8'))
        cls.manifest=json.loads((ROOT/'tool/manifests/sp002_social_five.json').read_text(encoding='utf-8'))
        cls.catalog=json.loads((ROOT/'output/cotejo_30/indice_editorial.json').read_text(encoding='utf-8'))
        archive=json.loads((ROOT/'output/cotejo_30/archivo_fichas_consolidadas.json').read_text(encoding='utf-8'))
        cls.expand=staticmethod(equivalent_codes(cls.catalog,archive))

    def test_requires_saved_66_question_base(self):
        shortened=copy.deepcopy(self.base)
        shortened['questions']=shortened['questions'][:63]
        with self.assertRaisesRegex(ValueError,'se requieren 66'):
            build_import(shortened,self.manifest,self.catalog,'D:/Icfes_SaberPlus')

    def test_blocks_active_candidate_and_equivalence(self):
        altered=copy.deepcopy(self.manifest)
        blocked={altered['questions'][0]['catalog_id']}
        with self.assertRaisesRegex(ValueError,'usado, candidato activo o equivalente'):
            build_import(self.base,altered,self.catalog,'D:/Icfes_SaberPlus',blocked,self.expand)

    def test_reviewed_pilot_preserves_all_prior_items_and_renders(self):
        # The actual OCR/PDF integration ran separately. This checks the saved pilot's invariants.
        pilot=ROOT/'output/pilots/sp002-social-71/project.json'
        self.assertTrue(pilot.is_file())
        imported=json.loads(pilot.read_text(encoding='utf-8'))
        validate_project(imported,exporting=True)
        self.assertEqual(imported['questions'][:66],self.base['questions'])
        self.assertEqual(imported['contexts'][:10],self.base['contexts'])
        self.assertEqual(len(imported['questions']),71)
        self.assertEqual([q['catalog_id'] for q in selected_questions(imported)[66:]],
                         [q['catalog_id'] for q in self.manifest['questions']])
        self.assertEqual([q['correct'] for q in selected_questions(imported)[66:]],list('DAACB'))
        with pymupdf.open(ROOT/'output/pilots/sp002-social-71/cuadernillo.pdf') as doc:
            answer=next(i for i,p in enumerate(doc) if 'HOJA DE RESPUESTAS' in p.get_text())
            body='\n'.join(p.get_text() for p in list(doc)[:answer])
            self.assertIn('71. En un pueblo panameño',body)
            self.assertIn('67. El 13 de enero de 1942',body)
            self.assertNotIn('72. ',body)

    def test_import_preflight_catches_missing_assets_and_duplicates(self):
        project=copy.deepcopy(self.base)
        self.assertTrue(inspect_project_import(project)['valid'])
        project['questions'][1]['catalog_id']=project['questions'][0]['catalog_id']
        self.assertFalse(inspect_project_import(project)['valid'])
        self.assertIn('repetido',' '.join(inspect_project_import(project)['errors']).lower())
        project['questions'][1]['catalog_id']=''
        project['questions'][1]['image']='assets/uploads/'+'f'*32+'.png'
        self.assertFalse(inspect_project_import(project)['valid'])

    def test_catalog_source_and_reservations_are_available(self):
        rows={r['catalog_id']:r for r in self.catalog}
        occupied=coordination_inputs()
        for item in self.manifest['questions']:
            code=item['catalog_id']
            self.assertFalse(self.expand(code)&occupied)
            self.assertTrue(source_path(rows[code],'D:/Icfes_SaberPlus').is_file())

    def test_91_question_pilot_preserves_base_and_visual_resources(self):
        pilot=ROOT/'output/pilots/sp002-social-91'
        previous=json.loads((ROOT/'output/pilots/sp002-social-71/project.json').read_text(encoding='utf-8'))
        project=json.loads((pilot/'project.json').read_text(encoding='utf-8'))
        manifest=json.loads((ROOT/'tool/manifests/sp002_social_twenty.json').read_text(encoding='utf-8'))
        validate_project(project,exporting=True)
        self.assertEqual(project['questions'][:71],previous['questions'])
        self.assertEqual(project['contexts'][:10],previous['contexts'])
        self.assertEqual(len(project['questions']),91)
        self.assertEqual([q['catalog_id'] for q in selected_questions(project)[71:]],
                         [q['catalog_id'] for q in manifest['questions']])
        self.assertEqual(len({q['catalog_id'] for q in project['questions'] if q.get('catalog_id')}),
                         len([q for q in project['questions'] if q.get('catalog_id')]))
        self.assertEqual(project['questions'][88]['context'],project['questions'][89]['context'])
        referenced={item['image'] for item in project['questions']+project['contexts'] if item.get('image')}
        referenced.update(o['image'] for q in project['questions'] for o in q['options'] if o.get('image'))
        self.assertEqual(len(referenced),30)
        self.assertTrue(all((pilot/path).is_file() for path in referenced))
        with pymupdf.open(pilot/'cuadernillo.pdf') as doc:
            answers=next(i for i,page in enumerate(doc) if 'HOJA DE RESPUESTAS' in page.get_text())
            body='\n'.join(page.get_text() for page in list(doc)[:answers])
            self.assertIn('91.',body)
            self.assertTrue(doc[44].get_images(full=True))
            self.assertEqual(body.count('Selva amazónica y pueblos aislados'),1)
            self.assertEqual(answers,45)

    def test_visual_equivalences_are_not_treated_as_unique(self):
        self.assertIn('USB-45e476387c60-Q017',self.expand('USB-8e6cf8399239-Q072'))
        self.assertIn('USB-4d0661231ca3-Q006',self.expand('USB-8e6cf8399239-Q083'))
        self.assertIn('USB-7c1a96cf7ade-Q004',self.expand('USB-a170782eadcb-Q081'))


if __name__=='__main__':
    unittest.main()
