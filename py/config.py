"""
Config File for Robot
"""


from wpilib import Solenoid, Compressor, DriverStation, DigitalInput
import wpilib
import math

from wpilib import DriverStation, CANTalon, DigitalInput

from grt.sensors.attack_joystick import Attack3Joystick
from grt.sensors.xbox_joystick import XboxJoystick
from grt.sensors.gyro import Gyro
from grt.core import SensorPoller
from grt.mechanism.drivetrain import DriveTrain
from grt.mechanism.drivecontroller import ArcadeDriveController
from grt.mechanism.motorset import Motorset
from grt.sensors.ticker import Ticker
from grt.sensors.encoder import Encoder
from grt.sensors.talon import Talon
from grt.sensors.ultrasonic import Ultrasonic
from grt.mechanism.betamechs import FourBar, TwoMotorPickup
from grt.mechanism.elevator import Elevator
from grt.mechanism.mechcontroller import MechController
#from grt.macro.align_macro import AlignMacro
from grt.autonomous.basic_auto import BasicAuto
from grt.autonomous.one_bin_stealer_auto import OneBinSteal
from grt.autonomous.backup_bin_stealer import BackupBinSteal
from teleop_controller import TeleopController
from record_controller import RecordMacro, PlaybackMacro
from collections import OrderedDict

from grt.sensors.imu_simple import IMUSimple
from grt.autonomous.crazy_auto import CrazyAuto

imu = IMUSimple()

#from grt.sensors.switch import Switch

#import grt.networktables as networktables

auto_enabled = True
recording_enabled = False


#Pin/Port map


#Talons

#dt_right_alt = Talon(1)
#dt_left_alt = Talon(2)

dt_right = Motorset((CANTalon(id) for id in range(1, 5)))
dt_left = Motorset((CANTalon(id) for id in range(7, 11)))

gyro = Gyro(1)

left_encoder = Encoder(0, 1, distance_per_rev=(4 * math.pi), reverse=True)
right_encoder = Encoder(2, 3, distance_per_rev=(4*math.pi))

dt = DriveTrain(dt_left, dt_right, left_encoder=left_encoder, right_encoder=right_encoder)

elevator_motor = CANTalon(11)
elevator_motor_2 = CANTalon(12)
elevator_motor_2.changeControlMode(CANTalon.ControlMode.Follower)
elevator_motor_2.set(11)



elevator_distance_per_rev = 1.273 * math.pi
#Changed to 120 for omega 2!
elevator_cpr = 120
elevator_encoder = Encoder(4, 5, distance_per_rev=elevator_distance_per_rev, cpr=elevator_cpr, reverse=False)
top_switch = DigitalInput(13)
bottom_limit_switch = DigitalInput(9)
bottom_switch = DigitalInput(8)
left_switch = DigitalInput(7)
right_switch = DigitalInput(6)
ultrasonic = Ultrasonic(0)
elevator = Elevator(elevator_motor, elevator_encoder, left_switch=left_switch, right_switch=right_switch, dt=dt, top_switch=top_switch, bottom_switch=bottom_switch, bottom_limit_switch=bottom_limit_switch, ultrasonic=ultrasonic)

fourbar_motor = CANTalon(5)
fourbar_distance_per_rev = 1
fourbar_cpr = 120
fourbar_encoder = Encoder(10, 11, distance_per_rev=fourbar_distance_per_rev, cpr=fourbar_cpr, reverse=False)
fourbar = FourBar(fourbar_motor, fourbar_encoder)

talon_arr_basic = [dt_right, dt_left, elevator.lift_macro]
talon_arr = [dt_right, dt_left, elevator.lift_macro, fourbar_motor]
#talon_arr_macro = [dt_right, dt_left, elevator.lift_macro, elevator_motor]
record_macro = RecordMacro(talon_arr)

