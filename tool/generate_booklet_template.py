"""Generate an original editorial sample, not an official exam or app export.

Run: uv run --with reportlab --with pymupdf python tool/generate_booklet_template.py
The JSON is editable separately. Layout fails rather than silently clipping text.
"""
import argparse
import json
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.platypus import Paragraph, Table, TableStyle
from assessment_metadata import validate_assessments, append_teacher_pages

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'output' / 'pdf'
W, H = A4
M = 42
INK = colors.HexColor('#171717')
RULE = colors.HexColor('#454545')
GRAY = colors.HexColor('#EEEEEE')
GRAY_LIGHT = colors.HexColor('#F7F7F7')
# Se conservan estos nombres para no romper el resto del generador; la
# plantilla editorial actual usa únicamente escala de grises.
BLUE = INK
BLUE_LIGHT = GRAY_LIGHT


class Book:
    def __init__(self, path, version):
        self.c = canvas.Canvas(str(path), pagesize=A4)
        self.c.setTitle('SaberPlus | ' + path.stem)
        self.c.setAuthor('SaberPlus')
        self.page = 0
        self.version = version

    def start(self, title, subtitle='MUESTRA EDITORIAL | NO OFICIAL'):
        if self.page:
            self.c.showPage()
        self.page += 1
        c = self.c
        c.setFillColor(INK)
        c.setFont('Helvetica-Bold', 13)
        c.drawString(M, H - 35, 'SaberPlus')
        c.setFont('Helvetica', 8)
        c.drawRightString(W - M, H - 35, self.version)
        c.setStrokeColor(INK)
        c.setLineWidth(.8)
        c.line(M, H - 46, W - M, H - 46)
        c.setFillColor(INK)
        c.setFont('Helvetica-Bold', 16)
        c.drawString(M, H - 73, title)
        c.setFont('Helvetica', 7.5)
        c.drawString(M, H - 89, subtitle)
        c.setStrokeColor(RULE)
        c.setLineWidth(.5)
        c.line(M, 39, W - M, 39)
        c.setFont('Helvetica', 7)
        c.drawString(M, 25, 'Material de práctica independiente | SaberPlus')
        c.drawRightString(W - M, 25, str(self.page))
        return H - 112

    def p(self, text, y, x=M, width=None, size=10.5, bold=False, gap=10):
        width = width or W - 2 * M
        style = ParagraphStyle('body', fontName='Helvetica-Bold' if bold else 'Helvetica',
                               fontSize=size, leading=size * 1.35, textColor=INK)
        p = Paragraph(text, style)
        _, h = p.wrap(width, H)
        if y - h < 52:
            raise ValueError(f'Page {self.page}: content exceeds printable area: {text[:65]}')
        p.drawOn(self.c, x, y - h)
        return y - h - gap

    def banner(self, text, y):
        self.c.setFillColor(GRAY_LIGHT)
        self.c.rect(M, y - 27, W - 2 * M, 27, fill=1, stroke=0)
        self.c.setStrokeColor(INK)
        self.c.setLineWidth(.65)
        self.c.line(M, y, W - M, y)
        self.c.line(M, y - 27, W - M, y - 27)
        return self.p(text, y - 7, x=M + 8, width=W - 2 * M - 16, size=9, bold=True, gap=15)

    def cover_cards(self, items, y):
        gap = 8
        width = (W - 2 * M - gap * (len(items) - 1)) / len(items)
        height = 48
        for index, (label, value) in enumerate(items):
            x = M + index * (width + gap)
            self.c.setFillColor(GRAY_LIGHT)
            self.c.setStrokeColor(RULE)
            self.c.setLineWidth(.55)
            self.c.rect(x, y - height, width, height, fill=1, stroke=1)
            self.c.setFillColor(GRAY)
            self.c.rect(x, y - 18, width, 18, fill=1, stroke=0)
            self.c.setFillColor(INK)
            self.c.setFont('Helvetica-Bold', 7)
            self.c.drawString(x + 8, y - 13, label.upper())
            self.c.setFillColor(INK)
            self.c.setFont('Helvetica-Bold', 12)
            self.c.drawString(x + 8, y - 38, value)
        return y - height - 18

    def image(self, image_value, y, x=M, width=None, max_height=150, gap=8):
        """Draw an optional question image without stretching or clipping it."""
        width = width or W - 2 * M
        if isinstance(image_value, dict):
            source = image_value.get('path')
            caption = image_value.get('caption', '')
            max_height = image_value.get('max_height', max_height)
        else:
            source = image_value
            caption = ''
        if not isinstance(source, str) or not source.strip():
            raise ValueError('La imagen debe indicar una ruta no vacía.')
        image_path = Path(source)
        if not image_path.is_absolute():
            image_path = ROOT / image_path
        if not image_path.exists():
            raise FileNotFoundError(f'No se encontró la imagen: {image_path}')
        image_width, image_height = ImageReader(str(image_path)).getSize()
        scale = min(width / image_width, max_height / image_height)
        draw_width = image_width * scale
        draw_height = image_height * scale
        if y - draw_height < 52:
            raise ValueError(f'La imagen excede el área imprimible de la página {self.page}.')
        draw_x = x + (width - draw_width) / 2
        self.c.drawImage(str(image_path), draw_x, y - draw_height, draw_width, draw_height,
                         preserveAspectRatio=True, mask='auto')
        y -= draw_height + gap
        if caption:
            y = self.p(escape(str(caption)), y, x=x, width=width, size=8, gap=6)
        return y

    def q(self, q, y, x=M, width=None):
        width = width or W - 2 * M
        self.c.setStrokeColor(RULE)
        self.c.setLineWidth(.55)
        self.c.line(x, y + 3, x + width, y + 3)
        y = self.p(f'<b>{q["n"]}.</b> {escape(q["stem"])}', y - 8, x, width, gap=6)
        if q.get('image'):
            y = self.image(q['image'], y - 2, x, width, max_height=135, gap=7)
        for letter, text in zip('ABCDEFG', q.get('options', [])):
            y = self.p(f'<b>{letter}.</b> {escape(text)}', y, x + 12, width - 12, gap=2)
        self.c.setStrokeColor(RULE)
        self.c.line(x, y - 3, x + width, y - 3)
        return y - 17

    def table(self, rows, y, widths):
        style = ParagraphStyle('cell', fontName='Helvetica', fontSize=9, leading=12,
                               textColor=INK)
        header_style = ParagraphStyle('header_cell', fontName='Helvetica-Bold', fontSize=9,
                                      leading=12, textColor=INK)
        data = []
        for row_index, row in enumerate(rows):
            cell_style = header_style if row_index == 0 else style
            data.append([Paragraph(escape(str(v)), cell_style) for v in row])
        t = Table(data, colWidths=widths, hAlign='LEFT')
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), GRAY),
            ('GRID', (0, 0), (-1, -1), .55, RULE),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        _, h = t.wrap(W - 2 * M, H)
        if y - h < 52:
            raise ValueError(f'Table exceeds page {self.page}')
        t.drawOn(self.c, M, y - h)
        return y - h - 18

    def save(self):
        self.c.save()


