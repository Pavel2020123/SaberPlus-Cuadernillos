"""Measured two-column editorial renderer. Keys never enter the student PDF."""
import copy
import json
import re
import subprocess
import sys
from io import BytesIO
from pathlib import Path
from xml.sax.saxutils import escape

import pymupdf as fitz
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, Image, Table, TableStyle, Spacer, Flowable
from PIL import Image as PILImage, ImageChops
from editor_model import ROOT, AREAS, SESSIONS, validate_project, selected_questions, blank_assessment, range_heading
from assessment_metadata import STATUS_LABELS

W, H = A4
M, GAP, BOTTOM = 38, 22, 48
WIDTH = W-2*M
CW = (WIDTH-GAP)/2
INK = colors.HexColor('#17263A')
GRAY = colors.HexColor('#87909A')


def para(text, size=10, bold=False):
    # Convert Unicode superscripts into real raised text supported by Helvetica.
    # Escape first: editorial text must never become arbitrary ReportLab markup.
    superscripts = '⁰¹²³⁴⁵⁶⁷⁸⁹ⁿⁱ⁺⁻⁼⁽⁾'
    normal = '0123456789ni+-=()'
    markup = escape(str(text)).replace('\n', '<br/>')
    equation = re.fullmatch(r'((?:[A-G]\.\s*)?)([A-Za-z]\s*=\s*[A-Za-z0-9⁰¹²³⁴⁵⁶⁷⁸⁹ⁿⁱ⁺⁻⁼⁽⁾+−*/^() .-]+)',str(text))
    if equation:
        # Explicit equation-shaped options only; never italicize ordinary prose.
        expression = re.sub(r'[A-Za-z]',lambda m:'<i>'+m.group()+'</i>',escape(equation[2]))
        markup = escape(equation[1])+expression
    markup = re.sub('['+superscripts+']+',
                    lambda match: '<super>'+re.sub(r'[ni]',r'<i>\g<0></i>',match.group().translate(str.maketrans(superscripts, normal)))+'</super>', markup)
    return Paragraph(markup, ParagraphStyle(
        'body', fontName='Times-Roman' if equation else 'Helvetica-Bold' if bold else 'Helvetica', fontSize=size,
        leading=size*1.33, textColor=INK, spaceAfter=0))


def picture(path, width, max_height=190, trim=False):
    resolved = (ROOT/path).resolve()
    if not resolved.is_relative_to((ROOT/'assets/uploads').resolve()) or not resolved.is_file():
        raise ValueError('No se encuentra una imagen cargada: '+path)
    source = str(resolved)
    if trim:
        # Trim only empty outer white/transparent margins in memory. The upload
        # stays intact; interior whitespace, lines and watermarks are untouched.
        with PILImage.open(resolved) as original:
            rgba=original.convert('RGBA')
            white=PILImage.new('RGBA',rgba.size,'white')
            white.alpha_composite(rgba)
            rgb=white.convert('RGB')
            difference=ImageChops.difference(rgb,PILImage.new('RGB',rgb.size,'white'))
            # Ignore only near-white compression noise at the outer boundary.
            mask=difference.convert('L').point(lambda value:255 if value>8 else 0)
            bounds=mask.getbbox()
            if bounds:
                left,top,right,bottom=bounds
                bounds=(max(0,left-6),max(0,top-6),min(rgb.width,right+6),min(rgb.height,bottom+6))
                buffer=BytesIO()
                rgb.crop(bounds).save(buffer,format='PNG')
                buffer.seek(0)
                source=buffer
    img = Image(source)
    scale = min(width/img.imageWidth, max_height/img.imageHeight, 1)
    img.drawWidth, img.drawHeight = img.imageWidth*scale, img.imageHeight*scale
    return img


def measure(flows, width):
    return sum(f.wrap(width, H)[1] for f in flows)


def draw(flows, c, x, top, width):
    for f in flows:
        fw, fh = f.wrap(width, H)
        f.drawOn(c, x+(width-fw)/2 if isinstance(f, Image) else x, top-fh)
        top -= fh
    return top


