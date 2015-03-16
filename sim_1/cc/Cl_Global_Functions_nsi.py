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
#*****************************************************************************************************************************************************************************************
	#this method returns [nb_veh_leave,t_ev_end_veh_dep,t_start_dep,depart duration],
	def fct_exam_nb_veh_dep_by_end_veh_hold_depart_order_related_to_t_veh_arrival_mi(self):
		#return [0,None,None,None,None]
		return [0,-10000,None,None,None]
#*****************************************************************************************************************************************************************************************
	#this method returns [...,[id_phase,nb_veh_leave,t_ev_end_veh_dep,t_start_dep,depart duration],..] or [[None,0,None,None,None]]
	def	fct_exam_nb_veh_dep_from_current_other_que_by_end_veh_depart_order_related_to_t_veh_arrival_dep_infinite_lk_capacity_mi(self):
		pass
#*****************************************************************************************************************************************************************************************
	#this method returns [...,[id_phase,nb_veh_leave,t_ev_end_veh_dep,t_start_dep,depart duration],..] or [[None,0,None,None,None]]
	def	fct_exam_nb_veh_dep_from_current_other_que_by_end_veh_depart_order_related_to_t_veh_arrival_dep_finite_lk_capacity_mi(self):
		pass
#*****************************************************************************************************************************************************************************************
	#this method returns [...,[id_phase,nb_veh_leave,t_ev_end_veh_dep,t_start_dep,depart duration],..] or [[None,0,None,None,None]]
	def fct_exam_nb_veh_dep_by_end_veh_depart_ev_depart_order_related_to_t_veh_arrival_mi(self):
		return [[None,0,None,None,None]]
#*****************************************************************************************************************************************************************************************
#*****************************************************************************************************************************************************************************************
#*****************************************************************************************************************************************************************************************


#*****************************************************************************************************************************************************************************************
	

			



























