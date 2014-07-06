import Cl_Event
import Cl_Vehicle
import Cl_Global_Functions
import List_Explicit_Values
import Cl_Ev_veh_arrived_at_que
import Cl_Ev_veh_arrived_at_que_nsi
import Cl_Ev_end_veh_hold_at_que
import Cl_Ev_end_decision_next_intersection_control
import Cl_Vehicle_Queue
import Cl_Network_Link
import Cl_Decisions
import Cl_Record_Database
import Cl_Intersection
import List_Explicit_Values
import Cl_Control_Actuate
import Global_Functions
import math

class Ev_end_veh_departure_from_que(Cl_Event.Event):

	"""class defining the event of a vehicle departing from a queue  """
	
	def __init__(self,val_ev_t=-1,val_id_queue_obj=-1,val_nb_depart_veh=-1):
	
		gl_funct_obj=Cl_Global_Functions.Global_Functions()
		
		Cl_Event.Event.__init__(self,val_event_time=val_ev_t,\
		val_event_type=Cl_Event.TYPE_EV["type_ev_end_veh_departure_from_que"],\
		val_global_fct_obj=gl_funct_obj)
		
		#the id of vehicle queue object associated with this event
		self._id_queue_obj=val_id_queue_obj
		
		#the number of departed vehicles
		self._nb_depart_veh=val_nb_depart_veh
		
		#the decision object  associated with this event
		obj_decisions=Cl_Decisions.Decisions()
		
		self._obj_decisions=obj_decisions
		
		#dictionary with the functions treat each case of this event
		#self._di_fct_ev_dep_treat={1:fct_treat_event_case_finite_lk_capacity,2:fct_treat_event_case_infinite_lk_capacity}
		
#*****************************************************************************************************************************************************************************************
	#method returning the id of vehicle queue object associated with this event
	def get_id_queue_obj(self):
		return self._id_queue_obj

#*****************************************************************************************************************************************************************************************
	#method returning the decision object  associated with this event
	def get_obj_decisions(self):
		return self._obj_decisions

#*****************************************************************************************************************************************************************************************
	#method returinig the number of departed vehicles
	def get_nb_depart_veh(self):
		return self._nb_depart_veh

#*****************************************************************************************************************************************************************************************
	#method returning the dictionary with the functions treat each case of this event
	#def get_di_fct_ev_dep_treat(self):
		#return self._di_fct_ev_dep_treat
	
#*****************************************************************************************************************************************************************************************
	
	#method modifying the id of the vehicle queue object associated with this event
	def set_id_queue_obj(self,n_v):
		self._id_queue_obj=n_v

#*****************************************************************************************************************************************************************************************
	
	#method modifying the decision object  associated with this event
	def set_obj_decisions(self,n_v):
		self._obj_decisions=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the number of departed vehicles
	def set_nb_depart_veh(self,n_v):
		self._nb_depart_veh=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the dictionary with the functions treat each case of this event
	#def set_di_fct_ev_dep_treat(self,n_v):
		#self._di_fct_ev_dep_treat=n_v
	
