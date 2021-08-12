
import threading
import subprocess
import atexit
import os
import signal
import time

from ..utils.singleton import Singleton

class VacuumModule(object):
    __metaclass__ = Singleton
    def __init__(self):
        print("Vacuum Module init")
        try:
            os.mkfifo("/tmp/vacmodstate")
            os.mkfifo("/tmp/vacmodcmd")
        except:
            pass
        
        file = os.path.abspath(__file__ + "/../") + "/vacmod"
        self.process = subprocess.Popen("nohup {} >/dev/null 2>&1 &".format(file),shell=True)

        atexit.register(self.clean)
        self.actual_state = None
        self.__sucked_cb = None
        self.__lost_cb = None
        time.sleep(0.1)
        state_reader = threading.Thread(target=self.__read_state)
        state_reader.start()
        
    

    def clean(self):
        print("Cleanup!")
        os.killpg(os.getpgid(self.process.pid), signal.SIGTERM)

    def suck(self, sucked_cb=None, lost_cb=None):
        with open("/tmp/vacmodcmd", "w") as startcmd:
            startcmd.write("START")

        if sucked_cb:
            self.__sucked_cb = sucked_cb
        if lost_cb:
            self.__lost_cb = lost_cb

        
    def release(self):
        with open("/tmp/vacmodcmd", "w") as stopcmd:
            stopcmd.write("STOP\n")

    def sucked(self):
        return self.current_state() == "SUCKED"

    def current_state(self):
        return self.actual_state

    def __read_state(self):
        while True:
            with open('/tmp/vacmodstate') as fifo:
                for state in fifo:
                    self.actual_state = state.rstrip('\x00')
                    if self.actual_state == "SUCKED" and self.__sucked_cb != None:
                        self.__sucked_cb(state)
                    elif self.actual_state == "LOST" and self.__lost_cb != None:
                        self.__lost_cb(state)


    def print_state(self,state):
        print("{}".format(state),end="\n")


                    

