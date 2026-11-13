"""Independent workspaces must preserve saved projects and their revisions."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import editor_parallel as parallel
import editor_server as server


class ParallelWorkspaceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.template = self.root / 'empty.json'
        self.project = server.new_project()
        self.project['code'] = 'SP-003'
        self.template.write_text(json.dumps(self.project), encoding='utf-8')

    def test_distinct_ports_and_invalid_paths(self):
        with patch.object(server, 'ROOT', self.root):
            a = parallel.workspace_directory('usuario', 4186)
            b = parallel.workspace_directory('usuario', 4187)
            self.assertNotEqual(a, b)
            self.assertNotEqual(a / 'project.json', self.root / 'data/project.json')
            for name in ('..', '../data', 'a/b', 'a\\b', ''):
                with self.assertRaises(ValueError):
                    parallel.workspace_directory(name, 4186)

    def test_reopening_preserves_saved_work(self):
        data = self.root / 'user'
        parallel.initialize_workspace(data, self.template)
        state = data / 'project.json'
        saved = dict(self.project, revision=7, time='Guardado por el usuario')
        state.write_text(json.dumps(saved), encoding='utf-8')
        self.assertEqual(parallel.initialize_workspace(data, self.template), saved)
        self.assertEqual(json.loads(state.read_text(encoding='utf-8')), saved)

    def test_nonempty_template_is_not_loaded_as_new_workspace(self):
        self.project['questions'] = [{'id': 'do-not-copy'}]
        self.template.write_text(json.dumps(self.project), encoding='utf-8')
        data = self.root / 'user'
        with self.assertRaises(ValueError):
            parallel.initialize_workspace(data, self.template)
        self.assertFalse((data / 'project.json').exists())

    def test_save_revisions_and_backups_stay_in_their_workspace(self):
        a, b = self.root / 'a', self.root / 'b'
        parallel.initialize_workspace(a, self.template)
        parallel.initialize_workspace(b, self.template)
        with patch.object(server, 'DATA', a), patch.object(server, 'STATE', a / 'project.json'):
            server.save(dict(self.project, time='A'), 0)
        with patch.object(server, 'DATA', b), patch.object(server, 'STATE', b / 'project.json'):
            self.assertEqual(server.load()['revision'], 0)
            server.save(dict(self.project, time='B'), 0)
        left = json.loads((a / 'project.json').read_text(encoding='utf-8'))
        right = json.loads((b / 'project.json').read_text(encoding='utf-8'))
        self.assertEqual((left['time'], right['time']), ('A', 'B'))
        self.assertEqual((left['revision'], right['revision']), (1, 1))
        self.assertEqual(len(list((a / 'backups').glob('*.json'))), 1)
        self.assertEqual(len(list((b / 'backups').glob('*.json'))), 1)


if __name__ == '__main__':
    unittest.main()
