__author__ = 'dhruv'

import math
from grt.core import GRTMacro

class UltrasonicAlignMacro(GRTMacro):
    def __init__(self, dt, l_ultrasonic, r_ultrasonic, l_switch, r_switch, target_distance=0, timeout=None):
        super().__init__(timeout)
        self.dt = dt
        self.l_switch = l_switch
        self.r_switch = r_switch
        self.l_ultrasonic = l_ultrasonic
        self.r_ultrasonic = r_ultrasonic
        self.target_distance = target_distance
        self.enabled = False
        self.run_threaded()

    def macro_periodic(self):
        if self.enabled:
            if math.fabs((self.l_ultrasonic.getDistance() + self.r_ultrasonic.getDistance()) / 2.0) / self.target_distance - 1 < 0.2:
                self.macro_stop()
                self.terminate()

            else:
                if not self.l_switch.get() and not self.r_switch.get():
                    self.macro_stop()
                    self.terminate()

                elif self.l_ultrasonic.getDistance() / self.r_ultrasonic.getDistance() < 0.8:
                    self.dt.set_scales(.4, .4 * (self.l_ultrasonic.getDistance() / self.r_ultrasonic.getDistance()) ** 2)

                elif self.r_ultrasonic.getDistance() / self.r_ultrasonic.getDistance() < 0.8:
                    self.dt.set_scales(.4 * (self.r_ultrasonic.getDistance() / self.l_ultrasonic.getDistance()) ** 2, .4)

    def macro_stop(self):
        self.dt.set_scales(1, 1)
        self.dt.set_dt_output(0, 0)