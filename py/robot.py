__author__ = "Sidd Karamcheti, Calvin Huang, Alex Mallery"


import wpilib
import inspect

import time

try:
    auto = basicauto
except NameError:
    auto_exists = False


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
        #sep = wpilib.SerialPort(57600, wpilib.SerialPort.Port.kOnboard)
        #for name, obj in inspect.getmembers(wpilib):
        #    print(obj)
        #talon8 = wpilib.Talon(8)
        #self.solenoid1 = wpilib.Solenoid(1)


    def disabled(self):
        if auto_exists:
            auto.stop_autonomous()
        while self.isDisabled():
            tinit = time.time()
            self.sp.poll()
            time.sleep(0.04 - (time.time() - tinit))
            #wpilib.Wait(0.04 - (time.time() - tinit))
    if auto_exists:
        def autonomous(self):
            global auto
            self.dt.up_shift()
            #self.watchdog.SetEnabled(False)

            if ds.getDigitalIn(1):
                auto = twoballauto
            else:
                auto = basicauto

            auto.run_autonomous()
            while self.isAutonomous() and self.isEnabled():
                tinit = time.time()
                self.sp.poll()
                time.sleep(0.04 - (time.time() - tinit))
            auto.stop_autonomous()
    else:
        def autonomous(self):
            pass
    
    def operatorControl(self):
        if auto_exists:
            auto.stop_autonomous()
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
