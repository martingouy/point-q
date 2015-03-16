import string
import Cl_Event
import List_Explicit_Values
import Cl_Vehicle
import Cl_Global_Functions
import Cl_Decisions
import Cl_Record_Database
import Cl_Vehicle_Queue
import Cl_Ev_end_veh_hold_at_que_nsi


class Ev_veh_appearance_nsi(Cl_Event.Event):

	def __init__(self,val_event_t=-1,val_vehicle=None,val_current_veh_id_demand_previous_sim=-1):
	
		#gl_funct_obj=Cl_Global_Functions.Global_Functions()
		
		Cl_Event.Event.__init__(self,val_event_time=val_event_t,val_event_type=Cl_Event.TYPE_EV["type_ev_veh_appearance_nsi"])
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

	#method treating the event when a new demand is employed
	def fct_treat_veh_ap_ev_nsi_case_new_demand(self,val_veh_id,\
	val_type_veh_final_destination,\
	val_netwrk,val_t_unit, val_min_veh_hold_time,val_round_prec,val_ev_list,\
	val_file_recording_event_db):
	
		#time at which the next veh will appear
		t_appear_next_veh=round(self._event_time+val_netwrk.get_di_entry_links_to_network()\
		[self._id_entry_link].fct_creating_demand_entry_link()*val_t_unit,val_round_prec)
		
		#creation of the next vehicle
		next_veh=Cl_Vehicle.Vehicle(val_t_veh_appearance_at_network=t_appear_next_veh,\
		val_id_entry_link_veh_ap=self._id_entry_link,val_type_vehicle_final_destination=val_type_veh_final_destination)
		
		
		#creation of the next vehicle appearance event
		ev_new_veh_ap_nsi=Ev_veh_appearance_nsi(val_event_t=t_appear_next_veh,\
		val_vehicle=next_veh,val_id_entry_link=self._id_entry_link)
		
		#we insert the event in the event list
		ev_new_veh_ap_nsi.fct_insertion_even_in_event_list(event_list=val_ev_list,\
		message="IN CL_EV_VEH_APPEARANCE_NSI IN FUNCT fct_treat_veh_ap_ev_nsi_case_new_demand,\
		NEXT VEH APPEARANCE EVENT HAS TIME < TIME FIRST EVENT IN THE LIST")
		
		#we attribute the id to the vehicle
		self._vehicle.set_id_veh(val_veh_id)
		
		#we update the number of vehicles in the link
		#val_netwrk.get_di_entry_links_to_network()[self._id_entry_link].set_current_nb_veh_link(val_netwrk.get_di_entry_links_to_network()\
		#[self._id_entry_link].get_current_nb_veh_link()+1)
		
		#we update the vehicle, we indicate the id of the new link location and the time at which it arrived at the new link
		self._vehicle.fct_veh_update_when_appear_at_link(self._id_entry_link,self._event_time)
		
		
		#if a final destination will be related to the vehicle by its appearance in the network 
		if val_type_veh_final_destination==Cl_Vehicle.TYPE_VEH_FINAL_DESTINATION["initially_defined_final_dest"]:
		
			#we calculate the veh final destination
			#li_rep=[unif nb, id current veh loca, selected id exit link ]
			li_rep=self._obj_decisions.fct_calcul_exit_lk_chosen_by_veh_cas_given_final_destination(\
			id_veh_entry_link=self._id_entry_link,\
			di_cum_mod=val_netwrk.get_di_intersections()[val_netwrk.get_di_entry_links_to_network()[self._id_entry_link].\
			get_id_head_intersection_node()].get_current_di_cum_mod())
			
			#we indicate the veh exit link for the record
			veh_exit_lk=li_rep[2]
			
			#we associate the final dest to the vehicle 
			self._vehicle.set_id_veh_final_destination_link(li_rep[2])
			
			#we update the indicator of the veh current location  in the que
			new_v=self._vehicle.get_index_current_veh_link_location_in_path_list_when_given_destination()+1
			
			self._vehicle.set_index_current_veh_link_location_in_path_list_when_given_destination(new_v)
			
					
			#we calculate the que chosen by the vehicle
			li_param_fct_calcul_que_chosen_by_veh=[self._id_entry_link,self._id_entry_link,self._vehicle.get_id_veh_final_destination_link(),\
			self._vehicle.get_index_current_veh_link_location_in_path_list_when_given_destination(),\
			val_netwrk.get_di_intersections()[val_netwrk.get_di_entry_links_to_network()[self._id_entry_link].get_id_head_intersection_node()].\
			get_current_di_unique_paths(),val_netwrk]
			
			
			#the vehicle queue  object chosen for the vehicle to join in
			queue_phase=self._obj_decisions.fct_calcul_queue_chosen_by_veh_cas_given_final_destination(*\
			li_param_fct_calcul_que_chosen_by_veh)
		
		#if the vehicle will not have a given final dest, (it will be dynamically constructed)
		else:
			lis_param_fct_calcul_queue_chosen_by_veh_from_cum_fct=[self._id_entry_link,\
			val_netwrk.get_di_intersections()[val_netwrk.get_di_entry_links_to_network()[self._id_entry_link].\
			get_id_head_intersection_node()].get_current_di_cum_rout_prob_input_lk()]
			
			
			rep=self._obj_decisions.fct_calcul_queue_chosen_by_veh_from_cum_fct(\
			*lis_param_fct_calcul_queue_chosen_by_veh_from_cum_fct)
			
			lis_param_fct_calcul_queue_chosen_by_veh=[self._id_entry_link,rep[List_Explicit_Values.val_third_element_of_list],val_network]
		
		
			queue_phase=self._obj_decisions.fct_calcul_queue_chosen_by_veh(*lis_param_fct_calcul_queue_chosen_by_veh)
		
			veh_exit_lk=-1
		

		
		#we update the vehicle, we indicate the chosen queue and its arrival time in the queue
		self._vehicle.fct_update_veh_after_choosing_queue(queue_phase.get_associated_phase_to_queue(),self._event_time)
		
		t_end_veh_hold_time=round(self._event_time+val_min_veh_hold_time,val_round_prec)
		
		
		#we examine if there are other vehicles in the que, before adding the vehicle
		if val_netwrk.get_di_entry_internal_links()[self._id_entry_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].\
		get_queue_veh()==[]:
			other_veh_in_que_before_add_veh=0
		else:
			other_veh_in_que_before_add_veh=1
			
		#we update queue (add the vehicle in the queue)
		val_netwrk.get_di_entry_internal_links()[self._id_entry_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].\
		fct_update_veh_queue_when_veh_prohibited_to_leave(self._vehicle)
		
		#we indicate the time at which the vehicle hold in the queue  ceases
		self._vehicle.set_t_end_veh_hold_time_que(t_end_veh_hold_time)
		
		#si que dif de RT, on ajout le vehicule dans le heap des veh tries par rapport le temps end hold time, self._di_key_id_phase_value_heap_veh
		if val_netwrk.get_di_entry_internal_links()[self._id_entry_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].get_type_veh_queue()!=\
		Cl_Vehicle_Queue.TYPE_VEHICLE_QUEUE["right_turn"]:
		
			#print("keys",\
			#val_netwrk.get_di_intersections()[\
			#val_netwrk.get_di_entry_internal_links()[self._id_entry_link].get_id_head_intersection_node()].\
			#get_di_key_id_phase_value_heap_veh())
			
			#print()
			#print(queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1])
			
			self._vehicle.fct_insertion_veh_in_veh_list(vehicle_list=\
			val_netwrk.get_di_intersections()[\
			val_netwrk.get_di_entry_internal_links()[self._id_entry_link].get_id_head_intersection_node()].\
			get_di_key_id_phase_value_heap_veh()[\
			queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]])
			
		#if there are no veh in the que (otherwise veh will keave with ev end veh departure) 
		if other_veh_in_que_before_add_veh==0:
			
			#creat ev_end_hold_time
			ev_end_hold_time_nsi=Cl_Ev_end_veh_hold_at_que_nsi.Ev_end_veh_hold_at_que_nsi(val_event_t= t_end_veh_hold_time,\
			val_id_que=queue_phase.get_associated_phase_to_queue())
					
			#we add the event in the event list
			ev_end_hold_time_nsi.fct_insertion_even_in_event_list(event_list=val_ev_list,\
			message="IN CL_EV_VEH_APPEARANCE_nsi IN FUNCT fct_treat_veh_ap_ev_case_new_demandl,\
			EVENT END HOLD_nsi TIME HAS TIME < TIME FIRST EVENT IN THE LIST")
			
			
		li_id_veh=[]
		for i in val_netwrk.get_di_entry_internal_links()[self._id_entry_link].get_set_veh_queue().\
		get_di_obj_veh_queue_at_link()\
		[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].get_queue_veh():
		
			li_id_veh.append(i.get_id_veh())
			
		#we create an record database object 
		record_db_obj=Cl_Record_Database.Record_Database(\
		val_file_db=val_file_recording_event_db,\
		val_ev_time=self._event_time,\
		val_ev_type=self._event_type,\
		val_id_inters_node=val_netwrk.get_di_entry_internal_links()[\
		queue_phase.get_associated_phase_to_queue()[0]].get_id_head_intersection_node(),\
		val_type_inters_node=val_netwrk.get_di_intersections()[\
		val_netwrk.get_di_entry_internal_links()[\
		queue_phase.get_associated_phase_to_queue()[0]].get_id_head_intersection_node()].\
		get_type_intersection(),\
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
		val_netwrk.get_di_entry_internal_links()[self._id_entry_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].\
		get_current_reached_service_rate(),\
		val_current_queue_service_rate=\
		val_netwrk.get_di_entry_internal_links()[self._id_entry_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].\
		get_current_queue_service_rate(),\
		val_li_id_vehicles_in_queue=li_id_veh,\
		val_nb_veh_in_ar_lk=val_netwrk.get_di_entry_internal_links()[self._id_entry_link].get_current_nb_veh_link(),\
		val_id_veh_final_dest_exit_lk=veh_exit_lk)
		
		#we record the event in the db 
		record_db_obj.fct_write_object_in_db_file()
		

