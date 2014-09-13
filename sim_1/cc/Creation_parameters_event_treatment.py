import Cl_Event
import Cl_Decisions
import Global_Functions
import Global_Functions_Network
import Cl_Global_Functions
import Cl_Global_Functions_nsi
import File_Sim_Name_Module_Files
import  List_Explicit_Values
import Cl_Control_Actuate
import Cl_Ev_veh_appearance
import Cl_Ev_end_veh_departure_from_que
import Cl_Ev_veh_arrived_at_que



#*************************************************************************************************************************************************************************************
#method creating returning a list with the parameters of a veh appearance event

def fct_define_param_ev_veh_ap(val_obj_simulation,val_obj_data_sim,val_obj_creation_record_files):

	#obj_ev_veh_ap=Cl_Ev_veh_appearance.Ev_veh_appearance()

	#if a new demand is considered
	if val_obj_data_sim.get_creation_new_dem()==List_Explicit_Values.initialisation_value_to_one:
		
	
		#if the path will dynam be computed (no predefined final destination)
		if val_obj_data_sim.get_type_veh_final_dest()==Cl_Decisions.TYPE_VEHICLE_FINAL_DESTINATION_AND_PATH["dynamically_defined"]:
		
			
		
			#val_fct=obj_ev_veh_ap.fct_treat_case_new_demand_final_dest_and_path_dynam_defined
			val_key_fct_in_dict=1
			
			val_li_parm_fct=[val_obj_simulation.get_new_veh_id(),val_obj_simulation.get_simul_system().get_network(),\
			val_obj_data_sim.get_type_veh_final_dest(),val_obj_data_sim.get_min_hold_t_veh_in_que(),\
			val_obj_data_sim.get_precision_round_for_defin_time(),val_obj_simulation.get_heap_even(),\
			val_obj_creation_record_files.get_file_recording_event_db(),\
			List_Explicit_Values.initialisation_value_to_one]
			
			
			return[val_key_fct_in_dict,val_li_parm_fct]
		
		#if  we have  OD and given path
		elif val_obj_data_sim.get_type_veh_final_dest()==Cl_Decisions.TYPE_VEHICLE_FINAL_DESTINATION_AND_PATH["initially_defined_and_path_given"]:
			
		
			#val_fct=obj_ev_veh_ap.fct_treat_case_new_demand_final_dest_and_path_initial_defined
			
			val_key_fct_in_dict=2
			
			val_li_parm_fct=[val_obj_simulation.get_new_veh_id(),val_obj_simulation.get_simul_system().get_network(),\
			val_obj_data_sim.get_type_veh_final_dest(),val_obj_data_sim.get_min_hold_t_veh_in_que(),\
			val_obj_data_sim.get_precision_round_for_defin_time(),val_obj_simulation.get_heap_even(),\
			val_obj_creation_record_files.get_file_recording_event_db(),\
			List_Explicit_Values.initialisation_value_to_one]
			
			return[val_key_fct_in_dict,val_li_parm_fct]
		
		#if we have OD and dyn computed path 
		elif val_obj_data_sim.get_type_veh_final_dest()==Cl_Decisions.TYPE_VEHICLE_FINAL_DESTINATION_AND_PATH["initially_defined_and_path_dyn_constructed"]:
		
		
			#selection of the rout algo
			if  val_obj_data_sim.get_type_rout_algo_when_given_od_and_dyn_computed_paths()==Cl_Decisions.TYPE_CALCUL_ROUT_PROP["dynam_based_on_t_trav_OD"]:
				
			
				import Routing_Algos.algo_based_on_t_travel
				from Routing_Algos.algo_based_on_t_travel import selfish_routing
				val_fct_calcul_que_id_when_given_final_dest_and_path_dynamic_constructed=selfish_routing.fct_calc_queue_id
				
			#if the path algo  is based on  the  probability if the path travel time (=proportionally to  trav times of all possible paths)
			elif val_obj_data_sim.get_type_rout_algo_when_given_od_and_dyn_computed_paths()== Cl_Decisions.TYPE_CALCUL_ROUT_PROP["dynam_based_on_prob_t_trav_OD"]:
			
				import Routing_Algos.algo_probabilistic
				from Routing_Algos.algo_probabilistic import probabilistic_routing
				val_fct_calcul_que_id_when_given_final_dest_and_path_dynamic_constructed=probabilistic_routing.fct_calc_queue_id
		
			else:
				print("PROBLEM IN CREATION_PARAMETERS_EVENT_TREAT, TYPE ROUT ALGO: ",val_obj_data_sim.get_type_rout_algo_when_given_od_and_dyn_computed_paths())
				import sys
				sys.exit()
				
			#val_fct=obj_ev_veh_ap.fct_treat_case_new_demand_final_dest_initial_defined_path_dyn_computed
			val_key_fct_in_dict=3
			
			val_li_parm_fct=[val_obj_simulation.get_new_veh_id(),val_obj_simulation.get_simul_system().get_network(),\
			val_obj_data_sim.get_type_veh_final_dest(),val_obj_data_sim.get_min_hold_t_veh_in_que(),\
			val_obj_data_sim.get_precision_round_for_defin_time(),val_obj_simulation.get_heap_even(),\
			val_obj_creation_record_files.get_file_recording_event_db(),\
			val_fct_calcul_que_id_when_given_final_dest_and_path_dynamic_constructed,\
			List_Explicit_Values.initialisation_value_to_one]
			
			return[val_key_fct_in_dict,val_li_parm_fct]
			
		#if we have a mixed management and the routing is either dynamical or  with od and given path
		elif val_obj_data_sim.get_type_veh_final_dest()==Cl_Decisions.TYPE_VEHICLE_FINAL_DESTINATION_AND_PATH["mixed_dyndefined_or_odwithgiven_path"]:
		
			val_key_fct_in_dict=7
			
			
			
			val_li_parm_fct=[\
			val_obj_simulation.get_new_veh_id(),val_obj_simulation.get_simul_system().get_network(),\
			val_obj_data_sim.get_type_veh_final_dest(),val_obj_data_sim.get_min_hold_t_veh_in_que(),\
			val_obj_data_sim.get_precision_round_for_defin_time(),val_obj_simulation.get_heap_even(),\
			val_obj_creation_record_files.get_file_recording_event_db(),\
			List_Explicit_Values.initialisation_value_to_one]
			
			
			return[val_key_fct_in_dict,val_li_parm_fct]
			
			
			
	
	#if a previously generated demand is considered
	elif val_obj_data_sim.get_creation_new_dem()==List_Explicit_Values.initialisation_value_to_zero:
		
	
		#if the path will dynam be computed (no predefined final destination)
		if val_obj_data_sim.get_type_veh_final_dest()==Cl_Decisions.TYPE_VEHICLE_FINAL_DESTINATION_AND_PATH["dynamically_defined"]:
		
			#val_fct=obj_ev_veh_ap.fct_treat_case_previous_demand_final_dest_and_path_dyn_defined
			val_key_fct_in_dict=4
			
			val_li_parm_fct=[val_obj_simulation.get_simul_system().get_network(),\
			val_obj_data_sim.get_type_veh_final_dest(),val_obj_data_sim.get_min_hold_t_veh_in_que(),\
			val_obj_data_sim.get_precision_round_for_defin_time(),val_obj_simulation.get_heap_even(),\
			val_obj_creation_record_files.get_file_recording_event_db(),\
			val_obj_data_sim.get_dict_entry_link_information_prev_sim(),\
			val_obj_data_sim.get_dict_veh_information_prev_sim(),\
			List_Explicit_Values.initialisation_value_to_one]
			
		
			return[val_key_fct_in_dict,val_li_parm_fct]
		
		#if the final destination is given by OD and the path is given or dyn computed
		elif val_obj_data_sim.get_type_veh_final_dest()==Cl_Decisions.TYPE_VEHICLE_FINAL_DESTINATION_AND_PATH["initially_defined_and_path_given"] or \
		val_obj_data_sim.get_type_veh_final_dest()==Cl_Decisions.TYPE_VEHICLE_FINAL_DESTINATION_AND_PATH["initially_defined_and_path_dyn_constructed"]:
			#if the purpose  of the implem is to evaluate the signal control policy
			if val_obj_data_sim.get_reason_employing_previous_demand()==Cl_Decisions.TYPE_REASON_EMPLOYING_PREVIOUS_DEMAND["CTRL_EVAL"]:
			
				#val_fct=obj_ev_veh_ap.fct_treat_case_veh_appear_previous_demand_final_dest_given_ctrl_eval
				val_key_fct_in_dict=5
				
				val_li_parm_fct=[val_obj_simulation.get_simul_system().get_network(),\
				val_obj_data_sim.get_type_veh_final_dest(),val_obj_data_sim.get_min_hold_t_veh_in_que(),\
				val_obj_data_sim.get_precision_round_for_defin_time(),val_obj_simulation.get_heap_even(),\
				val_obj_creation_record_files.get_file_recording_event_db(),\
				val_obj_data_sim.get_dict_entry_link_information_prev_sim(),\
				val_obj_data_sim.get_dict_veh_information_prev_sim(),\
				List_Explicit_Values.initialisation_value_to_one]
				
				return[val_key_fct_in_dict,val_li_parm_fct]
			
			#if the purpose of the implement is to evaluate the rout algo
			elif val_obj_data_sim.get_reason_employing_previous_demand()==Cl_Decisions.TYPE_REASON_EMPLOYING_PREVIOUS_DEMAND["ROUT_ALGO_EVAL"]:
			
				#selection of the rout algo
				if  val_obj_data_sim.get_type_rout_algo_when_given_od_and_dyn_computed_paths()==Cl_Decisions.TYPE_CALCUL_ROUT_PROP["dynam_based_on_t_trav_OD"]:
			
					import Routing_Algos.algo_based_on_t_travel
					from Routing_Algos.algo_based_on_t_travel import selfish_routing
					val_fct_calcul_que_id_when_given_final_dest_and_path_dynamic_constructed=selfish_routing.fct_calc_queue_id
				
				#if the algo comput split ratios is bases on  the  probability if the path travel time (=proportionally to  trav times of all possible paths)
				elif val_obj_data_sim.get_type_rout_algo_when_given_od_and_dyn_computed_paths()== Cl_Decisions.TYPE_CALCUL_ROUT_PROP["dynam_based_on_prob_t_trav_OD"]:
			
					import Routing_Algos.algo_probabilistic
					from Routing_Algos.algo_probabilistic import probabilistic_routing
					val_fct_calcul_que_id_when_given_final_dest_and_path_dynamic_constructed=probabilistic_routing.fct_calc_queue_id
		
				else:
					print("PROBLEM IN CREATION_PARAMETERS_EVENT_TREAT, TYPE ROUT ALGO: ",val_obj_data_sim.get_type_rout_algo_when_given_od_and_dyn_computed_paths())
					import sys
					sys.exit()
			
				#val_fct=obj_ev_veh_ap.fct_treat_case_veh_appear_previous_demand_final_dest_given_rout_algo_eval
				val_key_fct_in_dict=6
				
				val_li_parm_fct=[val_obj_simulation.get_simul_system().get_network(),\
				val_obj_data_sim.get_type_veh_final_dest(),val_obj_data_sim.get_min_hold_t_veh_in_que(),\
				val_obj_data_sim.get_precision_round_for_defin_time(),val_obj_simulation.get_heap_even(),\
				val_obj_creation_record_files.get_file_recording_event_db(),\
				val_obj_data_sim.get_dict_entry_link_information_prev_sim(),\
				val_obj_data_sim.get_dict_veh_information_prev_sim(),\
				val_fct_calcul_que_id_when_given_final_dest_and_path_dynamic_constructed,\
				List_Explicit_Values.initialisation_value_to_one]
				
				return[val_key_fct_in_dict,val_li_parm_fct]
				#if none of the previous case
			
		#if a mixed management is employed and a dynam routing is employed or  the final destination is given by OD and the path is given 
		elif val_obj_data_sim.get_type_veh_final_dest()==Cl_Decisions.TYPE_VEHICLE_FINAL_DESTINATION_AND_PATH["mixed_dyndefined_or_odwithgiven_path"]:
			
			
			val_key_fct_in_dict=8
				
			val_li_parm_fct=[val_obj_simulation.get_simul_system().get_network(),\
			val_obj_data_sim.get_type_veh_final_dest(),val_obj_data_sim.get_min_hold_t_veh_in_que(),\
			val_obj_data_sim.get_precision_round_for_defin_time(),val_obj_simulation.get_heap_even(),\
			val_obj_creation_record_files.get_file_recording_event_db(),\
			val_obj_data_sim.get_dict_entry_link_information_prev_sim(),\
			val_obj_data_sim.get_dict_veh_information_prev_sim(),\
			List_Explicit_Values.initialisation_value_to_one]
				
			return[val_key_fct_in_dict,val_li_parm_fct]
			
	
	#if a given demand is considered
	elif val_obj_data_sim.get_creation_new_dem()==List_Explicit_Values.initialisation_value_to_minus_one:
		print("A FAIRE")
		import sys
		sys.exit()
	
	#if none of the previous cases
	else:
		print("PROBLEM IN CREATION PARAM EVENT  TREATM, IN FCT fct_define_fct_and_param_veh_ap_event, DEMAND TYPE",\
		val_obj_data_sim.get_creation_new_dem())
		import sys
		sys.exit()

