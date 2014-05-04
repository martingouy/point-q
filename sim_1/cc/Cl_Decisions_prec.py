#!/usr/bin/python
import List_Explicit_Values
#import Control_Algos.Algorithm_FT_Control as Algorithm_FT_Control
#import Algorithm_FT_Control
#import Control_Algos.Algorithm_MP_Control as Algorithm_MP_Control
#import Control_Algos.Algorithm_MIXED_Control as Algorithm_MIXED_Control
#import Control_Algos.Algorithm_MP_BC_Control as Algorithm_MP_BC_Control
##import Control_Algos.Algorithm_MP_BC_Wasteful_Control as Algorithm_MP_BC_Wasteful_Control
#import Control_Algos.Algorithme_PREDEFINED_Control as Algorithme_PREDEFINED_Control
import Global_Functions
import File_Sim_Name_Module_Files
import Cl_Network_Link
import Cl_Control_Actuate
import random
import math

#TYPE_CONTROL={0:"type_control_red_clear",1:"type_control_FT", 2:"type_control_FT_with_offsets",3: "type_control_MP",4:"type_control_MIXED",\
#5:"type_control_MP_pro",6:"type_control_MP_pro_wasteful",7:"type_control_PREDEFINED"}
#TYPE_SIMULATOR_MANAGEMENT={1:"macro",2:"micro"}
TYPE_TRAVEL_DURAT_MANAG={1:"fixed_tr_dur",2:"stoch_tr_dur"}

TYPE_VEHICLE_FINAL_DESTINATION_AND_PATH={"dynamically_defined":1,"initially_defined":2}

class Decisions:

	def __init__(self):
		pass
#*****************************************************************************************************************************************************************************************
	#function defining the max number of departing vehicles from a queue
	def fct_calcul_period_service_rate_que(self,val_sat_flow_queue,val_act_duration_que,val_t_unit):
		return math.ceil(val_sat_flow_queue * val_act_duration_que/val_t_unit)

#*****************************************************************************************************************************************************************************************
			
	#method calculating the id of the queue that a vehicle chooses to join, according to the uniform prob law
	def fct_calcul_queue_chosen_by_veh_1(self,li_queue_phases):
		return random.choice(li_queue_phases)
		
		
#*****************************************************************************************************************************************************************************************
	#method returning the id of the queue chosen by a vehicle, when the queues of a linl have different probability
	#di_od_mat, dict, key=id entry_internal lk, value= [..., il dest lks,...], ATTENTION THE REAL OD MAT GIVING THE PROB OF
	#COUPLE (i,j) IS IN THE FOLDER MAT_OD, USED FOR CALCULATING MAT_OD_CUM
	#di_mat_cum_fct, duct, key=id entry-internal lk, value=[ values of cum fct]
	#i returns [ random uniform nb, id veh lk location, id dest lk]
	def fct_calcul_queue_chosen_by_veh_from_cum_fct_1(self,id_veh_lk_location, di_od_mat, di_mat_cum_fct,a=0,b=1):
	
		li=[]
		#we select a number ~uniform distribution
		x=random.uniform(a,b)
		li.append(x)
		li.append(id_veh_lk_location)
		nd_dest_trouve=0
		c=len(di_mat_cum_fct[id_veh_lk_location])
		for j in range(c):
			#print("j=",j,"di_mat_cum_fct[id_veh_lk_location][j+1]=",di_mat_cum_fct[id_veh_lk_location][j+1])
			if x < di_mat_cum_fct[id_veh_lk_location][j+1]:
				nd_dest_trouve=1
				#import sys
				#sys.exit()
				li.append(di_od_mat[id_veh_lk_location][j])
				#print(li)
				#import sys
				#sys.exit()
				return li
				
		if nd_dest_trouve==0:
			print (" PROBLEM  GC_DECISIONS ,fct_calcul_queue_chosen_by_veh_, ND_DEST_TROUVE :  ",nd_dest_trouve)
			sys.exit()

