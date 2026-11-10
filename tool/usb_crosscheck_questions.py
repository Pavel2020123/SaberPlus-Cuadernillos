"""Read-only duplicate candidate audit; similarity never removes a question."""
import json
import re
import unicodedata
from collections import Counter
from pathlib import Path

import usb_pdf_catalog as catalog
from usb_export_question_reviews import collect, collect_occurrences
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

OUT = Path(__file__).resolve().parents[1] / 'output' / 'cotejo_30'


def normalize(text):
    text = unicodedata.normalize('NFKD', text or '').lower()
    return re.sub(r'[^a-z0-9]+', ' ', ''.join(c for c in text if not unicodedata.combining(c))).strip()


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    conn = catalog.db()
    items = [x for x in collect(conn) if not x['exclude_academic']]
    pages = {(r['file_id'], r['page']): r['text'] for r in conn.execute('SELECT file_id,page,text FROM pages')}
    # Full-page OCR is candidate evidence only: columns and shared contexts prevent
    # treating a guessed question boundary as an exact-content fingerprint.
    descriptions = [normalize(x['topic'] + ' ' + (x['reason'] or '') + ' ' +
                              json.dumps(x['context_details'], ensure_ascii=False)) for x in items]
    page_texts = [normalize(pages.get((x['file_id'], x['physical_page']), '')) for x in items]
    meta = cosine_similarity(TfidfVectorizer(analyzer='char_wb', ngram_range=(3, 5), min_df=2).fit_transform(descriptions))
    page_sim = cosine_similarity(TfidfVectorizer(analyzer='char_wb', ngram_range=(4, 5), min_df=2).fit_transform(page_texts))
    # Compare all academic records; don't assume areas are classified consistently.
    pairs = []
    for i, a in enumerate(items):
        for j in range(i + 1, len(items)):
            b = items[j]
            if a['file_id'] == b['file_id']:
                continue
            related = ((a['related_file_id'], a['related_question']) == (b['file_id'], b['question']) or
                       (b['related_file_id'], b['related_question']) == (a['file_id'], a['question']))
            score = float(meta[i, j])
            ps = float(page_sim[i, j])
            if score >= .42 or (ps >= .72 and score >= .18) or related:
                pairs.append({'left': [a['file_id'], a['question']], 'right': [b['file_id'], b['question']],
                              'description_similarity': round(score, 4), 'page_similarity': round(ps, 4),
                              'prior_related': related, 'status': 'candidate_not_verified',
                              'same_proposed_answer': a['answer_proposal'] == b['answer_proposal']})
    pairs.sort(key=lambda p: max(p['description_similarity'], p['page_similarity'] * .85), reverse=True)
    (OUT / 'fichas_academicas.json').write_text(json.dumps(items, ensure_ascii=False), encoding='utf-8')
    (OUT / 'candidatos.json').write_text(json.dumps(pairs, ensure_ascii=False, indent=2), encoding='utf-8')
    lookup = {(x['file_id'], x['question']): x for x in items}
    lines = []
    for n, pair in enumerate(pairs, 1):
        a, b = (lookup[tuple(pair[key])] for key in ('left', 'right'))
        lines.append(f"{n:04d} meta={pair['description_similarity']:.3f} page={pair['page_similarity']:.3f} "
                     f"{a['file_id']} q{a['question']} p{a['physical_page']} [{a['answer_proposal']}] "
                     f"<> {b['file_id']} q{b['question']} p{b['physical_page']} [{b['answer_proposal']}]\n"
                     f"  {a['topic']} | {a['reason']}\n  {b['topic']} | {b['reason']}\n")
    (OUT / 'candidatos.txt').write_text('\n'.join(lines), encoding='utf-8')
    summary = {'academic_records_compared': len(items), 'pairs_scored': len(items)*(len(items)-1)//2,
               'candidate_pairs': len(pairs), 'unique_question_audit_complete': False,
               'automatic_merges': 0, 'warning': 'Candidates require source and shared-context verification.'}
    (OUT / 'estado.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
    print(json.dumps(summary), flush=True)


if __name__ == '__main__':
    main()