def all_questions(bank):
    e = bank['english']
    return (bank['reading']['questions'] + bank['mathematics'] + bank['science'] + bank['social']
            + e['matching'] + [e['notice'], e['conversation']] + e['grammar'] + e['literal']
            + [e['inference']] + e['lexical'])


def _mapping(value):
    return value if isinstance(value, dict) else {}


def _text(value):
    return isinstance(value, str) and bool(value.strip())


def _validate_question(question, path, expected_number, errors, option_count=None,
                       allowed_answers='ABCD'):
    if not isinstance(question, dict):
        errors.append(f'{path}: debe ser un objeto.')
        return
    if question.get('n') != expected_number:
        errors.append(f'{path}.n: se esperaba {expected_number}.')
    for field in ('stem', 'topic', 'why'):
        if not _text(question.get(field)):
            errors.append(f'{path}.{field}: es obligatorio y no puede estar vacío.')
    if not _text(question.get('answer')) or question.get('answer') not in allowed_answers:
        errors.append(f'{path}.answer: debe ser una letra de {allowed_answers}.')
    if option_count is None:
        return
    options = question.get('options')
    if not isinstance(options, list) or len(options) != option_count:
        errors.append(f'{path}.options: se esperaban {option_count} opciones.')
        return
    if any(not _text(option) for option in options):
        errors.append(f'{path}.options: ninguna opción puede estar vacía.')
    if len({option.strip() for option in options if isinstance(option, str)}) != len(options):
        errors.append(f'{path}.options: no puede haber opciones repetidas.')
    if question.get('answer') not in 'ABCDEFG'[:option_count]:
        errors.append(f'{path}.answer: no corresponde al número de opciones.')


