__author__ = "armin"
from grt.core import GRTMacro
import threading

class AlignMacro(GRTMacro):
	'''
	Using limit switch info, automatically
	align the pickup with a tote.  
	'''

	def __init__(self, dt, l_switch, r_switch, timeout):
		super().__init__(timeout)

		self.dt = dt
		self.l_switch = l_switch
		self.r_switch = r_switch


	def perform(self):
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
		
		if self.l_switch.get() and self.r_switch.get():
			self.dt.set_dt_output(ramming_power, ramming_power)
		elif not(self.l_switch.get() or self.r_switch.get()):
			#if both buttons are pressed (both are False)
			self.dt.set_dt_output(0, 0)
			print('ALIGNED')
			self.kill()
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
	def die(self):
		self.dt.set_dt_output(0, 0)



