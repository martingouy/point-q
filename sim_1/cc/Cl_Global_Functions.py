import heapq
from heapq import * 
import List_Explicit_Values
import Cl_Ev_end_veh_departure_from_que
import Cl_Ev_end_veh_hold_at_que
import Cl_Vehicle_Queue
import Cl_Network_Link
import Cl_Vehicle
import Cl_Network
import Cl_Decisions
import pickle
import math


class Global_Functions:

	def __init__(self):
		
		self._decision_obj=Cl_Decisions.Decisions()
		
#*****************************************************************************************************************************************************************************************
	#method returning the decision object
	def get_decision_obj(self):
		return self._decision_obj

#*****************************************************************************************************************************************************************************************
	#method modifying the decision object
	def set_desicion_obj(self,n_v):
		self._decision_obj=n_v

#*****************************************************************************************************************************************************************************************
	#method returning [the number of vehicles that can depart from a que, the associated dep time, \
	#total_potential_nb_dep_veh], 
	#(the service rate- currently reached service rate)
	#v_vect_nb_veh_to_exam=[nb veh permitted to go ny the sat flow, t_req] we use it for micro
	#AJOUTER LE NB DE PLACES DISPONIBLES
	def fct_calcul_nb_veh_they_can_leave_at_t_current_and_assoc_end_dep_time_ma(self,t_cur,t_unit,queue,min_veh_hold_time_in_que,\
	t_end_current_control,v_vect_nb_veh_to_exam,v_round_prec=1):

		
			
		#the potential number of vehicles that can leave que
		total_potential_nb_dep_veh= queue.get_current_queue_service_rate() - queue.get_current_reached_service_rate()
		#print("total_potential_nb_dep_veh",total_potential_nb_dep_veh)
		
		#the number of vehicles which have remained in the que for at least the min hold time and for which there is no planned dep
		nb_veh_have_rem_que_hold_time_without_plan_dep=\
		queue.fct_calcul_nb_of_veh_have_remained_in_que_at_least_for_min_hold_time_without_planned_dep(\
		t_current=t_cur,\
		min_hold_time=min_veh_hold_time_in_que,li_vehicles=queue.get_queue_veh()[:total_potential_nb_dep_veh],\
		val_precision=v_round_prec)
		#print("nb_veh_have_rem_que_hold_time_without_plan_dep",nb_veh_have_rem_que_hold_time_without_plan_dep)
			
			
		
		#the time left until the end of the current control +1 (t_end_current_control= the first second at which the new control is applied)
		t_left=round(t_end_current_control - t_cur,v_round_prec)
		#print("t_left",t_left)
		
		
		#the number of vehicles that can leave within t_left seconds
		#nb_veh_can_leave_during_t_left=math.ceil(queue.get_sat_flow_queue() * t_left/t_unit )
		nb_veh_can_leave_during_t_left=round(queue.get_sat_flow_queue() * t_left/t_unit )
		#print("nb_veh_can_leave_during_t_left",nb_veh_can_leave_during_t_left)
		
		
		#print("t_cur",t_cur,"nb_veh_have_rem_que_hold_time,",nb_veh_have_rem_que_hold_time,"nb_veh_can_leave_during_t_left",\
		#nb_veh_can_leave_during_t_left)
		#the number of veh that will leave
		nb_veh_leave=min(nb_veh_have_rem_que_hold_time_without_plan_dep,nb_veh_can_leave_during_t_left)
		#print("nb_veh_leave",nb_veh_leave)
		
		t_req=round(nb_veh_leave*t_unit/queue.get_sat_flow_queue(),v_round_prec)
		if t_req>t_left:
			t_req=t_left
		#print("t_req",t_req)
		
		
		#if t_req >t_left:
			#print("PROBLEM IN CL_GLOBAL_FUNCTIONS, IN fct_calcul_nb_veh_they_can_leave_at_t_current_and_assoc_end_dep_time_ma,\
			# t_req:", t_req,"t_left",t_left)
			#import sys
			#sys.exit()
		#print("t_cur",t_cur,"t_req",t_req,t_cur+t_req,nb_veh_leave/queue.get_sat_flow_queue())	
		
		#print("nb_veh_leave",nb_veh_leave,"t_cur",t_cur,"t_req",t_req)
		#return [nb_veh_leave,t_cur+t_req]
		t_ev_end_veh_dep=round(t_cur+t_req,v_round_prec)
		
		#if t_cur==98.3 and queue.get_associated_phase_to_queue()[0]==2 and queue.get_associated_phase_to_queue()[1]==3:
			#print("nb_veh_leave",nb_veh_leave,"t_ev_end_veh_dep",t_ev_end_veh_dep,"t_req",t_req,"t_cur+t_req",t_cur+t_req,"v_round_prec",v_round_prec)
			#import sys
			#sys.exit()
		return [nb_veh_leave,t_ev_end_veh_dep,total_potential_nb_dep_veh]

