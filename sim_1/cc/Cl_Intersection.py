import Cl_Node
import Cl_Vehicle_Queue
import Cl_Control_Actuate
import Cl_Network_Link


TYPE_INTERSECTION={"signalised_intersection":1, "non_signalised_intersection":0}
class Intersection(Cl_Node.Node):

	""" class defining a node type utilised for the network construction"""
	
	def __init__(self,val_id_nd=-1,val_li_id_input_network_links_to_inters_node=[],\
	val_li_id_output_network_links_from_inters_node=[],\
	val_type_intersection=1,val_current_di_rout_prob={},val_current_di_cum_rout_prob={},\
	val_estimated_turn_ratios=None,\
	val_current_di_cum_mod={},val_current_di_unique_paths={},\
	val_li_param_estim_turn_ratios=[],val_li_id_internal_links=[],\
	val_di_estimat_rp={},val_di_estimat_cum_rp={}):
	
		Cl_Node.Node.__init__(self,val_id_node=val_id_nd)
		
		#creation of a control actuate object for selecting the appropriate control to actuate
		#self._control_actuate_obj=Cl_Control_Actuate.Control_Actuate()
		
		
		#the set of input links to the current node
		self._li_id_input_network_links_to_inters_node=val_li_id_input_network_links_to_inters_node
		
		#the set of output links to the current node
		self._li_id_output_network_links_from_inters_node=val_li_id_output_network_links_from_inters_node
				
		
		#variable indicating the type of the intersection, (signal, non-signal)
		self._type_intersection=val_type_intersection
		
		#dict, key=id_phase, value= current value of the rout prob of phase, 
		self._current_di_rout_prob=val_current_di_rout_prob
		
		#dict with the current  values of the cum rout prob, key=id input link to the intersection, value=  [cum_prob, id dest link]
		self._current_di_cum_rout_prob=val_current_di_cum_rout_prob
		
		
		
		#variable indicating the lambda parameter employed when turn ratios are estimated
		#self._param_lambda_for_calculating_estimated_values_turn_ratios=val_param_lambda_for_calculating_estimated_values_turn_ratios
		
				
		#the dictionary with the current value of the od matrix (if the model considers it)
		#dict id entry link associated with the itnersection node, value=[...,[value cum prob, id final dest link],...]
		self._current_di_cum_mod=val_current_di_cum_mod
		
		#variable indicating if the turn ratios will be or not  (value 1 or 0) estimated (at least at the beginning  of the sim)
		self._estimated_turn_ratios=val_estimated_turn_ratios
		
		#the dictionary with the unique paths related to each (entry, exit) link of the intersection having entry links (and when the model
		#includes a final destination from the beginning).
		#dict, key=(id entry, id exit link), value=[...,link id to follow,...]
		self._current_di_unique_paths=val_current_di_unique_paths
		
	
		#list with the param required for the estim of the turn ratios [param convex combin, duration turn ratio values]
		self._li_param_estim_turn_ratios=val_li_param_estim_turn_ratios
		
		#variable indicating the id of the internal links corresponding to the intersection (employed when turn ratios are estimated)
		self._li_id_internal_link__s=val_li_id_internal_links
		
		#dict indicating t the estimated  turn ratios, dict,  key=id_phase, value= current value of the  estimated rout prob of phase
		#when  new estimatios  it is the corresponding part of the diction self._di_both_types_rp, (self._di_both_types_rp[2]) which will be updated
		#and not this member
		#self._di_estimat_rp=val_di_estimat_rp
		
		
		#dict indicating the dict with the cum values of the estimated  turn prob, dict, key=id input link to the intersection, value=  [cum_prob, id dest link]
		#self._di_estimat_cum_rp=val_di_estimat_cum_rp
		
		#di_cur_rp=dict(self._current_di_rout_prob)
		
		#dict with the routing prob (key =1) and the estimated routing probabilities (key=2)
		self._di_both_types_rp={1:self._current_di_rout_prob, 2:val_di_estimat_rp}
		
		
				
