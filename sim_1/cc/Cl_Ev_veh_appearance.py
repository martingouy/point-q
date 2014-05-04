import string
import Cl_Event
import List_Explicit_Values
import Cl_Vehicle
import Cl_Global_Functions
import Cl_Decisions
import Cl_Record_Database
import Cl_Ev_end_veh_hold_at_que
import Cl_Intersection
import Cl_Control_Actuate
import Cl_Vehicle_Queue
import Cl_Ev_end_decision_next_intersection_control



class Ev_veh_appearance(Cl_Event.Event):

	"""class defining the event of vehicle appearance at a tail node of an entry link """
	
	def __init__(self,val_event_t=-1,val_vehicle=None,val_current_veh_id_demand_previous_sim=-1):
	
		#gl_funct_obj=Cl_Global_Functions.Global_Functions()
		
		Cl_Event.Event.__init__(self,val_event_time=val_event_t,val_event_type=Cl_Event.TYPE_EV["type_ev_veh_appearance"])
		#,\
		#val_global_fct_obj=gl_funct_obj)
		
		
		#the vehicle appearing at the entry link
		self._vehicle=val_vehicle
		
		
		#the id of the entry link
		self._id_entry_link=self._vehicle.get_id_entry_link_veh_ap()
		
		#the decision object  associated with this event
		obj_decisions=Cl_Decisions.Decisions()
		
		self._obj_decisions=obj_decisions
		
		#the vehicle id when we employe a previously generated demand
		self._current_veh_id_demand_previous_sim=val_current_veh_id_demand_previous_sim
		
		#dictionary with the functions treat each case of this event
		#self._di_fct_ev_treat={1:fct_treat_case_new_demand_final_dest_and_path_dynam_defined,2:fct_treat_case_new_demand_final_dest_and_path_initial_defined,\
		#3:fct_treat_case_new_demand_final_dest_initial_defined_path_dyn_computed,4:fct_treat_case_previous_demand_final_dest_and_path_dyn_defined,\
		#5:fct_treat_case_veh_appear_previous_demand_final_dest_given_ctrl_eval,6:fct_treat_case_veh_appear_previous_demand_final_dest_given_rout_algo_eval}
	
#*****************************************************************************************************************************************************************************************

	#method returning the vehicle of the event
	def get_vehicle(self):
		return self._vehicle

#*****************************************************************************************************************************************************************************************
	#method returning the id of the associated entry link
	def get_id_entry_link(self):
		return self._id_entry_link
#*****************************************************************************************************************************************************************************************
	#method returning the decision object  associated with this event
	def get_obj_decisions(self):
		return self._obj_decisions

#*****************************************************************************************************************************************************************************************
	#method returning the vehicle id when we employe a previously generated demand
	def get_current_veh_id_demand_previous_sim(self):
		return self._current_veh_id_demand_previous_sim

#*****************************************************************************************************************************************************************************************
	#method returning the dictionary with the functions treat each case of this event
	#def get_di_fct_ev_treat(self):
		#return self._di_fct_ev_treat
#*****************************************************************************************************************************************************************************************

	
	#method modifying the vehicle of the event
	def set_vehicle(self,n_v):
		self._vehicle=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the id of the associated entry link
	def set_id_entry_link(self,n_v):
		self._id_entry_link=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the decision object  associated with this event
	def set_obj_decisions(self,n_v):
		self._obj_decisions=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the vehicle id when we employe a previously generated demand
	def set_current_veh_id_demand_previous_sim(self,n_v):
		self._current_veh_id_demand_previous_sim=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the dictionary with the functions treat each case of this event
	#def set_di_fct_ev_treat(self,n_v):
		#self._di_fct_ev_treat=n_v
#*****************************************************************************************************************************************************************************************
	
	#method examining whether the ctrl decision shoudl be updated in the intersection by the veh appearance
	#id_que=[id input lk, id output link]
	#we return 1 if the  decision should be updated (case when  all  ques of the actuat stage has flow <fmin or
	#when the selected queue by a veh  is actuated and has flow < fmin), o if the crrl decision should not be updated
	def fct_exam_whether_ctrl_decision_should_be_updated_when_record_flux_1(self,val_netw,val_min_allowed_flow_depart_link):
	
		#reponse=0
		
		#if we are at the begin of the sim 
		if val_netw.get_di_intersections()[val_netw.get_di_entry_links_to_network()[self._id_entry_link].\
		get_id_head_intersection_node()].get_t_last_request_ctrl_update_when_record_flux()==None:
			return 1
			
		#if we have not planned a control revision for this time,
		elif  val_netw.get_di_intersections()[val_netw.get_di_entry_links_to_network()[self._id_entry_link].\
		get_id_head_intersection_node()].get_t_last_request_ctrl_update_when_record_flux()==0:
		
			#if there is at least one queue of the actuated stage having flow >f_min, the decision will not be updated
			#for j in val_netw.get_di_intersections()[val_netw.get_di_entry_links_to_network()[self._id_entry_link].\
			#get_id_head_intersection_node()].get_di_stages_sign_intersection()[\
			#val_netw.get_di_intersections()[val_netw.get_di_entry_links_to_network()[self._id_entry_link].\
			#get_id_head_intersection_node()].get_intersection_control_obj().get_id_actuated_stage()]:
		
				#if there is at least one  queue in the link, having flows > f_min, we do not need to update the  decision
				
				#if val_netw.get_di_all_links()[j[0]].fct_examing_existence_que_actuates_stage_with_flow_sup_given_value(\
						#val_network=val_netw,val_fmin=val_min_allowed_flow_depart_link)==1:
							#return 0
			if val_netw.get_di_intersections()[val_netw.get_di_entry_links_to_network()[self._id_entry_link].get_id_head_intersection_node()].\
			fct_examing_existence_que_actuates_stage_with_flow_sup_given_value(\
			val_network=val_netw,val_fmin=val_min_allowed_flow_depart_link)==1:
				return 0
			return 1
	
		#if we have  planned a control revision 
		elif val_netw.get_di_intersections()[val_netw.get_di_entry_links_to_network()[self._id_entry_link].\
		get_id_head_intersection_node()].get_t_last_request_ctrl_update_when_record_flux()>0:
		
			#if the time at which the ctrl revision is planned is the current time
			if val_netw.get_di_intersections()[val_netw.get_di_entry_links_to_network()[self._id_entry_link].\
			get_id_head_intersection_node()].get_t_last_request_ctrl_update_when_record_flux()==self._event_time:
				return 0
				
			#if the time at which the ctrl revision is planned is  not the current time
			else:
				#if the type of the ctrl is FA
				if Cl_Control_Actuate.TYPE_CONTROL[val_netw.get_di_intersections()[val_netw.get_di_entry_links_to_network()[self._id_entry_link].\
				get_id_head_intersection_node()].get_intersection_control_obj().get_type_control()]==Cl_Control_Actuate.TYPE_CONTROL[12] or\
				Cl_Control_Actuate.TYPE_CONTROL[val_netw.get_di_intersections()[val_netw.get_di_entry_links_to_network()[self._id_entry_link].\
				get_id_head_intersection_node()].get_intersection_control_obj().get_type_control()]==Cl_Control_Actuate.TYPE_CONTROL[10]:
				
					print("PROBLEM IN CL_EV_VEH APPEAR, FCT fct_exam_whether_ctrl_decision_should_be_updated_when_record_flux, t request ctrl update: ",\
					val_netw.get_di_intersections()[val_netw.get_di_entry_links_to_network()[self._id_entry_link].\
					get_id_head_intersection_node()].get_t_last_request_ctrl_update_when_record_flux(),"t_cur",self._event_time)
					import sys
					sys.exit()
				#if the type of the ctrl is FA MG
				elif Cl_Control_Actuate.TYPE_CONTROL[val_netw.get_di_intersections()[val_netw.get_di_entry_links_to_network()[self._id_entry_link].\
				get_id_head_intersection_node()].get_intersection_control_obj().get_type_control()]==Cl_Control_Actuate.TYPE_CONTROL[11]:
				
					#if there is at least one queue of the actuated stage having flow >f_min, the decision will not be updated
					#for j in val_netw.get_di_intersections()[val_netw.get_di_entry_links_to_network()[self._id_entry_link].\
					#get_id_head_intersection_node()].get_di_stages_sign_intersection()[\
					#val_netw.get_di_intersections()[val_netw.get_di_entry_links_to_network()[self._id_entry_link].\
					#get_id_head_intersection_node()].get_intersection_control_obj().get_id_actuated_stage()]:
		
						#if there is at least one  queue in the link, having flows > f_min, we do not need to update the  decision
						#if val_netw.get_di_all_links()[j[0]].fct_examing_existence_que_actuates_stage_with_flow_sup_given_value(\
						#val_network=val_netw,val_fmin=val_min_allowed_flow_depart_link)==1:
							#return 0
					if val_netw.get_di_intersections()[val_netw.get_di_entry_links_to_network()[self._id_entry_link].get_id_head_intersection_node()].\
					fct_examing_existence_que_actuates_stage_with_flow_sup_given_value(\
					val_network=val_netw,val_fmin=val_min_allowed_flow_depart_link)==1:
						return 0
					return 1
				#if the type of the ctrl is not FA MG
				else:
					print("PROBLEM IN CL_EV_VEH APPEAR, FCT fct_exam_whether_ctrl_decision_should_be_updated_when_record_flux, type ctrl: ",\
					val_netw.get_di_intersections()[val_netw.get_di_entry_links_to_network()[self._id_entry_link].\
					get_id_head_intersection_node()].get_intersection_control_obj().get_type_control())
					import sys
					sys.exit()
		
		else:
			print("PROBLEM IN CL_EV_VEH APPEAR, FCT fct_exam_whether_ctrl_decision_should_be_updated,_when_record_flux  t request ctrl update: ",\
			val_netw.get_di_intersections()[val_netw.get_di_entry_links_to_network()[self._id_entry_link].get_id_head_intersection_node()].get_t_request_ctrl_update())
			import sys
			sys.exit()
			#if there is at least one queue of the actuated stage having flow >f_min, the decision will not be updated
			#for j in val_netw.get_di_intersections()[val_netw.get_di_entry_links_to_network()[self._id_entry_link].\
			#get_id_head_intersection_node()].get_di_stages_sign_intersection()[\
			#val_netw.get_di_intersections()[val_netw.get_di_entry_links_to_network()[self._id_entry_link].\
			#get_id_head_intersection_node()].get_intersection_control_obj().get_id_actuated_stage()]:
		
				#if there is at least one  queue in the link, having flows > f_min, we do not need to update the  decision
				#if val_netw.get_di_all_links()[j[0]].fct_examing_existence_que_actuates_stage_with_flow_sup_given_value(\
				#val_network=val_netw,val_fmin=val_min_allowed_flow_depart_link)==1:
					#return 0
			if val_netw.get_di_intersections()[val_netw.get_di_entry_links_to_network()[self._id_entry_link].get_id_head_intersection_node()].\
			fct_examing_existence_que_actuates_stage_with_flow_sup_given_value(\
			val_network=val_netw,val_fmin=val_min_allowed_flow_depart_link)==1:
				return 0
			return 1
		
#*****************************************************************************************************************************************************************************************
#*****************************************************************************************************************************************************************************************

#****************************************************************************Cas New Demand-no OD-without sensor monit ******************************************************

	#method treating the case when a veh appears, a new generated demand is being considered, the vehicle final destination is not predefined
	# the employed control does not require  sensor monitoring for the t at which is should  be revised 
	def fct_treat_case_veh_appear_new_demand_final_dest_and_path_dynam_defined_without_sensor_monit(self,\
	v_val_veh_id,v_val_netwk,v_val_type_veh_final_destination,v_val_min_veh_hold_time,v_val_prec_round,\
	v_val_ev_list,v_file_recording_event_db):
	

		t_appear_next_veh=round(self._event_time+v_val_netwk.get_di_entry_links_to_network()\
		[self._id_entry_link].fct_creating_demand_entry_link(),v_val_prec_round)
		
		#creation of the next vehicle
		next_veh=Cl_Vehicle.Vehicle(val_t_veh_appearance_at_network=t_appear_next_veh,\
		val_id_entry_link_veh_ap=self._id_entry_link)
		
		#creation of the next vehicle appearance event
		ev_new_veh_ap=Ev_veh_appearance(val_event_t=t_appear_next_veh,\
		val_vehicle=next_veh)
		
		#we insert the event in the event list
		ev_new_veh_ap.fct_insertion_even_in_event_list(event_list=v_val_ev_list,\
		message="IN CL_EV_VEH_APPEARANCE IN FUNCT \
		fct_treat_case_veh_appear_new_demand_final_dest_and_path_dynam_defined_without_sensor_monit \
		NEXT VEH APPEARANCE EVENT HAS TIME < TIME FIRST EVENT IN THE LIST")
		
		#we attribute the id to the vehicle
		self._vehicle.set_id_veh(v_val_veh_id)
		self._vehicle.set_type_vehicle_final_destination(v_val_type_veh_final_destination)
		
		#we update the vehicle, we indicate the id of the new link location and the time at which it arrived at the new link
		self._vehicle.fct_veh_update_when_appear_at_link(self._id_entry_link,self._event_time)
		
		#we update the number of vehicles in the  link
		#even in the case of infinite management of the internal links; that's why we avoid a test examining if the destination link
		#is  not exit link  but internal if  finite capacity 
		#v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].set_current_nb_veh_link(\
		#v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].get_current_nb_veh_link()+1)
		
		#if v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].\
		#get_id_head_intersection_node()==37605:
			#print("id nd",v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].\
			#get_id_head_intersection_node(),"here1",v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].\
			#get_id_head_intersection_node()].get_current_di_cum_rout_prob())
			#import sys
			#sys.exit()
		
		#param for the chosen queue
		lis_param_fct_calcul_queue_chosen_by_veh_from_cum_fct=[self._id_entry_link,\
		v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].\
		get_id_head_intersection_node()].get_current_di_cum_rout_prob()]
		
		
		
		rep=self._obj_decisions.fct_calcul_queue_chosen_by_veh_from_cum_fct(\
		*lis_param_fct_calcul_queue_chosen_by_veh_from_cum_fct)
			
		lis_param_fct_calcul_queue_chosen_by_veh=[self._id_entry_link,rep[List_Explicit_Values.val_third_element_of_list],v_val_netwk]
		
		
		queue_phase=self._obj_decisions.fct_calcul_queue_chosen_by_veh(*lis_param_fct_calcul_queue_chosen_by_veh)
		
		
		#we update the vehicle, we indicate the chosen queue and its arrival time in the queue
		self._vehicle.fct_update_veh_after_choosing_queue(queue_phase,self._event_time,v_val_netwk)
			
		t_end_veh_hold_time=round(self._event_time+v_val_min_veh_hold_time,v_val_prec_round)
			
		#we examine if there are other vehicles in the que
		if v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].\
		get_queue_veh()==[]:
			other_veh_in_que_before_add_veh=0
		else:
			other_veh_in_que_before_add_veh=1
			
		#we update queue (add the vehicle in the queue)
		v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].\
		fct_update_veh_queue_when_veh_prohibited_to_leave_no_mod(self._vehicle)
			
		#we indicate the time at which the vehicle hold in the queue  ceases
		self._vehicle.set_t_end_veh_hold_time_que(t_end_veh_hold_time)
		
		#if there are no veh in the que (otherwise veh will keave with ev end veh departure) 
		if other_veh_in_que_before_add_veh==0:
			
			#creat ev_end_hold_time
			ev_end_hold_time=Cl_Ev_end_veh_hold_at_que.Ev_end_veh_hold_at_que(val_event_t= t_end_veh_hold_time,\
			val_id_que=queue_phase.get_associated_phase_to_queue())
					
			#we add the event in the event list
			ev_end_hold_time.fct_insertion_even_in_event_list(event_list=v_val_ev_list,\
			message="IN CL_EV_VEH_APPEARANCE IN FUNCT fct_treat_case_veh_appear_new_demand_final_dest_and_path_dynam_defined_no_sensor_monit,\
			EVENT END HOLD TIME HAS TIME < TIME FIRST EVENT IN THE LIST")

		li_id_veh=[]
		for i in v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].get_set_veh_queue().\
		get_di_obj_veh_queue_at_link()\
		[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].get_queue_veh():
		
			li_id_veh.append(i.get_id_veh())
		
		#we create an record database object 
		record_db_obj=Cl_Record_Database.Record_Database(\
		val_file_db=v_file_recording_event_db,\
		val_ev_time=self._event_time,\
		val_ev_type=self._event_type,\
		val_id_inters_node=v_val_netwk.get_di_entry_links_to_network()[\
		queue_phase.get_associated_phase_to_queue()[0]].get_id_head_intersection_node(),\
		val_type_inters_node=v_val_netwk.get_di_intersections()[\
		v_val_netwk.get_di_entry_links_to_network()[\
		queue_phase.get_associated_phase_to_queue()[0]].get_id_head_intersection_node()].get_type_intersection(),\
		val_current_inters_matrix_with_the_associated_link_of_phase=\
		v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_links_to_network()[queue_phase.get_associated_phase_to_queue()[0]].\
		get_id_head_intersection_node()].\
		get_intersection_control_obj().get_di_intersection_control_mat(),\
		val_vehicle_id=self._vehicle.get_id_veh(),\
		val_time_veh_appearance_in_network=self._vehicle.get_t_veh_appearance_at_network(),\
		val_id_veh_entry_link=self._vehicle.get_id_entry_link_veh_ap(),\
		val_id_current_link_veh_location=self._vehicle.get_current_id_link_veh_location(),\
		val_time_veh_arrival_at_current_link=self._vehicle.get_t_vehicle_arrival_at_current_link(),\
		val_veh_current_queue_location=self._vehicle.get_veh_current_queue_location(),\
		val_time_veh_arrival_at_current_queue=self._vehicle.get_t_vehicle_arrival_at_current_queue(),\
		val_veh_id_destination_link=self._vehicle.get_veh_current_queue_location()[List_Explicit_Values.val_second_element_of_list],\
		val_id_event_link=self._id_entry_link,\
		val_current_achieved_queue_service_rate_including_current_vehicle=\
		v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].\
		get_current_reached_service_rate(),\
		val_current_queue_service_rate=\
		v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].\
		get_current_queue_service_rate(),\
		val_li_id_vehicles_in_queue=li_id_veh,\
		val_nb_veh_in_ar_lk=v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].get_current_nb_veh_link())
		
		#we record the event in the db 
		record_db_obj.fct_write_object_in_db_file()
		
#*****************************************************************************************************************************************************************************************
#*****************************************************************************************************************************************************************************************

