from grt.macro.assistance_macros import *
import wpilib

class Elevator:
    def __init__(self, elevator_motor, elevator_encoder, left_switch=None, right_switch=None, dt=None, winch_servo=None, top_switch=None, bottom_switch=None, bottom_limit_switch=None):
        self.elevator_motor = elevator_motor
        self.elevator_encoder = elevator_encoder
        self.winch_servo = winch_servo
        self.left_switch = left_switch
        self.right_switch = right_switch
        self.top_switch = top_switch
        self.bottom_switch = bottom_switch
        self.running_macros = []
        #The elevator passes itself to the macros so that they can take over its functions.
        self.release_macro = ReleaseMacro(self, dt)
        self.align_macro = AlignMacro(self, dt)
        self.lift_macro = ElevatorMacro(self)
        self.bottom_limit_switch = bottom_limit_switch

        #self.temp_talon = wpilib.Talon(9)

    def elevate(self):
        if self.winch_servo:
            self.release_winch()
        self.elevator_motor.set(1)

    def lower(self):
        if self.winch_servo:
            self.release_winch()
        self.elevator_motor.set(-1)

    def stop(self):
        if self.winch_servo:
            self.engage_winch()

        self.elevator_motor.set(0)
        #self.temp_talon.set(0)

    def elevate_speed(self, power):
        self.elevator_motor.set(power)
        #self.temp_talon.set(power)

    def engage_winch(self):
        self.winch_servo.setAngle(45)

    def release_winch(self):
        self.winch_servo.setAngle(0)

    def release(self):
        self.release_macro.release()
    def abort_release(self):
        self.release_macro.abort()
    def pickup(self):
        self.align_macro.align()
    def spring(self):
        self.wait_for_pickup()
        self.set_state('level4')
    def wait_for_pickup(self):
        self.align_macro.wait_for_align()

    def set_state(self, state):
        self.lift_macro.lift_to(state)

    def disable_all_macros(self):
        for macro in self.running_macros:
            if macro.enabled:
                macro.enabled = False

    def emergency_stop_all_macros(self):
        for macro in self.running_macros:
            macro.terminate()
            if macro.enabled:
                macro.enabled = False

    def emergency_restart_all_macros(self):
        self.kill_all_macros()
        for macro in self.running_macros:
            macro.run_threaded()
        #macro.thread.stop()

