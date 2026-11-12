"""Import reviewed PDF regions into a NEW editor project, never the active project.

PDF/OCR supplies candidates, not automatic academic validation. A manifest records
the visually checked corrections, keys and classification; uncertain fields stop
the import. Scans use the existing local Windows OCR helper, without cloud calls.
"""
import argparse
import copy
import hashlib
import json
import re
import subprocess
import tempfile
from pathlib import Path, PureWindowsPath

import pymupdf
from editor_model import ROOT, blank_assessment, validate_project, selected_questions


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def equivalent_codes(catalog, archive=None):
    graph={}
    def connect(a,b):
        graph.setdefault(a,set()).add(b)
        graph.setdefault(b,set()).add(a)
    def code(file_id,number):
        return f'{file_id}-Q{number:03d}'
    for row in catalog:
        for source in row.get('additional_source_evidence',[]):
            connect(row['catalog_id'],code(source['file_id'],source['question']))
        for source in (row,row.get('details',{})):
            if source.get('related_file_id') and source.get('related_question'):
                connect(row['catalog_id'],code(source['related_file_id'],source['related_question']))
    for row in (archive or {}).get('removed_full_reviews',[]):
        connect(code(row['file_id'],row['item']['question']),code(*row['canonical']))
    reviewed=ROOT/'tool/manifests/sp002_social_equivalences.json'
    if reviewed.is_file():
        for family in json.loads(reviewed.read_text(encoding='utf-8'))['visual_confirmed']:
            for other in family['codes'][1:]:
                connect(family['codes'][0],other)
    def expand(value):
        found={value}
        pending=[value]
        while pending:
            for other in graph.get(pending.pop(),set()):
                if other not in found:
                    found.add(other)
                    pending.append(other)
        return found
    return expand


def source_path(row,collection):
    # The catalogue records E:, but the same collection can be mounted elsewhere.
    parts=PureWindowsPath(row['source_path']).parts
    if len(parts)<3 or parts[1].lower()!='icfes_saberplus':
        raise ValueError('Ruta de catálogo no reconocida.')
    path=Path(collection).joinpath(*parts[2:]).resolve()
    if not path.is_relative_to(Path(collection).resolve()):
        raise ValueError('Fuente fuera de la colección autorizada.')
    if digest(path.read_bytes())!=row['source_sha256']:
        raise ValueError('La huella del PDF no coincide con el catálogo: '+str(path))
    return path


def region_rect(page,bounds):
    if (not isinstance(bounds,list) or len(bounds)!=4
            or any(type(v) not in (int,float) or not 0<=v<=1 for v in bounds)
            or bounds[0]>=bounds[2] or bounds[1]>=bounds[3]):
        raise ValueError('La región debe tener cuatro coordenadas normalizadas válidas.')
    return pymupdf.Rect(bounds[0]*page.rect.width,bounds[1]*page.rect.height,
                        bounds[2]*page.rect.width,bounds[3]*page.rect.height)


def windows_ocr(page,rect):
    with tempfile.TemporaryDirectory(prefix='saberplus-import-ocr-') as folder:
        folder=Path(folder)
        page.get_pixmap(matrix=pymupdf.Matrix(3,3),clip=rect,alpha=False).save(folder/'1.png')
        output=folder/'ocr.jsonl'
        result=subprocess.run(['powershell.exe','-NoProfile','-File',str(ROOT/'tool/usb_native_ocr.ps1'),
            '-InputFolder',str(folder),'-OutputFile',str(output)],capture_output=True,timeout=120)
        if result.returncode or not output.exists():
            raise ValueError('No se pudo extraer el escaneo con el OCR local.')
        record=json.loads(output.read_text(encoding='utf-8-sig').splitlines()[0])
        if record.get('error'):
            raise ValueError('OCR: '+record['error'])
        return record.get('text','')


def extract_region(page,bounds,ocr=windows_ocr):
    rect=region_rect(page,bounds)
    text=page.get_text('text',clip=rect).strip()
    method='native'
    if len(text)<30:
        text=ocr(page,rect).strip()
        method='windows_ocr'
    try:
        tables=len(page.find_tables(clip=rect).tables) if method=='native' else None
    except (ValueError,RuntimeError):
        tables=None
    signals={'raster_images':len(page.get_image_info()),'vector_paths':len(page.get_drawings()),
             'native_tables':tables,'scanned':method!='native'}
    return text,method,signals


