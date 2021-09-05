#! /usr/bin/env python3

import time
import threading
import RPi.GPIO as GPIO
import numpy as np
import os

class Led(object):
    def __init__(self,pin=15):
        self.__pin = pin
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.__pin, GPIO.OUT)
        self.__ledpwm = GPIO.PWM(self.__pin,700)
        self.__stop_event = threading.Event()
        self.__blink_thread = threading.Thread(target=self.__blinker, args=[self.__stop_event])
        self.__hearbeat_switch = threading.Event()
        self.__heartbeat_thread = threading.Thread(target=self.__heartbeat,args=[self.__hearbeat_switch])
        self.__heartbeat_thread.start()
        ecg_file_path = os.path.abspath(__file__+"/../") + "/ECG_EngZeeMod.npy"
        self.__ecg_pattern = np.load(ecg_file_path)
        self.set_heartbeat_speed(speed=1)
        self.__blink_thread.start()
        self.__blink_freq = 1
        self.__led_intensity = 0
        self.__ledpwm.start(100)

    def __del__(self):
        GPIO.cleanup()

    def dimm(self,intensity):
        self.__led_intensity = intensity
        self.__ledpwm.ChangeDutyCycle(100-intensity)

    def on(self,intensity=100):
        """
        Switches the led ring on
        """
        if self.__led_intensity != intensity:
            self.dimm(intensity)
            self.__led_intensity = intensity

     
    def off(self):
        """
        Switches the led ring on
        """
        self.dimm(0)


    def __heartbeat(self,switch_event):
        
        #v = np.abs(nk.ecg_simulate(duration=8, sampling_rate=100, heart_rate=80))
        #normalized_ecg = (v-v.min()) / (v.max()-v.min())
        #normalized_ecg = (normalized_ecg*100).astype(int)

        while True:
            if switch_event.wait():
                for sample in  self.__ecg_pattern:
                    self.__ledpwm.ChangeDutyCycle(100-int(sample))
                    time.sleep(self.__heartbeat_speed)
                    if not switch_event.wait():
                        print("here")
                        break
            else:
                time.sleep(1)
    
    def set_heartbeat_speed(self,speed):
        """
        Speed parameter can be set in between 1 and 100
        """
        if speed > 99:
            speed = 99
        elif speed < 1:
            speed = 1

        self.__heartbeat_speed = (200-speed)/100000

    def heartbeat_on(self,speed=1):
        self.set_heartbeat_speed(speed)
        self.__ledpwm.ChangeDutyCycle(100)
        self.__hearbeat_switch.set()
    
    def heartbeat_off(self):
        self.__hearbeat_switch.clear()
        self.__ledpwm.ChangeDutyCycle(100)

    def __blink_cycle(self,t):
        self.on()
        time.sleep(t)
        self.off()
        time.sleep(t)


    def __blinker(self,event):
        while True:
            if event.wait():
                self.__blink_cycle(1/(2*self.__blink_freq))
            else:
                time.sleep(1)

    def blink(self,freq=7,cnt=7):
        """
        Blink function for the LED ring:
        Parameters:
        freq : switching frequency
        cnt : How many counts will be switched.
        If cnt == 0 then it will be switched continously
        """
        self.__stop_event.clear()

        if freq == 0:
            self.off()
            return
        
        if cnt != 0:
            for _ in range(cnt):
                self.__blink_cycle((1/(2*freq)))
        else:
            self.__blink_freq = freq
            self.__stop_event.set()
    
    def blink_on(self,freq=7):
        self.blink(freq=freq,cnt=0)

    def stop_blink(self):
        self.__stop_event.clear()
        self.off()


if __name__ == "__main__":

    led = Led()
    """    
    led.on(10)
    time.sleep(3)
    led.on(100)
    time.sleep(3)
    led.off()
    time.sleep(1)
    """

    led.heartbeat_on(speed=50)
    time.sleep(15)
    led.heartbeat_off()
