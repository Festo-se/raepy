import unittest

from raepy import Servo
import time

class TestServomotor(unittest.TestCase):
    def test_set_zero(self):
        Servo.move_absolute_angle(5000)
        Servo.set_zero_here()
        self.assertAlmostEqual(Servo.actual_angle(),0,delta=20)

        Servo.move_absolute_angle(5000)
        Servo.set_zero_here()
        self.assertAlmostEqual(Servo.actual_angle(),0,delta=20)

        Servo.move_absolute_angle(-10000)
        Servo.set_zero_here()
        self.assertAlmostEqual(Servo.actual_angle(),0,delta=20)


    def test_move_absolute(self):
        Servo.set_zero_here()
        Servo.move_absolute_angle(1000)
        self.assertAlmostEqual(Servo.actual_angle(),1000,delta=20)

        Servo.move_absolute_angle(0)
        self.assertAlmostEqual(Servo.actual_angle(),0,delta=20)

        Servo.move_absolute_angle(1000)
        self.assertAlmostEqual(Servo.actual_angle(),1000,delta=20)

        Servo.move_absolute_angle(0)
        self.assertAlmostEqual(Servo.actual_angle(),0,delta=20)

    def test_move_relative(self):
        Servo.set_zero_here()
        Servo.move_relative_angle(1000)
        self.assertAlmostEqual(Servo.actual_angle(),1000,delta=20)

        Servo.move_relative_angle(-1000)
        self.assertAlmostEqual(Servo.actual_angle(),0,delta=20)



if __name__ == '__main__':
    unittest.main()