def crop_asset(doc,image,default_page,assets):
    """Crop a visually reviewed source region at fixed scale, preserving aspect ratio."""
    if not image.get('verified_unmarked'):
        raise ValueError('Recurso gráfico sin cotejo de datos y marcas.')
    page=doc[image.get('page',default_page)-1]
    rect=region_rect(page,image['region'])
    raw=page.get_pixmap(matrix=pymupdf.Matrix(3,3),clip=rect,alpha=False).tobytes('png')
    name='assets/uploads/'+digest(raw)[:32]+'.png'
    assets[name]=raw
    return name


def parse_question(text,number):
    text=re.sub(r'^\s*'+str(number)+r'[.)]\s*','',text.strip(),count=1)
    matches=list(re.finditer(r'(?m)^\s*([A-D])[.)]\s+',text))
    if [m[1] for m in matches]!=list('ABCD'):
        return None
    return {'stem':text[:matches[0].start()].strip(),
            'options':[text[m.end():(matches[i+1].start() if i+1<len(matches) else len(text))].strip()
                       for i,m in enumerate(matches)]}


def content_key(question,contexts):
    context=contexts.get(question.get('context'),{})
    value=[context.get('text',''),question.get('introduction',''),question.get('stem',''),
           [(o.get('text',''),o.get('image','')) for o in question.get('options',[])]]
    return re.sub(r'\W+','',json.dumps(value,ensure_ascii=False).lower())