#*************************************************************************************************************************************************************************************
#method creating returning a list with the parameters of an event end veh departure
def fct_define_param_ev_end_veh_dep(val_fct_calcul_nb_and_time_next_dep_veh,val_obj_simulation,val_obj_data_sim,val_fct_calcul_travel_time,\
val_obj_creation_record_files):

	#obj_ev_end_veh_dep=Cl_Ev_end_veh_departure_from_que.Ev_end_veh_departure_from_que()
	
	#fct_calcul_nb_and_time_next_dep_veh=val_gl_fct_obj.fct_calcul_nb_veh_they_can_leave_at_t_current_and_assoc_end_dep_time_mi
	
	
	
	#if finite link capacities are considered
	if val_obj_data_sim.get_variable_indicating_finite_capacity_internal_links()==List_Explicit_Values.initialisation_value_to_one:
		
	
		#val_fct=obj_ev_end_veh_dep.fct_treat_event_case_finite_lk_capacity
		val_key_fct_in_dict=1
		
		val_li_parm_fct=[val_obj_simulation.get_simul_system().get_network(),val_obj_data_sim.get_t_unit(),\
		val_fct_calcul_nb_and_time_next_dep_veh,List_Explicit_Values.initialisation_value_to_one,\
		val_obj_data_sim.get_precision_round_for_defin_time(),val_obj_simulation.get_heap_even(),\
		val_fct_calcul_travel_time,val_obj_data_sim.get_min_hold_t_veh_in_que(),\
		val_obj_creation_record_files.get_file_recording_event_db()]
		
		return [val_key_fct_in_dict,val_li_parm_fct]
		
	#if infinite link capacities are considered
	elif val_obj_data_sim.get_variable_indicating_finite_capacity_internal_links()==List_Explicit_Values.initialisation_value_to_zero:
	
		#val_fct=obj_ev_end_veh_dep.fct_treat_event_case_infinite_lk_capacity
		val_key_fct_in_dict=2
		
		val_li_parm_fct=[val_obj_simulation.get_simul_system().get_network(),val_obj_data_sim.get_t_unit(),\
		val_fct_calcul_nb_and_time_next_dep_veh,
		val_obj_data_sim.get_precision_round_for_defin_time(),val_obj_simulation.get_heap_even(),\
		val_fct_calcul_travel_time,val_obj_data_sim.get_min_hold_t_veh_in_que(),\
		val_obj_creation_record_files.get_file_recording_event_db(),\
		List_Explicit_Values.initialisation_value_to_one,val_obj_data_sim.get_t_unit()]
		
		return [val_key_fct_in_dict,val_li_parm_fct]
	
	
	#if no of the previous cases
	else:
		print("PROBLEM IN CREAT PARAM EVENT TREAT, FCT fct_define_param_ev_end_veh_dep, LINK CAPACITY:",\
		val_obj_data_sim.get_variable_indicating_finite_capacity_internal_links())
		import sys
		sys.exit()

