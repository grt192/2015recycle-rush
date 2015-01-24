__author__ = "Sidd Karamcheti, Calvin Huang, Alex Mallery"

try:
    from pyfrc import wpilib
except ImportError:
    import wpilib


import time




class MyRobot(wpilib.SampleRobot):
    def __init__(self):
        super().__init__()
        #print("Hi!")
        #print("Added in!")
        import config
        self.sp = config.sp
        self.hid_sp = config.hid_sp
        self.dt = config.dt
        self.ds = config.ds
        self.teleop_controller = config.teleop_controller
        try:
            self.auto = config.basic_auto
        except NameError:
            #self.auto_exists = False
            pass

    def disabled(self):
        #if self.auto_exists:
        self.auto.stop_autonomous()
        while self.isDisabled():
            tinit = time.time()
            self.sp.poll()
            time.sleep(0.04 - (time.time() - tinit))
            #wpilib.Wait(0.04 - (time.time() - tinit))
    
    def autonomous(self):
        
        #self.dt.up_shift()
            #self.watchdog.SetEnabled(False)

            

        self.auto.run_autonomous()
        while self.isAutonomous() and self.isEnabled():
            tinit = time.time()
            self.sp.poll()
            time.sleep(0.04 - (time.time() - tinit))
        self.auto.stop_autonomous()
    
    
    def operatorControl(self):
        #if self.auto_exists:
        self.auto.stop_autonomous()
        self.dt.downshift()  # start in low gear for tele
        #dog = self.getWatchdog()
        #dog.setExpiration(0.25)
        #dog.setEnabled(True)

        while self.isOperatorControl() and self.isEnabled():
            #dog.Feed()
            tinit = time.time()
            #print("Added in!")
            self.teleop_controller.poll()
            time.sleep(0.04 - (time.time() - tinit))


if __name__ == "__main__":
    print("Hi!")
    wpilib.run(MyRobot)
