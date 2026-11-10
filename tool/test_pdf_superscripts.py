import unittest
from editor_pdf import para

class SuperscriptTests(unittest.TestCase):
    def test_exponent_is_raised_and_minus_supported(self):
        p=para('G = 2ⁿ⁻¹')
        self.assertIn('<super><i>n</i>-1</super>',p.text)
        self.assertTrue(any(getattr(f,'rise',0)>0 for f in p.frags))

    def test_user_markup_stays_escaped(self):
        self.assertIn('&lt;super&gt;',para('<super>2</super>').text)

    def test_all_supported_characters(self):
        self.assertIn('<super>0123456789<i>n</i><i>i</i>+-=()</super>',para('⁰¹²³⁴⁵⁶⁷⁸⁹ⁿⁱ⁺⁻⁼⁽⁾').text)

    def test_equation_font_and_variables(self):
        p=para('D. G = 2ⁿ⁻¹')
        self.assertEqual(p.style.fontName,'Times-Roman')
        self.assertIn('<i>G</i>',p.text)
        self.assertTrue(any(getattr(f,'fontName','')=='Times-Italic' for f in p.frags))

    def test_prose_keeps_regular_font(self):
        self.assertEqual(para('G representa los granos de trigo.').style.fontName,'Helvetica')

if __name__=='__main__':unittest.main()
