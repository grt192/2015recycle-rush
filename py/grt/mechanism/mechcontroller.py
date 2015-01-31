class MechController:
    def __init__(self, elevator, fourbar, two_motor_pickup, driver_joystick, xbox_controller, aligner=None):
        self.elevator = elevator
        self.fourbar = fourbar
        self.two_motor_pickup = two_motor_pickup
        self.driver_joystick = driver_joystick
        self.xbox_controller = xbox_controller
        driver_joystick.add_listener(self._driver_joystick_listener)
        xbox_controller.add_listener(self._xbox_controller_listener)
        self.aligner = aligner

    def _xbox_controller_listener(self, sensor, state_id, datum):
        if state_id == 'r_y_axis':
            if datum:
                if abs(datum) > .05:
                    self.elevator.elevate_speed(datum)
                else:
                    self.elevator.stop()
        if state_id == 'l_y_axis':
            if datum:
                if abs(datum) > .05:
                    self.two_motor_pickup.operate(datum)
                else:
                    self.two_motor_pickup.stop()
        if state_id == "l_shoulder":
            if datum:
                self.fourbar.elevate_speed(.8)
            else:
                self.fourbar.stop()

        if state_id == "r_shoulder":
            if datum:
                self.fourbar.elevate_speed(-.8)
            else:
                self.fourbar.stop()
        if state_id == 'a_button' and self.aligner:
            if datum:
                self.aligner.align()
                print('THE A BUTTON HAS BEEN PRESSED')


    def _driver_joystick_listener(self, sensor, state_id, datum):
        pass