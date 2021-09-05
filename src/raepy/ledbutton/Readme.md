# Choose realsense or kinect version
Depending on your system, realsense or kinect, you have different numbers of Led-buttons.
The Realsense system has usually 1 and the kinect-system has 2.
## Realsense System (default)
```python
from raepy.ledbutton import LedButton
rsledbutton = LedButton(version="realsense")
# has 2 objects
rsledbutton.button
rsledbutton.led
```
## Kinect System
```python
from raepy.ledbutton import LedButton
rsledbutton = LedButton(version="kinect")
# has 4 objects
ktledbutton.button1
ktledbutton.led1
ktledbutton.button2
ktledbutton.led2
```

# Button functions
Generate `LedButton` object to control Led and Button.
```python 
lb = LedButton()
lb.button # Button object
```
## Read Button state
The current state of the button can be accessed through the `state()` function of th `Button` object.

```python
# Returns current button state as integer: 0 or 1
while True:
    if lb.button.state() == 1
        print("Button pressed")
    else:
        print("Button released)
```
## Event Trigger
If an event-based programming is necessary you just have to define handlers, either for the rising or falling edge trigger or both. Then you have to register the function in the system like below: 
```python
def button_pressed_handler():
    print("Button pressed")

def button_released_handler():
    print("Button released")

# Register the handlers as callback
lb.button.register_rising_edge_cb(button_pressed_handler)

lb.button.register_falling_edge_cb(button_released_handler)

```

# LED Functions

## On and Off
Generate `LedButton` object to control Led through the `lb.led` object.

```python 
lb = LedButton()
lb.led # Button object
```
## Blink
The Blink generator can either blink a certain endless or a certain amount of blink-periods.

```python
# The default blinks 7 times with 7 Hz
lb.blink()

# Customize the blink frequency and number of periods
lb.blink(freq=5,cnt=10)

# Endless blinking: Set cnt paramter to 0
lb.blink(freq=5,cnt=0)

# Stop the endless blinker
lb.stop_blink()
```

## Heartbeat
The heartbeat pattern is pretty realistic because it was generated with the python lib `neurokit2`.
The following script generated the heartbeat pattern an saved it as a numpy binary file `.npy`

```python
import neurokit2 as nk
import numpy as np

ecg = np.abs(nk.ecg_simulate(duration=30, sampling_rate=1000,heart_rate=90, heart_rate_std=3))
nk.ecg_clean(ecg, sampling_rate=1000, method="engzeemod2012")
v = ecg
normalized_ecg = (v-v.min()) / (v.max()-v.min())
int_ecg = (normalized_ecg*100).astype(int)
np.save("ECG_EngZeeMod", int_ecg)
```
The heartbeat pattern run as thread to be able to let it run in the backround.

```python
# The heartbeat pattern has an input parameter speed (1-100) to set the heart frequency: 
lb.led.heartbeat_on(speed=1)

# While running the heartbeat, the speed can be changed with
lb.led.set_heartbeat_speed(speed=99)

# Stop heartbeat pattern 
lb.led.heartbeat_off()
```