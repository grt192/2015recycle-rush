from grt.core import Constants
import math


class ArcadeDriveController:

    def __init__(self, dt, stick, secondstick = None):

        self.dt = dt
        self.stick = stick

        self.isHighGear = False
        self.left = 0
        self.right = 0
        self.wheel = 0
        self.throttle = 0
        self.oldWheel = 0
        self.negInertia = 0
        self.linearPower = 0
        self.angularPower = 0
        self.negInertiaPower = 0
        self.negInertiaAccumulator = 0

        self.throttleDeadband = 0.02
        self.wheelDeadband = 0.02
        self.highGear = 0.7
        self.lowGear = 0.6
        self.highGearScalar = 3
        self.lowGearScalar = 2

        stick.add_listener(self._joylistener)

    def _handleDeadband(self):

        '''

        Gets the throttle and wheel values. Handles deadzones.

        '''

        self.throttle = -1 * self.stick.y_axis
        self.throttle = 0 if (abs(self.throttle) < self.throttleDeadband) else self.throttle
        self.wheel    = self.stick.x_axis
        self.wheel    = 0 if (abs(self.wheel) < self.wheelDeadband) else self.wheel

    def _handleNonlinearity(self):

        '''

        Scales the wheel

        '''

        if(self.isHighGear):
            wheelNonLinearity = self.highGear
            self.wheel = math.sin(math.pi / 2.0 * wheelNonLinearity * self.wheel) / math.sin(math.pi / 2.0 * wheelNonLinearity)
            self.wheel = math.sin(math.pi / 2.0 * wheelNonLinearity * self.wheel) / math.sin(math.pi / 2.0 * wheelNonLinearity)
        else:
            wheelNonLinearity = self.lowGear
            self.wheel = math.sin(math.pi / 2.0 * wheelNonLinearity * self.wheel) / math.sin(math.pi / 2.0 * wheelNonLinearity)
            self.wheel = math.sin(math.pi / 2.0 * wheelNonLinearity * self.wheel) / math.sin(math.pi / 2.0 * wheelNonLinearity)
            self.wheel = math.sin(math.pi / 2.0 * wheelNonLinearity * self.wheel) / math.sin(math.pi / 2.0 * wheelNonLinearity)

    def _handleNegativeInertia(self):

        '''

        Negative inertia. Obstensibly makes stuff stop turning faster. Basically magnifies the rate at which the wheel changes.

        '''

        self.negInertia = self.wheel - self.oldWheel
        self.oldWheel = self.wheel

        self.negInertiaPower = self.negInertia * (self.highGearScalar if self.isHighGear else self.lowGearScalar)
        self.negInertiaAccumulator += self.negInertiaPower
        self.wheel += self.negInertiaAccumulator

        if(self.negInertiaAccumulator > 1):
            self.negInertiaAccumulator -= 1
        elif(self.negInertiaAccumulator < -1):
            self.negInertiaAccumulator += 1
        else:
            self.negInertiaAccumulator = 0

    def _blendInputs(self):

        '''

        Blends the modified wheel and throttle to get left and right PWM values

        '''

        self.linearPower = self.throttle
        self.angularPower = self.wheel * abs(self.throttle)

        self.left = self.linearPower
        self.right = self.linearPower

        self.left -= self.angularPower
        self.right += self.angularPower

    def _handleOverpower(self):

        '''

        Handles situations where the left or right PWM values are greater than 1

        '''

        if (self.left > 1.0):
            self.right = self.right / self.left
            self.left = 1.0
        if (self.left < -1.0):
            self.right = self.right / abs(self.left)
            self.left = -1.0
        if (self.right > 1.0):
            self.left = self.left / self.right
            self.right = 1.0
        if (self.right < -1.0):
            self.left = self.left / abs(self.right)
            self.right = -1.0

    def _joylistener(self, sensor, state_id, datum):

        if state_id in ('x_axis', 'y_axis'):

            self._handleDeadband()
            self._handleNegativeInertia()
            self._handleNonlinearity()
            self._blendInputs()
            self._handleOverpower()
            self.dt.set_dt_output(self.left, self.right)

        elif state_id == 'trigger':
            if datum:
                self.isHighGear = True
                self.dt.upshift()
            else:
                self.isHighGear = False
                self.dt.downshift()
