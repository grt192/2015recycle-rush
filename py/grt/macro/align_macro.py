__author__ = "armin"
from grt.core import GRTMacro

class AlignMacro(GRTMacro):
	'''
	Using limit switch info, automatically
	align the hook mechanism with a tote 
	such that it can pick it up. 
	'''

	def __init__(self, dt, l_switch, r_switch, timeout):
		super.__init__(timeout)

		self.dt = dt
		self.l_switch = l_switch
		self.r_switch = r_switch

		self.l_motor = dt.left_motor
		self.r_motor = dt.right_motor

	def align(self):
		'''
		Have the robot align itself by ramming into a box
		when it is reasonably close to it
		'''
		while(self.l_switch.Get() and self.r_switch.Get()):
			#double check to make sure if this is the correct way to 
			#see if limit switches are pressed. 
			#"While neither switch is pressed" (i.e. both Gets give True)
			ramming_power = 0.1
			self.l_motor.Set(ramming_power)
			self.r_motor.Set(ramming_power) 

			##### TESTING STUFF #####
			print('Left limit switch state: %f, Right limit switch state: %f'%(self.l_switch.Get(), self.r_switch.Get()))

		print('One of the limit switches is pressed')
		if not(self.l_switch.Get() or self.r_switch.Get()):
			#if both buttons are pressed (both are False)
			self.l_motor.Set(0)
			self.r_motor.Set(0)
			#stop the robot 
		elif self.l_switch.Get():
			#the right switch is pressed (because the left is not)
			#shut off the right side to turn into position
			while not self.l_switch.Get():
			    self.r_motor.Set(0)
			    self.l_motor.Set(0.05)
			self.l_motor.Set(0)
			#come to a stop

			
		else:
			#the left switch is pressed (because the right is not)
			#shut off the left side to turn into position
			while not self.r_switch.Get():
			    self.r_motor.Set(0.05)
			    self.l_motor.Set(0)
			self.r_motor.Set(0)
			#come to a stop
		print('ALIGNED')



