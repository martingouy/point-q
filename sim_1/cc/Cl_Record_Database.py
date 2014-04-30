import string


class Record_Database:

	""" class creating an object for the database recording"""
	
	def __init__(self,\
	val_file_db=None,\
	val_ev_time=-1,\
	val_ev_type=-1,\
	val_id_inters_node=-1,\
	val_type_inters_node=-1,\
	val_t_start_t_duration_sequence_next_inters_control_mat=[],\
	val_dt_min_margin_for_calcul_next_inters_control=-1,\
	val_t_start_current_inters_control=-1,\
	val_duration_current_inters_control=-1,\
	val_current_inters_control_matrix=-1, \
	val_current_inters_matrix_with_the_associated_link_of_phase=[],\
	val_duration_current_cycle=-1,\
	val_vehicle_id=-1,\
	val_time_veh_appearance_in_network=-1,\
	val_id_veh_entry_link=-1,\
	val_id_current_link_veh_location=-1,\
	val_time_veh_arrival_at_current_link=-1, \
	val_time_veh_start_departure_from_current_link=-1,\
	val_time_veh_departure_from_current_link=-1,\
	val_veh_current_queue_location=-1, \
	val_time_veh_arrival_at_current_queue=-1,\
	val_time_veh_start_departure_from_current_queue=-1,\
	val_time_veh_departure_from_current_queue=-1,\
	val_veh_id_destination_link=-1,\
	val_time_veh_exit_from_network=-1,\
	val_id_event_link=-1,\
	val_veh_can_leave_now=-1,\
	val_t_vehicle_arrival_at_next_link_or_queue=-1,\
	val_current_achieved_queue_service_rate_including_current_vehicle=-1,\
	val_current_queue_service_rate=-1,\
	val_li_id_vehicles_in_queue=-1, \
	val_li_inters_control_matrices_for_next_cycle=[],\
	val_icm_chosen_by_mp_control=-1,\
	val_nb_depart_veh_within_ev_end_veh_hold_at_que=-1,\
	val_mat_rp_cum_netw=[],val_nb_veh_in_ar_lk=0,val_nb_veh_in_dep_lk=0,\
	val_id_veh_final_dest_exit_lk=-1,\
	val_type_control=-1,\
	val_current_inters_turn_ratio_val={},val_new_estim_inters_turn_turn_ratio_val={},\
	val_mat_estimated_rp_cum_netw={},\
	val_current_estim_inters_turn_ratio_val={},\
	val_t_end_current_intersection_control={},\
	val_id_actuated_stage=-1,\
	val_current_inters_cum_turn_ratio_val={}):
	#,val_prob_rout_prop_netw={},val_prob_rout_prop_current_lk=[]):
	
		#the name of thr file where the db will be written
		self._file_db=val_file_db
		
	
		#the event time
		self._ev_time=val_ev_time
	
		#the event type
		self._ev_type=val_ev_type
		
		#the id of the intersection node
		self._id_inters_node=val_id_inters_node
	
	
		#the type of the intersection node, (signalised or not)
		self._type_inters_node=val_type_inters_node
		
		#the list with the [t_start,t_duration] for each intersection control matrix for the next cycle
		self._t_start_t_duration_sequence_next_inters_control_mat=val_t_start_t_duration_sequence_next_inters_control_mat
	
	
		#min margin time to calculate the intersection control matrix for the next cycle
		#if the current cycle finishes at t_fin, then the new network control matrix
		#should be calculated at t_fin- margin_dt
		self._dt_min_margin_for_calcul_next_inters_control=val_dt_min_margin_for_calcul_next_inters_control
	
	
		#the time at which the current  intersection control starts
		self._t_start_current_inters_control=val_t_start_current_inters_control
	
	
		#the duration of the current intersection control
		self._duration_current_inters_control=val_duration_current_inters_control	
	
		#the current intersection control matrix
		self._current_inters_control_matrix=val_current_inters_control_matrix
	
	
		#the current network intersectionmatrix for the associated link ([      ], on raw of the matrix)
		self._current_inters_matrix_with_the_associated_link_of_phase=val_current_inters_matrix_with_the_associated_link_of_phase
	
	
		#the duration of the current cycle
		self._duration_current_cycle=val_duration_current_cycle
	
	
		#the vehicle id
		self._vehicle_id=val_vehicle_id
	
	
		#the time at which the vehicle appeared in the the network
		self._time_veh_appearance_in_network=val_time_veh_appearance_in_network
	
	
		#the id of the entry link at which the associated vehicle appeared
		self._id_veh_entry_link=val_id_veh_entry_link
	
		
	
		#the id of the link where the vehicle is currently located
		self._id_current_link_veh_location=val_id_current_link_veh_location
	
		#the time at which thr vehicle arrived at the current link
		self._time_veh_arrival_at_current_link=val_time_veh_arrival_at_current_link
	
		#the time at which the vehile started its departure from the current link
		self._time_veh_start_departure_from_current_link=val_time_veh_start_departure_from_current_link
		
		#the time at which the vehile left the current link
		self._time_veh_departure_from_current_link=val_time_veh_departure_from_current_link
	
		#the current queue location of th evehicle (in the form of (l,m))
		self._veh_current_queue_location=val_veh_current_queue_location
		
		#the type of the queue (right turn or other)
		#self._type_current_queue_location=val_type_current_queue_location
	
		#the time at which the vehicle arrived at the current queue
		self._time_veh_arrival_at_current_queue=val_time_veh_arrival_at_current_queue
		
		#the time at which a vehicle started its departure from the current queue
		self._time_veh_start_departure_from_current_queue=val_time_veh_start_departure_from_current_queue
	
		#the time at which the vehicle left the current queue
		self._time_veh_departure_from_current_queue=val_time_veh_departure_from_current_queue
		
		#the id of the destination link of the vehicle when leaving the current link
		self._veh_id_destination_link=val_veh_id_destination_link
		
	
		#the time at which the vehicle left the network
		self._time_veh_exit_from_network=val_time_veh_exit_from_network
	
		#the id of the link associated with the current event
		self._id_event_link=val_id_event_link 
		
	
		#the answer (1, 0) indicating if the vehicle can leave the queue by its arrrival or not
		self._veh_can_leave_now=val_veh_can_leave_now
	
	
		#the time at which the vehicle will arrive at the next link or queue (this is for verifying the calculations)
		self._t_vehicle_arrival_at_next_link_or_queue=val_t_vehicle_arrival_at_next_link_or_queue
	
		#the currently achieved service rate of the queue where the vehicle is, including the vehicle (case when the vehicle can leave the queue)
		self._current_achieved_queue_service_rate_including_current_vehicle=val_current_achieved_queue_service_rate_including_current_vehicle
	
		#the current value of the service rate of the queue where the vehicle is located
		self._current_queue_service_rate=val_current_queue_service_rate

		#a list with the ids of the vehicles in the associated queue with this event
		self._li_id_vehicles_in_queue=val_li_id_vehicles_in_queue
	
	
		#the list of the network control matrices decided during the event Ev_end_decision_network_control, for the next cycle
		#(this information is in the object network_control_cycle)
		self._li_inters_control_matrices_for_next_cycle=val_li_inters_control_matrices_for_next_cycle
		
		
		#the ncm chosen by mp control 
		self._icm_chosen_by_mp_control=val_icm_chosen_by_mp_control
		
		
		#the number of departing vehicle within an end veh hold at que event or with the ev end veh dep
		self._nb_depart_veh_within_ev_end_veh_hold_at_que=val_nb_depart_veh_within_ev_end_veh_hold_at_que
		
		#the number of vehicles in the present vehicle link location
		#self._nb_veh_current_veh_link_location=val_nb_veh_current_veh_link_location
		
		#the dictionary with the prob of each queue (rout prop) of the network
		#self._prob_rout_prop_netw=val_prob_rout_prop_netw
		
		# mat od, dict, key=id entry itnernal lk, value=[.., value fct cum, ..]
		self._mat_rp_cum_netw=val_mat_rp_cum_netw
		
		#the nb of vehicles in the arrival  link
		self._nb_veh_in_ar_lk=val_nb_veh_in_ar_lk
		
		#the nb of veh in the depart link
		self._nb_veh_in_dep_lk=val_nb_veh_in_dep_lk
		
		#the id of the veh final destination (when the model  decides it by the veh appearance) (exit link)
		self._id_veh_final_dest_exit_lk=val_id_veh_final_dest_exit_lk
		
		
		#variable returning the type of control , 0 if the crrl is RC, 1 sinon
		self._type_control=val_type_control
		
		
		#variable indicating the current values od the turn ratios of the intersection
		self._current_inters_turn_ratio_val=val_current_inters_turn_ratio_val
		
		#variable indicating the new estimated values of the  turn ratios
		self._new_estim_inters_turn_turn_ratio_val=val_new_estim_inters_turn_turn_ratio_val
		
		#variable indicating the cum values of the new estim turn ratios
		self._mat_estimated_rp_cum_netw=val_mat_estimated_rp_cum_netw
		
		#variable indicating the current estimated values of the turn ratios (before replaced by the new estimated ones)
		self._current_estim_inters_turn_ratio_val=val_current_estim_inters_turn_ratio_val
		
		#variable indicating the  time at which finishes the current intersection control
		self._t_end_current_intersection_control=val_t_end_current_intersection_control
		
		#the id of the actuated staged  by a new cotnrol
		self._id_actuated_stage=val_id_actuated_stage
		
		#variable indicating the current cum values
		self._current_inters_cum_turn_ratio_val=val_current_inters_cum_turn_ratio_val
		
		