class TrackedOption(Flowable):
    """Record the printed option bounds without putting a key in student content."""
    def __init__(self, flows, book, correct):
        super().__init__()
        self.flows,self.book,self.correct=flows,book,correct

    def wrap(self, width, height):
        self.width=width
        self.height=measure(self.flows,width)
        return self.width,self.height

    def draw(self):
        if self.correct:
            x,y=self.canv.absolutePosition(0,0)
            self.book.answer_marks.append({'kind':'option','page':self.book.page,
                'rect':(x-2,H-y-self.height-2,x+self.width+2,H-y+2)})
        draw(self.flows,self.canv,0,self.height,self.width)


class BubbleRow(Flowable):
    """Vector circles, filled for the teacher or tracked for the solved copy."""
    def __init__(self, letters, number=None, marked=None, book=None, answer=None):
        super().__init__()
        self.letters,self.number,self.marked,self.book,self.answer=letters,number,marked,book,answer
        self.height=25

    def wrap(self,width,height):
        self.width=width
        return width,self.height

    def draw(self):
        c=self.canv
        c.saveState()
        c.setFillColor(INK)
        c.setFont('Helvetica-Bold',9)
        if self.number is not None:
            c.drawString(0,8,f'{self.number:03d}')
        start=35 if self.number is not None else 10
        for i,letter in enumerate(self.letters):
            x,y=start+i*23,11
            filled=letter==self.marked
            c.setStrokeColor(INK)
            c.setLineWidth(.65)
            c.setFillColor(INK if filled else colors.white)
            c.circle(x,y,6.5,stroke=1,fill=1)
            c.setFillColor(colors.white if filled else INK)
            c.setFont('Helvetica-Bold' if filled else 'Helvetica',7)
            c.drawCentredString(x,y-2.4,letter)
            if self.book and letter==self.answer:
                ax,ay=c.absolutePosition(x,y)
                self.book.answer_marks.append({'kind':'bubble','page':self.book.page,'center':(ax,H-ay),'letter':letter})
        c.restoreState()


def letters_for(q):
    return 'ABCDEFG' if q['area']=='english' and q['part']==1 else 'ABCD'[:len(q['options'])]


def column_block(book,flows):
    height=measure(flows,CW)
    if height>H-83-BOTTOM:
        raise ValueError('Un bloque de la hoja de respuestas excede el espacio disponible.')
    if book.ys[book.col]-height<BOTTOM:
        if book.col==0:
            book.col=1
        else:
            book.newpage()
    book.ys[book.col]=draw(flows,book.c,M+book.col*(CW+GAP),book.ys[book.col],CW)
    book.used[book.col]=True


def answer_sheet(book,questions,numbers,teacher=False):
    book.newpage('CLAVE DE RESPUESTAS · DOCENTE' if teacher else 'HOJA DE RESPUESTAS')
    intro=[para('USO EXCLUSIVO DEL DOCENTE' if teacher else 'Nombre: ____________________________________    Grupo: __________',9,teacher),Spacer(1,6),
           para('El círculo lleno indica la respuesta correcta. No entregar antes de finalizar la prueba.' if teacher else 'Rellene un solo círculo por pregunta. Las letras disponibles dependen del tipo de ejercicio.',9)]
    book.full(intro)
    previous=None
    for q in questions:
        flows=[]
        if q['area']!=previous:
            flows=[Spacer(1,5),para(AREAS[q['area']],9,True),Spacer(1,5)]
            previous=q['area']
        flows.append(BubbleRow(letters_for(q),numbers[q['id']],marked=q['correct'] if teacher else None,
                              book=None if teacher else book,answer=q['correct']))
        column_block(book,flows)


