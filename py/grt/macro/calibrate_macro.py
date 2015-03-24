
from grt.core import GRTMacro
import wpilib


class CalibrateMacro(GRTMacro):
    """
    Drives to a set distance from an object using an ultrasonic sensor.
    """
    def __init__(self, dt, ultrasonic, setpoint=0, timeout=None):
        super().__init__(timeout)
        self.dt = dt
        self.ultrasonic = ultrasonic
        self.setpoint = setpoint
        self.timeout = timeout

    def macro_periodic(self):
        self.ERROR = self.setpoint - self.ultrasonic.distance
        if self.ERROR >= 0:
            if self.ERROR > 10:
                self.dt.set_dt_output(.8, .8)
            elif self.ERROR <= 10 and self.ERROR > 1:
                self.dt.set_dt_output(.2, .2)
            if self.ERROR <= 1:
                self.macro_stop()
                self.terminate()

        elif self.ERROR < 0:
            if abs(self.ERROR) > 10:
                self.dt.set_dt_output(-.8, -.8)
            elif abs(self.ERROR) <= 10 and abs(self.ERROR) > 1:
                self.dt.set_dt_output(-.2, -.2)
            if abs(self.ERROR) <= 1:
                self.macro_stop()
                self.terminate()



    def macro_stop(self):
        self.dt.set_dt_output(0, 0)

    """def macro_initialize(self):
        start_angle = self.gyro.angle
        target_angle = start_angle + self.turn_angle
        self.controller.SetSetpoint(target_angle)
        self.controller.Enable()
        print('MacroTurn is initialized')
    """

    def drive_to(self, distance):
        self.setpoint = distance
        self.run_threaded()
    def turn(self, turn_angle):
        start_angle = self.gyro.getYaw()
        target_angle = start_angle + turn_angle
        self.setpoint = target_angle
        self.run_threaded()

    