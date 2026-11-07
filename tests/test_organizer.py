import csv
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'python'))
import file_organizer as organizer


class OrganizerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.log = self.root / 'logs/activity.csv'

    def test_preview_has_no_writes(self):
        source = self.root / 'Report.PDF'
        source.write_bytes(b'original')
        self.assertEqual(organizer.organize(self.root, {'.pdf': 'Documents'}, True, self.log), 0)
        self.assertEqual(list(self.root.iterdir()), [source])
        self.assertEqual(source.read_bytes(), b'original')

    def test_moves_preserve_existing_and_log_actual_destination(self):
        (self.root / 'Documents').mkdir()
        (self.root / 'Documents/report.pdf').write_bytes(b'keep')
        (self.root / 'report.pdf').write_bytes(b'new')
        (self.root / 'unknown.XYZ').write_bytes(b'unknown')
        self.assertEqual(organizer.organize(self.root, {'.pdf': 'Documents'}, False, self.log), 0)
        self.assertEqual((self.root / 'Documents/report.pdf').read_bytes(), b'keep')
        self.assertEqual((self.root / 'Documents/report_1.pdf').read_bytes(), b'new')
        self.assertEqual((self.root / 'Other/unknown.XYZ').read_bytes(), b'unknown')
        with self.log.open(newline='') as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual(len(rows), 2)
        self.assertTrue(any(row['destination'].endswith('report_1.pdf') for row in rows))

    def test_failed_copy_retains_source_and_removes_partial_destination(self):
        source, dest = self.root / 'source', self.root / 'destination'
        source.write_bytes(b'keep')
        with patch.object(organizer.shutil, 'copyfileobj', side_effect=OSError('disk full')):
            with self.assertRaises(OSError):
                organizer.move_without_overwrite(source, dest)
        self.assertEqual(source.read_bytes(), b'keep')
        self.assertFalse(dest.exists())

    def test_one_error_does_not_stop_other_files(self):
        (self.root / 'a.pdf').write_bytes(b'a')
        (self.root / 'b.txt').write_bytes(b'b')
        (self.root / 'Documents').write_bytes(b'blocked folder')
        errors = organizer.organize(self.root, {'.pdf': 'Documents', '.txt': 'Text'}, False, self.log)
        self.assertGreater(errors, 0)
        self.assertEqual((self.root / 'Text/b.txt').read_bytes(), b'b')

    def test_nested_files_are_not_scanned(self):
        (self.root / 'nested').mkdir()
        source = self.root / 'nested/report.pdf'
        source.write_bytes(b'keep')
        organizer.organize(self.root, {'.pdf': 'Documents'}, False, self.log)
        self.assertTrue(source.exists())

    def test_numbered_collisions(self):
        for name in ['report.pdf', 'report_1.pdf']:
            (self.root / name).touch()
        self.assertEqual(organizer.get_unique_destination(self.root / 'report.pdf').name, 'report_2.pdf')

    def test_destination_link_rejected(self):
        (self.root / 'report.pdf').write_bytes(b'keep')
        original = organizer.is_link
        with patch.object(organizer, 'is_link', side_effect=lambda p: p.name == 'Documents' or original(p)):
            self.assertEqual(organizer.organize(self.root, {'.pdf': 'Documents'}, False, self.log), 1)
        self.assertTrue((self.root / 'report.pdf').exists())

    def test_exclusive_creation_retries_race(self):
        source, destination = self.root / 'source', self.root / 'destination'
        source.write_bytes(b'new')
        real_open = Path.open
        attempted = []
        def racing_open(path, mode='r', *args, **kwargs):
            if mode == 'xb' and not attempted:
                attempted.append(True)
                path.write_bytes(b'concurrent')
            return real_open(path, mode, *args, **kwargs)
        with patch.object(Path, 'open', racing_open):
            actual = organizer.move_without_overwrite(source, destination)
        self.assertEqual(destination.read_bytes(), b'concurrent')
        self.assertEqual(actual.read_bytes(), b'new')


if __name__ == '__main__':
    unittest.main()
