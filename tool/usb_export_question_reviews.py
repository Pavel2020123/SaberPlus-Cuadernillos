"""Export actual manual reviews only, never inferred OCR question candidates."""
import csv
import html
import json
from collections import Counter
from contextlib import closing
from pathlib import Path
from urllib.parse import quote
import usb_pdf_catalog as catalog


def item_area(review, item, batch):
    """Use documented section ranges, not the label of a mixed-area work batch."""
    if item.get('area'):
        return item['area']
    for value in review.values():
        if not isinstance(value, dict):
            continue
        structure = value.get('structure', {})
        if not isinstance(structure, dict):
            continue
        for section in structure.get('sections', []):
            bounds = section.get('questions')
            if (isinstance(bounds, list) and len(bounds) == 2 and
                    all(isinstance(n, int) for n in bounds) and
                    bounds[0] <= item['question'] <= bounds[1]):
                name = section['area']
                return {'Sociales': 'Sociales y ciudadanas', 'Ciencias': 'Ciencias naturales',
                        'Ingles': 'Inglés'}.get(name, name)
    return batch.get('area', 'Matematicas')


def collect(conn):
    result = []
    for row in conn.execute('SELECT * FROM files WHERE duplicate_of IS NULL ORDER BY priority DESC,id'):
        review = json.loads(row['review_json'] or '{}')
        seen = set()
        for key, batch in review.items():
            if not isinstance(batch, dict) or 'items' not in batch or 'file_id' not in batch:
                continue
            if batch['file_id'] != row['id']:
                raise ValueError('Review attached to wrong source')
            contexts = {context['id']: context for context in batch.get('contexts', [])}
            for item in batch['items']:
                number = item['question']
                if number in seen:
                    raise ValueError(f'Duplicate manual review: {row["id"]} question {number}')
                seen.add(number)
                if not 1 <= item['page'] <= row['pages']:
                    raise ValueError('Invalid physical page')
                competency = item.get('competency_proposal') or batch.get('competency_proposal')
                if 'competency_code' in item:
                    competency = batch['competency_legend'][item['competency_code']]
                process = batch.get('process_legend', {}).get(item.get('process'))
                excluded = item.get('exclude_academic', False)
                context = contexts.get(item.get('context'), {})
                mark = item.get('observed_highlight')
                proposed = item.get('answer_proposal')
                annotation = item.get('observed_annotation') or {}
                annotation_value = annotation.get('value')
                annotation_comparison = 'sin_anotacion_documentada'
                if annotation_value:
                    annotation_comparison = 'anotacion_no_univoca_o_clave_sin_cerrar'
                    if len(annotation_value) == 1 and proposed:
                        annotation_comparison = 'coincide_con_propuesta' if annotation_value == proposed else 'discrepa_de_propuesta'
                mark_comparison = 'sin_resaltado_documentado'
                if mark:
                    mark_comparison = 'marca_no_univoca_o_clave_sin_cerrar'
                    if len(mark) == 1 and proposed:
                        mark_comparison = 'coincide_con_propuesta' if mark == proposed else 'discrepa_de_propuesta'
                result.append({
                    'file_id': row['id'], 'source_path': str(catalog.ROOT / row['current_path']),
                    'original_path': row['original_path'], 'source_sha256': row['sha256'],
                    'physical_page': item['page'], 'question': number,
                    'area': item_area(review, item, batch), 'topic': item['topic'],
                    'competency_proposal': competency, 'process_proposal': process,
                    'context_id': item.get('context'),
                    'context_title': context.get('title') or context.get('topic'),
                    'context_source_as_printed': context.get('source_as_printed'),
                    'related_file_id': item.get('related_file_id') or batch.get('related_file_id'),
                    'related_question': item.get('related_question'),
                    'related_physical_page': item.get('related_page'),
                    'answer_proposal': item.get('answer_proposal'),
                    'observed_highlight': mark,
                    'highlight_vs_proposal': mark_comparison,
                    'annotation_value': annotation_value,
                    'annotation_type': annotation.get('type'),
                    'annotation_provenance': annotation.get('provenance'),
                    'annotation_vs_proposal': annotation_comparison,
                    'reason': item.get('reason'), 'alert': item.get('alert') or item.get('pedagogical_alert'),
                    'ocr_correction': item.get('ocr_correction'),
                    'exclude_academic': excluded,
                    'review_status': 'autoinforme_sin_clave' if excluded else 'analisis_inicial_no_validado',
                    'review_scope': batch['scope'], 'batch_key': key, 'details': item,
                    'context_details': context,
                })
    return sorted(result, key=lambda item: (item['file_id'], item['question']))


