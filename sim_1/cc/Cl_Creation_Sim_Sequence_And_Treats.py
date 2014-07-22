import string
import List_Explicit_Values
import Cl_Creation_Object_Sim
import Cl_Data_Sim 
import Cl_Record_and_Treat_Sim_File_Names
import Creation_parameters_event_treatment
import Cl_Treatment_Sim_Res
import File_Sim_Name_Module_Files
import File_names_network_model
import Cl_Decisions
import Cl_Control_Actuate
import os
import time
from time import *

class Creation_Sim_Sequence_And_Treats:

	""" class performing simulation sequences and event treatments"""
	
	def __init__(self):
	
		#the name of the file indicating the names of the user (data) files in order to implement a series of simulations, f_d
		self._file_name_indicating_data_sim_user_files=File_Sim_Name_Module_Files.val_name_file_user_li_data_files
				
		#the name of the file where the names of recording files are written
		self._file_name_indicating_sim_record_file_names=File_Sim_Name_Module_Files.val_name_file_record_and_sim_treat_files
		
		#the file with the names of the folders and files for the stat analysis, "File_Stats_Anal_Folders_And_Files"
		self._file_stats_name_files=File_Sim_Name_Module_Files.val_name_file_stat_anal_folders_and_files
		
		#the module importing the file with the names of folders/files for the stat anaylis
		self._module_name_importing_file_names_stat_anal=__import__(self._file_stats_name_files)
		
		
				
#*****************************************************************************************************************************************************************************************
	#method returning the name of the file indicating the names of the user data files in order to implement a series of simulations
	def get_file_name_indicating_data_sim_user_files(self):
		return self._file_name_indicating_data_sim_user_files

#*****************************************************************************************************************************************************************************************
	#method returning the name of the file where the name of the recording files are written
	def get_file_name_indicating_sim_record_file_names(self):
		return self._file_name_indicating_sim_record_file_names

#*****************************************************************************************************************************************************************************************
	#method returning the file with the names of the folders and files for the stat analysis, "File_Stats_Anal_Folders_And_Files"
	def get_file_stats_name_files(self):
		return self._file_stats_name_files

#*****************************************************************************************************************************************************************************************
	#method returning the module importing the file with the names of folders/files for the stat analysis
	def get_module_name_importing_file_names_stat_anal(self):
		return self._module_name_importing_file_names_stat_anal

#*****************************************************************************************************************************************************************************************
	#method returning the folder whre all the FRes files will be placed
	#def get_folder_series_sims(self):
		#return self._folder_series_sims

#*****************************************************************************************************************************************************************************************

	#method modifying the name of the file indicating the names of the data files in order to implement a series of simulations
	def set_file_name_indicating_data_sim_user_files(self,n_v):
		self._file_name_indicating_data_sim_user_files=n_v


#*****************************************************************************************************************************************************************************************

	#method modifying the name of the file where the name of the recording files are written
	def set_file_name_indicating_name_sim_record_file_names(self,n_v):
		self._file_name_indicating_sim_record_file_names=n_v

#****************************************************************************************************************************************************************************************
	#method modifying the file with the names of the folders and files for the stat analysis, "File_Stats_Anal_Folders_And_Files"
	def set_file_stats_name_files(self,n_v):
		self._file_stats_name_files=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the module importing the file with the names of folders/files for the stat analysis
	def set_module_name_importing_file_names_stat_anal(self,n_v):
		self._module_name_importing_file_names_stat_anal=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the folder whre all the FRes files will be placed
	#def set_folder_series_sims(self,n_v):
		#self._folder_series_sims=n_v

