import Cl_Intersection
import Cl_Vehicle_Queue
import Cl_Control_Actuate


class Intersection_Signalised(Cl_Intersection.Intersection):

	def __init__(self,va_id_nd=-1,va_li_id_input_network_links_to_inters_node=[],va_li_id_output_network_links_from_inters_node=[],\
	val_di_stages_sign_intersection={},val_intersection_control_obj=None,val_ctrl_actuate_obj=None,\
	val_current_dict_rout_prob={},val_current_dict_cum_rout_prob={},val_current_dict_cum_mod={},\
	val_estim_turn_ratios=None,\
	val_lis_param_estim_turn_ratios=[],\
	val_dict_estimat_rp={},val_dict_estimat_cum_rp={}):
	
	
		Cl_Intersection.Intersection.__init__(self,val_id_nd=va_id_nd,\
		val_li_id_input_network_links_to_inters_node=va_li_id_input_network_links_to_inters_node,\
		val_li_id_output_network_links_from_inters_node=va_li_id_output_network_links_from_inters_node,\
		val_current_di_rout_prob=val_current_dict_rout_prob,\
		val_current_di_cum_rout_prob=val_current_dict_cum_rout_prob,\
		val_current_di_cum_mod=val_current_dict_cum_mod,\
		val_estimated_turn_ratios=val_estim_turn_ratios,\
		val_li_param_estim_turn_ratios=val_lis_param_estim_turn_ratios,\
		val_di_estimat_rp=val_dict_estimat_rp,val_di_estimat_cum_rp=val_dict_estimat_cum_rp)
		
		#the type of an intersection is signalised by default value
		
		#the dictionary with the stages, key=stage id (1,2 etc according to the number of intersection stages)
		#value=list phase ids( ex di={ 1:  [ [1,2],[5,6] ], 2:[ [7,8],[7,6] ] }, there are two possible interection stages, 
		#stage 1 actuating phases [1,2] and [5,6] and stage 2  actuating phases [7,8], and [7,6] .
		#At each time a single intersection stage is actuated
		self._di_stages_sign_intersection=val_di_stages_sign_intersection
		
		
		#the intersection control matrix, initiliases a zero and value zero always.
		#the current value fo the intersection control matrix is contained with the intersection control object
		#key=id allowed phase (for ex ni Uturns or any other not allowed mov),value=0
		self._di_intersection_control_matrix=self.fct_creat_di_key_id_phase_value_zero()
		
		#the intersection control object, will be initialised to None and will be contstructed by thte control algo,
		self._intersection_control_obj=val_intersection_control_obj
		
				
				
		#control actuate object
		self._ctrl_actuate_obj=val_ctrl_actuate_obj
		
				
#*****************************************************************************************************************************************************************************************
	#method returning the dictionary with the intersection stages
	def get_di_stages_sign_intersection(self):
		return self._di_stages_sign_intersection
		
#*****************************************************************************************************************************************************************************************
	#method returning the intersection control matrix
	def get_di_intersection_control_matrix(self):
		return self._di_intersection_control_matrix
#*****************************************************************************************************************************************************************************************
	#method returning the intersection control  objet
	def get_intersection_control_obj(self):
		return self._intersection_control_obj
#*****************************************************************************************************************************************************************************************
	#method returning the list with the times at which each planned  control is going to start
	#def get_li_t_start_new_inters_control_when_flux_monitoring(self):
		#return self._li_t_start_new_inters_control_when_flux_monitoring
	
#*****************************************************************************************************************************************************************************************
	#method returning the variable indicating he time of the last request of the control revision in this intersection when flux monitoring
	#def get_t_last_request_ctrl_revision_when_flux_monitoring(self):
		#return self._t_last_request_ctrl_revision_when_flux_monitoring

#*****************************************************************************************************************************************************************************************
	#method returning the variable indicating how many times a control revision is asked for the same time
	#def get_nb_times_ctrl_revision_corresponding_to_t_last_request_ctrl_revision_when_flux_monitoring(self):
		#return self._nb_times_ctrl_revision_corresponding_to_t_last_request_ctrl_revision_when_flux_monitoring

#*****************************************************************************************************************************************************************************************
	#method returning the variable indicating the time at which the ctrl is going to be  updated
	#def get_t_ctrl_revision_because_flux_var(self):
		#return self._t_ctrl_revision_because_flux_var
#*****************************************************************************************************************************************************************************************
	#method returning the ariable indicating the time at which the control should be revised because of its max duration
	#def get_t_ctrl_revision_because_max_ctrl_dur(self):
		#return self._t_ctrl_revision_because_max_ctrl_dur
#*****************************************************************************************************************************************************************************************
	#method returning the variable indicating the number of  times we have made a request for the ctrl to be updated, at a given time 
	#def get_nb_ev_related_to_t_ctrl_revision_because_flux_var(self):
		#return self._nb_ev_related_to_t_ctrl_revision_because_flux_var

#*****************************************************************************************************************************************************************************************
	#method retruning the list with the times at which each planned  control is going to start
	#def get_li_t_start_new_inters_control(self):
		#return self._li_t_start_new_inters_control

#*****************************************************************************************************************************************************************************************
	#method returning the list with the nb of new controls associated with  the ith element of  self._li_t_start_new_inters_control
	#def get_nb_ev_new_inters_ctrl_associated_with_each_t_of_li_t_start_new_inters_ctrl_when_fl_monit(self):
		#return self._nb_ev_new_inters_ctrl_associated_with_each_t_of_li_t_start_new_inters_ctrl_when_fl_monit