#*****************************************************************************************************************************************************************************************
	
	#method treating the case when exam whether other vehicles can leave the que
	def fct_treat_case_exam_other_veh_can_leave_que(self,val_id_que,val_netwk,val_t_unit,val_min_hold_time_veh_in_que,\
	val_fct_calcul_nb_and_t_dep_veh,va_round_prec,ev_li):
		
		
		#the time at which the new control is going to start
		t_end_control=val_netwk.get_di_intersections()[val_netwk.get_di_entry_internal_links()[self._id_queue_obj[0]].\
		get_id_head_intersection_node()].get_intersection_control_obj().get_t_end_control()+val_t_unit
		
		#if the que is RT
		if val_netwk.get_di_entry_internal_links()[val_id_que[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[val_id_que[0],val_id_que[1]].get_type_veh_queue()==Cl_Vehicle_Queue.TYPE_VEHICLE_QUEUE["right_turn"]:
		
		
			#t_end_control=val_netwk.get_current_network_control_obj().get_t_start_control()+\
			#val_netwk.get_current_network_control_obj().get_t_duration_control()
					
			#lis_par_fct_calcul_nb_and_t_dep_veh=[self._event_time,val_t_unit,\
			#val_netwk.get_di_entry_internal_links()[self._id_queue_obj[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
			#[val_id_que[0],val_id_que[1]],\
			#val_min_hold_time_veh_in_que,t_end_control,val_netwk,va_vect_nb_veh_to_exam,va_round_prec]
			
			
			
			lis_par_fct_calcul_nb_and_t_dep_veh=[self._event_time,val_t_unit,\
			val_netwk.get_di_entry_internal_links()[val_id_que[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
			[val_id_que[0],val_id_que[1]],\
			val_min_hold_time_veh_in_que,\
			t_end_control,val_netwk,va_round_prec]
				 
				
			nb_dep_veh=self._global_fct_obj.fct_treat_case_veh_can_go(\
			t_current=self._event_time,t_unit=val_t_unit,\
			fct_calcul_nb_and_t_dep_veh=val_fct_calcul_nb_and_t_dep_veh,\
			li_param_fct_calcul_nb_and_t_dep_veh=lis_par_fct_calcul_nb_and_t_dep_veh,\
			id_que=[val_id_que[0],val_id_que[1]],val_netw=val_netwk,val_t_round_prec=va_round_prec,ev_list=ev_li)
					
			
		
		#if the queue is not RT
		else:
			#this is actually the time at which the new control will be applied
			#t_end_control=val_netwk.get_current_network_control_obj().get_t_start_control()+\
			#val_netwk.get_current_network_control_obj().get_t_duration_control()

			#if the current control is one, we examine how many vehicles can go 
			
			if val_netwk.get_di_intersections()[val_netwk.get_di_entry_internal_links()[self._id_queue_obj[0]].\
			get_id_head_intersection_node()].\
			get_intersection_control_obj().get_di_intersection_control_mat()\
			[val_id_que[0],val_id_que[1]]==List_Explicit_Values.initialisation_value_to_one:
			
			
				#lis_par_fct_calcul_nb_and_t_dep_veh=[self._event_time,val_t_unit,\
				#val_netwk.get_di_entry_internal_links()[val_id_que[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
				#[val_id_que[0],val_id_que[1]],\
				#val_min_hold_time_veh_in_que,t_end_control,val_netwk,va_vect_nb_veh_to_exam,va_round_prec]
				
				lis_par_fct_calcul_nb_and_t_dep_veh=[self._event_time,val_t_unit,\
				val_netwk.get_di_entry_internal_links()[val_id_que[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
				[val_id_que[0],val_id_que[1]],\
				val_min_hold_time_veh_in_que,\
				t_end_control,val_netwk,va_round_prec]
				
				nb_dep_veh=self._global_fct_obj.fct_treat_case_veh_can_go(\
				t_current=self._event_time,t_unit=val_t_unit,\
				fct_calcul_nb_and_t_dep_veh=val_fct_calcul_nb_and_t_dep_veh,\
				li_param_fct_calcul_nb_and_t_dep_veh=lis_par_fct_calcul_nb_and_t_dep_veh,\
				id_que=[val_id_que[0],val_id_que[1]],val_netw=val_netwk,val_t_round_prec=va_round_prec,ev_list=ev_li)
			else:
				nb_dep_veh=0
		
		return nb_dep_veh
					
						
#*****************************************************************************************************************************************************************************************
	#method treating the case of examining if other vehs can leave from the current queue or the related minor or prior phases, in the case
	#when the current queue id prior, minor or any other regular  type
	def fct_treat_case_exam_other_veh_can_leave_current_or_other_que(self,val_netw,val_ti_unit,val_min_hold_time_duration,\
	val_fct_calcul_nb_and_t_dep_veh,val_round_precis,v_ev_list):
	
		
		#if the current queue corresponds to a minor phase, we examine if vehicles from each one of the related prior queues can leave
		#if val_netw.get_di_entry_internal_links()[self._id_queue_obj[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()[self._id_queue_obj[0],self._id_queue_obj[1]].\
		 #get_type_related_phase()==Cl_Vehicle_Queue.TYPE_RELATED_PHASE["minor_mv"]:
		 
			#indicator veh departures exam from the related prior movement
			#indic_veh_depar_prior_mv=0
			 
			#for each related prior phase to the current minor phase
			#for p in val_netw.get_di_entry_internal_links()[self._id_queue_obj[0]].get_set_veh_queue().\
			#get_di_obj_veh_queue_at_link()[self._id_queue_obj[0],self._id_queue_obj[1]].get_li_id_minor_prior_phases_related_to_que():
			
				#if there are vehs in the prior movement
				#if val_netw.get_di_entry_internal_links()[p[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()[p[0],p[1]].get_queue_veh() !=[]:
				
					#nb_veh_to_go=self.fct_treat_case_exam_other_veh_can_leave_que(\
					#val_id_que=p,val_netwk=val_netw,\
					#val_t_unit=val_ti_unit,val_min_hold_time_veh_in_que=val_min_hold_time_duration,\
					#val_fct_calcul_nb_and_t_dep_veh=val_fct_calcul_nb_and_t_dep_veh,\
					#va_round_prec=val_round_precis,\
					#ev_li=v_ev_list)
					
					#if nb_veh_to_go >0 and indic_veh_depar_prior_mv==0:
						#indic_veh_depar_prior_mv=1
				
			#if  no vehicle from a prior movement can leave, we examine if vehs can leave from the current minor movement
			#if indic_veh_depar_prior_mv==0:
				#nb_veh_to_go=self.fct_treat_case_exam_other_veh_can_leave_que(\
				#val_id_que=self._id_queue_obj,val_netwk=val_netw,\
				#val_t_unit=val_ti_unit,val_min_hold_time_veh_in_que=val_min_hold_time_duration,\
				#val_fct_calcul_nb_and_t_dep_veh=val_fct_calcul_nb_and_t_dep_veh,va_round_prec=val_round_precis,ev_li=v_ev_list)

		
		#if the queue correspons to a prior phase, 
		#elif val_netw.get_di_entry_internal_links()[self._id_queue_obj[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()[self._id_queue_obj[0],self._id_queue_obj[1]].\
		 #get_type_related_phase()==Cl_Vehicle_Queue.TYPE_RELATED_PHASE["prior_mv"]:
		 
			#we examine if other vehicles can leave from the current prior phase
			#nb_veh_to_go=self.fct_treat_case_exam_other_veh_can_leave_que(\
			#val_id_que=self._id_queue_obj,val_netwk=val_netw,\
			#val_t_unit=val_ti_unit,val_min_hold_time_veh_in_que=val_min_hold_time_duration,\
			#val_fct_calcul_nb_and_t_dep_veh=val_fct_calcul_nb_and_t_dep_veh,va_round_prec=val_round_precis,ev_li=v_ev_list)

			#if no vehicle can leave the prior phase we examine if vehs can leave  from the related minor phases
			#HERE WE CONSIDER THAT ALL THE RELATED MINOR MOVS TO THE PRIOR ONE ARE NOT CONFLICTING WITH EACH OTHER 
			#if nb_veh_to_go==0:
				#for m in val_netw.get_di_entry_internal_links()[self._id_queue_obj[0]].get_set_veh_queue().\
				#get_di_obj_veh_queue_at_link()[self._id_queue_obj[0],self._id_queue_obj[1]].get_li_id_minor_prior_phases_related_to_que():
					#nb_veh_to_go=self.fct_treat_case_exam_other_veh_can_leave_que(\
					#val_id_que=m,val_netwk=val_netw,\
					#val_t_unit=val_ti_unit,val_min_hold_time_veh_in_que=val_min_hold_time_duration,\
					#val_fct_calcul_nb_and_t_dep_veh=val_fct_calcul_nb_and_t_dep_veh,\
					#va_round_prec=val_round_precis,\
					#ev_li=v_ev_list)
			
			
		##if the current queue corresponds to any other type of movement (no prior-minor), we examine if other vehs cal leave the que
		#else:
		
		nb_veh_to_go=self.fct_treat_case_exam_other_veh_can_leave_que(\
		val_id_que=self._id_queue_obj,val_netwk=val_netw,\
		val_t_unit=val_ti_unit,val_min_hold_time_veh_in_que=val_min_hold_time_duration,\
		val_fct_calcul_nb_and_t_dep_veh=val_fct_calcul_nb_and_t_dep_veh,va_round_prec=val_round_precis,ev_li=v_ev_list)
			
		return nb_veh_to_go
			
		

#*****************************************************************************************************************************************************************************************
	
	#method treating the case of a saturated vehicle origin link, allowing new vehicles to enter it after the departure of  currently located vehicles
	def fct_treat_case_new_arrivals_towards_sat_lk_after_veh_dep(self,val_network,val_min_hold_time,\
	val_ti_unit,val_fct_calcul_nb_and_t_dep_veh,va_round_prec,val_ev_list):
	
		
		#the number of vehicles to be examined if the can leave according to the sat flow,  employed in a micro management
		#va_vect_nb_veh_to_exam=Global_Functions.fct_defin_nb_veh_leave_mi(\
		#v_sat_flow=\
		#val_network.get_di_entry_internal_links()[self._id_queue_obj[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		#[self._id_queue_obj[0],self._id_queue_obj[1]].get_sat_flow_queue(),\
		#v_t_unit=val_ti_unit,v_round_prec=va_round_prec)
		
	
		#for each input link to the currently saturated link
		for i in val_network.get_di_entry_internal_links()[self._id_queue_obj[0]].get_li_id_input_links_to_link():
			
			#if the (i,get_li_id_input_links_to_link) phase is authorised
			#if val_network.get_di_entry_internal_links()[i].\
			#get_set_veh_queue().get_dict_queue_max_queue_size_et_sat_flow_queue_type_param_trav_durat()[\
			#i,self._id_queue_obj[0]][List_Explicit_Values.val_second_element_of_list]>0:
				
			
			#if the (i,self._id_queue_obj[0]) phase is not a RT
			if val_network.get_di_entry_internal_links()[i].\
			get_set_veh_queue().get_dict_queue_max_queue_size_et_sat_flow_queue_type()[\
			i,self._id_queue_obj[0]][List_Explicit_Values.val_third_element_of_list]==List_Explicit_Values.initialisation_value_to_zero:
				
				#if the current control permits this movement (= one)
				#if val_network.get_di_intersections()[val_network.get_di_entry_internal_links()[self._id_queue_obj[0]].\
				#get_id_head_intersection_node()].\
				#get_intersection_control_obj().get_di_intersection_control_mat()\
				#[self._id_queue_obj[0],self._id_queue_obj[1]]==List_Explicit_Values.initialisation_value_to_one:
				if val_network.get_di_intersections()[val_network.get_di_entry_internal_links()[i].\
				get_id_head_intersection_node()].\
				get_intersection_control_obj().get_di_intersection_control_mat()\
				[i,self._id_queue_obj[0]]==List_Explicit_Values.initialisation_value_to_one:
				
						
					#this is the 1st moment at which a new control will be applied
					#the time at which the new control will be applied to the network
					#t_end_control=round(val_network.get_di_intersections()[val_network.get_di_entry_internal_links()[\
					#self._id_queue_obj[0]].\
					#get_id_head_intersection_node()].get_intersection_control_obj().get_t_end_control()+val_ti_unit,va_round_prec)
					t_end_control=round(val_network.get_di_intersections()[val_network.get_di_entry_internal_links()[\
					i].get_id_head_intersection_node()].get_intersection_control_obj().get_t_end_control()+val_ti_unit,va_round_prec)
								
					#lis_par_fct_calcul_nb_and_t_dep_veh=[self._event_time,val_ti_unit,\
					#val_network.get_di_entry_internal_links()[self._id_queue_obj[0]].get_set_veh_queue().\
					#get_di_obj_veh_queue_at_link()[self._id_queue_obj[0],self._id_queue_obj[1]],\
					#val_min_hold_time,t_end_control,val_network,va_vect_nb_veh_to_exam,va_round_prec]
					lis_par_fct_calcul_nb_and_t_dep_veh=[self._event_time,val_ti_unit,\
					val_network.get_di_entry_internal_links()[i].get_set_veh_queue().\
					get_di_obj_veh_queue_at_link()[i,self._id_queue_obj[0]],\
					val_min_hold_time,t_end_control,val_network,va_round_prec]
				
					
					
					#nb_veh_to_go=self._global_fct_obj.fct_treat_case_veh_can_go(\
					#t_current=self._event_time,t_unit=val_ti_unit,\
					#fct_calcul_nb_and_t_dep_veh=val_fct_calcul_nb_and_t_dep_veh,\
					#li_param_fct_calcul_nb_and_t_dep_veh=lis_par_fct_calcul_nb_and_t_dep_veh,\
					#id_que=[self._id_queue_obj[0],self._id_queue_obj[1]],val_netw=val_network,val_t_round_prec=va_round_prec,ev_list=val_ev_list)
					nb_veh_to_go=self._global_fct_obj.fct_treat_case_veh_can_go(\
					t_current=self._event_time,t_unit=val_ti_unit,\
					fct_calcul_nb_and_t_dep_veh=val_fct_calcul_nb_and_t_dep_veh,\
					li_param_fct_calcul_nb_and_t_dep_veh=lis_par_fct_calcul_nb_and_t_dep_veh,\
					id_que=[i,self._id_queue_obj[0]],val_netw=val_network,val_t_round_prec=va_round_prec,ev_list=val_ev_list)
					#if i==11:
						#print("nb_veh_to_go",nb_veh_to_go)
		
			#if the (i,get_li_id_input_links_to_link) phase is  a RT
			else:
				
				if val_network.get_di_entry_internal_links()[i].get_set_veh_queue().get_di_obj_veh_queue_at_link()[\
				i,self._id_queue_obj[0]].get_queue_veh()!=[]:
				
					#the time at which the new control will be applied to the network
					#t_end_control=round(val_network.get_di_intersections()[val_netwrk.get_di_entry_internal_links()[self._id_que[0]].\
					#get_id_head_intersection_node()].get_intersection_control_obj().\
					#get_t_end_control()+val_time_unit,val_round_prec)
					t_end_control=round(val_network.get_di_intersections()[val_network.get_di_entry_internal_links()[i].\
					get_id_head_intersection_node()].get_intersection_control_obj().\
					get_t_end_control()+val_ti_unit,va_round_prec)
					
					lis_par_fct_calcul_nb_and_t_dep_veh=[self._event_time,val_ti_unit,\
					val_network.get_di_entry_internal_links()[i].get_set_veh_queue().\
					get_di_obj_veh_queue_at_link()[i,self._id_queue_obj[0]],\
					val_min_hold_time,t_end_control,val_network,va_round_prec]
				 
				
					nb_veh_to_go=self._global_fct_obj.fct_treat_case_veh_can_go(\
					t_current=self._event_time,t_unit=val_ti_unit,\
					fct_calcul_nb_and_t_dep_veh=val_fct_calcul_nb_and_t_dep_veh,\
					li_param_fct_calcul_nb_and_t_dep_veh=lis_par_fct_calcul_nb_and_t_dep_veh,\
					id_que=[i,self._id_queue_obj[0]],val_netw=val_network,val_t_round_prec=va_round_prec,ev_list=val_ev_list)	
#*****************************************************************************************************************************************************************************************
#*****************************************************************************************************************************************************************************************


#**********************************Case finite capacity arriv link-no sensor monit for t ctrl revision-without estim turn ratios*****************************************************
	#method treat the event when a vehicle joins a finite link capacity (finite capac are  being considered), the control does not require sensor monitor for being revised 
	#and the turning ratios are not going to be estimated
	def fct_treat_event_case_finite_lk_capacity_without_sensor_monit_without_estim_turn_ratios(self,va_netwrk,va_time_unit,va_fct_calcul_nb_and_t_dep_veh,\
	va_round_prec,va_ev_list,va_fct_calcul_trav_time,va_min_hold_time,va_file_recording_event_db):
		
		#the list of departed vehicles, the earlier arrivals will leave first
		li_veh_dep=va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[self._id_queue_obj[0],self._id_queue_obj[1]].get_queue_veh()[:self._nb_depart_veh]
		
		
		#we update the vehicle queue (que from which vehicle has just departed)
		va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[self._id_queue_obj[0],self._id_queue_obj[1]].fct_update_veh_queue_when_vehicles_already_in_queue_quit_queue(\
		va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[self._id_queue_obj[0],self._id_queue_obj[1]].get_queue_veh()[self._nb_depart_veh:],self._nb_depart_veh)
		
		
		#we update each departing vehicle
		for i in li_veh_dep:
			#i.fct_veh_update_when_leaving_queue_going_to_another_link(self._event_time)
			i.fct_veh_update_when_depart_completed(\
			val_t_end_departure=self._event_time,val_new_id_lk_location=self._id_queue_obj[1])
			
		
		#the number of departed veh
		nb_veh_departed=len(li_veh_dep)

		#we update the nb of vehicles in the previous vehicle link location (its origin link) 
		va_netwrk.get_di_all_links()[self._id_queue_obj[0]].set_current_nb_veh_link(\
		va_netwrk.get_di_all_links()[self._id_queue_obj[0]].get_current_nb_veh_link()-nb_veh_departed)
		
		#if the veh origin link location is not an entry link
		if va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].get_type_network_link()!=\
		Cl_Network_Link.TYPE_NETWORK_LINK["entry"]:
		
		
			
			#the number of vehicles in the link from which the  vehicle has departed (its origin link) avant la mise a jour
			nb_veh_depart_lk_before_update=va_netwrk.get_di_all_links()[self._id_queue_obj[0]].get_current_nb_veh_link()
			
			
			#if the veh origin link was saturated before the veh departure and now there exist available places on this link
			if nb_veh_depart_lk_before_update>=va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].get_capacity_link():
				
				
				#if the current number of vehicles in the link is < to the link capacity
				if va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].get_current_nb_veh_link()<\
				va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].get_capacity_link():
						
					# we examine if vehicles can move towards this link from the input links
					self.fct_treat_case_new_arrivals_towards_sat_lk_after_veh_dep(val_network=va_netwrk,\
					val_min_hold_time=va_min_hold_time,\
					val_ti_unit=va_time_unit,val_fct_calcul_nb_and_t_dep_veh=va_fct_calcul_nb_and_t_dep_veh,\
					va_round_prec=va_round_prec,val_ev_list=va_ev_list)
	
		#we update the nb of vehicles in the new vehicle location (its destination link) 
		va_netwrk.get_di_all_links()[self._id_queue_obj[1]].set_current_nb_veh_link(\
		va_netwrk.get_di_all_links()[self._id_queue_obj[1]].get_current_nb_veh_link()+nb_veh_departed)

		#if the vehicle has not arrived at an exit link
		if va_netwrk.get_di_all_links()[li_veh_dep[0].get_current_id_link_veh_location()].get_type_network_link() !=\
		Cl_Network_Link.TYPE_NETWORK_LINK["exit"]:
		
			
			#calcul travel time for the departed veh, from the beginning of the link until the end of the chosen queue
			li_parameter_fct_calculating_travel_time=[self._event_time,li_veh_dep[0].get_current_id_link_veh_location(),\
			va_netwrk,va_round_prec]
		
			t_arrival=va_fct_calcul_trav_time(*li_parameter_fct_calculating_travel_time)
			if t_arrival<0:
				print("PROBLEM CL_EV_END_VEH_DEP, fct_treat_event_case_finite_lk_capacity_without_sensor_monit_without_estim_turn_ratios, T_ARRIVAL: ", t_arrival)
				import sys
				sys.exit()
			#if the vehicle is at a  signalised intersection
			if va_netwrk.get_di_intersections()[va_netwrk.\
			get_di_entry_internal_links()[li_veh_dep[0].get_current_id_link_veh_location()].get_id_head_intersection_node()].get_type_intersection()==\
			Cl_Intersection.TYPE_INTERSECTION["signalised_intersection"]:
			
				#print("t_arrival",t_arrival,"self._event_time",self._event_time)
				#we create the event vehicle arrival 
				ev_veh_ar=Cl_Ev_veh_arrived_at_que.Ev_veh_arrived_at_que(val_event_t=t_arrival,val_li_vehicle= li_veh_dep,\
				val_id_arrival_link=va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
				[self._id_queue_obj[0],self._id_queue_obj[1]].get_id_associated_output_link())
			
				#we add the event in the event list
				ev_veh_ar.fct_insertion_even_in_event_list(event_list=va_ev_list,\
				message="IN CL_EV_VEH_END_DEPARTURE FROM QUE IN FUNCT fct_treat_event_case_finite_lk_capacity_without_sensor_monit_without_estim_turn_ratios,\
				VEH ARRIVAL AT QUE EVENT HAS TIME < TIME FIRST EVENT IN THE LIST")
			
			#if the vehicle is at a non-signalised intersection
			else:
				ev_veh_ar_nsi=Cl_Ev_veh_arrived_at_que_nsi.Ev_veh_arrived_at_que_nsi(val_event_t=t_arrival,val_li_vehicle= li_veh_dep,\
				val_id_arrival_link=va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
				[self._id_queue_obj[0],self._id_queue_obj[1]].get_id_associated_output_link())
			
				#we add the event in the event list
				ev_veh_ar_nsi.fct_insertion_even_in_event_list(event_list=va_ev_list,\
				message="IN CL_EV_VEH_END_DEPARTURE FROM QUE IN FUNCT fct_treat_event_case_finite_lk_capacity_without_sensor_monit_without_estim_turn_ratios,\
				VEH ARRIVAL AT QUE EVENT NSI HAS TIME < TIME FIRST EVENT IN THE LIST")
		#if vehicles have reached an exit link
		else:
			#for each vehicle
			for m in li_veh_dep:
				#we indicate the time at which the vehicle leaves the network
				m.fct_update_veh_when_arriving_at_exit_link(self._event_time)
				t_arrival=self._event_time
				
		#the list with the veh id remaining in the queue
		li_veh_id_left_in_queue=[]
		
		#we create the list with the veh id in que
		if va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[self._id_queue_obj[0],self._id_queue_obj[1]].get_queue_veh() !=[]:
		
			li_veh_id_left_in_queue=[i.get_id_veh() for i in va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].\
			get_set_veh_queue().get_di_obj_veh_queue_at_link()[self._id_queue_obj[0],self._id_queue_obj[1]].get_queue_veh()]
			
		#we examine if other vehicles can leave and from which phase
		nb_veh_to_go=self.fct_treat_case_exam_other_veh_can_leave_current_or_other_que(val_netw=va_netwrk,val_ti_unit=va_time_unit,\
		val_min_hold_time_duration=va_min_hold_time,val_fct_calcul_nb_and_t_dep_veh=va_fct_calcul_nb_and_t_dep_veh,\
		val_round_precis=va_round_prec,v_ev_list=va_ev_list)
					
		#we register each departing vehicle
		for i in li_veh_dep:
			
			#we do not examine departure event from exit links
			record_db_obj=Cl_Record_Database.Record_Database(val_file_db=va_file_recording_event_db,\
			val_ev_time=self._event_time,val_ev_type=self._event_type,\
			val_vehicle_id=i.get_id_veh(),\
			val_time_veh_appearance_in_network=i.get_t_veh_appearance_at_network(),\
			val_id_veh_entry_link=i.get_id_entry_link_veh_ap(),\
			val_id_current_link_veh_location=i.get_current_id_link_veh_location(),\
			val_time_veh_arrival_at_current_link=i.get_t_vehicle_arrival_at_current_link(),\
			val_time_veh_start_departure_from_current_link=i.get_t_vehicle_started_departure_from_current_link(),\
			val_time_veh_departure_from_current_link=i.get_t_vehicle_departure_from_current_link(),\
			val_veh_current_queue_location=i.get_veh_current_queue_location(),\
			val_time_veh_arrival_at_current_queue=i.get_t_vehicle_arrival_at_current_queue(),\
			val_time_veh_start_departure_from_current_queue=i.get_t_vehicle_started_departure_from_current_queue(),\
			val_time_veh_departure_from_current_queue=i.get_t_vehicle_departure_from_current_queue(),\
			val_veh_id_destination_link=i.get_veh_current_queue_location()[List_Explicit_Values.val_second_element_of_list],\
			val_time_veh_exit_from_network=i.get_t_exit_veh_from_network(),\
			val_id_event_link= self._id_queue_obj[0],\
			val_veh_can_leave_now=List_Explicit_Values.initialisation_value_to_one,\
			val_t_vehicle_arrival_at_next_link_or_queue=t_arrival,\
			val_current_achieved_queue_service_rate_including_current_vehicle=\
			va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
			[self._id_queue_obj[0],self._id_queue_obj[1]].get_current_reached_service_rate(),\
			val_current_queue_service_rate=\
			va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
			[self._id_queue_obj[0],self._id_queue_obj[1]].get_current_queue_service_rate(),\
			val_li_id_vehicles_in_queue=li_veh_id_left_in_queue,\
			val_nb_depart_veh_within_ev_end_veh_hold_at_que=nb_veh_to_go,\
			val_nb_veh_in_ar_lk=va_netwrk.get_di_all_links()[i.get_current_id_link_veh_location()].get_current_nb_veh_link(),\
			val_nb_veh_in_dep_lk=va_netwrk.get_di_all_links()[self._id_queue_obj[0]].get_current_nb_veh_link())
			
			#if va_netwrk.get_di_all_links()[self._id_queue_obj[0]].get_current_nb_veh_link()<0:
				#print("here",self._id_queue_obj[0],self._id_queue_obj[1])
				#import sys
				#sys.exit()
			#we record the event in the db 
			record_db_obj.fct_write_object_in_db_file()
		
		#initialise the departed vehicles
		for i in li_veh_dep:
			#i.fct_initialising_veh_before_its_departure()
			i.fct_initialising_veh_before_its_arrival_at_que()

#*****************************************************************************************************************************************************************************************

#**********************************Case finite capacity arriv link-with sensor monit for t ctrl revision-without estim turn ratios***************************************************
	#method treat the event when a finite link capacity is being considered, the control  requires sensor monitor for being revised and
	#the turning ratios are not going to be estimated
	def fct_treat_event_case_finite_lk_capacity_with_sensor_monit_without_estim_turn_ratios(self,va_netwrk,va_time_unit,\
	va_fct_calcul_nb_and_t_dep_veh,\
	va_round_prec,va_ev_list,va_fct_calcul_trav_time,va_min_hold_time,va_file_recording_event_db,val_min_nb_vehicles_to_detect,\
	va_t_ctrl_revision_if_decided):
		
		#the list of departed vehicles, the earlier arrivals will leave first
		li_veh_dep=va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[self._id_queue_obj[0],self._id_queue_obj[1]].get_queue_veh()[:self._nb_depart_veh]
		
		#we update the vehicle queue (que from which vehicle has just departed)
		va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[self._id_queue_obj[0],self._id_queue_obj[1]].fct_update_veh_queue_when_vehicles_already_in_queue_quit_queue(\
		va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[self._id_queue_obj[0],self._id_queue_obj[1]].get_queue_veh()[self._nb_depart_veh:],self._nb_depart_veh)
		
		
		#we update each departing vehicle
		for i in li_veh_dep:
			#i.fct_veh_update_when_leaving_queue_going_to_another_link(self._event_time)
			i.fct_veh_update_when_depart_completed(\
			val_t_end_departure=self._event_time,val_new_id_lk_location=self._id_queue_obj[1])
		
	
		#the number of departed veh
		nb_veh_departed=len(li_veh_dep)
		
		#if the queue is not a right turn
		if va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].\
		get_set_veh_queue().get_di_obj_veh_queue_at_link()[self._id_queue_obj[0],self._id_queue_obj[1]].get_type_veh_queue()!=\
		Cl_Vehicle_Queue.TYPE_VEHICLE_QUEUE["right_turn"]:
		
			#if there is at least one detector detecting the veh
			if queue_phase.fct_exam_whether_at_least_nb_veh_detected_by_a_que_sensor(val_min_nb_veh_to_detect=val_min_nb_vehicles_to_detect)!=None:
			
					#on maj le controle
					ev_end_deci_next_icm=Cl_Ev_end_decision_next_intersection_control.Ev_end_decision_next_intersection_control(\
					val_ev_time=va_t_ctrl_revision_if_decided,\
					val_id_intersection_node=va_netwrk.get_di_all_links()[self._id_queue_obj[0]].get_id_head_intersection_node(),\
					val_type_control_to_employ=\
					va_netwrk.get_di_intersections()[va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].\
					get_id_head_intersection_node()].get_ctrl_actuate_obj().get_type_employed_ctrl(),\
					val_control_category="sensor_requirement")	
		
					#on insert the event ev_end_dec_next_icm into the event list
					ev_end_deci_next_icm.fct_insertion_even_in_event_list(event_list=va_ev_list,\
					message="IN CL_Ev_veh_dep_from_que IN FUNCT, fct_treat_event_case_finite_lk_capacity\
					NEXT ev_new_end_dec_netw_control EVENT HAS TIME < TIME FIRST EVENT IN THE LIST")
				
					#we indicate the intersection that a ctrl request is made
					#va_netwrk.get_di_intersections()[va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].get_id_head_intersection_node()].\
					#set_t_last_request_ctrl_revision_when_flux_monitoring(va_t_ctrl_revision_if_decided)
		
		#if the veh origin link location is not an entry link
		if va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].get_type_network_link()!=\
		Cl_Network_Link.TYPE_NETWORK_LINK["entry"]:
			
		
			#the number of vehicles in the link from which the  vehicle has departed (its origin link) avant la mise a jour
			nb_veh_depart_lk_before_update=va_netwrk.get_di_all_links()[self._id_queue_obj[0]].get_current_nb_veh_link()
		
		
	
			#we update the nb of vehicles in the previous vehicle link location (its origin link) 
			va_netwrk.get_di_all_links()[self._id_queue_obj[0]].set_current_nb_veh_link(\
			va_netwrk.get_di_all_links()[self._id_queue_obj[0]].get_current_nb_veh_link()-nb_veh_departed)		
				
			#if the veh origin link was saturated before the veh departure and now there exist available places on this link
			if nb_veh_depart_lk_before_update>=va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].get_capacity_link():
				
				
				#if the current number of vehicles in the link is < to the link capacity
				if va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].get_current_nb_veh_link()<\
				va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].get_capacity_link():
						
					# we examine if vehicles can move towards this link from the input links
					self.fct_treat_case_new_arrivals_towards_sat_lk_after_veh_dep(val_network=va_netwrk,\
					val_min_hold_time=va_min_hold_time,\
					val_ti_unit=va_time_unit,val_fct_calcul_nb_and_t_dep_veh=va_fct_calcul_nb_and_t_dep_veh,\
					va_round_prec=va_round_prec,val_ev_list=va_ev_list)
	
		#if the vehicle has not arrived at an exit link
		if va_netwrk.get_di_all_links()[li_veh_dep[0].get_current_id_link_veh_location()].get_type_network_link() !=\
		Cl_Network_Link.TYPE_NETWORK_LINK["exit"]:
		
							
			#we update the nb of vehicles in the new vehicle location (its destination link) 
			va_netwrk.get_di_all_links()[self._id_queue_obj[1]].set_current_nb_veh_link(\
			va_netwrk.get_di_all_links()[self._id_queue_obj[1]].get_current_nb_veh_link()+nb_veh_departed)
			
			#calcul travel time for the departed veh, from the beginning of the link until the end of the chosen queue
			li_parameter_fct_calculating_travel_time=[self._event_time,li_veh_dep[0].get_current_id_link_veh_location(),\
			va_netwrk,va_round_prec]
		

		
			t_arrival=va_fct_calcul_trav_time(*li_parameter_fct_calculating_travel_time)
			if t_arrival<0:
				print("PROBLEM CL_EV_END_VEH_DEP, fct_treat_event_case_finite_lk_capacity, T_ARRIVAL: ", t_arrival)
				import sys
				sys.exit()
			#if the vehicle is at a  signalised intersection
			if va_netwrk.get_di_intersections()[va_netwrk.\
			get_di_entry_internal_links()[li_veh_dep[0].get_current_id_link_veh_location()].get_id_head_intersection_node()].get_type_intersection()==\
			Cl_Intersection.TYPE_INTERSECTION["signalised_intersection"]:
			
				#print("t_arrival",t_arrival,"self._event_time",self._event_time)
				#we create the event vehicle arrival 
				ev_veh_ar=Cl_Ev_veh_arrived_at_que.Ev_veh_arrived_at_que(val_event_t=t_arrival,val_li_vehicle= li_veh_dep,\
				val_id_arrival_link=va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
				[self._id_queue_obj[0],self._id_queue_obj[1]].get_id_associated_output_link())
			
				#we add the event in the event list
				ev_veh_ar.fct_insertion_even_in_event_list(event_list=va_ev_list,\
				message="IN CL_EV_VEH_END_DEPARTURE FROM QUE IN FUNCT fct_treat_event_case_finite_lk_capacity,\
				VEH ARRIVAL AT QUE EVENT HAS TIME < TIME FIRST EVENT IN THE LIST")
			
			#if the vehicle is at a non-signalised intersection
			else:
				ev_veh_ar_nsi=Cl_Ev_veh_arrived_at_que_nsi.Ev_veh_arrived_at_que_nsi(val_event_t=t_arrival,val_li_vehicle= li_veh_dep,\
				val_id_arrival_link=va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
				[self._id_queue_obj[0],self._id_queue_obj[1]].get_id_associated_output_link())
			
				#we add the event in the event list
				ev_veh_ar_nsi.fct_insertion_even_in_event_list(event_list=va_ev_list,\
				message="IN CL_EV_VEH_END_DEPARTURE FROM QUE IN FUNCT fct_treat_event_case_inite_lk_capacity,\
				VEH ARRIVAL AT QUE EVENT NSI HAS TIME < TIME FIRST EVENT IN THE LIST")
		#if vehicles have reached an exit link
		else:
			#for each vehicle
			for m in li_veh_dep:
				#we indicate the time at which the vehicle leaves the network
				m.fct_update_veh_when_arriving_at_exit_link(self._event_time)
				t_arrival=self._event_time
				
		#the list with the veh id remaining in the queue
		li_veh_id_left_in_queue=[]
		
		#we create the list with the veh id in que
		if va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[self._id_queue_obj[0],self._id_queue_obj[1]].get_queue_veh() !=[]:
		
			li_veh_id_left_in_queue=[i.get_id_veh() for i in va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].\
			get_set_veh_queue().get_di_obj_veh_queue_at_link()[self._id_queue_obj[0],self._id_queue_obj[1]].get_queue_veh()]
			
		#we examine if other vehicles can leave and from which phase
		nb_veh_to_go=self.fct_treat_case_exam_other_veh_can_leave_current_or_other_que(val_netw=va_netwrk,val_ti_unit=va_time_unit,\
		val_min_hold_time_duration=va_min_hold_time,val_fct_calcul_nb_and_t_dep_veh=va_fct_calcul_nb_and_t_dep_veh,\
		val_round_precis=va_round_prec,v_ev_list=va_ev_list)
					
		#we register each departing vehicle
		for i in li_veh_dep:
			
			#we do not examine departure event from exit links
			record_db_obj=Cl_Record_Database.Record_Database(val_file_db=va_file_recording_event_db,\
			val_ev_time=self._event_time,val_ev_type=self._event_type,\
			val_vehicle_id=i.get_id_veh(),\
			val_time_veh_appearance_in_network=i.get_t_veh_appearance_at_network(),\
			val_id_veh_entry_link=i.get_id_entry_link_veh_ap(),\
			val_id_current_link_veh_location=i.get_current_id_link_veh_location(),\
			val_time_veh_arrival_at_current_link=i.get_t_vehicle_arrival_at_current_link(),\
			val_time_veh_start_departure_from_current_link=i.get_t_vehicle_started_departure_from_current_link(),\
			val_time_veh_departure_from_current_link=i.get_t_vehicle_departure_from_current_link(),\
			val_veh_current_queue_location=i.get_veh_current_queue_location(),\
			val_time_veh_arrival_at_current_queue=i.get_t_vehicle_arrival_at_current_queue(),\
			val_time_veh_start_departure_from_current_queue=i.get_t_vehicle_started_departure_from_current_queue(),\
			val_time_veh_departure_from_current_queue=i.get_t_vehicle_departure_from_current_queue(),\
			val_veh_id_destination_link=i.get_veh_current_queue_location()[List_Explicit_Values.val_second_element_of_list],\
			val_time_veh_exit_from_network=i.get_t_exit_veh_from_network(),\
			val_id_event_link= self._id_queue_obj[0],\
			val_veh_can_leave_now=List_Explicit_Values.initialisation_value_to_one,\
			val_t_vehicle_arrival_at_next_link_or_queue=t_arrival,\
			val_current_achieved_queue_service_rate_including_current_vehicle=\
			va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
			[self._id_queue_obj[0],self._id_queue_obj[1]].get_current_reached_service_rate(),\
			val_current_queue_service_rate=\
			va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
			[self._id_queue_obj[0],self._id_queue_obj[1]].get_current_queue_service_rate(),\
			val_li_id_vehicles_in_queue=li_veh_id_left_in_queue,\
			val_nb_depart_veh_within_ev_end_veh_hold_at_que=nb_veh_to_go,\
			val_nb_veh_in_ar_lk=va_netwrk.get_di_all_links()[i.get_current_id_link_veh_location()].get_current_nb_veh_link(),\
			val_nb_veh_in_dep_lk=va_netwrk.get_di_all_links()[self._id_queue_obj[0]].get_current_nb_veh_link())
			
			#if va_netwrk.get_di_all_links()[self._id_queue_obj[0]].get_current_nb_veh_link()<0:
				#print("here",self._id_queue_obj[0],self._id_queue_obj[1])
				#import sys
				#sys.exit()
			#we record the event in the db 
			record_db_obj.fct_write_object_in_db_file()
		
		#initialise the departed vehicles
		for i in li_veh_dep:
			#i.fct_initialising_veh_before_its_departure()
			i.fct_initialising_veh_before_its_arrival_at_que()

		
