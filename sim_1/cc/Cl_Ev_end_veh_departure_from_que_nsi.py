import Cl_Event
import Cl_Vehicle
import Cl_Global_Functions
import Cl_Global_Functions_nsi
import List_Explicit_Values
import Cl_Ev_veh_arrived_at_que
import Cl_Ev_end_veh_hold_at_que
import Cl_Vehicle_Queue
import Cl_Network_Link
import Cl_Intersection
import Cl_Decisions
import Cl_Record_Database
import List_Explicit_Values
import Global_Functions
import math

class Ev_end_veh_departure_from_que_nsi(Cl_Event.Event):

	"""class defining the event of a vehicle departing from a queue of a non signalised intersection """
	
	def __init__(self,val_ev_t=-1,val_id_queue_obj=-1,val_nb_depart_veh=-1):
	
		gl_funct_obj=Cl_Global_Functions.Global_Functions()
		
		gl_funct_nsi_obj=Cl_Global_Functions_nsi.Global_Functions_nsi()
		
		Cl_Event.Event.__init__(self,val_event_time=val_ev_t,\
		val_event_type=Cl_Event.TYPE_EV["type_ev_end_veh_departure_from_que_nsi"],\
		val_global_fct_obj=gl_funct_obj,val_global_fct_nsi_obj=gl_funct_nsi_obj)
		
		#the id of vehicle queue object associated with this event
		self._id_queue_obj=val_id_queue_obj
		
		#the number of departed vehicles
		self._nb_depart_veh=val_nb_depart_veh
		
		#the decision object  associated with this event
		obj_decisions=Cl_Decisions.Decisions()
		
		self._obj_decisions=obj_decisions
		
		
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
	#method  treat the case when exam if other vehicles can go, infinite link capacity micro manag
	def fct_treat_case_exam_veh_can_go_by_end_veh_dep_nsi_infinite_lk_cap_nsi_1(self,va_fct_exam_nb_dep_veh_by_end_veh_dep,\
	va_li_param_fct_exam_nb_dep_veh_by_end_veh_dep,va_netwrk,va_ev_list):
		
		#we examine if other vehicles can go
		#rep= [...,[id_phase,nb_veh_leave,t_ev_end_veh_dep],..]  or [[None,0,None]]
		rep=va_fct_exam_nb_dep_veh_by_end_veh_dep(*va_li_param_fct_exam_nb_dep_veh_by_end_veh_dep)
		
		#if other vehicles can go
		if rep[0][0]!=None:
			#we create the end veh dep events
			for i in rep:
				ev_en_veh_dep_nsi=Ev_end_veh_departure_from_que_nsi(val_ev_t=i[2],val_id_queue_obj=i[0],\
				val_nb_depart_veh=i[1])
				
				ev_en_veh_dep_nsi.fct_insertion_even_in_event_list(event_list=va_ev_list,\
				message="IN CL_EV_VEH_END_DEPARTURE FROM QUE_NSI IN FUNCT fct_treat_case_exam_veh_can_go_by_end_veh_dep_nsi_infinite_lk_cap_nsi,\
				EVENT END VEH DEPART HAS TIME < TIME FIRST EVENT IN THE LIST")
				
		
