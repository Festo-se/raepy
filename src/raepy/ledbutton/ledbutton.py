#! /usr/bin/env python3

from .led import Led
from .button import Button
import time

class LedButton(object):
    def __init__(self,ledpin=15,buttonpin=13):
        self.led = Led(ledpin)
        self.button = Button(buttonpin)


if __name__ == "__main__":

    lb = LedButton()
    while True:
        print(lb.button.state())
        if lb.button.state() == 1:
            lb.led.on()
        else:
            lb.led.off()
        time.sleep(0.1)
