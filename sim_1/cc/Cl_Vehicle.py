import List_Explicit_Values
import heapq
from heapq import *


TYPE_STATE_VEH={"veh_dep_planned":1,"other":-1}
TYPE_VEH_FINAL_DESTINATION={"dynam_constructed_final_dest":1,"initially_defined_final_dest":2}

class Vehicle:

	"""class defining a vehicle object """

	def __init__(self,val_id_veh=-1,val_t_veh_appearance_at_network=-1,val_id_entry_link_veh_ap=-1,\
	val_current_id_link_veh_location=-1,val_t_vehicle_arrival_at_current_link=-1,\
	val_t_vehicle_started_departure_from_current_link=-1,val_t_vehicle_departure_from_current_link=-1,\
	val_veh_current_queue_location=-1,val_t_vehicle_arrival_at_current_queue=-1,\
	val_t_vehicle_started_departure_from_current_queue=-1,val_t_vehicle_departure_from_current_queue=-1,\
	val_vehicle_id_destination_link=-1,val_t_exit_veh_from_network=-1,val_t_end_veh_hold_time_que=-1,val_state_veh=-1,\
	val_nb_veh_occupied_positions_in_que=1,val_time_veh_insertion_in_the_veh_list_when_at_nsi=-1,\
	val_type_vehicle_final_destination=None,val_id_veh_final_destination_link=None,\
	val_index_current_veh_link_location_in_path_list_when_given_destination=-1,val_veh_suppressed_when_que_update=-1,\
	val_veh_added_when_que_update=-1,val_veh_sat_flow_when_current_que_locat_affected=None):
	

		#the vehicle id
		self._id_veh=val_id_veh
		
		#the time at which a vehicle appears at  the network
		self._t_veh_appearance_at_network=val_t_veh_appearance_at_network
		
		#the id of the entry link at which the vehicle appeared
		self._id_entry_link_veh_ap=val_id_entry_link_veh_ap
		
		#the current link location of the vehicle 
		#if a vehicle is about to travel this value is -1
		self._current_id_link_veh_location=val_current_id_link_veh_location
		
		#the arrival time of a vehicle to the current link
		self._t_vehicle_arrival_at_current_link=val_t_vehicle_arrival_at_current_link
		
		#time at which a vehicle started its departure from the current link 
		self._t_vehicle_started_departure_from_current_link=val_t_vehicle_started_departure_from_current_link
		
		#time at which a vehicle left  from the current link
		self._t_vehicle_departure_from_current_link=val_t_vehicle_departure_from_current_link
		
		#the id of the vehicle current location (the id of the queue, in the form of (l,m))
		self._veh_current_queue_location=val_veh_current_queue_location
		
		
		#the time at which a vehicle joins the current queue
		self._t_vehicle_arrival_at_current_queue=val_t_vehicle_arrival_at_current_queue
		
		#time at which a vehicle will start leaving its queue
		self._t_vehicle_started_departure_from_current_queue=val_t_vehicle_started_departure_from_current_queue
		
		
		#the time at which a vehicle leff the current queue
		self._t_vehicle_departure_from_current_queue=val_t_vehicle_departure_from_current_queue
		
		#the time at which a vehicle leaves the network
		self._t_exit_veh_from_network=val_t_exit_veh_from_network
		
		#the id of the  destination link of the vehicle when leaving the current link
		self._vehicle_id_destination_link=val_vehicle_id_destination_link
		
		#the time at which ceases the hold of the veh at the que
		self._t_end_veh_hold_time_que=val_t_end_veh_hold_time_que
		
		#the state of vehicle
		self._state_veh=val_state_veh
		
		#type of the final vehicle destination
		self._type_vehicle_final_destination=val_type_vehicle_final_destination
		
		#the id of the final vehicle destination link
		self._id_veh_final_destination_link=val_id_veh_final_destination_link
		
		#the number indicating how many positions the vehicle occupies in the que
		self._nb_veh_occupied_positions_in_que=val_nb_veh_occupied_positions_in_que
		
		
		#variable indicating the time at which a vehicle inserted in the vehicle list of an non signalised intersection
		self._time_veh_insertion_in_the_veh_list_when_at_nsi=val_time_veh_insertion_in_the_veh_list_when_at_nsi
		
		#variable indicating the index of the current veh link location in the path 
		self._index_current_veh_link_location_in_path_list_when_given_destination=\
		val_index_current_veh_link_location_in_path_list_when_given_destination
		
		
		#variable indicating whether the vehicle is suppressed when updating the queue state
		self._veh_suppressed_when_que_update=val_veh_suppressed_when_que_update
		
		#variable inidicating whether the vehicle added when updating the queue state
		self._veh_added_when_que_update=val_veh_added_when_que_update
		
		#variable indicating the veh sat flow when jining a queue afectd by another one
		self._veh_sat_flow_when_current_que_locat_affected=val_veh_sat_flow_when_current_que_locat_affected
		
		
