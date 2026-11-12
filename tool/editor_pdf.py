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
from reportlab.platypus import Paragraph, Image, Table, TableStyle, Spacer, Flowable, ParagraphAndImage, HRFlowable
from PIL import Image as PILImage, ImageChops
from editor_model import ROOT, AREAS, SESSIONS, validate_project, selected_questions, blank_assessment, range_heading
from assessment_metadata import STATUS_LABELS
from editor_math import math_paragraph
from column_planner import column_chunk

W, H = A4
M, GAP, BOTTOM = 38, 22, 48
WIDTH = W-2*M
CW = (WIDTH-GAP)/2
INK = colors.HexColor('#17263A')
GRAY = colors.HexColor('#87909A')


def para(text, size=10, bold=False):
    if any(delimiter in str(text) for delimiter in ('\\(','\\)','\\[','\\]')):
        return math_paragraph(text,ParagraphStyle('math-body',
            fontName='Helvetica-Bold' if bold else 'Helvetica',fontSize=size,
            leading=size*1.33,textColor=INK,spaceAfter=0))
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
    subscripts = '₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎'
    markup = re.sub('['+subscripts+']+',
                    lambda match: '<sub>'+match.group().translate(str.maketrans(subscripts,'0123456789+-=()'))+'</sub>', markup)
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
    compact_english=all(q['area']=='english' for q in questions) and len(questions)<=55
    for q in questions:
        flows=[]
        if q['area']!=previous:
            flows=[Spacer(1,5),para(AREAS[q['area']],9,True),Spacer(1,5)]
            previous=q['area']
        row=BubbleRow(letters_for(q),numbers[q['id']],marked=q['correct'] if teacher else None,
                      book=None if teacher else book,answer=q['correct'])
        if compact_english:
            row.height=21
        flows.append(row)
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
    for q in questions:
        if q['area']=='english' and q['part']==1:
            for page in doc:
                matches=page.search_for(q['stem'])
                if matches:
                    rect=matches[-1]
                    page.insert_text((rect.x0,rect.y1+12),'Respuesta: '+q['correct'],fontname='hebo',fontsize=8,color=(.09,.15,.23))
                    break
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
                   and q.get('options_layout','vertical')=='vertical'
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
            flows += [picture(q['image'], min(width-18,q.get('image_width',300 if full else width-18)),
                              q.get('image_height',110 if full else 190),trim=True), Spacer(1, 5)]
        flows += [para(stem if introduction or q.get('image') else f'{number}.  '+stem), Spacer(1, 5)]
        if matching:
            flows += [para('Respuesta: A   B   C   D   E   F   G', 9)]
        else:
            grid=q.get('options_layout','vertical')=='grid2'
            option_width=(width-18)/2-12 if grid else width-18
            options=[]
            for letter, option in zip('ABCD', q['options']):
                option_flows=[para(letter+'.  '+option.get('text', ''))]
                if option.get('image'):
                    option_flows += [Spacer(1,4),picture(option['image'], option_width, 120 if grid else 100)]
                options.append(TrackedOption(option_flows,self,letter==q['correct']))
            if grid:
                rows=[options[i:i+2]+([''] if len(options[i:i+2])==1 else []) for i in range(0,len(options),2)]
                table=Table(rows,colWidths=[(width-18)/2]*2)
                table.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),
                    ('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),
                    ('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]))
                flows.append(table)
            else:
                for option in options:
                    flows += [option,Spacer(1,2)]
        return flows, full, False

    def question_height(self, q, number):
        flows, full, _ = self.question_flows(q, number)
        return measure(flows, (WIDTH if full else CW)-18)+(12 if full else 18)

    def column_group(self,items,numbers):
        """Buffer one consecutive run; close both columns on one common rule."""
        prepared=[(q,self.question_flows(q,numbers[q['id']])[0]) for q in items]
        heights=[measure(flows,CW-18)+12 for _,flows in prepared]
        mapping={};offset=0
        while offset<len(prepared):
            top=self.flush()
            plan=column_chunk(heights[offset:],top-BOTTOM)
            if plan is None:
                self.newpage()
                top=self.flush()
                plan=column_chunk(heights[offset:],top-BOTTOM)
            if plan is None:
                raise ValueError('La pregunta '+str(numbers[items[offset]['id']])+
                    ' no cabe completa en una columna. Usa ancho completo o un contexto; no se reducirá la letra.')
            count,split,left,right=plan
            for col,start,end in ((0,offset,offset+split),(1,offset+split,offset+count)):
                y=top
                for index in range(start,end):
                    question,flows=prepared[index]
                    draw(flows,self.c,M+col*(CW+GAP)+9,y-6,CW-18)
                    mapping[question['id']]=self.page
                    y-=heights[index]+10
            bottom=top-max(left,right)
            self.c.setStrokeColor(GRAY);self.c.setLineWidth(.45)
            if count>split:
                self.c.line(W/2,top,W/2,bottom)
            self.c.line(M,bottom,W-M,bottom)
            self.reset(bottom-10)
            offset+=count
            if offset<len(prepared):
                self.newpage()
        return mapping

    def shared_context(self, flows, first_question, number):
        reserve = self.question_height(first_question, number)+14
        context_height = measure(flows, WIDTH-18)+18
        available = H-83-BOTTOM
        if context_height > available:
            # Split printable paragraphs, leaving the stored context and its
            # links intact. Images and other indivisible resources still fail
            # explicitly if they exceed a page.
            remaining = list(flows)
            while measure(remaining, WIDTH-18)+18 > available:
                chunk = []
                budget = available-18
                advanced = False
                while remaining:
                    flow = remaining[0]
                    height = flow.wrap(WIDTH-18, H)[1]
                    if height <= budget:
                        chunk.append(remaining.pop(0))
                        budget -= height
                        if not getattr(flow, '_context_continuation', False) and not isinstance(flow, Spacer):
                            advanced = True
                        continue
                    parts = flow.split(WIDTH-18, budget) if isinstance(flow, Paragraph) else []
                    if parts:
                        chunk.append(parts[0])
                        remaining[:1] = parts[1:]
                        advanced = True
                    break
                if not advanced:
                    raise ValueError('Un recurso indivisible del contexto excede una página: '+first_question['id'])
                self.full(chunk, True)
                self.newpage()
                heading = para('CONTINUACIÓN DE LA LECTURA', 9, True)
                heading._context_continuation = True
                remaining.insert(0, heading)
                remaining.insert(1, Spacer(1, 7))
            return self.shared_context(remaining, first_question, number)
        if context_height+reserve > available:
            # A long reading may occupy its own page; never shrink or omit it.
            self.full(flows, True)
            self.newpage()
            return
        self.full(flows, True, reserve=reserve)

    def side_context(self, flows, first_question, number):
        """Start a shared reading on the left and its questions on the right."""
        height = measure(flows, CW-18)+18
        reserve = self.question_height(first_question, number)
        if height > H-83-BOTTOM:
            raise ValueError('La lectura compartida no cabe en una columna. Divídela en dos contextos o usa ancho completo.')
        if reserve > H-83-BOTTOM:
            raise ValueError('La primera pregunta del contexto no cabe en una columna.')
        top = self.flush()
        if top-max(height,reserve) < BOTTOM:
            self.newpage()
            top = self.flush()
        draw(flows, self.c, M+9, top-9, CW-18)
        self.reset(top)
        self.ys[0] = top-height
        self.used[0] = True
        self.col = 1

    def question(self, q, number, matching=False):
        if q.get('page_break_before') and (any(self.used) or min(self.ys)<H-65):
            self.newpage()
        flows, full, compact = self.question_flows(q, number, matching)
        width = WIDTH if full else CW
        height = measure(flows, width-18)+18
        if height > H-83-BOTTOM:
            raise ValueError(f'La pregunta {number} no cabe sin recortar. Elige ancho completo o divide su contexto.')
        if full:
            self.full(flows, separator=not compact)
            return
        if q.get('column_break_before'):
            if self.col==1 and self.used[1]:
                self.newpage()
            self.col=1
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
        flows += [Spacer(1,22)]
    return flows


def matching_example(ctx):
    """Read the saved worked example; never infer it from a scored answer."""
    value=ctx.get('example','').strip()
    match=re.fullmatch(r'0\.\s*(.*?)\s*(?:Respuesta:\s*|→\s*)([A-H])\.\s*(.+)',value,re.S)
    if not match:
        return None
    return match[1].strip(),match[2],match[3].strip().rstrip('.')


class MatchingExample(Flowable):
    """The single worked row 0, drawn sharply without importing a marked scan."""
    def __init__(self,prompt,answer):
        super().__init__()
        self.prompt,self.answer=prompt,answer

    def wrap(self,width,height):
        self.width=width
        self.line=para('0.   '+self.prompt,10)
        self.line_height=self.line.wrap(width,H)[1]
        self.height=22+self.line_height+49
        return width,self.height

    def draw(self):
        c=self.canv
        draw([para('Ejemplo:',10,True)],c,0,self.height,self.width)
        draw([self.line],c,0,self.height-22,self.width)
        box_width=min(316,self.width)
        x=self.width-box_width
        c.saveState()
        c.setStrokeColor(INK);c.setLineWidth(.65)
        c.setFillColor(colors.HexColor('#E9E9E9'))
        c.roundRect(x,3,box_width,35,4,stroke=1,fill=1)
        c.setFillColor(INK);c.setFont('Helvetica-Bold',10)
        c.drawString(x+8,16,'Respuesta:')
        c.setFillColor(colors.white)
        c.roundRect(x+73,6,box_width-77,29,4,stroke=1,fill=1)
        c.setFillColor(INK);c.drawString(x+81,16,'0.')
        for i,letter in enumerate('ABCDEFGH'):
            cx=x+110+i*25;cy=20
            c.setFillColor(colors.HexColor('#BDBDBD') if letter==self.answer else colors.white)
            c.circle(cx,cy,8,stroke=1,fill=1)
            c.setFillColor(INK);c.setFont('Helvetica-Bold' if letter==self.answer else 'Helvetica',9)
            c.drawCentredString(cx,cy-3,letter)
        c.restoreState()


class MatchingColumns(Flowable):
    """Descriptions left, one shared word bank right; answers only on the sheet."""
    def __init__(self,book,members,numbers,ctx):
        super().__init__()
        self.book,self.members,self.numbers,self.ctx=book,members,numbers,ctx

    def wrap(self,width,height):
        self.width=width
        self.split=width*.64
        self.left_width=self.split-24
        self.right_width=width-self.split-24
        self.descriptions=[]
        for item in self.members:
            # Keep images and introductions, but no inline answer row.
            flows=matching_descriptions(self.book,[item],self.numbers)[2:]
            flows=flows[:-1]  # spacing is measured between descriptions below
            self.descriptions.append(flows)
        heights=[measure(flows,self.left_width) for flows in self.descriptions]
        tallest=max(heights,default=0)
        self.height=max(350,58+tallest+(len(heights)-1)*max(52,tallest+12))
        self.words=[(letter,word) for letter,word in zip('ABCDEFG',self.ctx['words'])]
        example=matching_example(self.ctx)
        if example and example[1]=='H':
            self.words.append(('H',example[2]))
        self.tallest=tallest
        return width,self.height

    def draw(self):
        c=self.canv;c.saveState()
        c.setStrokeColor(GRAY);c.setLineWidth(.5)
        c.line(0,self.height-29,self.width,self.height-29)
        c.line(self.split,self.height, self.split,0)
        c.setFillColor(INK);c.setFont('Helvetica-Bold',11)
        c.drawCentredString(self.split/2,self.height-16,'Descripciones')
        c.drawCentredString(self.split+(self.width-self.split)/2,self.height-16,'Palabras')
        step=(self.height-48-self.tallest)/max(1,len(self.descriptions)-1)
        for i,flows in enumerate(self.descriptions):
            draw(flows,c,10,self.height-42-i*step,self.left_width)
        word_step=(self.height-62)/max(1,len(self.words)-1)
        correct={item['correct'] for item in self.members}
        for i,(letter,word) in enumerate(self.words):
            row=TrackedOption([para(letter+'.   '+word,10,letter=='H')],self.book,letter in correct)
            _,row_height=row.wrap(self.right_width,H)
            row.drawOn(c,self.split+14,self.height-42-i*word_step-row_height)
        c.restoreState()


def matching_flows(book,ctx,members,numbers):
    """Part 1 uses its own book layout, not the generic shared-context box."""
    center=lambda text,size,bold=False:Paragraph(escape(text),ParagraphStyle(
        'matching-center',fontName='Helvetica-Bold' if bold else 'Helvetica',
        fontSize=size,leading=size*1.33,textColor=INK,alignment=1))
    first,last=numbers[members[0]['id']],numbers[members[-1]['id']]
    flows=[center('PARTE 1',11,True),Spacer(1,9),
           center(range_heading(ctx.get('range_heading'),first,last),9,True),Spacer(1,9)]
    if ctx.get('instructions'):
        flows += [para(ctx['instructions']),Spacer(1,14)]
    if ctx.get('title'):
        flows += [center(ctx['title'],16,True),Spacer(1,16)]
    if ctx.get('text'):
        flows += [para(ctx['text']),Spacer(1,8)]
    example=matching_example(ctx)
    if example:
        flows += [MatchingExample(example[0],example[1]),Spacer(1,18)]
    elif ctx.get('example'):
        flows += [para('Ejemplo resuelto: '+ctx['example'],9),Spacer(1,18)]
    flows.append(MatchingColumns(book,members,numbers,ctx))
    if ctx.get('source'):
        flows += [Spacer(1,8),para('Fuente: '+ctx['source'],8)]
    return flows


class NoticeCard(Flowable):
    """Printable text-only notice: preserve its words without scan noise."""
    def __init__(self,text,dark=False):
        super().__init__()
        self.text,self.dark=text,dark

    def wrap(self,width,height):
        self.width=min(width,236)
        self.content=Paragraph(escape(self.text).replace('\n','<br/>'),ParagraphStyle(
            'notice',fontName='Helvetica-Bold' if self.dark else 'Times-Bold',
            fontSize=13,leading=15.6,alignment=1,
            textColor=colors.white if self.dark else INK))
        self.content_height=self.content.wrap(self.width-24,H)[1]
        self.height=max(56,self.content_height+22)
        return self.width,self.height

    def draw(self):
        c=self.canv;c.saveState()
        c.setLineWidth(.8);c.setStrokeColor(INK)
        c.setFillColor(INK if self.dark else colors.white)
        c.roundRect(0,0,self.width,self.height,8,stroke=1,fill=1)
        c.setStrokeColor(colors.white if self.dark else GRAY)
        c.roundRect(3,3,self.width-6,self.height-6,6,stroke=1,fill=0)
        # Each original notice has its own visual language, kept in grayscale.
        if '3D glasses' in self.text:
            c.setLineWidth(2);c.roundRect(6,6,self.width-12,self.height-12,4,fill=0)
            for x in (9,self.width-9):
                for y in (9,self.height-9):
                    c.setFillColor(colors.white);c.circle(x,y,1.3,fill=1,stroke=0)
        elif 'Small pets' in self.text:
            c.setStrokeColor(INK);c.setLineWidth(1.4)
            c.roundRect(6,6,self.width-12,self.height-12,10,fill=0)
            for x in (8,self.width-8):
                for y in (8,self.height-8):
                    c.circle(x,y,2.6,fill=0)
        elif 'fruit and green' in self.text:
            c.setFillColor(colors.HexColor('#EEEEEE'))
            c.roundRect(5,5,self.width-10,self.height-10,5,fill=1,stroke=0)
            c.setFillColor(INK)
            for x in (7,self.width-7):
                c.roundRect(x-3,self.height-8,6,6,1,fill=1,stroke=0)
                c.roundRect(x-3,2,6,5,1,fill=1,stroke=0)
        elif '40x50' in self.text:
            c.setStrokeColor(INK);c.setLineWidth(.6)
            c.roundRect(6,6,self.width-12,self.height-12,4,fill=0)
            for x in range(13,int(self.width)-10,12):
                c.arc(x,self.height-8,x+8,self.height-2,0,180)
                c.arc(x,2,x+8,8,180,180)
        elif 'run in the halls' in self.text:
            c.setFillColor(colors.HexColor('#DDDDDD'))
            c.roundRect(3,3,self.width-6,7,2,fill=1,stroke=0)
            c.roundRect(3,self.height-10,self.width-6,7,2,fill=1,stroke=0)
        self.content.drawOn(c,12,(self.height-self.content_height)/2)
        c.restoreState()


class NoticeRow(Flowable):
    """One notice left and its A-C choices right, without answer bubbles."""
    def __init__(self,book,item,number,track=True,plain=False):
        super().__init__()
        self.book,self.item,self.number,self.track=book,item,number,track
        self.plain=plain

    def wrap(self,width,height):
        self.width=width;self.split=width*.61
        self.card=(picture(self.item['image'],self.split-48,90,trim=True)
                   if self.item.get('image') else para(self.item['stem']) if self.plain
                   else NoticeCard(self.item['stem'],self.item.get('notice_style')=='dark'))
        self.card_width,self.card_height=self.card.wrap(self.split-48,H)
        self.options=[]
        for letter,option in zip('ABC',self.item['options']):
            flows=[para(letter+'.   '+option.get('text',''))]
            if option.get('image'):
                flows += [picture(option['image'],width-self.split-12,80)]
            row=TrackedOption(flows,self.book,self.track and letter==self.item['correct'])
            row.wrap(width-self.split-12,H)
            self.options.append(row)
        self.options_height=sum(r.height+4 for r in self.options)-4
        self.height=max(78 if self.plain else 87,self.card_height+15,self.options_height+15)
        return width,self.height

    def draw(self):
        c=self.canv;c.saveState();c.setFillColor(INK);c.setFont('Helvetica-Bold',10)
        c.drawString(0,self.height-16,str(self.number)+'.')
        self.card.drawOn(c,26,self.height-8-self.card_height)
        top=self.height-10
        for row in self.options:
            row.drawOn(c,self.split,top-row.height)
            top-=row.height+4
        c.restoreState()


class NoticeExample(Flowable):
    def __init__(self,ctx):
        super().__init__()
        self.ctx=ctx

    def wrap(self,width,height):
        self.width=width
        item={'stem':self.ctx['example_notice'],'options':[{'text':t} for t in self.ctx['example_options']],
              'correct':self.ctx['example_answer']}
        self.row=NoticeRow(None,item,0,track=False)
        self.row.wrap(width,H)
        self.height=self.row.height+43
        return width,self.height

    def draw(self):
        c=self.canv
        draw([para('Ejemplo:',10,True)],c,0,self.height,self.width)
        self.row.drawOn(c,0,25)
        c.saveState()
        x=self.width-214
        c.setStrokeColor(INK);c.setLineWidth(.7);c.setFillColor(colors.HexColor('#E9E9E9'))
        c.roundRect(x,0,214,30,3,stroke=1,fill=1)
        c.setFillColor(INK);c.setFont('Helvetica-Bold',10);c.drawString(x+7,11,'Respuesta:')
        c.setFillColor(colors.white);c.roundRect(x+72,3,138,24,3,stroke=1,fill=1)
        c.setFillColor(INK);c.drawString(x+80,11,'0.')
        for i,letter in enumerate('ABC'):
            cx=x+108+i*33
            c.setFillColor(colors.HexColor('#BDBDBD') if letter==self.ctx['example_answer'] else colors.white)
            c.circle(cx,15,8,stroke=1,fill=1)
            c.setFillColor(INK);c.setFont('Helvetica-Bold' if letter==self.ctx['example_answer'] else 'Helvetica',9)
            c.drawCentredString(cx,12,letter)
        c.restoreState()


def notice_flows(book,ctx,members,numbers):
    first,last=numbers[members[0]['id']],numbers[members[-1]['id']]
    centered=lambda t:Paragraph(escape(t),ParagraphStyle('notice-heading',fontName='Helvetica-Bold',
                                                       fontSize=10,leading=13.3,textColor=INK,alignment=1))
    flows=[centered('PARTE 2'),Spacer(1,9),
           centered(range_heading(ctx.get('range_heading'),first,last)),Spacer(1,9)]
    if ctx.get('instructions'):
        flows += [para(range_heading(ctx['instructions'],first,last)),Spacer(1,12)]
    if ctx.get('example_notice') and len(ctx.get('example_options',[]))==3 and ctx.get('example_answer') in 'ABC':
        flows += [NoticeExample(ctx),Spacer(1,18)]
    for item in members:
        flows.append(NoticeRow(book,item,numbers[item['id']]))
    return flows


def dialogue_flows(book,ctx,members,numbers):
    first,last=numbers[members[0]['id']],numbers[members[-1]['id']]
    centered=lambda t:Paragraph(escape(t),ParagraphStyle('dialogue-heading',fontName='Helvetica-Bold',
                                                       fontSize=10,leading=13.3,textColor=INK,alignment=1))
    flows=[centered('PARTE 3'),Spacer(1,9),
           centered(range_heading(ctx.get('range_heading'),first,last)),Spacer(1,9)]
    if ctx.get('instructions'):
        flows += [para(range_heading(ctx['instructions'],first,last)),Spacer(1,12)]
    if ctx.get('image'):
        flows += [para('Ejemplo:',10,True),Spacer(1,6),picture(ctx['image'],WIDTH-30,170,trim=True),Spacer(1,22)]
    elif ctx.get('example'):
        flows += [para('Ejemplo: '+ctx['example']),Spacer(1,22)]
    for item in members:
        flows.append(NoticeRow(book,item,numbers[item['id']],plain=True))
    return flows


class ClozeExampleAnswer(Flowable):
    def __init__(self,letters='ABC'):
        super().__init__();self.letters=letters
    def wrap(self,width,height):
        self.width=width
        return width,34
    def draw(self):
        c=self.canv
        box_width=181+25*(len(self.letters)-3)
        x=self.width-box_width
        c.saveState()
        c.setStrokeColor(INK)
        c.setFillColor(colors.HexColor('#EEEEEE'))
        c.roundRect(x,2,box_width,29,4,fill=1)
        c.setFillColor(INK);c.setFont('Helvetica-Bold',10)
        c.drawString(x+6,12,'Respuesta:');c.drawString(x+72,12,'0.')
        for i,letter in enumerate(self.letters):
            cx=x+111+i*25
            c.setFillColor(GRAY if i==0 else colors.white)
            c.circle(cx,16,10,fill=1)
            c.setFillColor(INK);c.drawCentredString(cx,12,letter)
        c.restoreState()


class ReadingPanel(Flowable):
    def __init__(self,title,text):
        super().__init__()
        self.flows=([Paragraph(escape(title),ParagraphStyle('reading-title',fontName='Helvetica-Bold',fontSize=17,leading=22,alignment=1)),Spacer(1,8)] if title else [])+[para(text,9.5)]
        if title:
            self.flows[-1].style.leading=11.2
    def wrap(self,width,height):
        self.width=width;self.height=measure(self.flows,width-28)+26
        return width,self.height
    def draw(self):
        self.canv.saveState();self.canv.setStrokeColor(INK);self.canv.setLineWidth(1.2)
        self.canv.roundRect(0,0,self.width,self.height,16,fill=0)
        draw(self.flows,self.canv,14,self.height-12,self.width-28)
        self.canv.restoreState()


def reading_flows(book,ctx,members,numbers):
    first,last=numbers[members[0]['id']],numbers[members[-1]['id']]
    centered=lambda text:Paragraph(escape(text),ParagraphStyle('reading-heading',fontName='Helvetica-Bold',fontSize=10,leading=13,alignment=1,textColor=INK))
    flows=[centered('PARTE 5'),Spacer(1,4),centered(range_heading(ctx['range_heading'],first,last)),Spacer(1,4),para(range_heading(ctx['instructions'],first,last)),Spacer(1,6),ReadingPanel(ctx['title'],ctx['text']),Spacer(1,4),para('Ejemplo:',9,True)]
    def row(number,stem,options,item=None):
        right=[]
        for letter,option in zip('ABC',options):
            content=[para(letter+'.    '+option,9)]
            right.append(TrackedOption(content,book,item['correct']==letter) if item else content[0])
        table=Table([[para(str(number)+'.',9,True),para(stem,9),right]],colWidths=[28,(WIDTH-18)*.55-28,(WIDTH-18)*.45])
        table.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),0),('TOPPADDING',(0,0),(-1,-1),1),('BOTTOMPADDING',(0,0),(-1,-1),1)]))
        return table
    flows += [row(0,ctx['example_prompt'],ctx['example_options']),ClozeExampleAnswer(),Spacer(1,4)]
    for item in members:
        flows.append(row(numbers[item['id']],item['stem'],[o['text'] for o in item['options']],item))
        flows.append(Spacer(1,3))
    return flows


