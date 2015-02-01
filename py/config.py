"""
Config File for Robot
"""


from wpilib import Solenoid, Compressor, DriverStation, CANTalon, DigitalInput

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
from grt.mechanism.betamechs import FourBar, TwoMotorPickup
from grt.mechanism.elevator import Elevator
from grt.mechanism.mechcontroller import MechController
from grt.macro.align_macro import AlignMacro

#DT Talons and Objects

dt_right = CANTalon(1)
dt_r2 = CANTalon(2)
dt_r3 = CANTalon(3)
dt_r4 = CANTalon(4)

dt_left = CANTalon(7)
dt_l2 = CANTalon(8)
dt_l3 = CANTalon(9)
dt_l4 = CANTalon(10)

dt_r2.changeControlMode(CANTalon.ControlMode.Follower)
dt_r3.changeControlMode(CANTalon.ControlMode.Follower)
dt_r4.changeControlMode(CANTalon.ControlMode.Follower)
dt_l2.changeControlMode(CANTalon.ControlMode.Follower)
dt_l3.changeControlMode(CANTalon.ControlMode.Follower)
dt_l4.changeControlMode(CANTalon.ControlMode.Follower)
dt_r2.set(1)
dt_r3.set(1)
dt_r4.set(1)
dt_l2.set(7)
dt_l3.set(7)
dt_l4.set(7)

dt = DriveTrain(dt_left, dt_right, left_encoder=None, right_encoder=None)


#Skeleton sensor poller
#ADD LIMIT SWITCHES FOR ALIGN MACRO
gyro = Gyro(1)
sp = SensorPoller((gyro,))

#Digital inputs
l_switch = DigitalInput(8)
r_switch = DigitalInput(9)

#Macros
a_macro = AlignMacro(dt, l_switch, r_switch, 10) 

# Drive Controllers
driver_stick = Attack3Joystick(0)
xbox_controller = XboxJoystick(1)
ac = ArcadeDriveController(dt, driver_stick, aligner=a_macro)
hid_sp = SensorPoller((driver_stick, xbox_controller))  # human interface devices



#Mech Talons, objects, and controller
fourbar_motor = CANTalon(5)
fourbar = FourBar(fourbar_motor)

elevator_motor = CANTalon(6)
elevator = Elevator(elevator_motor)

motor1 = CANTalon(12)
motor2 = CANTalon(11)
two_motor_pickup = TwoMotorPickup(motor1, motor2)




#make sure to pass the align macro (once defined) to the mech controller
mc = MechController(elevator, fourbar, two_motor_pickup, driver_stick, xbox_controller)

ds = DriverStation.getInstance()





