import unittest
from raepy  import rack
from raepy import servo
import time

class TestRack(unittest.TestCase):
    def test_home(self):
        rack.home()
        self.assertAlmostEqual(servo.actual_angle(), 600, delta=50)

    def test_to(self):
        for pos in [0.02, 0.05, 0.07, 0.05, 0.03, 0.01]:
            rack.to(pos)
            self.assertAlmostEqual(rack.position(), pos, delta=0.01)

if __name__ == '__main__':
    unittest.main()