#*****************************************************************************************************************************************************************************************
	#method returning the vehicle id
	def get_id_veh(self):
		return self._id_veh

#*****************************************************************************************************************************************************************************************
	#method returning the time at which a vehicle appears at  the network
	def get_t_veh_appearance_at_network(self):
		return self._t_veh_appearance_at_network

#*****************************************************************************************************************************************************************************************
	#method returning the id of the entry link at which the vehicle appeared
	def get_id_entry_link_veh_ap(self):
		return self._id_entry_link_veh_ap
#*****************************************************************************************************************************************************************************************
	#method returning the id of the current link where the vehicle is located
	def get_current_id_link_veh_location(self):
	
		return self._current_id_link_veh_location

#*****************************************************************************************************************************************************************************************
	#method returning the vehicle arrival at the current link
	def get_t_vehicle_arrival_at_current_link(self):
		return self._t_vehicle_arrival_at_current_link

#*****************************************************************************************************************************************************************************************
	#method returning the time at which a vehicle started its departure from the current link location
	def get_t_vehicle_started_departure_from_current_link(self):
		return self._t_vehicle_started_departure_from_current_link

#*****************************************************************************************************************************************************************************************
	#method returning the time at which the vehicle departed from the current link
	def get_t_vehicle_departure_from_current_link(self):
		return self._t_vehicle_departure_from_current_link

#*****************************************************************************************************************************************************************************************
	#method returning the id of the vehicle current location (the id of the queue)
	def  get_veh_current_queue_location(self):
		return self._veh_current_queue_location

#*****************************************************************************************************************************************************************************************
	#method returning the time at which a vehicle joins a queue
	def get_t_vehicle_arrival_at_current_queue(self):
		return self._t_vehicle_arrival_at_current_queue
#*****************************************************************************************************************************************************************************************

	#method returning the time at which a vehicle started leaving the current queue
	def get_t_vehicle_started_departure_from_current_queue(self):
		return self._t_vehicle_started_departure_from_current_queue

#*****************************************************************************************************************************************************************************************

	#method returning the time at which a vehicle left the current queue
	def get_t_vehicle_departure_from_current_queue(self):
		return self._t_vehicle_departure_from_current_queue

#*****************************************************************************************************************************************************************************************

	#method returning the time at which a vehicle leaves the network
	def get_t_exit_veh_from_network(self):
		return self._t_exit_veh_from_network

#*****************************************************************************************************************************************************************************************
	#method returning the id of the destination link of the vehicle when leaving the current link
	def get_vehicle_id_destination_link(self):
		return self._vehicle_id_destination_link

#*****************************************************************************************************************************************************************************************
	#method returning the time at which ceases the hold of the veh at the que
	def get_t_end_veh_hold_time_que(self):
		return self._t_end_veh_hold_time_que
#*****************************************************************************************************************************************************************************************
	#method returning the state of vehicle
	def get_state_veh(self):
		return self._state_veh
	
#*****************************************************************************************************************************************************************************************
	#method returning the type of the final vehicle destination
	def get_type_vehicle_final_destination(self):
		return self._type_vehicle_final_destination
#*****************************************************************************************************************************************************************************************
	#method returning the vehicle final destination link
	def get_id_veh_final_destination_link(self):
		return self._id_veh_final_destination_link
#*****************************************************************************************************************************************************************************************
	#method returning the number indicating how many positions the vehicle occupies in the que
	def get_nb_veh_occupied_positions_in_que(self):
		return self._nb_veh_occupied_positions_in_que
#*****************************************************************************************************************************************************************************************
	#method returning the variable indicating the time at which a vehicle inserted in the vehicle list of an non signalised intersection
	def get_time_veh_insertion_in_the_veh_list_when_at_nsi(self):
		return self._time_veh_insertion_in_the_veh_list_when_at_nsi
