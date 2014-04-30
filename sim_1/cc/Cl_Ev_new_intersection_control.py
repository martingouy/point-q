import csv
import string
import os
import sys
import itertools
import datetime
from datetime import *
import time
from time import *
import Cl_Event
import List_Explicit_Values
import Cl_Vehicle
import Cl_Decisions
import Cl_Intersection_Control
import Cl_Control_Actuate
#import Cl_Ev_end_veh_departure_from_queue_link
import Cl_Record_Database
import Cl_Vehicle_Queue
import Cl_Global_Functions
import Global_Functions
import math


class Ev_new_intersection_control(Cl_Event.Event):

	def __init__(self,val_ev_time,val_id_intersection_node,val_intersection_control_obj):
	#,val_ctlr_category):
	
		#print("val_id_intersection_node",val_id_intersection_node)
		
		gl_funct_obj=Cl_Global_Functions.Global_Functions()
		decision_obj=Cl_Decisions.Decisions()
		
		Cl_Event.Event.__init__(self,val_event_time=val_ev_time,val_event_type=Cl_Event.TYPE_EV["type_ev_new_intersection_control"],\
		val_global_fct_obj=gl_funct_obj)
		
		#the id of the related intersection node
		self._id_intersection_node=val_id_intersection_node
		
		
		#the current intersection control object 
		self._intersection_control_obj=val_intersection_control_obj
		
		#the decision object
		self._decision_obj=decision_obj
	
		#varibale indicating the id of the event, for identifying which event to treat when many decisions are planned for the same time
		#FA with red clearance
		#self._id_event=val_id_event
		
		#variable indicating whether the employed control requires sensot monit or not
		#self._ctlr_category=val_ctlr_category
		
#*****************************************************************************************************************************************************************************************
	#method returning the id of the related intersection node
	def get_id_intersection_node(self):
		return self._id_intersection_node

#*****************************************************************************************************************************************************************************************
	#method returning the current intersection control object 
	def get_intersection_control_obj(self):
		return self._intersection_control_obj

#*****************************************************************************************************************************************************************************************
	#method returning the decision object
	def get_decision_obj(self):
		return self._decision_obj
#*****************************************************************************************************************************************************************************************
	#method retruning the event id
	#def get_id_event(self):
		#return self._id_event
#*****************************************************************************************************************************************************************************************
	#method returning the variable indicating whethet the employed cotrl is revises within flow variation or not
	#def get_ctlr_category(self):
		#return self._ctlr_category
#*****************************************************************************************************************************************************************************************
	#method modifying the id of the related intersection node
	def set_id_intersection_node(self,n_v):
		self._id_intersection_node=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the current intersection control object 
	def set_intersection_control_obj(self,n_v):
		self._intersection_control_obj=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the decision object
	def set_decision_obj(self,n_v):
		self._decision_obj=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the event id
	#def set_id_event(self,n_v):
		#self._id_event=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the variable indicating whethet the employed cotrl is revises within flow variation or not
	#def set_ctlr_category(self,n_v):
		#self._ctlr_category=n_v
