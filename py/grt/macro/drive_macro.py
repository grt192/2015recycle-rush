__author__ = 'dhruv and alex m'

from grt.core import GRTMacro
import wpilib
#import threading


class DriveMacro(GRTMacro):
    def __init__(self, dt, distance_to_travel=0, timeout=None):
        """
        Initialize with drivetrain, gyroscope, desired turn angle and timeout.
        """
        super().__init__(timeout)
        self.dt = dt
        self.right_encoder = dt.right_encoder
        self.left_encoder = dt.left_encoder
        self.distance_to_travel = distance_to_travel
        self.timeout = timeout

    def macro_periodic(self):
        print("Driving!")
        self.left_error = self.left_setpoint - self.left_encoder.distance
        self.right_error = self.right_setpoint - self.right_encoder.distance
        self.ERROR = (self.left_error + self.right_error) / 2
        if self.ERROR >= 0:
            if self.ERROR > 3:
                self.dt.set_dt_output(.8, .8)
            elif self.ERROR <= 3 and self.ERROR > 1:
                self.dt.set_dt_output(.2, .2)
            if self.ERROR <= 1:
                self.macro_stop()
                self.terminate()

        elif self.ERROR < 0:
            if abs(self.ERROR) > 3:
                self.dt.set_dt_output(-.8, -.8)
            elif abs(self.ERROR) <= 3 and abs(self.ERROR) > 1:
                self.dt.set_dt_output(-.2, -.2)
            if abs(self.ERROR) <= 1:
                self.macro_stop()
                self.terminate()



    def macro_stop(self):
        self.dt.set_dt_output(0, 0)

    def macro_initialize(self):
        start_left_distance = self.left_encoder.distance
        start_right_distance = self.right_encoder.distance
        self.left_setpoint = start_left_distance + self.distance_to_travel
        self.right_setpoint = start_right_distance + self.distance_to_travel

    """def macro_initialize(self):
        start_angle = self.gyro.angle
        target_angle = start_angle + self.turn_angle
        self.controller.SetSetpoint(target_angle)
        self.controller.Enable()
        print('MacroTurn is initialized')
    """

    
    def drive(self, distance_to_travel):
        start_left_distance = self.left_encoder.distance
        start_right_distance = self.right_encoder.distance
        self.left_setpoint = start_left_distance + distance_to_travel
        self.right_setpoint = start_right_distance + distance_to_travel
        self.run_threaded()




