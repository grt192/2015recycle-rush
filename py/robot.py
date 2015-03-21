__author__ = "Sidd Karamcheti, Calvin Huang, Alex Mallery"


import wpilib

import time

auto = None
auto_exists = True


class MyRobot(wpilib.SampleRobot):
    def __init__(self):
        super().__init__()
        import config
        
        self.sp = config.sp
        self.hid_sp = config.hid_sp
        self.dt = config.dt
        self.ds = config.ds
        self.teleop_controller = config.teleop_controller
        self.driver_stick = config.driver_stick
        global auto
        global auto_exists
        self.basic_auto = config.basic_auto
        self.one_bin_steal = config.one_bin_steal
        try:
            auto = config.basic_auto
        except AttributeError:
            auto_exists = False


    def disabled(self):
        global auto_exists
        if auto_exists:
            self.basic_auto.stop_autonomous()
            self.one_bin_steal.stop_autonomous()
        while self.isDisabled():
            tinit = time.time()
            self.sp.poll()
            self.safeSleep(tinit, .04)
    if auto_exists:
        def autonomous(self):
            global auto
            print("Autonomous started")
            if self.driver_stick.j.getZ() > .5:
                self.basic_auto.run_autonomous()
            else:
                self.one_bin_steal.run_autonomous()
            while self.isAutonomous() and self.isEnabled():
                tinit = time.time()
                self.sp.poll()
                self.safeSleep(tinit, .04)
            self.basic_auto.stop_autonomous()
            self.one_bin_steal.stop_autonomous()
    else:
        def autonomous(self):
            pass
    
    def operatorControl(self):
        if auto_exists:
            self.basic_auto.stop_autonomous()
            self.one_bin_steal.stop_autonomous()
        while self.isOperatorControl() and self.isEnabled():
            tinit = time.time()
            #self.teleop_controller.poll()
            self.sp.poll()
            self.hid_sp.poll()
            self.safeSleep(tinit, .04)
            
    def safeSleep(self, tinit, duration):
        tdif = .04 - (time.time() - tinit)
        if tdif > 0:
            time.sleep(tdif)
        if tdif <= 0:
            #print("Code running slowly!")
            pass


if __name__ == "__main__":
    wpilib.run(MyRobot)