def solved_copy(student_path,out,project,questions,numbers,marks):
    """Overlay measured marks on an exact copy; explanations are appended afterwards."""
    doc=fitz.open(student_path)
    for i,page in enumerate(doc):
        labels=page.search_for(project['code']+' · BORRADOR')
        if i==0:
            labels+=page.search_for('CUADERNILLO DEL ESTUDIANTE')
        for rect in labels:
            page.add_redact_annot(rect,fill=(1,1,1))
        if labels:
            page.apply_redactions()
            for rect in labels:
                title='CUADERNILLO RESUELTO' if i==0 else project['code']+' · RESUELTO'
                page.insert_text((rect.x0,rect.y1-1.5),title,fontname='hebo',fontsize=7,color=(.09,.15,.23))
    for mark in marks:
        page=doc[mark['page']-1]
        if mark['kind']=='option':
            page.draw_rect(fitz.Rect(mark['rect']),color=(.58,.47,.12),fill=(1,.93,.45),
                           fill_opacity=.38,width=.65,overlay=True)
        else:
            x,y=mark['center']
            page.draw_circle((x,y),6.5,color=(.09,.15,.23),fill=(.09,.15,.23),width=.65)
            text_width=fitz.get_text_length(mark['letter'],fontname='hebo',fontsize=7)
            page.insert_text((x-text_width/2,y+2.4),mark['letter'],fontname='hebo',fontsize=7,color=(1,1,1))
    for page in doc:
        page.insert_text((M,H-10),'CUADERNILLO RESUELTO - COMPARTIR DESPUES DE LA APLICACION',fontsize=6,color=(.3,.3,.3))
    explanations=Interior(out/'explicaciones.pdf',project,start_page=len(doc)+1,resolved=True)
    explanations.newpage('RESPUESTAS EXPLICADAS')
    explanations.full([para('Revisa el razonamiento de cada respuesta',13,True),Spacer(1,7),
                       para('Las explicaciones corresponden a la misma numeración de este cuadernillo. Son material de repaso, no un informe de desempeño oficial.',9)])
    for q in questions:
        explanations.full([para(f'Pregunta {numbers[q["id"]]} · {AREAS[q["area"]]} · Respuesta {q["correct"]}',11,True),
                           Spacer(1,7),para(q['explanation'])],True)
    explanations.close()
    with fitz.open(out/'explicaciones.pdf') as extra:
        doc.insert_pdf(extra)
    doc.set_metadata({'title':project['code']+' · Cuadernillo resuelto','author':'SaberPlus'})
    doc.save(out/'cuadernillo_resuelto.pdf')
    doc.close()