#*******************************************************************************************************************************************************************************************

#**********************************Case finite capacity arriv link-no sensor monit for t ctrl revision-with estim turn ratios*********************************************************
	#method treat the event when a finite link capacity is being considered, the control does not requires sensor monitor for the t revision
	# and the turning ratios are going to be estimated
	def fct_treat_event_case_finite_lk_capacity_without_sensor_monit_with_estim_turn_ratios(self,va_netwrk,va_time_unit,\
	va_fct_calcul_nb_and_t_dep_veh,\
	va_round_prec,va_ev_list,va_fct_calcul_trav_time,va_min_hold_time,va_file_recording_event_db):
		
		#the list of departed vehicles, the earlier arrivals will leave first
		li_veh_dep=va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[self._id_queue_obj[0],self._id_queue_obj[1]].get_queue_veh()[:self._nb_depart_veh]
	
		#we update the vehicle queue (que from which vehicle has just departed)
		va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[self._id_queue_obj[0],self._id_queue_obj[1]].fct_update_veh_queue_when_vehicles_already_in_queue_quit_queue(\
		va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[self._id_queue_obj[0],self._id_queue_obj[1]].get_queue_veh()[self._nb_depart_veh:],self._nb_depart_veh)
		
		
		#we update each departing vehicle
		for i in li_veh_dep:
			#i.fct_veh_update_when_leaving_queue_going_to_another_link(self._event_time)
			i.fct_veh_update_when_depart_completed(\
			val_t_end_departure=self._event_time,val_new_id_lk_location=self._id_queue_obj[1])
			
		#the number of departed veh
		nb_veh_departed=len(li_veh_dep)
		
		#if the origin link id is been considered (when OD matrices, the entry links are considered but in case when final destin is dynam constructed, 
		#entry links do not belong to the diction witht he arrival link ids) 
		
		
		if self._id_queue_obj[0]  in va_netwrk.get_di_all_links()[self._id_queue_obj[1]].get_di_ar_to_link_current_period():
		
			#we update the link dict indicating the nb if vehicles joining this link (depending upon their departure link) since turn rations are  going to be estimated
			va_netwrk.get_di_all_links()[self._id_queue_obj[1]].get_di_ar_to_link_current_period()[self._id_queue_obj[0]]+=nb_veh_departed
			
			#if self._id_queue_obj[1]==709 and self._id_queue_obj[0]==23004:
				#print("dict updated in end_depar",va_netwrk.get_di_all_links()[self._id_queue_obj[1]].get_di_ar_to_link_current_period())
				#print()
		
					
		#if the veh origin link location is not an entry link
		if va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].get_type_network_link()!=\
		Cl_Network_Link.TYPE_NETWORK_LINK["entry"]:
			
			
			#the number of vehicles in the link from which the  vehicle has departed (its origin link) avant la mise a jour
			nb_veh_depart_lk_before_update=va_netwrk.get_di_all_links()[self._id_queue_obj[0]].get_current_nb_veh_link()

			
			#we update the nb of vehicles in the previous vehicle link location (its origin link) 
			va_netwrk.get_di_all_links()[self._id_queue_obj[0]].set_current_nb_veh_link(\
			va_netwrk.get_di_all_links()[self._id_queue_obj[0]].get_current_nb_veh_link()-nb_veh_departed)
			
			#if the veh origin link was saturated before the veh departure and now there exist available places on this link
			if nb_veh_depart_lk_before_update>=va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].get_capacity_link():
				
				
				#if the current number of vehicles in the link is < to the link capacity
				if va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].get_current_nb_veh_link()<\
				va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].get_capacity_link():
						
					# we examine if vehicles can move towards this link from the input links
					self.fct_treat_case_new_arrivals_towards_sat_lk_after_veh_dep(val_network=va_netwrk,\
					val_min_hold_time=va_min_hold_time,\
					val_ti_unit=va_time_unit,val_fct_calcul_nb_and_t_dep_veh=va_fct_calcul_nb_and_t_dep_veh,\
					va_round_prec=va_round_prec,val_ev_list=va_ev_list)
	
		#if the vehicle has not arrived at an exit link
		if va_netwrk.get_di_all_links()[li_veh_dep[0].get_current_id_link_veh_location()].get_type_network_link() !=\
		Cl_Network_Link.TYPE_NETWORK_LINK["exit"]:
							
			#we update the nb of vehicles in the new vehicle location (its destination link) 
			va_netwrk.get_di_all_links()[self._id_queue_obj[1]].set_current_nb_veh_link(\
			va_netwrk.get_di_all_links()[self._id_queue_obj[1]].get_current_nb_veh_link()+nb_veh_departed)
			
			#calcul travel time for the departed veh, from the beginning of the link until the end of the chosen queue
			li_parameter_fct_calculating_travel_time=[self._event_time,li_veh_dep[0].get_current_id_link_veh_location(),\
			va_netwrk,va_round_prec]
		
			t_arrival=va_fct_calcul_trav_time(*li_parameter_fct_calculating_travel_time)
			if t_arrival<0:
				print("PROBLEM CL_EV_END_VEH_DEP, fct_treat_event_case_finite_lk_capacity_without_sensor_monit_with_estim_turn_ratios, T_ARRIVAL: ", t_arrival)
				import sys
				sys.exit()
			#if the vehicle is at a  signalised intersection
			if va_netwrk.get_di_intersections()[va_netwrk.\
			get_di_entry_internal_links()[li_veh_dep[0].get_current_id_link_veh_location()].get_id_head_intersection_node()].get_type_intersection()==\
			Cl_Intersection.TYPE_INTERSECTION["signalised_intersection"]:
			
				#print("t_arrival",t_arrival,"self._event_time",self._event_time)
				#we create the event vehicle arrival 
				ev_veh_ar=Cl_Ev_veh_arrived_at_que.Ev_veh_arrived_at_que(val_event_t=t_arrival,val_li_vehicle= li_veh_dep,\
				val_id_arrival_link=va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
				[self._id_queue_obj[0],self._id_queue_obj[1]].get_id_associated_output_link())
			
				#we add the event in the event list
				ev_veh_ar.fct_insertion_even_in_event_list(event_list=va_ev_list,\
				message="IN CL_EV_VEH_END_DEPARTURE FROM QUE IN FUNCT fct_treat_event_case_finite_lk_capacity_without_sensor_monit_with_estim_turn_ratios,\
				VEH ARRIVAL AT QUE EVENT HAS TIME < TIME FIRST EVENT IN THE LIST")
			
			#if the vehicle is at a non-signalised intersection
			else:
				ev_veh_ar_nsi=Cl_Ev_veh_arrived_at_que_nsi.Ev_veh_arrived_at_que_nsi(val_event_t=t_arrival,val_li_vehicle= li_veh_dep,\
				val_id_arrival_link=va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
				[self._id_queue_obj[0],self._id_queue_obj[1]].get_id_associated_output_link())
			
				#we add the event in the event list
				ev_veh_ar_nsi.fct_insertion_even_in_event_list(event_list=va_ev_list,\
				message="IN CL_EV_VEH_END_DEPARTURE FROM QUE IN FUNCT fct_treat_event_case_finite_lk_capacity_without_sensor_monit_with_estim_turn_ratios,\
				VEH ARRIVAL AT QUE EVENT NSI HAS TIME < TIME FIRST EVENT IN THE LIST")
		#if vehicles have reached an exit link
		else:
			#for each vehicle
			for m in li_veh_dep:
				#we indicate the time at which the vehicle leaves the network
				m.fct_update_veh_when_arriving_at_exit_link(self._event_time)
				t_arrival=self._event_time
				
		#the list with the veh id remaining in the queue
		li_veh_id_left_in_queue=[]
		
		#we create the list with the veh id in que
		if va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[self._id_queue_obj[0],self._id_queue_obj[1]].get_queue_veh() !=[]:
		
			li_veh_id_left_in_queue=[i.get_id_veh() for i in va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].\
			get_set_veh_queue().get_di_obj_veh_queue_at_link()[self._id_queue_obj[0],self._id_queue_obj[1]].get_queue_veh()]
			
		#we examine if other vehicles can leave and from which phase
		nb_veh_to_go=self.fct_treat_case_exam_other_veh_can_leave_current_or_other_que(val_netw=va_netwrk,val_ti_unit=va_time_unit,\
		val_min_hold_time_duration=va_min_hold_time,val_fct_calcul_nb_and_t_dep_veh=va_fct_calcul_nb_and_t_dep_veh,\
		val_round_precis=va_round_prec,v_ev_list=va_ev_list)
					
		#we register each departing vehicle
		for i in li_veh_dep:
			
			#we do not examine departure event from exit links
			record_db_obj=Cl_Record_Database.Record_Database(val_file_db=va_file_recording_event_db,\
			val_ev_time=self._event_time,val_ev_type=self._event_type,\
			val_vehicle_id=i.get_id_veh(),\
			val_time_veh_appearance_in_network=i.get_t_veh_appearance_at_network(),\
			val_id_veh_entry_link=i.get_id_entry_link_veh_ap(),\
			val_id_current_link_veh_location=i.get_current_id_link_veh_location(),\
			val_time_veh_arrival_at_current_link=i.get_t_vehicle_arrival_at_current_link(),\
			val_time_veh_start_departure_from_current_link=i.get_t_vehicle_started_departure_from_current_link(),\
			val_time_veh_departure_from_current_link=i.get_t_vehicle_departure_from_current_link(),\
			val_veh_current_queue_location=i.get_veh_current_queue_location(),\
			val_time_veh_arrival_at_current_queue=i.get_t_vehicle_arrival_at_current_queue(),\
			val_time_veh_start_departure_from_current_queue=i.get_t_vehicle_started_departure_from_current_queue(),\
			val_time_veh_departure_from_current_queue=i.get_t_vehicle_departure_from_current_queue(),\
			val_veh_id_destination_link=i.get_veh_current_queue_location()[List_Explicit_Values.val_second_element_of_list],\
			val_time_veh_exit_from_network=i.get_t_exit_veh_from_network(),\
			val_id_event_link= self._id_queue_obj[0],\
			val_veh_can_leave_now=List_Explicit_Values.initialisation_value_to_one,\
			val_t_vehicle_arrival_at_next_link_or_queue=t_arrival,\
			val_current_achieved_queue_service_rate_including_current_vehicle=\
			va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
			[self._id_queue_obj[0],self._id_queue_obj[1]].get_current_reached_service_rate(),\
			val_current_queue_service_rate=\
			va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
			[self._id_queue_obj[0],self._id_queue_obj[1]].get_current_queue_service_rate(),\
			val_li_id_vehicles_in_queue=li_veh_id_left_in_queue,\
			val_nb_depart_veh_within_ev_end_veh_hold_at_que=nb_veh_to_go,\
			val_nb_veh_in_ar_lk=va_netwrk.get_di_all_links()[i.get_current_id_link_veh_location()].get_current_nb_veh_link(),\
			val_nb_veh_in_dep_lk=va_netwrk.get_di_all_links()[self._id_queue_obj[0]].get_current_nb_veh_link())
			
			#if va_netwrk.get_di_all_links()[self._id_queue_obj[0]].get_current_nb_veh_link()<0:
				#print("here",self._id_queue_obj[0],self._id_queue_obj[1])
				#import sys
				#sys.exit()
			#we record the event in the db 
			record_db_obj.fct_write_object_in_db_file()
		
		#initialise the departed vehicles
		for i in li_veh_dep:
			#i.fct_initialising_veh_before_its_departure()
			i.fct_initialising_veh_before_its_arrival_at_que()

		
