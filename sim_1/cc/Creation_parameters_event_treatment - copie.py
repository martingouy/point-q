import Cl_Event
import Cl_Decisions
import Global_Functions
import Global_Functions_Network
import Cl_Global_Functions
import Cl_Global_Functions_nsi
import File_Sim_Name_Module_Files


#method returning a dictionary with a list of parameters for the treatment of each event type
def fct_creating_parameter_list_event_treat_event_heap(obj_simulation,obj_data_sim,obj_creation_record_files):

	dec_obj=Cl_Decisions.Decisions()
	gl_fct_obj= Cl_Global_Functions.Global_Functions()
	gl_fct_nsi_obj=Cl_Global_Functions_nsi.Global_Functions_nsi()
	
	#we examine if the split r	atios will be dynamically constructed and consequently if the link travel time related to the split algo will be/not updated
	if obj_data_sim.get_type_split_ratio_calcul() in dec_obj.fct_exam_whether_type_calc_split_ratios_requires_li_id_output_links_of_all_queues_of_link():
		
		#if the employed	algorithm computing the split ratios is based on the shortest paths
		if  obj_data_sim.get_type_split_ratio_calcul()== Cl_Decisions.TYPE_CALCUL_ROUT_PROP["dynam_based_on_t_trav_OD"]:
			#import Routing_Algos+"/"+algo_based_on_t_travel+"/"+selfish_routing as selfish_routing
			#import Routing_Algos.algo_based_on_t_travel as algo_based_on_t_travel
			#import algo_based_on_t_travel.selfish_routing as selfish_routing
			import Routing_Algos.algo_based_on_t_travel
			from Routing_Algos.algo_based_on_t_travel import selfish_routing
			val_fct_calcul_que_id_when_given_final_dest_and_path_dynamic_constructed=selfish_routing.fct_calc_queue_id
		#if the algo comput split ratios is bases on  the  probability if the path travel time (=proportionally to  trav times of all possible paths)
		elif  obj_data_sim.get_type_split_ratio_calcul()== Cl_Decisions.TYPE_CALCUL_ROUT_PROP["dynam_based_on_prob_t_trav_OD"]:
			import Routing_Algos.algo_probabilistic
			from Routing_Algos.algo_probabilistic import probabilistic_routing
			val_fct_calcul_que_id_when_given_final_dest_and_path_dynamic_constructed=probabilistic_routing.fct_calc_queue_id
		
		else:
			print("PROBLEM IN CREATION_PARAMETERS_EVENT_TREAT, TYPE COMPUT SPLIT RATIOS: ",obj_data_sim.get_type_split_ratio_calcul())
			import sys
			sys.exit()
			
		
		#if the employed	algorithm computing the split ratios is the proba version
	else:
		val_fct_calcul_que_id_when_given_final_dest_and_path_dynamic_constructed=None

	#select of the control parameters
	#if a FT will be employed
	#if obj_data_sim.get_type_control_policy()==Cl_Decisions.TYPE_CONTROL[1]:
		#the list with the param of ft control
		#val_li_file_par_ft_control=Global_Functions_Network.fct_reading_file_parameters_FT_control(name_file_to_read=\
		#File_Sim_Name_Module_Files.val_name_folder_with_control_param_files+"/"+
		#File_Sim_Name_Module_Files.val_name_file_values_ft_control,\
		#nb_comment_lines=2)
		
	#we select the function for the number and time of veh dep
	#if a macro management is employed (for the veh dep)
	#if obj_data_sim.get_type_sim_management()==Cl_Decisions.TYPE_SIMULATOR_MANAGEMENT[1]:
		#print("IN CREATION_PARAM_EVENT_TREAT, TYPE SIM MANAGEMENT:",obj_data_sim.get_type_sim_management())
		#import sys
		#sys.exit()
		#fct_calcul_nb_and_time_next_dep_veh=gl_fct_obj.fct_calcul_nb_veh_they_can_leave_at_t_current_and_assoc_end_dep_time_ma

	
	#if a micro managemen is employed (for the veh dep)
	#elif obj_data_sim.get_type_sim_management()==Cl_Decisions.TYPE_SIMULATOR_MANAGEMENT[2]:
	
	fct_calcul_nb_and_time_next_dep_veh=gl_fct_obj.fct_calcul_nb_veh_they_can_leave_at_t_current_and_assoc_end_dep_time_mi
	fct_exam_nb_dep_veh_by_end_hold_nsi=gl_fct_nsi_obj.fct_exam_nb_veh_dep_by_end_veh_hold_depart_order_related_to_t_veh_arrival_mi
	fct_calcul_nb_and_t_dep_veh_end_veh_dep_nsi=gl_fct_nsi_obj.fct_exam_nb_veh_dep_by_end_veh_depart_ev_depart_order_related_to_t_veh_arrival_mi
		
	
	#else:
		#print("PROBLEM IN CREAT_PARAM_EVENT_TREATM, TYPE_SIMULATOR_MANAGEMENT:",\
		#Cl_Decisions.TYPE_SIMULATOR_MANAGEMENT[1])
		#import sys
		#sys.exit()
		
	#select of the fct defining the travel duration
	#if fixed travel duration  is employed	
	if obj_data_sim.get_type_trav_duration_managament()==Cl_Decisions.TYPE_TRAVEL_DURAT_MANAG[1]:
		fct_calcul_travel_time=dec_obj.fct_calcul_travel_time_from_link_l_to_link_m_fixe_duration
	#if stochastic travel duration  is employed	
	elif obj_data_sim.get_type_trav_duration_managament()==Cl_Decisions.TYPE_TRAVEL_DURAT_MANAG[2]:
		fct_calcul_travel_time=dec_obj.fct_calcul_travel_time_from_link_l_to_link_m_stoch_duration
	else:
		print("PROBLEM IN CREAT_PARAM_EVENT_TREATM,TYPE_TRAVEL_DURAT_MANAG: ",\
		obj_data_sim.get_type_trav_duration_managament())
		import sys
		sys.exit()
	
	#we select the function for the number and time of veh dep
	#if a macro management is employed (for the veh dep)
	#if obj_data_sim.get_type_sim_management()==Cl_Decisions.TYPE_SIMULATOR_MANAGEMENT[1]:
		#print("IN CREATION_PARAM_EVENT_TREAT, TYPE SIM MANAGEMENT:",obj_data_sim.get_type_sim_management())
		#import sys
		#sys.exit()
		#fct_calcul_nb_and_time_next_dep_veh=gl_fct_obj.fct_calcul_nb_veh_they_can_leave_at_t_current_and_assoc_end_dep_time_ma
	
	#if a micro managemen is employed (for the veh dep)
	#elif obj_data_sim.get_type_sim_management()==Cl_Decisions.TYPE_SIMULATOR_MANAGEMENT[2]:
		#fct_calcul_nb_and_time_next_dep_veh=gl_fct_obj.fct_calcul_nb_veh_they_can_leave_at_t_current_and_assoc_end_dep_time_mi
		
	#else:
		#print("PROBLEM IN CREAT_PARAM_EVENT_TREATM, TYPE_SIMULATOR_MANAGEMENT:",\
		#Cl_Decisions.TYPE_SIMULATOR_MANAGEMENT[1])
		#import sys
		#sys.exit()
		
