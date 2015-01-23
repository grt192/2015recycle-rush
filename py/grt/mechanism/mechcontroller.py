class MechController:
    def __init__(self, pickup_mech, elevator, fourbar, driver_joystick):
        self.pickup_mech = pickup_mech
        self.elevator = elevator
        self.fourbar = fourbar
        self.driver_joystick = driver_joystick
        driver_joystick.add_listener(self._driver_joystick_listener)

    def _driver_joystick_listener(self, sensor, state_id, datum):
        if state_id == 'button3':
            if datum:
                 self.pickup_mech.pickup()

        if state_id == 'button2':
            if datum:
                self.pickup_mech.release()

        if state_id == 'button4':
            if datum:
                self.elevator.elevate()
            else:
                self.elevator.stop()

        if state_id == 'button5':
            if datum:
                self.elevator.lower()
            else:
                self.elevator.stop()

        if state_id == ‘button6’:
            if datum:
                self.fourbar.elevate()
            else:
                self.fourbar.stop()

        if state_id == ‘button7’:
            if datum:
                self.fourbar.lower()
            else:
                self.fourbar.stop()