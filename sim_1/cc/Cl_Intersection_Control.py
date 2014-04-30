import List_Explicit_Values
import Cl_Control_Actuate

#TYPE_CONTROL={"other":0,"type_control_red_clear":1}


class Intersection_Control:

	def __init__(self,val_di_intersection_control_mat,val_t_start_control, \
	val_type_control,val_type_control_related_to_t_revision,\
	val_t_end_control,val_duration_control,\
	val_estim_turn_ratios_with_current_ctrl,\
	val_id_actuated_stage=-1,\
	val_t_start_cycle_associated_with_control=-1,\
	val_cycle_duration_associated_with_control=-1,val_t_max_permitted_current_stage=-1,\
	val_t_update_ctrl=-1,\
	val_t_duration_for_defining_t_ctrl_revision_when_at_given_time_sensor_records_veh_variation=-1):
	
		#the id of the intersection node
		#self._id_intersection_node=val_id_intersection_node
		
		#list with the id of the actuated stages
		#self._li_id_actuated_intersect_stages=val_li_id_actuated_intersect_stages
		
		#the dictionary with the  intersection controls, key=phase id, value=1 or 0 according to whether the control actuates the related phase
		#the number of keys=the number of the intersection phases
		self._di_intersection_control_mat=val_di_intersection_control_mat
		
		#the time at which the control starts
		self._t_start_control=val_t_start_control
		
		#the time at which the control ends
		self._t_end_control=val_t_end_control
		
		#the duration of the control
		self._duration_control=val_duration_control
		
		#the time at which the cycle associated with this control starts
		self._t_start_associated_cycle_with_control=val_t_start_cycle_associated_with_control
		
		#the duration of the cycle associated with this control
		self._cycle_duration_associated_with_control=val_cycle_duration_associated_with_control
		
		#the t latest at which the current stage can be actuated (case of continous actuation duration e.g. FA with max green)
		self._t_max_permitted_current_stage=val_t_max_permitted_current_stage
		
		
		#the type of the current control, MP, FT etc. The ctrl types are in Cl_Control_Actuate.py 
		self._type_control=val_type_control
		
		#variable indicating the control type related to the time at which it will be revised (requiring sensor monitoring or not)
		#the corresponding dict of types is in Cl_Control_Actuate
		self._type_control_related_to_t_revision=val_type_control_related_to_t_revision
		
	
		#variable indicating the id of the selected stage (we employs it for FA Max Green ctrl)
		self._id_actuated_stage=val_id_actuated_stage
		
		#variable indicating the time t which the control should be updated (required for all ctls having a predefined limited duration)
		self._t_update_ctrl=val_t_update_ctrl
		
		#variable indicating if withinh the current control the turn rations will be estimated (if val=1) or not (val=0)
		self._estim_turn_ratios_with_current_ctrl=val_estim_turn_ratios_with_current_ctrl
		
		#variable indicating the duration from a given time at which the control depending upon sensor recording for the t update,
		#will be revised (if the revision will be decided)
		self._t_duration_for_defining_t_ctrl_revision_when_at_given_time_sensor_records_veh_variation=\
		val_t_duration_for_defining_t_ctrl_revision_when_at_given_time_sensor_records_veh_variation
		
			
#*****************************************************************************************************************************************************************************************
	#method returning the  id of the intersection node
	#def get_id_intersection_node(self):
		#return self._id_intersection_node

#*****************************************************************************************************************************************************************************************
	#method returning the list of with theid of  the actiated stages by the current control
	#def get_li_id_actuated_intersect_stages(self):
		#return self._li_id_actuated_intersect_stages
#*****************************************************************************************************************************************************************************************
	#method returning the dictionary with the  intersection controls,
	# key=phase id, value=1 or 0 according to whether the control actuates the related phase
	def get_di_intersection_control_mat(self):
		return self._di_intersection_control_mat
#*****************************************************************************************************************************************************************************************
	#method returning the time at which the control starts
	def get_t_start_control(self):
		return self._t_start_control

#*****************************************************************************************************************************************************************************************
	#method returning the time at which the control ends
	def get_t_end_control(self):
		return self._t_end_control
#*****************************************************************************************************************************************************************************************
	#metho returning the duration of the control
	def get_duration_control(self):
		return self._duration_control

#*****************************************************************************************************************************************************************************************
	#method returning the time at which the cycle associated with this control starts
	def get_t_start_associated_cycle_with_control(self):
		return self._t_start_associated_cycle_with_control
	
