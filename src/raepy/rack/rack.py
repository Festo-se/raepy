
import time

class Rack(object):
    def __init__(self,Servo):
        self._servo = Servo

    def to(self,position):
        """
        position in meter. Constant 82644 is calculated by (43,56[mm/360°] => 0.121 [mm/°] => 8.2644 [°/mm] => 8264,46 [°/m]  * 10 => 82644 * (1/10°)/m
        """
        self._servo.move_absolute_angle(int(position*82644))
    
    def position(self):
        return self._servo.actual_angle()/82644

    def out(self):
        self.to(0.09)

    def home(self, feedback_cb=None):
        self._servo.jog(-50)
        cnt = 0
        while self._servo.actual_current() < 700:
            time.sleep(0.02)
            cnt+=1
            if cnt > 1000:
                return "No Rack inserted"

        self._servo.set_zero_here()
        self._servo.move_relative_angle(600)
        time.sleep(1)
    