#*****************************************************************************************************************************************************************************************



	#method  treating the event
	def event_treat_1(self,v_val_netwk,v_val_time_unit,v_val_fct_calcul_nb_and_t_dep_veh,v_val_min_hold_time_veh_in_que,v_val_round_prec,\
	v_file_recording_event_db,v_ev_li,val_t_start_sim):
		
		#print("self._event_time",self._event_time,"v_netwk.get_di_intersections()[self._id_intersection_node].get_li_t_start_new_inters_control()[0]",\
		#v_netwk.get_di_intersections()[self._id_intersection_node].get_li_t_start_new_inters_control()[0])
		#if the event time is the time of the first element of the t _list
		#print()
		#print("IN CL NEW CTRL, id node: ",self._id_intersection_node,",id event: ",self._id_event,\
		#",nb _events corresp at this time:",\
		#v_val_netwk.get_di_intersections()[self._id_intersection_node].get_li_nb_ev_new_inters_ctrl_associated_with_li_t_start_new_inters_ctrl()[0],\
		#",new inters ctrl event time:",self._event_time,",t_list_planned:",\
		#v_val_netwk.get_di_intersections()[self._id_intersection_node].get_li_t_start_new_inters_control())
		
		#if we have not already treated the right event
		if v_val_netwk.get_di_intersections()[self._id_intersection_node].get_li_t_start_new_inters_control()!=[]:
		
			#if the event time is = the time of the first element of the t _list
			if self._event_time==v_val_netwk.get_di_intersections()[self._id_intersection_node].get_li_t_start_new_inters_control()[0]:
			
				#if  self._id_event>v_val_netwk.get_di_intersections()[self._id_intersection_node].get_li_nb_ev_new_inters_ctrl_associated_with_li_t_start_new_inters_ctrl()[0]:
					#print("PROB 1IN CL EN NEW CTRL, ID EVENT: ",self._id_event,"NB EV CORRESP:",v_val_netwk.get_di_intersections()[self._id_intersection_node].get_li_nb_ev_new_inters_ctrl_associated_with_li_t_start_new_inters_ctrl()[0])
					#import sys
					#sys.exit()
			
				#if the event id is the number of the events corresponding at the nb of events of the first planned ctrl , we treat the event
				if self._id_event==v_val_netwk.get_di_intersections()[self._id_intersection_node].get_li_nb_ev_new_inters_ctrl_associated_with_li_t_start_new_inters_ctrl()[0]:
			
					self.fct_event_treat(val_netwk=v_val_netwk,val_time_unit=v_val_time_unit,val_fct_calcul_nb_and_t_dep_veh=v_val_fct_calcul_nb_and_t_dep_veh,\
					val_min_hold_time_veh_in_que=v_val_min_hold_time_veh_in_que,val_round_prec=v_val_round_prec,file_recording_event_db=v_file_recording_event_db,\
					ev_li=v_ev_li)

					#we delete the first time in the list of time
					v_val_netwk.get_di_intersections()[self._id_intersection_node].get_li_t_start_new_inters_control().remove(\
					v_val_netwk.get_di_intersections()[self._id_intersection_node].get_li_t_start_new_inters_control()[0])
							
			#if the event time is > the time of the first element of the t _list
			elif self._event_time>v_val_netwk.get_di_intersections()[self._id_intersection_node].get_li_t_start_new_inters_control()[0]:
				print("PROBLEM  IN CL_E NEW_INTERS CTRL, fct event_treat, t_current ", self._event_time, "t first time in list t_events",\
				v_val_netwk.get_di_intersections()[self._id_intersection_node].get_li_t_start_new_inters_control()[0],\
				"type current ctrl: ",v_val_netwk.get_di_intersections()[self._id_intersection_node].get_intersection_control_obj().get_type_control(),\
				"id node",self._id_intersection_node)
				import sys
				sys.exit()
			#if the event time < of the first element of the t_list
			#else:
				#print("PROBLEM IN CL_E NEW_INTERS CTRL, event_treat, t_current ", self._event_time, "t first time in list t_events",\
				#v_val_netwk.get_di_intersections()[self._id_intersection_node].get_li_t_start_new_inters_control()[0],\
				#"type ctrl: ",v_val_netwk.get_di_intersections()[self._id_intersection_node].get_intersection_control_obj().get_type_control())
				
				#import sys
				#sys.exit()
	
	
	#*****************************************************************************************************************************************************************************************

	#method  treating the event
	def event_treat(self,val_network,val_time_unit,val_fct_calcul_nb_and_t_dep_veh,val_min_hold_time_veh_in_que,val_round_prec,\
	val_file_recording_event_db,val_ev_li,val_t_start_sim):
		

		#we attribute the intersection control object to the related intersection
		val_network.get_di_intersections()[self._id_intersection_node].set_intersection_control_obj(self._intersection_control_obj)
		
		
		#if the control is  not red clearance
		if self._intersection_control_obj.get_type_control()!=Cl_Control_Actuate.TYPE_CONTROL[0]:
		
			#for each input link to the intersection
			for i in val_network.get_di_intersections()[self._id_intersection_node].get_li_id_input_network_links_to_inters_node():
				
				#for each phase related to the input link
				for j in val_network.get_di_entry_internal_links()[i].get_set_veh_queue().get_di_obj_veh_queue_at_link():
					
					#if the queue is associated with a right turn
					if val_network.get_di_entry_internal_links()[i].get_set_veh_queue().get_di_obj_veh_queue_at_link()[j].get_type_veh_queue()==\
					Cl_Vehicle_Queue.TYPE_VEHICLE_QUEUE["right_turn"]:
						
						#we calculate the max number of departing vehicles
						max_nb_dep_veh=self._decision_obj.fct_calcul_period_service_rate_que(val_sat_flow_queue=\
						val_network.get_di_entry_internal_links()[i].get_set_veh_queue().get_di_obj_veh_queue_at_link()[j].\
						get_sat_flow_queue(),\
						val_act_duration_que=self._intersection_control_obj.get_duration_control(),val_t_unit=val_time_unit)
		
						#we associate it  as current service rate of the queue
						val_network.get_di_entry_internal_links()[i].get_set_veh_queue().get_di_obj_veh_queue_at_link()[j].\
						set_current_queue_service_rate(max_nb_dep_veh)
				
						#we initialize the currently reached service rate of the queue at zero
						val_network.get_di_entry_internal_links()[i].get_set_veh_queue().get_di_obj_veh_queue_at_link()[j].\
						set_current_reached_service_rate(List_Explicit_Values.initialisation_value_to_zero)
				
						#the number of vehicles that can leave the queue according to the saturation flow
						#va_vect_nb_veh_to_exam=Global_Functions.fct_defin_nb_veh_leave_mi(\
						#v_sat_flow=\
						#val_network.get_di_entry_internal_links()[i].get_set_veh_queue().get_di_obj_veh_queue_at_link()[j].\
						#get_sat_flow_queue(),\
						#v_t_unit=val_time_unit,v_round_prec=val_round_prec)

						#the time at which the new control is applied
						t_end_control=self._intersection_control_obj.get_t_end_control()+val_time_unit
						
						li_par_fct_calcul_nb_and_t_dep_veh=[self._event_time,val_time_unit,\
						val_network.get_di_entry_internal_links()[i].get_set_veh_queue().get_di_obj_veh_queue_at_link()[j],\
						val_min_hold_time_veh_in_que,t_end_control,val_network,val_round_prec]
					
					
						self._global_fct_obj.fct_treat_case_veh_can_go(\
						t_current=self._event_time,t_unit=val_time_unit,\
						fct_calcul_nb_and_t_dep_veh=val_fct_calcul_nb_and_t_dep_veh,\
						li_param_fct_calcul_nb_and_t_dep_veh=li_par_fct_calcul_nb_and_t_dep_veh,\
						id_que=j,val_netw=val_network,val_t_round_prec=val_round_prec,ev_list=val_ev_li)
						
					#if the queue is not associated with a right turn
					else:
						#if the control actuates the phase related to the que,
						#print("j",j)
						#print()
						#print(self._intersection_control_obj.get_di_intersection_control_mat())
						if self._intersection_control_obj.get_di_intersection_control_mat()[j]==1:
							
							#we calculate the max number of departing vehicles
							max_nb_dep_veh=self._decision_obj.fct_calcul_period_service_rate_que(val_sat_flow_queue=\
							val_network.get_di_entry_internal_links()[i].get_set_veh_queue().get_di_obj_veh_queue_at_link()[j].\
							get_sat_flow_queue(),\
							val_act_duration_que=self._intersection_control_obj.get_duration_control(),val_t_unit=val_time_unit)
							
		
							#we associate it  as current service rate of the queue
							val_network.get_di_entry_internal_links()[i].get_set_veh_queue().get_di_obj_veh_queue_at_link()[j].\
							set_current_queue_service_rate(max_nb_dep_veh)
				
							#we initialize the currently reached service rate of the queue at zero
							val_network.get_di_entry_internal_links()[i].get_set_veh_queue().get_di_obj_veh_queue_at_link()[j].\
							set_current_reached_service_rate(List_Explicit_Values.initialisation_value_to_zero)
								
							#the time at which the new control is applied
							t_end_control=self._intersection_control_obj.get_t_end_control()+val_time_unit
								
							li_par_fct_calcul_nb_and_t_dep_veh=[self._event_time,val_time_unit,\
							val_network.get_di_entry_internal_links()[i].get_set_veh_queue().get_di_obj_veh_queue_at_link()[j],\
							val_min_hold_time_veh_in_que,t_end_control,val_network,val_round_prec]

							self._global_fct_obj.fct_treat_case_veh_can_go(\
							t_current=self._event_time,t_unit=val_time_unit,\
							fct_calcul_nb_and_t_dep_veh=val_fct_calcul_nb_and_t_dep_veh,\
							li_param_fct_calcul_nb_and_t_dep_veh=li_par_fct_calcul_nb_and_t_dep_veh,\
							id_que=j,val_netw=val_network,val_t_round_prec=val_round_prec,ev_list=val_ev_li)

	
		#if the control is  red clearance we let veh from RT to go
		else:
			#for each input link to the intersection
			for i in val_network.get_di_intersections()[self._id_intersection_node].get_li_id_input_network_links_to_inters_node():
			
				#for each phase related to the input link
				for j in val_network.get_di_entry_internal_links()[i].get_set_veh_queue().get_di_obj_veh_queue_at_link():
				
					#if the queue is associated with a right turn
					if val_network.get_di_entry_internal_links()[i].get_set_veh_queue().get_di_obj_veh_queue_at_link()[j].get_type_veh_queue()==\
					Cl_Vehicle_Queue.TYPE_VEHICLE_QUEUE["right_turn"]:

						#we calculate the max number of departing vehicles
						max_nb_dep_veh=self._decision_obj.fct_calcul_period_service_rate_que(val_sat_flow_queue=\
						val_network.get_di_entry_internal_links()[i].get_set_veh_queue().get_di_obj_veh_queue_at_link()[j].\
						get_sat_flow_queue(),\
						val_act_duration_que=self._intersection_control_obj.get_duration_control(),val_t_unit=val_time_unit)
		
						#we associate it  as current service rate of the queue
						val_network.get_di_entry_internal_links()[i].get_set_veh_queue().get_di_obj_veh_queue_at_link()[j].\
						set_current_queue_service_rate(max_nb_dep_veh)
				
						#we initialize the currently reached service rate of the queue at zero
						val_network.get_di_entry_internal_links()[i].get_set_veh_queue().get_di_obj_veh_queue_at_link()[j].\
						set_current_reached_service_rate(List_Explicit_Values.initialisation_value_to_zero)

						#the time at which the new control is applied
						t_end_control=self._intersection_control_obj.get_t_end_control()+val_time_unit
					
						li_par_fct_calcul_nb_and_t_dep_veh=[self._event_time,val_time_unit,\
						val_network.get_di_entry_internal_links()[i].get_set_veh_queue().get_di_obj_veh_queue_at_link()[j],\
						val_min_hold_time_veh_in_que,t_end_control,val_network,val_round_prec]
					
					
						self._global_fct_obj.fct_treat_case_veh_can_go(\
						t_current=self._event_time,t_unit=val_time_unit,\
						fct_calcul_nb_and_t_dep_veh=val_fct_calcul_nb_and_t_dep_veh,\
						li_param_fct_calcul_nb_and_t_dep_veh=li_par_fct_calcul_nb_and_t_dep_veh,\
						id_que=j,val_netw=val_network,val_t_round_prec=val_round_prec,ev_list=val_ev_li)
			
		
		#we create a record object
		record_db_obj=Cl_Record_Database.Record_Database(\
		val_file_db=val_file_recording_event_db,\
		val_ev_time=self._event_time,\
		val_ev_type=self._event_type,\
		val_id_inters_node=self._id_intersection_node,\
		val_t_start_current_inters_control=self._intersection_control_obj.get_t_start_control(),\
		val_duration_current_inters_control=self._intersection_control_obj.get_duration_control(),\
		val_current_inters_control_matrix=self._intersection_control_obj.get_di_intersection_control_mat(),\
		val_duration_current_cycle=self._intersection_control_obj.get_cycle_duration_associated_with_control(),\
		val_t_end_current_intersection_control=self._intersection_control_obj.get_t_end_control(),\
		val_id_actuated_stage=self._intersection_control_obj.get_id_actuated_stage())
		#,\
		#val_type_control=type_control)
		#,\
		#val_type_control=self._intersection_control_obj.get_type_control())

		
		#we record the event in the db 
		record_db_obj.fct_write_object_in_db_file()								
							
	
											  
																													  
																													  
																													  
																													  
																													
																													  
										
	
																													  
			
			