#*****************************************************************************************************************************************************************************************
	#method returning the variable indicating whether the new planned control is applied
	#def get_new_planned_ctrl_already_applied(self):
		#return self._new_planned_ctrl_already_applied

#*****************************************************************************************************************************************************************************************
	#method returning the time at which a new  control will be applied to the network (by event ev_new_ic)
	#def get_t_start_new_inters_ctrl(self):
		#return self._t_start_new_inters_ctrl

#*****************************************************************************************************************************************************************************************
	#method returning the control actuate object
	def get_ctrl_actuate_obj(self):
		return self._ctrl_actuate_obj
#*****************************************************************************************************************************************************************************************
	#method modifying the dictionary with the intersection stages
	def set_di_stages_sign_intersection(self,n_v):
		self._di_stages_sign_intersection=n_v
		
#*****************************************************************************************************************************************************************************************
	#method modifying the intersection control matrix
	def set_di_intersection_control_matrix(self,n_v):
		self._di_intersection_control_matrix=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the intersection control  objet
	def set_intersection_control_obj(self,n_v):
		self._intersection_control_obj=n_v
	
#*****************************************************************************************************************************************************************************************
	#method modifying the variable indicating he time of the last request of the control revision in this intersection when flux monitoring
	#def set_t_last_request_ctrl_revision_when_flux_monitoring(self,n_v):
		#self._t_last_request_ctrl_revision_when_flux_monitoring=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the variable indicating whether the new planned control is applied
	#def set_new_planned_ctrl_already_applied(self,n_v):
		#self._new_planned_ctrl_already_applied=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the variable indicating the time at which the ctrl is going to be  updated
	#def set_t_ctrl_revision_because_flux_var(self,n_v):
		#self._t_ctrl_revision_because_flux_var=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the variable indicating the time at which the control should be revised because of its max duration
	#def set_t_ctrl_revision_because_max_ctrl_dur(self,n_v):
		#self._t_ctrl_revision_because_max_ctrl_dur=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the variable indicating the number of  times we have made a request for the ctrl to be updated, at a given time 
	#def set_nb_ev_related_to_t_ctrl_revision_because_flux_var(self,n_v):
		#self._nb_ev_related_to_t_ctrl_revision_because_flux_var=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the list with the times at which each planned  control is going to start
	#def set_li_t_start_new_inters_control_when_flux_monitoring(self,n_v):
		#self._li_t_start_new_inters_control_when_flux_monitoring=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the variable indicating how many times a control revision is asked for the same time
	#def set_nb_times_ctrl_revision_corresponding_to_t_last_request_ctrl_revision_when_flux_monitoring(self,n_v):
		#self._nb_times_ctrl_revision_corresponding_to_t_last_request_ctrl_revision_when_flux_monitoring=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the list with the nb of new controls associated with  the ith element of  self._li_t_start_new_inters_control
	#def set_nb_ev_new_inters_ctrl_associated_with_each_t_of_li_t_start_new_inters_ctrl_when_fl_monit(self,n_v):
		#self._nb_ev_new_inters_ctrl_associated_with_each_t_of_li_t_start_new_inters_ctrl_when_fl_monit=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the control actuate object
	def set_ctrl_actuate_obj(self,n_v):
		self._ctrl_actuate_obj=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the time at which a new  control will be applied to the network (by event ev_new_ic)
	#def set_t_start_new_inters_ctrl(self,n_v):
		#self._t_start_new_inters_ctrl=n_v

#*****************************************************************************************************************************************************************************************
	
	#method creating a dictionary, key=id phase (of which the sat flow >0 and  que is not RT), value=0
	#this dictionary will correspond to the intersection control matrix
	def fct_creat_di_key_id_phase_value_zero(self):
	
		#dictionary=key =phase id, value=0
		di_rep={}
		#for each phase of each stage
		for i in self._di_stages_sign_intersection:
			for j in self._di_stages_sign_intersection[i]:
				di_rep[j[0],j[1]]=0
				
		return di_rep
				

#*****************************************************************************************************************************************************************************************
	#method creating a dictionary, key=id phase (of which the sat flow >0 and  que is not RT), value=0
	#this dictionary will correspond to the intersection control matrix
	def fct_creat_di_key_id_phase_value_zero_1(self):
	
		#dictionary=key =phase id, value=0
		di_rep={}
		#for each input link to the node
		#print("here", self._id_node)
		for i in self._li_id_input_network_links_to_inters_node:
			#print("i=",i)
			#print("i=",i,val_network.get_di_entry_internal_links()[i].get_set_veh_queue().get_di_obj_veh_queue_at_link())
			for j in val_network.get_di_entry_internal_links()[i].get_set_veh_queue().get_di_obj_veh_queue_at_link():
				
				if val_network.get_di_entry_internal_links()[i].get_set_veh_queue().get_di_obj_veh_queue_at_link()[j].\
				get_type_veh_queue()!=Cl_Vehicle_Queue.TYPE_VEHICLE_QUEUE["right_turn"]:
					di_rep[j]=0
		
		return di_rep
				

#*****************************************************************************************************************************************************************************************
	#method returning ine if there is at leasat one queue of the actuated stage having value > given value
	def fct_examing_existence_que_actuates_stage_with_flow_sup_given_value(self,val_network,val_fmin):
		rep=0
		
		#for each que of the actuate stage
		for i in self._di_stages_sign_intersection[self._intersection_control_obj.get_id_actuated_stage()]:
			if len(val_network.get_di_entry_internal_links()[i[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()[i[0],i[1]].get_queue_veh())>val_fmin:
				return 1
		if rep==0:
			return 0
				

#*****************************************************************************************************************************************************************************************





		
		
	
		