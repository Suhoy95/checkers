import unittest
import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))

from checkers import hacks_steps, field


class StepTest(unittest.TestCase):
    def test_eq(self):
        steps = [
            ((2, 2), (1, 1)),
            ((1, 1), (2, 2), [((3, 3), field.white_check)]),
            ((2, 2), (1, 1), [((3, 3), field.white_check)]),
            ((1, 1), (2, 2), [], True),
            ((2, 2), (1, 1), [], True),
            ((1, 1), (2, 2), [((3, 3), field.white_check)], True),
            ((2, 2), (1, 1), [((3, 3), field.white_check)], True),
        ]
        s = hacks_steps.Step((1, 1), (2, 2))
        s2 = hacks_steps.Step((1, 1), (2, 2))
        self.assertEqual(s, s2)
        for i in steps:
            self.assertNotEqual(s, hacks_steps.Step(*i))


class NodeTest(unittest.TestCase):
    def test_init(self):
        n = hacks_steps.Node((1, 2))

        self.assertTupleEqual(n.coords, (1, 2))        

    def test_add_child(self):
        n = hacks_steps.Node((1, 2))

        n.add_child(1)
        self.assertListEqual([1], n.childs)

        n.add_child(2)
        self.assertListEqual([1, 2], n.childs)

    def test_add_parrent(self):
        n = hacks_steps.Node((1, 2))

        n.add_parrent(1)
        self.assertEqual(n.parrent, 1)

    def test_eq(self):
        n = hacks_steps.Node((1, 2))
        n2 = hacks_steps.Node((1, 2))
        n3 = hacks_steps.Node((1, 3))

        self.assertEqual(n, n2)
        self.assertNotEqual(n, n3)

        n.add_parrent(1)
        n2.add_parrent(1)
        self.assertEqual(n, n2)        

        n.add_child(1)
        n2.add_child(1)
        self.assertEqual(n, n2)

        n.add_child(3)
        n2.add_child(2)
        self.assertNotEqual(n, n2)

        n.add_child(2)
        n2.add_child(3)
        self.assertEqual(n, n2)

        n2.add_child(3)
        self.assertEqual(n, n2)

        n.add_child(4)
        self.assertNotEqual(n, n2)

        n.add_parrent(1)
        n2.add_parrent(2)
        n2.add_child(4)
        self.assertNotEqual(n, n2)


class HacksTreeTest(unittest.TestCase):
    def test_add(self):
        t = hacks_steps.HacksTree()
        num = t.add((1, 2))
        self.assertEqual(num, 0)
        self.assertListEqual(t._nodes, [hacks_steps.Node((1, 2))])

        num = t.add((1, 3))
        self.assertEqual(num, 1)
        self.assertListEqual(t._nodes, [hacks_steps.Node((1, 2)), hacks_steps.Node((1, 3))])

    def test_get(self):
        t = hacks_steps.HacksTree()
        t.add((1, 2))
        t.add((1, 3))

        self.assertEqual(t.get(0), hacks_steps.Node((1, 2)))

    def test_get_bad(self):
        t = hacks_steps.HacksTree()
        t.add((1, 2))
        t.add((1, 3))

        with self.assertRaises(ValueError):
            t.get(-1)
        with self.assertRaises(ValueError):
            t.get(2)

    def test_incident(self):
        t = hacks_steps.HacksTree()


class GettersTest(unittest.TestCase):
    def test_get_cur_hacks(self):
        f = field.Field(empty=True)

        f.add_check((3, 8), field.black_check)
        f.add_check((2, 7), field.white_check)
        f.add_check((4, 7), field.white_check)
        hacks = set(hacks_steps._get_cur_hacks(f, field.black_check, (3, 8)))
        self.assertSetEqual(hacks, {(1, 6), (5, 6)})

        f.add_check((1, 8), field.black_check)
        hacks = set(hacks_steps._get_cur_hacks(f, field.black_check, (1, 8)))
        self.assertSetEqual(hacks, {(3, 6)})

        f.add_check((3, 6), field.black_check)
        f.add_check((2, 5), field.white_check)
        f.add_check((4, 5), field.white_check)
        f.del_check((1, 8))
        hacks = set(hacks_steps._get_cur_hacks(f, field.black_check, (3, 6)))
        self.assertSetEqual(hacks, {(1, 8), (5, 8), (1, 4), (5, 4)})

    def test_get_hacks(self):
        f = field.Field(empty=True)


if __name__ == '__main__':
    unittest.main()
