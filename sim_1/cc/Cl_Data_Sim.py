import csv
import os
import sys
import itertools
import Global_Functions
import Global_Functions_Network
import List_Explicit_Values
import Cl_Record_and_Treat_Sim_File_Names
import Record_and_Treat_Sim_File_Names
import File_Sim_Name_Module_Files
import File_names_network_model
import Cl_Decisions
import Cl_Control_Actuate
import Cl_Vehicle
import math


class Data_Sim:

	""" class defining the data from the user data file"""
	
	def __init__(self,val_name_file_with_veh_ap_ev_end_sim_to_read,val_path_veh_res_when_in_fres_folder,val_name_sim_user_file="Dsu"):
	
		#the name of the  user data file 
		self._name_user_data_file=val_name_sim_user_file
		
		
		#the name of the module importing the user data 
		self._module_name_importing_sim_user_data=__import__(self._name_user_data_file)
		
		#the name of the folder where the files for modeling the network are placed,SMALL_DATA_INTERS_3
		self._name_folder_network_files=self._module_name_importing_sim_user_data.val_name_folder_network_files
		
		#the folder with the files  modeling the network,  placed at the asociated directory
		self._folder_network_files="../"+self._name_folder_network_files
		
		#the name of the file containing  the demand of each entry links
		self._file_name_demand_param_entry_link=File_names_network_model.val_file_name_demand_param_entry_link
		
		#the file containing the demand of each entry link (placed in the directory)
		self._file_demand_param_entry_link=self._folder_network_files+"/"+self._file_name_demand_param_entry_link
		
		#variable indicating if messages will be print on the terminal during the simulation
		self._print_messages_on_term=self._module_name_importing_sim_user_data.print_messages_on_terminal
		
		#variable  indicating the precision on  some rounds that we will use (depending on t_unit)
		self._precision_round_for_defin_time=self._module_name_importing_sim_user_data.val_precision_round_for_defin_time
		
		#variable indicating the pression for computations  like pressure etc.
		self._round_precision=self._module_name_importing_sim_user_data.val_precision_round
		
		#variable indicating the time unit considered
		self._t_unit=self._module_name_importing_sim_user_data.val_t_unit
		
		#varibale indicating if we want to connect the simulator with the CTM simulator
		self._ctm_connect=self._module_name_importing_sim_user_data.val_ctm_connect
		
		#variable indicating whether the demand will be deterministic (value 0) or stochstic (value 1)
		self._val_indicating_stoch_demand=self._module_name_importing_sim_user_data.val_indicating_stoch_demand
		
		#variable indicating if we wish to create a new demand or not
		self._creation_new_dem=self._module_name_importing_sim_user_data.creation_new_demand
		
		#the path where the VEH_RES (created by the treat. of a sim) are located when we are already in a FRes... folder
		#this is Sim_Treat/VEH_RES
		self._path_veh_res_when_in_fres_folder=val_path_veh_res_when_in_fres_folder
		
		
		#variable indicating the type of each vehicle regarding its final destination
		self._type_veh_final_dest=self._module_name_importing_sim_user_data.val_type_veh_final_dest
		
	
		if self._type_veh_final_dest==Cl_Decisions.TYPE_VEHICLE_FINAL_DESTINATION_AND_PATH["initially_defined_and_path_dyn_constructed"]:
		
			#variable indicating how (the algo)  paths are computed when OD matrice and path dyn computed
			self._type_rout_algo_when_given_od_and_dyn_computed_paths=\
			self._module_name_importing_sim_user_data.val_type_rout_algo_when_given_od_and_dyn_computed_paths
			
		#the name of the file where the veh appear event remaining in the event list by the end of the sim are stored
		self._name_file_with_veh_ap_ev_end_sim_to_read=val_name_file_with_veh_ap_ev_end_sim_to_read
			
		
		#if we use a given demand, we read the id of the last created vehcle
		if self._creation_new_dem==List_Explicit_Values.initialisation_value_to_minus_one:
			
			self._last_created_veh_id_given_demand=Global_Functions.fct_reading_file(name_file_read=self._folder_network_files+"/"+\
			Record_and_Treat_Sim_File_Names.val_name_file_recording_last_veh_id_given_demand,nb_comment_lines=1)[0]
			
			self._dict_information_entry_lk_given_demand=self.fct_creat_dict_information_entry_link_given_demand()
			
			self._dict_veh_information_prev_sim=None
			self._dict_entry_link_information_prev_sim=None
		
		#if a previously generated demand will be employed
		elif self._creation_new_dem==List_Explicit_Values.initialisation_value_to_zero:
			
		
			#variable indicating the path of the folder where we write the file with the info of the veh ap events remaining
			#in the event lisy by the end of the sim 
			self._path_prev_generated_veh_demand=self._module_name_importing_sim_user_data.path_prev_generated_veh_demand
			
			
			#we create the dictionary with the veh information
			#and the dictionary of the entry link information
			self._dict_veh_information_prev_sim=self.fct_creat_dict_veh_prev_sim()
			

			
			self._dict_entry_link_information_prev_sim=self.fct_creat_dict_information_entry_link_prev_sim(\
			val_veh_final_dest_dynam_construct=self._type_veh_final_dest,\
			val_dict_vehicle_inform=self._dict_veh_information_prev_sim)
			
			self._dict_information_entry_lk_given_demand=None
			
			#creation of the variable indicating the reason of employing a previous demand
			self._reason_employing_previous_demand=self._module_name_importing_sim_user_data.reason_employing_previous_demand
			

		#if a new demand will be generated
		else:
			self._dict_veh_information_prev_sim=None
			self._dict_entry_link_information_prev_sim=None
			
			self._dict_information_entry_lk_given_demand=None
		
		#variable indicating if we wish to do a new simulation  or not (continue a previous sim)
		self._new_sim=self._module_name_importing_sim_user_data.new_simulation
		
		#if a previous sim will be continued
		if self._new_sim==List_Explicit_Values.initialisation_value_to_zero:
		
			#the path folder where the  files with the final state of a simulation are registered, 
			#utilised when we wish to continue a previously made simulation
			self._path_name_folder_results_sim_to_be_continued=self._module_name_importing_sim_user_data.path_name_folder_results_sim_to_be_continued
			
			
		#variable indicating the time at which we wish to start a new simulation
		self._t_start_new_sim=self._module_name_importing_sim_user_data.t_start_new_simulation	
		
		#variable indicating the time during which we wish to simulate
		self._t_simulation_duration=self._module_name_importing_sim_user_data.t_simulation_duration
		
		#variable indicating the min margin at which the new network control object (for the next cycle) mut be returned
		self._margin_dt=self._module_name_importing_sim_user_data.margin_dt
		
		#the variable indicating whether we consider internal links with finite- nfinite capacity
		self._variable_indicating_finite_capacity_internal_links=self._module_name_importing_sim_user_data.val_finite_capacity_internal_links
		
		
		#variable indicating the minimum hold  time  of a veh in a que
		self._min_hold_t_veh_in_que=self._module_name_importing_sim_user_data.val_min_hold_t_veh_in_que
		
		#variable employed for the first vehicle appearance events.
		#the time at which the vehicles will start to appear= self._t_start_veh_appearance+ time duration defined by Pois. process
		self._t_marge_start_calcul_veh_appearance=self._module_name_importing_sim_user_data.val_t_marge_start_calcul_veh_appearance
		
		#variable indicating if we wish to treat the sim resutls or not
		self._treat_sim_res=self._module_name_importing_sim_user_data.val_treat_sim_res
		
		#variable indicating whether we read the intersection control  or we calculate it
		self._each_icm_read=self._module_name_importing_sim_user_data.val_each_icm_read
		
	
		
		#variable indicating whether turn ratios are/not going to be estimated
		#self._turn_ratios_estimated=self._module_name_importing_sim_user_data.val_turn_ratios_estimated
		
		#variable indicating if a fixed or stochastic travel duration will be employed
		self._type_trav_duration_managament=self._module_name_importing_sim_user_data.val_type_trav_duration_managament


		
