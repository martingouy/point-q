import Demand_Variation_Algos.Algo_given_timeanddem_param_entire_sim as Algo_given_timeanddem_param_entire_sim

#Athe type of the algo for computing the paramet of the demand variation
TYPE_DEMAND_VARIATION_ALGORITHM={1:"ty_algo_given_timeanddem_param_entire_sim"}

class Demand_Variation_Algo_Actuate:

	def __init__(self,val_li_param_algo_given_timeanddem_param_entire_sim=None):
	
		#the list =[ ..., [durat first variation, demand param corresponding entry link],...]
		self._li_param_algo_given_timeanddem_param_entire_sim=val_li_param_algo_given_timeanddem_param_entire_sim
		
#*****************************************************************************************************************************************************************************************
	#method returning the list wth the param when the time at which the demand varies and the coresponding param are given for the entire sim
	def get_li_param_algo_given_timeanddem_param_entire_sim(self):
		return self._li_param_algo_given_timeanddem_param_entire_sim

#*****************************************************************************************************************************************************************************************

	#method modifying the list wth the param when the time at which the demand varies and the coresponding param are given for the entire sim
	def set_li_param_algo_given_timeanddem_param_entire_sim(self,n_v):
		self._li_param_algo_given_timeanddem_param_entire_sim=n_v

#*****************************************************************************************************************************************************************************************

	#fct selecting the appropriate algo for computing the demand variation
	def fct_select_appropriate_algo_demand_variat(self,va_type_algo_to_employ):
		if TYPE_DEMAND_VARIATION_ALGORITHM[va_type_algo_to_employ]==TYPE_DEMAND_VARIATION_ALGORITHM[1]:
		
			re=Algo_given_timeanddem_param_entire_sim.fct_calcul_t_and_param_demand_variation_entire_sim(val_li_t_and_dem_param=\
			self._li_param_algo_given_timeanddem_param_entire_sim)
			
		return re

#*****************************************************************************************************************************************************************************************