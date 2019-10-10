from unittest import TestCase

from src.python.Poststorm_Imagery.resizer.generate import resize_image


class TestGenerate(TestCase):
    def test_output(self):
        resize_image(path=os.path.abspath('./resizer/input'),
                     output_path=os.path.abspath('./resizer/output'),
                     scale=0.15,
                     debug=True)
        self.assertEqual(True, False)