#******************************************************		
		#variable indicating whether the given  routing proportions change during the current sim duration
		#self._varying_given_rout_prop=self._module_name_importing_sim_user_data.val_varying_given_rout_prop
		
		
		
		#if varying routing proportions are considered, we create the list with the dict of od matrices and
		#the related associated list of dict with the cum fcts
		#if self._varying_rout_prop==List_Explicit_Values.initialisation_value_to_one:
		
			#we create the variable indicating the  number of additional od matrices
			#self._nb_additonal_mat_rp=self._module_name_importing_sim_user_data.val_nb_additonal_mat_rp
			
			#print("self._name_folder_network_files",self._name_folder_network_files)
			#list mat rp id link
			#for i in os.listdir("../"+self._name_folder_network_files):
				#print(i)
			#li_mat_rp_id_lk=Global_Functions_Network.fct_creating_li_rp_mat(v_name_file_read="../"+self._name_folder_network_files+"/"+\
			#File_names_network_model.val_name_folder_mat_rout_prob_id_lk+"/"+\
			#File_names_network_model.val_name_file_id_entry_internal_lk_id_dest_links,\
			#v_nb_files=self._nb_additonal_mat_rp,v_nb_comment_lines=1)
			
			#self._li_rp_mat_id_lk=li_mat_rp_id_lk
			
			#list mat rout prop cum
			#li_mat_rp_cum=Global_Functions_Network.fct_creating_li_rp_mat(v_name_file_read="../"+self._name_folder_network_files+"/"+\
			#File_names_network_model.val_name_folder_mat_rout_prob_cum+"/"+\
			#File_names_network_model.val_name_file_mat_rp_cum_id_lk_val_cum_funct_dest_lk,\
			#v_nb_files=self._nb_additonal_mat_rp,v_nb_comment_lines=1)
			
			#self._li_rp_cum_mat=li_mat_rp_cum
			
			#list with the durations if each od mat (including the current one already in the network object)
			#li_dur_rp_mat=Global_Functions.fct_reading_file(name_file_read="../"+self._name_folder_network_files+"/"+\
			#File_names_network_model.val_name_file_duration_each_rp_mat,nb_comment_lines=1)
			
			#self._li_dur_rp_mat=li_dur_rp_mat
		#else:
			#we create the variable indicating the  number of additional od matrices
			#self._nb_additonal_mat_od=None
			
			#list mat od
			#self._li_od_mat=[]
			
			#list mat od cum
			#self._li_rp_cum_mat=[]
			
			#list with the durations if each od mat (including the current one already in the network object)
			#self._li_dur_rp_mat=[]
			
			
		
		
			
		
		#variable indicating the (path) folder where the files of a previously generated veh demand are stored
		#self._path_folder_veh_res_prev_sim=self._module_name_importing_sim_user_data.path_folder_veh_res_prev_sim
		
		#varibale indicating how the split ratios will be computed
		#self._type_split_ratio_calcul=self._module_name_importing_sim_user_data.val_type_split_ratio_calcul
		
					
	
		
		#variable indicating if we will  creat the text record file
		#self._creation_text_file_recording_sim_ev_text=self._module_name_importing_sim_user_data.creation_text_file_recording_sim_events_text
		
		
		
		
		#variable indicating the time unit (sec)
		#self._t_unit=self._module_name_importing_sim_user_data.val_t_unit
		
				
		#variable indicating if merging queues are considered in the network model
		#self._merging_ques_considered=self._module_name_importing_sim_user_data.val_merging_ques_considered
		
		
		#the vector with the values of the distrib function for the number of depart veh from each mov during the phase actuation
		#self._vector_distr_fct_nb_depart_veh=Global_Functions.fct_creating_vector_from_file(name_veh_file_read=\
		#File_Sim_Name_Module_Files.val_name_file_distribution_fct_nb_dep_veh)
		
		#the type of the control policy (it can be MP, FT, mixed..)
		#self._type_control_policy=self._module_name_importing_sim_user_data.val_type_control_policy
		
		#dictionary, key=id node, value=control type
		#self._dict_key_id_nd_value_ctrl_type=Global_Functions_Network.fct_reading_fi_id_node_type_control(\
		#val_name_file_to_read=File_Sim_Name_Module_Files.val_name_folder_with_control_param_files+"/"+\
		#File_Sim_Name_Module_Files.val_name_file_node_id_and_control_type,nb_comment_lines=1)
		
		
		
		#the name of the file with the parameters of the FT or MP control 
		#self._name_fi_values_ft_mp_control=self._module_name_importing_sim_user_data.val_name_fi_values_ft_mp_control
		
		#the type of the current control policy, we use it when a mixed control is applied to the network
		#if self._type_control_policy==Cl_Control_Actuate.TYPE_CONTROL[3]:
			#self._type_first_control_when_mixed_control_policy=self._module_name_importing_sim_user_data.\
			#val_type_first_control_when_mixed_control_policy
		#else:
			#self._type_first_control_when_mixed_control_policy=None
			
		
		#the type of simulator management, (for the veh departure), macro, micro
		#self._type_sim_management=self._module_name_importing_sim_user_data.val_type_sim_management
		
		
		
		
		
		
		
		#variable indicating the parameter defining the  latest time for a vehicle to leave 
		#when another veh of a compatible phase crosses an unsignalised intersection
		#self._param_epsilon_t_latest_for_veh_to_leave_compatible_phase_nsi=self._module_name_importing_sim_user_data.\
		#val_param_epsilon_t_latest_for_veh_to_leave_compatible_phase_nsi
		
		#dict, key=id entry-exit link, value=[...,link id to follow for arriving to next node,...,link id to follow for arriving at exit link]
		#self._dict_id_entry_exit_lk_value_unique_path=Global_Functions.fct_reading_file_fi_id_entry_exit_lk_related_unique_path(\
		#name_file_read=self._folder_network_files+"/"+File_names_network_model.val_name_file_id_entry_exit_link_path,nb_comment_lines=1)
		
		#dict, key=1,2 indicating repsectively if the vehicle has a dynamically constructed final destination
		#value= functions returning the que chosen by each type of vehicle
		#di_key_type_veh_regarding_its_destination_value_fct_returning_que_chosen_by_veh=\
		#{Cl_Vehicle.TYPE_VEH_FINAL_DESTINATION[1]=Cl_Decisions.
		
		
		
		#variable indicating the employed control category at the begin of the sim
		#self._type_ctrl_category_at_the_beg_of_sim=self._module_name_importing_sim_user_data.val_type_ctrl_category_at_the_beg_of_sim
		
		
