"""Validate a booklet bank without creating PDF files."""
import argparse
import json
from pathlib import Path

from generate_booklet_template import validate_bank


ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description='Validate the fixed 22-item booklet bank.')
    parser.add_argument('--bank', type=Path, default=ROOT / 'tool' / 'booklet_template_bank.json')
    args = parser.parse_args()
    bank = json.loads(args.bank.read_text(encoding='utf-8'))
    questions = validate_bank(bank)
    print(f'Valid bank: {len(questions)} items, seven English formats, version {bank["version"]}.')


if __name__ == '__main__':
    main()
