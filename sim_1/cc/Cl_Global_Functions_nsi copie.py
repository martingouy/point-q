import heapq
from heapq import * 
import List_Explicit_Values
import Cl_Ev_end_veh_departure_from_que
#import Cl_Ev_veh_arrived_at_lk
import Cl_Ev_end_veh_hold_at_que_nsi
import Cl_Ev_end_veh_departure_from_que
import Cl_Vehicle_Queue
import Cl_Network_Link
import Cl_Vehicle
import Cl_Network
import Global_Functions
import pickle
import math

class Global_Functions_nsi:

	def __init__(self):
		pass
#*****************************************************************************************************************************************************************************************
	#method calculating the nb of vehicles than can leave from a list of phases (knowing that there exist veh in the related ques and the mov
	#is allowed)
	#it returns [...,[phase id, nb veh to go, t_end_depart,t_start_dep,depart duration],...]
	def fct_calcul_nb_veh_leave_li_compatible_phases_infinite_lk_capacity(self,valeur_li_phase_id,valeur_netw,valeur_unit_time,valeur_cur_ti,\
	valeur_min_veh_hold_ti_in_que,valeur_prec_round):
		li_rep=[]
		#for each phase id we calculate the number of veh to go
		for i in valeur_li_phase_id:
			
			#rep=[nb_veh_leave,t_ev_end_veh_dep,t_start_dep,veh_dep_dur,t_start_dep,veh_dep_dur] 
			rep=self.fct_defin_nb_veh_can_leave_infinite_dest_lk_capacity_mi(\
			v_netwk=valeur_netw,v_que_id=i,v_unit_time=valeur_unit_time,v_cur_ti=valeur_cur_ti,\
			v_min_veh_hold_ti_in_que=valeur_min_veh_hold_ti_in_que,v_prec_round=valeur_prec_round)
			
			#if veh can go
			if rep[0]>0:
				li=[i]
				li.extend(rep)
				#li=[i,rep[0],rep[1]]
				li_rep.append(li)
		return li_rep
			
			
