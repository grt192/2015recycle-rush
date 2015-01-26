class MechController:
    def __init__(self, pickup_mech, elevator, fourbar, driver_joystick, xbox_controller):
        self.pickup_mech = pickup_mech
        self.elevator = elevator
        self.fourbar = fourbar
        self.driver_joystick = driver_joystick
        self.xbox_controller = xbox_controller
        driver_joystick.add_listener(self._driver_joystick_listener)
        xbox_controller.add_listener(self._xbox_controller_listener)

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
                    self.fourbar.elevate_speed(datum)
                else:
                    self.fourbar.stop()


    def _driver_joystick_listener(self, sensor, state_id, datum):
        if state_id == 'button6':
            if datum:
                 self.pickup_mech.pickup()

        if state_id == 'button7':
            if datum:
                self.pickup_mech.release()

        if state_id == 'button3':
            if datum:
                self.elevator.elevate()
            else:
                self.elevator.stop()

        if state_id == 'button2':
            if datum:
                self.elevator.lower()
            else:
                self.elevator.stop()

        if state_id == 'button11':
            if datum:
                self.fourbar.elevate()
            else:
                self.fourbar.stop()

        if state_id == 'button10':
            if datum:
                self.fourbar.lower()
            else:
                self.fourbar.stop()