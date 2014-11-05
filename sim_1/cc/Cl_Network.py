import Cl_Intersection
import Cl_Network_Entry_Link
import Cl_Network_Exit_Link
import Cl_Network_Internal_Link
import math

class Network:

	""" class defining the network object comprised of the intersections, network entry, exit, internal links,\
	the control object"""
	
	
	def __init__(self,val_id_network=1,val_di_intersections={},val_di_entry_links_to_network={},\
	val_di_exit_links_from_network={},val_di_internal_links_to_network={},val_di_sublinks={},\
	val_di_travel_durat_param_mu={},val_di_travel_durat_param_sigma={},val_di_travel_durat_param_shift={},\
	val_li_employed_ctrl_types=[],val_di_id_intersections_with_estim_turn_ratios={},val_dict_id_nds_with_entry_links=None,\
	val_di_intersections_with_var_turn_ratios={},\
	val_di_intersections_with_var_cum_turn_ratios={},val_di_inters_periods_with_var_turn_ratios={},\
	val_di_intersections_with_non_empty_init_que_state={},\
	val_di_entry_links_with_varying_demands={}):
	
	
		#the id of the network
		self._id_network=val_id_network
		
		#the set of intesections of the network (N) (dictionnaire: key= id node, value=node)
		self._di_intersections=dict(val_di_intersections)
		
		
		#the set of the entry links of the network (L_entry) (dictionnaire: key= id link, value=link)
		self._di_entry_links_to_network=dict(val_di_entry_links_to_network)
		
		#the set of the exit links  from the network (L_exit)
		self._di_exit_links_from_network=dict(val_di_exit_links_from_network)
		
		
		#the set of the internal links of the network (L)
		self._di_internal_links_to_network=dict(val_di_internal_links_to_network)
		
		#the dict of  the entry and internal links of the network, key is the link id and value is the associated link
		di_entry_internal_links={}
		di_entry_internal_links.update(self._di_entry_links_to_network)
		di_entry_internal_links.update(self._di_internal_links_to_network)
		self._di_entry_internal_links=di_entry_internal_links
		
		#the distionary of all links, entry, exit, internal
		di_all_links={}
		di_all_links.update(self._di_entry_internal_links)
		di_all_links.update(self._di_exit_links_from_network)
		self._di_all_links=di_all_links
		
		
		#the set (dictionaire) of sublinks
		#the key is the id of the sublink, the value is the sublink
		self._di_sublinks=val_di_sublinks
		
		
		#the dictionary indicating the mean value of the lognormal distribution of each edge, when calcul the travel duration
		#key=id edge, value=[shift]
		self._di_travel_durat_param_mu=val_di_travel_durat_param_mu
		
		#the dictionary indicating the sigma (stan deviation) value of the shifted lognormal law of each edge, when calcul the travel duration
		#key=id edge, value=[shift]
		self._di_travel_durat_param_sigma=val_di_travel_durat_param_sigma
		
		#the dictionary indicating the shift value of the lognormal law of each edge, when calcul the travel duration
		#key=id edge, value=[shift]
		self._di_travel_durat_param_shift=val_di_travel_durat_param_shift
		
		#we create the list with the surveyed queue phases
		self._li_surveyed_queues=self.fct_creat_li_surveyed_que_phases()
		
		#variable indicating the list with all the control types employed in the network at the beginning of the simulation
		self._li_employed_ctrl_types=val_li_employed_ctrl_types
		
		#variable indicating the inters of which turn ratios will be estimated
		#dict, key=id node, value=1
		self._di_id_intersections_with_estim_turn_ratios=val_di_id_intersections_with_estim_turn_ratios
		
		#dict, key=id node with entry links, value=[..., id entry links,...] (it will be used+createdwhe turn ratios estim)
		self._dict_id_nds_with_entry_links=val_dict_id_nds_with_entry_links
		
		#dict: key=id node, value=dict, key=id period, value=dict, key=id phase, value=cum rout prob at related period
		self._di_intersections_with_var_cum_turn_ratios=val_di_intersections_with_var_cum_turn_ratios
		
		#dict: key=node id, value=dict, key=id period valeur:duration previous values rp
		self._di_inters_periods_with_var_turn_ratios=val_di_inters_periods_with_var_turn_ratios
		
		#dict, key=id node, value=dict, key=id period, value=dict, key=id phase, value=cum rout prob at related period
		self._di_intersections_with_var_turn_ratios=val_di_intersections_with_var_turn_ratios
		
		#the dict with the init state if the related itnersections
		#dict, key=id node, value=dict, key=id phase, value=nb veh
		self._di_intersections_with_non_empty_init_que_state=val_di_intersections_with_non_empty_init_que_state
		
		#the dict with the id of the entry links with varying demands, key=id link,
		# value=[duree after the begin of the sim at which demand changes, type algo demand variation]
		self._di_entry_links_with_varying_demands=val_di_entry_links_with_varying_demands
		
		
	
		
		