#****************************************************************************Cas New Demand-no OD-with sensor monit **********************************************************
	#method treating the case when a veh appears, a new generated demand is being considered, the vehicle final destination is not predefined
	# the employed control requires  sensor monitoring for the t at which is should  be revised and the turning probabilities are not going to be estimated
	def fct_treat_case_veh_appear_new_demand_final_dest_and_path_dynam_defined_with_sensor_monit(self,\
	v_val_veh_id,v_val_netwk,v_val_type_veh_final_destination,v_val_min_veh_hold_time,v_val_ti_ctrl_revision_if_decided,\
	v_val_prec_round,v_val_ev_list,v_file_recording_event_db,val_min_nb_vehicles_to_detect):
	
		
		t_appear_next_veh=round(self._event_time+v_val_netwk.get_di_entry_links_to_network()\
		[self._id_entry_link].fct_creating_demand_entry_link(),v_val_prec_round)
		
		#creation of the next vehicle
		next_veh=Cl_Vehicle.Vehicle(val_t_veh_appearance_at_network=t_appear_next_veh,\
		val_id_entry_link_veh_ap=self._id_entry_link)
		
		#creation of the next vehicle appearance event
		ev_new_veh_ap=Ev_veh_appearance(val_event_t=t_appear_next_veh,\
		val_vehicle=next_veh)
		
		#we insert the event in the event list
		ev_new_veh_ap.fct_insertion_even_in_event_list(event_list=v_val_ev_list,\
		message="IN CL_EV_VEH_APPEARANCE IN FUNCT \
		fct_treat_case_veh_appear_new_demand_final_dest_and_path_dynam_defined_with_sensor_monit \
		NEXT VEH APPEARANCE EVENT HAS TIME < TIME FIRST EVENT IN THE LIST")
		
		#we attribute the id to the vehicle
		self._vehicle.set_id_veh(v_val_veh_id)
		
		self._vehicle.set_type_vehicle_final_destination(v_val_type_veh_final_destination)
	
		
		#we update the vehicle, we indicate the id of the new link location and the time at which it arrived at the new link
		self._vehicle.fct_veh_update_when_appear_at_link(self._id_entry_link,self._event_time)
		
		#we update the number of vehicles in the  link
		#even in the case of infinite management of the internal links; that's why we avoid a test examining if the destination link
		#is  not exit link  but internal if  finite capacity 
		#v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].set_current_nb_veh_link(\
		#v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].get_current_nb_veh_link()+1)
		
		
		#param for the chosen queue
		lis_param_fct_calcul_queue_chosen_by_veh_from_cum_fct=[self._id_entry_link,\
		v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].\
		get_id_head_intersection_node()].get_current_di_cum_rout_prob()]
		
		rep=self._obj_decisions.fct_calcul_queue_chosen_by_veh_from_cum_fct(\
		*lis_param_fct_calcul_queue_chosen_by_veh_from_cum_fct)
			
		lis_param_fct_calcul_queue_chosen_by_veh=[self._id_entry_link,rep[List_Explicit_Values.val_third_element_of_list],v_val_netwk]
		
		queue_phase=self._obj_decisions.fct_calcul_queue_chosen_by_veh(*lis_param_fct_calcul_queue_chosen_by_veh)
		
		
		#we update the vehicle, we indicate the chosen queue and its arrival time in the queue
		self._vehicle.fct_update_veh_after_choosing_queue(queue_phase,self._event_time,v_val_netwk)
			
		t_end_veh_hold_time=round(self._event_time+v_val_min_veh_hold_time,v_val_prec_round)
			
		#we examine if there are other vehicles in the que
		if v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].\
		get_queue_veh()==[]:
			other_veh_in_que_before_add_veh=0
		else:
			other_veh_in_que_before_add_veh=1
			
		#we update queue (add the vehicle in the queue)
		v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].\
		fct_update_veh_queue_when_veh_prohibited_to_leave_no_mod(self._vehicle)
			
		#we indicate the time at which the vehicle hold in the queue  ceases
		self._vehicle.set_t_end_veh_hold_time_que(t_end_veh_hold_time)
		
		#if there are no veh in the que (otherwise veh will keave with ev end veh departure) 
		if other_veh_in_que_before_add_veh==0:
			
			#creat ev_end_hold_time
			ev_end_hold_time=Cl_Ev_end_veh_hold_at_que.Ev_end_veh_hold_at_que(val_event_t= t_end_veh_hold_time,\
			val_id_que=queue_phase.get_associated_phase_to_queue())
					
			#we add the event in the event list
			ev_end_hold_time.fct_insertion_even_in_event_list(event_list=v_val_ev_list,\
			message="IN CL_EV_VEH_APPEARANCE IN FUNCT \
			fct_treat_case_veh_appear_new_demand_final_dest_and_path_dynam_defined_with_sensor_monit \
			EVENT END HOLD TIME HAS TIME < TIME FIRST EVENT IN THE LIST")
			
		#if the queue is not a right turn 
		if queue_phase.get_type_veh_queue()!=Cl_Vehicle_Queue.TYPE_VEHICLE_QUEUE["right_turn"]:

			#if there is at least one detector detecting the veh
			if queue_phase.fct_exam_whether_at_least_nb_veh_detected_by_a_que_sensor(val_min_nb_veh_to_detect=val_min_nb_vehicles_to_detect)!=None:
			
				
				# controle revision
				ev_end_deci_next_icm=Cl_Ev_end_decision_next_intersection_control.Ev_end_decision_next_intersection_control(\
				val_ev_time=v_val_ti_ctrl_revision_if_decided,\
				val_id_intersection_node=v_val_netwk.get_di_all_links()[self._id_entry_link].get_id_head_intersection_node(),\
				val_type_control_to_employ=\
				v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].\
				get_id_head_intersection_node()].get_ctrl_actuate_obj().get_type_employed_ctrl(),\
				val_control_category="sensor_requirement")
				#,val_reason_ctrl_revision_t_lim=0)	
		
				#on insert the event ev_end_dec_next_icm into the event list
				ev_end_deci_next_icm.fct_insertion_even_in_event_list(event_list=v_val_ev_list,\
				message="IN CL_Ev_appear IN FUNCT \
				fct_treat_case_veh_appear_new_demand_final_dest_and_path_dynam_defined_with_sensor_monit \
				NEXT ev_new_end_dec_netw_control EVENT HAS TIME < TIME FIRST EVENT IN THE LIST")
				
				#we indicate the intersection that a ctrl request is made
				#v_val_netwk.get_di_intersections()[v_val_netwk.get_di_all_links()[self._id_entry_link].get_id_head_intersection_node()].\
				#set_t_last_request_ctrl_revision_when_flux_monitoring(v_val_ti_ctrl_revision_if_decided)
				
				#we indicate the number of times a control revision is asked for the same time
				#v_val_netwk.get_di_intersections()[v_val_netwk.get_di_all_links()[self._id_entry_link].get_id_head_intersection_node()].\
				#set_nb_times_ctrl_revision_corresponding_to_t_last_request_ctrl_revision_when_flux_monitoring(\
				#v_val_netwk.get_di_intersections()[v_val_netwk.get_di_all_links()[self._id_entry_link].get_id_head_intersection_node()].\
				#set_nb_times_ctrl_revision_corresponding_to_t_last_request_ctrl_revision_when_flux_monitoring()+1)
	
		
		li_id_veh=[]
		for i in v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[queue_phase.get_associated_phase_to_queue()[0],\
		queue_phase.get_associated_phase_to_queue()[1]].get_queue_veh():
					
			li_id_veh.append(i.get_id_veh())
				
		#we create an record database object 
		record_db_obj=Cl_Record_Database.Record_Database(\
		val_file_db=v_file_recording_event_db,\
		val_ev_time=self._event_time,\
		val_ev_type=self._event_type,\
		val_id_inters_node=[v_val_netwk.get_di_entry_links_to_network()[\
		queue_phase.get_associated_phase_to_queue()[0]].get_id_head_intersection_node()],\
		val_t_start_current_inters_control=v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_links_to_network()[\
		queue_phase.get_associated_phase_to_queue()[0]].\
		get_id_head_intersection_node()].get_intersection_control_obj().get_t_start_control(),\
		val_duration_current_inters_control=v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_links_to_network()[\
		queue_phase.get_associated_phase_to_queue()[0]].\
		get_id_head_intersection_node()].get_intersection_control_obj().get_duration_control(),\
		val_current_inters_matrix_with_the_associated_link_of_phase=\
		v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_links_to_network()[\
		queue_phase.get_associated_phase_to_queue()[0]].get_id_head_intersection_node()].\
		get_intersection_control_obj().\
		get_di_intersection_control_mat(),\
		val_duration_current_cycle=v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_links_to_network()[\
		queue_phase.get_associated_phase_to_queue()[0]].\
		get_id_head_intersection_node()].get_intersection_control_obj().\
		get_cycle_duration_associated_with_control(),\
		val_vehicle_id=self._vehicle.get_id_veh(),\
		val_time_veh_appearance_in_network=self._vehicle.get_t_veh_appearance_at_network(),\
		val_id_veh_entry_link=self._vehicle.get_id_entry_link_veh_ap(),\
		val_id_current_link_veh_location=self._vehicle.get_current_id_link_veh_location(),\
		val_time_veh_arrival_at_current_link=self._vehicle.get_t_vehicle_arrival_at_current_link(),\
		val_time_veh_departure_from_current_link=self._vehicle.get_t_vehicle_departure_from_current_link(),\
		val_veh_current_queue_location=self._vehicle.get_veh_current_queue_location(),\
		val_time_veh_arrival_at_current_queue=self._vehicle.get_t_vehicle_arrival_at_current_queue(),\
		val_time_veh_start_departure_from_current_queue=self._vehicle.get_t_vehicle_started_departure_from_current_queue(),\
		val_time_veh_departure_from_current_queue=self._vehicle.get_t_vehicle_departure_from_current_queue(),\
		val_veh_id_destination_link=self._vehicle.get_veh_current_queue_location()[List_Explicit_Values.val_second_element_of_list],\
		val_time_veh_exit_from_network=self._vehicle.get_t_exit_veh_from_network(),\
		val_id_event_link=self._id_entry_link,\
		#val_veh_can_leave_now=veh_can_leave_que,\
		val_current_achieved_queue_service_rate_including_current_vehicle=\
		v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].\
		get_current_reached_service_rate(),\
		val_current_queue_service_rate=\
		v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].\
		get_current_queue_service_rate(),\
		val_li_id_vehicles_in_queue=li_id_veh,\
		val_nb_veh_in_ar_lk=v_val_netwk.get_di_all_links()[i.get_current_id_link_veh_location()].get_current_nb_veh_link())
		#val_prob_rout_prop_current_lk=val_netwk.get_dict_mat_od_key_id_entry_internal_lk_value_list_dest_lks()[\
		#queue_phase.get_associated_phase_to_queue()[0]])	
						
		#we record the event in the db 
		record_db_obj.fct_write_object_in_db_file()
	
	#*****************************************************************************************************************************************************************************************
	#*****************************************************************************************************************************************************************************************
	
	#***************************************************Cas New Demand-with OD and given path-without sensor monit *************************************************************	
	#method treating the case when a veh appears, a new generated demand is being considered, the vehicle final destination anf the entire veh path are predefined
	# the employed control does not require  sensor monitoring for the t at which is should  be revised 
	def fct_treat_case_veh_appear_new_demand_final_dest_and_path_intial_defined_without_sensor_monit(self,\
	v_val_veh_id,v_val_netwk,v_val_type_veh_final_destination,v_val_min_veh_hold_time,v_val_prec_round,v_val_ev_list,v_file_recording_event_db):
	
		t_appear_next_veh=round(self._event_time+v_val_netwk.get_di_entry_links_to_network()\
		[self._id_entry_link].fct_creating_demand_entry_link(),v_val_prec_round)
		
		#creation of the next vehicle
		next_veh=Cl_Vehicle.Vehicle(val_t_veh_appearance_at_network=t_appear_next_veh,\
		val_id_entry_link_veh_ap=self._id_entry_link)
		
		#creation of the next vehicle appearance event
		ev_new_veh_ap=Ev_veh_appearance(val_event_t=t_appear_next_veh,\
		val_vehicle=next_veh)
		
		#we insert the event in the event list
		ev_new_veh_ap.fct_insertion_even_in_event_list(event_list=v_val_ev_list,\
		message="IN CL_EV_VEH_APPEARANCE IN FUNCT event_treat ,\
		NEXT VEH APPEARANCE EVENT HAS TIME < TIME FIRST EVENT IN THE LIST")
		
		#we attribute the id to the vehicle
		self._vehicle.set_id_veh(v_val_veh_id)
		self._vehicle.set_type_vehicle_final_destination(v_val_type_veh_final_destination)
		
		#we update the vehicle, we indicate the id of the new link location and the time at which it arrived at the new link
		self._vehicle.fct_veh_update_when_appear_at_link(self._id_entry_link,self._event_time)
		
		#we decide  the veh final destination
		#li_rep=[unif nb, id current veh loca, selected id exit link ]
		li_rep=self._obj_decisions.fct_calcul_exit_lk_chosen_by_veh_cas_given_final_destination(\
		id_veh_entry_link=self._id_entry_link,\
		di_cum_mod=v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].\
		get_id_head_intersection_node()].get_current_di_cum_mod())
		
		#we indicate the veh exit link for the record
		veh_exit_lk=li_rep[2]
		
		#we associate the final dest to the vehicle 
		self._vehicle.set_id_veh_final_destination_link(li_rep[2])
		
		#we update the indicator of the veh current location  in the que
		new_v=self._vehicle.get_index_current_veh_link_location_in_path_list_when_given_destination()+1
			
		self._vehicle.set_index_current_veh_link_location_in_path_list_when_given_destination(new_v)
		
		#we update the number of vehicles in the  link
		#even in the case of infinite management of the internal links; that's why we avoid a test examining if the destination link
		#is  not exit link  but internal if  finite capacity 
		#v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].set_current_nb_veh_link(\
		#v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].get_current_nb_veh_link()+1)
					
		#we decide the que chosen by the vehicle
		li_param_fct_calcul_que_chosen_by_veh=[self._id_entry_link,self._id_entry_link,\
		self._vehicle.get_id_veh_final_destination_link(),\
		self._vehicle.get_index_current_veh_link_location_in_path_list_when_given_destination(),\
		v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].get_id_head_intersection_node()].\
		get_current_di_unique_paths(),v_val_netwk]
		
		#the vehicle queue  object chosen for the vehicle to join in
		queue_phase=self._obj_decisions.fct_calcul_queue_chosen_by_veh_cas_given_final_destination(*\
		li_param_fct_calcul_que_chosen_by_veh)
		
		#we update the vehicle, we indicate the chosen queue and its arrival time in the queue
		self._vehicle.fct_update_veh_after_choosing_queue(queue_phase,self._event_time,v_val_netwk)
			
		t_end_veh_hold_time=round(self._event_time+v_val_min_veh_hold_time,v_val_prec_round)
		
		#we examine if there are other vehicles in the que
		if v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].\
		get_queue_veh()==[]:
			other_veh_in_que_before_add_veh=0
		else:
			other_veh_in_que_before_add_veh=1
			
		#we update queue (add the vehicle in the queue)
		v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].\
		fct_update_veh_queue_when_veh_prohibited_to_leave_no_mod(self._vehicle)
		
		#we indicate the time at which the vehicle hold in the queue  ceases
		self._vehicle.set_t_end_veh_hold_time_que(t_end_veh_hold_time)
		
		#if there are no veh in the que (otherwise veh will keave with ev end veh departure) 
		if other_veh_in_que_before_add_veh==0:
			
			#creat ev_end_hold_time
			ev_end_hold_time=Cl_Ev_end_veh_hold_at_que.Ev_end_veh_hold_at_que(val_event_t= t_end_veh_hold_time,\
			val_id_que=queue_phase.get_associated_phase_to_queue())
					
			#we add the event in the event list
			ev_end_hold_time.fct_insertion_even_in_event_list(event_list=v_val_ev_list,\
			message="IN CL_EV_VEH_APPEARANCE IN FUNCT fct_treat_case_veh_appear_new_demand_final_dest_and_path_dynam_defined_no_sensor_monit,\
			EVENT END HOLD TIME HAS TIME < TIME FIRST EVENT IN THE LIST")
			
		li_id_veh=[]
		for i in v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].get_set_veh_queue().\
		get_di_obj_veh_queue_at_link()\
		[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].get_queue_veh():
		
			li_id_veh.append(i.get_id_veh())
		
		#we create an record database object 
		record_db_obj=Cl_Record_Database.Record_Database(\
		val_file_db=v_file_recording_event_db,\
		val_ev_time=self._event_time,\
		val_ev_type=self._event_type,\
		val_id_inters_node=v_val_netwk.get_di_entry_links_to_network()[\
		queue_phase.get_associated_phase_to_queue()[0]].get_id_head_intersection_node(),\
		val_type_inters_node=v_val_netwk.get_di_intersections()[\
		v_val_netwk.get_di_entry_links_to_network()[\
		queue_phase.get_associated_phase_to_queue()[0]].get_id_head_intersection_node()].get_type_intersection(),\
		val_current_inters_matrix_with_the_associated_link_of_phase=\
		v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_links_to_network()[queue_phase.get_associated_phase_to_queue()[0]].\
		get_id_head_intersection_node()].\
		get_intersection_control_obj().get_di_intersection_control_mat(),\
		val_vehicle_id=self._vehicle.get_id_veh(),\
		val_time_veh_appearance_in_network=self._vehicle.get_t_veh_appearance_at_network(),\
		val_id_veh_entry_link=self._vehicle.get_id_entry_link_veh_ap(),\
		val_id_current_link_veh_location=self._vehicle.get_current_id_link_veh_location(),\
		val_time_veh_arrival_at_current_link=self._vehicle.get_t_vehicle_arrival_at_current_link(),\
		val_veh_current_queue_location=self._vehicle.get_veh_current_queue_location(),\
		val_time_veh_arrival_at_current_queue=self._vehicle.get_t_vehicle_arrival_at_current_queue(),\
		val_veh_id_destination_link=self._vehicle.get_veh_current_queue_location()[List_Explicit_Values.val_second_element_of_list],\
		val_id_event_link=self._id_entry_link,\
		val_current_achieved_queue_service_rate_including_current_vehicle=\
		v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].\
		get_current_reached_service_rate(),\
		val_current_queue_service_rate=\
		v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].\
		get_current_queue_service_rate(),\
		val_li_id_vehicles_in_queue=li_id_veh,\
		val_nb_veh_in_ar_lk=v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].get_current_nb_veh_link(),\
		val_id_veh_final_dest_exit_lk=self._vehicle.get_id_veh_final_destination_link())
		
		#we record the event in the db 
		record_db_obj.fct_write_object_in_db_file()
		
#*****************************************************************************************************************************************************************************************
	
