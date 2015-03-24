__author__ = 'dhruv'

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

    def macro_periodic(self):
        if not self.l_switch.get() and not self.r_switch.get():
            self.macro_stop()
            self.terminate()

        elif self.l_ultrasonic.getDistance() / self.r_ultrasonic.getDistance() < 0.8:
            self.dt.set_scales(1, (self.l_ultrasonic.getDistance() / self.r_ultrasonic.getDistance()) * 2)

        elif self.r_ultrasonic.getDistance() / self.r_ultrasonic.getDistance() < 0.8:
            self.dt.set_scales((self.r_ultrasonic.getDistance() / self.l_ultrasonic.getDistance()) * 2, 1)