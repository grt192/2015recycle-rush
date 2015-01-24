"""
basic_auto.py
"""


__author__ = "Abraham Ryzhik"

from . import MacroSequence
from grt.core import Constants, GRTMacro
from grt.macro.drive_macro import DriveMacro



class BasicAuto(MacroSequence):
    """
    Basic autonomous mode. Drives and shoots. Pretty straightforward.
    """

    def __init__(self, dt, elevator=None, lead_screw=None):
        # self.pickup_macro = PickupMacro(lead_screw, “tote_long”, 1)
	# self.elevate_macro = ElevatorMacro(elevator, 1, 1)
        self.drive_macro = DriveMacro(dt, 5, 3)
        self.wait_macro = GRTMacro(0.5)  # blank macro just waits
	#self.lower_macro = ElevatorMacro(elevator, -1, 1)
	#self.release_macro = PickupMacro(lead_screw, “release”, 1)
        #self.macros = [self.pickup_macro, self.elevator_macro, self.drive_macro, self.wait_macro, self.lower_macro, self.release_macro]
        self.macros = [self.drive_macro, self.wait_macro]
        super().__init__(macros=self.macros)
       
   