class Interior:
    def __init__(self, path, project, start_page=3, resolved=False):
        self.c = canvas.Canvas(str(path), pagesize=A4)
        self.c.setTitle(project['code']+' · Cuadernillo del estudiante')
        self.project, self.page, self.open = project, start_page-1, False
        self.area = ''
        self.resolved = resolved
        self.answer_marks=[]

    def flush(self):
        if self.segment and (self.used[0] or self.used[1]):
            self.c.setStrokeColor(GRAY)
            self.c.setLineWidth(.45)
            self.c.line(W/2, self.segment, W/2, min(self.ys))
        bottom = min(self.ys)
        self.segment = 0
        return bottom

    def newpage(self, area=None, show_area=True, opening_title=None):
        if area is None and getattr(self,'content_area',False):
            show_area=False
        if self.open:
            self.flush()
            self.c.showPage()
        self.open = True
        self.page += 1
        if area is not None:
            self.area = area
        c = self.c
        c.setFillColor(INK)
        c.setFont('Helvetica-Bold', 11)
        c.drawString(M, H-32, 'SaberPlus')
        c.setFont('Helvetica', 8)
        c.drawRightString(W-M, H-32, self.project['code']+(' · RESUELTO' if self.resolved else ' · BORRADOR'))
        if opening_title:
            available=WIDTH-2*max(c.stringWidth('SaberPlus','Helvetica-Bold',11),
                c.stringWidth(self.project['code']+' · RESUELTO','Helvetica',8))-24
            size=10
            while size>7 and c.stringWidth(opening_title,'Helvetica-Bold',size)>available:
                size-=.5
            if c.stringWidth(opening_title,'Helvetica-Bold',size)>available:
                raise ValueError('El título del área es demasiado largo para el encabezado; acórtalo.')
            c.setFont('Helvetica-Bold',size)
            c.drawCentredString(W/2,H-32,opening_title)
        c.setStrokeColor(INK)
        c.line(M, H-42, W-M, H-42)
        if show_area:
            c.setFont('Helvetica-Bold', 13)
            c.drawString(M, H-64, self.area)
        c.setFont('Helvetica', 7)
        c.setFillColor(GRAY)
        c.drawString(M, 27, self.project['code']+' · '+('Primera sesión' if self.project['session']=='first' else 'Segunda sesión'))
        c.drawRightString(W-M, 27, str(self.page))
        c.setFont('Helvetica-Bold', 13)
        c.drawRightString(W-M-22, 25, 'S+')
        if self.resolved:
            c.setFont('Helvetica', 6)
            c.drawString(M, 10, 'CUADERNILLO RESUELTO - COMPARTIR DESPUES DE LA APLICACION')
        self.reset(H-83 if show_area else H-55)

    def reset(self, top):
        self.segment, self.ys, self.used, self.col = top, [top, top], [False, False], 0

    def full(self, flows, box=False, reserve=0, shaded=False, separator=False):
        top = self.flush()
        padding = 6 if separator else 9
        gap = 8 if separator else 14
        height = measure(flows, WIDTH-18)+2*padding
        if height+reserve > H-83-BOTTOM:
            raise ValueError('Un bloque compartido excede una página. Divide el texto en contextos más breves o reduce su imagen.')
        if top-height-reserve < BOTTOM:
            self.newpage()
            top = self.flush()
        if box:
            self.c.setStrokeColor(GRAY)
            self.c.setLineWidth(.65)
            self.c.setFillColor(colors.HexColor('#EEF1F4'))
            self.c.roundRect(M, top-height, WIDTH, height, 5, fill=int(shaded), stroke=1)
        draw(flows, self.c, M+9, top-padding, WIDTH-18)
        if separator:
            self.c.setStrokeColor(GRAY)
            self.c.setLineWidth(.5)
            self.c.line(M,top-height,W-M,top-height)
        self.reset(top-height-gap)

    def question_flows(self, q, number, matching=False):
        compact = (q['area']=='english' and q['part'] in (4,7)
                   and not q.get('introduction') and not q.get('image') and not any(o.get('image') for o in q['options']))
        if compact:
            cells=[para(str(number)+'.',10,True)]+[TrackedOption([para(letter+'. '+o.get('text',''),10)],self,letter==q['correct']) for letter,o in zip('ABCD',q['options'])]
            table=Table([cells],colWidths=[30]+[(WIDTH-48)/len(q['options'])]*len(q['options']))
            table.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),0)]))
            return [table], True, True
        full = q['layout']=='full'
        width = WIDTH if full else CW
        stem = q['stem'].replace('{{numero}}', str(number))
        introduction = q.get('introduction', '').strip().replace('{{numero}}', str(number))
        flows = []
        if introduction or q.get('image'):
            flows += [para(f'{number}.  '+introduction), Spacer(1, 5)]
        if q.get('image'):
            # A full-width block need not contain a full-width illustration.
            # Preserve proportions, with a smaller default for stacked questions.
            flows += [picture(q['image'], min(width-18,300) if full else width-18,
                              q.get('image_height',110 if full else 190),trim=True), Spacer(1, 5)]
        flows += [para(stem if introduction or q.get('image') else f'{number}.  '+stem), Spacer(1, 5)]
        if matching:
            flows += [para('Respuesta: A   B   C   D   E   F   G', 9)]
        else:
            for letter, option in zip('ABCD', q['options']):
                option_flows=[para(letter+'.  '+option.get('text', ''))]
                if option.get('image'):
                    option_flows += [Spacer(1,4),picture(option['image'], width-18, 100)]
                flows += [TrackedOption(option_flows,self,letter==q['correct']),Spacer(1,2)]
        return flows, full, False

    def question_height(self, q, number):
        flows, full, _ = self.question_flows(q, number)
        return measure(flows, (WIDTH if full else CW)-18)+(12 if full else 18)

    def shared_context(self, flows, first_question, number):
        reserve = self.question_height(first_question, number)+14
        if measure(flows, WIDTH-18)+18+reserve > H-83-BOTTOM:
            raise ValueError('El contexto y su primera pregunta no caben juntos en una página. '
                             'Divide el contexto o elige ancho completo para la pregunta: '+first_question['id'])
        self.full(flows, True, reserve=reserve)

    def question(self, q, number, matching=False):
        flows, full, compact = self.question_flows(q, number, matching)
        width = WIDTH if full else CW
        height = measure(flows, width-18)+18
        if height > H-83-BOTTOM:
            raise ValueError(f'La pregunta {number} no cabe sin recortar. Elige ancho completo o divide su contexto.')
        if full:
            self.full(flows, separator=not compact)
            return
        if self.ys[self.col]-height < BOTTOM:
            if self.col == 0:
                self.col = 1
            if self.ys[self.col]-height < BOTTOM:
                self.newpage()
        x, top = M+self.col*(CW+GAP), self.ys[self.col]
        self.c.setStrokeColor(GRAY)
        self.c.setLineWidth(.5)
        self.c.line(x, top-height, x+width, top-height)
        draw(flows, self.c, x+9, top-9, width-18)
        self.ys[self.col] = top-height-14
        self.used[self.col] = True

    def close(self):
        if self.open:
            self.flush()
        self.c.save()


