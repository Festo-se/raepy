import unittest
from raepy  import LedButton
import time

lb = LedButton()

class TestLed(unittest.TestCase):
    def test_onoff(self):
        lb.led.on()
        time.sleep(1)
        lb.led.off()
        self.assertTrue(True)

    def test_blink(self):
        print("Default blink.")
        lb.led.blink()
        print("Slow blink 3Hz. 10 Times.")
        lb.led.blink(freq=3,cnt=10)
        print("Fast blink 10Hz. Continous.")
        lb.led.blink(freq=10,cnt=0)
        time.sleep(2)
        print("Slow blink. Continous.")
        lb.led.blink(freq=2,cnt=0)
        time.sleep(3)
        print("Stop continous blinking")
        lb.led.stop_blink()
        self.assertTrue(True)

    def test_heartbeat(self):
        print("Default heartbeat")
        lb.led.heartbeat_on(speed=1)
        time.sleep(7)
        print("Heartbeat off")
        lb.led.heartbeat_off()
        time.sleep(1)
        print("Slow heartbeat")
        lb.led.heartbeat_on(speed=1)
        time.sleep(7)
        print("Increase speed +1")
        lb.led.set_heartbeat_speed(speed=2)
        time.sleep(7)
        print("Increase speed +1")
        lb.led.set_heartbeat_speed(speed=3)
        time.sleep(7)
        lb.led.heartbeat_off()
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()