#********************************************************************************************************************************************************************************************
#**********************************Case finite capacity arriv link-with sensor monit for t ctrl revision-with estim turn ratios*********************************************************
	#method treat the event when a finite link capacity is being considered and the turning ratios are going to be estimated
	def fct_treat_event_case_finite_lk_capacity_with_sensor_monit_with_estim_turn_ratios(self,va_netwrk,val_time_unit,\
	va_fct_calcul_nb_and_t_dep_veh,\
	va_round_prec,va_ev_list,va_fct_calcul_trav_time,va_min_hold_time,va_file_recording_event_db,val_min_nb_vehicles_to_detect,\
	va_t_ctrl_revision_if_decided):
		
		#the list of departed vehicles, the earlier arrivals will leave first
		li_veh_dep=va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[self._id_queue_obj[0],self._id_queue_obj[1]].get_queue_veh()[:self._nb_depart_veh]
		
		
		#we update the vehicle queue (que from which vehicle has just departed)
		va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[self._id_queue_obj[0],self._id_queue_obj[1]].fct_update_veh_queue_when_vehicles_already_in_queue_quit_queue(\
		va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[self._id_queue_obj[0],self._id_queue_obj[1]].get_queue_veh()[self._nb_depart_veh:],self._nb_depart_veh)
		
		
		#we update each departing vehicle
		for i in li_veh_dep:
			#i.fct_veh_update_when_leaving_queue_going_to_another_link(self._event_time)
			i.fct_veh_update_when_depart_completed(\
			val_t_end_departure=self._event_time,val_new_id_lk_location=self._id_queue_obj[1])
			
		#the number of departed veh
		nb_veh_departed=len(li_veh_dep)
		
		#if the origin link id is been considered (when OD matrices, the entry links are considered but in case when final destin is dynam constructed, 
		#entry links do not belong to the diction witht he arrival link ids) 
		if self._id_queue_obj[0]  in va_netwrk.get_di_all_links()[self._id_queue_obj[1]].get_di_ar_to_link_current_period():
		
			#we update the link dict indicating the nb if vehicles joining this link (depending upon their departure link) since turn rations are  going to be estimated
			va_netwrk.get_di_all_links()[self._id_queue_obj[1]].get_di_ar_to_link_current_period()[self._id_queue_obj[0]]+=nb_veh_departed
		
		
	
		
		#if the queue is not a right turn
		if va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].\
		get_set_veh_queue().get_di_obj_veh_queue_at_link()[self._id_queue_obj[0],self._id_queue_obj[1]].get_type_veh_queue()!=\
		Cl_Vehicle_Queue.TYPE_VEHICLE_QUEUE["right_turn"]:
			
			#if there is at least one detector of the que detecting the veh
			if queue_phase.fct_exam_whether_at_least_nb_veh_detected_by_a_que_sensor(val_min_nb_veh_to_detect=val_min_nb_vehicles_to_detect)!=None:
			
					
			
				#we revise le controle
				ev_end_deci_next_icm=Cl_Ev_end_decision_next_intersection_control.Ev_end_decision_next_intersection_control(\
				val_ev_time=va_t_ctrl_revision_if_decided,\
				val_id_intersection_node=va_netwrk.get_di_all_links()[self._id_queue_obj[0]].get_id_head_intersection_node(),\
				val_type_control_to_employ=\
				va_netwrk.get_di_intersections()[va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].\
				get_id_head_intersection_node()].get_ctrl_actuate_obj().get_type_employed_ctrl(),\
				val_control_category="sensor_requirement")	
		
				#on insert the event ev_end_dec_next_icm into the event list
				ev_end_deci_next_icm.fct_insertion_even_in_event_list(event_list=va_ev_list,\
				message="IN CL_Ev_veh_dep_from_que IN FUNCT,fct_treat_event_case_finite_lk_capacity_with_sensor_monit_with_estim_turn_ratios\
				NEXT ev_new_end_dec_netw_control EVENT HAS TIME < TIME FIRST EVENT IN THE LIST")
				
				#we indicate the intersection that a ctrl request is made
				#va_netwrk.get_di_intersections()[va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].get_id_head_intersection_node()].\
				#set_t_last_request_ctrl_revision_when_flux_monitoring(va_t_ctrl_revision_if_decided)
			
		#if the veh origin link location is not an entry link
		if va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].get_type_network_link()!=\
		Cl_Network_Link.TYPE_NETWORK_LINK["entry"]:
			
			
			#the number of vehicles in the link from which the  vehicle has departed (its origin link) avant la mise a jour
			nb_veh_depart_lk_before_update=va_netwrk.get_di_all_links()[self._id_queue_obj[0]].get_current_nb_veh_link()
		
	
			#we update the nb of vehicles in the previous vehicle link location (its origin link) 
			va_netwrk.get_di_all_links()[self._id_queue_obj[0]].set_current_nb_veh_link(\
			va_netwrk.get_di_all_links()[self._id_queue_obj[0]].get_current_nb_veh_link()-nb_veh_departed)

			
			#if the veh origin link was saturated before the veh departure and now there exist available places on this link
			if nb_veh_depart_lk_before_update>=va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].get_capacity_link():
				
				
				#if the current number of vehicles in the link is < to the link capacity
				if va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].get_current_nb_veh_link()<\
				va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].get_capacity_link():
						
					# we examine if vehicles can move towards this link from the input links
					self.fct_treat_case_new_arrivals_towards_sat_lk_after_veh_dep(val_network=va_netwrk,\
					val_min_hold_time=va_min_hold_time,\
					val_ti_unit=va_time_unit,val_fct_calcul_nb_and_t_dep_veh=va_fct_calcul_nb_and_t_dep_veh,\
					va_round_prec=va_round_prec,val_ev_list=va_ev_list)
	
		#if the vehicle has not arrived at an exit link
		if va_netwrk.get_di_all_links()[li_veh_dep[0].get_current_id_link_veh_location()].get_type_network_link() !=\
		Cl_Network_Link.TYPE_NETWORK_LINK["exit"]:
		
							
			#we update the nb of vehicles in the new vehicle location (its destination link) 
			va_netwrk.get_di_all_links()[self._id_queue_obj[1]].set_current_nb_veh_link(\
			va_netwrk.get_di_all_links()[self._id_queue_obj[1]].get_current_nb_veh_link()+nb_veh_departed)
			
			#calcul travel time for the departed veh, from the beginning of the link until the end of the chosen queue
			li_parameter_fct_calculating_travel_time=[self._event_time,li_veh_dep[0].get_current_id_link_veh_location(),\
			va_netwrk,va_round_prec]
		

		
			t_arrival=va_fct_calcul_trav_time(*li_parameter_fct_calculating_travel_time)
			if t_arrival<0:
				print("PROBLEM CL_EV_END_VEH_DEP, fct_treat_event_case_finite_lk_capacity_with_sensor_monit_with_estim_turn_ratios, T_ARRIVAL: ", t_arrival)
				import sys
				sys.exit()
			#if the vehicle is at a  signalised intersection
			if va_netwrk.get_di_intersections()[va_netwrk.\
			get_di_entry_internal_links()[li_veh_dep[0].get_current_id_link_veh_location()].get_id_head_intersection_node()].get_type_intersection()==\
			Cl_Intersection.TYPE_INTERSECTION["signalised_intersection"]:
			
				#print("t_arrival",t_arrival,"self._event_time",self._event_time)
				#we create the event vehicle arrival 
				ev_veh_ar=Cl_Ev_veh_arrived_at_que.Ev_veh_arrived_at_que(val_event_t=t_arrival,val_li_vehicle= li_veh_dep,\
				val_id_arrival_link=va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
				[self._id_queue_obj[0],self._id_queue_obj[1]].get_id_associated_output_link())
			
				#we add the event in the event list
				ev_veh_ar.fct_insertion_even_in_event_list(event_list=va_ev_list,\
				message="IN CL_EV_VEH_END_DEPARTURE FROM QUE IN FUNCT fct_treat_event_case_finite_lk_capacity_with_sensor_monit_with_estim_turn_ratios,\
				VEH ARRIVAL AT QUE EVENT HAS TIME < TIME FIRST EVENT IN THE LIST")
			
			#if the vehicle is at a non-signalised intersection
			else:
				ev_veh_ar_nsi=Cl_Ev_veh_arrived_at_que_nsi.Ev_veh_arrived_at_que_nsi(val_event_t=t_arrival,val_li_vehicle= li_veh_dep,\
				val_id_arrival_link=va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
				[self._id_queue_obj[0],self._id_queue_obj[1]].get_id_associated_output_link())
			
				#we add the event in the event list
				ev_veh_ar_nsi.fct_insertion_even_in_event_list(event_list=va_ev_list,\
				message="IN CL_EV_VEH_END_DEPARTURE FROM QUE IN FUNCT fct_treat_event_case_finite_lk_capacity_with_sensor_monit_with_estim_turn_ratios,\
				VEH ARRIVAL AT QUE EVENT NSI HAS TIME < TIME FIRST EVENT IN THE LIST")
		#if vehicles have reached an exit link
		else:
			#for each vehicle
			for m in li_veh_dep:
				#we indicate the time at which the vehicle leaves the network
				m.fct_update_veh_when_arriving_at_exit_link(self._event_time)
				t_arrival=self._event_time
				
		#the list with the veh id remaining in the queue
		li_veh_id_left_in_queue=[]
		
		#we create the list with the veh id in que
		if va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[self._id_queue_obj[0],self._id_queue_obj[1]].get_queue_veh() !=[]:
		
			li_veh_id_left_in_queue=[i.get_id_veh() for i in va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].\
			get_set_veh_queue().get_di_obj_veh_queue_at_link()[self._id_queue_obj[0],self._id_queue_obj[1]].get_queue_veh()]
			
		#we examine if other vehicles can leave and from which phase
		nb_veh_to_go=self.fct_treat_case_exam_other_veh_can_leave_current_or_other_que(val_netw=va_netwrk,val_ti_unit=va_time_unit,\
		val_min_hold_time_duration=va_min_hold_time,val_fct_calcul_nb_and_t_dep_veh=va_fct_calcul_nb_and_t_dep_veh,\
		val_round_precis=va_round_prec,v_ev_list=va_ev_list)
					
		#we register each departing vehicle
		for i in li_veh_dep:
			
			#we do not examine departure event from exit links
			record_db_obj=Cl_Record_Database.Record_Database(val_file_db=va_file_recording_event_db,\
			val_ev_time=self._event_time,val_ev_type=self._event_type,\
			val_vehicle_id=i.get_id_veh(),\
			val_time_veh_appearance_in_network=i.get_t_veh_appearance_at_network(),\
			val_id_veh_entry_link=i.get_id_entry_link_veh_ap(),\
			val_id_current_link_veh_location=i.get_current_id_link_veh_location(),\
			val_time_veh_arrival_at_current_link=i.get_t_vehicle_arrival_at_current_link(),\
			val_time_veh_start_departure_from_current_link=i.get_t_vehicle_started_departure_from_current_link(),\
			val_time_veh_departure_from_current_link=i.get_t_vehicle_departure_from_current_link(),\
			val_veh_current_queue_location=i.get_veh_current_queue_location(),\
			val_time_veh_arrival_at_current_queue=i.get_t_vehicle_arrival_at_current_queue(),\
			val_time_veh_start_departure_from_current_queue=i.get_t_vehicle_started_departure_from_current_queue(),\
			val_time_veh_departure_from_current_queue=i.get_t_vehicle_departure_from_current_queue(),\
			val_veh_id_destination_link=i.get_veh_current_queue_location()[List_Explicit_Values.val_second_element_of_list],\
			val_time_veh_exit_from_network=i.get_t_exit_veh_from_network(),\
			val_id_event_link= self._id_queue_obj[0],\
			val_veh_can_leave_now=List_Explicit_Values.initialisation_value_to_one,\
			val_t_vehicle_arrival_at_next_link_or_queue=t_arrival,\
			val_current_achieved_queue_service_rate_including_current_vehicle=\
			va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
			[self._id_queue_obj[0],self._id_queue_obj[1]].get_current_reached_service_rate(),\
			val_current_queue_service_rate=\
			va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
			[self._id_queue_obj[0],self._id_queue_obj[1]].get_current_queue_service_rate(),\
			val_li_id_vehicles_in_queue=li_veh_id_left_in_queue,\
			val_nb_depart_veh_within_ev_end_veh_hold_at_que=nb_veh_to_go,\
			val_nb_veh_in_ar_lk=va_netwrk.get_di_all_links()[i.get_current_id_link_veh_location()].get_current_nb_veh_link(),\
			val_nb_veh_in_dep_lk=va_netwrk.get_di_all_links()[self._id_queue_obj[0]].get_current_nb_veh_link())
			
			#if va_netwrk.get_di_all_links()[self._id_queue_obj[0]].get_current_nb_veh_link()<0:
				#print("here",self._id_queue_obj[0],self._id_queue_obj[1])
				#import sys
				#sys.exit()
			#we record the event in the db 
			record_db_obj.fct_write_object_in_db_file()
		
		#initialise the departed vehicles
		for i in li_veh_dep:
			#i.fct_initialising_veh_before_its_departure()
			i.fct_initialising_veh_before_its_arrival_at_que()