def _validate_group(section, items, numbers, errors, option_count=4, allowed_answers='ABCD'):
    if not isinstance(items, list):
        errors.append(f'{section}: debe ser una lista.')
        return
    if len(items) != len(numbers):
        errors.append(f'{section}: se esperaban {len(numbers)} preguntas y hay {len(items)}.')
    for index, expected_number in enumerate(numbers):
        if index < len(items):
            _validate_question(items[index], f'{section}[{index}]', expected_number, errors,
                               option_count, allowed_answers)


def validate_bank(bank):
    """Validate the fixed 22-item bank used by the booklet layout."""
    errors = []
    if not isinstance(bank, dict):
        raise ValueError('El banco debe ser un objeto JSON.')
    for field in ('title', 'version', 'disclaimer'):
        if not _text(bank.get(field)):
            errors.append(f'{field}: es obligatorio y no puede estar vacío.')

    reading = _mapping(bank.get('reading'))
    social = bank.get('social')
    mathematics = bank.get('mathematics')
    science = bank.get('science')
    english = _mapping(bank.get('english'))

    if not _text(reading.get('title')):
        errors.append('reading.title: es obligatorio.')
    if not _text(reading.get('text')):
        errors.append('reading.text: es obligatorio.')
    _validate_group('reading.questions', reading.get('questions'), [1, 2], errors)
    _validate_group('social', social, [3, 4], errors)
    _validate_group('mathematics', mathematics, [5, 6, 7], errors)
    _validate_group('science', science, [8, 9, 10], errors)

    words = english.get('words')
    if not isinstance(words, list) or len(words) != 7 or any(not _text(word) for word in words):
        errors.append('english.words: se requieren exactamente 7 palabras no vacías.')
    elif len(set(words)) != len(words):
        errors.append('english.words: no puede haber palabras repetidas.')
    _validate_group('english.matching', english.get('matching'), [11, 12, 13], errors,
                    option_count=None, allowed_answers='ABCDEFG')
    for field, number in (('notice', 14), ('conversation', 15), ('inference', 20)):
        option_count = 4 if field == 'inference' else 3
        _validate_question(english.get(field), f'english.{field}', number, errors, option_count)
    _validate_group('english.grammar', english.get('grammar'), [16, 17], errors, 3)
    _validate_group('english.literal', english.get('literal'), [18, 19], errors, 3)
    _validate_group('english.lexical', english.get('lexical'), [21, 22], errors, 4)

    text_placeholders = (
        ('english.grammarText', english.get('grammarText'), [16, 17]),
        ('english.literalText', english.get('literalText'), []),
        ('english.inferenceText', english.get('inferenceText'), []),
        ('english.lexicalText', english.get('lexicalText'), [21, 22]),
    )
    for path, value, placeholders in text_placeholders:
        if not _text(value):
            errors.append(f'{path}: es obligatorio.')
        elif placeholders:
            for number in placeholders:
                if f'{{{{{number}}}}}' not in value:
                    errors.append(f'{path}: falta el marcador {{{{{number}}}}}.')

    if not errors:
        questions = sorted(all_questions(bank), key=lambda question: question['n'])
        if [question['n'] for question in questions] != list(range(1, 23)):
            errors.append('La numeración final debe recorrer exactamente del 1 al 22.')
    if errors:
        details = '\n'.join(f'- {error}' for error in errors)
        raise ValueError('El banco no cumple la plantilla fija de 22 ítems:\n' + details)
    validate_assessments(bank, questions)
    return questions