#*****************************************************************************************************************************************************************************************
	
	#method treat the event when a infinite link capacity is been considered
	def fct_treat_event_end_veh_dep_case_infinite_lk_capacity_nsi(self,va_netwrk,va_time_unit,va_fct_calcul_nb_and_t_dep_veh_nsi,\
	va_li_param_va_fct_calcul_nb_and_t_dep_veh_nsi,va_round_prec,va_ev_list,va_fct_calcul_trav_time,va_min_hold_time,va_ti_unit,\
	va_param_epsilon_t_completion_depart,va_file_recording_event_db):
	
		#the list of departed vehicles, the earlier arrivals will leave first
		li_veh_dep=va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[self._id_queue_obj[0],self._id_queue_obj[1]].get_queue_veh()[:self._nb_depart_veh]
		
		#if vehicles left from a  minor phase, we indicate that no vehicle from minor phase  now crosses the intersection
		if va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[self._id_queue_obj[0],self._id_queue_obj[1]].get_type_related_phase()==Cl_Vehicle_Queue.TYPE_RELATED_PHASE["minor_mv"]:
			
			va_netwrk.get_di_intersections()[val_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].\
			get_id_head_intersection_node()].set_indicator_minor_mv_cross_intersection(List_Explicit_Values.initialisation_value_to_zero)
		elif va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[self._id_queue_obj[0],self._id_queue_obj[1]].get_type_related_phase()==Cl_Vehicle_Queue.TYPE_RELATED_PHASE["prior_mv"]:
			
			va_netwrk.get_di_intersections()[val_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].\
			get_id_head_intersection_node()].set_indicator_prior_mv_cross_intersection(List_Explicit_Values.initialisation_value_to_zero)	
			
		#we update the vehicle queue
		va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[self._id_queue_obj[0],self._id_queue_obj[1]].fct_update_veh_queue_when_vehicles_already_in_queue_quit_queue(\
		va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[self._id_queue_obj[0],self._id_queue_obj[1]].get_queue_veh()[self._nb_depart_veh:],self._nb_depart_veh)
		
		
		#if the que is not RT, we update the intersection heap indicating that the veh from its que crosses the intersection
		#we remove the phase id
		if va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[self._id_queue_obj[0],self._id_queue_obj[1]].get_type_veh_queue()!=Cl_Vehicle_Queue.TYPE_VEHICLE_QUEUE["right_turn"]:
		
			del va_netwrk.get_di_intersections()[va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].get_id_head_intersection_node()].\
			get_di_indicating_id_phase_cros_veh()[self._id_queue_obj[0],self._id_queue_obj[1]]
			
			
			
		#we update each departed vehicle
		for i in li_veh_dep:
			#i.fct_veh_update_when_leaving_queue_going_to_another_link(self._event_time)
			i.fct_veh_update_when_depart_completed(\
			val_t_end_departure=self._event_time,val_new_id_lk_location=self._id_queue_obj[1])
		#calcul travel time for the departed veh, from the beginning of the link until the end of the chosen queue
		li_parameter_fct_calculating_travel_time=[self._event_time,[self._id_queue_obj[0],self._id_queue_obj[1]],va_netwrk,va_round_prec]
		
		#if the vehicle has not arrived at an exit link
		if va_netwrk.get_di_all_links()[li_veh_dep[0].get_current_id_link_veh_location()].get_type_network_link() !=\
		Cl_Network_Link.TYPE_NETWORK_LINK["exit"]:
		
			t_arrival=va_fct_calcul_trav_time(*li_parameter_fct_calculating_travel_time)
			if t_arrival<0:
				print("PROBLEM CL_EV_END_VEH_DEP, fct_treat_event_case_infinite_lk_capacity,T_ARRIVAL: ", t_arrivaL)
				import sys
				sys.exit()
			#if the vehicle is at a  signalised intersection
			if va_netwrk.get_di_intersections()[va_netwrk.get_di_entry_internal_links()[li_veh_dep[0].get_current_id_link_veh_location()].\
			get_id_head_intersection_node()].get_type_intersection()==Cl_Intersection.TYPE_INTERSECTION["signalised_intersection"]:
			
				#print("t_arrival",t_arrival,"self._event_time",self._event_time)
				#we create the event vehicle arrival 
				ev_veh_ar=Cl_Ev_veh_arrived_at_que.Ev_veh_arrived_at_que(val_event_t=t_arrival,val_li_vehicle=li_veh_dep,\
				val_id_arrival_link=va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
				[self._id_queue_obj[0],self._id_queue_obj[1]].get_id_associated_output_link())
			
				#we add the event in the event list
				ev_veh_ar.fct_insertion_even_in_event_list(event_list=ev_list,\
				message="IN CL_EV_VEH_END_DEPARTURE FROM QUE_NSI IN FUNCT fct_treat_event_case_infinite_lk_capacity,\
				VEH ARRIVAL AT QUE EVENT HAS TIME < TIME FIRST EVENT IN THE LIST")
			
			#if the vehicle is at a non-signalised intersection
			else:
				ev_veh_ar_nsi=Cl_Ev_veh_arrived_at_que_nsi.Ev_veh_arrived_at_que_ns(val_event_t=t_arrival,val_li_vehicle= li_veh_dep,\
				val_id_arrival_link=va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
				[self._id_queue_obj[0],self._id_queue_obj[1]].get_id_associated_output_link())
			
				#we add the event in the event list
				ev_veh_ar_nsi.fct_insertion_even_in_event_list(event_list=ev_list,\
				message="IN CL_EV_VEH_END_DEPARTURE FROM QUE IN FUNCT fct_treat_event_case_infinite_lk_capacity,\
				VEH ARRIVAL AT QUE EVENT NSI HAS TIME < TIME FIRST EVENT IN THE LIST")
				
		#if vehicles have reached an exit link
		else:
			#for each vehicle
			for m in li_veh_dep:
				#we indicate the time at which the vehicle leaves the network
				m.fct_update_veh_when_arriving_at_exit_link(self._event_time)
				t_arrival=self._event_time
				
		#we create the list with the veh id in que
		if va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[self._id_queue_obj[0],self._id_queue_obj[1]].get_queue_veh() !=[]:
		
			li_veh_id_left_in_queue=[i.get_id_veh() for i in va_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].\
			get_set_veh_queue().get_di_obj_veh_queue_at_link()[self._id_queue_obj[0],self._id_queue_obj[1]].get_queue_veh()]
			
		#va_li_param_va_fct_calcul_nb_and_t_dep_veh=[va_netwrk,self._id_queue_obj,self._event_time,va_ti_unit,\
		#va_min_hold_time,va_round_prec,va_param_epsilon_t_completion_depart]
		
		
		#we examine if other vehicles can leave and from which phase and we treat the case
		nb_veh_to_go=va_fct_calcul_nb_and_t_dep_veh_nsi(*va_li_param_va_fct_calcul_nb_and_t_dep_veh_nsi)
		
		
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
			
				
			#we record the event in the db 
			record_db_obj.fct_write_object_in_db_file()
		
		#initialise the departed vehicles
		for i in li_veh_dep:
			#i.fct_initialising_veh_before_its_departure()
			i.fct_initialising_veh_before_its_arrival_at_que()
		
		
