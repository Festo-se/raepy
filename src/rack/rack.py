from raepy import Servo
import time

class Rack(object):
    def __init__(self):
        pass

    def to(self,position):
        """
        position in meter. Constant 82644 is calculated by (43,56[mm/360°] => 0.121 [mm/°] => 8.2644 [°/mm] => 8264,46 [°/m]  * 10 => 82644 * (1/10°)/m
        """
        Servo.move_absolute_angle(int(position*82644))
    
    def position(self):
        return Servo.actual_angle()/82644

    def out(self):
        self.to(0.08)

    def home(self, feedback_cb=None):
        Servo.jog(-50)
        cnt = 0
        while Servo.actual_current() < 700:
            time.sleep(0.02)
            print(cnt)
            cnt+=1
            if cnt > 1000:
                return "No Rack inserted"

        Servo.set_zero_here()
        Servo.move_relative_angle(600)
        time.sleep(1)
    

