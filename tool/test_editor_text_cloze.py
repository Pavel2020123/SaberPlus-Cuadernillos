import tempfile
import unittest
from pathlib import Path
import pymupdf
from editor_model import new_project, blank_assessment
from editor_pdf import generate, context_flows


class TextClozeTests(unittest.TestCase):
    def test_generic_instructions_use_final_question_numbers(self):
        ctx=dict(id='ctx-numbering',area='english',part=6,title='A journey',
            text='A complete reading.',instructions='En la pregunta {{desde}}, marque A–D.',
            range_heading='RESPONDA LA PREGUNTA {{desde}}')
        flows=context_flows(ctx,[{'id':'q-numbering','slot':''}],{'q-numbering':121})
        text=' '.join(f.getPlainText() for f in flows if hasattr(f,'getPlainText'))
        self.assertIn('En la pregunta 121, marque A–D.',text)
        self.assertNotIn('{{',text)
        self.assertIn('{{desde}}',ctx['instructions'])
        ctx['instructions']=' \n\n'
        flows=context_flows(ctx,[{'id':'q-numbering','slot':''}],{'q-numbering':121})
        text=' '.join(f.getPlainText() for f in flows if hasattr(f,'getPlainText'))
        self.assertNotIn('SIGUIENTE INFORMACIÓN',text)

    def test_four_choice_cloze_keeps_d_and_no_student_highlight(self):
        project = new_project()
        project.update(code='SP-TEST', session='second')
        project['contexts'] = [dict(id='ctx-cloze', area='english', part=7,
            title='A short story', text='It is (0)_____ clear that she {{gap}} the truth.',
            range_heading='PREGUNTAS {{desde}} A {{hasta}}', instructions='Seleccione la palabra.',
            cloze_layout='rows', example_options=['quite','most','more','much'])]
        project['questions'] = [dict(id='q-cloze', area='english', part=7, order=1,
            context='ctx-cloze', slot='gap', layout='full', included=True,
            topic='Grammar', subtopic='Tenses', stem='Choose the word.',
            options=[{'text':v} for v in ['know','knowing','known','knows']],
            correct='D', explanation='The subject she requires knows.',
            assessment=blank_assessment('english'))]
        with tempfile.TemporaryDirectory() as directory:
            generate(project, Path(directory))
            for name, resolved in [('cuadernillo.pdf', False), ('cuadernillo_resuelto.pdf', True)]:
                with pymupdf.open(Path(directory)/name) as doc:
                    page=next(p for p in doc if 'A short story' in p.get_text())
                    text=page.get_text()
                    self.assertIn('PARTE 7', text)
                    self.assertIn('D. knows', text)
                    highlights=[d for d in page.get_drawings() if d.get('fill') and d['fill'][0]>.9 and .8<d['fill'][1]<1 and d['fill'][2]<.6]
                    self.assertEqual(len(highlights), int(resolved))
                    if resolved:
                        self.assertIn('D. knows', page.get_textbox(highlights[0]['rect']))


if __name__ == '__main__':
    unittest.main()