#*****************************************************************************************************************************************************************************************
	#method returning the nb of vehicles that can leave from a queue in case where prior-minor phases are not considered,
	#in case of infinite capacity of the destination link
	#THE REMAINING TIME BEFORE THE COTNROL CHANGE IS NOT A CONSTRAINT IN THIS CASE
	def fct_calcul_nb_veh_they_can_leave_at_t_current_and_assoc_end_dep_time_mi_without_permis_prior_mv_infinite_lk_cap_1(self,\
	 va_t_end_current_control,va_t_cur,va_t_unit,\
	 va_queue,va_min_veh_hold_time_in_que,va_t_round_prec):
		
	 
		#the potential number of vehicles that can leave que from the service rate
		total_potential_nb_dep_veh= va_queue.get_current_queue_service_rate() - va_queue.get_current_reached_service_rate()
				
			
		total_potential_nb_dep_veh_1=min(total_potential_nb_dep_veh,va_queue.get_nb_veh_cal_leave_simult_que_from_sat_flow())
		
		#print("total_potential_nb_dep_veh_1",total_potential_nb_dep_veh_1)
		
		#the number of vehicles which have remained in the que for at least the min hold time without having a veh dep event planned
		nb_veh_have_rem_que_hold_time_without_plan_dep=\
		va_queue.fct_calcul_nb_of_n_veh_remained_in_que_for_min_t_hold_without_planned_dep_for_mi(t_current=va_t_cur,\
		min_hold_time=va_min_veh_hold_time_in_que,li_vehicles=va_queue.get_queue_veh()[:total_potential_nb_dep_veh_1],\
		nb_veh_to_exam=total_potential_nb_dep_veh_1,val_t_precision=va_t_round_prec)
		
		#print("nb_veh_have_rem_que_hold_time_without_plan_dep",nb_veh_have_rem_que_hold_time_without_plan_dep)
		
			
		#if there exist vehicles which have remained the min time in the queue and can leave simult
		if nb_veh_have_rem_que_hold_time_without_plan_dep>List_Explicit_Values.initialisation_value_to_zero:
		
			#the time left until the end of the current control +t_unit (t_end_current_control= the first moment, time unit, at which the new control is applied)
			#va_t_end_current_control=time at which the new control is going to start
			t_left=round(va_t_end_current_control - va_t_cur,va_t_round_prec) 
			#print("t_left",t_left,"t_req",va_queue.get_required_depart_time_que(),"va_t_end_current_control",va_t_end_current_control,"va_t_cur,",va_t_cur)
			
			if t_left<0:
				print("PROBLEM IN CL_GL_FCT, Fct_calcul_nb_veh_they_can_leave_at_t_current_and_assoc_end_dep_time_mi_without_permis_prior_mv_infinite_lk_cap, t_left",\
				t_left,"t_req",va_queue.get_required_depart_time_que(),"va_t_end_current_control",va_t_end_current_control,"va_t_cur,",va_t_cur)
				print("que",va_queue.get_id_associated_link(),va_queue.get_id_associated_output_link())
				import sys
				sys.exit()
			
			#If the required time > t_left
			if t_left< va_queue.get_required_depart_time_que():
			
				#veh_will_leave=self._decision_obj.\
				#fct_dec_whether_veh_depart_by_end_ctrl_act(val_t_remain=t_left,val_t_required=va_queue.get_required_depart_time_que(),a=0,b=1)
				veh_will_leave=List_Explicit_Values.initialisation_value_to_one
				
				if veh_will_leave==List_Explicit_Values.initialisation_value_to_one:
				
					nb_veh_leave=nb_veh_have_rem_que_hold_time_without_plan_dep
					
					
					#t_ev_end_veh_dep=round(va_t_cur+t_left,va_t_round_prec)
					#t_ev_end_veh_dep=math.floor((va_t_cur+t_left)*100)/100
					#t_ev_end_veh_dep=math.floor((va_t_cur+t_left)*10)/10
					
					t_ev_end_veh_dep=self._decision_obj.fct_def_time_end_veh_depart(\
					val_t_current=va_t_cur, val_duration=t_left,val_t_round=va_t_round_prec,val_decimal_digit_prec=10,val_probab=0,a=0,b=1)
					
					if t_ev_end_veh_dep==va_t_cur:
						print("ATTENTION IN CL_GLOB_FCT,\
						fct_calcul_nb_veh_they_can_leave_at_t_current_and_assoc_end_dep_time_mi_without_permis_prior_mv_infinite_lk_cap",\
						"t_cur",va_t_cur,"duree traj",t_left,"t_ev_end_veh_dep",t_ev_end_veh_dep)
				
				else:
					nb_veh_leave=List_Explicit_Values.initialisation_value_to_zero
					t_ev_end_veh_dep=None
					
			
			#if required time <= t_left
			else:
				nb_veh_leave=nb_veh_have_rem_que_hold_time_without_plan_dep
				
				
				#t_ev_end_veh_dep=round(va_t_cur+va_queue.get_required_depart_time_que(),va_t_round_prec)
				#duree_init=va_t_cur+va_queue.get_required_depart_time_que()
				#duree_init_multipliee=duree_init*100
				#chiffres decimaux
				#partie_entiere=math.floor(duree_init_multipliee)
				#partie_decimale=duree_init_multipliee-partie_entiere
				#if no decimals
				#if partie_decimale==0:
					#t_ev_end_veh_dep=duree_init
						
				#if  decimals
				#else:
					#t_ev_end_veh_dep=(duree_init_multipliee//1)/100
				#t_ev_end_veh_dep=math.floor((va_t_cur+va_queue.get_required_depart_time_que())*100)/100
				#t_ev_end_veh_dep=math.floor((va_t_cur+va_queue.get_required_depart_time_que())*10)/10
				
				t_ev_end_veh_dep=self._decision_obj.fct_def_time_end_veh_depart(\
				val_t_current=va_t_cur, val_duration=va_queue.get_required_depart_time_que(),\
				val_t_round=va_t_round_prec,val_decimal_digit_prec=10,val_probab=0,a=0,b=1)
				
				#print("va_queue.get_required_depart_time_que()",va_queue.get_required_depart_time_que())
				#print()
				#print("t_ev_end_veh_dep",t_ev_end_veh_dep,"t_cur",va_t_cur)
					
				if t_ev_end_veh_dep==va_t_cur:
					print("ATTENTION IN CL_GLOB_FCT,\
					fct_calcul_nb_veh_they_can_leave_at_t_current_and_assoc_end_dep_time_mi_without_permis_prior_mv_infinite_lk_cap",\
					"t_cur",va_t_cur,"duree traj",va_queue.get_required_depart_time_que(),"t_ev_end_veh_dep",t_ev_end_veh_dep)

		
		#if va_queue.get_associated_phase_to_queue()[0]==4 and va_queue.get_associated_phase_to_queue()[1]==5:
			#print("t_ev_end_veh_dep",t_ev_end_veh_dep)
			#import sys
			#sys.exit()
		#if no vehicle  has remained the min time in the queue
		else:
			nb_veh_leave=List_Explicit_Values.initialisation_value_to_zero
				
			#time at which the veh departure will be completed= value non defined
			t_ev_end_veh_dep=None
			
		#we indicate that the dest lk is not saturated
		state_destin_link=List_Explicit_Values.initialisation_value_to_zero
		
		#if nb_veh_leave>0 and va_queue.get_id_associated_link()==2 and va_queue.get_id_associated_output_link()==3:
		#if nb_veh_leave>0 :
			#print("va_t_cu",va_t_cur,"va_queue.get_required_depart_time_que()",va_queue.get_required_depart_time_que(),\
			#"t_ev_end_veh_dep",t_ev_end_veh_dep)
			#import sys
			#sys.exit()
		#if  va_queue.get_associated_phase_to_queue()[0]==1 and va_queue.get_associated_phase_to_queue()[1]==2:
			#print("nb_veh_leave,in fct",nb_veh_leave)
		return [nb_veh_leave,t_ev_end_veh_dep,total_potential_nb_dep_veh,state_destin_link]
#*****************************************************************************************************************************************************************************************
	#method returning the nb of vehicles that can leave from a queue in case where prior-minor phases are not considered,
	#in case of infinite capacity of the destination link
	#THE REMAINING TIME BEFORE THE COTNROL CHANGE IS NOT A CONSTRAINT IN THIS CASE
	def fct_calcul_nb_veh_they_can_leave_at_t_current_and_assoc_end_dep_time_mi_without_permis_prior_mv_infinite_lk_cap(self,\
	va_t_end_current_control,va_t_cur,va_t_unit,va_queue,va_min_veh_hold_time_in_que,va_t_round_prec):
		
		#the potential number of vehicles that can leave que from the service rate
		total_potential_nb_dep_veh= va_queue.get_current_queue_service_rate() - va_queue.get_current_reached_service_rate()

		#if vehicles can leave from the service rate
		if total_potential_nb_dep_veh>0:
	 
		
			#if  the veh has satisfied the hold constraint
			if va_queue.fct_calcul_first_veh_remained_in_que_for_min_t_hold_without_planned_dep_for_mi(t_current=va_t_cur,min_hold_time=va_min_veh_hold_time_in_que,li_vehicles=va_queue.get_queue_veh(),val_t_precision=va_t_round_prec)>List_Explicit_Values.initialisation_value_to_zero:
			
			
		
				#the time left until the end of the current control +t_unit (t_end_current_control= the first moment, time unit, at which the new control is applied)
				#va_t_end_current_control=time at which the new control is going to start
				t_left=round(va_t_end_current_control - va_t_cur,va_t_round_prec) 
			
			
				if t_left<0:
					print("PROBLEM IN CL_GL_FCT, Fct_calcul_nb_veh_they_can_leave_at_t_current_and_assoc_end_dep_time_mi_without_permis_prior_mv_infinite_lk_cap, t_left",\
					t_left,"t_req",va_queue.get_required_depart_time_que(),"va_t_end_current_control",va_t_end_current_control,"va_t_cur,",va_t_cur)
					print("que",va_queue.get_id_associated_link(),va_queue.get_id_associated_output_link())
					import sys
					sys.exit()
				
				else:
			
					#calcul of the required depart time
					#if a que sat flow corresponds to the vehicle 
					if va_queue.get_queue_veh()[0].get_veh_sat_flow_when_current_que_locat_affected()!=None:
				
						t_req_dep=va_queue.fct_defining_t_req_for_single_veh_depart(val_t_unit=va_t_unit,\
						val_sat_flow=va_queue.get_queue_veh()[0].get_veh_sat_flow_when_current_que_locat_affected(),val_dec_digits=10)
					
					#if no queue sat flow correspds to the vehicle 
					else:
				
						t_req_dep=va_queue.get_required_depart_time_que()
					
					#If the required time > t_left
					if t_req_dep> t_left:
				
						nb_veh_leave=List_Explicit_Values.initialisation_value_to_one
					
						t_ev_end_veh_dep=self._decision_obj.fct_def_time_end_veh_depart(\
						val_t_current=va_t_cur, val_duration=t_left,val_t_round=va_t_round_prec,val_decimal_digit_prec=10,val_probab=0,a=0,b=1)
					
						if t_ev_end_veh_dep==va_t_cur:
							print("ATTENTION IN CL_GLOB_FCT,\
							fct_calcul_nb_veh_they_can_leave_at_t_current_and_assoc_end_dep_time_mi_without_permis_prior_mv_infinite_lk_cap",\
							"t_cur",va_t_cur,"duree traj",t_left,"t_ev_end_veh_dep",t_ev_end_veh_dep)
						
						state_destin_link=List_Explicit_Values.initialisation_value_to_zero
					
						return [nb_veh_leave,t_ev_end_veh_dep,total_potential_nb_dep_veh,state_destin_link]
				
					#if required time <= t_left
					else:
						nb_veh_leave=List_Explicit_Values.initialisation_value_to_one
					
						t_ev_end_veh_dep=self._decision_obj.fct_def_time_end_veh_depart(\
						val_t_current=va_t_cur, val_duration=t_req_dep,\
						val_t_round=va_t_round_prec,val_decimal_digit_prec=10,val_probab=0,a=0,b=1)
						
						
					
						if t_ev_end_veh_dep==va_t_cur:
							print("ATTENTION IN CL_GLOB_FCT,\
							fct_calcul_nb_veh_they_can_leave_at_t_current_and_assoc_end_dep_time_mi_without_permis_prior_mv_infinite_lk_cap",\
							"t_cur",va_t_cur,"duree traj",va_queue.get_required_depart_time_que(),"t_ev_end_veh_dep",t_ev_end_veh_dep)
					
						state_destin_link=List_Explicit_Values.initialisation_value_to_zero
					
						return [nb_veh_leave,t_ev_end_veh_dep,total_potential_nb_dep_veh,state_destin_link]
				
				
		
			#if  the veh has not satisfied the hold constraint
			else:
				nb_veh_leave=List_Explicit_Values.initialisation_value_to_zero
				t_ev_end_veh_dep=None
				state_destin_link=List_Explicit_Values.initialisation_value_to_zero
			
				return [nb_veh_leave,t_ev_end_veh_dep,total_potential_nb_dep_veh,state_destin_link]
	 
		#if vehicles cannot leave from the service rate
		else:
	 
			nb_veh_leave=List_Explicit_Values.initialisation_value_to_zero
				
			#time at which the veh departure will be completed= value non defined
			t_ev_end_veh_dep=None
			
			#we indicate that the dest lk is not saturated
			state_destin_link=List_Explicit_Values.initialisation_value_to_zero
		
			return [nb_veh_leave,t_ev_end_veh_dep,total_potential_nb_dep_veh,state_destin_link]
	 
	 