#**************************************************Cas New Demand-with OD and given path-with sensor monit *****************************************************************

	#method treating the case when a veh appears, a new generated demand is being considered, the vehicle final destination and entire path are predefined
	# the employed control requires  sensor monitoring for the t at which is should  be revised 
	def fct_treat_case_veh_appear_new_demand_final_dest_and_path_intial_defined_with_sensor_monit(self,\
	v_val_veh_id,v_val_netwk,v_val_type_veh_final_destination,v_val_min_veh_hold_time,v_val_prec_round,\
	v_val_ev_list,v_val_ti_ctrl_revision_if_decided,\
	v_file_recording_event_db,val_min_nb_vehicles_to_detect):
	
		t_appear_next_veh=round(self._event_time+v_val_netwk.get_di_entry_links_to_network()\
		[self._id_entry_link].fct_creating_demand_entry_link(),v_val_prec_round)
		
		#creation of the next vehicle
		next_veh=Cl_Vehicle.Vehicle(val_t_veh_appearance_at_network=t_appear_next_veh,\
		val_id_entry_link_veh_ap=self._id_entry_link)
		
		#creation of the next vehicle appearance event
		ev_new_veh_ap=Ev_veh_appearance(val_event_t=t_appear_next_veh,\
		val_vehicle=next_veh)
		
		#we insert the event in the event list
		ev_new_veh_ap.fct_insertion_even_in_event_list(event_list=v_val_ev_list,\
		message="IN CL_EV_VEH_APPEARANCE IN FUNCT,\
		fct_treat_case_veh_appear_new_demand_final_dest_and_path_intial_defined_with_sensor_monit,\
		NEXT VEH APPEARANCE EVENT HAS TIME < TIME FIRST EVENT IN THE LIST")
		
		#we attribute the id to the vehicle
		self._vehicle.set_id_veh(v_val_veh_id)
		
		self._vehicle.set_type_vehicle_final_destination(v_val_type_veh_final_destination)
		
		#we update the vehicle, we indicate the id of the new link location and the time at which it arrived at the new link
		self._vehicle.fct_veh_update_when_appear_at_link(self._id_entry_link,self._event_time)
		
		#we decide  the veh final destination
		#li_rep=[unif nb, id current veh loca, selected id exit link ]
		li_rep=self._obj_decisions.fct_calcul_exit_lk_chosen_by_veh_cas_given_final_destination(\
		id_veh_entry_link=self._id_entry_link,\
		di_cum_mod=v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].\
		get_id_head_intersection_node()].get_current_di_cum_mod())
			
		#we indicate the veh exit link for the record
		veh_exit_lk=li_rep[2]
			
		#we associate the final dest to the vehicle 
		self._vehicle.set_id_veh_final_destination_link(li_rep[2])
		
		#we update the indicator of the veh current location  in the que
		new_v=self._vehicle.get_index_current_veh_link_location_in_path_list_when_given_destination()+1
			
		self._vehicle.set_index_current_veh_link_location_in_path_list_when_given_destination(new_v)
		
		#we update the number of vehicles in the  link
		#even in the case of infinite management of the internal links; that's why we avoid a test examining if the destination link
		#is  not exit link  but internal if  finite capacity 
		#v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].set_current_nb_veh_link(\
		#v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].get_current_nb_veh_link()+1)
					
		#we decide the que chosen by the vehicle
		li_param_fct_calcul_que_chosen_by_veh=[self._id_entry_link,self._id_entry_link,\
		self._vehicle.get_id_veh_final_destination_link(),\
		self._vehicle.get_index_current_veh_link_location_in_path_list_when_given_destination(),\
		v_val_netwk.get_di_intersections()[val_netwrk.get_di_entry_links_to_network()[self._id_entry_link].get_id_head_intersection_node()].\
		get_current_di_unique_paths(),v_val_netwk]
		
		#the vehicle queue  object chosen for the vehicle to join in
		queue_phase=self._obj_decisions.fct_calcul_queue_chosen_by_veh_cas_given_final_destination(*\
		li_param_fct_calcul_que_chosen_by_veh)
		
		#we update the vehicle, we indicate the chosen queue and its arrival time in the queue
		self._vehicle.fct_update_veh_after_choosing_queue(queue_phase,self._event_time,v_val_netwk)
			
		t_end_veh_hold_time=round(self._event_time+v_val_min_veh_hold_time,v_val_prec_round)
		
		#we examine if there are other vehicles in the que
		if v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].\
		get_queue_veh()==[]:
			other_veh_in_que_before_add_veh=0
		else:
			other_veh_in_que_before_add_veh=1
			
		#we update queue (add the vehicle in the queue)
		v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].\
		fct_update_veh_queue_when_veh_prohibited_to_leave_no_mod(self._vehicle)
			
		#we indicate the time at which the vehicle hold in the queue  ceases
		self._vehicle.set_t_end_veh_hold_time_que(t_end_veh_hold_time)
		
		#if there are no veh in the que (otherwise veh will keave with ev end veh departure) 
		if other_veh_in_que_before_add_veh==0:
			
			#creat ev_end_hold_time
			ev_end_hold_time=Cl_Ev_end_veh_hold_at_que.Ev_end_veh_hold_at_que(val_event_t= t_end_veh_hold_time,\
			val_id_que=queue_phase.get_associated_phase_to_queue())
					
			#we add the event in the event list
			ev_end_hold_time.fct_insertion_even_in_event_list(event_list=v_val_ev_list,\
			message="IN CL_EV_VEH_APPEARANCE IN FUNCT \
			fct_treat_case_veh_appear_new_demand_final_dest_and_path_intial_defined_with_sensor_monit \
			EVENT END HOLD TIME HAS TIME < TIME FIRST EVENT IN THE LIST")
			
		#if the queue is not a right turn 
		if queue_phase.get_type_veh_queue()!=Cl_Vehicle_Queue.TYPE_VEHICLE_QUEUE["right_turn"]:
			
			#if there is at least one detector detecting the veh
			if queue_phase.fct_exam_whether_at_least_nb_veh_detected_by_a_que_sensor(val_min_nb_veh_to_detect=val_min_nb_vehicles_to_detect)!=None:
							
				# controle dec update
				ev_end_deci_next_icm=Cl_Ev_end_decision_next_intersection_control.Ev_end_decision_next_intersection_control(\
				val_ev_time=v_val_ti_ctrl_revision_if_decided,\
				val_id_intersection_node=v_val_netwk.get_di_all_links()[self._id_entry_link].get_id_head_intersection_node(),\
				val_type_control_to_employ=\
				v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].\
				get_id_head_intersection_node()].get_ctrl_actuate_obj().get_type_employed_ctrl(),\
				val_control_category="sensor_requirement")
				#,val_reason_ctrl_revision_t_lim=0)	
		
				#on insert the event ev_end_dec_next_icm into the event list
				ev_end_deci_next_icm.fct_insertion_even_in_event_list(event_list=v_val_ev_list,\
				message="IN CL_Ev_appear IN FUNCT \
				fct_treat_case_veh_appear_new_demand_final_dest_and_path_intial_defined_with_sensor_monit\
				NEXT ev_new_end_dec_netw_control EVENT HAS TIME < TIME FIRST EVENT IN THE LIST")
				
				#we indicate the intersection that a ctrl request is made
				#v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].get_id_head_intersection_node()].\
				#set_t_last_request_ctrl_revision_when_flux_monitoring(v_val_ti_ctrl_revision_if_decided)
				
				#we indicate the number of times a control revision is asked for the same time
				#v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].get_id_head_intersection_node()].\
				#set_nb_times_ctrl_revision_corresponding_to_t_last_request_ctrl_revision_when_flux_monitoring(\
				#v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].get_id_head_intersection_node()].\
				#set_nb_times_ctrl_revision_corresponding_to_t_last_request_ctrl_revision_when_flux_monitoring()+1)
					
		li_id_veh=[]
		for i in v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[queue_phase.get_associated_phase_to_queue()[0],\
		queue_phase.get_associated_phase_to_queue()[1]].get_queue_veh():
					
			li_id_veh.append(i.get_id_veh())
				
		#we create an record database object 
		record_db_obj=Cl_Record_Database.Record_Database(\
		val_file_db=v_file_recording_event_db,\
		val_ev_time=self._event_time,\
		val_ev_type=self._event_type,\
		val_id_inters_node=[v_val_netwk.get_di_entry_links_to_network()[\
		queue_phase.get_associated_phase_to_queue()[0]].get_id_head_intersection_node()],\
		val_t_start_current_inters_control=v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_links_to_network()[\
		queue_phase.get_associated_phase_to_queue()[0]].\
		get_id_head_intersection_node()].get_intersection_control_obj().get_t_start_control(),\
		val_duration_current_inters_control=v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_links_to_network()[\
		queue_phase.get_associated_phase_to_queue()[0]].\
		get_id_head_intersection_node()].get_intersection_control_obj().get_duration_control(),\
		val_current_inters_matrix_with_the_associated_link_of_phase=\
		v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_links_to_network()[\
		queue_phase.get_associated_phase_to_queue()[0]].get_id_head_intersection_node()].\
		get_intersection_control_obj().\
		get_di_intersection_control_mat(),\
		val_duration_current_cycle=v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_links_to_network()[\
		queue_phase.get_associated_phase_to_queue()[0]].\
		get_id_head_intersection_node()].get_intersection_control_obj().\
		get_cycle_duration_associated_with_control(),\
		val_vehicle_id=self._vehicle.get_id_veh(),\
		val_time_veh_appearance_in_network=self._vehicle.get_t_veh_appearance_at_network(),\
		val_id_veh_entry_link=self._vehicle.get_id_entry_link_veh_ap(),\
		val_id_current_link_veh_location=self._vehicle.get_current_id_link_veh_location(),\
		val_time_veh_arrival_at_current_link=self._vehicle.get_t_vehicle_arrival_at_current_link(),\
		val_time_veh_departure_from_current_link=self._vehicle.get_t_vehicle_departure_from_current_link(),\
		val_veh_current_queue_location=self._vehicle.get_veh_current_queue_location(),\
		val_time_veh_arrival_at_current_queue=self._vehicle.get_t_vehicle_arrival_at_current_queue(),\
		val_time_veh_start_departure_from_current_queue=self._vehicle.get_t_vehicle_started_departure_from_current_queue(),\
		val_time_veh_departure_from_current_queue=self._vehicle.get_t_vehicle_departure_from_current_queue(),\
		val_veh_id_destination_link=self._vehicle.get_veh_current_queue_location()[List_Explicit_Values.val_second_element_of_list],\
		val_time_veh_exit_from_network=self._vehicle.get_t_exit_veh_from_network(),\
		val_id_event_link=self._id_entry_link,\
		val_current_achieved_queue_service_rate_including_current_vehicle=\
		v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].\
		get_current_reached_service_rate(),\
		val_current_queue_service_rate=\
		v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].\
		get_current_queue_service_rate(),\
		val_li_id_vehicles_in_queue=li_id_veh,\
		val_nb_veh_in_ar_lk=v_val_netwk.get_di_all_links()[i.get_current_id_link_veh_location()].get_current_nb_veh_link(),\
		val_id_veh_final_dest_exit_lk=self._vehicle.get_id_veh_final_destination_link())
		#val_prob_rout_prop_current_lk=val_netwk.get_dict_mat_od_key_id_entry_internal_lk_value_list_dest_lks()[\
		#queue_phase.get_associated_phase_to_queue()[0]],\
		#val_id_veh_final_dest_exit_lk=self._vehicle.get_id_veh_final_destination_link())	
						
		#we record the event in the db 
		record_db_obj.fct_write_object_in_db_file()
		
#*****************************************************************************************************************************************************************************************


#**************************************************Cas New Demand-with OD and dyn computed path-without sensor monit ***************************************************

	#method treating the case when a veh appears, a new generated demand is being considered, the vehicle final destination is predefined, the path
	#is computed, the employed control does not require  sensor monitoring for the t at which is should  be revised 
	def fct_treat_case_veh_appear_new_demand_final_dest_intial_defined_path_dyn_computed_without_sensor_monit(self,\
	v_val_veh_id,v_val_netwk,v_val_type_veh_final_destination,v_val_min_veh_hold_time,v_val_prec_round,v_val_ev_list,v_file_recording_event_db,\
	v_val_fct_calc_queue_id_when_given_final_dest_and_path_dynam_constructed):
	
		t_appear_next_veh=round(self._event_time+v_val_netwk.get_di_entry_links_to_network()\
		[self._id_entry_link].fct_creating_demand_entry_link(),v_val_prec_round)
		
		#creation of the next vehicle
		next_veh=Cl_Vehicle.Vehicle(val_t_veh_appearance_at_network=t_appear_next_veh,\
		val_id_entry_link_veh_ap=self._id_entry_link)
		
		#creation of the next vehicle appearance event
		ev_new_veh_ap=Ev_veh_appearance(val_event_t=t_appear_next_veh,\
		val_vehicle=next_veh)
		
		#we insert the event in the event list
		ev_new_veh_ap.fct_insertion_even_in_event_list(event_list=v_val_ev_list,\
		message="IN CL_EV_VEH_APPEARANCE IN FUNCT\
		fct_treat_case_veh_appear_new_demand_final_dest_intial_defined_path_dyn_computed_without_sensor_monit ,\
		NEXT VEH APPEARANCE EVENT HAS TIME < TIME FIRST EVENT IN THE LIST")
		
		#we attribute the id to the vehicle
		self._vehicle.set_id_veh(v_val_veh_id)
		self._vehicle.set_type_vehicle_final_destination(v_val_type_veh_final_destination)
		
		#we update the vehicle, we indicate the id of the new link location and the time at which it arrived at the new link
		self._vehicle.fct_veh_update_when_appear_at_link(self._id_entry_link,self._event_time)
		
		#we decide  the veh final destination
		#li_rep=[unif nb, id current veh loca, selected id exit link ]
		li_rep=self._obj_decisions.fct_calcul_exit_lk_chosen_by_veh_cas_given_final_destination(\
		id_veh_entry_link=self._id_entry_link,\
		di_cum_mod=v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].\
		get_id_head_intersection_node()].get_current_di_cum_mod())
		
		#we indicate the veh exit link for the record
		veh_exit_lk=li_rep[2]
		
		#we associate the final dest to the vehicle 
		self._vehicle.set_id_veh_final_destination_link(li_rep[2])
		
		#we update the indicator of the veh current location  in the que
		#new_v=self._vehicle.get_index_current_veh_link_location_in_path_list_when_given_destination()+1
			
		#self._vehicle.set_index_current_veh_link_location_in_path_list_when_given_destination(new_v)
		
		#we update the number of vehicles in the  link
		#even in the case of infinite management of the internal links; that's why we avoid a test examining if the destination link
		#is  not exit link  but internal if  finite capacity 
		#v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].set_current_nb_veh_link(\
		#v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].get_current_nb_veh_link()+1)
					
		#we decide the que chosen by the vehicle
		li_param_fct_calcul_que_chosen_by_veh=[\
		v_val_netwk,self._id_entry_link,self._vehicle.get_id_veh_final_destination_link(),v_val_fct_calc_queue_id_when_given_final_dest_and_path_dynam_constructed]
		
		
		id_dest_lk=self._obj_decisions.fct_calcul_queue_chosen_by_veh_cas_given_final_destination_dyn_constr_path(*\
		li_param_fct_calcul_que_chosen_by_veh)
		
		#the vehicle queue  object chosen for the vehicle to join in
		queue_phase=v_val_netwk.get_di_entry_internal_links()[self._id_entry_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()[\
		self._id_entry_link,id_dest_lk]
		
		
		#we update the vehicle, we indicate the chosen queue and its arrival time in the queue
		self._vehicle.fct_update_veh_after_choosing_queue(queue_phase,self._event_time,v_val_netwk)
			
		t_end_veh_hold_time=round(self._event_time+v_val_min_veh_hold_time,v_val_prec_round)
		
		#we examine if there are other vehicles in the que
		if v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].\
		get_queue_veh()==[]:
			other_veh_in_que_before_add_veh=0
		else:
			other_veh_in_que_before_add_veh=1
			
		#we update queue (add the vehicle in the queue)
		v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].\
		fct_update_veh_queue_when_veh_prohibited_to_leave_no_mod(self._vehicle)
		
		#we indicate the time at which the vehicle hold in the queue  ceases
		self._vehicle.set_t_end_veh_hold_time_que(t_end_veh_hold_time)
		
		#if there are no veh in the que (otherwise veh will keave with ev end veh departure) 
		if other_veh_in_que_before_add_veh==0:
			
			#creat ev_end_hold_time
			ev_end_hold_time=Cl_Ev_end_veh_hold_at_que.Ev_end_veh_hold_at_que(val_event_t= t_end_veh_hold_time,\
			val_id_que=queue_phase.get_associated_phase_to_queue())
					
			#we add the event in the event list
			ev_end_hold_time.fct_insertion_even_in_event_list(event_list=v_val_ev_list,\
			message="IN CL_EV_VEH_APPEARANCE IN FUNCT \
			fct_treat_case_veh_appear_new_demand_final_dest_intial_defined_path_dyn_computed_without_sensor_monit,\
			EVENT END HOLD TIME HAS TIME < TIME FIRST EVENT IN THE LIST")
			
		li_id_veh=[]
		for i in v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].get_set_veh_queue().\
		get_di_obj_veh_queue_at_link()\
		[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].get_queue_veh():
		
			li_id_veh.append(i.get_id_veh())
		
		#we create an record database object 
		record_db_obj=Cl_Record_Database.Record_Database(\
		val_file_db=v_file_recording_event_db,\
		val_ev_time=self._event_time,\
		val_ev_type=self._event_type,\
		val_id_inters_node=v_val_netwk.get_di_entry_links_to_network()[\
		queue_phase.get_associated_phase_to_queue()[0]].get_id_head_intersection_node(),\
		val_type_inters_node=v_val_netwk.get_di_intersections()[\
		v_val_netwk.get_di_entry_links_to_network()[\
		queue_phase.get_associated_phase_to_queue()[0]].get_id_head_intersection_node()].get_type_intersection(),\
		val_current_inters_matrix_with_the_associated_link_of_phase=\
		v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_links_to_network()[queue_phase.get_associated_phase_to_queue()[0]].\
		get_id_head_intersection_node()].\
		get_intersection_control_obj().get_di_intersection_control_mat(),\
		val_vehicle_id=self._vehicle.get_id_veh(),\
		val_time_veh_appearance_in_network=self._vehicle.get_t_veh_appearance_at_network(),\
		val_id_veh_entry_link=self._vehicle.get_id_entry_link_veh_ap(),\
		val_id_current_link_veh_location=self._vehicle.get_current_id_link_veh_location(),\
		val_time_veh_arrival_at_current_link=self._vehicle.get_t_vehicle_arrival_at_current_link(),\
		val_veh_current_queue_location=self._vehicle.get_veh_current_queue_location(),\
		val_time_veh_arrival_at_current_queue=self._vehicle.get_t_vehicle_arrival_at_current_queue(),\
		val_veh_id_destination_link=self._vehicle.get_veh_current_queue_location()[List_Explicit_Values.val_second_element_of_list],\
		val_id_event_link=self._id_entry_link,\
		val_current_achieved_queue_service_rate_including_current_vehicle=\
		v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].\
		get_current_reached_service_rate(),\
		val_current_queue_service_rate=\
		v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].\
		get_current_queue_service_rate(),\
		val_li_id_vehicles_in_queue=li_id_veh,\
		val_nb_veh_in_ar_lk=v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].get_current_nb_veh_link(),\
		val_id_veh_final_dest_exit_lk=self._vehicle.get_id_veh_final_destination_link())
		
		#we record the event in the db 
		record_db_obj.fct_write_object_in_db_file()
		
#*****************************************************************************************************************************************************************************************


