from raepy import Servo
import math, time
import shelve
import pathlib
import os

shelfdir = os.path.abspath(__file__ + "/../../") + "/shelf"

# Distance from finger joint to midline = 0.035
class RadialGripper(object):
    def __init__(self):
        
        shelf = shelve.open(shelfdir)
        self._fingerlength = shelf["fingerlength"]
        self._zero_offset = shelf["radialgripper_zero_offset"]
        self._mid_axis_offset = shelf["radialgripper_mid_axis_offset"]
        shelf.close()

    def set_fingerlength(self,length):
        self._fingerlength = length
        shelf = shelve.open(shelfdir)
        shelf["fingerlength"] = length
        shelf.close()
        print("raepy : fingerlength set to {} m".format(length))

    def to(self, position, feedback_cb = None):
        """
        30 = i * 10 
        i gear ratio
        10 : because motor accepts 1/10 °. 3600 -> 360°
        """
        Servo.limp()
        goal_angle = 30 * (math.degrees(math.asin(((position/2)-0.035)/self._fingerlength)) + self._mid_axis_offset)
        Servo.move_absolute_angle(int(goal_angle)+self._zero_offset, current=1000)

    def grasp(self, speed=360, current = 900, feedback_cb = None):
        Servo.jog(-speed, current=current)
        time.sleep(0.02)
        while Servo.get_motor_mode() != 'Holding':
            time.sleep(0.01)

    def openfingers(self):
        self.to(0.2)

    def release(self, feedback_cb = None):
        Servo.move_relative_angle(400)
        time.sleep(1)
        Servo.limp()

    def calibrate(self, feedback_cb = None):
        if self._fingerlength == None:
            print("raepy: set fingerlength before calling calibrating the gripper")
            return
        Servo.jog(-50)
        while Servo.actual_current() < 550:
            time.sleep(0.01)
        Servo.limp()
        time.sleep(1)
        #Servo.set_zero_here()
        shelf = shelve.open(shelfdir)
        self._zero_offset = Servo.actual_angle()
        shelf["radialgripper_zero_offset"] = self._zero_offset

        self._mid_axis_offset = math.degrees(math.asin(0.035/self._fingerlength))
        shelf["radialgripper_mid_axis_offset"] = self._mid_axis_offset
        shelf.close()
        print("raepy : offset angle set to {} deg".format(self._mid_axis_offset))

    def fingertip_distance(self):
        """
        returns fingertip distance in meter
        """
        return 2*math.sin(math.radians((Servo.actual_angle()-self._zero_offset)/30)* self._fingerlength)

