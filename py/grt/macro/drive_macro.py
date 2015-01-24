__author__ = 'dhruv and alex m'

from grt.core import GRTMacro
import wpilib

#constants = Constants()


class DriveMacro(GRTMacro):
    """
    Drive Macro; drives forwards a certain distance while
    maintaining orientation
    """
    leftSF = 1
    rightSF = -1
    DTP = 1
    DTI = 0
    DTD = 0
    CP = 1
    CI = 0
    CD = 0
    TOLERANCE = 0.01
    MAX_MOTOR_OUTPUT = 1

    distance = None
    previously_on_target = False

    def __init__(self, dt, distance, timeout):
        """
        Pass drivetrain, distance to travel (ft), and timeout (secs)
        """
        super().__init__(timeout)
        self.dt = dt
        self.distance = distance
        self.left_encoder = dt.left_encoder
        self.right_encoder = dt.right_encoder
        self.dt_output = self.DTOutput(self)
        self.dt_source = self.DTSource(self)
        self.straight_source = self.StraightSource(self)
        self.straight_output = self.StraightOutput(self)
        self.DTController = wpilib.PIDController(self.DTP, self.DTI, self.DTD, self.dt_source, self.dt_output)
        self.straight_controller = wpilib.PIDController(self.CP, self.CI, self.CD,
                                                        self.straight_source, self.straight_output)
        self.straight_controller.setOutputRange(0, 1)

        self.DTController.setPID(self.DTP, self.DTI, self.DTD)
        self.straight_controller.setPID(self.CP, self.CI, self.CD)
        self.DTController.setAbsoluteTolerance(self.TOLERANCE)
        self.DTController.setOutputRange(-self.MAX_MOTOR_OUTPUT, self.MAX_MOTOR_OUTPUT)
        #constants.add_listener(self._constant_listener)

    def _constant_listener(self, sensor, state_id, datum):
        if state_id in ('DTP', 'DTI', 'DTD'):
            self.__dict__[state_id] = datum
            self.DTController.setPID(self.DTP, self.DTI, self.DTD)
        elif state_id in ('CP', 'CI', 'CD'):
            self.__dict__[state_id] = datum
            self.straight_controller.setPID(self.CP, self.CI, self.CD)
        elif state_id == 'DMtol':
            self.TOLERANCE = datum
            self.DTController.setAbsoluteTolerance(datum)
        elif state_id == 'DMMAX':
            self.MAX_MOTOR_OUTPUT = datum
            self.DTController.setOutputRange(-self.MAX_MOTOR_OUTPUT, self.MAX_MOTOR_OUTPUT)

    def initialize(self):
        self.left_initial_distance = self.left_encoder.e.getDistance()
        self.right_initial_distance = self.right_encoder.e.getDistance()

        self.DTController.setSetpoint(self.distance)
        self.straight_controller.setSetpoint(0)
        self.DTController.enable()
        self.straight_controller.enable()

        self.leftSF = self.rightSF = 1
        print("Starting DriveMacro")

    def update_motor_speeds(self):
        self.dt.set_dt_output(self.speed * self.leftSF, self.speed * self.rightSF)

    def right_traveled_distance(self):
        return self.right_encoder.distance - self.right_initial_distance

    def left_traveled_distance(self):
        return self.left_encoder.distance - self.left_initial_distance

    def get_distance_traveled(self):
        """
        Return average of left_traveled_distance and right_traveled_distance
        """
        return (self.left_traveled_distance() + self.right_traveled_distance()) / 2

    def perform(self):
        #print("DTerror: " + str(self.DTController.GetError()))
        #print("Left Traveled Distance:" + str(self.left_traveled_distance()))
        #print("Right Traveled Distance:" + str(self.right_traveled_distance()))

        #print("Distance Traveled: " + str(self.get_distance_traveled()))
        if (self.DTController.onTarget()):
            print("On target!")
            if (self.previously_on_target):
                self.kill()
            else:
                self.previously_on_target = True
        else:
            self.previously_on_target = False

    def die(self):
        self.dt.set_dt_output(0, 0)
        self.DTController.disable()
        self.straight_controller.disable()

    class DTSource(wpilib.interfaces.PIDSource):
        """
        PIDSource implementation for DT PID controller.

        Use avg of left, right distance traveled to control distance.
        """
        def __init__(self, drive_macro):
            super().__init__()
            self.drive_macro = drive_macro

        def pidGet(self):
            return (self.drive_macro.right_traveled_distance() + self.drive_macro.left_traveled_distance()) / 2

    class DTOutput(wpilib.interfaces.PIDOutput):
        """
        PIDOutput implementation for DT PID controller.
        """
        def __init__(self, drive_macro):
            super().__init__()
            self.drive_macro = drive_macro

        def pidWrite(self, output):
            self.drive_macro.speed = output
            self.drive_macro.update_motor_speeds()

    class StraightSource(wpilib.interfaces.PIDSource):
        """
        PIDSource implementation for straight PID controller.

        Use distance difference (between L/R DTs), to keep
        robot straight.
        """
        def __init__(self, drive_macro):
            super().__init__()
            self.drive_macro = drive_macro

        def pidGet(self):
            return self.drive_macro.right_traveled_distance() - self.drive_macro.left_traveled_distance()

    class StraightOutput(wpilib.interfaces.PIDOutput):
        """
        PIDOutput implementation for straight PID controller.
        """
        def __init__(self, drive_macro):
            super().__init__()
            self.drive_macro = drive_macro

        def pidWrite(self, output):
            modifier = abs(output)
            #rookie puzzle
            self.drive_macro.leftSF = 1 - (modifier if self.drive_macro.speed * output < 0 else 0)
            self.drive_macro.rightSF = 2 - modifier - self.drive_macro.leftSF
            self.drive_macro.update_motor_speeds()
