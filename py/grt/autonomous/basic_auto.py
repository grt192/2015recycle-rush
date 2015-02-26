"""
basic_auto.py
"""


__author__ = "Abraham Ryzhik"

from . import MacroSequence
from grt.core import Constants, GRTMacro
from grt.macro.drive_macro import DriveMacro
from grt.macro.elevator_macro import ElevatorMacro
from collections import OrderedDict
from record_controller import PlaybackMacro



class BasicAuto(MacroSequence):
    """
    Basic autonomous mode. Drives and shoots. Pretty straightforward.
    """

    def __init__(self, dt, elevator, talon_arr):
        instructions = OrderedDict([("1, <class 'wpilib.cantalon.CANTalon'>", [-0.015640273704789834, -0.015640273704789834, -0.015640273704789834, -0.015640273704789834, -0.015640273704789834, -0.015640273704789834, -0.015640273704789834, 0.04594330400782014, 0.0, 0.0, 0.0, -0.07038123167155426, -0.3704789833822092, -0.5581622678396871, -0.6373411534701857, -0.5034213098729228, -0.46432062561094817, -0.5268817204301075, -0.5112414467253177, -0.41642228739002934, -0.3460410557184751, -0.3304007820136852, -0.3069403714565005, -0.3069403714565005, -0.2913000977517107, -0.2678396871945259, -0.2678396871945259, -0.2678396871945259, -0.3304007820136852, -0.3460410557184751, -0.36950146627565983, -0.2668621700879765, -0.007820136852394917, 0.022482893450635387, 0.022482893450635387, 0.022482893450635387]), ("7, <class 'wpilib.cantalon.CANTalon'>", [-0.015640273704789834, -0.015640273704789834, -0.015640273704789834, -0.015640273704789834, -0.015640273704789834, -0.015640273704789834, -0.015640273704789834, 0.04594330400782014, 0.0, 0.0, 0.0, 0.039100684261974585, 0.4946236559139785, 0.5581622678396871, 0.5747800586510264, 0.44086021505376344, 0.47996089931573804, 0.41642228739002934, 0.40078201368523947, 0.41642228739002934, 0.3616813294232649, 0.37732160312805474, 0.35386119257087, 0.35386119257087, 0.33822091886608013, 0.3616813294232649, 0.3616813294232649, 0.3616813294232649, 0.2825024437927664, 0.2825024437927664, 0.2590420332355816, 0.20430107526881722, 0.10166177908113393, 0.022482893450635387, 0.022482893450635387, 0.022482893450635387]), ("100, <class 'grt.macro.assistance_macros.ElevatorMacro'>", [0, 0, 0, 0, 0, 0, 0, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 0, 0, 0, 0, 0, 0])])
        self.playback_macro = PlaybackMacro(instructions, talon_arr)
        self.drive_macro = DriveMacro(dt, 24-5, 300)
        self.elevator_macro = ElevatorMacro(elevator, 750, 2)
        self.drive_macro2 = DriveMacro(dt, 70-5, 300) #units are in inches
        #self.wait_macro = GRTMacro(0.5)  # blank macro just waits
        #self.drive_macro2 = DriveMacro(dt, 70-5, 300) #units are in inches
        self.elevator_macro2 = ElevatorMacro(elevator, -550, 1)
        self.macros = [self.playback_macro]
        #[self.drive_macro, self.elevator_macro, self.drive_macro2, self.elevator_macro2]
        super().__init__(macros=self.macros)  