#*************************************************Cas New Demand-with OD and dyn computed path-with sensor monit ********************************************************

	#method treating the case when a veh appears, a new generated demand is being considered, the vehicle final destination is predefined, the path
	#is computed, the employed control does not require  sensor monitoring for the t at which is should  be revised a
	def fct_treat_case_veh_appear_new_demand_final_dest_intial_defined_path_dyn_computed_with_sensor_monit(self,\
	v_val_veh_id,v_val_netwk,v_val_type_veh_final_destination,v_val_min_veh_hold_time,v_val_ti_ctrl_revision_if_decided,v_val_prec_round,v_val_ev_list,\
	v_file_recording_event_db,v_val_fct_calc_queue_id_when_given_final_dest_and_path_dynam_constructed,val_min_nb_vehicles_to_detect):
	
		t_appear_next_veh=round(self._event_time+v_val_netwk.get_di_entry_links_to_network()\
		[self._id_entry_link].fct_creating_demand_entry_link(),v_val_prec_round)
		
		#creation of the next vehicle
		next_veh=Cl_Vehicle.Vehicle(val_t_veh_appearance_at_network=t_appear_next_veh,\
		val_id_entry_link_veh_ap=self._id_entry_link)
		
		#creation of the next vehicle appearance event
		ev_new_veh_ap=Ev_veh_appearance(val_event_t=t_appear_next_veh,\
		val_vehicle=next_veh)
		
		#we insert the event in the event list
		ev_new_veh_ap.fct_insertion_even_in_event_list(event_list=v_val_ev_list,\
		message="IN CL_EV_VEH_APPEARANCE IN FUNCT,\
		fct_treat_case_veh_appear_new_demand_final_dest_intial_defined_path_dyn_computed_with_sensor_monit,\
		NEXT VEH APPEARANCE EVENT HAS TIME < TIME FIRST EVENT IN THE LIST")
		
		#we attribute the id to the vehicle
		self._vehicle.set_id_veh(v_val_veh_id)
		
		self._vehicle.set_type_vehicle_final_destination(v_val_type_veh_final_destination)
		
		#we update the vehicle, we indicate the id of the new link location and the time at which it arrived at the new link
		self._vehicle.fct_veh_update_when_appear_at_link(self._id_entry_link,self._event_time)
		
		#we decide  the veh final destination
		#li_rep=[unif nb, id current veh loca, selected id exit link ]
		li_rep=self._obj_decisions.fct_calcul_exit_lk_chosen_by_veh_cas_given_final_destination(\
		id_veh_entry_link=self._id_entry_link,\
		di_cum_mod=v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].\
		get_id_head_intersection_node()].get_current_di_cum_mod())
			
		#we indicate the veh exit link for the record
		veh_exit_lk=li_rep[2]
			
		#we associate the final dest to the vehicle 
		self._vehicle.set_id_veh_final_destination_link(li_rep[2])
		
		#we update the indicator of the veh current location  in the que
		new_v=self._vehicle.get_index_current_veh_link_location_in_path_list_when_given_destination()+1
			
		self._vehicle.set_index_current_veh_link_location_in_path_list_when_given_destination(new_v)
		
		#we update the number of vehicles in the  link
		#even in the case of infinite management of the internal links; that's why we avoid a test examining if the destination link
		#is  not exit link  but internal if  finite capacity 
		#v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].set_current_nb_veh_link(\
		#v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].get_current_nb_veh_link()+1)
				
		
		#we decide the que chosen by the vehicle
		li_param_fct_calcul_que_chosen_by_veh=[\
		v_val_netwk,self._id_entry_link,self._vehicle.get_id_veh_final_destination_link(),v_val_fct_calc_queue_id_when_given_final_dest_and_path_dynam_constructed]
		
		
		id_dest_lk=self._obj_decisions.fct_calcul_queue_chosen_by_veh_cas_given_final_destination_dyn_constr_path(*\
		li_param_fct_calcul_que_chosen_by_veh)
		
		
		#the vehicle queue  object chosen for the vehicle to join in
		queue_phase=v_val_netwk.get_di_entry_internal_links()[self._id_entry_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()[\
		self._id_entry_link,id_dest_lk]
		
		#we update the vehicle, we indicate the chosen queue and its arrival time in the queue
		self._vehicle.fct_update_veh_after_choosing_queue(queue_phase,self._event_time,v_val_netwk)
			
		t_end_veh_hold_time=round(self._event_time+v_val_min_veh_hold_time,v_val_prec_round)
		
		#we examine if there are other vehicles in the que
		if v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].\
		get_queue_veh()==[]:
			other_veh_in_que_before_add_veh=0
		else:
			other_veh_in_que_before_add_veh=1
			
		#we update queue (add the vehicle in the queue)
		v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].\
		fct_update_veh_queue_when_veh_prohibited_to_leave_no_mod(self._vehicle)
			
		#we indicate the time at which the vehicle hold in the queue  ceases
		self._vehicle.set_t_end_veh_hold_time_que(t_end_veh_hold_time)
		
		#if there are no veh in the que (otherwise veh will keave with ev end veh departure) 
		if other_veh_in_que_before_add_veh==0:
			
			#creat ev_end_hold_time
			ev_end_hold_time=Cl_Ev_end_veh_hold_at_que.Ev_end_veh_hold_at_que(val_event_t= t_end_veh_hold_time,\
			val_id_que=queue_phase.get_associated_phase_to_queue())
					
			#we add the event in the event list
			ev_end_hold_time.fct_insertion_even_in_event_list(event_list=v_val_ev_list,\
			message="IN CL_EV_VEH_APPEARANCE IN FUNCT \
			fct_treat_case_veh_appear_new_demand_final_dest_intial_defined_path_dyn_computed_with_sensor_monit \
			EVENT END HOLD TIME HAS TIME < TIME FIRST EVENT IN THE LIST")
			
		#if the queue is not a right turn 
		if queue_phase.get_type_veh_queue()!=Cl_Vehicle_Queue.TYPE_VEHICLE_QUEUE["right_turn"]:
		
			#if there is at least one detector detecting the veh
			if queue_phase.fct_exam_whether_at_least_nb_veh_detected_by_a_que_sensor(val_min_nb_veh_to_detect=val_min_nb_vehicles_to_detect)!=None:
		
				
				# controle dec update
				ev_end_deci_next_icm=Cl_Ev_end_decision_next_intersection_control.Ev_end_decision_next_intersection_control(\
				val_ev_time=v_val_ti_ctrl_revision_if_decided,\
				val_id_intersection_node=v_val_netwk.get_di_all_links()[self._id_entry_link].get_id_head_intersection_node(),\
				val_type_control_to_employ=\
				v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].\
				get_id_head_intersection_node()].get_ctrl_actuate_obj().get_type_employed_ctrl(),\
				val_control_category="sensor_requirement")
				#,val_reason_ctrl_revision_t_lim=0)	
		
				#on insert the event ev_end_dec_next_icm into the event list
				ev_end_deci_next_icm.fct_insertion_even_in_event_list(event_list=v_val_ev_list,\
				message="IN CL_Ev_appear IN FUNCT \
				fct_treat_case_veh_appear_new_demand_final_dest_intial_defined_path_dyn_computed_with_sensor_monit\
				NEXT ev_new_end_dec_netw_control EVENT HAS TIME < TIME FIRST EVENT IN THE LIST")
				
				#we indicate the intersection that a ctrl request is made
				#v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].get_id_head_intersection_node()].\
				#set_t_last_request_ctrl_revision_when_flux_monitoring(v_val_ti_ctrl_revision_if_decided)
				
				#we indicate the number of times a control revision is asked for the same time
				#v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].get_id_head_intersection_node()].\
				#set_nb_times_ctrl_revision_corresponding_to_t_last_request_ctrl_revision_when_flux_monitoring(\
				#v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].get_id_head_intersection_node()].\
				#set_nb_times_ctrl_revision_corresponding_to_t_last_request_ctrl_revision_when_flux_monitoring()+1)
				
				
		li_id_veh=[]
		for i in v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[queue_phase.get_associated_phase_to_queue()[0],\
		queue_phase.get_associated_phase_to_queue()[1]].get_queue_veh():
					
			li_id_veh.append(i.get_id_veh())
				
		#we create an record database object 
		record_db_obj=Cl_Record_Database.Record_Database(\
		val_file_db=v_file_recording_event_db,\
		val_ev_time=self._event_time,\
		val_ev_type=self._event_type,\
		val_id_inters_node=[v_val_netwk.get_di_entry_links_to_network()[\
		queue_phase.get_associated_phase_to_queue()[0]].get_id_head_intersection_node()],\
		val_t_start_current_inters_control=v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_links_to_network()[\
		queue_phase.get_associated_phase_to_queue()[0]].\
		get_id_head_intersection_node()].get_intersection_control_obj().get_t_start_control(),\
		val_duration_current_inters_control=v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_links_to_network()[\
		queue_phase.get_associated_phase_to_queue()[0]].\
		get_id_head_intersection_node()].get_intersection_control_obj().get_duration_control(),\
		val_current_inters_matrix_with_the_associated_link_of_phase=\
		v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_links_to_network()[\
		queue_phase.get_associated_phase_to_queue()[0]].get_id_head_intersection_node()].\
		get_intersection_control_obj().\
		get_di_intersection_control_mat(),\
		val_duration_current_cycle=v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_links_to_network()[\
		queue_phase.get_associated_phase_to_queue()[0]].\
		get_id_head_intersection_node()].get_intersection_control_obj().\
		get_cycle_duration_associated_with_control(),\
		val_vehicle_id=self._vehicle.get_id_veh(),\
		val_time_veh_appearance_in_network=self._vehicle.get_t_veh_appearance_at_network(),\
		val_id_veh_entry_link=self._vehicle.get_id_entry_link_veh_ap(),\
		val_id_current_link_veh_location=self._vehicle.get_current_id_link_veh_location(),\
		val_time_veh_arrival_at_current_link=self._vehicle.get_t_vehicle_arrival_at_current_link(),\
		val_time_veh_departure_from_current_link=self._vehicle.get_t_vehicle_departure_from_current_link(),\
		val_veh_current_queue_location=self._vehicle.get_veh_current_queue_location(),\
		val_time_veh_arrival_at_current_queue=self._vehicle.get_t_vehicle_arrival_at_current_queue(),\
		val_time_veh_start_departure_from_current_queue=self._vehicle.get_t_vehicle_started_departure_from_current_queue(),\
		val_time_veh_departure_from_current_queue=self._vehicle.get_t_vehicle_departure_from_current_queue(),\
		val_veh_id_destination_link=self._vehicle.get_veh_current_queue_location()[List_Explicit_Values.val_second_element_of_list],\
		val_time_veh_exit_from_network=self._vehicle.get_t_exit_veh_from_network(),\
		val_id_event_link=self._id_entry_link,\
		val_current_achieved_queue_service_rate_including_current_vehicle=\
		v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].\
		get_current_reached_service_rate(),\
		val_current_queue_service_rate=\
		v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].\
		get_current_queue_service_rate(),\
		val_li_id_vehicles_in_queue=li_id_veh,\
		val_nb_veh_in_ar_lk=v_val_netwk.get_di_all_links()[i.get_current_id_link_veh_location()].get_current_nb_veh_link(),\
		val_id_veh_final_dest_exit_lk=self._vehicle.get_id_veh_final_destination_link())
		#val_prob_rout_prop_current_lk=val_netwk.get_dict_mat_od_key_id_entry_internal_lk_value_list_dest_lks()[\
		#queue_phase.get_associated_phase_to_queue()[0]])	
						
		#we record the event in the db 
		record_db_obj.fct_write_object_in_db_file()
		
#*****************************************************************************************************************************************************************************************
#*****************************************************************Cas Previous Demand-no OD-without sensor monit *************************************************************
	
	#method treating the case when a veh appears, a previously generated demand is being considered, 
	#the vehicle final destination and path were dyn decided,(in prev demand),
	# the employed control does not require  sensor monitoring for the t at which is should  be revised 
	def fct_treat_case_veh_appear_previous_demand_final_dest_and_path_dyn_defined_without_sensor_monit(self,\
	v_val_netwk,v_val_type_veh_final_destination,v_val_min_veh_hold_time,v_val_prec_round,v_val_ev_list,v_file_recording_event_db,\
	v_val_dict_entry_link_info_prev_sim,v_val_dict_veh_info_prev_sim):
	
		#if the previous demand has generated a veh appearance, (this is  that  we have at least the same number of veh appear)
		if v_val_dict_entry_link_info_prev_sim[self._id_entry_link] !=[]:
		
			t_appear_next_veh=v_val_dict_entry_link_info_prev_sim[self._id_entry_link][0][0]
			
			#creation of the next vehicle
			next_veh=Cl_Vehicle.Vehicle(val_t_veh_appearance_at_network=t_appear_next_veh,\
			val_id_entry_link_veh_ap=self._id_entry_link)
			
			#creation of the next vehicle appearance event
			ev_new_veh_ap=Ev_veh_appearance(val_event_t=t_appear_next_veh,\
			val_vehicle=next_veh,\
			val_current_veh_id_demand_previous_sim=v_val_dict_entry_link_info_prev_sim[self._id_entry_link][0][1])
			
			#we insert the event in the event list
			ev_new_veh_ap.fct_insertion_even_in_event_list(event_list=v_val_ev_list,\
			message="IN CL_EV_VEH_APPEARANCE IN FUNCT f\
			ct_treat_case_veh_appear_previous_demand_final_dest_and_path_dyn_defined_without_sensor_monit\
			NEXT VEH APPEARANCE EVENT HAS TIME < TIME FIRST EVENT IN THE LIST")
			
			#we delete the first element of the list corrresponding to the associated entry link
			#val_dict_entry_link_info_previous_sim= dict,key =id entry link, 
			#value= [...,  [t_appearance_veh, veh_id ],...  ] 
			v_val_dict_entry_link_info_prev_sim[self._id_entry_link].remove(v_val_dict_entry_link_info_prev_sim[self._id_entry_link][0])
			
			#we attribute the id to the vehicle
			self._vehicle.set_id_veh(self._current_veh_id_demand_previous_sim)
			self._vehicle.set_type_vehicle_final_destination(v_val_type_veh_final_destination)
			
			#we update the vehicle, we indicate the id of the new link location and the time at which it arrived at the new link
			self._vehicle.fct_veh_update_when_appear_at_link(self._id_entry_link,self._event_time)
			
			#we update the number of vehicles in the  link
			#even in the case of infinite management of the internal links; that's why we avoid a test examining if the destination link
			#is  not exit link  but internal if  finite capacity 
			#v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].set_current_nb_veh_link(\
			#v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].get_current_nb_veh_link()+1)
			
			#if we have generated a next destination for the vehicle 
			if len(v_val_dict_veh_info_prev_sim[self._vehicle.get_id_veh()][1])>List_Explicit_Values.initialisation_value_to_one:
			
				queue_phase=v_val_netwk.get_di_entry_links_to_network()[v_val_dict_veh_info_prev_sim[self._vehicle.get_id_veh()][1][0]].\
				get_set_veh_queue().get_di_obj_veh_queue_at_link()[v_val_dict_veh_info_prev_sim[self._vehicle.get_id_veh()][1][0],\
				v_val_dict_veh_info_prev_sim[self._vehicle.get_id_veh()][1][1]]
				
				#we delete the first link location from the veh dictionary 
				v_val_dict_veh_info_prev_sim[self._vehicle.get_id_veh()][1].remove(v_val_dict_veh_info_prev_sim[self._vehicle.get_id_veh()][1][0])
					
			#if we have not generated a next destination for the vehicle, we will generate a new one
			else:
				print("PR0BLEM IN C VEH APPEAR, IN FCT,\
				fct_treat_case_veh_appear_previous_demand_final_dest_and_path_dyn_defined_without_sensor_monit\
				the previous demands has not generated a dest for the veh. The previously made sim should be at least as long as the current one,\
				length dict veh info:",len(v_val_dict_veh_info_prev_sim[self._vehicle.get_id_veh()][1]))
				import sys
				sys.exit()
				
			#we update the vehicle, we indicate the chosen queue and its arrival time in the queue
			self._vehicle.fct_update_veh_after_choosing_queue(queue_phase,self._event_time,v_val_netwk)
			
			t_end_veh_hold_time=round(self._event_time+v_val_min_veh_hold_time,v_val_prec_round)
			
			#we examine if there are other vehicles in the que
			if v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
			[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].\
			get_queue_veh()==[]:
				other_veh_in_que_before_add_veh=0
			else:
				other_veh_in_que_before_add_veh=1
				
			#we add the vehicle in the queue
			v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
			[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].\
			fct_update_veh_queue_when_veh_prohibited_to_leave_no_mod(self._vehicle)
			
			#we indicate the time at which the vehicle hold in the queue  ceases
			self._vehicle.set_t_end_veh_hold_time_que(t_end_veh_hold_time)
			
			#if there are no veh in the que (otherwise veh will keave with ev end veh departure) 
			if other_veh_in_que_before_add_veh==0:
			
				#creat ev_end_hold_time
				ev_end_hold_time=Cl_Ev_end_veh_hold_at_que.Ev_end_veh_hold_at_que(val_event_t= t_end_veh_hold_time,\
				val_id_que=queue_phase.get_associated_phase_to_queue())
					
				#we add the event in the event list
				ev_end_hold_time.fct_insertion_even_in_event_list(event_list=v_val_ev_list,\
				message="IN CL_EV_VEH_APPEARANCE IN FUNC\
				T fct_treat_case_veh_appear_previous_demand_final_dest_and_path_dyn_defined_without_sensor_monit\
				EVENT END HOLD TIME HAS TIME < TIME FIRST EVENT IN THE LIST")

		
		#if the previous demand has not generated a veh appearance, (this is  that  we have at least the same number of veh appear)
		else:
			print("PROBLEM IN CL EV VEH APPEAR, \
			fct_treat_case_veh_appear_previous_demand_final_dest_and_path_dyn_defined_without_sensor_monit,\
			the previous demand has not generated a veh appear")
			import sys
			sys.exit()
				
		li_id_veh=[]
		for i in v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].get_set_veh_queue().\
		get_di_obj_veh_queue_at_link()\
		[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].get_queue_veh():
		
			li_id_veh.append(i.get_id_veh())
		
		#we create an record database object 
		record_db_obj=Cl_Record_Database.Record_Database(\
		val_file_db=v_file_recording_event_db,\
		val_ev_time=self._event_time,\
		val_ev_type=self._event_type,\
		val_id_inters_node=v_val_netwk.get_di_entry_links_to_network()[\
		queue_phase.get_associated_phase_to_queue()[0]].get_id_head_intersection_node(),\
		val_type_inters_node=v_val_netwk.get_di_intersections()[\
		v_val_netwk.get_di_entry_links_to_network()[\
		queue_phase.get_associated_phase_to_queue()[0]].get_id_head_intersection_node()].get_type_intersection(),\
		val_current_inters_matrix_with_the_associated_link_of_phase=\
		v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_links_to_network()[queue_phase.get_associated_phase_to_queue()[0]].\
		get_id_head_intersection_node()].\
		get_intersection_control_obj().get_di_intersection_control_mat(),\
		val_vehicle_id=self._vehicle.get_id_veh(),\
		val_time_veh_appearance_in_network=self._vehicle.get_t_veh_appearance_at_network(),\
		val_id_veh_entry_link=self._vehicle.get_id_entry_link_veh_ap(),\
		val_id_current_link_veh_location=self._vehicle.get_current_id_link_veh_location(),\
		val_time_veh_arrival_at_current_link=self._vehicle.get_t_vehicle_arrival_at_current_link(),\
		val_veh_current_queue_location=self._vehicle.get_veh_current_queue_location(),\
		val_time_veh_arrival_at_current_queue=self._vehicle.get_t_vehicle_arrival_at_current_queue(),\
		val_veh_id_destination_link=self._vehicle.get_veh_current_queue_location()[List_Explicit_Values.val_second_element_of_list],\
		val_id_event_link=self._id_entry_link,\
		val_current_achieved_queue_service_rate_including_current_vehicle=\
		v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].\
		get_current_reached_service_rate(),\
		val_current_queue_service_rate=\
		v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].\
		get_current_queue_service_rate(),\
		val_li_id_vehicles_in_queue=li_id_veh,\
		val_nb_veh_in_ar_lk=v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].get_current_nb_veh_link())
		
		#we record the event in the db 
		record_db_obj.fct_write_object_in_db_file()
		
#*****************************************************************************************************************************************************************************************

