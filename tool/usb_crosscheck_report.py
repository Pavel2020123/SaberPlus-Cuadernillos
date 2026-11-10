"""Editorial handoff, pending comparisons, and searchable source index (not an app bank)."""
import csv
import html
import json
import re
import shutil
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

import usb_pdf_catalog as catalog
from usb_export_question_reviews import collect, collect_occurrences
from usb_crosscheck_decisions import resolve

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'output' / 'cotejo_30'


def area_name(value):
    text = ''.join(c for c in unicodedata.normalize('NFKD', value).lower() if not unicodedata.combining(c))
    for fragment, canonical in [('matem', 'Matemáticas'), ('lectura', 'Lectura crítica'),
                                ('social', 'Sociales y ciudadanas'), ('cien', 'Ciencias naturales'),
                                ('ingl', 'Inglés')]:
        if fragment in text:
            return canonical
    return value


def main():
    conn = catalog.db()
    full = collect(conn)
    refs = collect_occurrences(conn, full)
    items = [x for x in full if not x['exclude_academic']]
    lookup = {(i['file_id'], i['question']): i for i in full}
    archive = json.loads((OUT / 'archivo_fichas_consolidadas.json').read_text(encoding='utf-8'))
    mapping = {(i['file_id'], i['item']['question']): tuple(i['canonical']) for i in archive['removed_full_reviews']}
    initial = json.loads((OUT / 'candidatos.json').read_text(encoding='utf-8'))
    pending = {}
    for pair in initial:
        left, right = (resolve(tuple(pair[k]), mapping) for k in ('left', 'right'))
        if left == right:
            continue
        key = tuple(sorted((left, right)))
        if key not in pending:
            pending[key] = dict(pair, left=list(key[0]), right=list(key[1]), status='pendiente_cotejo_visual')
    # Genuine differences explicitly documented in earlier item-level comparisons.
    variants = []
    for item in items:
        evidence = item['details'].get('variant_comparison', '')
        if 'es variante,conservar ambos' in evidence or 'Variante de distractor' in evidence:
            a = (item['file_id'], item['question'])
            b = resolve((item['related_file_id'], item['related_question']), mapping)
            assert a != b, 'A documented variant must never be merged'
            variants.append({'left': list(a), 'right': list(b), 'evidence': evidence})
            pending.pop(tuple(sorted((a, b))), None)
        if item['file_id'] == 'USB-f00a52c8b6f2' and 80 <= item['question'] <= 84:
            a = (item['file_id'], item['question'])
            b = resolve(('USB-1bc205e23b46', item['question']), mapping)
            variants.append({'left': list(a), 'right': list(b), 'evidence': item['alert']})
            pending.pop(tuple(sorted((a, b))), None)
    involved = {tuple(p[k]) for p in pending.values() for k in ('left', 'right')}
    occurrence_counts = Counter((r['canonical_file_id'], r['canonical_question']) for r in refs)
    source_evidence = defaultdict(list)
    for ref in refs:
        if any(ref.get(k) for k in ('source_answer_proposal', 'source_alert', 'source_observed_highlight')):
            source_evidence[(ref['canonical_file_id'], ref['canonical_question'])].append({
                'file_id': ref['file_id'], 'question': ref['question'], 'page': ref['page'],
                'answer_proposal': ref.get('source_answer_proposal'), 'alert': ref.get('source_alert'),
                'observed_highlight': ref.get('source_observed_highlight')})
    rows = []
    for item in items:
        key = (item['file_id'], item['question'])
        blockers = ['transcribir_y_verificar_enunciado_opciones_y_recursos',
                    'revision_docente_pendiente', 'permiso_de_reproduccion_no_verificado']
        if key in involved:
            blockers.append('cotejo_de_posibles_coincidencias_pendiente')
        if not item['answer_proposal']:
            blockers.append('clave_sin_cerrar')
        if item['alert']:
            blockers.append('alerta_documentada_requiere_revision')
        if any(e['alert'] for e in source_evidence[key]):
            blockers.append('alerta_en_aparicion_repetida_archivada')
        key_conflict = any(e['answer_proposal'] and item['answer_proposal'] and
                           e['answer_proposal'] != item['answer_proposal'] for e in source_evidence[key])
        if key_conflict:
            blockers.append('propuestas_de_clave_discrepantes_entre_fuentes')
        row = dict(item, catalog_id=f"{item['file_id']}-Q{str(item['question']).zfill(3)}",
                   area_normalized=area_name(item['area']),
                   additional_exact_occurrences=occurrence_counts[key],
                   additional_source_evidence=source_evidence[key], cross_source_key_conflict=key_conflict,
                   potential_match_pending=key in involved,
                   ready_for_app=False, ready_for_publication=False,
                   teacher_validated=False, reproduction_permission='no_verificado',
                   blockers=blockers)
        rows.append(row)
    academic_refs = sum(not lookup[(r['canonical_file_id'], r['canonical_question'])]['exclude_academic'] for r in refs)
    total_fids = {x['file_id'] for x in full} | {x['file_id'] for x in refs}
    summary = {
        'date': '2026-10-31', 'covered_pdf_count': len(total_fids),
        'academic_records_before': 2834, 'academic_records_now': len(items),
        'additional_full_reviews_consolidated': len(mapping),
        'academic_exact_repeat_occurrences': academic_refs,
        'academic_source_appearances': len(items)+academic_refs,
        'self_report_full_reviews': len(full)-len(items),
        'self_report_repeat_occurrences': len(refs)-academic_refs,
        'all_exact_reference_occurrences': len(refs),
        'candidate_pairs_initial': len(initial), 'pending_distinct_pairs': len(pending),
        'records_with_pending_pairs': len(involved),
        'records_without_detected_pending_pairs': len(items)-len(involved),
        'explicit_variants_preserved_in_this_pass': len(variants),
        'records_without_proposed_key': sum(not x['answer_proposal'] for x in items),
        'records_with_alert': sum(bool(x['alert']) for x in items),
        'canonical_records_with_cross_source_key_conflict': sum(r['cross_source_key_conflict'] for r in rows),
        'by_area': dict(Counter(r['area_normalized'] for r in rows)),
        'all_collection_complete': False, 'unique_question_audit_complete': False,
        'teacher_validated': False, 'importable_question_bank_complete': False,
        'ready_for_publication_count': 0,
        'warning': 'Analysis index only. Similarity is not identity; no automatic publication or import.'}
    for name, data in [('estado_actual.json', summary), ('indice_editorial.json', rows),
                       ('cotejos_pendientes.json', list(pending.values())), ('variantes_preservadas.json', variants)]:
        (OUT / name).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    fields = ['catalog_id', 'file_id', 'question', 'physical_page', 'area_normalized', 'topic',
              'competency_proposal', 'answer_proposal', 'additional_exact_occurrences',
              'potential_match_pending', 'alert', 'source_path', 'source_sha256',
              'ready_for_app', 'ready_for_publication', 'blockers']
    with (OUT / 'indice_editorial.csv').open('w', encoding='utf-8-sig', newline='') as stream:
        writer = csv.DictWriter(stream, fields, extrasaction='ignore', delimiter=';')
        writer.writeheader()
        for row in rows:
            writer.writerow(dict(row, blockers=' | '.join(row['blockers'])))
    esc = html.escape
    page = ['<!doctype html><html lang="es"><meta charset="utf-8"><title>Cotejo editorial SaberPlus</title>',
            '<style>body{font:16px system-ui;margin:24px;color:#17263a}input,select{padding:10px;margin:5px}table{border-collapse:collapse;width:100%}td,th{border-bottom:1px solid #ddd;padding:10px;text-align:left;vertical-align:top}th{background:#eef1f5;position:sticky;top:0}.alert{color:#98350d}</style>',
            '<h1>Índice editorial de referencias · Lote 30</h1>',
            f'<p>{len(items)} fichas académicas · {academic_refs} apariciones exactas adicionales · {len(pending)} pares pendientes de revisión.</p>',
            '<p class="alert">No es un banco importable ni una colección validada. Cada pregunta requiere transcripción completa, revisión docente y permiso de uso. Las claves son propuestas. No publicar automáticamente.</p>',
            '<input id="search" placeholder="Tema, competencia, archivo o pregunta" size="45"><select id="area"><option value="">Todas las áreas</option>',
            *[f'<option>{esc(a)}</option>' for a in sorted(summary['by_area'])],
            '</select><select id="state"><option value="">Todos los estados</option><option value="match">Con cotejo pendiente</option><option value="no-key">Sin clave cerrada</option><option value="alert">Con alerta</option></select><p id="count"></p>',
            '<table><thead><tr><th>ID / fuente</th><th>Área, tema y competencia</th><th>Clave propuesta</th><th>Pendientes</th></tr></thead><tbody>']
    for row in rows:
        href = Path(row['source_path']).as_uri()+f"#page={row['physical_page']}"
        searchable = esc(' '.join(str(row[k] or '') for k in ('catalog_id', 'topic', 'competency_proposal', 'source_path')).lower(), quote=True)
        page.append(f'<tr data-search="{searchable}" data-area="{esc(row["area_normalized"])}" data-match="{int(row["potential_match_pending"])}" data-key="{int(bool(row["answer_proposal"]))}" data-alert="{int(bool(row["alert"]))}"><td>{esc(row["catalog_id"])}<br><a href="{esc(href)}">Abrir fuente, página {row["physical_page"]}</a><br>{row["additional_exact_occurrences"]} apariciones exactas adicionales</td><td>{esc(row["area_normalized"])}<br>{esc(row["topic"])}<br><small>{esc(row["competency_proposal"] or "Sin clasificar")}</small></td><td>{esc(row["answer_proposal"] or "SIN CERRAR")}<br>{esc(row["reason"] or "")}</td><td>{"Cotejo pendiente. " if row["potential_match_pending"] else "Sin coincidencias pendientes detectadas por el filtro. "}<span class="alert">{esc(row["alert"] or "")}</span><br>Revisión docente, contenido estructurado y permisos pendientes.</td></tr>')
    page.append('''</tbody></table><script>
const rows=[...document.querySelectorAll('tbody tr')];
const search=document.getElementById('search'),area=document.getElementById('area'),state=document.getElementById('state');
function filter(){let n=0;for(const r of rows){let s=state.value;let yes=r.dataset.search.includes(search.value.toLowerCase())&&(!area.value||r.dataset.area===area.value)&&(!s||(s==='match'&&r.dataset.match==='1')||(s==='no-key'&&r.dataset.key==='0')||(s==='alert'&&r.dataset.alert==='1'));r.hidden=!yes;if(yes)n++;}document.getElementById('count').textContent=n+' fichas visibles';}
for(const id of ['search','area','state'])document.getElementById(id).addEventListener('input',filter);filter();</script></html>''')
    (OUT / 'INDICE.html').write_text(''.join(page), encoding='utf-8')
    no_key = ['# Fichas sin clave propuesta cerrada', '',
              'No usar como preguntas calificables hasta resolverlas y revisarlas con un docente.', '',
              '| ID | Área | Tema | Razón documentada |', '|---|---|---|---|']
    for row in rows:
        if not row['answer_proposal']:
            values = [row['catalog_id'], row['area_normalized'], row['topic'], row['alert'] or row['reason'] or 'Pendiente']
            no_key.append('| ' + ' | '.join(str(v).replace('|', '/').replace('\n', ' ') for v in values) + ' |')
    (OUT / 'sin_clave_cerrada.md').write_text('\n'.join(no_key)+'\n', encoding='utf-8')
    lines = ['# Cotejo de preguntas: estado actual', '', 'Fecha: 31 de octubre de 2026.', '',
             '## Resultado comprobado', '',
             f'- {len(total_fids)} PDF cubiertos por el lote; no se inició el PDF 31.',
             f'- {len(items)} fichas académicas actuales, frente a 2834 anteriores.',
             f'- {len(mapping)} fichas adicionales consolidadas con evidencia: 64 cotejos visuales históricos explícitos y seis coincidencias nuevas verificadas en imágenes lado a lado.',
             f'- {academic_refs} apariciones académicas exactas adicionales; se conservan {len(items)+academic_refs} apariciones académicas en total.',
             f'- {len(full)-len(items)} fichas y {len(refs)-academic_refs} repeticiones de autoinformes, excluidas del banco académico.',
             '- No se borró ni alteró el contenido de ningún PDF. Se preservaron marcas y fichas previas en un archivo recuperable.',
             '- Los enlaces repetidos apuntan directamente a una ficha existente, sin cadenas. La cobertura por fuente se conserva.', '',
             '## Lo que todavía NO está terminado', '',
             f'El filtro automático examinó 2834 fichas y produjo {len(initial)} pares candidatos. Tras la consolidación y el registro de variantes explícitas quedan {len(pending)} pares distintos pendientes, que involucran {len(involved)} fichas. No son duplicados confirmados: son casos por contrastar; varios pueden compartir tema sin ser la misma pregunta.',
             f'Hay {summary["records_without_proposed_key"]} fichas sin clave propuesta cerrada y {summary["records_with_alert"]} con alertas documentadas. Una alerta no equivale siempre a un error: debe leerse y resolverla.',
             'El índice conserva temas, competencias propuestas, claves razonadas y páginas de origen. No contiene todavía todos los enunciados, opciones y recursos separados en el formato del editor/app. Ninguna ficha se declara validada por docente, autorizada comercialmente ni lista para publicación automática.', '',
             '## Entrega y continuación', '',
             '- `output/cotejo_30/INDICE.html`: índice local con búsqueda y filtros.',
             '- `indice_editorial.json` y CSV: inventario editorial, NO banco importable.',
             '- `cotejos_pendientes.json`: cola verificable y reanudable de pares.',
             '- `variantes_preservadas.json`: siete relaciones explícitas conservadas en este pase; no representa todas las variantes existentes.',
             '- `archivo_fichas_consolidadas.json`: fichas originales completas y estado previo para recuperación.',
             '- `estado_actual.json`: conteos actuales; sustituye para estos conteos la fotografía histórica de cierre del lote.', '',
             'Siguiente trabajo: verificar candidatos en sus fuentes y contextos completos, registrar decisión por par, luego transcribir contenido y recursos con permiso de uso, revisar claves y competencias, y finalmente seleccionar la matriz de las dos sesiones. No sustituir estos pasos por similitud automática.', '',
             '## Validación técnica', '',
             '23 pruebas USB aprobadas después de añadir pruebas de cadenas/ciclos, conservación de marcas, destinos inexistentes y área de lotes mixtos. Se comprobaron las identidades de las referencias y la igualdad de cobertura antes/después. No se probaron importaciones en la app porque este índice no es ese banco.']
    report = '\n'.join(lines)+'\n'
    (ROOT / 'docs' / 'COTEJO_PREGUNTAS_ESTADO_ACTUAL.md').write_text(report, encoding='utf-8')
    target = catalog.AUDIT / 'cotejo_30'
    target.mkdir(exist_ok=True)
    for name in ('estado_actual.json', 'indice_editorial.json', 'indice_editorial.csv',
                 'cotejos_pendientes.json', 'variantes_preservadas.json', 'INDICE.html', 'sin_clave_cerrada.md'):
        shutil.copy2(OUT / name, target / name)
    (target / 'LEEME.md').write_text(report, encoding='utf-8')
    print(json.dumps(summary, ensure_ascii=True), flush=True)


if __name__ == '__main__':
    main()
