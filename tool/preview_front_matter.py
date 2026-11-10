"""Standalone cover/instructions design preview; not an assembled exam."""
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle

ROOT = Path(__file__).resolve().parents[1]
W, H = A4
M = 42
INK = colors.HexColor('#17243A')
LIGHT = colors.HexColor('#F1F4F8')
MUTED = colors.HexColor('#526176')
OUTPUT = ROOT / 'output/pdf/SaberPlus_portada_e_indicaciones_propuesta.pdf'
OUTPUT.parent.mkdir(parents=True, exist_ok=True)
c = canvas.Canvas(str(OUTPUT), pagesize=A4)
c.setTitle('SaberPlus | Propuesta de portada e indicaciones')
c.setAuthor('SaberPlus')


def text(value, x, y, width, size=11, bold=False):
    p = Paragraph(value, ParagraphStyle('p', fontName='Helvetica-Bold' if bold else 'Helvetica',
                  fontSize=size, leading=size*1.35, textColor=INK))
    _, h = p.wrap(width, H)
    if y-h < 48:
        raise ValueError('Content exceeds page')
    p.drawOn(c, x, y-h)
    return y-h


def footer(page):
    c.setStrokeColor(colors.HexColor('#CDD4DE'))
    c.line(M, 42, W-M, 42)
    c.setFillColor(MUTED)
    c.setFont('Helvetica', 8)
    c.drawString(M, 27, 'SaberPlus | Práctica independiente, no oficial')
    c.drawRightString(W-M, 27, f'Propuesta visual / {page}')


def box(x, top, width, height, title, value):
    c.setFillColor(LIGHT)
    c.roundRect(x, top-height, width, height, 10, fill=1, stroke=0)
    text(title.upper(), x+14, top-13, width-28, 8, True)
    text(value, x+14, top-34, width-28, 12, True)


text('SaberPlus', M, H-40, 220, 23, True)
text('SIMULACROS / EDICIÓN PROPIA', M, H-73, 300, 9)
c.setFillColor(LIGHT)
c.roundRect(M, H-365, W-2*M, 245, 18, fill=1, stroke=0)
text('Tu siguiente<br/>paso empieza<br/>aquí.', M+22, H-153, 260, 29, True)
text('Lee con atención.<br/>Piensa y decide.', M+22, H-285, 240, 12)
c.drawImage(str(ROOT/'assets/Sabi_Inicio_Refuerzo.png'), W-285, H-365, 240, 245,
            preserveAspectRatio=True, anchor='c', mask='auto')
text('SIMULACRO DE PRÁCTICA', M, H-392, W-2*M, 21, True)
text('Propuesta de portada. La sesión se define al armar el cuadernillo.', M, H-425, W-2*M, 10)
width=(W-2*M-12)/2
box(M,H-461,width,75,'Sesión','Primera / Segunda')
box(M+width+12,H-461,width,75,'Versión','Código del cuadernillo')
y=H-563
for label in ['Nombre completo', 'Institución y grupo', 'Fecha de aplicación']:
    text(label.upper(),M,y,W-2*M,8,True)
    c.setStrokeColor(colors.HexColor('#A9B3C2'))
    c.line(M,y-36,W-M,y-36)
    y-=58
text('Antes de comenzar, consulta las indicaciones de la página siguiente.',M,100,W-2*M,10,True)
footer(1)
c.showPage()

text('Antes de comenzar',M,H-43,340,24,True)
text('Sabi te acompaña en la preparación.',M,H-80,340,11)
c.drawImage(str(ROOT/'assets/Sabi_Inicio_Refuerzo.png'),W-165,H-161,110,115,
            preserveAspectRatio=True,anchor='c',mask='auto')
y=H-165
steps=[
 ('Revisa tu material','Comprueba la sesión, la versión del cuadernillo y la hoja de respuestas. Escribe tus datos donde corresponda.'),
 ('Lee el contexto completo','Algunas preguntas comparten una lectura, una tabla o una gráfica. Úsala para responder el grupo indicado.'),
 ('Marca una sola respuesta','Comprueba el número de la pregunta y rellena una única opción en la hoja de respuestas. Evita dejar dos opciones marcadas.'),
 ('Revisa cada parte de inglés','El banco de palabras, los avisos, las conversaciones y las lecturas tienen instrucciones y cantidades de opciones diferentes.'),
 ('Sigue las indicaciones de aplicación','El docente indicará el tiempo y los materiales permitidos. Comienza cuando se dé la señal y revisa tus respuestas antes de entregar.'),
]
for i,(title,body) in enumerate(steps,1):
    c.setFillColor(INK)
    c.circle(M+13,y-14,13,fill=1,stroke=0)
    c.setFillColor(colors.white)
    c.setFont('Helvetica-Bold',11)
    c.drawCentredString(M+13,y-18,str(i))
    bottom=text(title,M+39,y,W-2*M-39,12,True)
    bottom=text(body,M+39,bottom-6,W-2*M-39,10.5)
    y=bottom-23
text('Ejemplo de marcado',M,y,W-2*M,12,True)
y-=42
c.setFont('Helvetica-Bold',10)
c.setFillColor(INK)
c.drawString(M,y,'01')
for i,letter in enumerate('ABCD'):
    x=M+68+i*45
    c.setStrokeColor(INK)
    c.setFillColor(INK if letter=='B' else colors.white)
    c.circle(x,y+3,9,fill=1,stroke=1)
    c.setFillColor(colors.white if letter=='B' else INK)
    c.setFont('Helvetica',9)
    c.drawCentredString(x,y,letter)
text('En este ejemplo se seleccionó únicamente B.',M,y-22,W-2*M,9)
text('La tabla de áreas, cantidades y tiempo se incorporará desde la configuración de cada simulacro. Esta propuesta no fija todavía esos valores.',M,104,W-2*M,9)
footer(2)
c.save()
print(OUTPUT)