def inference_flows(book,ctx,members,numbers):
    first,last=numbers[members[0]['id']],numbers[members[-1]['id']]
    centered=lambda text:Paragraph(escape(text),ParagraphStyle('inference-heading',fontName='Helvetica-Bold',fontSize=10,leading=13,alignment=1,textColor=INK))
    flows=[centered('PARTE 6'),Spacer(1,5),centered(range_heading(ctx['range_heading'],first,last)),Spacer(1,6),para(range_heading(ctx['instructions'],first,last)),Spacer(1,5),ReadingPanel('',ctx['text']),Spacer(1,5)]
    for item in members:
        flows += [para(str(numbers[item['id']])+'. '+item['stem'],9,True),Spacer(1,3)]
        if item.get('answer_cards'):
            cells=[]
            for letter,option in zip('ABCD',item['options']):
                card=Table([[para(option['text'],9,True)]],colWidths=[(WIDTH-18)/2-35],cornerRadii=[7]*4)
                card.setStyle(TableStyle([('BOX',(0,0),(-1,-1),.8,INK),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]))
                cells.append([para(letter+'.',9,True),TrackedOption([card],book,item['correct']==letter)])
            rows=[cells[0]+cells[1],cells[2]+cells[3]]
            table=Table(rows,colWidths=[22,(WIDTH-18)/2-22]*2)
            table.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),0),('TOPPADDING',(0,0),(-1,-1),3),('BOTTOMPADDING',(0,0),(-1,-1),5)]))
            flows.append(table)
        else:
            for letter,option in zip('ABCD',item['options']):
                flows.append(TrackedOption([para(letter+'.    '+option['text'],9)],book,item['correct']==letter))
        flows.append(Spacer(1,3))
    return flows


