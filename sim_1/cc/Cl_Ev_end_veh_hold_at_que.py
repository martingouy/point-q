import string
import Cl_Event
import List_Explicit_Values
import Cl_Global_Functions
import Global_Functions
import Cl_Decisions
import Cl_Vehicle
import Cl_Record_Database
import Cl_Vehicle_Queue



class Ev_end_veh_hold_at_que(Cl_Event.Event):

	""" class defining the event of  the end of veh hold at queue"""
	
	def __init__(self,val_event_t=-1,val_id_que=-1):
	
		gl_funct_obj=Cl_Global_Functions.Global_Functions()
		
		Cl_Event.Event.__init__(self,val_event_time=val_event_t,val_event_type=Cl_Event.TYPE_EV["ty_ev_end_veh_hold_at_que"],\
		val_global_fct_obj=gl_funct_obj)
		
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
	
	#method treating the event
	
	def event_treat(self,val_netwrk=None,val_time_unit=None,val_min_hold_time=-1,\
	val_fct_calcul_nb_and_t_dep_veh=None,\
	val_round_prec=None,\
	val_ev_list=[],file_recording_event_db=None):
	
		
		
		#the number of vehicles to be examined if the can leave according to the sat flow,  employed in a micro management
		#va_vect_nb_veh_to_exam=Global_Functions.fct_defin_nb_veh_leave_mi(\
		#v_sat_flow=\
		#val_netwrk.get_di_entry_internal_links()[self._id_que[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		#[self._id_que[0],self._id_que[1]].get_sat_flow_queue(),\
		#v_t_unit=val_time_unit,v_round_prec=val_round_prec)

	
		#if the que is RT
		if val_netwrk.get_di_entry_internal_links()[self._id_que[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[self._id_que[0],self._id_que[1]].get_type_veh_queue()==Cl_Vehicle_Queue.TYPE_VEHICLE_QUEUE["right_turn"]:
			
						
			#t_end_control=round(val_netwrk.get_current_network_control_obj().get_t_start_control()+\
			#val_netwrk.get_current_network_control_obj().get_t_duration_control(),val_round_prec)
			
			#the time at which the new control will be applied to the network
			t_end_control=round(val_netwrk.get_di_intersections()[val_netwrk.get_di_entry_internal_links()[self._id_que[0]].\
			get_id_head_intersection_node()].\
			get_intersection_control_obj().get_t_end_control()+val_time_unit,val_round_prec)
					
			lis_par_fct_calcul_nb_and_t_dep_veh=[self._event_time,val_time_unit,\
			val_netwrk.get_di_entry_internal_links()[self._id_que[0]].get_set_veh_queue().\
			get_di_obj_veh_queue_at_link()[self._id_que[0],self._id_que[1]],\
			val_min_hold_time,t_end_control,val_netwrk,val_round_prec]
				 
				
			nb_veh_to_go=self._global_fct_obj.fct_treat_case_veh_can_go(\
			t_current=self._event_time,t_unit=val_time_unit,\
			fct_calcul_nb_and_t_dep_veh=val_fct_calcul_nb_and_t_dep_veh,\
			li_param_fct_calcul_nb_and_t_dep_veh=lis_par_fct_calcul_nb_and_t_dep_veh,\
			id_que=[self._id_que[0],self._id_que[1]],val_netw=val_netwrk,val_t_round_prec=val_round_prec,ev_list=val_ev_list)
			
			#if self._event_time==449.1 and self._id_que==[27,7]:
				#print(nb_veh_to_go)
				#import sys
				#sys.exit()
						
	
		#if the que is not a RT
		else:
			
			#print("HERE",val_netwrk.get_di_intersection_controls()[
			#val_netwrk.get_di_entry_internal_links()[self._id_que[0]].get_id_head_intersection_node()].\
			#get_di_intersection_control_mat()[self._id_que[0],self._id_que[1]])
			#import sys
			#sys.exit()
			#if the current control permits movement (= one)
			#print("CL EV END VEH HOL ID QUE",self._id_que)
			#print("id nd",val_netwrk.get_di_entry_internal_links()[self._id_que[0]].get_id_head_intersection_node())
			#print(val_netwrk.get_di_intersections()[val_netwrk.get_di_entry_internal_links()[self._id_que[0]].get_id_head_intersection_node()].\
			#get_intersection_control_obj().get_di_intersection_control_mat().keys())
			if val_netwrk.get_di_intersections()[val_netwrk.get_di_entry_internal_links()[self._id_que[0]].get_id_head_intersection_node()].\
			get_intersection_control_obj().get_di_intersection_control_mat()\
			[self._id_que[0],self._id_que[1]]==List_Explicit_Values.initialisation_value_to_one:
			
					
				#this is the 1st moment at which a new control will be applied
				#the time at which the new control will be applied to the network
				t_end_control=round(val_netwrk.get_di_intersections()[val_netwrk.get_di_entry_internal_links()[self._id_que[0]].\
				get_id_head_intersection_node()].get_intersection_control_obj().\
				get_t_end_control()+val_time_unit,val_round_prec)
								
				lis_par_fct_calcul_nb_and_t_dep_veh=[self._event_time,val_time_unit,\
				val_netwrk.get_di_entry_internal_links()[self._id_que[0]].get_set_veh_queue().\
				get_di_obj_veh_queue_at_link()[self._id_que[0],self._id_que[1]],\
				val_min_hold_time,t_end_control,val_netwrk,val_round_prec]
				
				
				nb_veh_to_go=self._global_fct_obj.fct_treat_case_veh_can_go(\
				t_current=self._event_time,t_unit=val_time_unit,\
				fct_calcul_nb_and_t_dep_veh=val_fct_calcul_nb_and_t_dep_veh,\
				li_param_fct_calcul_nb_and_t_dep_veh=lis_par_fct_calcul_nb_and_t_dep_veh,\
				id_que=[self._id_que[0],self._id_que[1]],val_netw=val_netwrk,val_t_round_prec=val_round_prec,ev_list=val_ev_list)
				
				
			else:
				nb_veh_to_go=0
		
		#if self._event_time==449.1 and  self._id_que==[6,7]:
			#print("IN THE EVENT",nb_veh_to_go)
			#import sys
			#sys.exit()
		
		record_db_obj=Cl_Record_Database.Record_Database(val_file_db=file_recording_event_db,\
		val_ev_time=self._event_time,val_ev_type=self._event_type,\
		val_type_inters_node=val_netwrk.get_di_intersections()[val_netwrk.get_di_entry_internal_links()[self._id_que[0]].\
		get_id_head_intersection_node()].get_type_intersection(),\
		val_t_start_current_inters_control=val_netwrk.get_di_intersections()[val_netwrk.get_di_entry_internal_links()[self._id_que[0]].\
		get_id_head_intersection_node()].get_intersection_control_obj().get_t_start_control(),\
		val_duration_current_inters_control=val_netwrk.get_di_intersections()[val_netwrk.get_di_entry_internal_links()[self._id_que[0]].\
		get_id_head_intersection_node()].get_intersection_control_obj().get_duration_control(),\
		val_current_inters_matrix_with_the_associated_link_of_phase=\
		val_netwrk.get_di_intersections()[val_netwrk.get_di_entry_internal_links()[self._id_que[0]].\
		get_id_head_intersection_node()].get_intersection_control_obj().get_di_intersection_control_mat(),\
		val_duration_current_cycle=val_netwrk.get_di_intersections()[val_netwrk.get_di_entry_internal_links()[self._id_que[0]].\
		get_id_head_intersection_node()].get_intersection_control_obj().get_cycle_duration_associated_with_control(),\
		val_veh_current_queue_location=self._id_que,\
		val_id_event_link= self._id_que[0],\
		val_current_achieved_queue_service_rate_including_current_vehicle=\
		val_netwrk.get_di_entry_internal_links()[self._id_que[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[self._id_que[0],self._id_que[1]].get_current_reached_service_rate(),\
		val_current_queue_service_rate=\
		val_netwrk.get_di_entry_internal_links()[self._id_que[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[self._id_que[0],self._id_que[1]].get_current_queue_service_rate(),\
		val_nb_depart_veh_within_ev_end_veh_hold_at_que=nb_veh_to_go)
		
		
		
		
		#we record the event in the db 
		record_db_obj.fct_write_object_in_db_file()



#*****************************************************************************************************************************************************************************************
	