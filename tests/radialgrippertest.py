import unittest
from raepy import RadialGripper as gripper
import time

class TestRadialGripper(unittest.TestCase):

    def test_set_fingerlength(self):
        print("test_set_fingerlength")
        gripper.set_fingerlength(0.1)
        self.assertEqual(0.1, gripper._fingerlength)

    def test_calibrate(self):
        print("test_calibrate")
        gripper.set_fingerlength(0.1)
        gripper.calibrate()
        self.assertAlmostEqual(gripper.fingertip_distance(),0.0,delta=0.05)


    def test_to(self):
        print("test_to")
        gripper.to(0.1)
        self.assertAlmostEqual(gripper.fingertip_distance(),0.1,delta=0.02)
        gripper.to(0.2)
        self.assertAlmostEqual(gripper.fingertip_distance(),0.2,delta=0.02)
        gripper.to(0.1)
        self.assertAlmostEqual(gripper.fingertip_distance(),0.1,delta=0.02)
    
    def test_grasp(self):
        print("test_grasp")
        gripper.to(0.2)
        time.sleep(1)
        gripper.grasp()
        self.assertAlmostEqual(gripper.fingertip_distance(),0.0,delta=0.05)
        time.sleep(1)

class TestRack(unittest.TestCase):
    pass

if __name__ == '__main__':
    unittest.main()