"""
basic_auto.py
"""


__author__ = "Abraham Ryzhik"

from . import MacroSequence
from grt.core import Constants, GRTMacro
from grt.macro.drive_macro import DriveMacro
from grt.macro.elevator_macro import ElevatorMacro



class BasicAuto(MacroSequence):
    """
    Basic autonomous mode. Drives and shoots. Pretty straightforward.
    """

    def __init__(self, dt, elevator):

        self.drive_macro = DriveMacro(dt, 24-5, 300)
        self.elevator_macro = ElevatorMacro(elevator, 750, 2)
        self.drive_macro2 = DriveMacro(dt, 70-5, 300) #units are in inches
        #self.wait_macro = GRTMacro(0.5)  # blank macro just waits
        #self.drive_macro2 = DriveMacro(dt, 70-5, 300) #units are in inches
        self.elevator_macro2 = ElevatorMacro(elevator, -550, 1)
        self.macros = [self.drive_macro, self.elevator_macro, self.drive_macro2, self.elevator_macro2]
        super().__init__(macros=self.macros)  