def matching_descriptions(book, members, numbers):
    flows = [para('DESCRIPCIONES',10,True),Spacer(1,12)]
    for item in members:
        introduction = item.get('introduction', '').strip().replace('{{numero}}', str(numbers[item['id']]))
        if introduction or item.get('image'):
            flows += [para(str(numbers[item['id']])+'. '+introduction),Spacer(1,5)]
        if item.get('image'):
            flows += [picture(item['image'], (WIDTH-18)*.64-20, 100), Spacer(1,5)]
        flows += [para(item['stem'] if introduction or item.get('image') else str(numbers[item['id']])+'. '+item['stem']),Spacer(1,5)]
        flows += [BubbleRow('ABCDEFG',book=book,answer=item['correct']),Spacer(1,10)]
    return flows


def context_flows(ctx, members, numbers, show_words=True):
    flows = []
    first, last = numbers[members[0]['id']], numbers[members[-1]['id']]
    if ctx.get('part'):
        flows += [para('PARTE '+str(ctx['part']), 10, True), Spacer(1, 5)]
    flows += [para(range_heading(ctx.get('range_heading'), first, last), 9, True), Spacer(1, 7)]
    for key in ('instructions', 'title'):
        if ctx.get(key):
            flows += [para(ctx[key], 10, key=='title'), Spacer(1, 7)]
    text = ctx.get('text', '')
    for q in members:
        if q.get('slot'):
            text = text.replace('{{'+q['slot']+'}}', f'({numbers[q["id"]]}) __________')
    if text:
        flows += [para(text), Spacer(1, 8)]
    if ctx.get('image'):
        flows += [picture(ctx['image'], WIDTH-18, 220), Spacer(1, 8)]
    if ctx.get('table'):
        rows = [line.split(';') for line in ctx['table'].strip().splitlines()]
        ncols = max(map(len, rows))
        table = Table([[para(cell, 9) for cell in row]+['']*(ncols-len(row)) for row in rows], colWidths=[(WIDTH-18)/ncols]*ncols)
        table.setStyle(TableStyle([('GRID',(0,0),(-1,-1),.5,GRAY),('VALIGN',(0,0),(-1,-1),'TOP'),('BACKGROUND',(0,0),(-1,0),colors.HexColor('#EEF1F4')),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7)]))
        flows += [table, Spacer(1, 8)]
    if ctx.get('words') and show_words:
        flows += [para('PALABRAS:  '+'     '.join(letter+'. '+word for letter, word in zip('ABCDEFG',ctx['words'])),10,True)]
    if ctx.get('example'):
        flows += [Spacer(1, 6),para('Ejemplo resuelto: '+ctx['example'],9)]
    if ctx.get('source'):
        flows += [Spacer(1, 7),para('Fuente: '+ctx['source'],8)]
    return flows