#*****************************************************************************************************************************************************************************************
	#method treat the event when a finite link capacity is been considered
	def fct_treat_event_case_finite_lk_capacity(self,va_netwrk,va_time_unit,va_fct_calcul_nb_and_t_dep_veh,\
	va_round_prec,va_ev_list,va_fct_calcul_trav_time,va_min_hold_time,va_file_recording_event_db):
		pass
		
#*****************************************************************************************************************************************************************************************
	
	#method treating the event
	def event_treat(self,val_netwrk=None,val_time_unit=-1,fct_calcul_trav_time=None,min_hold_time=-1,\
	fct_calcul_nb_and_t_dep_veh_end_veh_dep_nsi=None,val_round_prec=1,ev_list=[],val_param_epsilon_t_completion_depart=None,\
	file_recording_event_db=None):
	
		#if inifnite link capacity is been considered
		if val_netwrk.get_di_entry_internal_links()[self._id_queue_obj[0]].get_capacity_link() <0:
		
			val_li_param_va_fct_calcul_nb_and_t_dep_veh_nsi=[]
			
			self.fct_treat_event_end_veh_dep_case_infinite_lk_capacity_nsi(\
			va_netwrk=val_netwrk,va_time_unit=val_time_unit,\
			va_fct_calcul_nb_and_t_dep_veh_nsi=fct_calcul_nb_and_t_dep_veh_end_veh_dep_nsi,\
			va_li_param_va_fct_calcul_nb_and_t_dep_veh_nsi=val_li_param_va_fct_calcul_nb_and_t_dep_veh_nsi,\
			va_round_prec=val_round_prec,va_ev_list=ev_list,\
			va_fct_calcul_trav_time=fct_calcul_trav_time,va_min_hold_time=min_hold_time,va_ti_unit=val_time_unit,\
			va_param_epsilon_t_completion_depart=val_param_epsilon_t_completion_depart,\
			va_file_recording_event_db=file_recording_event_db)
		
		#if inifnite link capacity is been considered
		else:
			pass

























