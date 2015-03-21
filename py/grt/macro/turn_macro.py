__author__ = "dhruv, Sidd Karamcheti"

from grt.core import GRTMacro
import wpilib


class TurnMacro(GRTMacro):
    def __init__(self, dt, gyro, setpoint=0, timeout=None):
        """
        Initialize with drivetrain, gyroscope, desired turn angle and timeout.
        """
        super().__init__(timeout)
        self.dt = dt
        self.gyro = gyro
        self.setpoint = setpoint
        self.timeout = timeout

    def macro_periodic(self):
        print("Turning!")
        self.ERROR = self.gyro.getYaw() - self.setpoint 
        print(self.ERROR)
        if self.ERROR >= 0:
            if self.ERROR > 30:
                self.dt.set_dt_output(-.5, .5)
            elif self.ERROR <= 30 and self.ERROR > 25:
                self.dt.set_dt_output(-.1, .1)
            if self.ERROR <= 25:
                print("Terminated 2")
                self.macro_stop()
                print("Terminated 1")
                self.terminate()
                print("Terminated")
        elif self.ERROR < 0:
            if abs(self.ERROR) > 30:
                self.dt.set_dt_output(.5, -.5)
            elif abs(self.ERROR) <= 30 and abs(self.ERROR) > 25:
                self.dt.set_dt_output(.1, -.1)
            if abs(self.ERROR) <= 25:
                print("Terminated 2")
                self.macro_stop()
                print("Terminated 1")
                self.terminate()
                print("Terminated")


    def macro_stop(self):
        self.dt.set_dt_output(0, 0)

    """def macro_initialize(self):
        start_angle = self.gyro.angle
        target_angle = start_angle + self.turn_angle
        self.controller.SetSetpoint(target_angle)
        self.controller.Enable()
        print('MacroTurn is initialized')
    """

    def turn_to(self, turn_angle):
        self.setpoint = turn_angle
        self.run_threaded()
    def turn(self, turn_angle):
        start_angle = self.gyro.getYaw()
        target_angle = start_angle + turn_angle
        self.setpoint = target_angle
        self.run_threaded()

class TurnRawMacro(TurnMacro):
    def __init__(self, dt, gyro, setpoint=0, timeout=None):
        """
        Initialize with drivetrain, gyroscope, desired turn angle and timeout.
        """
        super().__init__(dt, gyro, setpoint, timeout)
        self.dt = dt
        self.gyro = gyro
        self.setpoint = setpoint
        self.timeout = timeout
    def macro_initialize(self):
        start_angle = self.gyro.getYaw()
        target_angle = start_angle + turn_angle
        self.setpoint = target_angle

