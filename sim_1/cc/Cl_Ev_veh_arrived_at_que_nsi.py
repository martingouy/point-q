import string
import Cl_Event
import List_Explicit_Values
import Cl_Global_Functions
import Cl_Ev_end_veh_hold_at_que_nsi
import Cl_Vehicle_Queue
import Cl_Decisions
import Cl_Vehicle
import Cl_Record_Database

class Ev_veh_arrived_at_que_nsi(Cl_Event.Event):

	""" class defining the event of vehicle arrival at a queue of a link (when considering that a link had many queues) or at a new link"""
	
	def __init__(self,val_event_t=-1,val_li_vehicle=None,val_id_arrival_link=-1):
	
		gl_funct_obj=Cl_Global_Functions.Global_Functions()
		
		Cl_Event.Event.__init__(self,val_event_time=val_event_t,val_event_type=Cl_Event.TYPE_EV["type_ev_veh_arrived_at_que_nsi"],\
		val_global_fct_obj=gl_funct_obj)
		
		
		#the list of vehicles arriving at the link
		self._li_vehicle=val_li_vehicle
		
		#the id of the link
		self._id_arrival_link=val_id_arrival_link
		
		
		#the decision object  associated with this event
		obj_decisions=Cl_Decisions.Decisions()
		
		self._obj_decisions=obj_decisions
		
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
	#method treating the case when new generated vehicles will join a que
	def fct_treat_case_new_veh_demand_veh_join_que_nsi(self,val_netwk,\
	val_min_veh_hold_time,val_prec_round,val_ev_list,file_recording_event_db):

		#for each vehicle
		for i in self._li_vehicle:
		
			#if a final destination is related to the vehicle by its appearance in the network
			if i.get_id_veh_final_destination_link() >0:
			
				#we update the indicator of the veh current location  in the que
				new_v=i.get_index_current_veh_link_location_in_path_list_when_given_destination()+1
			
				i.set_index_current_veh_link_location_in_path_list_when_given_destination(new_v)
				
				#we calculate the que chosen by the vehicle
				li_param_fct_calcul_que_chosen_by_veh=[i.get_id_entry_link_veh_ap(),self._id_arrival_link,\
				i.get_id_veh_final_destination_link(),\
				i.get_index_current_veh_link_location_in_path_list_when_given_destination(),\
				val_netwk.get_di_intersections()[val_netwk.get_di_entry_links_to_network()[i.get_id_entry_link_veh_ap()].\
				get_id_head_intersection_node()].get_current_di_unique_paths(),val_netwk]
			
			
				#the vehicle queue  object chosen for the vehicle to join in
				queue_phase=self._obj_decisions.fct_calcul_queue_chosen_by_veh_cas_given_final_destination(*\
				li_param_fct_calcul_que_chosen_by_veh)
			
			
			
			#if no final destination is related to the vehicle by its appearance in the network
			else:
				#we calculate the que chosen by the vehicle
					
				lis_param_fct_calcul_queue_chosen_by_veh_from_cum_fct=[self._id_arrival_link,\
				val_network.get_dict_mat_rp_cum_key_entry_intern_lk_value_list_cum_fct_values()]
			
				#rep=[[ random uniform nb, id veh lk location, id dest lk]]
				rep=self._obj_decisions.fct_calcul_queue_chosen_by_veh_from_cum_fct(\
				*lis_param_fct_calcul_queue_chosen_by_veh_from_cum_fct)
			
				lis_param_fct_calcul_queue_chosen_by_veh=[self._id_arrival_link,\
				rep[List_Explicit_Values.val_third_element_of_list],val_network]
				
				queue_phase=self._obj_decisions.fct_calcul_queue_chosen_by_veh(*lis_param_fct_calcul_queue_chosen_by_veh)
			
			#we update the vehicle, we indicate the chosen queue and its arrival time in the queue
			i.fct_update_veh_after_choosing_queue(queue_phase.get_associated_phase_to_queue(),self._event_time)
		
		
			#we examine if vehicle can leave the queue immediately
			veh_can_leave_que=self._obj_decisions.fct_defining_whether_veh_can_leave_que_by_its_arrival()
			
			#if the vehicle can leave the que
			if veh_can_leave_que==List_Explicit_Values.initialisation_value_to_one:
				print("PROBLEM IN CL_Ev_veh_arrived_at_que_nsi, veh_can_leave_que: ",veh_can_leave_que)
				import sys
				sys.exit()
			
			#if the vehicle cannot leave the que
			else:
			
				t_end_veh_hold_time=round(self._event_time+val_min_veh_hold_time,val_prec_round)
				
				#we examine if there are other vehicles in the que
				
				if val_netwk.get_di_entry_internal_links()[self._id_arrival_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
				[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].\
				get_queue_veh()==[]:
					other_veh_in_que_before_add_veh=0
				else:
					other_veh_in_que_before_add_veh=1
					
				
				#we add the vehicle in the queue
				val_netwk.get_di_entry_internal_links()[self._id_arrival_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
				[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].\
				fct_update_veh_queue_when_veh_prohibited_to_leave(i)
				
				#we indicate the time at which the vehicle can leave the que regarding the hold duration
				i.set_t_end_veh_hold_time_que(t_end_veh_hold_time)
				
				#si que dif de RT, on ajout le vehicule dans le heap 
				if val_netwk.get_di_entry_internal_links()[self._id_arrival_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
				[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].get_type_veh_queue()!=\
				Cl_Vehicle_Queue.TYPE_VEHICLE_QUEUE["right_turn"]:
		
					#we add the veh in the inter heap, sorted according to its end hold time
					i.fct_insertion_veh_in_veh_list(vehicle_list=val_netwk.get_di_intersections()[\
					val_netwk.get_di_entry_internal_links()[self._id_arrival_link].get_id_head_intersection_node()].\
					get_di_key_id_phase_value_heap_veh()[\
					queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]])
				
		
				#if there are no veh in the que (otherwise veh will leave with ev end veh departure) 
				if other_veh_in_que_before_add_veh==0:
					
					#creat ev_end_hold_time
					ev_end_hold_time_nsi=Cl_Ev_end_veh_hold_at_que_nsi.Ev_end_veh_hold_at_que_nsi(val_event_t= t_end_veh_hold_time,\
					val_id_que=queue_phase.get_associated_phase_to_queue())
					
					#we add the event in the event list
					ev_end_hold_time_nsi.fct_insertion_even_in_event_list(event_list=val_ev_list,\
					message="IN CL_EV_VEH_ARRIVED_QUE IN FUNCT ffct_treat_case_new_veh_demand_veh_join_que,\
					EVENT END HOLD TIME HAS TIME < TIME FIRST EVENT IN THE LIST")
				
			
				
			li_id_veh=[]
			for i in val_netwk.get_di_entry_internal_links()[self._id_arrival_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
			[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].get_queue_veh():
				li_id_veh.append(i.get_id_veh())
			
	
			#we create an record database object 
			record_db_obj=Cl_Record_Database.Record_Database(val_file_db=file_recording_event_db,\
			val_ev_time=self._event_time,val_ev_type=self._event_type,\
			val_vehicle_id=i.get_id_veh(),\
			val_time_veh_appearance_in_network=i.get_t_veh_appearance_at_network(),\
			val_id_veh_entry_link=i.get_id_entry_link_veh_ap(),\
			val_id_current_link_veh_location=i.get_current_id_link_veh_location(),\
			val_time_veh_arrival_at_current_link=i.get_t_vehicle_arrival_at_current_link(),\
			val_time_veh_departure_from_current_link=i.get_t_vehicle_departure_from_current_link(),\
			val_veh_current_queue_location=i.get_veh_current_queue_location(),\
			val_time_veh_arrival_at_current_queue=i.get_t_vehicle_arrival_at_current_queue(),\
			val_time_veh_start_departure_from_current_queue=i.get_t_vehicle_started_departure_from_current_queue(),\
			val_time_veh_departure_from_current_queue=i.get_t_vehicle_departure_from_current_queue(),\
			val_veh_id_destination_link=i.get_veh_current_queue_location()[List_Explicit_Values.val_second_element_of_list],\
			val_time_veh_exit_from_network=i.get_t_exit_veh_from_network(),\
			val_id_event_link=self._id_arrival_link,\
			val_veh_can_leave_now=veh_can_leave_que,\
			val_current_achieved_queue_service_rate_including_current_vehicle=\
			val_netwk.get_di_entry_internal_links()[self._id_arrival_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
			[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].\
			get_current_reached_service_rate(),\
			val_current_queue_service_rate=\
			val_netwk.get_di_entry_internal_links()[self._id_arrival_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
			[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].\
			get_current_queue_service_rate(),\
			val_li_id_vehicles_in_queue=li_id_veh,\
			val_nb_veh_in_ar_lk=val_netwk.get_di_all_links()[i.get_current_id_link_veh_location()].get_current_nb_veh_link())
			#,\
			#val_prob_rout_prop_current_lk=val_netwk.get_dict_mat_od_key_id_entry_internal_lk_value_list_dest_lks()[\
			#queue_phase.get_associated_phase_to_queue()[0]])
				
			#we record the event in the db 
			record_db_obj.fct_write_object_in_db_file()
			
			#if the vehicle will leave immediately, (if the arrival time is >0)
			#if li_queue_phase_t_ar[1]>List_Explicit_Values.initialisation_value_to_zero:
				#we initialise the vehicle
				#i.fct_initialising_veh_before_its_departure()
		
#*****************************************************************************************************************************************************************************************
	#method treating the case when previously generated vehicles  arrive at an internal link
	def fct_treat_case_prev_veh_demand_join_que_nsi(self,val_netwk,\
	val_min_veh_hold_time,val_prec_round,val_ev_list,file_recording_event_db,val_dict_vehicle_info_prev_sim):
	
		#for each vehicle
		for i in self._li_vehicle:
		
			#if in the previous sim we have generated as many vehicle destinations
			#val_dict_vehicle_info_prev_sim=dict key is the veh id and 
			#val_dict_vehicle_info_prev_sim[i.get_id_veh()]=
			#[[t_vehicle_appearance_in_the_network, [id_entry_link, id_destination_link_1, id_destination_link_2,.... ] ]
			if len(val_dict_vehicle_info_prev_sim[i.get_id_veh()][1]) != List_Explicit_Values.initialisation_value_to_one:
			
			
				#the vehicle queue  object chosen for the vehicle to join in
				queue_phase=val_netwk.get_di_entry_internal_links()[val_dict_vehicle_info_prev_sim[i.get_id_veh()][1][0]].\
				get_set_veh_queue().get_di_obj_veh_queue_at_link()[val_dict_vehicle_info_prev_sim[i.get_id_veh()][1][0],\
				val_dict_vehicle_info_prev_sim[i.get_id_veh()][1][1]]
				
				#we delete the first link location from the veh dictionary 
				#print("HERE",dict_veh_info_prev_sim[val_vehicle.get_id_veh()][1])
				val_dict_vehicle_info_prev_sim[i.get_id_veh()][1].remove(val_dict_vehicle_info_prev_sim[i.get_id_veh()][1][0])
			
			#if in the previous sim we have not generated as many vehicle destinations
			else:
				#if a final destination is related to the vehicle by its appearance in the network
				if i.get_id_veh_final_destination_link() >0:
			
				
					#we update the indicator of the veh current location  in the que
					new_v=i.get_index_current_veh_link_location_in_path_list_when_given_destination()+1
			
					i.set_index_current_veh_link_location_in_path_list_when_given_destination(new_v)
				
					#we calculate the que chosen by the vehicle
					li_param_fct_calcul_que_chosen_by_veh=[i.get_id_entry_link_veh_ap(),self._id_arrival_link,\
					i.get_id_veh_final_destination_link(),\
					i.get_index_current_veh_link_location_in_path_list_when_given_destination(),\
					val_netwk.get_di_intersections()[val_netwk.get_di_entry_links_to_network()[i.get_id_entry_link_veh_ap()].\
					get_id_head_intersection_node()].get_current_di_unique_paths(),val_netwk]
			
			
					#the vehicle queue  object chosen for the vehicle to join in
					queue_phase=self._obj_decisions.fct_calcul_queue_chosen_by_veh_cas_given_final_destination(*\
					li_param_fct_calcul_que_chosen_by_veh)
			
			
			
				#if no final destination is related to the vehicle by its appearance in the network
				else:
					#we calculate the que chosen by the vehicle
					
					lis_param_fct_calcul_queue_chosen_by_veh_from_cum_fct=[self._id_arrival_link,\
					val_network.get_dict_mat_rp_cum_key_entry_intern_lk_value_list_cum_fct_values()]
			
					#rep=[[ random uniform nb, id veh lk location, id dest lk]]
					rep=self._obj_decisions.fct_calcul_queue_chosen_by_veh_from_cum_fct(\
					*lis_param_fct_calcul_queue_chosen_by_veh_from_cum_fct)
			
					lis_param_fct_calcul_queue_chosen_by_veh=[self._id_arrival_link,\
					rep[List_Explicit_Values.val_third_element_of_list],val_network]
				
					queue_phase=self._obj_decisions.fct_calcul_queue_chosen_by_veh(*lis_param_fct_calcul_queue_chosen_by_veh)
			
				
			#we update the vehicle, we indicate the chosen queue and its arrival time in the queue
			i.fct_update_veh_after_choosing_queue(queue_phase.get_associated_phase_to_queue(),self._event_time)
				
			#we update the queue, we increase the number of veh passages  by the queue
			#val_netwk.get_di_entry_internal_links()[self._id_arrival_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()[\
			#queue_phase.get_associated_phase_to_queue()[0],\
			#queue_phase.get_associated_phase_to_queue()[1]].\
			#fct_update_veh_queue_when_veh_ar()		
				
			#we examine if vehicle can leave the queue immediately
			veh_can_leave_que=self._obj_decisions.fct_defining_whether_veh_can_leave_que_by_its_arrival()
				
			#if the vehicle can leave the que
			if veh_can_leave_que==List_Explicit_Values.initialisation_value_to_one:
					
				print("PROBLEM IN CL_Ev_veh_arrived_at_que veh_can_leave_que_nsi, fct_treat_case_prev_veh_demand_join_que_nsi: ",\
				veh_can_leave_que)
				import sys
				sys.exit()
				
			#if the vehicle can not leave the que
			else:
				t_end_veh_hold_time=round(self._event_time+val_min_veh_hold_time,val_prec_round)
			
				#we examine if there are other vehicles in the que
				if val_netwk.get_di_entry_internal_links()[self._id_arrival_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
				[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].\
				get_queue_veh()==[]:
					other_veh_in_que_before_add_veh=0
				else:
					other_veh_in_que_before_add_veh=1


				#we add the vehicle in the queue
				val_netwk.get_di_entry_internal_links()[self._id_arrival_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
				[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].\
				fct_update_veh_queue_when_veh_prohibited_to_leave(i)
				
				#we indicate the time at which the vehicle can leave the que regarding the hold duration
				i.set_t_end_veh_hold_time_que(t_end_veh_hold_time)
				
				#si que dif de RT, on ajout le vehicule dans le heap 
				if val_netwk.get_di_entry_internal_links()[self._id_arrival_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
				[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].get_type_veh_queue()!=\
				Cl_Vehicle_Queue.TYPE_VEHICLE_QUEUE["right_turn"]:
		
					#we add the veh in the inter heap, sorted according to its end hold time
					i.fct_insertion_veh_in_veh_list(vehicle_list=val_netwk.get_di_intersections()[\
					val_netwk.get_di_entry_internal_links()[self._id_arrival_link].get_id_head_intersection_node()].\
					get_di_key_id_phase_value_heap_veh()[\
					queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]])
				
				#if there are no veh in the que (otherwise veh will keave with ev end veh departure) 
				if other_veh_in_que_before_add_veh==0:
				
					#creat ev_end_hold_time
					ev_end_hold_time_nsi=Cl_Ev_end_veh_hold_at_que_nsi.Ev_end_veh_hold_at_que_nsi(val_event_t= t_end_veh_hold_time,\
					val_id_que=queue_phase.get_associated_phase_to_queue())
					
					#we add the event in the event list
					ev_end_hold_time.fct_insertion_even_in_event_list(event_list=val_ev_list,\
					message="IN CL_EV_VEH_ARRIVED_AT_QUE_NSI IN FUNCT fct_treat_case_prev_veh_demand_join_que_nsi,\
					EVENT END HOLD TIME HAS TIME < TIME FIRST EVENT IN THE LIST")
			
					
			
			li_id_veh=[]
			for i in val_netwk.get_di_entry_internal_links()[self._id_arrival_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
			[queue_phase.get_associated_phase_to_queue()[0],\
			queue_phase.get_associated_phase_to_queue()[1]].get_queue_veh():
					
				li_id_veh.append(i.get_id_veh())
				
			#we create an record database object 
			record_db_obj=Cl_Record_Database.Record_Database(val_file_db=file_recording_event_db,\
			val_ev_time=self._event_time,val_ev_type=self._event_type,\
			val_vehicle_id=i.get_id_veh(),\
			val_time_veh_appearance_in_network=i.get_t_veh_appearance_at_network(),\
			val_id_veh_entry_link=i.get_id_entry_link_veh_ap(),\
			val_id_current_link_veh_location=i.get_current_id_link_veh_location(),\
			val_time_veh_arrival_at_current_link=i.get_t_vehicle_arrival_at_current_link(),\
			val_time_veh_departure_from_current_link=i.get_t_vehicle_departure_from_current_link(),\
			val_veh_current_queue_location=i.get_veh_current_queue_location(),\
			val_time_veh_arrival_at_current_queue=i.get_t_vehicle_arrival_at_current_queue(),\
			val_time_veh_start_departure_from_current_queue=i.get_t_vehicle_started_departure_from_current_queue(),\
			val_time_veh_departure_from_current_queue=i.get_t_vehicle_departure_from_current_queue(),\
			val_veh_id_destination_link=i.get_veh_current_queue_location()[List_Explicit_Values.val_second_element_of_list],\
			val_time_veh_exit_from_network=i.get_t_exit_veh_from_network(),\
			val_id_event_link=self._id_arrival_link,\
			val_veh_can_leave_now=veh_can_leave_que,\
			val_current_achieved_queue_service_rate_including_current_vehicle=\
			val_netwk.get_di_entry_internal_links()[self._id_arrival_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
			[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].\
			get_current_reached_service_rate(),\
			val_current_queue_service_rate=\
			val_netwk.get_di_entry_internal_links()[self._id_arrival_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
			[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].\
			get_current_queue_service_rate(),\
			val_li_id_vehicles_in_queue=li_id_veh,\
			val_nb_veh_in_ar_lk=val_netwk.get_di_all_links()[i.get_current_id_link_veh_location()].get_current_nb_veh_link())
			#val_prob_rout_prop_current_lk=val_netwk.get_dict_mat_od_key_id_entry_internal_lk_value_list_dest_lks()[\
			#queue_phase.get_associated_phase_to_queue()[0]])					
			#we record the event in the db 
			record_db_obj.fct_write_object_in_db_file()
			
			#if the vehicle will leave immediately, (if the arrival time is d>0)
			#if li_queue_phase_t_ar[1]>List_Explicit_Values.initialisation_value_to_zero:
				#we initialise the vehicle
				#i.fct_initialising_veh_before_its_departure()


	
		
#*****************************************************************************************************************************************************************************************
	#method treating the event
	def event_treat_1(self):
		pass
		
	def event_treat(self,val_network=None,val_dict_veh_info_prev_data={},val_creation_new_veh_demand=-1,\
	val_min_vehicle_hold_time=-1,val_round_prec=None,event_list=[],\
	fi_recording_event_db=None):
	
		#lis_param_fct_calcul_queue_chosen_by_veh_from_cum_fct=[self._id_arrival_link,\
		#val_network.get_dict_mat_rp_cum_key_entry_intern_lk_value_list_cum_fct_values()]
		
		#rep=self._obj_decisions.fct_calcul_queue_chosen_by_veh_from_cum_fct(\
		#*lis_param_fct_calcul_queue_chosen_by_veh_from_cum_fct)
		
			
		#lis_param_fct_calcul_queue_chosen_by_veh=[self._id_arrival_link,\
		#rep[List_Explicit_Values.val_third_element_of_list],val_network]
		
		#if new veh demand is employed
		if val_creation_new_veh_demand==List_Explicit_Values.initialisation_value_to_one:
			
			self.fct_treat_case_new_veh_demand_veh_join_que_nsi(\
			val_netwk=val_network,\
			val_min_veh_hold_time=val_min_vehicle_hold_time,val_prec_round=val_round_prec,\
			val_ev_list=event_list,file_recording_event_db=fi_recording_event_db)
		
		#if a previously generated demand is employed
		elif  val_creation_new_veh_demand==List_Explicit_Values.initialisation_value_to_zero:
		
			self.fct_treat_case_prev_veh_demand_join_que_nsi(\
			val_netwk=val_network,\
			val_min_veh_hold_time=val_min_vehicle_hold_time,val_prec_round=val_round_prec,\
			val_ev_list=event_list,\
			file_recording_event_db=fi_recording_event_db,val_dict_vehicle_info_prev_sim=val_dict_veh_info_prev_data)
		
		#if a given demand is employed
		elif  val_creation_new_veh_demand==List_Explicit_Values.initialisation_value_to_minus_one:
			self.fct_treat_case_new_veh_demand_veh_join_que_nsi(\
			val_netwk=val_network,\
			val_min_veh_hold_time=val_min_vehicle_hold_time,val_prec_round=val_round_prec,\
			val_ev_list=event_list,file_recording_event_db=fi_recording_event_db)
		
		#if none of the previous cases concerns the demand, there is a problem, we stop the sim
		else:
			print("PROBLEM IN CL_EV_VEH_ARRIVED_AT_QUE_NSI, fct event_treat, val_creation_new_veh_demand=", val_creation_new_veh_demand)
			import sys
			sys.exit()
	
		
#*****************************************************************************************************************************************************************************************
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
		