#*****************************************************************************************************************************************************************************************
	#method returning the  name of thr file where the db will be written
	def get_file_db(self):
		return self._file_db

#*****************************************************************************************************************************************************************************************
	#method returning the event time
	def get_ev_time(self):
		return self._ev_time

#*****************************************************************************************************************************************************************************************
	#method returning the event type
	def get_ev_type(self):
		return self._ev_type

#*****************************************************************************************************************************************************************************************
	#method returning  the id of the intersection node
	def get_id_inters_node(self):
		return self._id_inters_node
#*****************************************************************************************************************************************************************************************
	#method returning the type of the intersection node
	def get_type_inters_node(self):
		return self._type_inters_node
#*****************************************************************************************************************************************************************************************
	#method returning the list with the [t_start,t_duration] for each intersectio  control matrix 
	def get_t_start_t_duration_sequence_next_inters_control_mat(self):
		return self._t_start_t_duration_sequence_next_inters_control_mat

#*****************************************************************************************************************************************************************************************
	#method returning the min margin time to calculate the next intersection control matrix 
	def get_dt_min_margin_for_calcul_next_inters_control(self):
		return self._dt_min_margin_for_calcul_next_inters_control


#*****************************************************************************************************************************************************************************************
	#method returning the time at which the current intersection control starts
	def get_t_start_current_inters_control(self):
		return self._t_start_current_inters_control