#*****************************************************************************************************************************************************************************************
	#method returning the name of the  user data file
	def get_name_user_data_file(self):
		return self._name_user_data_file

#*****************************************************************************************************************************************************************************************
	#method returning the name of the module importing the user data 
	def get_module_name_importing_sim_user_data(self):
		return self._module_name_importing_sim_user_data

#*****************************************************************************************************************************************************************************************
	#method returning the name of the folder where the files for modeling the network are placed
	def get_name_folder_network_files(self):
		return self._name_folder_network_files
	
	
#*****************************************************************************************************************************************************************************************
	#method returning the name of the folder where the files for modeling the network are placed
	def get_folder_network_files(self):
		return self._folder_network_files
	
	
#*****************************************************************************************************************************************************************************************
	#method returning the name of the file containing the the demand of each entry link
	def get_file_name_demand_param_entry_link(self):
		return self._file_name_demand_param_entry_link

#*****************************************************************************************************************************************************************************************
	#method returning  the file containing the the demand of each entry link
	def get_file_demand_param_entry_link(self):
		return self._file_demand_param_entry_link

#*****************************************************************************************************************************************************************************************


	#method returning the variable indicating if messages will be print on the terminal during the simulation
	def get_print_messages_on_term(self):
		return self._print_messages_on_term