def collect_occurrences(conn, items):
    """Keep verified repeated appearances as references, not question copies.

    Similarity/related_file_id alone is deliberately insufficient: variants
    must retain their own reviews. Only an explicit exact_content flag enters.
    """
    targets = {(item['file_id'], item['question']) for item in items}
    occupied = set(targets)
    result = []
    for row in conn.execute('SELECT * FROM files WHERE duplicate_of IS NULL'):
        for batch in json.loads(row['review_json'] or '{}').values():
            if not isinstance(batch, dict):
                continue
            for ref in batch.get('duplicate_occurrences', []):
                if batch.get('file_id') != row['id'] or ref.get('exact_content') is not True:
                    raise ValueError('Unverified exact occurrence')
                target = (ref['canonical_file_id'], ref['canonical_question'])
                source = (row['id'], ref['question'])
                if target not in targets or source in occupied:
                    raise ValueError('Missing canonical question or repeated occurrence')
                if not 1 <= ref['page'] <= row['pages']:
                    raise ValueError('Occurrence page outside source')
                occupied.add(source)
                result.append(dict(ref, file_id=row['id'],
                                   source_path=str(catalog.ROOT / row['current_path']),
                                   source_sha256=row['sha256']))
    return result


def review_html(items, summary):
    esc = lambda value: html.escape(str(value or ''))
    parts = ['<!doctype html><html lang="es"><meta charset="utf-8"><title>Preguntas documentadas - PAVEL</title>',
             '<style>body{font:16px Segoe UI,sans-serif;margin:24px;color:#17263a}table{border-collapse:collapse;width:100%}td,th{padding:10px;border:1px solid #ccd4dd;text-align:left;vertical-align:top}th{background:#edf1f4}details{margin:12px 0}.alerta{color:#8a2c13}summary{cursor:pointer}small{display:block;margin-top:5px}a{color:#24548b}</style>',
             '<h1>Preguntas documentadas</h1><p><a href="../INDICE.html">Volver al inventario</a></p>',
             f'<p>{summary["academic_items_initially_reviewed"]} preguntas academicas con analisis inicial; {summary["excluded_self_report_items"]} autoinformes separados; {summary["files_with_manual_question_reviews"]} de {summary["retained_files"]} PDF con preguntas documentadas.</p>',
             '<p>La coleccion NO esta terminada. Las claves y competencias son propuestas pendientes de revision docente. Los resaltados del ejemplar no son claves oficiales. Usar Ctrl+F para buscar un tema o numero.</p>']
    for file_id in dict.fromkeys(item['file_id'] for item in items):
        group = [item for item in items if item['file_id'] == file_id]
        source = Path(group[0]['source_path'])
        href = '../../' + quote(source.relative_to(catalog.ROOT).as_posix(), safe='/')
        parts.extend([f'<h2>{esc(file_id)}</h2><p><a href="{esc(href)}">{esc(source.name)}</a><small>Nombre original: {esc(group[0]["original_path"])}</small></p>',
                      '<table><thead><tr><th>Pregunta / pagina fisica</th><th>Tema y clasificacion propuesta</th><th>Clave propuesta / marca visible</th><th>Razonamiento y alertas</th></tr></thead><tbody>'])
        for item in group:
            details = esc(item['reason'] or 'Autoinforme excluido: no se califica.')
            if item['alert']:
                details += '<p class="alerta">ALERTA: ' + esc(item['alert']) + '</p>'
            if item['ocr_correction']:
                details += '<p>Correccion OCR: ' + esc(item['ocr_correction']) + '</p>'
            if item.get('annotation_value'):
                details += '<p>Anotacion del ejemplar (NO oficial): ' + esc(item['annotation_value']) + ' - ' + esc(item['annotation_type']) + '. Origen: ' + esc(item['annotation_provenance']) + '. ' + esc(item['annotation_vs_proposal']) + '</p>'
            if item['related_file_id']:
                details += '<small>Coincidencia cotejada: ' + esc(item['related_file_id']) + ', pregunta ' + esc(item['related_question']) + '</small>'
            parts.append(f'<tr><td><a href="{esc(href)}#page={item["physical_page"]}">{item["question"]} / {item["physical_page"]}</a></td><td>{esc(item["area"])}<br>{esc(item["topic"])}<small>{esc(item["competency_proposal"] or "No aplica")}</small><small>{esc(item["process_proposal"])}</small><small>{esc(item["context_title"])}</small></td><td>{esc(item["answer_proposal"] or "Sin cerrar / no aplica")}<small>Marca: {esc(item["observed_highlight"] or "No documentada")}</small><small>{esc(item["highlight_vs_proposal"])}</small></td><td>{details}</td></tr>')
        parts.append('</tbody></table>')
    parts.append('</html>')
    return ''.join(parts)


