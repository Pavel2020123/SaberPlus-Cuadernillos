import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import editor_server
from editor_model import demo_project, validate_project
from export_used_questions import records
from sync_used_questions import merge


class CatalogExamCodesTests(unittest.TestCase):
    def test_exam_suffixes_survive_save_export_and_registry(self):
        project = demo_project()
        codes = ['USB-60fb8a40c3bb-Q010.1', 'USB-60fb8a40c3bb-Q010.2']
        for question, code in zip(project['questions'], codes):
            question['catalog_id'] = code
        original = copy.deepcopy(project)
        with tempfile.TemporaryDirectory() as directory:
            data = Path(directory)
            state = data / 'project.json'
            state.write_text(json.dumps(project), encoding='utf8')
            with patch.object(editor_server, 'DATA', data), patch.object(editor_server, 'STATE', state):
                saved = editor_server.save(project, project['revision'])
            self.assertEqual([q['catalog_id'] for q in saved['questions'][:2]], codes)
            self.assertEqual([q['catalog_id'] for q in json.loads(state.read_text(encoding='utf8'))['questions'][:2]], codes)
        self.assertCountEqual([q['catalog_id'] for q in records(saved, 'segunda') if q['catalog_id']], codes)
        merged, clashes = merge({'preguntas': [], 'reservas': []}, saved, 'segunda')
        self.assertFalse(clashes)
        self.assertCountEqual([q['catalog_id'] for q in merged if q['catalog_id']], codes)
        self.assertEqual([q['catalog_id'] for q in original['questions'][:2]], codes)

    def test_only_supported_suffixes_are_accepted(self):
        for code in ['', 'USB-60fb8a40c3bb-Q010', 'USB-60fb8a40c3bb-Q010.1', 'USB-60fb8a40c3bb-Q010.2']:
            with self.subTest(code=code):
                project = demo_project()
                project['questions'][0]['catalog_id'] = code
                validate_project(project)
        for suffix in ['.0', '.3', '.01', '.1.2', '.x']:
            with self.subTest(suffix=suffix):
                project = demo_project()
                project['questions'][0]['catalog_id'] = 'USB-60fb8a40c3bb-Q010' + suffix
                with self.assertRaisesRegex(ValueError, 'sufijo opcional'):
                    validate_project(project)


if __name__ == '__main__':
    unittest.main()
