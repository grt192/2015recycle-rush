__author__ = 'dhruv'
from grt.core import Sensor
from

class BoxAlignController(Sensor):
    def __init__(self, dt, l_switch, r_switch, l_ultrasonic, r_ultrasonic):
        super().__init__()
        self.dt = dt
        self.l_switch = l_switch
        self.r_switch = r_switch
        self.l_ultrasonic = l_ultrasonic
        self.r_ultrasonic = r_ultrasonic
        self.enabled = False

