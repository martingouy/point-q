
class Simulation_System:

	""" class defining the systeme to be simulated"""
	
	def __init__(self,val_network=None,val_dict_information_veh_previous_sim={}):
	
		#the employed network
		self._network=val_network
		
		#the dictionary with the information of a previously generated (vehicle) demand
		self._dict_information_veh_previous_sim=val_dict_information_veh_previous_sim
		
#*****************************************************************************************************************************************************************************************
	#method returning the employed network
	def get_network(self):
		return self._network
#*****************************************************************************************************************************************************************************************
	#method returning the dictionary with the information of a previously generated (vehicle) demand
	def get_dict_information_veh_previous_sim(self):
		return self._dict_information_veh_previous_sim

#*****************************************************************************************************************************************************************************************

	#method modifying the employed network
	def set_network(self,n_v):
		self._network=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the dictionary with the information of a previously generated (vehicle) demand
	def set_dict_information_veh_previous_sim(self,n_n_v):
		self._dict_information_veh_previous_sim=n_v

#*****************************************************************************************************************************************************************************************