#*****************************************************************************************************************************************************************************************
	#method returning the control actuate object, for selecting the appropriate control for the intersection
	#def get_control_actuate_obj(self):
		#return self._control_actuate_obj
#*****************************************************************************************************************************************************************************************
	#method returning the set of input links to the current link
	def get_li_id_input_network_links_to_inters_node(self):
		return self._li_id_input_network_links_to_inters_node
#*****************************************************************************************************************************************************************************************
	#method returning the set of output links to the current link
	def get_li_id_output_network_links_from_inters_node(self):
		return self._li_id_output_network_links_from_inters_node
#*****************************************************************************************************************************************************************************************
	#method returning the dictionary with the related stages to the intersection
	#def get_di_stages_intersection(self):
		#return self._di_stages_intersection

#*****************************************************************************************************************************************************************************************
	
	#method returning the variable indicating the type of the intersection
	def get_type_intersection(self):
		return self._type_intersection

#*****************************************************************************************************************************************************************************************
	#method returning the variable indicating the phase id and the associated value of  rout prob
	def get_current_di_rout_prob(self):
		return self._current_di_rout_prob
#*****************************************************************************************************************************************************************************************
	#method returning the di with the values of the cum rout prob, key=id input link to the intersection, value=  [cum_prob, id dest link]
	def get_current_di_cum_rout_prob(self):
		return self._current_di_cum_rout_prob
	
#*****************************************************************************************************************************************************************************************

	#method returning the variable indicating if a vehicle of a prior movement is crossing the intersection
	def get_indicator_prior_mv_cross_intersection(self):
		return self._indicator_prior_mv_cross_intersection

#*****************************************************************************************************************************************************************************************
	#method returning the variable indicating whether a vehicle of a minor movement is crossing the intersection
	#def get_indicator_minor_mv_cross_intersection(self):
		#return self._indicator_minor_mv_cross_intersection

#*****************************************************************************************************************************************************************************************
	#method returning the dict with the duration of rout prob for the input links having varying rout prob
	#def get_di_duration_varying_rp_input_lk(self):
	#return self._di_duration_varying_rp_input_lk

#*****************************************************************************************************************************************************************************************
	#method returning the variable indicating the lambda parameter employed when turn ratios are estimated
	#def get_param_lambda_for_calculating_estimated_values_turn_ratios(self):
		#return self._param_lambda_for_calculating_estimated_values_turn_ratios

#*****************************************************************************************************************************************************************************************
	#method returning the dict with the cum rout prob of the links  with varuing  split ratios
	#def get_di_varying_cum_rp_input_lk(self):
		#return self._di_varying_cum_rp_input_lk
#*****************************************************************************************************************************************************************************************
	#method returning the the dictionary with the current value of the od matrix (if the model considers it)
	def get_current_di_cum_mod(self):
		return self._current_di_cum_mod
#*****************************************************************************************************************************************************************************************
	#method returning the variable indicating if the turn ratios will be estimated (at least at the beginning  of the sim)
	def get_estimated_turn_ratios(self):
		return self._estimated_turn_ratios
#*****************************************************************************************************************************************************************************************

	#method returning the dictionary with the unique paths related to each (entry, exit) link of the intersection
	def get_current_di_unique_paths(self):
		return self._current_di_unique_paths
#*****************************************************************************************************************************************************************************************
	#method returning the list with the param required for the estim of the turn ratios
	def get_li_param_estim_turn_ratios(self):
		return self._li_param_estim_turn_ratios

#*****************************************************************************************************************************************************************************************
	#method returning the list with the id of internal links related to the intersection
	def get_li_id_internal_links(self):
		return self._li_id_internal_links
#*****************************************************************************************************************************************************************************************
	#method returning the dict with the estimated  turn ratios
	#def get_di_estimat_rp(self):
		#return self._di_estimat_rp