#*****************************************************************************************************************************************************************************************
	#method returning the id of the queue chosen by a vehicle, 
	#di_cum_prob: dict, key=id entry-internal link, value=[...,[cum prob, id related dest link],...]
	#value has as many elemens as the phases of the key
	#i returns [ random uniform nb, id veh lk location, id dest lk]
	def fct_calcul_queue_chosen_by_veh_from_cum_fct_2(self,id_veh_lk_location, di_cum_prob,a=0,b=1):
	
		li=[]
		#we select a number ~uniform distribution
		x=random.uniform(a,b)
		li.append(x)
		li.append(id_veh_lk_location)
		nd_dest_trouve=0
		c=len(di_mat_cum_fct[id_veh_lk_location])
		for j in range(c):
			#print("j=",j,"di_mat_cum_fct[id_veh_lk_location][j+1]=",di_mat_cum_fct[id_veh_lk_location][j+1])
			if x < di_cum_prob[id_veh_lk_location][j+1][0]:
				nd_dest_trouve=1
				#import sys
				#sys.exit()
				li.append(di_cum_prob[id_veh_lk_location][j+1][1])
				#print(li)
				#import sys
				#sys.exit()
				return li
				
		if nd_dest_trouve==0:
			print (" PROBLEM  GC_DECISIONS ,fct_calcul_queue_chosen_by_veh_, ND_DEST_TROUVE :  ",nd_dest_trouve)
			sys.exit()

#*****************************************************************************************************************************************************************************************
	#method returning the id of the queue chosen by a vehicle, 
	#di_cum_prob: dict, key=id entry-internal link, value=[...,[cum prob, id related dest link],...]
	#value has as many elemens as the phases of the key
	#i returns [ random uniform nb, id veh lk location, id dest lk]
	def fct_calcul_queue_chosen_by_veh_from_cum_fct(self,id_veh_lk_location, di_cum_prob,a=0,b=1):
	
		#print("di_cum_prob[id_veh_lk_location",di_cum_prob)
		li=[]
		#we select a number ~uniform distribution
		x=random.uniform(a,b)
		#print("DICT PROB",di_cum_prob)
		#print("RANDOM UNIF NB  TIREx",x,"id_veh_lk_location",id_veh_lk_location)
		#print()
		li.append(x)
		li.append(id_veh_lk_location)
		nd_dest_trouve=0
		#print("di_cum_prob[id_veh_lk_location]",di_cum_prob[id_veh_lk_location])
		#print()
		c=len( di_cum_prob[id_veh_lk_location])
		#if id_veh_lk_location==14:
			#print()
			#print("x=",x)
		for j in range(c):
			#print("id_veh_lk_location",id_veh_lk_location)
			#print("di_cum_prob[id_veh_lk_location]",di_cum_prob[id_veh_lk_location])
			#print()
			#print("j=",j,"di_cum_prob[id_veh_lk_location][1][0]",di_cum_prob[id_veh_lk_location][j][0])
			#print()
			#if id_veh_lk_location==14:
				#print("di_cum_prob[id_veh_lk_location][j][0]",di_cum_prob[id_veh_lk_location][j][0])
				#print("di_cum_prob[id_veh_lk_location][j][1]",di_cum_prob[id_veh_lk_location][j][1])
			if x < di_cum_prob[id_veh_lk_location][j][0]:
				nd_dest_trouve=1
				#print( di_cum_prob[id_veh_lk_location][j][0])
				#import sys
				#sys.exit()
				li.append(di_cum_prob[id_veh_lk_location][j][1])
				
				#print("li",li)
				#import sys
				#sys.exit()
				#if id_veh_lk_location==14:
					#print(li)
				return li
				
		if nd_dest_trouve==0:
			print (" PROBLEM  GC_DECISIONS ,fct_calcul_queue_chosen_by_veh_, ND_DEST_TROUVE :  ",nd_dest_trouve)
			import sys
			sys.exit()

#*****************************************************************************************************************************************************************************************
	#method returning the final destination (exit link) link chosen by the vehicle (when the related sim mode is being considered)
	def fct_calcul_exit_lk_chosen_by_veh_cas_given_final_destination(self,id_veh_entry_link,di_cum_mod,a=0,b=1):
	
		li=[]
		
		
		#we select a number  ~uniform distribution
		x=random.uniform(a,b)
		li.extend([x,id_veh_entry_link])
		#if id_veh_entry_link==13:
			#print("x",x)
		lk_dest_trouve=0
		#if id_veh_entry_link==13:
			#print("id entry link",id_veh_entry_link,"di_cum_mod[id_veh_entry_link]",di_cum_mod[id_veh_entry_link])
			
		c=len(di_cum_mod[id_veh_entry_link])
		for j in range(c):
			#if id_veh_entry_link==13:
				#print("x",x,"di_cum_mod[id_veh_entry_link][j][0]",di_cum_mod[id_veh_entry_link][j][0],x < di_cum_mod[id_veh_entry_link][j][0])
			if x < di_cum_mod[id_veh_entry_link][j][0]:
				lk_dest_trouve=1
				li.append(di_cum_mod[id_veh_entry_link][j][1])
				#if id_veh_entry_link==13:
					#print("x",x,"di_cum_mod[id_veh_entry_link][j][1]",di_cum_mod[id_veh_entry_link][j][1])
				return li
		if li_dest_trouve==0:
			print (" PROBLEM  GC_DECISIONS, fct_calcul_exit_lk_chosen_by_veh_cas_given_final_destination, ND_DEST_TROUVE :  ",\
			lk_dest_trouve)
			import sys
			sys.exit()
			

