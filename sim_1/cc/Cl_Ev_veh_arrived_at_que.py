import string
import Cl_Event
import List_Explicit_Values
import Cl_Global_Functions
import Cl_Ev_end_veh_hold_at_que
import Cl_Decisions
import Cl_Vehicle
import Cl_Record_Database
import Cl_Control_Actuate
import Cl_Vehicle_Queue
import Cl_Ev_end_decision_next_intersection_control



class Ev_veh_arrived_at_que(Cl_Event.Event):

	""" class defining the event of vehicle arrival at a queue of a link (when considering that a link had many queues) or at a new link"""
	
	def __init__(self,val_event_t=-1,val_li_vehicle=None,val_id_arrival_link=-1):
	
		gl_funct_obj=Cl_Global_Functions.Global_Functions()
		
		Cl_Event.Event.__init__(self,val_event_time=val_event_t,val_event_type=Cl_Event.TYPE_EV["type_ev_veh_arrived_at_que"],\
		val_global_fct_obj=gl_funct_obj)
		
		
		#the list of vehicles arriving at the link
		self._li_vehicle=val_li_vehicle
		
		#the id of the link
		self._id_arrival_link=val_id_arrival_link
		
		
		#the decision object  associated with this event
		obj_decisions=Cl_Decisions.Decisions()
		
		self._obj_decisions=obj_decisions
		
		#dictionary with the functions treat each case of this event
		#self._di_fct_ev_veh_ar_treat={1:self.fct_treat_case_veh_ar_at_que_when_new_demand_final_dest_and_path_dynam_defined,\
		#2:self.fct_treat_case_veh_ar_at_que_when_new_demand_final_dest_and_path_given,\
		#3:self.fct_treat_case_veh_ar_at_que_when_new_demand_given_final_dest_and_dyn_computed_path,\
		#4:self.fct_treat_case_veh_ar_at_que_when_previous_demand_final_dest_and_dyn_computed,\
		#5:self.fct_treat_case_veh_ar_at_que_when_previous_demand_given_final_dest_and_path,\
		#6:self.fct_treat_case_veh_ar_at_que_when_previous_demand_given_final_dest_and_path_dyn_computed_ctr_eval,\
		#7:self.fct_treat_case_veh_ar_at_que_when_previous_demand_given_final_dest_and_path_dyn_computed_rout_algo_eval}	
		
		
#*****************************************************************************************************************************************************************************************
	#method returning the list of vehicles vehicle of the event
	def get_li_vehicle(self):
		return self._li_vehicle

#*****************************************************************************************************************************************************************************************
	#method returning the id of the associated entry link
	def get_id_link(self):
		return self._id_arrival_link
#*****************************************************************************************************************************************************************************************
	#method returning the decision object  associated with this event
	def get_obj_decisions(self):
		return self._obj_decisions

#*****************************************************************************************************************************************************************************************
	#method returning the dictionary indicating the functions for treat each case
	#def get_di_fct_ev_veh_ar_treat(self):
		#return self._di_fct_ev_veh_ar_treat

#*****************************************************************************************************************************************************************************************

	#method modifying the vehicle  list of the event
	def set_li_vehicle(self,n_v):
		self._li_vehicle=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the id of the associated entry link
	def set_id_link(self,n_v):
		self._id_arrival_link=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the decision object  associated with this event
	def set_obj_decisions(self,n_v):
		self._obj_decisions=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the dictionary indicating the functions for treat each case
	#def set_di_fct_ev_veh_ar_treat(self,n_v):
		#self._di_fct_ev_veh_ar_treat=n_v

#*****************************************************************************************************************************************************************************************
	#method examining if there is at least one que actualised by the ctrl for which the flux < f_min
	#di_id_que=dict, key=[id input lk, id output link], value is 1
	def fct_exam_existence_que_actualised_by_ctrl_with_flux_inferior_to_f_min_permit_1(self,\
	di_id_que,val_netw,val_min_allowed_flow_depart_link):
	
		#if self._id_arrival_link==3 or self._id_arrival_link==1:
			#print("dict:",di_id_que) 
		reponse=0
		#si le ctrl actualise la queue ou le vehicule arrive et le flux de cette que est <min val permise
		for i in di_id_que:
			if val_netw.get_di_intersections()[val_netw.get_di_entry_internal_links()[self._id_arrival_link].\
				get_id_head_intersection_node()].get_intersection_control_obj().get_di_intersection_control_mat()\
				[i[0],i[1]]==1 and \
			len(\
			val_netw.get_di_entry_internal_links()[self._id_arrival_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
			[i[0],i[1]].get_queue_veh()) <val_min_allowed_flow_depart_link:
				return 1
		
		if reponse==0:
			return reponse
#*****************************************************************************************************************************************************************************************
	#method examining whether the ctrl decision should be updated in the intersection by the veh arrival
	#di_id_que=dict, key=[id input lk, id output link], value is 1
	#it returns 1 if the ctrl decision should be updated cas when one of the selected ques is actuated and has flow <f_min or
	#if all  the queues of the actuated stage have flow <f_min, 0 otherwise
	
	def fct_exam_whether_ctrl_dec_should_be_updated_1(self,di_id_que,val_netw,val_min_allowed_flow_depart_link):
	
		#if self._id_arrival_link==3 or self._id_arrival_link==1:
			#print("dict:",di_id_que) 
			
		reponse=0
		#si le ctrl actualise la queue ou le vehicule arrive et le flux de cette que est <min val permise
		for i in di_id_que:
			if val_netw.get_di_intersections()[val_netw.get_di_entry_internal_links()[self._id_arrival_link].\
				get_id_head_intersection_node()].get_intersection_control_obj().get_di_intersection_control_mat()\
				[i[0],i[1]]==1 and len(\
				val_netw.get_di_entry_internal_links()[self._id_arrival_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
				[i[0],i[1]].get_queue_veh()) <val_min_allowed_flow_depart_link:
				
					return 1
					
		
		#si on n'est pas en rc
		if val_netw.get_di_intersections()[val_netw.get_di_entry_internal_links()[self._id_arrival_link].\
		get_id_head_intersection_node()].get_intersection_control_obj().get_id_actuated_stage() !=0:
			
			#for each input link of the actuated phases, we examine if their queues have flows > f_min
			#for j in val_netw.get_di_intersections()[val_netw.get_di_entry_internal_links()[self._id_arrival_link].\
			#get_id_head_intersection_node()].get_di_stages_sign_intersection()[\
			#val_netw.get_di_intersections()[val_netw.get_di_entry_internal_links()[self._id_arrival_link].\
			#get_id_head_intersection_node()].get_intersection_control_obj().get_id_actuated_stage()]:
			
				#if there is at least one queue having flow>f_min, the ctrl is not updated
				#if val_netw.get_di_all_links()[j[0]].fct_examing_existence_que_actuates_stage_with_flow_sup_given_value(\
				#val_network=val_netw,val_fmin=val_min_allowed_flow_depart_link)==1:
				#	return 0
			if val_netw.get_di_intersections()[val_netw.get_di_entry_internal_links()[self._id_arrival_link].get_id_head_intersection_node()].\
			fct_examing_existence_que_actuates_stage_with_flow_sup_given_value(val_network=val_netw,val_fmin=val_min_allowed_flow_depart_link)==1:
				return 0
			#si on n'a pas trouve que with flow > f_min, we update the ctrl
			return 1
		
		if reponse==0:
			return reponse
#*****************************************************************************************************************************************************************************************
	#method examining whether the ctrl decision should be updated in the intersection by the veh arrival
	#di_id_que=dict, key=[id input lk, id output link], value is 1
	#it returns 1 if the ctrl decision should be, 0 otherwise
	
	def fct_exam_whether_ctrl_dec_should_be_updated_2(self,val_netw,val_min_allowed_flow_depart_link):
	
		#if self._id_arrival_link==3 or self._id_arrival_link==1:
			#print("dict:",di_id_que) 
			
			
		#reponse=0
	
		#if we are in red clearance and we have not planned to update the decision we update the decision
		if val_netw.get_di_intersections()[val_netw.get_di_entry_internal_links()[self._id_arrival_link].\
		get_id_head_intersection_node()].get_intersection_control_obj().get_type_control()==Cl_Control_Actuate.TYPE_CONTROL[0]:
		
			if  val_netw.get_di_intersections()[val_netw.get_di_entry_internal_links()[self._id_arrival_link].\
			get_id_head_intersection_node()].get_indicating_t_last_request_ctrl_update()==None:
			
				return 1
			elif val_netw.get_di_intersections()[val_netw.get_di_entry_internal_links()[self._id_arrival_link].\
			get_id_head_intersection_node()].get_indicating_t_last_request_ctrl_update()<self._event_time:
				return 1
			else:
				return 0
		
		#if we are not in red clearance
		else:
			#if there is at least one que of the actuates stage having flow > f_min then the decision will not be updated
			#for j in val_netw.get_di_intersections()[val_netw.get_di_entry_internal_links()[self._id_arrival_link].\
			#get_id_head_intersection_node()].get_di_stages_sign_intersection()[\
			#val_netw.get_di_intersections()[val_netw.get_di_entry_internal_links()[self._id_arrival_link].\
			#get_id_head_intersection_node()].get_intersection_control_obj().get_id_actuated_stage()]:
		
				#if there is at least one queue having flow>f_min, the ctrl is not updated
				#if val_netw.get_di_all_links()[j[0]].fct_examing_existence_que_actuates_stage_with_flow_sup_given_value(\
				#val_network=val_netw,val_fmin=val_min_allowed_flow_depart_link)==1:
					#return 0
			if val_netw.get_di_intersections()[val_netw.get_di_entry_internal_links()[self._id_arrival_link].get_id_head_intersection_node()].\
			fct_examing_existence_que_actuates_stage_with_flow_sup_given_value(val_network=val_netw,val_fmin=val_min_allowed_flow_depart_link)==1:
				return 0		
			if  val_netw.get_di_intersections()[val_netw.get_di_entry_internal_links()[self._id_arrival_link].\
			get_id_head_intersection_node()].get_indicating_t_last_request_ctrl_update()!=self._event_time:
			
				return 1
			else:
				return 0
				
			#return 1
	
				
		#if reponse==0:
			#return reponse
#*****************************************************************************************************************************************************************************************


#********************************************************Cas New Demand-no OD-without sensor monit **********************************************************
	#method treating the case when a vehicle arrives at a que, a new generated demand is been generated, final destination and path are dyn defined, 
	#the employed control does not require  sensor monitoring for the t at which is should  be revised 
	def fct_treat_case_veh_arrival_que_new_demand_final_dest_and_path_dyn_defined_without_sensor_monit(self,\
	vehicle,v_val_netwk,v_val_min_veh_hold_time,v_val_prec_round,v_val_ev_list,v_file_recording_event_db):
	
		#we calculate the que chosen by the vehicle
		lis_param_fct_calcul_queue_chosen_by_veh_from_cum_fct=[self._id_arrival_link,\
		v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_internal_links()[self._id_arrival_link].\
		get_id_head_intersection_node()].get_current_di_cum_rout_prob()]
		
		#rep=[[ random uniform nb, id veh lk location, id dest lk]]
		rep=self._obj_decisions.fct_calcul_queue_chosen_by_veh_from_cum_fct(\
		*lis_param_fct_calcul_queue_chosen_by_veh_from_cum_fct)
		
		lis_param_fct_calcul_queue_chosen_by_veh=[self._id_arrival_link,rep[List_Explicit_Values.val_third_element_of_list],v_val_netwk]
				
		queue_phase=self._obj_decisions.fct_calcul_queue_chosen_by_veh(*lis_param_fct_calcul_queue_chosen_by_veh)
		
		#we update the vehicle, we indicate the chosen queue and its arrival time in the queue
		vehicle.fct_update_veh_after_choosing_queue(queue_phase,self._event_time,v_val_netwk)
		

		
		#we examine if vehicle can leave the queue immediately
		veh_can_leave_que=self._obj_decisions.fct_defining_whether_veh_can_leave_que_by_its_arrival()
		
		#if the vehicle can leave the que
		if veh_can_leave_que==List_Explicit_Values.initialisation_value_to_one:
			print("PROBLEM IN CL_Ev_veh_arrived_que,\
			fct_treat_case_veh_arrival_que_new_demand_final_dest_and_path_dyn_defined_without_sensor_monit_without_estim_turn_prob: ",\
			veh_can_leave_que)
			import sys
			sys.exit()
			
		#if the vehicle cannot leave the que
		else:
			t_end_veh_hold_time=round(self._event_time+v_val_min_veh_hold_time,v_val_prec_round)
			
		#we examine if there are other vehicles in the que
		if v_val_netwk.get_di_entry_internal_links()[self._id_arrival_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].get_queue_veh()==[]:
			other_veh_in_que_before_add_veh=0
		else:
			other_veh_in_que_before_add_veh=1
			
		#we add the vehicle in the queue
		v_val_netwk.get_di_entry_internal_links()[self._id_arrival_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].\
		fct_update_veh_queue_when_veh_prohibited_to_leave_no_mod(vehicle)
		
		#we indicate the time at which the vehicle can leave the que regarding the hold duration
		vehicle.set_t_end_veh_hold_time_que(t_end_veh_hold_time)
		
		#if there are no veh in the que (otherwise veh will keave with ev end veh departure) 
		if other_veh_in_que_before_add_veh==0:
			#creat ev_end_hold_time
			ev_end_hold_time=Cl_Ev_end_veh_hold_at_que.Ev_end_veh_hold_at_que(val_event_t= t_end_veh_hold_time,\
			val_id_que=queue_phase.get_associated_phase_to_queue())
					
			#we add the event in the event list
			ev_end_hold_time.fct_insertion_even_in_event_list(event_list=v_val_ev_list,\
			message="IN CL_EV_VEH_ARRIVED_AT_QUE IN FUNCT f\
			fct_treat_case_veh_arrival_que_new_demand_final_dest_and_path_dyn_defined_without_sensor_monit_without_estim_turn_prob\
			EVENT END HOLD TIME HAS TIME < TIME FIRST EVENT IN THE LIST")
			
		li_id_veh=[]
		#print("queue_phase.get_associated_phase_to_queue()",queue_phase.get_associated_phase_to_queue())
		for i in v_val_netwk.get_di_entry_internal_links()[self._id_arrival_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].get_queue_veh():
			li_id_veh.append(i.get_id_veh())
			
	
		#we create an record database object 
		record_db_obj=Cl_Record_Database.Record_Database(\
		val_file_db=v_file_recording_event_db,\
		val_ev_time=self._event_time,\
		val_ev_type=self._event_type,\
		val_id_inters_node=[v_val_netwk.get_di_entry_internal_links()[\
		queue_phase.get_associated_phase_to_queue()[0]].get_id_head_intersection_node()],\
		val_t_start_current_inters_control=v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_internal_links()[\
		queue_phase.get_associated_phase_to_queue()[0]].\
		get_id_head_intersection_node()].get_intersection_control_obj().get_t_start_control(),\
		val_duration_current_inters_control=v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_internal_links()[\
		queue_phase.get_associated_phase_to_queue()[0]].\
		get_id_head_intersection_node()].get_intersection_control_obj().get_duration_control(),\
		val_current_inters_matrix_with_the_associated_link_of_phase=\
		v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_internal_links()[\
		queue_phase.get_associated_phase_to_queue()[0]].get_id_head_intersection_node()].\
		get_intersection_control_obj().\
		get_di_intersection_control_mat(),\
		val_duration_current_cycle=v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_internal_links()[\
		queue_phase.get_associated_phase_to_queue()[0]].\
		get_id_head_intersection_node()].get_intersection_control_obj().\
		get_cycle_duration_associated_with_control(),\
		val_vehicle_id=vehicle.get_id_veh(),\
		val_time_veh_appearance_in_network=vehicle.get_t_veh_appearance_at_network(),\
		val_id_veh_entry_link=vehicle.get_id_entry_link_veh_ap(),\
		val_id_current_link_veh_location=vehicle.get_current_id_link_veh_location(),\
		val_time_veh_arrival_at_current_link=vehicle.get_t_vehicle_arrival_at_current_link(),\
		val_time_veh_departure_from_current_link=vehicle.get_t_vehicle_departure_from_current_link(),\
		val_veh_current_queue_location=vehicle.get_veh_current_queue_location(),\
		val_time_veh_arrival_at_current_queue=vehicle.get_t_vehicle_arrival_at_current_queue(),\
		val_time_veh_start_departure_from_current_queue=vehicle.get_t_vehicle_started_departure_from_current_queue(),\
		val_time_veh_departure_from_current_queue=vehicle.get_t_vehicle_departure_from_current_queue(),\
		val_veh_id_destination_link=vehicle.get_veh_current_queue_location()[List_Explicit_Values.val_second_element_of_list],\
		val_time_veh_exit_from_network=vehicle.get_t_exit_veh_from_network(),\
		val_id_event_link=self._id_arrival_link,\
		val_veh_can_leave_now=veh_can_leave_que,\
		val_current_achieved_queue_service_rate_including_current_vehicle=\
		v_val_netwk.get_di_entry_internal_links()[self._id_arrival_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].\
		get_current_reached_service_rate(),\
		val_current_queue_service_rate=\
		v_val_netwk.get_di_entry_internal_links()[self._id_arrival_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].\
		get_current_queue_service_rate(),\
		val_li_id_vehicles_in_queue=li_id_veh)
			
				
		#we record the event in the db 
		record_db_obj.fct_write_object_in_db_file()
	
#*****************************************************************************************************************************************************************************************
	