def preview_project(project):
    """Use visible placeholders in a deep copy; never save or revise editorial content."""
    draft=copy.deepcopy(project)
    warnings=[]
    for q in draft.get('questions',[]):
        q['assessment']=blank_assessment(q['area'])
        if not q.get('stem','').strip():
            q['stem']='[Enunciado pendiente]'
            warnings.append('Hay enunciados pendientes.')
        matching=q['area']=='english' and q.get('part')==1
        count=0 if matching else 3 if q['area']=='english' and q.get('part') in (2,3,4,5) else 4
        opts=q.get('options',[])
        q['options']=[copy.deepcopy(opts[i]) if i<len(opts) else {} for i in range(count)]
        for option in q['options']:
            if not option.get('text','').strip() and not option.get('image'):
                option['text']='[Opción pendiente]'
                warnings.append('Hay opciones pendientes.')
        q['correct']='A'
        q['explanation']='Solo vista previa; sin clave de corrección.'
    if not selected_questions(draft):
        first=SESSIONS[draft['session']][0]
        draft['questions'].append({'id':'preview-empty','area':first,'part':0,'order':0,'layout':'columns','included':True,
            'stem':'[Aquí aparecerán tus preguntas al incluirlas en esta sesión.]',
            'options':[{'text':'[Opción pendiente]'} for _ in range(4)],'correct':'A',
            'explanation':'Vista previa','assessment':blank_assessment(first)})
        warnings.append('La sesión todavía está vacía: se muestra un espacio ilustrativo.')
    validate_project(draft)  # Structural failures must not disappear under placeholders.
    return draft, list(dict.fromkeys(warnings))