#*****************************************************************************************************************************************************************************************
	#method treating the event when a previous demand is employed
	def fct_treat_veh_ap_ev_nsi_case_prev_demand(self,val_veh_id,\
	val_type_veh_final_destination,\
	val_netwrk,val_min_veh_hold_time,val_round_prec,val_ev_list,\
	val_file_recording_event_db,val_dict_entry_link_info_prev_sim,val_dict_veh_info_prev_sim):
	
		#if the previous demand has generated a veh appearance, (this is  that  we have at least the same number of veh appear)
		if len(val_dict_entry_link_info_prev_sim[self._id_entry_link]) !=List_Explicit_Values.initialisation_value_to_zero:
		
			t_appear_next_veh=val_dict_entry_link_info_prev_sim[self._id_entry_link][0][0]
			
			#the entry link is the 1st element of the 3rd element of the diction
			veh=Cl_Vehicle.Vehicle(val_t_veh_appearance_at_network=t_appear_next_veh,\
			val_id_entry_link_veh_ap=val_dict_entry_link_info_prev_sim[self._id_entry_link][0][2][0],val_type_vehicle_final_destination=val_type_veh_final_destination)
			
			ev_new_veh_ap_nsi=Ev_veh_appearance_nsi(val_event_t=t_appear_next_veh,val_vehicle=veh,\
			val_id_entry_link=val_dict_entry_link_info_prev_sim[self._id_entry_link][0][2][0],\
			val_current_veh_id_demand_previous_sim=val_dict_entry_link_info_prev_sim[self._id_entry_link][0][1])
			
			#we insert the event in the event list
			ev_new_veh_ap_nsi.fct_insertion_even_in_event_list(event_list=val_ev_list,\
			message="IN CL_EV_VEH_APPEARANCE NSI IN FUNCT fct_treat_veh_ap_ev_nsi_case_prev_demand,\
			NEXT VEH APPEARANCE EVENT HAS TIME < TIME FIRST EVENT IN THE LIST")
			
			#we delete the first element of the list corrresponding to the associated entry link
			#val_dict_entry_link_info_previous_sim= dict,key =id entry link, 
			#value= [...,  [t_appearance_veh, veh_id, [id_current_link_location_1,id_destination_link_1,...]     ]  ] 
			val_dict_entry_link_info_prev_sim[self._id_entry_link].remove(val_dict_entry_link_info_prev_sim[self._id_entry_link][0])
			
			#we attribute the id to the vehicle
			self._vehicle.set_id_veh(self._current_veh_id_demand_previous_sim)
			
			#we update the vehicle, we indicate the id of the new link location and the time at which it arrived at the new link
			self._vehicle.fct_veh_update_when_appear_at_link(self._id_entry_link,self._event_time)
			
			#if we have generated a destination for the vehicle 
			if len(val_dict_veh_info_prev_sim[self._vehicle.get_id_veh()][1])>List_Explicit_Values.initialisation_value_to_one:
				queue_phase=val_netwrk.get_di_entry_internal_links()[val_dict_veh_info_prev_sim[self._vehicle.get_id_veh()][1][0]].\
				get_set_veh_queue().get_di_obj_veh_queue_at_link()[val_dict_veh_info_prev_sim[self._vehicle.get_id_veh()][1][0],\
				val_dict_veh_info_prev_sim[self._vehicle.get_id_veh()][1][1]]
				
				#we delete the first link location from the veh dictionary 
				val_dict_veh_info_prev_sim[self._vehicle.get_id_veh()][1].remove(val_dict_veh_info_prev_sim[self._vehicle.get_id_veh()][1][0])
				
			#if we have not generated a destination for the vehicle 
			else:
				#if a final destination will be related to the vehicle by its appearance in the network 
				if val_type_veh_final_destination==Cl_Vehicle.TYPE_VEH_FINAL_DESTINATION["initially_defined_final_dest"]:
		
					#we calculate the veh final destination
					#li_rep=[unif nb, id current veh loca, selected id exit link ]
					li_rep=self._obj_decisions.fct_calcul_exit_lk_chosen_by_veh_cas_given_final_destination(\
					id_veh_entry_link=self._id_entry_link,\
					di_cum_mod=val_netwrk.get_di_intersections()[val_netwrk.get_di_entry_links_to_network()[self._id_entry_link].\
					get_id_head_intersection_node()].get_current_di_cum_mod())
			
					#we indicate the veh exit link for the record
					veh_exit_lk=li_rep[2]
			
					#we associate the final dest to the vehicle 
					self._vehicle.set_id_veh_final_destination_link(li_rep[2])
			
					#we update the indicator of the veh current location  in the que
					new_v=self._vehicle.get_index_current_veh_link_location_in_path_list_when_given_destination()+1
			
					self._vehicle.set_index_current_veh_link_location_in_path_list_when_given_destination(new_v)
			
					
					#we calculate the que chosen by the vehicle
					li_param_fct_calcul_que_chosen_by_veh=[self._id_entry_link,self._id_entry_link,\
					self._vehicle.get_id_veh_final_destination_link(),\
					self._vehicle.get_index_current_veh_link_location_in_path_list_when_given_destination(),\
					val_netwrk.get_di_intersections()[val_netwrk.get_di_entry_links_to_network()[self._id_entry_link].get_id_head_intersection_node()].\
					get_current_di_unique_paths(),val_netwrk]
			
			
					#the vehicle queue  object chosen for the vehicle to join in
					queue_phase=self._obj_decisions.fct_calcul_queue_chosen_by_veh_cas_given_final_destination(*\
					li_param_fct_calcul_que_chosen_by_veh)
		
				#if the vehicle will not have a given final dest, (it will be dynamically constructed)
				else:
					lis_param_fct_calcul_queue_chosen_by_veh_from_cum_fct=[self._id_entry_link,\
					val_netwrk.get_di_intersections()[val_netwrk.get_di_entry_links_to_network()[self._id_entry_link].\
					get_id_head_intersection_node()].get_current_di_cum_rout_prob_input_lk()]
			
			
					rep=self._obj_decisions.fct_calcul_queue_chosen_by_veh_from_cum_fct(\
					*lis_param_fct_calcul_queue_chosen_by_veh_from_cum_fct)
			
					lis_param_fct_calcul_queue_chosen_by_veh=[self._id_entry_link,rep[List_Explicit_Values.val_third_element_of_list],val_network]
		
		
					queue_phase=self._obj_decisions.fct_calcul_queue_chosen_by_veh(*lis_param_fct_calcul_queue_chosen_by_veh)
		
					veh_exit_lk=-1
		

				
			#we update the vehicle, we indicate the chosen queue and its arrival time in the queue
			self._vehicle.fct_update_veh_after_choosing_queue(queue_phase.get_associated_phase_to_queue(),self._event_time)
			
			#we update the number of vehicles in the link
			#val_netwrk.get_di_entry_links_to_network()[self._id_entry_link].set_current_nb_veh_link(val_netwrk.get_di_entry_links_to_network()\
			#[self._id_entry_link].get_current_nb_veh_link()+1)
			
			t_end_veh_hold_time=round(self._event_time+val_min_veh_hold_time,val_round_prec)
			
			#we examine if there are other vehicles in the que, before adding the vehicle
			if val_netwrk.get_di_entry_internal_links()[self._id_entry_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
			[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].\
			get_queue_veh()==[]:
				other_veh_in_que_before_add_veh=0
			else:
				other_veh_in_que_before_add_veh=1
				
			#we add the vehicle in the queue
			val_netwrk.get_di_entry_internal_links()[self._id_entry_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
			[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].\
			fct_update_veh_queue_when_veh_prohibited_to_leave(self._vehicle)
			
			#we indicate the time at which the vehicle can leave the que
			self._vehicle.set_t_end_veh_hold_time_que(t_end_veh_hold_time)
			
			
			#si que dif de RT, on ajout le vehicule dans le heap es veh triees par rap leur t_end_hold, self._di_key_id_phase_value_heap_veh
			if val_netwrk.get_di_entry_internal_links()[self._id_entry_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
			[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].get_type_veh_queue()!=\
			Cl_Vehicle_Queue.TYPE_VEHICLE_QUEUE["right_turn"]:
			
				#we add the veh in the inter heap, sorted according to its end hold time
				self._vehicle.fct_insertion_veh_in_veh_list(vehicle_list=\
				val_netwrk.get_di_intersections()[\
				val_netwrk.get_di_entry_internal_links()[self._id_entry_link].get_id_head_intersection_node()].\
				get_di_key_id_phase_value_heap_veh()[\
				queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]])
				
			#if there are no veh in the que (otherwise veh will keave with ev end veh departure) 
			if other_veh_in_que_before_add_veh==0:
			
				#creat ev_end_hold_time
				ev_end_hold_time_nsi=Cl_Ev_end_veh_hold_at_que_nsi.Ev_end_veh_hold_at_que_nsi(val_event_t= t_end_veh_hold_time,\
				val_id_que=queue_phase.get_associated_phase_to_queue())
					
				#we add the event in the event list
				ev_end_hold_time_nsi.fct_insertion_even_in_event_list(event_list=val_ev_list,\
				message="IN CL_EV_VEH_APPEARANCE_NSI  IN FUNCT fct_treat_veh_ap_ev_nsi_case_prev_demand,\
				EVENT END HOLD TIME HAS TIME < TIME FIRST EVENT IN THE LIST")
				
			li_id_veh=[]
			for i in val_netwrk.get_di_entry_internal_links()[self._id_entry_link].get_set_veh_queue().\
			get_di_obj_veh_queue_at_link()[queue_phase.get_associated_phase_to_queue()[0],\
			queue_phase.get_associated_phase_to_queue()[1]].get_queue_veh():
		
				li_id_veh.append(i.get_id_veh())	
				
			#we create an record database object 
			record_db_obj=Cl_Record_Database.Record_Database(\
			val_file_db=val_file_recording_event_db,\
			val_ev_time=self._event_time,\
			val_ev_type=self._event_type,\
			val_id_inters_node=val_netwrk.get_di_entry_internal_links()[\
			queue_phase.get_associated_phase_to_queue()[0]].get_id_head_intersection_node(),\
			val_type_inters_node=val_netwrk.get_di_intersections()[\
			val_netwrk.get_di_entry_internal_links()[\
			queue_phase.get_associated_phase_to_queue()[0]].get_id_head_intersection_node()].\
			get_type_intersection(),\
			val_time_veh_appearance_in_network=self._vehicle.get_t_veh_appearance_at_network(),\
			val_id_veh_entry_link=self._vehicle.get_id_entry_link_veh_ap(),\
			val_id_current_link_veh_location=self._vehicle.get_current_id_link_veh_location(),\
			val_time_veh_arrival_at_current_link=self._vehicle.get_t_vehicle_arrival_at_current_link(),\
			val_veh_current_queue_location=self._vehicle.get_veh_current_queue_location(),\
			val_time_veh_arrival_at_current_queue=self._vehicle.get_t_vehicle_arrival_at_current_queue(),\
			val_veh_id_destination_link=self._vehicle.get_veh_current_queue_location()[List_Explicit_Values.val_second_element_of_list],\
			val_id_event_link=self._id_entry_link,\
			val_current_achieved_queue_service_rate_including_current_vehicle=\
			val_netwrk.get_di_entry_internal_links()[self._id_entry_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
			[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].\
			get_current_reached_service_rate(),\
			val_current_queue_service_rate=\
			val_netwrk.get_di_entry_internal_links()[self._id_entry_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
			[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].\
			get_current_queue_service_rate(),\
			val_li_id_vehicles_in_queue=li_id_veh,\
			val_nb_veh_in_ar_lk=val_netwrk.get_di_entry_internal_links()[self._id_entry_link].get_current_nb_veh_link(),\
			val_id_veh_final_dest_exit_lk=veh_exit_lk)
			
			#we record the event in the db 
			record_db_obj.fct_write_object_in_db_file()

		
		#if the previous demand has not generated a veh appearance, (this is  that  previously we generated less vehicles)
		else:
			print("PROBLEM IN CL EV VEH APPEAR NSI, fct fct_treat_veh_ap_ev_nsi_case_prev_demand, the previous demand has not generated a veh appear")
			import sys
			sys.exit()
	
#*****************************************************************************************************************************************************************************************
	#method treating the event when a given demand is employed (not generates by a sim run for which only veh appearance times are available)
	#val_dict_entry_link_info_given_data dict, key=id entry link, value=[...,t veh appearance, ...]
	def fct_treat_veh_ap_ev_nsi_case_given_demand(self,val_veh_id,\
	val_type_veh_final_destination,\
	val_netwrk,val_min_veh_hold_time,val_round_prec,val_ev_list,\
	val_file_recording_event_db,val_dict_entry_link_info_given_data):
	
		t_appear_next_veh=val_dict_entry_link_info_given_data[self._id_entry_link][0]
		
		#the entry link is the 1st element of the 3rd element of the diction
		veh=Cl_Vehicle.Vehicle(val_t_veh_appearance_at_network=t_appear_next_veh,\
		val_id_entry_link_veh_ap=self._id_entry_link,val_type_vehicle_final_destination=val_type_veh_final_destination)
				
		ev_new_veh_ap_nsi=Ev_veh_appearance_nsi(val_event_t=t_appear_next_veh,val_vehicle=veh,\
		val_id_entry_link=self._id_entry_link)
			
		#we insert the event in the event list
		ev_new_veh_ap.fct_insertion_even_in_event_list(event_list=val_ev_list,\
		message="IN CL_EV_VEH_APPEARANCE nsi IN FUNCT fct_treat_veh_ap_ev_nso_case_given_demand ,\
		NEXT VEH APPEARANCE EVENT HAS TIME < TIME FIRST EVENT IN THE LIST")
		
		#we delete the first element of the list corrresponding to the associated entry link
		val_dict_entry_link_info_given_data[self._id_entry_link].remove(val_dict_entry_link_info_given_data[self._id_entry_link][0])
		
		#we attribute the id to the vehicle
		self._vehicle.set_id_veh(val_veh_id)
		
		#we update the vehicle, we indicate the id of the new link location and the time at which it arrived at the new link
		self._vehicle.fct_veh_update_when_appear_at_link(self._id_entry_link,self._event_time)
		
		#we update the number of vehicles in the link
		val_netwrk.get_di_entry_links_to_network()[self._id_entry_link].set_current_nb_veh_link(val_netwrk.get_di_entry_links_to_network()\
		[self._id_entry_link].get_current_nb_veh_link()+1)
		
		#if a final destination will be related to the vehicle by its appearance in the network 
		if val_type_veh_final_destination==Cl_Vehicle.TYPE_VEH_FINAL_DESTINATION["initially_defined_final_dest"]:
		
			#we calculate the veh final destination
			#li_rep=[unif nb, id current veh loca, selected id exit link ]
			li_rep=self._obj_decisions.fct_calcul_exit_lk_chosen_by_veh_cas_given_final_destination(\
			id_veh_entry_link=self._id_entry_link,\
			di_cum_mod=val_netwrk.get_di_intersections()[val_netwrk.get_di_entry_links_to_network()[self._id_entry_link].\
			get_id_head_intersection_node()].get_current_di_cum_mod())
			
			#we indicate the veh exit link for the record
			veh_exit_lk=li_rep[2]
			
			#we associate the final dest to the vehicle 
			self._vehicle.set_id_veh_final_destination_link(li_rep[2])
			
			#we update the indicator of the veh current location  in the que
			new_v=self._vehicle.get_index_current_veh_link_location_in_path_list_when_given_destination()+1
			
			self._vehicle.set_index_current_veh_link_location_in_path_list_when_given_destination(new_v)
			
					
			#we calculate the que chosen by the vehicle
			li_param_fct_calcul_que_chosen_by_veh=[self._id_entry_link,self._id_entry_link,\
			self._vehicle.get_id_veh_final_destination_link(),\
			self._vehicle.get_index_current_veh_link_location_in_path_list_when_given_destination(),\
			val_netwrk.get_di_intersections()[val_netwrk.get_di_entry_links_to_network()[self._id_entry_link].get_id_head_intersection_node()].\
			get_current_di_unique_paths(),val_netwrk]
			
			
			#the vehicle queue  object chosen for the vehicle to join in
			queue_phase=self._obj_decisions.fct_calcul_queue_chosen_by_veh_cas_given_final_destination(*\
			li_param_fct_calcul_que_chosen_by_veh)
		
		#if the vehicle will not have a given final dest, (it will be dynamically constructed)
		else:
			lis_param_fct_calcul_queue_chosen_by_veh_from_cum_fct=[self._id_entry_link,\
			val_netwrk.get_di_intersections()[val_netwrk.get_di_entry_links_to_network()[self._id_entry_link].\
			get_id_head_intersection_node()].get_current_di_cum_rout_prob_input_lk()]
			
			
			rep=self._obj_decisions.fct_calcul_queue_chosen_by_veh_from_cum_fct(\
			*lis_param_fct_calcul_queue_chosen_by_veh_from_cum_fct)
			
			lis_param_fct_calcul_queue_chosen_by_veh=[self._id_entry_link,rep[List_Explicit_Values.val_third_element_of_list],val_network]
		
		
			queue_phase=self._obj_decisions.fct_calcul_queue_chosen_by_veh(*lis_param_fct_calcul_queue_chosen_by_veh)
		
			veh_exit_lk=-1
		
		#we update the vehicle, we indicate the chosen queue and its arrival time in the queue
		self._vehicle.fct_update_veh_after_choosing_queue(queue_phase.get_associated_phase_to_queue(),self._event_time)
		
		
		t_end_veh_hold_time=round(self._event_time+val_min_veh_hold_time,val_round_prec)
		
		#we examine if there are other vehicles in the que before adding the vehicle
		if val_netwrk.get_di_entry_internal_links()[self._id_entry_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].\
		get_queue_veh()==[]:
			other_veh_in_que_before_add_veh=0
		else:
			other_veh_in_que_before_add_veh=1
		
		#we add the vehicle in the queue
		val_netwrk.get_di_entry_internal_links()[self._id_entry_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].\
		fct_update_veh_queue_when_veh_prohibited_to_leave(self._vehicle)
		
		
		#we indicate the vehicle hold time in queue
		self._vehicle.set_t_end_veh_hold_time_que(t_end_veh_hold_time)
		
		#si que dif de RT, on ajout le vehicule dans le heap 
		if val_netwrk.get_di_entry_internal_links()[self._id_entry_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].get_type_veh_queue()!=\
		Cl_Vehicle_Queue.TYPE_VEHICLE_QUEUE["right_turn"]:
		
			#we add the veh in the inter heap, sorted according to its end hold time
			self._vehicle.fct_insertion_veh_in_veh_list(vehicle_list=\
			val_netwrk.get_di_intersections()[\
			val_netwrk.get_di_entry_internal_links()[self._id_entry_link].get_id_head_intersection_node()].\
			get_di_key_id_phase_value_heap_veh()[\
			queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]])
			
		#if there are no veh in the que (otherwise veh will keave with ev end veh departure) 
		if other_veh_in_que_before_add_veh==0:
			
			#creat ev_end_hold_time
			ev_end_hold_time_nsi=Cl_Ev_end_veh_hold_at_que_nsi.Ev_end_veh_hold_at_que_nsi(val_event_t= t_end_veh_hold_time,\
			val_id_que=queue_phase.get_associated_phase_to_queue())
					
			#we add the event in the event list
			ev_end_hold_time_nsi.fct_insertion_even_in_event_list(event_list=val_ev_list,\
			message="IN CL_EV_VEH_APPEARANCE_nsi IN FUNCT fct_treat_veh_ap_ev_nso_case_given_demand,\
			EVENT END HOLD TIME HAS TIME < TIME FIRST EVENT IN THE LIST")
			
		li_id_veh=[]
		for i in val_netwrk.get_di_entry_internal_links()[self._id_entry_link].get_set_veh_queue().\
		get_di_obj_veh_queue_at_link()[queue_phase.get_associated_phase_to_queue()[0],\
		queue_phase.get_associated_phase_to_queue()[1]].get_queue_veh():
		
			li_id_veh.append(i.get_id_veh())
			
		#we create an record database object 
		record_db_obj=Cl_Record_Database.Record_Database(\
		val_file_db=val_file_recording_event_db,\
		val_ev_time=self._event_time,\
		val_ev_type=self._event_type,\
		val_id_inters_node=val_netwrk.get_di_entry_internal_links()[\
		queue_phase.get_associated_phase_to_queue()[0]].get_id_head_intersection_node(),\
		val_type_inters_node=val_netwrk.get_di_intersections()[\
		val_netwrk.get_di_entry_internal_links()[\
		queue_phase.get_associated_phase_to_queue()[0]].get_id_head_intersection_node()].\
		get_type_intersection(),\
		val_time_veh_appearance_in_network=self._vehicle.get_t_veh_appearance_at_network(),\
		val_id_veh_entry_link=self._vehicle.get_id_entry_link_veh_ap(),\
		val_id_current_link_veh_location=self._vehicle.get_current_id_link_veh_location(),\
		val_time_veh_arrival_at_current_link=self._vehicle.get_t_vehicle_arrival_at_current_link(),\
		val_veh_current_queue_location=self._vehicle.get_veh_current_queue_location(),\
		val_time_veh_arrival_at_current_queue=self._vehicle.get_t_vehicle_arrival_at_current_queue(),\
		val_veh_id_destination_link=self._vehicle.get_veh_current_queue_location()[List_Explicit_Values.val_second_element_of_list],\
		val_id_event_link=self._id_entry_link,\
		val_current_achieved_queue_service_rate_including_current_vehicle=\
		val_netwrk.get_di_entry_internal_links()[self._id_entry_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].\
		get_current_reached_service_rate(),\
		val_current_queue_service_rate=\
		val_netwrk.get_di_entry_internal_links()[self._id_entry_link].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[queue_phase.get_associated_phase_to_queue()[0],queue_phase.get_associated_phase_to_queue()[1]].\
		get_current_queue_service_rate(),\
		val_li_id_vehicles_in_queue=li_id_veh,\
		val_nb_veh_in_ar_lk=val_netwrk.get_di_entry_internal_links()[self._id_entry_link].get_current_nb_veh_link(),\
		val_id_veh_final_dest_exit_lk=veh_exit_lk)


		#we record the event in the db 
		record_db_obj.fct_write_object_in_db_file()
	
	
	
#*****************************************************************************************************************************************************************************************
	#method treating the event
	def event_treat_1(self):
		pass

	#method treating the event
	def event_treat(self,\
	val_vehicle_id=-1,val_type_veh_final_dest=None,val_network=None,\
	val_time_unit=None,val_min_vehicle_hold_time=-1,val_round_prec=2,ev_list=[],val_creation_new_demand=-1,\
	val_dict_entry_link_info_previous_sim={},val_dict_veh_info_previous_sim={},val_dict_entry_link_info_given_data={},\
	file_recording_event_db=None):
	
		#lis_param_fct_calcul_queue_chosen_by_veh_from_cum_fct=[self._id_entry_link,\
		#val_network.get_dict_mat_rp_cum_key_entry_intern_lk_value_list_cum_fct_values()]
		
		
		#rep=[[ random uniform nb, id veh lk location, id dest lk]]
		#rep=self._obj_decisions.fct_calcul_queue_chosen_by_veh_from_cum_fct(\
		#*lis_param_fct_calcul_queue_chosen_by_veh_from_cum_fct)
		
		#lis_param_fct_calcul_queue_chosen_by_veh=[self._id_entry_link,rep[List_Explicit_Values.val_third_element_of_list],val_network]
		
		#if new vehicle demand will be generated
		if val_creation_new_demand==List_Explicit_Values.initialisation_value_to_one:
		
			self.fct_treat_veh_ap_ev_nsi_case_new_demand(val_veh_id=val_vehicle_id,\
			val_type_veh_final_destination=val_type_veh_final_dest,\
			val_netwrk=val_network,val_t_unit=val_time_unit,val_min_veh_hold_time=val_min_vehicle_hold_time,\
			val_round_prec=val_round_prec,\
			val_ev_list=ev_list,\
			val_file_recording_event_db=file_recording_event_db)
		
		#if we wish to employ a previously generated demand (from the sim)
		elif val_creation_new_demand==List_Explicit_Values.initialisation_value_to_zero:
		
			self.fct_treat_veh_ap_ev_nsi_case_prev_demand(val_veh_id=val_vehicle_id,\
			val_type_veh_final_destination=val_type_veh_final_dest,\
			val_netwrk=val_network,val_min_veh_hold_time=val_min_vehicle_hold_time,\
			val_round_prec=val_round_prec,\
			val_ev_list=ev_list,\
			val_file_recording_event_db=file_recording_event_db,\
			val_dict_entry_link_info_prev_sim=val_dict_entry_link_info_previous_sim,\
			val_dict_veh_info_prev_sim=val_dict_veh_info_previous_sim)
		
		#if we wish to employ a given demand
		elif val_creation_new_demand==List_Explicit_Values.initialisation_value_to_minus_one:
		
			self.fct_treat_veh_ap_ev_nsi_case_given_demand(val_veh_id=val_vehicle_id,\
			val_type_veh_final_destination=val_type_veh_final_dest,\
			val_netwrk=val_network,val_min_veh_hold_time=val_min_vehicle_hold_time,\
			val_round_prec=val_round_prec,\
			val_ev_list=ev_list,\
			val_file_recording_event_db=file_recording_event_db,\
			val_dict_entry_link_info_given_data=val_dict_entry_link_info_given_data)
		
		#if none of the previous cases  holds,  there is a problem
		else:
			print("PROBLEM IN CL_EV_VEH_AP_NSI fct event_treat, val_creation_new_demand= ", val_creation_new_demand)
			import sys
			sys.exit()
	
	
	
		


















