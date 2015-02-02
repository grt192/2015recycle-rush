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

        self.elevator_macro = ElevatorMacro(elevator, 50, 1)
        #self.drive_macro = DriveMacro(dt, 700, 30) 
        self.wait_macro = GRTMacro(0.5)  # blank macro just waits
        #self.elevator_macro = ElevatorMacro(elevator, -50, 1)
        self.macros = [self.elevator_macro, self.wait_macro]
        super().__init__(macros=self.macros)  