def main():
    with closing(catalog.db()) as conn:
        items = collect(conn)
        occurrences = collect_occurrences(conn, items)
        file_count = conn.execute('SELECT count(*) FROM files WHERE duplicate_of IS NULL').fetchone()[0]
    output = catalog.AUDIT / 'preguntas_revisadas'
    output.mkdir(exist_ok=True)
    (output / 'apariciones_repetidas.json').write_text(
        json.dumps(occurrences, indent=2, ensure_ascii=False), encoding='utf-8')
    with (output / 'preguntas.jsonl').open('w', encoding='utf-8') as handle:
        for item in items:
            handle.write(json.dumps(item, ensure_ascii=False) + '\n')
    fields = [key for key in items[0] if key not in ('details', 'context_details')] if items else ['file_id', 'question']
    with (output / 'preguntas.csv').open('w', encoding='utf-8-sig', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction='ignore', delimiter=';')
        writer.writeheader()
        writer.writerows(items)
    counts = Counter(item['file_id'] for item in items)
    academics = sum(not item['exclude_academic'] for item in items)
    item_lookup = {(item['file_id'], item['question']): item for item in items}
    academic_references = sum(not item_lookup[(ref['canonical_file_id'], ref['canonical_question'])]['exclude_academic']
                              for ref in occurrences)
    summary = {'retained_files': file_count, 'files_with_manual_question_reviews': len(counts),
               'files_with_reviews_or_exact_references': len(set(counts) | {ref['file_id'] for ref in occurrences}),
               'academic_items_initially_reviewed': academics,
               'excluded_self_report_items': len(items) - academics,
               'all_collection_complete': False,
               'manual_counts_by_file': dict(counts),
               'exact_duplicate_occurrences_linked': len(occurrences),
               'academic_exact_repeat_occurrences': academic_references,
               'academic_source_appearances': academics + academic_references,
               'self_report_exact_repeat_occurrences': len(occurrences)-academic_references,
               'unique_question_audit_complete': False,
               'warning': 'Counts indicate initial analysis, not teacher validation or completed variant comparison.'}
    (output / 'avance.json').write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding='utf-8')
    (output / 'INDICE.html').write_text(review_html(items, summary), encoding='utf-8')
    relations = [dict(file_id=item['file_id'], question=item['question'],
                      physical_page=item['physical_page'], related_file_id=item['related_file_id'],
                      related_question=item['related_question'], related_physical_page=item['related_physical_page'],
                      status='coincidencia_visual_en_alcance_revisado_no_duplicado_binario')
                 for item in items if item['related_file_id'] and item['related_question']]
    (output / 'coincidencias_revisadas.json').write_text(json.dumps(relations, indent=2, ensure_ascii=False), encoding='utf-8')
    lines = ['# Preguntas revisadas: avance verificable', '',
             f'PDF conservados: {file_count}. PDF con preguntas documentadas: {len(counts)}.',
             f'Preguntas academicas con analisis inicial: {academics}. Autoinformes excluidos: {len(items)-academics}.',
             '', 'No es una coleccion terminada ni una clave oficial. Las propuestas requieren revision docente.',
             'Las paginas son fisicas del PDF; no confundir con la numeracion impresa.',
             'JSONL conserva detalles y CSV permite filtrar sin cargar en Excel todos los PDF.', '']
    for file_id in counts:
        group = [item for item in items if item['file_id'] == file_id]
        lines.extend([f'## {file_id}', '', f'Fuente: {group[0]["source_path"]}', ''])
        for item in group:
            lines.extend([f'### Pregunta {item["question"]} - pagina fisica {item["physical_page"]}',
                          f'Area: {item["area"]}. Tema: {item["topic"]}.',
                          f'Competencia propuesta: {item["competency_proposal"] or "No aplica"}.',
                          f'Proceso propuesto: {item["process_proposal"] or "No separado"}.',
                          f'Clave propuesta: {item["answer_proposal"] or "Sin cerrar / no aplica"}.',
                          item['reason'] or 'Autoinforme excluido del banco academico.'])
            if item['alert']:
                lines.append('ALERTA: ' + item['alert'])
            if item['observed_highlight']:
                lines.append('Marca visible del ejemplar (no oficial): ' + item['observed_highlight'])
            if item.get('annotation_value'):
                lines.append('Anotacion del ejemplar (NO oficial): ' + item['annotation_value'] + ' - ' + str(item['annotation_type']) + '; origen: ' + str(item['annotation_provenance']) + '; ' + item['annotation_vs_proposal'])
            if item['ocr_correction']:
                lines.append('CORRECCION OCR: ' + item['ocr_correction'])
            lines.append('')
    (output / 'LEEME.md').write_text('\n'.join(lines), encoding='utf-8')
    print(json.dumps(summary, ensure_ascii=True))


if __name__ == '__main__':
    main()