#*****************************************************************************************************************************************************************************************

	#method copying some input files for the current run in the folder created by each sim Fres so as to
	#know to which data correspond the associated sim res folder Fres
	#val_user_name_file=Dsu
	def fct_copy_data_files_in_sim_res_folder(self,val_obj_record_and_treat_files,val_user_name_file,val_li_type_control,\
	val_name_file_mov_actuated_by_each_icm,val_path_and_name_folder_network,val_new_dem_generated):
		
		#cur_dir=os.getcwd()
		#a=os.listdir(File_Sim_Name_Module_Files.val_name_folder_with_control_param_files)
		#print(a)
		
		#b=os.path.isdir(File_Sim_Name_Module_Files.val_name_folder_with_control_param_files)
		#print(b)
		
		
		
		li_files_to_copy=[]
		for i in val_li_type_control:
			#1=FT,2:MP,3:Mixed,4:MP BC, 5: MP Wasteful,6:Predefined
			val_name_file_values_control_alg_1=None
			if Cl_Control_Actuate.TYPE_CONTROL[i]==Cl_Control_Actuate.TYPE_CONTROL[1]:
				fi_FT=File_Sim_Name_Module_Files.val_name_file_values_ft_control
				li_files_to_copy.append(fi_FT)
			elif Cl_Control_Actuate.TYPE_CONTROL[i]==Cl_Control_Actuate.TYPE_CONTROL[2]:
				fi_FOFS=File_Sim_Name_Module_Files.val_name_file_values_ft_offset_control
				li_files_to_copy.append(fi_FOFS)
			elif Cl_Control_Actuate.TYPE_CONTROL[i]==Cl_Control_Actuate.TYPE_CONTROL[3]:
				fi_MP=File_Sim_Name_Module_Files.val_name_file_values_mp_control
				fi_addit_MP=File_Sim_Name_Module_Files.val_name_addit_file_mp_control
				li_files_to_copy.append(fi_MP)
				li_files_to_copy.append(fi_addit_MP)
			#elif val_type_control==Cl_Control_Actuate.TYPE_CONTROL[4]:
				#val_name_file_values_control_alg=File_Sim_Name_Module_Files.val_name_file_values_ft_param_for_mixed_control
				#val_name_file_values_control_alg_1=File_Sim_Name_Module_Files.val_name_file_values_mp_param_for_mixed_control
			elif Cl_Control_Actuate.TYPE_CONTROL[i]==Cl_Control_Actuate.TYPE_CONTROL[5]:
				fi_MP_PRO=File_Sim_Name_Module_Files.val_name_file_values_mp_bc_control
				li_files_to_copy.append(fi_MP_PRO)
			#elif val_type_control==Cl_Control_Actuate.TYPE_CONTROL[6]:
				#val_name_file_values_control_alg=File_Sim_Name_Module_Files.val_name_file_values_predifined_control
			#elif val_type_control==Cl_Control_Actuate.TYPE_CONTROL[1,3]:
				#val_name_file_values_control_alg=File_Sim_Name_Module_Files.val_name_file_values_mp_control
			#elif val_type_control==Cl_Control_Actuate.TYPE_CONTROL[8]:
				#val_name_file_values_control_alg=File_Sim_Name_Module_Files.val_name_File_Pres_Stage_Duration_Control_Alg_Param
			elif Cl_Control_Actuate.TYPE_CONTROL[i]==Cl_Control_Actuate.TYPE_CONTROL[9]:
				fi_MP_no_outp_que=File_Sim_Name_Module_Files.val_name_file_values_mp_control_no_output_queues
				li_files_to_copy.append(fi_MP_no_outp_que)
			elif Cl_Control_Actuate.TYPE_CONTROL[i]==Cl_Control_Actuate.TYPE_CONTROL[10]:
				fi_FA_no_rec_clear=File_Sim_Name_Module_Files.val_name_File_fa_no_red_clear_control
				li_files_to_copy.append(fi_FA_no_rec_clear)
			elif Cl_Control_Actuate.TYPE_CONTROL[i]==Cl_Control_Actuate.TYPE_CONTROL[11]:
				fi_FA_MAX_green=File_Sim_Name_Module_Files.val_name_File_fa_max_green_control
				li_files_to_copy.append(fi_FA_MAX_green)
			elif Cl_Control_Actuate.TYPE_CONTROL[i]==Cl_Control_Actuate.TYPE_CONTROL[12]:
				fi_FA_with_red_clear=File_Sim_Name_Module_Files.val_name_File_fa_with_red_clear_control
				li_files_to_copy.append(fi_FA_with_red_clear)
			elif Cl_Control_Actuate.TYPE_CONTROL[i]==Cl_Control_Actuate.TYPE_CONTROL[13]:
				fi_MP_PRACT=File_Sim_Name_Module_Files.val_name_file_values_mp_practical_control
				fi_addit_MP_Pract=File_Sim_Name_Module_Files.val_name_addit_file_mp_pract_control
				li_files_to_copy.append(fi_MP_PRACT)
				li_files_to_copy.append(fi_addit_MP_Pract)
			elif Cl_Control_Actuate.TYPE_CONTROL[i]==Cl_Control_Actuate.TYPE_CONTROL[14]:
				fi_MP_No_rc=File_Sim_Name_Module_Files.val_name_file_values_mp_without_rc_control
				fi_addit_MP_No_rc=File_Sim_Name_Module_Files.val_name_addit_file_mp_without_rc_control
				li_files_to_copy.append(fi_MP_No_rc)
				li_files_to_copy.append(fi_addit_MP_No_rc)
			elif Cl_Control_Actuate.TYPE_CONTROL[i]==Cl_Control_Actuate.TYPE_CONTROL[15]:
				fi_MP_Pract_No_rc=File_Sim_Name_Module_Files.val_name_file_values_mp_pract_without_rc_control
				fi_addit_MP_Pract_No_rc=File_Sim_Name_Module_Files.val_name_addit_file_mp_pract_without_rc_control
				li_files_to_copy.append(fi_MP_Pract_No_rc)
				li_files_to_copy.append(fi_addit_MP_Pract_No_rc)
			else:
				print("PROBLEM IN CL_CREAT_SIM_AND_SEQ_AND_TREATS, FCT fct_copy_data_files_in_sim_res_folder,  val_type_control: ",i)
				import sys
				sys.exit()
			
		
		for j in li_files_to_copy:
			
			#we record the file with the parameters (duration) of the control  applied in the sim,
			val_obj_record_and_treat_files.fct_copy_file_in_sim_res_folder(File_Sim_Name_Module_Files.val_name_folder_with_control_param_files,j,j)
		
		#if two parameter files have been empoyed  the second file is also copied
		#if val_name_file_values_control_alg_1!=None:
			#val_obj_record_and_treat_files.fct_copy_file_in_sim_res_folder(File_Sim_Name_Module_Files.val_name_folder_with_control_param_files,\
			#val_name_file_values_control_alg_1,val_name_file_values_control_alg_1)
		
		
		
		#we record the file with the phases actuated by each ncm actuated
		#v_name_file_mov_actuated_by_each_ncm=val_path_and_name_folder_network+"/"+val_name_file_mov_actuated_by_each_ncm
		v_name_file_mov_actuated_by_each_icm=val_name_file_mov_actuated_by_each_icm
		val_obj_record_and_treat_files.fct_copy_file_in_sim_res_folder(val_path_and_name_folder_network,\
		v_name_file_mov_actuated_by_each_icm,val_name_file_mov_actuated_by_each_icm)
		
		#we record the file with the  permissive movements of a nsi
		val_obj_record_and_treat_files.fct_copy_file_in_sim_res_folder(val_path_and_name_folder_network,\
		File_names_network_model.val_name_file_stages_each_non_signalised_inters,\
		File_names_network_model.val_name_file_stages_each_non_signalised_inters)
		
		
		#we record the file with the link param for the travel time
		val_obj_record_and_treat_files.fct_copy_file_in_sim_res_folder(val_path_and_name_folder_network,\
		File_names_network_model.val_file_name_id_all_network_link_id_orig_dest_node_length_link_capacity_link_param_travel_duration,\
		File_names_network_model.val_file_name_id_all_network_link_id_orig_dest_node_length_link_capacity_link_param_travel_duration)
		
		
		
		val_user_name_file_1=val_user_name_file+".py"
		#we record the Dsu file
		val_obj_record_and_treat_files.fct_copy_file_in_sim_res_folder1(val_user_name_file,val_name=val_user_name_file_1)
		
		# we record the file with the demand at each entry link
		
		#the name of the module importing the user data 
		self._module_name_imp_sim_user_data=__import__(val_user_name_file)
		
		
		#val_path_name_fi_demand_param_entry_link="../"+self._module_name_imp_sim_user_data.val_name_folder_network_files+"/"+\
		#File_Sim_Name_Module_Files.val_name_fi_demand_param_entry_link
		
		#if a new demand is employed, we copy the demand file
		if val_new_dem_generated==List_Explicit_Values.initialisation_value_to_one:
			val_path_name_fi_demand_param_entry_link=File_names_network_model.val_file_name_demand_param_entry_link
		
			val_obj_record_and_treat_files.fct_copy_file_in_sim_res_folder(val_path_and_name_folder_network,\
			val_path_name_fi_demand_param_entry_link,\
			File_names_network_model.val_file_name_demand_param_entry_link)
		
		
		
		#val_path_name_inform_netwk_phases="../"+self._module_name_imp_sim_user_data.val_name_folder_network_files+"/"+\
		#File_Sim_Name_Module_Files.val_name_inform_netwk_phases
		
		val_path_name_inform_netwk_phases=File_names_network_model.\
		val_file_name_id_all_phases_max_queue_size_and_sat_flow_queue_type
		
		# we copy the file fi_id_all_phases_max_queue_size_sat_flow_queue_type.txt with the phase character (sat flow etc.)
		val_obj_record_and_treat_files.fct_copy_file_in_sim_res_folder(val_path_and_name_folder_network,\
		val_path_name_inform_netwk_phases,\
		File_names_network_model.val_file_name_id_all_phases_max_queue_size_and_sat_flow_queue_type)
		
		#we copy the file Creation_parameters_event_treatment.py so as to know which control (mp, ft) we applied 
		#to delete it when we are sure that sim funct ok
		val_obj_record_and_treat_files.fct_copy_file_in_sim_res_folder1(name_file="Creation_parameters_event_treatment",\
		val_name="Creation_parameters_event_treatment.py")
		
		#wec opy the file with the ctrl type applied to each node
		val_obj_record_and_treat_files.fct_copy_file_in_sim_res_folder2(\
		name_file=File_Sim_Name_Module_Files.val_name_folder_with_control_param_files+"/"+\
		File_Sim_Name_Module_Files.val_name_file_node_id_control_type_category,\
		val_name=File_Sim_Name_Module_Files.val_name_file_node_id_control_type_category)
		
		
		
		
		#"/Users/jennie/Desktop/SIM_INTERS/SMALL_DATA_INTERS_3/fi_demand_param_entry_link.txt","fi_demand_param_entry_link.txt")
		
		#self._module_name_imp_sim_user_data.val_name_folder_network_files+"/"+\
		#File_Sim_Name_Module_Files.val_name_fi_demand_param_entry_link)
		
		#val_obj_record_and_treat_files.fct_copy_file_in_sim_res_folder(self._module_name_imp_sim_user_data.val_name_folder_network_files+"/"+\
		#File_Sim_Name_Module_Files.val_name_fi_demand_param_entry_link)
		 
		
		
