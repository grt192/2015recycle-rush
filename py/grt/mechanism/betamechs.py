class Pickup:
    def __init__(self, clamp_pn):
        self.clamp_pn = clamp_pn

    def pickup(self):
        self.clamp_pn.set(1)

    def release(self):
        self.clamp_pn.set(0)

class FourBar:
    def __init__(self, fourbar_motor):
        self.fourbar_motor = fourbar_motor

    def elevate(self):
        self.fourbar_motor.set(1)

    def lower(self):
        self.fourbar_motor.set(-.5)

    def stop(self):
        self.fourbar_motor.set(0)

    def elevate_speed(self, power):
        self.fourbar_motor.set(power)