#*****************************************************************************************************************************************************************************************
	#method returning the variable  indicating the precision on  some rounds that we will use (depending on  t_unit)
	def get_precision_round_for_defin_time(self):
		return self._precision_round_for_defin_time

#*****************************************************************************************************************************************************************************************
	#method returning the variable indicating the pression for computations  like pressure etc.
	def get_round_precision(self):
		return self._round_precision
#*****************************************************************************************************************************************************************************************
	#method returning the variable indicating the time unit 
	def get_t_unit(self):
		return self._t_unit

#*****************************************************************************************************************************************************************************************
	#method returning the CTM connect option
	def get_ctm_connect(self):
		return self._ctm_connect


#*****************************************************************************************************************************************************************************************
	#method returning the variable indicating whether stochastic ordeterministic demand will be employed
	def get_val_indicating_stoch_demand(self):
		return self._val_indicating_stoch_demand
#*****************************************************************************************************************************************************************************************

	#method returning the variable indicating the number of times that the routing proportions change during the current sim duration
	#def get_varying_given_rout_prop(self):
		#return self._varying_given_rout_prop

#*****************************************************************************************************************************************************************************************

	#method returning  the variable indicating if the turn prob will be estimated during the sim
	#def get_turn_ratios_estimated(self):
		#return self._turn_ratios_estimated

#*****************************************************************************************************************************************************************************************
	#method returning the variable indicating the  number of additional rout prop matrices
	#def get_nb_additonal_mat_rp(self):
		#return self._nb_additonal_mat_rp

#*****************************************************************************************************************************************************************************************
	#method returning the list with the rout prop matrices
	#def get_li_rp_mat_id_lk(self):
		#return self._li_rp_mat_id_lk

#*****************************************************************************************************************************************************************************************
	#method returning the list mat rout prop cum
	#def get_list_mat_rp_cum(self):
		#return self._li_rp_cum_mat
#*****************************************************************************************************************************************************************************************
	#method returning the list with the durations if each rout prop mat (including the current one already in the network object)
	#def get_li_dur_rp_mat(self):
		#return self._li_dur_rp_mat
#*****************************************************************************************************************************************************************************************
	#method returning the variable indicating if we wish to create a new demand or not
	def get_creation_new_dem(self):
		return self._creation_new_dem

#*****************************************************************************************************************************************************************************************

	#method returning the variable indicating if we wish to create a new demand or not
	def get_last_created_veh_id_given_demand(self):
		return self._last_created_veh_id_given_demand

#*****************************************************************************************************************************************************************************************
	#method returning the variable indicating the (path) folder where the files of a previously generated veh demand are stored
	def get_path_folder_veh_res_prev_sim(self):
		return self._path_folder_veh_res_prev_sim

#*****************************************************************************************************************************************************************************************
	#method returning the path folder where the veh information of a previously generated veh demand is stored
	def get_path_prev_generated_veh_demand(self):
		return self._path_prev_generated_veh_demand

#*****************************************************************************************************************************************************************************************
	#method returning the name of the file where the veh appear event remaininf in the event list by the end of the sim are stored
	def get_name_file_with_veh_ap_ev_end_sim_to_read(self):
		return self._name_file_with_veh_ap_ev_end_sim_to_read

#*****************************************************************************************************************************************************************************************
	#method returning the path where the VEH_RES (created by the treat. of a sim) are located when we are already in a FRes... folder
	def get_path_veh_res_when_in_fres_folder(self):
		return self._path_veh_res_when_in_fres_folder

#*****************************************************************************************************************************************************************************************
	#method returning the dictionary with the veh information of a previously generated demand
	def get_dict_veh_information_prev_sim(self):
		return self._dict_veh_information_prev_sim

#*****************************************************************************************************************************************************************************************
	#method returning the dictionary when a given demand is employed
	def get_dict_information_entry_lk_given_demand(self):
		return self._dict_information_entry_lk_given_demand
#*****************************************************************************************************************************************************************************************
	#method returning the he dictionary of the entry link information
	def get_dict_entry_link_information_prev_sim(self):
		return self._dict_entry_link_information_prev_sim