#*****************************************************************************************************************************************************************************************
	#the list with the parameters for the treatment of the vehicle appearance event Ev_veh_appearance, at a sign intersection event type 1
	
	li_param_fct_calcul_id_queue_chosen_by_veh=[]
	
	#lis_1=[1]
	
	li_1=[obj_simulation.get_new_veh_id(),\
	obj_data_sim.get_type_veh_final_dest(),\
	obj_simulation.get_simul_system().get_network(),\
	obj_data_sim.get_t_unit(),\
	obj_data_sim.get_min_hold_t_veh_in_que(),\
	obj_data_sim.get_precision_round_for_defin_time(),\
	obj_simulation.get_heap_even(),\
	obj_data_sim.get_creation_new_dem(),\
	obj_data_sim.get_dict_entry_link_information_prev_sim(),\
	obj_data_sim.get_dict_veh_information_prev_sim(),\
	obj_data_sim.get_dict_information_entry_lk_given_demand(),\
	obj_creation_record_files.get_file_recording_event_db(),\
	val_fct_calcul_que_id_when_given_final_dest_and_path_dynamic_constructed]
		
	
#*****************************************************************************************************************************************************************************************

	#the list with the parameters for the treatment of Cl_Ev_end_decision_next_intersection_control, event type 2
	
	
	li_2=[obj_simulation.get_simul_system().get_network(),\
	obj_data_sim.get_t_unit(),\
	obj_data_sim.get_round_precision(),\
	obj_data_sim.get_precision_round_for_defin_time(),\
	obj_simulation.get_heap_even(),\
	obj_creation_record_files.get_file_recording_event_db(),\
	obj_data_sim.get_margin_dt(),\
	obj_data_sim.get_t_simulation_duration(),\
	obj_data_sim.get_t_start_new_sim()]
	