#*****************************************************************************************************************************************************************************************

#*****************************************************************************************************************************************************************************************
#**********************************Case infinite capacity-without sensor monit for t ctrl revision-without estim turn ratios*******************************************************
	#method treat the event when  the vehicle left a link of an infinite capacity the ctrl  does not require sensor monitor for being revised 
	#and the turn rations are not going to be estimated
	def fct_treat_event_case_infinite_lk_capacity_without_sensor_monit_without_estim_turn_ratios(self,va_netwrk,va_time_unit,\
	va_fct_calcul_nb_and_t_dep_veh,\
	va_round_prec,va_ev_list,va_fct_calcul_trav_time,va_min_hold_time,va_file_recording_event_db):
	
		#the list of departed vehicles, the earlier arrivals will leave first
		li_veh_dep=va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[self._id_queue_obj[0],self._id_queue_obj[1]].get_queue_veh()[:self._nb_depart_veh]
		

		#we update the vehicle queue
		va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[self._id_queue_obj[0],self._id_queue_obj[1]].fct_update_veh_queue_when_vehicles_already_in_queue_quit_queue(\
		va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[self._id_queue_obj[0],self._id_queue_obj[1]].get_queue_veh()[self._nb_depart_veh:],self._nb_depart_veh)
		
		#we update each departing vehicle
		for i in li_veh_dep:
			#i.fct_veh_update_when_leaving_queue_going_to_another_link(self._event_time)
			i.fct_veh_update_when_depart_completed(\
			val_t_end_departure=self._event_time,val_new_id_lk_location=self._id_queue_obj[1])
		
		#the number of departed veh
		#nb_veh_departed=len(li_veh_dep)
				
		#if the vehicle has not arrived at an exit link
		if va_netwrk.get_di_all_links()[li_veh_dep[0].get_current_id_link_veh_location()].get_type_network_link() !=\
		Cl_Network_Link.TYPE_NETWORK_LINK["exit"]:
		
			#calcul travel time for the departed veh, from the beginning of the link until the end of the chosen queue
			li_parameter_fct_calculating_travel_time=[self._event_time,li_veh_dep[0].get_current_id_link_veh_location(),\
			va_netwrk,va_round_prec]
		
			t_arrival=va_fct_calcul_trav_time(*li_parameter_fct_calculating_travel_time)
			if t_arrival<0:
				print("PROBLEM CL_EV_END_VEH_DEP, fct_treat_event_case_infinite_lk_capacity_without_sensor_monit_without_estim_turn_ratios,T_ARRIVAL: ", t_arrivaL)
				import sys
				sys.exit()
			
			#if the vehicle is at a  signalised intersection
			if va_netwrk.get_di_intersections()[va_netwrk.get_di_entry_internal_links()[li_veh_dep[0].get_current_id_link_veh_location()].\
			get_id_head_intersection_node()].get_type_intersection()==\
			Cl_Intersection.TYPE_INTERSECTION["signalised_intersection"]:
			
				#print("t_arrival",t_arrival,"self._event_time",self._event_time)
				#we create the event vehicle arrival 
				ev_veh_ar=Cl_Ev_veh_arrived_at_que.Ev_veh_arrived_at_que(val_event_t=t_arrival,val_li_vehicle= li_veh_dep,\
				val_id_arrival_link=va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
				[self._id_queue_obj[0],self._id_queue_obj[1]].get_id_associated_output_link())
			
				#we add the event in the event list
				ev_veh_ar.fct_insertion_even_in_event_list(event_list=va_ev_list,\
				message="IN CL_EV_VEH_END_DEPARTURE FROM QUE IN FUNCT fct_treat_event_case_finite_lk_capacity_without_sensor_monit_without_estim_turn_ratios,\
				VEH ARRIVAL AT QUE EVENT HAS TIME < TIME FIRST EVENT IN THE LIST")
			
			#if the vehicle is at a non-signalised intersection
			else:
				ev_veh_ar_nsi=Cl_Ev_veh_arrived_at_que_nsi.Ev_veh_arrived_at_que_nsi(val_event_t=t_arrival,val_li_vehicle= li_veh_dep,\
				val_id_arrival_link=va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
				[self._id_queue_obj[0],self._id_queue_obj[1]].get_id_associated_output_link())
			
				#we add the event in the event list
				ev_veh_ar_nsi.fct_insertion_even_in_event_list(event_list=va_ev_list,\
				message="IN CL_EV_VEH_END_DEPARTURE FROM QUE IN FUNCT fct_treat_event_case_finite_lk_capacity_without_sensor_monit_without_estim_turn_ratios,\
				VEH ARRIVAL AT QUE EVENT NSI HAS TIME < TIME FIRST EVENT IN THE LIST")
		#if vehicles have reached an exit link
		else:
			#for each vehicle
			for m in li_veh_dep:
				#we indicate the time at which the vehicle leaves the network
				m.fct_update_veh_when_arriving_at_exit_link(self._event_time)
				t_arrival=self._event_time
				
		#the list with the veh id remaining in the queue
		li_veh_id_left_in_queue=[]
		
		#we create the list with the veh id in que
		if va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[self._id_queue_obj[0],self._id_queue_obj[1]].get_queue_veh() !=[]:
		
			li_veh_id_left_in_queue=[i.get_id_veh() for i in va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].\
			get_set_veh_queue().get_di_obj_veh_queue_at_link()[self._id_queue_obj[0],self._id_queue_obj[1]].get_queue_veh()]
			
		#we examine if other vehicles can leave and from which phase
		nb_veh_to_go=self.fct_treat_case_exam_other_veh_can_leave_current_or_other_que(val_netw=va_netwrk,val_ti_unit=va_time_unit,\
		val_min_hold_time_duration=va_min_hold_time,val_fct_calcul_nb_and_t_dep_veh=va_fct_calcul_nb_and_t_dep_veh,\
		val_round_precis=va_round_prec,v_ev_list=va_ev_list)
					
		#we register each departing vehicle
		for i in li_veh_dep:
			
			#we do not examine departure event from exit links
			record_db_obj=Cl_Record_Database.Record_Database(val_file_db=va_file_recording_event_db,\
			val_ev_time=self._event_time,val_ev_type=self._event_type,\
			val_vehicle_id=i.get_id_veh(),\
			val_time_veh_appearance_in_network=i.get_t_veh_appearance_at_network(),\
			val_id_veh_entry_link=i.get_id_entry_link_veh_ap(),\
			val_id_current_link_veh_location=i.get_current_id_link_veh_location(),\
			val_time_veh_arrival_at_current_link=i.get_t_vehicle_arrival_at_current_link(),\
			val_time_veh_start_departure_from_current_link=i.get_t_vehicle_started_departure_from_current_link(),\
			val_time_veh_departure_from_current_link=i.get_t_vehicle_departure_from_current_link(),\
			val_veh_current_queue_location=i.get_veh_current_queue_location(),\
			val_time_veh_arrival_at_current_queue=i.get_t_vehicle_arrival_at_current_queue(),\
			val_time_veh_start_departure_from_current_queue=i.get_t_vehicle_started_departure_from_current_queue(),\
			val_time_veh_departure_from_current_queue=i.get_t_vehicle_departure_from_current_queue(),\
			val_veh_id_destination_link=i.get_veh_current_queue_location()[List_Explicit_Values.val_second_element_of_list],\
			val_time_veh_exit_from_network=i.get_t_exit_veh_from_network(),\
			val_id_event_link= self._id_queue_obj[0],\
			val_veh_can_leave_now=List_Explicit_Values.initialisation_value_to_one,\
			val_t_vehicle_arrival_at_next_link_or_queue=t_arrival,\
			val_current_achieved_queue_service_rate_including_current_vehicle=\
			va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
			[self._id_queue_obj[0],self._id_queue_obj[1]].get_current_reached_service_rate(),\
			val_current_queue_service_rate=\
			va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
			[self._id_queue_obj[0],self._id_queue_obj[1]].get_current_queue_service_rate(),\
			val_li_id_vehicles_in_queue=li_veh_id_left_in_queue,\
			val_nb_depart_veh_within_ev_end_veh_hold_at_que=nb_veh_to_go)
			#,\
			#val_nb_veh_in_ar_lk=va_netwrk.get_di_all_links()[i.get_current_id_link_veh_location()].get_current_nb_veh_link(),\
			#val_nb_veh_in_dep_lk=va_netwrk.get_di_all_links()[self._id_queue_obj[0]].get_current_nb_veh_link())
			
				
			#we record the event in the db 
			record_db_obj.fct_write_object_in_db_file()
		
		#initialise the departed vehicles
		for i in li_veh_dep:
			#i.fct_initialising_veh_before_its_departure()
			i.fct_initialising_veh_before_its_arrival_at_que()

		
#***************************************************************************************************************************************************************************************************

