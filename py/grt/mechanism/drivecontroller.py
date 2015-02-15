"""
Module for various drivetrain control mechanisms.
Listens to Attack3Joysticks, not wpilib.Joysticks.
"""


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
                self.record_macro.start_record()
        if state_id == "button10":
            if datum:
                self.instructions = self.record_macro.stop_record()
                #self.record_macro.instructions = self.instructions
        if state_id == "button9":
            if datum:
                self.playback_macro.start_playback(self.instructions)
        if state_id == "button8":
            if datum:
                self.playback_macro.stop_playback()
        if state_id == "button7":
            if datum:
                self.playback_macro.load("instructions.py")
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
