import List_Explicit_Values
import Cl_Vehicle
import Cl_Sensor_Presence_Detection
import Cl_Sensor_Que_Size_Detection
import Cl_Decisions
import math


#TYPE_VEHICLE_QUEUE={"left_turn":1,"straight_movement":2,"right_turn":3}
TYPE_VEHICLE_QUEUE={"right_turn":1, "other":0}
TYPE_RELATED_PHASE={"prior_mv":1,"minor_mv":2,"other":0,"main_mv":3,"side_mv":4}



class Vehicle_Queue:
	""" class defining a vehiclue queue object associated to a link"""

	#def __init__(self,val_t_unit,\
	#val_id_queue=-1,val_id_associated_link=-1,val_id_associated_output_link=-1,\
	#val_queue_veh=[],val_max_veh_queue_size=-1,val_sat_flow_queue=-1,\
	#val_type_veh_queue=-1,val_current_queue_service_rate=-1,\
	#val_current_reached_service_rate=0,\
	#val_li_posit_presence_detector_in_que={},val_li_posit_que_size_detector_in_que={},\
	#val_total_mumber_of_veh_passages_by_queue=0,\
	#val_didetector_associated_to_que={},\
	#val_current_nb_veh_chosen_que_during_period=0):
	#val_nb_veh_arrived_current_period=0):
	def __init__(self,val_t_unit,\
	val_id_queue=-1,val_id_associated_link=-1,val_id_associated_output_link=-1,\
	val_queue_veh=[],val_max_veh_queue_size=-1,val_sat_flow_queue=-1,\
	val_type_veh_queue=-1,val_current_queue_service_rate=-1,\
	val_current_reached_service_rate=0,\
	val_total_mumber_of_veh_passages_by_queue=0,\
	val_di_phase_interference={},\
	val_di_detector_associated_to_que={}):
	
		#the id of the queue
		self._id_queue=val_id_queue
		
		#the id of the associated link
		self._id_associated_link=val_id_associated_link
		
		#the id of the associated output link
		self._id_associated_output_link=val_id_associated_output_link
		
		#the associated phase of this queue
		self._associated_phase_to_queue=[self._id_associated_link,self._id_associated_output_link]
		
		#the vehicle queue (list of vehicles) 
		self._queue_veh=val_queue_veh
		
		#the max permitted vehicle queue size (the capacity of the queue may be infinite)
		self._max_veh_queue_size=val_max_veh_queue_size
		
		#the associated saturation flow of the queue (of the phase (l,m))
		self._sat_flow_queue=val_sat_flow_queue
		
		
		#if micro managmement is been considered
		#if val_type_sim_management==Cl_Decisions.TYPE_SIMULATOR_MANAGEMENT[2]:
		#re=[nb veh to leave, time toleave the queue]
		rep=self.fct_defin_nb_veh_leave_mi(v_t_unit=val_t_unit)
		
		#the number of vehicles that can leave the queue, as defined by the sat flow
		self._nb_veh_cal_leave_simult_que_from_sat_flow=rep[0]
			
		
		#the required time for "nb of veh that can leave queue" to depart
		self._required_depart_time_que=rep[1]
		
			
			#print("self._id_queue",self._id_queue,"self._nb_veh_cal_leave_que_from_sat_flow",self._nb_veh_cal_leave_simult_que_from_sat_flow,\
			#"self._required_depart_time_que",self._required_depart_time_que)
		#if any other mangement is been considered
		#else:
			#self._nb_veh_cal_leave_simult_que_from_sat_flow=None
			#self._required_depart_time_que=None
			#print("In CL VEH QUE, the number of departing veh and the required time should be defined for this management")
			#import sys
			#sys.exit()
			
			
		
		#the type of the vehicle queue (right turn,etc)
		self._type_veh_queue=val_type_veh_queue
		
		#the routing proportions corresponding to this queue (turning ratio)
		#self._rout_prop_queue=val_rout_prop_queue
		
		#the current service rate of the queue phase
		#it will defined as the saturation flow x the current period duration
		#for a non signalised intersection, this value will be the que service rate during the sim duration
		self._current_queue_service_rate=val_current_queue_service_rate
		
		#the currently reached service rate
		self._current_reached_service_rate=val_current_reached_service_rate
		
		#a list with the positions of the presence detector in the que,  (1st posit corrersponds to nb 1)
		#val_li_posit_presence_detector_in_que=[...,[id init pos prese detector i, id final posit pres detector i],...]
		#self._li_posit_presence_detector_in_que=val_li_posit_presence_detector_in_que
		
		#a list with the positions of the que size detectors in the que,  (1st posit corrersponds to nb 1)
		#these detector measure whether  the que size has reached their position
		#self._li_posit_que_size_detector_in_que=val_li_posit_que_size_detector_in_que
		
		#creat  a dict of the presence detectors, key=init position of the pres detector in the que, value=presence detector
		#first position corresponds to nb 1
		#self._dict_key_pos_pres_detect_value_pres_detect_obj=self.fct_creat_di_presence_detectors(\
		#val_li_posit_presence_detector_in_que=self._li_posit_presence_detector_in_que)
		
		#creat  a dict of the que size detectors, key=position of the que size detector in the que, value=que size detector
		#self._dict_key_pos_que_size_detect_value_que_size_detect=self.fct_creat_di_que_size_detectors(\
		#val_li_posit_que_size_detector_in_que=self._li_posit_que_size_detector_in_que)
				
		
		#the total number of vehicles passed by this queue
		self._total_mumber_of_veh_passages_by_queue=val_total_mumber_of_veh_passages_by_queue
		
		#dict, key=sensor id, value=[[initial position captured by sensor, final position captured by sensor], final position captured by sensor- initial position captures by sensor+1]
		#indicating the zobe covered by the related sensor
		#or value=-1 if the detector covers the entire queue area
		self._di_detector_associated_to_que=val_di_detector_associated_to_que
		
		#variable indicating the the phases affecting the current phase and the related parameter
		#dict, key=id phase, valeur=associated parameter
		self._di_phase_interference=val_di_phase_interference
		
		
		#the parameter for the travel duration from the input link to the output link associated with the queue
		#self._param_travel_durat_from_input_lk_to_output_lk=val_param_travel_durat_from_input_lk_to_output_lk
		
		#the list with the id of the merging ques to the current que=[..., id dest link phase,...]
		#so the merging queue to the current queue will be [key,id dest link phase]
		#self._li_id_merging_ques=val_li_id_merging_ques
		
		
		#the dictionary of which key=time at which a vehicle finishes its hold duration in the que, 
		#value=the number of vehicles corresponding to this t_end_veh_hold_at_que
		#self._dict_key_t_end_hold_veh_at_que_ev_value_nb_of_veh={}
		
		#variable indicating if the queue is related to a prior,minor or other type of phase
		#self._type_related_phase=val_type_related_phase
		
		#the list with the minor, prior movements associated with the prior,minor, queue
		#self._li_id_minor_prior_phases_related_to_que=val_li_id_minor_prior_phases_related_to_que
		
		#the list with the main phases related to the side phase, (for the semi-act ctrls)
		#self._li_id_main_phases_related_to_current_side_que=val_li_id_main_phases_related_to_current_side_que
		
		
		#the list with the side phases related to the main phase, (for the semi-act ctrls)
		#self._li_id_side_phases_related_to_current_main_que=val_li_id_side_phases_related_to_current_main_que
		
		#variable indicating the number of veh arrived at queue during the current period.
		#its value should be updated at the appropriate time
		#it  will be employed when od matrices are  considered   A VERIFIER SI CETTE VARIABLE EST EMPLOYEE !!!!
		#self._nb_veh_arrived_current_period=val_nb_veh_arrived_current_period
		
		
		#the current number of vehicles arrived in que during a period
		#it is employed when we consider the realised split rratios during the sim
		#self._current_nb_veh_chosen_que_during_period=val_current_nb_veh_chosen_que_during_period
		
		