#*****************************************************************************************************************************************************************************************
	#method defining the number of vehicles that can go when known that veh is (are) allowed to leave a given que and
	#the related t end veh departure
	#it returns [nb_veh_leave,t_ev_end_veh_dep,t_start_dep,veh_dep_dur]
	def fct_defin_nb_veh_can_leave_infinite_dest_lk_capacity_mi(self,v_netwk,v_que_id,v_unit_time,v_cur_ti,\
	v_min_veh_hold_ti_in_que,v_prec_round):
	
		#the potential number of vehicles that can leave que from the service rate
		total_potential_nb_dep_veh= v_netwk.get_di_entry_internal_links()[v_que_id[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[v_que_id[0],v_que_id[1]].get_current_queue_service_rate() -\
		v_netwk.get_di_entry_internal_links()[v_que_id[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[v_que_id[0],v_que_id[1]].get_current_reached_service_rate()
		
		#if v_que_id[0]==21 and v_que_id[1]==22:
			#print(total_potential_nb_dep_veh)
		
		
		#the number of vehicles to be examined if the can leave according to the sat flow,  employed in a micro management
		#va_vect_nb_veh_to_exam=[nb veh to leave, time required toleave the queue]
		va_vect_nb_veh_to_exam=Global_Functions.fct_defin_nb_veh_leave_mi(\
		v_sat_flow=\
		v_netwk.get_di_entry_internal_links()[v_que_id[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[v_que_id[0],v_que_id[1]].get_sat_flow_queue(),v_t_unit=v_unit_time,v_round_prec=v_prec_round)
		
		#if v_que_id[0]==21 and v_que_id[1]==22:
			#print(va_vect_nb_veh_to_exam)
			
		
		#the potential number of vehicles that can leave que
		total_potential_nb_dep_veh_1=min(total_potential_nb_dep_veh,va_vect_nb_veh_to_exam[0])
		
		#the number of vehicles  defined by the sat flow 
		#which have remained in the que for at least the min hold time without having a veh dep event planned
		nb_veh_leave=\
		v_netwk.get_di_entry_internal_links()[v_que_id[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()[v_que_id[0],\
		v_que_id[1]].fct_calcul_nb_of_n_veh_remained_in_que_for_min_t_hold_without_planned_dep_for_mi(t_current=v_cur_ti,\
		min_hold_time=v_min_veh_hold_ti_in_que,\
		li_vehicles=v_netwk.get_di_entry_internal_links()[v_que_id[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()[v_que_id[0],\
		v_que_id[1]].get_queue_veh()[:total_potential_nb_dep_veh_1],\
		nb_veh_to_exam=total_potential_nb_dep_veh_1,val_precision=v_prec_round)
		
		#the required time for nb_veh_leave to leave
		t_req=round(nb_veh_leave*v_unit_time/v_netwk.\
		get_di_entry_internal_links()[v_que_id[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()[v_que_id[0],v_que_id[1]].\
		get_sat_flow_queue(),v_prec_round)
		
		t_ev_end_veh_dep=round(v_cur_ti+t_req,v_prec_round)
		
		return [nb_veh_leave,t_ev_end_veh_dep,v_cur_ti,t_req]
		
		
#*****************************************************************************************************************************************************************************************
	#method defining the number of vehicles that can go when known that veh can leave and the related t end veh departure
	#it returns [nb_veh_leave,t_ev_end_veh_dep,t_start_dep,dep duration]
	def fct_defin_nb_veh_can_leave_finite_dest_lk_capacity_mi(self,v_nb_avail_places_dest_lk,v_netwk,v_que_id,v_unit_time,v_cur_ti,\
	v_min_veh_hold_ti_in_que,v_prec_round):
	
		#if the destination link is not saturated, then vehicles can move towards the destination link
		#nb_avail_places_dest_lk=\
		#v_netwk.get_di_entry_internal_links()[va_queue.get_id_associated_output_link()].get_capacity_link() - \
		#v_netwk.get_di_entry_internal_links()[va_queue.get_id_associated_output_link()].get_current_nb_veh_link()
		
		if v_nb_avail_places_dest_lk>0 :
	
			#the potential number of vehicles that can leave que from the service rate
			total_potential_nb_dep_veh= v_netwk.get_di_entry_internal_links()[v_que_id[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
			[v_que_id[0],v_que_id[1]].get_current_queue_service_rate() -\
			v_netwk.get_di_entry_internal_links()[v_que_id[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
			[v_que_id[0],v_que_id[1]].get_current_reached_service_rate()
		
		
			#the number of vehicles to be examined if the can leave according to the sat flow,  employed in a micro management
			#va_vect_nb_veh_to_exam=[nb veh to leave, time required toleave the queue]
			va_vect_nb_veh_to_exam=Global_Functions.fct_defin_nb_veh_leave_mi(\
			v_sat_flow=\
			v_netwk.get_di_entry_internal_links()[v_que_id[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
			[v_que_id[0],v_que_id[1]].get_sat_flow_queue(),v_t_unit=v_unit_time,v_round_prec=v_prec_round)
		
			#the potential number of vehicles that can leave que
			total_potential_nb_dep_veh_1=min(total_potential_nb_dep_veh,va_vect_nb_veh_to_exam[0],nb_avail_places_dest_lk)
		
			#the number of vehicles  defined by the sat flow 
			#which have remained in the que for at least the min hold time without having a veh dep event planned
			nb_veh_leave=\
			v_netwk.get_di_entry_internal_links()[v_que_ide[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()[v_que_id[0],\
			v_que_id[1]].fct_calcul_nb_of_n_veh_remained_in_que_for_min_t_hold_without_planned_dep_for_mi(t_current=v_cur_ti,\
			min_hold_time=v_min_veh_hold_ti_in_que,\
			li_vehicles=v_netwk.get_di_entry_internal_links()[v_que_id[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()[v_que_id[0],\
			v_que_id[1]].get_queue_veh()[:total_potential_nb_dep_veh_1],\
			nb_veh_to_exam=total_potential_nb_dep_veh_1,val_precision=v_prec_round)
		
			#the required time for nb_veh_leave to leave
			t_req=round(nb_veh_leave*v_unit_time/v_netwk.\
			get_di_entry_internal_links()[id_que[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()[v_que_id[0],v_que_id[1]].\
			get_sat_flow_queue(),v_prec_round)
		
			t_ev_end_veh_dep=round(v_cur_ti+t_req,v_prec_round)
			
		#if the destination link is saturated
		else:
			nb_veh_leave=0
			t_ev_end_veh_dep=None
			t_req=None
		
		return [nb_veh_leave,t_ev_end_veh_dep,v_cur_ti,t_req]
		
		
#*****************************************************************************************************************************************************************************************
	#method examining if a vehicle of a non compatible movement to the related que is crossing the intersection
	#this method returns 1 if  veh from a non compatible  phase cross the intersection, 0 otherwise
	def fct_exam_whether_veh_no_compat_movem_crosses_inters(self,val_netw,val_id_que):
		
		#if no vehicle  cross the network
		if val_netw.get_di_intersections()[val_id_que[0]].get_di_indicating_id_phase_cros_veh()=={}:
			return 0
		
		#if vehicles  cross the network
		else:
			#dict, key=id phase from which a veh is crossing the  intersection, value=1
			rep=0
			for i in val_netw.get_di_intersections()[val_id_que[0]].get_di_indicating_id_phase_cros_veh():
			
				#if the phase is  not compatible with the que
				if i not in val_netw.get_di_intersections()[val_id_que[0]].get_di_key_id_phase_value_li_compatible_phases()[val_id_que[0],val_id_que[1]]:
					rep=1
					return rep
		return rep
		
#*****************************************************************************************************************************************************************************************
	#method examining if a vehicle of a non compatible movement and a veh of a compatible movement , related to the que is crossing the intersection
	#this method returns a list, 
	#[indicator veh non compatible mov cross, indicator veh compatible mov cross,t_end_veh_dep,t_start_veh_dep_compatible_mv,departure duration]
	#indicator veh non compatible mov cross=1 if  veh from a non compatible  phase cross the intersection, 0 otherwise
	#similarly for indicator veh compatible mov cross
	#t_end_dep_compatible_mv=None if no veh of compatible movem crosses
	def fct_exam_whether_veh_no_compat_and_compat_movem_crosses_inters(self,val_netw,val_id_que):
		#if no vehicle  cross the intersection
		if val_netw.get_di_intersections()[val_netw.get_di_entry_internal_links()[val_id_que[0]].get_id_head_intersection_node()].get_di_indicating_id_phase_cros_veh()=={}:
			return [0,0,None,None,None]
		
		#if vehicles  cross the intersection
		else:
			#dict, key=id phase from which a veh is crossing the  intersection, value=1
			rep_non_comp=0
			rep_comp=0
			rep_t_end_veh_dep_compat_mv=None
			rep_t_start_veh_dep_compat_mv=None
			rep_veh_departure_duration=None
			
			#val_netw.get_di_intersections()[val_id_que[0]].get_di_indicating_id_phase_cros_veh() dict;, key=id phase
			#value=[val_t_end_veh_dep,val_start_dep_crossing_veh, duree veh depart]
			for i in val_netw.get_di_intersections()[val_id_que[0]].get_di_indicating_id_phase_cros_veh():
			
				#if the phase is  not compatible with the que: WHEN SURE THAT NON COMP MOV DO NOT LEAVE WITH COMP PHASES
				#ADD RERURN WHEN REP..=1 !!!!!!
				if i not in val_netw.get_di_intersections()[val_id_que[0]].get_di_key_id_phase_value_li_compatible_phases()[\
				val_id_que[0],val_id_que[1]]:
					rep_non_comp=1
				#if the phase is compatible with the que
				else:
					rep_comp=1
		
					rep_t_end_veh_dep_compat_mv=val_netw.get_di_intersections()[val_id_que[0]].get_di_indicating_id_phase_cros_veh()[i][0]
					rep_t_start_veh_dep_compat_mv=val_netw.get_di_intersections()[val_id_que[0]].get_di_indicating_id_phase_cros_veh()[i][1]
					rep_veh_departure_duration=val_netw.get_di_intersections()[val_id_que[0]].get_di_indicating_id_phase_cros_veh()[i][2]
					
					#return rep
		return [rep_non_comp,rep_comp,rep_t_end_veh_dep_compat_mv,rep_t_start_veh_dep_compat_mv,rep_veh_departure_duration]
		
#*****************************************************************************************************************************************************************************************

	#method defining the number of vehicles which can leave a que by the end of the hold time when an infinite link capacity is considered
	#the priority order is related to the veh arrival time at the que and the phase of the current veh crossing the intersection
	#this method returns [nb_veh_leave,t_end_dep,t_start_veh_dep,veh_dep_duration],
	#val_param_epsilon_t_completion_depart is such that: t_current<  t_star_veh_depart+epsilon x depart duration, 0<epsilon<=1
	def fct_exam_nb_veh_dep_by_end_veh_hold_prior_related_to_t_veh_arrival_infinite_lk_capacity_mi(self,\
	va_netw,id_que,va_time_unit,va_t_cur,va_min_veh_hold_time_in_que,va_round_prec,val_param_epsilon_t_completion_depart):
	
	
		nb_veh_leave=List_Explicit_Values.initialisation_value_to_zero
			
		t_end_veh_dep=None
			
		t_start_veh_dep=None
			
		veh_dep_duration=None
			

	
		#if the max allowed service rate is  reached NO veh can go, default values to return
		if va_netw.get_di_entry_internal_links()[id_que[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()[id_que[0],id_que[1]].\
		get_current_reached_service_rate() >=\
		va_netw.get_di_entry_internal_links()[id_que[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()[id_que[0],id_que[1]].\
		get_current_queue_service_rate():
			#print("HERE1")
			#print(va_netw.get_di_entry_internal_links()[id_que[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()[id_que[0],id_que[1]].\
			#get_current_reached_service_rate())
			#print(va_netw.get_di_entry_internal_links()[id_que[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()[id_que[0],id_que[1]].\
			#get_current_queue_service_rate())
		
			#if id_que[0]==21 and id_que[1]==22:
				#print("HERE1",nb_veh_leave,t_end_veh_dep,t_start_veh_dep,veh_dep_duration)
				#import sys
				#sys.exit()
			return [nb_veh_leave,t_end_veh_dep,t_start_veh_dep,veh_dep_duration]
			
		#if the max allowed service rate is not yet achieved
		else:
		
			#if the que is RT
			if va_netw.get_di_entry_internal_links()[id_que[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()[id_que[0],id_que[1]].\
			get_type_veh_queue() == Cl_Vehicle_Queue.TYPE_VEHICLE_QUEUE["right_turn"]:
				
				#rep=[nb_veh_leave,t_ev_end_veh_dep,t_start_dep,veh_dep_dur]
				rep=self.fct_defin_nb_veh_can_leave_infinite_dest_lk_capacity_mi(\
				v_netwk=va_netw,v_que_id=id_que,v_unit_time=va_time_unit,v_cur_ti=va_t_cur,\
				v_min_veh_hold_ti_in_que=va_min_veh_hold_time_in_que,v_prec_round=va_round_prec)
				#print("HERE2")
				#if id_que[0]==21 and id_que[1]==22:
					#print("HERE2",rep)
					#import sys
					#sys.exit()
				return rep
				
				#nb_veh_leave=rep[0]	
				#t_end_veh_dep=rep[1]
				#t_start_veh_dep=rep[2]
				#veh_dep_duration=rep[3]
				
				#we indicate that the dest lk is not saturated
				#state_destin_link=List_Explicit_Values.initialisation_value_to_zero
				
			
			#if the que is not a RT
			else:
				#we examine if veh of a non compatible phase cross the intersection
				#veh_non_compat_phase_cross=
				#[indicator veh non compatible mov cross, indicator veh compatible mov cross,t_end_veh_dep_duration,t_start_veh_dep_compatible_mv,\
				#veh departure duration]
				#indicator veh non compatible mov cross=1 if  veh from a non compatible  phase cross the intersection, 0 otherwise
				#similarly for indicator veh compatible mov cross
				veh_non_compat_phase_cross=self.fct_exam_whether_veh_no_compat_and_compat_movem_crosses_inters(va_netw,id_que)
				
				#if a veh of a non compatible movem cross, NO  veh can leave, on retourne les valeurs par default 
				if veh_non_compat_phase_cross[0] ==List_Explicit_Values.initialisation_value_to_one:
					#print("HERE3")
					#if id_que[0]==21 and id_que[1]==22:
						#print("HERE3",nb_veh_leave,t_end_veh_dep,t_start_veh_dep,veh_dep_duration)
						#import sys
						#sys.exit()
					return [nb_veh_leave,t_end_veh_dep,t_start_veh_dep,veh_dep_duration]
				#if no veh of a non compatible movem cross
				else:
				
					#if vehicles of a compatible phase cross
					if veh_non_compat_phase_cross[1]==List_Explicit_Values.initialisation_value_to_one:
					
						#if t current <= t_start_veh_dep+ epsilon x duree_depart,  other vehicles can  depart
						if  va_t_cur <= veh_non_compat_phase_cross[3]+ val_param_epsilon_t_completion_depart * veh_non_compat_phase_cross[4]:
							
							#we calculate the number of veh to leave
							#rep=[nb_veh_leave,t_ev_end_veh_dep,t_start_dep,veh_dep_dur]
							rep=self.fct_defin_nb_veh_can_leave_infinite_dest_lk_capacity_mi(\
							v_netwk=va_netw,v_que_id=id_que,v_unit_time=va_time_unit,v_cur_ti=va_t_cur,\
							v_min_veh_hold_ti_in_que=va_min_veh_hold_time_in_que,v_prec_round=va_round_prec)
							#print("HERE4")
							#if id_que[0]==21 and id_que[1]==22:
								#print("HERE4",rep)
								#import sys
								#sys.exit()
							return rep
							
						#if t current > t_start_veh_dep+ epsilon x duree_depart,  the vehicle will  depart, NO veh will go
						else:
							#print("HERE5")
							#if id_que[0]==21 and id_que[1]==22:
								#print("HERE5",nb_veh_leave,t_end_veh_dep,t_start_veh_dep,veh_dep_duration)
								#import sys
								#sys.exit()
							return [nb_veh_leave,t_end_veh_dep,t_start_veh_dep,veh_dep_duration]

					#if no veh cross the intersection
					else:
					
						#rep=[nb_veh_leave,t_ev_end_veh_dep,t_start_dep,veh_dep_dur]
						rep=self.fct_defin_nb_veh_can_leave_infinite_dest_lk_capacity_mi(\
						v_netwk=va_netw,v_que_id=id_que,v_unit_time=va_time_unit,v_cur_ti=va_t_cur,\
						v_min_veh_hold_ti_in_que=va_min_veh_hold_time_in_que,v_prec_round=va_round_prec)
						#print("HERE6")
						#if id_que[0]==21 and id_que[1]==22:
							#print("HERE6",rep)
							#import sys
							#sys.exit()
						return rep
					
		#return [nb_veh_leave,t_end_veh_dep,t_start_veh_dep,veh_dep_duration]
				
#*****************************************************************************************************************************************************************************************

	#method defining the number of vehicles which can leave a que by the end of the hold time when an infinite link capacity is considered
	#the priority order is related to the veh arrival time at the que and the phase of the current veh crossing the intersection
	#this method returns [nb_veh_leave,t_end_dep,t_start_dep,depart duration],
	#val_param_epsilon_t_completion_depart is such that: t_current<  t_star_veh_depart+epsilon x depart duration, 0<epsilon<=1
	def fct_exam_nb_veh_dep_by_end_veh_hold_prior_related_to_t_veh_arrival_finite_lk_capacity_mi(self,\
	va_netw,id_que,va_time_unit,va_t_cur,va_min_veh_hold_time_in_que,va_round_prec,val_param_epsilon_t_completion_depart):
	
		nb_veh_leave=List_Explicit_Values.initialisation_value_to_zero
			
		t_end_veh_dep=None
			
		t_start_veh_dep=None
			
		veh_dep_duration=None
	
		#if the max allowed service rate is  reached NO veh can go, default values to return
		if va_netw.get_di_entry_internal_links()[id_que[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()[id_que[0],id_que[1]].\
		get_current_reached_service_rate() >=\
		va_netw.get_di_entry_internal_links()[id_que[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()[id_que[0],id_que[1]].\
		get_current_queue_service_rate():
		
			return [nb_veh_leave,t_end_veh_dep,t_start_veh_dep,veh_dep_duration]
			
		#if the max allowed service rate is not yet achieved
		else:
			# the nb of available places in the destination link
			nb_avail_places_dest_lk=\
			va_netw.get_di_entry_internal_links()[va_queue.get_id_associated_output_link()].get_capacity_link() - \
			va_netw.get_di_entry_internal_links()[va_queue.get_id_associated_output_link()].get_current_nb_veh_link()
			
			#if the destination link is not saturated, then vehicles can move towards the destination link
			if nb_avail_places_dest_lk>0 :
			
				#if the que is RT
				if va_netw.get_di_entry_internal_links()[id_que[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()[id_que[0],id_que[1]].\
				get_type_veh_queue() == Cl_Vehicle_Queue.TYPE_VEHICLE_QUEUE["right_turn"]:
				
					#rep=[nb_veh_leave,t_ev_end_veh_dep,t_start_dep,veh_dep_dur]
					rep=self.fct_defin_nb_veh_can_leave_finite_dest_lk_capacity_mi(\
					v_nb_avail_places_dest_lk=nb_avail_places_dest_lk,v_netwk=va_netw,v_que_id=id_que,v_unit_time=va_time_unit,\
					v_cur_ti=va_t_cur,v_min_veh_hold_ti_in_que=va_min_veh_hold_time_in_que,v_prec_round=va_round_prec)
					
					return rep
					
					#we indicate that the dest lk is not saturated
					#state_destin_link=List_Explicit_Values.initialisation_value_to_zero

				
				#if the que is not a RT
				else:
					#we examine if veh of a non compatible phase cross the intersection
					#veh_non_compat_phase_cross=
					#[indicator veh non compatible mov cross, indicator veh compatible mov cross,t_end_veh_dep_duration,t_start_veh_dep_compatible_mv,\
					#veh departure duration]
					#indicator veh non compatible mov cross=1 if  veh from a non compatible  phase cross the intersection, 0 otherwise
					#similarly for indicator veh compatible mov cross
					veh_non_compat_phase_cross=fct_exam_whether_veh_no_compat_and_compat_movem_crosses_inters(self,va_netw,id_que)
				
					#if a veh of a non compatible movem cross, no other veh can leave,on retourne les valeurs par default 
					if veh_non_compat_phase_cross[0]==List_Explicit_Values.initialisation_value_to_one:
				
						return [nb_veh_leave,t_end_veh_dep,t_start_veh_dep,veh_dep_duration]
				
						#we indicate that the dest lk is not saturated
						#state_destin_link=List_Explicit_Values.initialisation_value_to_zero
				
					#if no veh of a non compatible movem cross
					else:
						#if vehicles of a compatible phas(s) cross
						if veh_non_compat_phase_cross[1]==List_Explicit_Values.initialisation_value_to_one:
						
							#if t current <= t_start_veh_dep+ epsilon x duree_depart,  the vehicle will  depart
							if  va_t_cur <= veh_non_compat_phase_cross[3]+ val_param_epsilon_t_completion_depart * veh_non_compat_phase_cross[4]:
							
								#we calculate the number of veh to leave
								#rep=[nb_veh_leave,t_ev_end_veh_dep,t_start_dep,veh_dep_dur]
								rep=self.fct_defin_nb_veh_can_leave_infinite_dest_lk_capacity_mi(\
								v_netwk=va_netw,v_que_id=id_que,v_unit_time=va_time_unit,v_cur_ti=va_t_cur,\
								v_min_veh_hold_ti_in_que=va_min_veh_hold_time_in_que,v_prec_round=va_round_prec)
								
								return rep
							#if t current > t_start_veh_dep+ epsilon x duree_depart,  the vehicle will  depart, NO veh will go
							else:
								return [nb_veh_leave,t_end_veh_dep,t_start_veh_dep,veh_dep_duration]
						#if no veh cross the intersection
						else:
							#rep=[nb_veh_leave,t_ev_end_veh_dep,t_start_dep,veh_dep_dur]
							rep=self.fct_defin_nb_veh_can_leave_infinite_dest_lk_capacity_mi(\
							v_netwk=va_netw,v_que_id=id_que,v_unit_time=va_time_unit,v_cur_ti=va_t_cur,\
							v_min_veh_hold_ti_in_que=va_min_veh_hold_time_in_que,v_prec_round=va_round_prec)
				
							return rep
												
							#we indicate that the dest lk is not saturated
							#state_destin_link=List_Explicit_Values.initialisation_value_to_zero
			
			#if the vehicle destination link is  saturated, no vehicle will leave
			else:
				#the nb of departing veh
				#nb_veh_leave=0
				
				#time at which the veh departure will be completed= value non defined
				#t_ev_end_veh_dep=None
				return [nb_veh_leave,t_end_veh_dep,t_start_veh_dep,veh_dep_duration]
	
					
		#return [nb_veh_leave,t_ev_end_veh_dep]
		
#*****************************************************************************************************************************************************************************************
	#method defining the number of vehicles which can leave a que by the end of the hold time
	#the priority departure order is related to the veh arrival time at the que and the phase of the current veh crossing the intersection
	#this method returns [nb_veh_leave,t_ev_end_veh_dep,t_start_dep,depart duration],
	#val_param_epsilon_t_completion_depart is such that: t_current< epsilon x t_end_duration
	def fct_exam_nb_veh_dep_by_end_veh_hold_depart_prior_related_to_t_veh_arrival_mi(self,v_netw,v_id_que,v_t_unit,\
	v_t_cur,v_min_veh_hold_time_in_que,v_round_prec,v_param_epsilon_t_completion_depart):
	
		#if the vehicle destination link is not an exit link 
		
		if v_netw.get_di_all_links()[v_id_que[1]].get_type_network_link()!=Cl_Network_Link.TYPE_NETWORK_LINK["exit"]:
			
			#if we consider infinity  capacity of the destination link
			if v_netw.get_di_entry_internal_links()[v_id_que[1]].get_capacity_link() ==-1:
				
				rep=self.fct_exam_nb_veh_dep_by_end_veh_hold_prior_related_to_t_veh_arrival_infinite_lk_capacity_mi(\
				va_netw=v_netw,id_que=v_id_que,va_time_unit=v_t_unit,va_t_cur=v_t_cur,\
				va_min_veh_hold_time_in_que=v_min_veh_hold_time_in_que,va_round_prec=v_round_prec,\
				val_param_epsilon_t_completion_depart=v_param_epsilon_t_completion_depart)
				
			#if we consider limited capacity of the destination link
			else:
				rep= self.fct_exam_nb_veh_dep_by_end_veh_hold_prior_related_to_t_veh_arrival_finite_lk_capacity_mi(\
				va_netw=v_netw,id_que=v_id_que,va_time_unit=v_t_unit,va_t_cur=v_t_cur,\
				va_min_veh_hold_time_in_que=v_min_veh_hold_time_in_que,va_round_prec=v_round_prec,\
				val_param_epsilon_t_completion_depart=v_param_epsilon_t_completion_depart)
				
		#if the  vehicle destination link is an exit link we let the vehicle(s) to go. No queues at exit links.
		else:

			rep=self.fct_exam_nb_veh_dep_by_end_veh_hold_prior_related_to_t_veh_arrival_infinite_lk_capacity_mi(\
			va_netw=v_netw,id_que=v_id_que,va_time_unit=v_t_unit,va_t_cur=v_t_cur,\
			va_min_veh_hold_time_in_que=v_min_veh_hold_time_in_que,va_round_prec=v_round_prec,\
			val_param_epsilon_t_completion_depart=v_param_epsilon_t_completion_depart)
			
		return rep

#*****************************************************************************************************************************************************************************************
	#method defining the numbr of veh that can leave from an intersection by an end veh departure event
	#the priority departure order is related to the veh arrival time at the que and the phase of the current veh crossing the intersection
	def fct_exam_nb_veh_dep_by_end_veh_depart_depart_prior_related_to_t_veh_arrival_mi_1(self,v_netw,v_id_que,v_t_unit,v_t_cur,\
	v_min_veh_hold_time_in_que,v_round_prec,v_param_epsilon_t_completion_depart):
		
		#if an infinite link capacity is been considered
		if v_netw.get_di_entry_internal_links()[v_id_que[1]].get_capacity_link() ==-1:
		
			##this method returns [...,[id_phase,nb_veh_leave,t_ev_end_veh_dep],..]  which can be [[None,0,None]] if no vehicle can go
			rep=self.fct_exam_nb_veh_dep_from_current_other_que_by_end_veh_depart_prior_related_to_t_veh_arrival_dep_infinite_lk_capacity_mi(\
			va_netwk=v_netw,va_id_queue=v_id_que,va_t_cur=v_t_cur,va_t_unit=v_t_unit,\
			va_t_min_veh_hold=v_min_veh_hold_time_in_que,va_round_prec=v_round_prec,\
			va_param_epsilon_t_completion_depart=v_param_epsilon_t_completion_depart)
		
		#if a finite link capacity is considered
		else:
			pass
			
		return rep
	

#*****************************************************************************************************************************************************************************************
	#method exam when vehicles can go from current or other que, by the end_veh_departure, when an infinite capacity of the dest link is considered
	#this method returns [...,[id_phase,nb_veh_leave,t_ev_end_veh_dep,t_start_dep,depart duration],..] or [[None,0,None,None,None]]
	#this function is called when examining if other veh can go by the end of a veh departure event nsi
	#and this function will be utilised by self.fct_treat_case_exam_veh_can_go_by_end_veh_dep_mi
	
	def fct_exam_nb_veh_dep_from_current_other_que_by_end_veh_depart_prior_related_to_t_veh_arrival_dep_infinite_lk_capacity_mi(self,\
	va_netwk,va_id_queue,va_t_cur,va_t_unit,va_t_min_veh_hold,va_round_prec,va_param_epsilon_t_completion_depart):
		
		#if the current que is a RT
		if va_netw.get_di_entry_internal_links()[id_que[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()[va_id_queue[0],va_id_queue[1]].\
		get_type_veh_queue() == Cl_Vehicle_Queue.TYPE_VEHICLE_QUEUE["right_turn"]:
		
			#if the max allowed service rate is reached
			if va_netw.get_di_entry_internal_links()[va_id_queue[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()[va_id_queue[0],va_id_queue[1]].\
			get_current_reached_service_rate() >=\
			va_netw.get_di_entry_internal_links()[va_id_que[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()[va_id_queue[0],va_id_queue[1]].\
			get_current_queue_service_rate():
				#the nb of departing veh
				#nb_veh_leave=0
				
				#time at which the veh departure will be completed= value non defined
				#t_ev_end_veh_dep=None
				#return [[va_id_queue,nb_veh_leave,t_ev_end_veh_dep]]
				return [[None,0,None,None,None]]
			
			#if the max allowed service rate is not reached
			else:
				#rep=[nb_veh_leave,t_ev_end_veh_dep,t_start_dep,veh_dep_dur]]
				rep=sel.fct_defin_nb_veh_can_leave_infinite_dest_lk_capacity_mi(\
				v_netwk=va_netw,v_que_id=id_que,v_unit_time=va_t_unit,v_cur_ti=va_t_cur,\
				v_min_veh_hold_ti_in_que=va_t_min_veh_hold,v_prec_round=va_round_prec)
				
				#nb_veh_leave=rep[0]
				
				#t_ev_end_veh_dep=rep[1]
				rep_1=[va_id_queue]
				rep_1.extend(rep)
				return rep_1
				#return [[va_id_queue,rep[0],rep[1]]]
				
			
		#if the current que is not a RT
		else:
			#if the max allowed service rate is reached
			#if va_netw.get_di_entry_internal_links()[va_id_queue[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()[va_id_queue[0],va_id_queue[1]].\
			#get_current_reached_service_rate() >=\
			#va_netw.get_di_entry_internal_links()[va_id_que[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()[va_id_queue[0],va_id_queue[1]].\
			#get_current_queue_service_rate():
			
				
			#we examine if veh from a non compatible phase crosses the intersection,
			#this method returns a list, 
			#[indicator veh non compatible mov cross, indicator veh compatible mov cross,t_end_veh_dep,t_start_veh_dep_compatible_mv,departure duration]
			rep_nc_cross=self.fct_exam_whether_veh_no_compat_and_compat_movem_crosses_inters(val_netw=va_netwk,val_id_que=va_id_queue)
				
			#if veh from non comptable phases cross the intersection
			if rep_nc_cross[0]==1:
				print("PROBLEM IN CGLOBAL_FUNCTIONS_NSI,\
				fct_exam_nb_veh_dep_from_current_other_que_by_end_veh_prior_related_to_t_veh_arrival_dep_infinite_lk_capacity_mi, val_id_que: ",\
				va_id_queue,"veh from non compatible phase crosses inters: ",rep_nc_cross[0])
				import sys
				sys.exit()

			#if  veh from a compatible phase cross the intersection
			elif rep_nc_cross[1]==1:
				
				#rep=[...,[phase id, nb veh to go, t_end_depart,t_start_dep,depart duration],...] or [[None,0,None,None,None]] 
				rep=self.fct_treat_case_exam_nb_veh_can_go_when_veh_compatible_phase_cross_infinite_lk_capacity_mi(\
				val_netw=va_netw,\
				val_ti_current=va_t_cur,val_param_epsilon_ti_completion_depart=va_param_epsilon_t_completion_depart,\
				val_start_ti_depart=rep_nc_cross[3],val_depart_dur=rep_nc_cross[4],va_queue_id=va_id_queue)
					
				return rep

			#if no veh crosses the intersection
			else:
				#rep=[...,[phase id, nb veh to go, t_end_depart,t_start_depart,depart duration],...] or [[None,0,None,None,None]] 
				rep=self.fct_treat_case_exam_nb_veh_can_go_no_veh_cross_inters_infinite_lk_capacity_mi(\
				val_netw=va_netw,val_ti_current=va_t_cur,val_ti_unit=va_t_unit,\
				val_id_intersection_node=va_netw.get_di_entry_internal_links()[va_id_queue[0]].get_id_head_intersection_node(),\
				val_min_veh_hold_ti=va_t_min_veh_hold,val_prec_round=va_round_prec)
				
				
				return rep
				
			##if the max allowed service rate is not achieved
			#else:
				
			
	
#*****************************************************************************************************************************************************************************************
	#method examining if there exists enough time for a vehicle of a compatible phase to leave when a vehicle from another compatible phase
	#is crossing the intersection 
	#it returns 1 if a vehicle can leave, zero otherwise
	def fct_examine_if_exists_enough_time_for_veh_of_comp_phase_to_leave_infinite_lk_capacity_mi(self,val_ti_current,\
	val_param_epsilon_ti_completion_depart,val_t_start_depart, val_depart_duration):
	
		if val_ti_current >val_t_start_depart+val_param_epsilon_ti_completion_depart *val_depart_duration:
			return 0
		else:
			return 1

#*****************************************************************************************************************************************************************************************
	#method treating the case when there exists enough time for a veh from a compatible mov to leave and we search which phase has the 
	#earlier arrival and service rate not reached
	#it returns a list with the phase id from which vehicles can go, None otherwise
	def fct_search_compatible_phase_with_earlier_veh_t_end_hold_1(self,v_netw,v_id_phase,v_ti_current):
	
		li_veh=[]
		#for every compatible phase with phase v_id_phase
		for i in v_netw.get_di_intersections()[v_id_phase[0]].get_di_key_id_phase_value_li_compatible_phases()[v_id_phase]:
		
			#if the max service rate of the  phase is not achieved
			if v_netw.get_di_entry_internal_links()[i[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()[i[0],i[1]].\
			get_current_reached_service_rate() >=\
			v_netw.get_di_entry_internal_links()[i[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()[i[0],i[1]].\
			get_current_queue_service_rate():
				#on ajout le premier vehicule du heap de phase i, trie par rapport a son temps end hold, dans li_veh
				#egal triee par rap a son end hold time
				if v_netw.get_di_intersections()[v_id_phase[0]].get_di_key_id_phase_value_heap_veh()[i[0],i[1]] !=[]:
					heappush(li_veh,v_netw.get_di_intersections()[v_id_phase[0]].get_di_key_id_phase_value_heap_veh()[i[0],i[1]][0])
			
		
		#if the 1st veh of the heap, has end hold time <= t_current we select this phase otherwise no vehicle from no compatible phase can go
		if li_veh[0].get_t_end_veh_hold_time_que()>v_ti_current:
			return None
		else:
			rep=[]
			#for all the phases compatible to que li_veh[0].get_veh_current_queue_location()
			for j in v_netw.get_di_intersections()[li_veh[0].get_veh_current_queue_location()[0]].get_di_key_id_phase_value_li_compatible_phases()\
			[li_veh[0].get_veh_current_queue_location()[0],li_veh[0].get_veh_current_queue_location()[1]]:
				#if there are veh in the que, we add the que id in the list
				if v_netw.get_di_intersections()[j[0],j[1]].get_di_key_id_phase_value_heap_veh()[j[0],j[1]] !=[]:
					rep.append(j)
			return rep
#*****************************************************************************************************************************************************************************************
	#method treating the case when there exists enough time for a veh from a compatible mov to leave and we search which phase has not 
	#reached the max service rate 
	#it returns a list with the phase id, compatible with the given phase and  from which the 1st vehicle has completed its min veh hold time, 
	def fct_search_compatible_phase_from_which_veh_can_go(self,v_netw,v_id_phase,v_ti_current):
	
		li_phase_id=[]
		#for every compatible phase with phase v_id_phase
		for i in v_netw.get_di_intersections()[v_id_phase[0]].get_di_key_id_phase_value_li_compatible_phases()[v_id_phase]:
		
			#if the max service rate of the  phase is not achieved
			if v_netw.get_di_entry_internal_links()[i[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()[i[0],i[1]].\
			get_current_reached_service_rate() >=\
			v_netw.get_di_entry_internal_links()[i[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()[i[0],i[1]].\
			get_current_queue_service_rate():
			
				#if the end hold time of the first veh of the heap (the one with the earlier t end hold time) <= t_current, we consider that phase
				if v_netw.get_di_intersections()[v_id_phase[0]].get_di_key_id_phase_value_heap_veh()[i[0],i[1]] !=[]:
					if v_netw.get_di_intersections()[v_id_phase[0]].get_di_key_id_phase_value_heap_veh()[i[0],i[1]][0].get_t_end_veh_hold_time_que()<=\
					v_ti_current:
						li_phase_id.append(i)
			return li_phase_id
#*****************************************************************************************************************************************************************************************
	#method searching the phase with the earlier t_end_hold time having at least one vehicle which can leave by the end hold of which the 
	#service rate is not saturated
	#it returns id_phase if found one, None otherwise
	def fct_search_phase_with_earlier_veh_t_end_hold(self,v_netw,v_id_intersection_node,v_ti_current):
		
		li_veh=[]
		#for every heap of the intersection 
		for i in v_netw.v_netw.get_di_intersections()[v_id_intersection_node].get_di_key_id_phase_value_heap_veh():
		
			#if the max service rate of the  phase is not achieved
			if v_netw.get_di_entry_internal_links()[i[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()[i[0],i[1]].\
			get_current_reached_service_rate() >=\
			v_netw.get_di_entry_internal_links()[i[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()[i[0],i[1]].\
			get_current_queue_service_rate():
			
				#if the t_end hold of the 1st veh of the related heap <= t_current
				if v_netw.get_di_intersections()[v_id_intersection_node].get_di_key_id_phase_value_heap_veh()[i[0],i[1]][0].\
				get_t_end_veh_hold_time_que()<=v_ti_current:
				
					heappush(li_veh,v_netw.get_di_intersections()[v_id_intersection_node].get_di_key_id_phase_value_heap_veh()[i[0],i[1]][0])
					
		#we return the que of the earlier arrived veh having completed its hold time and of which the max que service rate is not achieved
		if li_veh !=[]:
			return li_veh[0].get_veh_current_queue_location
		else:
			return None
		
		

#*****************************************************************************************************************************************************************************************
	#method treat the case when exam if veh can go  from compatble phases when veh  cross(es) the intersection
	#it returns [...,[phase id, nb veh to go, t_end_depart,t_start_dep,depart_dur],...] with [[None,0,None,None,None]] 
	#when no vehicle can go (case when no enough time exists for new vehs to cross)
	def fct_treat_case_exam_nb_veh_can_go_when_veh_compatible_phase_cross_infinite_lk_capacity_mi(self,val_netw,\
	val_ti_current,val_param_epsilon_ti_completion_depart,val_start_ti_depart,val_depart_dur,va_queue_id):
		#we examine if there exists enough time for a veh to cross the intersection, 
		#before the one(s) who currently cross(es) complete their departure
		
		#enough_time_for_veh_comp_phase_to_leave=1 if there exists enough time, 0 otherwise
		enough_time_for_veh_comp_phase_to_leave=\
		self.fct_examine_if_exists_enough_time_for_veh_of_comp_phase_to_leave_infinite_lk_capacity_mi(val_ti_current=val_ti_current,\
		val_param_epsilon_ti_completion_depart=val_param_epsilon_ti_completion_depart,val_t_start_depart=val_start_ti_depart,\
		val_depart_duration=val_depart_dur)
		
		#if there exists enough time for a veh to cross
		if enough_time_for_veh_comp_phase_to_leave==1:
		
			#li_id_phase_veh_to_go=[phase id for veh to go] 
			li_id_phase_veh_to_go=self.fct_search_compatible_phase_from_which_veh_can_go(\
			v_netw=val_netw,v_id_phase=va_queue_id,v_ti_current=val_ti_current)
			
			#if phases have been found from which veh can leave
			if li_id_phase_veh_to_go !=[]:
				#rep=[...,[phase id, nb veh to go, t_end_depart,t_start_dep,depart duration],...]
				rep=self.fct_calcul_nb_veh_leave_li_compatible_phases_infinite_lk_capacity(\
				valeur_li_phase_id=li_id_phase_veh_to_go,valeur_netw=va_netwk,\
				valeur_unit_time=va_t_unit,valeur_cur_ti=va_t_cur,\
				valeur_min_veh_hold_ti_in_que=va_t_min_veh_hold,valeur_prec_round=va_round_prec)
				
				return rep
			#if no phase is found from which veh can leave
			else:
				#nb_veh_leave=rep[0]
				
				#t_ev_end_veh_dep=rep[1]
				
				#return [[va_id_queue,nb_veh_leave,t_ev_end_veh_dep]]
				
				return [[None,0,None,None,None]]
		#if there is no enough time for a veh to cross
		else:
			return [[None,0,None,None,None]]
			
#*****************************************************************************************************************************************************************************************
	#method treat the case when exam if veh can go  when no veh  crosses the intersection
	#it returns [...,[phase id, nb veh to go, t_end_depart,t_start_depart, depart duration],...] if there exist phase(s) from which veh can go, 
	#[[None,0,None,None,None]] otherwise
	def fct_treat_case_exam_nb_veh_can_go_no_veh_cross_inters_infinite_lk_capacity_mi(self,val_netw,val_ti_current,val_ti_unit,\
	val_id_intersection_node,val_min_veh_hold_ti,val_prec_round):
	
		#phase with the earlier t_end_hold of which the max service rate is not yet reached and of which the 1st veh has completed its end veh hold
		#rep=id phase if one found, None otherwise
		rep=self.fct_search_phase_with_earlier_veh_t_end_hold(v_netw=val_netw,v_id_intersection_node=val_id_intersection_node,\
		v_ti_current=val_ti_current)
		
		#si il y a au moins une que (we already know that the 1st veh of the heap can go)
		if rep !=None:
			#the list of  all the compatible phases to phase rep
			li_id_phases_to_exam=val_netw.get_di_intersections()[val_id_intersection_node].get_di_key_id_phase_value_li_compatible_phases()\
			[rep[0],rep[1]]
			#we add in the list the selected que
			li_id_phases_to_exam.append(rep)
		
			#rep_1=it returns [...,[phase id, nb veh to go, t_end_depart,t_start_dep,depart duration],...], at least one elem exists in this list because of rep
			rep_1=self.fct_calcul_nb_veh_leave_li_compatible_phases_infinite_lk_capacity(\
			valeur_li_phase_id=li_id_phases_to_exam,valeur_netw=val_netw,valeur_unit_time=val_ti_unit,valeur_cur_ti=val_ti_current,\
			valeur_min_veh_hold_ti_in_que=val_min_veh_hold_ti,valeur_prec_round=val_prec_round)
			
			return rep_1
			
		
		#si aucune que existe
		else:
			return [[None,0,None,None,None]]
		

#*****************************************************************************************************************************************************************************************
	#method treat the case when we examine if veh can go by the end of a veh departure event from one or more phases
	#we return the total number of veh to go for the recording
	def fct_treat_case_exam_veh_can_go_by_end_veh_dep_mi(self,va_fct_exam_nb_dep_veh_by_end_veh_dep,\
	va_li_param_fct_exam_nb_dep_veh_by_end_veh_dep,va_netw,va_id_que,va_ev_list):
	
		#[...,[id_phase,nb_veh_leave,t_ev_end_veh_dep,t_start_depart,depart duration],..]  which can be [[None,0,None,None,None]] if no vehicle can go
		id_phase_nb_and_t_dep_veh=va_fct_exam_nb_dep_veh_by_end_veh_dep(*va_li_param_fct_exam_nb_dep_veh_by_end_veh_dep)
		
		nb_veh_to_go=0
		#print("id_phase_nb_and_t_dep_veh",id_phase_nb_and_t_dep_veh)
		#if veh can go from at least one phase
		if id_phase_nb_and_t_dep_veh[0][0] !=None:
		
			#for each phase from which veh can go
			for i in id_phase_nb_and_t_dep_veh:
				
				#if the movement is prior or minor, the we indicate the intersection that a prior or minor mv is about to cross
				if va_netw.get_di_entry_internal_links()[va_id_que[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
				[va_id_que[0],va_id_que[1]].get_type_related_phase()==Cl_Vehicle_Queue.TYPE_RELATED_PHASE["minor_mv"]:
					va_netw.get_di_intersections()[va_netw.get_di_entry_internal_links()[va_id_que[0]].\
					get_id_head_intersection_node()].set_indicator_minor_mv_cross_intersection(List_Explicit_Values.initialisation_value_to_one)
			
				elif va_netw.get_di_entry_internal_links()[id_que[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
				[va_id_que[0],id_que[1]].get_type_related_phase()==Cl_Vehicle_Queue.TYPE_RELATED_PHASE["prior_mv"]:
					va_netw.get_di_intersections()[va_netw.get_di_entry_internal_links()[va_id_que[0]].\
					get_id_head_intersection_node()].set_indicator_prior_mv_cross_intersection(List_Explicit_Values.initialisation_value_to_one)
					
				nb_veh_leave=i[1]
				nb_veh_to_go+=nb_veh_leave	
				
				#we update each departing vehicle (its state  and t start depart)
				t_end_dep=i[2]
			
				#we update each departing vehicle and we indicate  if from which phase veh cross the intersection
				self.fct_update_each_dep_veh_and_veh_heap_at_nsi(v_nb_dep_veh=nb_veh_leave,\
				v_id_que=i[List_Explicit_Values.val_first_element_of_list],v_netwk=va_netw,v_t_end_veh_depart=t_end_dep,\
				v_t_start_depart=i[3],v_depart_duration=i[4])

		
				ev_end_veh_dep=Cl_Ev_end_veh_departure_from_que.Ev_end_veh_departure_from_que(\
				val_ev_t=t_end_dep,val_id_queue_obj=i[0],val_nb_depart_veh=nb_veh_leave)
			
				#we insert the event in the event list
				ev_end_veh_dep.fct_insertion_even_in_event_list(event_list=va_ev_list,\
				message="IN CL_GLOB FUNCT_NSI IN FUNCT fct_treat_case_exam_veh_can_go_by_end_veh_dep_mi,\
				EVENT END VEH DEP_NSI HAS TIME < TIME FIRST EVENT IN THE LIST")

		
		return nb_veh_to_go
#*****************************************************************************************************************************************************************************************

	#method updating each departing vehicle and the corresponding vehicle heap of the intersection
	def fct_update_each_dep_veh_and_veh_heap_at_nsi(self,v_nb_dep_veh,v_id_que,v_netwk,v_t_end_veh_depart,\
	v_t_start_depart,v_depart_duration):
		
		#if the que is a not RT
		if v_netwk.get_di_entry_internal_links()[v_id_que[0]].get_set_veh_queue().\
		get_dict_queue_max_queue_size_et_sat_flow_queue_type_param_trav_durat()[v_id_que[0],v_id_que[1]][2]==\
		Cl_Vehicle_Queue.TYPE_VEHICLE_QUEUE["other"]:
		
			#we indicate the new state of each departing vehicle from que v_id_que
			for i in v_netwk.get_di_entry_internal_links()[v_id_que[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
			[v_id_que[0],v_id_que[1]].get_queue_veh()[:v_nb_dep_veh]:
			
				#we indicate the new state of the vehicle
				i.set_state_veh(Cl_Vehicle.TYPE_STATE_VEH["veh_dep_planned"])
			
				#we indicate the time at which the vehicle started to depart the link
				i.set_t_vehicle_started_departure_from_current_link(v_t_start_depart)
				
				#we indicate the time at which the vehicle started to depart the queue
				i.set_t_vehicle_started_departure_from_current_queue(v_t_start_depart)
			
				#we remove the vehicle from the corresponding veh heap of the non-signalised intersection, if the que is not a RT
				#if v_id_que[0]==21 and v_id_que[1]==22:
					#print("i=",i,i.get_veh_current_queue_location())
					#print("cles",v_netwk.get_di_intersections()[v_id_que[0].get_di_key_id_phase_value_heap_veh().keys())
				v_netwk.get_di_intersections()[v_netwk.get_di_entry_internal_links()[v_id_que[0]].get_id_head_intersection_node()].\
				get_di_key_id_phase_value_heap_veh()[v_id_que[0],v_id_que[1]].remove(i)
			
			#we sort the heap of vehicles		
			heapify(v_netwk.get_di_intersections()[v_netwk.get_di_entry_internal_links()[v_id_que[0]].get_id_head_intersection_node()].\
			get_di_key_id_phase_value_heap_veh()[v_id_que[0],v_id_que[1]])
		
			#print(v_netwk.get_di_intersections()[v_netwk.get_di_entry_internal_links()[v_id_que[0]].get_id_head_intersection_node()].\
			#get_di_indicating_id_phase_cros_veh().keys())
			#we update the intersection indicator showing that a veh from a phase crrosses the intersection di_indicating_id_phase_cros_veh
			#key=id phase, vaue=[val_t_end_veh_dep,val_start_dep_crossing_veh, duree veh depart]
			v_netwk.get_di_intersections()[v_netwk.get_di_entry_internal_links()[v_id_que[0]].get_id_head_intersection_node()].\
			get_di_indicating_id_phase_cros_veh()[v_id_que[0],v_id_que[1]]=(v_t_end_veh_depart,v_t_start_depart,v_depart_duration)


		
		#if the que is a RT
		else:
			#we indicate the new state of each departing vehicle from que v_id_que
			for i in v_netwk.get_di_entry_internal_links()[v_id_que[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
			[v_id_que[0],v_id_que[1]].get_queue_veh()[:v_nb_dep_veh]:
			
				#we indicate the new state of the vehicle
				i.set_state_veh(Cl_Vehicle.TYPE_STATE_VEH["veh_dep_planned"])
			
				#we indicate the time at which the vehicle started to depart the link
				i.set_t_vehicle_started_departure_from_current_link(v_t_start_depart)
			
				#we indicate the time at which the vehicle started to depart the queue
				i.set_t_vehicle_started_departure_from_current_queue(v_t_start_depart)
			
						
#*****************************************************************************************************************************************************************************************
			



























