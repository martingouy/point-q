import string
import Cl_Event
import Cl_Ev_new_intersection_control
import List_Explicit_Values
import Cl_Vehicle
import Cl_Global_Functions
import Cl_Decisions
import Cl_Control_Actuate   
import Cl_Record_Database


class Ev_end_decision_next_intersection_control(Cl_Event.Event):

	def __init__(self,val_ev_time=-1,val_id_intersection_node=-1,val_t_end_last_intersection_control_matrix=-1,\
	val_type_control_to_employ=-1,val_indicat_whether_estim_turn_ratio_values=-1):
	#,val_control_category=None,\
	#val_reason_ctrl_revision_t_lim=None):
	
		gl_funct_obj=Cl_Global_Functions.Global_Functions()
		#decision_obj=Cl_Decisions.Decisions()
		
		Cl_Event.Event.__init__(self,val_event_time=val_ev_time,\
		val_event_type=Cl_Event.TYPE_EV["type_ev_end_decision_next_intersection_control"],val_global_fct_obj=gl_funct_obj)
		
		#the decision object
		#self._decision_obj=decision_obj
	
		#the intersection id
		self._id_intersection_node=val_id_intersection_node
		
		#the time at which ends the (last planned)  intersection control matrix
		self._t_end_last_intersection_control_matrix=val_t_end_last_intersection_control_matrix
		
		#the type of network control policy (1:FT, 2:MP, 3:mixed)
		self._type_control_to_employ=val_type_control_to_employ
		
		
		#variable indicating whether the turn ratio values will be estimated or not during the current decisison
		self._indicat_whether_estim_turn_ratio_values=val_indicat_whether_estim_turn_ratio_values
		
		
		#the type of the currently used control 
		#this member has a sense  when a  mixed type of control is  employed
		#self._type_current_control_when_mixed_policy_employed=val_type_current_control_when_mixed_policy_employed
		
		#variable indicating whether the control to employ requires or not sensor monitoring fot the t update
		#self._control_category=val_control_category
		
		
	
		#variable employed in the case fof controls requiring sensor monitoring  of which the actuated stages are constrained
		# by a limited continuous actuated duration
		#it indicates whether this event is generated simply for deciding a new control  or becauce the limit time of the control is reached 
		#and a different ctrl should be selected
		#if this variable values to 1, the reason of this event is because the t _lim of the current control is reached, 0 otherwise
		#self._reason_ctrl_revision_t_lim=val_reason_ctrl_revision_t_lim
		
#*****************************************************************************************************************************************************************************************
	#method returning the decision object
	#def get_decision_obj(self):
		#return self._decision_obj

#*****************************************************************************************************************************************************************************************
	#method returning the intersection id
	def get_id_intersection_node(self):
		return self._id_intersection_node

#*****************************************************************************************************************************************************************************************
	#method returning the time at which ends the last planned intersection control matrix
	def get_t_end_last_intersection_control_matrix(self):
		return self._t_end_last_intersection_control_matrix
#*****************************************************************************************************************************************************************************************
	#method returning the type of the control  applied in the next control
	def get_type_control_to_employ(self):
		return self._type_control_to_employ
#*****************************************************************************************************************************************************************************************
	#method returning the type of the control  applied in the next control
	def get_type_control_to_employl(self):
		return self._type_control_to_employ
#*****************************************************************************************************************************************************************************************
	#method returning the variable whether the turn ratio values will be estimated or not during the current decisison
	def get_indicat_whether_estim_turn_ratio_values(self):
		return self._indicat_whether_estim_turn_ratio_values

#*****************************************************************************************************************************************************************************************
	#method returning the type of the currently empoyed control when self._type_control=3
	#def get_type_current_control_when_mixed_policy_employed(self):
		#return self._type_current_control_when_mixed_policy_employed
	
#*****************************************************************************************************************************************************************************************
	#method retruning the variable indicating whether the control to employ requires or not sensor monitoring
	#def get_control_category(self):
		#return self._control_category

#*****************************************************************************************************************************************************************************************
	#method returning whether the control needs to be updated because its t_lim soon will be reached or not
	#def get_reason_ctrl_revision_t_lim(self):
		#return self._reason_ctrl_revision_t_lim


#*****************************************************************************************************************************************************************************************
	#method modifying the decision object
	#def set_decision_obj(self,n_v):
		#self._decision_obj=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the intersection id
	def set_id_intersection_node(self,n_v):
		self._id_intersection_node=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying he time at which ends the last planned intersection control matrix
	def set_t_end_last_intersection_control_matrix(self,n_v):
		self._t_end_last_intersection_control_matrix=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the type of the control  applied in the next control
	def set_type_control_to_employ(self,n_v):
		self._type_control_to_employ=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the variable whether the turn ratio values will be estimated or not during the current decisison
	def set_indicat_whether_estim_turn_ratio_values(self,n_v):
		self._indicat_whether_estim_turn_ratio_values=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the type of the currently empoyed control when self._type_control=3
	#def set_type_current_control_when_mixed_policy_employed(self,n_v):
		#self._type_current_control_when_mixed_policy_employed=n_v
	
	
#*****************************************************************************************************************************************************************************************
	#method modifying the variable indicating whether the control to employ requires or not sensor monitoring
	#def set_control_category(self,n_v):
		#self._control_category=n_v

#*****************************************************************************************************************************************************************************************

	#method modying the variable indicating whether the control needs to be updated because its t_lim soon will be reached or not
	#def set_reason_ctrl_revision_t_lim(self,n_v):
		#self._reason_ctrl_revision_t_lim=n_v

