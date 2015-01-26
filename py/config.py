"""
Config File for Robot
"""

__author__ = "Sidd Karamcheti"

from wpilib import Solenoid, Compressor, DriverStation, CANTalon
import wpilib

from grt.sensors.attack_joystick import Attack3Joystick
from grt.sensors.xbox_joystick import XboxJoystick
from grt.sensors.gyro import Gyro
from grt.core import SensorPoller #, Constants
from grt.mechanism.drivetrain import DriveTrain
from grt.mechanism.drivecontroller import ArcadeDriveController
from grt.mechanism.motorset import Motorset
from grt.sensors.ticker import Ticker
from grt.sensors.encoder import Encoder
from teleop_controller import TeleopController
from grt.sensors.talon import Talon
from grt.mechanism.betamechs import Pickup
from grt.mechanism.betamechs import FourBar
from grt.mechanism.elevator import Elevator
from grt.mechanism.mechcontroller import MechController

#import grt.networktables as networktables


#Pin/Port map
#Talons

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


#dt_right = Talon(0) #Motorset((Talon(0), Talon(1)), scalefactors=(-1, 1))
#dt_left = Talon(1) #Motorset((Talon(2), Talon(3)), scalefactors=(-1, 1))
talon_arr = [dt_right, dt_left]


#Solenoids + Relays
compressor_pin = 1
dt_shifter = Solenoid(2)

#Digital Sensors
#left_encoder = Encoder(3, 4, constants['dt_dpp'], reverse=True)
#right_encoder = Encoder(1, 2, constants['dt_dpp'])
pressure_sensor_pin = 14

#Analog Sensors
gyro = Gyro(1)

# Controllers
driver_stick = Attack3Joystick(0)
xbox_controller = XboxJoystick(1)

#Mechs

fourbar_motor = CANTalon(5)
elevator_motor = CANTalon(6)
#elevator_motor.setVoltageRampRate(2000)
#fourbar_motor.setVoltageRampRate(2000)
pickup_pn = Solenoid(1)
pickup = Pickup(pickup_pn)
elevator = Elevator(elevator_motor)
fourbar = FourBar(fourbar_motor)




#Teleop Controllers
mc = MechController(pickup, elevator, fourbar, driver_stick, xbox_controller)

#DT
dt = DriveTrain(dt_left, dt_right, dt_shifter,
                left_encoder=None, right_encoder=None)
ac = ArcadeDriveController(dt, driver_stick)

#Sensor Pollers
sp = SensorPoller((gyro,))
hid_sp = SensorPoller((driver_stick, xbox_controller))  # human interface devices

ds = DriverStation.getInstance()

teleop_controller = TeleopController(driver_stick, ac, talon_arr, sp, hid_sp)


"""
#Compressor
compressor = Compressor(pressure_sensor_pin, compressor_pin)
compressor.Start()
"""

#Mechs

#Teleop Controllers
"""
#Network Tables
#vision_table = networktables.get_table('vision')
#status_table = networktables.get_table('status')
"""

"""
#Diagnostic ticker
def status_tick():
    status_table['l_speed'] = dt.left_motor.Get()
    status_table['r_speed'] = dt.right_motor.Get()
    status_table['voltage'] = ds.GetBatteryVoltage()
    status_table['status'] = 'disabled' if ds.IsDisabled() else 'teleop' if ds.IsOperatorControl() else 'auto'

status_ticker = Ticker(.05)
status_ticker.tick = status_tick


def reset_tick():
    if driver_stick.button10 and driver_stick.button11:
        constants.poll()

reset_ticker = Ticker(1)
reset_ticker.tick = reset_tick
"""
#Autonomous