#*****************************************************************************************************************************************************************************************
	#method returning the duration of the current control
	def get_duration_current_control(self):
		return self._duration_current_control

#*****************************************************************************************************************************************************************************************
	#method returning the current network control matrix
	def get_current_inters_control_matrix(self):
		return self._current_inters_control_matrix

#*****************************************************************************************************************************************************************************************
	#method returning the current inters control matrix for the associated link ([      ], on raw of the matrix)
	def get_current_inters_matrix_with_the_associated_link_of_phase(self):
		return self._current_inters_matrix_with_the_associated_link_of_phase

#*****************************************************************************************************************************************************************************************
	#method returning the duration of the current cycle
	def get_duration_current_cycle(self):
		return self._duration_current_cycle

#*****************************************************************************************************************************************************************************************
	#method returning the vehicle id
	def get_vehicle_id(self):
		return self._vehicle_id

#*****************************************************************************************************************************************************************************************
	#method returning the time at which the vehicle appeared in the the network
	def get_time_veh_appearance_in_network(self):
		return self._time_veh_appearance_in_network

#*****************************************************************************************************************************************************************************************
	#method returning the id of the entry link at which the associated vehicle appeared
	def get_id_veh_entry_link(self):
		return self._id_veh_entry_link

#*****************************************************************************************************************************************************************************************
	#method returning the number of vehicles appearing at the entry link
	def get_nb_veh_appear_entry_link(self):
		return self._nb_veh_appear_entry_link
#*****************************************************************************************************************************************************************************************
	#method returning the id of the link where the vehicle is currently located
	def get_id_current_link_veh_location(self):
		return self._id_current_link_veh_location
	
#*****************************************************************************************************************************************************************************************
	#method returning the time at which thr vehicle arrived at the current link
	def get_time_veh_arrival_at_current_link(self):
		return self._time_veh_arrival_at_current_link

#*****************************************************************************************************************************************************************************************
	#method returning the time at which the vehile started its departure from the current link
	def get_time_veh_start_departure_from_current_link(self):
		return self._time_veh_start_departure_from_current_link

