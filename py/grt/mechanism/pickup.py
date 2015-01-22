class Pickup
    def __init__(self, leadscrew_motor):
        self.leadscrew_motor = leadscrew_motor

    def pickup(self):
        self.leadscrew_motor.Set(0.2)

    def release(self):
        self.leadscrew_motor.Set(-0.2)

    def stop(self):
        self.leadscrew_motor.Set(0)
		