#*************************************************************************************************************************************************************************************
#method creating returning a list with the parameters of an event  veh ar at que
def fct_define_param_ev_veh_ar_at_que(val_gl_fct_obj,val_obj_simulation,val_obj_data_sim,val_dec_obj,val_obj_creation_record_files):

	#obj_ev_veh_ar=Cl_Ev_veh_arrived_at_que.Ev_veh_arrived_at_que()
	
	#if new demand is employed
	if val_obj_data_sim.get_creation_new_dem()==List_Explicit_Values.initialisation_value_to_one:
	
		#if the path will dynam be computed (no predefined final destination)
		if val_obj_data_sim.get_type_veh_final_dest()==Cl_Decisions.TYPE_VEHICLE_FINAL_DESTINATION_AND_PATH["dynamically_defined"]:
		
			#val_fct=obj_ev_veh_ar.fct_treat_case_veh_ar_at_que_when_new_demand_final_dest_and_path_dynam_defined
			val_key_fct_in_dict=1
			
			val_li_parm_fct=[val_obj_simulation.get_simul_system().get_network(),\
			val_obj_data_sim.get_min_hold_t_veh_in_que(),\
			val_obj_data_sim.get_precision_round_for_defin_time(),val_obj_simulation.get_heap_even(),\
			val_obj_creation_record_files.get_file_recording_event_db(),\
			List_Explicit_Values.initialisation_value_to_one]
			
			return [val_key_fct_in_dict,val_li_parm_fct]
		
		#if  we have  OD and given path
		elif val_obj_data_sim.get_type_veh_final_dest()==Cl_Decisions.TYPE_VEHICLE_FINAL_DESTINATION_AND_PATH["initially_defined_and_path_given"]:
		
			#val_fct=obj_ev_veh_ar.fct_treat_case_veh_ar_at_que_when_new_demand_final_dest_and_path_given
			val_key_fct_in_dict=2
			
			val_li_parm_fct=[val_obj_simulation.get_simul_system().get_network(),\
			val_obj_data_sim.get_min_hold_t_veh_in_que(),\
			val_obj_data_sim.get_precision_round_for_defin_time(),val_obj_simulation.get_heap_even(),\
			val_obj_creation_record_files.get_file_recording_event_db(),\
			List_Explicit_Values.initialisation_value_to_one]
			
			return [val_key_fct_in_dict,val_li_parm_fct]
		
		
		#if we have OD and dyn computed path 
		elif val_obj_data_sim.get_type_veh_final_dest()==Cl_Decisions.TYPE_VEHICLE_FINAL_DESTINATION_AND_PATH["initially_defined_and_path_dyn_constructed"]:
		
			#selection of the rout algo
			if  val_obj_data_sim.get_type_rout_algo_when_given_od_and_dyn_computed_paths()==Cl_Decisions.TYPE_CALCUL_ROUT_PROP["dynam_based_on_t_trav_OD"]:
			
				import Routing_Algos.algo_based_on_t_travel
				from Routing_Algos.algo_based_on_t_travel import selfish_routing
				val_fct_calcul_que_id_when_given_final_dest_and_path_dynamic_constructed=selfish_routing.fct_calc_queue_id
				
			#if the path algo  is based on  the  probability if the path travel time (=proportionally to  trav times of all possible paths)
			elif val_obj_data_sim.get_type_rout_algo_when_given_od_and_dyn_computed_paths()==Cl_Decisions.TYPE_CALCUL_ROUT_PROP["dynam_based_on_prob_t_trav_OD"]:
			
				import Routing_Algos.algo_probabilistic
				from Routing_Algos.algo_probabilistic import probabilistic_routing
				val_fct_calcul_que_id_when_given_final_dest_and_path_dynamic_constructed=probabilistic_routing.fct_calc_queue_id
		
			else:
				print("PROBLEM IN CREATION_PARAMETERS_EVENT_TREAT, TYPE ROUT ALGO: ",val_obj_data_sim.get_type_rout_algo_when_given_od_and_dyn_computed_paths())
				import sys
				sys.exit()
			

		
			#val_fct=obj_ev_veh_ar.fct_treat_case_veh_ar_at_que_when_new_demand_given_final_dest_and_dyn_computed_path
			val_key_fct_in_dict=3
			
			val_li_parm_fct=[val_obj_simulation.get_simul_system().get_network(),\
			val_obj_data_sim.get_min_hold_t_veh_in_que(),\
			val_obj_data_sim.get_precision_round_for_defin_time(),val_obj_simulation.get_heap_even(),\
			val_obj_creation_record_files.get_file_recording_event_db(),\
			val_fct_calcul_que_id_when_given_final_dest_and_path_dynamic_constructed,\
			List_Explicit_Values.initialisation_value_to_one]
			
			return [val_key_fct_in_dict,val_li_parm_fct]
		
		#if we have a mixed management (dyn defined paths and or OD with given path)
		elif val_obj_data_sim.get_type_veh_final_dest()==Cl_Decisions.TYPE_VEHICLE_FINAL_DESTINATION_AND_PATH["mixed_dyndefined_or_odwithgiven_path"]:
		
			val_key_fct_in_dict=8
			
			val_li_parm_fct=[val_obj_simulation.get_simul_system().get_network(),\
			val_obj_data_sim.get_min_hold_t_veh_in_que(),\
			val_obj_data_sim.get_precision_round_for_defin_time(),val_obj_simulation.get_heap_even(),\
			val_obj_creation_record_files.get_file_recording_event_db(),\
			List_Explicit_Values.initialisation_value_to_one]
			
			return [val_key_fct_in_dict,val_li_parm_fct]
		else:
			print("PROBLEM IN CREATION_PARAMETERS_EVENT_TREAT, final dest: ",val_obj_data_sim.get_type_veh_final_dest())
			import sys
			sys.exit()
		

	#if a previousl generated demand is employed
	elif val_obj_data_sim.get_creation_new_dem()==List_Explicit_Values.initialisation_value_to_zero:
	
		#if the path will dynam be computed (no predefined final destination)
		if val_obj_data_sim.get_type_veh_final_dest()==Cl_Decisions.TYPE_VEHICLE_FINAL_DESTINATION_AND_PATH["dynamically_defined"]:
		
			#val_fct=obj_ev_veh_ar.fct_treat_case_veh_ar_at_que_when_previous_demand_final_dest_and_dyn_computed		
			val_key_fct_in_dict=4		
	
			val_li_parm_fct=[val_obj_simulation.get_simul_system().get_network(),\
			val_obj_data_sim.get_dict_veh_information_prev_sim(),\
			val_obj_data_sim.get_min_hold_t_veh_in_que(),\
			val_obj_data_sim.get_precision_round_for_defin_time(),val_obj_simulation.get_heap_even(),\
			val_obj_creation_record_files.get_file_recording_event_db(),\
			List_Explicit_Values.initialisation_value_to_one]
			
			return [val_key_fct_in_dict,val_li_parm_fct]
			
		
		
		#if we have OD given path
		elif val_obj_data_sim.get_type_veh_final_dest()==Cl_Decisions.TYPE_VEHICLE_FINAL_DESTINATION_AND_PATH["initially_defined_and_path_given"]:
		
			#val_fct=obj_ev_veh_ar.fct_treat_case_veh_ar_at_que_when_previous_demand_given_final_dest_and_path
			val_key_fct_in_dict=5
	
			val_li_parm_fct=[val_obj_simulation.get_simul_system().get_network(),\
			val_obj_data_sim.get_min_hold_t_veh_in_que(),\
			val_obj_data_sim.get_precision_round_for_defin_time(),val_obj_simulation.get_heap_even(),\
			val_obj_creation_record_files.get_file_recording_event_db(),\
			List_Explicit_Values.initialisation_value_to_one]
			
			return [val_key_fct_in_dict,val_li_parm_fct]
		
		#if we have a mixed management (dyn defined paths and or OD with given path)
		elif val_obj_data_sim.get_type_veh_final_dest()==Cl_Decisions.TYPE_VEHICLE_FINAL_DESTINATION_AND_PATH["mixed_dyndefined_or_odwithgiven_path"]:
		
			val_key_fct_in_dict=9
			
			val_li_parm_fct=[val_obj_simulation.get_simul_system().get_network(),\
			val_obj_data_sim.get_dict_veh_information_prev_sim(),\
			val_obj_data_sim.get_min_hold_t_veh_in_que(),\
			val_obj_data_sim.get_precision_round_for_defin_time(),val_obj_simulation.get_heap_even(),\
			val_obj_creation_record_files.get_file_recording_event_db(),\
			List_Explicit_Values.initialisation_value_to_one]
			
			return [val_key_fct_in_dict,val_li_parm_fct]
		
		
		#if we have OD and dyn computed path 
		elif val_obj_data_sim.get_type_veh_final_dest()==Cl_Decisions.TYPE_VEHICLE_FINAL_DESTINATION_AND_PATH["initially_defined_and_path_dyn_constructed"]:
		
			#selection of the rout algo
			if  val_obj_data_sim.get_type_rout_algo_when_given_od_and_dyn_computed_paths()==Cl_Decisions.TYPE_CALCUL_ROUT_PROP["dynam_based_on_t_trav_OD"]:
			
				import Routing_Algos.algo_based_on_t_travel
				from Routing_Algos.algo_based_on_t_travel import selfish_routing
				val_fct_calcul_que_id_when_given_final_dest_and_path_dynamic_constructed=selfish_routing.fct_calc_queue_id
				
			#if the algo comput split ratios is bases on  the  probability if the path travel time (=proportionally to  trav times of all possible paths)
			elif val_obj_data_sim.get_type_rout_algo_when_given_od_and_dyn_computed_paths()== Cl_Decisions.TYPE_CALCUL_ROUT_PROP["dynam_based_on_prob_t_trav_OD"]:
			
				import Routing_Algos.algo_probabilistic
				from Routing_Algos.algo_probabilistic import probabilistic_routing
				val_fct_calcul_que_id_when_given_final_dest_and_path_dynamic_constructed=probabilistic_routing.fct_calc_queue_id
		
			else:
				print("PROBLEM IN CREATION_PARAMETERS_EVENT_TREAT, TYPE ROUT ALGO: ",val_obj_data_sim.get_type_rout_algo_when_given_od_and_dyn_computed_paths())
				import sys
				sys.exit()

		
			#if the purpose  of the implem is to evaluate the signal control policy
			if val_obj_data_sim.get_reason_employing_previous_demand()==Cl_Decisions.TYPE_REASON_EMPLOYING_PREVIOUS_DEMAND["CTRL_EVAL"]:
			
			
				#val_fct=obj_ev_veh_ar.fct_treat_case_veh_ar_at_que_when_previous_demand_given_final_dest_and_path_dyn_computed_ctr_eval
				val_key_fct_in_dict=6
								
				val_li_parm_fct=[val_obj_simulation.get_simul_system().get_network(),\
				val_obj_data_sim.get_min_hold_t_veh_in_que(),\
				val_obj_data_sim.get_precision_round_for_defin_time(),val_obj_simulation.get_heap_even(),\
				val_obj_creation_record_files.get_file_recording_event_db(),\
				val_obj_data_sim.get_dict_veh_information_prev_sim(),\
				val_fct_calcul_que_id_when_given_final_dest_and_path_dynamic_constructed,\
				List_Explicit_Values.initialisation_value_to_one]
				
				return [val_key_fct_in_dict,val_li_parm_fct]
			
			#if the purpose of the implement is to evaluate the rout algo
			elif val_obj_data_sim.get_reason_employing_previous_demand()==Cl_Decisions.TYPE_REASON_EMPLOYING_PREVIOUS_DEMAND["ROUT_ALGO_EVAL"]:
			
				#selection of the rout algo
				if  val_obj_data_sim.get_type_rout_algo_when_given_od_and_dyn_computed_paths()==Cl_Decisions.TYPE_CALCUL_ROUT_PROP["dynam_based_on_t_trav_OD"]:
			
					import Routing_Algos.algo_based_on_t_travel
					from Routing_Algos.algo_based_on_t_travel import selfish_routing
					val_fct_calcul_que_id_when_given_final_dest_and_path_dynamic_constructed=selfish_routing.fct_calc_queue_id
				
				#if the algo comput split ratios is bases on  the  probability if the path travel time (=proportionally to  trav times of all possible paths)
				elif val_obj_data_sim.get_type_rout_algo_when_given_od_and_dyn_computed_paths()== Cl_Decisions.TYPE_CALCUL_ROUT_PROP["dynam_based_on_prob_t_trav_OD"]:
			
					import Routing_Algos.algo_probabilistic
					from Routing_Algos.algo_probabilistic import probabilistic_routing
					val_fct_calcul_que_id_when_given_final_dest_and_path_dynamic_constructed=probabilistic_routing.fct_calc_queue_id
		
				else:
					print("PROBLEM IN CREATION_PARAMETERS_EVENT_TREAT, TYPE ROUT ALGO: ",val_obj_data_sim.get_type_rout_algo_when_given_od_and_dyn_computed_paths())
					import sys
					sys.exit()

			
				#val_fct=obj_ev_veh_ar.fct_treat_case_veh_ar_at_que_when_previous_demand_given_final_dest_and_path_dyn_computed_rout_algo_eval
				val_key_fct_in_dict=7
				
				val_li_parm_fct=[val_obj_simulation.get_simul_system().get_network(),\
				val_obj_data_sim.get_min_hold_t_veh_in_que(),\
				val_obj_data_sim.get_precision_round_for_defin_time(),val_obj_simulation.get_heap_even(),\
				val_obj_creation_record_files.get_file_recording_event_db(),\
				val_fct_calcul_que_id_when_given_final_dest_and_path_dynamic_constructed,\
				List_Explicit_Values.initialisation_value_to_one]
				
				return [val_key_fct_in_dict,val_li_parm_fct]

			
				
	
	
	#if a given demand is considered
	elif val_demand_type==List_Explicit_Values.initialisation_value_to_minus_one:
		print("A FAIRE")
		import sys
		sys.exit()
	
	#if none of the previous cases concerning the demand
	else:
		print("PROBLEM IN CREATION PARAM EVENT  TREATM, IN FCT fct_define_param_ev_veh_ar_at_que, DEMAND TYPE",val_demand_type)
		import sys
		sys.exit()
	