#*****************************************************************************************************************************************************************************************
	#the list with the parameters for the treatment of Ev_new_intersection_control, even type 3
	li_3=[obj_simulation.get_simul_system().get_network(),\
	obj_data_sim.get_t_unit(),\
	fct_calcul_nb_and_time_next_dep_veh,\
	obj_data_sim.get_min_hold_t_veh_in_que(),\
	obj_data_sim.get_precision_round_for_defin_time(),\
	obj_creation_record_files.get_file_recording_event_db(),\
	obj_simulation.get_heap_even(),obj_data_sim.get_t_start_new_sim()]
	
#*****************************************************************************************************************************************************************************************
	#the list with the parameters for the treatment of the Ev_veh_departure_from_que, event type 4
	
	li_4=[obj_simulation.get_simul_system().get_network(),\
	obj_data_sim.get_t_unit(),\
	fct_calcul_travel_time,\
	obj_data_sim.get_min_hold_t_veh_in_que(),\
	fct_calcul_nb_and_time_next_dep_veh,\
	obj_data_sim.get_precision_round_for_defin_time(),\
	obj_simulation.get_heap_even(),obj_creation_record_files.get_file_recording_event_db(),\
	obj_data_sim.get_variable_indicating_finite_capacity_internal_links()]
#*****************************************************************************************************************************************************************************************
	#the list with the parameters for the treatment of Ev_veh_arrived_at_que, event type 5
	li_5=[obj_simulation.get_simul_system().get_network(),\
	obj_data_sim.get_dict_veh_information_prev_sim(),\
	obj_data_sim.get_creation_new_dem(),\
	obj_data_sim.get_min_hold_t_veh_in_que(),\
	obj_data_sim.get_precision_round_for_defin_time(),\
	obj_simulation.get_heap_even(),\
	obj_creation_record_files.get_file_recording_event_db(),\
	obj_data_sim.get_t_unit(),\
	val_fct_calcul_que_id_when_given_final_dest_and_path_dynamic_constructed]

#*****************************************************************************************************************************************************************************************
	#the list with the parameters for the treatment of Ev_veh_hold_at_que, event type 6
	li_6=[obj_simulation.get_simul_system().get_network(),\
	obj_data_sim.get_t_unit(),\
	obj_data_sim.get_min_hold_t_veh_in_que(),\
	fct_calcul_nb_and_time_next_dep_veh,\
	obj_data_sim.get_precision_round_for_defin_time(),\
	obj_simulation.get_heap_even(),\
	obj_creation_record_files.get_file_recording_event_db()]

