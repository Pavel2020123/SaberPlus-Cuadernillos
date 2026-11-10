"""Versioned editorial front matter, independent of the fixed sample bank.

uv run --with reportlab python tool/preview_editorial_cover.py
Counts and time are deliberately unconfigured; do not infer an official exam.
"""
import json
import argparse
from pathlib import Path
from xml.sax.saxutils import escape
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--config', type=Path, default=ROOT/'tool/editorial_cover_config.json')
parser.add_argument('--output', type=Path, default=ROOT/'output/pdf/SaberPlus_portada_e_indicaciones_SP-001_ajustada.pdf')
args = parser.parse_args()
CFG = json.loads(args.config.read_text(encoding='utf-8'))
OUTPUT = args.output
W, H = A4
M = 38
NAVY = colors.HexColor('#17263A')
MID = colors.HexColor('#546175')
PALE = colors.HexColor('#EEF1F4')
LINE = colors.HexColor('#BAC3CC')
ACCENT = colors.HexColor('#357B88')
c = canvas.Canvas(str(OUTPUT), pagesize=A4)
c.setTitle('SaberPlus | Simulacro SP-001')
c.setAuthor('SaberPlus')


def p(value, x, top, width, size=10, bold=False, color=NAVY):
    para = Paragraph(value, ParagraphStyle('p', fontName='Helvetica-Bold' if bold else 'Helvetica',
                     fontSize=size, leading=size*1.3, textColor=color))
    _, height = para.wrap(width, H)
    if top-height < 48:
        raise ValueError('Text exceeds printable area')
    para.drawOn(c, x, top-height)
    return top-height


def line(x, y, x2, y2, color=LINE, weight=.6):
    c.setStrokeColor(color)
    c.setLineWidth(weight)
    c.line(x,y,x2,y2)


def rect(x, top, width, height, color, stroke=None, radius=0):
    c.setFillColor(color)
    if stroke:
        c.setStrokeColor(stroke)
    c.setLineWidth(.6)
    if radius:
        c.roundRect(x,top-height,width,height,radius,fill=1,stroke=bool(stroke))
    else:
        c.rect(x,top-height,width,height,fill=1,stroke=bool(stroke))


def header(label):
    p('SaberPlus',M,H-30,220,21,True)
    p(CFG['version'],W-130,H-36,92,10,True)
    line(M,H-78,W-M,H-78,NAVY,1)
    p(label,M,H-87,W-2*M,8,True,color=MID)


def footer(number):
    line(M,42,W-M,42)
    c.setFillGray(.38)
    c.setFont('Helvetica',8)
    c.drawString(M,24,CFG['version']+' · '+CFG['session'])
    # Small neutral-gray editorial watermark, clear of all question content.
    c.saveState()
    c.setFillGray(.70)
    c.setFont('Helvetica-Bold',18)
    c.drawString(W-M-45,19,'S')
    c.setFont('Helvetica-Bold',10)
    c.drawString(W-M-33,27,'+')
    c.restoreState()
    c.setFillGray(.30)
    c.setFont('Helvetica',8.5)
    c.drawRightString(W-M,24,str(number))


def mascot(x, y, width, height, image='assets/Sabi_Inicio_Refuerzo.png'):
    c.drawImage(str(ROOT/image),x,y,width,height,
                preserveAspectRatio=True,anchor='c',mask='auto')


header('CUADERNILLO DEL ESTUDIANTE')
if CFG.get('notice'):
    p(escape(CFG['notice']),M,H-102,W-2*M,7,color=MID)
p('SIMULACRO',M,H-115,340,32,True)
p(escape(CFG['session']).upper(),M,H-164,340,13,True,color=ACCENT)

# New mascot illustration replaces the schematic cards and repeated cutout.
hero_width = 430
hero_left = (W-hero_width)/2
hero_top = H-205
hero_height = 186
hero_padding = 14
rect(hero_left,hero_top,hero_width,hero_height,PALE,radius=16)
# The entire image box fits inside the panel; no gills, feet or desk overflow.
mascot(hero_left+hero_padding,hero_top-hero_height+hero_padding,
       hero_width-2*hero_padding,hero_height-2*hero_padding,CFG['cover_image'])

