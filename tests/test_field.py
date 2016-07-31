import unittest
import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))

from checkers import field, hacks_steps


class FieldTest(unittest.TestCase):
    def test_generate_start_pos(self):
        coords_of_checks = [
            (2, 1), (4, 1), (6, 1), (8, 1), (10, 1),
            (1, 2), (3, 2), (5, 2), (7, 2), (9, 2),
            (2, 3), (4, 3), (6, 3), (8, 3), (10, 3),
            (1, 4), (3, 4), (5, 4), (7, 4), (9, 4),
            (2, 7), (4, 7), (6, 7), (8, 7), (10, 7),
            (1, 8), (3, 8), (5, 8), (7, 8), (9, 8),
            (2, 9), (4, 9), (6, 9), (8, 9), (10, 9),
            (1, 10), (3, 10), (5, 10), (7, 10), (9, 10)
        ]

        checks_for_start_pos = [
            (field.white_check, field.black_check),
            (field.black_check, field.white_check)
        ]

        for c in checks_for_start_pos:
            checks = field.Field.generate_start_pos(*c)

            for i in coords_of_checks[:20]:
                self.assertEqual(checks[i], c[1])

            for i in coords_of_checks[20:]:
                self.assertEqual(checks[i], c[0])

            self.assertListEqual(list(checks.keys()), coords_of_checks)

    def test__init__field(self):
        f = field.Field()

        self.assertEqual(len(f._checks), 40)

    def test_get_checks_of_this_color(self):
        coords_of_checks = [
            (2, 1), (4, 1), (6, 1), (8, 1), (10, 1),
            (1, 2), (3, 2), (5, 2), (7, 2), (9, 2),
            (2, 3), (4, 3), (6, 3), (8, 3), (10, 3),
            (1, 4), (3, 4), (5, 4), (7, 4), (9, 4),
            (2, 7), (4, 7), (6, 7), (8, 7), (10, 7),
            (1, 8), (3, 8), (5, 8), (7, 8), (9, 8),
            (2, 9), (4, 9), (6, 9), (8, 9), (10, 9),
            (1, 10), (3, 10), (5, 10), (7, 10), (9, 10)
        ]
        f = field.Field()

        white_checks = list(f.get_checks_of_this_color(field.Colors.WHITE))
        black_checks = list(f.get_checks_of_this_color(field.Colors.BLACK))

        self.assertListEqual(black_checks, coords_of_checks[:20])
        self.assertListEqual(white_checks, coords_of_checks[20:])

    def test_get_checks_of_this_color_bad(self):
        f = field.Field()

        with self.assertRaises(ValueError):
            f.get_checks_of_this_color(4)

    def test_get_check(self):
        f = field.Field()

        self.assertEqual(f.get_check((1, 2)), field.black_check)
        self.assertEqual(f.get_check((2, 7)), field.white_check)
        self.assertEqual(f.get_check((1, 1)), -1)

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
            f.move_check((1, 2), (2, 1))
        with self.assertRaises(ValueError):
            f.move_check((1, 1), (2, 1))

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
        f = field.Field()

        with self.assertRaises(ValueError):
            f.update_check((5, 5))

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

    def test_do_step(self):
        f = field.Field()
        step = hacks_steps.Step((1, 4), (2, 5))
        f.do_step(step)
        self.assertEqual(f.get_check((1, 4)), -1)
        self.assertEqual(f.get_check((2, 5)), field.black_check)

        f = field.Field()
        step = hacks_steps.Step((1, 4), (2, 5), [((2, 1), field.black_check), ((2, 7), field.white_check)])
        f.do_step(step)
        self.assertEqual(f.get_check((1, 4)), -1)
        self.assertEqual(f.get_check((2, 5)), field.black_check)
        self.assertEqual(f.get_check((2, 1)), -1)
        self.assertEqual(f.get_check((2, 7)), -1)

        f = field.Field()
        step = hacks_steps.Step((1, 4), (2, 5), is_become_queen=True)
        f.do_step(step)
        self.assertEqual(f.get_check((1, 4)), -1)
        self.assertEqual(f.get_check((2, 5)), field.black_queen)

        f = field.Field()
        step = hacks_steps.Step((1, 4), (2, 5), [((2, 1), field.black_check), ((2, 7), field.white_check)], is_become_queen=True)
        f.do_step(step)
        self.assertEqual(f.get_check((1, 4)), -1)
        self.assertEqual(f.get_check((2, 5)), field.black_queen)
        self.assertEqual(f.get_check((2, 1)), -1)
        self.assertEqual(f.get_check((2, 7)), -1)

    def test_undo(self):
        start_field = field.Field()

        f = field.Field()
        step = hacks_steps.Step((1, 4), (2, 5))
        f.do_step(step)
        f.undo_step(step)
        self.assertEqual(f, start_field)

        f = field.Field()
        step = hacks_steps.Step((1, 4), (2, 5), [((2, 1), field.black_check), ((2, 7), field.white_check)])
        f.do_step(step)
        f.undo_step(step)
        self.assertEqual(f, start_field)

        f = field.Field()
        step = hacks_steps.Step((1, 4), (2, 5), is_become_queen=True)
        f.do_step(step)
        f.undo_step(step)
        self.assertEqual(f, start_field)

        f = field.Field()
        step = hacks_steps.Step((1, 4), (2, 5), [((2, 1), field.black_check), ((2, 7), field.white_check)], is_become_queen=True)
        f.do_step(step)
        f.undo_step(step)
        self.assertEqual(f, start_field)

    def test_eq(self):
        f1 = field.Field()
        f2 = field.Field()
        self.assertEqual(f1, f2)

        f1.add_check((5, 5), field.white_check)
        f2.add_check((5, 5), field.white_check)
        self.assertEqual(f1, f2)

        f1.del_check((5, 5))
        f2.del_check((5, 5))

        f1.add_check((5, 5), field.white_check)
        f2.add_check((5, 5), field.black_check)
        self.assertNotEqual(f1, f2)

        f1.del_check((5, 5))
        f2.del_check((5, 5))

        f1.add_check((5, 5), field.white_check)
        self.assertNotEqual(f1, f2)


if __name__ == '__main__':
    unittest.main()
