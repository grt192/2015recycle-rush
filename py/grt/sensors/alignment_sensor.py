__author__ = 'dhruv'

import math
from grt.core import CompoundSensor

class AlignmentSensor(CompoundSensor):

    target_distance = 1.5

    def __init__(self, dt, l_ultrasonic, r_ultrasonic, l_switch, r_switch, driver_joystick):
        super().__init__()
        self.dt = dt
        self.l_ultrasonic = l_ultrasonic
        self.r_ultrasonic = r_ultrasonic
        self.l_switch = l_switch
        self.r_switch = r_switch
        self.driver_joystick = driver_joystick
        self.enabled = False
        self.add_listener(self._ultrasonic_alignment_listener)

    def _ultrasonic_alignment_listener(self, state_id, datum):
        if self.enabled:
            if math.fabs((self.l_ultrasonic.getDistance() + self.r_ultrasonic.getDistance()) / 2.0) / self.target_distance - 1 < 0.2:
                self.terminate()

            else:
                if not self.l_switch.get() and not self.r_switch.get():
                    self.terminate()

                elif self.l_ultrasonic.getDistance() / self.r_ultrasonic.getDistance() < 0.8:
                    self.dt.set_scales(.4, .4 * (self.l_ultrasonic.getDistance() / self.r_ultrasonic.getDistance()) ** 2)

                elif self.r_ultrasonic.getDistance() / self.r_ultrasonic.getDistance() < 0.8:
                    self.dt.set_scales(.4 * (self.r_ultrasonic.getDistance() / self.l_ultrasonic.getDistance()) ** 2, .4)

    def terminate(self):
        self.dt.set_scales(1, 1)
        self.enabled = False