class DriveMacroOld(GRTMacro):

    def __init__(self, dt, distance, timeout):
        """
        Pass drivetrain, distance to travel (ft), and timeout (secs)
        """
        super().__init__(timeout)
        self.dt = dt
        self.distance = distance
        self.left_encoder = dt.left_encoder
        self.right_encoder = dt.right_encoder
        self.setpoint = distance
        #self.dt_output = self.DTOutput(self)
        #self.dt_source = self.DTSource(self)
        #self.straight_source = self.StraightSource(self)
        #self.straight_output = self.StraightOutput(self)
        #self.DTController = wpilib.PIDController(self.DTP, self.DTI, self.DTD, self.dt_source, self.dt_output)
        #self.straight_controller = wpilib.PIDController(self.CP, self.CI, self.CD,
         #                                               self.straight_source, self.straight_output)
        #self.straight_controller.SetOutputRange(0, 1)

        #self.DTController.SetPID(self.DTP, self.DTI, self.DTD)
        #self.straight_controller.SetPID(self.CP, self.CI, self.CD)
        #self.DTController.SetAbsoluteTolerance(self.TOLERANCE)
        #self.DTController.SetOutputRange(-self.MAX_MOTOR_OUTPUT, self.MAX_MOTOR_OUTPUT)

    def initialize(self):
        self.left_initial_distance = self.left_encoder.e.getDistance()
        self.right_initial_distance = self.right_encoder.e.getDistance()
        #self.right_thread = threading.Thread(target=self.run_right_drive_macro)
        #self.left_thread = threading.Thread(target=self.run_left_drive_macro)
        #self.right_thread.start()
        #print("Starting left thread")
        #self.left_thread.start()
        self.run_both_drive_macro()
        print("running")

    """
    def initialize(self):
        self.left_initial_distance = self.left_encoder.e.GetDistance()
        self.right_initial_distance = self.right_encoder.e.GetDistance()
        self.right_thread = threading.thread(target=self.run_right_drive_macro)
        self.left_thread = threading.thread(target=self.run_left_drive_macro)
        self.right_thread.start()
        self.left_thread.start()
        

        #self.DTController.SetSetpoint(self.distance)
        #self.straight_controller.SetSetpoint(0)
        #self.DTController.Enable()
        #self.straight_controller.Enable()

        #self.leftSF = self.rightSF = 1
        print("Starting DriveMacro")

    def update_motor_speeds(self):
        self.dt.set_dt_output(self.speed * self.leftSF, self.speed * self.rightSF)
    """
    def right_traveled_distance(self):
        print("right travel:" , (self.right_encoder.distance - self.right_initial_distance))
        return self.right_encoder.distance - self.right_initial_distance

    def left_traveled_distance(self):
        print("left travel:" , (self.left_encoder.distance - self.left_initial_distance))
        return self.left_encoder.distance - self.left_initial_distance

    def get_distance_traveled(self):
        """
        Return average of left_traveled_distance and right_traveled_distance
        """
        return (self.left_traveled_distance() + self.right_traveled_distance()) / 2

    def run_right_drive_macro(self):
        while(self.right_traveled_distance() > -self.setpoint * .8):
            self.dt.set_right_motor(1)
            #print("right motor power: 1")
        while(self.right_traveled_distance() > -self.setpoint):
            self.dt.set_right_motor(.5)
            #print("right motor power: .5")
        self.dt.set_right_motor(0)

    def run_left_drive_macro(self):
        while(self.left_traveled_distance() > -self.setpoint * .8):
            self.dt.set_left_motor(1)
           # print("left motor power: 1")
        while(self.left_traveled_distance() > -self.setpoint):
            self.dt.set_left_motor(.5)
           # print("left motor power: .5")
        self.dt.set_left_motor(0)

    def run_both_drive_macro(self):
        while(self.get_distance_traveled() > -self.setpoint * .8):
            self.dt.set_dt_output(.6, .6)
            print("power: %f" % .6)
        while(self.get_distance_traveled() > -self.setpoint):
            self.dt.set_dt_output(.3, .3)
            print("power: %f" % .3)
        self.dt.set_dt_output(0, 0)
        self.kill()
        print("Ended")

    """
    def perform(self):
        #print("DTerror: " + str(self.DTController.GetError()))
        #print("Left Traveled Distance:" + str(self.left_traveled_distance()))
        #print("Right Traveled Distance:" + str(self.right_traveled_distance()))

        #print("Distance Traveled: " + str(self.get_distance_traveled()))
        if (self.DTController.OnTarget()):
            print("On target!")
            if (self.previously_on_target):
                self.kill()
            else:
                self.previously_on_target = True
        else:
            self.previously_on_target = False

    def die(self):
        self.dt.set_dt_output(0, 0)
        #self.DTController.Disable()
        #self.straight_controller.Disable()
    """
    
    class DTSource(wpilib.interfaces.PIDSource):
        """
        PIDSource implementation for DT PID controller.

        Use avg of left, right distance traveled to control distance.
        """
        def __init__(self, drive_macro):
            super().__init__()
            self.drive_macro = drive_macro

        def PIDGet(self):
            return (self.drive_macro.right_traveled_distance() + self.drive_macro.left_traveled_distance()) / 2

    class DTOutput(wpilib.interfaces.PIDOutput):
        """
        PIDOutput implementation for DT PID controller.
        """
        def __init__(self, drive_macro):
            super().__init__()
            self.drive_macro = drive_macro

        def PIDWrite(self, output):
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

        def PIDGet(self):
            return self.drive_macro.right_traveled_distance() - self.drive_macro.left_traveled_distance()

    class StraightOutput(wpilib.interfaces.PIDOutput):
        """
        PIDOutput implementation for straight PID controller.
        """
        def __init__(self, drive_macro):
            super().__init__()
            self.drive_macro = drive_macro

        def PIDWrite(self, output):
            modifier = abs(output)
            #rookie puzzle
            self.drive_macro.leftSF = 1 - (modifier if self.drive_macro.speed * output < 0 else 0)
            self.drive_macro.rightSF = 2 - modifier - self.drive_macro.leftSF
            self.drive_macro.update_motor_speeds()