#***************************************************************Cas New Demand-no OD-with sensor monit ***********************************************************************
	#method treating the case when a vehicle arrives at a que, a new generated demand is been generated, final destination and path are dyn defined, 
	#the employed control  requires  sensor monitoring for the t at which is should  be revised 
	
	def fct_treat_case_veh_arrival_que_new_demand_final_dest_and_path_dyn_defined_with_sensor_monit(self,\
	vehicle,v_val_netwk,v_val_min_veh_hold_time,v_val_prec_round,v_val_ev_list,v_file_recording_event_db,\
	v_val_ti_ctrl_revision_if_decided,val_min_nb_vehicles_to_detect):
	
		lis_param_fct_calcul_queue_chosen_by_veh_from_cum_fct=[self._id_arrival_link,\
		v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_internal_links()[self._id_arrival_link].\
		get_id_head_intersection_node()].get_current_di_cum_rout_prob()]
			
		#rep=[[ random uniform nb, id veh lk location, id dest lk]]
		rep=self._obj_decisions.fct_calcul_queue_chosen_by_veh_from_cum_fct(\
		*lis_param_fct_calcul_queue_chosen_by_veh_from_cum_fct)
			
		lis_param_fct_calcul_queue_chosen_by_veh=[self._id_arrival_link,\
		rep[List_Explicit_Values.val_third_element_of_list],v_val_netwk]
				
		queue_phase=self._obj_decisions.fct_calcul_queue_chosen_by_veh(*lis_param_fct_calcul_queue_chosen_by_veh)
		
		#we update the vehicle, we indicate the chosen queue and its arrival time in the queue
		vehicle.fct_update_veh_after_choosing_queue(queue_phase,self._event_time,v_val_netwk)
		
		#we examine if vehicle can leave the queue immediately
		veh_can_leave_que=self._obj_decisions.fct_defining_whether_veh_can_leave_que_by_its_arrival()
		
		#if the vehicle can leave the que
		if veh_can_leave_que==List_Explicit_Values.initialisation_value_to_one:
			print("PROBLEM IN CL_Ev_veh_arrived_que, fct_treat_case_veh_arrival_que_new_demand_final_dest_dynam_defined_with_sensor_monit: ",\
			veh_can_leave_que)
			import sys
			sys.exit()
		
		#if the vehicle cannot leave the que
		else:
			t_end_veh_hold_time=round(self._event_time+v_val_min_veh_hold_time,v_val_prec_round)
			
			#we examine if there are other vehicles in the que
			if v_val_netwk.get_di_entry_internal_links()[self._id_arrival_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
			[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].get_queue_veh()==[]:
					other_veh_in_que_before_add_veh=0
			else:
					other_veh_in_que_before_add_veh=1
					
			#we add the vehicle in the queue
			v_val_netwk.get_di_entry_internal_links()[self._id_arrival_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
			[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].\
			fct_update_veh_queue_when_veh_prohibited_to_leave_no_mod(vehicle)
				
			#we indicate the time at which the vehicle can leave the que regarding the hold duration
			vehicle.set_t_end_veh_hold_time_que(t_end_veh_hold_time)
				
			#if there are no veh in the que (otherwise veh will keave with ev end veh departure) 
			if other_veh_in_que_before_add_veh==0:
					
				#creat ev_end_hold_time
				ev_end_hold_time=Cl_Ev_end_veh_hold_at_que.Ev_end_veh_hold_at_que(val_event_t= t_end_veh_hold_time,\
				val_id_que=queue_phase.get_associated_phase_to_queue())
					
				#we add the event in the event list
				ev_end_hold_time.fct_insertion_even_in_event_list(event_list=v_val_ev_list,\
				message="IN CL_EV_VEH_ARRIVED_AT_QUE IN FUNCT \
				fct_treat_case_veh_arrival_que_new_demand_final_dest_and_path_dyn_defined_with_sensor_monit,\
				EVENT END HOLD TIME HAS TIME < TIME FIRST EVENT IN THE LIST")
				
			#if the queue is not a right turn 
			if queue_phase.get_type_veh_queue()!=Cl_Vehicle_Queue.TYPE_VEHICLE_QUEUE["right_turn"]:
			
				#if there is at least one detector detecting the veh
				if queue_phase.fct_exam_whether_at_least_nb_veh_detected_by_a_que_sensor(val_min_nb_veh_to_detect=val_min_nb_vehicles_to_detect)!=None:
				
					# controle dec update
					ev_end_deci_next_icm=Cl_Ev_end_decision_next_intersection_control.Ev_end_decision_next_intersection_control(\
					val_ev_time=v_val_ti_ctrl_revision_if_decided,\
					val_id_intersection_node=v_val_netwk.get_di_internal_links_to_network()[self._id_arrival_link].get_id_head_intersection_node(),\
					val_type_control_to_employ=\
					v_val_netwk.get_di_intersections()[v_val_netwk.get_di_internal_links_to_network()[self._id_arrival_link].\
					get_id_head_intersection_node()].get_ctrl_actuate_obj().get_type_employed_ctrl(),\
					val_control_category="sensor_requirement")
					#,val_reason_ctrl_revision_t_lim=0)	
		
					#on insert the event ev_end_dec_next_icm into the event list
					ev_end_deci_next_icm.fct_insertion_even_in_event_list(event_list=v_val_ev_list,\
					message="IN CL_Ev_veh_Arrived_at_quel IN FUNCT, \
					fct_treat_case_veh_arrival_que_new_demand_final_dest_and_path_dyn_defined_with_sensor_monit\
					NEXT ev_new_end_dec_netw_control EVENT HAS TIME < TIME FIRST EVENT IN THE LIST")
				
					#we indicate the intersection that a ctrl request is made
					v_val_netwk.get_di_intersections()[v_val_netwk.get_di_internal_links_to_network()[self._id_arrival_link].get_id_head_intersection_node()].\
					set_t_last_request_ctrl_revision_when_flux_monitoring(v_val_ti_ctrl_revision_if_decided)
						
					#we indicate the number of times a control revision is asked for the same time
					v_val_netwk.get_di_intersections()[v_val_netwk.get_di_internal_links_to_network()[self._id_arrival_link].get_id_head_intersection_node()].\
					set_nb_times_ctrl_revision_corresponding_to_t_last_request_ctrl_revision_when_flux_monitoring(\
					v_val_netwk.get_di_intersections()[v_val_netwk.get_di_internal_links_to_network()[self._id_arrival_link].get_id_head_intersection_node()].\
					set_nb_times_ctrl_revision_corresponding_to_t_last_request_ctrl_revision_when_flux_monitoring()+1)
			
		li_id_veh=[]
		#print("queue_phase.get_associated_phase_to_queue()",queue_phase.get_associated_phase_to_queue())
		for i in v_val_netwk.get_di_entry_internal_links()[self._id_arrival_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].get_queue_veh():
			li_id_veh.append(i.get_id_veh())
				
		#we create an record database object 
		record_db_obj=Cl_Record_Database.Record_Database(\
		val_file_db=v_file_recording_event_db,\
		val_ev_time=self._event_time,\
		val_ev_type=self._event_type,\
		val_id_inters_node=[v_val_netwk.get_di_entry_internal_links()[\
		queue_phase.get_associated_phase_to_queue()[0]].get_id_head_intersection_node()],\
		val_t_start_current_inters_control=v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_internal_links()[\
		queue_phase.get_associated_phase_to_queue()[0]].\
		get_id_head_intersection_node()].get_intersection_control_obj().get_t_start_control(),\
		val_duration_current_inters_control=v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_internal_links()[\
		queue_phase.get_associated_phase_to_queue()[0]].\
		get_id_head_intersection_node()].get_intersection_control_obj().get_duration_control(),\
		val_current_inters_matrix_with_the_associated_link_of_phase=\
		v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_internal_links()[\
		queue_phase.get_associated_phase_to_queue()[0]].get_id_head_intersection_node()].\
		get_intersection_control_obj().\
		get_di_intersection_control_mat(),\
		val_duration_current_cycle=v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_internal_links()[\
		queue_phase.get_associated_phase_to_queue()[0]].\
		get_id_head_intersection_node()].get_intersection_control_obj().\
		get_cycle_duration_associated_with_control(),\
		val_vehicle_id=vehicle.get_id_veh(),\
		val_time_veh_appearance_in_network=vehicle.get_t_veh_appearance_at_network(),\
		val_id_veh_entry_link=vehicle.get_id_entry_link_veh_ap(),\
		val_id_current_link_veh_location=vehicle.get_current_id_link_veh_location(),\
		val_time_veh_arrival_at_current_link=vehicle.get_t_vehicle_arrival_at_current_link(),\
		val_time_veh_departure_from_current_link=vehicle.get_t_vehicle_departure_from_current_link(),\
		val_veh_current_queue_location=vehicle.get_veh_current_queue_location(),\
		val_time_veh_arrival_at_current_queue=vehicle.get_t_vehicle_arrival_at_current_queue(),\
		val_time_veh_start_departure_from_current_queue=vehicle.get_t_vehicle_started_departure_from_current_queue(),\
		val_time_veh_departure_from_current_queue=vehicle.get_t_vehicle_departure_from_current_queue(),\
		val_veh_id_destination_link=vehicle.get_veh_current_queue_location()[List_Explicit_Values.val_second_element_of_list],\
		val_time_veh_exit_from_network=vehicle.get_t_exit_veh_from_network(),\
		val_id_event_link=self._id_arrival_link,\
		val_veh_can_leave_now=veh_can_leave_que,\
		val_current_achieved_queue_service_rate_including_current_vehicle=\
		v_val_netwk.get_di_entry_internal_links()[self._id_arrival_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].\
		get_current_reached_service_rate(),\
		val_current_queue_service_rate=\
		v_val_netwk.get_di_entry_internal_links()[self._id_arrival_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].\
		get_current_queue_service_rate(),\
		val_li_id_vehicles_in_queue=li_id_veh,\
		val_nb_veh_in_ar_lk=v_val_netwk.get_di_all_links()[i.get_current_id_link_veh_location()].get_current_nb_veh_link())
				
		#we record the event in the db 
		record_db_obj.fct_write_object_in_db_file()
				
			
#*****************************************************************************************************************************************************************************************
#********************************************************Cas New Demand-no OD****************************************************************************************************
	#method treat the case when a new demand is consired, veh final dest and path are dynam calculated
	def fct_treat_case_veh_ar_at_que_when_new_demand_final_dest_and_path_dynam_defined(self,\
	val_netwk,val_min_veh_hold_time,val_prec_round,val_ev_list,val_file_recording_event_db,val_min_nb_veh_to_detect):
	
		#if the t control revison requires sensor monitor
		if val_netwk.get_di_intersections()[val_netwk.get_di_entry_internal_links()\
		[self._id_arrival_link].get_id_head_intersection_node()].get_intersection_control_obj().get_type_control_related_to_t_revision()==\
		Cl_Control_Actuate.TYPE_CONTROL_T_REVISION_CATEGORY["sensor_requirement_for_t_update"]:
		
			val_ti_ctrl_revision_if_decided=self._obj_decisions.fct_calculate_t_ctrl_revision(t_cur=self._event_time,dur=\
			val_netwk.get_di_intersections()[val_netwk.get_di_entry_internal_links()\
			[self._id_arrival_link].get_id_head_intersection_node()].get_intersection_control_obj().\
			get_t_duration_for_defining_t_ctrl_revision_when_at_given_time_sensor_records_veh_variation())
			
			for i in self._li_vehicle:
		
				self.fct_treat_case_veh_arrival_que_new_demand_final_dest_and_path_dyn_defined_with_sensor_monit(\
				vehicle=i,v_val_netwk=val_netwk,v_val_min_veh_hold_time=val_min_veh_hold_time,v_val_prec_round=val_prec_round,\
				v_val_ev_list=val_ev_list,v_file_recording_event_db=val_file_recording_event_db,\
				v_val_ti_ctrl_revision_if_decided=val_ti_ctrl_revision_if_decided,val_min_nb_vehicles_to_detect=val_min_nb_veh_to_detect)
		
		#if the t control revison does not require sensor monitor
		elif val_netwk.get_di_intersections()[val_netwk.get_di_entry_internal_links()\
		[self._id_arrival_link].get_id_head_intersection_node()].get_intersection_control_obj().get_type_control_related_to_t_revision()==\
		Cl_Control_Actuate.TYPE_CONTROL_T_REVISION_CATEGORY["without_sensor_requirement_for_t_update"]:
			
			for i in self._li_vehicle:
		
				self.fct_treat_case_veh_arrival_que_new_demand_final_dest_and_path_dyn_defined_without_sensor_monit(\
				vehicle=i,v_val_netwk=val_netwk,v_val_min_veh_hold_time=val_min_veh_hold_time,v_val_prec_round=val_prec_round,\
				v_val_ev_list=val_ev_list,v_file_recording_event_db=val_file_recording_event_db)
		
		#if none of the previous cases
		else:
			print("PROBLEM IN CL_EV_VEH_AR, FCT fct_treat_case_veh_ar_at_que_when_new_demand_final_dest_and_path_dynam_defined, ",\
			val_netwk.get_di_intersections()[val_netwk.get_di_entry_internal_links()\
			[self._id_arrival_link].get_id_head_intersection_node()].get_intersection_control_obj().get_type_control_related_to_t_revision())
			import sys
			sys.exit()
 

#*****************************************************************************************************************************************************************************************


#***************************************************Cas New Demand-with OD and given path-without sensor monit *************************************************************
	#method treating the case when a vehicle arrives at a que, a new generated demand is been generated, final destination and path are initially defined, 
	#the employed control  does not require  sensor monitoring for the t at which is should  be revised 
	
	def fct_treat_case_veh_arrival_que_new_demand_final_dest_and_path_intial_defined_without_sensor_monit(self,\
	vehicle,v_val_netwk,v_val_min_veh_hold_time,v_val_prec_round,v_val_ev_list,v_file_recording_event_db):
	
		#we update the indicator of the veh current location  in the que
		new_v=vehicle.get_index_current_veh_link_location_in_path_list_when_given_destination()+1
			
		vehicle.set_index_current_veh_link_location_in_path_list_when_given_destination(new_v)
		
		#we calculate the que chosen by the vehicle
		li_param_fct_calcul_que_chosen_by_veh=[vehicle.get_id_entry_link_veh_ap(),self._id_arrival_link,\
		vehicle.get_id_veh_final_destination_link(),\
		vehicle.get_index_current_veh_link_location_in_path_list_when_given_destination(),\
		v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_internal_links()[vehicle.get_id_entry_link_veh_ap()].\
		get_id_head_intersection_node()].get_current_di_unique_paths(),v_val_netwk]
		
		#the vehicle queue  object chosen for the vehicle to join in
		queue_phase=self._obj_decisions.fct_calcul_queue_chosen_by_veh_cas_given_final_destination(*li_param_fct_calcul_que_chosen_by_veh)
		
		#we update the vehicle, we indicate the chosen queue and its arrival time in the queue
		vehicle.fct_update_veh_after_choosing_queue(queue_phase,self._event_time,v_val_netwk)
		
		#we examine if vehicle can leave the queue immediately
		veh_can_leave_que=self._obj_decisions.fct_defining_whether_veh_can_leave_que_by_its_arrival()
		
		#if the vehicle can leave the que
		if veh_can_leave_que==List_Explicit_Values.initialisation_value_to_one:
			print("PROBLEM IN CL_Ev_veh_arrived_que, fct_treat_case_veh_arrival_que_new_demand_final_dest_and_path_intial_defined_without_sensor_monit: ",\
			veh_can_leave_que)
			import sys
			sys.exit()
			
		#if the vehicle cannot leave the que
		else:
			t_end_veh_hold_time=round(self._event_time+v_val_min_veh_hold_time,v_val_prec_round)
			
			#we examine if there are other vehicles in the que
			if v_val_netwk.get_di_entry_internal_links()[self._id_arrival_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
			[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].get_queue_veh()==[]:
				other_veh_in_que_before_add_veh=0
			else:
				other_veh_in_que_before_add_veh=1
				
			#we add the vehicle in the queue
			v_val_netwk.get_di_entry_internal_links()[self._id_arrival_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
			[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].\
			fct_update_veh_queue_when_veh_prohibited_to_leave_with_mod(vehicle)
			
			#we indicate the time at which the vehicle can leave the que regarding the hold duration
			vehicle.set_t_end_veh_hold_time_que(t_end_veh_hold_time)
			
			#if there are no veh in the que (otherwise veh will keave with ev end veh departure)
			if other_veh_in_que_before_add_veh==0:
				#creat ev_end_hold_time
				ev_end_hold_time=Cl_Ev_end_veh_hold_at_que.Ev_end_veh_hold_at_que(val_event_t= t_end_veh_hold_time,\
				val_id_que=queue_phase.get_associated_phase_to_queue())
					
				#we add the event in the event list
				ev_end_hold_time.fct_insertion_even_in_event_list(event_list=v_val_ev_list,\
				message="IN CL_EV_VEH_ARRIVED_AT_QUE IN FUNCT \
				fct_treat_case_veh_arrival_que_new_demand_final_dest_and_path_intial_defined_without_sensor_monit,\
				EVENT END HOLD TIME HAS TIME < TIME FIRST EVENT IN THE LIST")
			
		li_id_veh=[]
		#print("queue_phase.get_associated_phase_to_queue()",queue_phase.get_associated_phase_to_queue())
		for i in v_val_netwk.get_di_entry_internal_links()[self._id_arrival_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].get_queue_veh():
			li_id_veh.append(i.get_id_veh())
			
	
		#we create an record database object 
		record_db_obj=Cl_Record_Database.Record_Database(\
		val_file_db=v_file_recording_event_db,\
		val_ev_time=self._event_time,\
		val_ev_type=self._event_type,\
		val_id_inters_node=[v_val_netwk.get_di_entry_internal_links()[\
		queue_phase.get_associated_phase_to_queue()[0]].get_id_head_intersection_node()],\
		val_t_start_current_inters_control=v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_internal_links()[\
		queue_phase.get_associated_phase_to_queue()[0]].\
		get_id_head_intersection_node()].get_intersection_control_obj().get_t_start_control(),\
		val_duration_current_inters_control=v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_internal_links()[\
		queue_phase.get_associated_phase_to_queue()[0]].\
		get_id_head_intersection_node()].get_intersection_control_obj().get_duration_control(),\
		val_current_inters_matrix_with_the_associated_link_of_phase=\
		v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_internal_links()[\
		queue_phase.get_associated_phase_to_queue()[0]].get_id_head_intersection_node()].\
		get_intersection_control_obj().\
		get_di_intersection_control_mat(),\
		val_duration_current_cycle=v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_internal_links()[\
		queue_phase.get_associated_phase_to_queue()[0]].\
		get_id_head_intersection_node()].get_intersection_control_obj().\
		get_cycle_duration_associated_with_control(),\
		val_vehicle_id=vehicle.get_id_veh(),\
		val_time_veh_appearance_in_network=vehicle.get_t_veh_appearance_at_network(),\
		val_id_veh_entry_link=vehicle.get_id_entry_link_veh_ap(),\
		val_id_current_link_veh_location=vehicle.get_current_id_link_veh_location(),\
		val_time_veh_arrival_at_current_link=vehicle.get_t_vehicle_arrival_at_current_link(),\
		val_time_veh_departure_from_current_link=vehicle.get_t_vehicle_departure_from_current_link(),\
		val_veh_current_queue_location=vehicle.get_veh_current_queue_location(),\
		val_time_veh_arrival_at_current_queue=vehicle.get_t_vehicle_arrival_at_current_queue(),\
		val_time_veh_start_departure_from_current_queue=vehicle.get_t_vehicle_started_departure_from_current_queue(),\
		val_time_veh_departure_from_current_queue=vehicle.get_t_vehicle_departure_from_current_queue(),\
		val_veh_id_destination_link=vehicle.get_veh_current_queue_location()[List_Explicit_Values.val_second_element_of_list],\
		val_time_veh_exit_from_network=vehicle.get_t_exit_veh_from_network(),\
		val_id_event_link=self._id_arrival_link,\
		val_veh_can_leave_now=veh_can_leave_que,\
		val_current_achieved_queue_service_rate_including_current_vehicle=\
		v_val_netwk.get_di_entry_internal_links()[self._id_arrival_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].\
		get_current_reached_service_rate(),\
		val_current_queue_service_rate=\
		v_val_netwk.get_di_entry_internal_links()[self._id_arrival_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].\
		get_current_queue_service_rate(),\
		val_li_id_vehicles_in_queue=li_id_veh)
		#,\
		#val_nb_veh_in_ar_lk=val_netwk.get_di_all_links()[i.get_current_id_link_veh_location()].get_current_nb_veh_link())
		#val_prob_rout_prop_current_lk=val_netwk.get_dict_mat_od_key_id_entry_internal_lk_value_list_dest_lks()[\
		#queue_phase.get_associated_phase_to_queue()[0]])
				
		#we record the event in the db 
		record_db_obj.fct_write_object_in_db_file()

#*****************************************************************************************************************************************************************************************

#**************************************************Cas New Demand-with OD and given path-with sensor monit *****************************************************************
	#method treating the case when a vehicle arrives at a que, a new generated demand is been generated, final destination and path are initially defined, 
	#the employed control  requires  sensor monitoring for the t at which is should  be revised 
	
	def fct_treat_case_veh_arrival_que_new_demand_final_dest_and_path_intial_defined_with_sensor_monit(self,\
	vehicle,v_val_netwk,v_val_min_veh_hold_time,\
	v_val_prec_round,v_val_ev_list,v_file_recording_event_db,v_val_ti_ctrl_revision_if_decided,\
	val_min_nb_vehicles_to_detect):
	
		#we update the indicator of the veh current location  in the que
		new_v=vehicle.get_index_current_veh_link_location_in_path_list_when_given_destination()+1
					
		vehicle.set_index_current_veh_link_location_in_path_list_when_given_destination(new_v)
		
		#we calculate the que chosen by the vehicle
		li_param_fct_calcul_que_chosen_by_veh=[\
		vehicle.get_id_entry_link_veh_ap(),self._id_arrival_link,\
		vehicle.get_id_veh_final_destination_link(),\
		vehicle.get_index_current_veh_link_location_in_path_list_when_given_destination(),\
		v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_internal_links()[vehicle.get_id_entry_link_veh_ap()].\
		get_id_head_intersection_node()].get_current_di_unique_paths(),v_val_netwk]
		
		#the vehicle queue  object chosen for the vehicle to join in
		queue_phase=self._obj_decisions.fct_calcul_queue_chosen_by_veh_cas_given_final_destination(*li_param_fct_calcul_que_chosen_by_veh)
		
		#we update the vehicle, we indicate the chosen queue and its arrival time in the queue
		vehicle.fct_update_veh_after_choosing_queue(queue_phase,self._event_time,v_val_netwk)
		
		#we examine if vehicle can leave the queue immediately
		veh_can_leave_que=self._obj_decisions.fct_defining_whether_veh_can_leave_que_by_its_arrival()
		
		#if the vehicle can leave the que
		if veh_can_leave_que==List_Explicit_Values.initialisation_value_to_one:
			print("PROBLEM IN CL_Ev_veh_arrived_at_que veh_can_leave_que, \
			fct_treat_case_veh_arrival_que_new_demand_final_dest_and_path_intial_defined_with_sensor_monit ",veh_can_leave_que)
			import sys
			sys.exit()
		
		#if the vehicle can not leave the que
		else:
			t_end_veh_hold_time=round(self._event_time+v_val_min_veh_hold_time,v_val_prec_round)
			
			#we examine if there are other vehicles in the que
			if v_val_netwk.get_di_entry_internal_links()[self._id_arrival_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
			[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].get_queue_veh()==[]:
				other_veh_in_que_before_add_veh=0
			else:
				other_veh_in_que_before_add_veh=1
				
			#we add the vehicle in the queue
			v_val_netwk.get_di_entry_internal_links()[self._id_arrival_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
			[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].\
			fct_update_veh_queue_when_veh_prohibited_to_leave_with_mod(vehicle)
			
			#we indicate the time at which the vehicle can leave the que regarding the hold duration
			vehicle.set_t_end_veh_hold_time_que(t_end_veh_hold_time)
			
			#if there are no veh in the que (otherwise veh will keave with ev end veh departure) 
			if other_veh_in_que_before_add_veh==0:
			
				#creat ev_end_hold_time
				ev_end_hold_time=Cl_Ev_end_veh_hold_at_que.Ev_end_veh_hold_at_que(val_event_t= t_end_veh_hold_time,\
				val_id_que=queue_phase.get_associated_phase_to_queue())
					
				#we add the event in the event list
				ev_end_hold_time.fct_insertion_even_in_event_list(event_list=v_val_ev_list,\
				message="IN CL_EV_VEH_ARRIVED_AT_QUE IN FUNCT \
				fct_treat_case_veh_arrival_que_new_demand_final_dest_and_path_intial_defined_with_sensor_monit,\
				EVENT END HOLD TIME HAS TIME < TIME FIRST EVENT IN THE LIST")
				
			#if the queue is not a right turn 
			if queue_phase.get_type_veh_queue()!=Cl_Vehicle_Queue.TYPE_VEHICLE_QUEUE["right_turn"]:
			
				#if there is at least one detector detecting the veh
				if queue_phase.fct_exam_whether_at_least_nb_veh_detected_by_a_que_sensor(val_min_nb_veh_to_detect=val_min_nb_vehicles_to_detect)!=None:
				
					# controle dec update
					ev_end_deci_next_icm=Cl_Ev_end_decision_next_intersection_control.Ev_end_decision_next_intersection_control(\
					val_ev_time=v_val_ti_ctrl_revision_if_decided,\
					val_id_intersection_node=v_val_netwk.get_di_internal_links_to_network()[self._id_arrival_link].get_id_head_intersection_node(),\
					val_type_control_to_employ=\
					v_val_netwk.get_di_intersections()[v_val_netwk.get_di_internal_links_to_network()[self._id_arrival_link].\
					get_id_head_intersection_node()].get_ctrl_actuate_obj().get_type_employed_ctrl(),\
					val_control_category="sensor_requirement")
					#,val_reason_ctrl_revision_t_lim=0)	
		
					#on insert the event ev_end_dec_next_icm into the event list
					ev_end_deci_next_icm.fct_insertion_even_in_event_list(event_list=v_val_ev_list,\
					message="IN CL_Ev_veh_Arrived_at_quel IN FUNCT, \
					fct_treat_case_veh_arrival_que_new_demand_final_dest_and_path_intial_defined_with_sensor_monit\
					NEXT ev_new_end_dec_netw_control EVENT HAS TIME < TIME FIRST EVENT IN THE LIST")
				
					#we indicate the intersection that a ctrl request is made
					#v_val_netwk.get_di_intersections()[v_val_netwk.get_di_internal_links_to_network()[self._id_arrival_link].get_id_head_intersection_node()].\
					#set_t_last_request_ctrl_revision_when_flux_monitoring(v_val_ti_ctrl_revision_if_decided)
						
					#we indicate the number of times a control revision is asked for the same time
					#v_val_netwk.get_di_intersections()[v_val_netwk.get_di_internal_links_to_network()[self._id_arrival_link].get_id_head_intersection_node()].\
					#set_nb_times_ctrl_revision_corresponding_to_t_last_request_ctrl_revision_when_flux_monitoring(\
					#v_val_netwk.get_di_intersections()[v_val_netwk.get_di_internal_links_to_network()[self._id_arrival_link].get_id_head_intersection_node()].\
					#set_nb_times_ctrl_revision_corresponding_to_t_last_request_ctrl_revision_when_flux_monitoring()+1)
		
		li_id_veh=[]
		for i in v_val_netwk.get_di_entry_internal_links()[self._id_arrival_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[queue_phase.get_associated_phase_to_queue()[0],\
		queue_phase.get_associated_phase_to_queue()[1]].get_queue_veh():
					
			li_id_veh.append(i.get_id_veh())
						
		#we create an record database object 
		record_db_obj=Cl_Record_Database.Record_Database(\
		val_file_db=v_file_recording_event_db,\
		val_ev_time=self._event_time,\
		val_ev_type=self._event_type,\
		val_id_inters_node=[v_val_netwk.get_di_entry_internal_links()[\
		queue_phase.get_associated_phase_to_queue()[0]].get_id_head_intersection_node()],\
		val_t_start_current_inters_control=v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_internal_links()[\
		queue_phase.get_associated_phase_to_queue()[0]].\
		get_id_head_intersection_node()].get_intersection_control_obj().get_t_start_control(),\
		val_duration_current_inters_control=v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_internal_links()[\
		queue_phase.get_associated_phase_to_queue()[0]].\
		get_id_head_intersection_node()].get_intersection_control_obj().get_duration_control(),\
		val_current_inters_matrix_with_the_associated_link_of_phase=\
		v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_internal_links()[\
		queue_phase.get_associated_phase_to_queue()[0]].get_id_head_intersection_node()].\
		get_intersection_control_obj().\
		get_di_intersection_control_mat(),\
		val_duration_current_cycle=v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_internal_links()[\
		queue_phase.get_associated_phase_to_queue()[0]].\
		get_id_head_intersection_node()].get_intersection_control_obj().\
		get_cycle_duration_associated_with_control(),\
		val_vehicle_id=vehicle.get_id_veh(),\
		val_time_veh_appearance_in_network=vehicle.get_t_veh_appearance_at_network(),\
		val_id_veh_entry_link=vehicle.get_id_entry_link_veh_ap(),\
		val_id_current_link_veh_location=vehicle.get_current_id_link_veh_location(),\
		val_time_veh_arrival_at_current_link=vehicle.get_t_vehicle_arrival_at_current_link(),\
		val_time_veh_departure_from_current_link=vehicle.get_t_vehicle_departure_from_current_link(),\
		val_veh_current_queue_location=vehicle.get_veh_current_queue_location(),\
		val_time_veh_arrival_at_current_queue=vehicle.get_t_vehicle_arrival_at_current_queue(),\
		val_time_veh_start_departure_from_current_queue=vehicle.get_t_vehicle_started_departure_from_current_queue(),\
		val_time_veh_departure_from_current_queue=vehicle.get_t_vehicle_departure_from_current_queue(),\
		val_veh_id_destination_link=vehicle.get_veh_current_queue_location()[List_Explicit_Values.val_second_element_of_list],\
		val_time_veh_exit_from_network=vehicle.get_t_exit_veh_from_network(),\
		val_id_event_link=self._id_arrival_link,\
		val_veh_can_leave_now=veh_can_leave_que,\
		val_current_achieved_queue_service_rate_including_current_vehicle=\
		v_val_netwk.get_di_entry_internal_links()[self._id_arrival_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].\
		get_current_reached_service_rate(),\
		val_current_queue_service_rate=\
		v_val_netwk.get_di_entry_internal_links()[self._id_arrival_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].\
		get_current_queue_service_rate(),\
		val_li_id_vehicles_in_queue=li_id_veh,\
		val_nb_veh_in_ar_lk=v_val_netwk.get_di_all_links()[i.get_current_id_link_veh_location()].get_current_nb_veh_link())
		#val_prob_rout_prop_current_lk=val_netwk.get_dict_mat_od_key_id_entry_internal_lk_value_list_dest_lks()[\
		#queue_phase.get_associated_phase_to_queue()[0]])					
		#we record the event in the db 
			
		record_db_obj.fct_write_object_in_db_file()
		