#*****************************************************************************************************************************************************************************************
	#method eturning the nb of vehicles that can leave from a queue in case where prior-minor phases are not considered,
	#in case of finite capacity of the destination link
	#IN THIS CASE THE CONSTRAINT OF THE TIME LEFT IS NOT TAKEN INTO CONSIDERATION
	def fct_calcul_nb_veh_they_can_leave_at_t_current_and_assoc_end_dep_time_mi_without_permis_prior_mv_finite_lk_cap(self,\
	va_t_end_current_control,va_t_cur,va_t_unit,va_netw,va_queue,va_min_veh_hold_time_in_que,va_t_round_prec):
	 

		nb_avail_places_dest_lk=\
		va_netw.get_di_entry_internal_links()[va_queue.get_id_associated_output_link()].get_capacity_link() - \
		va_netw.get_di_entry_internal_links()[va_queue.get_id_associated_output_link()].get_current_nb_veh_link()
		
		
		#If the dest link is not saturated
		if nb_avail_places_dest_lk>List_Explicit_Values.initialisation_value_to_zero:
			
			#the potential number of vehicles that can leave que from the service rate
			total_potential_nb_dep_veh=va_queue.get_current_queue_service_rate() - va_queue.get_current_reached_service_rate()
			
			#if vehicles can leave from the service rate
			if total_potential_nb_dep_veh>List_Explicit_Values.initialisation_value_to_zero:
			
				#if the first veh has satisfied the hold constraint
				if va_queue.fct_calcul_first_veh_remained_in_que_for_min_t_hold_without_planned_dep_for_mi(\
				t_current=va_t_cur,min_hold_time=va_min_veh_hold_time_in_que,li_vehicles=va_queue.get_queue_veh(),val_t_precision=va_t_round_prec)>\
				List_Explicit_Values.initialisation_value_to_zero:
				
					#the time left until the end of the current control +t_unit (t_end_current_control= the first moment, time unit, at which the new control is applied)
					#va_t_end_current_control=time at which the new control is going to start
					t_left=round(va_t_end_current_control - va_t_cur,va_t_round_prec) 
					
					
					if t_left<0:
						print("PROBLEM IN CL_GL_FCT, Fct_calcul_nb_veh_they_can_leave_at_t_current_and_assoc_end_dep_time_mi_without_permis_prior_mv_infinite_lk_cap, t_left",\
						t_left,"t_req",va_queue.get_required_depart_time_que(),"va_t_end_current_control",va_t_end_current_control,"va_t_cur,",va_t_cur)
						print("que",va_queue.get_id_associated_link(),va_queue.get_id_associated_output_link())
						import sys
						sys.exit()
						
					else:
						#calcul of the required depart time
						#if a que sat flow corresponds to the vehicle 
						if va_queue.get_queue_veh()[0].get_veh_sat_flow_when_current_que_locat_affected()!=None:
						
							t_req_dep=va_queue.fct_defining_t_req_for_single_veh_depart(val_t_unit=va_t_unit,\
							val_sat_flow=va_queue.get_queue_veh()[0].get_veh_sat_flow_when_current_que_locat_affected(),val_dec_digits=10)
							
							print("t_req_dep",t_req_dep)
							import sys
							sys.exit()
						
						#if no que sat flow corresponds to the vehicle 
						else:
							t_req_dep=va_queue.get_required_depart_time_que()
							
						#If the required time > t_left
						if t_req_dep> t_left:
						
							nb_veh_leave=List_Explicit_Values.initialisation_value_to_one
							
							t_ev_end_veh_dep=self._decision_obj.fct_def_time_end_veh_depart(\
							val_t_current=va_t_cur, val_duration=t_left,val_t_round=va_t_round_prec,val_decimal_digit_prec=10,val_probab=0,a=0,b=1)
							
							if t_ev_end_veh_dep==va_t_cur:
								print("ATTENTION IN CL_GLOB_FCT,\
								fct_calcul_nb_veh_they_can_leave_at_t_current_and_assoc_end_dep_time_mi_without_permis_prior_mv_finite_lk_cap",\
								"t_cur",va_t_cur,"duree traj",t_left,"t_ev_end_veh_dep",t_ev_end_veh_dep,"t_veh_dur=t_left=",t_left)
								
							state_destin_link=List_Explicit_Values.initialisation_value_to_zero
							
							return [nb_veh_leave,t_ev_end_veh_dep,total_potential_nb_dep_veh,state_destin_link]
						
						#If the required time <= t_left
						else:
						
							nb_veh_leave=List_Explicit_Values.initialisation_value_to_one
					
							t_ev_end_veh_dep=self._decision_obj.fct_def_time_end_veh_depart(\
							val_t_current=va_t_cur, val_duration=t_req_dep,\
							val_t_round=va_t_round_prec,val_decimal_digit_prec=10,val_probab=0,a=0,b=1)
						
							if t_ev_end_veh_dep==va_t_cur:
								print("ATTENTION IN CL_GLOB_FCT,\
								fct_calcul_nb_veh_they_can_leave_at_t_current_and_assoc_end_dep_time_mi_without_permis_prior_mv_finite_lk_cap",\
								"t_cur",va_t_cur,"duree traj",va_queue.get_required_depart_time_que(),"t_ev_end_veh_dep",t_ev_end_veh_dep,"t_veh_dur=t_left=",t_left)
				
				
							state_destin_link=List_Explicit_Values.initialisation_value_to_zero
							
							return [nb_veh_leave,t_ev_end_veh_dep,total_potential_nb_dep_veh,state_destin_link]
							
				#if the first veh has not satisfied the hold constraint
				else:
					nb_veh_leave=List_Explicit_Values.initialisation_value_to_zero
					t_ev_end_veh_dep=None
					state_destin_link=List_Explicit_Values.initialisation_value_to_zero
					
					return [nb_veh_leave,t_ev_end_veh_dep,total_potential_nb_dep_veh,state_destin_link]

			
			#if vehicles cannot leave from the service rate
			else:
			
				nb_veh_leave=List_Explicit_Values.initialisation_value_to_zero
				
				#time at which the veh departure will be completed= value non defined
				t_ev_end_veh_dep=None
				
				#we indicate that the dest lk is not saturated
				state_destin_link=List_Explicit_Values.initialisation_value_to_zero
				
				return [nb_veh_leave,t_ev_end_veh_dep,total_potential_nb_dep_veh,state_destin_link]
			
		#If the dest link is  saturated
		else:
		
			#the nb of departing veh
			nb_veh_leave=List_Explicit_Values.initialisation_value_to_zero
				
			#time at which the veh departure will be completed= value non defined
			t_ev_end_veh_dep=None
				
			total_potential_nb_dep_veh= va_queue.get_current_queue_service_rate() - va_queue.get_current_reached_service_rate()
				
			#we indicate that the dest lk is  saturated
			state_destin_link=List_Explicit_Values.initialisation_value_to_one
			
			return [nb_veh_leave,t_ev_end_veh_dep,total_potential_nb_dep_veh,state_destin_link]
				
