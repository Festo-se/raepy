#! /usr/bin/env python3

from .led import Led
from .button import Button
import time

class LedButton(object):
    def __init__(self,version="realsense"):
        if version == "realsense":
            self.led = Led()
            self.button = Button()

        if version == "kinect":
            self.led1 = Led()
            self.button1 = Button()
            self.led2 = Led(pin=16)
            self.button2 = Button(pin=18)


if __name__ == "__main__":

    lb = LedButton()
    while True:
        print(lb.button.state())
        if lb.button.state() == 1:
            lb.led.on()
        else:
            lb.led.off()
        time.sleep(0.1)
