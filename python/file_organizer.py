"""Organize immediate child files; import safely without performing any work."""
import argparse
import csv
from datetime import datetime
import json
import os
from pathlib import Path
import shutil
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
FIELDS = ['timestamp', 'filename', 'extension', 'source', 'destination', 'category', 'status']


def is_link(path):
    return path.is_symlink() or (hasattr(path, 'is_junction') and path.is_junction())


def load_config(settings_path, categories_path):
    settings_path, categories_path = Path(settings_path), Path(categories_path)
    settings = json.loads(settings_path.read_text(encoding='utf-8-sig'))
    categories = json.loads(categories_path.read_text(encoding='utf-8-sig'))
    if not isinstance(settings, dict) or type(settings.get('dry_run')) is not bool:
        raise ValueError('settings must contain a boolean dry_run')
    folder = settings.get('test_folder')
    if not isinstance(folder, str) or not folder.strip():
        raise ValueError('test_folder must be a nonempty path')
    folder = Path(folder).expanduser()
    if not folder.is_absolute():
        folder = settings_path.resolve().parent / folder
    if not folder.is_dir() or is_link(folder):
        raise ValueError('test_folder must be an existing directory, not a link')
    if not isinstance(categories, dict):
        raise ValueError('categories must be a JSON object')
    normalized = {}
    reserved = {'CON', 'PRN', 'AUX', 'NUL'} | {f'{s}{n}' for s in ('COM', 'LPT') for n in range(1, 10)}
    for extension, category in categories.items():
        if not isinstance(extension, str) or not extension.startswith('.') or len(extension) < 2:
            raise ValueError('category extensions must start with a dot')
        if (not isinstance(category, str) or not category or category in {'.', '..'}
                or any(c in category for c in '<>:"/\\|?*') or any(ord(c) < 32 for c in category)
                or category.endswith((' ', '.')) or category.split('.')[0].upper() in reserved):
            raise ValueError(f'Unsafe category folder: {category!r}')
        if extension.lower() in normalized:
            raise ValueError(f'Duplicate extension: {extension}')
        normalized[extension.lower()] = category
    return folder.resolve(), settings['dry_run'], normalized


def get_unique_destination(destination):
    destination = Path(destination)
    candidate, counter = destination, 0
    while candidate.exists() or candidate.is_symlink():
        counter += 1
        candidate = destination.with_name(f'{destination.stem}_{counter}{destination.suffix}')
    return candidate


def move_without_overwrite(source, destination):
    """Reserve the output exclusively, copy, then remove the source after success."""
    while True:
        destination = get_unique_destination(destination)
        try:
            output = destination.open('xb')
            break
        except FileExistsError:
            continue
    try:
        with output, source.open('rb') as incoming:
            shutil.copyfileobj(incoming, output)
            output.flush()
            os.fsync(output.fileno())
        shutil.copystat(source, destination)
        source.unlink()
    except BaseException:
        destination.unlink(missing_ok=True)
        raise
    return destination


def log_action(log_file, source, destination, category, status):
    log_file = Path(log_file)
    log_file.parent.mkdir(parents=True, exist_ok=True)
    exists = log_file.exists() and log_file.stat().st_size > 0
    with log_file.open('a', newline='', encoding='utf-8') as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        if not exists:
            writer.writeheader()
        writer.writerow(dict(zip(FIELDS, [datetime.now().isoformat(timespec='seconds'), source.name,
                         source.suffix.lower(), str(source), str(destination), category, status])))


def organize(folder, categories, dry_run=True, log_file=None):
    folder = Path(folder).resolve()
    # Read the input list once so newly created category folders are never scanned.
    files = sorted(folder.iterdir(), key=lambda path: path.name.lower())
    errors, processed = 0, 0
    for source in files:
        if is_link(source) or not source.is_file():
            continue
        if log_file is not None and source.resolve() == Path(log_file).resolve():
            continue
        category = categories.get(source.suffix.lower(), 'Other')
        destination = folder / category / source.name
        try:
            parent = destination.parent
            if is_link(parent) or parent.resolve().parent != folder:
                raise ValueError(f'Unsafe destination: {parent}')
            destination = get_unique_destination(destination)
            if dry_run:
                print(f'Would move: {source.name} -> {destination}')
            else:
                parent.mkdir(exist_ok=True)
                destination = move_without_overwrite(source, destination)
                print(f'Moved: {source.name} -> {destination}')
                if log_file is not None:
                    log_action(log_file, source, destination, category, 'Moved')
            processed += 1
        except (OSError, ValueError) as error:
            errors += 1
            print(f'Error processing {source.name}: {error}', file=sys.stderr)
    print(f'Completed: {processed} processed, {errors} errors; dry_run={dry_run}')
    return errors


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--settings', type=Path, default=PROJECT_ROOT / 'config/settings.json')
    parser.add_argument('--categories', type=Path, default=PROJECT_ROOT / 'config/file_categories.json')
    parser.add_argument('--log', type=Path, default=PROJECT_ROOT / 'logs/file_activity.csv')
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--dry-run', action='store_true', help='preview with no writes')
    mode.add_argument('--apply', action='store_true', help='move files without changing saved settings')
    args = parser.parse_args(argv)
    try:
        folder, dry_run, categories = load_config(args.settings, args.categories)
        if args.dry_run:
            dry_run = True
        elif args.apply:
            dry_run = False
        return 1 if organize(folder, categories, dry_run, args.log) else 0
    except (OSError, ValueError) as error:
        print(f'Configuration or run error: {error}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