#*****************************************************************************************************************************************************************************************
	#method returning the nb of vehicles that can leave from a queue in case where prior-minor phases are not considered,
	#in case of finite capacity of the destination link
	#IN THIS CASE THE CONSTRAINT OF THE TIME LEFT IS NOT TAKEN INTO CONSIDERATION
	def fct_calcul_nb_veh_they_can_leave_at_t_current_and_assoc_end_dep_time_mi_without_permis_prior_mv_finite_lk_cap_1(self,\
	 va_t_end_current_control,va_t_cur,va_t_unit,va_netw,\
	 va_queue,va_min_veh_hold_time_in_que,va_t_round_prec):
	 
		
		nb_avail_places_dest_lk=\
		va_netw.get_di_entry_internal_links()[va_queue.get_id_associated_output_link()].get_capacity_link() - \
		va_netw.get_di_entry_internal_links()[va_queue.get_id_associated_output_link()].get_current_nb_veh_link()
		
		
		
		#if the destination link is not saturated, then vehicles can move towards the destination link
		if nb_avail_places_dest_lk>0 :
		
			#the potential number of vehicles that can leave que from the service rate
			total_potential_nb_dep_veh= va_queue.get_current_queue_service_rate() - va_queue.get_current_reached_service_rate()
				
			total_potential_nb_dep_veh_1=min(total_potential_nb_dep_veh,va_queue.get_nb_veh_cal_leave_simult_que_from_sat_flow(),nb_avail_places_dest_lk)
			
			#the number of vehicles which have remained in the que for at least the min hold time without having a veh dep event planned
			nb_veh_have_rem_que_hold_time_without_plan_dep=\
			va_queue.fct_calcul_nb_of_n_veh_remained_in_que_for_min_t_hold_without_planned_dep_for_mi(t_current=va_t_cur,\
			min_hold_time=va_min_veh_hold_time_in_que,li_vehicles=va_queue.get_queue_veh()[:total_potential_nb_dep_veh_1],\
			nb_veh_to_exam=total_potential_nb_dep_veh_1,val_t_precision=va_t_round_prec)
			
			#if there exist vehicles which have remained the min time in the queue
			if nb_veh_have_rem_que_hold_time_without_plan_dep>List_Explicit_Values.initialisation_value_to_zero:
			
				#the time left until the end of the current control +t_unit (t_end_current_control= the first moment, time unit, at which the new control is applied)
				#va_t_end_current_control=time at which the new control is going to start
				t_left=round(va_t_end_current_control - va_t_cur,va_t_round_prec) 
				
				#If the required time > t_left
				if t_left< va_queue.get_required_depart_time_que():
				
					#veh_will_leave=self._decision_obj.\
					#fct_dec_whether_veh_depart_by_end_ctrl_act(val_t_remain=t_left,val_t_required=va_queue.get_required_depart_time_que(),a=0,b=1)
					veh_will_leave=List_Explicit_Values.initialisation_value_to_one
					
					if veh_will_leave==List_Explicit_Values.initialisation_value_to_one:
					
						nb_veh_leave=nb_veh_have_rem_que_hold_time_without_plan_dep
						#t_ev_end_veh_dep=math.floor((va_t_cur+t_left)*100)/100
						#t_ev_end_veh_dep=math.floor((va_t_cur+t_left)*10)/10
						
						t_ev_end_veh_dep=self._decision_obj.fct_def_time_end_veh_depart(\
						val_t_current=va_t_cur, val_duration=t_left,val_t_round=va_t_round_prec,val_decimal_digit_prec=10,val_probab=0,a=0,b=1)
						
						if t_ev_end_veh_dep==va_t_cur:
							print("ATTENTION IN CL_GLOB_FCT,\
							fct_calcul_nb_veh_they_can_leave_at_t_current_and_assoc_end_dep_time_mi_without_permis_prior_mv_finite_lk_cap",\
							"t_cur",va_t_cur,"duree traj",t_left,"t_ev_end_veh_dep",t_ev_end_veh_dep,"t_veh_dur=t_left=",t_left)
						
						#we indicate that the dest lk is  not saturated
						state_destin_link=List_Explicit_Values.initialisation_value_to_zero
					else:
						nb_veh_leave=List_Explicit_Values.initialisation_value_to_zero
						t_ev_end_veh_dep=None
						
						#we indicate that the dest lk is  not saturated
						state_destin_link=List_Explicit_Values.initialisation_value_to_zero

				#If the required time <= t_left
				else:
					nb_veh_leave=nb_veh_have_rem_que_hold_time_without_plan_dep
					
					#t_ev_end_veh_dep=math.floor((va_t_cur+va_queue.get_required_depart_time_que())*100)/100
					#t_ev_end_veh_dep=math.floor((va_t_cur+va_queue.get_required_depart_time_que())*10)/10
					
					t_ev_end_veh_dep=self._decision_obj.fct_def_time_end_veh_depart(\
					val_t_current=va_t_cur, val_duration=va_queue.get_required_depart_time_que(),val_t_round=va_t_round_prec,\
					val_decimal_digit_prec=10,val_probab=0,a=0,b=1)
					
					if t_ev_end_veh_dep==va_t_cur:
						print("ATTENTION IN CL_GLOB_FCT,\
						fct_calcul_nb_veh_they_can_leave_at_t_current_and_assoc_end_dep_time_mi_without_permis_prior_mv_finite_lk_cap",\
						"t_cur",va_t_cur,"duree traj",va_queue.get_required_depart_time_que(),"t_ev_end_veh_dep",t_ev_end_veh_dep,"t_veh_dur=t_left=",t_left)
					
					#we indicate that the dest lk is  not saturated
					state_destin_link=List_Explicit_Values.initialisation_value_to_zero
			
			
			#if no vehicle has remained in the que for the min time
			else:
				nb_veh_leave=List_Explicit_Values.initialisation_value_to_zero
				
				#time at which the veh departure will be completed= value non defined
				t_ev_end_veh_dep=None
				
				#we indicate that the dest lk is  not saturated
				state_destin_link=List_Explicit_Values.initialisation_value_to_zero
			
		#if the destination link is saturated
		else:
			#the nb of departing veh
			nb_veh_leave=0
				
			#time at which the veh departure will be completed= value non defined
			t_ev_end_veh_dep=None
				
			total_potential_nb_dep_veh= va_queue.get_current_queue_service_rate() - va_queue.get_current_reached_service_rate()
				
			#we indicate that the dest lk is  saturated
			state_destin_link=List_Explicit_Values.initialisation_value_to_one
			
			
		return [nb_veh_leave,t_ev_end_veh_dep,total_potential_nb_dep_veh,state_destin_link]

