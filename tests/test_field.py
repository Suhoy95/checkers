import unittest
import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))

from checkers.field import Field, Check, Colors

class FieldTest(unittest.TestCase):
    def test__init__field(self):
        f = Field()
        self.assertEqual(f.get_check((1, 2)), Check(Colors.BLACK))
        self.assertEqual(f.get_check((2, 7)), Check(Colors.WHITE))

    def test_get_checks_of_this_color(self):
        f = Field()

    def test_move_check(self):
        f = Field()

        f.move_check((1, 4), (2, 5))
        self.assertEqual(f.get_check((2, 5)), Check(Colors.BLACK))
        with self.assertRaises(ValueError):
            f.get_check((1, 4))

    def test_move_check_bad(self):
        f = Field()

if __name__ == '__main__':
    unittest.main()