#*****************************************************************************************************************************************************************************************
	#method returning the time at which the vehile left the current link
	def get_time_veh_departure_from_current_link(self):
		return self._time_veh_departure_from_current_link

#*****************************************************************************************************************************************************************************************
	#method returning the current queue location of th evehicle (in the form of (l,m))
	def get_veh_current_queue_location(self):
		return self._veh_current_queue_location

#*****************************************************************************************************************************************************************************************
	#method returning the type of the queue (right turn or other)
	# get_type_current_queue_location(self):
		#return self._type_current_queue_location

#*****************************************************************************************************************************************************************************************
	#method returning the time at which the vehicle arrived at the current queue
	def get_time_veh_arrival_at_current_queue(self):
		return self._time_veh_arrival_at_current_queue
	
#*****************************************************************************************************************************************************************************************
	#method returning the time at which the vehicle started its departure from the current queue
	def get_time_veh_start_departure_from_current_queue(self):
		return self._time_veh_start_departure_from_current_queue

#*****************************************************************************************************************************************************************************************

	#method returning the time at which the vehicle left the current queue
	def get_time_veh_departure_from_current_queue(self):
		return self._time_veh_departure_from_current_queue

#*****************************************************************************************************************************************************************************************
	#method returning the id of the destination link when the vehicle leaves the current queue
	def get_veh_id_destination_link(self):
		return self._veh_id_destination_link

#*****************************************************************************************************************************************************************************************
	#method returning the time at which the vehicle left the network
	def get_time_veh_exit_from_network(self):
		return self._time_veh_exit_from_network

#*****************************************************************************************************************************************************************************************
	#method returning the id of the link associated with the current event
	def get_id_event_link(self):
		return self._id_event_link
	
#*****************************************************************************************************************************************************************************************
	
	#method returning the answer (1, 0) indicating if the vehicle can leave the queue by its arrrival or not
	def get_veh_can_leave_now(self):
		return self._veh_can_leave_now

#*****************************************************************************************************************************************************************************************
	#method returning the time at which the vehicle will arrive at the next link or queue (this is for verifying the calculations)
	def get_t_vehicle_arrival_at_next_link_or_queue(self):
		return self._t_vehicle_arrival_at_next_link_or_queue

#*****************************************************************************************************************************************************************************************
	#method returning the currently achieved service rate of the queue where the vehicle is, including the vehicle 
	#(case when the vehicle can leave the queue)
	def get_current_achieved_queue_service_rate_including_current_vehicle(self):
		return self._current_achieved_queue_service_rate_including_current_vehicle

#*****************************************************************************************************************************************************************************************
	#method returning the current value of the service rate of the queue where the vehicle is located
	def get_current_queue_service_rate(self):
		return self._current_queue_service_rate

#*****************************************************************************************************************************************************************************************
	#method returning a list with the ids of the vehicles in the associated queue with this event
	def get_li_id_vehicles_in_queue(self):
		return self._li_id_vehicles_in_queue

#*****************************************************************************************************************************************************************************************
	#method returning the list of the inters control matrices decided during the event Ev_end_decision_intersection_control, for the next cycle
	def get_li_inters_control_matrices_for_next_cycle(self):
		return self._li_inters_control_matrices_for_next_cycle

#*****************************************************************************************************************************************************************************************
	
	#method returning the ncm chosen by mp control 
	def get_ncm_chosen_by_mp_control(self):
		return self._ncm_chosen_by_mp_control

#*****************************************************************************************************************************************************************************************
	#method returning the number of deparing veh within a veh departure event
	def get_nb_depart_veh_within_dep_ev(self):
		return self._nb_depart_veh_within_dep_ev

#*****************************************************************************************************************************************************************************************
	#method returning the number of departing vehicle within an end veh hold at que event
	def get_nb_depart_veh_within_ev_end_veh_hold_at_que(self):
		return self._nb_depart_veh_within_ev_end_veh_hold_at_que
#*****************************************************************************************************************************************************************************************
	#method returning the the dictionary with the prob of each queue (rout prop) of the network
	#def get_prob_rout_prop_netw(self):
		#return self._prob_rout_prop_netw
#*****************************************************************************************************************************************************************************************
	#method returning the dictionary with the rp_mat_cum
	#key=id entry itnernal lk, value=[.., value fct cum, ..]
	def get_mat_rp_cum_netw(self):
		return self._mat_rp_cum_netw
