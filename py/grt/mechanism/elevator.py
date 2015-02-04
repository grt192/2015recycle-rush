class Elevator:
    def __init__(self, elevator_motor, elevator_encoder, winch_servo=None):
        self.elevator_motor = elevator_motor
        self.elevator_encoder = elevator_encoder
        self.winch_servo = winch_servo

    def elevate(self):
        if self.winch_servo:
            self.release_winch()
        self.elevator_motor.set(1)

    def lower(self):
        if self.winch_servo:
            self.release_winch()
        self.elevator_motor.set(-1)

    def stop(self):
        if self.winch_servo:
            self.engage_winch()
        self.elevator_motor.set(0)

    def elevate_speed(self, power):
    	self.elevator_motor.set(power)

    def engage_winch(self):
        self.winch_servo.setAngle(45)

    def release_winch(self):
        self.winch_wervo.setAngle(0)