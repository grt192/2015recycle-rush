"""
Module for various drivetrain control mechanisms.
Listens to Attack3Joysticks, not wpilib.Joysticks.
"""
from collections import OrderedDict

class ArcadeDriveController:
    """
    Class for controlling DT in arcade drive mode, with one or two joysticks.
    """

    def __init__(self, dt, l_joystick, record_macro=None, playback_macro=None, r_joystick=None):
        """
        Initialize arcade drive controller with a DT and up to two joysticks.
        """
        self.dt = dt
        self.l_joystick = l_joystick
        self.r_joystick = r_joystick
        self.record_macro = record_macro
        self.playback_macro = playback_macro
        self.instructions = OrderedDict([("1, <class 'wpilib.cantalon.CANTalon'>", [-0.015640273704789834, -0.015640273704789834, -0.015640273704789834, -0.015640273704789834, -0.015640273704789834, -0.015640273704789834, -0.015640273704789834, 0.04594330400782014, 0.0, 0.0, 0.0, -0.07038123167155426, -0.3704789833822092, -0.5581622678396871, -0.6373411534701857, -0.5034213098729228, -0.46432062561094817, -0.5268817204301075, -0.5112414467253177, -0.41642228739002934, -0.3460410557184751, -0.3304007820136852, -0.3069403714565005, -0.3069403714565005, -0.2913000977517107, -0.2678396871945259, -0.2678396871945259, -0.2678396871945259, -0.3304007820136852, -0.3460410557184751, -0.36950146627565983, -0.2668621700879765, -0.007820136852394917, 0.022482893450635387, 0.022482893450635387, 0.022482893450635387]), ("7, <class 'wpilib.cantalon.CANTalon'>", [-0.015640273704789834, -0.015640273704789834, -0.015640273704789834, -0.015640273704789834, -0.015640273704789834, -0.015640273704789834, -0.015640273704789834, 0.04594330400782014, 0.0, 0.0, 0.0, 0.039100684261974585, 0.4946236559139785, 0.5581622678396871, 0.5747800586510264, 0.44086021505376344, 0.47996089931573804, 0.41642228739002934, 0.40078201368523947, 0.41642228739002934, 0.3616813294232649, 0.37732160312805474, 0.35386119257087, 0.35386119257087, 0.33822091886608013, 0.3616813294232649, 0.3616813294232649, 0.3616813294232649, 0.2825024437927664, 0.2825024437927664, 0.2590420332355816, 0.20430107526881722, 0.10166177908113393, 0.022482893450635387, 0.022482893450635387, 0.022482893450635387]), ("100, <class 'grt.macro.assistance_macros.ElevatorMacro'>", [0, 0, 0, 0, 0, 0, 0, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 0, 0, 0, 0, 0, 0])])
        self.engage()

    def _joylistener(self, sensor, state_id, datum):
        if sensor in (self.l_joystick, self.r_joystick) and state_id in ('x_axis', 'y_axis'):
            power = -self.l_joystick.y_axis
            turnval = self.r_joystick.x_axis if self.r_joystick else self.l_joystick.x_axis
            # get turn value from r_joystick if it exists, else get it from l_joystick
            #print("Power: %f" % power)

            self.dt.set_dt_output(power + turnval,
                                  power - turnval)
        elif sensor == self.l_joystick and state_id == 'trigger':
            if datum:
                self.dt.upshift()
            else:
                self.dt.downshift()
        if state_id == "button11":
            if datum:
                print("Recording started")
                self.record_macro.start_record()
        if state_id == "button10":
            if datum:
                print("Recording stopped")
                self.instructions = self.record_macro.stop_record()
                #self.record_macro.instructions = self.instructions
        if state_id == "button9":
            if datum:
                self.playback_macro.start_playback(self.instructions)
        if state_id == "button8":
            if datum:
                self.playback_macro.stop_playback()
        if state_id == "button70":
            if datum:
                self.playback_macro.load("/home/lvuser/py/instructions.py")
                self.playback_macro.start_playback()


    def engage(self):
            self.l_joystick.add_listener(self._joylistener)
            if self.r_joystick:
                self.r_joystick.add_listener(self._joylistener)

    def disengage(self):
            self.l_joystick.remove_listener(self._joylistener)
            if self.r_joystick:
                self.r_joystick.remove_listener(self._joylistener)

class TankDriveController:
    """
    Class for controlling DT in tank drive mode with two joysticks.
    """

    def __init__(self, dt, l_joystick, r_joystick):
        """
        Initializes self with a DT and left and right joysticks.
        """
        self.dt = dt
        self.l_joystick = l_joystick
        self.r_joystick = r_joystick
        l_joystick.add_listener(self._joylistener)
        r_joystick.add_listener(self._joylistener)

    def _joylistener(self, sensor, state_id, datum):
        if sensor in (self.l_joystick, self.r_joystick) and state_id in ('x_axis', 'y_axis'):
            self.dt.set_dt_output(self.l_joystick.y_axis,
                                  self.r_joystick.y_axis)