#*****************************************************************************************************************************************************************************************
	#method returning the variable indicating the reason of employing a previous demand
	def get_reason_employing_previous_demand(self):
		return self._reason_employing_previous_demand
#*****************************************************************************************************************************************************************************************
	#method returning the variable indicating if we wish to do a new simulation  or not
	def get_new_sim(self):
		return self._new_sim
#*****************************************************************************************************************************************************************************************
	
	#method returning the the path folder where the  files with the final state of a simulation are registered
	##utilised when we wish to continue a previously made simulation
	def get_path_name_folder_results_sim_to_be_continued(self):
		return self._path_name_folder_results_sim_to_be_continued

#*****************************************************************************************************************************************************************************************
	#method returning the variable indicating the time at which we wish to start a new simulation
	def get_t_start_new_sim(self):
		return self._t_start_new_sim

#*****************************************************************************************************************************************************************************************
	#method returning the variable indicating the time during which we wish to simulate
	def get_t_simulation_duration(self):
		return self._t_simulation_duration

#*****************************************************************************************************************************************************************************************
	#method returning if a text recording file will be created 
	#def get_creation_text_file_recording_sim_ev_text(self):
		#return self._creation_text_file_recording_sim_ev_text

#*****************************************************************************************************************************************************************************************
	#method returning the variable indicating the min margin at which the new network control object (for the next cycle) mut be returned
	def get_margin_dt(self):
		return self._margin_dt

#*****************************************************************************************************************************************************************************************
	
	#method returning the variable indicating the minimum hold  time  of a veh in a que
	def get_min_hold_t_veh_in_que(self):
		return self._min_hold_t_veh_in_que

#*****************************************************************************************************************************************************************************************
	#method returning the variable indicating the cycle duration
	#def get_time_cycle_duration(self):
		#return self._time_cycle_duration

#*****************************************************************************************************************************************************************************************
	
	
	#method returning the employed variable for calculating  the first vehicle appearance events
	def get_t_marge_start_calcul_veh_appearance(self):
		return self._t_marge_start_calcul_veh_appearance
	
#*****************************************************************************************************************************************************************************************
	#method indicating if we wish to treat the sim results or not
	def get_treat_sim_res(self):
		return self._treat_sim_res
#*****************************************************************************************************************************************************************************************
	#method returning the variable indicating the type of each vehicle regarding its final destination
	def get_type_veh_final_dest(self):
		return self._type_veh_final_dest
#*****************************************************************************************************************************************************************************************
	#method returning the variable indicating how paths are computed when D and paths are dyn computed
	def get_type_rout_algo_when_given_od_and_dyn_computed_paths(self):
		return self._type_rout_algo_when_given_od_and_dyn_computed_paths
	
#*****************************************************************************************************************************************************************************************
	#method returning if merging queues are considered in the network model
	#def get_merging_ques_considered(self):
		#return self._merging_ques_considered
#*****************************************************************************************************************************************************************************************
	#method returning the file with the parameters of the FT or MP control 
	#def get_name_fi_values_ft_mp_control(self):
		#return self._name_fi_values_ft_mp_control

#*****************************************************************************************************************************************************************************************
	#method returing the vecotr with the values of the distribution fct for the nb of departing vehicles from an actuated phase
	#def get_vector_distr_fct_nb_depart_veh(self):
		#return self._vector_distr_fct_nb_depart_veh
#*****************************************************************************************************************************************************************************************
	#method returning the variable with the type of the employed control policy
	#def get_type_control_policy(self):
		#return self._type_control_policy
#*****************************************************************************************************************************************************************************************
	#method returning the dictionary, key =id node, value=control type
	#def get_dict_key_id_nd_value_ctrl_type(self):
		#return self._dict_key_id_nd_value_ctrl_type

#*****************************************************************************************************************************************************************************************
	#method returning the type of the current control policy, we use it when a mixed control is applied to the network
	#def get_type_first_control_when_mixed_control_policy(self):
		#return self._type_first_control_when_mixed_control_policy
		
#*****************************************************************************************************************************************************************************************
	#method returning the type of simulator management, (for the veh departure), macro, micro
	#def get_type_sim_management(self):
		#return self._type_sim_management
#*****************************************************************************************************************************************************************************************
	#method returning the variable indicating if a fixed or stochastic travel duration will be employed
	def get_type_trav_duration_managament(self):
		return self._type_trav_duration_managament
#*****************************************************************************************************************************************************************************************
	#method returning the variable indicating whether we read the network control  or we calculate it
	def get_each_icm_read(self):
		return self._each_icm_read
#*****************************************************************************************************************************************************************************************
	
	
	#method returning the variable indicating the parameter defining the  latest time for a vehicle to leave
	#when another veh of a compatible phase crosses an unsignalised intersection
	#def get_param_epsilon_t_latest_for_veh_to_leave_compatible_phase_nsi(self):
		#return self._param_epsilon_t_latest_for_veh_to_leave_compatible_phase_nsi