#*****************************************************************************************************************************************************************************************
	#method returning the variable indicating the index of the current veh link location in the path 
	def get_index_current_veh_link_location_in_path_list_when_given_destination(self):
		return self._index_current_veh_link_location_in_path_list_when_given_destination
#*****************************************************************************************************************************************************************************************
	#method returning the variable indicating whether the vehicle is suppressed when updating the queue state
	def get_veh_suppressed_when_que_update(self):
		return self._veh_suppressed_when_que_update
#*****************************************************************************************************************************************************************************************
	#method returning the variable inidicating whether the vehicle added when updating the queue state
	def get_veh_added_when_que_update(self):
		return self._veh_added_when_que_update
#*****************************************************************************************************************************************************************************************
	#method returning the variable indicating the veh sat flow when jining a queue afectd by another one
	def get_veh_sat_flow_when_current_que_locat_affected(self):
		return self._veh_sat_flow_when_current_que_locat_affected

#*****************************************************************************************************************************************************************************************

	
	#method modyfing  the vehicle id
	def set_id_veh(self,n_v):
		self._id_veh=n_v

#*****************************************************************************************************************************************************************************************
	#method modyfing the time at which a vehicle appears at  the network
	def set_t_veh_appearance_at_network(self,n_v):
		self._t_veh_appearance_at_network=n_v

#*****************************************************************************************************************************************************************************************
	#method modyfing the id of the entry link at which the vehicle appeared
	def set_id_entry_link_veh_ap(self,n_v):
		self._id_entry_link_veh_ap=n_v
#*****************************************************************************************************************************************************************************************
	#method modyfing the id of the current link where the vehicle is located
	def set_current_id_link_veh_location(self,n_v):
	
		self._current_id_link_veh_location=val_current_id_link_veh_location=n_v

#*****************************************************************************************************************************************************************************************
	#method modyfing the vehicle arrival at the current link
	def set_t_vehicle_arrival_at_current_link(self,n_v):
		self._t_vehicle_arrival_at_current_link=n_v

#*****************************************************************************************************************************************************************************************
	#mehod modifying the time at which a vehicle started its departure from the current link
	def set_t_vehicle_started_departure_from_current_link(self,n_v):
		self._t_vehicle_started_departure_from_current_link=n_v
#*****************************************************************************************************************************************************************************************
	
	#method modifying the time at which  vehicle departed from the current link
	def set_t_vehicle_departure_from_current_link(self,n_v):
		self._t_vehicle_departure_from_current_link=n_v

#*****************************************************************************************************************************************************************************************
	#method modyfing the id of the vehicle current location (the id of the queue)
	def  set_veh_current_queue_location(self,n_v):
		self._veh_current_queue_location=n_v
#*****************************************************************************************************************************************************************************************
	
	#method modifying the time at which a vehicle joins a queue
	def set_t_vehicle_arrival_at_current_queue(self,n_v):
		self._t_vehicle_arrival_at_current_queue=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the time at which a vehicle started leaving the current queue
	def set_t_vehicle_started_departure_from_current_queue(self,n_v):
		self._t_vehicle_started_departure_from_current_queue=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the time at which a vehicle left the current queue
	def set_t_vehicle_departure_from_current_queue(self,n_v):
		self._t_vehicle_departure_from_current_queue=n_v

#*****************************************************************************************************************************************************************************************

	#method modyfing the time at which a vehicle leaves the network
	def set_t_exit_veh_from_network(self,n_v):
		self._t_exit_veh_from_network=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the id of the destination link of the vehicle when leaving the current link
	def set_vehicle_id_destination_link(self,n_v):
		self._vehicle_id_destination_link=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the time at which ceases the hold of the veh at the que
	def set_t_end_veh_hold_time_que(self,n_v):
		self._t_end_veh_hold_time_que=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the state of vehicle
	def set_state_veh(self,n_v):
		self._state_veh=n_v
	
