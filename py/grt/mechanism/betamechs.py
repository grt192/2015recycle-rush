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
        self.fourbar_motor.set(.7)

    def lower(self):
        self.fourbar_motor.set(-.5)

    def stop(self):
        self.fourbar_motor.set(0)

    def elevate_speed(self, power):
        self.fourbar_motor.set(power)

class TwoMotorPickup:
    def __init__(self, motor1, motor2):
        self.motor1 = motor1
        self.motor2 = motor2

    def operate(self, power):
        self.motor1.set(power)
        self.motor2.set(-power)
    def stop(self):
        self.motor1.set(0)
        self.motor2.set(0)