class IllustratedClozePanel(Flowable):
    def __init__(self,ctx,text):
        super().__init__()
        portrait=ctx.get('image_side')=='right'
        self.title=Paragraph(escape(ctx['title']),ParagraphStyle('illustrated-title',fontName='Times-BoldItalic' if portrait else 'Helvetica-Bold',fontSize=23 if portrait else 18,leading=27 if portrait else 24,alignment=1))
        if portrait:
            body=Paragraph(escape(text).replace('\n','<br/>').replace('Things Fall Apart','<i>Things Fall Apart</i>'),ParagraphStyle('portrait-reading',fontName='Times-Roman',fontSize=11,leading=12.8,textColor=INK))
        else:
            body=para(text,9.5,True)
        self.content=ParagraphAndImage(body,picture(ctx['image'],115 if portrait else 177,135 if portrait else 96),xpad=8,ypad=2,side='right' if portrait else 'left')
    def wrap(self,width,height):
        self.width=width
        self.title_height=self.title.wrap(width-28,height)[1]
        self.content_height=self.content.wrap(width-28,height)[1]
        self.height=self.title_height+self.content_height+34
        return width,self.height
    def draw(self):
        c=self.canv;c.saveState();c.setStrokeColor(INK);c.setLineWidth(1.2)
        c.roundRect(0,0,self.width,self.height,15,fill=0)
        self.title.drawOn(c,14,self.height-10-self.title_height)
        self.content.drawOn(c,14,12)
        c.restoreState()


