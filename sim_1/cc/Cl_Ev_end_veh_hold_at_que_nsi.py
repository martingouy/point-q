import string
import Cl_Event
import List_Explicit_Values
import Cl_Global_Functions_nsi
import Global_Functions
import Cl_Decisions
import Cl_Vehicle
import Cl_Record_Database
import Cl_Vehicle_Queue
import Cl_Ev_end_veh_departure_from_que_nsi

class Ev_end_veh_hold_at_que_nsi(Cl_Event.Event):

	""" class defining the event of  the end of veh hold at queue for a non signalised intersection"""
	
	def __init__(self,val_event_t=-1,val_id_que=-1):
	
		gl_funct_nsi_obj=Cl_Global_Functions_nsi.Global_Functions_nsi()
		
		Cl_Event.Event.__init__(self,val_event_time=val_event_t,val_event_type=Cl_Event.TYPE_EV["ty_ev_end_veh_hold_at_que_nsi"],\
		val_global_fct_nsi_obj=gl_funct_nsi_obj)
		
		#the id of the associated que
		self._id_que=val_id_que
		
				
		
#*****************************************************************************************************************************************************************************************
	#method returning the id of the associated que
	def get_id_que(self):
		return self._id_que

#*****************************************************************************************************************************************************************************************

	#method modifying the id of the associated que
	def set_id_que(self,n_v):
		self._id_que=n_v

#*****************************************************************************************************************************************************************************************

	#method treating the event
	def event_treat_1(self):
		pass
		
	def event_treat(self,val_network,val_fct_exam_nb_dep_veh_by_end_hold_nsi,val_time_unit,\
	val_min_veh_hold_time_in_que,val_round_prec,ev_list,file_recording_event_db,val_param_epsilon_t_completion_depart):
	
		#on examine if vehicles can go
		#li_param_val_fct_exam_nb_dep_veh_by_end_hold_nsi=[val_network,self._id_que,\
		#val_time_unit,self._event_time,val_min_veh_hold_time_in_que,val_round_prec,val_param_epsilon_t_completion_depart]
		
		li_param_val_fct_exam_nb_dep_veh_by_end_hold_nsi=[]
			
		#nb_and_t_dep_veh=[nb_veh_leave,t_end_dep,t_start_veh_dep,veh_dep_duration]
		nb_and_t_dep_veh=val_fct_exam_nb_dep_veh_by_end_hold_nsi(*li_param_val_fct_exam_nb_dep_veh_by_end_hold_nsi)
		#print("HERE",nb_and_t_dep_veh)	
		
		#print("nb_and_t_dep_veh[1]",nb_and_t_dep_veh[1])
		if nb_and_t_dep_veh[1]==self._event_time and nb_and_t_dep_veh[0]>0:
			print("PROBLEM IN CL_EV_END_VEH_HOLD_AT_QUE_NSI,  fct_event_treat",\
			"nb depart veh and t dep: ",nb_and_t_dep_veh[0],nb_and_t_dep_veh[1],"t_current",self._event_time)
			import sys
			sys.exit()
			
		#if vehicles can leave
		if nb_and_t_dep_veh[List_Explicit_Values.val_first_element_of_list] >0:
			
			#if the movement is prior or minor, the we indicate the intersection that a prior or minor mv is about to cross
			#if val_netw.get_di_entry_internal_links()[id_que[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
			#[id_que[0],id_que[1]].get_type_related_phase()==Cl_Vehicle_Queue.TYPE_RELATED_PHASE["minor_mv"]:
				#val_netw.get_di_intersections()[val_netw.get_di_entry_internal_links()[id_que[0]].\
				#get_id_head_intersection_node()].set_indicator_minor_mv_cross_intersection(List_Explicit_Values.initialisation_value_to_one)
			
			#elif val_netw.get_di_entry_internal_links()[id_que[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
			#[id_que[0],id_que[1]].get_type_related_phase()==Cl_Vehicle_Queue.TYPE_RELATED_PHASE["prior_mv"]:
				#val_netw.get_di_intersections()[val_netw.get_di_entry_internal_links()[id_que[0]].\
				#get_id_head_intersection_node()].set_indicator_prior_mv_cross_intersection(List_Explicit_Values.initialisation_value_to_one)
			
			#we update each departing vehicle ( its state  and t start depart) and the corresponding indicators of the intersection
			t_end_veh_dep=nb_and_t_dep_veh[List_Explicit_Values.val_second_element_of_list]
			
			self._global_fct_nsi_obj.fct_update_each_dep_veh_and_veh_heap_at_nsi(\
			v_nb_dep_veh=nb_and_t_dep_veh[List_Explicit_Values.val_first_element_of_list],\
			v_id_que=self._id_que,v_netwk=val_network,\
			v_t_end_veh_depart=t_end_veh_dep,v_t_start_depart=nb_and_t_dep_veh[2],\
			v_depart_duration=nb_and_t_dep_veh[3])
				
			ev_end_veh_dep_nsi=Cl_Ev_end_veh_departure_from_que_nsi.Ev_end_veh_departure_from_que_nsi(\
			val_ev_t=t_end_veh_dep,\
			val_id_queue_obj=self._id_que,val_nb_depart_veh=nb_and_t_dep_veh[List_Explicit_Values.val_first_element_of_list])
			
			#we insert the event in the event list
			ev_end_veh_dep_nsi.fct_insertion_even_in_event_list(event_list=ev_list,\
			message="IN CL_GLOB FUNCT_NSI  IN FUNCT fct_treat_case_veh_can_go_nsi,\
			EVENT END VEH DEP HAS TIME < TIME FIRST EVENT IN THE LIST")
				
				
		#if no vehicles can leave, we do nothing,  they will leave by an event end veh departure
		record_db_obj=Cl_Record_Database.Record_Database(val_file_db=file_recording_event_db,\
		val_ev_time=self._event_time,val_ev_type=self._event_type,\
		val_type_inters_node=val_network.get_di_intersections()[val_network.get_di_entry_internal_links()[self._id_que[0]].\
		get_id_head_intersection_node()].get_type_intersection(),\
		val_veh_current_queue_location=self._id_que,\
		val_id_event_link= self._id_que[0],\
		val_current_achieved_queue_service_rate_including_current_vehicle=\
		val_network.get_di_entry_internal_links()[self._id_que[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[self._id_que[0],self._id_que[1]].get_current_reached_service_rate(),\
		val_current_queue_service_rate=\
		val_network.get_di_entry_internal_links()[self._id_que[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[self._id_que[0],self._id_que[1]].get_current_queue_service_rate(),\
		val_nb_depart_veh_within_ev_end_veh_hold_at_que=nb_and_t_dep_veh[0])
		
		#we record the event in the db 
		record_db_obj.fct_write_object_in_db_file()
	
			
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
		
