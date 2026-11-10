"""Evidence-backed consolidation; retain full original records in an audit archive."""
import json
import shutil
from datetime import datetime
from pathlib import Path

import usb_pdf_catalog as catalog
from usb_export_question_reviews import collect, collect_occurrences

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'output' / 'cotejo_30'

# Exact historical descriptions were inspected in this pass. Unlike generic
# related_file_id, these expressly record a prior visual content comparison.
EXACT_PREFIXES = (
    'Contexto,enunciado y opciones cotejados visualmente;distinta',
    'Contexto,enunciado,datos y opciones cotejados visualmente;distinta',
    'Contexto, enunciado y opciones cotejados visualmente; cambia',
    'Contexto, datos, enunciado y opciones cotejados visualmente; cambia',
    'Coincidencia de contexto, datos, opciones y diagramas cotejada visualmente;',
    'Contexto,enunciado y opciones cotejados visualmente;diferente',
    'Contexto,enunciado y alternativas cotejados visualmente;distinta',
)


def resolve(key, mapping):
    seen = set()
    while key in mapping:
        if key in seen:
            raise ValueError('Canonical-reference cycle')
        seen.add(key)
        key = mapping[key]
    return key


def transform(reviews, mappings, evidence):
    removed = []
    page_map = {}
    for fid, review in reviews.items():
        for batch in review.values():
            if isinstance(batch, dict) and batch.get('file_id') == fid:
                for item in batch.get('items', []):
                    page_map[(fid, item['question'])] = item['page']
    for source, target in mappings.items():
        if source not in page_map or resolve(target, mappings) not in page_map:
            raise ValueError('Unknown source or target')
    for fid, review in reviews.items():
        for batch_key, batch in review.items():
            if not isinstance(batch, dict) or batch.get('file_id') != fid:
                continue
            retained = []
            for item in batch.get('items', []):
                source = (fid, item['question'])
                if source not in mappings:
                    retained.append(item)
                    continue
                target = resolve(source, mappings)
                removed.append({'file_id': fid, 'batch_key': batch_key,
                                'item': item, 'canonical': list(target),
                                'evidence': evidence[source]})
                batch.setdefault('duplicate_occurrences', []).append({
                    'question': item['question'], 'page': item['page'],
                    'canonical_file_id': target[0], 'canonical_question': target[1],
                    'canonical_page': page_map[target], 'exact_content': True,
                    'verification': evidence[source], 'crosscheck_date': '2026-10-31',
                    # Marks and proposals belong to their source, even if text is exact.
                    'source_answer_proposal': item.get('answer_proposal'),
                    'source_observed_highlight': item.get('observed_highlight'),
                    'source_alert': item.get('alert') or item.get('pedagogical_alert'),
                    'archived_full_review': 'archivo_fichas_consolidadas.json',
                })
            if 'items' in batch:
                batch['items'] = retained
            for ref in batch.get('duplicate_occurrences', []):
                key = (ref['canonical_file_id'], ref['canonical_question'])
                target = resolve(key, mappings)
                ref.update(canonical_file_id=target[0], canonical_question=target[1],
                           canonical_page=page_map[target])
    return removed


def main():
    conn = catalog.db()
    all_items = collect(conn)
    before_refs = collect_occurrences(conn, all_items)
    if (OUT / 'archivo_fichas_consolidadas.json').exists():
        raise RuntimeError('Already applied; use archive rather than replaying')
    reviews = {r['id']: json.loads(r['review_json'] or '{}') for r in
               conn.execute('SELECT * FROM files WHERE duplicate_of IS NULL')}
    mapping, evidence = {}, {}
    for item in all_items:
        comparison = item['details'].get('variant_comparison', '')
        if comparison.startswith(EXACT_PREFIXES):
            key = (item['file_id'], item['question'])
            mapping[key] = (item['related_file_id'], item['related_question'])
            evidence[key] = 'Consolidacion de cotejo visual historico explicito: ' + comparison
    # Newly viewed side-by-side renderings: complete statements, options and tables.
    for source_id, numbers, target_id, offset, image in (
        ('USB-578d9b20297e', range(15, 18), 'USB-1c44481d3d4a', -11, 'pair-0013.png'),
        ('USB-91836110f48e', range(15, 18), 'USB-1c44481d3d4a', 25, 'pair-0024.png'),
    ):
        for number in numbers:
            key = (source_id, number)
            mapping[key] = (target_id, number + offset)
            evidence[key] = ('Cotejo visual de enunciado, contexto, opciones, tablas y graficas el 2026-10-31; '
                             f'evidencia local {image}. Solo cambian numeracion y marcas/escaneo.')
    # The eleven science matches also have historical evidence and were visually
    # rechecked in pair-0001/0005/0008/0010.png. Do not count them twice.
    assert len(mapping) == 70, len(mapping)
    original = json.loads(json.dumps(reviews))
    removed = transform(reviews, mapping, evidence)
    assert len(removed) == len(mapping)
    archive = {'date': datetime.now().isoformat(), 'removed_full_reviews': removed,
               'reference_count_before': len(before_refs), 'original_reviews':
               {fid: original[fid] for fid in reviews if reviews[fid] != original[fid]}}
    # Local rollback evidence is written before the single database transaction.
    (OUT / 'archivo_fichas_consolidadas.json').write_text(json.dumps(archive, ensure_ascii=False, indent=2), encoding='utf-8')
    try:
        with conn:
            for fid in reviews:
                if reviews[fid] != original[fid]:
                    conn.execute('UPDATE files SET review_json=? WHERE id=?',
                                 (json.dumps(reviews[fid], ensure_ascii=False), fid))
            after = collect(conn)
            refs = collect_occurrences(conn, after)
            assert len(after) == len(all_items)-70
            assert len(refs) == len(before_refs)+70
            assert len(after)+len(refs) == len(all_items)+len(before_refs)
            conn.execute('INSERT INTO actions VALUES(?,?,?,?)',
                         (datetime.now().isoformat(), 'crosscheck_consolidation', 'batch_30',
                          json.dumps({'consolidated': 70, 'archive': str(OUT / 'archivo_fichas_consolidadas.json')})))
    except Exception:
        # Evidence remains but records are rolled back; never silently replay.
        raise
    for name in ('archivo_fichas_consolidadas.json',):
        shutil.copy2(OUT / name, catalog.AUDIT / 'preguntas_revisadas' / name)
    print(json.dumps({'consolidated': 70, 'academic_records': sum(not x['exclude_academic'] for x in after),
                      'all_exact_references': len(refs), 'coverage_preserved': True}), flush=True)


if __name__ == '__main__':
    main()
