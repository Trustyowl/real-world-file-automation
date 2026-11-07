"""Summarize the last seven days of organizer activity."""
import argparse
from collections import Counter
import csv
from datetime import datetime, timedelta
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def build_report(log_file, days=7, now=None):
    if days < 1:
        raise ValueError('days must be positive')
    now = now or datetime.now()
    start = now - timedelta(days=days)
    categories, statuses = Counter(), Counter()
    skipped = 0
    log_file = Path(log_file)
    if log_file.exists():
        with log_file.open(newline='', encoding='utf-8-sig') as handle:
            reader = csv.DictReader(handle)
            if not {'timestamp', 'category', 'status'}.issubset(reader.fieldnames or []):
                raise ValueError('Log is missing timestamp, category or status columns')
            for row in reader:
                try:
                    stamp = datetime.fromisoformat(row['timestamp'])
                    if stamp.tzinfo is not None or not row['category'] or not row['status']:
                        raise ValueError('Unsupported row')
                except (TypeError, ValueError):
                    skipped += 1
                    continue
                if start <= stamp <= now:
                    categories[row['category']] += 1
                    statuses[row['status']] += 1
    lines = ['FILE ORGANIZATION REPORT', f'Window: {start.isoformat(timespec="seconds")} to {now.isoformat(timespec="seconds")}',
             f'Total actions: {sum(statuses.values())}', f'Successful moves: {statuses["Moved"]}',
             f'Dry-run actions (legacy logs): {statuses["Dry Run"]}', f'Malformed rows skipped: {skipped}', '', 'Actions by category:']
    lines += [f'- {key}: {value}' for key, value in sorted(categories.items())]
    lines += ['', 'Status summary:'] + [f'- {key}: {value}' for key, value in sorted(statuses.items())]
    return '\n'.join(lines) + '\n'


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--log', type=Path, default=PROJECT_ROOT / 'logs/file_activity.csv')
    parser.add_argument('--output', type=Path, default=PROJECT_ROOT / 'reports/weekly_report.txt')
    parser.add_argument('--days', type=int, default=7)
    args = parser.parse_args(argv)
    try:
        report = build_report(args.log, args.days)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(report, encoding='utf-8')
        print(f'Report created: {args.output}')
        return 0
    except (OSError, ValueError) as error:
        print(f'Report error: {error}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