#*****************************************************************************************************************************************************************************************

#********************************************************************NEW DEMAND - WITH OD AND GIVEN PATH ***************************************************************
	#method treating the case when New demand is employed final dest and path are given
	def fct_treat_case_veh_ar_at_que_when_new_demand_final_dest_and_path_given(self,val_netwk,val_min_veh_hold_time,val_prec_round,val_ev_list,\
	val_file_recording_event_db,val_min_nb_veh_to_detect):
	
		#if the t control revison requires sensor monitor for the  t update
		if val_netwk.get_di_intersections()[val_netwk.get_di_entry_internal_links()\
		[self._id_arrival_link].get_id_head_intersection_node()].get_intersection_control_obj().get_type_control_related_to_t_revision()==\
		Cl_Control_Actuate.TYPE_CONTROL_T_REVISION_CATEGORY["sensor_requirement_for_t_update"]:
		
			val_ti_ctrl_revision_if_decided=self._obj_decisions.fct_calculate_t_ctrl_revision(t_cur=self._event_time,dur=\
			val_netwk.get_di_intersections()[val_netwk.get_di_entry_internal_links()\
			[self._id_arrival_link].get_id_head_intersection_node()].get_intersection_control_obj().\
			get_t_duration_for_defining_t_ctrl_revision_when_at_given_time_sensor_records_veh_variation())
			
			for i in self._li_vehicle:
			
				self.fct_treat_case_veh_arrival_que_new_demand_final_dest_and_path_intial_defined_with_sensor_monit(\
				vehicle=i,v_val_netwk=val_netwk,v_val_min_veh_hold_time=val_min_veh_hold_time,\
				v_val_prec_round=val_prec_round,v_val_ev_list=val_ev_list,v_file_recording_event_db=val_file_recording_event_db,\
				v_val_ti_ctrl_revision_if_decided=val_ti_ctrl_revision_if_decided,\
				val_min_nb_vehicles_to_detect=val_min_nb_veh_to_detect)
			
		
		#if the t control revison does not require sensor monitor for the t update
		elif val_netwk.get_di_intersections()[val_netwk.get_di_entry_internal_links()\
		[self._id_arrival_link].get_id_head_intersection_node()].get_intersection_control_obj().get_type_control_related_to_t_revision()==\
		Cl_Control_Actuate.TYPE_CONTROL_T_REVISION_CATEGORY["without_sensor_requirement_for_t_update"]:
		
			for i in self._li_vehicle:
			
				self.fct_treat_case_veh_arrival_que_new_demand_final_dest_and_path_intial_defined_without_sensor_monit(\
				vehicle=i,v_val_netwk=val_netwk,v_val_min_veh_hold_time=val_min_veh_hold_time,v_val_prec_round=val_prec_round,\
				v_val_ev_list=val_ev_list,v_file_recording_event_db=val_file_recording_event_db)
		
		#if none of the previous cases
		else:
			print("PROBLEM IN CL_EV_VEH_AR, FCT fct_treat_case_veh_ar_at_que_when_new_demand_final_dest_and_path_given, ",\
			val_netwk.get_di_intersections()[val_netwk.get_di_entry_internal_links()\
			[self._id_arrival_link].get_id_head_intersection_node()].get_intersection_control_obj().get_type_control_related_to_t_revision())
			import sys
			sys.exit()
		
		


#*****************************************************************************************************************************************************************************************

#**************************************************Cas New Demand-with OD and dyn computed path-without sensor monit ***************************************************

	#method treating the case when veh arrives at a queue, a new demand is generated and the final vehicle destination is initially defined, its path is dyn computed
	#the employed control requires no monitoring for the t at which is should  be revised
	def fct_treat_case_veh_arrival_que_new_demand_final_dest_initial_defined_path_dyn_computed_without_sensor_monit(self,vehicle,v_val_netwk,\
	v_val_min_veh_hold_time,v_val_prec_round,v_val_ev_list,v_file_recording_event_db,v_val_fct_calc_queue_id_when_given_final_dest_and_path_dynam_constructed):
	
		#we update the indicator of the veh current location  in the que
		new_v=vehicle.get_index_current_veh_link_location_in_path_list_when_given_destination()+1
			
		vehicle.set_index_current_veh_link_location_in_path_list_when_given_destination(new_v)
				
		#we decide the que chosen by the vehicle
		li_param_fct_calcul_que_chosen_by_veh=[\
		v_val_netwk,self._id_arrival_link,vehicle.get_id_veh_final_destination_link(),v_val_fct_calc_queue_id_when_given_final_dest_and_path_dynam_constructed]
		
		#id_que=[id input lk, id output lk]
		id_dest_lk=self._obj_decisions.fct_calcul_queue_chosen_by_veh_cas_given_final_destination_dyn_constr_path(*\
		li_param_fct_calcul_que_chosen_by_veh)
		
		#the vehicle queue  object chosen for the vehicle to join in
		queue_phase=v_val_netwk.get_di_entry_internal_links()[self._id_arrival_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()[\
		self._id_arrival_link,id_dest_lk]
		
		#we update the vehicle, we indicate the chosen queue and its arrival time in the queue
		vehicle.fct_update_veh_after_choosing_queue(queue_phase,self._event_time,v_val_netwk)
		
		#we update the link (its travel time employed by the algo computing the split ratios)
		v_val_netwk.get_di_entry_internal_links()[self._id_arrival_link].fct_update_link_when_split_ratios_dyn_computed(\
		val_new_trav_time=round(self._event_time-vehicle.get_t_vehicle_arrival_at_current_link()))
		
		#we examine if vehicle can leave the queue immediately
		veh_can_leave_que=self._obj_decisions.fct_defining_whether_veh_can_leave_que_by_its_arrival()
		
		#if the vehicle can leave the que
		if veh_can_leave_que==List_Explicit_Values.initialisation_value_to_one:
			print("PROBLEM IN CL_Ev_veh_arrived_que, \
			fct_treat_case_veh_arrival_que_new_demand_final_dest_initial_defined_path_dyn_computed_without_sensor_monit: ",\
			veh_can_leave_que)
			import sys
			sys.exit()
			
		#if the vehicle cannot leave the que
		else:
			t_end_veh_hold_time=round(self._event_time+v_val_min_veh_hold_time,v_val_prec_round)
			
			#we examine if there are other vehicles in the que
			if v_val_netwk.get_di_entry_internal_links()[self._id_arrival_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
			[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].get_queue_veh()==[]:
				other_veh_in_que_before_add_veh=0
			else:
				other_veh_in_que_before_add_veh=1
				
			#we add the vehicle in the queue
			v_val_netwk.get_di_entry_internal_links()[self._id_arrival_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
			[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].\
			fct_update_veh_queue_when_veh_prohibited_to_leave_no_mod(vehicle)
			
			#we indicate the time at which the vehicle can leave the que regarding the hold duration
			vehicle.set_t_end_veh_hold_time_que(t_end_veh_hold_time)
			
			#if there are no veh in the que (otherwise veh will keave with ev end veh departure) 
			if other_veh_in_que_before_add_veh==0:
					
				#creat ev_end_hold_time
				ev_end_hold_time=Cl_Ev_end_veh_hold_at_que.Ev_end_veh_hold_at_que(val_event_t= t_end_veh_hold_time,\
				val_id_que=queue_phase.get_associated_phase_to_queue())
					
				#we add the event in the event list
				ev_end_hold_time.fct_insertion_even_in_event_list(event_list=v_val_ev_list,\
				message="IN CL_EV_VEH_ARRIVED_AT_QUE IN FUNCT \
				fct_treat_case_veh_arrival_que_new_demand_final_dest_initial_defined_path_dyn_computed_without_sensor_monit,\
				EVENT END HOLD TIME HAS TIME < TIME FIRST EVENT IN THE LIST")
				
		li_id_veh=[]
		#print("queue_phase.get_associated_phase_to_queue()",queue_phase.get_associated_phase_to_queue())
		for i in v_val_netwk.get_di_entry_internal_links()[self._id_arrival_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].get_queue_veh():
			li_id_veh.append(i.get_id_veh())
				
		#we create an record database object 
		record_db_obj=Cl_Record_Database.Record_Database(\
		val_file_db=v_file_recording_event_db,\
		val_ev_time=self._event_time,\
		val_ev_type=self._event_type,\
		val_id_inters_node=[v_val_netwk.get_di_entry_internal_links()[\
		queue_phase.get_associated_phase_to_queue()[0]].get_id_head_intersection_node()],\
		val_t_start_current_inters_control=v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_internal_links()[\
		queue_phase.get_associated_phase_to_queue()[0]].\
		get_id_head_intersection_node()].get_intersection_control_obj().get_t_start_control(),\
		val_duration_current_inters_control=v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_internal_links()[\
		queue_phase.get_associated_phase_to_queue()[0]].\
		get_id_head_intersection_node()].get_intersection_control_obj().get_duration_control(),\
		val_current_inters_matrix_with_the_associated_link_of_phase=\
		v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_internal_links()[\
		queue_phase.get_associated_phase_to_queue()[0]].get_id_head_intersection_node()].\
		get_intersection_control_obj().\
		get_di_intersection_control_mat(),\
		val_duration_current_cycle=v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_internal_links()[\
		queue_phase.get_associated_phase_to_queue()[0]].\
		get_id_head_intersection_node()].get_intersection_control_obj().\
		get_cycle_duration_associated_with_control(),\
		val_vehicle_id=vehicle.get_id_veh(),\
		val_time_veh_appearance_in_network=vehicle.get_t_veh_appearance_at_network(),\
		val_id_veh_entry_link=vehicle.get_id_entry_link_veh_ap(),\
		val_id_current_link_veh_location=vehicle.get_current_id_link_veh_location(),\
		val_time_veh_arrival_at_current_link=vehicle.get_t_vehicle_arrival_at_current_link(),\
		val_time_veh_departure_from_current_link=vehicle.get_t_vehicle_departure_from_current_link(),\
		val_veh_current_queue_location=vehicle.get_veh_current_queue_location(),\
		val_time_veh_arrival_at_current_queue=vehicle.get_t_vehicle_arrival_at_current_queue(),\
		val_time_veh_start_departure_from_current_queue=vehicle.get_t_vehicle_started_departure_from_current_queue(),\
		val_time_veh_departure_from_current_queue=vehicle.get_t_vehicle_departure_from_current_queue(),\
		val_veh_id_destination_link=vehicle.get_veh_current_queue_location()[List_Explicit_Values.val_second_element_of_list],\
		val_time_veh_exit_from_network=vehicle.get_t_exit_veh_from_network(),\
		val_id_event_link=self._id_arrival_link,\
		val_veh_can_leave_now=veh_can_leave_que,\
		val_current_achieved_queue_service_rate_including_current_vehicle=\
		v_val_netwk.get_di_entry_internal_links()[self._id_arrival_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].\
		get_current_reached_service_rate(),\
		val_current_queue_service_rate=\
		v_val_netwk.get_di_entry_internal_links()[self._id_arrival_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].\
		get_current_queue_service_rate(),\
		val_li_id_vehicles_in_queue=li_id_veh,\
		val_nb_veh_in_ar_lk=v_val_netwk.get_di_all_links()[i.get_current_id_link_veh_location()].get_current_nb_veh_link())
				
		#we record the event in the db 
		record_db_obj.fct_write_object_in_db_file()

#*****************************************************************************************************************************************************************************************




#*************************************************Cas New Demand-with OD and dyn computed path-with sensor monit ********************************************************
	#method treating the case when veh arrives at a queue, a new demand is generated and the final vehicle destination is initially defined, its path is dyn computed
	#the employed control requires monitoring for the t at which is should  be revised
	def fct_treat_case_veh_arrival_que_new_demand_final_dest_initial_defined_path_dyn_computed_with_sensor_monit(self,\
	vehicle,v_val_netwk,v_val_min_veh_hold_time,v_val_prec_round,v_val_ev_list,v_file_recording_event_db,\
	v_val_ti_ctrl_revision_if_decided,v_val_fct_calc_queue_id_when_given_final_dest_and_path_dynam_constructed,\
	val_min_nb_vehicles_to_detect):
	
		#we update the indicator of the veh current location  in the que
		new_v=vehicle.get_index_current_veh_link_location_in_path_list_when_given_destination()+1
			
		vehicle.set_index_current_veh_link_location_in_path_list_when_given_destination(new_v)
				
		#we decide the que chosen by the vehicle
		li_param_fct_calcul_que_chosen_by_veh=[\
		v_val_netwk,self._id_arrival_link,vehicle.get_id_veh_final_destination_link(),v_val_fct_calc_queue_id_when_given_final_dest_and_path_dynam_constructed]
		
		#id_que=[id input lk, id output lk]
		id_dest_lk=self._obj_decisions.fct_calcul_queue_chosen_by_veh_cas_given_final_destination_dyn_constr_path(*\
		li_param_fct_calcul_que_chosen_by_veh)
		
		#the vehicle queue  object chosen for the vehicle to join in
		queue_phase=v_val_netwk.get_di_entry_internal_links()[self._id_arrival_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()[\
		self._id_arrival_link,id_dest_lk]
		
		#we update the vehicle, we indicate the chosen queue and its arrival time in the queue
		vehicle.fct_update_veh_after_choosing_queue(queue_phase,self._event_time,v_val_netwk)
		
		#we update the link (its travel time employed by the algo computing the split ratios)
		v_val_netwk.get_di_entry_internal_links()[self._id_arrival_link].fct_update_link_when_split_ratios_dyn_computed(\
		val_new_trav_time=round(self._event_time-vehicle.get_t_vehicle_arrival_at_current_link()))
		
		#we examine if vehicle can leave the queue immediately
		veh_can_leave_que=self._obj_decisions.fct_defining_whether_veh_can_leave_que_by_its_arrival()
		
		#if the vehicle can leave the que
		if veh_can_leave_que==List_Explicit_Values.initialisation_value_to_one:
			print("PROBLEM IN CL_Ev_veh_arrived_que, fct_treat_case_veh_arrival_que_new_demand_final_dest_initial_defined_path_dyn_computed_with_sensor_monit: ",\
			veh_can_leave_que)
			import sys
			sys.exit()
			
		#if the vehicle cannot leave the que
		else:
			t_end_veh_hold_time=round(self._event_time+v_val_min_veh_hold_time,v_val_prec_round)
			
			#we examine if there are other vehicles in the que
			if v_val_netwk.get_di_entry_internal_links()[self._id_arrival_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
			[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].get_queue_veh()==[]:
				other_veh_in_que_before_add_veh=0
			else:
				other_veh_in_que_before_add_veh=1
				
			#we add the vehicle in the queue
			v_val_netwk.get_di_entry_internal_links()[self._id_arrival_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
			[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].\
			fct_update_veh_queue_when_veh_prohibited_to_leave_no_mod(vehicle)
			
			#we indicate the time at which the vehicle can leave the que regarding the hold duration
			vehicle.set_t_end_veh_hold_time_que(t_end_veh_hold_time)
			
			#if there are no veh in the que (otherwise veh will keave with ev end veh departure) 
			if other_veh_in_que_before_add_veh==0:
					
				#creat ev_end_hold_time
				ev_end_hold_time=Cl_Ev_end_veh_hold_at_que.Ev_end_veh_hold_at_que(val_event_t= t_end_veh_hold_time,\
				val_id_que=queue_phase.get_associated_phase_to_queue())
					
				#we add the event in the event list
				ev_end_hold_time.fct_insertion_even_in_event_list(event_list=v_val_ev_list,\
				message="IN CL_EV_VEH_ARRIVED_AT_QUE IN FUNCT\
				 fct_treat_case_veh_arrival_que_new_demand_final_dest_initial_defined_path_dyn_computed_with_sensor_monit,\
				EVENT END HOLD TIME HAS TIME < TIME FIRST EVENT IN THE LIST")
				
			#if the queue is not a right turn 
			if queue_phase.get_type_veh_queue()!=Cl_Vehicle_Queue.TYPE_VEHICLE_QUEUE["right_turn"]:
			
				#if there is at least one detector detecting the veh
				if queue_phase.fct_exam_whether_at_least_nb_veh_detected_by_a_que_sensor(val_min_nb_veh_to_detect=val_min_nb_vehicles_to_detect)!=None:
				
					
					# controle dec update
					ev_end_deci_next_icm=Cl_Ev_end_decision_next_intersection_control.Ev_end_decision_next_intersection_control(\
					val_ev_time=v_val_ti_ctrl_revision_if_decided,\
					val_id_intersection_node=v_val_netwk.get_di_internal_links_to_network()[self._id_arrival_link].get_id_head_intersection_node(),\
					val_type_control_to_employ=\
					v_val_netwk.get_di_intersections()[v_val_netwk.get_di_internal_links_to_network()[self._id_arrival_link].\
					get_id_head_intersection_node()].get_ctrl_actuate_obj().get_type_employed_ctrl(),\
					val_control_category="sensor_requirement")
					#,val_reason_ctrl_revision_t_lim=0)	
		
					#on insert the event ev_end_dec_next_icm into the event list
					ev_end_deci_next_icm.fct_insertion_even_in_event_list(event_list=v_val_ev_list,\
					message="IN CL_Ev_veh_Arrived_at_quel IN FUNCT, \
					fct_treat_case_veh_arrival_que_new_demand_final_dest_initial_defined_path_dyn_computed_with_sensor_monit\
					NEXT ev_new_end_dec_netw_control EVENT HAS TIME < TIME FIRST EVENT IN THE LIST")
				
					#we indicate the intersection that a ctrl request is made
					#v_val_netwk.get_di_intersections()[v_val_netwk.get_di_internal_links_to_network()[self._id_arrival_link].get_id_head_intersection_node()].\
					#set_t_last_request_ctrl_revision_when_flux_monitoring(v_val_ti_ctrl_revision_if_decided)
						
					#we indicate the number of times a control revision is asked for the same time
					#v_val_netwk.get_di_intersections()[v_val_netwk.get_di_internal_links_to_network()[self._id_arrival_link].get_id_head_intersection_node()].\
					#set_nb_times_ctrl_revision_corresponding_to_t_last_request_ctrl_revision_when_flux_monitoring(\
					#v_val_netwk.get_di_intersections()[v_val_netwk.get_di_internal_links_to_network()[self._id_arrival_link].get_id_head_intersection_node()].\
					#set_nb_times_ctrl_revision_corresponding_to_t_last_request_ctrl_revision_when_flux_monitoring()+1)
		
		li_id_veh=[]
		#print("queue_phase.get_associated_phase_to_queue()",queue_phase.get_associated_phase_to_queue())
		for i in v_val_netwk.get_di_entry_internal_links()[self._id_arrival_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].get_queue_veh():
			li_id_veh.append(i.get_id_veh())
				
		#we create an record database object 
		record_db_obj=Cl_Record_Database.Record_Database(\
		val_file_db=v_file_recording_event_db,\
		val_ev_time=self._event_time,\
		val_ev_type=self._event_type,\
		val_id_inters_node=[v_val_netwk.get_di_entry_internal_links()[\
		queue_phase.get_associated_phase_to_queue()[0]].get_id_head_intersection_node()],\
		val_t_start_current_inters_control=v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_internal_links()[\
		queue_phase.get_associated_phase_to_queue()[0]].\
		get_id_head_intersection_node()].get_intersection_control_obj().get_t_start_control(),\
		val_duration_current_inters_control=v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_internal_links()[\
		queue_phase.get_associated_phase_to_queue()[0]].\
		get_id_head_intersection_node()].get_intersection_control_obj().get_duration_control(),\
		val_current_inters_matrix_with_the_associated_link_of_phase=\
		v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_internal_links()[\
		queue_phase.get_associated_phase_to_queue()[0]].get_id_head_intersection_node()].\
		get_intersection_control_obj().\
		get_di_intersection_control_mat(),\
		val_duration_current_cycle=v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_internal_links()[\
		queue_phase.get_associated_phase_to_queue()[0]].\
		get_id_head_intersection_node()].get_intersection_control_obj().\
		get_cycle_duration_associated_with_control(),\
		val_vehicle_id=vehicle.get_id_veh(),\
		val_time_veh_appearance_in_network=vehicle.get_t_veh_appearance_at_network(),\
		val_id_veh_entry_link=vehicle.get_id_entry_link_veh_ap(),\
		val_id_current_link_veh_location=vehicle.get_current_id_link_veh_location(),\
		val_time_veh_arrival_at_current_link=vehicle.get_t_vehicle_arrival_at_current_link(),\
		val_time_veh_departure_from_current_link=vehicle.get_t_vehicle_departure_from_current_link(),\
		val_veh_current_queue_location=vehicle.get_veh_current_queue_location(),\
		val_time_veh_arrival_at_current_queue=vehicle.get_t_vehicle_arrival_at_current_queue(),\
		val_time_veh_start_departure_from_current_queue=vehicle.get_t_vehicle_started_departure_from_current_queue(),\
		val_time_veh_departure_from_current_queue=vehicle.get_t_vehicle_departure_from_current_queue(),\
		val_veh_id_destination_link=vehicle.get_veh_current_queue_location()[List_Explicit_Values.val_second_element_of_list],\
		val_time_veh_exit_from_network=vehicle.get_t_exit_veh_from_network(),\
		val_id_event_link=self._id_arrival_link,\
		val_veh_can_leave_now=veh_can_leave_que,\
		val_current_achieved_queue_service_rate_including_current_vehicle=\
		v_val_netwk.get_di_entry_internal_links()[self._id_arrival_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].\
		get_current_reached_service_rate(),\
		val_current_queue_service_rate=\
		v_val_netwk.get_di_entry_internal_links()[self._id_arrival_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].\
		get_current_queue_service_rate(),\
		val_li_id_vehicles_in_queue=li_id_veh,\
		val_nb_veh_in_ar_lk=v_val_netwk.get_di_all_links()[i.get_current_id_link_veh_location()].get_current_nb_veh_link())
				
		#we record the event in the db 
		record_db_obj.fct_write_object_in_db_file()

