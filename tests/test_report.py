import csv
from datetime import datetime
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'python'))
import weekly_report as report


class ReportTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.log = Path(self.temp.name) / 'activity.csv'

    def test_window_and_malformed_rows(self):
        with self.log.open('w', newline='') as handle:
            writer = csv.writer(handle)
            writer.writerow(['timestamp', 'category', 'status'])
            writer.writerows([
                ['2026-11-06 12:00:00', 'Documents', 'Moved'],
                ['2026-10-30 12:00:00', 'Images', 'Dry Run'],
                ['2026-10-29 12:00:00', 'Old', 'Moved'],
                ['2026-11-07 12:00:00', 'Future', 'Moved'],
                ['broken', 'Other', 'Moved']])
        result = report.build_report(self.log, now=datetime(2026, 11, 6, 12))
        self.assertIn('Total actions: 2', result)
        self.assertIn('Successful moves: 1', result)
        self.assertIn('Malformed rows skipped: 1', result)
        self.assertNotIn('- Old:', result)
        self.assertNotIn('- Future:', result)

    def test_missing_log_is_empty_report(self):
        self.assertIn('Total actions: 0', report.build_report(self.log))

    def test_bad_headers_fail(self):
        self.log.write_text('wrong,columns\n')
        with self.assertRaises(ValueError):
            report.build_report(self.log)

    def test_invalid_window(self):
        with self.assertRaises(ValueError):
            report.build_report(self.log, 0)

    def test_cli_creates_output(self):
        output = self.log.parent / 'reports/weekly.txt'
        self.assertEqual(report.main(['--log', str(self.log), '--output', str(output)]), 0)
        self.assertTrue(output.is_file())


if __name__ == '__main__':
    unittest.main()
