"""Local, vector Mathtext inside measured ReportLab paragraphs; no external TeX."""
from functools import lru_cache
from io import BytesIO
import base64
import re
import threading
from xml.sax.saxutils import escape
from PIL import Image
from reportlab.platypus import Paragraph
from reportlab.lib.utils import ImageReader

LOCK=threading.RLock()
TOKEN=re.compile(r'\\\((.*?)\\\)|\\\[(.*?)\\\]',re.S)
_blank=BytesIO()
Image.new('RGBA',(1,1),(255,255,255,0)).save(_blank,format='PNG')
BLANK='data:image/png;base64,'+base64.b64encode(_blank.getvalue()).decode('ascii')


@lru_cache(maxsize=256)
def equation_path(expression,size):
    """Return immutable vector geometry and physical metrics, in PDF points."""
    if not expression.strip() or len(expression)>600:
        raise ValueError('Ecuación vacía o demasiado larga (máximo 600 caracteres).')
    if '$' in expression:
        raise ValueError('Dentro de una ecuación no uses $. Usa los delimitadores \\( y \\).')
    # Mathtext expects a single line even when display delimiters span lines.
    expression=re.sub(r'[\r\n\t]+',' ',expression).strip()
    try:
        from matplotlib.font_manager import FontProperties
        from matplotlib.textpath import TextPath
    except ImportError as exc:
        raise ValueError('Falta el motor matemático. Inicia el editor con uv run --with matplotlib.') from exc
    try:
        with LOCK:
            prop=FontProperties(size=size,math_fontfamily='stix')
            path=TextPath((0,0),'$'+expression+'$',size=size,prop=prop,usetex=False)
            bounds=path.get_extents()
            # Use ink bounds with a small safety margin for radicals/accents.
            left,bottom,right,top=map(float,(bounds.x0,bounds.y0,bounds.x1,bounds.y1))
            if not all(__import__('math').isfinite(v) for v in (left,bottom,right,top)):
                raise ValueError('La ecuación no contiene símbolos visibles.')
            segments=tuple((tuple(map(float,points)),int(code))
                           for points,code in path.iter_segments(curves=True,simplify=False))
        return (right-left+2,top-bottom+2,max(0,-bottom)+1,left,bottom,segments)
    except (ValueError,RuntimeError,KeyError) as exc:
        raise ValueError('Ecuación inválida o comando no soportado: '+expression[:100]) from exc


def draw_equation(canvas,geometry,x,baseline,color):
    width,height,depth,left,bottom,segments=geometry
    canvas.saveState()
    canvas.translate(x+1-left,baseline)
    canvas.setFillColor(color)
    path=canvas.beginPath()
    current=(0,0)
    for points,code in segments:
        if code==1:
            path.moveTo(*points);current=points
        elif code==2:
            path.lineTo(*points);current=points
        elif code==3:
            cx,cy,x2,y2=points;x0,y0=current
            path.curveTo(x0+2*(cx-x0)/3,y0+2*(cy-y0)/3,
                         x2+2*(cx-x2)/3,y2+2*(cy-y2)/3,x2,y2)
            current=(x2,y2)
        elif code==4:
            path.curveTo(*points);current=points[-2:]
        elif code==79:
            path.close()
    canvas.drawPath(path,stroke=0,fill=1)
    canvas.restoreState()


class MathParagraph(Paragraph):
    """Reserve equation width/height in normal text wrapping, paint as vectors."""
    def __init__(self,*args,equations=None,**kwargs):
        self.equations=equations or {}
        super().__init__(*args,**kwargs)
        if self.equations:
            index=0
            for fragment in self.frags:
                callback=getattr(fragment,'cbDefn',None)
                if callback and callback.kind=='img':
                    reader=ImageReader(BytesIO(_blank.getvalue()))
                    reader._sp_geometry=self.equations[str(index)]
                    callback.image=reader
                    index+=1

    def wrap(self,width,height):
        if any(g[0]>width for g in self.equations.values()):
            raise ValueError('Una ecuación excede el ancho disponible. Divide la fórmula o usa ancho completo; no se reducirá la letra automáticamente.')
        wrapped_width,wrapped_height=super().wrap(width,height)
        # Extra room above the first line for formulas taller than the text ascent.
        return wrapped_width,wrapped_height+getattr(self,'top_pad',0)

    def split(self,width,height):
        parts=super().split(width,height)
        for part in parts:
            part.equations=self.equations
        return parts

    def draw(self):
        canvas=self.canv
        previous=canvas.drawImage
        def draw_inline(image,x,y,width=None,height=None,*args,**kwargs):
            geometry=getattr(image,'_sp_geometry',None)
            if geometry is not None:
                # Position from the *same indivisible inline image* that reserves
                # width. A preceding zero-width callback can stay on an old line.
                draw_equation(canvas,geometry,x,y+geometry[2],self.style.textColor)
                return geometry[0],geometry[1]
            return previous(image,x,y,width,height,*args,**kwargs)
        canvas.drawImage=draw_inline
        try:
            super().draw()
        finally:
            canvas.drawImage=previous


def _plain(fragment):
    """Escape prose around formulas; Unicode subscripts become real lowered text."""
    markup=escape(fragment).replace('\n','<br/>')
    return re.sub('[₀-₉]+',lambda m:'<sub>'+''.join(str(ord(c)-0x2080) for c in m.group())+'</sub>',markup)


def math_paragraph(text,style,bullet=None):
    text=str(text)
    matches=list(TOKEN.finditer(text))
    remainder=TOKEN.sub('',text)
    if any(delimiter in remainder for delimiter in ('\\(','\\)','\\[','\\]')):
        raise ValueError('Hay una ecuación sin cerrar. Usa \\( fórmula \\) o \\[ fórmula \\].')
    if len(matches)>40:
        raise ValueError('Un párrafo admite como máximo 40 ecuaciones.')
    markup=[];geometries={};position=0
    for index,match in enumerate(matches):
        markup.append(_plain(text[position:match.start()]))
        expression=match[1] if match[1] is not None else match[2]
        # Mathtext sets fractions at script size; in body text they must print at
        # full size, so render every fraction in display style (same expression).
        geometry=equation_path(re.sub(r'\\frac(?![A-Za-z])',r'\\dfrac',expression),style.fontSize)
        width,height,depth,*_=geometry
        key=str(index);geometries[key]=geometry
        fragment=f'<img src="{BLANK}" width="{width}" height="{height}" valign="{-depth}"/>'
        if match[2] is not None:
            # A display formula sits on its own line; do not stack extra blank lines
            # when the author already left line breaks around it.
            before='' if text[:match.start()].rstrip(' ').endswith('\n') or match.start()==0 else '<br/>'
            after='' if text[match.end():].lstrip(' ').startswith('\n') or match.end()==len(text) else '<br/>'
            fragment=before+fragment+after
        markup.append(fragment)
        position=match.end()
    markup.append(_plain(text[position:]))
    style=__import__('copy').copy(style)
    style.autoLeading='max'
    tallest=max((g[1] for g in geometries.values()),default=0)
    if tallest>style.leading and len(remainder)<=160:
        # autoLeading does not reserve height when a tall formula wraps alone onto
        # the next line of a short paragraph (an option): lines overlapped. Use a
        # fixed leading that always fits the tallest formula instead.
        style.autoLeading='off'
        style.leading=tallest+3
    paragraph=MathParagraph(''.join(markup),style,bulletText=bullet,equations=geometries)
    if style.autoLeading=='off':
        rise=max((g[1]-g[2] for g in geometries.values()),default=0)
        paragraph.top_pad=max(0,rise-style.fontSize*.9)
    return paragraph