#*****************************************************************************************************************************************************************************************
	#method modifying the type of the final vehicle destination
	def set_type_vehicle_final_destination(self,n_v):
		self._type_vehicle_final_destination=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the vehicle final destination link (when the related sim mode is been considered)
	def set_id_veh_final_destination_link(self,n_v):
		self._id_veh_final_destination_link=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the number indicating how many positions the vehicle occupies in the que
	def set_nb_veh_occupied_positions_in_que(self,n_v):
		self._nb_veh_occupied_positions_in_que=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the variable indicating the time at which a vehicle inserted in the vehicle list of an non signalised intersection
	def set_time_veh_insertion_in_the_veh_list_when_at_nsi(self,n_v):
		self._time_veh_insertion_in_the_veh_list_when_at_nsi=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the variable indicating the index of the current veh link location in the path 
	def set_index_current_veh_link_location_in_path_list_when_given_destination(self,n_v):
		self._index_current_veh_link_location_in_path_list_when_given_destination=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the variable indicating whether the vehicle is suppressed when updating the queue state
	def set_veh_suppressed_when_que_update(self,n_v):
		self._veh_suppressed_when_que_update=n_v
#*****************************************************************************************************************************************************************************************
	#method modofying the variable inidicating whether the vehicle added when updating the queue state
	def set_veh_added_when_que_update(self,n_v):
		self._veh_added_when_que_update=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the variable indicating the veh sat flow when jining a queue afectd by another one
	def set_veh_sat_flow_when_current_que_locat_affected(self,n_v):
		self._veh_sat_flow_when_current_que_locat_affected=n_v

#*****************************************************************************************************************************************************************************************
	def __le__(self,other_vehicle):
		return  self._t_end_veh_hold_time_que<=other_vehicle.get_t_end_veh_hold_time_que()		
#*****************************************************************************************************************************************************************************************
	def __lt__(self,other_vehicle):
		return self._t_end_veh_hold_time_que<other_vehicle.get_t_end_veh_hold_time_que()

#*****************************************************************************************************************************************************************************************
	#method inserting a vehicle in an veh list (use when vehicle joins a non signalised intersection)
	#time will be the end veh hold time
	def fct_insertion_veh_in_veh_list(self,vehicle_list):
	
		#if the veh list is not empty
		if vehicle_list!=[]:
			#print(len(vehicle_list))
			#if  time is < to the time of the first event
			if  self._t_end_veh_hold_time_que< vehicle_list[List_Explicit_Values.val_first_element_of_list].get_t_end_veh_hold_time_que():
		
				
				print("PROBLEM IN CL_VEH, fct_insertion_veh_in_veh_list ",self._t_end_veh_hold_time_que,"END HOLD TIME FIRST VEH IN THE LIST: ",\
				vehicle_list[List_Explicit_Values.val_first_element_of_list].get_t_end_veh_hold_time_que())
				#print (message)
				import sys
				sys.exit()
			else:
				heappush(vehicle_list,self)
				
		
		#if the veh list is empty
		else:
			heappush(vehicle_list,self)

#*****************************************************************************************************************************************************************************************
	#method updating a vehicle when it reaches an exit link
	#we consider that  its arrival time and location have been updated earlier
	def fct_update_veh_when_arriving_at_exit_link(self,t_arrival):
		#we indicate the time at which the vehicle leaves the 
		self._t_exit_veh_from_network=t_arrival

#*****************************************************************************************************************************************************************************************
	#method updating the vehicle when it arrives at a link, before choosing its queue
	def fct_veh_update_when_arriving_at_link_1(self,val_id_arrival_link,val_t_arrival_at_link):
	
		#we initialise the destination link  of the vehicle
		self._vehicle_id_destination_link=List_Explicit_Values.initialisation_value_to_minus_one
	
		#we indicate the id of the current link location of the vehicle
		self._current_id_link_veh_location=val_id_arrival_link
	
		#we indicate the arrival time
		self._t_vehicle_arrival_at_current_link=val_t_arrival_at_link
		

#*****************************************************************************************************************************************************************************************
	#method updating the vehicle when it arrives at a link, before choosing its queue
	def fct_veh_update_when_appear_at_link(self,val_id_arrival_link,val_t_arrival_at_link):
	
		#we initialise the destination link  of the vehicle
		#self._vehicle_id_destination_link=List_Explicit_Values.initialisation_value_to_minus_one
	
		#we indicate the id of the current link location of the vehicle
		self._current_id_link_veh_location=val_id_arrival_link
	
		#we indicate the arrival time
		self._t_vehicle_arrival_at_current_link=val_t_arrival_at_link
		