def generate(project, out, preview=False):
    warnings = validate_project(project, exporting=True)
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    selected = selected_questions(project)
    numbers = {q['id']: i for i,q in enumerate(selected,1)}
    ctxs = {c['id']: c for c in project['contexts']}
    cfg = json.loads((ROOT/'tool/editorial_cover_config.json').read_text(encoding='utf-8'))
    cfg.update(version=project['code'],session='Primera sesión' if project['session']=='first' else 'Segunda sesión',time=project.get('time') or 'Por definir',
               notice='BORRADOR EDITORIAL · Material de práctica. No es una prueba oficial.',
               areas=[{'name':AREAS[a],'count':sum(q['area']==a for q in selected)} for a in SESSIONS[project['session']]])
    (out/'cover.json').write_text(json.dumps(cfg,ensure_ascii=False),encoding='utf-8')
    subprocess.run([sys.executable,str(ROOT/'tool/preview_editorial_cover.py'),'--config',str(out/'cover.json'),'--output',str(out/'cover.pdf')],check=True,capture_output=True)
    book = Interior(out/'interior.pdf', project)
    last_area, seen, last_part = None, set(), None
    page_map={}
    for q in selected:
        if q['area'] != last_area:
            header=project.get('area_headers',{}).get(q['area'],{})
            book.content_area=True
            book.newpage(AREAS[q['area']].upper(),show_area=False,
                         opening_title=header.get('title','').strip() or AREAS[q['area']].upper())
            area_questions=[item for item in selected if item['area']==q['area']]
            first,last=numbers[area_questions[0]['id']],numbers[area_questions[-1]['id']]
            if header.get('instructions','').strip():
                book.full([para(range_heading(header['instructions'],first,last),10)],reserve=120)
            last_area, last_part = q['area'], None
        cid = q.get('context')
        if cid and cid not in seen:
            members = [item for item in selected if item.get('context')==cid]
            matching=q['area']=='english' and q['part']==1
            if matching:
                flows=context_flows(ctxs[cid],members,numbers,False)
                desc=matching_descriptions(book,members,numbers)
                words=[para('PALABRAS',10,True),Spacer(1,12)]
                for letter,word in zip('ABCDEFG',ctxs[cid]['words']):
                    words += [para(letter+'.   '+word),Spacer(1,13)]
                table=Table([[desc,words]],colWidths=[(WIDTH-18)*.64,(WIDTH-18)*.36])
                table.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LINEBEFORE',(1,0),(1,0),.5,GRAY),('LEFTPADDING',(0,0),(-1,-1),10),('RIGHTPADDING',(0,0),(-1,-1),10)]))
                flows += [Spacer(1,10),table]
                book.full(flows,False)
                page_map.update({item['id']:book.page for item in members})
            else:
                context = context_flows(ctxs[cid],members,numbers)
                book.shared_context(context,q,numbers[q['id']])
            seen.add(cid)
            last_part = q.get('part')
        elif q['area']=='english' and q['part']!=last_part:
            book.full([para('PARTE '+str(q['part']),11,True)],reserve=105)
            last_part=q['part']
        if not (q['area']=='english' and q['part']==1):
            book.question(q,numbers[q['id']])
            page_map[q['id']]=book.page
    answer_sheet(book,selected,numbers)
    book.close()
    merged=fitz.open()
    for name in ('cover.pdf','interior.pdf'):
        with fitz.open(out/name) as doc:
            merged.insert_pdf(doc)
    merged.save(out/'cuadernillo.pdf')
    merged.close()
    if preview:
        return {'warnings':warnings,'questions':len(selected),'page_map':page_map}
    solved_copy(out/'cuadernillo.pdf',out,project,selected,numbers,book.answer_marks)
    key=Interior(out/'clave_docente.pdf',project,start_page=1)
    answer_sheet(key,selected,numbers,teacher=True)
    key.close()
    teacher = Interior(out/'guia_docente.pdf',project,start_page=1)
    teacher.newpage('GUÍA DOCENTE · NO ENTREGAR AL ESTUDIANTE')
    teacher.full([para('Claves y clasificación editorial',13,True),Spacer(1,7),para('Clasificación interna de SaberPlus, sin requisito de revisión docente ni validación externa implícita. No asigna puntajes ni niveles oficiales.',9)])
    for q in selected:
        a=q['assessment']
        area=__import__('assessment_metadata').CATALOG['areas'][q['area']]
        label=area['competencies'].get(a.get('competency'),{}).get('label','Pendiente')
        flows=[para(f'{numbers[q["id"]]}. {AREAS[q["area"]]} · Clave {q["correct"]}',11,True),Spacer(1,6),para(q['explanation']),Spacer(1,6),para(f'Competencia: {label}. Clasificación: {STATUS_LABELS[a["status"]]}. Afirmación: {a.get("claim") or "—"}. Evidencia: {a.get("evidence") or "—"}.',9)]
        if a.get('rationale'):
            flows += [Spacer(1,5),para('Justificación: '+a['rationale'],9)]
        if a['status']=='reviewed' and a.get('reviewer'):
            flows += [para('Revisó: '+a['reviewer']+' · '+str(a.get('reviewed_at')),9)]
        teacher.full(flows,True)
    teacher.close()
    (out/'proyecto.json').write_text(json.dumps(project,ensure_ascii=False,indent=2),encoding='utf-8')
    (out/'numeracion_docente.json').write_text(json.dumps([{'number':numbers[q['id']],'id':q['id'],'answer':q['correct'],'assessment':q['assessment']} for q in selected],ensure_ascii=False,indent=2),encoding='utf-8')
    return {'warnings':warnings,'questions':len(selected),'student':'cuadernillo.pdf','solved':'cuadernillo_resuelto.pdf',
            'teacher':'clave_docente.pdf','review':'guia_docente.pdf','page_map':page_map}