#*****************************************************************************************************************************************************************************************

#************************************************************Case New Demand-with OD and dyn computed path*****************************************************************
	#method treat the case when a new demand is employed, with OD anf dyn computed final destination
	def fct_treat_case_veh_ar_at_que_when_new_demand_given_final_dest_and_dyn_computed_path(self, val_netwk,val_min_veh_hold_time,val_prec_round,\
	val_ev_list,val_file_recording_event_db,\
	val_fct_calc_queue_id_when_given_final_dest_and_path_dynam_constructed,val_min_nb_vehicles_to_detect):
	
		#if the employed control requires sensor record for th t update
		if val_netwk.get_di_intersections()[val_netwk.get_di_entry_internal_links()\
		[self._id_arrival_link].get_id_head_intersection_node()].get_intersection_control_obj().get_type_control_related_to_t_revision()==\
		Cl_Control_Actuate.TYPE_CONTROL_T_REVISION_CATEGORY["sensor_requirement_for_t_update"]:
		
			val_ti_ctrl_revision_if_decided=self._obj_decisions.fct_calculate_t_ctrl_revision(t_cur=self._event_time,dur=\
			val_netwk.get_di_intersections()[val_netwk.get_di_entry_internal_links()\
			[self._id_arrival_link].get_id_head_intersection_node()].get_intersection_control_obj().\
			get_t_duration_for_defining_t_ctrl_revision_when_at_given_time_sensor_records_veh_variation())
		
			for i in self._li_vehicle:
			
				self.fct_treat_case_veh_arrival_que_new_demand_final_dest_initial_defined_path_dyn_computed_with_sensor_monit(\
				vehicle=i,v_val_netwk=val_netwk,v_val_min_veh_hold_time=val_min_veh_hold_time,v_val_prec_round=val_prec_round,\
				v_val_ev_list=val_ev_list,v_file_recording_event_db=val_file_recording_event_db,\
				v_val_ti_ctrl_revision_if_decided=val_ti_ctrl_revision_if_decided,\
				v_val_fct_calc_queue_id_when_given_final_dest_and_path_dynam_constructed=val_fct_calc_queue_id_when_given_final_dest_and_path_dynam_constructed,\
				val_min_nb_vehicles_to_detect=val_min_nb_veh_to_detect)
		
		
		
		#if the employed control does not require sensor monitor for the t update
		elif val_netwk.get_di_intersections()[val_netwk.get_di_entry_internal_links()\
		[self._id_arrival_link].get_id_head_intersection_node()].get_intersection_control_obj().get_type_control_related_to_t_revision()==\
		Cl_Control_Actuate.TYPE_CONTROL_T_REVISION_CATEGORY["without_sensor_requirement_for_t_update"]:
		
			for i in self._li_vehicle:
		
				self.fct_treat_case_veh_arrival_que_new_demand_final_dest_initial_defined_path_dyn_computed_without_sensor_monit(\
				vehicle=i,v_val_netwk=val_netwk,\
				v_val_min_veh_hold_time=val_min_veh_hold_time,v_val_prec_round=val_prec_round,v_val_ev_list=val_ev_list,\
				v_file_recording_event_db=val_file_recording_event_db,\
				v_val_fct_calc_queue_id_when_given_final_dest_and_path_dynam_constructed=val_fct_calc_queue_id_when_given_final_dest_and_path_dynam_constructed)
		
		#if none of the rpevious cases for the t update of the control
		else:
			print("PROBLEM IN CL_EV_VEH_AR, FCT fct_treat_case_veh_ar_at_que_when_new_demand_given_final_dest_and_dyn_computed_path ",\
			val_netwk.get_di_intersections()[val_netwk.get_di_entry_internal_links()\
			[self._id_arrival_link].get_id_head_intersection_node()].get_intersection_control_obj().get_type_control_related_to_t_revision())
			import sys
			sys.exit()

#*****************************************************************************************************************************************************************************************

#****************************************************Cas New demand - mixed management*************************************************************************************
	#method treating the case when a new demand is consired and a mixed routing management is employed 
	def fct_treat_case_veh_ar_at_que_new_demand_mixed_management_dyn_defined_path_or_initial_given_path(self,\
	v_val_netwk,v_val_min_veh_hold_time,v_val_prec_round,v_val_ev_list,\
	v_val_file_recording_event_db,v_val_min_nb_veh_to_detect):
		
		#if a dynam routing is employed for the vehicle 
		if self._li_vehicle[0].get_type_vehicle_rout_when_mixed_manag()==-1:
		
			self.fct_treat_case_veh_ar_at_que_when_new_demand_final_dest_and_path_dynam_defined(\
			val_netwk=v_val_netwk,val_min_veh_hold_time=v_val_min_veh_hold_time,val_prec_round=v_val_prec_round,\
			val_ev_list=v_val_ev_list,val_file_recording_event_db=v_val_file_recording_event_db,val_min_nb_veh_to_detect=v_val_min_nb_veh_to_detect)
			
		#if an OD and initially given path is employed for the vehicle
		elif self._li_vehicle[0].get_type_vehicle_rout_when_mixed_manag()==Cl_Vehicle.TYPE_VEH_ROUT_WHEN_MIXED_MANAGEMENT["od_and_initially_given_path"]:
		
			self.fct_treat_case_veh_ar_at_que_when_new_demand_final_dest_and_path_given(\
			val_netwk=v_val_netwk,val_min_veh_hold_time=v_val_min_veh_hold_time,val_prec_round=v_val_prec_round,val_ev_list=v_val_ev_list,\
			val_file_recording_event_db=v_val_file_recording_event_db,val_min_nb_veh_to_detect=v_val_min_nb_veh_to_detect)
		
		
		#if an OD and dynamical constructed path is employed for the vehicle
		#elif self._li_vehicle[0].get_type_vehicle_rout_when_mixed_manag()==Cl_Vehicle.TYPE_VEH_ROUT_WHEN_MIXED_MANAGEMENT["od_and_dynam_constructed_path"]:
		
			#self.fct_treat_case_veh_ar_at_que_when_new_demand_given_final_dest_and_dyn_computed_path(\
			#val_netwk=v_val_netwk,val_min_veh_hold_time=v_val_min_veh_hold_time,val_prec_round=v_val_prec_round,\
			#val_ev_list=v_val_ev_list,val_file_recording_event_db=v_val_file_recording_event_db,\
			#val_fct_calc_queue_id_when_given_final_dest_and_path_dynam_constructed=v_val_fct_calc_queue_id_when_given_final_dest_and_path_dynam_constructed,\
			#val_min_nb_vehicles_to_detect=v_val_min_nb_veh_to_detect)
		
		#if none of the previous cases is employed
		else:
			print("PROBLEM IN CL_EV_VEH_ARRIVED_AT_QUE, FCT fct_treat_case_veh_ar_at_que_new_demand_mixed_management,ROUTING TYPE EMPLOYED BY VEH:",self._li_vehicle[0].get_type_vehicle_rout_when_mixed_manag())
			import sys
			sys.exit()

#*****************************************************************************************************************************************************************************************
	
#*****************************************************************Cas Previous Demand-no OD-without sensor monit *************************************************************
	#method treating the case when a vehicle arrives at a que, a previously generated demand is empoyed,
	# final destination and path were dyn defined in the empoyed demand, 
	#the utilised control does not require  sensor monitoring for the t at which is should  be revised 
	def fct_treat_case_veh_arrival_previous_demand_final_dest_and_path_dyn_defined_without_sensor_monit(self,\
	vehicle,v_val_netwk,v_val_dict_vehicle_info_prev_sim,v_val_min_veh_hold_time,v_val_prec_round,v_val_ev_list,v_file_recording_event_db):
	
		#if in the previous sim we have generated as many vehicle destinations
		if len(v_val_dict_vehicle_info_prev_sim[vehicle.get_id_veh()][1]) != List_Explicit_Values.initialisation_value_to_one:
			
			#the vehicle queue  object chosen for the vehicle to join in
			queue_phase=v_val_netwk.get_di_entry_internal_links()[v_val_dict_vehicle_info_prev_sim[vehicle.get_id_veh()][1][0]].\
			get_set_veh_queue().get_di_obj_veh_queue_at_link()[v_val_dict_vehicle_info_prev_sim[vehicle.get_id_veh()][1][0],\
			v_val_dict_vehicle_info_prev_sim[vehicle.get_id_veh()][1][1]]
				
			#we delete the first link location from the veh dictionary 
			#print("HERE",dict_veh_info_prev_sim[val_vehicle.get_id_veh()][1])
			v_val_dict_vehicle_info_prev_sim[vehicle.get_id_veh()][1].remove(v_val_dict_vehicle_info_prev_sim[vehicle.get_id_veh()][1][0])
			
		#if in the previous sim we have not generated as many vehicle destinations
		else:
			#we calculate the que chosen by the vehicle (dyn choice of the destin)
			lis_param_fct_calcul_queue_chosen_by_veh_from_cum_fct=[self._id_arrival_link,\
			v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_internal_links()[self._id_arrival_link].\
			get_id_head_intersection_node()].get_current_di_cum_rout_prob()]
			
			#rep=[[ random uniform nb, id veh lk location, id dest lk]]
			rep=self._obj_decisions.fct_calcul_queue_chosen_by_veh_from_cum_fct(\
			*lis_param_fct_calcul_queue_chosen_by_veh_from_cum_fct)
			
			lis_param_fct_calcul_queue_chosen_by_veh=[self._id_arrival_link,\
			rep[List_Explicit_Values.val_third_element_of_list],v_val_netwk]
				
			queue_phase=self._obj_decisions.fct_calcul_queue_chosen_by_veh(*lis_param_fct_calcul_queue_chosen_by_veh)
			
		#we update the vehicle, we indicate the chosen queue and its arrival time in the queue
		vehicle.fct_update_veh_after_choosing_queue(queue_phase,self._event_time,v_val_netwk)
				
		#we examine if vehicle can leave the queue immediately
		veh_can_leave_que=self._obj_decisions.fct_defining_whether_veh_can_leave_que_by_its_arrival()
			
		#if the vehicle can leave the que
		if veh_can_leave_que==List_Explicit_Values.initialisation_value_to_one:
					
			print("PROBLEM IN CL_Ev_veh_arrived_at_que , in fct fct_treat_case_veh_arrival_previous_demand_final_dest_and_path_dyn_defined_without_sensor_monit\
			veh_can_leave_que by its arrival: ",veh_can_leave_que)
			import sys
			sys.exit()
			
		#if the vehicle can not leave the que
		else:
			t_end_veh_hold_time=round(self._event_time+v_val_min_veh_hold_time,v_val_prec_round)
				
			#we examine if there are other vehicles in the que
			if v_val_netwk.get_di_entry_internal_links()[self._id_arrival_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
			[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].get_queue_veh()==[]:
				other_veh_in_que_before_add_veh=0
			else:
				other_veh_in_que_before_add_veh=1
				
			#we add the vehicle in the queue
			v_val_netwk.get_di_entry_internal_links()[self._id_arrival_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
			[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].\
			fct_update_veh_queue_when_veh_prohibited_to_leave_no_mod(vehicle)
				
			#we indicate the time at which the vehicle can leave the que regarding the hold duration
			vehicle.set_t_end_veh_hold_time_que(t_end_veh_hold_time)
			
			#if there are no veh in the que (otherwise veh will keave with ev end veh departure) 
			if other_veh_in_que_before_add_veh==0:
			
				#creat ev_end_hold_time
				ev_end_hold_time=Cl_Ev_end_veh_hold_at_que.Ev_end_veh_hold_at_que(val_event_t= t_end_veh_hold_time,\
				val_id_que=queue_phase.get_associated_phase_to_queue())
					
				#we add the event in the event list
				ev_end_hold_time.fct_insertion_even_in_event_list(event_list=v_val_ev_list,\
				message="IN CL_EV_VEH_ARRIVED_AT_QUE IN FUNCT \
				fct_treat_case_veh_arrival_previous_demand_final_dest_and_path_dyn_defined_without_sensor_monit,\
				EVENT END HOLD TIME HAS TIME < TIME FIRST EVENT IN THE LIST")
			
		li_id_veh=[]
		for i in v_val_netwk.get_di_entry_internal_links()[self._id_arrival_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[queue_phase.get_associated_phase_to_queue()[0],\
		queue_phase.get_associated_phase_to_queue()[1]].get_queue_veh():
					
			li_id_veh.append(i.get_id_veh())
				
		#we create an record database object 
		record_db_obj=Cl_Record_Database.Record_Database(\
		val_file_db=v_file_recording_event_db,\
		val_ev_time=self._event_time,\
		val_ev_type=self._event_type,\
		val_id_inters_node=[v_val_netwk.get_di_entry_internal_links()[\
		queue_phase.get_associated_phase_to_queue()[0]].get_id_head_intersection_node()],\
		val_t_start_current_inters_control=v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_internal_links()[\
		queue_phase.get_associated_phase_to_queue()[0]].\
		get_id_head_intersection_node()].get_intersection_control_obj().get_t_start_control(),\
		val_duration_current_inters_control=v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_internal_links()[\
		queue_phase.get_associated_phase_to_queue()[0]].\
		get_id_head_intersection_node()].get_intersection_control_obj().get_duration_control(),\
		val_current_inters_matrix_with_the_associated_link_of_phase=\
		v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_internal_links()[\
		queue_phase.get_associated_phase_to_queue()[0]].get_id_head_intersection_node()].\
		get_intersection_control_obj().\
		get_di_intersection_control_mat(),\
		val_duration_current_cycle=v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_internal_links()[\
		queue_phase.get_associated_phase_to_queue()[0]].\
		get_id_head_intersection_node()].get_intersection_control_obj().\
		get_cycle_duration_associated_with_control(),\
		val_vehicle_id=vehicle.get_id_veh(),\
		val_time_veh_appearance_in_network=vehicle.get_t_veh_appearance_at_network(),\
		val_id_veh_entry_link=vehicle.get_id_entry_link_veh_ap(),\
		val_id_current_link_veh_location=vehicle.get_current_id_link_veh_location(),\
		val_time_veh_arrival_at_current_link=vehicle.get_t_vehicle_arrival_at_current_link(),\
		val_time_veh_departure_from_current_link=vehicle.get_t_vehicle_departure_from_current_link(),\
		val_veh_current_queue_location=vehicle.get_veh_current_queue_location(),\
		val_time_veh_arrival_at_current_queue=vehicle.get_t_vehicle_arrival_at_current_queue(),\
		val_time_veh_start_departure_from_current_queue=vehicle.get_t_vehicle_started_departure_from_current_queue(),\
		val_time_veh_departure_from_current_queue=vehicle.get_t_vehicle_departure_from_current_queue(),\
		val_veh_id_destination_link=vehicle.get_veh_current_queue_location()[List_Explicit_Values.val_second_element_of_list],\
		val_time_veh_exit_from_network=vehicle.get_t_exit_veh_from_network(),\
		val_id_event_link=self._id_arrival_link,\
		val_veh_can_leave_now=veh_can_leave_que,\
		val_current_achieved_queue_service_rate_including_current_vehicle=\
		v_val_netwk.get_di_entry_internal_links()[self._id_arrival_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].\
		get_current_reached_service_rate(),\
		val_current_queue_service_rate=\
		v_val_netwk.get_di_entry_internal_links()[self._id_arrival_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].\
		get_current_queue_service_rate(),\
		val_li_id_vehicles_in_queue=li_id_veh,\
		val_nb_veh_in_ar_lk=v_val_netwk.get_di_all_links()[i.get_current_id_link_veh_location()].get_current_nb_veh_link())
		#val_prob_rout_prop_current_lk=val_netwk.get_dict_mat_od_key_id_entry_internal_lk_value_list_dest_lks()[\
		#queue_phase.get_associated_phase_to_queue()[0]])		
					
		#we record the event in the db 
		record_db_obj.fct_write_object_in_db_file()
#*****************************************************************************************************************************************************************************************

