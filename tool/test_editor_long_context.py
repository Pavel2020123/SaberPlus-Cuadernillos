"""Long shared readings keep every line and their group when paginated."""
import copy
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock

import pymupdf
from reportlab.platypus import Spacer, Flowable
from editor_model import demo_project, validate_project
from editor_pdf import generate, Interior, H, BOTTOM


class LongContextTests(unittest.TestCase):
    def test_all_lines_and_source_survive_across_pages_without_mutation(self):
        project=demo_project()
        question=next(q for q in project['questions'] if q['area']=='reading')
        question.update(context='long-reading', order=1, layout='columns')
        project['questions']=[question]
        lines=[f'Renglon{i:03}: contenido completo de la lectura compartida.' for i in range(125)]
        project['contexts']=[dict(id='long-reading',area='reading',part=0,
            title='Texto extenso',text='\n'.join(lines),source='Credito conservado al final.')]
        before=copy.deepcopy(project)
        with tempfile.TemporaryDirectory() as folder:
            result=generate(project,folder)
            with pymupdf.open(Path(folder)/'cuadernillo.pdf') as doc:
                text=''.join(p.get_text() for p in doc)
                self.assertIn('CONTINUACIÓN DE LA LECTURA',text)
                for line in lines:self.assertEqual(text.count(line),1,line)
                self.assertEqual(text.count('Credito conservado al final.'),1)
                page=doc[result['page_map'][question['id']]-1]
                self.assertIn(question['stem'].splitlines()[0],page.get_text())
        self.assertEqual(project,before)

    def test_indivisible_resource_still_fails_instead_of_looping_or_clipping(self):
        class TallResource(Flowable):
            def wrap(self,w,h):return w,H
        book=Interior.__new__(Interior)
        book.question_height=Mock(return_value=100)
        book.full=Mock();book.newpage=Mock()
        with self.assertRaisesRegex(ValueError,'indivisible'):
            book.shared_context([TallResource()],{'id':'q'},1)

    def test_full_width_accepts_tall_figure_but_columns_and_excess_do_not(self):
        project=demo_project()
        q=next(q for q in project['questions'] if q['area']=='mathematics')
        q.update(layout='full',image_height=365)
        validate_project(project)
        q['layout']='columns'
        with self.assertRaisesRegex(ValueError,'altura'):validate_project(project)
        q.update(layout='full',image_height=401)
        with self.assertRaisesRegex(ValueError,'altura'):validate_project(project)


if __name__=='__main__':unittest.main()