#*****************************************************************************************************************************************************************************************
	#method returning the id of the queue
	def get_id_queue(self):
		return self._id_queue

#*****************************************************************************************************************************************************************************************

	#method returning the id of the associated link
	def get_id_associated_link(self):
		return self._id_associated_link

#*****************************************************************************************************************************************************************************************
	#method returning the id of the associated destination link
	def get_id_associated_output_link(self):
		return self._id_associated_output_link

#*****************************************************************************************************************************************************************************************
	#method returning the  associated phase of this queue
	def get_associated_phase_to_queue(self):
		return self._associated_phase_to_queue

#*****************************************************************************************************************************************************************************************
	#method returning the  vehicle queue 
	def get_queue_veh(self):
		return self._queue_veh

#*****************************************************************************************************************************************************************************************

	#method returning the max permitted vehicle queue size
	def get_max_veh_queue_size(self):
		return self._max_veh_queue_size

#*****************************************************************************************************************************************************************************************
	#method returning the associated saturation flow of the queue
	def get_sat_flow_queue(self):
		return self._sat_flow_queue

#*****************************************************************************************************************************************************************************************
	#method returning the number of vehciles that can depart simultanesouly the queue,  defined from the sat flow
	def get_nb_veh_cal_leave_simult_que_from_sat_flow(self):
		return self._nb_veh_cal_leave_simult_que_from_sat_flow

#*****************************************************************************************************************************************************************************************
	#method returning the required time for departing the queue
	def get_required_depart_time_que(self):
		return self._required_depart_time_que

#*****************************************************************************************************************************************************************************************
	#method retunring the the type of the vehicle queue
	def get_type_veh_queue(self):
		return self._type_veh_queue
#*****************************************************************************************************************************************************************************************
	#method returning the routing proportion of this queue
	#def get_rout_prop_queue(self):
		#return self._rout_prop_queue
#*****************************************************************************************************************************************************************************************
	#method returning the current service rate of the queue
	def get_current_queue_service_rate(self):
		return self._current_queue_service_rate
#*****************************************************************************************************************************************************************************************
	#method returning the current reached service rate
	def get_current_reached_service_rate(self):
		return self._current_reached_service_rate