#*****************************************************************************************************************************************************************************************
	#the list with the parameters for the treatment of Ev_veh_flow_changes, event of type 7
	li_7=[obj_simulation.get_simul_system().get_network(),obj_creation_record_files.get_file_recording_event_db()]

#*****************************************************************************************************************************************************************************************
	#the list with the parameters for the treatment of Ev_end_veh_appearance_nsi, event of type 8
	#the list with the parameters for the treatment of the vehicle appearance event Ev_veh_appearance, event type 1
	
	li_param_fct_calcul_id_queue_chosen_by_veh=[]
	
	#lis_1=[1]
	
	li_8=[obj_simulation.get_new_veh_id(),\
	obj_data_sim.get_type_veh_final_dest(),\
	obj_simulation.get_simul_system().get_network(),\
	obj_data_sim.get_t_unit(),\
	obj_data_sim.get_min_hold_t_veh_in_que(),\
	obj_data_sim.get_precision_round_for_defin_time(),\
	obj_simulation.get_heap_even(),\
	obj_data_sim.get_creation_new_dem(),\
	obj_data_sim.get_dict_entry_link_information_prev_sim(),\
	obj_data_sim.get_dict_veh_information_prev_sim(),\
	obj_data_sim.get_dict_information_entry_lk_given_demand(),\
	obj_creation_record_files.get_file_recording_event_db()]
		
#*****************************************************************************************************************************************************************************************
	#the list with the parameters for the treatment of  Ev_veh_hold_at_que_nsi, event of type 9
	
	li_9=[obj_simulation.get_simul_system().get_network(),\
	fct_exam_nb_dep_veh_by_end_hold_nsi,\
	obj_data_sim.get_t_unit(),\
	obj_data_sim.get_min_hold_t_veh_in_que(),\
	obj_data_sim.get_precision_round_for_defin_time(),\
	obj_simulation.get_heap_even(),\
	obj_creation_record_files.get_file_recording_event_db(),\
	None]
	#obj_data_sim.get_param_epsilon_t_latest_for_veh_to_leave_compatible_phase_nsi()]

#*****************************************************************************************************************************************************************************************
	#the list with the parameters for the treatment of Ev_veh_departure_from_que_nsi, evebt of type 10
	#li_10=[]
	li_10=[obj_simulation.get_simul_system().get_network(),\
	obj_data_sim.get_t_unit(),\
	fct_calcul_travel_time,\
	obj_data_sim.get_min_hold_t_veh_in_que(),\
	fct_calcul_nb_and_t_dep_veh_end_veh_dep_nsi,\
	obj_data_sim.get_precision_round_for_defin_time(),\
	obj_simulation.get_heap_even(),None,\
	#obj_data_sim.get_param_epsilon_t_latest_for_veh_to_leave_compatible_phase_nsi(),\
	obj_creation_record_files.get_file_recording_event_db()]
#*****************************************************************************************************************************************************************************************
	#the list with the parameters for the treatment of Ev_veh_arrived_at_que_nsi, evebt of type 11
	#li_11=[]
	li_11=[obj_simulation.get_simul_system().get_network(),\
	obj_data_sim.get_dict_veh_information_prev_sim(),\
	obj_data_sim.get_creation_new_dem(),\
	obj_data_sim.get_min_hold_t_veh_in_que(),\
	obj_data_sim.get_precision_round_for_defin_time(),\
	obj_simulation.get_heap_even(),\
	obj_creation_record_files.get_file_recording_event_db()]
#*****************************************************************************************************************************************************************************************		
	
	
	
	dict_p={1:li_1,2:li_2,3:li_3,4:li_4,5:li_5,6:li_6,7:li_7,8:li_8,9:li_9,10:li_10,11:li_11}
	return dict_p
#*****************************************************************************************************************************************************************************************	