#*****************************************************************************************************************************************************************************************
	#method returning the nb of vehicles that can leave from a queue in case where prior-minor phases are not considered,
	#in case of infinite capacity of the destination link
	def fct_calcul_nb_veh_they_can_leave_at_t_current_and_assoc_end_dep_time_mi_without_permis_prior_mv_finite_lk_cap_exit_dest_link_1(self,\
	 va_t_end_current_control,va_t_cur,va_t_unit,\
	 va_queue,va_min_veh_hold_time_in_que,va_t_round_prec):
		
	 
		#the potential number of vehicles that can leave que from the service rate
		#total_potential_nb_dep_veh= va_queue.get_current_queue_service_rate() - va_queue.get_current_reached_service_rate()
				
			
		#total_potential_nb_dep_veh_1=min(total_potential_nb_dep_veh,va_queue.get_nb_veh_cal_leave_simult_que_from_sat_flow())
				
				
		#the number of vehicles which have remained in the que for at least the min hold time without having a veh dep event planned
		nb_veh_have_rem_que_hold_time_without_plan_dep=\
		va_queue.fct_calcul_nb_of_n_veh_remained_in_que_for_min_t_hold_without_planned_dep_for_mi(t_current=va_t_cur,\
		min_hold_time=va_min_veh_hold_time_in_que,li_vehicles=va_queue.get_queue_veh()[:va_queue.get_nb_veh_cal_leave_simult_que_from_sat_flow()],\
		nb_veh_to_exam=va_queue.get_nb_veh_cal_leave_simult_que_from_sat_flow(),val_t_precision=va_t_round_prec)
		
		#if there exist vehicles which have remained the min time in the queue and can leave simul
		if nb_veh_have_rem_que_hold_time_without_plan_dep>List_Explicit_Values.initialisation_value_to_zero:
		
			#the time left until the end of the current control +t_unit (t_end_current_control= the first moment, time unit, at which the new control is applied)
			#va_t_end_current_control=time at which the new control is going to start
			t_left=round(va_t_end_current_control - va_t_cur,va_t_round_prec)
			
			#If the required time > t_left
			if t_left< va_queue.get_required_depart_time_que():
			
				nb_veh_leave=nb_veh_have_rem_que_hold_time_without_plan_dep
				
				t_ev_end_veh_dep=self._decision_obj.fct_def_time_end_veh_depart(\
				val_t_current=va_t_cur, val_duration=t_left,val_t_round=va_t_round_prec,val_decimal_digit_prec=10,val_probab=0,a=0,b=1)
					
				if t_ev_end_veh_dep==va_t_cur:
					print("ATTENTION IN CL_GLOB_FCT,\
					fct_calcul_nb_veh_they_can_leave_at_t_current_and_assoc_end_dep_time_mi_without_permis_prior_mv_infinite_lk_cap",\
					"t_cur",va_t_cur,"duree traj",t_left,"t_ev_end_veh_dep",t_ev_end_veh_dep)
			
					#veh_will_leave=self._decision_obj.\
					#fct_dec_whether_veh_depart_by_end_ctrl_act(val_t_remain=t_left,val_t_required=va_queue.get_required_depart_time_que(),a=0,b=1)
				
					#if veh_will_leave==List_Explicit_Values.initialisation_value_to_one:
				
					#nb_veh_leave=nb_veh_have_rem_que_hold_time_without_plan_dep
					
					#t_ev_end_veh_dep=round(va_t_cur+t_left,va_t_round_prec)
					#t_ev_end_veh_dep=math.floor((va_t_cur+t_left)*100)/100
					#t_ev_end_veh_dep=math.floor((va_t_cur+t_left)*10)/10
					
					#t_ev_end_veh_dep=self._decision_obj.fct_def_time_end_veh_depart(\
					#val_t_current=va_t_cur, val_duration=t_left,val_t_round=va_t_round_prec,val_decimal_digit_prec=10,val_probab=0,a=0,b=1)
					
					#if t_ev_end_veh_dep==va_t_cur:
						#print("ATTENTION IN CL_GLOB_FCT,\
						#fct_calcul_nb_veh_they_can_leave_at_t_current_and_assoc_end_dep_time_mi_without_permis_prior_mv_infinite_lk_cap",\
						#"t_cur",va_t_cur,"duree traj",t_left,"t_ev_end_veh_dep",t_ev_end_veh_dep)
				
					#else:
						#nb_veh_leave=List_Explicit_Values.initialisation_value_to_zero
						#t_ev_end_veh_dep=None
			
			#if required time <= t_left
			else:
				nb_veh_leave=nb_veh_have_rem_que_hold_time_without_plan_dep
				
				#t_ev_end_veh_dep=round(va_t_cur+va_queue.get_required_depart_time_que(),va_t_round_prec)
				#duree_init=va_t_cur+va_queue.get_required_depart_time_que()
				#duree_init_multipliee=duree_init*100
				#chiffres decimaux
				#partie_entiere=math.floor(duree_init_multipliee)
				#partie_decimale=duree_init_multipliee-partie_entiere
				#if no decimals
				#if partie_decimale==0:
					#t_ev_end_veh_dep=duree_init
				#if  decimals
				#else:
					#t_ev_end_veh_dep=(duree_init_multipliee//1)/100
				#t_ev_end_veh_dep=math.floor((va_t_cur+va_queue.get_required_depart_time_que())*100)/100
				#t_ev_end_veh_dep=math.floor((va_t_cur+va_queue.get_required_depart_time_que())*10)/10
				
				t_ev_end_veh_dep=self._decision_obj.fct_def_time_end_veh_depart(\
					val_t_current=va_t_cur, val_duration=va_queue.get_required_depart_time_que(),val_t_round=va_t_round_prec,\
					val_decimal_digit_prec=10,val_probab=0,a=0,b=1)
				
				if t_ev_end_veh_dep==va_t_cur:
					print("ATTENTION IN CL_GLOB_FCT,\
					fct_calcul_nb_veh_they_can_leave_at_t_current_and_assoc_end_dep_time_mi_without_permis_prior_mv_infinite_lk_cap",\
					"t_cur",va_t_cur,"duree traj",va_queue.get_required_depart_time_que(),"t_ev_end_veh_dep",t_ev_end_veh_dep)
		
		#if no vehicle  has remained the min time in the queue
		else:
			nb_veh_leave=List_Explicit_Values.initialisation_value_to_zero
				
			#time at which the veh departure will be completed= value non defined
			t_ev_end_veh_dep=None
			
		#we indicate that the dest lk is not saturated
		state_destin_link=List_Explicit_Values.initialisation_value_to_zero
		
		#if nb_veh_leave>0 and va_queue.get_id_associated_link()==2 and va_queue.get_id_associated_output_link()==3:
		#if nb_veh_leave>0 :
			#print("va_t_cu",va_t_cur,"va_queue.get_required_depart_time_que()",va_queue.get_required_depart_time_que(),\
			#"t_ev_end_veh_dep",t_ev_end_veh_dep)
			#import sys
			#sys.exit()
		return [nb_veh_leave,t_ev_end_veh_dep,va_queue.get_nb_veh_cal_leave_simult_que_from_sat_flow(),state_destin_link]
		
#*****************************************************************************************************************************************************************************************
	#method returning the nb of vehicles that can leave from a queue in case where prior-minor phases are not considered,
	#in case of infinite capacity of the destination link
	def fct_calcul_nb_veh_they_can_leave_at_t_current_and_assoc_end_dep_time_mi_without_permis_prior_mv_finite_lk_cap_exit_dest_link(self,\
	 va_t_end_current_control,va_t_cur,va_t_unit,\
	 va_queue,va_min_veh_hold_time_in_que,va_t_round_prec):
		
	 
		#the potential number of vehicles that can leave que from the service rate
		total_potential_nb_dep_veh= va_queue.get_current_queue_service_rate() - va_queue.get_current_reached_service_rate()
		
		#if vehicles can leave from the service rate
		if total_potential_nb_dep_veh>List_Explicit_Values.initialisation_value_to_zero:
		
			#if the first veh has satisfied the hold constraint
			if va_queue.fct_calcul_first_veh_remained_in_que_for_min_t_hold_without_planned_dep_for_mi(\
			t_current=va_t_cur,min_hold_time=va_min_veh_hold_time_in_que,li_vehicles=va_queue.get_queue_veh(),val_t_precision=va_t_round_prec)>\
			List_Explicit_Values.initialisation_value_to_zero:
			
				#the time left until the end of the current control +t_unit (t_end_current_control= the first moment, time unit, at which the new control is applied)
				#va_t_end_current_control=time at which the new control is going to start
				t_left=round(va_t_end_current_control - va_t_cur,va_t_round_prec) 
				
				if t_left<0:
						print("PROBLEM IN CL_GL_FCT, fct_calcul_nb_veh_they_can_leave_at_t_current_and_assoc_end_dep_time_mi_without_permis_prior_mv_finite_lk_cap_exit_dest_link, t_left",\
						t_left,"t_req",va_queue.get_required_depart_time_que(),"va_t_end_current_control",va_t_end_current_control,"va_t_cur,",va_t_cur)
						print("que",va_queue.get_id_associated_link(),va_queue.get_id_associated_output_link())
						import sys
						sys.exit()
						
				else:
					#calcul of the required depart time
				
					#if a que sat flow corresponds to the vehicle
					if va_queue.get_queue_veh()[0].get_veh_sat_flow_when_current_que_locat_affected()!=None:
				
						t_req_dep=va_queue.fct_defining_t_req_for_single_veh_depart(val_t_unit=va_t_unit,\
						val_sat_flow=va_queue.get_queue_veh()[0].get_veh_sat_flow_when_current_que_locat_affected(),val_dec_digits=10)
						
						
				
					#if no que sat flow corresponds to the vehicle 
					else:
						t_req_dep=va_queue.get_required_depart_time_que()
					
					#If the required time > t_left
					if t_req_dep> t_left:
						nb_veh_leave=List_Explicit_Values.initialisation_value_to_one
					
						t_ev_end_veh_dep=self._decision_obj.fct_def_time_end_veh_depart(\
						val_t_current=va_t_cur, val_duration=t_left,val_t_round=va_t_round_prec,val_decimal_digit_prec=10,val_probab=0,a=0,b=1)
					
						if t_ev_end_veh_dep==va_t_cur:
							print("ATTENTION IN CL_GLOB_FCT,\
							fct_calcul_nb_veh_they_can_leave_at_t_current_and_assoc_end_dep_time_mi_without_permis_prior_mv_finite_lk_cap_exit_dest_link",\
							"t_cur",va_t_cur,"duree traj",t_left,"t_ev_end_veh_dep",t_ev_end_veh_dep,"t_veh_dur=t_left=",t_left)
						
						state_destin_link=List_Explicit_Values.initialisation_value_to_zero
					
						return [nb_veh_leave,t_ev_end_veh_dep,total_potential_nb_dep_veh,state_destin_link]
				
					#If the required time <= t_left
					else:
				
						nb_veh_leave=List_Explicit_Values.initialisation_value_to_one
					
						t_ev_end_veh_dep=self._decision_obj.fct_def_time_end_veh_depart(\
						val_t_current=va_t_cur, val_duration=t_req_dep,\
						val_t_round=va_t_round_prec,val_decimal_digit_prec=10,val_probab=0,a=0,b=1)
					
						if t_ev_end_veh_dep==va_t_cur:
							print("ATTENTION IN CL_GLOB_FCT,\
							fct_calcul_nb_veh_they_can_leave_at_t_current_and_assoc_end_dep_time_mi_without_permis_prior_mv_finite_lk_cap_exit_dest_link",\
							"t_cur",va_t_cur,"duree traj",va_queue.get_required_depart_time_que(),"t_ev_end_veh_dep",t_ev_end_veh_dep,"t_veh_dur=t_left=",t_left)
						
						state_destin_link=List_Explicit_Values.initialisation_value_to_zero
						
						return [nb_veh_leave,t_ev_end_veh_dep,total_potential_nb_dep_veh,state_destin_link]
			
			#if the first veh has not satisfied the hold constraint
			else:
				nb_veh_leave=List_Explicit_Values.initialisation_value_to_zero
				t_ev_end_veh_dep=None
				state_destin_link=List_Explicit_Values.initialisation_value_to_zero
					
				return [nb_veh_leave,t_ev_end_veh_dep,total_potential_nb_dep_veh,state_destin_link]
		
		
		
		#if vehicles cannot leave from the service rate
		else:
			nb_veh_leave=List_Explicit_Values.initialisation_value_to_zero
				
			#time at which the veh departure will be completed= value non defined
			t_ev_end_veh_dep=None
			
			#we indicate that the dest lk is not saturated
			state_destin_link=List_Explicit_Values.initialisation_value_to_zero
			
			return [nb_veh_leave,t_ev_end_veh_dep,total_potential_nb_dep_veh,state_destin_link]
			
				