#***************************************************Cas Previous Demand-no OD-with sensor monit *******************************************************************************
	#method treating the case when a vehicle arrives at a que, a previously generated demand is empoyed,
	# final destination and path were dyn defined in the empoyed demand, 
	#the utilised control  requires  sensor monitoring for the t at which is should  be revised 
	def fct_treat_case_veh_arrival_previous_demand_final_dest_and_path_dyn_defined_with_sensor_monit(self,\
	vehicle,v_val_netwk,v_val_dict_vehicle_info_prev_sim,v_val_min_veh_hold_time,v_val_prec_round,v_val_ev_list,\
	v_file_recording_event_db,v_val_ti_ctrl_revision_if_decided,\
	val_min_nb_vehicles_to_detect):
	
		#if in the previous sim we have generated as many vehicle destinations
		if len(v_val_dict_vehicle_info_prev_sim[vehicle.get_id_veh()][1]) != List_Explicit_Values.initialisation_value_to_one:
			
			#the vehicle queue  object chosen for the vehicle to join in
			queue_phase=v_val_netwk.get_di_entry_internal_links()[v_val_dict_vehicle_info_prev_sim[vehicle.get_id_veh()][1][0]].\
			get_set_veh_queue().get_di_obj_veh_queue_at_link()[v_val_dict_vehicle_info_prev_sim[vehicle.get_id_veh()][1][0],\
			v_val_dict_vehicle_info_prev_sim[vehicle.get_id_veh()][1][1]]
				
			#we delete the first link location from the veh dictionary 
			#print("HERE",dict_veh_info_prev_sim[val_vehicle.get_id_veh()][1])
			v_val_dict_vehicle_info_prev_sim[vehicle.get_id_veh()][1].remove(v_val_dict_vehicle_info_prev_sim[vehicle.get_id_veh()][1][0])
			
		#if in the previous sim we have not generated as many vehicle destinations
		else:
			#we calculate the que chosen by the vehicle (next destination dynam defined-no final destination)
			lis_param_fct_calcul_queue_chosen_by_veh_from_cum_fct=[self._id_arrival_link,\
			v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_internal_links()[self._id_arrival_link].\
			get_id_head_intersection_node()].get_current_di_cum_rout_prob()]
			
			#rep=[[ random uniform nb, id veh lk location, id dest lk]]
			rep=self._obj_decisions.fct_calcul_queue_chosen_by_veh_from_cum_fct(\
			*lis_param_fct_calcul_queue_chosen_by_veh_from_cum_fct)
			
			lis_param_fct_calcul_queue_chosen_by_veh=[self._id_arrival_link,\
			rep[List_Explicit_Values.val_third_element_of_list],v_val_netwk]
				
			queue_phase=self._obj_decisions.fct_calcul_queue_chosen_by_veh(*lis_param_fct_calcul_queue_chosen_by_veh)
			
		#we update the vehicle, we indicate the chosen queue and its arrival time in the queue
		vehicle.fct_update_veh_after_choosing_queue(queue_phase,self._event_time,v_val_netwk)
				
		#we examine if vehicle can leave the queue immediately
		veh_can_leave_que=self._obj_decisions.fct_defining_whether_veh_can_leave_que_by_its_arrival()
			
		#if the vehicle can leave the que
		if veh_can_leave_que==List_Explicit_Values.initialisation_value_to_one:
					
			print("PROBLEM IN CL_Ev_veh_arrived_at_que in fct: \
			fct_treat_case_veh_arrival_previous_demand_final_dest_and_path_dyn_defined_with_sensor_monit,\
			veh_can_leave_que,veh_can_leave_que")
			import sys
			sys.exit()
			
		#if the vehicle can not leave the que
		else:
			t_end_veh_hold_time=round(self._event_time+v_val_min_veh_hold_time,v_val_prec_round)
				
			#we examine if there are other vehicles in the que
			if v_val_netwk.get_di_entry_internal_links()[self._id_arrival_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
			[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].get_queue_veh()==[]:
				other_veh_in_que_before_add_veh=0
			else:
				other_veh_in_que_before_add_veh=1
				
			#we add the vehicle in the queue
			v_val_netwk.get_di_entry_internal_links()[self._id_arrival_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
			[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].\
			fct_update_veh_queue_when_veh_prohibited_to_leave_no_mod(vehicle)
				
			#we indicate the time at which the vehicle can leave the que regarding the hold duration
			vehicle.set_t_end_veh_hold_time_que(t_end_veh_hold_time)
			
			#if there are no veh in the que (otherwise veh will keave with ev end veh departure) 
			if other_veh_in_que_before_add_veh==0:
			
				#creat ev_end_hold_time
				ev_end_hold_time=Cl_Ev_end_veh_hold_at_que.Ev_end_veh_hold_at_que(val_event_t= t_end_veh_hold_time,\
				val_id_que=queue_phase.get_associated_phase_to_queue())
					
				#we add the event in the event list
				ev_end_hold_time.fct_insertion_even_in_event_list(event_list=v_val_ev_list,\
				message="IN CL_EV_VEH_ARRIVED_AT_QUE IN FUNCT \
				fct_treat_case_veh_arrival_previous_demand_final_dest_and_path_dyn_defined_with_sensor_monit,\
				EVENT END HOLD TIME HAS TIME < TIME FIRST EVENT IN THE LIST")
				
			#if the queue is not a right turn 
			if queue_phase.get_type_veh_queue()!=Cl_Vehicle_Queue.TYPE_VEHICLE_QUEUE["right_turn"]:
			
				#if there is at least one detector detecting the veh
				if queue_phase.fct_exam_whether_at_least_nb_veh_detected_by_a_que_sensor(val_min_nb_veh_to_detect=val_min_nb_vehicles_to_detect)!=None:
				
														
					# controle dec update
					ev_end_deci_next_icm=Cl_Ev_end_decision_next_intersection_control.Ev_end_decision_next_intersection_control(\
					val_ev_time=v_val_ti_ctrl_revision_if_decided,\
					val_id_intersection_node=v_val_netwk.get_di_internal_links_to_network()[self._id_arrival_link].get_id_head_intersection_node(),\
					val_type_control_to_employ=\
					v_val_netwk.get_di_intersections()[v_val_netwk.get_di_internal_links_to_network()[self._id_arrival_link].\
					get_id_head_intersection_node()].get_ctrl_actuate_obj().get_type_employed_ctrl(),\
					val_control_category="sensor_requirement")
					#,val_reason_ctrl_revision_t_lim=0)	
		
					#on insert the event ev_end_dec_next_icm into the event list
					ev_end_deci_next_icm.fct_insertion_even_in_event_list(event_list=v_val_ev_list,\
					message="IN CL_Ev_veh_Arrived_at_quel IN FUNCT, \
					fct_treat_case_veh_arrival_previous_demand_final_dest_and_path_dyn_defined_with_sensor_monit,\
					NEXT ev_new_end_dec_netw_control EVENT HAS TIME < TIME FIRST EVENT IN THE LIST")
				
					#we indicate the intersection that a ctrl request is made
					#v_val_netwk.get_di_intersections()[v_val_netwk.get_di_internal_links_to_network()[self._id_arrival_link].get_id_head_intersection_node()].\
					#set_t_last_request_ctrl_revision_when_flux_monitoring(v_val_ti_ctrl_revision_if_decided)
						
					#we indicate the number of times a control revision is asked for the same time
					#v_val_netwk.get_di_intersections()[v_val_netwk.get_di_internal_links_to_network()[self._id_arrival_link].get_id_head_intersection_node()].\
					#set_nb_times_ctrl_revision_corresponding_to_t_last_request_ctrl_revision_when_flux_monitoring(\
					#v_val_netwk.get_di_intersections()[v_val_netwk.get_di_internal_links_to_network()[self._id_arrival_link].get_id_head_intersection_node()].\
					#set_nb_times_ctrl_revision_corresponding_to_t_last_request_ctrl_revision_when_flux_monitoring()+1)
				
		li_id_veh=[]
		for i in v_val_netwk.get_di_entry_internal_links()[self._id_arrival_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[queue_phase.get_associated_phase_to_queue()[0],\
		queue_phase.get_associated_phase_to_queue()[1]].get_queue_veh():
					
			li_id_veh.append(i.get_id_veh())
				
		#we create an record database object 
		record_db_obj=Cl_Record_Database.Record_Database(\
		val_file_db=v_file_recording_event_db,\
		val_ev_time=self._event_time,\
		val_ev_type=self._event_type,\
		val_id_inters_node=[v_val_netwk.get_di_entry_internal_links()[\
		queue_phase.get_associated_phase_to_queue()[0]].get_id_head_intersection_node()],\
		val_t_start_current_inters_control=v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_internal_links()[\
		queue_phase.get_associated_phase_to_queue()[0]].\
		get_id_head_intersection_node()].get_intersection_control_obj().get_t_start_control(),\
		val_duration_current_inters_control=v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_internal_links()[\
		queue_phase.get_associated_phase_to_queue()[0]].\
		get_id_head_intersection_node()].get_intersection_control_obj().get_duration_control(),\
		val_current_inters_matrix_with_the_associated_link_of_phase=\
		v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_internal_links()[\
		queue_phase.get_associated_phase_to_queue()[0]].get_id_head_intersection_node()].\
		get_intersection_control_obj().\
		get_di_intersection_control_mat(),\
		val_duration_current_cycle=v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_internal_links()[\
		queue_phase.get_associated_phase_to_queue()[0]].\
		get_id_head_intersection_node()].get_intersection_control_obj().\
		get_cycle_duration_associated_with_control(),\
		val_vehicle_id=vehicle.get_id_veh(),\
		val_time_veh_appearance_in_network=vehicle.get_t_veh_appearance_at_network(),\
		val_id_veh_entry_link=vehicle.get_id_entry_link_veh_ap(),\
		val_id_current_link_veh_location=vehicle.get_current_id_link_veh_location(),\
		val_time_veh_arrival_at_current_link=vehicle.get_t_vehicle_arrival_at_current_link(),\
		val_time_veh_departure_from_current_link=vehicle.get_t_vehicle_departure_from_current_link(),\
		val_veh_current_queue_location=vehicle.get_veh_current_queue_location(),\
		val_time_veh_arrival_at_current_queue=vehicle.get_t_vehicle_arrival_at_current_queue(),\
		val_time_veh_start_departure_from_current_queue=vehicle.get_t_vehicle_started_departure_from_current_queue(),\
		val_time_veh_departure_from_current_queue=vehicle.get_t_vehicle_departure_from_current_queue(),\
		val_veh_id_destination_link=vehicle.get_veh_current_queue_location()[List_Explicit_Values.val_second_element_of_list],\
		val_time_veh_exit_from_network=vehicle.get_t_exit_veh_from_network(),\
		val_id_event_link=self._id_arrival_link,\
		val_veh_can_leave_now=veh_can_leave_que,\
		val_current_achieved_queue_service_rate_including_current_vehicle=\
		v_val_netwk.get_di_entry_internal_links()[self._id_arrival_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].\
		get_current_reached_service_rate(),\
		val_current_queue_service_rate=\
		v_val_netwk.get_di_entry_internal_links()[self._id_arrival_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].\
		get_current_queue_service_rate(),\
		val_li_id_vehicles_in_queue=li_id_veh,\
		val_nb_veh_in_ar_lk=v_val_netwk.get_di_all_links()[i.get_current_id_link_veh_location()].get_current_nb_veh_link())
		#val_prob_rout_prop_current_lk=val_netwk.get_dict_mat_od_key_id_entry_internal_lk_value_list_dest_lks()[\
		#queue_phase.get_associated_phase_to_queue()[0]])	
						
		#we record the event in the db 
		record_db_obj.fct_write_object_in_db_file()
#*****************************************************************************************************************************************************************************************
#****************************************************Previous demand - No OD*******************************************************************************************************
	#method treating the case when a previous demand is employed- without OD
	def fct_treat_case_veh_ar_at_que_when_previous_demand_final_dest_and_dyn_computed(self,val_netwk,val_dict_vehicle_info_prev_sim,\
	val_min_veh_hold_time,val_prec_round,val_ev_list,val_file_recording_event_db,val_min_nb_veh_to_detect):
		#if the control requires sensor monitor for the t update
		if val_netwk.get_di_intersections()[val_netwk.get_di_entry_internal_links()\
		[self._id_arrival_link].get_id_head_intersection_node()].get_intersection_control_obj().get_type_control_related_to_t_revision()==\
		Cl_Control_Actuate.TYPE_CONTROL_T_REVISION_CATEGORY["sensor_requirement_for_t_update"]:
		
			val_ti_ctrl_revision_if_decided=self._obj_decisions.fct_calculate_t_ctrl_revision(t_cur=self._event_time,dur=\
			val_netwk.get_di_intersections()[val_netwk.get_di_entry_internal_links()\
			[self._id_arrival_link].get_id_head_intersection_node()].get_intersection_control_obj().\
			get_t_duration_for_defining_t_ctrl_revision_when_at_given_time_sensor_records_veh_variation())
			
			for i in self._li_vehicle:
		
				self.fct_treat_case_veh_arrival_previous_demand_final_dest_and_path_dyn_defined_with_sensor_monit(\
				vehicle=i,v_val_netwk=val_netwk,v_val_dict_vehicle_info_prev_sim=val_dict_vehicle_info_prev_sim,v_val_min_veh_hold_time=val_min_veh_hold_time,\
				v_val_prec_round=val_prec_round,v_val_ev_list=val_ev_list,\
				v_file_recording_event_db=val_file_recording_event_db,v_val_ti_ctrl_revision_if_decided=val_ti_ctrl_revision_if_decided,\
				val_min_nb_vehicles_to_detect=val_min_nb_veh_to_detect)
		
		#if the cotnrol does not require sensor monitor for the t update
		elif val_netwk.get_di_intersections()[val_netwk.get_di_entry_internal_links()\
		[self._id_arrival_link].get_id_head_intersection_node()].get_intersection_control_obj().get_type_control_related_to_t_revision()==\
		Cl_Control_Actuate.TYPE_CONTROL_T_REVISION_CATEGORY["without_sensor_requirement_for_t_update"]:
		
			for i in self._li_vehicle:
		
				self.fct_treat_case_veh_arrival_previous_demand_final_dest_and_path_dyn_defined_without_sensor_monit(\
				vehicle=i,v_val_netwk=val_netwk,v_val_dict_vehicle_info_prev_sim=val_dict_vehicle_info_prev_sim,\
				v_val_min_veh_hold_time=val_min_nb_veh_to_detect,v_val_prec_round=val_prec_round,v_val_ev_list=val_ev_list,\
				v_file_recording_event_db=val_file_recording_event_db)
	
		#if none of the rpevious cases for the t update of the control
		else:
			print("PROBLEM IN CL_EV_VEH_AR, FCT fct_treat_case_veh_ar_at_que_when_previous_demand_final_dest_and_dyn_computed ",\
			val_netwk.get_di_intersections()[val_netwk.get_di_entry_internal_links()\
			[self._id_arrival_link].get_id_head_intersection_node()].get_intersection_control_obj().get_type_control_related_to_t_revision())
			import sys
			sys.exit()

#*****************************************************************************************************************************************************************************************

#***************************************************Cas Previous Demand-with OD given path-without sensor monit *************************************************************
	#method treating the case when a vehicle arrives at a que, a previously generated demand is empoyed,
	# final destination and path were given in the empoyed demand, 
	#the utilised control  does not require  sensor monitoring for the t at which is should  be revised 
	def fct_treat_case_veh_arrival_previous_demand_final_dest_and_path_intial_defined_without_sensor_monit(self,\
	vehicle,v_val_netwk,v_val_min_veh_hold_time,v_val_prec_round,v_val_ev_list,v_file_recording_event_db):
	
		#we update the indicator of the veh current location  in the que
		new_v=vehicle.get_index_current_veh_link_location_in_path_list_when_given_destination()+1
					
		vehicle.set_index_current_veh_link_location_in_path_list_when_given_destination(new_v)
		
		#we calculate the que chosen by the vehicle
		li_param_fct_calcul_que_chosen_by_veh=[\
		vehicle.get_id_entry_link_veh_ap(),self._id_arrival_link,\
		vehicle.get_id_veh_final_destination_link(),\
		vehicle.get_index_current_veh_link_location_in_path_list_when_given_destination(),\
		v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_internal_links()[vehicle.get_id_entry_link_veh_ap()].\
		get_id_head_intersection_node()].get_current_di_unique_paths(),v_val_netwk]
		
		#the vehicle queue  object chosen for the vehicle to join in
		queue_phase=self._obj_decisions.fct_calcul_queue_chosen_by_veh_cas_given_final_destination(*li_param_fct_calcul_que_chosen_by_veh)
		
		#we update the vehicle, we indicate the chosen queue and its arrival time in the queue
		vehicle.fct_update_veh_after_choosing_queue(queue_phase,self._event_time,v_val_netwk)
		
		#we examine if vehicle can leave the queue immediately
		veh_can_leave_que=self._obj_decisions.fct_defining_whether_veh_can_leave_que_by_its_arrival()
		
		#if the vehicle can leave the que
		if veh_can_leave_que==List_Explicit_Values.initialisation_value_to_one:
			print("PROBLEM IN CL_Ev_veh_arrived_at_que veh_can_leave_que, \
			fct_treat_case_veh_arrival_previous_demand_final_dest_and_path_intial_defined_without_sensor_monit ",veh_can_leave_que)
			import sys
			sys.exit()
		
		#if the vehicle can not leave the que
		else:
			t_end_veh_hold_time=round(self._event_time+v_val_min_veh_hold_time,v_val_prec_round)
			
			#we examine if there are other vehicles in the que
			if v_val_netwk.get_di_entry_internal_links()[self._id_arrival_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
			[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].get_queue_veh()==[]:
				other_veh_in_que_before_add_veh=0
			else:
				other_veh_in_que_before_add_veh=1
				
			#we add the vehicle in the queue
			v_val_netwk.get_di_entry_internal_links()[self._id_arrival_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
			[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].\
			fct_update_veh_queue_when_veh_prohibited_to_leave_with_mod(vehicle)
			
			#we indicate the time at which the vehicle can leave the que regarding the hold duration
			vehicle.set_t_end_veh_hold_time_que(t_end_veh_hold_time)
			
			#if there are no veh in the que (otherwise veh will keave with ev end veh departure) 
			if other_veh_in_que_before_add_veh==0:
			
				#creat ev_end_hold_time
				ev_end_hold_time=Cl_Ev_end_veh_hold_at_que.Ev_end_veh_hold_at_que(val_event_t= t_end_veh_hold_time,\
				val_id_que=queue_phase.get_associated_phase_to_queue())
					
				#we add the event in the event list
				ev_end_hold_time.fct_insertion_even_in_event_list(event_list=v_val_ev_list,\
				message="IN CL_EV_VEH_ARRIVED_AT_QUE IN FUNCT ,\
				fct_treat_case_veh_arrival_previous_demand_final_dest_and_path_intial_defined_without_sensor_monit,\
				EVENT END HOLD TIME HAS TIME < TIME FIRST EVENT IN THE LIST")
		
		li_id_veh=[]
		for i in v_val_netwk.get_di_entry_internal_links()[self._id_arrival_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[queue_phase.get_associated_phase_to_queue()[0],\
		queue_phase.get_associated_phase_to_queue()[1]].get_queue_veh():
					
			li_id_veh.append(i.get_id_veh())
						
		#we create an record database object 
		record_db_obj=Cl_Record_Database.Record_Database(\
		val_file_db=v_file_recording_event_db,\
		val_ev_time=self._event_time,\
		val_ev_type=self._event_type,\
		val_id_inters_node=[v_val_netwk.get_di_entry_internal_links()[\
		queue_phase.get_associated_phase_to_queue()[0]].get_id_head_intersection_node()],\
		val_t_start_current_inters_control=v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_internal_links()[\
		queue_phase.get_associated_phase_to_queue()[0]].\
		get_id_head_intersection_node()].get_intersection_control_obj().get_t_start_control(),\
		val_duration_current_inters_control=v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_internal_links()[\
		queue_phase.get_associated_phase_to_queue()[0]].\
		get_id_head_intersection_node()].get_intersection_control_obj().get_duration_control(),\
		val_current_inters_matrix_with_the_associated_link_of_phase=\
		v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_internal_links()[\
		queue_phase.get_associated_phase_to_queue()[0]].get_id_head_intersection_node()].\
		get_intersection_control_obj().\
		get_di_intersection_control_mat(),\
		val_duration_current_cycle=v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_internal_links()[\
		queue_phase.get_associated_phase_to_queue()[0]].\
		get_id_head_intersection_node()].get_intersection_control_obj().\
		get_cycle_duration_associated_with_control(),\
		val_vehicle_id=vehicle.get_id_veh(),\
		val_time_veh_appearance_in_network=vehicle.get_t_veh_appearance_at_network(),\
		val_id_veh_entry_link=vehicle.get_id_entry_link_veh_ap(),\
		val_id_current_link_veh_location=vehicle.get_current_id_link_veh_location(),\
		val_time_veh_arrival_at_current_link=vehicle.get_t_vehicle_arrival_at_current_link(),\
		val_time_veh_departure_from_current_link=vehicle.get_t_vehicle_departure_from_current_link(),\
		val_veh_current_queue_location=vehicle.get_veh_current_queue_location(),\
		val_time_veh_arrival_at_current_queue=vehicle.get_t_vehicle_arrival_at_current_queue(),\
		val_time_veh_start_departure_from_current_queue=vehicle.get_t_vehicle_started_departure_from_current_queue(),\
		val_time_veh_departure_from_current_queue=vehicle.get_t_vehicle_departure_from_current_queue(),\
		val_veh_id_destination_link=vehicle.get_veh_current_queue_location()[List_Explicit_Values.val_second_element_of_list],\
		val_time_veh_exit_from_network=vehicle.get_t_exit_veh_from_network(),\
		val_id_event_link=self._id_arrival_link,\
		val_veh_can_leave_now=veh_can_leave_que,\
		val_current_achieved_queue_service_rate_including_current_vehicle=\
		v_val_netwk.get_di_entry_internal_links()[self._id_arrival_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].\
		get_current_reached_service_rate(),\
		val_current_queue_service_rate=\
		v_val_netwk.get_di_entry_internal_links()[self._id_arrival_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].\
		get_current_queue_service_rate(),\
		val_li_id_vehicles_in_queue=li_id_veh,\
		val_nb_veh_in_ar_lk=v_val_netwk.get_di_all_links()[i.get_current_id_link_veh_location()].get_current_nb_veh_link())
		#val_prob_rout_prop_current_lk=val_netwk.get_dict_mat_od_key_id_entry_internal_lk_value_list_dest_lks()[\
		#queue_phase.get_associated_phase_to_queue()[0]])					
		#we record the event in the db 
			
		record_db_obj.fct_write_object_in_db_file()
		