#**********************************Case infinite capacity arriv link-with sensor monit for t ctrl revision-without estim turn ratios***********************************************************
	
	#method treat the event when  the vehicle left a link of an infinite capacity the ctrl  requires sensor monitor for being revised 
	#and the turn rations are not going to be estimated
	
	def fct_treat_event_case_infinite_lk_capacity_with_sensor_monit_without_estim_turn_ratios(self,va_netwrk,va_time_unit,\
	va_fct_calcul_nb_and_t_dep_veh,\
	va_round_prec,va_ev_list,va_fct_calcul_trav_time,va_min_hold_time,va_file_recording_event_db,val_min_nb_vehicles_to_detect,\
	va_t_ctrl_revision_if_decided):
		
		#the list of departed vehicles, the earlier arrivals will leave first
		li_veh_dep=va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[self._id_queue_obj[0],self._id_queue_obj[1]].get_queue_veh()[:self._nb_depart_veh]
		
		#taille queue  depart avant maj
		que_size_before_update=len(\
		va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[self._id_queue_obj[0],self._id_queue_obj[1]].get_queue_veh())
		
		#we update the vehicle queue
		va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[self._id_queue_obj[0],self._id_queue_obj[1]].fct_update_veh_queue_when_vehicles_already_in_queue_quit_queue(\
		va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[self._id_queue_obj[0],self._id_queue_obj[1]].get_queue_veh()[self._nb_depart_veh:],self._nb_depart_veh)
		
		#we update each departing vehicle
		for i in li_veh_dep:
			#i.fct_veh_update_when_leaving_queue_going_to_another_link(self._event_time)
			i.fct_veh_update_when_depart_completed(\
			val_t_end_departure=self._event_time,val_new_id_lk_location=self._id_queue_obj[1])
			

		#if the queue is not a right turn
		if va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].\
		get_set_veh_queue().get_di_obj_veh_queue_at_link()[self._id_queue_obj[0],self._id_queue_obj[1]].get_type_veh_queue()!=\
		Cl_Vehicle_Queue.TYPE_VEHICLE_QUEUE["right_turn"]:
		
			#if there is at least one detector detecting the veh
			if queue_phase.fct_exam_whether_at_least_nb_veh_detected_by_a_que_sensor(val_min_nb_veh_to_detect=val_min_nb_vehicles_to_detect)!=None:
			
				
								
				#on maj le controle
				ev_end_deci_next_icm=Cl_Ev_end_decision_next_intersection_control.Ev_end_decision_next_intersection_control(\
				val_ev_time=va_t_ctrl_revision_if_decided,\
				val_id_intersection_node=va_netwrk.get_di_all_links()[self._id_queue_obj[0]].get_id_head_intersection_node(),\
				val_type_control_to_employ=\
				va_netwrk.get_di_intersections()[va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].\
				get_id_head_intersection_node()].get_ctrl_actuate_obj().get_type_employed_ctrl(),\
				val_control_category="sensor_requirement")	
		
				#on insert the event ev_end_dec_next_icm into the event list
				ev_end_deci_next_icm.fct_insertion_even_in_event_list(event_list=va_ev_list,\
				message="IN CL_Ev_end_veh_Dep, IN FUNCT,fct_treat_event_case_infinite_lk_capacity_with_sensor_monit_without_estim_turn_ratios\
				NEXT ev_new_end_dec_netw_control EVENT HAS TIME < TIME FIRST EVENT IN THE LIST")
				
				#we indicate the intersection that a ctrl request is made
				#va_netwrk.get_di_intersections()[va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].get_id_head_intersection_node()].\
				#set_t_last_request_ctrl_revision_when_flux_monitoring(va_t_ctrl_revision_if_decided)
					
			
		#if the vehicle has not arrived at an exit link
		if va_netwrk.get_di_all_links()[li_veh_dep[0].get_current_id_link_veh_location()].get_type_network_link() !=\
		Cl_Network_Link.TYPE_NETWORK_LINK["exit"]:
		
			#calcul travel time for the departed veh, from the beginning of the link until the end of the chosen queue
			li_parameter_fct_calculating_travel_time=[self._event_time,li_veh_dep[0].get_current_id_link_veh_location(),\
			va_netwrk,va_round_prec]
		
			t_arrival=va_fct_calcul_trav_time(*li_parameter_fct_calculating_travel_time)
			if t_arrival<0:
				print("PROBLEM CL_EV_END_VEH_DEP, fct_treat_event_case_infinite_lk_capacity_with_sensor_monit_without_estim_turn_ratios,T_ARRIVAL: ", t_arrivaL)
				import sys
				sys.exit()
			
			#if the vehicle is at a  signalised intersection
			if va_netwrk.get_di_intersections()[va_netwrk.get_di_entry_internal_links()[li_veh_dep[0].get_current_id_link_veh_location()].\
			get_id_head_intersection_node()].get_type_intersection()==\
			Cl_Intersection.TYPE_INTERSECTION["signalised_intersection"]:
			
				#print("t_arrival",t_arrival,"self._event_time",self._event_time)
				#we create the event vehicle arrival 
				ev_veh_ar=Cl_Ev_veh_arrived_at_que.Ev_veh_arrived_at_que(val_event_t=t_arrival,val_li_vehicle= li_veh_dep,\
				val_id_arrival_link=va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
				[self._id_queue_obj[0],self._id_queue_obj[1]].get_id_associated_output_link())
			
				#we add the event in the event list
				ev_veh_ar.fct_insertion_even_in_event_list(event_list=va_ev_list,\
				message="IN CL_EV_VEH_END_DEPARTURE FROM QUE IN FUNCT fct_treat_event_case_infinite_lk_capacity_with_sensor_monit_without_estim_turn_ratios,\
				VEH ARRIVAL AT QUE EVENT HAS TIME < TIME FIRST EVENT IN THE LIST")
			
			#if the vehicle is at a non-signalised intersection
			else:
				ev_veh_ar_nsi=Cl_Ev_veh_arrived_at_que_nsi.Ev_veh_arrived_at_que_nsi(val_event_t=t_arrival,val_li_vehicle= li_veh_dep,\
				val_id_arrival_link=va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
				[self._id_queue_obj[0],self._id_queue_obj[1]].get_id_associated_output_link())
			
				#we add the event in the event list
				ev_veh_ar_nsi.fct_insertion_even_in_event_list(event_list=va_ev_list,\
				message="IN CL_EV_VEH_END_DEPARTURE FROM QUE IN FUNCT fct_treat_event_case_infinite_lk_capacity_with_sensor_monit_without_estim_turn_ratios,\
				VEH ARRIVAL AT QUE EVENT NSI HAS TIME < TIME FIRST EVENT IN THE LIST")
		#if vehicles have reached an exit link
		else:
			#for each vehicle
			for m in li_veh_dep:
				#we indicate the time at which the vehicle leaves the network
				m.fct_update_veh_when_arriving_at_exit_link(self._event_time)
				t_arrival=self._event_time
				
		#the list with the veh id remaining in the queue
		li_veh_id_left_in_queue=[]
		
		#we create the list with the veh id in que
		if va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[self._id_queue_obj[0],self._id_queue_obj[1]].get_queue_veh() !=[]:
		
			li_veh_id_left_in_queue=[i.get_id_veh() for i in va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].\
			get_set_veh_queue().get_di_obj_veh_queue_at_link()[self._id_queue_obj[0],self._id_queue_obj[1]].get_queue_veh()]
			
		#we examine if other vehicles can leave and from which phase
		nb_veh_to_go=self.fct_treat_case_exam_other_veh_can_leave_current_or_other_que(val_netw=va_netwrk,val_ti_unit=va_time_unit,\
		val_min_hold_time_duration=va_min_hold_time,val_fct_calcul_nb_and_t_dep_veh=va_fct_calcul_nb_and_t_dep_veh,\
		val_round_precis=va_round_prec,v_ev_list=va_ev_list)
					
		#we register each departing vehicle
		for i in li_veh_dep:
			
			#we do not examine departure event from exit links
			record_db_obj=Cl_Record_Database.Record_Database(val_file_db=va_file_recording_event_db,\
			val_ev_time=self._event_time,val_ev_type=self._event_type,\
			val_vehicle_id=i.get_id_veh(),\
			val_time_veh_appearance_in_network=i.get_t_veh_appearance_at_network(),\
			val_id_veh_entry_link=i.get_id_entry_link_veh_ap(),\
			val_id_current_link_veh_location=i.get_current_id_link_veh_location(),\
			val_time_veh_arrival_at_current_link=i.get_t_vehicle_arrival_at_current_link(),\
			val_time_veh_start_departure_from_current_link=i.get_t_vehicle_started_departure_from_current_link(),\
			val_time_veh_departure_from_current_link=i.get_t_vehicle_departure_from_current_link(),\
			val_veh_current_queue_location=i.get_veh_current_queue_location(),\
			val_time_veh_arrival_at_current_queue=i.get_t_vehicle_arrival_at_current_queue(),\
			val_time_veh_start_departure_from_current_queue=i.get_t_vehicle_started_departure_from_current_queue(),\
			val_time_veh_departure_from_current_queue=i.get_t_vehicle_departure_from_current_queue(),\
			val_veh_id_destination_link=i.get_veh_current_queue_location()[List_Explicit_Values.val_second_element_of_list],\
			val_time_veh_exit_from_network=i.get_t_exit_veh_from_network(),\
			val_id_event_link= self._id_queue_obj[0],\
			val_veh_can_leave_now=List_Explicit_Values.initialisation_value_to_one,\
			val_t_vehicle_arrival_at_next_link_or_queue=t_arrival,\
			val_current_achieved_queue_service_rate_including_current_vehicle=\
			va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
			[self._id_queue_obj[0],self._id_queue_obj[1]].get_current_reached_service_rate(),\
			val_current_queue_service_rate=\
			va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
			[self._id_queue_obj[0],self._id_queue_obj[1]].get_current_queue_service_rate(),\
			val_li_id_vehicles_in_queue=li_veh_id_left_in_queue,\
			val_nb_depart_veh_within_ev_end_veh_hold_at_que=nb_veh_to_go)
			#,\
			#val_nb_veh_in_ar_lk=va_netwrk.get_di_all_links()[i.get_current_id_link_veh_location()].get_current_nb_veh_link(),\
			#val_nb_veh_in_dep_lk=va_netwrk.get_di_all_links()[self._id_queue_obj[0]].get_current_nb_veh_link())
			
				
			#we record the event in the db 
			record_db_obj.fct_write_object_in_db_file()
		
		#initialise the departed vehicles
		for i in li_veh_dep:
			#i.fct_initialising_veh_before_its_departure()
			i.fct_initialising_veh_before_its_arrival_at_que()

		
#***************************************************************************************************************************************************************************************************
#**********************************Case infinite capacity arriv link-without sensor monit for t ctrl revision-with estim turn ratios***********************************************************
	
	#method treat the event when  the vehicle left a link of an infinite capacity the ctrl  does not require sensor monitor for being revised 
	#and the turn rations are  going to be estimated
	
	def fct_treat_event_case_infinite_lk_capacity_without_sensor_monit_with_estim_turn_ratios(self,\
	va_netwrk,va_fct_calcul_nb_and_t_dep_veh,va_round_prec,va_ev_list,va_fct_calcul_trav_time,va_min_hold_time,va_time_unit,\
	va_file_recording_event_db):
		
		#the list of departed vehicles, the earlier arrivals will leave first
		li_veh_dep=va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[self._id_queue_obj[0],self._id_queue_obj[1]].get_queue_veh()[:self._nb_depart_veh]
		
		
		#we update the vehicle queue
		va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[self._id_queue_obj[0],self._id_queue_obj[1]].fct_update_veh_queue_when_vehicles_already_in_queue_quit_queue(\
		va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[self._id_queue_obj[0],self._id_queue_obj[1]].get_queue_veh()[self._nb_depart_veh:],self._nb_depart_veh)
		
		#we update each departing vehicle
		for i in li_veh_dep:
			#i.fct_veh_update_when_leaving_queue_going_to_another_link(self._event_time)
			i.fct_veh_update_when_depart_completed(\
			val_t_end_departure=self._event_time,val_new_id_lk_location=self._id_queue_obj[1])
			
		#the number of departed veh
		nb_veh_departed=len(li_veh_dep)
		
		#if the origin link id is been considered (when OD matrices, the entry links are considered but in case when final destin is dynam constructed, 
		#entry links do not belong to the diction witht he arrival link ids) 
		if self._id_queue_obj[0]  in va_netwrk.get_di_all_links()[self._id_queue_obj[1]].get_di_ar_to_link_current_period():
		
		
			#we update the link dict indicating the nb if vehicles joining this link (depending upon their departure link) since turn rations are  going to be estimated
			va_netwrk.get_di_all_links()[self._id_queue_obj[1]].get_di_ar_to_link_current_period()[self._id_queue_obj[0]]+=nb_veh_departed
		
		
		#if the vehicle has not arrived at an exit link
		if va_netwrk.get_di_all_links()[li_veh_dep[0].get_current_id_link_veh_location()].get_type_network_link() !=\
		Cl_Network_Link.TYPE_NETWORK_LINK["exit"]:
		
			#calcul travel time for the departed veh, from the beginning of the link until the end of the chosen queue
			li_parameter_fct_calculating_travel_time=[self._event_time,li_veh_dep[0].get_current_id_link_veh_location(),\
			va_netwrk,va_round_prec]
		
			t_arrival=va_fct_calcul_trav_time(*li_parameter_fct_calculating_travel_time)
			if t_arrival<0:
				print("PROBLEM CL_EV_END_VEH_DEP, fct_treat_event_case_infinite_lk_capacity_without_sensor_monit_with_estim_turn_ratios,T_ARRIVAL: ", t_arrivaL)
				import sys
				sys.exit()
			
			#if the vehicle is at a  signalised intersection
			if va_netwrk.get_di_intersections()[va_netwrk.get_di_entry_internal_links()[li_veh_dep[0].get_current_id_link_veh_location()].\
			get_id_head_intersection_node()].get_type_intersection()==\
			Cl_Intersection.TYPE_INTERSECTION["signalised_intersection"]:
			
				#print("t_arrival",t_arrival,"self._event_time",self._event_time)
				#we create the event vehicle arrival 
				ev_veh_ar=Cl_Ev_veh_arrived_at_que.Ev_veh_arrived_at_que(val_event_t=t_arrival,val_li_vehicle= li_veh_dep,\
				val_id_arrival_link=va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
				[self._id_queue_obj[0],self._id_queue_obj[1]].get_id_associated_output_link())
			
				#we add the event in the event list
				ev_veh_ar.fct_insertion_even_in_event_list(event_list=va_ev_list,\
				message="IN CL_EV_VEH_END_DEPARTURE FROM QUE IN FUNCT fct_treat_event_case_infinite_lk_capacity_without_sensor_monit_with_estim_turn_ratios,\
				VEH ARRIVAL AT QUE EVENT HAS TIME < TIME FIRST EVENT IN THE LIST")
			
			#if the vehicle is at a non-signalised intersection
			else:
				ev_veh_ar_nsi=Cl_Ev_veh_arrived_at_que_nsi.Ev_veh_arrived_at_que_nsi(val_event_t=t_arrival,val_li_vehicle= li_veh_dep,\
				val_id_arrival_link=va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
				[self._id_queue_obj[0],self._id_queue_obj[1]].get_id_associated_output_link())
			
				#we add the event in the event list
				ev_veh_ar_nsi.fct_insertion_even_in_event_list(event_list=va_ev_list,\
				message="IN CL_EV_VEH_END_DEPARTURE FROM QUE IN FUNCT fct_treat_event_case_infinite_lk_capacity,\
				VEH ARRIVAL AT QUE EVENT NSI HAS TIME < TIME FIRST EVENT IN THE LIST")
		#if vehicles have reached an exit link
		else:
			#for each vehicle
			for m in li_veh_dep:
				#we indicate the time at which the vehicle leaves the network
				m.fct_update_veh_when_arriving_at_exit_link(self._event_time)
				t_arrival=self._event_time
				
		#the list with the veh id remaining in the queue
		li_veh_id_left_in_queue=[]
		
		#we create the list with the veh id in que
		if va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[self._id_queue_obj[0],self._id_queue_obj[1]].get_queue_veh() !=[]:
		
			li_veh_id_left_in_queue=[i.get_id_veh() for i in va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].\
			get_set_veh_queue().get_di_obj_veh_queue_at_link()[self._id_queue_obj[0],self._id_queue_obj[1]].get_queue_veh()]
			
		#we examine if other vehicles can leave and from which phase
		nb_veh_to_go=self.fct_treat_case_exam_other_veh_can_leave_current_or_other_que(val_netw=va_netwrk,val_ti_unit=va_time_unit,\
		val_min_hold_time_duration=va_min_hold_time,val_fct_calcul_nb_and_t_dep_veh=va_fct_calcul_nb_and_t_dep_veh,\
		val_round_precis=va_round_prec,v_ev_list=va_ev_list)
					
		#we register each departing vehicle
		for i in li_veh_dep:
			
			#we do not examine departure event from exit links
			record_db_obj=Cl_Record_Database.Record_Database(val_file_db=va_file_recording_event_db,\
			val_ev_time=self._event_time,val_ev_type=self._event_type,\
			val_vehicle_id=i.get_id_veh(),\
			val_time_veh_appearance_in_network=i.get_t_veh_appearance_at_network(),\
			val_id_veh_entry_link=i.get_id_entry_link_veh_ap(),\
			val_id_current_link_veh_location=i.get_current_id_link_veh_location(),\
			val_time_veh_arrival_at_current_link=i.get_t_vehicle_arrival_at_current_link(),\
			val_time_veh_start_departure_from_current_link=i.get_t_vehicle_started_departure_from_current_link(),\
			val_time_veh_departure_from_current_link=i.get_t_vehicle_departure_from_current_link(),\
			val_veh_current_queue_location=i.get_veh_current_queue_location(),\
			val_time_veh_arrival_at_current_queue=i.get_t_vehicle_arrival_at_current_queue(),\
			val_time_veh_start_departure_from_current_queue=i.get_t_vehicle_started_departure_from_current_queue(),\
			val_time_veh_departure_from_current_queue=i.get_t_vehicle_departure_from_current_queue(),\
			val_veh_id_destination_link=i.get_veh_current_queue_location()[List_Explicit_Values.val_second_element_of_list],\
			val_time_veh_exit_from_network=i.get_t_exit_veh_from_network(),\
			val_id_event_link= self._id_queue_obj[0],\
			val_veh_can_leave_now=List_Explicit_Values.initialisation_value_to_one,\
			val_t_vehicle_arrival_at_next_link_or_queue=t_arrival,\
			val_current_achieved_queue_service_rate_including_current_vehicle=\
			va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
			[self._id_queue_obj[0],self._id_queue_obj[1]].get_current_reached_service_rate(),\
			val_current_queue_service_rate=\
			va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
			[self._id_queue_obj[0],self._id_queue_obj[1]].get_current_queue_service_rate(),\
			val_li_id_vehicles_in_queue=li_veh_id_left_in_queue,\
			val_nb_depart_veh_within_ev_end_veh_hold_at_que=nb_veh_to_go)
			#,\
			#val_nb_veh_in_ar_lk=va_netwrk.get_di_all_links()[i.get_current_id_link_veh_location()].get_current_nb_veh_link(),\
			#val_nb_veh_in_dep_lk=va_netwrk.get_di_all_links()[self._id_queue_obj[0]].get_current_nb_veh_link())
			
				
			#we record the event in the db 
			record_db_obj.fct_write_object_in_db_file()
		
		#initialise the departed vehicles
		for i in li_veh_dep:
			#i.fct_initialising_veh_before_its_departure()
			i.fct_initialising_veh_before_its_arrival_at_que()

		