#*****************************************************************************************************************************************************************************************
	#method returning the duration of the cycle associated with this control
	def get_cycle_duration_associated_with_control(self):
		return self._cycle_duration_associated_with_control

#*****************************************************************************************************************************************************************************************
	#method returning the  latest at which the current stage can be actuated 
	def get_t_max_permitted_current_stage(self):
		return self._t_max_permitted_current_stage
#*****************************************************************************************************************************************************************************************
	#method returning the type of the cotnrol
	def get_type_control(self):
		return self._type_control
#*****************************************************************************************************************************************************************************************
	#method returning the type of the control related to the time at which it wil be updated (whether it requires or not sensor monitor)
	def get_type_control_related_to_t_revision(self):
		return self._type_control_related_to_t_revision
	

#*****************************************************************************************************************************************************************************************
	#methode returning the id of the actuated  stage
	def get_id_actuated_stage(self):
		return self._id_actuated_stage
	
#*****************************************************************************************************************************************************************************************
	#method modifying the  id of the intersection node
	#def set_id_intersection_node(self,n_v):
		#self._id_intersection_node=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the list of with theid of  the actiated stages by the current control
	#def set_li_id_actuated_intersect_stages(self,n_v):
		#self._li_id_actuated_intersect_stages=n_v
#*****************************************************************************************************************************************************************************************
	#method retuning the time at which this control should be updated
	def get_t_update_ctrl(self):
		return self._t_update_ctrl

#*****************************************************************************************************************************************************************************************
	#method returning the variable indicating if withinh the current control the turn rations will be estimated
	def get_estim_turn_ratios_with_current_ctrl(self):
		return self._estim_turn_ratios_with_current_ctrl

#*****************************************************************************************************************************************************************************************
	#method returning the variable indicating the duration from a given time at which the control depending upon sensor recording for the t update,
	#will be revised 
	def get_t_duration_for_defining_t_ctrl_revision_when_at_given_time_sensor_records_veh_variation(self):
		return self._t_duration_for_defining_t_ctrl_revision_when_at_given_time_sensor_records_veh_variation

#*****************************************************************************************************************************************************************************************
	#method modifying the dictionary with the  intersection controls,
	# key=phase id, value=1 or 0 according to whether the control actuates the related phase
	def set_di_intersection_control_mat(self,n_v):
		self._di_intersection_control_mat=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the time at which the control starts
	def set_t_start_control(self,n_v):
		self._t_start_control=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the time at which the control ends
	def set_t_end_control(self,n_v):
		self._t_end_control=n_v
#*****************************************************************************************************************************************************************************************
	#metho modifying the duration of the control
	def set_duration_control(self,n_v):
		self._duration_control=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the time at which the cycle associated with this control starts
	def set_t_start_associated_cycle_with_control(self,n_v):
		self._t_start_associated_cycle_with_control=n_v
	
#*****************************************************************************************************************************************************************************************
	#method modifying the duration of the cycle associated with this control
	def set_cycle_duration_associated_with_control(self,n_v):
		self._cycle_duration_associated_with_control=n_v


#*****************************************************************************************************************************************************************************************
	#method modifying the  latest at which the current stage can be actuated 
	def set_t_max_permitted_current_stage(self,n_v):
		self._t_max_permitted_current_stage=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the type of the cotnrol
	def set_type_control(self,n_v):
		self._type_control=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the type of the control related to the time at which it wil be updated (whether it requires or not sensor monitor)
	def set_type_control_related_to_t_revision(self,n_v):
		self._type_control_related_to_t_revision=n_v
	

#*****************************************************************************************************************************************************************************************
	
	#method modifying the time at which this control should be updated
	def set_t_update_ctrl(self,n_v):
		self._t_update_ctrl=n_v
	
#*****************************************************************************************************************************************************************************************
	#method modifying the variable indicating if withinh the current control the turn rations will be estimated
	def set_estim_turn_ratios_with_current_ctrl(self,n_v):
		self._estim_turn_ratios_with_current_ctrl=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the variable indicating the duration from a given time at which the control depending upon sensor recording for the t update,
	#will be revised 
	def set_t_duration_for_defining_t_ctrl_revision_when_at_given_time_sensor_records_veh_variation(self,n_v):
		self._t_duration_for_defining_t_ctrl_revision_when_at_given_time_sensor_records_veh_variation=n_v

#*****************************************************************************************************************************************************************************************
	

	
		