#*****************************************************************************************************************************************************************************************
#***************************************************Cas Previous Demand-with OD given path-with sensor monit *****************************************************************
	#method treating the case when a vehicle arrives at a que, a previously generated demand is empoyed,
	# final destination and path were given in the empoyed demand, 
	#the utilised control  requires  sensor monitoring for the t at which is should  be revised 
	def fct_treat_case_veh_arrival_previous_demand_final_dest_and_path_intial_defined_with_sensor_monit(self,\
	vehicle,v_val_netwk,v_val_min_veh_hold_time,v_val_prec_round,v_val_ev_list,v_file_recording_event_db,\
	v_val_ti_ctrl_revision_if_decided,val_min_nb_vehicles_to_detect):
	
		#we update the indicator of the veh current location  in the que
		new_v=vehicle.get_index_current_veh_link_location_in_path_list_when_given_destination()+1
					
		vehicle.set_index_current_veh_link_location_in_path_list_when_given_destination(new_v)
		
		#we calculate the que chosen by the vehicle
		li_param_fct_calcul_que_chosen_by_veh=[\
		vehicle.get_id_entry_link_veh_ap(),self._id_arrival_link,\
		vehicle.get_id_veh_final_destination_link(),\
		vehicle.get_index_current_veh_link_location_in_path_list_when_given_destination(),\
		v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_internal_links()[vehicle.get_id_entry_link_veh_ap()].\
		get_id_head_intersection_node()].get_current_di_unique_paths(),v_val_netwk]
		
		#the vehicle queue  object chosen for the vehicle to join in
		queue_phase=self._obj_decisions.fct_calcul_queue_chosen_by_veh_cas_given_final_destination(*li_param_fct_calcul_que_chosen_by_veh)
		
		#we update the vehicle, we indicate the chosen queue and its arrival time in the queue
		vehicle.fct_update_veh_after_choosing_queue(queue_phase,self._event_time,v_val_netwk)
		
		#we examine if vehicle can leave the queue immediately
		veh_can_leave_que=self._obj_decisions.fct_defining_whether_veh_can_leave_que_by_its_arrival()
		
		#if the vehicle can leave the que
		if veh_can_leave_que==List_Explicit_Values.initialisation_value_to_one:
			print("PROBLEM IN CL_Ev_veh_arrived_at_que veh_can_leave_que, \
			fct_treat_case_veh_arrival_previous_demand_final_dest_and_path_intial_defined_with_sensor_monit: ",veh_can_leave_que)
			import sys
			sys.exit()
		
		#if the vehicle can not leave the que
		else:
			t_end_veh_hold_time=round(self._event_time+v_val_min_veh_hold_time,v_val_prec_round)
			
			#we examine if there are other vehicles in the que
			if v_val_netwk.get_di_entry_internal_links()[self._id_arrival_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
			[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].get_queue_veh()==[]:
				other_veh_in_que_before_add_veh=0
			else:
				other_veh_in_que_before_add_veh=1
				
			#we add the vehicle in the queue
			v_val_netwk.get_di_entry_internal_links()[self._id_arrival_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
			[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].\
			fct_update_veh_queue_when_veh_prohibited_to_leave_with_mod(vehicle)
			
			#we indicate the time at which the vehicle can leave the que regarding the hold duration
			vehicle.set_t_end_veh_hold_time_que(t_end_veh_hold_time)
			
			#if there are no veh in the que (otherwise veh will keave with ev end veh departure) 
			if other_veh_in_que_before_add_veh==0:
			
				#creat ev_end_hold_time
				ev_end_hold_time=Cl_Ev_end_veh_hold_at_que.Ev_end_veh_hold_at_que(val_event_t= t_end_veh_hold_time,\
				val_id_que=queue_phase.get_associated_phase_to_queue())
					
				#we add the event in the event list
				ev_end_hold_time.fct_insertion_even_in_event_list(event_list=v_val_ev_list,\
				message="IN CL_EV_VEH_ARRIVED_AT_QUE IN FUNCT ,\
				fct_treat_case_veh_arrival_previous_demand_final_dest_and_path_intial_defined_with_sensor_monit,\
				EVENT END HOLD TIME HAS TIME < TIME FIRST EVENT IN THE LIST")
				
			#if the queue is not a right turn 
			if queue_phase.get_type_veh_queue()!=Cl_Vehicle_Queue.TYPE_VEHICLE_QUEUE["right_turn"]:
			
				#if there is at least one detector detecting the veh
				if queue_phase.fct_exam_whether_at_least_nb_veh_detected_by_a_que_sensor(val_min_nb_veh_to_detect=val_min_nb_vehicles_to_detect)!=None:
				
					
					# controle dec update
					ev_end_deci_next_icm=Cl_Ev_end_decision_next_intersection_control.Ev_end_decision_next_intersection_control(\
					val_ev_time=v_val_ti_ctrl_revision_if_decided,\
					val_id_intersection_node=v_val_netwk.get_di_internal_links_to_network()[self._id_arrival_link].get_id_head_intersection_node(),\
					val_type_control_to_employ=\
					v_val_netwk.get_di_intersections()[v_val_netwk.get_di_internal_links_to_network()[self._id_arrival_link].\
					get_id_head_intersection_node()].get_ctrl_actuate_obj().get_type_employed_ctrl(),\
					val_control_category="sensor_requirement")
					#,val_reason_ctrl_revision_t_lim=0)	
		
					#on insert the event ev_end_dec_next_icm into the event list
					ev_end_deci_next_icm.fct_insertion_even_in_event_list(event_list=v_val_ev_list,\
					message="IN CL_Ev_veh_Arrived_at_quel IN FUNCT, \
					fct_treat_case_veh_arrival_previous_demand_final_dest_and_path_intial_defined_with_sensor_monit\
					NEXT ev_new_end_dec_netw_control EVENT HAS TIME < TIME FIRST EVENT IN THE LIST")
				
					#we indicate the intersection that a ctrl request is made
					#v_val_netwk.get_di_intersections()[v_val_netwk.get_di_internal_links_to_network()[self._id_arrival_link].get_id_head_intersection_node()].\
					#set_t_last_request_ctrl_revision_when_flux_monitoring(v_val_ti_ctrl_revision_if_decided)
						
					#we indicate the number of times a control revision is asked for the same time
					#v_val_netwk.get_di_intersections()[v_val_netwk.get_di_internal_links_to_network()[self._id_arrival_link].get_id_head_intersection_node()].\
					#set_nb_times_ctrl_revision_corresponding_to_t_last_request_ctrl_revision_when_flux_monitoring(\
					#v_val_netwk.get_di_intersections()[v_val_netwk.get_di_internal_links_to_network()[self._id_arrival_link].get_id_head_intersection_node()].\
					#set_nb_times_ctrl_revision_corresponding_to_t_last_request_ctrl_revision_when_flux_monitoring()+1)
			
		li_id_veh=[]
		for i in v_val_netwk.get_di_entry_internal_links()[self._id_arrival_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[queue_phase.get_associated_phase_to_queue()[0],\
		queue_phase.get_associated_phase_to_queue()[1]].get_queue_veh():
					
			li_id_veh.append(i.get_id_veh())
						
		#we create an record database object 
		record_db_obj=Cl_Record_Database.Record_Database(\
		val_file_db=v_file_recording_event_db,\
		val_ev_time=self._event_time,\
		val_ev_type=self._event_type,\
		val_id_inters_node=[v_val_netwk.get_di_entry_internal_links()[\
		queue_phase.get_associated_phase_to_queue()[0]].get_id_head_intersection_node()],\
		val_t_start_current_inters_control=v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_internal_links()[\
		queue_phase.get_associated_phase_to_queue()[0]].\
		get_id_head_intersection_node()].get_intersection_control_obj().get_t_start_control(),\
		val_duration_current_inters_control=v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_internal_links()[\
		queue_phase.get_associated_phase_to_queue()[0]].\
		get_id_head_intersection_node()].get_intersection_control_obj().get_duration_control(),\
		val_current_inters_matrix_with_the_associated_link_of_phase=\
		v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_internal_links()[\
		queue_phase.get_associated_phase_to_queue()[0]].get_id_head_intersection_node()].\
		get_intersection_control_obj().\
		get_di_intersection_control_mat(),\
		val_duration_current_cycle=v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_internal_links()[\
		queue_phase.get_associated_phase_to_queue()[0]].\
		get_id_head_intersection_node()].get_intersection_control_obj().\
		get_cycle_duration_associated_with_control(),\
		val_vehicle_id=vehicle.get_id_veh(),\
		val_time_veh_appearance_in_network=vehicle.get_t_veh_appearance_at_network(),\
		val_id_veh_entry_link=vehicle.get_id_entry_link_veh_ap(),\
		val_id_current_link_veh_location=vehicle.get_current_id_link_veh_location(),\
		val_time_veh_arrival_at_current_link=vehicle.get_t_vehicle_arrival_at_current_link(),\
		val_time_veh_departure_from_current_link=vehicle.get_t_vehicle_departure_from_current_link(),\
		val_veh_current_queue_location=vehicle.get_veh_current_queue_location(),\
		val_time_veh_arrival_at_current_queue=vehicle.get_t_vehicle_arrival_at_current_queue(),\
		val_time_veh_start_departure_from_current_queue=vehicle.get_t_vehicle_started_departure_from_current_queue(),\
		val_time_veh_departure_from_current_queue=vehicle.get_t_vehicle_departure_from_current_queue(),\
		val_veh_id_destination_link=vehicle.get_veh_current_queue_location()[List_Explicit_Values.val_second_element_of_list],\
		val_time_veh_exit_from_network=vehicle.get_t_exit_veh_from_network(),\
		val_id_event_link=self._id_arrival_link,\
		val_veh_can_leave_now=veh_can_leave_que,\
		val_current_achieved_queue_service_rate_including_current_vehicle=\
		v_val_netwk.get_di_entry_internal_links()[self._id_arrival_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].\
		get_current_reached_service_rate(),\
		val_current_queue_service_rate=\
		v_val_netwk.get_di_entry_internal_links()[self._id_arrival_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].\
		get_current_queue_service_rate(),\
		val_li_id_vehicles_in_queue=li_id_veh,\
		val_nb_veh_in_ar_lk=v_val_netwk.get_di_all_links()[i.get_current_id_link_veh_location()].get_current_nb_veh_link())
		#val_prob_rout_prop_current_lk=val_netwk.get_dict_mat_od_key_id_entry_internal_lk_value_list_dest_lks()[\
		#queue_phase.get_associated_phase_to_queue()[0]])					
		#we record the event in the db 
			
		record_db_obj.fct_write_object_in_db_file()
		

#*****************************************************************************************************************************************************************************************

#***********************************************************Case Previous Demand -OD given path*********************************************************************************
	#method treating the case when a previous demand is employed, with given  final dest and path
	def fct_treat_case_veh_ar_at_que_when_previous_demand_given_final_dest_and_path(self,val_netwk,val_min_veh_hold_time,val_prec_round,\
	val_ev_list,val_file_recording_event_db,val_min_nb_veh_to_detect):
	
		#if the t control revision requires sensor monitor
		if val_netwk.get_di_intersections()[val_netwk.get_di_entry_internal_links()\
		[self._id_arrival_link].get_id_head_intersection_node()].get_intersection_control_obj().get_type_control_related_to_t_revision()==\
		Cl_Control_Actuate.TYPE_CONTROL_T_REVISION_CATEGORY["sensor_requirement_for_t_update"]:
		
			val_ti_ctrl_revision_if_decided=self._obj_decisions.fct_calculate_t_ctrl_revision(t_cur=self._event_time,dur=\
			val_netwk.get_di_intersections()[val_netwk.get_di_entry_internal_links()\
			[self._id_arrival_link].get_id_head_intersection_node()].get_intersection_control_obj().\
			get_t_duration_for_defining_t_ctrl_revision_when_at_given_time_sensor_records_veh_variation())
		
			for i in self._li_vehicle:
		
				self.fct_treat_case_veh_arrival_previous_demand_final_dest_and_path_intial_defined_with_sensor_monit(\
				vehicle=i,v_val_netwk=val_netwk,v_val_min_veh_hold_time=val_min_veh_hold_time,v_val_prec_round=val_prec_round,\
				v_val_ev_list=val_ev_list,v_file_recording_event_db=val_file_recording_event_db,\
				v_val_ti_ctrl_revision_if_decided=val_ti_ctrl_revision_if_decided,val_min_nb_vehicles_to_detect=val_min_nb_veh_to_detect)
		
		
		#if the t control revision does nor require sensor monitor
		elif val_netwk.get_di_intersections()[val_netwk.get_di_entry_internal_links()\
		[self._id_arrival_link].get_id_head_intersection_node()].get_intersection_control_obj().get_type_control_related_to_t_revision()==\
		Cl_Control_Actuate.TYPE_CONTROL_T_REVISION_CATEGORY["without_sensor_requirement_for_t_update"]:
		
			for i in self._li_vehicle:
		
				self.fct_treat_case_veh_arrival_previous_demand_final_dest_and_path_intial_defined_without_sensor_monit(\
				vehicle=i,v_val_netwk=val_netwk,v_val_min_veh_hold_time=val_min_veh_hold_time,v_val_prec_round=val_prec_round,\
				v_val_ev_list=val_ev_list,v_file_recording_event_db=val_file_recording_event_db)
		
		#if none of the rpevious cases for the t update of the control
		else:
			print("PROBLEM IN CL_EV_VEH_AR, FCT ffct_treat_case_veh_ar_at_que_when_previous_demand_given_final_dest_and_path ",\
			val_netwk.get_di_intersections()[val_netwk.get_di_entry_internal_links()\
			[self._id_arrival_link].get_id_head_intersection_node()].get_intersection_control_obj().get_type_control_related_to_t_revision())
			import sys
			sys.exit()


#*****************************************************************************************************************************************************************************************

#***************************************************Cas Previous Demand-with OD dyn computed path-eval ctrl-without sensor monit *****************************************
	#method treating the case when a vehicle arrives at a que, a previously generated demand is empoyed,
	# final destination was  given, the path dynam computed in the empoyed demand, 
	#the utilised control  does not require  sensor monitoring for the t at which is should  be revised 
	#the purpose fo the implementation is to evaluate the control (so the demamnd and path has to be the same or fo the same law of the previouslu generated demand)
	def fct_treat_case_veh_arrival_previous_demand_final_dest_initial_defined_path_dyn_computed_without_sensor_monit_ctrl_eval(self,\
	vehicle,v_val_netwk,v_val_min_veh_hold_time,v_val_prec_round,v_val_ev_list,v_file_recording_event_db,\
	v_val_dict_vehicle_info_prev_sim,v_val_fct_calc_queue_id_when_given_final_dest_and_path_dynam_constructed):
	
		#if in the previous sim we have generated as many vehicle destinations
		if len(v_val_dict_vehicle_info_prev_sim[vehicle.get_id_veh()][1]) != List_Explicit_Values.initialisation_value_to_one:
			
			#the vehicle queue  object chosen for the vehicle to join in
			queue_phase=v_val_netwk.get_di_entry_internal_links()[v_val_dict_vehicle_info_prev_sim[vehicle.get_id_veh()][1][0]].\
			get_set_veh_queue().get_di_obj_veh_queue_at_link()[v_val_dict_vehicle_info_prev_sim[vehicle.get_id_veh()][1][0],\
			v_val_dict_vehicle_info_prev_sim[vehicle.get_id_veh()][1][1]]
				
			#we delete the first link location from the veh dictionary 
			#print("HERE",dict_veh_info_prev_sim[val_vehicle.get_id_veh()][1])
			v_val_dict_vehicle_info_prev_sim[vehicle.get_id_veh()][1].remove(v_val_dict_vehicle_info_prev_sim[vehicle.get_id_veh()][1][0])
			
		#if in the previous sim we have not generated as many vehicle destinations
		else:
			#we decide the que chosen by the vehicle
			li_param_fct_calcul_que_chosen_by_veh=[\
			v_val_netwk,self._id_arrival_link,vehicle.get_id_veh_final_destination_link(),v_val_fct_calc_queue_id_when_given_final_dest_and_path_dynam_constructed]
		
			id_dest_lk=self._obj_decisions.fct_calcul_queue_chosen_by_veh_cas_given_final_destination_dyn_constr_path(*\
			li_param_fct_calcul_que_chosen_by_veh)
		
			#the vehicle queue  object chosen for the vehicle to join in
			queue_phase=v_val_netwk.get_di_entry_internal_links()[self._id_arrival_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()[\
			self._id_arrival_link,id_dest_lk]
		
		
		
		#we update the vehicle, we indicate the chosen queue and its arrival time in the queue
		vehicle.fct_update_veh_after_choosing_queue(queue_phase,self._event_time,v_val_netwk)
		
		#we update the link (its travel time employed by the algo computing the split ratios)
		v_val_netwk.get_di_entry_internal_links()[self._id_arrival_link].fct_update_link_when_split_ratios_dyn_computed(\
		val_new_trav_time=round(self._event_time-vehicle.get_t_vehicle_arrival_at_current_link()))
		
		#we examine if vehicle can leave the queue immediately
		veh_can_leave_que=self._obj_decisions.fct_defining_whether_veh_can_leave_que_by_its_arrival()
		
		#if the vehicle can leave the que
		if veh_can_leave_que==List_Explicit_Values.initialisation_value_to_one:
			print("PROBLEM IN CL_Ev_veh_arrived_at_que veh_can_leave_que, \
			fct_treat_case_veh_arrival_previous_demand_final_dest_initial_defined_path_dyn_computed_without_sensor_monit_ctrl_eval ",veh_can_leave_que)
			import sys
			sys.exit()
		
		#if the vehicle can not leave the que
		else:
			t_end_veh_hold_time=round(self._event_time+v_val_min_veh_hold_time,v_val_prec_round)
			
			#we examine if there are other vehicles in the que
			if v_val_netwk.get_di_entry_internal_links()[self._id_arrival_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
			[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].get_queue_veh()==[]:
				other_veh_in_que_before_add_veh=0
			else:
				other_veh_in_que_before_add_veh=1
				
			#we add the vehicle in the queue
			v_val_netwk.get_di_entry_internal_links()[self._id_arrival_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
			[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].\
			fct_update_veh_queue_when_veh_prohibited_to_leave_with_mod(vehicle)
			
			#we indicate the time at which the vehicle can leave the que regarding the hold duration
			vehicle.set_t_end_veh_hold_time_que(t_end_veh_hold_time)
			
			#if there are no veh in the que (otherwise veh will keave with ev end veh departure) 
			if other_veh_in_que_before_add_veh==0:
			
				#creat ev_end_hold_time
				ev_end_hold_time=Cl_Ev_end_veh_hold_at_que.Ev_end_veh_hold_at_que(val_event_t= t_end_veh_hold_time,\
				val_id_que=queue_phase.get_associated_phase_to_queue())
					
				#we add the event in the event list
				ev_end_hold_time.fct_insertion_even_in_event_list(event_list=v_val_ev_list,\
				message="IN CL_EV_VEH_ARRIVED_AT_QUE IN FUNCT \
				fct_treat_case_veh_arrival_previous_demand_final_dest_initial_defined_path_dyn_computed_without_sensor_monit_ctrl_eval,\
				EVENT END HOLD TIME HAS TIME < TIME FIRST EVENT IN THE LIST")
		
		li_id_veh=[]
		for i in v_val_netwk.get_di_entry_internal_links()[self._id_arrival_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[queue_phase.get_associated_phase_to_queue()[0],\
		queue_phase.get_associated_phase_to_queue()[1]].get_queue_veh():
					
			li_id_veh.append(i.get_id_veh())
						
		#we create an record database object 
		record_db_obj=Cl_Record_Database.Record_Database(\
		val_file_db=v_file_recording_event_db,\
		val_ev_time=self._event_time,\
		val_ev_type=self._event_type,\
		val_id_inters_node=[v_val_netwk.get_di_entry_internal_links()[\
		queue_phase.get_associated_phase_to_queue()[0]].get_id_head_intersection_node()],\
		val_t_start_current_inters_control=v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_internal_links()[\
		queue_phase.get_associated_phase_to_queue()[0]].\
		get_id_head_intersection_node()].get_intersection_control_obj().get_t_start_control(),\
		val_duration_current_inters_control=v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_internal_links()[\
		queue_phase.get_associated_phase_to_queue()[0]].\
		get_id_head_intersection_node()].get_intersection_control_obj().get_duration_control(),\
		val_current_inters_matrix_with_the_associated_link_of_phase=\
		v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_internal_links()[\
		queue_phase.get_associated_phase_to_queue()[0]].get_id_head_intersection_node()].\
		get_intersection_control_obj().\
		get_di_intersection_control_mat(),\
		val_duration_current_cycle=v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_internal_links()[\
		queue_phase.get_associated_phase_to_queue()[0]].\
		get_id_head_intersection_node()].get_intersection_control_obj().\
		get_cycle_duration_associated_with_control(),\
		val_vehicle_id=vehicle.get_id_veh(),\
		val_time_veh_appearance_in_network=vehicle.get_t_veh_appearance_at_network(),\
		val_id_veh_entry_link=vehicle.get_id_entry_link_veh_ap(),\
		val_id_current_link_veh_location=vehicle.get_current_id_link_veh_location(),\
		val_time_veh_arrival_at_current_link=vehicle.get_t_vehicle_arrival_at_current_link(),\
		val_time_veh_departure_from_current_link=vehicle.get_t_vehicle_departure_from_current_link(),\
		val_veh_current_queue_location=vehicle.get_veh_current_queue_location(),\
		val_time_veh_arrival_at_current_queue=vehicle.get_t_vehicle_arrival_at_current_queue(),\
		val_time_veh_start_departure_from_current_queue=vehicle.get_t_vehicle_started_departure_from_current_queue(),\
		val_time_veh_departure_from_current_queue=vehicle.get_t_vehicle_departure_from_current_queue(),\
		val_veh_id_destination_link=vehicle.get_veh_current_queue_location()[List_Explicit_Values.val_second_element_of_list],\
		val_time_veh_exit_from_network=vehicle.get_t_exit_veh_from_network(),\
		val_id_event_link=self._id_arrival_link,\
		val_veh_can_leave_now=veh_can_leave_que,\
		val_current_achieved_queue_service_rate_including_current_vehicle=\
		v_val_netwk.get_di_entry_internal_links()[self._id_arrival_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].\
		get_current_reached_service_rate(),\
		val_current_queue_service_rate=\
		v_val_netwk.get_di_entry_internal_links()[self._id_arrival_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].\
		get_current_queue_service_rate(),\
		val_li_id_vehicles_in_queue=li_id_veh,\
		val_nb_veh_in_ar_lk=v_val_netwk.get_di_all_links()[i.get_current_id_link_veh_location()].get_current_nb_veh_link())
		#val_prob_rout_prop_current_lk=val_netwk.get_dict_mat_od_key_id_entry_internal_lk_value_list_dest_lks()[\
		#queue_phase.get_associated_phase_to_queue()[0]])					
		#we record the event in the db 
			
		record_db_obj.fct_write_object_in_db_file()
		

#*****************************************************************************************************************************************************************************************

