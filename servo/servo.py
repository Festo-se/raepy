from typing import Type
import time

import pathlib
from raepy.LSS_Library_Python.src import lss

from raepy.LSS_Library_Python.src import lss_const as lssc

from .exceptions import SerialConnectionError

from serial.tools import list_ports
import os


import shelve
shelfdir = os.path.abspath(__file__ + "/../../") +"/shelf"

class Servo(object):
    def __init__(self, CST_LSS_Port="/dev/ttyS0", CST_LSS_Baud = lssc.LSS_DefaultBaud):
        self._CST_LSS_Port = CST_LSS_Port
        self._CST_LSS_Baud = CST_LSS_Baud
        lss.initBus(self._CST_LSS_Port,self._CST_LSS_Baud)
        self._lss = lss.LSS(0)

        shelf = shelve.open(shelfdir)
        self._offset_angle = shelf["Servo_offset"]
        shelf.close()

        self._trial_counter = 0
        self._led_switcher = {
            "black": lssc.LSS_LED_Black,
            "red": lssc.LSS_LED_Red,
            "green": lssc.LSS_LED_Green,
            "blue": lssc.LSS_LED_Blue,
            "yellow": lssc.LSS_LED_Yellow,
            "cyan": lssc.LSS_LED_Cyan,
            "magenta": lssc.LSS_LED_Magenta,
            "white": lssc.LSS_LED_White
        }

        self._motormodes={
            0:'Unknown',
            1:'Limp',
            2:'Free Moving',
            3:'Accelerating',
            4:'Traveling',
            5:'Decelerating',
            6:'Holding',
            7:'Outside limits',
            8:'Stuck',
            9:'Blocked',
            10:'Safe Mode'
        }


    def jog(self,speed, current=700):
        """
        speed paramter is in 1/10 degrees/sec: 3600 is maximum which is 360 deg/sec
        """
        cnt = 0
        self._lss.wheel(speed,current)
        while speed != self.get_target_speed():
            self._lss.wheel(speed)
            time.sleep(0.02)
            cnt+=1
            if cnt > 5:
                raise SerialConnectionError

    def move_absolute_angle(self, angle, current=700):
        """
        Absolute Positioning in 1/10 degree: 500 => 50°
        angle: target angle in 1/10 °
        current: threshold where motor halt and holds
        """

        if abs(self.actual_angle() - angle) < 5:
            return

        self._lss.move(int(angle) - self._offset_angle , current)

        cnt = 0
        while self.get_target_angle() - self._offset_angle != angle:
            self._lss.move(int(angle) + self._offset_angle, current)
            time.sleep(0.02)
            cnt+=1
            if cnt > 5:
                raise SerialConnectionError

        while abs(self.get_target_angle() - self._offset_angle - self.actual_angle()) > 10:
            self._lss.move(int(angle) + self._offset_angle, current)
            time.sleep(0.02)

        

    def move_relative_angle(self, angle, current=1000):
        """
        Relative positioning in 1/10 degree: 500 => 50°
        """
        first_angle = self.actual_angle()
        goal_angle = first_angle + angle
        
        self._lss.moveRelative(int(angle), current)
        diff = abs(self.actual_angle() - goal_angle)

        cnt = 0
        while diff > 30:
            last_diff = diff
            diff = abs(self.actual_angle() - goal_angle)
            time.sleep(0.02)
            if last_diff - diff == 0:
                cnt+=1
            if cnt > 10:
                print("repeat")
                self._lss.moveRelative(int(angle), current)

        

    def actual_current(self):
        """
        returns the motor current in milliAmps
        """
        current = self._lss.getCurrent()
        if current is None:
            return current
        else:
            return int(current)

    def actual_angle(self):
        """
        returns the current angle as 1/10 degree. 360° > 3600
        """
        angle = self._lss.getPosition()
        cnt = 0
        while angle is None:
            angle = self._lss.getPosition()
            cnt += 1
            if cnt > 5:
                raise SerialConnectionError
        return int(angle) - self._offset_angle

    def actual_speed(self):
        """
        returns the current speed in 1/10 °/sec
        """
        speed = self._lss.getSpeed()
        if speed == None:
            return speed
        else:
            return int(speed)

    def actual_LED_color(self):
        """
        returns the current LED Color as String
        """
        color = None
        cnt = 0
        while color == None:
            color = self._lss.getColorLED()
            cnt+=1
            time.sleep(0.02)
            if cnt > 5:
                raise SerialConnectionError
        color = int(color)
        return [color_str for color_str,id in self._led_switcher.items() if id == color][0]

    def hold(self):
        """
        holds the motor with an specific torque in position
        """

        cnt = 0
        self._lss.hold()
        while self.get_motor_mode() != 'Holding':
            self._lss.hold()
            time.sleep(0.01)
            cnt+=1
            if cnt > 5:
                raise SerialConnectionError
        return True

    
    def limp(self):
        """
        Turns holding torque off
        """
        cnt = 0
        self._lss.limp()
        while self.get_motor_mode() != 'Holding':
            self._lss.hold()
            time.sleep(0.01)
            cnt += 1
            if cnt > 5:
                raise SerialConnectionError

    def set_zero_here(self,offset=0):
        """
        Set the zero Position
        """

        self._offset_angle = self.actual_angle() + self._offset_angle

        shelf = shelve.open(shelfdir)
        shelf["Servo_offset"] = self._offset_angle
        shelf.close()

        return True

    def reset_motor(self):
        """
        Reset Motor
        """
        self._lss.reset()

    def get_motor_mode(self):
        """
        Returns the current motor mode
        """
        mode = self._lss.getStatus()
        if mode == None:
            return 'Unknown'

        return self._motormodes.get(int(mode))

    def get_target_angle(self):
        """
        returns target Angle
        """
        cnt = 0
        while True:
            pos = int(self._lss.getTargetPosition())
            if pos != None:
                return pos
            time.sleep(0.02)
            cnt+=1
            if cnt > 10:
                raise SerialConnectionError


    def get_target_speed(self):
        """
        return speed
        """
        return int(self._lss.getTargetSpeed())

    def led_to(self, color):
        colorcode = self._led_switcher.get(color, "invalid color")
        self._lss.setColorLED(colorcode)
        while colorcode != int(self._lss.getColorLED()):
            self.led_to(color)
            time.sleep(0.01)

    def _continue_if_motion_detected(self):
        cnt = 0
        while self.get_motor_mode() != 'Accelerating':
            time.sleep(0.01)
            cnt += 1
            if cnt > 5:
                raise SerialConnectionError