#*****************************************************************************************************************************************************************************************
	#method returning the dict with the paths to follow in order to reach a given exit link from a given entry link
	def get_dict_id_entry_exit_lk_value_unique_path(self):
		return self._dict_id_entry_exit_lk_value_unique_path
#*****************************************************************************************************************************************************************************************
	#method returning the variable  indicating whether we consider internal links with finite/infinite capacity
	def get_variable_indicating_finite_capacity_internal_links(self):
		return self._variable_indicating_finite_capacity_internal_links
#*****************************************************************************************************************************************************************************************
	#method returning the variable indicating the employed control category at the begin of the sim
	#def get_type_ctrl_category_at_the_beg_of_sim(self):
		#return self._type_ctrl_category_at_the_beg_of_sim
#*****************************************************************************************************************************************************************************************
	#method returning the variable indicating whether turn ratios are/not going to be estimated
	#def get_turn_ratios_estimated(self):
		#return self._turn_ratios_estimated

#*****************************************************************************************************************************************************************************************
	
	#method modifying the name of the  user data file
	def set_name_user_data_file(self,n_v):
		self._name_user_data_file=n_v

#*****************************************************************************************************************************************************************************************
	#method rmodifying the name of the module importing the user data 
	def set_module_name_importing_sim_user_data(self,n_v):
		self._module_name_importing_sim_user_data=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the name of the folder where the files for modeling the network are placed
	def set_name_folder_network_files(self,n_v):
		self._name_folder_network_files=n_v
	
	
#*****************************************************************************************************************************************************************************************
	#method modifying the name of the folder where the files for modeling the network are placed
	def set_folder_network_files(self,n_v):
		self._folder_network_files=n_v
	
#*****************************************************************************************************************************************************************************************
	#method modifying the name of the file containing the the demand of each entry link
	def set_file_name_demand_param_entry_link(self,n_v):
		self._file_name_demand_param_entry_link=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying  the file containing the the demand of each entry link
	def set_file_demand_param_entry_link(self,n_v):
		self._file_demand_param_entry_link=n_v

#*****************************************************************************************************************************************************************************************
		
	#method modifying the variable indicating if messages will be print on the terminal during the simulation
	def set_print_messages_on_term(self,n_v):
		self._print_messages_on_term=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the variable  indicating the precision on  some rounds that we will use (depending on  t_unit)
	def set_precision_round_for_defin_time(self,n_v):
		self._precision_round_for_defin_time=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the variable indicating the pression for computations  like pressure etc.
	def set_round_precision(self,n_v):
		self._round_precision=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the variable indicating the time unit 
	def set_t_unit(self,n_v):
		self._t_unit=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the variable indicating whether stochastic ordeterministic demand will be employed
	def set_val_indicating_stoch_demand(self,n_v):
		self._val_indicating_stoch_demand=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the variable indicating whether the routing proportions change during the current sim duration
	#def set_varying_given_rout_prop(self,n_v):
		#self._varying_given_rout_prop=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying  the variable indicating if the turn prob will be estimated during the sim
	#def set_turn_ratios_estimated(self,n_v):
		#self._turn_ratios_estimated=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the variable indicating the  number of additional rout prop matrices
	#def set_nb_additonal_mat_rp(self,n_v):
		#self._nb_additonal_mat_rp=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the list with the od matrices
	#def set_li_rp_mat_id_lk(self,n_v):
		#self._li_rp_mat_id_lk=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the list mat rout prop cum
	def set_list_mat_rp_cum(self,n_v):
		self._list_mat_rp_cum=n_v
#*****************************************************************************************************************************************************************************************
	#methodmodifying the list with the durations if each od mat (including the current one already in the network object)
	#def set_li_dur_rp_mat(self,n_v):
		#self._li_dur_rp_mat=n_v
#*****************************************************************************************************************************************************************************************

	#method modifying the variable indicating if we wish to create a new demand or not
	def set_creation_new_dem(self,n_v):
		self._creation_new_dem=n_v

#*****************************************************************************************************************************************************************************************
	#method modyfing the id of the last created vehicle
	def set_last_created_veh_id_given_demand(self,n_v):
		self._last_created_veh_id_given_demand=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the variable indicating the (path) folder where the files of a previously generated veh demand are stored
	#def set_path_folder_veh_res_prev_sim(self,n_v):
		#self._path_folder_veh_res_prev_sim=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the path where the VEH_RES (created by the treat. of a sim) are located when we are already in a FRes... folder
	def set_path_veh_res_when_in_fres_folder(self,n_v):
		self._path_veh_res_when_in_fres_folder=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the path folder where the veh information of a previously generated veh demand is stored
	def set_path_directory_prev_generated_veh_demand(self,n_v):
		self._path_directory_prev_generated_veh_demand=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the name of the file where the veh appear event remaininf in the event list by the end of the sim are stored
	def set_name_file_with_veh_ap_ev_end_sim_to_read(self,n_v):
		self._name_file_with_veh_ap_ev_end_sim_to_read=n_v