def make_student(bank, path):
    b = Book(path, bank['version'])
    y = b.start('Cuadernillo de práctica', 'EDICIÓN DE MUESTRA | 22 PREGUNTAS | CINCO ÁREAS')
    y = b.p('Practicar también es aprender<br/>a leer la prueba.', y - 20, size=26, bold=True, gap=24)
    y = b.p(escape(bank['disclaimer']), y, size=11, gap=24)
    y = b.cover_cards([
        ('Edición', bank['version']),
        ('Ítems', '22'),
        ('Áreas', '5'),
        ('Uso', 'Práctica'),
    ], y - 2)
    y = b.table([['Área', 'Preguntas'], ['Lectura crítica', '1-2'], ['Sociales y ciudadanas', '3-4'],
                 ['Matemáticas', '5-7'], ['Ciencias naturales', '8-10'], ['Inglés', '11-22']], y, [350, W - 2*M - 350])
    y = b.p('Nombre: ___________________________________________', y - 8)
    y = b.p('Institución / grupo: ___________________________________', y)
    y = b.p('Fecha: __________________     Versión: ' + bank['version'], y, gap=24)
    y = b.banner('ANTES DE COMENZAR', y)
    y = b.p('Lee cada contexto y selecciona una sola respuesta por pregunta. Marca las respuestas en la hoja del final, no sobre las opciones del cuadernillo.', y)
    y = b.p('En inglés, revisa las instrucciones de cada parte: algunas preguntas tienen tres opciones; otras, cuatro; el vocabulario usa un banco común A-G.', y)
    b.p('Esta muestra ilustra el diseño. No representa la extensión, distribución, duración ni calificación oficial del examen. El docente define el tiempo de esta actividad.', y, size=9)

    y = b.start('Lectura crítica y Sociales y ciudadanas')
    y = b.banner('RESPONDE LAS PREGUNTAS 1 Y 2 SEGÚN EL SIGUIENTE TEXTO', y)
    y = b.p(escape(bank['reading']['title']), y, size=13, bold=True)
    y = b.p(escape(bank['reading']['text']), y, gap=6)
    y = b.p('Texto original elaborado para esta muestra.', y, size=8, gap=18)
    col = (W - 2 * M - 24) / 2
    ends = [b.q(q, y, M + i * (col + 24), col) for i, q in enumerate(bank['reading']['questions'])]
    b.c.setStrokeColor(RULE)
    b.c.setLineWidth(.55)
    b.c.line(M + col + 12, y + 3, M + col + 12, min(ends) + 8)
    y = b.banner('SOCIALES Y CIUDADANAS | PREGUNTAS INDEPENDIENTES', min(ends) - 6)
    for q in bank['social']:
        y = b.q(q, y)

    y = b.start('Matemáticas')
    y = b.banner('UTILIZA LA TABLA PARA RESPONDER LA PREGUNTA 5', y)
    y = b.table([['Día', 'Lunes', 'Martes', 'Miércoles', 'Jueves'], ['Préstamos', '20', '30', '10', '40']], y,
                [W - 2*M - 4*98, 98, 98, 98, 98])
    for q in bank['mathematics']:
        y = b.q(q, y)
    y = b.banner('ESPACIO PARA PROCEDIMIENTOS', y)
    for k in range(5):
        b.c.setStrokeColor(GRAY)
        b.c.line(M, y - k * 24, W - M, y - k * 24)

    y = b.start('Ciencias naturales')
    y = b.banner('SELECCIONA LA OPCIÓN QUE MEJOR EXPLICA CADA SITUACIÓN', y)
    for q in bank['science']:
        y = b.q(q, y)
    y = b.p('Esquema de apoyo para la pregunta 10 (no está a escala).', y, size=9)
    c = b.c
    for i, (label, width) in enumerate([('Área de apoyo: 0,02 m²', 90), ('Área de apoyo: 0,04 m²', 150)]):
        x = M + 35 + i * 250
        c.setFillColor(GRAY)
        c.setStrokeColor(INK)
        c.rect(x, y - 65, width, 42, fill=1)
        c.line(x - 10, y - 65, x + width + 10, y - 65)
        c.setFillColor(INK)
        c.setFont('Helvetica', 9)
        c.drawString(x, y - 83, label)
        c.drawString(x, y - 12, 'Mismo peso: 120 N')

    e = bank['english']
    y = b.start('Inglés | Partes 1, 2 y 3')
    y = b.banner('PARTE 1 | ASOCIACIÓN DE VOCABULARIO | 11-13', y)
    y = b.p('Relaciona cada descripción con una palabra del banco A-G. Sobran cuatro palabras. El ejemplo usa H y no se incluye en el banco.', y, size=9)
    y = b.p('<b>Ejemplo 0.</b> You sit on this. <b>H. chair</b>', y, size=10, gap=16)
    left_y = right_y = y
    for q in e['matching']:
        left_y = b.p(f'<b>{q["n"]}.</b> {escape(q["stem"])}', left_y, width=300, gap=23)
    for letter, word in zip('ABCDEFG', e['words']):
        right_y = b.p(f'<b>{letter}.</b> {word}', right_y, x=385, width=150, gap=7)
    b.c.setStrokeColor(colors.HexColor('#B8BEC8'))
    b.c.line(365, y, 365, min(left_y, right_y))
    y = b.banner('PARTE 2 | AVISOS | PREGUNTA 14', min(left_y, right_y) - 14)
    y = b.p('Lee el aviso y selecciona A, B o C.', y, size=9)
    y = b.table([['PLEASE RETURN BOOKS TO THE DESK AFTER USE']], y, [W - 2*M])
    y = b.q(e['notice'], y)
    y = b.banner('PARTE 3 | CONVERSACIONES | PREGUNTA 15', y)
    y = b.p('Selecciona la respuesta más apropiada: A, B o C.', y, size=9)
    b.q(e['conversation'], y)

    y = b.start('Inglés | Partes 4 y 5')
    y = b.banner('PARTE 4 | COMPLETA EL TEXTO | 16-17', y)
    y = b.p('Selecciona la palabra correcta para cada espacio: A, B o C.', y, size=9)
    y = b.p(escape(e['grammarText']).replace('{{16}}', '________').replace('{{17}}', '________'), y, gap=20)
    for q in e['grammar']:
        y = b.q(q, y)
    y = b.banner('PARTE 5 | COMPRENSIÓN LITERAL | 18-19', y)
    y = b.p('Lee el texto y responde. Selecciona A, B o C.', y, size=9)
    y = b.p(escape(e['literalText']), y, gap=20)
    for q in e['literal']:
        y = b.q(q, y)

    y = b.start('Inglés | Partes 6 y 7')
    y = b.banner('PARTE 6 | COMPRENSIÓN INFERENCIAL | PREGUNTA 20', y)
    y = b.p('Lee el texto y selecciona A, B, C o D.', y, size=9)
    y = b.p(escape(e['inferenceText']), y, gap=20)
    y = b.q(e['inference'], y)
    y = b.banner('PARTE 7 | VOCABULARIO EN CONTEXTO | 21-22', y)
    y = b.p('Selecciona la palabra correcta para cada espacio: A, B, C o D.', y, size=9)
    y = b.p(escape(e['lexicalText']).replace('{{21}}', '________').replace('{{22}}', '________'), y, gap=20)
    for q in e['lexical']:
        y = b.q(q, y)

    y = b.start('Hoja de respuestas')
    y = b.p('Nombre: _____________________________________    Grupo: ______________', y)
    y = b.p('Rellena un solo círculo por fila. En las preguntas 11-13 se usa A-G; en las demás se muestran únicamente las opciones disponibles.', y, size=10, gap=18)
    y = b.p('<b>Ejemplo de marcado:</b> elige una sola opción y rellena completamente su círculo.', y, size=8.5, gap=18)
    questions = sorted(all_questions(bank), key=lambda q: q['n'])
    for q in questions:
        if y < 80:
            raise ValueError('Answer sheet overflow')
        b.c.setFillColor(INK)
        b.c.setFont('Helvetica-Bold', 10)
        b.c.drawString(M + 12, y, f'{q["n"]:02}')
        letters = 'ABCDEFG' if q['n'] in (11, 12, 13) else 'ABCD'[:len(q['options'])]
        for i, letter in enumerate(letters):
            x = M + 90 + i * 43
            b.c.setStrokeColor(INK)
            b.c.circle(x, y + 3, 8)
            b.c.setFont('Helvetica', 8)
            b.c.drawCentredString(x, y + .3, letter)
        y -= 25
    b.p('Hoja para corrección manual. No está calibrada para lectura óptica.', y - 8, size=8)
    b.save()