#***************************************************Cas Previous Demand-with OD dyn computed path-eval ctrl-with sensor monit ********************************************
	#method treating the case when a vehicle arrives at a que, a previously generated demand is employed,
	# final destination was  given, the path dynam computed in the empoyed demand, 
	#the utilised control  requires sensor monitoring for the t at which is should  be revised 
	#the purpose fo the implementation is to evaluate the control (so the demamnd and path has to be the same or fo the same law of the previouslu generated demand)
	def fct_treat_case_veh_arrival_previous_demand_final_dest_initial_defined_path_dyn_computed_with_sensor_monit_ctrl_eval(self,\
	vehicle,v_val_netwk,v_val_min_veh_hold_time,\
	v_val_prec_round,v_val_ev_list,v_file_recording_event_db,v_val_ti_ctrl_revision_if_decided,\
	v_val_dict_vehicle_info_prev_sim,v_val_fct_calc_queue_id_when_given_final_dest_and_path_dynam_constructed,\
	val_min_nb_vehicles_to_detect):
	
		#if in the previous sim we have generated as many vehicle destinations
		if len(v_val_dict_vehicle_info_prev_sim[vehicle.get_id_veh()][1]) != List_Explicit_Values.initialisation_value_to_one:
			
			#the vehicle queue  object chosen for the vehicle to join in
			queue_phase=v_val_netwk.get_di_entry_internal_links()[v_val_dict_vehicle_info_prev_sim[vehicle.get_id_veh()][1][0]].\
			get_set_veh_queue().get_di_obj_veh_queue_at_link()[v_val_dict_vehicle_info_prev_sim[vehicle.get_id_veh()][1][0],\
			v_val_dict_vehicle_info_prev_sim[vehicle.get_id_veh()][1][1]]
				
			#we delete the first link location from the veh dictionary 
			#print("HERE",dict_veh_info_prev_sim[val_vehicle.get_id_veh()][1])
			v_val_dict_vehicle_info_prev_sim[vehicle.get_id_veh()][1].remove(v_val_dict_vehicle_info_prev_sim[vehicle.get_id_veh()][1][0])
			
		#if in the previous sim we have not generated as many vehicle destinations
		else:
			#we decide the que chosen by the vehicle
			li_param_fct_calcul_que_chosen_by_veh=[\
			v_val_netwk,self._id_arrival_link,vehicle.get_id_veh_final_destination_link(),v_val_fct_calc_queue_id_when_given_final_dest_and_path_dynam_constructed]
		
			id_dest_lk=self._obj_decisions.fct_calcul_queue_chosen_by_veh_cas_given_final_destination_dyn_constr_path(*\
			li_param_fct_calcul_que_chosen_by_veh)
		
			#the vehicle queue  object chosen for the vehicle to join in
			queue_phase=v_val_netwk.get_di_entry_internal_links()[self._id_arrival_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()[\
			self._id_arrival_link,id_dest_lk]
			
		#we update the vehicle, we indicate the chosen queue and its arrival time in the queue
		vehicle.fct_update_veh_after_choosing_queue(queue_phase,self._event_time,v_val_netwk)
		#we update the link (its travel time employed by the algo computing the split ratios)
		v_val_netwk.get_di_entry_internal_links()[self._id_arrival_link].fct_update_link_when_split_ratios_dyn_computed(\
		val_new_trav_time=round(self._event_time-vehicle.get_t_vehicle_arrival_at_current_link()))
		
		#we examine if vehicle can leave the queue immediately
		veh_can_leave_que=self._obj_decisions.fct_defining_whether_veh_can_leave_que_by_its_arrival()
		
		#if the vehicle can leave the que
		if veh_can_leave_que==List_Explicit_Values.initialisation_value_to_one:
			print("PROBLEM IN CL_Ev_veh_arrived_at_que veh_can_leave_que, \
			fct_treat_case_veh_arrival_previous_demand_final_dest_initial_defined_path_dyn_computed_with_sensor_monit_ctrl_eval ",veh_can_leave_que)
			import sys
			sys.exit()
		
		#if the vehicle can not leave the que
		else:
			t_end_veh_hold_time=round(self._event_time+v_val_min_veh_hold_time,v_val_prec_round)
			
			#we examine if there are other vehicles in the que
			if v_val_netwk.get_di_entry_internal_links()[self._id_arrival_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
			[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].get_queue_veh()==[]:
				other_veh_in_que_before_add_veh=0
			else:
				other_veh_in_que_before_add_veh=1
				
			#we add the vehicle in the queue
			v_val_netwk.get_di_entry_internal_links()[self._id_arrival_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
			[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].\
			fct_update_veh_queue_when_veh_prohibited_to_leave_with_mod(vehicle)
			
			#we indicate the time at which the vehicle can leave the que regarding the hold duration
			vehicle.set_t_end_veh_hold_time_que(t_end_veh_hold_time)
			
			#if there are no veh in the que (otherwise veh will keave with ev end veh departure) 
			if other_veh_in_que_before_add_veh==0:
			
				#creat ev_end_hold_time
				ev_end_hold_time=Cl_Ev_end_veh_hold_at_que.Ev_end_veh_hold_at_que(val_event_t= t_end_veh_hold_time,\
				val_id_que=queue_phase.get_associated_phase_to_queue())
					
				#we add the event in the event list
				ev_end_hold_time.fct_insertion_even_in_event_list(event_list=v_val_ev_list,\
				message="IN CL_EV_VEH_ARRIVED_AT_QUE IN FUNCT \
				fct_treat_case_veh_arrival_previous_demand_final_dest_initial_defined_path_dyn_computed_with_sensor_monit_ctrl_eval,\
				EVENT END HOLD TIME HAS TIME < TIME FIRST EVENT IN THE LIST")
				
			#if the queue is not a right turn 
			if queue_phase.get_type_veh_queue()!=Cl_Vehicle_Queue.TYPE_VEHICLE_QUEUE["right_turn"]:
			
				#if there is at least one detector detecting the veh
				if queue_phase.fct_exam_whether_at_least_nb_veh_detected_by_a_que_sensor(val_min_nb_veh_to_detect=val_min_nb_vehicles_to_detect)!=None:
				
					
					# controle dec update
					ev_end_deci_next_icm=Cl_Ev_end_decision_next_intersection_control.Ev_end_decision_next_intersection_control(\
					val_ev_time=v_val_ti_ctrl_revision_if_decided,\
					val_id_intersection_node=v_val_netwk.get_di_internal_links_to_network()[self._id_arrival_link].get_id_head_intersection_node(),\
					val_type_control_to_employ=\
					v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_internal_links()[self._id_arrival_link].\
					get_id_head_intersection_node()].get_ctrl_actuate_obj().get_type_employed_ctrl(),\
					val_control_category="sensor_requirement")
					#,val_reason_ctrl_revision_t_lim=0)	
		
					#on insert the event ev_end_dec_next_icm into the event list
					ev_end_deci_next_icm.fct_insertion_even_in_event_list(event_list=v_val_ev_list,\
					message="IN CL_Ev_veh_Arrived_at_quel IN FUNCT, \
					fct_treat_case_veh_arrival_previous_demand_final_dest_initial_defined_path_dyn_computed_with_sensor_monit_ctrl_eval\
					NEXT ev_new_end_dec_netw_control EVENT HAS TIME < TIME FIRST EVENT IN THE LIST")
				
					#we indicate the intersection that a ctrl request is made
					#v_val_netwk.get_di_intersections()[v_val_netwk.get_di_internal_links_to_network()[self._id_arrival_link].get_id_head_intersection_node()].\
					#set_t_last_request_ctrl_revision_when_flux_monitoring(v_val_ti_ctrl_revision_if_decided)
					
					#we indicate the number of times a control revision is asked for the same time
					#v_val_netwk.get_di_intersections()[v_val_netwk.get_di_internal_links_to_network()[self._id_arrival_link].get_id_head_intersection_node()].\
					#set_nb_times_ctrl_revision_corresponding_to_t_last_request_ctrl_revision_when_flux_monitoring(\
					#v_val_netwk.get_di_intersections()[v_val_netwk.get_di_internal_links_to_network()[self._id_arrival_link].get_id_head_intersection_node()].\
					#set_nb_times_ctrl_revision_corresponding_to_t_last_request_ctrl_revision_when_flux_monitoring()+1)
		
		li_id_veh=[]
		for i in v_val_netwk.get_di_entry_internal_links()[self._id_arrival_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[queue_phase.get_associated_phase_to_queue()[0],\
		queue_phase.get_associated_phase_to_queue()[1]].get_queue_veh():
					
			li_id_veh.append(i.get_id_veh())
						
		#we create an record database object 
		record_db_obj=Cl_Record_Database.Record_Database(\
		val_file_db=v_file_recording_event_db,\
		val_ev_time=self._event_time,\
		val_ev_type=self._event_type,\
		val_id_inters_node=[v_val_netwk.get_di_entry_internal_links()[\
		queue_phase.get_associated_phase_to_queue()[0]].get_id_head_intersection_node()],\
		val_t_start_current_inters_control=v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_internal_links()[\
		queue_phase.get_associated_phase_to_queue()[0]].\
		get_id_head_intersection_node()].get_intersection_control_obj().get_t_start_control(),\
		val_duration_current_inters_control=v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_internal_links()[\
		queue_phase.get_associated_phase_to_queue()[0]].\
		get_id_head_intersection_node()].get_intersection_control_obj().get_duration_control(),\
		val_current_inters_matrix_with_the_associated_link_of_phase=\
		v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_internal_links()[\
		queue_phase.get_associated_phase_to_queue()[0]].get_id_head_intersection_node()].\
		get_intersection_control_obj().\
		get_di_intersection_control_mat(),\
		val_duration_current_cycle=v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_internal_links()[\
		queue_phase.get_associated_phase_to_queue()[0]].\
		get_id_head_intersection_node()].get_intersection_control_obj().\
		get_cycle_duration_associated_with_control(),\
		val_vehicle_id=vehicle.get_id_veh(),\
		val_time_veh_appearance_in_network=vehicle.get_t_veh_appearance_at_network(),\
		val_id_veh_entry_link=vehicle.get_id_entry_link_veh_ap(),\
		val_id_current_link_veh_location=vehicle.get_current_id_link_veh_location(),\
		val_time_veh_arrival_at_current_link=vehicle.get_t_vehicle_arrival_at_current_link(),\
		val_time_veh_departure_from_current_link=vehicle.get_t_vehicle_departure_from_current_link(),\
		val_veh_current_queue_location=vehicle.get_veh_current_queue_location(),\
		val_time_veh_arrival_at_current_queue=vehicle.get_t_vehicle_arrival_at_current_queue(),\
		val_time_veh_start_departure_from_current_queue=vehicle.get_t_vehicle_started_departure_from_current_queue(),\
		val_time_veh_departure_from_current_queue=vehicle.get_t_vehicle_departure_from_current_queue(),\
		val_veh_id_destination_link=vehicle.get_veh_current_queue_location()[List_Explicit_Values.val_second_element_of_list],\
		val_time_veh_exit_from_network=vehicle.get_t_exit_veh_from_network(),\
		val_id_event_link=self._id_arrival_link,\
		val_veh_can_leave_now=veh_can_leave_que,\
		val_current_achieved_queue_service_rate_including_current_vehicle=\
		v_val_netwk.get_di_entry_internal_links()[self._id_arrival_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].\
		get_current_reached_service_rate(),\
		val_current_queue_service_rate=\
		v_val_netwk.get_di_entry_internal_links()[self._id_arrival_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].\
		get_current_queue_service_rate(),\
		val_li_id_vehicles_in_queue=li_id_veh,\
		val_nb_veh_in_ar_lk=v_val_netwk.get_di_all_links()[i.get_current_id_link_veh_location()].get_current_nb_veh_link())
		#val_prob_rout_prop_current_lk=val_netwk.get_dict_mat_od_key_id_entry_internal_lk_value_list_dest_lks()[\
		#queue_phase.get_associated_phase_to_queue()[0]])					
		#we record the event in the db 
			
		record_db_obj.fct_write_object_in_db_file()
		
#*****************************************************************************************************************************************************************************************

#*********************************************************Case Previous Demand-with OD and path dyn computed ctrl eval******************************************************
	#method treating the case when a prev demand is employed, given final destination and path dyn computed
	#the reason of the implem is to evaluate ctrl policy
	def fct_treat_case_veh_ar_at_que_when_previous_demand_given_final_dest_and_path_dyn_computed_ctr_eval(self,val_netwk,\
	val_min_veh_hold_time,val_prec_round,val_ev_list,val_file_recording_event_db,val_dict_vehicle_info_prev_sim,\
	val_fct_calc_queue_id_when_given_final_dest_and_path_dynam_constructed,val_min_nb_veh_to_detect):
	
		#if the t control revision requires sensor monitor
		if val_netwk.get_di_intersections()[val_netwk.get_di_entry_internal_links()\
		[self._id_arrival_link].get_id_head_intersection_node()].get_intersection_control_obj().get_type_control_related_to_t_revision()==\
		Cl_Control_Actuate.TYPE_CONTROL_T_REVISION_CATEGORY["sensor_requirement_for_t_update"]:
		
			val_ti_ctrl_revision_if_decided=self._obj_decisions.fct_calculate_t_ctrl_revision(t_cur=self._event_time,dur=\
			val_netwk.get_di_intersections()[val_netwk.get_di_entry_internal_links()\
			[self._id_arrival_link].get_id_head_intersection_node()].get_intersection_control_obj().\
			get_t_duration_for_defining_t_ctrl_revision_when_at_given_time_sensor_records_veh_variation())
			
			for i in self._li_vehicle:
			
			
				self.fct_treat_case_veh_arrival_previous_demand_final_dest_initial_defined_path_dyn_computed_with_sensor_monit_ctrl_eval(\
				vehicle=i,v_val_netwk=val_netwk,v_val_min_veh_hold_time=val_min_veh_hold_time,\
				v_val_prec_round=val_prec_round,v_val_ev_list=val_ev_list,v_file_recording_event_db=val_file_recording_event_db,\
				v_val_ti_ctrl_revision_if_decided=val_ti_ctrl_revision_if_decided,\
				v_val_dict_vehicle_info_prev_sim=val_dict_vehicle_info_prev_sim,\
				v_val_fct_calc_queue_id_when_given_final_dest_and_path_dynam_constructed=val_fct_calc_queue_id_when_given_final_dest_and_path_dynam_constructed,\
				val_min_nb_vehicles_to_detect=val_min_nb_veh_to_detect)
		
		
		#if the t control revision does not require sensor monitor
		elif val_netwk.get_di_intersections()[val_netwk.get_di_entry_internal_links()\
		[self._id_arrival_link].get_id_head_intersection_node()].get_intersection_control_obj().get_type_control_related_to_t_revision()==\
		Cl_Control_Actuate.TYPE_CONTROL_T_REVISION_CATEGORY["without_sensor_requirement_for_t_update"]:
		
			for i in self._li_vehicle:
		
				self.fct_treat_case_veh_arrival_previous_demand_final_dest_initial_defined_path_dyn_computed_without_sensor_monit_ctrl_eval(\
				vehicle=i,v_val_netwk=val_netwk,v_val_min_veh_hold_time=val_min_veh_hold_time,v_val_prec_round=val_prec_round,\
				v_val_ev_list=val_ev_list,v_file_recording_event_db=val_file_recording_event_db,\
				v_val_dict_vehicle_info_prev_sim=val_dict_vehicle_info_prev_sim,\
				v_val_fct_calc_queue_id_when_given_final_dest_and_path_dynam_constructed=val_fct_calc_queue_id_when_given_final_dest_and_path_dynam_constructed)
		
		#if none of the previous cases
		else:
			print("PROBLEM IN CL_EV_VEH_AR, FCT fct_treat_case_veh_ar_at_que_when_previous_demand_given_final_dest_and_path_dyn_computed, ",\
			val_netwk.get_di_intersections()[val_netwk.get_di_entry_internal_links()\
			[self._id_arrival_link].get_id_head_intersection_node()].get_intersection_control_obj().get_type_control_related_to_t_revision())
			import sys
			sys.exit()


#*****************************************************************************************************************************************************************************************


#***************************************************Cas Previous Demand-with OD dyn computed path-eval rout algo-without sensor monit *****************************************
	#method treating the case when a vehicle arrives at a que, a previously generated demand is empoyed,
	# final destination was  given, the path dynam computed in the empoyed demand, 
	#the utilised control  does not require  sensor monitoring for the t at which is should  be revised 
	#the purpose fo the implementation is to evaluate the routing algo (so the path has to be recalculated and not consider the destinations of the previous demand)
	def fct_treat_case_veh_arrival_previous_demand_final_dest_initial_defined_path_dyn_computed_without_sensor_monit_rout_eval(self,\
	vehicle,v_val_netwk,v_val_min_veh_hold_time,v_val_prec_round,v_val_ev_list,v_file_recording_event_db,\
	v_val_fct_calc_queue_id_when_given_final_dest_and_path_dynam_constructed):
	
		
		#we decide the que chosen by the vehicle
		li_param_fct_calcul_que_chosen_by_veh=[\
		v_val_netwk,self._id_arrival_link,vehicle.get_id_veh_final_destination_link(),v_val_fct_calc_queue_id_when_given_final_dest_and_path_dynam_constructed]
		
		id_dest_lk=self._obj_decisions.fct_calcul_queue_chosen_by_veh_cas_given_final_destination_dyn_constr_path(*\
		li_param_fct_calcul_que_chosen_by_veh)
		
		#the vehicle queue  object chosen for the vehicle to join in
		queue_phase=v_val_netwk.get_di_entry_internal_links()[self._id_arrival_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()[\
		self._id_arrival_link,id_dest_lk]
		
		
		
		#we update the vehicle, we indicate the chosen queue and its arrival time in the queue
		vehicle.fct_update_veh_after_choosing_queue(queue_phase,self._event_time,v_val_netwk)
		
		#we update the link (its travel time employed by the algo computing the split ratios)
		v_val_netwk.get_di_entry_internal_links()[self._id_arrival_link].fct_update_link_when_split_ratios_dyn_computed(\
		val_new_trav_time=round(self._event_time-vehicle.get_t_vehicle_arrival_at_current_link()))
		
		#we examine if vehicle can leave the queue immediately
		veh_can_leave_que=self._obj_decisions.fct_defining_whether_veh_can_leave_que_by_its_arrival()
		
		#if the vehicle can leave the que
		if veh_can_leave_que==List_Explicit_Values.initialisation_value_to_one:
			print("PROBLEM IN CL_Ev_veh_arrived_at_que veh_can_leave_que, \
			fct_treat_case_veh_arrival_previous_demand_final_dest_initial_defined_path_dyn_computed_without_sensor_monit_rout_eval",veh_can_leave_que)
			import sys
			sys.exit()
		
		#if the vehicle can not leave the que
		else:
			t_end_veh_hold_time=round(self._event_time+v_val_min_veh_hold_time,v_val_prec_round)
			
			#we examine if there are other vehicles in the que
			if v_val_netwk.get_di_entry_internal_links()[self._id_arrival_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
			[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].get_queue_veh()==[]:
				other_veh_in_que_before_add_veh=0
			else:
				other_veh_in_que_before_add_veh=1
				
			#we add the vehicle in the queue
			v_val_netwk.get_di_entry_internal_links()[self._id_arrival_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
			[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].\
			fct_update_veh_queue_when_veh_prohibited_to_leave_with_mod(vehicle)
			
			#we indicate the time at which the vehicle can leave the que regarding the hold duration
			vehicle.set_t_end_veh_hold_time_que(t_end_veh_hold_time)
			
			#if there are no veh in the que (otherwise veh will keave with ev end veh departure) 
			if other_veh_in_que_before_add_veh==0:
			
				#creat ev_end_hold_time
				ev_end_hold_time=Cl_Ev_end_veh_hold_at_que.Ev_end_veh_hold_at_que(val_event_t= t_end_veh_hold_time,\
				val_id_que=queue_phase.get_associated_phase_to_queue())
					
				#we add the event in the event list
				ev_end_hold_time.fct_insertion_even_in_event_list(event_list=v_val_ev_list,\
				message="IN CL_EV_VEH_ARRIVED_AT_QUE IN FUNCT \
				fct_treat_case_veh_arrival_previous_demand_final_dest_initial_defined_path_dyn_computed_without_sensor_monit_rout_eval,\
				EVENT END HOLD TIME HAS TIME < TIME FIRST EVENT IN THE LIST")
		
		li_id_veh=[]
		for i in v_val_netwk.get_di_entry_internal_links()[self._id_arrival_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[queue_phase.get_associated_phase_to_queue()[0],\
		queue_phase.get_associated_phase_to_queue()[1]].get_queue_veh():
					
			li_id_veh.append(i.get_id_veh())
						
		#we create an record database object 
		record_db_obj=Cl_Record_Database.Record_Database(\
		val_file_db=v_file_recording_event_db,\
		val_ev_time=self._event_time,\
		val_ev_type=self._event_type,\
		val_id_inters_node=[v_val_netwk.get_di_entry_internal_links()[\
		queue_phase.get_associated_phase_to_queue()[0]].get_id_head_intersection_node()],\
		val_t_start_current_inters_control=v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_internal_links()[\
		queue_phase.get_associated_phase_to_queue()[0]].\
		get_id_head_intersection_node()].get_intersection_control_obj().get_t_start_control(),\
		val_duration_current_inters_control=v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_internal_links()[\
		queue_phase.get_associated_phase_to_queue()[0]].\
		get_id_head_intersection_node()].get_intersection_control_obj().get_duration_control(),\
		val_current_inters_matrix_with_the_associated_link_of_phase=\
		v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_internal_links()[\
		queue_phase.get_associated_phase_to_queue()[0]].get_id_head_intersection_node()].\
		get_intersection_control_obj().\
		get_di_intersection_control_mat(),\
		val_duration_current_cycle=v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_internal_links()[\
		queue_phase.get_associated_phase_to_queue()[0]].\
		get_id_head_intersection_node()].get_intersection_control_obj().\
		get_cycle_duration_associated_with_control(),\
		val_vehicle_id=vehicle.get_id_veh(),\
		val_time_veh_appearance_in_network=vehicle.get_t_veh_appearance_at_network(),\
		val_id_veh_entry_link=vehicle.get_id_entry_link_veh_ap(),\
		val_id_current_link_veh_location=vehicle.get_current_id_link_veh_location(),\
		val_time_veh_arrival_at_current_link=vehicle.get_t_vehicle_arrival_at_current_link(),\
		val_time_veh_departure_from_current_link=vehicle.get_t_vehicle_departure_from_current_link(),\
		val_veh_current_queue_location=vehicle.get_veh_current_queue_location(),\
		val_time_veh_arrival_at_current_queue=vehicle.get_t_vehicle_arrival_at_current_queue(),\
		val_time_veh_start_departure_from_current_queue=vehicle.get_t_vehicle_started_departure_from_current_queue(),\
		val_time_veh_departure_from_current_queue=vehicle.get_t_vehicle_departure_from_current_queue(),\
		val_veh_id_destination_link=vehicle.get_veh_current_queue_location()[List_Explicit_Values.val_second_element_of_list],\
		val_time_veh_exit_from_network=vehicle.get_t_exit_veh_from_network(),\
		val_id_event_link=self._id_arrival_link,\
		val_veh_can_leave_now=veh_can_leave_que,\
		val_current_achieved_queue_service_rate_including_current_vehicle=\
		v_val_netwk.get_di_entry_internal_links()[self._id_arrival_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].\
		get_current_reached_service_rate(),\
		val_current_queue_service_rate=\
		v_val_netwk.get_di_entry_internal_links()[self._id_arrival_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].\
		get_current_queue_service_rate(),\
		val_li_id_vehicles_in_queue=li_id_veh,\
		val_nb_veh_in_ar_lk=v_val_netwk.get_di_all_links()[i.get_current_id_link_veh_location()].get_current_nb_veh_link())
		#val_prob_rout_prop_current_lk=val_netwk.get_dict_mat_od_key_id_entry_internal_lk_value_list_dest_lks()[\
		#queue_phase.get_associated_phase_to_queue()[0]])					
		#we record the event in the db 
			
		record_db_obj.fct_write_object_in_db_file()
		