#*****************************************************************Cas Previous Demand-no OD-with sensor monit ****************************************************************

	#method treating the case when a veh appears, a previously generated demand is being considered, 
	#the vehicle final destination and path were dyn decided,(in prev demand),
	# the employed control  requires  sensor monitoring for the t at which is should  be revised 
	def fct_treat_case_veh_appear_previous_demand_final_dest_and_path_dyn_defined_with_sensor_monit(self,\
	v_val_netwk,v_val_min_veh_hold_time,v_val_type_veh_final_destination,v_val_ti_ctrl_revision_if_decided,v_val_prec_round,\
	v_val_ev_list,v_file_recording_event_db,v_val_dict_entry_link_info_prev_sim,v_val_dict_veh_info_prev_sim,\
	val_min_nb_vehicles_to_detect):
	
		#if the previous demand has generated a veh appearance, (this is  that  we have at least the same number of veh appear)
		if v_val_dict_entry_link_info_prev_sim[self._id_entry_link] !=[]:
		
			t_appear_next_veh=v_val_dict_entry_link_info_prev_sim[self._id_entry_link][0][0]
			
			#creation of the next vehicle
			next_veh=Cl_Vehicle.Vehicle(val_t_veh_appearance_at_network=t_appear_next_veh,\
			val_id_entry_link_veh_ap=self._id_entry_link)
			
			#creation of the next vehicle appearance event
			ev_new_veh_ap=Ev_veh_appearance(val_event_t=t_appear_next_veh,\
			val_vehicle=next_veh,\
			val_current_veh_id_demand_previous_sim=v_val_dict_entry_link_info_prev_sim[self._id_entry_link][0][1])
			
			#we insert the event in the event list
			ev_new_veh_ap.fct_insertion_even_in_event_list(event_list=v_val_ev_list,\
			message="IN CL_EV_VEH_APPEARANCE IN FUNCT,\
			fct_treat_case_veh_appear_previous_demand_final_dest_and_path_dyn_defined_with_sensor_monit,\
			NEXT VEH APPEARANCE EVENT HAS TIME < TIME FIRST EVENT IN THE LIST")
			
			#we delete the first element of the list corrresponding to the associated entry link
			#val_dict_entry_link_info_previous_sim= dict,key =id entry link, 
			#value= [...,  [t_appearance_veh, veh_id ],...  ] 
			v_val_dict_entry_link_info_prev_sim[self._id_entry_link].remove(v_val_dict_entry_link_info_prev_sim[self._id_entry_link][0])
			
			#we attribute the id to the vehicle
			self._vehicle.set_id_veh(self._current_veh_id_demand_previous_sim)
			
			self._vehicle.set_type_vehicle_final_destination(v_val_type_veh_final_destination)
			
			
			#we update the vehicle, we indicate the id of the new link location and the time at which it arrived at the new link
			self._vehicle.fct_veh_update_when_appear_at_link(self._id_entry_link,self._event_time)
			
			#we update the number of vehicles in the  link
			#even in the case of infinite management of the internal links; that's why we avoid a test examining if the destination link
			#is  not exit link  but internal if  finite capacity 
			#v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].set_current_nb_veh_link(\
			#v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].get_current_nb_veh_link()+1)
			
			#if we have generated a next destination for the vehicle 
			if len(v_val_dict_veh_info_prev_sim[self._vehicle.get_id_veh()][1])>List_Explicit_Values.initialisation_value_to_one:
			
				queue_phase=v_val_netwk.get_di_entry_links_to_network()[v_val_dict_veh_info_prev_sim[self._vehicle.get_id_veh()][1][0]].\
				get_set_veh_queue().get_di_obj_veh_queue_at_link()[v_val_dict_veh_info_prev_sim[self._vehicle.get_id_veh()][1][0],\
				v_val_dict_veh_info_prev_sim[self._vehicle.get_id_veh()][1][1]]
				
				#we delete the first link location from the veh dictionary 
				v_val_dict_veh_info_prev_sim[self._vehicle.get_id_veh()][1].remove(v_val_dict_veh_info_prev_sim[self._vehicle.get_id_veh()][1][0])
					
			#if we have not generated a next destination for the vehicle, we will generate a new one
			else:
				print("PROBLEM IN CL EV VEH APPEAR, IN FCT \
				fct_treat_case_veh_appear_previous_demand_final_dest_and_path_dyn_defined_with_sensor_monit,\
				WE HAVE NOT GENERATED A NEXT DEST FOR THE VEHICLE, ",len(v_val_dict_veh_info_prev_sim[self._vehicle.get_id_veh()][1]))
				import sys
				sys.exit()
				
			#we update the vehicle, we indicate the chosen queue and its arrival time in the queue
			self._vehicle.fct_update_veh_after_choosing_queue(queue_phase,self._event_time,v_val_netwk)
			
			t_end_veh_hold_time=round(self._event_time+v_val_min_veh_hold_time,v_val_prec_round)
			
			#we examine if there are other vehicles in the que
			if v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
			[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].\
			get_queue_veh()==[]:
				other_veh_in_que_before_add_veh=0
			else:
				other_veh_in_que_before_add_veh=1
				
			#we add the vehicle in the queue
			v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
			[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].\
			fct_update_veh_queue_when_veh_prohibited_to_leave_no_mod(self._vehicle)
			
			#we indicate the time at which the vehicle hold in the queue  ceases
			self._vehicle.set_t_end_veh_hold_time_que(t_end_veh_hold_time)
			
			#if there are no veh in the que (otherwise veh will keave with ev end veh departure) 
			if other_veh_in_que_before_add_veh==0:
			
				#creat ev_end_hold_time
				ev_end_hold_time=Cl_Ev_end_veh_hold_at_que.Ev_end_veh_hold_at_que(val_event_t= t_end_veh_hold_time,\
				val_id_que=queue_phase.get_associated_phase_to_queue())
					
				#we add the event in the event list
				ev_end_hold_time.fct_insertion_even_in_event_list(event_list=v_val_ev_list,\
				message="IN CL_EV_VEH_APPEARANCE IN FUNCT \
				fct_treat_case_veh_appear_previous_demand_final_dest_and_path_dyn_defined_with_sensor_monit,\
				EVENT END HOLD TIME HAS TIME < TIME FIRST EVENT IN THE LIST")
				
			#if the queue is not a right turn 
			if queue_phase.get_type_veh_queue()!=Cl_Vehicle_Queue.TYPE_VEHICLE_QUEUE["right_turn"]:
				
			
				# controle dec update
				ev_end_deci_next_icm=Cl_Ev_end_decision_next_intersection_control.Ev_end_decision_next_intersection_control(\
				val_ev_time=v_val_ti_ctrl_revision_if_decided,\
				val_id_intersection_node=v_val_netwk.get_di_all_links()[self._id_entry_link].get_id_head_intersection_node(),\
				val_type_control_to_employ=\
				v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].\
				get_id_head_intersection_node()].get_ctrl_actuate_obj().get_type_employed_ctrl(),\
				val_control_category="sensor_requirement")
				#,val_reason_ctrl_revision_t_lim=0)	
		
				#on insert the event ev_end_dec_next_icm into the event list
				ev_end_deci_next_icm.fct_insertion_even_in_event_list(event_list=v_val_ev_list,\
				message="IN CL_Ev_appear IN FUNCT \
				fct_treat_case_veh_appear_previous_demand_final_dest_and_path_dyn_defined_with_sensor_monit\
				NEXT ev_new_end_dec_netw_control EVENT HAS TIME < TIME FIRST EVENT IN THE LIST")
				
				#we indicate the intersection that a ctrl request is made
				#v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].get_id_head_intersection_node()].\
				#set_t_last_request_ctrl_revision_when_flux_monitoring(v_val_ti_ctrl_revision_if_decided)
				
				#we indicate the number of times a control revision is asked for the same time
				#v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].get_id_head_intersection_node()].\
				#set_nb_times_ctrl_revision_corresponding_to_t_last_request_ctrl_revision_when_flux_monitoring(\
				#v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].get_id_head_intersection_node()].\
				#set_nb_times_ctrl_revision_corresponding_to_t_last_request_ctrl_revision_when_flux_monitoring()+1)
				
		
		
		#if the previous demand has not generated a veh appearance, (this is  that  we have at least the same number of veh appear)
		else:
			print("PROBLEM IN CL EV VEH APPEAR\
			fct_treat_case_veh_appear_previous_demand_final_dest_and_path_dyn_defined_with_sensor_monit \
			the previous demand has not generated a veh appear")
			import sys
			sys.exit()
			
		li_id_veh=[]
		for i in v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[queue_phase.get_associated_phase_to_queue()[0],\
		queue_phase.get_associated_phase_to_queue()[1]].get_queue_veh():
					
			li_id_veh.append(i.get_id_veh())
				
		#we create an record database object 
		record_db_obj=Cl_Record_Database.Record_Database(\
		val_file_db=v_file_recording_event_db,\
		val_ev_time=self._event_time,\
		val_ev_type=self._event_type,\
		val_id_inters_node=[v_val_netwk.get_di_entry_links_to_network()[\
		queue_phase.get_associated_phase_to_queue()[0]].get_id_head_intersection_node()],\
		val_t_start_current_inters_control=v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_links_to_network()[\
		queue_phase.get_associated_phase_to_queue()[0]].\
		get_id_head_intersection_node()].get_intersection_control_obj().get_t_start_control(),\
		val_duration_current_inters_control=v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_links_to_network()[\
		queue_phase.get_associated_phase_to_queue()[0]].\
		get_id_head_intersection_node()].get_intersection_control_obj().get_duration_control(),\
		val_current_inters_matrix_with_the_associated_link_of_phase=\
		v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_links_to_network()[\
		queue_phase.get_associated_phase_to_queue()[0]].get_id_head_intersection_node()].\
		get_intersection_control_obj().\
		get_di_intersection_control_mat(),\
		val_duration_current_cycle=v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_links_to_network()[\
		queue_phase.get_associated_phase_to_queue()[0]].\
		get_id_head_intersection_node()].get_intersection_control_obj().\
		get_cycle_duration_associated_with_control(),\
		val_vehicle_id=self._vehicle.get_id_veh(),\
		val_time_veh_appearance_in_network=self._vehicle.get_t_veh_appearance_at_network(),\
		val_id_veh_entry_link=self._vehicle.get_id_entry_link_veh_ap(),\
		val_id_current_link_veh_location=self._vehicle.get_current_id_link_veh_location(),\
		val_time_veh_arrival_at_current_link=self._vehicle.get_t_vehicle_arrival_at_current_link(),\
		val_time_veh_departure_from_current_link=self._vehicle.get_t_vehicle_departure_from_current_link(),\
		val_veh_current_queue_location=self._vehicle.get_veh_current_queue_location(),\
		val_time_veh_arrival_at_current_queue=self._vehicle.get_t_vehicle_arrival_at_current_queue(),\
		val_time_veh_start_departure_from_current_queue=self._vehicle.get_t_vehicle_started_departure_from_current_queue(),\
		val_time_veh_departure_from_current_queue=self._vehicle.get_t_vehicle_departure_from_current_queue(),\
		val_veh_id_destination_link=self._vehicle.get_veh_current_queue_location()[List_Explicit_Values.val_second_element_of_list],\
		val_time_veh_exit_from_network=self._vehicle.get_t_exit_veh_from_network(),\
		val_id_event_link=self._id_entry_link,\
		#val_veh_can_leave_now=veh_can_leave_que,\
		val_current_achieved_queue_service_rate_including_current_vehicle=\
		v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].\
		get_current_reached_service_rate(),\
		val_current_queue_service_rate=\
		v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].\
		get_current_queue_service_rate(),\
		val_li_id_vehicles_in_queue=li_id_veh,\
		val_nb_veh_in_ar_lk=v_val_netwk.get_di_all_links()[i.get_current_id_link_veh_location()].get_current_nb_veh_link())
		#val_prob_rout_prop_current_lk=val_netwk.get_dict_mat_od_key_id_entry_internal_lk_value_list_dest_lks()[\
		#queue_phase.get_associated_phase_to_queue()[0]])	
						
		#we record the event in the db 
		record_db_obj.fct_write_object_in_db_file()
		

#*****************************************************************************************************************************************************************************************************

#***************************************************Cas Previous Demand-with OD-ctrl eval-without sensor monit ***************************************************************************
	#method treating the case when a veh appears, a previously generated demand is being considered,,
	#purpose of the study is to eavluate the control perform,
	# the employed control does not require  sensor monitoring for the t at which is should  be revised 
	def fct_treat_case_veh_appear_previous_demand_without_sensor_monit_ctr_eval(self,\
	v_val_netwk,v_val_type_veh_final_destination,v_val_min_veh_hold_time,v_val_prec_round,v_val_ev_list,v_file_recording_event_db,\
	v_val_dict_entry_link_info_prev_sim,v_val_dict_veh_info_prev_sim):
	
		#if the previous demand has generated a veh appearance, (this is  that  we have at least the same number of veh appear)
		if v_val_dict_entry_link_info_prev_sim[self._id_entry_link] !=[]:
		
			t_appear_next_veh=v_val_dict_entry_link_info_prev_sim[self._id_entry_link][0][0]
			
			#creation of the next vehicle
			next_veh=Cl_Vehicle.Vehicle(val_t_veh_appearance_at_network=t_appear_next_veh,\
			val_id_entry_link_veh_ap=self._id_entry_link)
			
			#creation of the next vehicle appearance event
			ev_new_veh_ap=Ev_veh_appearance(val_event_t=t_appear_next_veh,\
			val_vehicle=next_veh,\
			val_current_veh_id_demand_previous_sim=v_val_dict_entry_link_info_prev_sim[self._id_entry_link][0][1])
			
			#we insert the event in the event list
			ev_new_veh_ap.fct_insertion_even_in_event_list(event_list=v_val_ev_list,\
			message="IN CL_EV_VEH_APPEARANCE IN FUNCTfct_treat_case_veh_appear_previous_demand_without_sensor_monit_ctr_eval,\
			NEXT VEH APPEARANCE EVENT HAS TIME < TIME FIRST EVENT IN THE LIST")
			
			#we delete the first element of the list corrresponding to the associated entry link
			#val_dict_entry_link_info_previous_sim= dict,key =id entry link, 
			#value= [...,  [t_appearance_veh, veh_id ],...  ] 
			v_val_dict_entry_link_info_prev_sim[self._id_entry_link].remove(v_val_dict_entry_link_info_prev_sim[self._id_entry_link][0])
			
			#we attribute the id to the vehicle
			self._vehicle.set_id_veh(self._current_veh_id_demand_previous_sim)
			
			self._vehicle.set_type_vehicle_final_destination(v_val_type_veh_final_destination)
			
			#we update the vehicle, we indicate the id of the new link location and the time at which it arrived at the new link
			self._vehicle.fct_veh_update_when_appear_at_link(self._id_entry_link,self._event_time)
			
			
			#we update the number of vehicles in the  link
			#even in the case of infinite management of the internal links; that's why we avoid a test examining if the destination link
			#is  not exit link  but internal if  finite capacity 
			#v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].set_current_nb_veh_link(\
			#v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].get_current_nb_veh_link()+1)
			
			#if we have generated a final destination for the vehicle 
			if self._vehicle.get_id_veh() in v_val_dict_veh_info_prev_sim:
			
				#we associate the final dest to the vehicle 
				self._vehicle.set_id_veh_final_destination_link(v_val_dict_veh_info_prev_sim[self._vehicle.get_id_veh()][2])
				
				#we remove the vehicle if from the dictionary
				del v_val_dict_veh_info_prev_sim[self._vehicle.get_id_veh()]
				
				#we update the indicator of the veh current location  in the que
				new_v=self._vehicle.get_index_current_veh_link_location_in_path_list_when_given_destination()+1
				
				self._vehicle.set_index_current_veh_link_location_in_path_list_when_given_destination(new_v)
				
				#we calculate the que chosen by the vehicle
				li_param_fct_calcul_que_chosen_by_veh=[self._id_entry_link,self._id_entry_link,\
				self._vehicle.get_id_veh_final_destination_link(),\
				self._vehicle.get_index_current_veh_link_location_in_path_list_when_given_destination(),\
				v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].get_id_head_intersection_node()].\
				get_current_di_unique_paths(),v_val_netwk]
			
				#the vehicle queue  object chosen for the vehicle to join in
				queue_phase=self._obj_decisions.fct_calcul_queue_chosen_by_veh_cas_given_final_destination(*\
				li_param_fct_calcul_que_chosen_by_veh)
			
			#if we have not treated this vehicle in the previous sim (so  the veh final destination is not defined)
			else:
				print("PROBLEM IN CL_EV_VEH_APPEAR,  IN FCT, \
				fct_treat_case_veh_appear_previous_demand_without_sensor_monit_ctr_eval,\
				FINAL DEST AND PATH ARE INIT GIVEN AND  VEH FINAL DEST IS NOT AVAILABLE,self._vehicle.get_id_veh() in v_val_dict_veh_info_prev_sim",\
				self._vehicle.get_id_veh() in v_val_dict_veh_info_prev_sim)
				import sys
				sys.exit()
				
			#we update the vehicle, we indicate the chosen queue and its arrival time in the queue
			self._vehicle.fct_update_veh_after_choosing_queue(queue_phase,self._event_time,v_val_netwk)
			
			t_end_veh_hold_time=round(self._event_time+v_val_min_veh_hold_time,v_val_prec_round)
			
			#we examine if there are other vehicles in the que
			if v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
			[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].\
			get_queue_veh()==[]:
				other_veh_in_que_before_add_veh=0
			else:
				other_veh_in_que_before_add_veh=1
				
			#we add the vehicle in the queue
			v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
			[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].\
			fct_update_veh_queue_when_veh_prohibited_to_leave_no_mod(self._vehicle)
			
			#we indicate the time at which the vehicle hold in the queue  ceases
			self._vehicle.set_t_end_veh_hold_time_que(t_end_veh_hold_time)
			
			#if there are no veh in the que (otherwise veh will keave with ev end veh departure) 
			if other_veh_in_que_before_add_veh==0:
			
				#creat ev_end_hold_time
				ev_end_hold_time=Cl_Ev_end_veh_hold_at_que.Ev_end_veh_hold_at_que(val_event_t= t_end_veh_hold_time,\
				val_id_que=queue_phase.get_associated_phase_to_queue())
					
				#we add the event in the event list
				ev_end_hold_time.fct_insertion_even_in_event_list(event_list=v_val_ev_list,\
				message="IN CL_EV_VEH_APPEARANCE IN FUNCT fct_treat_case_veh_appear_previous_demand_without_sensor_monit_ctr_eval,\
				EVENT END HOLD TIME HAS TIME < TIME FIRST EVENT IN THE LIST")
		
		#if the previous demand has not generated a veh appearance, (this is  that  we have at least the same number of veh appear)
		else:
			print("PROBLEM IN CL EV VEH APPEAR, \
			fct_treat_case_veh_appear_previous_demand_without_sensor_monit_ctr_eval(")
			import sys
			sys.exit()
			
		li_id_veh=[]
		for i in v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].get_set_veh_queue().\
		get_di_obj_veh_queue_at_link()\
		[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].get_queue_veh():
		
			li_id_veh.append(i.get_id_veh())
			
		#we create an record database object 
		record_db_obj=Cl_Record_Database.Record_Database(\
		val_file_db=v_file_recording_event_db,\
		val_ev_time=self._event_time,\
		val_ev_type=self._event_type,\
		val_id_inters_node=v_val_netwk.get_di_entry_links_to_network()[\
		queue_phase.get_associated_phase_to_queue()[0]].get_id_head_intersection_node(),\
		val_type_inters_node=v_val_netwk.get_di_intersections()[\
		v_val_netwk.get_di_entry_links_to_network()[\
		queue_phase.get_associated_phase_to_queue()[0]].get_id_head_intersection_node()].get_type_intersection(),\
		val_current_inters_matrix_with_the_associated_link_of_phase=\
		v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_links_to_network()[queue_phase.get_associated_phase_to_queue()[0]].\
		get_id_head_intersection_node()].\
		get_intersection_control_obj().get_di_intersection_control_mat(),\
		val_vehicle_id=self._vehicle.get_id_veh(),\
		val_time_veh_appearance_in_network=self._vehicle.get_t_veh_appearance_at_network(),\
		val_id_veh_entry_link=self._vehicle.get_id_entry_link_veh_ap(),\
		val_id_current_link_veh_location=self._vehicle.get_current_id_link_veh_location(),\
		val_time_veh_arrival_at_current_link=self._vehicle.get_t_vehicle_arrival_at_current_link(),\
		val_veh_current_queue_location=self._vehicle.get_veh_current_queue_location(),\
		val_time_veh_arrival_at_current_queue=self._vehicle.get_t_vehicle_arrival_at_current_queue(),\
		val_veh_id_destination_link=self._vehicle.get_veh_current_queue_location()[List_Explicit_Values.val_second_element_of_list],\
		val_id_event_link=self._id_entry_link,\
		val_current_achieved_queue_service_rate_including_current_vehicle=\
		v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].\
		get_current_reached_service_rate(),\
		val_current_queue_service_rate=\
		v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].\
		get_current_queue_service_rate(),\
		val_li_id_vehicles_in_queue=li_id_veh,\
		val_nb_veh_in_ar_lk=v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].get_current_nb_veh_link(),\
		val_id_veh_final_dest_exit_lk=self._vehicle.get_id_veh_final_destination_link())
		
		#we record the event in the db 
		record_db_obj.fct_write_object_in_db_file()
		