#*****************************************************************************************************************************************************************************************
#*****************************************************************************************************************************************************************************************
#*****************************************************************************************************************************************************************************************
	#method treating the event
	def event_treat(self,val_network,val_t_unit,val_round_precis,val_t_round_prec,val_ev_list,val_file_recording_event_db,v_dt,\
	val_sim_dur,val_t_start_sim,val_init_small_val=-10**10):
	
			
		
	
		#we decide of the  control of the next period
		#li_ic_obj_and_ev_end_dec_next_ic=
		#[li_ico, type next control to employ, 1 ou 0 according as if an event end_next_decision control will /not be generated,1 or 2 for indicating the key 
		#in the dictionary for selecting the employed rout prob (estimated or not) at the next decision]
		#or None
		li_ic_obj_and_ev_end_dec_next_ic=val_network.get_di_intersections()[self._id_intersection_node].get_ctrl_actuate_obj().\
		fct_select_appropriate_control(\
		va_id_nd=self._id_intersection_node,\
		va_type_control_to_employ=self._type_control_to_employ,\
		val_indicator_whether_estim_rout_prob_during_first_decis=self._indicat_whether_estim_turn_ratio_values,\
		va_di_inters_control_matrix=val_network.get_di_intersections()[self._id_intersection_node].\
		get_di_intersection_control_matrix(),\
		va_di_intersection_stages=val_network.get_di_intersections()[self._id_intersection_node].get_di_stages_sign_intersection(),\
		va_t_end_current_intersection_control=self._t_end_last_intersection_control_matrix,\
		va_t_unit=val_t_unit,\
		va_round_precis=val_round_precis,\
		va_t_round_prec=val_t_round_prec,\
		va_network=val_network,\
		va_init_small_val=val_init_small_val,\
		val_t_current=self._event_time,\
		va_sim_dur=	val_sim_dur,\
		va_marge_dt=v_dt,\
		va_t_start_sim=val_t_start_sim)
		
		#if  a stage is selected
		if li_ic_obj_and_ev_end_dec_next_ic !=None:
		
			#if at current time we can define when it will be the next control update
			if  li_ic_obj_and_ev_end_dec_next_ic[List_Explicit_Values.val_third_element_of_list]==1:
			
				#we generate the next event end decision
				ev_end_deci_next_icm=Ev_end_decision_next_intersection_control(\
				val_ev_time=li_ic_obj_and_ev_end_dec_next_ic[0][len(li_ic_obj_and_ev_end_dec_next_ic[0])-1].get_t_update_ctrl(),\
				val_id_intersection_node=self._id_intersection_node,\
				val_t_end_last_intersection_control_matrix=li_ic_obj_and_ev_end_dec_next_ic[0][len(li_ic_obj_and_ev_end_dec_next_ic[0])-1].get_t_end_control(),\
				val_type_control_to_employ=li_ic_obj_and_ev_end_dec_next_ic[1],\
				val_indicat_whether_estim_turn_ratio_values=li_ic_obj_and_ev_end_dec_next_ic[3])
			
				#on insert the event ev_end_dec_next_icm into the event list
				ev_end_deci_next_icm.fct_insertion_even_in_event_list(event_list=val_ev_list,\
				message="IN CL_Ev_end_decision_next_intersection_control IN FUNCT event_treat,\
				NEXT ev_new_end_dec_netw_control EVENT HAS TIME < TIME FIRST EVENT IN THE LIST")
				
				
			nb_ctrls_planned=len(li_ic_obj_and_ev_end_dec_next_ic[List_Explicit_Values.val_first_element_of_list])
			
			for i in range(nb_ctrls_planned):
			
				ev_new_ic=Cl_Ev_new_intersection_control.Ev_new_intersection_control(\
				val_ev_time= li_ic_obj_and_ev_end_dec_next_ic[List_Explicit_Values.val_first_element_of_list][i].get_t_start_control(),\
				val_id_intersection_node=self._id_intersection_node,\
				val_intersection_control_obj=\
				li_ic_obj_and_ev_end_dec_next_ic[List_Explicit_Values.val_first_element_of_list][i])
					
					
				ev_new_ic.fct_insertion_even_in_event_list(event_list=val_ev_list,\
				message="IN Ev_end_decision_next_intersection_control IN FUNCT event_treat,\
				EVENT NEW  INTERSECTION CONTROL HAS TIME < TIME FIRST EVENT IN THE LIST")
				
				
			li_li_t_start_duration_control=[]
			
			for m in li_ic_obj_and_ev_end_dec_next_ic[0]:
				li_t_start_duration_control=[m.get_t_start_control(),m.get_duration_control()]
					
				li_li_t_start_duration_control.append(li_t_start_duration_control)
					
			#we create a record database object 
			record_db_obj=Cl_Record_Database.Record_Database(\
			val_file_db=val_file_recording_event_db,\
			val_ev_time=self._event_time,\
			val_ev_type=self._event_type,\
			val_id_inters_node=self._id_intersection_node,\
			val_t_start_t_duration_sequence_next_inters_control_mat=li_li_t_start_duration_control,\
			val_dt_min_margin_for_calcul_next_inters_control=v_dt)
			#,\
			#val_duration_current_cycle=va_duration_current_cycle)
				
				
			#we record the event in the db 
			record_db_obj.fct_write_object_in_db_file()
		
		












































