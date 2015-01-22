"""
Config File for Robot
"""

__author__ = "Sidd Karamcheti"

from wpilib import Solenoid, Compressor, DriverStation
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
from grt.mechanism.pickup import Pickup
from grt.mechanism.elevator import Elevator
from grt.mechanism.mechcontroller import MechController

#import grt.networktables as networktables


#Pin/Port map
#Talons
dt_right = Talon(0) #Motorset((Talon(0), Talon(1)), scalefactors=(-1, 1))
dt_left = Talon(1) #Motorset((Talon(2), Talon(3)), scalefactors=(-1, 1))
talon_arr = [dt_right, dt_left]


#Solenoids + Relays
compressor_pin = 1
dt_shifter = Solenoid(1)

#Digital Sensors
#left_encoder = Encoder(3, 4, constants['dt_dpp'], reverse=True)
#right_encoder = Encoder(1, 2, constants['dt_dpp'])
pressure_sensor_pin = 14

#Analog Sensors
gyro = Gyro(1)

# Controllers
driver_stick = Attack3Joystick(0)
xbox_controller = XboxJoystick(1)

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

leadscrew_motor = Talon(PUTANUMBERHERE)
elevator_motor = Talon(PUTNUMBERHERETOO)
pickup = Pickup(leadscrew_motor)
elevator = Elevator(elevator_motor)

#Teleop Controllers
mc = MechController(pickup, elevator, driver_stick)
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