#*****************************************************************************************************************************************************************************************

#*****************************************************************************************************************************************************************************************
#**********************************Case infinite capacity arriv link-with sensor monit for t ctrl revision-with estim turn ratios*****************************************************
	#method treat the event when  the vehicle left a link of an infinite capacity the ctrl   requires sensor monitor for being revised 
	#and the turn rations are  going to be estimated
	def fct_treat_event_case_infinite_lk_capacity_with_sensor_monit_with_estim_turn_ratios(self,va_netwrk,va_time_unit,\
	va_fct_calcul_nb_and_t_dep_veh,\
	va_round_prec,va_ev_list,va_fct_calcul_trav_time,va_min_hold_time,va_file_recording_event_db,val_min_nb_vehicles_to_detect,\
	va_t_ctrl_revision_if_decided):
		
		#the list of departed vehicles, the earlier arrivals will leave first
		li_veh_dep=va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[self._id_queue_obj[0],self._id_queue_obj[1]].get_queue_veh()[:self._nb_depart_veh]
		
		#we update the vehicle queue
		va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[self._id_queue_obj[0],self._id_queue_obj[1]].fct_update_veh_queue_when_vehicles_already_in_queue_quit_queue(\
		va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[self._id_queue_obj[0],self._id_queue_obj[1]].get_queue_veh()[self._nb_depart_veh:],self._nb_depart_veh)
		
		#we update each departing vehicle
		for i in li_veh_dep:
			#i.fct_veh_update_when_leaving_queue_going_to_another_link(self._event_time)
			i.fct_veh_update_when_depart_completed(\
			val_t_end_departure=self._event_time,val_new_id_lk_location=self._id_queue_obj[1])
			
		#the number of departed veh
		nb_veh_departed=len(li_veh_dep)
		
		#if the origin link id is been considered (when OD matrices, the entry links are considered but in case when final destin is dynam constructed, 
		#entry links do not belong to the diction witht he arrival link ids) 
		if self._id_queue_obj[0]  in va_netwrk.get_di_all_links()[self._id_queue_obj[1]].get_di_ar_to_link_current_period():
		
		
			#we update the link dict indicating the nb if vehicles joining this link (depending upon their departure link) since turn rations are  going to be estimated
			va_netwrk.get_di_all_links()[self._id_queue_obj[1]].get_di_ar_to_link_current_period()[self._id_queue_obj[0]]+=nb_veh_departed
		
		
		
		#if the queue is not a right turn
		if va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].\
		get_set_veh_queue().get_di_obj_veh_queue_at_link()[self._id_queue_obj[0],self._id_queue_obj[1]].get_type_veh_queue()!=\
		Cl_Vehicle_Queue.TYPE_VEHICLE_QUEUE["right_turn"]:
		
			#if there is at least one detector detecting the veh
			if queue_phase.fct_exam_whether_at_least_nb_veh_detected_by_a_que_sensor(val_min_nb_veh_to_detect=val_min_nb_vehicles_to_detect)!=None:
			
				
				
				#on maj le controle
				ev_end_deci_next_icm=Cl_Ev_end_decision_next_intersection_control.Ev_end_decision_next_intersection_control(\
				val_ev_time=va_t_ctrl_revision_if_decided,\
				val_id_intersection_node=va_netwrk.get_di_all_links()[self._id_queue_obj[0]].get_id_head_intersection_node(),\
				val_type_control_to_employ=\
				va_netwrk.get_di_intersections()[va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].\
				get_id_head_intersection_node()].get_ctrl_actuate_obj().get_type_employed_ctrl(),\
				val_control_category="sensor_requirement")	
		
				#on insert the event ev_end_dec_next_icm into the event list
				ev_end_deci_next_icm.fct_insertion_even_in_event_list(event_list=va_ev_list,\
				message="IN CL_Ev_end_veh_Dep, IN FUNCT, fct_treat_event_case_infinite_lk_capacity_with_sensor_monit_with_estim_turn_ratios\
				NEXT ev_new_end_dec_netw_control EVENT HAS TIME < TIME FIRST EVENT IN THE LIST")
				
					
					
		#if the vehicle has not arrived at an exit link
		if va_netwrk.get_di_all_links()[li_veh_dep[0].get_current_id_link_veh_location()].get_type_network_link() !=\
		Cl_Network_Link.TYPE_NETWORK_LINK["exit"]:
		
			#calcul travel time for the departed veh, from the beginning of the link until the end of the chosen queue
			li_parameter_fct_calculating_travel_time=[self._event_time,li_veh_dep[0].get_current_id_link_veh_location(),\
			va_netwrk,va_round_prec]
		
			t_arrival=va_fct_calcul_trav_time(*li_parameter_fct_calculating_travel_time)
			if t_arrival<0:
				print("PROBLEM CL_EV_END_VEH_DEP,  fct_treat_event_case_infinite_lk_capacity_with_sensor_monit_with_estim_turn_ratios,T_ARRIVAL: ", t_arrivaL)
				import sys
				sys.exit()
			
			#if the vehicle is at a  signalised intersection
			if va_netwrk.get_di_intersections()[va_netwrk.get_di_entry_internal_links()[li_veh_dep[0].get_current_id_link_veh_location()].\
			get_id_head_intersection_node()].get_type_intersection()==\
			Cl_Intersection.TYPE_INTERSECTION["signalised_intersection"]:
			
				#print("t_arrival",t_arrival,"self._event_time",self._event_time)
				#we create the event vehicle arrival 
				ev_veh_ar=Cl_Ev_veh_arrived_at_que.Ev_veh_arrived_at_que(val_event_t=t_arrival,val_li_vehicle= li_veh_dep,\
				val_id_arrival_link=va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
				[self._id_queue_obj[0],self._id_queue_obj[1]].get_id_associated_output_link())
			
				#we add the event in the event list
				ev_veh_ar.fct_insertion_even_in_event_list(event_list=va_ev_list,\
				message="IN CL_EV_VEH_END_DEPARTURE FROM QUE IN FUNCT  fct_treat_event_case_infinite_lk_capacity_with_sensor_monit_with_estim_turn_ratios,\
				VEH ARRIVAL AT QUE EVENT HAS TIME < TIME FIRST EVENT IN THE LIST")
			
			#if the vehicle is at a non-signalised intersection
			else:
				ev_veh_ar_nsi=Cl_Ev_veh_arrived_at_que_nsi.Ev_veh_arrived_at_que_nsi(val_event_t=t_arrival,val_li_vehicle= li_veh_dep,\
				val_id_arrival_link=va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
				[self._id_queue_obj[0],self._id_queue_obj[1]].get_id_associated_output_link())
			
				#we add the event in the event list
				ev_veh_ar_nsi.fct_insertion_even_in_event_list(event_list=va_ev_list,\
				message="IN CL_EV_VEH_END_DEPARTURE FROM QUE IN FUNCT  fct_treat_event_case_infinite_lk_capacity_with_sensor_monit_with_estim_turn_ratios,\
				VEH ARRIVAL AT QUE EVENT NSI HAS TIME < TIME FIRST EVENT IN THE LIST")
		#if vehicles have reached an exit link
		else:
			#for each vehicle
			for m in li_veh_dep:
				#we indicate the time at which the vehicle leaves the network
				m.fct_update_veh_when_arriving_at_exit_link(self._event_time)
				t_arrival=self._event_time
				
		#the list with the veh id remaining in the queue
		li_veh_id_left_in_queue=[]
		
		#we create the list with the veh id in que
		if va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[self._id_queue_obj[0],self._id_queue_obj[1]].get_queue_veh() !=[]:
		
			li_veh_id_left_in_queue=[i.get_id_veh() for i in va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].\
			get_set_veh_queue().get_di_obj_veh_queue_at_link()[self._id_queue_obj[0],self._id_queue_obj[1]].get_queue_veh()]
			
		#we examine if other vehicles can leave and from which phase
		nb_veh_to_go=self.fct_treat_case_exam_other_veh_can_leave_current_or_other_que(val_netw=va_netwrk,val_ti_unit=va_time_unit,\
		val_min_hold_time_duration=va_min_hold_time,val_fct_calcul_nb_and_t_dep_veh=va_fct_calcul_nb_and_t_dep_veh,\
		val_round_precis=va_round_prec,v_ev_list=va_ev_list)
					
		#we register each departing vehicle
		for i in li_veh_dep:
			
			#we do not examine departure event from exit links
			record_db_obj=Cl_Record_Database.Record_Database(val_file_db=va_file_recording_event_db,\
			val_ev_time=self._event_time,val_ev_type=self._event_type,\
			val_vehicle_id=i.get_id_veh(),\
			val_time_veh_appearance_in_network=i.get_t_veh_appearance_at_network(),\
			val_id_veh_entry_link=i.get_id_entry_link_veh_ap(),\
			val_id_current_link_veh_location=i.get_current_id_link_veh_location(),\
			val_time_veh_arrival_at_current_link=i.get_t_vehicle_arrival_at_current_link(),\
			val_time_veh_start_departure_from_current_link=i.get_t_vehicle_started_departure_from_current_link(),\
			val_time_veh_departure_from_current_link=i.get_t_vehicle_departure_from_current_link(),\
			val_veh_current_queue_location=i.get_veh_current_queue_location(),\
			val_time_veh_arrival_at_current_queue=i.get_t_vehicle_arrival_at_current_queue(),\
			val_time_veh_start_departure_from_current_queue=i.get_t_vehicle_started_departure_from_current_queue(),\
			val_time_veh_departure_from_current_queue=i.get_t_vehicle_departure_from_current_queue(),\
			val_veh_id_destination_link=i.get_veh_current_queue_location()[List_Explicit_Values.val_second_element_of_list],\
			val_time_veh_exit_from_network=i.get_t_exit_veh_from_network(),\
			val_id_event_link= self._id_queue_obj[0],\
			val_veh_can_leave_now=List_Explicit_Values.initialisation_value_to_one,\
			val_t_vehicle_arrival_at_next_link_or_queue=t_arrival,\
			val_current_achieved_queue_service_rate_including_current_vehicle=\
			va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
			[self._id_queue_obj[0],self._id_queue_obj[1]].get_current_reached_service_rate(),\
			val_current_queue_service_rate=\
			va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
			[self._id_queue_obj[0],self._id_queue_obj[1]].get_current_queue_service_rate(),\
			val_li_id_vehicles_in_queue=li_veh_id_left_in_queue,\
			val_nb_depart_veh_within_ev_end_veh_hold_at_que=nb_veh_to_go)
			#,\
			#val_nb_veh_in_ar_lk=va_netwrk.get_di_all_links()[i.get_current_id_link_veh_location()].get_current_nb_veh_link(),\
			#val_nb_veh_in_dep_lk=va_netwrk.get_di_all_links()[self._id_queue_obj[0]].get_current_nb_veh_link())
			
				
			#we record the event in the db 
			record_db_obj.fct_write_object_in_db_file()
		
		#initialise the departed vehicles
		for i in li_veh_dep:
			#i.fct_initialising_veh_before_its_departure()
			i.fct_initialising_veh_before_its_arrival_at_que()

		