#*****************************************************************************************************************************************************************************************
	#method returning the id of the network
	def get_id_network(self):
		return self._id_network
#*****************************************************************************************************************************************************************************************

	#method returning the set of intesections of the network
	def get_di_intersections(self):
		return self._di_intersections
#*****************************************************************************************************************************************************************************************
	#method returning the set of the entry links of the network
	def get_di_entry_links_to_network(self):
		return self._di_entry_links_to_network

#*****************************************************************************************************************************************************************************************
	#method returning the set of the exit links  from the network
	def get_di_exit_links_from_network(self):
		return self._di_exit_links_from_network

#*****************************************************************************************************************************************************************************************
	#method returning the set of the internal links of the network
	def get_di_internal_links_to_network(self):
		return self._di_internal_links_to_network
#*****************************************************************************************************************************************************************************************
	#method returning the dict of  the entry and internal links
	def get_di_entry_internal_links(self):
		return self._di_entry_internal_links
#*****************************************************************************************************************************************************************************************
	#method returning the dictionary of all links
	def get_di_all_links(self):
		return self._di_all_links
#*****************************************************************************************************************************************************************************************
	#method returning the set (dictionaire) of sublinks
	def get_di_sublinks(self):
		return self._di_sublinks
#*****************************************************************************************************************************************************************************************
	#method returning the dictionary with the intersection control matrices
	#def get_di_intersection_control_matrices(self):
		#return self._di_intersection_control_matrices
#*****************************************************************************************************************************************************************************************
	#method returning the inters controls  object
	#def get_di_intersection_controls(self):
		#return self._di_intersection_controls

#*****************************************************************************************************************************************************************************************
	#method returning the dictionary indicating the mean value of the lognormal distribution of each edge, when calcul the travel duration
	def get_di_travel_durat_param_mu(self):
		return self._di_travel_durat_param_mu

#*****************************************************************************************************************************************************************************************
	#method returning the dictionary indicating the sigma (stan deviation) value of the shifted lognormal law of each edge, when calcul the travel duration
	def get_di_travel_durat_param_sigma(self):
		return self._di_travel_durat_param_sigma
#*****************************************************************************************************************************************************************************************
	#method returning the dictionary indicating the shift value of the lognormal law of each edge, when calcul the travel duration
	def get_di_travel_durat_param_shift(self):
		return self._di_travel_durat_param_shift
#*****************************************************************************************************************************************************************************************
	#method returning the list with the surved queue phases
	def get_li_surveyed_queues(self):
		return self._li_surveyed_queues

#*****************************************************************************************************************************************************************************************
	#method returning the variable indicating the list with all the control types employed in the network at the beginning of the simulation
	def get_li_employed_ctrl_types(self):
		return self._li_employed_ctrl_types

#*****************************************************************************************************************************************************************************************
	#method returning the variable indicating the inters of which turn ratios will be estimated
	def get_di_id_intersections_with_estim_turn_ratios(self):
		return self._di_id_intersections_with_estim_turn_ratios
	
#*****************************************************************************************************************************************************************************************
	#method returning the control actuate object, for selecting the appropriate control for the intersection
	def get_control_actuate_obj(self):
		return self._control_actuate_obj
#*****************************************************************************************************************************************************************************************
	#method returning the dictionary with the inters having entry links
	def get_dict_id_nds_with_entry_links(self):
		return self._dict_id_nds_with_entry_links

#*****************************************************************************************************************************************************************************************
	#method returning the dict with the intersections with varying cum turn ratios
	def get_di_intersections_with_var_cum_turn_ratios(self):
		return self._di_intersections_with_var_cum_turn_ratios
#*****************************************************************************************************************************************************************************************
	#method returning the dict with the durations of the rout prob
	def get_di_inters_periods_with_var_turn_ratios(self):
		return self._di_inters_periods_with_var_turn_ratios
#*****************************************************************************************************************************************************************************************
	#method returning the dict with the varying cum turn ratios
	def get_di_intersections_with_var_turn_ratios(self):
		return self._di_intersections_with_var_turn_ratios
#*****************************************************************************************************************************************************************************************
	#method returning the  dict with the init state if the related itnersections
	def get_di_intersections_with_non_empty_init_que_state(self):
		return self._di_intersections_with_non_empty_init_que_state
#*****************************************************************************************************************************************************************************************
	#method returning the dict with the id of the entry links with varying demands
	def get_di_entry_links_with_varying_demands(self):
		return self._di_entry_links_with_varying_demands

#*****************************************************************************************************************************************************************************************

	#method modifying  the id of the network
	def set_id_network(self,n_v):
		self._id_network=n_v
