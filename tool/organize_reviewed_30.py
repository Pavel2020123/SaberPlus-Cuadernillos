"""Organize only the closed 30-PDF batch, retaining stable IDs and audit history."""
import json
import re
from datetime import datetime
from pathlib import Path

import usb_pdf_catalog as catalog
import usb_export_question_reviews as export


def main():
    local = Path(__file__).resolve().parents[1] / 'docs'
    closure = json.loads((local / 'CIERRE_LOTE_30_PDF.json').read_text(encoding='utf-8'))
    conn = catalog.db()
    plans = []
    for entry in closure['records']:
        row = conn.execute('SELECT * FROM files WHERE id=?', (entry['id'],)).fetchone()
        source = catalog.safe(catalog.ROOT / row['current_path'])
        if catalog.digest(source) != entry['source_sha256']:
            raise ValueError(f"Source changed: {entry['id']}")
        name = source.stem
        year = re.search(r'(?<!\d)20(?:1\d|2\d)(?!\d)', name)
        confirmed = re.search(r'Cal-([AB])(?!-por-confirmar)', name)
        group = (f'{year[0]} - Calendario {confirmed[1]}' if year and confirmed else
                 f'{year[0]} - Calendario por confirmar' if year else
                 'Sin ano confirmado - Cuadernillos de referencia')
        # Preserve descriptive/source details; ID prevents collisions between variants.
        stem = re.sub(r'[^A-Za-z0-9_-]+', '-', name).strip('-')
        stem = stem.replace(entry['id'], '').strip('-_')
        stem = f'{stem}_{entry["id"]}'
        target = catalog.safe(catalog.ROOT / 'Revisados - Lote 30' / group / stem / (stem + '.pdf'))
        if target.exists():
            raise FileExistsError(target)
        plans.append({'id': entry['id'], 'old_path': row['current_path'],
                      'new_path': catalog.relative(target), 'sha256': row['sha256'],
                      'year_basis': 'Nombre documentado; no certifica fecha ni autenticidad',
                      'calendar': confirmed[1] if confirmed else 'Por confirmar'})
    stamp = datetime.now().isoformat()
    manifest = {'date': stamp, 'status': 'planned', 'records': plans}
    journal = catalog.AUDIT / 'ORGANIZACION_LOTE_30.json'
    journal.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    # Backup database before changing paths. No PDF is overwritten or deleted.
    import shutil
    conn.commit()
    checkpoint = conn.execute('PRAGMA wal_checkpoint(FULL)').fetchone()
    if checkpoint[0] != 0:
        raise RuntimeError('Catalog busy; cannot take consistent backup')
    shutil.copy2(catalog.AUDIT / 'catalogo.sqlite',
                 catalog.AUDIT / 'catalogo_antes_organizar_30_verificado.sqlite')
    for item in plans:
        source = catalog.safe(catalog.ROOT / item['old_path'])
        target = catalog.safe(catalog.ROOT / item['new_path'])
        target.parent.mkdir(parents=True, exist_ok=True)
        source.rename(target)
        if catalog.digest(target) != item['sha256']:
            raise ValueError('Post-move hash mismatch')
        conn.execute('UPDATE files SET current_path=? WHERE id=?', (item['new_path'], item['id']))
        conn.execute('INSERT INTO actions VALUES(?,?,?,?)',
                     (stamp, 'organize_reviewed_30', item['id'], json.dumps(item, ensure_ascii=False)))
        conn.commit()
        print(f"Moved and verified {item['id']}", flush=True)
        with (catalog.AUDIT / 'renombrados.jsonl').open('a', encoding='utf-8') as stream:
            stream.write(json.dumps({'time': stamp, **item}, ensure_ascii=False) + '\n')
        for entry in closure['records']:
            if entry['id'] == item['id']:
                entry['path'] = item['new_path']
    manifest['status'] = 'completed_and_sha256_verified'
    text = json.dumps(manifest, ensure_ascii=False, indent=2)
    journal.write_text(text, encoding='utf-8')
    (local / journal.name).write_text(text, encoding='utf-8')
    for folder in (local, catalog.AUDIT):
        (folder / 'CIERRE_LOTE_30_PDF.json').write_text(json.dumps(closure, ensure_ascii=False, indent=2), encoding='utf-8')
    lines = ['# Organizacion de los 30 PDF revisados', '',
             'Una carpeta por documento, agrupada por ano y calendario confirmado.',
             'El ano conservado del nombre no certifica autenticidad. Los calendarios dudosos no se infieren.',
             'No se borraron PDF. El identificador estable conserva la vinculacion con las preguntas.', '',
             '| ID | Antes | Ahora |', '|---|---|---|']
    lines += [f"| {p['id']} | {p['old_path']} | {p['new_path']} |" for p in plans]
    for folder in (local, catalog.AUDIT):
        (folder / 'ORGANIZACION_LOTE_30.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    catalog.report(conn)
    conn.close()
    print(json.dumps({'organized': len(plans), 'confirmed_calendar': sum(p['calendar'] != 'Por confirmar' for p in plans)}))


if __name__ == '__main__':
    main()