#*****************************************************************************************************************************************************************************************
#*****************************************************************************************************************************************************************************************
#******************************************************CASE FINITE CAPACITY******************************************************************************************************
	#method treating the case of a finite (internal) link capacity
	def fct_treat_event_case_finite_lk_capacity(self,val_netwk,val_time_unit,val_fct_calcul_nb_and_t_dep_veh,val_min_nb_veh_to_detect,\
	val_round_prec,val_ev_list,val_fct_calcul_trav_time,val_min_hold_time,val_file_recording_event_db):
		#,\
		#val_t_duration_obtain_decis_ctrl_upd):
	
	
		#if the control revision  requires sensor monitoring for its t revision
		if val_netwk.get_di_intersections()[val_netwk.get_di_entry_internal_links()\
		[self._id_queue_obj[0]].get_id_head_intersection_node()].get_intersection_control_obj().get_type_control_related_to_t_revision()==\
		Cl_Control_Actuate.TYPE_CONTROL_T_REVISION_CATEGORY["sensor_requirement_for_t_update"]:
		
			val_t_ctrl_revision_if_decided=round(self._event_time+val_t_duration_obtain_decis_ctrl_upd,val_round_prec)
		
			#the time at which the cotnrol will be revised if a revision will be decided by the control
			#val_ti_ctrl_revision_if_decided=self._obj_decisions.fct_calculate_t_ctrl_revision(t_cur=self._event_time,dur=\
			#val_netwk.get_di_intersections()[val_network.get_di_entry_internal_links()\
			#[self._id_queue_obj[0]].get_id_head_intersection_node()].get_intersection_control_obj().\
			#get_t_duration_for_defining_t_ctrl_revision_when_at_given_time_sensor_records_veh_variation())
	
			#if  turn ratios will be estimated with the current control
			if val_netwk.get_di_intersections()[val_netwk.get_di_entry_internal_links()\
			[self._id_queue_obj[0]].get_id_head_intersection_node()].get_intersection_control_obj().get_estim_turn_ratios_with_current_ctrl()==List_Explicit_Values.initialisation_value_to_one:
			
				self.fct_treat_event_case_finite_lk_capacity_with_sensor_monit_with_estim_turn_ratios(\
				va_netwrk=val_netwk,va_time_unit=val_time_unit,\
				va_fct_calcul_nb_and_t_dep_veh=val_fct_calcul_nb_and_t_dep_veh,\
				va_round_prec=val_round_prec,va_ev_list=val_ev_list,va_fct_calcul_trav_time=val_fct_calcul_trav_time,\
				va_min_hold_time=val_min_hold_time,va_file_recording_event_db=val_file_recording_event_db,
				val_min_nb_vehicles_to_detect=val_min_nb_veh_to_detect,va_t_ctrl_revision_if_decided=val_t_ctrl_revision_if_decided)
			
			
			#if fixed values wil be employed for the turn ratios
			elif val_netwk.get_di_intersections()[val_netwk.get_di_entry_internal_links()\
			[self._id_queue_obj[0]].get_id_head_intersection_node()].get_intersection_control_obj().get_estim_turn_ratios_with_current_ctrl()==List_Explicit_Values.initialisation_value_to_zero:
			
				self.fct_treat_event_case_finite_lk_capacity_with_sensor_monit_without_estim_turn_ratios(\
				va_netwrk=val_netwk,va_time_unit=val_time_unit,va_fct_calcul_nb_and_t_dep_veh=val_fct_calcul_trav_time,\
				va_round_prec=val_round_prec,va_ev_list=val_ev_list,va_fct_calcul_trav_time=val_fct_calcul_nb_and_t_dep_veh,\
				va_min_hold_time=val_min_hold_time,va_file_recording_event_db=val_file_recording_event_db,\
				val_min_nb_vehicles_to_detect=val_min_nb_veh_to_detect,va_t_ctrl_revision_if_decided=val_t_ctrl_revision_if_decided)
			
			#if none of the previous values for the turn ratios
			else:
				print("PROBLEM IN CL_EV_VEH_DEP, FCT fct_treat_event_case_finite_lk_capacity, VALUE FOR ESTIM TURN RATIOS:",\
				val_netwk.get_di_intersections()[val_netwk.get_di_entry_internal_links()\
				[self._id_queue_obj[0]].get_id_head_intersection_node()].get_intersection_control_obj().get_estim_turn_ratios_with_current_ctrl())
				import sys
				sys.exit()
		
			
		#if the control  does not require sensor monitoring for its t revision
		if val_netwk.get_di_intersections()[val_netwk.get_di_entry_internal_links()\
		[self._id_queue_obj[0]].get_id_head_intersection_node()].get_intersection_control_obj().get_type_control_related_to_t_revision()==\
		Cl_Control_Actuate.TYPE_CONTROL_T_REVISION_CATEGORY["without_sensor_requirement_for_t_update"]:
		
			
			#if estimated turn ratios
			if val_netwk.get_di_intersections()[val_netwk.get_di_entry_internal_links()\
			[self._id_queue_obj[0]].get_id_head_intersection_node()].get_intersection_control_obj().get_estim_turn_ratios_with_current_ctrl()==List_Explicit_Values.initialisation_value_to_one:
			
				self.fct_treat_event_case_finite_lk_capacity_without_sensor_monit_with_estim_turn_ratios(\
				va_netwrk=val_netwk,va_time_unit=val_time_unit,va_fct_calcul_nb_and_t_dep_veh=val_fct_calcul_nb_and_t_dep_veh,\
				va_round_prec=val_round_prec,va_ev_list=val_ev_list,va_fct_calcul_trav_time=val_fct_calcul_trav_time,\
				va_min_hold_time=val_min_hold_time,va_file_recording_event_db=val_file_recording_event_db)
			
			
			#if turn ratios will not be estimated
			else: 
			
				self.fct_treat_event_case_finite_lk_capacity_without_sensor_monit_without_estim_turn_ratios(\
				va_netwrk=val_netwk,va_time_unit=val_time_unit,va_fct_calcul_nb_and_t_dep_veh=val_fct_calcul_nb_and_t_dep_veh,\
				va_round_prec=val_round_prec,va_ev_list=val_ev_list,va_fct_calcul_trav_time=val_fct_calcul_trav_time,\
				va_min_hold_time=val_min_hold_time,va_file_recording_event_db=val_file_recording_event_db)
			
				
				
		#if the control type related to the t revision is not of the previous cases
		else:
			print("PROBLEM IN CL_EV_VEH_END_DEP, FCT ct_treat_event_case_finite_lk_capacity,\
			CTRL TYPE RELATED TO T REVISION:",\
			val_netwk.get_di_intersections()[val_netwk.get_di_entry_internal_links()\
			[self._id_queue_obj[0]].get_id_head_intersection_node()].get_intersection_control_obj().get_type_control_related_to_t_revision())
			import sys
			sys.exit()

#*****************************************************************************************************************************************************************************************
#******************************************************CASE INFINITE CAPACITY******************************************************************************************************
	#method treating the case of a infinite (internal) link capacity
	def fct_treat_event_case_infinite_lk_capacity(self,val_netwk,val_time_unit,val_fct_calcul_nb_and_t_dep_veh,\
	val_round_prec,val_ev_list,val_fct_calcul_trav_time,va_min_hold_time,val_file_recording_event_db,\
	val_min_nb_veh_to_detect,val_ti_unit):
	
		#if the control revision  requires sensor monitoring for its t revision
		if val_netwk.get_di_intersections()[val_netwk.get_di_entry_internal_links()\
		[self._id_queue_obj[0]].get_id_head_intersection_node()].get_intersection_control_obj().get_type_control_related_to_t_revision()==\
		Cl_Control_Actuate.TYPE_CONTROL_T_REVISION_CATEGORY["sensor_requirement_for_t_update"]:
		
			val_t_ctrl_revision_if_decided=round(self._event_time+val_t_duration_obtain_decis_ctrl_upd,val_round_prec)

			#if  turn ratios wil be estimated
			if val_netwk.get_di_intersections()[val_netwk.get_di_entry_internal_links()\
			[self._id_queue_obj[0]].get_id_head_intersection_node()].get_intersection_control_obj().get_estim_turn_ratios_with_current_ctrl()==List_Explicit_Values.initialisation_value_to_one:
			
				self.fct_treat_event_case_infinite_lk_capacity_with_sensor_monit_with_estim_turn_ratios(\
				va_netwrk=val_netwk,va_time_unit=val_time_unit,va_fct_calcul_nb_and_t_dep_veh=val_fct_calcul_nb_and_t_dep_veh,\
				va_round_prec=val_round_prec,va_ev_list=val_ev_list,va_fct_calcul_trav_time=val_fct_calcul_trav_time,\
				va_min_hold_time=va_min_hold_time,va_file_recording_event_db=val_file_recording_event_db,\
				val_min_nb_vehicles_to_detect=val_min_nb_veh_to_detect,\
				va_t_ctrl_revision_if_decided=val_t_ctrl_revision_if_decided)
			
			#if  turn ratios wil not be estimated
			elif val_netwk.get_di_intersections()[val_netwk.get_di_entry_internal_links()\
			[self._id_queue_obj[0]].get_id_head_intersection_node()].get_intersection_control_obj().get_estim_turn_ratios_with_current_ctrl()==List_Explicit_Values.initialisation_value_to_zero:

				self.fct_treat_event_case_infinite_lk_capacity_with_sensor_monit_without_estim_turn_ratios(\
				va_netwrk=val_netwk,va_time_unit=val_time_unit,va_fct_calcul_nb_and_t_dep_veh=val_fct_calcul_nb_and_t_dep_veh,\
				va_round_prec=val_round_prec,va_ev_list=val_ev_list,va_fct_calcul_trav_time=val_fct_calcul_trav_time,\
				va_min_hold_time=va_min_hold_time,va_file_recording_event_db=val_file_recording_event_db,\
				val_min_nb_vehicles_to_detect=val_min_nb_veh_to_detect,\
				va_t_ctrl_revision_if_decided=val_t_ctrl_revision_if_decided)
				
			#if none of the previous values for the turn ratios
			else:
				print("PROBLEM IN CL_EV_VEH_DEP, FCT fct_treat_event_case_infinite_lk_capacity, VALUE FOR ESTIM TURN RATIOS:",\
				val_netwk.get_di_intersections()[val_netwk.get_di_entry_internal_links()\
				[self._id_queue_obj[0]].get_id_head_intersection_node()].get_intersection_control_obj().get_estim_turn_ratios_with_current_ctrl())
				import sys
				sys.exit()
	
		
		#if the control  does not require sensor monitoring for its t revision
		elif val_netwk.get_di_intersections()[val_netwk.get_di_entry_internal_links()\
		[self._id_queue_obj[0]].get_id_head_intersection_node()].get_intersection_control_obj().get_type_control_related_to_t_revision()==\
		Cl_Control_Actuate.TYPE_CONTROL_T_REVISION_CATEGORY["without_sensor_requirement_for_t_update"]:
		
			#if  turn ratios wil be estimated
			if val_netwk.get_di_intersections()[val_netwk.get_di_entry_internal_links()\
			[self._id_queue_obj[0]].get_id_head_intersection_node()].get_intersection_control_obj().get_estim_turn_ratios_with_current_ctrl()==List_Explicit_Values.initialisation_value_to_one:
			
				self.fct_treat_event_case_infinite_lk_capacity_without_sensor_monit_with_estim_turn_ratios(\
				va_netwrk=val_netwk,va_fct_calcul_nb_and_t_dep_veh=val_fct_calcul_nb_and_t_dep_veh,\
				va_round_prec=val_round_prec,va_ev_list=val_ev_list,va_fct_calcul_trav_time=val_fct_calcul_trav_time,\
				va_min_hold_time=va_min_hold_time,\
				va_time_unit=val_ti_unit,\
				va_file_recording_event_db=val_file_recording_event_db)
			
			#if  turn ratios wil not be estimated
			elif val_netwk.get_di_intersections()[val_netwk.get_di_entry_internal_links()\
			[self._id_queue_obj[0]].get_id_head_intersection_node()].get_intersection_control_obj().get_estim_turn_ratios_with_current_ctrl()==List_Explicit_Values.initialisation_value_to_zero:
			
				self.fct_treat_event_case_infinite_lk_capacity_without_sensor_monit_without_estim_turn_ratios(\
				va_netwrk=val_netwk,va_time_unit=val_time_unit,\
				va_fct_calcul_nb_and_t_dep_veh=val_fct_calcul_nb_and_t_dep_veh,\
				va_round_prec=val_round_prec,va_ev_list=val_ev_list,\
				va_fct_calcul_trav_time=val_fct_calcul_trav_time,va_min_hold_time=va_min_hold_time,va_file_recording_event_db=val_file_recording_event_db)
				
			#if none of the previous values for the turn ratios
			else:
				print("PROBLEM IN CL_EV_VEH_DEP, FCT fct_treat_event_case_infinite_lk_capacity without_sensor_requirement_for_t_update, VALUE FOR ESTIM TURN RATIOS:",\
				val_netwk.get_di_intersections()[val_netwk.get_di_entry_internal_links()\
				[self._id_queue_obj[0]].get_id_head_intersection_node()].get_intersection_control_obj().get_estim_turn_ratios_with_current_ctrl())
				import sys
				sys.exit()
				
		#if the control type related to the t revision is not of the previous cases
		else:
			print("PROBLEM IN CL_EV_VEH_END_DEP, FCT fct_treat_event_case_infinite_lk_capacity,\
			CTRL TYPE RELATED TO T REVISION:",\
			val_netwk.get_di_intersections()[val_netwk.get_di_entry_internal_links()\
			[self._id_queue_obj[0]].get_id_head_intersection_node()].get_intersection_control_obj().get_type_control_related_to_t_revision())
			import sys
			sys.exit()

#*****************************************************************************************************************************************************************************************
#*****************************************************************************************************************************************************************************************
	#method treating the event
	def event_treat_1(self,val_network=None,val_t_unit=-1,val_fct_calcul_travel_time=None,val_min_veh_hold_time=None,\
	val_fct_calcul_nb_and_t_dep_vehicles=None,val_round_precis=-1,val_ev_list=[],val_file_recording_ev_db=None,val_capacite_intern_link=None,\
	val_min_nb_vehicles_to_detect=None):
	
		#if finite link capacities are being considered
		if val_capacite_intern_link==List_Explicit_Values.initialisation_value_to_one:
		
			self.fct_treat_event_case_finite_lk_capacity(\
			val_netwk=val_network,val_time_unit=val_t_unit,val_fct_calcul_nb_and_t_dep_veh=val_fct_calcul_nb_and_t_dep_vehicles,\
			val_min_nb_veh_to_detect=val_min_nb_vehicles_to_detect,\
			val_round_prec=val_round_precis,val_ev_list=val_ev_list,val_fct_calcul_trav_time=val_fct_calcul_travel_time,\
			val_min_hold_time=val_min_veh_hold_time,val_file_recording_event_db=val_file_recording_ev_db)
		
		#if infinite link capacities are considered
		elif val_capacite_intern_lk==List_Explicit_Values.initialisation_value_to_zero:
		
			self.fct_treat_event_case_infinite_lk_capacity(\
			val_netwk=val_network,val_time_unit=val_t_unit,\
			val_fct_calcul_nb_and_t_dep_veh=val_fct_calcul_nb_and_t_dep_vehicles,val_min_nb_veh_to_detect=val_min_nb_vehicles_to_detect,\
			val_round_prec=val_round_precis,val_ev_list=val_ev_list,val_fct_calcul_trav_time=val_fct_calcul_travel_time,\
			va_min_hold_time=val_min_veh_hold_time,val_file_recording_event_db=val_file_recording_ev_db,val_ti_unit=val_t_unit)
		
		else:
			print("PROBLEM IN CL_EV_END_VEH_DEPART FROM QUE, FCT event_treat, CAPACITY INTERNAL LINKS: ",val_capacite_intern_lk)
			import sys
			sys.exit()


#*****************************************************************************************************************************************************************************************

	#method treating the event
	def event_treat(self,val_key_fct_in_dict_to_treat,li_param_fct_treat_event):
	
		#dictionary with the functions treat each case of this event
		di_fct_ev_dep_treat={1:self.fct_treat_event_case_finite_lk_capacity,2:self.fct_treat_event_case_infinite_lk_capacity}
		
		return di_fct_ev_dep_treat[val_key_fct_in_dict_to_treat](*li_param_fct_treat_event)
		