#*****************************************************************************************************************************************************************************************

	#method modifying the set of intesections of the network
	def set_di_intersections(self,n_v):
		self._di_intersections=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the set of the entry links of the network
	def set_di_entry_links_to_network(self,n_v):
		self._di_entry_links_to_network=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the dictionary of all links
	def set_di_all_links(self,n_v):
		self._di_all_links=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the set of the exit links  from the network
	def set_di_exit_links_from_network(self,n_v):
		self._di_exit_links_from_network=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the set of the internal links of the network
	def set_di_internal_links_to_network(self,n_v):
		self._di_internal_links_to_network=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the dict of  the entry and internal links
	def set_di_entry_internal_links(self,n_v):
		 self._di_entry_internal_links=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the set (dictionaire) of sublinks
	def set_di_sublinks(self,n_v):
		self._di_sublinks=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the variable indicating the inters of which turn ratios will be estimated
	def set_di_id_intersections_with_estim_turn_ratios(self,n_v):
		self._di_id_intersections_with_estim_turn_ratios=n_v
	
#*****************************************************************************************************************************************************************************************
	#method modifying the dictionary with the intersection control matrices
	#def set_di_intersection_control_matrices(self,n_v):
		#self._di_intersection_control_matrices=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the inters controls object
	#def set_di_intersection_controls(self,n_v):
		#self._di_intersection_controls=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the inters control object of a given intersection
	#def set_di_intersection_controls_given_intersection(self,id_inters_nd,n_v):
		#di={}
		#di[id_inters_nd]=n_v
		#self._di_intersection_controls.update(di)

#*****************************************************************************************************************************************************************************************
	
	#method modifying the dictionary indicating the mean value of the lognormal distribution of each edge, when calcul the travel duration
	def set_di_travel_durat_param_mu(self,n_v):
		self._di_travel_durat_param_mu=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the dictionary indicating the sigma (stan deviation) value of the shifted lognormal law of each edge, when calcul the travel duration
	def set_di_travel_durat_param_sigma(self,n_v):
		self._di_travel_durat_param_sigma=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the dictionary indicating the shift value of the lognormal law of each edge, when calcul the travel duration
	def set_di_travel_durat_param_shift(self,n_v):
		self._di_travel_durat_param_shift=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the list with the surved queue phases
	def set_li_surveyed_queues(self,n_v):
		self._li_surveyed_queues=n_v

#*****************************************************************************************************************************************************************************************
	
	#method modifying the dictionary corresponding to the od matrix
	#def set_dict_mat_rp_key_id_entry_internal_lk_value_list_dest_lks(self,n_v):
		#self._dict_mat_rp_key_id_entry_internal_lk_value_list_dest_lks=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the dictionary corresponding to the prob of each output link
	# (of which the sat flow >0)  from any entry-internal link
	#def set_dict_mat_od(self,n_v):
		#return self._dict_mat_od

#*****************************************************************************************************************************************************************************************
	#method modifying the dictionary corresponding to the cum  rp matrix
	#def set_dict_mat_rp_cum_key_entry_intern_lk_value_list_cum_fct_values(self,n_v):
		#self._dict_mat_rp_cum_key_entry_intern_lk_value_list_cum_fct_values=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the control actuate object, for selecting the appropriate control for the intersection
	def set_control_actuate_obj(self,n_v):
		self._control_actuate_obj=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the variable indicating the list with all the control types employed in the network at the beginning of the simulation
	def set_li_employed_ctrl_types(self,n_v):
		self._li_employed_ctrl_types=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the dictionary with the inters having entry links
	def set_dict_id_nds_with_entry_links(self,n_v):
		self._dict_id_nds_with_entry_links=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the dict with the intersections with varying turn ratios
	def set_di_intersections_with_var_cum_turn_ratios(self,n_v):
		self._di_intersections_with_var_cum_turn_ratioss=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the dict with the durations of the rout prob
	def set_di_inters_periods_with_var_turn_ratios(self,n_v):
		self._di_inters_periods_with_var_turn_ratios=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the dict with the varying cum turn ratios
	def set_di_intersections_with_var_turn_ratios(self,n_v):
		self._di_intersections_with_var_turn_ratios=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the  dict with the init state if the related itnersections
	def set_di_intersections_with_non_empty_init_que_state(self,n_v):
		self._di_intersections_with_non_empty_init_que_state=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the dict with the id of the entry links with varying demands
	def set_di_entry_links_with_varying_demands(self,n_v):
		self._di_entry_links_with_varying_demands=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the dict with the id of prior.-minor phases
	#def set_di_key_id_int_value_id_prior_phase_value_li_id_minor_phases(self,n_v):
		#self._di_key_id_int_value_id_prior_phase_value_li_id_minor_phases=n_v
	