def build_import(base,manifest,catalog,collection,blocked=(),expand=lambda c:{c},ocr=windows_ocr):
    expected=manifest.get('expected_base_questions')
    if expected is not None and len(base['questions'])!=expected:
        raise ValueError(f'La base tiene {len(base["questions"])} preguntas; se requieren {expected}. No se completará con datos inventados.')
    validate_project(base)
    original=copy.deepcopy(base)
    result=copy.deepcopy(base)
    rows={r['catalog_id']:r for r in catalog}
    existing={q.get('catalog_id') for q in base['questions'] if q.get('catalog_id')}
    for code in existing:
        if sum(q.get('catalog_id')==code for q in base['questions'])>1:
            raise ValueError('La base contiene un código repetido: '+code)
    contexts={c['id']:c for c in base['contexts']}
    fingerprints={content_key(q,contexts) for q in base['questions']}
    report=[]
    assets={}
    context_ids={}
    for ctx in manifest.get('contexts',[]):
        if not ctx.get('verified') or not ctx.get('text','').strip():
            raise ValueError('Contexto sin texto cotejado.')
        cid='ctx-import-'+digest(ctx['key'].encode())[:24]
        if cid in contexts or ctx['key'] in context_ids:
            raise ValueError('Contexto repetido en el lote.')
        value={'id':cid,'area':ctx['area'],'part':0,'title':ctx.get('title',''),
               'text':ctx['text'],'source':ctx.get('source',''),'layout':'full',
               'instructions':'','table':'','words':[],'example':''}
        if ctx.get('visual_required') and not ctx.get('assets'):
            raise ValueError('El contexto requiere un recurso gráfico: '+ctx['key'])
        if ctx.get('assets'):
            source=rows[ctx['source_catalog_id']]
            with pymupdf.open(source_path(source,collection)) as doc:
                for image in ctx['assets']:
                    if value.get('image'):
                        raise ValueError('Combina los recursos del contexto en una región revisada.')
                    value['image']=crop_asset(doc,image,source['physical_page'],assets)
        result['contexts'].append(value)
        contexts[cid]=value
        context_ids[ctx['key']]=cid
    for item in manifest['questions']:
        code=item['catalog_id']
        if code not in rows:
            raise ValueError('Código inexistente en el catálogo: '+code)
        row=rows[code]
        if row.get('area_normalized')!='Sociales y ciudadanas' or item.get('area')!='social':
            raise ValueError('Área no coincide con la fuente: '+code)
        family=expand(code)
        if family.intersection(existing|set(blocked)):
            raise ValueError('Código usado, candidato activo o equivalente: '+code)
        if item['page']!=row['physical_page']:
            raise ValueError('La página no corresponde a la ficha: '+code)
        if row.get('context_id') and not item.get('context_key'):
            raise ValueError('Falta el contexto compartido documentado: '+code)
        if item.get('context_key') and item['context_key'] not in context_ids:
            raise ValueError('Contexto declarado ausente del lote: '+code)
        path=source_path(row,collection)
        with pymupdf.open(path) as doc:
            page=doc[item['page']-1]
            raw,method,signals=extract_region(page,item['region'],ocr)
            extracted=parse_question(raw,row['question'])
            reviewed=item.get('reviewed_text')
            if not item.get('verified'):
                raise ValueError('Falta cotejo visual de texto, opciones y clave: '+code)
            fields=reviewed or extracted
            if not fields or not fields.get('stem') or len(fields.get('options',[]))!=4 or not all(fields['options']):
                raise ValueError('Enunciado u opciones ilegibles/incompletos: '+code)
            if not isinstance(item.get('correct'),str) or item['correct'] not in 'ABCD' or not item.get('explanation','').strip():
                raise ValueError('Clave o explicación sin sustento: '+code)
            assessment=blank_assessment(item['area'])
            assessment.update(status='proposed',competency=item['competency'],rationale=item['rationale'])
            question={'id':'q-import-'+digest(code.encode())[:24], 'area':item['area'],'part':0,
                'order':item['order'],'topic':item['topic'],'subtopic':item['subtopic'],
                'stem':fields['stem'],'options':[{'text':o} for o in fields['options']],
                'correct':item['correct'],'explanation':item['explanation'],'layout':item.get('layout','full'),
                'included':True,'context':context_ids.get(item.get('context_key')),'slot':'',
                'assessment':assessment,'catalog_id':code,'option_drafts':{},
                'provenance':{'pdf_sha256':row['source_sha256'],'file_id':row['file_id'],
                    'physical_page':item['page'],'original_question':row['question'],
                    'region':item['region'],'method':method,'editorial_status':'propuesta_pendiente_coordinacion'}}
            if item.get('image_height'):
                question['image_height']=item['image_height']
            if item.get('image_width'):
                question['image_width']=item['image_width']
            visual_hint=bool(re.search(r'\b(gráfic[ao]|figura|imagen|mapa|tabla|caricatura|infografía|fotografía|diagrama)\b',
                raw+' '+row.get('topic',''),re.I))
            if (item.get('visual_required') or visual_hint) and not (item.get('assets') or item.get('context_key')):
                raise ValueError('La pregunta parece necesitar una imagen y no tiene recorte: '+code)
            for image in item.get('assets',[]):
                name=crop_asset(doc,image,item['page'],assets)
                if image.get('option'):
                    if image['option'] not in 'ABCD':
                        raise ValueError('Letra de recurso gráfico inválida: '+code)
                    question['options']['ABCD'.index(image['option'])]['image']=name
                else:
                    if question.get('image'):
                        raise ValueError('Combina los recursos del enunciado en una sola región revisada.')
                    question['image']=name
            key=content_key(question,contexts)
            if key in fingerprints:
                raise ValueError('Contenido repetido aunque cambie el código: '+code)
            result['questions'].append(question)
            fingerprints.add(key)
            existing.update(family)
            report.append({'catalog_id':code,'source':str(path),'physical_page':item['page'],
                'original_question':row['question'],'raw_text':raw,'method':method,'visual_signals':signals,
                'parsed_automatically':extracted is not None,'reviewed_correction':reviewed is not None,
                'visual_hint':visual_hint,'visual_required':bool(item.get('visual_required')),
                'assets':[image['region'] for image in item.get('assets',[])],
                'quality_flags':(['OCR cotejado: revisar fidelidad y marcas de agua.'] if method!='native' else [])+
                    (['Revisión de recorte visual requerida.'] if item.get('assets') else []),
                'status':'propuesta; cotejos de variantes y aprobación del coordinador pendientes'})
    validate_project(result,exporting=True)
    if result['questions'][:len(original['questions'])]!=original['questions'] or result['contexts'][:len(original['contexts'])]!=original['contexts'] or base!=original:
        raise AssertionError('Se alteraron preguntas/contextos anteriores.')
    if manifest.get('expected_total') is not None and len(result['questions'])!=manifest['expected_total']:
        raise ValueError('El total importado no coincide con el total esperado.')
    return result,{'base_questions':len(original['questions']),'questions':len(result['questions']),
        'preserved_base':True,'selected_questions':len(selected_questions(result)),'items':report},assets


