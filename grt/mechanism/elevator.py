class Elevator:
    def __init__(self, elevator_motor):
        self.elevator_motor = elevator_motor

    def elevate(self):
        self.elevator_motor.set(1)

    def lower(self):
        self.elevator_motor.set(-1)

    def stop(self):
        self.elevator_motor.set(0)
    def elevate_speed(self, power):
    	self.elevator_motor.set(power)