#*****************************************************************************************************************************************************************************************
	#method returning the dictionary with the inform of  presence detectors associated to the que
	#def get_li_posit_presence_detector_in_que(self):
		#return self._li_posit_presence_detector_in_que

#*****************************************************************************************************************************************************************************************
	#method returning the dictionary with the inform of the que size detectors associated to the que
	#these detector measure whether  the que size has reached their position
	#def get_li_posit_que_size_detector_in_que(self):
		#return self._li_posit_que_size_detector_in_que

#*****************************************************************************************************************************************************************************************
	#method returning the dictionary key = position pres detector in the que, value=pres detector
	#def get_dict_key_pos_pres_detect_value_pres_detect_obj(self):
		#return self._dict_key_pos_pres_detect_value_pres_detect_obj
#*****************************************************************************************************************************************************************************************
	#method returning the dictionary key = position que size detector in the que, value=que size detector
	#def get_dict_key_pos_que_size_detect_value_que_size_detect(self):
		#return self._dict_key_pos_que_size_detect_value_que_size_detect
#*****************************************************************************************************************************************************************************************
	#method returning the total number of vehicles passed by this queue
	def get_total_mumber_of_veh_passages_by_queue(self):
		return self._total_mumber_of_veh_passages_by_queue

#*****************************************************************************************************************************************************************************************
	#method returning the dict with the phases affecting the current phase
	def get_di_phase_interference(self):
		return self._di_phase_interference
	

#*****************************************************************************************************************************************************************************************
	#method returning he parameter for the travel duration from the input link to the output link associated with the queue
	#def get_param_travel_durat_from_input_lk_to_output_lk(self):
		#return self._param_travel_durat_from_input_lk_to_output_lk

#*****************************************************************************************************************************************************************************************
	
	#method returning the dictionary of which key=time of an end hold veh at que event, 
	#value=the number of vehicles corresponding to this t_end_veh_hold_at_que
	#def get_dict_key_t_end_hold_veh_at_que_ev_value_nb_of_veh(self):
		#return self._dict_key_t_end_hold_veh_at_que_ev_value_nb_of_veh
#*****************************************************************************************************************************************************************************************
	#method returning the list of the merging queues with/to the current que
	#def get_li_id_merging_ques(self):
		#return self._li_id_merging_ques
#*****************************************************************************************************************************************************************************************
	#method returning the variable indicating if the queue is related to a prior,minor or other type of phase
	#def get_type_related_phase(self):
		#return self._type_related_phase
#*****************************************************************************************************************************************************************************************
	#method returning the list with the minor, prior movements associated with the prior,minor, queue
	#def get_li_id_minor_prior_phases_related_to_que(self):
		#return self._li_id_minor_prior_phases_related_to_que
#*****************************************************************************************************************************************************************************************
	#method returning the diction with the sensor information
	def get_di_detector_associated_to_que(self):
		return self._di_detector_associated_to_que

#*****************************************************************************************************************************************************************************************
	#method returning the list with the main phases related to the side phase
	#def get_li_id_main_phases_related_to_current_side_que(self):
		#return self._li_id_main_phases_related_to_current_side_que
#*****************************************************************************************************************************************************************************************
	#method returning the list with the side phases related to the main phase
	#def get_li_id_side_phases_related_to_current_main_que(self):
		#return self._li_id_side_phases_related_to_current_main_que
#*****************************************************************************************************************************************************************************************
	#method returning the variable indicating the number of veh arrived at queue during the current period.
	#def get_nb_veh_arrived_current_period(self):
		#return self._nb_veh_arrived_current_period

#*****************************************************************************************************************************************************************************************
	
	#method modifying the id of the queue
	def set_id_queue(self,n_v):
		self._id_queue=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the id of the associated link
	def set_id_associated_link(self,n_v):
		self._id_associated_link=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the id of the associated output link
	def set_id_associated_output_link(self,n_v):
		self._id_associated_output_link=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the  associated phase of this queue
	def set_associated_phase_to_queue(self,n_v):
		self._associated_phase_to_queue=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the  vehicle queue at the associated  link
	def set_queue_veh(self,n_v):
		self._queue_veh=n_v

#*****************************************************************************************************************************************************************************************
	#method  modifying the max vehicle queue size
	def set_max_veh_queue_size(self,n_v):
		self._max_veh_queue_size=n_v

#*****************************************************************************************************************************************************************************************
	#method modifyng the associated saturation flow of the queue
	def set_sat_flow_queue(self,n_v):
		self._sat_flow_queue=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the number of vehciles that can depart simultanesouly the queue,  defined from the sat flow
	def set_nb_veh_cal_leave_simult_que_from_sat_flow(self,n_v):
		self._nb_veh_cal_leave_simult_que_from_sat_flow=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the required time for departing the queue
	def set_required_depart_time_que(self,n_v):
		self._required_depart_time_que=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the the type of the vehicle queue
	def set_type_veh_queue(self,n_v):
		self._type_veh_queue=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the routing proportion of this queue
	#def set_rout_prop_queue(self,n_v):
		#self._rout_prop_queue=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the current service rate of the queue
	def set_current_queue_service_rate(self,n_v):
		self._current_queue_service_rate=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the current reached service rate
	def set_current_reached_service_rate(self,n_v):
		self._current_reached_service_rate=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the list with the positions of the presence detector in the que
	def set_li_posit_presence_detector_in_que(self,n_v):
		self._li_posit_presence_detector_in_que=n_v

