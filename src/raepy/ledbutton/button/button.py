#! /usr/bin/env python3
import time
import threading
import RPi.GPIO as GPIO

class Button(object):
    def __init__(self,pin=13):
        self.__pin = pin

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        self.__state = 0
        self.__prev_state = 0
        threading.Thread(target=self.__read_states).start()
        self.__rising_edge_callback = None
        self.__falling_edge_callback = None
    def __del__(self):
        GPIO.cleanup()
        

    def __read_states(self):
        """
        Read the button states continously inside an threaded loop
        """
        while True:
            self.__state = GPIO.input(self.__pin)
            if self.__state > self.__prev_state:
                self.__rising_edge()
            elif self.__state < self.__prev_state:
                self.__falling_edge()
            time.sleep(0.05)
            self.__prev_state = self.__state

    def __rising_edge(self):
        """
        Calls the callback if available
        """
        if self.__rising_edge_callback != None:
            self.__rising_edge_callback()

    def __falling_edge(self):
        """
        Calls the callback if available
        """
        if self.__falling_edge_callback != None:
            self.__falling_edge_callback()

    def register_rising_edge_cb(self,cb):
        """
        Register callback that will be triggered when the button gets clicked
        """
        self.__rising_edge_callback = cb

    def register_falling_edge_cb(self,cb):
        """
        Register callback that will be triggered when the button gets released
        """
        self.__falling_edge_callback = cb


    def state(self):
        """
        returns the current state of the button
        0 : Button pressed
        1 : Button released
        """
        return int(self.__state)
        
def pressed_event():
    print("Button pressed event")

def released_event():
    print("Button released event")

if __name__ == "__main__":

    lb = Button(pin=13)
    lb.register_rising_edge_cb(pressed_event)
    lb.register_falling_edge_cb(released_event)

    while True:
        if lb.state() == 1:
            print("Button pressed")
        else:
            print("Button released")
        time.sleep(1)