def coordination_inputs():
    registry=json.loads((ROOT/'planning/PREGUNTAS_USADAS_GLOBAL.json').read_text(encoding='utf-8'))
    blocked={r['catalog_id'] for r in registry['preguntas']+registry.get('reservas',[]) if r.get('catalog_id')}
    texts=[]
    for path in ['planning/SP001_S1_SOCIALES_CANDIDATAS.md']:
        texts.append((ROOT/path).read_text(encoding='utf-8'))
    try:
        texts.append(subprocess.check_output(['git','show','origin/trabajo/sp-003:planning/reservas/SP-003.md'],cwd=ROOT).decode('utf-8'))
    except subprocess.CalledProcessError as exc:
        raise ValueError('No se pudieron consultar las reservas locales de SP-003.') from exc
    for text in texts:
        # Only table rows: narrative examples and historical warnings are not reservations.
        for line in text.splitlines():
            if line.startswith('|'):
                blocked.update(re.findall(r'USB-[a-f0-9]{12}-Q\d{3}',line))
    return blocked


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base',type=Path,required=True)
    parser.add_argument('--manifest',type=Path,required=True)
    parser.add_argument('--collection',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True,help='Carpeta NUEVA e independiente; nunca data/.')
    args=parser.parse_args()
    out=args.output.resolve()
    if out.is_relative_to((ROOT/'data').resolve()) or out.exists() or args.base.resolve().is_relative_to(out):
        parser.error('La salida debe ser una carpeta nueva, independiente de data/ y de la base.')
    original=args.base.read_bytes()
    catalog=json.loads((ROOT/'output/cotejo_30/indice_editorial.json').read_text(encoding='utf-8'))
    archive=json.loads((ROOT/'output/cotejo_30/archivo_fichas_consolidadas.json').read_text(encoding='utf-8'))
    project,report,assets=build_import(json.loads(original),json.loads(args.manifest.read_text(encoding='utf-8')),
        catalog,args.collection,coordination_inputs(),equivalent_codes(catalog,archive))
    if args.base.read_bytes()!=original:
        raise ValueError('La base cambió durante la lectura: vuelve a ejecutar con una copia estable.')
    out.mkdir(parents=True)
    referenced={value['image'] for value in project['contexts']+project['questions'] if value.get('image')}
    referenced.update(option['image'] for q in project['questions'] for option in q.get('options',[]) if option.get('image'))
    for path in referenced:
        if path not in assets:
            original_asset=ROOT/path
            if not original_asset.is_file():
                raise ValueError('Imagen anterior no encontrada: '+path)
            assets[path]=original_asset.read_bytes()
    for path,raw in assets.items():
        target=ROOT/path
        if target.exists() and target.read_bytes()!=raw:
            raise ValueError('Colisión de recurso gráfico; no se sobrescribirá.')
        target.parent.mkdir(parents=True,exist_ok=True)
        if not target.exists():
            target.write_bytes(raw)
        pilot_asset=out/path
        pilot_asset.parent.mkdir(parents=True,exist_ok=True)
        pilot_asset.write_bytes(raw)
    report['base_sha256']=digest(original)
    (out/'project.json').write_text(json.dumps(project,ensure_ascii=False,indent=2),encoding='utf-8')
    (out/'import-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'project':str(out/'project.json'),'questions':len(project['questions']),
                      'report':str(out/'import-report.json')},ensure_ascii=False))


if __name__=='__main__':
    main()