#*****************************************************************************************************************************************************************************************

	#method modifying the dictionary with the veh information of a previously generated demand
	def set_dict_veh_information_prev_sim(self,n_v):
		self._dict_veh_information_prev_sim=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the dictionary when a given demand is employed
	def set_dict_information_entry_lk_given_demand(self,n_v):
		self._dict_information_entry_lk_given_demand=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the he dictionary of the entry link information
	def set_dict_entry_link_information_prev_sim(self,n_v):
		self._dict_entry_link_information_prev_sim=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the variable indicating the reason of employing a previous demand
	def set_reason_employing_previous_demand(self,n_v):
		self._reason_employing_previous_demand=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the variable indicating if we wish to do a new simulation  or not
	def set_new_sim(self,n_v):
		self._new_sim=n_v

#*****************************************************************************************************************************************************************************************
	
	#method modifying the the path folder where the  files with the final state of a simulation are registered
	##utilised when we wish to continue a previously made simulation
	def set_path_name_folder_results_sim_to_be_continued(self,n_v):
		self._path_name_folder_results_sim_to_be_continued=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the variable indicating the time at which we wish to start a new simulation
	def set_t_start_new_sim(self,n_v):
		self._t_start_new_sim=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the variable indicating the time during which we wish to simulate
	def set_t_simulation_duration(self,n_v):
		self._t_simulation_duration=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying if a text recording file will be created 
	#def set_creation_text_file_recording_sim_ev_text(self,n_v):
		#self._creation_text_file_recording_sim_ev_text=n_v

#*****************************************************************************************************************************************************************************************
	#method  modifying the variable indicating the min margin at which the new network control object (for the next cycle) mut be returned
	def set_margin_dt(self,n_v):
		self._margin_dt=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the  time unit (in secs)
	def set_t_unit(self,n_v):
		self._t_unit=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the variable indicating the minimum hold  time  of a veh in a que
	def set_min_hold_t_veh_in_que(self,n_v):
		self._min_hold_t_veh_in_que=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the variable indicating the cycle duration
	#def set_time_cycle_duration(self,n_v):
		#self._time_cycle_duration=n_v

#*****************************************************************************************************************************************************************************************
	
	#method modifying the employed variable for calculating  the first vehicle appearance events
	def set_t_marge_start_calcul_veh_appearance(self,n_v):
		self._t_marge_start_calcul_veh_appearance=n_v
	
#*****************************************************************************************************************************************************************************************
	#method modifying the variable indicating whether  we wish to treat the sim results or not
	def set_treat_sim_res(self,n_v):
		self._treat_sim_res=n_v
#*****************************************************************************************************************************************************************************************
	#method returning the variable indicating how paths are computed when D and paths are dyn computed
	def get_type_rout_algo_when_given_od_and_dyn_computed_paths(self):
		return self._type_rout_algo_when_given_od_and_dyn_computed_paths
	
#*****************************************************************************************************************************************************************************************
	#method modifyinh if merging queues are considered in the network model
	#def set_merging_ques_considered(self,n_v):
		#self._merging_ques_considered=n_v
#*****************************************************************************************************************************************************************************************

	#method returning the variable with the type of the employed control policy
	#def set_type_control_policy(self,n_v):
		#self._type_control_policy=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the dictionary, key =id node, value=control type
	#def set_dict_key_id_nd_value_ctrl_type(self,n_v):
		#self._dict_key_id_nd_value_ctrl_type=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the vector with the values of the distribution fct for the nb of departing vehicles from an actuated phase
	#def set_vector_distr_fct_nb_depart_veh(self,n_v):
		#self._vector_distr_fct_nb_depart_veh=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the type of the current control policy, we use it when a mixed control is applied to the network
	#def set_type_first_control_when_mixed_control_policy(self,n_v):
		#self._type_first_control_when_mixed_control_policy=n_v
		
#*****************************************************************************************************************************************************************************************
	#method modifying the type of simulator management, (for the veh departure), macro, micro
	#def set_type_sim_management(self,n_v):
		#self._type_sim_management=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the variable indicating if a fixed or stochastic travel duration will be employed
	def set_type_trav_duration_managament(self,n_v):
		self._type_trav_duration_managament=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the variable indicating whether we read the network control  or we calculate it
	def set_each_icm_read(self,n_v):
		self._each_icm_read=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the variable indicating the type of each vehicle regarding its final destination
	def set_type_veh_final_dest(self,n_v):
		self._type_veh_final_dest=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the variable indicating whether turn ratios are/not going to be estimated
	#def set_turn_ratios_estimated(self,n_v):
		#self._turn_ratios_estimated=n_v

#*****************************************************************************************************************************************************************************************
	
	#method modifying the variable indicating the parameter defining the  latest time for a vehicle to leave
	#when another veh of a compatible phase crosses an unsignalised intersection
	#def set_param_epsilon_t_latest_for_veh_to_leave_compatible_phase_nsi(self,n_v):
		#self._param_epsilon_t_latest_for_veh_to_leave_compatible_phase_nsi=n_v
	