#*****************************************************************************************************************************************************************************************
	#method returning the dict indicating the dict with the cum values of the estimated  turn prob
	def get_di_estimat_cum_rp(self):
		return self._di_estimat_cum_rp
#*****************************************************************************************************************************************************************************************
	#method returning the dict with both the routing probab and the estimated ones
	def get_di_both_types_rp(self):
		return self._di_both_types_rp

#*****************************************************************************************************************************************************************************************
	
	#method modifying the control actuate object, for selecting the appropriate control for the intersection
	#def set_control_actuate_obj(self,n_v):
		#self._control_actuate_obj=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the set of input links to the current link
	def set_li_id_input_network_links_to_inters_node(self,n_v):
		self._li_id_input_network_links_to_inters_node=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the set of input links to the current link
	def set_li_id_output_network_links_from_inters_node(self,n_v):
		self._li_id_output_network_links_from_inters_node=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the dictionary with the related stages to the intersection
	#def set_di_stages_intersection(self,n_v):
		#self._di_stages_intersection=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the variable indicating the type of the intersection
	def set_type_intersection(self,n_v):
		self._type_intersection=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the variable indicating the phase id and the associated value of  rout prob
	def set_current_di_rout_prob(self,n_v):
		self._current_di_rout_prob=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the di with the values of the cum rout prob, key=id input link to the intersection, value=  [cum_prob, id dest link]
	def set_current_di_cum_rout_prob(self,n_v):
		self._current_di_cum_rout_prob=n_v
	
#*****************************************************************************************************************************************************************************************
	
	#method moodifying the variable indicating the lambda parameter employed when turn ratios are estimated
	#def set_param_lambda_for_calculating_estimated_values_turn_ratios(self,n_v):
		#self._param_lambda_for_calculating_estimated_values_turn_ratios=n_v

#*****************************************************************************************************************************************************************************************
		#method modifying the the dictionary with the current value of the od matrix (if the model considers it)
	def set_current_di_cum_mod(self,n_v):
		self._current_di_cum_mod=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying  the variable indicating if the turn ratios will be estimated (at least at the beginning  of the sim)
	def set_estimated_turn_ratios(self,n_v):
		self._estimated_turn_ratios=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the dictionary with the unique paths related to each (entry, exit) link of the intersection
	def set_current_di_unique_paths(self,n_v):
		self._current_di_unique_paths=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the list with the param required for the estim of the turn ratios
	def set_li_param_estim_turn_ratios(self,n_v):
		self._li_param_estim_turn_ratios=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the list with the id of internal links related to the intersection
	def set_li_id_internal_links(self,n_v):
		self._li_id_internal_links=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the dict with the estimated  turn ratios
	def set_di_estimat_rp(self,n_v):
		self._di_estimat_rp=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the dict indicating the dict with the cum values of the estimated  turn prob
	#def set_di_estimat_cum_rp(self,n_v):
		#self._di_estimat_cum_rp=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the dict with both the routing probab and the estimated ones
	def set_di_both_types_rp(self,n_v):
		self._di_both_types_rp=n_v

#*****************************************************************************************************************************************************************************************
	#method updating the itnersection when the turn ratios are estimated
	def fct_update_intersection_case_estimated_turn_ratios_1(self,val_di_turn_ratios,val_di_cum_turn_ratios,val_netwk):
	
		#update the intersection dict with rout proba
		self._current_di_rout_prob=val_di_turn_ratios
		
		#update the intersection dict with cum rout proba
		self._current_di_cum_rout_prob=val_di_cum_turn_ratios
		
		#for each input, output link of the intersection, 
		#we initialise the dict indicating the the id of the origin link and number of vehicles joined the link durning the current period
		for i in self._li_id_input_network_links_to_inters_node:
			if val_netwk.get_di_entry_internal_links()[i].get_type_network_link() != Cl_Network_Link.TYPE_NETWORK_LINK["entry"]:
				val_netwk.get_di_entry_internal_links()[i].fct_initialise_di_ar_to_link_current_period()
		
			for j in self._li_id_output_network_links_from_inters_node:
				val_netwk.get_di_all_links()[j].fct_initialise_di_ar_to_link_current_period()
			