# Session structure is configured, never copied from unrelated booklets.
y=H-416
table_top = y
table_height = 25 + 24 + 28 * len(CFG['areas']) + 30
c.saveState()
table_clip = c.beginPath()
table_clip.roundRect(M, table_top-table_height, W-2*M, table_height, 12)
c.clipPath(table_clip, stroke=0, fill=0)
rect(M,y,W-2*M,25,NAVY)
p('ESTRUCTURA DE LA SESIÓN',M+10,y-6,300,9,True,color=colors.white)
y-=25
rect(M,y,W-2*M,24,PALE)
p('ÁREA',M+11,y-6,300,8,True)
p('PREGUNTAS',W-145,y-6,100,8,True)
y-=24
for area in CFG['areas']:
    p(escape(area['name']),M+11,y-7,330,10)
    p(str(area['count']) if area['count'] is not None else 'Por definir',W-145,y-7,100,9,color=MID)
    y-=28
    line(M,y,W-M,y)
rect(M,y,W-2*M,30,PALE)
p('TIEMPO DE APLICACIÓN',M+11,y-9,280,8,True)
p(escape(CFG['time']),W-145,y-8,100,10,True)
c.restoreState()
c.setStrokeColor(LINE)
c.setLineWidth(.6)
c.roundRect(M,table_top-table_height,W-2*M,table_height,12,stroke=1,fill=0)
y-=43
p('DATOS DEL ESTUDIANTE',M,y,300,8,True,color=MID)
y-=24
for label in ['Nombre completo', 'Institución y grupo']:
    p(label,M,y,250,8,color=MID)
    line(M,y-31,W-M,y-31)
    y-=44
p('Fecha: ____________________',M,y,270,9)
p('Código: '+CFG['version'],W-165,y,130,9)
rect(M,94,W-2*M,25,NAVY,radius=8)
p('NO COMIENCES HASTA RECIBIR LA INDICACIÓN DEL DOCENTE',M+10,87,W-2*M-20,8.5,True,color=colors.white)
footer(1)
c.showPage()

header('')
p('Antes de comenzar',M,H-116,365,24,True)
p('Revisa tu material. Organiza tu tiempo. Responde con atención.',M,H-150,370,10,color=MID)
mascot(W-142,H-200,102,100,CFG['instructions_image'])


def block(number,title,body,x,top,width):
    rect(x,top,width,112,colors.white,LINE,radius=12)
    c.setFillColor(NAVY)
    c.circle(x+23,top-22,12,fill=1,stroke=0)
    p(str(number).zfill(2),x+16,top-15,24,9,True,color=colors.white)
    p(title,x+44,top-15,width-54,10.5,True)
    p(body,x+14,top-45,width-28,9.3)


col=(W-2*M-14)/2
items=[
 ('Identifica tu cuadernillo','Comprueba la sesión y la versión. Escribe tus datos tanto en el cuadernillo como en la hoja de respuestas.'),
 ('Comprueba el material','Ten a mano el cuadernillo, la hoja de respuestas y los útiles autorizados por el docente.'),
 ('Lee antes de responder','Revisa el enunciado completo y todas sus opciones. Algunas preguntas comparten textos, imágenes o tablas.'),
 ('Ubica bien tu respuesta','Haz coincidir el número de la pregunta con la fila de la hoja. Marca solo una opción por pregunta.'),
 ('Atiende cada formato','Si la sesión incluye inglés, sigue las instrucciones de cada parte: pueden cambiar las letras disponibles.'),
 ('Administra tu tiempo','El docente indicará la duración. Revisa tus respuestas y entrega el material cuando se solicite.'),
]
for i,(title,body) in enumerate(items):
    block(i+1,title,body,M+(i%2)*(col+14),H-218-(i//2)*125,col)

top=H-610
rect(M,top,W-2*M,107,PALE,radius=12)
p('ASÍ SE MARCA UNA RESPUESTA',M+12,top-10,400,9,True)
base=top-50
for group,(label,marked) in enumerate([('UNA OPCIÓN',{'B'}),('EVITA DOS MARCAS',{'A','C'})]):
    x=M+13+group*col
    p(label,x,base+13,200,7.5,True,color=MID)
    for i,letter in enumerate('ABCD'):
        cx=x+14+i*35
        c.setStrokeColor(NAVY)
        c.setFillColor(NAVY if letter in marked else colors.white)
        c.circle(cx,base-18,8,fill=1,stroke=1)
        c.setFillColor(colors.white if letter in marked else NAVY)
        c.setFont('Helvetica',8)
        c.drawCentredString(cx,base-21,letter)
p('Ejemplo ilustrativo: las letras disponibles dependen del tipo de pregunta.',M+12,top-88,W-2*M-24,8,color=MID)
p('Durante la aplicación',M,101,240,10,True)
p('Sigue las reglas que indique tu docente sobre dispositivos, consultas y materiales permitidos.',M,83,W-2*M,9)
footer(2)
c.save()
print(OUTPUT)
