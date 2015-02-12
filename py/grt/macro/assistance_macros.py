
from grt.core import GRTMacro
import wpilib
import threading
import time



class ReleaseMacro(GRTMacro):
    def __init__(self, elevator, dt, timeout=None):
        super().__init__(timeout)
        self.left_switch = elevator.left_switch
        self.right_switch = elevator.right_switch
        self.elevator_motor = elevator.elevator_motor #change how the motor is being called!
        #ie. use the elevator's functions
        elevator.running_macros.append(self)
        self.enabled = False
        self.run_threaded()
        self.dt = dt
    #while any switches are pressed, lower elevator
    def macro_periodic(self):
        if self.enabled:
            if self.left_switch or self.right_switch:
                self.elevator.lower()
            else:
                self.elevator.stop()
                self.dt.set_dt_output(-.5, -.5)
                time.sleep(.5)
                self.dt.set_dt_output(0, 0)
                self.enabled = False
                #self.kill()
    def macro_stop(self):
        self.elevator.stop()
        self.dt.set_dt_output(0)

    def release(self):
        #self.run_threaded() #forces the macro to thread
        self.enabled = True


class AlignMacro(GRTMacro):
    '''
    Using limit switch info, automatically
    align the pickup with a tote.  
    '''

    def __init__(self, elevator, dt, timeout=None):
        super().__init__(timeout)

        self.dt = dt
        self.l_switch = elevator.left_switch
        self.r_switch = elevator.right_switch
        self.aligning = False
        self.enabled = False
        self.run_threaded()

    def macro_periodic(self):
        '''
        Have the robot align itself by ramming into a box
        when it is reasonably close to it
        '''
        ramming_power = 0.2
        turning_power = 0.2
        weak_turning = 0.1
        '''
        while(self.l_switch.get() and self.r_switch.get() and self.aligning ):
            #double check to make sure if this is the correct way to 
            #see if limit switches are pressed. 
            #"While neither switch is pressed" (i.e. both Gets give True)
            self.dt.set_dt_output(ramming_power, ramming_power)
    
            ##### TESTING STUFF #####
            #print('Left limit switch state: %f, Right limit switch state: %f'%(self.l_switch.get(), self.r_switch.get())
       '''
        if self.enabled:
            if self.l_switch.get() and self.r_switch.get():
                self.dt.set_dt_output(ramming_power, ramming_power)
            elif not(self.l_switch.get() or self.r_switch.get()):
                #if both buttons are pressed (both are False)
                self.dt.set_dt_output(0, 0)
                print('ALIGNED')
                #self.kill()
                self.enabled = False
                #stop the robot 
            elif self.l_switch.get():
                #the right switch is pressed (because the left is not)
                #shut off the right side to turn into position
                self.dt.set_dt_output(turning_power, weak_turning)
            else:
                #the left switch is pressed (because the right is not)
                #shut off the left side to turn into position
                self.dt.set_dt_output(weak_turning, turning_power)
                #come to a stop
            #print('ALIGNED')

    def align(self):
        #self.run_threaded()
        self.enabled = True

    def wait_for_align(self):
        #self.run_linear()
        self.process.join(timeout=2)

    
    def macro_stop(self):
        #self.aligning = False
        self.dt.set_dt_output(0, 0)

    #def wait_for_align(self):
        #Do the same thing here. NOT threaded.




#constants = Constants()