#*************************************************************************************************************************************************************************************
#method returning a dictionary with a list of parameters for the treatment of each event type
def fct_creating_parameter_list_event_treat_event_heap(obj_simulation,obj_data_sim,obj_creation_record_files):

	dec_obj=Cl_Decisions.Decisions()
	gl_fct_obj= Cl_Global_Functions.Global_Functions()
	gl_fct_nsi_obj=Cl_Global_Functions_nsi.Global_Functions_nsi()
	
	
	fct_exam_nb_dep_veh_by_end_hold_nsi=gl_fct_nsi_obj.fct_exam_nb_veh_dep_by_end_veh_hold_depart_order_related_to_t_veh_arrival_mi
	fct_calcul_nb_and_t_dep_veh_end_veh_dep_nsi=gl_fct_nsi_obj.fct_exam_nb_veh_dep_by_end_veh_depart_ev_depart_order_related_to_t_veh_arrival_mi
	
	#fct calcul nb and t departing vehicles
	fct_calcul_nb_and_time_next_dep_veh=gl_fct_obj.fct_calcul_nb_veh_they_can_leave_at_t_current_and_assoc_end_dep_time_mi	
	
	
	#fct for calcul travel time
	if obj_data_sim.get_type_trav_duration_managament()==Cl_Decisions.TYPE_TRAVEL_DURAT_MANAG[1]:
	
		fct_calcul_travel_time=dec_obj.fct_calcul_travel_time_from_link_l_to_link_m_fixe_duration
	#if stochastic travel duration  is employed	
	elif obj_data_sim.get_type_trav_duration_managament()==Cl_Decisions.TYPE_TRAVEL_DURAT_MANAG[2]:
		fct_calcul_travel_time=dec_obj.fct_calcul_travel_time_from_link_l_to_link_m_stoch_duration
	else:
		print("PROBLEM IN CREAT_PARAM_EVENT_TREAT, fct_creating_parameter_list_event_treat_event_heap, TYPE_TRAVEL_DURAT_MANAG: ",\
		val_obj_data_sim.get_type_trav_duration_managament())
		import sys
		sys.exit()


