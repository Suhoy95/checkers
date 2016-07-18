import unittest
import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))

from checkers import field

class FieldTest(unittest.TestCase):
    def test__init__field(self):
        f = field.Field()

        self.assertEqual(len(f._checks), 40)
        self.assertEqual(len(f._lighting_cells), 0)

    def test_get_checks_of_this_color(self):
        f = field.Field()

        self.assertEqual(len(list(f.get_checks_of_this_color(field.Colors.WHITE))), 20)
        self.assertEqual(len(list(f.get_checks_of_this_color(field.Colors.BLACK))), 20)

        for i in f.get_checks_of_this_color(field.Colors.WHITE):
            self.assertEqual(i, field.white_check)
        for i in f.get_checks_of_this_color(field.Colors.BLACK):
            self.assertEqual(i, field.black_check)

    def test_check_coords(self):
        f = field.Field()

        self.assertFalse(f._check_coords((0, 1, 2)))
        self.assertFalse(f._check_coords((0, 1)))
        self.assertFalse(f._check_coords((1, 0)))
        self.assertFalse(f._check_coords((0, 0)))

        self.assertTrue(f._check_coords((2, 4)))
        self.assertTrue(f._check_coords((1, 1)))
        self.assertTrue(f._check_coords((10, 10)))
        self.assertTrue(f._check_coords((1, 10)))
        self.assertTrue(f._check_coords((10, 1)))

    def test_get_check(self):
        f = field.Field()

        self.assertEqual(f.get_check((1, 2)), field.black_check)
        self.assertEqual(f.get_check((2, 7)), field.white_check)
        self.assertEqual(f.get_check((1, 1)), -1)

    def test_get_check_bad(self):
        f = field.Field()

        with self.assertRaises(ValueError):
            f.get_check((0, 1))
        with self.assertRaises(ValueError):
            f.get_check((1, 0))
        with self.assertRaises(ValueError):
            f.get_check((1, 2, 3))

    def test_move_check(self):
        f = field.Field()

        f.move_check((1, 4), (2, 5))
        self.assertEqual(f.get_check((2, 5)), field.black_check)
        self.assertEqual(f.get_check((1, 4)), -1)

    def test_move_check_bad(self):
        f = field.Field()

        with self.assertRaises(ValueError):
            f.move_check((1, 1), (5, 5))
        with self.assertRaises(ValueError):
            f.move_check((1, 1), (4, 4, 4))
        with self.assertRaises(ValueError):
            f.move_check((1, 2), (2, 3))

if __name__ == '__main__':
    unittest.main()