#****************************************************************************************************************************************************************************************
	#method examining whether the list with the ids of the output links of the queues of a link needs to be calculated or not
	#vval_ty_split_ratio_calcul = the type of the algo computing the split ratios
	def fct_exam_construction_li_id_output_links_of_all_queues_on_a_link_1(self,val_ty_split_ratio_calcul,val_turn_prob_estim):
		
		a=Cl_Decisions.Decisions()
		if val_ty_split_ratio_calcul in \
		a.fct_exam_whether_type_calc_split_ratios_requires_li_id_output_links_of_all_queues_of_link() or\
		val_turn_prob_estim==1:
			return 1
		else:
			return 0

#*****************************************************************************************************************************************************************************************
	#method examining whether the list with the ids of the output links of the queues of a link needs to be calculated or not
	#vval_ty_split_ratio_calcul = the type of the algo computing the split ratios
	def fct_exam_construction_li_id_output_links_of_all_queues_on_a_link_2(self,val_obj_data):
	
		a=Cl_Decisions.Decisions()
		
		if val_obj_data.get_type_veh_final_dest() in a.fct_li_policies_intial_defining_veh_final_destination() or\
		val_obj_data.get_turn_ratios_estimated()==1:
			return 1
		else:
			return 0
		
#*****************************************************************************************************************************************************************************************


	#method doind a series of sim 
	#list_data_files is a file containing all the data user files for each sim	
	def fct_sim_treat(self,list_data_files,va_nb_comment_lines_ft,va_nb_comment_lines_mp,va_nb_comment_lines_psd,\
	va_nb_comment_lines_ft_off,va_nb_comment_lines_fa,va_nb_comment_lines_fa_max_green,\
	va_di_param_ctrl_mp_practical_ctrl):
	
		
		#the dictionary with the parameter list for the treatment of each event
		#dict_param_event_treat=Creation_parameters_event_treatment_event_list.fct_creating_parameter_list_event_treat_event_heap()
		
		#creation of the folder where to place the Fres files when one or more sims are done
		#creation of a folder where we place all the Fres files created by the series of sims
		b=strftime("-%a-%d-%b-%Y_%H-%M-%S",localtime())
		os.mkdir(self._module_name_importing_file_names_stat_anal.name_folder_series_sims+b)
		
		self_folder_series_sims=self._module_name_importing_file_names_stat_anal.name_folder_series_sims+b
				
		
		#creation (of an empty) simulation object
		#cr_obj_sim=Cl_Creation_Object_Sim.Creation_Object_Sim()
		
		
		nb_files=len(list_data_files)
		#for each data file
		for i in range(nb_files):
			#print("HERE",list_data_files[i])
			
		
			#creation of a record files object
			obj_record_and_treat_files=Cl_Record_and_Treat_Sim_File_Names.Record_and_Treat_Sim_File_Names(\
			val_name_sim_record_file_names=self._file_name_indicating_sim_record_file_names,val_folder_series_sims=self_folder_series_sims)
			
			
			
			#we prepare the record files emloyed by the sim before the implementation, (open)
			#and we creae the file where the sim events will be recorded as txt
			obj_record_and_treat_files.preparation_record_files_before_start_sim()
			
			
			#creation of  data object
			obj_data_sim=Cl_Data_Sim.Data_Sim(val_name_file_with_veh_ap_ev_end_sim_to_read=\
			obj_record_and_treat_files.get_name_file_recording_veh_appear_event_remaining_in_ev_list_by_end_sim_before_open(),\
			val_path_veh_res_when_in_fres_folder=obj_record_and_treat_files.get_folder_with_veh_files_created_by_sim_treat_1(),\
			val_name_sim_user_file=str(list_data_files[i]))
			

			
			#if we wish to start a new simulation
			if obj_data_sim.get_new_sim()== List_Explicit_Values.initialisation_value_to_one:
			
				#the first queue of the network will have the id 1
				val_ind_que=List_Explicit_Values.initialisation_value_to_one
				
				#creation of a  "creation simulation object"
				#if we employ a given demand
				if obj_data_sim.get_creation_new_dem()==List_Explicit_Values.initialisation_value_to_minus_one:
					cr_obj_sim=Cl_Creation_Object_Sim.Creation_Object_Sim(val_t_start_sim=obj_data_sim.get_t_start_new_sim(),\
					val_t_duration_sim=obj_data_sim.get_t_simulation_duration(),val_new_vehicle_id=\
					obj_data_sim.get_last_created_veh_id_given_demand())
				#if we generate a new demand or employ a previously generated demand
				else:
					cr_obj_sim=Cl_Creation_Object_Sim.Creation_Object_Sim(val_t_start_sim=obj_data_sim.get_t_start_new_sim(),\
					val_t_duration_sim=obj_data_sim.get_t_simulation_duration())
				
				
				sim_obj=cr_obj_sim.fct_creation_object_sim(val_fi_name_user_data=list_data_files[i],\
				val_ind_queue=val_ind_que)
				
				
				#the dictionary with the parameter list for the treatment of each event
				dict_param_event_treat=Creation_parameters_event_treatment.fct_creating_parameter_list_event_treat_event_heap(\
				sim_obj,obj_data_sim,obj_record_and_treat_files)
				
				#we attribute it to the simulation object
				sim_obj.set_dict_parameters_fcts_event_treat(dict_param_event_treat)
				
				
				
				#we do the simulation
				sim_obj.simulation_1(\
				val_veh_previous_demand_have_dynam_constr_final_dest=obj_data_sim.get_type_veh_final_dest(),\
				val_creation_new_vehicle_demand=obj_data_sim.get_creation_new_dem(),\
				val_di_veh_inform_previous_sim=obj_data_sim.get_dict_veh_information_prev_sim(),\
				val_di_entry_link_info_previous_sim=obj_data_sim.get_dict_entry_link_information_prev_sim(),\
				val_di_entry_link_info_given_data=obj_data_sim.get_dict_information_entry_lk_given_demand(),\
				val_file_record_netw_obj_sim=obj_record_and_treat_files.get_file_recording_network_obj_sim(),\
				val_file_record_next_veh_id=obj_record_and_treat_files.get_file_recording_next_veh_id_obj_sim(),\
				val_file_record_pile_event_obj_sim=obj_record_and_treat_files.get_file_recording_pile_even_obj_sim(),\
				val_print_messages_on_terminal=obj_data_sim.get_print_messages_on_term(),\
				val_t_start_calcul_veh_appearance=obj_data_sim.get_t_marge_start_calcul_veh_appearance(),\
				val_t_start_sim=obj_data_sim.get_t_start_new_sim(),\
				val_t_unit=obj_data_sim.get_t_unit(),\
				val_ctm_connect=obj_data_sim.get_ctm_connect(),\
                val_fol_ctm_connect=obj_data_sim.get_fol_ctm_connect())
				
			
			
			#if we wish to continue a previously started simulation
			else:
			
				
				#creation of an empty   "creation simulation object"
				cr_obj_sim=Cl_Creation_Object_Sim.Creation_Object_Sim()
				
				
				#we create the sim object 
				sim_obj=cr_obj_sim.fct_recreation_object_sim_prev_sim(\
				val_fi_record_network_prev_sim=obj_data_sim.get_path_name_folder_results_sim_to_be_continued()+"/"+\
				obj_record_and_treat_files.get_name_file_recording_network_obj_sim(),\
				val_fi_record_ev_pile_prev_sim=obj_data_sim.get_path_name_folder_results_sim_to_be_continued()+"/"+\
				obj_record_and_treat_files.get_name_file_recording_pile_even_obj_sim(),\
				val_fi_record_next_veh_id_prev_sim=obj_data_sim.get_path_name_folder_results_sim_to_be_continued()+"/"+\
				obj_record_and_treat_files.get_name_file_recording_next_veh_id_obj_sim(),\
				val_name_data_folder=obj_data_sim.get_folder_network_files(),\
				val_file_name_demand_param_entry_link=obj_data_sim.get_file_name_demand_param_entry_link(),\
				val_name_file_user_data=list_data_files[i],\
				val_nb_comment_lines_ft=va_nb_comment_lines_ft,\
				val_nb_comment_lines_mp=va_nb_comment_lines_mp,\
				val_nb_comment_lines_ft_off=va_nb_comment_lines_ft_off,\
				val_nb_comment_lines_fa=va_nb_comment_lines_fa,\
				val_nb_comment_lines_fa_max_green=va_nb_comment_lines_fa_max_green)
				
				
				#the dictionary with the parameter list for the treatment of each event
				dict_param_event_treat=Creation_parameters_event_treatment.fct_creating_parameter_list_event_treat_event_heap(\
				sim_obj,obj_data_sim,obj_record_and_treat_files)
				
				
				
				
				#we attribute it to the simulation object
				sim_obj.set_dict_parameters_fcts_event_treat(dict_param_event_treat)
				
				#we complete the sim object
				#we define the sim duration
				sim_obj.set_t_duration_simulation(obj_data_sim.get_t_simulation_duration())
				
				
				#we do the simulation
				sim_obj.simulation_2(\
				val_file_record_netw_obj_sim=obj_record_and_treat_files.get_file_recording_network_obj_sim(),\
				val_file_record_next_veh_id=obj_record_and_treat_files.get_file_recording_next_veh_id_obj_sim(),\
				val_file_record_pile_event_obj_sim=obj_record_and_treat_files.get_file_recording_pile_even_obj_sim(),\
				val_print_messages_on_terminal=obj_data_sim.get_print_messages_on_term())
				
			
						
			#we copy the data files
			self.fct_copy_data_files_in_sim_res_folder(val_obj_record_and_treat_files=obj_record_and_treat_files,\
			val_user_name_file=list_data_files[i],\
			val_li_type_control=sim_obj.get_simul_system().get_network().get_li_employed_ctrl_types(),\
			val_name_file_mov_actuated_by_each_icm=File_names_network_model.val_name_file_stages_each_signalised_inters,\
			val_path_and_name_folder_network="../"+obj_data_sim.get_name_folder_network_files(),\
			val_new_dem_generated=obj_data_sim.get_creation_new_dem())
			
			
						
			# we record the veh appear events remained  in the event list
			obj_record_and_treat_files.fct_write_information_veh_appearance_event_in_ev_list_end_sim(\
			val_event_list=sim_obj.get_heap_even()) 
				
			
				
			#we prepare the files the sim has used, (we close them)
			obj_record_and_treat_files.preparation_record_files_after_end_sim()
				
			#if we wish to treat the sim results (produce the veh files etc.)
			if obj_data_sim.get_treat_sim_res()==List_Explicit_Values.initialisation_value_to_one:
				
				#we creat a tretament_sim_res_object
				treat_sim_res_obj=Cl_Treatment_Sim_Res.Treatment_Sim_Res(\
				val_db_file_sim_res_to_treat=obj_record_and_treat_files.get_folder_res_sim()+"/"+\
				obj_record_and_treat_files.get_name_file_recording_event_db(),\
				val_veh_file_to_write_res=obj_record_and_treat_files.get_file_veh_res(),\
				val_veh_final_dest_dynam_constructed=obj_data_sim.get_type_veh_final_dest())
					
				#we write the veh files
				treat_sim_res_obj.fct_write_file_vehicles_sim()
			
#*****************************************************************************************************************************************************************************************			

	#methode qui lit un fichier et  met toutes les valeurs dans un vecteur. 
	#Chaque element du vecteur retourne st sous forme string.
	def reading_file_res_string(self,name_f):
		
		f=open(name_f,"r")
		res=[]
		for i in f.readlines():
			a=i.rsplit()
			for j in a:
				res.append(j)
				#print("RES",res)
		f.close()
		return res
#*****************************************************************************************************************************************************************************************
	#method returning a list with the args for the method fct_sim_treat
	
	def creation_args_fct_sim_treat(self):
		
		#li_1=[self.reading_file_res_string(self._file_name_indicating_data_sim_user_files)]
		li_1=self.reading_file_res_string(self._file_name_indicating_data_sim_user_files)
		return li_1


#*****************************************************************************************************************************************************************************************

#cr=Creation_Sim_Sequence_And_Treats()
#lis=cr.creation_args_fct_sim_treat()
#print(lis)
#cr.fct_sim_treat(*lis)


#*****************************************************************************************************************************************************************************************










































