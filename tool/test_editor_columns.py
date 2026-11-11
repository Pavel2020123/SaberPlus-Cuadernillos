import unittest
from io import BytesIO
import pymupdf
from reportlab.pdfgen import canvas
from editor_model import demo_project
from editor_pdf import Interior,W,H,M,WIDTH,context_flows
from column_planner import column_chunk

class ColumnPlannerTests(unittest.TestCase):
    def test_shared_reading_left_questions_right(self):
        project=demo_project()
        base=next(q for q in project['questions'] if q['area']=='mathematics')
        stream=BytesIO();book=object.__new__(Interior)
        book.c=canvas.Canvas(stream,pagesize=(W,H));book.project=project
        book.open=False;book.page=2;book.area='';book.content_area=True
        book.resolved=False;book.answer_marks=[]
        book.newpage('LECTURA CRITICA',show_area=False)
        q={**base,'id':'side-q','layout':'columns','introduction':'','image':None,
           'stem':'Pregunta sobre el texto', 'options':[{'text':str(k)} for k in range(4)],
           'correct':'C','context':'side-context'}
        ctx={'range_heading':'RESPONDA LAS PREGUNTAS {{desde}} A {{hasta}}',
             'title':'Lectura de prueba','text':'Un texto compartido. '*70}
        book.side_context(context_flows(ctx,[q],{'side-q':1},column=True),q,1)
        book.question(q,1)
        self.assertEqual(book.page,3)
        self.assertEqual(len(book.answer_marks),1)
        self.assertGreater(book.answer_marks[0]['rect'][0],W/2)
        book.close()
        with pymupdf.open(stream=stream.getvalue(),filetype='pdf') as doc:
            page=doc[0]
            words=page.get_text('words')
            self.assertLess(next(w[0] for w in words if w[4]=='Lectura'),W/2)
            self.assertGreater(next(w[0] for w in words if w[4]=='Pregunta'),W/2)

    def test_two_columns_below_wide(self):
        self.assertEqual(column_chunk([180,220],250),(2,1,180,220))

    def test_contiguous_balanced_prefix(self):
        self.assertEqual(column_chunk([100,100,180,300],250),(3,2,210,180))

    def test_oversized_first_does_not_skip(self):
        self.assertIsNone(column_chunk([800,50],700))

    def test_empty(self):
        self.assertIsNone(column_chunk([],700))

    def test_gap_counts_only_between_items(self):
        self.assertEqual(column_chunk([100,100,100,100],210),(4,2,210,210))

    def test_wide_then_balanced_columns_then_wide(self):
        project=demo_project()
        base=next(q for q in project['questions'] if q['area']=='mathematics')
        stream=BytesIO();book=object.__new__(Interior)
        book.c=canvas.Canvas(stream,pagesize=(W,H));book.project=project
        book.open=False;book.page=2;book.area='';book.content_area=True
        book.resolved=False;book.answer_marks=[]
        book.newpage('MATEMATICAS',show_area=False)
        def item(i,layout):
            return {**base,'id':str(i),'layout':layout,'introduction':'',
                    'image':None,'stem':'Pregunta de prueba '+str(i),
                    'options':[{'text':str(k)} for k in range(4)],'correct':'C',
                    'context':None}
        book.question(item(1,'full'),1)
        top=book.flush()
        mapping=book.column_group([item(2,'columns'),item(3,'columns')],{'2':2,'3':3})
        bottom=book.flush()
        self.assertEqual(mapping,{'2':3,'3':3})
        self.assertEqual(len(book.answer_marks),3)
        self.assertLess(book.answer_marks[1]['rect'][0],W/2)
        self.assertGreater(book.answer_marks[2]['rect'][0],W/2)
        book.question(item(4,'full'),4)
        self.assertEqual(book.page,3)
        book.close()
        with pymupdf.open(stream=stream.getvalue(),filetype='pdf') as doc:
            lines=[d['rect'] for d in doc[0].get_drawings() if d['rect'].width<1 and abs(d['rect'].x0-W/2)<1]
            self.assertEqual(len(lines),1)
            self.assertAlmostEqual(lines[0].y0,H-top,places=2)
            self.assertAlmostEqual(lines[0].y1,H-(bottom+10),places=2)
            text=doc[0].get_text()
            self.assertLess(text.index('prueba 2'),text.index('prueba 3'))

if __name__=='__main__':
    unittest.main()