#*****************************************************************************************************************************************************************************************
	#method returning [the number of vehicles that can depart from a que, the associated end dep time, \
	#the total potential number of vehicles in the que, the state of the dest link, whether  it is/not saturated], 
	#according to a micro management (veh can leave as as et) 
	def fct_calcul_nb_veh_they_can_leave_at_t_current_and_assoc_end_dep_time_mi_without_permis_mv(self,v_t_cur,v_t_unit,v_queue,\
	v_min_veh_hold_time_in_que,v_t_end_current_control,v_netw,val_t_round_prec):
	
		#print("IN CL GLOBAL FCTS:",v_netw.get_di_intersections()[v_netw.get_di_entry_internal_links()[v_queue.get_id_associated_link()].get_id_head_intersection_node()].\
		#get_intersection_control_obj().get_type_control())
		#print("que",v_queue.get_id_associated_link(),v_queue.get_id_associated_output_link())
		#print("T CURRENT: ",v_t_cur)
		#print("T START CTRL",v_netw.get_di_intersections()[v_netw.get_di_entry_internal_links()[v_queue.get_id_associated_link()].get_id_head_intersection_node()].\
		#get_intersection_control_obj().get_t_start_control())
		#print("T ENDS CTRL",v_netw.get_di_intersections()[v_netw.get_di_entry_internal_links()[v_queue.get_id_associated_link()].get_id_head_intersection_node()].\
		#get_intersection_control_obj().get_t_end_control())
		#print("T UPDATE CTRL",v_netw.get_di_intersections()[v_netw.get_di_entry_internal_links()[v_queue.get_id_associated_link()].get_id_head_intersection_node()].\
		#get_intersection_control_obj().get_t_update_ctrl())
		
		#print("VAL NET", val_netw)
		#if the vehicle destination link is not an exit link (double check for exit links here but it is ok, in order to avoid any error in the network data file
		#PERHAPS TO BE REMOVED LATER 
		if v_netw.get_di_all_links()[v_queue.get_id_associated_output_link()].get_type_network_link()!=Cl_Network_Link.TYPE_NETWORK_LINK["exit"]:
			
			
			#if we consider an infiniy  capacity of the dest link or if the vehicle  dest is/exit link DOUBLE CHECK !!!
			if v_netw.get_di_entry_internal_links()[v_queue.get_id_associated_output_link()].get_capacity_link() ==-1 or\
			 v_netw.get_di_entry_internal_links()[v_queue.get_id_associated_output_link()].get_capacity_link() ==0:
				
				
				rep=self.fct_calcul_nb_veh_they_can_leave_at_t_current_and_assoc_end_dep_time_mi_without_permis_prior_mv_infinite_lk_cap(\
				va_t_end_current_control=v_t_end_current_control,va_t_cur=v_t_cur,va_t_unit=v_t_unit,\
				va_queue=v_queue,\
				va_min_veh_hold_time_in_que=v_min_veh_hold_time_in_que,va_t_round_prec=val_t_round_prec)
				
				
				
			
			#if we consider limited link capacity fot the dest link
			elif v_netw.get_di_entry_internal_links()[v_queue.get_id_associated_output_link()].get_capacity_link() >0:
			
				rep= self.fct_calcul_nb_veh_they_can_leave_at_t_current_and_assoc_end_dep_time_mi_without_permis_prior_mv_finite_lk_cap(\
				va_t_end_current_control=v_t_end_current_control,va_t_cur=v_t_cur,va_t_unit=v_t_unit,va_netw=v_netw,\
				va_queue=v_queue,\
				va_min_veh_hold_time_in_que=v_min_veh_hold_time_in_que,va_t_round_prec=val_t_round_prec)
				

		
		#if the  vehicle destination link is an exit link we let the vehicle(s) to go. No queues at exit links.
		else:
			#if we consider finite link capacities
			if v_netw.get_di_entry_internal_links()[v_queue.get_id_associated_link()].get_capacity_link() >0:
				rep=self.\
				fct_calcul_nb_veh_they_can_leave_at_t_current_and_assoc_end_dep_time_mi_without_permis_prior_mv_finite_lk_cap_exit_dest_link(\
				va_t_end_current_control=v_t_end_current_control,va_t_cur=v_t_cur,va_t_unit=v_t_unit,\
				va_queue=v_queue,\
				va_min_veh_hold_time_in_que=v_min_veh_hold_time_in_que,va_t_round_prec=val_t_round_prec)
			#if we consider infinite link capacitites
			else: 
				rep=self.fct_calcul_nb_veh_they_can_leave_at_t_current_and_assoc_end_dep_time_mi_without_permis_prior_mv_infinite_lk_cap(\
				va_t_end_current_control=v_t_end_current_control,va_t_cur=v_t_cur,va_t_unit=v_t_unit,\
				va_queue=v_queue,\
				va_min_veh_hold_time_in_que=v_min_veh_hold_time_in_que,va_t_round_prec=val_t_round_prec)
				
		return rep


#*****************************************************************************************************************************************************************************************


	#method returning [nb_veh_leave,t_ev_end_veh_dep,total_potential_nb_dep_veh,state_destin_link], indicator minor phase, indicator prior phase], 
	#according to a micro management 
	#v_vect_nb_veh_to_exam=[nb veh permitted to go ny the sat flow, t_req]
	def fct_calcul_nb_veh_they_can_leave_at_t_current_and_assoc_end_dep_time_mi(self,t_cur,t_unit,queue,min_veh_hold_time_in_que,\
	t_end_current_control,val_netw,v_t_round_prec):
		
		
		
		#if the examined queue is related to a permissive phase
		#if queue.get_type_related_phase()==Cl_Vehicle_Queue.TYPE_RELATED_PHASE["minor_mv"]:
			
		
			#for each prior movement related to the permissive one
			#for i in queue.get_li_id_minor_prior_phases_related_to_que():
				
				
				#nb_veh_leave_t_ev_end_veh_dep_total_potential_nb_dep_veh=
				#[nb_veh_leave,t_ev_end_veh_dep,total_potential_nb_dep_veh,state_destin_link]
				#nb_veh_leave_t_ev_end_veh_dep_total_potential_nb_dep_veh=\
				#self.fct_calcul_nb_veh_they_can_leave_at_t_current_and_assoc_end_dep_time_mi_from_permis_mv(\
				#va_t_current=t_cur, va_t_unit=t_unit,va_t_end_current_control=t_end_current_control,\
				#va_min_veh_hold_time_in_que=min_veh_hold_time_in_que, \
				#va_id_input_lk_minor_phase=queue.get_id_associated_link(),\
				#va_id_output_lk_minor_phase=queue.get_id_associated_output_link(),\
				#va_id_input_lk_prior_phase=i[0],\
				#va_id_output_lk_prior_phase=i[1],\
				#va_network=val_netw,va_vect_nb_veh_to_exam=v_vect_nb_veh_to_exam,va_t_round_prec=v_t_round_prec)
				
				#if nb_veh_leave_t_ev_end_veh_dep_total_potential_nb_dep_veh[0]==0:
				
					#indicator_minor_mv=1
					#indicator_prior_mv=0
				
					#return [nb_veh_leave_t_ev_end_veh_dep_total_potential_nb_dep_veh,indicator_minor_mv,indicator_prior_mv]
					
			#we indicate that we treat a minor movement	
			#indicator_minor_mv=1
			#indicator_prior_mv=0
			#return [nb_veh_leave_t_ev_end_veh_dep_total_potential_nb_dep_veh,indicator_minor_mv,indicator_prior_mv]
			
		# if the examined queue is related to a prior movement
		#elif queue.get_type_related_phase()==Cl_Vehicle_Queue.TYPE_RELATED_PHASE["prior_mv"]:
		
			#nb_veh_leave_t_ev_end_veh_dep_total_potential_nb_dep_veh=\
			#self.fct_calcul_nb_veh_they_can_leave_at_t_current_and_assoc_end_dep_time_mi_from_prior_mv(va_t_cur=t_cur,va_t_unit=t_unit,\
			#va_queue=queue,va_min_veh_hold_time_in_que=min_veh_hold_time_in_que,\
			#va_t_end_current_control=t_end_current_control,va_netw=val_netw,va_vect_nb_veh_to_exam=v_vect_nb_veh_to_exam,\
			#va_t_round_prec=v_t_round_prec)
			
			#we indicate that we treat a prior movement
			#indicator_minor_mv=0
			#indicator_prior_mv=1
		
		#if the examined queue does not correspond to a permissive phase simultanesouly actuated with the related prior. phase
		#else:
			
		#nb_veh_leave_t_ev_end_veh_dep_total_potential_nb_dep_veh=\
		#[nb_veh_leave,t_ev_end_veh_dep,total_potential_nb_dep_veh,state_destin_link]
		nb_veh_leave_t_ev_end_veh_dep_total_potential_nb_dep_veh=\
		self.fct_calcul_nb_veh_they_can_leave_at_t_current_and_assoc_end_dep_time_mi_without_permis_mv(\
		v_t_cur=t_cur,v_t_unit=t_unit,v_queue=queue,v_min_veh_hold_time_in_que=min_veh_hold_time_in_que,\
		v_t_end_current_control=t_end_current_control,v_netw=val_netw,\
		val_t_round_prec=v_t_round_prec)
		 
		
			
			
		#we indicate that the examined phase is neither a prior nor a minor movement
		indicator_minor_mv=0
		indicator_prior_mv=0
			
		return [nb_veh_leave_t_ev_end_veh_dep_total_potential_nb_dep_veh,indicator_minor_mv,indicator_prior_mv]
