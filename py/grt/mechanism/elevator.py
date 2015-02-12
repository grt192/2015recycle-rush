class Elevator:
    def __init__(self, elevator_motor1, elevator_encoder, winch_servo=None):
        self.elevator_motor1 = elevator_motor1
        
        self.elevator_encoder = elevator_encoder
        self.winch_servo = winch_servo

    def elevate(self):
        if self.winch_servo:
            self.release_winch()
        self.elevator_motor1.set(1)
        

    def lower(self):
        if self.winch_servo:
            self.release_winch()
        self.elevator_motor.set(-1)
        

    def stop(self):
        if self.winch_servo:
            self.engage_winch()
        self.elevator_motor1.set(0)
        

    def elevate_speed(self, power):
        self.elevator_motor1.set(power)
        

    def engage_winch(self):
        self.winch_servo.setAngle(45)

    def release_winch(self):
        self.winch_wervo.setAngle(0)