__author__ = 'dhruv'
from grt.core import Sensor

class BoxAlignController(Sensor):
    def __init__(self, dt, l_switch, r_switch, l_ultrasonic, r_ultrasonic):
        super().__init__()
        self.dt = dt
        self.l_switch = l_switch
        self.r_switch = r_switch
        self.l_ultrasonic = l_ultrasonic
        self.r_ultrasonic = r_ultrasonic

    def _alignment_listener(self, state_id, datum):
        if not self.l_switch.get() and not self.r_switch.get():
            self.dt.set_dt_output(0, 0)

        elif self.l_ultrasonic.getDistance() / self.r_ultrasonic.getDistance() < 1:
            self.dt.set_dt_output()