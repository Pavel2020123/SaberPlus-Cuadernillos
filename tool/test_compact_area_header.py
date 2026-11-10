"""Header pagination regression checks using an in-memory PDF only."""
from io import BytesIO
import unittest
import pymupdf
from reportlab.pdfgen import canvas
from editor_pdf import Interior
from editor_model import AREAS

class CompactAreaHeaderTests(unittest.TestCase):
    def test_every_area_title_only_on_opening_page(self):
        for area in AREAS.values():
            with self.subTest(area=area):
                data=BytesIO()
                book=object.__new__(Interior)
                book.c=canvas.Canvas(data)
                book.project={'code':'SP-001','session':'first'}
                book.resolved=False;book.open=False;book.page=0
                book.area='';book.content_area=True
                book.newpage(area.upper(),show_area=False,opening_title=area.upper())
                book.newpage()
                book.close()
                with pymupdf.open(stream=data.getvalue(),filetype='pdf') as doc:
                    self.assertEqual(doc[0].get_text().count(area.upper()),1)
                    self.assertNotIn(area.upper(),doc[1].get_text())
                    title=next(b for b in doc[0].get_text('blocks') if area.upper() in b[4])
                    self.assertLess(title[3],45)

if __name__=='__main__':unittest.main()
