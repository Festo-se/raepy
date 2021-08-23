
import time
from ..utils.singleton import Singleton
from ..servo.servo import Servo


class Rack(object):
    __metaclass__ = Singleton
    def __init__(self):
        self._servo = Servo()

    def to(self,position,current=800,cb=None):
        """
        position in meter. Constant 82644 is calculated by (43,56[mm/360°] => 0.121 [mm/°] => 8.2644 [°/mm] => 8264,46 [°/m]  * 10 => 82644 * (1/10°)/m
        """
        self._servo.move_absolute_angle(int(position*82644),current=current,cb=cb)
        return True
    
    def position(self):
        return self._servo.actual_angle()/82644

    def out(self):
        self.to(0.08)

    def home(self, cb=None):
        self._servo.jog(-50)
        cnt = 0
        while self._servo.actual_current() < 700:
            time.sleep(0.02)
            cnt+=1
            if cnt > 1000:
                return "No Rack inserted"
            if cb:
                cb(self._servo.actual_angle(), self._servo.actual_current())
        self._servo.limp()
        time.sleep(1)
        self._servo.set_zero_here()
        self.to(0.005)
        self._servo.limp()
    