#*****************************************************************************************************************************************************************************************


#***************************************************Cas Previous Demand-with OD dyn computed path-eval rout algo-with sensor monit *****************************************
	#method treating the case when a vehicle arrives at a que, a previously generated demand is empoyed,
	# final destination was  given, the path dynam computed in the empoyed demand, 
	#the utilised control  requires  sensor monitoring for the t at which is should  be revised 
	#the purpose fo the implementation is to evaluate the routing algo (so the path has to be recalculated and not consider the destinations of the previous demand)
	def fct_treat_case_veh_arrival_previous_demand_final_dest_initial_defined_path_dyn_computed_with_sensor_monit_rout_eval(self,\
	vehicle,v_val_netwk,v_val_min_veh_hold_time,\
	v_val_prec_round,v_val_ev_list,v_file_recording_event_db,v_val_ti_ctrl_revision_if_decided,\
	v_val_fct_calc_queue_id_when_given_final_dest_and_path_dynam_constructed,\
	val_min_nb_vehicles_to_detect):
	
	
		#we decide the que chosen by the vehicle
		li_param_fct_calcul_que_chosen_by_veh=[\
		v_val_netwk,self._id_arrival_link,vehicle.get_id_veh_final_destination_link(),v_val_fct_calc_queue_id_when_given_final_dest_and_path_dynam_constructed]
		
		id_dest_lk=self._obj_decisions.fct_calcul_queue_chosen_by_veh_cas_given_final_destination_dyn_constr_path(*\
		li_param_fct_calcul_que_chosen_by_veh)
		
		#the vehicle queue  object chosen for the vehicle to join in
		queue_phase=v_val_netwk.get_di_entry_internal_links()[self._id_arrival_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()[\
		self._id_arrival_link,id_dest_lk]
			
		#we update the vehicle, we indicate the chosen queue and its arrival time in the queue
		vehicle.fct_update_veh_after_choosing_queue(queue_phase,self._event_time,v_val_netwk)
		#we update the link (its travel time employed by the algo computing the split ratios)
		v_val_netwk.get_di_entry_internal_links()[self._id_arrival_link].fct_update_link_when_split_ratios_dyn_computed(\
		val_new_trav_time=round(self._event_time-vehicle.get_t_vehicle_arrival_at_current_link()))
		
		#we examine if vehicle can leave the queue immediately
		veh_can_leave_que=self._obj_decisions.fct_defining_whether_veh_can_leave_que_by_its_arrival()
		
		#if the vehicle can leave the que
		if veh_can_leave_que==List_Explicit_Values.initialisation_value_to_one:
			print("PROBLEM IN CL_Ev_veh_arrived_at_que veh_can_leave_que, \
			 fct_treat_case_veh_arrival_previous_demand_final_dest_initial_defined_path_dyn_computed_with_sensor_monit_rout_eval ",veh_can_leave_que)
			import sys
			sys.exit()
		
		#if the vehicle can not leave the que
		else:
			t_end_veh_hold_time=round(self._event_time+v_val_min_veh_hold_time,v_val_prec_round)
			
			#we examine if there are other vehicles in the que
			if v_val_netwk.get_di_entry_internal_links()[self._id_arrival_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
			[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].get_queue_veh()==[]:
				other_veh_in_que_before_add_veh=0
			else:
				other_veh_in_que_before_add_veh=1
				
			#we add the vehicle in the queue
			v_val_netwk.get_di_entry_internal_links()[self._id_arrival_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
			[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].\
			fct_update_veh_queue_when_veh_prohibited_to_leave_with_mod(vehicle)
			
			#we indicate the time at which the vehicle can leave the que regarding the hold duration
			vehicle.set_t_end_veh_hold_time_que(t_end_veh_hold_time)
			
			#if there are no veh in the que (otherwise veh will keave with ev end veh departure) 
			if other_veh_in_que_before_add_veh==0:
			
				#creat ev_end_hold_time
				ev_end_hold_time=Cl_Ev_end_veh_hold_at_que.Ev_end_veh_hold_at_que(val_event_t= t_end_veh_hold_time,\
				val_id_que=queue_phase.get_associated_phase_to_queue())
					
				#we add the event in the event list
				ev_end_hold_time.fct_insertion_even_in_event_list(event_list=v_val_ev_list,\
				message="IN CL_EV_VEH_ARRIVED_AT_QUE IN FUNCT \
				 fct_treat_case_veh_arrival_previous_demand_final_dest_initial_defined_path_dyn_computed_with_sensor_monit_rout_eval,\
				EVENT END HOLD TIME HAS TIME < TIME FIRST EVENT IN THE LIST")
				
			#if the queue is not a right turn 
			if queue_phase.get_type_veh_queue()!=Cl_Vehicle_Queue.TYPE_VEHICLE_QUEUE["right_turn"]:
			
				#if there is at least one detector detecting the veh
				if queue_phase.fct_exam_whether_at_least_nb_veh_detected_by_a_que_sensor(val_min_nb_veh_to_detect=val_min_nb_vehicles_to_detect)!=None:
				
					
					# controle dec update
					ev_end_deci_next_icm=Cl_Ev_end_decision_next_intersection_control.Ev_end_decision_next_intersection_control(\
					val_ev_time=v_val_ti_ctrl_revision_if_decided,\
					val_id_intersection_node=v_val_netwk.get_di_internal_links_to_network()[self._id_arrival_link].get_id_head_intersection_node(),\
					val_type_control_to_employ=\
					v_val_netwk.get_di_intersections()[v_val_netwk.get_di_internal_links_to_network()[self._id_arrival_link].\
					get_id_head_intersection_node()].get_ctrl_actuate_obj().get_type_employed_ctrl(),\
					val_control_category="sensor_requirement")
					#,val_reason_ctrl_revision_t_lim=0)	
		
					#on insert the event ev_end_dec_next_icm into the event list
					ev_end_deci_next_icm.fct_insertion_even_in_event_list(event_list=v_val_ev_list,\
					message="IN CL_Ev_veh_Arrived_at_quel IN FUNCT, \
					fct_treat_case_veh_arrival_previous_demand_final_dest_initial_defined_path_dyn_computed_with_sensor_monit_rout_eval\
					NEXT ev_new_end_dec_netw_control EVENT HAS TIME < TIME FIRST EVENT IN THE LIST")
				
					#we indicate the intersection that a ctrl request is made
					#v_val_netwk.get_di_intersections()[v_val_netwk.get_di_internal_links_to_network()[self._id_arrival_link].get_id_head_intersection_node()].\
					#set_t_last_request_ctrl_revision_when_flux_monitoring(v_val_ti_ctrl_revision_if_decided)
					
					#we indicate the number of times a control revision is asked for the same time
					#v_val_netwk.get_di_intersections()[v_val_netwk.get_di_internal_links_to_network()[self._id_arrival_link].get_id_head_intersection_node()].\
					#set_nb_times_ctrl_revision_corresponding_to_t_last_request_ctrl_revision_when_flux_monitoring(\
					#v_val_netwk.get_di_intersections()[v_val_netwk.get_di_internal_links_to_network()[self._id_arrival_link].get_id_head_intersection_node()].\
					#set_nb_times_ctrl_revision_corresponding_to_t_last_request_ctrl_revision_when_flux_monitoring()+1)
				
		
		li_id_veh=[]
		for i in v_val_netwk.get_di_entry_internal_links()[self._id_arrival_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[queue_phase.get_associated_phase_to_queue()[0],\
		queue_phase.get_associated_phase_to_queue()[1]].get_queue_veh():
					
			li_id_veh.append(i.get_id_veh())
						
		#we create an record database object 
		record_db_obj=Cl_Record_Database.Record_Database(\
		val_file_db=v_file_recording_event_db,\
		val_ev_time=self._event_time,\
		val_ev_type=self._event_type,\
		val_id_inters_node=[v_val_netwk.get_di_entry_internal_links()[\
		queue_phase.get_associated_phase_to_queue()[0]].get_id_head_intersection_node()],\
		val_t_start_current_inters_control=v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_internal_links()[\
		queue_phase.get_associated_phase_to_queue()[0]].\
		get_id_head_intersection_node()].get_intersection_control_obj().get_t_start_control(),\
		val_duration_current_inters_control=v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_internal_links()[\
		queue_phase.get_associated_phase_to_queue()[0]].\
		get_id_head_intersection_node()].get_intersection_control_obj().get_duration_control(),\
		val_current_inters_matrix_with_the_associated_link_of_phase=\
		v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_internal_links()[\
		queue_phase.get_associated_phase_to_queue()[0]].get_id_head_intersection_node()].\
		get_intersection_control_obj().\
		get_di_intersection_control_mat(),\
		val_duration_current_cycle=v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_internal_links()[\
		queue_phase.get_associated_phase_to_queue()[0]].\
		get_id_head_intersection_node()].get_intersection_control_obj().\
		get_cycle_duration_associated_with_control(),\
		val_vehicle_id=vehicle.get_id_veh(),\
		val_time_veh_appearance_in_network=vehicle.get_t_veh_appearance_at_network(),\
		val_id_veh_entry_link=vehicle.get_id_entry_link_veh_ap(),\
		val_id_current_link_veh_location=vehicle.get_current_id_link_veh_location(),\
		val_time_veh_arrival_at_current_link=vehicle.get_t_vehicle_arrival_at_current_link(),\
		val_time_veh_departure_from_current_link=vehicle.get_t_vehicle_departure_from_current_link(),\
		val_veh_current_queue_location=vehicle.get_veh_current_queue_location(),\
		val_time_veh_arrival_at_current_queue=vehicle.get_t_vehicle_arrival_at_current_queue(),\
		val_time_veh_start_departure_from_current_queue=vehicle.get_t_vehicle_started_departure_from_current_queue(),\
		val_time_veh_departure_from_current_queue=vehicle.get_t_vehicle_departure_from_current_queue(),\
		val_veh_id_destination_link=vehicle.get_veh_current_queue_location()[List_Explicit_Values.val_second_element_of_list],\
		val_time_veh_exit_from_network=vehicle.get_t_exit_veh_from_network(),\
		val_id_event_link=self._id_arrival_link,\
		val_veh_can_leave_now=veh_can_leave_que,\
		val_current_achieved_queue_service_rate_including_current_vehicle=\
		v_val_netwk.get_di_entry_internal_links()[self._id_arrival_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].\
		get_current_reached_service_rate(),\
		val_current_queue_service_rate=\
		v_val_netwk.get_di_entry_internal_links()[self._id_arrival_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].\
		get_current_queue_service_rate(),\
		val_li_id_vehicles_in_queue=li_id_veh,\
		val_nb_veh_in_ar_lk=v_val_netwk.get_di_all_links()[i.get_current_id_link_veh_location()].get_current_nb_veh_link())
		#val_prob_rout_prop_current_lk=val_netwk.get_dict_mat_od_key_id_entry_internal_lk_value_list_dest_lks()[\
		#queue_phase.get_associated_phase_to_queue()[0]])					
		#we record the event in the db 
			
		record_db_obj.fct_write_object_in_db_file()
		
#*****************************************************************************************************************************************************************************************
#*************************************Case Previous Demand-with OD path dyn computed rout algo eval*************************************************************************
	#method treat the case of a prev demand, path dyn computed the reason of the implem is the algo eval
	def fct_treat_case_veh_ar_at_que_when_previous_demand_given_final_dest_and_path_dyn_computed_rout_algo_eval(self,\
	val_netw,val_min_veh_hold_time,val_prec_round,val_ev_list,val_file_recording_event_db,\
	val_fct_calc_queue_id_when_given_final_dest_and_path_dynam_constructed,val_min_nb_veh_to_detect):
	
		#if the t control revision requires sensor monitor
		if val_netw.get_di_intersections()[val_netw.get_di_entry_internal_links()\
		[self._id_arrival_link].get_id_head_intersection_node()].get_intersection_control_obj().get_type_control_related_to_t_revision()==\
		Cl_Control_Actuate.TYPE_CONTROL_T_REVISION_CATEGORY["sensor_requirement_for_t_update"]:
		
			val_ti_ctrl_revision_if_decided=self._obj_decisions.fct_calculate_t_ctrl_revision(t_cur=self._event_time,dur=\
			val_netw.get_di_intersections()[val_netw.get_di_entry_internal_links()\
			[self._id_arrival_link].get_id_head_intersection_node()].get_intersection_control_obj().\
			get_t_duration_for_defining_t_ctrl_revision_when_at_given_time_sensor_records_veh_variation())
			
			for i in self._li_vehicle:
			
				self.fct_treat_case_veh_arrival_previous_demand_final_dest_initial_defined_path_dyn_computed_with_sensor_monit_rout_eval(\
				vehicle=i,v_val_netwk=val_netw,v_val_min_veh_hold_time=val_min_veh_hold_time,\
				v_val_prec_round=val_prec_round,v_val_ev_list=val_ev_list,v_file_recording_event_db=val_file_recording_event_db,\
				v_val_ti_ctrl_revision_if_decided=val_ti_ctrl_revision_if_decided,\
				v_val_fct_calc_queue_id_when_given_final_dest_and_path_dynam_constructed=val_fct_calc_queue_id_when_given_final_dest_and_path_dynam_constructed,\
				val_min_nb_vehicles_to_detect=val_min_nb_veh_to_detect)
			
		#if the t control revision does not require sensor monitor
		elif val_netw.get_di_intersections()[val_netw.get_di_entry_internal_links()\
		[self._id_arrival_link].get_id_head_intersection_node()].get_intersection_control_obj().get_type_control_related_to_t_revision()==\
		Cl_Control_Actuate.TYPE_CONTROL_T_REVISION_CATEGORY["without_sensor_requirement_for_t_update"]:
		
			for i in self._li_vehicle:
			
				self.fct_treat_case_veh_arrival_previous_demand_final_dest_initial_defined_path_dyn_computed_without_sensor_monit_rout_eval(\
				vehicle=i,v_val_netwk=val_netw,v_val_min_veh_hold_time=val_min_veh_hold_time,v_val_prec_round=val_prec_round,\
				v_val_ev_list=val_ev_list,v_file_recording_event_db=val_file_recording_event_db,\
				v_val_fct_calc_queue_id_when_given_final_dest_and_path_dynam_constructed=val_fct_calc_queue_id_when_given_final_dest_and_path_dynam_constructed)
			
		#if none of the previous cases
		else:
			print("PROBLEM IN CL_EV_VEH_AR, FCT fct_treat_case_veh_ar_at_que_when_previous_demand_given_final_dest_and_path_dyn_computed_rout_algo_eval, ",\
			val_netwk.get_di_intersections()[val_netwk.get_di_entry_internal_links()\
			[self._id_arrival_link].get_id_head_intersection_node()].get_intersection_control_obj().get_type_control_related_to_t_revision())
			import sys
			sys.exit()

#*****************************************************************************************************************************************************************************************

#************************************************Cas Previous Demand Mixed management ***********************************************************************************
	def fct_treat_case_veh_ar_at_que_previous_demand_mixed_management_dyn_defined_path_or_initial_given_path(self,v_val_netwk,v_val_dict_vehicle_info_prev_sim,\
	v_val_min_veh_hold_time,v_val_prec_round,v_val_ev_list,v_val_file_recording_event_db,v_val_min_nb_veh_to_detect):
	
		#if a dynam routing is employed for the vehicle 
		if self._li_vehicle[0].get_type_vehicle_rout_when_mixed_manag()==-1:
		
			self.fct_treat_case_veh_ar_at_que_when_previous_demand_final_dest_and_dyn_computed(\
			val_netwk=v_val_netwk,val_dict_vehicle_info_prev_sim=v_val_dict_vehicle_info_prev_sim,\
			val_min_veh_hold_time=v_val_min_veh_hold_time,val_prec_round=v_val_prec_round,val_ev_list=v_val_ev_list,\
			val_file_recording_event_db=v_val_file_recording_event_db,val_min_nb_veh_to_detect=v_val_min_nb_veh_to_detect)
		
		#if an OD and initially given path is employed for the vehicle
		elif self._li_vehicle[0].get_type_vehicle_rout_when_mixed_manag()==Cl_Vehicle.TYPE_VEH_ROUT_WHEN_MIXED_MANAGEMENT["od_and_initially_given_path"]:
		
			self.fct_treat_case_veh_ar_at_que_when_previous_demand_given_final_dest_and_path(\
			val_netwk=v_val_netwk,val_min_veh_hold_time=v_val_min_veh_hold_time,val_prec_round=v_val_prec_round,\
			val_ev_list=v_val_ev_list,val_file_recording_event_db=v_val_file_recording_event_db,val_min_nb_veh_to_detect=v_val_min_nb_veh_to_detect)
		
		
		
		#if an OD and dynamical constructed path is employed for the vehicle
		#elif self._li_vehicle[0].get_type_vehicle_rout_when_mixed_manag()==Cl_Vehicle.TYPE_VEH_ROUT_WHEN_MIXED_MANAGEMENT["od_and_dynam_constructed_path"]:
		
		#if none of the previous cases is employed
		else:
			print("PROBLEM IN CL_EV_VEH_ARRIVED_AT_QUE, FCT fct_treat_case_veh_ar_at_que_previous_demand_mixed_management,ROUTING TYPE EMPLOYED BY VEH:",self._li_vehicle[0].get_type_vehicle_rout_when_mixed_manag())
			import sys
			sys.exit()
	


#*****************************************************************************************************************************************************************************************
	def fct_treat_case_veh_ar_at_que_previous_demand_mixed_management_dyn_defined_path_or_dyn_constructed_ctr_eval_1(self,v_val_netwk,v_val_dict_vehicle_info_prev_sim,\
	v_val_min_veh_hold_time,v_val_prec_round,v_val_ev_list,v_val_file_recording_event_db,v_val_min_nb_veh_to_detect):
	
		#if a dynam routing is employed for the vehicle 
		if self._li_vehicle[0].get_type_vehicle_rout_when_mixed_manag()==-1:
		
			self.fct_treat_case_veh_ar_at_que_when_previous_demand_final_dest_and_dyn_computed(\
			val_netwk=v_val_netwk,val_dict_vehicle_info_prev_sim=v_val_dict_vehicle_info_prev_sim,\
			val_min_veh_hold_time=v_val_min_veh_hold_time,val_prec_round=v_val_prec_round,val_ev_list=v_val_ev_list,\
			val_file_recording_event_db=v_val_file_recording_event_db,val_min_nb_veh_to_detect=v_val_min_nb_veh_to_detect)
	
		
		#if an OD and dynamical constructed path is employed for the vehicle
		elif self._li_vehicle[0].get_type_vehicle_rout_when_mixed_manag()==Cl_Vehicle.TYPE_VEH_ROUT_WHEN_MIXED_MANAGEMENT["od_and_dynam_constructed_path"]:
		
			self.fct_treat_case_veh_ar_at_que_when_previous_demand_given_final_dest_and_path_dyn_computed_ctr_eval(\
			val_netwk,\
			val_min_veh_hold_time,val_prec_round,val_ev_list,val_file_recording_event_db,val_dict_vehicle_info_prev_sim,\
			val_fct_calc_queue_id_when_given_final_dest_and_path_dynam_constructed,val_min_nb_veh_to_detect)
		
		#if none of the previous cases is employed
		else:
			print("PROBLEM IN CL_EV_VEH_ARRIVED_AT_QUE, FCT fct_treat_case_veh_ar_at_que_previous_demand_mixed_management,ROUTING TYPE EMPLOYED BY VEH:",self._li_vehicle[0].get_type_vehicle_rout_when_mixed_manag())
			import sys
			sys.exit()
	


#*****************************************************************************************************************************************************************************************
#*****************************************************************************************************************************************************************************************
	#method treating the event
	def event_treat(self,val_key_fct_in_dict_to_treat,li_param_fct_treat_event):
	
		#dictionary with the functions treat each case of this event
		di_fct_ev_veh_ar_treat={1:self.fct_treat_case_veh_ar_at_que_when_new_demand_final_dest_and_path_dynam_defined,\
		2:self.fct_treat_case_veh_ar_at_que_when_new_demand_final_dest_and_path_given,\
		3:self.fct_treat_case_veh_ar_at_que_when_new_demand_given_final_dest_and_dyn_computed_path,\
		4:self.fct_treat_case_veh_ar_at_que_when_previous_demand_final_dest_and_dyn_computed,\
		5:self.fct_treat_case_veh_ar_at_que_when_previous_demand_given_final_dest_and_path,\
		6:self.fct_treat_case_veh_ar_at_que_when_previous_demand_given_final_dest_and_path_dyn_computed_ctr_eval,\
		7:self.fct_treat_case_veh_ar_at_que_when_previous_demand_given_final_dest_and_path_dyn_computed_rout_algo_eval,\
		8:self.fct_treat_case_veh_ar_at_que_new_demand_mixed_management_dyn_defined_path_or_initial_given_path,\
		9:self.fct_treat_case_veh_ar_at_que_previous_demand_mixed_management_dyn_defined_path_or_initial_given_path}	
	
		return di_fct_ev_veh_ar_treat[val_key_fct_in_dict_to_treat](*li_param_fct_treat_event)