#*****************************************************************************************************************************************************************************************
	#method treating the case when vehicles are authorised to leave the queue
	def fct_treat_case_veh_can_go(self,\
	t_current,t_unit,fct_calcul_nb_and_t_dep_veh,li_param_fct_calcul_nb_and_t_dep_veh,id_que,val_netw,val_t_round_prec,ev_list):
	
		
		#calcul of number dep vehicles, this method returns
		#[nb_veh_leave_t_ev_end_veh_dep_total_potential_nb_dep_veh,indicator_minor_mv,indicator_prior_mv], where
		#nb_veh_leave_t_ev_end_veh_dep_total_potential_nb_dep_veh=
		#[nb_veh_leave,t_ev_end_veh_dep,total_potential_nb_dep_veh,state_destin_link]
		nb_and_t_dep_veh=fct_calcul_nb_and_t_dep_veh(*li_param_fct_calcul_nb_and_t_dep_veh)
		
		#if id_que[0]==1 and id_que[1]==2:
			#print("nb_and_t_dep_veh",nb_and_t_dep_veh,fct_calcul_nb_and_t_dep_veh)
			
		#print(nb_and_t_dep_veh[0],t_current)
		#print("here",id_que)
		#import sys
		#sys.exit()
		#if t_current==62.1 and id_que==(4,5):
			#print(nb_and_t_dep_veh)
			#import sys
			#sys.exit()
		if nb_and_t_dep_veh[0][1]==t_current and nb_and_t_dep_veh[0][0]>0:
			print("ATTENTION IN CL_GLOB FUNCT fct_treat_case_veh_can_go, t_end_veh_dep",\
			"nb depart veh: ",nb_and_t_dep_veh[0][0],nb_and_t_dep_veh[0][1],"t_current",t_current,"id queue",id_que[0],id_que[1])
			#import sys
			#sys.exit()
		
		
		#if there are vehicles which can leave
		if nb_and_t_dep_veh[0][List_Explicit_Values.val_first_element_of_list] >List_Explicit_Values.initialisation_value_to_zero:
			
		
			if nb_and_t_dep_veh[0][List_Explicit_Values.val_first_element_of_list] >List_Explicit_Values.initialisation_value_to_one:
				print("VERIFY IN CL_GLOB FCT, fct_treat_case_veh_can_go, \
				NB SIMULTANEOUS VEH DEPARTING", \
				nb_and_t_dep_veh[0][List_Explicit_Values.val_first_element_of_list])
				import sys
				sys.exit()
		
			#if the movement is prior or minor, the we indicate the intersection that a prior or minor mv is about to cross
			#if val_netw.get_di_entry_internal_links()[id_que[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
			#[id_que[0],id_que[1]].get_type_related_phase()==Cl_Vehicle_Queue.TYPE_RELATED_PHASE["minor_mv"]:
				#val_netw.get_di_intersections()[val_netw.get_di_entry_internal_links()[id_que[0]].\
				#get_id_head_intersection_node()].set_indicator_minor_mv_cross_intersection(List_Explicit_Values.initialisation_value_to_one)
			
			#elif val_netw.get_di_entry_internal_links()[id_que[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
			#[id_que[0],id_que[1]].get_type_related_phase()==Cl_Vehicle_Queue.TYPE_RELATED_PHASE["prior_mv"]:
				#val_netw.get_di_intersections()[val_netw.get_di_entry_internal_links()[id_que[0]].\
				#get_id_head_intersection_node()].set_indicator_prior_mv_cross_intersection(List_Explicit_Values.initialisation_value_to_one)
		
			#we update each departing vehicle ( its state  and t start depart)
			self.fct_update_each_dep_veh(nb_dep_veh=nb_and_t_dep_veh[0][List_Explicit_Values.val_first_element_of_list],\
			val_id_que=id_que,val_netwk=val_netw,val_t_start_depart=t_current)

		
			ev_end_veh_dep=Cl_Ev_end_veh_departure_from_que.Ev_end_veh_departure_from_que(\
			val_ev_t=nb_and_t_dep_veh[0][List_Explicit_Values.val_second_element_of_list],\
			val_id_queue_obj=id_que,val_nb_depart_veh=nb_and_t_dep_veh[0][List_Explicit_Values.val_first_element_of_list])
			
			#we insert the event in the event list
			ev_end_veh_dep.fct_insertion_even_in_event_list(event_list=ev_list,\
			message="IN CL_GLOB FUNCT IN FUNCT Fct_treat_case_veh_can_go,\
			EVENT END VEH DEP HAS TIME < TIME FIRST EVENT IN THE LIST")
		
		#if no vehicle can leave the queue and there are vehicles in the que we examine if we can  create an event end veh hold
		elif nb_and_t_dep_veh[0][List_Explicit_Values.val_first_element_of_list] ==List_Explicit_Values.initialisation_value_to_zero and \
		len(val_netw.get_di_entry_internal_links()[id_que[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[id_que[0],id_que[1]].get_queue_veh())>nb_and_t_dep_veh[0][List_Explicit_Values.val_first_element_of_list]:
		
			#if the related movement is not a permissive one or prior movement, then we examine if an event end veh hold can be created
			if nb_and_t_dep_veh[1]==List_Explicit_Values.initialisation_value_to_zero and\
			 nb_and_t_dep_veh[2]==List_Explicit_Values.initialisation_value_to_zero:
			
			
		
				#print("HERE LEN",len(val_netw.get_di_entry_internal_links()[id_que[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
				#[id_que[0],id_que[1]].get_queue_veh()),\
				#"nb_and_t_dep_veh[List_Explicit_Values.val_first_element_of_list]",\
				#nb_and_t_dep_veh[List_Explicit_Values.val_first_element_of_list],"id_que",id_que,"t_current",t_current)
			
				#t_start_new_cont=val_netw.get_current_network_control_obj().get_t_start_control()+\
				#val_netw.get_current_network_control_obj().get_t_duration_control()
				
				
				t_start_new_cont=val_netw.get_di_intersections()[val_netw.get_di_entry_internal_links()[id_que[0]].\
				get_id_head_intersection_node()].get_intersection_control_obj().get_t_end_control()+t_unit
			
			
				self.fct_treat_case_veh_in_que_none_can_dep(v_t_current=t_current, \
				v_t_end_hold_first_veh_in_que=\
				val_netw.get_di_entry_internal_links()[id_que[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
				[id_que[0],id_que[1]].get_queue_veh()[nb_and_t_dep_veh[0][List_Explicit_Values.val_first_element_of_list]:\
				nb_and_t_dep_veh[0][List_Explicit_Values.val_first_element_of_list]+1][0].get_t_end_veh_hold_time_que(),\
				v_t_unit=t_unit,\
				v_t_start_new_contr=t_start_new_cont,\
				val_dest_lk_saturated=nb_and_t_dep_veh[0][List_Explicit_Values.val_fourth_element_of_list],\
				v_nb_veh_possible_to_leave_from_serv_rate=nb_and_t_dep_veh[0][List_Explicit_Values.val_third_element_of_list],\
				v_state_first_veh_in_que=val_netw.get_di_entry_internal_links()[id_que[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
				[id_que[0],id_que[1]].get_queue_veh()[nb_and_t_dep_veh[0][List_Explicit_Values.val_first_element_of_list]:\
				nb_and_t_dep_veh[0][List_Explicit_Values.val_first_element_of_list]+1][0].get_state_veh(),\
				v_que=val_netw.get_di_entry_internal_links()[id_que[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
				[id_que[0],id_que[1]],\
				v_t_round_prec=val_t_round_prec,v_ev_list=ev_list)
		
				
			#if the related movement is  a permissive one or prior movement, then 
			#if  no vehicle of prior-minor mv cross the intersection and if the vehicle has not achived its hold time at this moment
			#then we examine if  end of the veh hold event may be created
			else:
				#if there are vehs in the que
				#if val_netw.get_di_entry_internal_links()[id_que[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
				#[id_que[0],id_que[1]].get_queue_veh() !=[]:
				
				#if no minor or prior veh crosses the intersection
				if val_netw.get_di_intersections()[val_netw.get_di_entry_internal_links()[id_que[0]].get_id_head_intersection_node()].\
				get_indicator_prior_mv_cross_intersection()==List_Explicit_Values.initialisation_value_to_zero and\
				val_netw.get_di_intersections()[val_netw.get_di_entry_internal_links()[id_que[0]].get_id_head_intersection_node()].\
				get_indicator_minor_mv_cross_intersection()==List_Explicit_Values.initialisation_value_to_zero:
					
					#t_start_new_cont=val_netw.get_current_network_control_obj().get_t_start_control()+\
					#val_netw.get_current_network_control_obj().get_t_duration_control()
						
					t_start_new_cont=val_netw.get_di_intersection_controls()[\
					val_netw.get_di_entry_internal_links()[id_que[0]].get_id_head_intersection_node()].\
					get_t_end_control()+t_unit

					
					self.fct_treat_case_veh_in_que_none_can_dep(v_t_current=t_current, \
					v_t_end_hold_first_veh_in_que=\
					val_netw.get_di_entry_internal_links()[id_que[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
					[id_que[0],id_que[1]].get_queue_veh()[nb_and_t_dep_veh[0][List_Explicit_Values.val_first_element_of_list]:\
					nb_and_t_dep_veh[0][List_Explicit_Values.val_first_element_of_list]+1][0].get_t_end_veh_hold_time_que(),\
					v_t_unit=t_unit,\
					v_t_start_new_contr=t_start_new_cont,\
					val_dest_lk_saturated=nb_and_t_dep_veh[0][List_Explicit_Values.val_fourth_element_of_list],\
					v_nb_veh_possible_to_leave_from_serv_rate=nb_and_t_dep_veh[0][List_Explicit_Values.val_third_element_of_list],\
					v_state_first_veh_in_que=val_netw.get_di_entry_internal_links()[id_que[0]].get_set_veh_queue().\
					get_di_obj_veh_queue_at_link()\
					[id_que[0],id_que[1]].get_queue_veh()[nb_and_t_dep_veh[0][List_Explicit_Values.val_first_element_of_list]:\
					nb_and_t_dep_veh[0][List_Explicit_Values.val_first_element_of_list]+1][0].get_state_veh(),\
					v_que=val_netw.get_di_entry_internal_links()[id_que[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
					[id_que[0],id_que[1]],\
					v_t_round_prec=val_t_round_prec,v_ev_list=ev_list)
											
		return nb_and_t_dep_veh[0][List_Explicit_Values.val_first_element_of_list] 
			
			

#*****************************************************************************************************************************************************************************************

	#method returning the first element of a (ordered)  list, being greater to a given value
	#ex: li=[]60,120,180,240], val=130 -> 180
	def fct_returning_first_li_elem_great_to_given_val(self,val_list, val_elem):
		ok=0
		for i in val_list:
			
			if val_elem<i:
				ok=1
				return i
		if ok==0:
			print("PROBLEM IN CL_GL FUNCT, fct_returning_first_li_elem_great_to_given_val, NI ELEM IN THE LIST: ",val_list, "GREATER TO: ",val_elem)
			import sys
			sys.exit()

#*****************************************************************************************************************************************************************************************

	#method updating each departing vehicle
	def fct_update_each_dep_veh(self,nb_dep_veh,val_id_que,val_netwk,val_t_start_depart):
		
		#we indicate the new state of the vehicle
		for i in val_netwk.get_di_entry_internal_links()[val_id_que[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[val_id_que[0],val_id_que[1]].get_queue_veh()[:nb_dep_veh]:
			
			#we indicate the new state of the vehicle
			i.set_state_veh(Cl_Vehicle.TYPE_STATE_VEH["veh_dep_planned"])
			
			#we indicate the time at which the vehicle started to depart the link
			i.set_t_vehicle_started_departure_from_current_link(val_t_start_depart)
			
			#we indicate the time at which the vehicle started to depart the queue
			i.set_t_vehicle_started_departure_from_current_queue(val_t_start_depart)
			
			

#*****************************************************************************************************************************************************************************************

	#we examine in which case an end hold event will be created,when no vehicle can leave the queue but there still vehicles in the que
	#val_nb_veh_possible_to_leave_from_serv_rate=que service rate-currently reached que service  rate
	
	def fct_treat_case_veh_in_que_none_can_dep(self,v_t_current, v_t_end_hold_first_veh_in_que,v_t_unit,v_t_start_new_contr,\
	val_dest_lk_saturated,v_nb_veh_possible_to_leave_from_serv_rate,v_state_first_veh_in_que,\
	v_que,v_t_round_prec, v_ev_list):
	
		#if the destination link is not saturated
		if val_dest_lk_saturated==List_Explicit_Values.initialisation_value_to_zero:
		
			#if the nb of vehilces permitted to leave from the service rate (this  is service rate - currently reached service rate) >0
			#if no vehicles are permitted to leave now (concerning the service rate), they will have to wait for a new cotnrol to be applied
			#which it will reinitialise the queue service rate
			if v_nb_veh_possible_to_leave_from_serv_rate>0:
		
				#if the 1st veh in the que has no planned dep event
				if v_state_first_veh_in_que==Cl_Vehicle.TYPE_STATE_VEH["other"]:
					#we calculate the time of the event to reexamine if the veh can leave
					if v_t_end_hold_first_veh_in_que<=v_t_current:
						t_new_end_hold=round(v_t_current+ v_t_unit,v_t_round_prec)
					else:
						t_new_end_hold=v_t_end_hold_first_veh_in_que
					
						
						#if the remaining time before a new ctrl starts is enough for a vehicle to depart,
						#then we examine if an event end hold time can be created
						v_t_start_new_contr_1=v_t_start_new_contr-v_t_unit
						t_left=round(v_t_start_new_contr_1 - v_t_current,v_t_round_prec) 
						
						#the number of vehicles that can leave within t_left seconds
						#nb_veh_can_leave_during_t_left=math.ceil(queue.get_sat_flow_queue() * t_left/t_unit )
						nb_veh_can_leave_during_t_left=round(v_que.get_sat_flow_queue() * t_left/v_t_unit )
						
						if nb_veh_can_leave_during_t_left>0:
					
							#we create the event end veh hold
							ev_end_veh_hold=Cl_Ev_end_veh_hold_at_que.Ev_end_veh_hold_at_que(\
							val_event_t=t_new_end_hold,val_id_que=[v_que.get_id_associated_link(),v_que.get_id_associated_output_link()])
			
							#we insert the event in the event list
							ev_end_veh_hold.fct_insertion_even_in_event_list(event_list=v_ev_list,\
							message="IN CL_GLOB FUNCT IN FUNCTfct_treat_case_veh_in_que_none_can_dep,EVENT END VEH HOLD HAS TIME < TIME FIRST EVENT IN THE LIST")
					
#*****************************************************************************************************************************************************************************************


	#method retrieving the final state of the network of a previous sim
	def retrieve_network_obj_prevous_sim(self,file_saved_network):
		
		FILE=open(file_saved_network,"rb")
		new_netw_objet=pickle.load(FILE)
		FILE.close()
		return new_netw_objet
	 
#*****************************************************************************************************************************************************************************************		
	#method retrieving the event list at the end of a previous sim
	def retrieve_event_list_previous_sim(self,file_saved_pile_event):
	
		FILE=open(file_saved_pile_event,"rb")
		new_event_list=pickle.load(FILE)
		FILE.close()
		return new_event_list
	
#*****************************************************************************************************************************************************************************************
	#method retrieving an object srored in a file
	def retrieve_object_previous_sim(self,file_saved_object):
		
		FILE=open(file_saved_object,"rb")
		new_objet=pickle.load(FILE)
		FILE.close()
		return new_objet
		

#*****************************************************************************************************************************************************************************************


