#*****************************************************************************************************************************************************************************************
	#method modofying the list with the positions of the que size detector in the que
	#these detector measure whether  the que size has reached their position
	#def set_li_posit_que_size_detector_in_que(self,n_v):
		#self._li_posit_que_size_detector_in_que=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the dictionary key = position pres detector in the que, value=pres detector
	#def set_dict_key_pos_pres_detect_value_pres_detect_obj(self,n_v):
		#self._dict_key_pos_pres_detect_value_pres_detect_obj=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the dictionary key = position que size detector in the que, value=que size detector
	#def set_dict_key_pos_que_size_detect_value_que_size_detect(self,n_v):
		#self._dict_key_pos_que_size_detect_value_que_size_detect=n_v
#*****************************************************************************************************************************************************************************************
	#method modifyng the total number of vehicles passed by this queue
	def set_total_mumber_of_veh_passages_by_queue(self,n_v):
		self._total_mumber_of_veh_passages_by_queue=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the dict with the phases affecting the current phase
	def set_di_phase_interference(self,n_v):
		self._di_phase_interference=n_v
	
#*****************************************************************************************************************************************************************************************


	#method modifying the diction with the sensor information
	def set_di_detector_associated_to_que(self,n_v):
		self._di_detector_associated_to_que=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the number of vehicles chosen the  queue during a period
	#def set_current_nb_veh_chosen_que_during_period(self,n_v):
		#self._current_nb_veh_chosen_que_during_period=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying he parameter for the travel duration from the input link to the output link associated with the queue
	#def set_param_travel_durat_from_input_lk_to_output_lk(self,n_v):
		#self._param_travel_durat_from_input_lk_to_output_lk=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying  the list with the id of the merging queues with/to the current que
	#def set_li_id_merging_ques(self,n_v):
		#self._li_id_merging_ques=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the dictionary of which key=time of an end hold veh at que event, 
	#value=the number of vehicles corresponding to this t_end_veh_hold_at_que
	#def set_dict_key_t_end_hold_veh_at_que_ev_value_nb_of_veh(self,n_v):
		#self._dict_key_t_end_hold_veh_at_que_ev_value_nb_of_veh=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the variable indicating if the queue is related to a prior,minor or other type of phase
	#def set_type_related_phase(self,n_v):
		#self._type_related_phase=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the list with the minor, prior movements associated with the prior,minor, queue
	#def set_li_id_minor_prior_phases_related_to_que(self,n_v):
		#self._li_id_minor_prior_phases_related_to_que=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the list with the main phases related to the side phase
	#def set_li_id_main_phases_related_to_current_side_que(self,n_v):
		#self._li_id_main_phases_related_to_current_side_que=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the list with the side phases related to the main phase
	#def set_li_id_side_phases_related_to_current_main_que(self,n_v):
		#self._li_id_side_phases_related_to_current_main_que=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the variable indicating the number of veh arrived at queue during the current period.
	#def set_nb_veh_arrived_current_period(self,n_v):
		#self._nb_veh_arrived_current_period=n_v

#*****************************************************************************************************************************************************************************************
	#method returning the number of vehicles that have remained in the queue for at least the min hold time
	def fct_calcul_nb_of_veh_have_remained_in_que_at_least_for_min_hold_time(self,t_current,min_hold_time,li_vehicles):
	
		nb_veh=0
		
		for i in li_vehicles:
			#print("i.get_t_vehicle_arrival_at_current_queue(),",i.get_t_vehicle_arrival_at_current_queue(),\
			#"t_current",t_current,"i.get_t_vehicle_arrival_at_current_queue()-t_current",i.get_t_vehicle_arrival_at_current_queue()-t_current,\
			#"min_hold_time",min_hold_time)
			if t_current-i.get_t_vehicle_arrival_at_current_queue()>=min_hold_time:
				nb_veh+=List_Explicit_Values.initialisation_value_to_one
			else:
				break
		#print("nb_veh",nb_veh,"len(li_vehicles))",len(li_vehicles))
			
		return nb_veh
		
#*****************************************************************************************************************************************************************************************
	#method returning 1or zero according  to when there is at least one vehicle in the queue or not
	def fct_examine_presence_at_least_one_veh_in_que_1(self):
		
		if self._type_veh_queue==[]:
			return List_Explicit_Values.initialisation_value_to_zero
		else:
			return List_Explicit_Values.initialisation_value_to_one