def illustrated_cloze_flows(book,ctx,members,numbers):
    width=WIDTH-18
    first,last=numbers[members[0]['id']],numbers[members[-1]['id']]
    centered=lambda text:Paragraph(escape(text),ParagraphStyle('illustrated-heading',fontName='Helvetica-Bold',fontSize=10,leading=13,alignment=1,textColor=INK))
    text=ctx['text']
    for item in members:text=text.replace('{{'+item['slot']+'}}','('+str(numbers[item['id']])+')_____')
    flows=[centered(('PARTE 7.B' if ctx.get('image_side')=='right' else 'PARTE 7.A')),Spacer(1,6),centered(range_heading(ctx['range_heading'],first,last)),Spacer(1,7),para(range_heading(ctx['instructions'],first,last)),Spacer(1,10),IllustratedClozePanel(ctx,text),Spacer(1,9),para('Ejemplo:',9,True)]
    def row(number,options,item=None):
        cells=[para(str(number)+'.',9,True)]
        for letter,option in zip('ABCD',options):
            content=Paragraph('<b>'+letter+'.</b>    '+escape(option),ParagraphStyle('illustrated-choice',fontName='Helvetica',fontSize=9,leading=12,textColor=INK))
            cells.append(TrackedOption([content],book,item['correct']==letter) if item else content)
        table=Table([cells],colWidths=[29]+[(width-29)/4]*4)
        table.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),0),('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4)]))
        return table
    flows += [row(0,ctx['example_options']),ClozeExampleAnswer('ABCD'),Spacer(1,7),HRFlowable(width='100%',thickness=.5,color=GRAY),Spacer(1,7)]
    for item in members:flows.append(row(numbers[item['id']],[o['text'] for o in item['options']],item))
    return flows


def cloze_flows(book,ctx,members,numbers):
    first,last=numbers[members[0]['id']],numbers[members[-1]['id']]
    centered=lambda text: Paragraph(escape(text),ParagraphStyle('cloze-heading',fontName='Helvetica-Bold',fontSize=10,leading=14,alignment=1,textColor=INK))
    flows=[centered('PARTE 4'),Spacer(1,9),centered(range_heading(ctx['range_heading'],first,last)),Spacer(1,10),para(range_heading(ctx['instructions'],first,last)),Spacer(1,14)]
    text=ctx['text']
    for item in members:
        text=text.replace('{{'+item['slot']+'}}','('+str(numbers[item['id']])+')_____')
    panel=Table([[Paragraph(escape(ctx['title']),ParagraphStyle('cloze-title',fontName='Times-Bold',fontSize=24,leading=29,alignment=1))],[para(text,11)]],colWidths=[WIDTH-24],cornerRadii=[14]*4)
    panel.setStyle(TableStyle([('BOX',(0,0),(-1,-1),1.2,INK),('LEFTPADDING',(0,0),(-1,-1),14),('RIGHTPADDING',(0,0),(-1,-1),14),('TOPPADDING',(0,0),(-1,-1),12),('BOTTOMPADDING',(0,0),(-1,-1),9)]))
    flows += [panel,Spacer(1,12),para('Ejemplo:',10,True),Spacer(1,7)]
    def row(number,options,item=None):
        cells=[para(str(number)+'.',10,True)]
        for index,option in enumerate(options):
            label=chr(65+index)
            cell=para(label+'.    '+option,10)
            cells.append(TrackedOption([cell],book,item['correct']==label) if item else cell)
        table=Table([cells],colWidths=[30]+[(WIDTH-30)/3]*3)
        table.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),5),('TOPPADDING',(0,0),(-1,-1),4)]))
        return table
    flows += [row(0,ctx['example_options']),ClozeExampleAnswer(),Spacer(1,10)]
    for item in members:
        flows += [row(numbers[item['id']],[option['text'] for option in item['options']],item),Spacer(1,4)]
    return flows