basic_auto = BasicAuto(dt, elevator, talon_arr_basic)
one_bin_steal = OneBinSteal(talon_arr)
backup_bin_steal = BackupBinSteal(talon_arr)
playback_macro = backup_bin_steal.playback_macro

crazy_auto = CrazyAuto(talon_arr, dt, imu, ultrasonic)


sp = SensorPoller((gyro, left_encoder, right_encoder, elevator_encoder, ultrasonic))

#Analog Sensors

# Controllers
driver_stick = Attack3Joystick(0)
xbox_controller = XboxJoystick(1)
ac = ArcadeDriveController(dt, driver_stick, record_macro, playback_macro)
hid_sp = SensorPoller((driver_stick, xbox_controller))  # human interface devices

if recording_enabled:
	from record_controller import RecordController, PlaybackController
	from collections import OrderedDict
	instructions = OrderedDict([("1, <class 'grt.sensors.talon.Talon'>", [0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.8, -0.8, -0.8, -0.8, -0.8, -0.8, -0.8, -0.8, -0.8, -0.8, -0.8, -0.8, -0.8, -0.8, -0.8, -0.8, -0.8, -0.8, 0.2571428571428571, 0.2571428571428571, 0.2571428571428571, 0.2571428571428571, 0.2571428571428571, 0.2571428571428571, 0.2571428571428571, 0.2571428571428571, 0.2571428571428571, 0.2571428571428571, 0.2571428571428571, 0.2571428571428571, 0.2571428571428571, 0.2571428571428571, 0.2571428571428571, 0.2571428571428571, 0.2571428571428571, -0.6285714285714286, -0.6285714285714286, -0.6285714285714286, -0.6285714285714286, -0.6285714285714286, -0.6285714285714286, -0.6285714285714286, -0.6285714285714286, -0.6285714285714286, -0.6285714285714286, -0.6285714285714286, -0.6285714285714286, -0.6285714285714286, -0.6285714285714286, -0.6285714285714286, -0.6285714285714286, -0.6285714285714286, -0.6285714285714286, -0.6285714285714286, -0.6285714285714286, -1.1714285714285715, -1.1714285714285715, -1.1714285714285715, -1.1714285714285715, -1.1714285714285715, -1.1714285714285715, -1.1714285714285715, -1.1714285714285715, -1.1714285714285715, -1.1714285714285715, -1.1714285714285715, -1.1714285714285715, -1.1714285714285715, -1.1714285714285715, -1.1714285714285715, -1.1714285714285715, -1.1714285714285715, -1.1714285714285715, -1.1714285714285715, -1.1714285714285715, -1.1714285714285715, -1.1714285714285715, -1.1714285714285715, -1.1714285714285715, -1.1714285714285715, 0.1428571428571429, 0.1428571428571429, 0.1428571428571429, 0.1428571428571429, 0.1428571428571429, 0.1428571428571429, 0.1428571428571429, 0.1428571428571429, 0.1428571428571429, 0.1428571428571429, 0.1428571428571429, 0.1428571428571429, 0.1428571428571429, 0.1428571428571429, 0.1428571428571429, 0.1428571428571429, 0.1428571428571429, 0.1428571428571429, 0.1428571428571429, 0.1428571428571429, 0.1428571428571429, 0.1428571428571429, 0.1428571428571429, 0.1428571428571429, 0.1428571428571429, 1.2571428571428571, 1.2571428571428571, 1.2571428571428571, 1.2571428571428571, 1.2571428571428571, 1.2571428571428571, 1.2571428571428571, 1.2571428571428571, 1.2571428571428571, 1.2571428571428571, 1.2571428571428571, 1.2571428571428571, 1.2571428571428571, 1.2571428571428571, 1.2571428571428571, 1.2571428571428571, 1.2571428571428571, 1.2571428571428571, 1.2571428571428571, 1.2571428571428571, 1.2571428571428571, 1.2571428571428571, 0.17142857142857137, 0.17142857142857137, 0.17142857142857137, 0.17142857142857137, 0.17142857142857137]), ("2, <class 'grt.sensors.talon.Talon'>", [0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.8, -0.8, -0.8, -0.8, -0.8, -0.8, -0.8, -0.8, -0.8, -0.8, -0.8, -0.8, -0.8, -0.8, -0.8, -0.8, -0.8, -0.8, 0.2571428571428571, 0.2571428571428571, 0.2571428571428571, 0.2571428571428571, 0.2571428571428571, 0.2571428571428571, 0.2571428571428571, 0.2571428571428571, 0.2571428571428571, 0.2571428571428571, 0.2571428571428571, 0.2571428571428571, 0.2571428571428571, 0.2571428571428571, 0.2571428571428571, 0.2571428571428571, 0.2571428571428571, -0.6285714285714286, -0.6285714285714286, -0.6285714285714286, -0.6285714285714286, -0.6285714285714286, -0.6285714285714286, -0.6285714285714286, -0.6285714285714286, -0.6285714285714286, -0.6285714285714286, -0.6285714285714286, -0.6285714285714286, -0.6285714285714286, -0.6285714285714286, -0.6285714285714286, -0.6285714285714286, -0.6285714285714286, -0.6285714285714286, -0.6285714285714286, -0.6285714285714286, -1.1714285714285715, -1.1714285714285715, -1.1714285714285715, -1.1714285714285715, -1.1714285714285715, -1.1714285714285715, -1.1714285714285715, -1.1714285714285715, -1.1714285714285715, -1.1714285714285715, -1.1714285714285715, -1.1714285714285715, -1.1714285714285715, -1.1714285714285715, -1.1714285714285715, -1.1714285714285715, -1.1714285714285715, -1.1714285714285715, -1.1714285714285715, -1.1714285714285715, -1.1714285714285715, -1.1714285714285715, -1.1714285714285715, -1.1714285714285715, -1.1714285714285715, 0.1428571428571429, 0.1428571428571429, 0.1428571428571429, 0.1428571428571429, 0.1428571428571429, 0.1428571428571429, 0.1428571428571429, 0.1428571428571429, 0.1428571428571429, 0.1428571428571429, 0.1428571428571429, 0.1428571428571429, 0.1428571428571429, 0.1428571428571429, 0.1428571428571429, 0.1428571428571429, 0.1428571428571429, 0.1428571428571429, 0.1428571428571429, 0.1428571428571429, 0.1428571428571429, 0.1428571428571429, 0.1428571428571429, 0.1428571428571429, 0.1428571428571429, 1.2571428571428571, 1.2571428571428571, 1.2571428571428571, 1.2571428571428571, 1.2571428571428571, 1.2571428571428571, 1.2571428571428571, 1.2571428571428571, 1.2571428571428571, 1.2571428571428571, 1.2571428571428571, 1.2571428571428571, 1.2571428571428571, 1.2571428571428571, 1.2571428571428571, 1.2571428571428571, 1.2571428571428571, 1.2571428571428571, 1.2571428571428571, 1.2571428571428571, 1.2571428571428571, 1.2571428571428571, 0.17142857142857137, 0.17142857142857137, 0.17142857142857137, 0.17142857142857137, 0.17142857142857137])])
	talon_arr = [dt_right, dt_left]
	record_controller = RecordController([talon_arr[0], talon_arr[1]])
	playback_controller = PlaybackController(instructions, talon_arr, revert_controller=drive_controller)
	teleop_controller = TeleopController(sp, hid_sp, driver_stick, ac, record_controller, playback_controller)
else:
	teleop_controller = TeleopController(sp, hid_sp)

motor1 = CANTalon(14)
motor2 = CANTalon(15)
two_motor_pickup = TwoMotorPickup(motor1, motor2)

mc = MechController(elevator, fourbar, two_motor_pickup, driver_stick, xbox_controller)

ds = DriverStation.getInstance()
