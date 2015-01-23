"""
basic_auto.py
"""


__author__ = “Abraham Ryzhik“

from . import MacroSequence
from grt.core import Constants, GRTMacro
from grt.macro.drive_macro import DriveMacro



class BasicAuto(MacroSequence):
    """
    Basic autonomous mode. Drives and shoots. Pretty straightforward.
    """

    def __init__(self, dt, elevator):
	self.elevate_macro = ElevatorMacro(elevator, 1, 1)
        self.drive_macro = DriveMacro(dt, 5, 3)
        self.wait_macro = GRTMacro(0.5)  # blank macro just waits
	self.lower_macro = ElevatorMacro(elevator, -1, 1)
        self.macros = [self.elevator_macro, self.drive_macro, self.wait_macro, self.lower_macro]
        super().__init__(macros=self.macros)