def context_flows(ctx, members, numbers, show_words=True, column=False):
    flows = []
    first, last = numbers[members[0]['id']], numbers[members[-1]['id']]
    if ctx.get('part'):
        label='PARTE '+str(ctx['part'])
        heading=(Paragraph(escape(label),ParagraphStyle('english-part',fontName='Helvetica-Bold',
                 fontSize=10,leading=13.3,textColor=INK,alignment=1))
                 if ctx.get('area')=='english' else para(label,10,True))
        flows += [heading, Spacer(1, 5)]
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
        flows += [picture(ctx['image'], (CW if column else WIDTH)-18, 220), Spacer(1, 8)]
    if ctx.get('table'):
        rows = [line.split(';') for line in ctx['table'].strip().splitlines()]
        ncols = max(map(len, rows))
        table = Table([[para(cell, 9) for cell in row]+['']*(ncols-len(row)) for row in rows], colWidths=[((CW if column else WIDTH)-18)/ncols]*ncols)
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
        if not q.get('stem','').strip() and not q.get('introduction','').strip():
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
    if all(q['area']=='english' for q in selected):
        cfg.update(session='Práctica de inglés · Segunda sesión',time='Por definir',areas=[{'name':AREAS['english'],'count':len(selected)}])
    (out/'cover.json').write_text(json.dumps(cfg,ensure_ascii=False),encoding='utf-8')
    subprocess.run([sys.executable,str(ROOT/'tool/preview_editorial_cover.py'),'--config',str(out/'cover.json'),'--output',str(out/'cover.pdf')],check=True,capture_output=True)
    book = Interior(out/'interior.pdf', project)
    last_area, seen, last_part = None, set(), None
    page_map={}
    pending_columns=[]
    side_context_id=None
    def flush_columns():
        if pending_columns:
            page_map.update(book.column_group(pending_columns,numbers))
            pending_columns.clear()
    for q in selected:
        if q['area'] != last_area:
            flush_columns()
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
        use_band=(project.get('column_flow','sequential')=='balanced' and not cid
                  and q['area']!='english' and q['layout'] in ('columns','boxed')
                  and not q.get('page_break_before') and not q.get('column_break_before'))
        if not use_band:
            flush_columns()
        if cid and cid not in seen:
            members = [item for item in selected if item.get('context')==cid]
            matching=q['area']=='english' and q['part']==1
            if matching:
                flows=matching_flows(book,ctxs[cid],members,numbers)
                book.full(flows,False)
                page_map.update({item['id']:book.page for item in members})
            elif q['area']=='english' and q['part']==2 and ctxs[cid].get('notice_layout')=='paired':
                book.full(notice_flows(book,ctxs[cid],members,numbers),False)
                page_map.update({item['id']:book.page for item in members})
            elif q['area']=='english' and q['part']==3 and ctxs[cid].get('dialogue_layout')=='paired':
                book.full(dialogue_flows(book,ctxs[cid],members,numbers),False)
                page_map.update({item['id']:book.page for item in members})
            elif q['area']=='english' and q['part']==4 and ctxs[cid].get('cloze_layout')=='rows':
                book.full(cloze_flows(book,ctxs[cid],members,numbers),False)
                page_map.update({item['id']:book.page for item in members})
            elif q['area']=='english' and q['part']==5 and ctxs[cid].get('reading_layout')=='paired':
                book.full(reading_flows(book,ctxs[cid],members,numbers),False)
                page_map.update({item['id']:book.page for item in members})
            elif q['area']=='english' and q['part']==6 and ctxs[cid].get('inference_layout')=='stacked':
                book.full(inference_flows(book,ctxs[cid],members,numbers),False)
                page_map.update({item['id']:book.page for item in members})
            elif q['area']=='english' and q['part']==7 and ctxs[cid].get('illustrated_cloze_layout')=='rows':
                book.full(illustrated_cloze_flows(book,ctxs[cid],members,numbers),False)
                page_map.update({item['id']:book.page for item in members})
            else:
                side = ctxs[cid].get('layout')=='side_by_side'
                context = context_flows(ctxs[cid],members,numbers,column=side)
                if side:
                    book.side_context(context,q,numbers[q['id']])
                    side_context_id=cid
                else:
                    book.shared_context(context,q,numbers[q['id']])
            seen.add(cid)
            last_part = q.get('part')
        elif q['area']=='english' and q['part']!=last_part:
            book.full([para('PARTE '+str(q['part']),11,True)],reserve=105)
            last_part=q['part']
        group_rendered=(q['area']=='english' and (q['part']==1 or
                        (q['part']==2 and cid and ctxs[cid].get('notice_layout')=='paired') or
                        (q['part']==3 and cid and ctxs[cid].get('dialogue_layout')=='paired') or
                        (q['part']==4 and cid and ctxs[cid].get('cloze_layout')=='rows') or
                        (q['part']==5 and cid and ctxs[cid].get('reading_layout')=='paired') or
                        (q['part']==6 and cid and ctxs[cid].get('inference_layout')=='stacked') or
                        (q['part']==7 and cid and ctxs[cid].get('illustrated_cloze_layout')=='rows')))
        if not group_rendered:
            if use_band:
                pending_columns.append(q)
            else:
                book.question(q,numbers[q['id']])
                page_map[q['id']]=book.page
        if side_context_id and cid==side_context_id and q is members[-1]:
            bottom=book.flush()
            book.reset(bottom-12)
            side_context_id=None
    flush_columns()
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
