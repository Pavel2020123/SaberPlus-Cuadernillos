"""Apply explicit, manually verified PDF basenames through the existing journaled renamer."""
import argparse
import json
from contextlib import closing
from datetime import datetime
from pathlib import Path
import usb_pdf_catalog as catalog

parser = argparse.ArgumentParser()
parser.add_argument('--rename', nargs=2, action='append', metavar=('ID', 'BASENAME'), required=True)
parser.add_argument('--apply', action='store_true')
args = parser.parse_args()
with closing(catalog.db()) as conn:
    records = []
    for file_id, name in args.rename:
        row = conn.execute('SELECT * FROM files WHERE id=?', (file_id,)).fetchone()
        if not row or row['duplicate_of'] or row['status'] == 'requiere_ocr':
            raise ValueError('Rename only an existing retained, extracted, manually reviewed source')
        if Path(name).name != name or not name.lower().endswith('.pdf'):
            raise ValueError('Expected a simple PDF basename')
        record = json.loads(row['review_json'] or '{}')
        if not record or row['review_status'] == 'pendiente':
            raise ValueError('Manual identification is required before renaming')
        record.update(id=file_id, status=row['review_status'], rename=name)
        records.append(record)
    if args.apply:
        folder = catalog.AUDIT / 'planes_renombrado_revisados'
        folder.mkdir(exist_ok=True)
        plan = folder / (datetime.now().strftime('%Y%m%d_%H%M%S_%f') + '.json')
        with plan.open('x', encoding='utf-8') as handle:
            json.dump(records, handle, ensure_ascii=False, indent=2)
        catalog.review(conn, plan)
    else:
        print(json.dumps([{'id': r['id'], 'rename': r['rename']} for r in records], ensure_ascii=True))
