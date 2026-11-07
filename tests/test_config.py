import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'python'))
import file_organizer as organizer


class ConfigTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / 'inbox').mkdir()
        self.settings = self.root / 'settings.json'
        self.categories = self.root / 'categories.json'
        self.settings.write_text(json.dumps({'dry_run': True, 'test_folder': 'inbox'}))
        self.categories.write_text(json.dumps({'.PDF': 'Documents'}))

    def test_relative_paths_and_normalization(self):
        folder, dry_run, categories = organizer.load_config(self.settings, self.categories)
        self.assertEqual(folder, self.root / 'inbox')
        self.assertTrue(dry_run)
        self.assertEqual(categories, {'.pdf': 'Documents'})

    def test_boolean_required(self):
        for value in ['false', 0, None]:
            with self.subTest(value=value):
                self.settings.write_text(json.dumps({'dry_run': value, 'test_folder': 'inbox'}))
                with self.assertRaises(ValueError):
                    organizer.load_config(self.settings, self.categories)

    def test_unsafe_categories(self):
        for category in ['../escape', '..', 'C:\\escape', 'nested/folder', 'CON', 'name.', 'bad:name', '']:
            with self.subTest(category=category):
                self.categories.write_text(json.dumps({'.pdf': category}))
                with self.assertRaises(ValueError):
                    organizer.load_config(self.settings, self.categories)

    def test_missing_folder(self):
        self.settings.write_text(json.dumps({'dry_run': True, 'test_folder': 'missing'}))
        with self.assertRaises(ValueError):
            organizer.load_config(self.settings, self.categories)

    def test_invalid_json_exit_code(self):
        self.settings.write_text('{')
        self.assertEqual(organizer.main(['--settings', str(self.settings), '--categories', str(self.categories)]), 2)

    def test_apply_override_does_not_edit_settings(self):
        original = self.settings.read_bytes()
        (self.root / 'inbox/test.PDF').write_bytes(b'example')
        result = organizer.main(['--settings', str(self.settings), '--categories', str(self.categories),
                                 '--log', str(self.root / 'log.csv'), '--apply'])
        self.assertEqual(result, 0)
        self.assertEqual(self.settings.read_bytes(), original)
        self.assertEqual((self.root / 'inbox/Documents/test.PDF').read_bytes(), b'example')


if __name__ == '__main__':
    unittest.main()