#*****************************************************************************************************************************************************************************************
	#method returning the number of vehicles in the arrival  link
	def get_nb_veh_in_ar_lk(self):
		return self._nb_veh_in_ar_lk
#*****************************************************************************************************************************************************************************************
	#method returning the number of vehicles in the depart  link
	def get_nb_veh_in_dep_lk(self):
		return self._nb_veh_in_dep_lk
#*****************************************************************************************************************************************************************************************
	#method returning the veh final destination (exit link)
	def get_id_veh_final_dest_exit_lk(self):
		return self._id_veh_final_dest_exit_lk
#*****************************************************************************************************************************************************************************************
	#method retruning the type of the cotnrol, 0 if the crrl is RC, 1 sinon
	def get_type_control(self):
		return self._type_control
#*****************************************************************************************************************************************************************************************
	#method returning the variable indicating the current values od the turn ratios of the intersection
	def get_current_inters_turn_ratio_val(self):
		return self._current_inters_turn_ratio_val

#*****************************************************************************************************************************************************************************************
	#method returning the variable indicating the new estimatd values of the  turn ratios
	def get_new_estim_inters_turn_turn_ratio_val(self):
		return self._new_estim_inters_turn_turn_ratio_val

#*****************************************************************************************************************************************************************************************
	#method returning the variable indicating the cum values of the new estim turn ratios
	def get_mat_estimated_rp_cum_netw(self):
		return self._mat_estimated_rp_cum_netw

#*****************************************************************************************************************************************************************************************
	#method returning the variable indicating the current estimated values of the turn ratios (before replaced by the new estimated ones)
	def get_current_estim_inters_turn_ratio_val(self):
		return self._current_estim_inters_turn_ratio_val
#*****************************************************************************************************************************************************************************************
	#method returning the variable indicating the  time at which finishes the current intersection control 
	def get_t_end_current_intersection_control(self):
		return self._t_end_current_intersection_control

#*****************************************************************************************************************************************************************************************
	#method returning the id fo the actuated stage by a new control
	def get_id_actuated_stage(self):
		return self._id_actuated_stage

#*****************************************************************************************************************************************************************************************
	#method returning the variable indicating the current cum values
	def get_current_inters_cum_turn_ratio_val(self):
		return self._current_inters_cum_turn_ratio_val

#*****************************************************************************************************************************************************************************************
	
	#method modifying the  name of thr file where the db will be written
	def set_file_db(self,n_v):
		self._file_db=n_v

#*****************************************************************************************************************************************************************************************
	
	#method modifying the event time
	def set_ev_time(self,n_v):
		self._ev_time=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the event type
	def set_ev_type(self,n_v):
		self._ev_type=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying  the id of the intersection node
	def set_id_inters_node(self,n_v):
		self._id_inters_node=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the type of the intersection node
	def set_type_inters_node(self,n_v):
		self._type_inters_node=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the list with the [t_start,t_duration] for each intersection control matrix 
	def set_t_start_t_duration_sequence_next_inters_control_mat(self,n_v):
		self._t_start_t_duration_sequence_next_inters_control_mat=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the min margin time to calculate the inters control matrix 
	def set_dt_min_margin_for_calcul_next_inters_control(self,n_v):
		self._dt_min_margin_for_calcul_next_inters_control=n_v


#*****************************************************************************************************************************************************************************************
	#method modifying the time at which the current control starts
	def set_t_start_current_inters_control(self,n_v):
		self._t_start_current_inters_control=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the duration of the current control
	def set_duration_current_control(self,n_v):
		self._duration_current_control=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the current intersection control matrix
	def set_current_inters_control_matrix(self,n_v):
		self._current_inters_control_matrix=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the current network control matrix for the associated link ([      ], on raw of the matrix)
	def set_current_inters_matrix_with_the_associated_link_of_phase(self,n_v):
		self._current_inters_matrix_with_the_associated_link_of_phase=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the duration of the current cycle
	def set_duration_current_cycle(self,n_v):
		self._duration_current_cycle=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the vehicle id
	def set_vehicle_id(self,n_v):
		self._vehicle_id=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the time at which the vehicle appeared in the the network
	def set_time_veh_appearance_in_network(self,n_v):
		self._time_veh_appearance_in_network=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the id of the entry link at which the associated vehicle appeared
	def set_id_veh_entry_link(self,n_v):
		self._id_veh_entry_link=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the number of vehicles appearing at the entry link
	def set_nb_veh_appear_entry_link(self,n_v):
		self._nb_veh_appear_entry_link=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the id of the link where the vehicle is currently located
	def set_id_current_link_veh_location(self,n_v):
		self._id_current_link_veh_location=n_v
	