#*****************************************************************************************************************************************************************************************
	#method returning the que chosen by a vehicle when a given exit link has been attributed
	#di_key_id_entry_exit_lk_value_list_id_path_lks=dict, 
	#key=(id entry lk, id exit link), value=[.., id link to join next node, ..., id link to follow for arriving at exit lk]
	def fct_calcul_queue_chosen_by_veh_cas_given_final_destination(self,id_veh_entry_link,id_veh_current_lk_location,\
	id_final_destination_lk,\
	index_cur_veh_lk_location_ds_list,di_key_id_entry_exit_lk_value_list_id_path_lks,val_netw):
		
		
		next_dest_link= di_key_id_entry_exit_lk_value_list_id_path_lks[id_veh_entry_link,id_final_destination_lk][index_cur_veh_lk_location_ds_list]
		
		
		que=val_netw.get_di_entry_internal_links()[id_veh_current_lk_location].get_set_veh_queue().get_di_obj_veh_queue_at_link()[\
		id_veh_current_lk_location,next_dest_link]
		
		return que
		

#*****************************************************************************************************************************************************************************************
	#method returning the id of the queue chosen by a vehicle,
	#we consider that  the result previously calculated by fct fct_calcul_queue_chosen_by_veh_from_prob, 
	#so this fct returns the  que corresponding que phase
	def fct_calcul_queue_chosen_by_veh(self,val_id_veh_lk_location,id_dest_lk,val_netw):
	
		que=val_netw.get_di_entry_internal_links()[val_id_veh_lk_location].get_set_veh_queue().get_di_obj_veh_queue_at_link()[\
		val_id_veh_lk_location,id_dest_lk]
		
		#print(que.get_id_associated_link(),que.get_id_associated_output_link())
		#import sys
		#sys.exit()
			
		return que

