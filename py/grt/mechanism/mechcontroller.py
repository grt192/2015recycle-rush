class MechController:
    def __init__(self, elevator, fourbar, two_motor_pickup, driver_joystick, xbox_controller):
        self.elevator = elevator
        self.fourbar = fourbar
        self.two_motor_pickup = two_motor_pickup
        self.driver_joystick = driver_joystick
        self.xbox_controller = xbox_controller
        driver_joystick.add_listener(self._driver_joystick_listener)
        xbox_controller.add_listener(self._xbox_controller_listener)
        self.trigger_count = 0
        self.button9_count = 0
        self.last_height = 0
        self.manual_control = False

    def _xbox_controller_listener(self, sensor, state_id, datum):
        if self.manual_control:
            if state_id == 'r_y_axis':
                if datum:
                    if abs(datum) > .05:
                        self.elevator.elevate_speed_safe(datum)
                    else:
                        self.elevator.stop()
        if state_id == 'l_y_axis':
            if datum:
                if abs(datum) > .05:
                    self.fourbar.elevate_speed(datum)
                else:
                    self.fourbar.stop()
        if state_id == "back_button": #Makes it hard to accidentally press this.
            if datum:
                self.elevator.lift_macro.enabled = False
                self.manual_control = True
        if state_id == "start_button":
            if datum:
                self.elevator.lift_macro.enabled = True
                self.manual_control = False
        """                    
        if state_id == "l_shoulder":
            if datum:
                self.two_motor_pickup.operate(.5)
                
            else:
                self.two_motor_pickup.stop()

        if state_id == "r_shoulder":
            if datum:
                self.two_motor_pickup.operate(.5)
            else:
                self.two_motor_pickup.stop()
        """



    def _driver_joystick_listener(self, sensor, state_id, datum):
        if state_id == "z_axis":
            height = datum
            if abs(height - self.last_height) > .3:
                 #self.driver_joystick.j.getZ()
                if height >= -1 and height < -3/5:
                    self.elevator.set_state('level0')
                    print("Level 0!")
                elif height > -3/5 and height < -1/5:
                    print("Level 0.5!")
                    self.elevator.set_state('level0.5')
                elif height > -1/5 and height < 1/5:
                    self.elevator.set_state('level1')
                elif height > 1/5 and height < 3/5:
                    self.elevator.set_state('level2')
                elif height > 3/5 and height <= 1:
                    self.elevator.set_state('level3')
                else:
                    print('Unknown range set!')
                self.last_height = height

        if state_id == 'trigger':
            if datum:
                #if self.trigger_count == 1:
                #    self.trigger_count = 0
                #    self.elevator.release()
                #if self.trigger_count == 0:
                #    self.elevator.set_state('level3')
                #    self.trigger_count += 1
                if self.elevator.lift_macro.current_state is "level0":
                    self.elevator.set_state('level3')
                else:
                    self.elevator.lower_half_step()
            
            #if datum:
            #    self.elevator.set_state('level3')
            #else:
            #   self.elevator.set_state('level0')
        if state_id == "button57":
            if datum:
                self.elevator.pickup()
            else:
                self.elevator.align_macro.enabled = False
        if state_id == "button6":
            if datum:
                self.elevator.toggle_step()


        if state_id == "button3":
            if datum:
                self.fourbar.elevate()
            else:
                self.fourbar.stop()
        if state_id == "button2":
            if datum:
                self.fourbar.lower()
            else:
                self.fourbar.stop()
        

        """
        if state_id == 'button10':
            if datum:
                self.elevator.abort()

        #Springloaded button 9
        if state_id == 'button9':
            if datum:
                pass
            else:
                self.elevator.spring()
        """

    def _universal_abort_listener(self, sensor, state_id, datum):
        if state_id == 'button8':
            if datum:
                self.elevator.kill_all_macros()



