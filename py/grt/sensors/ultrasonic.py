from wpilib import AnalogInput
from grt.core import Sensor


class Ultrasonic(Sensor):
    distance = 0

    def __init__(self, channel, mv_per_in=9.8):
        super().__init__()
        self.mv_per_in = mv_per_in #millivolts per inch
        self.u = AnalogInput(channel)

    def poll(self):
        self.distance = self.u.getVoltage() * 1000 / self.mv_per_in
        print(self.distance)