#*****************************************************************************************************************************************************************************************
	#method updating the vehicle when it arrives at a link, before choosing its queue
	#def fct_veh_update_when_arriving_at_link(self,val_id_arrival_link,val_t_arrival_at_link):
	
		#we initialise the destination link  of the vehicle
		#self._vehicle_id_destination_link=List_Explicit_Values.initialisation_value_to_minus_one
	
		#we indicate the id of the current link location of the vehicle
		#self._current_id_link_veh_location=val_id_arrival_link
	
		#we indicate the arrival time
		#self._t_vehicle_arrival_at_current_link=val_t_arrival_at_link
		

#*****************************************************************************************************************************************************************************************
	#method updating the vehicle when arriving at a link before choosing its destination
	def fct_veh_update_when_arriving_at_link_before_choosing_dest_1(self):
	
		#we initialise the destination link  of the vehicle
		self._vehicle_id_destination_link=List_Explicit_Values.initialisation_value_to_minus_one
#*****************************************************************************************************************************************************************************************
	#method updating a vehicle after choosing the queue to join
	def fct_update_veh_after_choosing_queue_1(self,val_associated_phase_to_current_queue_location,val_t_arrival_queue):
	
		#we indicate the current queue location (id in form of (l,m))
		self._veh_current_queue_location=val_associated_phase_to_current_queue_location
		
		#we indicate the arrival time at the current queue
		self._t_vehicle_arrival_at_current_queue=val_t_arrival_queue
		
		#we indicate the vehicle destination link when leaving the current link
		self._vehicle_id_destination_link=self._veh_current_queue_location[List_Explicit_Values.val_second_element_of_list]
		
		