def make_teacher(bank, path):
    b = Book(path, bank['version'] + '-DOC')
    y = b.start('Guía de plantilla y control docente')
    y = b.p('Propuesta editorial, no especificación oficial del examen.', y, size=12, bold=True)
    y = b.table([
        ['Elemento', 'Decisión de esta plantilla'],
        ['Página', 'A4 vertical; márgenes de 42 pt (aprox. 15 mm). Se puede preparar una variante Carta.'],
        ['Tipografía', 'Texto 10,5 pt; interlineado 14,2 pt; títulos 16 pt. Texto seleccionable y gráficos vectoriales.'],
        ['Distribución', 'Una columna para tablas y contextos; dos para preguntas breves. No partir preguntas entre páginas.'],
        ['Identificación', 'Marca propia, versión visible y numeración continua. Sin logotipos oficiales ni respuestas marcadas.'],
        ['Contextos', 'Texto o imagen una sola vez por bloque; rango de preguntas explícito. Fuente y licencia en el banco definitivo.'],
        ['Inglés', 'Siete partes ilustradas. Banco A-G; selección A-C y A-D; ejemplos separados de los ítems evaluados.'],
        ['Entrega', 'Cuadernillo del estudiante + hoja de respuestas; clave y explicaciones en archivo docente separado.'],
        ['Alcance', '22 preguntas originales de muestra. No equivale a un simulacro completo ni a cobertura de todo el currículo.'],
    ], y, [95, W - 2*M - 95])
    y = b.banner('ANTES DE GENERAR CUADERNILLOS COMERCIALES', y)
    for text in [
        '1. Acordar áreas, temas, competencias, cantidad de preguntas y tiempo de aplicación con el docente.',
        '2. Revisar cada pregunta: una clave inequívoca, distractores plausibles, cálculos, redacción y accesibilidad.',
        '3. Registrar autoría, fuentes, permisos y cambios. Las referencias proporcionadas se usan para observar el formato; aquí no se reproducen sus preguntas.',
        '4. Validar dificultad mediante revisión y aplicación piloto; no asignar niveles psicométricos sin evidencia.',
        '5. Generar versiones sin duplicar ítems ni separar un contexto de sus preguntas. Si se barajan opciones, regenerar la clave.',
        '6. Renderizar, revisar cada página e imprimir una prueba al 100 %. Mantener la clave docente fuera del PDF del estudiante.',
    ]:
        y = b.p(text, y, size=9.5)
    b.p('Generador local de muestra independiente de la app: no modifica el banco cargado, diagnósticos ni servicios. La selección automática de un banco grande es una etapa posterior.', y, size=9)

    y = b.start('Clave de respuestas y cobertura')
    y = b.p('Uso docente. Respuestas propuestas y revisadas en cálculos y coherencia interna; requieren aprobación docente antes de aplicarlas como evaluación.', y, size=9)
    rows = [['N.º', 'Clave', 'Tema / justificación']]
    for q in sorted(all_questions(bank), key=lambda q: q['n']):
        rows.append([q['n'], q['answer'], q['topic'] + ': ' + q['why']])
    b.table(rows, y, [34, 45, W - 2*M - 79])
    append_teacher_pages(b, bank, sorted(all_questions(bank), key=lambda q: q['n']))
    b.save()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--bank', type=Path, default=ROOT / 'tool' / 'booklet_template_bank.json')
    parser.add_argument('--output-suffix', default='', help='Sufijo para conservar versiones anteriores.')
    parser.add_argument('--validate-only', action='store_true',
                        help='Valida el banco y no genera PDF.')
    args = parser.parse_args()
    bank = json.loads(args.bank.read_text(encoding='utf-8'))
    questions = validate_bank(bank)
    if args.validate_only:
        print(f'Valid bank: {len(questions)} items, seven English formats, version {bank["version"]}.')
        return
    OUT.mkdir(parents=True, exist_ok=True)
    suffix = f'_{args.output_suffix}' if args.output_suffix else ''
    make_student(bank, OUT / f'SaberPlus_muestra_cuadernillo{suffix}.pdf')
    make_teacher(bank, OUT / f'SaberPlus_guia_plantilla_y_clave{suffix}.pdf')
    print('Generated two PDFs; 22 items, seven English formats. No source questions copied.')


if __name__ == '__main__':
    main()
