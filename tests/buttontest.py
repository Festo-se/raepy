import unittest
from raepy import ledbutton
from raepy.ledbutton import led
from raepy import LedButton
import time
lb = LedButton()

class TestButton(unittest.TestCase):
    def test_buttonpress(self):
        print("Press button")
        while True:
            if lb.button.state() == 1:
                break
        self.assertTrue(True)
    
    def test_event_trigger(self):
        time.sleep(1)
        print("Press button again")
        result = False
        def press_handler():
            result = True
            
        lb.button.register_rising_edge_cb(press_handler)

        while result:
            time.sleep(0.1)
        self.assertTrue((True))

if __name__ == '__main__':
    unittest.main()