#*****************************************************************************************************************************************************************************************************

#***************************************************Cas Previous Demand-with OD ctrl eval-with sensor monit *******************************************************************************


	#method treating the case when a veh appears, a previously generated demand is being considered, 
	#purpose of the study is to eavluate the control perform,
	# the employed control  requires  sensor monitoring for the t at which is should  be revised 
	def fct_treat_case_veh_appear_previous_demand_with_sensor_monit_ctrl_eval(self,\
	v_val_netwk,v_val_min_veh_hold_time,v_val_type_veh_final_destination,v_val_ti_ctrl_revision_if_decided,v_val_prec_round,v_val_ev_list,\
	v_file_recording_event_db,v_val_dict_entry_link_info_prev_sim,v_val_dict_veh_info_prev_sim,val_min_nb_vehicles_to_detect):
	
		#if the previous demand has generated a veh appearance, (this is  that  we have at least the same number of veh appear)
		if v_val_dict_entry_link_info_prev_sim[self._id_entry_link] !=[]:
		
			t_appear_next_veh=v_val_dict_entry_link_info_prev_sim[self._id_entry_link][0][0]
			
			#creation of the next vehicle
			next_veh=Cl_Vehicle.Vehicle(val_t_veh_appearance_at_network=t_appear_next_veh,\
			val_id_entry_link_veh_ap=self._id_entry_link)
			
			#creation of the next vehicle appearance event
			ev_new_veh_ap=Ev_veh_appearance(val_event_t=t_appear_next_veh,\
			val_vehicle=next_veh,\
			val_current_veh_id_demand_previous_sim=v_val_dict_entry_link_info_prev_sim[self._id_entry_link][0][1])
			
			#we insert the event in the event list
			ev_new_veh_ap.fct_insertion_even_in_event_list(event_list=v_val_ev_list,\
			message="IN CL_EV_VEH_APPEARANCE IN FUNCT\
			fct_treat_case_veh_appear_previous_demand_with_sensor_monit_ctrl_eval ,\
			NEXT VEH APPEARANCE EVENT HAS TIME < TIME FIRST EVENT IN THE LIST")
			
			#we delete the first element of the list corrresponding to the associated entry link
			#val_dict_entry_link_info_previous_sim= dict,key =id entry link, 
			#value= [...,  [t_appearance_veh, veh_id ],...  ] 
			v_val_dict_entry_link_info_prev_sim[self._id_entry_link].remove(v_val_dict_entry_link_info_prev_sim[self._id_entry_link][0])
			
			#we attribute the id to the vehicle
			self._vehicle.set_id_veh(self._current_veh_id_demand_previous_sim)
			
			self._vehicle.set_type_vehicle_final_destination(v_val_type_veh_final_destination)
			
			#we update the vehicle, we indicate the id of the new link location and the time at which it arrived at the new link
			self._vehicle.fct_veh_update_when_appear_at_link(self._id_entry_link,self._event_time)
			
			#we update the number of vehicles in the  link
			#even in the case of infinite management of the internal links; that's why we avoid a test examining if the destination link
			#is  not exit link  but internal if  finite capacity 
			#v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].set_current_nb_veh_link(\
			#v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].get_current_nb_veh_link()+1)
			
			#if we have generated a final destination for the vehicle 
			if self._vehicle.get_id_veh() in v_val_dict_veh_info_prev_sim:
			
				#we associate the final dest to the vehicle 
				self._vehicle.set_id_veh_final_destination_link(v_val_dict_veh_info_prev_sim[self._vehicle.get_id_veh()][2])
				
				#we remove the vehicle if from the dictionary
				del v_val_dict_veh_info_prev_sim[self._vehicle.get_id_veh()]
				
				#we update the indicator of the veh current location  in the que
				new_v=self._vehicle.get_index_current_veh_link_location_in_path_list_when_given_destination()+1
				
				self._vehicle.set_index_current_veh_link_location_in_path_list_when_given_destination(new_v)
				
				#we calculate the que chosen by the vehicle
				li_param_fct_calcul_que_chosen_by_veh=[self._id_entry_link,self._id_entry_link,\
				self._vehicle.get_id_veh_final_destination_link(),\
				self._vehicle.get_index_current_veh_link_location_in_path_list_when_given_destination(),\
				v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].get_id_head_intersection_node()].\
				get_current_di_unique_paths(),v_val_netwk]
			
				#the vehicle queue  object chosen for the vehicle to join in
				queue_phase=self._obj_decisions.fct_calcul_queue_chosen_by_veh_cas_given_final_destination(*\
				li_param_fct_calcul_que_chosen_by_veh)
				
			#if we have not treated this vehicle in the previous sim (so  the veh final destination is not defined)
			else:
				print("PROBLEM IN CL_EV VEH APPEAR, IN FCT fct_treat_case_veh_appear_previous_demand_with_sensor_monit_ctrl_eval,\
				NO FINAL DESTINATION IS DEFIEND FOR THE PREVIOUSLY GENERATED VEH")
				import sys
				sys.exit()
			
			#we update the vehicle, we indicate the chosen queue and its arrival time in the queue
			self._vehicle.fct_update_veh_after_choosing_queue(queue_phase,self._event_time,v_val_netwk)
			
			t_end_veh_hold_time=round(self._event_time+v_val_min_veh_hold_time,v_val_prec_round)
			
			#we examine if there are other vehicles in the que
			if v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
			[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].\
			get_queue_veh()==[]:
				other_veh_in_que_before_add_veh=0
			else:
				other_veh_in_que_before_add_veh=1
				
			#we add the vehicle in the queue
			v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
			[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].\
			fct_update_veh_queue_when_veh_prohibited_to_leave_no_mod(self._vehicle)
			
			#we indicate the time at which the vehicle hold in the queue  ceases
			self._vehicle.set_t_end_veh_hold_time_que(t_end_veh_hold_time)
			
			#if there are no veh in the que (otherwise veh will keave with ev end veh departure) 
			if other_veh_in_que_before_add_veh==0:
			
				#creat ev_end_hold_time
				ev_end_hold_time=Cl_Ev_end_veh_hold_at_que.Ev_end_veh_hold_at_que(val_event_t= t_end_veh_hold_time,\
				val_id_que=queue_phase.get_associated_phase_to_queue())
					
				#we add the event in the event list
				ev_end_hold_time.fct_insertion_even_in_event_list(event_list=v_val_ev_list,\
				message="IN CL_EV_VEH_APPEARANCE IN FUNCT\
				fct_treat_case_veh_appear_previous_demand_with_sensor_monit_ctrl_eval,\
				EVENT END HOLD TIME HAS TIME < TIME FIRST EVENT IN THE LIST")
			
			#if the queue is not a right turn 
			if queue_phase.get_type_veh_queue()!=Cl_Vehicle_Queue.TYPE_VEHICLE_QUEUE["right_turn"]:
			
				#if there is at least one detector detecting the veh
				if queue_phase.fct_exam_whether_at_least_nb_veh_detected_by_a_que_sensor(val_min_nb_veh_to_detect=val_min_nb_vehicles_to_detect)!=None:
			
					# controle dec update
					ev_end_deci_next_icm=Cl_Ev_end_decision_next_intersection_control.Ev_end_decision_next_intersection_control(\
					val_ev_time=v_val_ti_ctrl_revision_if_decided,\
					val_id_intersection_node=v_val_netwk.get_di_all_links()[self._id_entry_link].get_id_head_intersection_node(),\
					val_type_control_to_employ=\
					v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].\
					get_id_head_intersection_node()].get_ctrl_actuate_obj().get_type_employed_ctrl(),\
					val_control_category="sensor_requirement")
					#,val_reason_ctrl_revision_t_lim=0)	
		
					#on insert the event ev_end_dec_next_icm into the event list
					ev_end_deci_next_icm.fct_insertion_even_in_event_list(event_list=v_val_ev_list,\
					message="IN CL_Ev_appear IN FUNCT \
					fct_treat_case_veh_appear_previous_demand_with_sensor_monit_ctrl_eval\
					NEXT ev_new_end_dec_netw_control EVENT HAS TIME < TIME FIRST EVENT IN THE LIST")
				
					#we indicate the intersection that a ctrl request is made
					#v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].get_id_head_intersection_node()].\
					#set_t_last_request_ctrl_revision_when_flux_monitoring(v_val_ti_ctrl_revision_if_decided)
					
					#we indicate the number of times a control revision is asked for the same time
					#v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].get_id_head_intersection_node()].\
					#set_nb_times_ctrl_revision_corresponding_to_t_last_request_ctrl_revision_when_flux_monitoring(\
					#v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].get_id_head_intersection_node()].\
					#set_nb_times_ctrl_revision_corresponding_to_t_last_request_ctrl_revision_when_flux_monitoring()+1)
			
			li_id_veh=[]
			for i in v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
			[queue_phase.get_associated_phase_to_queue()[0],\
			queue_phase.get_associated_phase_to_queue()[1]].get_queue_veh():
					
				li_id_veh.append(i.get_id_veh())
				
			#we create an record database object 
			record_db_obj=Cl_Record_Database.Record_Database(\
			val_file_db=v_file_recording_event_db,\
			val_ev_time=self._event_time,\
			val_ev_type=self._event_type,\
			val_id_inters_node=[v_val_netwk.get_di_entry_links_to_network()[\
			queue_phase.get_associated_phase_to_queue()[0]].get_id_head_intersection_node()],\
			val_t_start_current_inters_control=v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_links_to_network()[\
			queue_phase.get_associated_phase_to_queue()[0]].\
			get_id_head_intersection_node()].get_intersection_control_obj().get_t_start_control(),\
			val_duration_current_inters_control=v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_links_to_network()[\
			queue_phase.get_associated_phase_to_queue()[0]].\
			get_id_head_intersection_node()].get_intersection_control_obj().get_duration_control(),\
			val_current_inters_matrix_with_the_associated_link_of_phase=\
			v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_links_to_network()[\
			queue_phase.get_associated_phase_to_queue()[0]].get_id_head_intersection_node()].\
			get_intersection_control_obj().\
			get_di_intersection_control_mat(),\
			val_duration_current_cycle=v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_links_to_network()[\
			queue_phase.get_associated_phase_to_queue()[0]].\
			get_id_head_intersection_node()].get_intersection_control_obj().\
			get_cycle_duration_associated_with_control(),\
			val_vehicle_id=self._vehicle.get_id_veh(),\
			val_time_veh_appearance_in_network=self._vehicle.get_t_veh_appearance_at_network(),\
			val_id_veh_entry_link=self._vehicle.get_id_entry_link_veh_ap(),\
			val_id_current_link_veh_location=self._vehicle.get_current_id_link_veh_location(),\
			val_time_veh_arrival_at_current_link=self._vehicle.get_t_vehicle_arrival_at_current_link(),\
			val_time_veh_departure_from_current_link=self._vehicle.get_t_vehicle_departure_from_current_link(),\
			val_veh_current_queue_location=self._vehicle.get_veh_current_queue_location(),\
			val_time_veh_arrival_at_current_queue=self._vehicle.get_t_vehicle_arrival_at_current_queue(),\
			val_time_veh_start_departure_from_current_queue=self._vehicle.get_t_vehicle_started_departure_from_current_queue(),\
			val_time_veh_departure_from_current_queue=self._vehicle.get_t_vehicle_departure_from_current_queue(),\
			val_veh_id_destination_link=self._vehicle.get_veh_current_queue_location()[List_Explicit_Values.val_second_element_of_list],\
			val_time_veh_exit_from_network=self._vehicle.get_t_exit_veh_from_network(),\
			val_id_event_link=self._id_entry_link,\
			val_current_achieved_queue_service_rate_including_current_vehicle=\
			v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
			[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].\
			get_current_reached_service_rate(),\
			val_current_queue_service_rate=\
			v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
			[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].\
			get_current_queue_service_rate(),\
			val_li_id_vehicles_in_queue=li_id_veh,\
			val_nb_veh_in_ar_lk=v_val_netwk.get_di_all_links()[i.get_current_id_link_veh_location()].get_current_nb_veh_link(),\
			val_id_veh_final_dest_exit_lk=self._vehicle.get_id_veh_final_destination_link())
			#val_prob_rout_prop_current_lk=val_netwk.get_dict_mat_od_key_id_entry_internal_lk_value_list_dest_lks()[\
			#queue_phase.get_associated_phase_to_queue()[0]])	
						
			#we record the event in the db 
			record_db_obj.fct_write_object_in_db_file()
	
		#if the previous demand has not generated a veh appearance, (this is  that  we have at least the same number of veh appear)
		else:
			print("PROBLEM IN CL EV VEH APPEAR,  fct_treat_case_veh_appear_previous_demand_with_sensor_monit_ctrl_eval")
			import sys
			sys.exit()
	
	
#*****************************************************************************************************************************************************************************************



#*****************************************************************************************************************************************************************************************************

#***************************************************Cas Previous Demand-with OD-rout algo eval-without sensor monit *********************************************************************
	#method treating the case when a veh appears, a previously generated demand is being considered,,
	#purpose of the study is to eavluate the rout algorothm perform,
	# the employed control does not require  sensor monitoring for the t at which is should  be revised 
	def fct_treat_case_veh_appear_previous_demand_without_sensor_monit_rout_algo_eval(self,\
	v_val_netwk,v_val_type_veh_final_destination,v_val_min_veh_hold_time,v_val_prec_round,v_val_ev_list,v_file_recording_event_db,\
	v_val_dict_entry_link_info_prev_sim,v_val_dict_veh_info_prev_sim,v_val_fct_calc_queue_id_when_given_final_dest_and_path_dynam_constructed):
	
		#if the previous demand has generated a veh appearance, (this is  that  we have at least the same number of veh appear)
		if v_val_dict_entry_link_info_prev_sim[self._id_entry_link] !=[]:
		
			t_appear_next_veh=v_val_dict_entry_link_info_prev_sim[self._id_entry_link][0][0]
			
			#creation of the next vehicle
			next_veh=Cl_Vehicle.Vehicle(val_t_veh_appearance_at_network=t_appear_next_veh,\
			val_id_entry_link_veh_ap=self._id_entry_link)
			
			#creation of the next vehicle appearance event
			ev_new_veh_ap=Ev_veh_appearance(val_event_t=t_appear_next_veh,\
			val_vehicle=next_veh,\
			val_current_veh_id_demand_previous_sim=v_val_dict_entry_link_info_prev_sim[self._id_entry_link][0][1])
			
			#we insert the event in the event list
			ev_new_veh_ap.fct_insertion_even_in_event_list(event_list=v_val_ev_list,\
			message="IN CL_EV_VEH_APPEARANCE IN FUNCT fct_treat_case_veh_appear_previous_demand_without_sensor_monit_rout_algo_eval,\
			NEXT VEH APPEARANCE EVENT HAS TIME < TIME FIRST EVENT IN THE LIST")
			
			#we delete the first element of the list corrresponding to the associated entry link
			#val_dict_entry_link_info_previous_sim= dict,key =id entry link, 
			#value= [...,  [t_appearance_veh, veh_id ],...  ] 
			v_val_dict_entry_link_info_prev_sim[self._id_entry_link].remove(v_val_dict_entry_link_info_prev_sim[self._id_entry_link][0])
			
			#we attribute the id to the vehicle
			self._vehicle.set_id_veh(self._current_veh_id_demand_previous_sim)
			
			self._vehicle.set_type_vehicle_final_destination(v_val_type_veh_final_destination)
			
			#we update the vehicle, we indicate the id of the new link location and the time at which it arrived at the new link
			self._vehicle.fct_veh_update_when_appear_at_link(self._id_entry_link,self._event_time)
			
			
			#we update the number of vehicles in the  link
			#even in the case of infinite management of the internal links; that's why we avoid a test examining if the destination link
			#is  not exit link  but internal if  finite capacity 
			#v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].set_current_nb_veh_link(\
			#v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].get_current_nb_veh_link()+1)
			
			#if we have generated a final destination for the vehicle 
			if self._vehicle.get_id_veh() in v_val_dict_veh_info_prev_sim:
			
				#we associate the final dest to the vehicle 
				self._vehicle.set_id_veh_final_destination_link(v_val_dict_veh_info_prev_sim[self._vehicle.get_id_veh()][2])
				
				#we remove the vehicle id from the dictionary
				del v_val_dict_veh_info_prev_sim[self._vehicle.get_id_veh()]
				
				#we update the indicator of the veh current location  in the que
				#new_v=self._vehicle.get_index_current_veh_link_location_in_path_list_when_given_destination()+1
				
				#self._vehicle.set_index_current_veh_link_location_in_path_list_when_given_destination(new_v)
				
				#we calculate the que chosen by the vehicle
				li_param_fct_calcul_que_chosen_by_veh=[\
				v_val_netwk,self._id_entry_link,self._vehicle.get_id_veh_final_destination_link(),v_val_fct_calc_queue_id_when_given_final_dest_and_path_dynam_constructed]
		
				id_dest_lk=self._obj_decisions.fct_calcul_queue_chosen_by_veh_cas_given_final_destination_dyn_constr_path(*\
				li_param_fct_calcul_que_chosen_by_veh)
		
				#the vehicle queue  object chosen for the vehicle to join in
				queue_phase=v_val_netwk.get_di_entry_internal_links()[self._id_entry_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()[\
				self._id_entry_link,id_dest_lk]
				
			
			#if we have not treated this vehicle in the previous sim (so  the veh final destination is not defined)
			else:
				print("PROBLEM IN CL_EV_VEH_APPEAR,  IN FCT, \
				 fct_treat_case_veh_appear_previous_demand_without_sensor_monit_rout_algo_eval,\
				FINAL DEST AND PATH ARE INIT GIVEN AND  VEH FINAL DEST IS NOT AVAILABLE,self._vehicle.get_id_veh() in v_val_dict_veh_info_prev_sim",\
				self._vehicle.get_id_veh() in v_val_dict_veh_info_prev_sim)
				import sys
				sys.exit()
				
			#we update the vehicle, we indicate the chosen queue and its arrival time in the queue
			self._vehicle.fct_update_veh_after_choosing_queue(queue_phase,self._event_time,v_val_netwk)
			
			t_end_veh_hold_time=round(self._event_time+v_val_min_veh_hold_time,v_val_prec_round)
			
			#we examine if there are other vehicles in the que
			if v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
			[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].\
			get_queue_veh()==[]:
				other_veh_in_que_before_add_veh=0
			else:
				other_veh_in_que_before_add_veh=1
				
			#we add the vehicle in the queue
			v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
			[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].\
			fct_update_veh_queue_when_veh_prohibited_to_leave_no_mod(self._vehicle)
			
			#we indicate the time at which the vehicle hold in the queue  ceases
			self._vehicle.set_t_end_veh_hold_time_que(t_end_veh_hold_time)
			
			#if there are no veh in the que (otherwise veh will keave with ev end veh departure) 
			if other_veh_in_que_before_add_veh==0:
			
				#creat ev_end_hold_time
				ev_end_hold_time=Cl_Ev_end_veh_hold_at_que.Ev_end_veh_hold_at_que(val_event_t= t_end_veh_hold_time,\
				val_id_que=queue_phase.get_associated_phase_to_queue())
					
				#we add the event in the event list
				ev_end_hold_time.fct_insertion_even_in_event_list(event_list=v_val_ev_list,\
				message="IN CL_EV_VEH_APPEARANCE IN FUNCT ffct_treat_case_veh_appear_previous_demand_without_sensor_monit_rout_algo_eval,\
				EVENT END HOLD TIME HAS TIME < TIME FIRST EVENT IN THE LIST")
		
		#if the previous demand has not generated a veh appearance, (this is  that  we have at least the same number of veh appear)
		else:
			print("PROBLEM IN CL EV VEH APPEAR, \
			 fct_treat_case_veh_appear_previous_demand_without_sensor_monit_rout_algo_eval")
			import sys
			sys.exit()
			
		li_id_veh=[]
		for i in v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].get_set_veh_queue().\
		get_di_obj_veh_queue_at_link()\
		[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].get_queue_veh():
		
			li_id_veh.append(i.get_id_veh())
			
		#we create an record database object 
		record_db_obj=Cl_Record_Database.Record_Database(\
		val_file_db=v_file_recording_event_db,\
		val_ev_time=self._event_time,\
		val_ev_type=self._event_type,\
		val_id_inters_node=v_val_netwk.get_di_entry_links_to_network()[\
		queue_phase.get_associated_phase_to_queue()[0]].get_id_head_intersection_node(),\
		val_type_inters_node=v_val_netwk.get_di_intersections()[\
		v_val_netwk.get_di_entry_links_to_network()[\
		queue_phase.get_associated_phase_to_queue()[0]].get_id_head_intersection_node()].get_type_intersection(),\
		val_current_inters_matrix_with_the_associated_link_of_phase=\
		v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_links_to_network()[queue_phase.get_associated_phase_to_queue()[0]].\
		get_id_head_intersection_node()].\
		get_intersection_control_obj().get_di_intersection_control_mat(),\
		val_vehicle_id=self._vehicle.get_id_veh(),\
		val_time_veh_appearance_in_network=self._vehicle.get_t_veh_appearance_at_network(),\
		val_id_veh_entry_link=self._vehicle.get_id_entry_link_veh_ap(),\
		val_id_current_link_veh_location=self._vehicle.get_current_id_link_veh_location(),\
		val_time_veh_arrival_at_current_link=self._vehicle.get_t_vehicle_arrival_at_current_link(),\
		val_veh_current_queue_location=self._vehicle.get_veh_current_queue_location(),\
		val_time_veh_arrival_at_current_queue=self._vehicle.get_t_vehicle_arrival_at_current_queue(),\
		val_veh_id_destination_link=self._vehicle.get_veh_current_queue_location()[List_Explicit_Values.val_second_element_of_list],\
		val_id_event_link=self._id_entry_link,\
		val_current_achieved_queue_service_rate_including_current_vehicle=\
		v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].\
		get_current_reached_service_rate(),\
		val_current_queue_service_rate=\
		v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].\
		get_current_queue_service_rate(),\
		val_li_id_vehicles_in_queue=li_id_veh,\
		val_nb_veh_in_ar_lk=v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].get_current_nb_veh_link(),\
		val_id_veh_final_dest_exit_lk=self._vehicle.get_id_veh_final_destination_link())
		
		#we record the event in the db 
		record_db_obj.fct_write_object_in_db_file()
		


