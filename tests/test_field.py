import unittest
import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))

from checkers import field

class FieldTest(unittest.TestCase):
    def test_generate_start_pos(self):
        pass

    def test__init__field(self):
        f = field.Field()

        self.assertEqual(len(f._checks), 40)

    def test_get_checks_of_this_color(self):
        f = field.Field()

        self.assertEqual(len(list(f.get_checks_of_this_color(field.Colors.WHITE))), 20)
        self.assertEqual(len(list(f.get_checks_of_this_color(field.Colors.BLACK))), 20)

        for i in f.get_checks_of_this_color(field.Colors.WHITE):
            self.assertEqual(i, field.white_check)
        for i in f.get_checks_of_this_color(field.Colors.BLACK):
            self.assertEqual(i, field.black_check)

    def test_get_checks_of_this_color_bad(self):
        f = field.Field()

        with self.assertRaises(ValueError):
            f.get_checks_of_this_color(4)

    def test_check_coords(self):
        for c in [(0, 1, 2), (0, 1), (1, 0), (0, 0), (11, 1), (1, 11), (11, 11)]:
            self.assertFalse(field.Field.check_coords(c))

        for c in [(2, 4), (1, 1), (10, 10), (1, 10), (10, 1)]:
            self.assertTrue(field.Field.check_coords(c))

    def test_get_check(self):
        f = field.Field()

        self.assertEqual(f.get_check((1, 2)), field.black_check)
        self.assertEqual(f.get_check((2, 7)), field.white_check)
        self.assertEqual(f.get_check((1, 1)), -1)

    def test_get_check_bad(self):
        f = field.Field()

        for c in [(0, 1, 2), (0, 1), (1, 0), (0, 0), (11, 1), (1, 11), (11, 11)]:    
            with self.assertRaises(ValueError):
                f.get_check(c)

    def test_move_check(self):
        f = field.Field()

        f.move_check((1, 4), (2, 5))
        self.assertEqual(f.get_check((2, 5)), field.black_check)
        self.assertEqual(f.get_check((1, 4)), -1)

    def test_update_check(self):
        f = field.Field()

        f.update_check((1, 2))
        self.assertEqual(f.get_check((1, 2)), field.black_queen)
        f.update_check((1, 2))
        self.assertEqual(f.get_check((1, 2)), field.black_check)
        f.update_check((1, 8))
        self.assertEqual(f.get_check((1, 8)), field.white_queen)
        f.update_check((1, 8))
        self.assertEqual(f.get_check((1, 8)), field.white_check)

    def test_update_check_bad(self):
        pass

    def test_move_check_bad(self):
        f = field.Field()

        with self.assertRaises(ValueError):
            f.move_check((1, 1), (5, 5))
        with self.assertRaises(ValueError):
            f.move_check((1, 1), (4, 4, 4))
        with self.assertRaises(ValueError):
            f.move_check((1, 2), (2, 3))

    def test_del_check(self):
        f = field.Field()

        f.del_check((2, 1))
        self.assertEqual(f.get_check((2, 1)), -1)
        f.del_check((1, 10))
        self.assertEqual(f.get_check((1, 10)), -1)

    def test_del_check_bad(self):
        f = field.Field()

        with self.assertRaises(ValueError):
            f.del_check((5, 5))

    def test_add_check(self):
        f = field.Field()

        f.add_check((5, 5), field.white_check)
        self.assertEqual(f.get_check((5, 5)), field.white_check)
        f.add_check((6, 6), field.black_check)
        self.assertEqual(f.get_check((6, 6)), field.black_check)

    def test_add_check_bad(self):
        f = field.Field()

        with self.assertRaises(ValueError):
            f.add_check((1, 2), field.white_check)
        with self.assertRaises(ValueError):
            f.add_check((1, 2), field.black_check)
        with self.assertRaises(TypeError):
            f.add_check((5, 5), [])

if __name__ == '__main__':
    unittest.main()
