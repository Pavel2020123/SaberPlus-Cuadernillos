"""Image fitting with real raster sizes; all files are isolated temporary fixtures."""
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from PIL import Image
from editor_pdf import picture


class ImageSizeTests(unittest.TestCase):
    def test_dimensions_preserve_ratio_fit_limits_and_never_upscale(self):
        sizes = [(1200,320),(600,600),(360,1000),(40,20),(4000,300),(300,4000)]
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root/'assets/uploads').mkdir(parents=True)
            with patch('editor_pdf.ROOT',root):
                for index,(width,height) in enumerate(sizes):
                    with self.subTest(size=(width,height)):
                        path = f'assets/uploads/{index:032x}.png'
                        Image.new('RGB',(width,height),'white').save(root/path)
                        result = picture(path,230,190)
                        self.assertAlmostEqual(result.drawWidth/result.drawHeight,width/height)
                        # Floating-point scaling can exceed an exact bound by ~1e-14 pt.
                        self.assertLessEqual(result.drawWidth,min(width,230)+1e-9)
                        self.assertLessEqual(result.drawHeight,min(height,190)+1e-9)

    def test_missing_resource_and_external_path_are_rejected(self):
        with tempfile.TemporaryDirectory() as folder,patch('editor_pdf.ROOT',Path(folder)):
            for path in ('assets/uploads/missing.png','../external.png'):
                with self.subTest(path=path),self.assertRaisesRegex(ValueError,'No se encuentra'):
                    picture(path,230)


if __name__ == '__main__':
    unittest.main()
