

from . import MacroSequence
from grt.core import Constants, GRTMacro
from collections import OrderedDict
from record_controller import PlaybackMacro
from grt.macro.turn_macro import TurnMacro
from grt.macro.drive_macro import DriveMacro
from grt.macro.calibrate_macro import CalibrateMacro



class CrazyAuto(MacroSequence):
    """
    Crazy auto mode. Picks up one bin with a recording, turns 90 degrees, drives across
    the field, turns back 90 degrees to face the step, calibrates its position with an 
    ultrasonic sensor, and then runs another record to pick up a second bin.
    """

    def __init__(self, talon_arr, dt, gyro, ultrasonic):
        first_bin_steal_instructions = OrderedDict([("1, <class 'wpilib.cantalon.CANTalon'>", [0.005865102639296188, 0.005865102639296188, 0.005865102639296188, 0.005865102639296188, 0.005865102639296188, 0.011730205278592375, 0.024437927663734114, 0.024437927663734114, 0.024437927663734114, 0.024437927663734114, 0.024437927663734114, 0.024437927663734114, 0.024437927663734114, 0.024437927663734114, 0.024437927663734114, 0.024437927663734114, 0.024437927663734114, 0.024437927663734114, 0.024437927663734114, 0.024437927663734114, 0.024437927663734114, 0.024437927663734114, 0.024437927663734114, 0.024437927663734114, 0.024437927663734114, 0.024437927663734114, 0.024437927663734114, 0.024437927663734114, 0.024437927663734114, -0.024437927663734114, -0.05571847507331378, -0.1573802541544477, -0.21994134897360704, -0.26392961876832843, -0.26392961876832843, -0.26392961876832843, -0.26392961876832843, -0.26392961876832843, -0.26392961876832843, -0.26392961876832843, -0.23264907135874877, -0.26392961876832843, -0.23264907135874877, -0.01857282502443793, -0.01857282502443793, -0.04985337243401759, -0.03714565004887586, 0.005865102639296188, 0.005865102639296188, 0.13098729227761485, 0.3870967741935484, 0.4995112414467253, 0.4995112414467253, 0.4995112414467253, 0.4496578690127077, 0.3870967741935484, 0.3870967741935484, 0.4496578690127077, 0.4496578690127077, 0.4496578690127077, 0.4496578690127077, 0.4496578690127077, 0.3870967741935484, 0.2932551319648094, 0.13685239491691104, -0.03714565004887586, 0.05571847507331378, 0.011730205278592375, 0.011730205278592375, 0.005865102639296188, 0.005865102639296188, 0.005865102639296188, -0.01857282502443793, -0.01857282502443793, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.01857282502443793]), ("7, <class 'wpilib.cantalon.CANTalon'>", [-0.005865102639296188, -0.005865102639296188, -0.005865102639296188, -0.005865102639296188, -0.005865102639296188, 0.0, 0.011730205278592375, 0.011730205278592375, 0.011730205278592375, 0.011730205278592375, 0.011730205278592375, 0.011730205278592375, 0.011730205278592375, 0.011730205278592375, 0.011730205278592375, 0.011730205278592375, 0.011730205278592375, 0.011730205278592375, 0.011730205278592375, 0.011730205278592375, 0.011730205278592375, 0.011730205278592375, 0.011730205278592375, 0.011730205278592375, 0.011730205278592375, 0.011730205278592375, 0.011730205278592375, 0.011730205278592375, 0.011730205278592375, 0.06256109481915934, 0.05571847507331378, 0.1573802541544477, 0.21994134897360704, 0.26392961876832843, 0.26392961876832843, 0.26392961876832843, 0.26392961876832843, 0.26392961876832843, 0.26392961876832843, 0.26392961876832843, 0.13196480938416422, 0.11241446725317693, 0.23264907135874877, 0.03128054740957967, 0.03128054740957967, 0.06256109481915934, 0.04985337243401759, 0.005865102639296188, 0.005865102639296188, -0.09286412512218964, -0.34995112414467255, -0.46236559139784944, -0.46236559139784944, -0.46236559139784944, -0.46236559139784944, -0.34995112414467255, -0.34995112414467255, -0.4115347018572825, -0.4115347018572825, -0.4115347018572825, -0.4115347018572825, -0.4115347018572825, -0.34995112414467255, -0.2561094819159335, -0.187683284457478, 0.005865102639296188, -0.043010752688172046, 0.0, 0.0, 0.005865102639296188, 0.005865102639296188, 0.005865102639296188, 0.03128054740957967, 0.03128054740957967, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.03128054740957967]), ("100, <class 'grt.macro.assistance_macros.ElevatorMacro'>", [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]), ("5, <class 'wpilib.cantalon.CANTalon'>", [0.0, 0.0, 0.0, 0.0, 0.0, -0.4995112414467253, -0.4995112414467253, -0.4995112414467253, -0.4995112414467253, -0.4995112414467253, -0.4995112414467253, -0.4995112414467253, -0.4995112414467253, -0.4995112414467253, -0.4995112414467253, -0.4995112414467253, -0.4995112414467253, -0.4995112414467253, -0.4995112414467253, -0.4995112414467253, -0.4995112414467253, -0.4995112414467253, -0.4995112414467253, -0.4995112414467253, -0.4995112414467253, -0.4995112414467253, -0.4995112414467253, -0.4995112414467253, -0.4995112414467253, -0.4995112414467253, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.6999022482893451, 0.6999022482893451, 0.6999022482893451, 0.6999022482893451, 0.6999022482893451, 0.6999022482893451, 0.6999022482893451, 0.6999022482893451, 0.6999022482893451, 0.6999022482893451, 0.6999022482893451, 0.6999022482893451, 0.6999022482893451, 0.6999022482893451, 0.6999022482893451, 0.6999022482893451, 0.6999022482893451, 0.6999022482893451, 0.6999022482893451, 0.6999022482893451, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])])
        second_bin_steal_instructions = first_bin_steal_instructions
        self.first_bin_steal = PlaybackMacro(first_bin_steal_instructions, talon_arr)
        self.first_turn_macro = TurnMacro(dt, gyro, -90, timeout=2)
        self.drive_macro = DriveMacro(dt, 120, timeout=3)
        self.second_turn_macro = TurnMacro(dt, gyro, 90, timeout=2)
        self.calibrate_macro = CalibrateMacro(dt, ultrasonic, 79, timeout=1)
        self.second_bin_steal = PlaybackMacro(second_bin_steal_instructions, talon_arr)
        self.macros = [self.first_bin_steal, self.first_turn_macro, self.drive_macro, self.second_turn_macro, self.calibrate_macro, self.second_bin_steal]
        super().__init__(macros=self.macros)  