#*****************************************************************************************************************************************************************************************
	#method returning the number of vehicles that have remained in the queue for at least the min hold time and 
	#for which ni veh departure event is planned
	def fct_calcul_nb_of_veh_have_remained_in_que_at_least_for_min_hold_time_without_planned_dep(self,t_current,min_hold_time,li_vehicles,\
	val_precision):
	
		nb_veh=0
		
		for i in li_vehicles:
			#print("i.get_t_vehicle_arrival_at_current_queue(),",i.get_t_vehicle_arrival_at_current_queue(),\
			#"t_current",t_current,"i.get_t_vehicle_arrival_at_current_queue()-t_current",i.get_t_vehicle_arrival_at_current_queue()-t_current,\
			#"min_hold_time",min_hold_time)
			if round(t_current-i.get_t_vehicle_arrival_at_current_queue(),val_precision)>=min_hold_time and \
			i.get_state_veh()==Cl_Vehicle.TYPE_STATE_VEH["other"]:
				nb_veh+=List_Explicit_Values.initialisation_value_to_one
			else:
				break
		#print("nb_veh",nb_veh,"len(li_vehicles))",len(li_vehicles))
		#if t_current==85.1 and self._id_associated_link==1 and self._id_associated_output_link==2:
			#a=round(t_current-i.get_t_vehicle_arrival_at_current_queue(),val_precision)
			#print("t_current-i.get_t_vehicle_arrival_at_current_queue()",a,\
			#"min_hold_time",min_hold_time,"i.get_state_veh()",i.get_state_veh(), "i.get_id_veh()",i.get_id_veh(),"nb_veh",nb_veh)
		return nb_veh
		
#*****************************************************************************************************************************************************************************************
	#method examining if the  n first vehicles in the queue has remained for at least the min hold time and has no planned 
	#departure event. It will be used for defining the number of veh that can go in a micro simulation.
	#nb_veh_to_exam= the nb of veh which we wish to examine
	def fct_calcul_nb_of_n_veh_remained_in_que_for_min_t_hold_without_planned_dep_for_mi(self,\
	t_current,min_hold_time,li_vehicles,nb_veh_to_exam,val_t_precision):
	
		nb_veh=0
		#print("hereee",li_vehicles[:nb_veh_to_exam])
		for i in li_vehicles[:nb_veh_to_exam]:
			#print("i.get_t_vehicle_arrival_at_current_queue(),",i.get_t_vehicle_arrival_at_current_queue(),\
			#"t_current",t_current,"t_current-i.get_t_vehicle_arrival_at_current_queue()-",t_current-i.get_t_vehicle_arrival_at_current_queue(),\
			#"min_hold_time",min_hold_time)
			#print("in fct exam veh remained in que without plan dep", round(t_current-i.get_t_vehicle_arrival_at_current_queue(),val_t_precision)>=min_hold_time,\
			#i.get_state_veh(),Cl_Vehicle.TYPE_STATE_VEH["other"])
			if round(t_current-i.get_t_vehicle_arrival_at_current_queue(),val_t_precision)>=min_hold_time and \
			i.get_state_veh()==Cl_Vehicle.TYPE_STATE_VEH["other"]:
				nb_veh+=List_Explicit_Values.initialisation_value_to_one
			else:
				break
		#print("nb_veh",nb_veh,"len(li_vehicles))",len(li_vehicles))
			
		return nb_veh

#*****************************************************************************************************************************************************************************************
	#method examining if the first vehicles in the queue has remained for at least the min hold time and has no planned 
	#departure event. It will be used for defining the number of veh that can go in a micro simulation.
	#nb_veh_to_exam= the nb of veh which we wish to examine
	def fct_calcul_first_veh_remained_in_que_for_min_t_hold_without_planned_dep_for_mi(self,\
	t_current,min_hold_time,li_vehicles,val_t_precision):
	
		nb_veh=0
		#print("hereee",li_vehicles[:nb_veh_to_exam])
		for i in li_vehicles[:1]:
			#print("i.get_t_vehicle_arrival_at_current_queue(),",i.get_t_vehicle_arrival_at_current_queue(),\
			#"t_current",t_current,"t_current-i.get_t_vehicle_arrival_at_current_queue()-",t_current-i.get_t_vehicle_arrival_at_current_queue(),\
			#"min_hold_time",min_hold_time)
			#print("in fct exam veh remained in que without plan dep", round(t_current-i.get_t_vehicle_arrival_at_current_queue(),val_t_precision)>=min_hold_time,\
			#i.get_state_veh(),Cl_Vehicle.TYPE_STATE_VEH["other"])
			if round(t_current-i.get_t_vehicle_arrival_at_current_queue(),val_t_precision)>=min_hold_time and \
			i.get_state_veh()==Cl_Vehicle.TYPE_STATE_VEH["other"]:
				nb_veh+=List_Explicit_Values.initialisation_value_to_one
			else:
				break
		#print("nb_veh",nb_veh,"len(li_vehicles))",len(li_vehicles))
			
		return nb_veh

#*****************************************************************************************************************************************************************************************

	#method calculating the current service rate of a queue
	def fct_calcul_queue_service_rate(self,val_t_period_duration):
	
		#the service rate= the service flow x the period duration
		return self._sat_flow_queue * val_t_period_duration

