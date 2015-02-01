__author__ = "armin"
from grt.core import GRTMacro

class AlignMacro(GRTMacro):
	'''
	Using limit switch info, automatically
	align the hook mechanism with a tote 
	such that it can pick it up. 
	'''

	def __init__(self, dt, l_switch, r_switch, timeout):
		super().__init__(timeout)

		self.dt = dt
		self.l_switch = l_switch
		self.r_switch = r_switch
		self.aligning = False


	def align(self):
		'''
		Have the robot align itself by ramming into a box
		when it is reasonably close to it
		'''
		self.aligning = True
		ramming_power = 0.3
		turning_power = 0.3
		weak_turning = 0.1
		while(self.l_switch.get() and self.r_switch.get()):
			#double check to make sure if this is the correct way to 
			#see if limit switches are pressed. 
			#"While neither switch is pressed" (i.e. both Gets give True)
			self.dt.set_dt_output(ramming_power, ramming_power)
	
			##### TESTING STUFF #####
			#print('Left limit switch state: %f, Right limit switch state: %f'%(self.l_switch.get(), self.r_switch.get())
	
		print('One of the limit switches is pressed')
		if not(self.l_switch.get() or self.r_switch.get()):
			#if both buttons are pressed (both are False)
			self.dt.set_dt_output(0, 0)
			#stop the robot 
		elif self.l_switch.get():
			#the right switch is pressed (because the left is not)
			#shut off the right side to turn into position
			while self.l_switch.get():
			    self.dt.set_dt_output(turning_power, weak_turning)
			self.dt.set_dt_output(0, 0)
			#come to a stop

			
		else:
			#the left switch is pressed (because the right is not)
			#shut off the left side to turn into position
			while self.r_switch.get():
			    self.dt.set_dt_output(weak_turning, turning_power)
			self.dt.set_dt_output(0, 0)
			#come to a stop
		print('ALIGNED')