#*****************************************************************************************************************************************************************************************
	#method updating the itnersection when the turn ratios are estimated
	def fct_update_intersection_case_estimated_turn_ratios_2(self,val_di_turn_ratios,val_di_cum_turn_ratios,val_netwk):
	
		#update the intersection  dict with teh estimated rout proba
		self._di_both_types_rp[2]=val_di_turn_ratios
		
		
		#update the intersection dict with cum estimated  rout proba
		self._di_estimat_cum_rp=val_di_cum_turn_ratios
		
		#for each input, output link of the intersection, 
		#we initialise the dict indicating the the id of the origin link and number of vehicles joined the link durning the current period
		for i in self._li_id_input_network_links_to_inters_node:
			#if val_netwk.get_di_entry_internal_links()[i].get_type_network_link() != Cl_Network_Link.TYPE_NETWORK_LINK["entry"]:
				#val_netwk.get_di_internal_links_to_network()[i].fct_initialise_di_ar_to_link_current_period()
		
			for j in self._li_id_output_network_links_from_inters_node:
				val_netwk.get_di_all_links()[j].fct_initialise_di_ar_to_link_current_period()
			

#*****************************************************************************************************************************************************************************************
	#method updating the itnersection when the turn ratios are estimated
	def fct_update_intersection_case_estimated_turn_ratios(self,val_di_turn_ratios,val_netwk):
	
		#update the intersection  dict with teh estimated rout proba
		self._di_both_types_rp[2]=dict(val_di_turn_ratios)
		#self._di_estimat_rp=val_di_turn_ratios
		
		#update the intersection dict with cum estimated  rout proba
		#self._di_estimat_cum_rp=val_di_cum_turn_ratios
		
		#for each input, output link of the intersection, 
		#we initialise the dict indicating the the id of the origin link and number of vehicles joined the link durning the current period
		for i in self._li_id_input_network_links_to_inters_node:
			#if val_netwk.get_di_entry_internal_links()[i].get_type_network_link() != Cl_Network_Link.TYPE_NETWORK_LINK["entry"]:
				#val_netwk.get_di_internal_links_to_network()[i].fct_initialise_di_ar_to_link_current_period()
		
			for j in self._li_id_output_network_links_from_inters_node:
				val_netwk.get_di_all_links()[j].fct_initialise_di_ar_to_link_current_period()
			

#*****************************************************************************************************************************************************************************************
	#method updating the routing proportions and the cum routing prob
	def fct_update_intersection_case_modif_turn_ratios(self,val_di_turn_prob,val_di_cum_turn_prob):
	
		#update the dict with the rp
		self._current_di_rout_prob=val_di_turn_prob
		
		#FAIRE MIEUX !
		self._di_both_types_rp[1]=val_di_turn_prob
		
		#update the dict with the cum rp
		self._current_di_cum_rout_prob=val_di_cum_turn_prob
		


#*****************************************************************************************************************************************************************************************
	
	


#ex
#nd=Intersection_Node(val_li_id_input_network_links_to_inters_node=[],val_li_id_output_network_links_from_inters_node=[])
#print("Id node, type node",nd.get_id_node(),nd.get_type_node())
#print("AVANT ND INTERSECTION",nd.get_li_id_input_network_links_to_inters_node(),nd.get_li_id_output_network_links_to_inters_node())
#nd.set_li_id_input_network_links_to_inters_node(li_in)
#print("AFTER ND INTERSECTION",nd.get_li_id_input_network_links_to_inters_node(),nd.get_li_id_output_network_links_to_inters_node())