#*****************************************************************************************************************************************************************************************
	#function defining the number of vehicles to leave in a micro management and the associated required time
	#it returns [nb veh to leave, time toleave the queue]
	def fct_defin_nb_veh_leave_mi_1(self,v_t_unit):
	
		nb_veh_go_and_t=[]
		#if the sat flow is > 1
		if self._sat_flow_queue>1:
			#nb_veh_go_and_t=[round(v_sat_flow, v_round_prec),v_t_unit]
			nb_veh_go_and_t=[math.ceil(self._sat_flow_queue),v_t_unit]
	
		#if the sat flow =1
		elif self._sat_flow_queue==1:
			nb_veh_go_and_t=[self._sat_flow_queue,v_t_unit]
	
		#if the sat flow is <1
		else:
			#calc the required time for one veh to go
			#t_req=round(v_t_unit/v_sat_flow, v_round_prec)
			#print("t_req",t_req,"v_t_unit",v_t_unit,"v_sat_flow",v_sat_flow)
		
			nb_veh_partir_simult=math.ceil(self._sat_flow_queue)
		
			#duree_init=v_t_unit*nb_veh_partir_simult/self._sat_flow_queue
		
			#duree_init_multipliee=duree_init*100
		
			#chiffres decimaux
			#partie_entiere=math.floor(duree_init_multipliee)
			#partie_decimale=duree_init_multipliee-partie_entiere
		
			#if no decimals
			#if partie_decimale==0:
				#t_req=duree_init
		
			#if decimals
			#else:
				#t_req=(duree_init_multipliee//1)/100
			#t_req=(math.floor((v_t_unit*nb_veh_partir_simult/self._sat_flow_queue)*100))/100
			#t_req=(math.floor((v_t_unit*nb_veh_partir_simult/self._sat_flow_queue)*10))/10
			t_req=self.fct_defining_t_req_for_single_veh_depart_when_sat_flow_infer_to_one(\
			val_t_unit=v_t_unit,val_nb_veh_partir_simult=nb_veh_partir_simult, val_sat_flow=self._sat_flow_queue,val_dec_digits=10)
		
			nb_veh_go_and_t=[nb_veh_partir_simult,t_req]
		
		return nb_veh_go_and_t
#*****************************************************************************************************************************************************************************************	
	#function defining the number of vehicles to leave in a micro management and the associated required time
	#it returns [nb veh to leave, time toleave the queue]
	def fct_defin_nb_veh_leave_mi(self,v_t_unit):
	
		nb_veh_go_and_t=[]
		
		#calc the required time for one veh to go
		
		nb_veh_partir_simult=List_Explicit_Values.initialisation_value_to_one
		
			
		t_req=self.fct_defining_t_req_for_single_veh_depart(\
		val_t_unit=v_t_unit, val_sat_flow=self._sat_flow_queue,val_dec_digits=10)
		
		nb_veh_go_and_t=[nb_veh_partir_simult,t_req]
		
		return nb_veh_go_and_t
	
#*****************************************************************************************************************************************************************************************

	#method returning the required time for 1 vehicle to eave from the sat flow, when sat flow is <1
	def fct_defining_t_req_for_single_veh_depart_when_sat_flow_infer_to_one(self,val_t_unit,val_nb_veh_partir_simult, val_sat_flow,val_dec_digits=10):
		return (math.floor((val_t_unit*val_nb_veh_partir_simult/val_sat_flow)*val_dec_digits))/val_dec_digits

#*****************************************************************************************************************************************************************************************
	#method returning the required time for 1 vehicle to leave from the sat flow
	def fct_defining_t_req_for_single_veh_depart(self,val_t_unit, val_sat_flow,val_dec_digits=10):
		
		return (math.floor((val_t_unit/val_sat_flow)*val_dec_digits))/val_dec_digits

#*****************************************************************************************************************************************************************************************
	#method updating the queue when  vehicle arrives
	def fct_update_veh_queue_when_veh_ar(self):
	
		#we increase the number of vehicles passed by this queue
		self._total_mumber_of_veh_passages_by_queue+=List_Explicit_Values.initialisation_value_to_one
		
#*****************************************************************************************************************************************************************************************
	#method updating the queue when  a set of one or more vehicle arrived
	def fct_update_veh_queue_when_set_veh_ar(self,val_nb_veh_arrived):
	
		#we increase the number of vehicles passed by this queue
		self._total_mumber_of_veh_passages_by_queue+=val_nb_veh_arrived
		
#*****************************************************************************************************************************************************************************************
	#method updating the queue when a vehicle  cannot leave the queue as soon as it arrives
	def fct_update_veh_queue_when_veh_prohibited_to_leave_no_mod(self,vehicle):
		
		#we add the vehicle in the queue
		self._queue_veh.append(vehicle)