#*****************************************************************************************************************************************************************************************

	#method calculating the travel for going from link l to link m when a vehicle is at queue(l,m)
	#t_end_current_cycle_inters_queue_lm= time at which the current cycle finishes. The current cycle is the one permitting 
	#vehicle(s) to leave
	#(l is an input link to the intersection node, m is an output link from the intersection node and consequently from link l)
	def fct_calcul_travel_time_from_link_l_to_link_m_fixe_duration_1(self,t_current, id_que,val_netw,val_prec=2):
	
		#print("id_que",id_que)
		#print("val_netw.get_di_entry_internal_links()[id_que[0]]",val_netw.get_di_entry_internal_links()[id_que[0]])
		travel_duration=val_netw.get_di_entry_internal_links()[id_que[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[id_que[0],id_que[1]].get_param_travel_durat_from_input_lk_to_output_lk()
		
		return round(t_current+travel_duration, val_prec)

#*****************************************************************************************************************************************************************************************
	#method calculating the travel for going from link l to link m when a vehicle is at queue(l,m)
	#t_end_current_cycle_inters_queue_lm= time at which the current cycle finishes. The current cycle is the one permitting 
	#vehicle(s) to leave
	#(l is an input link to the intersection node, m is an output link from the intersection node and consequently from link l)
	def fct_calcul_travel_time_from_link_l_to_link_m_fixe_duration_2(self,t_current, id_que,val_netw,val_prec=2):
	
		#print("id_que",id_que)
		
		#if the destination link is not an exit link
		if val_netw.get_di_all_links()[id_que[1]].get_type_network_link() !=Cl_Network_Link.TYPE_NETWORK_LINK["exit"]:
		
			#temps x available capacity of the destination link / capacity of the destination link
			travel_duration=round(val_netw.get_di_entry_internal_links()[id_que[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
			[id_que[0],id_que[1]].get_param_travel_durat_from_input_lk_to_output_lk() *\
			(val_netw.get_di_entry_internal_links()[id_que[1]].get_capacity_link() - \
			val_netw.get_di_entry_internal_links()[id_que[1]].get_current_nb_veh_link()) /\
			val_netw.get_di_entry_internal_links()[id_que[1]].get_capacity_link(),val_prec)
			
			
		
		#if the destination link is  an exit link
		else:
			travel_duration=List_Explicit_Values.initialisation_value_to_zero
		 
		
		return round(t_current+travel_duration, val_prec)

#*****************************************************************************************************************************************************************************************
	#method calculating the travel for going from link l to link m when a vehicle is at queue(l,m)
	#t_end_current_cycle_inters_queue_lm= time at which the current cycle finishes. The current cycle is the one permitting 
	#vehicle(s) to leave
	#(l is an input link to the intersection node, m is an output link from the intersection node and consequently from link l)
	def fct_calcul_travel_time_from_link_l_to_link_m_fixe_duration_1(self,t_current, id_que,val_netw,val_prec=2):
	
				
		#if the destination link is not an exit link
		if val_netw.get_di_all_links()[id_que[1]].get_type_network_link() !=Cl_Network_Link.TYPE_NETWORK_LINK["exit"]:
			
			#temps trajet destinatin link x available capacity of the destination link / capacity of the destination link
			travel_duration=round(val_netw.get_di_entry_internal_links()[id_que[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
			[id_que[0],id_que[1]].get_param_travel_durat_from_input_lk_to_output_lk() *\
			(val_netw.get_di_entry_internal_links()[id_que[1]].get_capacity_link() - \
			val_netw.get_di_entry_internal_links()[id_que[1]].get_current_nb_veh_link())/val_netw.get_di_entry_internal_links()\
			[id_que[1]].get_capacity_link(),val_prec)
			
			#print("travel_duration",travel_duration)
			if travel_duration<0:
				travel_duration=0
			
			
		
		#if the destination link is  an exit link
		else:
			travel_duration=List_Explicit_Values.initialisation_value_to_zero
		 
		
		return round(t_current+travel_duration, val_prec)

#*****************************************************************************************************************************************************************************************
	#method calculating the travel for going from link l to link m when a vehicle is at queue(l,m)
	#t_end_current_cycle_inters_queue_lm= time at which the current cycle finishes. The current cycle is the one permitting 
	#vehicle(s) to leave
	#(l is an input link to the intersection node, m is an output link from the intersection node and consequently from link l)
	#def fct_calcul_travel_time_from_link_l_to_link_m_fixe_duration(self,t_current, id_que,val_netw,val_prec=2):
	def fct_calcul_travel_time_from_link_l_to_link_m_fixe_duration(self,t_current, id_current_lk_location,val_netw,val_prec):
	
		#If link capacity is infinite
		if val_netw.get_di_entry_internal_links()[id_current_lk_location].get_capacity_link()<0:
			travel_duration=val_netw.get_di_entry_internal_links()[id_current_lk_location].get_param_link_travel_duration()
		
		#If link capacity is limited
		else:
			#temps trajet destinatin link x available capacity of the destination link / capacity of the destination link
			travel_duration=round((val_netw.get_di_entry_internal_links()[id_current_lk_location].get_param_link_travel_duration()*\
			(val_netw.get_di_entry_internal_links()[id_current_lk_location].get_capacity_link() - \
			val_netw.get_di_entry_internal_links()[id_current_lk_location].get_current_nb_veh_link()))/val_netw.get_di_entry_internal_links()\
			[id_current_lk_location].get_capacity_link(),val_prec)
		
		
			#travel_duration=round(val_netw.get_di_entry_internal_links()[id_que[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
			#[id_que[0],id_que[1]].get_param_travel_durat_from_input_lk_to_output_lk() *\
			#(val_netw.get_di_entry_internal_links()[id_que[1]].get_capacity_link() - \
			#val_netw.get_di_entry_internal_links()[id_que[1]].get_current_nb_veh_link())/val_netw.get_di_entry_internal_links()\
			#[id_que[1]].get_capacity_link(),val_prec)
			
			#print("travel_duration",travel_duration)
			if travel_duration<0:
				travel_duration=0
			
		return round(t_current+travel_duration, val_prec)

#*****************************************************************************************************************************************************************************************
	#method calculating the travel for going from link l to link m when a vehicle is at queue(l,m)
	#t_end_current_cycle_inters_queue_lm= time at which the current cycle finishes. The current cycle is the one permitting 
	#vehicle(s) to leave
	#(l is an input link to the intersection node, m is an output link from the intersection node and consequently from link l)
	def fct_calcul_travel_time_from_link_l_to_link_m_stoch_duration(self,t_current, id_current_lk_location,val_netw,val_prec=2):
	
		#If link capacity is infinite
		if val_netw.get_di_entry_internal_links()[id_current_lk_location].get_capacity_link()<0:
		
			travel_duration=random.lognormvariate(val_netw.get_di_travel_durat_param_mu()[id_current_lk_location],\
			val_netw.get_di_travel_durat_param_sigma()[id_current_lk_location])+val_netw.get_di_travel_durat_param_shift()[id_current_lk_location]
			
		#If link capacity is limited
		else:
			#travel_duration=random.lognormvariate(m,s)+shift
			travel_dur=random.lognormvariate(val_netw.get_di_travel_durat_param_mu()[id_current_lk_location],\
			val_netw.get_di_travel_durat_param_sigma()[id_current_lk_location])+val_netw.get_di_travel_durat_param_shift()[id_current_lk_location]
			
			#print("id_current_lk_location",id_current_lk_location,"moy",val_netw.get_di_travel_durat_param_mu()[id_current_lk_location],"sigma",
			#print("travel_du",travel_dur)
		
			travel_duration=round((travel_dur*\
			(val_netw.get_di_entry_internal_links()[id_current_lk_location].get_capacity_link() - \
			val_netw.get_di_entry_internal_links()[id_current_lk_location].get_current_nb_veh_link()))/val_netw.get_di_entry_internal_links()\
			[id_current_lk_location].get_capacity_link(),val_prec)
		
			#m=val_netw.get_di_entry_internal_links()[id_que[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
			#[id_que[0]id_que[1]].get
			#s=val_netw.get_di_entry_internal_links()[id_que[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
			#[id_que[0]id_que[1]].get
		
			#shift=val_netw.get_di_entry_internal_links()[id_que[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
			#[id_que[0]id_que[1]].get
			#travel_duration=random.lognormvariate(m,s)+shift
			
						
			if travel_duration<0:
				travel_duration=0
		#print("travel time",round(t_current+travel_duration,val_prec))
		return round(t_current+travel_duration,val_prec)
		

#*****************************************************************************************************************************************************************************************
	

	#function creating the initial network control matrix (0 everywhere)
	def fct_creat_init_ncm_1(self,val_di_id_all_links={}):
	
		dict_network_control_matrix={}

		
		#for each  link (entry, exit, and internal)
		for i in val_di_id_all_links:
			#the matrix line i will have a list of 0 elements; the number of elements of this list will be the number of links
			dict_network_control_matrix[i]=len(val_di_id_all_links)*[0]
		#print("HERECREAT NETW KEYS NCM: ",dict_network_control_matrix.keys())
		#print(dict_network_control_matrix)
		
			
		return dict_network_control_matrix

#*****************************************************************************************************************************************************************************************
	#method defining whether a vehicle can depart by the end  of the control actuation duration
	def fct_dec_whether_veh_depart_by_end_ctrl_act(self,val_t_remain,val_t_required,a=0,b=1):
		
		x=random.uniform(a,b)
		#print("x=",x)
		
		#if x<round(val_t_remain/val_t_required,val_t_round_prec):
		if x<val_t_remain/val_t_required:
			#print("x=",x,"val_t_remain",val_t_remain,"val_t_required",val_t_required,"(val_t_remain/val_t_required)",val_t_remain/val_t_required)
			#print("rep",x<val_t_remain/val_t_required)
			return List_Explicit_Values.initialisation_value_to_one
		else:
			#print("x=",x,"val_t_remain",val_t_remain,"val_t_required",val_t_required,"(val_t_remain/val_t_required)",val_t_remain/val_t_required)
			#print("rep",x<val_t_remain/val_t_required)
			return List_Explicit_Values.initialisation_value_to_zero
		
#*****************************************************************************************************************************************************************************************
	#method defining the time at which a vehicles departure will have completed
	def fct_def_time_end_veh_depart(self,val_t_current, val_duration,val_t_round,val_decimal_digit_prec=10,val_probab=0,a=0,b=1):
	
		x=random.uniform(a,b)
		
		if x<val_probab:
			return round(val_t_current + val_duration,val_t_round)
		else:
			#return math.floor((val_t_current + val_duration)*10)/10
			return math.floor((val_t_current + val_duration)*val_decimal_digit_prec)/val_decimal_digit_prec
		
#*****************************************************************************************************************************************************************************************
	
	#method returning 1 or 0 accordin as vehicle can or cannot leave the que by its arrival
	def fct_defining_whether_veh_can_leave_que_by_its_arrival(self):
		return 0


#*****************************************************************************************************************************************************************************************
	
	#function returning [ list_network_control_objects, t_end_cycle,t_cycle_duration,t_end_current_sequence_ncm,type of control]
	#val_list_file_param=[idle time L (seconds), the cycle duration T (seconsd), the actuation duration of the selected stage 50 (secs)]
	#par ex [10,60,50] , tgese values are written in file File_Sim_Name_Module_Files.val_name_file_values_mp_control
	def fct_defining_seq_nco_next_cycle_mp(self,val_netwk,val_list_file_param,val_t_end_current_ncm,val_time_unit,\
	val_t_round_precision=1,val_nb_comment_lines=1):
	
		
		
		#in a text file, we have written the idle time L (seconds), the cycle duration T (seconsd) and the actuation duration of the selected stage 50 (secs)
		#[10,60,50]  when we want only one stage within a cycle or [10,60,25] if we want two stages within a cycle, and so on.
		#li_re=Global_Functions.function_reading_file_param_netwk_control(name_file_read=\
		#File_Sim_Name_Module_Files.val_name_file_values_mp_control,\
		#nb_comment_lines=val_nb_comment_lines)
		
		#print(li_re[0])
		#print(li_re[1])
		#import sys
		#sys.exit()
		re=Control_Algos.Algorithm_MP_Control.admissible_network_control_objects_next_cycle_mp(\
		val_network=val_netwk,val_t_end_current_network_control_matrix=val_t_end_current_ncm,\
		duration_idle_time=val_list_file_param[0],duration_cycle=val_list_file_param[1],duration_ncm=val_list_file_param[2],\
		val_t_unit=val_time_unit,val_t_round_prec=val_t_round_precision)
		
		
		return re


#*****************************************************************************************************************************************************************************************


	#method returning [ list_network_control_objects, t_end_cycle,t_cycle_duration,t_end_current_sequence_ncm,type of next network control]
	#val_list_file_param= [ [param of ft], [param of mp]]
	def fct_defining_seq_nco_next_cycle_mixed(self,val_currently_employed_control,\
	val_netwk,val_list_file_param,val_t_end_current_ncm,val_time_unit,val_t_round_precision=1,val_nb_comment_lines=1):
	
		
		re=Control_Algos.Algorithm_MIXED_Control.admissible_network_control_objects_next_cycle_mixed_control(\
		val_cur_employed_control=val_currently_employed_control,val_netw=val_netwk, \
		val_li_ncm=val_netwk.get_network_control_mat_obj().get_li_dict_network_control_matrices(),\
		vat_t_end_current_ncm=val_t_end_current_ncm,\
		val_li_duration_each_ncm=val_list_file_param[0],\
		val_dur_idle_time=val_list_file_param[1][0],val_dur_cycle=val_list_file_param[1][1],\
		val_duration_ncm=val_list_file_param[1][2],\
		val_time_unit=val_time_unit,val_time_round_prec=val_t_round_precision)
		
		return re
#*****************************************************************************************************************************************************************************************
	#function returning [ list_network_control_objects, t_end_cycle,t_cycle_duration,t_end_current_sequence_ncm,type of control]
	#val_list_file_param=[idle time L (seconds), the cycle duration T (seconsd), the actuation duration of the selected stage 50 (secs)]
	#par ex [10,60,50] , tgese values are written in file File_Sim_Name_Module_Files.val_name_file_values_mp_control
	#val_li_id_surveyed_phase=[2,3] if we survey the size of queue [2,3]
	def fct_defining_seq_nco_next_cycle_mp_bc(self,val_netwk,val_list_file_param,val_t_end_current_ncm,\
	val_name_netwk_data_folder,val_time_unit,\
	val_t_round_precision,val_nb_comment_lines=1):
	
		
		
		#in a text file, we have written the idle time L (seconds), the cycle duration T (seconsd) and the actuation duration of the selected stage 50 (secs)
		#[10,60,50]  when we want only one stage within a cycle or [10,60,25] if we want two stages within a cycle, and so on.
		#li_re=Global_Functions.function_reading_file_param_netwk_control(name_file_read=\
		#File_Sim_Name_Module_Files.val_name_file_values_mp_control,\
		#nb_comment_lines=val_nb_comment_lines)
		
		#print(li_re[0])
		#print(li_re[1])
		#import sys
		#sys.exit()
		re=Algorithm_MP_BC_Control.admissible_network_control_objects_next_cycle_mp_bc(\
		val_network=val_netwk,val_t_end_current_network_control_matrix=val_t_end_current_ncm,\
		duration_idle_time=val_list_file_param[0],duration_cycle=val_list_file_param[1],duration_ncm=val_list_file_param[2],\
		val_name_network_data_folder=val_name_netwk_data_folder,\
		val_t_unit=val_time_unit,val_t_round_prec=val_t_round_precision)
		
		
		return re


#*****************************************************************************************************************************************************************************************
	#function returning [ list_network_control_objects, t_end_cycle,t_cycle_duration,t_end_current_sequence_ncm,type of control]
	#val_list_file_param=[idle time L (seconds), the cycle duration T (seconsd), the actuation duration of the selected stage 50 (secs)]
	#par ex [10,60,50] , tgese values are written in file File_Sim_Name_Module_Files.val_name_file_values_mp_control
	def fct_defining_seq_nco_next_cycle_mp_bc_wasteful(self,val_netwk,val_list_file_param,val_t_end_current_ncm,\
	val_name_netwk_data_folder,val_time_unit,\
	val_t_round_precision,val_nb_comment_lines=1):
	
		
		
		#in a text file, we have written the idle time L (seconds), the cycle duration T (seconsd) and the actuation duration of the selected stage 50 (secs)
		#[10,60,50]  when we want only one stage within a cycle or [10,60,25] if we want two stages within a cycle, and so on.
		#li_re=Global_Functions.function_reading_file_param_netwk_control(name_file_read=\
		#File_Sim_Name_Module_Files.val_name_file_values_mp_control,\
		#nb_comment_lines=val_nb_comment_lines)
		
		#print(li_re[0])
		#print(li_re[1])
		#import sys
		#sys.exit()
		re=Algorithm_MP_BC_Wasteful_Control.admissible_network_control_objects_next_cycle_mp_bc_wasteful(\
		val_network=val_netwk,val_t_end_current_network_control_matrix=val_t_end_current_ncm,\
		duration_idle_time=val_list_file_param[0],duration_cycle=val_list_file_param[1],duration_ncm=val_list_file_param[2],\
		val_name_network_data_folder=val_name_netwk_data_folder,\
		val_t_unit=val_time_unit,val_t_round_prec=val_t_round_precision)
		
		
		return re


#*****************************************************************************************************************************************************************************************
	#function returning [ list_network_control_objects, t_end_cycle,t_cycle_duration,t_end_current_sequence_ncm]
	#val_list_file_param=[list_duration_ncm including L], [ 19,6,19,8,8,10],
	#written in file  with the name File_FT_Control_Alg_Param
	def fct_defining_predefined_nco_next_period(self,val_netwk,val_list_file_param_pred_ctrl,\
	val_t_end_current_ncm,val_time_unit,val_t_round_precision,val_nb_comment_lines=1):
	
		#the duration of each network control matrix, the phases that will be actuated during each network control matrix, are wirtten in a text file
		#coinained in this folder, with the name File_FT_Control_Alg_Param.
		#this method returns [ list_duration_ncm] 
		#ex [ 2,2,30  ]
		#li_re=Global_Functions.function_reading_file_param_netwk_control(name_file_read=File_Sim_Name_Module_Files.val_name_file_values_ft_control,\
		#nb_comment_lines=val_nb_comment_lines)
		
		
		
		#print(li_re[0])
		#print(li_re[1])
		#import sys
		#sys.exit()
	
		
		re=Algorithme_PREDEFINED_Control.admissible_network_control_objects_next_cycle_predefined(\
		val_netw_control_matrix=val_netwk.get_network_control_mat_obj().get_li_dict_network_control_matrices()[0],\
		val_t_end_current_network_control_matrix=val_t_end_current_ncm,\
		val_dur_ncm=val_list_file_param_pred_ctrl[0],\
		val_t_unit=val_time_unit,val_t_round_prec=val_t_round_precision)
		
		#we delete the 1st ncm since it is the one currently employed
		val_netwk.get_network_control_mat_obj().get_li_dict_network_control_matrices().remove(\
		val_netwk.get_network_control_mat_obj().get_li_dict_network_control_matrices()[0])
		
		#we delete the 1st element if the lust of the actuation duration of each ncm
		val_list_file_param_pred_ctrl.remove(val_list_file_param_pred_ctrl[0])
		
		
		
		return re
	
#*****************************************************************************************************************************************************************************************
	#method examining whether the ctrl decision shoudl be updated in the intersection by the veh appearance
	#we return 1 if the  decision should be updated (case when  all  ques of the actuat stage has flow <fmin or
	#when the selected queue by a veh  is actuated and has flow < fmin), 0 otherwise
	#val_t_ctrl_revision_if_decided= variable indicating the time at which the cotnrol will be revised if  it is so decided (that  will be the t of ev_end_decision)
	def fct_exam_whether_ctrl_decision_should_be_updated_when_record_flux_with_ctrls_without_limited_continuous_actuation_duration(self,\
	val_intersection,val_net,val_min_allowed_flow_depart_link,val_t_ctrl_revision_if_decided):
	
				
		#if we are in red clearance
		if val_intersection.get_intersection_control_obj().get_type_control()==Cl_Control_Actuate.TYPE_CONTROL[0]:
			
			return 0
		#if we are not in red clearance
		else:
			
			#if no control revision request is made for that time and no new control is going to be applied at this time 
			if (val_intersection.get_t_last_request_ctrl_revision_when_flux_monitoring()==None and\
			val_intersection.get_li_t_start_new_inters_control_when_flux_monitoring()==[]):
			
				if val_intersection.\
				fct_examing_existence_que_actuates_stage_with_flow_sup_given_value(\
				val_network=val_net,val_fmin=val_min_allowed_flow_depart_link)==1:
					return 0
				return 1
			#if	 a control request is already made for the same time then we do not ask for a second one
			else:
				return 0
	
#*****************************************************************************************************************************************************************************************
	#method examining whether the ctrl decision shoudl be updated in the intersection by the veh appearance
	#when the employed contols requires sensor monitoring and imposes a limited continuous actuation durations for the stages (ex FA with max green)
	#we return 1 if the  decision should be updated (case when  all  ques of the actuat stage has flow <fmin or
	#when the selected queue by a veh  is actuated and has flow < fmin), 0 otherwise
	#val_t_ctrl_revision_if_decided= variable indicating the time at which the cotnrol will be revised if  it is so decided (that  will be the t of ev_end_decision)
	def fct_exam_whether_ctrl_decision_should_be_updated_when_record_flux_with_ctrls_with_limited_continuous_actuation_duration(self,\
	val_intersection,val_net,val_min_allowed_flow_depart_link,val_t_ctrl_revision_if_decided,val_t_start_ctrl_if_decided):
		#print("IN CL DECISIONS")
		#print("val_t_start_ctrl_if_decided",val_t_start_ctrl_if_decided)
		#print("T CTRL UPDATE:",val_intersection.get_intersection_control_obj().get_t_update_ctrl())
		#print("TYPE CTRL",val_intersection.get_intersection_control_obj().get_type_control())
		#print("NODE ID",val_intersection.get_id_node())
		#print("T LAST EQUEST",val_intersection.get_t_last_request_ctrl_revision_when_flux_monitoring())
		#print("LI T START NEW ITERS CTRL:",val_intersection.get_li_t_start_new_inters_control_when_flux_monitoring())
		#print()
		#if we are in red clearance
		if val_intersection.get_intersection_control_obj().get_type_control()==Cl_Control_Actuate.TYPE_CONTROL[0]:
			return 0
		#if we are not in red clearance
		else:
			#if no control revision request is made for the time we will ask for the ctrl revision  and no new control is going to be applied at this time 
			#and it is not the time of the ctrl update because of the max duration
			if val_intersection.get_t_last_request_ctrl_revision_when_flux_monitoring()==None and\
			val_intersection.get_li_t_start_new_inters_control_when_flux_monitoring()==[] and \
			val_intersection.get_intersection_control_obj().get_t_update_ctrl()>val_t_start_ctrl_if_decided:
			
				#if there is at least one queue of the actuat stage having flow > f min, we do not revise the control
				#for j in val_netw.get_di_intersections()[val_netw.get_di_entry_internal_links()[self._id_entry_link].\
					#get_id_head_intersection_node()].get_di_stages_sign_intersection()[\
					#val_netw.get_di_intersections()[val_netw.get_di_entry_internal_links()[self._id_entry_link].\
					#get_id_head_intersection_node()].get_intersection_control_obj().get_id_actuated_stage()]:
		
						##if there is at least one  queue in the link, having flows > f_min, we do not need to update the  decision
						#if val_netw.get_di_all_links()[j[0]].fct_examing_existence_que_actuates_stage_with_flow_sup_given_value(\
						#val_network=val_netw,val_fmin=val_min_allowed_flow_depart_link)==1:
							#return 0
				if val_intersection.\
				fct_examing_existence_que_actuates_stage_with_flow_sup_given_value(\
				val_network=val_net,val_fmin=val_min_allowed_flow_depart_link)==1:
					return 0
				return 1
			#if	 a control request is already made for the same time then we do not ask for a second one
			else:
				return 0
	
#*****************************************************************************************************************************************************************************************


#a=Decisions()
#li= a.fct_calcul_max_nb_departing_veh_que()
#print(li)




