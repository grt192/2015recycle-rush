class Pickup:
    def __init___(self, clamp_pn):
        self.clamp_pn = clamp_pn

    def pickup(self):
        self.clamp_pn.Set(true)

    def release(self):
        self.clamp_pn.Set(false)

class FourBar:
    def __init__(self, fourbar_motor):
        self.fourbar_motor = fourbar_motor

    def elevate(self):
        self.fourbar_motor.Set(0.5)

    def lower(self):
        self.fourbar_motor.Set(-0.5)

    def stop(self):
        self.fourbar_motor.Set(0)