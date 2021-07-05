# About
This is the official repositiory for the python based software drivers of the robot autonomy effector.
This package enables you to control the fingertip distance of the gripper, the position of the rack and direct Servo access.

# Prerequisites
* Python > 3.6
* Linux based System OS
* Ethernet or Wifi Connected RPi4
* SSH Connection to RPi (VSCODE SSH extension is strongly recommended)
  
# Installation
Either clone this repository with
```bash
pip3 install git+https://github.com/romzn/raepy.git
```
or direct from the pypi repository
```bash
pip3 install raepy
```
or build the newest version and 
```bash
git clone github.com/romzn/raepy.git
cd raepy

## Build repository and Install
python3 -m pip install --upgrade build
pip3 -m build
pip3 install .

# Start tests to see basic functionality (!!After the racktest and servoest an recalibration has to be made!!)
pip3 -m unittest racktest.py
pip3 -m unittest radialgrippertest.py
pip3 -m unittest racktest.py
```

# Basic functionality
To move the gripper or the rack the their specific objects has to be loaded in the current script.

```python
from raepy import rack, gripper, servo


rack.out() # brings the rack to the front position (+8cm) and the grippers back


gripper.grasp() # brings the grippers together until they meet resistance, then they are holding with an specific force.


gripper.to(0.1) # Set the distance between the two fingertips to 10 cm


gripper.to(0.2) # Set the distance between the two fingertips to 20 cm


rack.to(0.5) # Drives the rack to an absolute position (5cm)


rack.to(1.2) # Drives the rack out !! but before dismantle the grippers or they will collide !!


servo.led_to(color) # sets the color to ['black', 'red', 'green', 'blue', 'yellow', 'cyab', 'magenta']


servo.limp() # Sets the motor current to zero which results in powerless fingers


servo.hold() # holds the position with an specific force (max 28 Nm)


# ! There are some servomotor functions more, just take a look at the sources ./src/servo !

```



# Calibration
To calibrate the gripper two steps has to be made. 

In the first step the grippers have to be dismantled an the rack must drive Rack Out

>Normally an calibration is not needed because the gripper is calibrated by factory. 
>In the case you dismantle Gripper without mounting them back into exactly the same position, 
or you drive the rack completely out an recalibration is necessary. It is also necesseary if the package was updated

