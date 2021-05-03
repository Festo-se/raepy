from raepy.servo import Servo 
from raepy.radialgripper import RadialGripper 
from raepy.rack import Rack 

from threading import Lock

mutex = Lock()

# inject mutex and servo object
servo = Servo(mutex)
gripper = RadialGripper(mutex,servo)
rack = Rack(servo)