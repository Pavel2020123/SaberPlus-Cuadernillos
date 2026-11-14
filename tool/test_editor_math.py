"""No stored project changes: render regression tests entirely in memory."""
import copy
from io import BytesIO
import unittest
import pymupdf
from reportlab.pdfgen import canvas
from editor_pdf import para,Interior,CW,WIDTH
from editor_math import equation_path
from editor_model import demo_project,validate_project

class EditorMathTests(unittest.TestCase):
    def test_display_formula_accepts_line_breaks_inside_delimiters(self):
        self.assertEqual(equation_path('\n x +\n y\n',10),equation_path('x +  y',10))

    def test_supported_notation_and_sequences(self):
        for formula in (r'\sqrt{x^2+1}',r'\frac{a}{b}',r'a_{n+1}=2a_n',
                        r'\sqrt[3]{8}',r'\sum_{k=1}^{n}k',r'\alpha\leq\pi',
                        r'\frac{1}{1+\frac{1}{x}}',r'\overline{AB}',r'\lim_{x\to0}x'):
            with self.subTest(formula=formula):
                geometry=equation_path(formula,10)
                self.assertGreater(geometry[0],0)
                self.assertGreater(geometry[1],0)
                self.assertTrue(geometry[-1])

    def test_inline_wrap_reserves_fraction_height_and_baseline(self):
        normal=para('Texto normal.')
        math=para(r'Calcula \(\frac{1}{\sqrt{x_1^2+1}}\) para el primer término.')
        self.assertGreater(math.wrap(200,700)[1],normal.wrap(200,700)[1])
        stream=BytesIO();c=canvas.Canvas(stream)
        math.drawOn(c,40,600);c.save()
        with pymupdf.open(stream=stream.getvalue(),filetype='pdf') as doc:
            self.assertIn('Calcula',doc[0].get_text())
            self.assertGreater(len(doc[0].get_drawings()),0)

    def test_no_external_tex_or_html_execution(self):
        for formula in (r'\input{/etc/passwd}',r'\write18{anything}',r'\href{http://example.com}{x}'):
            with self.assertRaisesRegex(ValueError,'inválida'):
                equation_path(formula,10)
        p=para(r'<script>no</script> \(x_1\)')
        self.assertIn('&lt;script&gt;',p.text)

    def test_invalid_and_unclosed_notation_gives_actionable_error(self):
        for text in (r'\(\frac{a}\)',r'\(x',r'x\)',r'\[x'):
            with self.subTest(text=text),self.assertRaises(ValueError):para(text)

    def test_money_and_legacy_content_unchanged(self):
        self.assertEqual(para('Costo $3.000').getPlainText(),'Costo $3.000')
        project=demo_project();before=copy.deepcopy(project)
        validate_project(project,exporting=True)
        self.assertEqual(before,project)

    def test_wide_formula_is_not_silently_shrunk(self):
        p=para('\\('+'+'.join(['x_1']*40)+'\\)')
        with self.assertRaisesRegex(ValueError,'excede el ancho'):p.wrap(100,700)

    def test_formula_moves_with_its_reserved_width_when_line_wraps(self):
        p=para('Texto que ocupa casi toda la línea antes de la fórmula '+
               r'\(d=\sqrt{9^2+12^2}=\sqrt{81+144}=\sqrt{225}=15\).')
        p.wrap(230,700)
        data=BytesIO();c=canvas.Canvas(data)
        p.drawOn(c,40,600);c.save()
        with pymupdf.open(stream=data.getvalue(),filetype='pdf') as doc:
            for drawing in doc[0].get_drawings():
                self.assertGreaterEqual(drawing['rect'].x0,39)
                self.assertLessEqual(drawing['rect'].x1,271)

    def test_grid_and_optional_layout_are_measured(self):
        q=next(q for q in demo_project()['questions'] if q['area']=='mathematics')
        q={**q,'layout':'full','options_layout':'grid2',
           'options':[{'text':r'\(\frac{1}{2}\)'},{'text':r'\(\sqrt{2}\)'},
                      {'text':r'\(x_1^2\)'},{'text':r'\(a_n\)'}]}
        book=object.__new__(Interior)
        flows,full,compact=book.question_flows(q,1)
        self.assertTrue(full);self.assertFalse(compact)
        self.assertEqual(len(flows[-1]._cellvalues),2)
        self.assertGreater(flows[-1].wrap(WIDTH-18,700)[1],0)

    def test_new_settings_validate_without_migration(self):
        p=demo_project();q=p['questions'][0]
        q.update(options_layout='grid2',page_break_before=True,image_height=140)
        validate_project(p)
        q['page_break_before']='yes'
        with self.assertRaises(ValueError):validate_project(p)

    def test_grid_answer_tracking_and_manual_right_column(self):
        project=demo_project()
        q=next(q for q in project['questions'] if q['area']=='mathematics')
        stream=BytesIO();book=object.__new__(Interior)
        book.c=canvas.Canvas(stream);book.project=project;book.resolved=False
        book.open=False;book.page=0;book.area='';book.content_area=True;book.answer_marks=[]
        book.newpage('MATEMÁTICAS',show_area=False,opening_title='MATEMÁTICAS')
        question={**q,'layout':'columns','column_break_before':True,'options_layout':'grid2',
            'options':[{'text':r'\(x_1\)'} for _ in range(4)],'correct':'B'}
        book.question(question,1)
        self.assertEqual(book.col,1)
        self.assertEqual(len(book.answer_marks),1)
        self.assertGreater(book.answer_marks[0]['rect'][0],300)
        book.close()

if __name__=='__main__':unittest.main()