#*****************************************************************************************************************************************************************************************

	#method updating a vehicle after choosing the queue to join
	#it works only when a queue is affected by at  most one queue
	def fct_update_veh_after_choosing_queue(self,val_selected_que,val_t_arrival_queue,val_netw):
	
		#we indicate the current queue location (id in form of (l,m))
		self._veh_current_queue_location=val_selected_que.get_associated_phase_to_queue()
		
		
		#we indicate the arrival time at the current queue
		self._t_vehicle_arrival_at_current_queue=val_t_arrival_queue
		
		#we indicate the vehicle destination link when leaving the current link
		self._vehicle_id_destination_link=self._veh_current_queue_location[List_Explicit_Values.val_second_element_of_list]
		
		#we indicate the sat flow corresponing to the veh if the selected queue interfers with another one
		if val_selected_que.get_di_phase_interference()!={}:
		
			for i in val_selected_que.get_di_phase_interference():
			
				a=len(val_netw.get_di_entry_internal_links()[i[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()[i[0],i[1]].get_queue_veh())
				#if the  affecting queue is of limited que size
				if a>0:
					#if the size of the afffecting queue exceeds the max permitted size
					if a>val_netw.get_di_entry_internal_links()[i[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()[i[0],i[1]].get_max_veh_queue_size():
				
						self._veh_sat_flow_when_current_que_locat_affected=val_selected_que.fct_calcul_sat_flow_at_given_t_when_que_interf(val_id_affecting_que=[i[0],i[1]])
						
						
			
			
		
		
			
#*****************************************************************************************************************************************************************************************
		
	#method updating the vehicle when its dearture from the queue and the related link has been completed
	#val_t_current= the time at which the vehicle leaves the queue
	#val_new_id_lk_location=the id of the link  to which the vehicle has just arrived
	def fct_veh_update_when_depart_completed(self,val_t_end_departure,val_new_id_lk_location):
		
		#we indicate the time at which a vehicle left the  link
		self._t_vehicle_departure_from_current_link=val_t_end_departure
	
		#we indicate the time at which the vehicle left the queue
		self._t_vehicle_departure_from_current_queue=val_t_end_departure
		
		#we indicate the new current link location
		self._current_id_link_veh_location=val_new_id_lk_location
		
		#we indicate the time at which the vehicle joined its new location
		self._t_vehicle_arrival_at_current_link=val_t_end_departure
		
		#we idicate that at this time the veh has not a future destination (yet)
		self._vehicle_id_destination_link=List_Explicit_Values.initialisation_value_to_minus_one
		
		#we update the corresponding sat flow to the veh
		self._veh_sat_flow_when_current_que_locat_affected=None
		
#*****************************************************************************************************************************************************************************************

	#method updating the vehicle when leaving a queue to join another link
	#val_t_current= the time at which the vehicle leaves the queue
	def fct_veh_update_when_leaving_queue_going_to_another_link_1(self,t_departure):
		
		#we indicate the time at which a vehicle leaves the current link
		self._t_vehicle_departure_from_current_link=t_departure
	
		#we indicate the time at which the vehicle leaves the queue
		self._t_vehicle_departure_from_current_queue=t_departure
#*****************************************************************************************************************************************************************************************
	
	#method initialising the members of a vehicle before leaving a queue
	def fct_initialising_veh_before_its_departure(self):
	
		#we initialise the current link location
		self._current_id_link_veh_location=List_Explicit_Values.initialisation_value_to_minus_one
		
		
		
		#we initialie the current queue location
		self._veh_current_queue_location=List_Explicit_Values.initialisation_value_to_minus_one
		
		#we initialise the time at which the vehicle arrived at  the link
		self._t_vehicle_arrival_at_current_link=List_Explicit_Values.initialisation_value_to_minus_one
		
		#we initialise the time at which the vehicle started its departure from the  link
		self._t_vehicle_started_departure_from_current_link=List_Explicit_Values.initialisation_value_to_minus_one
		
		#we initialise the time at which the vehicle departed from  the link
		self._t_vehicle_departure_from_current_link=List_Explicit_Values.initialisation_value_to_minus_one
		
		#we initialise the time at which the vehicle arrived at  the queue
		self._t_vehicle_arrival_at_current_queue=List_Explicit_Values.initialisation_value_to_minus_one
		
		#we initilaise the time at which the vehicle started its departure from the que
		self._t_vehicle_started_departure_from_current_queue=List_Explicit_Values.initialisation_value_to_minus_one
		
		#we initialise the time at which the vehicle left the queue
		self._t_vehicle_departure_from_current_queue=List_Explicit_Values.initialisation_value_to_minus_one
		
		#we initialise the time at which ceases the hold of the veh at the que
		self._t_veh_hold_time_que=List_Explicit_Values.initialisation_value_to_minus_one
		
		#we initialise the state of the vehicle
		self._state_veh=TYPE_STATE_VEH["other"]


#*****************************************************************************************************************************************************************************************
	#method initialising the members of a vehicle before leaving a queue
	def fct_initialising_veh_before_its_arrival_at_que(self):
	
		#we initialise the current link location
		#self._current_id_link_veh_location=List_Explicit_Values.initialisation_value_to_minus_one
		
		#we initialsie the current queue location
		self._veh_current_queue_location=List_Explicit_Values.initialisation_value_to_minus_one
		
		#we initialise the time at which the vehicle arrived at  the link
		#self._t_vehicle_arrival_at_current_link=List_Explicit_Values.initialisation_value_to_minus_one
		
		#we initialise the time at which the vehicle started its departure from the  link
		self._t_vehicle_started_departure_from_current_link=List_Explicit_Values.initialisation_value_to_minus_one
		
		#we initialise the time at which the vehicle departed from  the link
		self._t_vehicle_departure_from_current_link=List_Explicit_Values.initialisation_value_to_minus_one
		
		#we initialise the time at which the vehicle arrived at  the queue
		self._t_vehicle_arrival_at_current_queue=List_Explicit_Values.initialisation_value_to_minus_one
		
		#we initilaise the time at which the vehicle started its departure from the que
		self._t_vehicle_started_departure_from_current_queue=List_Explicit_Values.initialisation_value_to_minus_one
		
		#we initialise the time at which the vehicle left the queue
		self._t_vehicle_departure_from_current_queue=List_Explicit_Values.initialisation_value_to_minus_one
		
		#we initialise the time at which ceases the hold of the veh at the que
		self._t_veh_hold_time_que=List_Explicit_Values.initialisation_value_to_minus_one
		
		#we initialise the state of the vehicle
		self._state_veh=TYPE_STATE_VEH["other"]


#*****************************************************************************************************************************************************************************************
	
	


#ex
#ve=Vehicule(val_id_veh=11,val_t_enter_veh_network=11,val_t_exit_veh_network=21,val_id_current_location=5)
#print("ID, T_ENTER,T_EXIT,ID_CUR_LOC: ", ve.get_id_veh(),ve.get_t_enter_veh_network(),ve.get_t_exit_veh_network(),ve.get_id_current_location())














		
				
		