class ElevatorMacro(GRTMacro):
    """
    Drive Macro; drives forwards a certain distance while
    maintaining orientation
    """
    leftSF = 1
    rightSF = -1
    distance = None
    previously_on_target = False

    def __init__(self, elevator, distance=0, timeout=None):
        """
        Pass drivetrain, distance to travel (ft), and timeout (secs)
        """
        super().__init__(timeout)
        self.elevator= elevator
        self.distance = distance
        self.elevator_encoder = elevator.elevator_encoder
        self.STATE_DICT = {'level0' : 0, 'level0.5' : 500, 'level1' : 1000, 'level2' : 1500, 'level3' : 2000, 'level4' : 2500}
        self.setpoint = distance
        self.zero = self.elevator_encoder.e.getDistance()
        self.current_state = 'level0'
        self.run_threaded()

    def macro_initialize(self):
        self.initial_distance = self.elevator_encoder.e.getDistance()
        print("Initialized")

    def macro_periodic(self):
        """
        self.initial_distance = self.elevator_encoder.e.getDistance()
        print(self.initial_distance)
        if(self.setpoint>self.initial_distance):
            while(self.traveled_distance() < self.setpoint * .8):
                print("travel: %f" % self.traveled_distance())
                self.elevator.elevate_speed(.6)
                if not self.running:
                    print("Clearing close")
                    return
            while(self.traveled_distance() < self.setpoint):
                print("half power travel: %f" % self.traveled_distance())
                self.elevator.elevate_speed(.3)
            self.elevator.stop()
        elif(self.setpoint<self.initial_distance):
            while(self.traveled_distance() > self.setpoint * .8):
                print("travel: %f" % self.traveled_distance())
                self.elevator.elevate_speed(-.6)
            while(self.traveled_distance() > self.setpoint):
                print("half power travel: %f" % self.traveled_distance())
                self.elevator.elevate_speed(-.3)
            self.elevator.stop()
        print("Cleared close")
        self.terminate()
        """
        #print("Polling")
        #print(self.initial_distance)
        #print(self.zero)

        #Move initial distance logic to a special if statement
        # that gets called only once when the macro is first enabled.
        # self.initialize() calls will be useless for these macros.
        self.ERROR = self.setpoint - self.elevator_encoder.distance
        #If the setpoint is above the current distance.
        if self.ERROR >= 0:
            #print("Started")
            #if self.ERROR < self.setpoint * .8:
            #    self.elevator.elevate_speed(.6)
            #elif self.elevator_encoder.distance < self.setpoint:
            #    self.elevator.elevate_speed(.3)
            if self.ERROR > 100 and abs(self.ERROR) > 50:
                self.elevator.elevate_speed(.6)
            elif self.ERROR <= 100 and self.ERROR > 50:
                self.elevator.elevate_speed(.1)
            if self.ERROR <= 50:
                #self.ERROR = 0
                #print("Stopped +")
                self.macro_stop()
        elif self.ERROR < 0:
            #print("Started")
            #if self.ERROR < self.setpoint * .8:
            #    self.elevator.elevate_speed(.6)
            #elif self.elevator_encoder.distance < self.setpoint:
            #    self.elevator.elevate_speed(.3)
            if abs(self.ERROR) > 100 and abs(self.ERROR) > 50:
                self.elevator.elevate_speed(-.6)
            elif abs(self.ERROR) <= 100 and abs(self.ERROR) > 50:
                self.elevator.elevate_speed(-.1)
            if abs(self.ERROR) <= 50:
                #self.ERROR = 0
                #print("Stopped -")
                self.macro_stop()




    def macro_stop(self):
        self.elevator.stop()

    def lift_to(self, state):
        #Add in self.enabled logic here!
        #These macros are always running, each in their own separate background thread, but 
        #they only do anything interesting when enabled by their specific methods.
        #They can also stop themselves easily (or be stopped by something else easily)
        #by disabling them. 
        #In an emergency, their threads can also be terminated. This method will require
        #the macro's thread to be restarted before it can be used again.
        #self.running = False
        self.initial_distance = 0
        self.setpoint = self.STATE_DICT[state] #-self.STATE_DICT[state] + self.elevator_encoder.distance #self.STATE_DICT[self.current_state]
        self.current_state = state
        #self.terminate()
        #print("Open threads: ", threading.active_count())
        print(self.setpoint)
        print("Encoder distance: ", self.elevator_encoder.distance)
        #self.run_threaded()
        #thread = threading.Thread(target=self.initialize)
        #thread.Start()
        #self.initialize()
        

    def traveled_distance(self):
        return abs(self.elevator_encoder.distance - self.initial_distance)
        #return self.elevator_encoder.distance

    """
    def run_elevator_macro(self):
        if(self.setpoint>0):
            while(self.traveled_distance() < self.setpoint * .8):
                print("travel: %f" % self.traveled_distance())
                self.elevator.elevate_speed(.6)
            while(self.traveled_distance() < self.setpoint):
                print("half power travel: %f" % self.traveled_distance())
                self.elevator.elevate_speed(.3)
            self.elevator.stop()
        elif(self.setpoint<0):
            while(self.traveled_distance() > self.setpoint * .8):
                print("travel: %f" % self.traveled_distance())
                self.elevator.elevate_speed(-.6)
            while(self.traveled_distance() > self.setpoint):
                print("half power travel: %f" % self.traveled_distance())
                self.elevator.elevate_speed(-.3)
            self.elevator.stop()
        self.kill()
    """
   