#*****************************************************************************************************************************************************************************************
	#method modifying the dict with the paths to follow in order to reach a given exit link from a given entry link
	def set_dict_id_entry_exit_lk_value_unique_path(self,n_v):
		self._dict_id_entry_exit_lk_value_unique_path=n_
#*****************************************************************************************************************************************************************************************
	#method modifying  the variable  indicating whether we consider internal links with finite/infinite capacity
	def set_variable_indicating_finite_capacity_internal_links(self,n_v):
		self._variable_indicating_finite_capacity_internal_links=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the variable indicating the employed control category at the begin of the sim
	#def set_type_ctrl_category_at_the_beg_of_sim(self,n_v):
		#self._type_ctrl_category_at_the_beg_of_sim=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the file with the parameters of the FT or MP control 
	#def set_name_fi_values_ft_mp_control(self,n_v):
		#self._name_fi_values_ft_mp_control=n_v

#*****************************************************************************************************************************************************************************************
	#function creating the dictionary with the veh inform of a previously made demand
	#the key is the vehicle id and
	#the value is a list [t_vehicle_appearance_in_the_network, [id_entry_link, id_destination_link_1, id_destination_link_2,.... ] ]
	def fct_creat_dict_veh_prev_sim(self):
	
		#di=Global_Functions.fct_creating_dict_list_veh_files_creat_by_sim_treat(path_list_files=self._path_folder_veh_res_prev_sim,val_line_number=7)
		
		path_li_files=self._path_prev_generated_veh_demand+"/"+self._path_veh_res_when_in_fres_folder
		#path_li_files=self._path_veh_res_when_in_fres_folder
		#print("HERE",path_li_files)
		
		di=Global_Functions.fct_creating_dict_list_veh_files_creat_by_sim_treat(\
		veh_final_dest_dynam_construct=self._type_veh_final_dest,path_list_files=path_li_files)
		
		#path_li_files=self._path_prev_generated_veh_demand+"/"+self._path_veh_res_when_in_fres_folder
		#di=Global_Functions.fct_creating_dict_list_veh_files_creat_by_sim_treat(path_list_files=path_li_files,val_line_number=7)
		
		return di

#*****************************************************************************************************************************************************************************************
	#function creating the dictionary with the informatio of each entry link when a previously generated demand is considered
	def fct_creat_dict_information_entry_link_prev_sim(self,val_veh_final_dest_dynam_construct,val_dict_vehicle_inform):
		

		di=Global_Functions.fct_creat_dict_information_entry_link_prev_sim(\
		v_veh_final_dest_dynam_construct=val_veh_final_dest_dynam_construct,\
		v_dict_vehicle_inform=val_dict_vehicle_inform,\
		v_name_file_with_veh_ap_ev_end_sim_to_read=self._path_prev_generated_veh_demand+"/"+\
		self._name_file_with_veh_ap_ev_end_sim_to_read)
		
		
		
		#self._path_directory_prev_generated_veh_demand+"/"+\
		#a.get_name_file_veh_appearance_after_end_sim())
		return di
		

#*****************************************************************************************************************************************************************************************
	# function creating the dictionary with the informatio of each entry link when a given demand is considered
	#dict, key=id entry-internal lk, value=[..,t_veh_appearance,...]
	def fct_creat_dict_information_entry_link_given_demand(self):
	
		di=Global_Functions.fct_creat_dict_key_id_entry_lk_value_lis_t_veh_appear_given_demand(\
		name_file_read=self._folder_network_files+"/"+File_names_network_model.val_name_file_id_entry_lk_t_veh_appear_given_demand,\
		nb_comment_lines=1)
		#print(di[1])
		#import sys
		#sys.exit()
		
		return di
		

#*****************************************************************************************************************************************************************************************
	#method creating a list of which the ith element is the time at which end the ith cycle, 
	def fct_creat_list_t_end_each_cycle1(self,val_sim_duration, val_cycle_total_duration):
	
		#the number of cycles within the simulation duration (if there are 56.12 we return 57)
		nb_cycles=math.ceil(val_sim_duration/val_cycle_total_duration)
		
		li=[]
		
		for i in range(nb_cycles+1):
			li.append((i+1)*val_cycle_total_duration)
			
		return li

#*****************************************************************************************************************************************************************************************
	#method creating a list of which the ith element is the time at which end the ith cycle, 
	def fct_creat_list_t_end_each_cycle2(self,val_sim_duration, val_cycle_total_duration):
	
		#the number of cycles within the simulation duration (if there are 56.12 we return 57)
		nb_cycles=math.ceil(val_sim_duration/val_cycle_total_duration)
		
		li=[]
		
		#we consider that t_start sim=0
		if self._new_sim==1:
			for i in range(nb_cycles+1):
				li.append((i+1)*val_cycle_total_duration)
		else:
			for i in range(nb_cycles+1):
				val=(i+1)*val_cycle_total_duration+self._t_duration_previous_simulation
				li.append(val)
			
			
		return li

#*****************************************************************************************************************************************************************************************
	