#*****************************************************************************************************************************************************************************************************

#***************************************************Cas Previous Demand-with OD ctrl eval-with sensor monit *******************************************************************************


	#method treating the case when a veh appears, a previously generated demand is being considered, 
	#purpose of the study is to eavluate the rout algo perform,
	# the employed control  requires  sensor monitoring for the t at which is should  be revised 
	def fct_treat_case_veh_appear_previous_demand_with_sensor_monit_rout_algo_eval(self,\
	v_val_netwk,v_val_min_veh_hold_time,v_val_type_veh_final_destination,v_val_ti_ctrl_revision_if_decided,v_val_prec_round,v_val_ev_list,\
	v_file_recording_event_db,v_val_dict_entry_link_info_prev_sim,v_val_dict_veh_info_prev_sim,\
	v_val_fct_calc_queue_id_when_given_final_dest_and_path_dynam_constructed,val_min_nb_vehicles_to_detect):
	
		#if the previous demand has generated a veh appearance, (this is  that  we have at least the same number of veh appear)
		if v_val_dict_entry_link_info_prev_sim[self._id_entry_link] !=[]:
		
			t_appear_next_veh=v_val_dict_entry_link_info_prev_sim[self._id_entry_link][0][0]
			
			#creation of the next vehicle
			next_veh=Cl_Vehicle.Vehicle(val_t_veh_appearance_at_network=t_appear_next_veh,\
			val_id_entry_link_veh_ap=self._id_entry_link)
			
			#creation of the next vehicle appearance event
			ev_new_veh_ap=Ev_veh_appearance(val_event_t=t_appear_next_veh,\
			val_vehicle=next_veh,\
			val_current_veh_id_demand_previous_sim=v_val_dict_entry_link_info_prev_sim[self._id_entry_link][0][1])
			
			#we insert the event in the event list
			ev_new_veh_ap.fct_insertion_even_in_event_list(event_list=v_val_ev_list,\
			message="IN CL_EV_VEH_APPEARANCE IN FUNCT\
			fct_treat_case_veh_appear_previous_demand_with_sensor_monit_rout_algo_eval,\
			NEXT VEH APPEARANCE EVENT HAS TIME < TIME FIRST EVENT IN THE LIST")
			
			#we delete the first element of the list corrresponding to the associated entry link
			#val_dict_entry_link_info_previous_sim= dict,key =id entry link, 
			#value= [...,  [t_appearance_veh, veh_id ],...  ] 
			v_val_dict_entry_link_info_prev_sim[self._id_entry_link].remove(v_val_dict_entry_link_info_prev_sim[self._id_entry_link][0])
			
			#we attribute the id to the vehicle
			self._vehicle.set_id_veh(self._current_veh_id_demand_previous_sim)
			
			self._vehicle.set_type_vehicle_final_destination(v_val_type_veh_final_destination)
			
			#we update the vehicle, we indicate the id of the new link location and the time at which it arrived at the new link
			self._vehicle.fct_veh_update_when_appear_at_link(self._id_entry_link,self._event_time)
			
			#we update the number of vehicles in the  link
			#even in the case of infinite management of the internal links; that's why we avoid a test examining if the destination link
			#is  not exit link  but internal if  finite capacity 
			#v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].set_current_nb_veh_link(\
			#v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].get_current_nb_veh_link()+1)
			
			#if we have generated a final destination for the vehicle 
			if self._vehicle.get_id_veh() in v_val_dict_veh_info_prev_sim:
			
				#we associate the final dest to the vehicle 
				self._vehicle.set_id_veh_final_destination_link(v_val_dict_veh_info_prev_sim[self._vehicle.get_id_veh()][2])
				
				#we remove the vehicle if from the dictionary
				del v_val_dict_veh_info_prev_sim[self._vehicle.get_id_veh()]
				
				#we update the indicator of the veh current location  in the que
				#new_v=self._vehicle.get_index_current_veh_link_location_in_path_list_when_given_destination()+1
				
				#self._vehicle.set_index_current_veh_link_location_in_path_list_when_given_destination(new_v)
				
				
				#we calculate the que chosen by the vehicle
				li_param_fct_calcul_que_chosen_by_veh=[\
				v_val_netwk,self._id_entry_link,self._vehicle.get_id_veh_final_destination_link(),v_val_fct_calc_queue_id_when_given_final_dest_and_path_dynam_constructed]
		
				id_dest_lk=self._obj_decisions.fct_calcul_queue_chosen_by_veh_cas_given_final_destination_dyn_constr_path(*\
				li_param_fct_calcul_que_chosen_by_veh)
		
				#the vehicle queue  object chosen for the vehicle to join in
				queue_phase=v_val_netwk.get_di_entry_internal_links()[self._id_entry_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()[\
				self._id_entry_link,id_dest_lk]
				
			#if we have not treated this vehicle in the previous sim (so  the veh final destination is not defined)
			else:
				print("PROBLEM IN CL_EV VEH APPEAR, IN FCT fct_treat_case_veh_appear_previous_demand_with_sensor_monit_rout_algo_eval,\
				NO FINAL DESTINATION IS DEFIEND FOR THE PREVIOUSLY GENERATED VEH")
				import sys
				sys.exit()
			
			#we update the vehicle, we indicate the chosen queue and its arrival time in the queue
			self._vehicle.fct_update_veh_after_choosing_queue(queue_phase,self._event_time,v_val_netwk)
			
			t_end_veh_hold_time=round(self._event_time+v_val_min_veh_hold_time,v_val_prec_round)
			
			#we examine if there are other vehicles in the que
			if v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
			[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].\
			get_queue_veh()==[]:
				other_veh_in_que_before_add_veh=0
			else:
				other_veh_in_que_before_add_veh=1
				
			#we add the vehicle in the queue
			v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
			[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].\
			fct_update_veh_queue_when_veh_prohibited_to_leave_no_mod(self._vehicle)
			
			#we indicate the time at which the vehicle hold in the queue  ceases
			self._vehicle.set_t_end_veh_hold_time_que(t_end_veh_hold_time)
			
			#if there are no veh in the que (otherwise veh will keave with ev end veh departure) 
			if other_veh_in_que_before_add_veh==0:
			
				#creat ev_end_hold_time
				ev_end_hold_time=Cl_Ev_end_veh_hold_at_que.Ev_end_veh_hold_at_que(val_event_t= t_end_veh_hold_time,\
				val_id_que=queue_phase.get_associated_phase_to_queue())
					
				#we add the event in the event list
				ev_end_hold_time.fct_insertion_even_in_event_list(event_list=v_val_ev_list,\
				message="IN CL_EV_VEH_APPEARANCE IN FUNCT\
				fct_treat_case_veh_appear_previous_demand_with_sensor_monit_rout_algo_eval,\
				EVENT END HOLD TIME HAS TIME < TIME FIRST EVENT IN THE LIST")
			
			#if the queue is not a right turn 
			if queue_phase.get_type_veh_queue()!=Cl_Vehicle_Queue.TYPE_VEHICLE_QUEUE["right_turn"]:
			
				#if there is at least one detector detecting the veh
				if queue_phase.fct_exam_whether_at_least_nb_veh_detected_by_a_que_sensor(val_min_nb_veh_to_detect=val_min_nb_vehicles_to_detect)!=None:
			
					# controle dec update
					ev_end_deci_next_icm=Cl_Ev_end_decision_next_intersection_control.Ev_end_decision_next_intersection_control(\
					val_ev_time=v_val_ti_ctrl_revision_if_decided,\
					val_id_intersection_node=v_val_netwk.get_di_all_links()[self._id_entry_link].get_id_head_intersection_node(),\
					val_type_control_to_employ=\
					v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].\
					get_id_head_intersection_node()].get_ctrl_actuate_obj().get_type_employed_ctrl(),\
					val_control_category="sensor_requirement")
					#,val_reason_ctrl_revision_t_lim=0)	
		
					#on insert the event ev_end_dec_next_icm into the event list
					ev_end_deci_next_icm.fct_insertion_even_in_event_list(event_list=v_val_ev_list,\
					message="IN CL_Ev_appear IN FUNCT \
					fct_treat_case_veh_appear_previous_demand_with_sensor_monit_rout_algo_evall\
					NEXT ev_new_end_dec_netw_control EVENT HAS TIME < TIME FIRST EVENT IN THE LIST")
						
					#we indicate the intersection that a ctrl request is made
					#v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].get_id_head_intersection_node()].\
					#set_t_last_request_ctrl_revision_when_flux_monitoring(v_val_ti_ctrl_revision_if_decided)
				
					#we indicate the number of times a control revision is asked for the same time
					#v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].get_id_head_intersection_node()].\
					#set_nb_times_ctrl_revision_corresponding_to_t_last_request_ctrl_revision_when_flux_monitoring(\
					#v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].get_id_head_intersection_node()].\
					#set_nb_times_ctrl_revision_corresponding_to_t_last_request_ctrl_revision_when_flux_monitoring()+1)
			
			li_id_veh=[]
			for i in v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
			[queue_phase.get_associated_phase_to_queue()[0],\
			queue_phase.get_associated_phase_to_queue()[1]].get_queue_veh():
					
				li_id_veh.append(i.get_id_veh())
				
			#we create an record database object 
			record_db_obj=Cl_Record_Database.Record_Database(\
			val_file_db=v_file_recording_event_db,\
			val_ev_time=self._event_time,\
			val_ev_type=self._event_type,\
			val_id_inters_node=[v_val_netwk.get_di_entry_links_to_network()[\
			queue_phase.get_associated_phase_to_queue()[0]].get_id_head_intersection_node()],\
			val_t_start_current_inters_control=v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_links_to_network()[\
			queue_phase.get_associated_phase_to_queue()[0]].\
			get_id_head_intersection_node()].get_intersection_control_obj().get_t_start_control(),\
			val_duration_current_inters_control=v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_links_to_network()[\
			queue_phase.get_associated_phase_to_queue()[0]].\
			get_id_head_intersection_node()].get_intersection_control_obj().get_duration_control(),\
			val_current_inters_matrix_with_the_associated_link_of_phase=\
			v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_links_to_network()[\
			queue_phase.get_associated_phase_to_queue()[0]].get_id_head_intersection_node()].\
			get_intersection_control_obj().\
			get_di_intersection_control_mat(),\
			val_duration_current_cycle=v_val_netwk.get_di_intersections()[v_val_netwk.get_di_entry_links_to_network()[\
			queue_phase.get_associated_phase_to_queue()[0]].\
			get_id_head_intersection_node()].get_intersection_control_obj().\
			get_cycle_duration_associated_with_control(),\
			val_vehicle_id=self._vehicle.get_id_veh(),\
			val_time_veh_appearance_in_network=self._vehicle.get_t_veh_appearance_at_network(),\
			val_id_veh_entry_link=self._vehicle.get_id_entry_link_veh_ap(),\
			val_id_current_link_veh_location=self._vehicle.get_current_id_link_veh_location(),\
			val_time_veh_arrival_at_current_link=self._vehicle.get_t_vehicle_arrival_at_current_link(),\
			val_time_veh_departure_from_current_link=self._vehicle.get_t_vehicle_departure_from_current_link(),\
			val_veh_current_queue_location=self._vehicle.get_veh_current_queue_location(),\
			val_time_veh_arrival_at_current_queue=self._vehicle.get_t_vehicle_arrival_at_current_queue(),\
			val_time_veh_start_departure_from_current_queue=self._vehicle.get_t_vehicle_started_departure_from_current_queue(),\
			val_time_veh_departure_from_current_queue=self._vehicle.get_t_vehicle_departure_from_current_queue(),\
			val_veh_id_destination_link=self._vehicle.get_veh_current_queue_location()[List_Explicit_Values.val_second_element_of_list],\
			val_time_veh_exit_from_network=self._vehicle.get_t_exit_veh_from_network(),\
			val_id_event_link=self._id_entry_link,\
			val_current_achieved_queue_service_rate_including_current_vehicle=\
			v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
			[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].\
			get_current_reached_service_rate(),\
			val_current_queue_service_rate=\
			v_val_netwk.get_di_entry_links_to_network()[self._id_entry_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
			[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].\
			get_current_queue_service_rate(),\
			val_li_id_vehicles_in_queue=li_id_veh,\
			val_nb_veh_in_ar_lk=v_val_netwk.get_di_all_links()[i.get_current_id_link_veh_location()].get_current_nb_veh_link(),\
			val_id_veh_final_dest_exit_lk=self._vehicle.get_id_veh_final_destination_link())
			#val_prob_rout_prop_current_lk=val_netwk.get_dict_mat_od_key_id_entry_internal_lk_value_list_dest_lks()[\
			#queue_phase.get_associated_phase_to_queue()[0]])	
						
			#we record the event in the db 
			record_db_obj.fct_write_object_in_db_file()
	
		#if the previous demand has not generated a veh appearance, (this is  that  we have at least the same number of veh appear)
		else:
			print("PROBLEM IN CL EV VEH APPEAR,  fct_treat_case_veh_appear_previous_demand_with_sensor_monit_rout_algo_eval")
			import sys
			sys.exit()
	
	
#*****************************************************************************************************************************************************************************************


#************************************Case New Demand-Without OD*****************************************************************************************************************
	#method treating the case where a new demand is been employed, the vehicle final destination is not initally defined, 
	def fct_treat_case_new_demand_final_dest_and_path_dynam_defined(self,val_veh_id,val_network,\
	val_type_veh_final_destination,val_min_veh_hold_time,val_prec_round,val_ev_list,val_file_recording_event_db,\
	val_min_nb_veh_to_detect):
	
			
		#if the control revision does not require sensor monitoring for its t revision
		if val_network.get_di_intersections()[val_network.get_di_entry_internal_links()\
		[self._id_entry_link].get_id_head_intersection_node()].get_intersection_control_obj().get_type_control_related_to_t_revision()==\
		Cl_Control_Actuate.TYPE_CONTROL_T_REVISION_CATEGORY["without_sensor_requirement_for_t_update"]:
			
			self.fct_treat_case_veh_appear_new_demand_final_dest_and_path_dynam_defined_without_sensor_monit(\
			v_val_veh_id=val_veh_id,v_val_netwk=val_network,v_val_type_veh_final_destination=val_type_veh_final_destination,\
			v_val_min_veh_hold_time=val_min_veh_hold_time,\
			v_val_prec_round=val_prec_round,v_val_ev_list=val_ev_list,v_file_recording_event_db=val_file_recording_event_db)

		
		#if the control revision requires sensor monitoring for its t revision
		elif val_network.get_di_intersections()[val_network.get_di_entry_internal_links()\
		[self._id_entry_link].get_id_head_intersection_node()].get_intersection_control_obj().get_type_control_related_to_t_revision()==\
		Cl_Control_Actuate.TYPE_CONTROL_T_REVISION_CATEGORY["sensor_requirement_for_t_update"]:
		
			#the time at which the cotnrol will be revised if a revision will be decided by the control
			val_ti_ctrl_revision_if_decided=self._obj_decisions.fct_calculate_t_ctrl_revision(t_cur=self._event_time,dur=\
			val_network.get_di_intersections()[val_network.get_di_entry_internal_links()\
			[self._id_entry_link].get_id_head_intersection_node()].get_intersection_control_obj().\
			get_t_duration_for_defining_t_ctrl_revision_when_at_given_time_sensor_records_veh_variation())
			

			self.fct_treat_case_veh_appear_new_demand_final_dest_and_path_dynam_defined_with_sensor_monit(\
			v_val_veh_id=val_veh_id,v_val_netwk=val_network,v_val_type_veh_final_destination=val_type_veh_final_destination,\
			v_val_min_veh_hold_time=val_min_veh_hold_time,\
			v_val_ti_ctrl_revision_if_decided=val_ti_ctrl_revision_if_decided,\
			v_val_prec_round=val_prec_round,v_val_ev_list=val_ev_list,v_file_recording_event_db=val_file_recording_event_db,\
			val_min_nb_vehicles_to_detect=val_min_nb_veh_to_detect)
			
		#if the control type related to the t revision is not of the previous cases
		else:
			print("PROBLEM IN CL_EV_VEH_APPEAR, FCT  fct_treat_case_new_demand_final_dest_and_path_dynam_defined, CTRL TYPE RELATED TO T REVISION:",\
			val_network.get_di_intersections()[val_network.get_di_entry_internal_links()\
			[self._id_entry_link].get_id_head_intersection_node()].get_intersection_control_obj().get_type_control_related_to_t_revision())
			import sys
			sys.exit()

#*****************************************************************************************************************************************************************************************

