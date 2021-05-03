
import math, time
import shelve
import pathlib
import os



# Distance from finger joint to midline = 0.035
class RadialGripper(object):
    def __init__(self,mutex,Servo):
        self._servo = Servo
        self._shelfdir = os.path.abspath(__file__ + "/../../") + "/shelf"
        self._mutex = mutex
        self._init_shelf()


    def _init_shelf(self):
        self._mutex.acquire()
        shelf = shelve.open(self._shelfdir)
        if "fingerlength" in shelf:
            self._fingerlength = shelf["fingerlength"]
        else:
            shelf["fingerlength"] = 0.1
        
        if "radialgripper_zero_offset" in shelf:
            self._zero_offset = shelf["radialgripper_zero_offset"]
        else:
            shelf["radialgripper_zero_offset"] = 50
        
        if "radialgripper_mid_axis_offset" in shelf:
            self._mid_axis_offset = shelf["radialgripper_mid_axis_offset"]
        else:
            shelf["radialgripper_mid_axis_offset"] = 20
        shelf.close()
        self._mutex.release()


    def set_fingerlength(self,length):
        self._fingerlength = length
        shelf = shelve.open(self._shelfdir)
        shelf["fingerlength"] = length
        shelf.close()
        print("raepy : fingerlength set to {} m".format(length))

    def to(self, position, feedback_cb = None):
        """
        30 = i * 10 
        i gear ratio
        10 : because motor accepts 1/10 °. 3600 -> 360°
        """
        self._servo.limp()
        goal_angle = 30 * (math.degrees(math.asin(((position/2)-0.035)/self._fingerlength)) + self._mid_axis_offset)
        self._servo.move_absolute_angle(int(goal_angle)+self._zero_offset, current=1000)

    def grasp(self, speed=360, current = 900, feedback_cb = None):
        self._servo.jog(-speed, current=current)
        time.sleep(0.02)
        while self._servo.get_motor_mode() != 'Holding':
            time.sleep(0.01)

    def openfingers(self):
        self.to(0.2)

    def release(self, feedback_cb = None):
        self._servo.move_relative_angle(400)
        time.sleep(1)
        self._servo.limp()

    def calibrate(self, feedback_cb = None):
        if self._fingerlength == None:
            print("raepy: set fingerlength before calling calibrating the gripper")
            return
        self._servo.jog(-50)
        while Servo.actual_current() < 550:
            time.sleep(0.01)
        self._servo.limp()
        time.sleep(1)
        #Servo.set_zero_here()
        self._mutex.acquire()
        shelf = shelve.open(self._shelfdir)
        self._zero_offset = self._servo.actual_angle()
        shelf["radialgripper_zero_offset"] = self._zero_offset

        self._mid_axis_offset = math.degrees(math.asin(0.035/self._fingerlength))
        shelf["radialgripper_mid_axis_offset"] = self._mid_axis_offset
        shelf.close()
        self._mutex.release()
        print("raepy : offset angle set to {} deg".format(self._mid_axis_offset))

    def fingertip_distance(self):
        """
        returns fingertip distance in meter
        """
        return 2*math.sin(math.radians((self._servo.actual_angle()-self._zero_offset)/30)*self._fingerlength)

