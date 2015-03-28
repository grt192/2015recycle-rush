import wpilib


class GRTCANTalon:
    def __init__(self, channel):
        self.t = wpilib.CANTalon(channel)
        self.channel = channel

    def set(self, power):
        self.t.set(power)

    def Get(self):
        # print(self.t.Get())
        return self.t.get()

    def GetChannel(self):
        return self.channel