#*****************************************************************************************************************************************************************************************
	#method modifying the time at which thr vehicle arrived at the current link
	def set_time_veh_arrival_at_current_link(self,n_v):
		self._time_veh_arrival_at_current_link=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the time at which the vehile started its departure from the current link
	def set_time_veh_start_departure_from_current_link(self,n_v):
		self._time_veh_start_departure_from_current_link=n_v

#*****************************************************************************************************************************************************************************************

	#method modifying the time at which the vehile left the current link
	def set_time_veh_departure_from_current_link(self,n_v):
		self._time_veh_departure_from_current_link=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the current queue location of th evehicle (in the form of (l,m))
	def set_veh_current_queue_location(self,n_v):
		self._veh_current_queue_location=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the type of the queue (right turn or other)
	#def set_type_current_queue_location(self,n_v):
		#self._type_current_queue_location=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the time at which the vehicle arrived at the current queue
	def set_time_veh_arrival_at_current_queue(self,n_v):
		self._time_veh_arrival_at_current_queue=n_v
	
#*****************************************************************************************************************************************************************************************
	#method modifying the time at which the vehicle started its departure from the current queue
	def set_time_veh_start_departure_from_current_queue(self,n_v):
		self._time_veh_start_departure_from_current_queue=n_v

#*****************************************************************************************************************************************************************************************

	#method modifying the time at which the vehicle left the current queue
	def set_time_veh_departure_from_current_queue(self,n_v):
		self._time_veh_departure_from_current_queue=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the id of the destination link when the vehicle leaves the current queue
	def set_veh_id_destination_link(self,n_v):
		self._veh_id_destination_link=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the time at which the vehicle left the network
	def set_time_veh_exit_from_network(self,n_v):
		self._time_veh_exit_from_network=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the id of the link associated with the current event
	def set_id_event_link(self,n_v):
		self._id_event_link=n_v
	
#*****************************************************************************************************************************************************************************************
	
	#method modifying the answer (1, 0) indicating if the vehicle can leave the queue by its arrrival or not
	def set_veh_can_leave_now(self,n_v):
		self._veh_can_leave_now=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the time at which the vehicle will arrive at the next link or queue (this is for verifying the calculations)
	def set_t_vehicle_arrival_at_next_link_or_queue(self,n_v):
		self._t_vehicle_arrival_at_next_link_or_queue=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the currently achieved service rate of the queue where the vehicle is, including the vehicle 
	#(case when the vehicle can leave the queue)
	def set_current_achieved_queue_service_rate_including_current_vehicle(self,n_v):
		self._current_achieved_queue_service_rate_including_current_vehicle=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the current value of the service rate of the queue where the vehicle is located
	def set_current_queue_service_rate(self,n_v):
		self._current_queue_service_rate=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying a list with the ids of the vehicles in the associated queue with this event
	def set_li_id_vehicles_in_queue(self,n_v):
		self._li_id_vehicles_in_queue=n_v

#*****************************************************************************************************************************************************************************************
	
	#method modifying the list of the network control matrices decided during the event Ev_end_decision_network_control, for the next cycle
	def set_li_network_control_matrices_for_next_cycle(self,n_v):
		self._li_network_control_matrices_for_next_cycle=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the ncm chosen by mp control 
	def set_ncm_chosen_by_mp_control(self,n_v):
		self._ncm_chosen_by_mp_control=n_v

#*****************************************************************************************************************************************************************************************

	#method modifying the number of departing vehicle within an end veh hold at que event
	def set_nb_depart_veh_within_ev_end_veh_hold_at_que(self,n_v):
		self._nb_depart_veh_within_ev_end_veh_hold_at_que=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the the dictionary with the prob of each queue (rout prop) of the network
	#def set_prob_rout_prop_netw(self,n_v):
		#self._prob_rout_prop_netw=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the  list with the prob of each queue associated with the current link
	def set_prob_rout_prop_current_lk(self,n_v):
		self._prob_rout_prop_current_lk=n_v
