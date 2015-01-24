class Elevator:
    def __init__(self, elevator_motor):
        self.elevator_motor = elevator_motor

    def elevate(self):
        self.elevator_motor.Set(0.5)

    def lower(self):
        self.elevator_motor.Set(-0.5)

    def stop(self):
        self.elevator_motor.Set(0)
        