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
            ((1, 1), (2, 2), [((3, 3), field.white_check)])
        ]
        s = hacks_steps.Step((1, 1), (2, 2))
        for i in steps:
            self.assertNotEqual(s, hacks_steps.Step(*i))

    def test_do(self):
        f = field.Field()
        step = hacks_steps.Step((1, 4), (2, 5))
        step.do(f)
        self.assertEqual(f.get_check((1, 4)), -1)
        self.assertEqual(f.get_check((2, 5)), field.black_check)

if __name__ == '__main__':
    unittest.main()