#*****************************************************************************************************************************************************************************************
	#method updating the queue when a vehicle  cannot leave the queue as soon as it arrives
	def fct_update_veh_queue_when_veh_prohibited_to_leave_with_mod(self,vehicle):
		
		#we add the vehicle in the queue
		self._queue_veh.append(vehicle)
		
		#if self._id_associated_link==14 and( self._id_associated_output_link==2 or self._id_associated_output_link==15 or self._id_associated_output_link==17):
			#print("IN CL Veh qeue avant",self._nb_veh_arrived_current_period)
		#we update the number of vehicles arrived in que du
		#self._nb_veh_arrived_current_period+=1
		#if self._id_associated_link==14 and( self._id_associated_output_link==2 or self._id_associated_output_link==15 or self._id_associated_output_link==17):
			#print("apres",self._nb_veh_arrived_current_period)
	

#*****************************************************************************************************************************************************************************************
	#method updating the vehicle queue when a number of vehicles quit the queue immediately after their arrival at the queue
	#so the vehicles have not been joined in the queue, case of RT
	#we suppose that we have already verified that this number of vehicles can actually leave the queue
	def fct_update_veh_queue_when_single_veh_quit_que_im_by_its_ar(self):
		
		#we update the currently reached service rate
		self._current_reached_service_rate+=List_Explicit_Values.initialisation_value_to_one
	
		

#*****************************************************************************************************************************************************************************************
	#method updating the vehicle queue when vehicles already in the queue quit the queue
	#li_vehicles_remaining_in_queue a list with the vehicle objects remaining in the queue
	#nb_of_leaving_veh=the number of vehicles leaving the queue
	def fct_update_veh_queue_when_vehicles_already_in_queue_quit_queue(self,li_vehicles_remaining_in_queue,nb_of_leaving_veh):
	
		#we update the currently reached service rate
		self._current_reached_service_rate+=nb_of_leaving_veh
		
		#the new list of vehicles in the queue
		self._queue_veh=li_vehicles_remaining_in_queue
		

#*****************************************************************************************************************************************************************************************
	#method updating the vehicle queue when the first vehicle of the queue quit the queue 
	def fct_update_veh_queue_when_first_veh_quit_queue(self):
	
		#we update the currently reached service rate
		self._current_reached_service_rate+=List_Explicit_Values.initialisation_value_to_one
		
		#we remove the first veh of the queue
		self._queue_veh.remove(self._queue_veh[List_Explicit_Values.val_first_element_of_list])
		
		
#*****************************************************************************************************************************************************************************************
	
	
	#method defining if the vehicle can leave the queue by the end of the min hold time, it returns 1 or 0 according as
	#if the vehicle can or cannot leave
	#val_associat_phase_to_que=[id input link to que, id output link from que]
	#val_t_end_current_ncm=t_start_control+val_duration_control-1, this is the last minute during which the current cotnrol is applied to the netw
	#val_t_veh_can_depart= time at which finishes the end of hold of the veh in the queue
	#val_t_veh_can_depart= time when the  hold time ends
	def fct_defining_whether_veh_can_leave_que_at_the_end_of_min_hold_time(self,val_t_end_current_ncm,\
	val_t_veh_can_depart):
		
		if val_t_veh_can_depart<=val_t_end_current_ncm:
			return List_Explicit_Values.initialisation_value_to_one
		else:
			return List_Explicit_Values.initialisation_value_to_zero
			
#*****************************************************************************************************************************************************************************************
	#method creating a dictionary of presence detectors
	#dict, key=initial posit of the detector in the que (1st posit corresponds to 1), value=detector
	#val_li_posit_presence_detector_in_que= [ [id_init_posit sensor in que, id_final_posit_sensor in que],....]
	def fct_creat_di_presence_detectors_1(self,val_li_posit_presence_detector_in_que):
		
		di={}
		for i in val_li_posit_presence_detector_in_que:
			for j in i:
				detector=Cl_Sensor_Presence_Detection.Sensor_Presence_Detection(\
				val_id_link_sens_location=self._id_associated_link,val_id_que_destination_link_sens_location=self._id_associated_output_link,\
				val_init_que_position_measured_by_sens=j[0],val_final_que_position_measured_by_sensor=j[1])
			
				di[j[0]]=detector
			
		return di

#*****************************************************************************************************************************************************************************************
	#method creating a dictionary of presence detectors
	#dict, key=initial posit of the detector in the que (1st posit corresponds to 1), value=detector
	#val_li_posit_presence_detector_in_que= [ [id_init_posit sensor in que, id_final_posit_sensor in que],....]
	def fct_creat_di_presence_detectors_2(self,val_li_posit_presence_detector_in_que):
		
		di={}
		#print(val_li_posit_presence_detector_in_que)
		#val_li_posit_presence_detector_in_que=[...,[init posit i det, final posit i detector],...]
		for i in val_li_posit_presence_detector_in_que:
			
			detector=Cl_Sensor_Presence_Detection.Sensor_Presence_Detection(\
			val_id_link_sens_location=self._id_associated_link,val_id_que_destination_link_sens_location=self._id_associated_output_link,\
			val_init_que_position_measured_by_sens=i[0],val_final_que_position_measured_by_sensor=i[1])
			
			di[i[0]]=detector
			#print("HERE",i[0])
			#import sys
			#sys.exit()
			
		return di