#*****************************************************************************************************************************************************************************************
	#method returning the dictionary with the rp_mat_cum
	#key=id entry itnernal lk, value=[.., value fct cum, ..]
	def set_mat_rp_cum_netw(self,n_v):
		self._mat_rp_cum_netw=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the number of vehicles in the ar link
	def set_nb_veh_in_ar_lk(self,n_v):
		self._nb_veh_in_ar_lk=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the number of vehicles in the depart  link
	def set_nb_veh_in_dep_lk(self,n_v):
		self._nb_veh_in_dep_lk=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the veh final destination (exit link)
	def set_id_veh_final_dest_exit_lk(self,n_v):
		self._id_veh_final_dest_exit_lk
#*****************************************************************************************************************************************************************************************
	#method modifying the type of the cotnrol, 0 if the crrl is RC, 1 sinon
	def set_type_control(self,n_v):
		self._type_control=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the variable indicating the current values od the turn ratios of the intersection
	def set_current_inters_turn_ratio_val(self,n_v):
		self._current_inters_turn_ratio_val=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the variable indicating the new estimatd values of the  turn ratios
	def set_new_estim_inters_turn_turn_ratio_val(self,n_v):
		self._new_estim_inters_turn_turn_ratio_val=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the variable indicating the cum values of the new estim turn ratios
	def set_mat_estimated_rp_cum_netw(self,n_v):
		self._mat_estimated_rp_cum_netw=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the variable indicating the current estimated values of the turn ratios (before replaced by the new estimated ones)
	def set_current_estim_inters_turn_ratio_val(self):
		return self._current_estim_inters_turn_ratio_val


#*****************************************************************************************************************************************************************************************
	#method modifying the vairiable indicating the  time at which finishes the current intersection control
	def set_t_end_current_intersection_control(self,n_v):
		self._t_end_current_intersection_control=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the id of the actuated stage by a new control
	def set_id_actuated_stage(self,n_v):
		self._id_actuated_stage=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the variable indicating the current cum values
	def set_current_inters_cum_turn_ratio_val(self,n_v):
		self._current_inters_cum_turn_ratio_val=n_v

#*****************************************************************************************************************************************************************************************
		
	
	
	#method writing each member of this object in the db file
	def fct_write_object_in_db_file(self):
		self._file_db.writerow([\
		self._ev_time,\
		self._ev_type,\
		self._id_inters_node,\
		self._type_inters_node,\
		self._t_start_t_duration_sequence_next_inters_control_mat,\
		self._dt_min_margin_for_calcul_next_inters_control,\
		self._t_start_current_inters_control,\
		self._duration_current_inters_control,\
		self._current_inters_control_matrix,\
		self._current_inters_matrix_with_the_associated_link_of_phase,\
		self._duration_current_cycle,\
		self._vehicle_id,\
		self._time_veh_appearance_in_network,\
		self._id_veh_entry_link,\
		self._id_current_link_veh_location,\
		self._time_veh_arrival_at_current_link,\
		self._time_veh_start_departure_from_current_link,\
		self._time_veh_departure_from_current_link,\
		self._veh_current_queue_location,\
		self._time_veh_arrival_at_current_queue,\
		self._time_veh_start_departure_from_current_queue,\
		self._time_veh_departure_from_current_queue,\
		self._veh_id_destination_link,\
		self._time_veh_exit_from_network,\
		self._id_event_link,\
		self._veh_can_leave_now,\
		self._t_vehicle_arrival_at_next_link_or_queue,\
		self._current_achieved_queue_service_rate_including_current_vehicle,\
		self._current_queue_service_rate,\
		self._li_id_vehicles_in_queue,\
		self._li_inters_control_matrices_for_next_cycle,\
		self._icm_chosen_by_mp_control,\
		self._nb_depart_veh_within_ev_end_veh_hold_at_que,\
		self._mat_rp_cum_netw,\
		self._nb_veh_in_ar_lk,\
		self._nb_veh_in_dep_lk,\
		self._id_veh_final_dest_exit_lk,\
		self._type_control,\
		self._current_inters_turn_ratio_val,\
		self._new_estim_inters_turn_turn_ratio_val,\
		self._mat_estimated_rp_cum_netw,\
		self._current_estim_inters_turn_ratio_val,\
		self._t_end_current_intersection_control,\
		self._id_actuated_stage,\
		self._current_inters_cum_turn_ratio_val])
		#self._prob_rout_prop_netw,\
		#self._prob_rout_prop_current_lk])
		

#*****************************************************************************************************************************************************************************************	
	
	
	
	
	
	
	
	
	
	
	
	
	