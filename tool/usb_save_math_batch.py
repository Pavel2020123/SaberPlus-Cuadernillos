"""Merge the manually inspected math batch without renaming queued source PDFs."""
import json
import argparse
from contextlib import closing
from pathlib import Path
import usb_pdf_catalog as catalog

parser = argparse.ArgumentParser()
parser.add_argument('--batch', type=Path, default=Path(__file__).with_name('usb_math_review_batch.json'))
parser.add_argument('--key', default='math_followup_review')
parser.add_argument('--no-report', action='store_true', help='Save SQLite now; regenerate catalog once after a group of batches')
args = parser.parse_args()
batch_path = args.batch
batch = json.loads(batch_path.read_text(encoding='utf-8'))
questions = [item['question'] for item in batch['items']]
if len(set(questions)) != len(questions):
    raise ValueError('Repeated question number in batch')
if any(item['page'] < 1 for item in batch['items']):
    raise ValueError('Invalid physical page number')
catalog.serial()
with closing(catalog.db()) as conn:
    row = conn.execute('SELECT * FROM files WHERE id=?', (batch['file_id'],)).fetchone()
    if not row or row['duplicate_of']:
        raise ValueError('Expected retained source')
    if catalog.digest(catalog.safe(catalog.ROOT / row['current_path'])) != row['sha256']:
        raise ValueError('Source hash changed')
    review = json.loads(row['review_json'] or '{}')
    review.setdefault('id', row['id'])
    review.setdefault('status', 'revision_parcial')
    if any(item['page'] > row['pages'] for item in batch['items']):
        raise ValueError('Review page outside source PDF')
    review[args.key] = batch
    conn.execute("UPDATE files SET review_json=?,review_status='revision_parcial' WHERE id=?",
                 (json.dumps(review, ensure_ascii=False), batch['file_id']))
    conn.commit()
    if not args.no_report:
        catalog.report(conn)
print(f'Saved {len(questions)} item reviews in {args.key}; document remains partially reviewed.')