#*****************************************************************************************************************************************************************************************
	#the list with the parameters for the treatment of the vehicle appearance event Ev_veh_appearance, at a sign intersection event type 1
	
	li_1=fct_define_param_ev_veh_ap(val_obj_simulation=obj_simulation,val_obj_data_sim=obj_data_sim,val_obj_creation_record_files=obj_creation_record_files)
	
		
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
	
	li_4=fct_define_param_ev_end_veh_dep(\
	val_fct_calcul_nb_and_time_next_dep_veh=fct_calcul_nb_and_time_next_dep_veh,\
	val_obj_simulation=obj_simulation,val_obj_data_sim=obj_data_sim,\
	val_fct_calcul_travel_time=fct_calcul_travel_time,\
	val_obj_creation_record_files=obj_creation_record_files)
	
#*****************************************************************************************************************************************************************************************
	#the list with the parameters for the treatment of Ev_veh_arrived_at_que, event type 5
	li_5=fct_define_param_ev_veh_ar_at_que(val_gl_fct_obj=gl_fct_obj,val_obj_simulation=obj_simulation,val_obj_data_sim=obj_data_sim,\
	val_dec_obj=dec_obj,val_obj_creation_record_files=obj_creation_record_files)

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
	
	li_7=[obj_simulation.get_simul_system().get_network(),obj_data_sim.get_precision_round_for_defin_time(),\
	obj_data_sim.get_type_veh_final_dest(),\
	obj_creation_record_files.get_file_recording_event_db(),\
	obj_simulation.get_heap_even()]

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