#*****************************************************************************************************************************************************************************************
	#method calculating and associating the service rate for a period, for each queue of the network entry and interval  links
	#the service rate of a  queue is defined as the product of the saturation flow of the phase x the period duration
	#we define the service rate of all the queues even if they are not actuated
	def fct_calcul_and_associating_service_rate_with_entry_internal_links_current_period(self):
		
		#for each entry and internal link
		for  i in self._di_entry_internal_links:
			#for each queue of link i, the service rate = the saturation flow of the phase  x the current network control period duration
			for j in self._di_entry_internal_links[i].get_set_veh_queue().get_di_obj_veh_queue_at_link():
				
				self._di_entry_internal_links[i].get_set_veh_queue().get_di_obj_veh_queue_at_link()[j].set_current_queue_service_rate(\
				math.ceil(self._di_entry_internal_links[i].get_set_veh_queue().get_di_obj_veh_queue_at_link()[j].get_sat_flow_queue()* \
				self._current_network_control_obj.get_t_duration_control()))
				#print("entry link",i,"service rate",self._di_entry_internal_links[i].get_set_veh_queue().get_di_obj_veh_queue_at_link()[j].get_current_queue_service_rate(),\
				#"calc serv rat",self._di_entry_internal_links[i].get_set_veh_queue().get_di_obj_veh_queue_at_link()[j].get_sat_flow_queue(),
				#self._current_network_control_obj.get_t_duration_control())
		
				
				#print("saturation flow=",self._di_entry_internal_links[i].get_set_veh_queue().get_di_obj_veh_queue_at_link()[j].get_sat_flow_queue(),\
				#"period duaration=",self._current_network_control.get_t_duration_control(),"service rate=",\
				#round(self._di_entry_internal_links[i].get_set_veh_queue().get_di_obj_veh_queue_at_link()[j].get_sat_flow_queue()* \
				#self._current_network_control.get_t_duration_control()))
				

#*****************************************************************************************************************************************************************************************
	#method creating a dictionary : key=id signalised node, value : dictionary
	def fct_creat_di_intersection_control_matrices(self,val_di_id_sign_intersections_val_one):
		di_rep={}
		for i in self._di_intersections:
			if i in val_di_id_sign_intersections_val_one:
				di_rep[i]=self._di_intersections[i].fct_creat_di_key_id_phase_value_zero(self)
		#print(di_rep)	
		#import sys
		#sys.exit()	
		
		return di_rep

#*****************************************************************************************************************************************************************************************
	#method returning a list with the surveyed phases of all entry-internal links (these are the queues of which the max permitted queue size is different to -1)
	#ex [ [2,3]]
	
	def fct_creat_li_surveyed_que_phases(self):
		li=[]
		for i in self._di_entry_internal_links:
			#dict, key =  phase id (l,m), value=[max que size, sat flow,rout  prop, travl time param]
			for j in self._di_entry_internal_links[i].get_set_veh_queue().get_dict_queue_max_queue_size_et_sat_flow_queue_type():
				#print(self._di_entry_internal_links[i].get_set_veh_queue().get_dict_queue_max_queue_size_et_sat_flow_queue_type_rout_prop_param_trav_durat()[j])
				if self._di_entry_internal_links[i].get_set_veh_queue().get_dict_queue_max_queue_size_et_sat_flow_queue_type()[j][0]!=-1:
					li.append([j[0],j[1]])
		return li


#*****************************************************************************************************************************************************************************************
	

#ex


#lk_1=Cl_Network_Entry_Link.Network_Entry_Link(val_id_lik=9,val_li_id_vehicle_que=[5,7],val_id_head_intersection_nd=98,val_li_id_sublnk=[4,7])
#di_1={9:lk_1}

#lk_2=Cl_Network_Exit_Link.Network_Exit_Link(val_id_lik=10,val_li_id_vehicle_que=[5,7],val_id_tail_intersection_nd=97,val_li_id_sublnk=[14,17])
#di_2={10:lk_2}

#lk_3=Cl_Network_Internal_Link.Network_Internal_Link(val_id_lik=19,val_li_id_vehicle_que=[15,17],val_id_tail_intersection_nd=198,val_li_id_sublnk=[24,27])
#di_3={19:lk_3}


#nd=Cl_Intersection_Node.Intersection_Node(val_id_nd=122,val_li_id_input_network_links_to_inters_node=[19],val_li_id_output_network_links_from_inters_node=[10])

#nt=Network(val_di_intersections={122:nd},val_di_entry_links_to_network=di_1,val_di_exit_links_from_network=di_2, val_di_internal_links_to_network=di_3)
#print("ID NETWORK,DI ENTRY LINKS",nt.get_di_intersections(),nt.get_di_entry_links_to_network())		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