#*****************************************************************************************************************************************************************************************
	#method creating a dictionary of que size detectors
	#dict, key=initial posit of the detector in the que (1st posit corresponds to 1), value=detector
	#val_li_posit_que_size_detector_in_que=[id position1 sensor in que, id position2 sensor in que,...]
	def fct_creat_di_que_size_detectors_3(self,val_li_posit_que_size_detector_in_que):
		
		di={}
		#print(val_li_posit_que_size_detector_in_que)
		#import sys
		#sys.exit()
		for i in val_li_posit_que_size_detector_in_que:
			detector=Cl_Sensor_Que_Size_Detection.Sensor_Que_Size_Detection(\
			val_id_link_sens_location=self._id_associated_link,val_id_que_destination_link_sens_location=self._id_associated_output_link,\
			val_init_que_position_measured_by_sens=i)
			
			di[i]=detector
			
		return di
			
#*****************************************************************************************************************************************************************************************
	#method examining if the max service rate of the queue has been reached, it returns 1 id the max serv rate is achieved zero otherwise
	def fct_examine_max_que_service_rate_achieved(self):
	
		if self._current_reached_service_rate==self._current_queue_service_rate:
			return List_Explicit_Values.initialisation_value_to_zero
		elif self._current_reached_service_rate<self._current_reached_service_rate:
			return List_Explicit_Values.initialisation_value_to_one
		else:
			print("PROBLEM IN CL_VEHICLE QUE, current_reached_service_rate",self._current_reached_service_rate,\
			"current_queue_service_rate",self._current_queue_service_rate)
			import sys
			sys.exit()

#*****************************************************************************************************************************************************************************************
	#method increasing the number of vehicles chosen the queue during the current  period
	#def fct_update_current_nb_veh_chosen_que_during_period(self,nb_veh_to_add=1):
		#self._current_nb_veh_chosen_que_during_period+=nb_veh_to_add
#*****************************************************************************************************************************************************************************************
	#method returning the number of vehicles exsiting at the current moment in the region covered by the detector 
	def fct_returning_nb_veh_existing_in_area_covered_by_detector(self,val_id_detector):
	
		q_s=len(self._queue_veh)
		
		#if the detector covers the entire (que) area
		if self._di_detector_associated_to_que[val_id_detector]==-1:
			return q_s
		#if the detector covers the the que from a given point (up to the end of the queue)
		elif self._di_detector_associated_to_que[val_id_detector]>0:
			return q_s-self._di_detector_associated_to_que[val_id_detector]
		
		#if the detector covers only a zone
		else:
			#if the que size joins at least the beginning of the region covered by the detector
			if q_s>=self._di_detector_associated_to_que[val_id_detector][0][0]:
			
				#if the que size is at most as large as the max posit the detector can capture
				if q_s<=self._di_detector_associated_to_que[val_id_detector][0][1]:
					return self._di_detector_associated_to_que[val_id_detector][0][1]-q_s
				
				#if the que size is  larger than the max posit the detector can capture
				else:
					return self._di_detector_associated_to_que[val_id_detector][1]
				
			#if the que size does not join  the beginning of the region covered by the detector
			else:
				return List_Explicit_Values.initialisation_value_to_zero
		
#*****************************************************************************************************************************************************************************************
	#methid returning a dict with the number of vehicles captured by each detector associated with the queue
	def fct_return_nb_veh_captured_by_each_detector_of_que(self):
	
		di_rep={}
		
		for i in self._di_detector_associated_to_que:
			di_rep[i]=self.fct_returning_nb_veh_existing_in_area_covered_by_detector(val_id_detector=i)
			
		return di_rep
			
#*****************************************************************************************************************************************************************************************
	#method examining if there is at elast one sensor of the queue detecting at least 'n' vehicle in which case it returns 
	#[1,idictionary with the measurements of each sensor, id first found sensor measuring a positive value] otherwise it returns None
	def fct_exam_whether_at_least_nb_veh_detected_by_a_que_sensor(self,val_min_nb_veh_to_detect):
		
		di_id_det_nb_detected_veh=self.fct_return_nb_veh_captured_by_each_detector_of_que
		
		rep=0
		for i in di_id_det_nb_detected_veh:
			if di_id_det_nb_detected_veh[i]>val_min_nb_veh_to_detect:
				return [1,di_id_det_nb_detected_veh,i]
		if rep==0:
			return None


#*****************************************************************************************************************************************************************************************
	#method returning the sat flow corresponding to the queue when another queue interfers
	def fct_calcul_sat_flow_at_given_t_when_que_interf(self,val_id_affecting_que):
		
		return round(self._sat_flow_queue*self._di_phase_interference[val_id_affecting_que[0],val_id_affecting_que[1]],2)

#*****************************************************************************************************************************************************************************************


	

#ex
#qu=Vehicle_Queue(val_id_queue=11,val_type_queue=TYPE_VEHICLE_QUEUE["left_turn"],val_id_associated_link=21)
#print("queue id , type",qu.get_id_queue(),qu.get_type_queue())