#************************************Case New Demand-With OD given path********************************************************************************************************
	#method treating the case when a veh appears, a new generated demand is being considered, the vehicle final destination and path are defined by its appearance
	def fct_treat_case_new_demand_final_dest_and_path_initial_defined(self,\
	val_veh_id,val_netwk,val_type_veh_final_destination,val_min_veh_hold_time,val_prec_round,val_ev_list,val_file_recording_event_db,\
	val_min_nb_vehicles_to_detect):
	
		#if the control revision does not require sensor monitoring for its t revision
		if val_netwk.get_di_intersections()[val_netwk.get_di_entry_internal_links()\
		[self._id_entry_link].get_id_head_intersection_node()].get_intersection_control_obj().get_type_control_related_to_t_revision()==\
		Cl_Control_Actuate.TYPE_CONTROL_T_REVISION_CATEGORY["without_sensor_requirement_for_t_update"]:
		
			self.fct_treat_case_veh_appear_new_demand_final_dest_and_path_intial_defined_without_sensor_monit(\
			v_val_veh_id=val_veh_id,v_val_netwk=val_netwk,v_val_type_veh_final_destination=val_type_veh_final_destination,\
			v_val_min_veh_hold_time=val_min_veh_hold_time,\
			v_val_prec_round=val_prec_round,v_val_ev_list=val_ev_list,v_file_recording_event_db=val_file_recording_event_db)
		
		#if the control  requireSsensor monitoring for its t  revision
		elif val_netwk.get_di_intersections()[val_netwk.get_di_entry_internal_links()\
		[self._id_entry_link].get_id_head_intersection_node()].get_intersection_control_obj().get_type_control_related_to_t_revision()==\
		Cl_Control_Actuate.TYPE_CONTROL_T_REVISION_CATEGORY["sensor_requirement_for_t_update"]:
		
			#the time at which the cotnrol will be revised if a revision will be decided by the control
			val_ti_ctrl_revision_if_decided=self._obj_decisions.fct_calculate_t_ctrl_revision(t_cur=self._event_time,dur=\
			val_netwk.get_di_intersections()[val_netwk.get_di_entry_internal_links()\
			[self._id_entry_link].get_id_head_intersection_node()].get_intersection_control_obj().\
			get_t_duration_for_defining_t_ctrl_revision_when_at_given_time_sensor_records_veh_variation())
			
			self.fct_treat_case_veh_appear_new_demand_final_dest_and_path_intial_defined_with_sensor_monit(\
			v_val_veh_id=val_veh_id,v_val_netwk=val_netwk,v_val_type_veh_final_destination=val_type_veh_final_destination,\
			v_val_min_veh_hold_time=val_min_veh_hold_time,\
			v_val_prec_round=val_prec_round,v_val_ev_list=val_ev_list,\
			v_val_ti_ctrl_revision_if_decided=val_ti_ctrl_revision_if_decided,\
			v_file_recording_event_db=val_file_recording_event_db,\
			val_min_nb_vehicles_to_detect=val_min_nb_veh_to_detect)
			
		#if the control type related to the t revision is not of the previous cases
		else:
			print("PROBLEM IN CL_EV_VEH_APPEAR, FCT  fct_treat_case_new_demand_final_dest_and_path_initial_defined, CTRL TYPE RELATED TO T REVISION:",\
			val_netwk.get_di_intersections()[val_network.get_di_entry_internal_links()\
			[self._id_entry_link].get_id_head_intersection_node()].get_intersection_control_obj().get_type_control_related_to_t_revision())
			import sys
			sys.exit()
	

#************************************Case New Demand-With OD and dyn computed path*****************************************************************************
	#method treating the case when a veh appears, a new generated demand is being considered, the vehicle final destination id defined by its appearance
	
	def fct_treat_case_new_demand_final_dest_initial_defined_path_dyn_computed(self,\
	val_veh_id,val_netwk,val_type_veh_final_destination,val_min_veh_hold_time,val_prec_round,val_ev_list,val_file_recording_event_db,\
	val_fct_calc_queue_id_when_given_final_dest_and_path_dynam_constructed,val_min_nb_veh_to_detect):
	
		#if the control revision does not require sensor monitoring for its t revision
		if val_netwk.get_di_intersections()[val_netwk.get_di_entry_internal_links()\
		[self._id_entry_link].get_id_head_intersection_node()].get_intersection_control_obj().get_type_control_related_to_t_revision()==\
		Cl_Control_Actuate.TYPE_CONTROL_T_REVISION_CATEGORY["without_sensor_requirement_for_t_update"]:
		
			self.fct_treat_case_veh_appear_new_demand_final_dest_intial_defined_path_dyn_computed_without_sensor_monit(\
			v_val_veh_id=val_veh_id,v_val_netwk=val_netwk,v_val_type_veh_final_destination=val_type_veh_final_destination,\
			v_val_min_veh_hold_time=val_min_veh_hold_time,\
			v_val_prec_round=val_prec_round,v_val_ev_list=val_ev_list,v_file_recording_event_db=val_file_recording_event_db,\
			v_val_fct_calc_queue_id_when_given_final_dest_and_path_dynam_constructed=val_fct_calc_queue_id_when_given_final_dest_and_path_dynam_constructed)
		
		#if the control  requires sensor monitor for its t revision
		elif val_netwk.get_di_intersections()[val_netwk.get_di_entry_internal_links()\
		[self._id_entry_link].get_id_head_intersection_node()].get_intersection_control_obj().get_type_control_related_to_t_revision()==\
		Cl_Control_Actuate.TYPE_CONTROL_T_REVISION_CATEGORY["sensor_requirement_for_t_update"]:
		
		
			#the time at which the cotnrol will be revised if a revision will be decided by the control
			val_ti_ctrl_revision_if_decided=self._obj_decisions.fct_calculate_t_ctrl_revision(t_cur=self._event_time,dur=\
			val_netwk.get_di_intersections()[val_netwk.get_di_entry_internal_links()\
			[self._id_entry_link].get_id_head_intersection_node()].get_intersection_control_obj().\
			get_t_duration_for_defining_t_ctrl_revision_when_at_given_time_sensor_records_veh_variation())
		
		
			self.fct_treat_case_veh_appear_new_demand_final_dest_intial_defined_path_dyn_computed_with_sensor_monit(self,\
			v_val_veh_id=val_veh_id,v_val_netwk=val_netwk,v_val_type_veh_final_destination=val_type_veh_final_destination,\
			v_val_min_veh_hold_time=val_min_veh_hold_time,\
			v_val_ti_ctrl_revision_if_decided=val_ti_ctrl_revision_if_decided,\
			v_val_prec=val_prec_round_round,v_val_ev_list=val_ev_list,\
			v_file_recording_event_db=val_file_recording_event_db,\
			v_val_fct_calc_queue_id_when_given_final_dest_and_path_dynam_constructed=val_fct_calc_queue_id_when_given_final_dest_and_path_dynam_constructed,\
			val_min_nb_vehicles_to_detect=val_min_nb_veh_to_detect)
			
		#if the control type related to the t revision is not of the previous cases
		else:
			print("PROBLEM IN CL_EV_VEH_APPEAR, FCT fct_treat_case_new_demand_final_dest_initial_defined_path_dyn_computed, CTRL TYPE RELATED TO T REVISION:",\
			val_netwk.get_di_intersections()[val_network.get_di_entry_internal_links()\
			[self._id_entry_link].get_id_head_intersection_node()].get_intersection_control_obj().get_type_control_related_to_t_revision())
			import sys
			sys.exit()

#******************************************************************************************************************************************************************************************
#*****************************************************************Cas Previous Demand-without OD***************************************************************************************
	#method treating the case when a veh appears, a previously generated demand is being considered, 
	#the vehicle final destination and path were dyn decided,(in prev demand)
	def fct_treat_case_previous_demand_final_dest_and_path_dyn_defined(self,\
	val_netwk,val_type_veh_final_destination,val_min_veh_hold_time,val_prec_round,val_ev_list,val_file_recording_event_db,\
	val_dict_entry_link_info_prev_sim,val_dict_veh_info_prev_sim,val_min_nb_veh_to_detect):
	
		#if the control revision does not require sensor monitoring for its t revision
		if val_netwk.get_di_intersections()[val_netwk.get_di_entry_internal_links()\
		[self._id_entry_link].get_id_head_intersection_node()].get_intersection_control_obj().get_type_control_related_to_t_revision()==\
		Cl_Control_Actuate.TYPE_CONTROL_T_REVISION_CATEGORY["without_sensor_requirement_for_t_update"]:
				
			self.fct_treat_case_veh_appear_previous_demand_final_dest_and_path_dyn_defined_without_sensor_monit(\
			v_val_netwk=val_netwk,v_val_type_veh_final_destination=val_type_veh_final_destination,\
			v_val_min_veh_hold_time=val_min_veh_hold_time,\
			v_val_prec_round=val_prec_round,v_val_ev_list=val_ev_list,v_file_recording_event_db=val_file_recording_event_db,\
			v_val_dict_entry_link_info_prev_sim=val_dict_entry_link_info_prev_sim,v_val_dict_veh_info_prev_sim=val_dict_veh_info_prev_sim)
		
		#if the control  requires sensor monitor for its t revision
		elif val_netwk.get_di_intersections()[val_netwk.get_di_entry_internal_links()\
		[self._id_entry_link].get_id_head_intersection_node()].get_intersection_control_obj().get_type_control_related_to_t_revision()==\
		Cl_Control_Actuate.TYPE_CONTROL_T_REVISION_CATEGORY["sensor_requirement_for_t_update"]:
		
			#the time at which the cotnrol will be revised if a revision will be decided by the control
			val_ti_ctrl_revision_if_decided=self._obj_decisions.fct_calculate_t_ctrl_revision(t_cur=self._event_time,dur=\
			val_netwk.get_di_intersections()[val_network.get_di_entry_internal_links()\
			[self._id_entry_link].get_id_head_intersection_node()].get_intersection_control_obj().\
			get_t_duration_for_defining_t_ctrl_revision_when_at_given_time_sensor_records_veh_variation())
		
			self.fct_treat_case_veh_appear_previous_demand_final_dest_and_path_dyn_defined_with_sensor_monit(\
			v_val_netwk=val_netwk,v_val_min_veh_hold_time=val_min_veh_hold_time,v_val_type_veh_final_destination=val_type_veh_final_destination,\
			v_val_ti_ctrl_revision_if_decided=val_ti_ctrl_revision_if_decided,\
			v_val_prec_round=val_prec_round,\
			v_val_ev_list=val_ev_list,v_file_recording_event_db=val_file_recording_event_db,v_val_dict_entry_link_info_prev_sim=val_dict_entry_link_info_prev_sim,\
			v_val_dict_veh_info_prev_sim=val_dict_veh_info_prev_sim,\
			val_min_nb_vehicles_to_detect=val_min_nb_veh_to_detect)
			
		#if the control type related to the t revision is not of the previous cases
		else:
			print("PROBLEM IN CL_EV_VEH_APPEAR, FCT fct_treat_case_previous_demand_final_dest_and_path_dyn_defined, CTRL TYPE RELATED TO T REVISION:",\
			val_netwk.get_di_intersections()[val_network.get_di_entry_internal_links()\
			[self._id_entry_link].get_id_head_intersection_node()].get_intersection_control_obj().get_type_control_related_to_t_revision())
			import sys
			sys.exit()
	
#******************************************************************************************************************************************************************************************
#***************************************************Cas Previous Demand-with OD - ctrl eval**************************************************************************************************
	#method treating the case when a veh appears, a previously generated demand is being considered, the vehicle final destination is predefined,
	#and the purpose of the study is to eval the control
	
	def fct_treat_case_veh_appear_previous_demand_final_dest_given_ctrl_eval(self,\
	val_netwk,val_type_veh_final_destination,val_min_veh_hold_time,val_prec_round,val_ev_list,\
	val_file_recording_event_db,val_dict_entry_link_info_prev_sim,val_dict_veh_info_prev_sim,val_min_nb_veh_to_detect):
	
		#if the control revision does not require sensor monitoring for its t revision
		if val_netwk.get_di_intersections()[val_netwk.get_di_entry_internal_links()\
		[self._id_entry_link].get_id_head_intersection_node()].get_intersection_control_obj().get_type_control_related_to_t_revision()==\
		Cl_Control_Actuate.TYPE_CONTROL_T_REVISION_CATEGORY["without_sensor_requirement_for_t_update"]:
		
			self.fct_treat_case_veh_appear_previous_demand_without_sensor_monit_ctr_eval(\
			v_val_netwk=val_netwk,v_val_type_veh_final_destination=val_type_veh_final_destination,v_val_min_veh_hold_time=val_min_veh_hold_time,\
			v_val_prec_round=val_prec_round,v_val_ev_list=val_ev_list,v_file_recording_event_db=val_file_recording_event_db,\
			v_val_dict_entry_link_info_prev_sim=val_dict_entry_link_info_prev_sim,v_val_dict_veh_info_prev_sim=val_dict_veh_info_prev_sim)
		
			
		
		#if the control  requires sensor monitor for its t revision
		elif val_netwk.get_di_intersections()[val_netwk.get_di_entry_internal_links()\
		[self._id_entry_link].get_id_head_intersection_node()].get_intersection_control_obj().get_type_control_related_to_t_revision()==\
		Cl_Control_Actuate.TYPE_CONTROL_T_REVISION_CATEGORY["sensor_requirement_for_t_update"]:
		
			#the time at which the cotnrol will be revised if a revision will be decided by the control
			val_ti_ctrl_revision_if_decided=self._obj_decisions.fct_calculate_t_ctrl_revision(t_cur=self._event_time,dur=\
			val_netwk.get_di_intersections()[val_netwk.get_di_entry_internal_links()\
			[self._id_entry_link].get_id_head_intersection_node()].get_intersection_control_obj().\
			get_t_duration_for_defining_t_ctrl_revision_when_at_given_time_sensor_records_veh_variation())
		
			self.fct_treat_case_veh_appear_previous_demand_with_sensor_monit_ctrl_eval(\
			v_val_netwk=val_netwk,v_val_min_veh_hold_time=val_min_veh_hold_time,v_val_type_veh_final_destination=val_type_veh_final_destination,\
			v_val_ti_ctrl_revision_if_decided=val_ti_ctrl_revision_if_decided,\
			v_val_prec_round=val_prec_round,v_val_ev_list=val_ev_list,\
			v_file_recording_event_db=val_file_recording_event_db,v_val_dict_entry_link_info_prev_sim=val_dict_entry_link_info_prev_sim,\
			v_val_dict_veh_info_prev_sim=val_dict_veh_info_prev_sim,val_min_nb_vehicles_to_detect=val_min_nb_veh_to_detect)

		#if the control type related to the t revision is not of the previous cases
		else:
			print("PROBLEM IN CL_EV_VEH_APPEAR, FCT fct_treat_case_veh_appear_previous_demand_final_dest_given_ctrl_eval,\
			CTRL TYPE RELATED TO T REVISION:",\
			val_netwk.get_di_intersections()[val_network.get_di_entry_internal_links()\
			[self._id_entry_link].get_id_head_intersection_node()].get_intersection_control_obj().get_type_control_related_to_t_revision())
			import sys
			sys.exit()
#******************************************************************************************************************************************************************************************


#***************************************************Cas Previous Demand-with OD rout algo*****************************************************************************
	#method treating the case when a veh appears, a previously generated demand is being considered, the vehicle final destination is predefined,
	#and the purpose of the study is to eval the rout algo
	
	def fct_treat_case_veh_appear_previous_demand_final_dest_given_rout_algo_eval(self,\
	val_netwk,val_type_veh_final_destination,val_min_veh_hold_time,val_prec_round,val_ev_list,\
	val_file_recording_event_db,val_dict_entry_link_info_prev_sim,val_dict_veh_info_prev_sim,\
	val_fct_calc_queue_id_when_given_final_dest_and_path_dynam_constructed,val_min_nb_veh_to_detect):
	
		#if the control revision does not require sensor monitoring for its t revision
		if val_netwk.get_di_intersections()[val_netwk.get_di_entry_internal_links()\
		[self._id_entry_link].get_id_head_intersection_node()].get_intersection_control_obj().get_type_control_related_to_t_revision()==\
		Cl_Control_Actuate.TYPE_CONTROL_T_REVISION_CATEGORY["without_sensor_requirement_for_t_update"]:
		
			self.fct_treat_case_veh_appear_previous_demand_without_sensor_monit_rout_algo_eval(\
			v_val_netwk=val_netwk,v_val_type_veh_final_destination=val_type_veh_final_destination,v_val_min_veh_hold_time=val_min_veh_hold_time,\
			v_val_prec_round=val_prec_round,v_val_ev_list=val_ev_list,v_file_recording_event_db=val_file_recording_event_db,\
			v_val_dict_entry_link_info_prev_sim=val_dict_entry_link_info_prev_sim,v_val_dict_veh_info_prev_sim=val_dict_veh_info_prev_sim,\
			v_val_fct_calc_queue_id_when_given_final_dest_and_path_dynam_constructed=val_fct_calc_queue_id_when_given_final_dest_and_path_dynam_constructed)
		
			
		
		#if the control  requires sensor monitor for its t revision
		elif val_netwk.get_di_intersections()[val_netwk.get_di_entry_internal_links()\
		[self._id_entry_link].get_id_head_intersection_node()].get_intersection_control_obj().get_type_control_related_to_t_revision()==\
		Cl_Control_Actuate.TYPE_CONTROL_T_REVISION_CATEGORY["sensor_requirement_for_t_update"]:
		
			#the time at which the cotnrol will be revised if a revision will be decided by the control
			val_ti_ctrl_revision_if_decided=self._obj_decisions.fct_calculate_t_ctrl_revision(t_cur=self._event_time,dur=\
			val_netwk.get_di_intersections()[val_network.get_di_entry_internal_links()\
			[self._id_entry_link].get_id_head_intersection_node()].get_intersection_control_obj().\
			get_t_duration_for_defining_t_ctrl_revision_when_at_given_time_sensor_records_veh_variation())
			
			self.fct_treat_case_veh_appear_previous_demand_with_sensor_monit_rout_algo_eval(\
			v_val_netwk=val_netwk,v_val_min_veh_hold_time=val_min_veh_hold_time,v_val_type_veh_final_destinatio=val_type_veh_final_destination,\
			v_val_ti_ctrl_revision_if_decided=val_ti_ctrl_revision_if_decided,\
			v_val_prec_round=val_prec_round,v_val_ev_list=val_ev_list,\
			v_file_recording_event_db=val_file_recording_event_db,v_val_dict_entry_link_info_prev_sim=val_dict_entry_link_info_prev_sim,\
			v_val_dict_veh_info_prev_sim=val_dict_veh_info_prev_sim,\
			v_val_fct_calc_queue_id_when_given_final_dest_and_path_dynam_constructed=val_fct_calc_queue_id_when_given_final_dest_and_path_dynam_constructed,\
			val_min_nb_vehicles_to_detect=val_min_nb_veh_to_detect)
			
		#if the control type related to the t revision is not of the previous cases
		else:
			print("PROBLEM IN CL_EV_VEH_APPEAR, FCT fct_treat_case_veh_appear_previous_demand_final_dest_given_rout_algo_eval,\
			CTRL TYPE RELATED TO T REVISION:",\
			val_network.get_di_intersections()[val_network.get_di_entry_internal_links()\
			[self._id_entry_link].get_id_head_intersection_node()].get_intersection_control_obj().get_type_control_related_to_t_revision())
			import sys
			sys.exit()


#******************************************************************************************************************************************************************************************
	#method treating the event
	def event_treat(self,val_key_fct_in_dict_to_treat,val_li_param_fct_to_treat):
	
		#dictionary with the functions treat each case of this event
		di_fct_ev_treat={1:self.fct_treat_case_new_demand_final_dest_and_path_dynam_defined,2:self.fct_treat_case_new_demand_final_dest_and_path_initial_defined,\
		3:self.fct_treat_case_new_demand_final_dest_initial_defined_path_dyn_computed,4:self.fct_treat_case_previous_demand_final_dest_and_path_dyn_defined,\
		5:self.fct_treat_case_veh_appear_previous_demand_final_dest_given_ctrl_eval,6:self.fct_treat_case_veh_appear_previous_demand_final_dest_given_rout_algo_eval}
		
		
		return di_fct_ev_treat[val_key_fct_in_dict_to_treat](*val_li_param_fct_to_treat)
	
































	











