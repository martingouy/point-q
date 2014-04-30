import Cl_Event
import Cl_Treatment_Sim_Res
import Cl_Event
import File_Sim_Name_Module_Files
import List_Explicit_Values
import Cl_Vehicle_Queue
import Cl_Creation_Network
import Global_Functions
import File_Stats_Anal_Folders_And_Files
import Cl_Decisions
import operator
import os
import math


class Stat_Analysis:

	""" class creating information from the db file produced by a sim, employed for the statistical analysis """
	def __init__(self, val_folder_sim_files_for_stat_anal=None):
	
	
		#the file with the names of the folders and files for the stat analysis, "File_Stats_Anal_Folders_And_Files"
		self._file_stats_name_files=File_Sim_Name_Module_Files.val_name_file_stat_anal_folders_and_files
			
		#the module importing the file with the names of folders/files for the stat anaylis
		self._module_name_importing_file_names_stat_anal=__import__(self._file_stats_name_files)
		
		
		#the file name with  the file names for the recording during the sim,"Record_and_Treat_Sim_File_Names"
		self._file_name_record_and_sim_treat_files=File_Sim_Name_Module_Files.val_name_file_record_and_sim_treat_files
		
		
		#the module importing the file with the file names for the recording during the sim
		self._module_name_importing_file_name_record_and_sim_treat_files=__import__(self._file_name_record_and_sim_treat_files)
		
		
		#the  folder containing the files produced by the desired analysing sim
		#for ex "./FRes-Mon-10-Sep-2012_23-04-37"
		self._folder_sim_files_for_stat_anal=val_folder_sim_files_for_stat_anal
		
		
		#the folder where will be placed the folders with the various files produced by the stat analysis
		os.mkdir(self._folder_sim_files_for_stat_anal+"/"+self._module_name_importing_file_names_stat_anal.name_folder_stat_anal)
		
		self._folder_stat_anal=self._folder_sim_files_for_stat_anal+"/"+\
		self._module_name_importing_file_names_stat_anal.name_folder_stat_anal
		
		#the db file produced by the sim,  "file_recording_event_db.txt"
		self._db_file=self._folder_sim_files_for_stat_anal+"/"+self._module_name_importing_file_name_record_and_sim_treat_files.\
		val_name_file_recording_event_db
		
		#a Treatment_Sim_Res objet
		self._treat_sim_res_obj=Cl_Treatment_Sim_Res.Treatment_Sim_Res(val_db_file_sim_res_to_treat=self._db_file)
		
		#the folder with the vehicle information Sim_Treat
		#self._folder_veh_info=self._folder_sim_files_for_stat_anal+"/"+self._module_name_importing_file_name_record_and_sim_treat_files.\
		#val_name_folder_with_files_created_by_sim_treat
		
		#File_Sim_Name_Module_Files.val_name_file_record_and_sim_treat_files.\
		#val_name_file_recording_event_db
		
		#the folder where to add the files containg the evolution of each queue, during the analysed  sim,
		#"/FRes-Mon-10-Sep-2012_23-04-37/QUE_EVOL"
		os.mkdir(self._folder_stat_anal+"/"+\
		self._module_name_importing_file_names_stat_anal.name_folder_queue_evol)
		
		self._folder_que_evol_files=self._folder_stat_anal+"/"+\
		self._module_name_importing_file_names_stat_anal.name_folder_queue_evol
		
	
	
		#the file to write the res (already placed in the correct directory)
		#/FRes-Mon-10-Sep-2012_23-04-37/QUE_EVOL/"fi_evol_que_"
		self._file_to_write_que_res=self._folder_que_evol_files+"/"+self._module_name_importing_file_names_stat_anal.\
		name_file_queue_evol
		
		#****************** test with more info for each veh que **************************
		
		#the folder where to add the files containg the evolution of each queue, during the analysed  sim,
		#"/FRes-Mon-10-Sep-2012_23-04-37/QUE_EVOL"
		#os.mkdir(self._folder_stat_anal+"/"+\
		#self._module_name_importing_file_names_stat_anal.name_folder_queue_evol_1)
		os.mkdir(self._folder_sim_files_for_stat_anal+"/"+\
		self._module_name_importing_file_names_stat_anal.name_folder_queue_evol_1)

		
		#self._folder_que_evol_files_1=self._folder_stat_anal+"/"+\
		#self._module_name_importing_file_names_stat_anal.name_folder_queue_evol_1
		self._folder_que_evol_files_1=self._folder_sim_files_for_stat_anal+"/"+\
		self._module_name_importing_file_names_stat_anal.name_folder_queue_evol_1
		


		
		self._file_to_write_que_res_1=self._folder_que_evol_files_1+"/"+self._module_name_importing_file_names_stat_anal.\
		name_file_queue_evol_1
		
		#******************#******************#******************#******************#******************#******************		
		
		#the folder where to add the files containg the files with the number of veh in queue after each veh arrival/appearance
		#"/FRes-Mon-10-Sep-2012_23-04-37/QUE_EVOL_VEH_AR_AP"
		#os.mkdir(self._folder_stat_anal+"/"+\
		#self._module_name_importing_file_names_stat_anal.name_folder_nb_veh_que_ar_ap)
		
		#self._folder_nb_veh_que_ar_ap=self._folder_stat_anal+"/"+\
		#self._module_name_importing_file_names_stat_anal.name_folder_nb_veh_que_ar_ap
		
		#the file where to write the queue evol after each veh arrival/appear, (already placed in the correct directory)
		#"/FRes-Mon-10-Sep-2012_23-04-37/QUE_EVOL_VEH_AR_AP/fi_nb_veh_ar_ap_que_"
		#self._file_to_write_nb_veh_que_ar_ap=self._folder_nb_veh_que_ar_ap+\
		#"/"+self._module_name_importing_file_names_stat_anal.name_file_nb_veh_que_ar_ap
		
		
		#the folder where to add the files  with the number of departing veh from a que, "
		#/FRes-Mon-10-Sep-2012_23-04-37/QUE_EVOL_VEH_DEP"
		#os.mkdir(self._folder_stat_anal+"/"+\
		#self._module_name_importing_file_names_stat_anal.name_folder_nb_veh_dep_que)
		
		#self._folder_nb_veh_dep_que=self._folder_stat_anal+"/"+\
		#self._module_name_importing_file_names_stat_anal.name_folder_nb_veh_dep_que
		
		#the file with the number of departing veh from a que (already placed in the correct directory)
		#"FRes-Mon-10-Sep-2012_23-04-37/QUE_EVOL_VEH_DEP/fi_nb_veh_dep_que_"
		#self._file_nb_veh_dep_que=self._folder_nb_veh_dep_que+"/"+self._module_name_importing_file_names_stat_anal.\
		#name_file_nb_veh_dep_que
		
		#File_Sim_Name_Module_Files.val_name_file_stat_anal_folders_and_files.\
		#name_file_nb_veh_dep_que
		
		#the folder  where to add the files  with the number of vehicles in the queue and the number of times
		#"FRes-Mon-10-Sep-2012_23-04-37/QUE_NB_TIMES_NB_VEH_AR_AP"
		#os.mkdir(self._folder_stat_anal+"/"+\
		#self._module_name_importing_file_names_stat_anal.name_folder_nb_times_with_nb_veh_at_que_ar_ap)
		
		#self._folder_nb_times_with_nb_veh_at_que_ar_ap=self._folder_stat_anal+"/"+\
		#self._module_name_importing_file_names_stat_anal.name_folder_nb_times_with_nb_veh_at_que_ar_ap
		
		#the file with the number of vehicles in the queue and the number of times, (already placed in the correct directory)
		#"FRes-Mon-10-Sep-2012_23-04-37/QUE_NB_TIMES_NB_VEH_AR_AP/fi_nb_times_nb_veh_ar_ap_que_"
		#self._file_nb_times_with_nb_veh_at_que_ar_ap=self._folder_nb_times_with_nb_veh_at_que_ar_ap+"/"+\
		#self._module_name_importing_file_names_stat_anal.name_file_nb_times_nb_veh_que_ar_ap
		
		
		#the folder  where to add the files  with the number of departing vehicles from the queue and the number of times
		#"FRes-Mon-10-Sep-2012_23-04-37/"QUE_NB_TIMES_NB_VEH_DEP"
		os.mkdir(self._folder_stat_anal+"/"+\
		self._module_name_importing_file_names_stat_anal.name_folder_nb_times_with_nb_veh_dep_que)
		
		self._folder_nb_times_with_nb_veh_dep_que=self._folder_stat_anal+"/"+\
		self._module_name_importing_file_names_stat_anal.name_folder_nb_times_with_nb_veh_dep_que
		
		#the file with the number of depart vehicles from the queue and the number of times, (already placed in the correct directory)
		#"FRes-Mon-10-Sep-2012_23-04-37/QUE_NB_TIMES_NB_VEH_DEP/fi_nb_veh_dep_que_"
		self._file_nb_times_with_nb_dep_veh_from_que=self._folder_nb_times_with_nb_veh_dep_que+"/"+\
		self._module_name_importing_file_names_stat_anal.name_file_nb_times_nb_veh_dep_que
		
		#the folder to add the files with the mean travel time of each entry exit link
		os.mkdir(self._folder_stat_anal+"/"+\
		self._module_name_importing_file_names_stat_anal.name_folder_mean_travel_time_entry_exit_lk)
		
		self._folder_mean_travel_time_entry_exit_lk=self._folder_stat_anal+"/"+\
		self._module_name_importing_file_names_stat_anal.name_folder_mean_travel_time_entry_exit_lk
		
	
		
		self._file_name_folder_mean_travel_time_entry_exit_lk=self._folder_mean_travel_time_entry_exit_lk+"/"+\
		self._module_name_importing_file_names_stat_anal.name_file_mean_travel_time_entry_exit_lk
		
		
		
		#the file with the mean travel time between entry-exit links
		os.mkdir(self._folder_stat_anal+"/"+\
		self._module_name_importing_file_names_stat_anal.name_folder_traveled_dist_per_period_entry_exit_lk)
		
		#the folder with the files with the mean traveled distance between entry-exit link per period
		self._name_folder_mean_traveled_distance_per_period_entry_exit_lk=self._folder_stat_anal+"/"+\
		self._module_name_importing_file_names_stat_anal.name_folder_traveled_dist_per_period_entry_exit_lk
		
		#the folder to add the files with the evolution of each phase
		os.mkdir(self._folder_stat_anal+"/"+\
		self._module_name_importing_file_names_stat_anal.name_folder_ctrl_evol)
		
	
		self._folder_ctrl_evol=self._folder_stat_anal+"/"+\
		self._module_name_importing_file_names_stat_anal.name_folder_ctrl_evol
		
		
		#the folder to add the files with the evolutuon of each stage of each intersection
		os.mkdir(self._folder_stat_anal+"/"+\
		self._module_name_importing_file_names_stat_anal.name_folder_stage_evol_per_intersection)
		
		self._folder_stage_evol_inters=self._folder_stat_anal+"/"+\
		self._module_name_importing_file_names_stat_anal.name_folder_stage_evol_per_intersection
		
		#the folder to add the files with the evolutuon of each stage type 2 of each intersection
		#os.mkdir(self._folder_stat_anal+"/"+"STAGE_EVOL_NDS")
		
		#self._folder_stage_evol_nodes=self._folder_stat_anal+"/"+"STAGE_EVOL_nds"
		
		
		#the folder with the files indicating  the number ofstage  switches per itnersection node
		os.mkdir(self._folder_stat_anal+"/"+self._module_name_importing_file_names_stat_anal.name_folder_stage_switches_per_intersection)
		
		self._folder_stage_switches_per_intersection=self._folder_stat_anal+"/"+self._module_name_importing_file_names_stat_anal.name_folder_stage_switches_per_intersection
		

		
		
		#the folder to add the files  describing the evolution of each link
		os.mkdir(self._folder_stat_anal+"/"+\
		self._module_name_importing_file_names_stat_anal.name_folder_link_evol)
		
		self._folder_link_evol=self._folder_stat_anal+"/"+\
		self._module_name_importing_file_names_stat_anal.name_folder_link_evol
		
		#the folder to add the files with the queue evolution after each veh departure
		os.mkdir(self._folder_stat_anal+"/"+\
		self._module_name_importing_file_names_stat_anal.name_folder_queue_evol_after_veh_dep)
		
		self._folder_queue_evol_after_veh_dep=self._folder_stat_anal+"/"+\
		self._module_name_importing_file_names_stat_anal.name_folder_queue_evol_after_veh_dep
		
		#the file with he queue evolution after each veh departure
		self._file_queue_evol_after_veh_dep=self._folder_queue_evol_after_veh_dep+"/"+\
		self._module_name_importing_file_names_stat_anal.name_file_queue_evol_after_veh_dep
		
				
		# the folder for the sum of all queue values during the sim
		os.mkdir(self._folder_stat_anal+"/"+\
		self._module_name_importing_file_names_stat_anal.name_folder_sum_queues_evol)
		
		self._folder_sum_queues_evol=self._folder_stat_anal+"/"+\
		self._module_name_importing_file_names_stat_anal.name_folder_sum_queues_evol
		
		
		#the file with the values of the sum of all queues during sim
		self._file_sum_queue_evol=self._folder_sum_queues_evol+"/"+\
		self._module_name_importing_file_names_stat_anal.name_file_sum_queue_evol
		
		
		#the folder with the average value of the sum of the queues (sum of queues (t)/total number of vehicle queues)
		os.mkdir(self._folder_stat_anal+"/"+\
		self._module_name_importing_file_names_stat_anal.name_folder_average_sum_queues_evol)
		
		self.folder_average_sum_queue_evol=self._folder_stat_anal+"/"+\
		self._module_name_importing_file_names_stat_anal.name_folder_average_sum_queues_evol
		
		#the file with the values of the sum of all queues during sim
		self._file_average_sum_queue_evol=self.folder_average_sum_queue_evol+"/"+\
		self._module_name_importing_file_names_stat_anal.name_file_average_sum_queue_evol
		
		
		
		#the name of the file with the weighted mean  of the sum of queues
		self._file_mean_length_sum_queues=self._folder_stat_anal+"/"+\
		self._module_name_importing_file_names_stat_anal.name_file_mean_length_sum_queues
		
		
		#the file containing the number of veh in the sum of queues and the prob of having this number
		self._file_name_file_nb_veh_prob_sum_que=self._folder_stat_anal+"/"+\
		self._module_name_importing_file_names_stat_anal.name_file_nb_veh_prob_sum_que
		
		#the file containing the number of veh in the sum of queues and the prob of having this number
		self._file_name_file_nb_veh_prob_sum_que=self._folder_stat_anal+"/"+\
		self._module_name_importing_file_names_stat_anal.name_file_nb_veh_prob_sum_que
		
		#the folder with the file where the the file with the mean length of each queue is written
		os.mkdir(self._folder_stat_anal+"/"+\
		self._module_name_importing_file_names_stat_anal.name_folder_mean_time_spent_by_veh_in_que)
		
		self._folder_mean_value_each_queue=self._folder_stat_anal+"/"+\
		self._module_name_importing_file_names_stat_anal.name_folder_mean_time_spent_by_veh_in_que
		
				
		
		#the file with the mean  value spent by veh, for every queue
		self._file_mean_time_spent_by_veh_in_que=self._folder_mean_value_each_queue+"/"+\
		self._module_name_importing_file_names_stat_anal.name_file_mean_time_spent_by_veh_in_que
		
		#the file with the mean value of the average time spent by veh in ques
		self._file_mean_of_aver_sojourn_time=self._folder_mean_value_each_queue+"/"+\
		self._module_name_importing_file_names_stat_anal.val_name_file_mean_of_aver_sojourn_time
		
		#the folder with the veh of trav time evolution per time period, for each entry exit link
		os.mkdir(self._folder_stat_anal+"/"+\
		self._module_name_importing_file_names_stat_anal.name_folder_travel_time_per_period_entry_exit_lk)
		
		self._folder_travel_time_per_period_entry_exit_lk=self._folder_stat_anal+"/"+\
		self._module_name_importing_file_names_stat_anal.name_folder_travel_time_per_period_entry_exit_lk
		
		#the file with the trav time evolution per time period, for an entry exit link
		self._file_travel_time_per_period_entry_exit_link=self._folder_travel_time_per_period_entry_exit_lk+"/"+\
		self._module_name_importing_file_names_stat_anal.name_file_travel_time_per_period_entry_exit_link
		
		
		#the folder with the files with the total actuation duration per period of each phase
		os.mkdir(self._folder_stat_anal+"/"+\
		self._module_name_importing_file_names_stat_anal.name_folder_phase_act_durat_per_period)
		
		self._folder_phase_act_durat_per_period=self._folder_stat_anal+"/"+\
		self._module_name_importing_file_names_stat_anal.name_folder_phase_act_durat_per_period
		
		
#*****************************************************************************************************************************************************************************************	
		
	#method returning the file with the names of the folders and files for the stat analysis
	def  get_file_stats_name_files(self):
		return self._file_stats_name_files
#*****************************************************************************************************************************************************************************************
	#method returning the the module importing the file with the names of folders/files for the stat anaylis
	def get_module_name_importing_file_names_stat_anal(self):
		return self._module_name_importing_file_names_stat_anal
#*****************************************************************************************************************************************************************************************

	#method returning the folder containing the files for the stat analysis
	def get_folder_stat_anal(self):
		return self._folder_stat_anal
#*****************************************************************************************************************************************************************************************
	#method returning the db file produced by the sim,  "file_recording_event_db.txt"
	def get_db_file(self):
		return self._db_file
#*****************************************************************************************************************************************************************************************
	#method returning the treat_sim_res object
	def get_treat_sim_res_obj(self):
		return self._treat_sim_res_obj
#*****************************************************************************************************************************************************************************************
	#method returning the folder with the veh information
	#def get_folder_veh_info(self):
		#return self._folder_veh_info
#*****************************************************************************************************************************************************************************************


	#method returning the  file name with  the file names for the recording during the sim
	def get_file_name_record_and_sim_treat_files(self):
		return self._file_name_record_and_sim_treat_files

#*****************************************************************************************************************************************************************************************
	#method returning the module importing the file with the file names for the recording during the sim
	def get_module_name_importing_file_name_record_and_sim_treat_files(self):
		return self._module_name_importing_file_name_record_and_sim_treat_files

#*****************************************************************************************************************************************************************************************
	#method returning the   folder where the sim results, wished to be treated are recorded
	def get_folder_sim_files_for_stat_anal(self):
		return self._folder_sim_files_for_stat_anal
#*****************************************************************************************************************************************************************************************
	#method returning the the folder where to add the files containg the evolution of each queue, during the analysed  sim
	def get_folder_que_evol_files(self):
		return self._folder_que_evol_files

#*****************************************************************************************************************************************************************************************
	#method returning #the file to write the res (already placed in the correct directory)
	def get_file_to_write_que_res(self):
		return self._file_to_write_que_res
#*****************************************************************************************************************************************************************************************
	#method returning the name of the folder with the files describing the ctrl evolution of each phase
	def get_folder_ctrl_evol(self):
		return self._folder_ctrl_evol
#*****************************************************************************************************************************************************************************************
	#method returning the folder to add the files with the evolutuon of each stage of each intersection
	def get_folder_stage_evol_inters(self):
		return self._folder_stage_evol_inters
#*****************************************************************************************************************************************************************************************
	#method returning  the folder with the files  describing the evolution of each link
	def get_folder_link_evol(self):
		return self._folder_link_evol
#*****************************************************************************************************************************************************************************************
	#method returning the folder where to add the files containg the files with the number of veh in queue after each veh arrival/appearance
	def get_folder_nb_veh_que_ar_ap(self):
		return self._folder_nb_veh_que_ar_ap

#*****************************************************************************************************************************************************************************************
	#method returning the file where to write the queue evol after each veh arrival/appear, (already placed in the correct directory)
	def get_file_to_write_nb_veh_que_ar_ap(self):
		return self._file_to_write_nb_veh_que_ar_ap
	
#*****************************************************************************************************************************************************************************************
	#method returning folder where to add the files  with the number of departing veh from a que
	def get_folder_nb_veh_dep_que(self):
		return self._folder_nb_veh_dep_que
#*****************************************************************************************************************************************************************************************
	
	#method returning the file with the number of departing veh from a que (already placed in the correct directory)
	def get_file_nb_veh_dep_que(self):
		return self._file_nb_veh_dep_que
#*****************************************************************************************************************************************************************************************
	#method returning the folder  where to add the files  with the number of departing vehicles from the queue and the number of times
	def get_folder_nb_times_with_nb_veh_dep_que(self):
		return self._folder_nb_times_with_nb_veh_dep_que
#*****************************************************************************************************************************************************************************************
	#method returning the file with the number of depart vehicles from the queue and the number of times, (already placed in the correct directory)
	def get_file_nb_times_with_nb_dep_veh_from_que(self):
		return self._file_nb_times_with_nb_dep_veh_from_que

#*****************************************************************************************************************************************************************************************
	#method returning the folder to add the files with the mean travel time of each entry exit link
	def get_folder_mean_travel_time_entry_exit_lk(self):
		return self._folder_mean_travel_time_entry_exit_lk
#*****************************************************************************************************************************************************************************************

	#method returning the name of the file with the mean travel time between entry-exit links
	def get_file_name_folder_mean_travel_time_entry_exit_lk(self):
		return self._file_name_folder_mean_travel_time_entry_exit_lk

#*****************************************************************************************************************************************************************************************

	#method returning the name of the folder  to add the files with the queue evolution after each veh departure
	def get_folder_queue_evol_after_veh_dep(self):
		return self._folder_queue_evol_after_veh_dep
#*****************************************************************************************************************************************************************************************
	#method returning the name of the file with he queue evolution after each veh departure
	def get_file_queue_evol_after_veh_dep(self):
		return self._file_queue_evol_after_veh_dep
	
#*****************************************************************************************************************************************************************************************
	#method returning the folder for the sum of all queue values during the sim
	def get_folder_sum_queues_evol(self):
		return self._folder_sum_queues_evol
#*****************************************************************************************************************************************************************************************
	#method returning the folder with the file with the average values of the sum of the queeus during the sim
	def get_folder_sum_queues_evol(self):
		return self._folder_sum_queues_evol
#*****************************************************************************************************************************************************************************************
	#method returning the name of the folder with the files indicating the number of stage switches per itnersection
	def get_folder_stage_switches_per_intersection(self):
		return self._folder_stage_switches_per_intersection
#*****************************************************************************************************************************************************************************************
	#method returning the file with the values of the sum of all queues during sim
	def get_fIle_sum_queue_evol(self):
		return self._file_sum_queue_evol
#*****************************************************************************************************************************************************************************************
	#method returning the file with the values of the average sum of all queues during sim
	def get_file_average_sum_queue_evol(self):
		return self._file_average_sum_queue_evol

#*****************************************************************************************************************************************************************************************
	#method returning the file with the weighted mean  of the sum of queues
	def get_file_mean_length_sum_queues(self):
		return self._file_mean_length_sum_queues
#*****************************************************************************************************************************************************************************************
	#method returning the file containing the number of veh in the sum of queues and the prob of having this number
	def get_file_name_file_nb_veh_prob_sum_que(self):
		return self._file_name_file_nb_veh_prob_sum_que
#*****************************************************************************************************************************************************************************************
	#method returning the file with the mean  length of each queue
	def get_file_time_spent_by_veh_in_que(self):
		return self._file_time_spent_by_veh_in_que

#*****************************************************************************************************************************************************************************************
	#method returning the folder with the veh of trav time evolution per time period, for each entry exit link
	def get_folder_travel_time_per_period_entry_exit_lk(self):
		return self._folder_travel_time_per_period_entry_exit_lk

#*****************************************************************************************************************************************************************************************
	#method returning the file with the trav time evolution per time period, for an entry exit link
	def get_file_travel_time_per_period_entry_exit_link(self):
		return self._file_travel_time_per_period_entry_exit_link
#*****************************************************************************************************************************************************************************************
	#merhod returning the  folder with the files with the total actuation duration per period of each phase
	def get_folder_phase_act_durat_per_period(self):
		return self._folder_phase_act_durat_per_period
#*****************************************************************************************************************************************************************************************
	#method returning the folder with the files with the mean traveled distance between entry-exit link per period
	def get_name_folder_mean_traveled_distance_per_period_entry_exit_lk(self):
		return self._name_folder_mean_traveled_distance_per_period_entry_exit_lk
#*****************************************************************************************************************************************************************************************
	#method returning the folder with the file where the mean queue lengths are written
	#def get_folder_mean_queue_length(self):
		#return self._folder_mean_queue_length

#*****************************************************************************************************************************************************************************************

	#method returning the file with the mean queue length of each phase
	#def get_file_mean_queue_length(self):
		#return self._file_mean_queue_length

#*****************************************************************************************************************************************************************************************

	#method modifying the file with the names of the folders and files for the stat analysis
	def  set_file_stats_name_files(self,n_v):
		self._file_stats_name_files=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying  the folder with the files  describing the evolution of each link
	def set_folder_link_evol(self,n_v):
		self._folder_link_evol=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the name of the folder with the files  describing the evolution of each link
	def set_folder_link_evol(self,n_v):
		self._folder_link_evol=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the the module importing the file with the names of folders/files for the stat anaylis
	def set_module_name_importing_file_names_stat_anal(self,n_v):
		self._module_name_importing_file_names_stat_anal=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the folder containing the files for the stat analysis
	def set_folder_stat_anal(self,n_v):
		self._folder_stat_anal=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the db file produced by the sim,  "file_recording_event_db.txt"
	def set_db_file(self,n_v):
		self._db_file=n_v

#*****************************************************************************************************************************************************************************************
	#method returning the treat_sim_res object
	def set_treat_sim_res_obj(self,n_v):
		self._treat_sim_res_obj=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the folder with the veh information
	#def set_folder_veh_info(self,n_v):
		#self._folder_veh_info=n-v
#*****************************************************************************************************************************************************************************************

	#method modifying the  file name with  the file names for the recording during the sim
	def set_file_name_record_and_sim_treat_files(self,n_v):
		self._file_name_record_and_sim_treat_files=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the module importing the file with the file names for the recording during the sim
	def set_module_name_importing_file_name_record_and_sim_treat_files(self,n_v):
		self._module_name_importing_file_name_record_and_sim_treat_files=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the   folder where the sim results, wished to be treated are recorded
	def set_folder_sim_files_for_stat_anal(self,n_v):
		self._folder_sim_files_for_stat_anal=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the the folder where to add the files containg the evolution of each queue, during the analysed  sim
	def set_folder_que_evol_files(self,n_v):
		self._folder_que_evol_files=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the file to write the res (already placed in the correct directory)
	def set_file_to_write_que_res(self,n_v):
		self._file_to_write_que_res=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the folder where to add the files containg the files with the number of veh in queue after each veh arrival/appearance
	def set_folder_nb_veh_que_ar_ap(self,n_v):
		self._folder_nb_veh_que_ar_ap=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the file where to write the queue evol after each veh arrival/appear, (already placed in the correct directory)
	def set_file_to_write_nb_veh_que_ar_ap(self,n_v):
		self._file_to_write_nb_veh_que_ar_ap=n_v
	
#*****************************************************************************************************************************************************************************************
	#method modifying folder where to add the files  with the number of departing veh from a que
	def set_folder_nb_veh_dep_que(self,n_v):
		self._folder_nb_veh_dep_que=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the file with the number of departing veh from a que (already placed in the correct directory)
	def set_file_nb_veh_dep_que(self,n_v):
		self._file_nb_veh_dep_que=n_v
#*****************************************************************************************************************************************************************************************

	#method modifying the file to write the queue length during a vehicle arrival or appearance event, already placed in the correct directory)
	def set_file_to_write_que_res_veh_arrival_appear(self,n_v):
		self._file_to_write_que_res_veh_arrival_appear=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the file to write the number of vehicles in the queue and the number of times that we had this nb of veh, during the sim
	def set_file_write_nb_veh_ar_ap_queue_nb_times(self,n_v):
		self._file_write_nb_veh_ar_ap_queue_nb_times=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the file to write the neumber of departing vehicles of a queue
	def set_file_write_nb_veh_depart_queue_nb(self,n_v):
		self._file_write_nb_veh_depart_queue_nb=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the name of the file to write the veh id and the veh travel time
	def set_file_write_veh_id_and_travel_time(self,n_v):
		self._file_write_veh_id_and_travel_time=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the folder  where to add the files  with the number of departing vehicles from the queue and the number of times
	def set_folder_nb_times_with_nb_veh_dep_que(self,n_v):
		self._folder_nb_times_with_nb_veh_dep_que=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the file with the number of depart vehicles from the queue and the number of times, (already placed in the correct directory)
	def set_file_nb_times_with_nb_dep_veh_from_que(self,n_v):
		self._file_nb_times_with_nb_dep_veh_from_que=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the folder to add the files with the mean travel time of each entry exit link
	def set_folder_mean_travel_time_entry_exit_lk(self,n_v):
		self._folder_mean_travel_time_entry_exit_lk=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the name of the file with the mean travel time between entry-exit links
	def set_file_name_folder_mean_travel_time_entry_exit_lk(self,n_v):
		self._file_name_folder_mean_travel_time_entry_exit_lk=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the name of the folder  to add the files with the queue evolution after each veh departure
	def set_folder_queue_evol_after_veh_dep(self,n_v):
		self._folder_queue_evol_after_veh_dep=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the name of the file with he queue evolution after each veh departure
	def set_file_queue_evol_after_veh_dep(self,n_v):
		self._file_queue_evol_after_veh_dep=n_v
	
#*****************************************************************************************************************************************************************************************
	#method returning the file with the mean  length of each queue
	def set_file_time_spent_by_veh_in_que(self,n_v):
		self._file_time_spent_by_veh_in_que=n_v

#*****************************************************************************************************************************************************************************************

	#method modifying the folder for the sum of all queue values during the sim
	def set_folder_sum_queues_evol(self,n_v):
		self._folder_sum_queues_evol=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the folder for the average value of the sum of all queue values during the sim
	def set_folder_average_sum_queue_evol(self):
		return self._folder_average_sum_queue_evol
#*****************************************************************************************************************************************************************************************
	#method modifying the file with the values of the sum of all queues during sim
	def set_file_sum_queue_evol_end_cycle(self,n_v):
		self._file_sum_queue_evol=n_v

#*****************************************************************************************************************************************************************************************

	#method modifying the file with the average values of the sum of all queues during sim
	def set_file_average_sum_queue_evol(self,n_v):
		self._file_average_sum_queue_evol=n_file_average_sum_queue_evo
#*****************************************************************************************************************************************************************************************
	#method modifying the file with the weighted mean  of the sum of queues
	def set_file_mean_length_sum_queues(self,n_v):
		self._file_mean_length_sum_queues=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the name of the folder with the files indicating the number of stage switches per itnersection
	def set_folder_stage_switches_per_intersection(self,n_v):
		self._folder_stage_switches_per_intersection=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the file containing the number of veh in the sum of queues and the prob of having this number
	def set_file_name_file_nb_veh_prob_sum_que(self,n_v):
		self._file_name_file_nb_veh_prob_sum_que=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the file with the mean  length of each queue
	def set_file_time_spent_by_veh_in_que(self,n_v):
		self._file_time_spent_by_veh_in_que=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the folder with the veh of trav time evolution per time period, for each entry exit link
	def set_folder_travel_time_per_period_entry_exit_lk(self,n_v):
		self._folder_travel_time_per_period_entry_exit_lk=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the file with the trav time evolution per time period, for an entry exit link
	def set_file_travel_time_per_period_entry_exit_link(self,n_v):
		self._file_travel_time_per_period_entry_exit_link=n_v
#*****************************************************************************************************************************************************************************************
	#merhod modifying the  folder with the files with the total actuation duration per period of each phase
	def set_folder_phase_act_durat_per_period(self,n_v):
		self._folder_phase_act_durat_per_period=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the folder to add the files with the evolutuon of each stage of each intersection
	def set_folder_stage_evol_inters(self,n_v):
		self._folder_stage_evol_inters=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the folder with the files with the mean traveled distance between entry-exit link per period
	def set_name_folder_mean_traveled_distance_per_period_entry_exit_lk(self,n_v):
		self._name_folder_mean_traveled_distance_per_period_entry_exit_lk=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the folder with the file where the mean queue lengths are written
	#def set_folder_mean_queue_length(self,n_v):
		#self._folder_mean_queue_length=n_v

#*****************************************************************************************************************************************************************************************

	#method modifying the file with the mean queue length of each phase
	#def set_file_mean_queue_length(self,n_v):
		#self._file_mean_queue_length=n_v

#*****************************************************************************************************************************************************************************************
	#method calculating the avearge length value of a queue, employed formula  
	#it returns a list [ mean time spent by veh in this queue, nb of veh]
	#sum (t_exit-veh-from-queue -  t_entry-veh-to-que)/nb_veh-enter-exit-que
	#id_queu=[id_current_link, id_dest_link]
	def fct_calcul_average_time_spent_by_veh_in_a_que_1(self,id_que=[], dict_key_movem_value_record_obj={}):
		
		dif=0
		nb_veh=0
		for i in dict_key_movem_value_record_obj[id_que]:
			if i.get_ev_type()== Cl_Event.TYPE_EV["type_ev_end_veh_departure_from_que"]:
				#print("id_queue=",id_que,"dep",i.get_time_veh_departure_from_current_queue(),"ar",i.get_time_veh_arrival_at_current_queue())
				dif+=i.get_time_veh_departure_from_current_queue()-i.get_time_veh_arrival_at_current_queue()
			
				nb_veh+=1
				
				#print("dif",dif,"nb_veh",nb_veh)
			#print("id_que=",id_que,"nb veh1, ",nb_veh)
		if nb_veh !=0:			
			return [round(dif/nb_veh,2),nb_veh]
		else:
			return [0,0]
#*****************************************************************************************************************************************************************************************
	#method calculating the average length of each queue of the network
	#it returns a a list, [ dict, the mean value of the average time spent by veh in queues]
	#dictionary of which key=queue id (ex [1,2]), value= [the average length of the queue, nb of veh went through the que]
	def fct_calcul_average_time_spent_by_veh_in_a_que_for_each_que_1(self,dict_key_mov_value_record_obj={}):
		di={}
		som=0
		for i in dict_key_mov_value_record_obj:
			di[i]=self.fct_calcul_average_time_spent_by_veh_in_a_que_1(id_que=i, dict_key_movem_value_record_obj=dict_key_mov_value_record_obj)
			som+=di[i][0]
			
			
		return [di,round(som/len(dict_key_mov_value_record_obj),2)]

#***************************************************************************************************************************************************************************************** 
	#method calculating the avearge length value of a queue, returns [average time spent by veh in que, nb_veh]
	#employed formula sum ni x ti / sum ni, where ni=observed value of queue length, ti=total time during which the queue had this length
	#di_key_nb_veh_que_value_prob_and_dur_time list= [dict,
	#dict, key=nb of veh, 
	#value= [ [prob, time with this number of veh at queue], total nb veh]
	def fct_calcul_average_time_spent_by_veh_in_a_que_2(self, di_key_nb_veh_que_value_prob_and_dur_time,\
	val_round_prec=1):
	
		som=0
		
		#print("HERE3",di_key_nb_veh_que_value_prob_and_dur_time)
		
		#print()
		
		
		for i in di_key_nb_veh_que_value_prob_and_dur_time[0]:
		
			#sum ni x ti
			som+=di_key_nb_veh_que_value_prob_and_dur_time[0][i][1] * i
			#print(di_key_nb_veh_que_value_prob_and_dur_time[0])
			
			
			
		if di_key_nb_veh_que_value_prob_and_dur_time[1] !=0:
		
			#print(round(som/di_key_nb_veh_que_value_prob_and_dur_time[1],2),i)
			
			#we return the number of vehicles in the queue for the plot
			#print(i)
			#import sys
			#sys.exit()
			#return [round(som/di_key_nb_veh_que_value_prob_and_dur_time[1],2),i]
			return [round(som/di_key_nb_veh_que_value_prob_and_dur_time[1],val_round_prec),di_key_nb_veh_que_value_prob_and_dur_time[1]]
		else:
			return 0
#***************************************************************************************************************************************************************************************** 
	#method calculating the average length of each queue of the network
	#it returns a a list, [ dict, the mean value of the average time spent by veh in queues]
	
	#di_key_mov_val_sorted_li_t_que_length= dict, key=mov, 
	#value =list [  [ ...,sorted li,...]=[ ..[t, que length at t],..], nb of depart veh + veh remained in the que by the end of sim ]
	def fct_calcul_average_time_spent_by_veh_in_a_que_for_each_que_2(self,di_key_mov_val_sorted_li_t_que_length,val_durat_sim,\
	val_round_prec=1):
	
		di_1={}
		som=0
		#print(di_key_mov_val_sorted_li_t_que_length)
		#import sys
		#sys.exit()
		for i in di_key_mov_val_sorted_li_t_que_length:
			
			#if i[0]==9 and i[1]==14:
				#print(di_key_mov_val_sorted_li_t_que_length[i])
				
			
			#di=key nb of veh in queue i, value =[prob, time with this number of veh at queue]
			di=self.fct_calc_prob_of_nb_veh_at_queue_and_duration(li_t_que_len=di_key_mov_val_sorted_li_t_que_length[i][0],\
			dur_sim=val_durat_sim)
			#if i[0]==9 and i[1]==14:
				#print(di)
				
			
			lis=[di,di_key_mov_val_sorted_li_t_que_length[i][1]]
			#print("lis",lis)
			
			
			
			#di_1[i]=list [average time spend by veh in the queue i , nb of veh arrived in  queue]
			di_1[i]=self.fct_calcul_average_time_spent_by_veh_in_a_que_2(di_key_nb_veh_que_value_prob_and_dur_time=lis)
			
			#if i[0]==9 and i[1]==14:
				#print(di_1[i])
				#import sys
				#sys.exit()
			
			#print("i=",i,"di_1[i]",di_1[i])
			som+=di_1[i][0]
			
			#print("HERE1","i: ",i, "di_1[i]", di_1[i],"som/len(di_key_mov_val_sorted_li_t_que_length",som/len(di_key_mov_val_sorted_li_t_que_length))
		#print()
		#print("HERE5",di_1)
		return [di_1,round(som/len(di_key_mov_val_sorted_li_t_que_length),val_round_prec)]
		

		
		
#***************************************************************************************************************************************************************************************** 
	#method calculating the average length of each queue of the network
	#it returns a a list, [dict, the mean value of the average time spent by veh in queues]
	#dict= diction, key=mov, value=list [average time spend by veh in the queue, nb of veh arrived in the queue]
	#di_key_nb_veh_que_val_prob_and_dur=dict, key=nb of veh in the que, value=[prob of having this nb of veh in que, total time with this nb of veh in que]
	#di_key_mov_val_sorted_li_t_que_length= dict, key=mov, 
	#value =list [  [ ...,sorted li,...]=[ ..[t, que length at t],..], nb of depart veh + veh remained in the que by the end of sim ]
	def fct_calcul_average_time_spent_by_veh_in_a_que_for_each_que_2_2(self,di_key_nb_veh_que_val_prob_and_dur,\
	di_key_mov_val_sorted_li_t_que_length):
	
		#dict, key=mov, value=list [average time spend by veh in the queue, nb of veh in the queue]
		di_1={}
		som=0
		#print(di_key_mov_val_sorted_li_t_que_length)
		#import sys
		#sys.exit()
		
		
		for i in di_key_mov_val_sorted_li_t_que_length:
			

			lis=[di_key_nb_veh_que_val_prob_and_dur,di_key_mov_val_sorted_li_t_que_length[i][1]]
			
			#di_1[i]=list [average time spend by veh in the queue sum og qur, nb of veh arrived in the queue]
			di_1[i]=self.fct_calcul_average_time_spent_by_veh_in_a_que_2(di_key_nb_veh_que_value_prob_and_dur_time=lis)
			
			#print("i=",i,"di_1[i]",di_1[i])
			som+=di_1[i][0]
			
			#print("HERE1","i: ",i, "di_1[i]", di_1[i],"som/len(di_key_mov_val_sorted_li_t_que_length",som/len(di_key_mov_val_sorted_li_t_que_length))
		
		return [di_1,round(som/len(di_key_mov_val_sorted_li_t_que_length),2)]
		
#***************************************************************************************************************************************************************************************** 
	#method reading a file with the lengths of a queue and returns the maximum length
	def fct_calcul_max_que_size(self,name_file_read):
		
		#we open the file
		file=open(name_file_read,"r")
		
		li=[]
		
		#each line is: time, queue size
		for i in file.readlines():
			a=i.rsplit()
			
			li.append(eval(a[1]))
		
		return max(li)
	
						
		
#***************************************************************************************************************************************************************************************** 
	

	#method returning the sum of the queues at each t sim
	#val_li_t_sim=an ordered list with the sim times
	#li_v_q= a list, its ith element is [... [time, queue val],...] of a queue
	def fct_calc_som_que_t_sim(self,val_li_t_sim,val_li_v_q):
		li=[]
	
		som=0
		#for each sim time
		for i in val_li_t_sim:
			#print("i=", i)
			som=0
		
			#for each queue, val_li_v_q=[ [inform file 1], [information file 2],...], inform file 1=[ ...., [t_i, legnth queue_1 et t_i],...]	
			#print("val_li_v_q=",val_li_v_q)
			for j in val_li_v_q:
				#print("j=",j)
				for k in range(len(j)):
					#print("k=",k,"i=",i,"j[k][0]",j[k][0])
					if i<j[k][0]:
						if k!=0:
							val=j[k-1][1]
						else:
							val=0
						som+=val
						#print("som",som)
						break
					elif i==j[k][0]:
						val=j[k][1]
						som+=val
						#print("som",som)
						break
					# if  i >j[k][0]
					elif i >j[k][0] and k+1==len(j):
					
						#print("HERE","i=",i,"j[k][0]",j[k][0])
						#import sys
						#sys.exit()
						val=j[k][1]
						som+=val
			li.append([i,som])
					
		return li

#***************************************************************************************************************************************************************************************** 
	#method returning the sum of the queues at each t sim, from the queue files
	def fct_calcul_sum_que_t_sim(self,val_path_list_files):

		li_t_que_val=self.fct_sim_u_t_instances_and_que_inf(val_li_path_files=val_path_list_files)
		
	
		#print("Cl_STAT ANAL, fct_calcul_sum_que_t_sim",li_t_que_val[1])
		#import sys
		#sys.exit()
		
		li_sum=self.fct_calc_som_que_t_sim(val_li_t_sim=li_t_que_val[0],val_li_v_q=li_t_que_val[1])
	
		return li_sum

#*****************************************************************************************************************************************************************************************
	#method returning the average value sum of the queues at each t sim, from the queue files, regarding the total number of network queues
	#average value sum of all the network queues at time t= the sum of network queeus at time t/ total number of network queeus
	def fct_calcul_average_sum_que_t_sim(self,val_path_list_files,val_total_nb_network_queues):

		li_t_que_val=self.fct_sim_u_t_instances_and_que_inf(val_li_path_files=val_path_list_files)
		
	
		#print("Cl_STAT ANAL, fct_calcul_sum_que_t_sim",li_t_que_val[1])
		#import sys
		#sys.exit()
		
		
		#li_sum_1=[...,[time, queue value],...]
		li_sum_1=self.fct_calc_som_que_t_sim(val_li_t_sim=li_t_que_val[0],val_li_v_q=li_t_que_val[1])
		
		
		#li_sum=[...,[time, queue value/total nb of vehicle queues in the network],...]
		li_sum=[]
		for i in li_sum_1:
			#print()
			#print("i[1]",i[1],"val_total_nb_network_queues",val_total_nb_network_queues,round(i[1]/val_total_nb_network_queues,2))
			average_que_size=round(i[1]/val_total_nb_network_queues,2)
			li_sum.append([i[0],average_que_size])
		
		return li_sum

#*****************************************************************************************************************************************************************************************
	#method calcul the prob of a existing n vehicles at  the sum of queues
	#returns a dictionary, key=nb of veh, value=[prob, time with this number of veh at queue]
	#li_t_que_len=[....[time, queue length at time t]...]
	def fct_calc_prob_of_nb_veh_at_queue_and_duration(self,li_t_que_len,dur_sim):
	
		li_1=list(li_t_que_len)
		#print("li_1",li_1)
		
		#we add a 3rd elem to li_1 indicating the duartion of the time with this que length
		for i in range(len(li_1)-1):
			li_1[i].append(li_1[i+1][0]-li_1[i][0])
		#we add 1 sec for the last time
		li_1[len(li_1)-1].append(1)
		
		#print()
		#print("li_1 after",li_1)
		
		#di=dict, key=queue length, value=[dur 1, dur2,..]]	
		di={}
		#li_1=[[t,queue length,duration of this queue length],..] ex li_1=[[4,3,3],[7,1,1]...]
		#print("li_1",li_1)
		for i in li_1:
			#print("i=",i)
			if i[1] not in di:
				di[i[1]]=[i[2]]
			else:
				di[i[1]].append(i[2])
		#print()
		#print("di",di)
		#di_1=dict, key=nb of veh in the que, value=[prob of having this number of veh in the que, total time with this nb of veh in the queue]
		#prob of having this number of veh in the que=total time with this number of veh in the que/sim duration		
		di_1={}
		for i in di:
			dur=sum(di[i])
			di_1[i]=[dur/dur_sim, dur]
			#print("i",i,"dur",dur,"dur_sim",dur_sim,"dur/dur_sim",dur/dur_sim)
		#print(di)
		return di_1
				
		
			
		

#***************************************************************************************************************************************************************************************** 				
	#method calculating the weight mean and stan dev of sum of queues and returns a list 
	#[weighted mean, stand deviat, mean-stan dev, mean+stan dev]
	#dict_nb_veh_que_and_dur=dict, key=number of veh at queue, value=[ prob of having that number, time duration with this number]
	def fct_calc_weighted_mean_sd_sum_que(self,dict_nb_veh_que_and_dur,dur_sim,val_round_prec=1):


		w_s=0
		v_s=0
		
		for i in dict_nb_veh_que_and_dur:
			w_s+=i*dict_nb_veh_que_and_dur[i][1]
			v_s+=(i**2)*dict_nb_veh_que_and_dur[i][1]
			#print("w_s=",w_s,"v_s=",v_s)
			#print()
		
		
		#print("w_s=",w_s,"sd_s=",v_s)
		#sd=math.sqrt(var)
		#print(" [w_s/dur_sim,sd]",w_s/dur_sim,sd)
		#a=round(w_s/dur_sim,2)
		#b=round(sd,2)
		#print("a=",a,"b=",b)
		#return [a,b,a-b,a+b]
		
		moy=w_s/dur_sim
		#print(moy,moy**2)
		
		var=(v_s/dur_sim)-(moy**2)
		#print(var)
		#print("var=",var)
		sd=math.sqrt(var)
		a=round(moy,val_round_prec)
		b=round(sd,val_round_prec)
		c=round(a-b,val_round_prec)
		d=round(a+b,val_round_prec)
		#print([a,b,c,d])
		#print("v_s",v_s,"dur_sim",dur_sim,"v_s/dur_sim",v_s/dur_sim,"moy",moy)
		return[a,b,c,d]
#***************************************************************************************************************************************************************************************** 		
			
	

	
	#method returning a dictionary, key=the element of a list, value= the mumber of its occurences 
	#this method will be used to plot a piechart (ex veh arrivals/appearances at a queue) 
	#ex li=[1,5,6,1] , the result will be di={1:2,5:1,6:1  }
	def fct_creat_dict_nb_occurences_elem_list1(self,li):
		#we sort the list
		li.sort()
		di={}
		#print("li",li)
		#print()
		if len(li)>0:
			i=min(li)
			for j in range(max(li)):
				#print(j,"i,",i)
				if i not in di:
					if i in li:
						di[i]=li.count(i)
				i+=1
		return di
#*****************************************************************************************************************************************************************************************


	#method returning a dictionary, key=the element of a list, value= the mumber of its occurences 
	#this method will be used to plot a piechart (ex veh arrivals/appearances at a queue) 
	#ex li=[1,5,6,1] , the result will be di={1:2,5:1,6:1  }
	def fct_creat_dict_nb_occurences_elem_list(self,li):
		#we sort the list
		li.sort()
		di={}
		#print("li",li)
		#print()
		
		i=min(li)
		for j in range(max(li)):
			#print(j,"i,",i)
			if i not in di:
				if i in li:
					di[i]=li.count(i)
			i+=1
		return di
#*****************************************************************************************************************************************************************************************
	
	#val_dict={1:8,5:1,6:1  }, key=any value, value= the nb of times the key was observed, ew, we had 8 times the value 1, 1 time value 5 etc
	#we return a dict, key=the key of val_dict, value=[ key of val_dict,appearing percentage of this observation] 
	def fct_creat_dict_with_perc_val(self,val_dict):
	
		#calculation of the sum of all the observation times, (8+1+1)
		som=0
		#for each value
		#print(val_dict)
		for i in val_dict:
			som+=val_dict[i]
		#print(som)
		
		di_1={}
		for j in val_dict:
			a=round(((val_dict[j]/som))*100,2)
			di_1[j]=[val_dict[j],a]
		#print(di_1)
		return di_1
		
		
		
#*****************************************************************************************************************************************************************************************
	#method creating a dict with the control of each phase
	#key=id phase, value=lst of two elements, [[...,[temps, crl value,type control (0 si RC, 1 sinon),nb decisions without RC],...]
	#ce dictionnaire peut etre vide si le ctrl n'est pas maj, cas possible  FA ctrl
	def fct_creat_dict_ctrl_per_phase_1(self,dict_db_key_id_event_type_val_record_obj):
		di_rep={}
		di_rep_1={}
		
		#si on a maj le controle 
		if Cl_Event.TYPE_EV["type_ev_new_intersection_control"] in  dict_db_key_id_event_type_val_record_obj:
			#key of the dictionary is the event type, value=[...,[record_database_obj_of_type_i_1,record_database_obj_of_type_i_2, ...  ]  ...]
			for i in dict_db_key_id_event_type_val_record_obj[Cl_Event.TYPE_EV["type_ev_new_intersection_control"]]:
		
				for j in i.get_current_inters_control_matrix():
					
					#if the phase is not in the dictionary
					if j not in di_rep:
						if i.get_type_control() !=0:
							som=1
						else:
							som=0
							
						di_rep[j]=[[i.get_ev_time(),i.get_current_inters_control_matrix()[j],i.get_type_control(),som]]
					else:
						if i.get_type_control() !=0:
							som=di_rep[j][len(di_rep[j])-1][3]+1
						else:
							som=di_rep[j][len(di_rep[j])-1][3]
							
						di_rep[j].append([i.get_ev_time(),i.get_current_inters_control_matrix()[j],i.get_type_control(),som])
						
					
		#print(di_rep)
		#import sys
		#sys.exit()
		return di_rep
#*****************************************************************************************************************************************************************************************
	#method creating a dict 
	#key=id phase, value=dict, cle=[t_start_actuated_period,t_end_acuated_period], value=1(indicating that during this time the phase was actuated)
	def fct_creat_dict_phase_actuat(self,dict_db_key_id_event_type_val_record_obj,v_sim_dur,v_t_period,v_t_unit,v_t_init):
	
		di_rep={}
		
		#di_rep_1= dict, key=id phase, value=dict, key=[t start control ,t _end control], value=1 (symbolic)
		di_rep_1={}
		
		#si on a maj le controle 
		if Cl_Event.TYPE_EV["type_ev_new_intersection_control"] in  dict_db_key_id_event_type_val_record_obj:
			#key of the dictionary is the event type, value=[...,[record_database_obj_of_type_i_1,record_database_obj_of_type_i_2, ...  ]  ...]
			for i in dict_db_key_id_event_type_val_record_obj[Cl_Event.TYPE_EV["type_ev_new_intersection_control"]]:
			
				
				#for each phase
				for j in i.get_current_inters_control_matrix():
				
					#if the phase is actuated
					if i.get_current_inters_control_matrix()[j]==1:
					
						#if the phase is  in the dictionary
						if j in di_rep_1:
							di={}
							di[i.get_t_start_current_inters_control(),i.get_t_end_current_intersection_control()]=1
							di_rep_1[j].update(di)
							
						#if the  phase is not in the diction
						else:
							 di_rep_1[j]={}
							 di={}
							 di[i.get_t_start_current_inters_control(),i.get_t_end_current_intersection_control()]=1
							 di_rep_1[j].update(di)
							
					#di_rep_1[j].sort()
							
		#li_t_interval=[..., [t start, t_end of ith period],...]
		li_t_interval=[]
		nb_interv=math.ceil(v_sim_dur/v_t_period)
		t_init=v_t_init
		for k in range(nb_interv):
			li_t_interval.append([t_init, t_init+v_t_period-v_t_unit])
			t_init=t_init+v_t_period
		
		#nb of time period intervals
		len_li_inter=len(li_t_interval)
		
		#di_rep_info_per_period=dict, key=id phase, value=dict, cle=[t_start_period, t_end_period], 
		#value=total actuation duration of the phase during the period
		di_rep_info_per_period={}
		
		
		#di_rep_1= dict, key=id phase, value=dict, key=[t start control ,t _end control], value=1 (symbolic)
		for m in di_rep_1:
			som=0
			di_rep_info_per_period[m]={}
			
			for n in  di_rep_1[m]:
				
				nb_inter=math.floor(n[1]/v_t_period)+1
				
				#print("nb_inter",nb_inter,"n[1]",n[1],"v_t_period",v_t_period,"len(li_t_interva)",len(li_t_interval))
				#print("li_t_interval[nb_inter-1]",li_t_interval[nb_inter-1])
				
				if nb_inter> len_li_inter:
					if nb_inter==len_li_inter+1:
						nb_inter=nb_inter-1
					else:
						print("PROBL IN CL STAT ANALYSIS, FCT fct_creat_dict_phase_actuat, NUMBER TIME PERIOD INTERVALS ",\
						len_li_inter,"nb_inter",nb_inter)
						import sys
						sys.exit()
				
				if (li_t_interval[nb_inter-1][0], li_t_interval[nb_inter-1][1]) in di_rep_info_per_period[m]:
				
				
					di_rep_info_per_period[m][li_t_interval[nb_inter-1][0], li_t_interval[nb_inter-1][1]]+=n[1]-n[0]
				
				else:
					di={}
					di[li_t_interval[nb_inter-1][0], li_t_interval[nb_inter-1][1]]=n[1]-n[0]
					
					di_rep_info_per_period[m].update(di)
					

		#print(di_rep)
		#import sys
		#sys.exit()
		return di_rep_info_per_period
#*****************************************************************************************************************************************************************************************
	
	#method retruning dict=key id phase, value=nb ctrl changes no RC inclded
	#di_key_id_phase_value_temps_and_ctrl_value_and_type_ctrl=dict,
	#key=id phase, value=[...,[temps, crl value,type control (0 si RC, 1 sinon],...]
	def fct_calcul_nb_ctrl_changes_no_rc_1(self, di_key_id_phase_value_temps_and_ctrl_value_and_type_ctrl):
	
		di_rep={}
		val_init_ctrl=-1
		
		#key=id phase, value=[...,[temps, crl value,type control (0 si RC, 1 sinon],...]
		for i in di_key_id_phase_value_temps_and_ctrl_value_and_type_ctrl:
			som=-1
			for j in di_key_id_phase_value_temps_and_ctrl_value_and_type_ctrl[i]:
				#si la valeur du ctrl est differente et si le ctrl n'est pas RC, on maj le som, on compte
				if val_init_ctrl!=j[1] and j[2] !=0:
					som+=1
					val_init_ctrl=j[1]
			di_rep[i]=som
		return di_rep
					
		
#*****************************************************************************************************************************************************************************************
	#method retruning dict=key id phase, value=nb ctrl changes no RC inclded
	#di_key_id_phase_value_temps_and_ctrl_value_and_type_ctrl=dict,
	#key=id phase, value=[...,[temps, crl value,type control (0 si RC, 1 sinon],...]
	def fct_calcul_nb_ctrl_changes_no_rc(self, di_key_id_phase_value_temps_and_ctrl_value_and_type_ctrl):
	
		di_rep={}
		
		
		#dict, key=id phase, value=[...., 1 or 0 according as of the phase was/not actuated,...]
		di_ctrl_sans_rc={}
		
		#key=id phase, value=[...,[temps, crl value,type control (0 si RC, 1 sinon],...]
		for i in di_key_id_phase_value_temps_and_ctrl_value_and_type_ctrl:
		
			di_ctrl_sans_rc[i]=[]
			
			for j in di_key_id_phase_value_temps_and_ctrl_value_and_type_ctrl[i]:
				#if the ctls is not rc, we add it to the dictionary
				if j[2] !=0:
					di_ctrl_sans_rc[i].append(j[1])
		
		#dict, key=id phase, value=[...., 1 or 0 according as of the phase was/not actuated,...]
		for m in di_ctrl_sans_rc:
			val_init_ctrl=-1
			som=-1
			for n in di_ctrl_sans_rc[m]:
				#si la valeur initiale est differente du controle j on maj la somme
				if val_init_ctrl != n:
					som+=1
					val_init_ctrl=n
			di_rep[m]=som
				
		return di_rep
					
		
#*****************************************************************************************************************************************************************************************
	#method returning the number  of times that each phase of an intersection  is beeen actuated
	#it returns  dict, key=id phase, value=[nb times actuat,[.., time ith actuation,..]]
	def fct_creat_dict_nb_times_actuat_phase(self,dict_key_id_phase_val_lis_time_and_ctrl_value):
		di_rep={}
		#dict_key_id_phase_val_lis_time_and_ctrl_value, key=id phase, value=[...,[temps, crl value,type control, nd ctrls],...]
		for i in dict_key_id_phase_val_lis_time_and_ctrl_value:
			nb_times_phase_act=0
			li_t_act=[]
			for j in dict_key_id_phase_val_lis_time_and_ctrl_value[i]:
				
				if j[1]==1:
					nb_times_phase_act+=1
					li_t_act.append(j[0])
					#if i[0]==1 and i[1]==2:
						#print("i",i,"j,",j,nb_times_phase_act)
					
			di_rep[i]=[nb_times_phase_act,li_t_act]
			#if i[0]==1 and i[1]==2:
				#print("di_rep[i]",di_rep[i])
		return di_rep

#*****************************************************************************************************************************************************************************************
	#fct creating a dictionary with the number of vehicles in each internal link,
	#key=id link, value=[...,[temps,nb veh link],...]
	def fct_creat_dict_current_nb_veh_in_link(self,v_netw, dict_db_key_id_event_type_val_record_obj):
		
		di_rep={}
		
		#for each evet_end_veh_departure
		for i in dict_db_key_id_event_type_val_record_obj[Cl_Event.TYPE_EV["type_ev_end_veh_departure_from_que"]]:
		
			
			#if the origin link of the veh (its location when the departure started) is not in the dictionary
			if i.get_veh_current_queue_location()[0] not in di_rep:
				di_rep[i.get_veh_current_queue_location()[0]]=[[i.get_ev_time(),i.get_nb_veh_in_dep_lk()]]
				
			#if the origin link of the veh (its location when the departure started) is in the dictionary
			else:
				di_rep[i.get_veh_current_queue_location()[0]].append([i.get_ev_time(),i.get_nb_veh_in_dep_lk()])
					
			#si le veh n'est pas arrive a un arc de sortie, on ecrit le nb des veh trouves a sa nouvelle position
			if i.get_veh_current_queue_location()[1] not in v_netw.get_di_exit_links_from_network():
			
				#if the current veh location is not in the dict
				if i.get_veh_current_queue_location()[1] not in di_rep:
					di_rep[i.get_veh_current_queue_location()[1]]=[[i.get_ev_time(),i.get_nb_veh_in_ar_lk()]]
			
				#if the current veh location is in the dict
				else:
					di_rep[i.get_veh_current_queue_location()[1]].append([i.get_ev_time(),i.get_nb_veh_in_ar_lk()])

				
		if Cl_Event.TYPE_EV["type_ev_end_veh_departure_from_que_nsi"] in dict_db_key_id_event_type_val_record_obj:
		
			#  CHECK THAT ev ty_ev_end_veh_hold_at_que_nsi should register THIS INFO ! 
			for j in dict_db_key_id_event_type_val_record_obj[Cl_Event.TYPE_EV["type_ev_end_veh_departure_from_que_nsi"]]:
			
				#if the origin link of the veh (its location when the departure started) is not in the dictionary
				if j.get_veh_current_queue_location()[0] not in di_rep:
					di_rep[j.get_veh_current_queue_location()[0]]=[[j.get_ev_time(),j.get_nb_veh_in_dep_lk()]]
				
				#if the origin link of the veh (its location when the departure started) is in the dictionary
				else:
					di_rep[j.get_veh_current_queue_location()[0]].append([j.get_ev_time(),j.get_nb_veh_in_dep_lk()])
					
				#si le veh n'est pas arrive a un arc de sortie, on  ecrit le nb des veh trouves a sa nouvelle position
				if j.get_veh_current_queue_location()[1] not in v_netw.get_di_exit_links_from_network():
			
					#if the current veh location is not in the dict
					if j.get_veh_current_queue_location()[1] not in di_rep:
						di_rep[j.get_veh_current_queue_location()[1]]=[[j.get_ev_time(),j.get_nb_veh_in_ar_lk()]]
			
					#if the current veh location is in the dict
					else:
						di_rep[j.get_veh_current_queue_location()[1]].append([j.get_ev_time(),j.get_nb_veh_in_ar_lk()])
		
		for i in dict_db_key_id_event_type_val_record_obj[Cl_Event.TYPE_EV["type_ev_veh_appearance"]]:	
		
			#si le veh n'est pas parti d'un arc d'entree, on ecrit le nombre des veh sur l'arc d'ou il est parti
			#if i.get_veh_current_queue_location()[0] not in v_netw.get_di_entry_links_to_network():
			#if the origin link of the veh (its location when the departure started) is not in the dictionary
			if i.get_veh_current_queue_location()[0] not in di_rep:
				di_rep[i.get_veh_current_queue_location()[0]]=[[i.get_ev_time(),i.get_nb_veh_in_ar_lk()]]
				
			#if the origin link of the veh (its location when the departure started) is in the dictionary
			else:
				di_rep[i.get_veh_current_queue_location()[0]].append([i.get_ev_time(),i.get_nb_veh_in_ar_lk()])
					
			
		if Cl_Event.TYPE_EV["type_ev_veh_appearance_nsi"] in dict_db_key_id_event_type_val_record_obj:
			for j in dict_db_key_id_event_type_val_record_obj[Cl_Event.TYPE_EV["type_ev_veh_appearance_nsi"]]:
				print("IN CLASSE STAT ANAL,  CHECK IF EV _ev_veh_appearance_nsI RECORD IS MADE CORRECTLY")
				import sys
				sys.exit()
				#if the origin link of the veh (its location when the departure started) is not in the dictionary
				if j.get_veh_current_queue_location()[0] not in di_rep:
					di_rep[j.get_veh_current_queue_location()[0]]=[[j.get_ev_time(),j.get_nb_veh_in_ar_lk()]]
				
				#if the origin link of the veh (its location when the departure started) is in the dictionary
				else:
					di_rep[j.get_veh_current_queue_location()[0]].append([j.get_ev_time(),j.get_nb_veh_in_ar_lk()])
		
		for i in di_rep:
			di_rep[i].sort()
				
		return di_rep
				
				
			
#***************************************************************************************************************************************************************************************** 

	#method creating a dictionary, key=the movement [l,m]
	#the value=dict, key=time, value= [   [nb of vehicles in the queue,ev type     ]  ]
	
	def fct_creat_dict_queue_lengths_during_sim_1(self,val_network,dict_db_file):
	
		
		
		#for each movement we associate of this event type we exctract the time, the queue id in the form of a movement [l,m], the number of vehicles in the queue at this time
		#dictionary, key = the movement id (l,m), value =[ time, number of vehicles in the queue]
		dict_id_queue={}
		
		#for each movement, dict_db_file=dict, key=movement,value=record object
		for i in dict_db_file:
		
			#if the movement is not a right turn we create the movement and calculate the queue length
			if val_network.get_di_all_links()[i[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()[i[0],i[1]].get_type_veh_queue()!=\
			Cl_Vehicle_Queue.TYPE_VEHICLE_QUEUE["right_turn"]:
			
				#we create the associated element of the dictionary to return 
				dict_id_queue[i]={}
				for j in dict_db_file[i]:
					#if the event we wish to add is of type veh arrival
					if j.get_ev_type()==Cl_Event.TYPE_EV["type_ev_veh_arrived_at_que"] or  \
					j.get_ev_type()==Cl_Event.TYPE_EV["type_ev_veh_appearance"] or\
					j.get_ev_type()==Cl_Event.TYPE_EV["type_ev_veh_arrived_at_que_nsi"] or \
					j.get_ev_type()==Cl_Event.TYPE_EV["type_ev_veh_appearance_ns"]:
						
						#if the time is not already in the dictionary, then we add
						if j.get_ev_time() not in dict_id_queue[i]:
							dict_id_queue[i][j.get_ev_time()]=[[ len(j.get_li_id_vehicles_in_queue()),j.get_ev_type() ]]
					
						#if the time is  already in the dictionary, if the existing event is of the same type then we use the new value of the que
						else:
							
							ind_elem=0
							for k in dict_id_queue[i][j.get_ev_time()]:
								#if another record is ound of the same event type and the same queue length then it won't be add
								if k[1]==j.get_ev_type() and k[0] < len(j.get_li_id_vehicles_in_queue()):
									
									
									k[0]=len(j.get_li_id_vehicles_in_queue())
									break
								elif k[1]==j.get_ev_type() and k[0] > len(j.get_li_id_vehicles_in_queue()):
									dict_id_queue[i][j.get_ev_time()].append([ len(j.get_li_id_vehicles_in_queue()),j.get_ev_type() ])
									break
									#ind_elem=1
							#if ind_elem==0:
								#dict_id_queue[i][j.get_ev_time()].append([ len(j.get_li_id_vehicles_in_queue()),j.get_ev_type() ])
								
					#if the event we wish to add is veh departure
					elif j.get_ev_type()==Cl_Event.TYPE_EV["type_ev_end_veh_departure_from_que"] or\
					j.get_ev_type()==Cl_Event.TYPE_EV["type_ev_end_veh_departure_from_que_nsi"]:
						#if the time is not already in the dictionary, then we add
						if j.get_ev_time() not in dict_id_queue[i]:
							dict_id_queue[i][j.get_ev_time()]=[[ len(j.get_li_id_vehicles_in_queue()),j.get_ev_type() ]]
						#if the event time is already in the dictionary, we add the event only if the value of the queue length is different
						else:
						
							if dict_id_queue[i][j.get_ev_time()][len (dict_id_queue[i][j.get_ev_time()])-1][0] != len(j.get_li_id_vehicles_in_queue()):
								
								dict_id_queue[i][j.get_ev_time()].append([ len(j.get_li_id_vehicles_in_queue()),j.get_ev_type() ])
							
							
					#if the event we wish to add is of any other type
					else:
						print("PROB, CL_STAT, FCT fct_creat_dict_queue_lengths_during_sim, EVENT TYPE TO ADD ",\
						j.get_ev_type())
						import sys
						sys.exit()
					
			
		
		return dict_id_queue

#*****************************************************************************************************************************************************************************************
	#method creating a dictionary, key=the movement [l,m]
	#the value=dict, key=time, value= [   [nb of vehicles in the queue,ev type,veh id     ]  ]
	
	def fct_creat_dict_queue_lengths_during_sim(self,val_network,dict_db_file):
	
		#print("dict_db_file",dict_db_file.keys())
		
		
		#for each movement we associate of this event type we exctract the time, the queue id in the form of a movement [l,m], the number of vehicles in the queue at this time
		#dictionary, key = the movement id (l,m), value =[ time, number of vehicles in the queue]
		dict_id_queue={}
		
		#for each movement, dict_db_file=dict, key=movement,value=record object
		for i in dict_db_file:
			#print("val_network.get_di_all_links()[i[0]]",val_network.get_di_all_links()[i[0]])
		
			#if the movement is not a right turn we create the movement and calculate the queue length
			if val_network.get_di_all_links()[i[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()[i[0],i[1]].get_type_veh_queue()!=\
			Cl_Vehicle_Queue.TYPE_VEHICLE_QUEUE["right_turn"]:
			
				#we create the associated element of the dictionary to return 
				dict_id_queue[i]={}
				for j in dict_db_file[i]:
					#if the event we wish to add is of type veh arrival
					if j.get_ev_type()==Cl_Event.TYPE_EV["type_ev_veh_arrived_at_que"] or  \
					j.get_ev_type()==Cl_Event.TYPE_EV["type_ev_veh_appearance"] or\
					j.get_ev_type()==Cl_Event.TYPE_EV["type_ev_veh_arrived_at_que_nsi"] or \
					j.get_ev_type()==Cl_Event.TYPE_EV["type_ev_veh_appearance_nsi"]:
						
						#if the time is not already in the dictionary, then we add
						if j.get_ev_time() not in dict_id_queue[i]:
							dict_id_queue[i][j.get_ev_time()]=[[ len(j.get_li_id_vehicles_in_queue()),j.get_ev_type(),j.get_vehicle_id() ]]
					
						#if the time is  already in the dictionary, if the existing event is of the same type then we use the new value of the que
						else:
							dict_id_queue[i][j.get_ev_time()].append([ len(j.get_li_id_vehicles_in_queue()),j.get_ev_type(),j.get_vehicle_id() ])
																	
					#if the event we wish to add is veh end departure
					elif j.get_ev_type()==Cl_Event.TYPE_EV["type_ev_end_veh_departure_from_que"] or \
					j.get_ev_type()==Cl_Event.TYPE_EV["type_ev_end_veh_departure_from_que_nsi"]:
						#if the time is not already in the dictionary, then we add
						if j.get_ev_time() not in dict_id_queue[i]:
							dict_id_queue[i][j.get_ev_time()]=[[ len(j.get_li_id_vehicles_in_queue()),j.get_ev_type(),j.get_vehicle_id() ]]
						#if the event time is already in the dictionary, we add the event only if the value of the queue length is different
						else:
						
							if dict_id_queue[i][j.get_ev_time()][len (dict_id_queue[i][j.get_ev_time()])-1][0] != len(j.get_li_id_vehicles_in_queue()):
								
								dict_id_queue[i][j.get_ev_time()].append([ len(j.get_li_id_vehicles_in_queue()),j.get_ev_type(),j.get_vehicle_id() ])
								
					#if the event we wish to add is end  veh hold at que
					elif j.get_ev_type()==Cl_Event.TYPE_EV["ty_ev_end_veh_hold_at_que"] or\
					j.get_ev_type()==Cl_Event.TYPE_EV["ty_ev_end_veh_hold_at_que_nsi"]:
						pass
							
					#if the event we wish to add is of any other type
					else:
						print("PROB, CL_STAT, FCT fct_creat_dict_queue_lengths_during_sim, EVENT TYPE TO ADD ",\
						j.get_ev_type())
						import sys
						sys.exit()
					
			
		
		return dict_id_queue

#*****************************************************************************************************************************************************************************************
	#method creating a dictionary, key = movement (l,m)
	#the value =  [   [time, nb of arrivals at the queue     ]  ]
	def fct_creat_dict_queue_veh_arrivals_ap_during_sim(self,val_network,dict_db_file):
	
		dict_id_queue={}
		#for each movement, dict_db_file= dict, key =movem, value=record obj
		for i in dict_db_file:
			if val_network.get_di_all_links()[i[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()[i[0],i[1]].get_type_veh_queue()!=\
			Cl_Vehicle_Queue.TYPE_VEHICLE_QUEUE["right_turn"]:
				#we create the associated element of the dictionary to return 
				dict_id_queue[i]={}
				for j in dict_db_file[i]:
					#if the event type is vehicle arrival then we add it
					if j.get_ev_type()==Cl_Event.TYPE_EV["type_ev_veh_arrived_at_que"] or \
					j.get_ev_type()==Cl_Event.TYPE_EV["type_ev_veh_appearance"] or\
					j.get_ev_type()==Cl_Event.TYPE_EV["type_ev_veh_arrived_at_que_nsi"] or\
					j.get_ev_type()==Cl_Event.TYPE_EV["type_ev_veh_appearance_nsi"]:
				
						#if the time is not already in the dictionary
						if j.get_ev_time() not in dict_id_queue[i]:
							dict_id_queue[i][j.get_ev_time()]=[[len(j.get_li_id_vehicles_in_queue()),j.get_ev_type()]]
						
						#if the time is already in the dictionary
						else:
							ind_elem=0
							#for each element at this time
							for k in dict_id_queue[i][j.get_ev_time()]:
								#print("HERE",j.get_ev_time(),k,len(j.get_li_id_vehicles_in_queue()),j.get_ev_type())
								#if the existing queue legnth is < and the event type is the same
								if k[0]<len(j.get_li_id_vehicles_in_queue()) and k[1]==j.get_ev_type():
							
									#we delete the elem
									dict_id_queue[i][j.get_ev_time()].remove(k)
									#we insert the new one
									dict_id_queue[i][j.get_ev_time()].append([len(j.get_li_id_vehicles_in_queue()),j.get_ev_type()])
								  
									ind_elem=1
							if ind_elem==0:
								dict_id_queue[i][j.get_ev_time()].append([len(j.get_li_id_vehicles_in_queue()),j.get_ev_type()])
							
				
		return dict_id_queue
		
#*****************************************************************************************************************************************************************************************
	#method returning a dictionary, key=id phase, value=[...,nb veh arrived at ith cycle,...]
	#ATTENTION BECAUSE OF THE INIT OF t_fin_cycle_init=val_cycle_duration, COMPUT IS CORRECT FOR NEW SIM !!!!
	def fct_creat_dict_veh_arrival_at_phase_per_cycle(self,val_network,val_dict_db_file,val_cycle_duration):
	
		di_rep={}
		
		di_key_id_phase_value_ev_veh_ar={}
		
		#dict, key=mov, value = [...,record obj,...]
		for i in val_dict_db_file:
			di_key_id_phase_value_ev_veh_ar[i]=[]
			for j in val_dict_db_file[i]:
				if j.get_ev_type()==Cl_Event.TYPE_EV["type_ev_veh_arrived_at_que"] or \
					j.get_ev_type()==Cl_Event.TYPE_EV["type_ev_veh_appearance"] or\
					j.get_ev_type()==Cl_Event.TYPE_EV["type_ev_veh_arrived_at_que_nsi"] or\
					j.get_ev_type()==Cl_Event.TYPE_EV["type_ev_veh_appearance_nsi"]:
					
						di_key_id_phase_value_ev_veh_ar[i].append(j)
		
		#dict, key=id phase, value= ev_veh_ar or ev_veh_ap
		for m in di_key_id_phase_value_ev_veh_ar:
			di_rep[m]=[]
			
			t_fin_cycle_init=val_cycle_duration
			nb_veh_ar_cycle_init=0
			
			nb_ar=len(di_key_id_phase_value_ev_veh_ar[m])
			
			for n in range(nb_ar):
				#calcul du t fin cycle correspondant
				t_fin_cycle_correspondant_t_even=\
				math.ceil(di_key_id_phase_value_ev_veh_ar[m][n].get_ev_time()/val_cycle_duration)*val_cycle_duration
				
				#si on se  met a un nouveau cycle, on enregistre le nb des arrivees et on commence nouvelle  enumerat
				if t_fin_cycle_correspondant_t_even >t_fin_cycle_init:
				
					di_rep[m].append(nb_veh_ar_cycle_init)
					#calcul du nb de cycles entre t_fin_cycle_init et t_fin_cycle_correspondant_t_even
					cycle_corres_au_t_fin_cycle_correspondant_t_even=math.ceil(t_fin_cycle_correspondant_t_even/val_cycle_duration)
					cycle_corresp_au_t_fin_cycle_init=math.ceil(t_fin_cycle_init/val_cycle_duration)
					nb_cycles_interm=cycle_corres_au_t_fin_cycle_correspondant_t_even-cycle_corresp_au_t_fin_cycle_init
					if nb_cycles_interm>1:
						#print(cycle_corres_au_t_fin_cycle_correspondant_t_even,cycle_corresp_au_t_fin_cycle_init)
						#import sys
						#sys.exit()
						nb_cycles_ajout=int(nb_cycles_interm-1)
						di_rep[m].extend(nb_cycles_ajout*[0])
					t_fin_cycle_init= t_fin_cycle_correspondant_t_even
					nb_veh_ar_cycle_init=1
				
				else:

					nb_veh_ar_cycle_init+=1
			#si on est au dernier even du cycle courant, comme il n'y a pas de cycle proch on doit mettre le nb d'arrivees dans dict
			if n==nb_ar-1:
				di_rep[m].append(nb_veh_ar_cycle_init)
				
					
		return di_rep
				
#*****************************************************************************************************************************************************************************************				
				
	#method returning a dictionary, key=id phase, value=[...,nb veh dep at ith cycle,...]
	def fct_creat_dict_veh_depart_from_phase_per_cycle(self,val_network,val_dict_db_file,val_cycle_duration):
	
		di_rep={}
		
		di_key_id_phase_value_ev_veh_dep={}
		
		#dict, key=mov, value = [...,record obj,...]
		for i in val_dict_db_file:
			di_key_id_phase_value_ev_veh_dep[i]=[]
			for j in val_dict_db_file[i]:
				if j.get_ev_type()==Cl_Event.TYPE_EV["type_ev_end_veh_departure_from_que"] or \
					j.get_ev_type()==Cl_Event.TYPE_EV["type_ev_end_veh_departure_from_que_nsi"]:
						di_key_id_phase_value_ev_veh_dep[i].append(j)
		
		#dict, key=id phase, value= ev_veh_ar or ev_veh_dep
		for m in di_key_id_phase_value_ev_veh_dep:
			di_rep[m]=[]
			t_fin_cycle_init=val_cycle_duration
			nb_veh_dep_cycle_init=0
			
			nb_dep=len(di_key_id_phase_value_ev_veh_dep[m])
			 
			if nb_dep==0:
				print("phase", m,"none departed")
			for n in range(nb_dep):
				#calcul du t fin cycle correspondant
				t_fin_cycle_correspondant_t_even=\
				math.ceil(di_key_id_phase_value_ev_veh_dep[m][n].get_ev_time()/val_cycle_duration)*val_cycle_duration
				#si on se  met a un nouveau cycle, on enregistre le nb des arrivees et on commence nouvelle  enumerat
				if t_fin_cycle_correspondant_t_even >t_fin_cycle_init:
					di_rep[m].append(nb_veh_dep_cycle_init)
					#calcul du nb de cycles entre t_fin_cycle_init et t_fin_cycle_correspondant_t_even
					cycle_corres_au_t_fin_cycle_correspondant_t_even=math.ceil(t_fin_cycle_correspondant_t_even/val_cycle_duration)
					cycle_corresp_au_t_fin_cycle_init=math.ceil(t_fin_cycle_init/val_cycle_duration)
					nb_cycles_interm=cycle_corres_au_t_fin_cycle_correspondant_t_even-cycle_corresp_au_t_fin_cycle_init
					if nb_cycles_interm>1:
						#print(cycle_corres_au_t_fin_cycle_correspondant_t_even,cycle_corresp_au_t_fin_cycle_init)
						nb_cycles_ajout=int(nb_cycles_interm-1)
						di_rep[m].extend(nb_cycles_ajout*[0])
					t_fin_cycle_init= t_fin_cycle_correspondant_t_even
					nb_veh_dep_cycle_init=1
				
				else:
					nb_veh_dep_cycle_init+=1
			if n==nb_dep-1:
				di_rep[m].append(nb_veh_dep_cycle_init)
				
		return di_rep
		
#*****************************************************************************************************************************************************************************************				
	#method returning a dict, key=id phase, value=[....,departs-arrivals ith cycle,...]
	def fct_creat_dict_differ_depart_minus_ar(self,val_di_key_id_phase_val_ar_ap_per_cycle,val_di_key_id_phase_val_dep_per_cycle):
		
		di_rep={}
		nb_phases_with_ar=len(val_di_key_id_phase_val_ar_ap_per_cycle)
		nb_phases_with_dep=len(val_di_key_id_phase_val_dep_per_cycle)
		
		
		
		
		#si le nb des phases avec ar == nb phases avec departs
		if nb_phases_with_ar==nb_phases_with_dep:
			#val_di_key_id_phase_val_ar_ap_per_cycle=dict, key=id phase, value=[...,nb veh arrival or appear at ith cycle,...]
			for i in val_di_key_id_phase_val_ar_ap_per_cycle:
				di_rep[i]=[]
				nb_ar_phase_i=len(val_di_key_id_phase_val_ar_ap_per_cycle[i])
				nb_dep_phase_i=len(val_di_key_id_phase_val_dep_per_cycle[i])
			
				#si les arrivees en phase i = departs de phase i
				if nb_ar_phase_i==nb_dep_phase_i:
					for j in range(nb_ar_phase_i):
						dif=val_di_key_id_phase_val_dep_per_cycle[i][j] - val_di_key_id_phase_val_ar_ap_per_cycle[i][j]
						di_rep[i].append(dif)
			
				#si les arrivees en  i > departs de phase i
				elif nb_ar_phase_i>nb_dep_phase_i:
					for j in range(nb_dep_phase_i):
						dif=val_di_key_id_phase_val_dep_per_cycle[i][j] - val_di_key_id_phase_val_ar_ap_per_cycle[i][j]
						di_rep[i].append(dif)
					for m in val_di_key_id_phase_val_ar_ap_per_cycle[i][nb_dep_phase_i :]:
						dif=0 - m
						di_rep[i].append(dif)
					
			
				#si les arrivees au phase i < departs de phase i
				elif nb_ar_phase_i < nb_dep_phase_i:
					for j in range(nb_ar_phase_i):
						dif=val_di_key_id_phase_val_dep_per_cycle[i][j] - val_di_key_id_phase_val_ar_ap_per_cycle[i][j]
						di_rep[i].append(dif)
					for m in val_di_key_id_phase_val_dep_per_cycle[i][nb_ar_phase_i :]:
						dif=m
						di_rep[i].append(dif)
	
		#si le nb des phases avec ar  different du nb phases avec departs
		else:
			print("PROBL IN CL STAT ANAL, FCT fct_creat_dict_differ_depart_minus_ar nb_phases_with_ar,nb_phases_with_dep",nb_phases_with_ar,nb_phases_with_dep)
			import sys
			sys.exit()
		
		return di_rep
				
		

#*****************************************************************************************************************************************************************************************
	#method creating a dictionary, key = movement (l,m)
	#the value = dict, key= time, value= [   [nb of dep veh, ev type  ]  ]
	def fct_creat_dict_queue_veh_depart_during_sim1(self,val_network,dict_db_file):
	
		dict_id_queue={}
		#dict_db_file= dict, key =movem, value=record obj
		for i in dict_db_file:
			#if the movement is not a right turn
			if val_network.get_di_all_links()[i[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()[i[0],i[1]].get_type_veh_queue()!=\
			Cl_Vehicle_Queue.TYPE_VEHICLE_QUEUE["right_turn"]:
		
				#we create the associated element of the dictionary to return 
				dict_id_queue[i]={}
				for j in dict_db_file[i]:
					#if the event type is vehicle departure or appearance i, which the veh leaves im, then we add it
					if j.get_ev_type()==Cl_Event.TYPE_EV["type_ev_end_veh_departure_from_que"]  or\
					 j.get_ev_type()==Cl_Event.TYPE_EV["type_ev_end_veh_departure_from_que_nsi"] or \
					(j.get_ev_type()==Cl_Event.TYPE_EV["type_ev_veh_appearance"] or \
					j.get_ev_type()==Cl_Event.TYPE_EV["type_ev_veh_appearance_nsi"] and \
					len(j.get_li_id_vehicles_in_queue())==0):
					
						#if the time is not already in the dictionary
						if j.get_ev_time() not in dict_id_queue[i]:
							dict_id_queue[i][j.get_ev_time()]=[\
							[j.get_current_achieved_queue_service_rate_including_current_vehicle(),j.get_ev_type()]]
					
						#if the time is already in the dictionary
						else:
							#if the event type is veh appearance 
							#then we increase by one the number of departing vehicles
							if j.get_ev_type()==Cl_Event.TYPE_EV["type_ev_veh_appearance"] or \
							i.get_ev_type()==Cl_Event.TYPE_EV["type_ev_veh_appearance_nsi"]:
								ind_elem=0
								for k in dict_id_queue[i][j.get_ev_time()]:
									#if the type of the existing element is veh appearance
									if k[1]==j.get_ev_type():
										k[0]=j.get_current_achieved_queue_service_rate_including_current_vehicle()
										ind_elem=1
								if ind_elem==0:
									dict_id_queue[i][j.get_ev_time()].\
									append([j.get_current_achieved_queue_service_rate_including_current_vehicle(),j.get_ev_type()])
									
				
	
		return dict_id_queue

#*****************************************************************************************************************************************************************************************
	#method creating a dictionary, key = movement (l,m)
	#the value = dict, key= time, value= [   [nb of dep veh, ev type  ]  ]
	def fct_creat_dict_queue_veh_depart_during_sim(self,val_network,dict_db_file):
	
		dict_id_queue={}
		#dict_db_file= dict, key =movem, value=record obj
		for i in dict_db_file:
			#if the movement is not a right turn
			if val_network.get_di_all_links()[i[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()[i[0],i[1]].get_type_veh_queue()!=\
			Cl_Vehicle_Queue.TYPE_VEHICLE_QUEUE["right_turn"]:
				
				#we create the associated element of the dictionary to return 
				dict_id_queue[i]={}
				for j in dict_db_file[i]:
					
					#if the event type is vehicle departure or appearance i, which the veh leaves im, then we add it
					if j.get_ev_type()==Cl_Event.TYPE_EV["type_ev_end_veh_departure_from_que"] or\
					j.get_ev_type()==Cl_Event.TYPE_EV["type_ev_end_veh_departure_from_que_nsi"]:
					
						#if the time is not already in the dictionary
						if j.get_ev_time() not in dict_id_queue[i]:
							dict_id_queue[i][j.get_ev_time()]=[\
							[j.get_nb_depart_veh_within_dep_ev(),j.get_ev_type()]]
							
					#if the event is veh appearance ant the vehicle leaves im the queue
					if (j.get_ev_type()==Cl_Event.TYPE_EV["type_ev_veh_appearance"] or\
					j.get_ev_type()==Cl_Event.TYPE_EV["type_ev_veh_appearance_nsi"] and \
					len(j.get_li_id_vehicles_in_queue())==0):
					
						#if the time is not already in the dictionary
						if j.get_ev_time() not in dict_id_queue[i]:
							dict_id_queue[i][j.get_ev_time()]=[\
							[1,j.get_ev_type()]]
					
						#if the time is already in the dictionary
						else:
							#if the event type is veh appearance 
							#then we increase by one the number of departing vehicles
							if j.get_ev_type()==Cl_Event.TYPE_EV["type_ev_veh_appearance"] or\
							j.get_ev_type()==Cl_Event.TYPE_EV["type_ev_veh_appearance_nsi"]:
								ind_elem=0
								for k in dict_id_queue[i][j.get_ev_time()]:
									#if the type of the existing element is veh appearance
									if k[1]==j.get_ev_type():
										k[0]=j.get_current_achieved_queue_service_rate_including_current_vehicle()
										ind_elem=1
								if ind_elem==0:
									dict_id_queue[i][j.get_ev_time()].\
									append([j.get_current_achieved_queue_service_rate_including_current_vehicle(),j.get_ev_type()])
									
				
	
		return dict_id_queue

#*****************************************************************************************************************************************************************************************
	#method creating a dictionary, key = movement (l,m)
	#the value = dict, key= time, value= [   [length veh queue after veh dep, ev type  ]  ]
	def fct_creat_dict_queue_evol_after_veh_depart_during_sim(self,val_network,dict_db_file):
		dict_id_queue={}
		#dict_db_file= dict, key =movem, value=record obj
		for i in dict_db_file:
			#if the movement is not a right turn
			if val_network.get_di_all_links()[i[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()[i[0],i[1]].get_type_veh_queue()!=\
			Cl_Vehicle_Queue.TYPE_VEHICLE_QUEUE["right_turn"]:
				#we create the associated element of the dictionary to return 
				dict_id_queue[i]={}
				for j in dict_db_file[i]:
					#if the event type is vehicle departure or appearance i, which the veh leaves im, then we add it
					if j.get_ev_type()==Cl_Event.TYPE_EV["type_ev_end_veh_departure_from_que"]  or\
					j.get_ev_type()==Cl_Event.TYPE_EV["type_ev_end_veh_departure_from_que"] or\
					(j.get_ev_type()==Cl_Event.TYPE_EV["type_ev_veh_appearance"] or\
					j.get_ev_type()==Cl_Event.TYPE_EV["type_ev_veh_appearance_nsi"] and \
					len(j.get_li_id_vehicles_in_queue())==0):
					
						#if the time is not already in the dictionary
						if j.get_ev_time() not in dict_id_queue[i]:
							dict_id_queue[i][j.get_ev_time()]=[\
							[len(j.get_li_id_vehicles_in_queue()),j.get_ev_type()]]
					
						#if the time is already in the dictionary
						else:
							#if the event type is veh appearance 
							#then we increase by one the number of departing vehicles
							if j.get_ev_type()==Cl_Event.TYPE_EV["type_ev_veh_appearance"] or\
							j.get_ev_type()==Cl_Event.TYPE_EV["type_ev_veh_appearance_nsi"]:
								ind_elem=0
								for k in dict_id_queue[i][j.get_ev_time()]:
									#if the type of the existing element is veh appearance
									if k[1]==j.get_ev_type():
										k[0]=len(j.get_li_id_vehicles_in_queue())
										ind_elem=1
								if ind_elem==0:
									dict_id_queue[i][j.get_ev_time()].\
									append([len(j.get_li_id_vehicles_in_queue()),j.get_ev_type()])
									
				
	
		return dict_id_queue

#*****************************************************************************************************************************************************************************************

	#function creating a dictionary with exit link information, key=[id of entry link,id of exit link], value= [,...[t veh_ap,t_veh_exit],...]
	#di_db_file=dict, key= event type, value =[...,record obj,....]
	def fct_creat_dict_exit_link_info1(self,val_network):
	
	
		treat_sim_obj=Cl_Treatment_Sim_Res.Treatment_Sim_Res(val_db_file_sim_res_to_treat=self._db_file)
		
		#dict key= event type, value =record obj
		dict_db_file=treat_sim_obj.fct_creation_dictionary_from_the_db_file()
		
		di={}
		
		#from al the arrival events, we choose those for which the time_veh_exit_from_network, is >0
		#for each arrival object
		for i in dict_db_file[Cl_Event.TYPE_EV["type_ev_veh_arrived_at_que"]]:
		
			#if the exit time is >0
			if i.get_time_veh_exit_from_network()>0:
			
				#if the movement is not a right turn on the  node at which the vehicle entered, this is
				#(veh entry link=entry link of the node,
				#veh exit _link= exit link of the same node and (veh entry link,veh exit _link) right turn 
				if (i.get_id_veh_entry_link(),i.get_id_current_link_veh_location()) not in \
				val_network.get_di_all_links()[i.get_id_veh_entry_link()].get_set_veh_queue().get_di_obj_veh_queue_at_link() or\
				(i.get_id_veh_entry_link(),i.get_id_current_link_veh_location())  in \
				val_network.get_di_all_links()[i.get_id_veh_entry_link()].get_set_veh_queue().get_di_obj_veh_queue_at_link() and\
				val_network.get_di_all_links()[i.get_id_veh_entry_link()].get_set_veh_queue().\
				get_di_obj_veh_queue_at_link()[i.get_id_veh_entry_link(),i.get_id_current_link_veh_location()].get_type_veh_queue()!=\
				Cl_Vehicle_Queue.TYPE_VEHICLE_QUEUE["right_turn"]:
				
				
					#if the movement (entry link, exit link) is not in the dict
					if (i.get_id_veh_entry_link(),i.get_id_current_link_veh_location()) not in di:
				 
						di[ i.get_id_veh_entry_link(),i.get_id_current_link_veh_location()]=\
							[[ i.get_time_veh_appearance_in_network(),i.get_time_veh_exit_from_network()]]

				
					#if the movement (entry link, exit link) is  in the dict
					else:
						di[i.get_id_veh_entry_link(),i.get_id_current_link_veh_location()].append(\
						[ i.get_time_veh_appearance_in_network(),i.get_time_veh_exit_from_network()])
		
		return di
#***************************************************************************************************************************************************************************************** 
	#function creating a dictionary with exit link information, key=[id of entry link,id of exit link], value= [,...[t veh_ap,t_veh_exit],...]
	#di_db_file=dict, key= event type, value =[...,record obj,....]		A VOIR !!!!
	def fct_creat_dict_exit_link_info_1(self):
	
		treat_sim_obj=Cl_Treatment_Sim_Res.Treatment_Sim_Res(val_db_file_sim_res_to_treat=self._db_file)
		
		#dict key= event type, value =record obj
		dict_db_file=treat_sim_obj.fct_creation_dictionary_from_the_db_file()
		
		di={}
		
		#from al the arrival events, we choose those for which the time_veh_exit_from_network, is >0
		#for each arrival at a signalised intersection object
		for i in dict_db_file[Cl_Event.TYPE_EV["type_ev_veh_arrived_at_que"]]:
		
			#if the exit time is >0
			if i.get_time_veh_exit_from_network()>0:
			
				#if the movement (entry link, exit link) is not in the dict
				if (i.get_id_veh_entry_link(),i.get_id_current_link_veh_location()) not in di:
				 
					di[ i.get_id_veh_entry_link(),i.get_id_current_link_veh_location()]=\
						[[ i.get_time_veh_appearance_in_network(),i.get_time_veh_exit_from_network()]]

				
				#if the movement (entry link, exit link) is  in the dict
				else:
					di[i.get_id_veh_entry_link(),i.get_id_current_link_veh_location()].append(\
					[ i.get_time_veh_appearance_in_network(),i.get_time_veh_exit_from_network()])
					
		#for each arrival at a non-signalised intersection object			
		for j in dict_db_file[Cl_Event.TYPE_EV["type_ev_veh_arrived_at_que_nsi"]]:
		
			#if the exit time is >0
			if j.get_time_veh_exit_from_network()>0:
			
				#if the movement (entry link, exit link) is not in the dict
				if (j.get_id_veh_entry_link(),j.get_id_current_link_veh_location()) not in di:
				 
					di[ j.get_id_veh_entry_link(),j.get_id_current_link_veh_location()]=\
						[[ j.get_time_veh_appearance_in_network(),j.get_time_veh_exit_from_network()]]

				
				#if the movement (entry link, exit link) is  in the dict
				else:
					di[j.get_id_veh_entry_link(),j.get_id_current_link_veh_location()].append(\
					[ j.get_time_veh_appearance_in_network(),j.get_time_veh_exit_from_network()])
		
		return di
#***************************************************************************************************************************************************************************************** 
	#function creating a dictionary with exit link information, key=[id of entry link,id of exit link], value= [,...[t veh_ap,t_veh_exit],...]
	#di_db_file=dict, key= event type, value =[...,record obj,....]		A VOIR !!!!
	def fct_creat_dict_exit_link_info(self):
	
		treat_sim_obj=Cl_Treatment_Sim_Res.Treatment_Sim_Res(val_db_file_sim_res_to_treat=self._db_file)
		
		#dict key= event type, value =record obj
		dict_db_file=treat_sim_obj.fct_creation_dictionary_from_the_db_file()
		
		di={}
		
		#from al the arrival events, we choose those for which the time_veh_exit_from_network, is >0
		#for each arrival at a signalised intersection object
		for i in dict_db_file[Cl_Event.TYPE_EV["type_ev_end_veh_departure_from_que"]]:
		
			#if the exit time is >0
			if i.get_time_veh_exit_from_network()>0:
			
				#if the movement (entry link, exit link) is not in the dict
				if (i.get_id_veh_entry_link(),i.get_id_current_link_veh_location()) not in di:
				 
					di[ i.get_id_veh_entry_link(),i.get_id_current_link_veh_location()]=\
						[[ i.get_time_veh_appearance_in_network(),i.get_time_veh_exit_from_network()]]

				
				#if the movement (entry link, exit link) is  in the dict
				else:
					di[i.get_id_veh_entry_link(),i.get_id_current_link_veh_location()].append(\
					[ i.get_time_veh_appearance_in_network(),i.get_time_veh_exit_from_network()])
		
		if Cl_Event.TYPE_EV["type_ev_end_veh_departure_from_que_nsi"] in dict_db_file:
			#for each arrival at a non-signalised intersection object			
			for j in dict_db_file[Cl_Event.TYPE_EV["type_ev_end_veh_departure_from_que_nsi"]]:
		
				#if the exit time is >0
				if j.get_time_veh_exit_from_network()>0:
			
					#if the movement (entry link, exit link) is not in the dict
					if (j.get_id_veh_entry_link(),j.get_id_current_link_veh_location()) not in di:
				 
						di[ j.get_id_veh_entry_link(),j.get_id_current_link_veh_location()]=\
							[[ j.get_time_veh_appearance_in_network(),j.get_time_veh_exit_from_network()]]

				
					#if the movement (entry link, exit link) is  in the dict
					else:
						di[j.get_id_veh_entry_link(),j.get_id_current_link_veh_location()].append(\
						[ j.get_time_veh_appearance_in_network(),j.get_time_veh_exit_from_network()])
		
		else:
			print("ATTENTION,  AUCUN EVEN end_veh_departure_from_que_ns TROUVE, IN CL_STAT_ANALYSIS,  fct_creat_dict_exit_link_info")
			
				
		
		return di
#***************************************************************************************************************************************************************************************** 
	
	#function creating a dictionary, key=[id of entry link,id of exit link], value=[mean travel time,nb_veh_exit]
	def fct_creat_dict_mean_travel_time_entry_exit_link(self,di_info_entry_exit_lk,val_round_prec=2):
	
		#we create a dict, key=[id of entry link,id of exit link], value= [,...[t veh_ap,t_veh_exit],...]
		#di_info_entry_exit_lk=self.fct_creat_dict_exit_link_info()
		#print(di_info_entry_exit_lk.keys())
		#print()
		#for k in di_info_entry_exit_lk:
			#print("k=",k,di_info_entry_exit_lk[k])
			#print()
		
		di={}
		#for each (entry, exit lin,k)
		for i in di_info_entry_exit_lk:
			som=0
			for j in di_info_entry_exit_lk[i]:
				som+=j[1]-j[0]
				#print(i,"j[0]",j[0],"j[1]",j[1],"som",som)
				if som<0:
					print("PROBLEM ",j[0],j[1],j[1]-j[0])
					import sys
					sys.exit()
			#print("som=",som)
			a=len(di_info_entry_exit_lk[i])
			mean=round(som/a,val_round_prec)
			#mean=round(som/a,2)
			#print(mean)
			#print("mean=",mean)
			di[i]=[mean,a]
		#print()
		#print("di=",di)
		return di

#***************************************************************************************************************************************************************************************** 
	#function creating a dictionary, key=[id of entry link,id of exit link], value=[mean travel time,nb_veh_exit]
	def fct_creat_dict_mean_travel_time_entry_exit_link_per_per_1(self,v_sim_dur,v_t_period,v_t_unit,val_round_prec=2):
		
		#we create a dict, key=[id of entry link,id of exit link], value= [,...[t veh_ap,t_veh_exit],...]
		di_info_entry_exit_lk=self.fct_creat_dict_exit_link_info()
		
			
		#dict, key=[id of entry link,id of exit link], value= [..,t veh_ap,,...]
		li_t_interval=[]
		nb_interv=math.ceil(v_sim_dur/v_t_period)
		t_init=0
		for i in range(nb_interv):
			li_t_interval.append([t_init, t_init+v_t_period-v_t_unit])
			t_init=t_init+v_t_period
		#import sys
		#sys.exit()
		
		#dict, key=(id entry, id exit lk), value=[ [mean, a, for the 1st period],[mean, a, for the 2nd period],....]
		di_rep={}
		
		
		#for each (entry, exit link)
		for i in di_info_entry_exit_lk:
			#we sor thte list regarding the t_appear
			di_info_entry_exit_lk[i].sort()
			
			di_rep[i]=len(li_t_interval)*[]
			som=0
			nb_elem=0
			ind=0
			
			m=len(di_info_entry_exit_lk[i])
			#if i[0]==11 and i[1]==16:
				#print("m=",m)
			#print(i,m,di_info_entry_exit_lk[i])
			
			
			for j in range(m):
				
				if di_info_entry_exit_lk[i][j][0]<=li_t_interval[ind][1]:
				
					som+=di_info_entry_exit_lk[i][j][1]-di_info_entry_exit_lk[i][j][0]
					nb_elem+=1
					
					if som<0:
						print("PROBLEM ",di_info_entry_exit_lk[i][j][0],di_info_entry_exit_lk[i][j][1],\
						di_info_entry_exit_lk[i][j][1]-di_info_entry_exit_lk[i][j][0])
						import sys
						sys.exit()
					
					if j==m-1:
						mean=round(som/nb_elem,val_round_prec)
						di_rep[i].append([mean,nb_elem])
						
						index_interval_t_ap=math.ceil(di_info_entry_exit_lk[i][j][0]/v_t_period)-1
						print("index_interval_t_ap",index_interval_t_ap,di_info_entry_exit_lk[i][j][0],v_t_period,di_info_entry_exit_lk[i][j][0]/v_t_period)
						
						li=(nb_interv-index_interval_t_ap-1)*[[mean,nb_elem]]
						
						print("li",li)
						di_rep[i].extend(li)
						print(di_rep[i])
						import sys
						sys.exit()
						#if  i[0]==13 and i[1]==22:
							#print("APRES di_rep[i]",di_rep[i])
				#if the t_appear > to the t_lim of the 1st interval
				else:
					#print("di_rep[i] avant",di_rep[i],"i=",i)
					if nb_elem>0:
						mean=round(som/nb_elem,val_round_prec)
					else:
						mean=0

					di_rep[i].append([mean,nb_elem])
					#we calcultate the index of the itnerval at which the t_ap belongs
					index_interval_t_ap=math.ceil(di_info_entry_exit_lk[i][j][0]/v_t_period)-1
					#we add as many values [mean,nb_elem] as the index_interval_t_ap -1
					ind_creat_list_supplem=index_interval_t_ap-ind-1
		
					if ind_creat_list_supplem>0:
						li=ind_creat_list_supplem*[[mean,nb_elem]]
						di_rep[i].extend(li)
						
		
					ind=index_interval_t_ap
					som=di_info_entry_exit_lk[i][j][1]-di_info_entry_exit_lk[i][j][0]
					nb_elem=1
					
					if j==m-1:
						mean=round(som/nb_elem,val_round_prec)
						#if  i[0]==13 and i[1]==22:
							#print("AVANT di_rep[i]",di_rep[i])
						di_rep[i].append([mean,nb_elem])
						index_interval_t_ap=math.ceil(di_info_entry_exit_lk[i][j][0]/v_t_period)-1
						#if i[0]==11 and i[1]==16:
							#print("nb_interv",nb_interv,"index_interval_t_ap",index_interval_t_ap)
							#import sys
							#sys.exit()
						li=(nb_interv-index_interval_t_ap-1)*[[mean,nb_elem]]
						#if  i[0]==13 and i[1]==22:
							#print("AVANT di_rep[i]",di_rep[i])
						di_rep[i].extend(li)

						#if  i[0]==13 and i[1]==22:
							#print("AVANT di_rep[i]",di_rep[i])
						
		#print(di_rep[13,22])
		#print()	
		#print(di_rep)
		import sys
		sys.exit()		
		return di_rep

#***************************************************************************************************************************************************************************************** 
	#function creating a dictionary, key=[id of entry link,id of exit link], value=dict, key=(t_start period, t_end period),
	#value= [mean travel time, nb vehicles]
	def fct_creat_dict_mean_travel_time_entry_exit_link_per_per(self,v_sim_dur,v_t_period,v_t_unit,v_t_init,val_round_prec,di_info_entry_exit_lk):
		
		#di_info_entry_exit_lk= dict, key=[id of entry link,id of exit link], value= [,...[t veh_ap,t_veh_exit],...]
		#di_info_entry_exit_lk=self.fct_creat_dict_exit_link_info()
		
		#li_t_interval=[..., [t start i period, t_end of ith period],...]
		li_t_interval=[]
		nb_interv=math.ceil(v_sim_dur/v_t_period)
		t_init=v_t_init
		for i in range(nb_interv):
			li_t_interval.append([t_init, t_init+v_t_period-v_t_unit])
			t_init=t_init+v_t_period
		#print(li_t_interval)
		#import sys
		#sys.exit()
		
		
		
	
		#dict, key=(id entry, id exit lk), value=dict, key=(t_start_period, t_end_period), value=[som of (t_exit-t_entry corresponding period), nb vehicles exited during current period]
		di_rep_info_per_period={}
		
		for i in di_info_entry_exit_lk:
			
			#dict, key=(t_start_period, t_end_period), value=[som of (t_exit-t_entry corresponding period), nb vehicles exited during current period]
			di_rep_info_per_period[i]={}
			
			#di_info_entry_exit_lk= dict, key=[id of entry link,id of exit link], value= [,...[t veh_ap,t_veh_exit],...]
			di_info_entry_exit_lk[i].sort()
			
			ind=0
			som_t_total_veh_travel=0
			nb_veh_exited_period=0
			
			#di_info_entry_exit_lk= dict, key=[id of entry link,id of exit link], value= [,...[t veh_ap,t_veh_exit],...]
			for j in di_info_entry_exit_lk[i]:
			
				#numero interval to which belong the t_exit
				num_inter=math.floor(j[1]/v_t_period)+1
				
				if (li_t_interval[num_inter-1][0], li_t_interval[num_inter-1][1]) in di_rep_info_per_period[i]:
				
					new_dur=j[1]-j[0]
					
					#we update the som of (t_exit- t_ap)
					#print("ici avant",di_rep_info_per_period[i][li_t_interval[num_inter-1][0],li_t_interval[num_inter-1][1]])
					
					di_rep_info_per_period[i][li_t_interval[num_inter-1][0], li_t_interval[num_inter-1][1]][0]+=new_dur
					
					#we update the corresponding number of vehicles
					di_rep_info_per_period[i][li_t_interval[num_inter-1][0], li_t_interval[num_inter-1][1]][1]+=1
					
					#print("ici apres",di_rep_info_per_period[i][li_t_interval[num_inter-1][0],li_t_interval[num_inter-1][1]])
				
				else:
					new_dur=j[1]-j[0]
					
					nb_veh=1
					di={}
					
					#we update the som of (t_exit- t_ap)
					di[li_t_interval[num_inter-1][0], li_t_interval[num_inter-1][1]]=[new_dur,1]
					
					
					di_rep_info_per_period[i].update(di)
				for k in 	li_t_interval:
					if (k[0],k[1]) not in di_rep_info_per_period[i]:
						di_rep_info_per_period[i][k[0],k[1]]=[0,0]
		
		#print(di_info_entry_exit_lk[2370, 2351])
		#print()		
		#print(di_rep_info_per_period[2370, 2351])	
		#import sys
		#sys.exit()
		
		#di_rep_mean_travel_time=dict, key=(id entry, id exit link), value=dict, key=(t_start_time period, t_end_time period)
		#value=[som (t_exit-t_entry), nb veh)]
		di_rep_mean_travel_time={}
		
		for m in di_rep_info_per_period:
			di_rep_mean_travel_time[m]={}
			for n in di_rep_info_per_period[m]:
				di={}
				if di_rep_info_per_period[m][n][0]!=0:
					#if m[0]==2370  and m[1]==2351:
						#print("n",n)
						#print(di_rep_info_per_period[m][n][1],di_rep_info_per_period[m][n][0],\
						#round(di_rep_info_per_period[m][n][0]/di_rep_info_per_period[m][n][1],2))
					di[n]=[round(di_rep_info_per_period[m][n][0]/di_rep_info_per_period[m][n][1],2),di_rep_info_per_period[m][n][1]]
				else:
					di[n]=[0,0]
				di_rep_mean_travel_time[m].update(di)
		#print()
		#print(di_rep_mean_travel_time[2370, 2351])	
		#import sys
		#sys.exit()
						
		#print(di_rep[13,22])
		#print()	
		#print(di_rep)
		#import sys
		#sys.exit()		
		return di_rep_mean_travel_time

#***************************************************************************************************************************************************************************************** 
	#method calculating the max value inclded in each time interval, when we want to divide the sim duration in periods
	def fct_calcul_max_value_included_in_each_time_interval(self,v_total_sim_time,v_period,v_t_unit):
	
		lis_t=[]
		a=v_total_sim_time//v_period
		reste=v_total_sim_time%v_period
		for i in range(a):
			s=(i+1)*v_period-v_t_unit
			lis_t.append(s)
		if reste!=0:
			#s=li_t[len(li_t)-1]
			lis_t.append(v_total_sim_time)
		if lis_t[len(lis_t)-1]>v_total_sim_time:
			print("PROBLEME IN CL_STAT_VERIF,v_total_sim_time ",v_total_sim_time)
			import sys
			sys.exit()
		return lis_t

#***************************************************************************************************************************************************************************************** 
	#method calculating the max value inclded in each time interval, when we want to divide the sim duration in periods
	def fct_calcul_min_value_included_in_each_time_interval(self,v_total_sim_time,v_period,v_init_interval):
	
		lis_t=[]
		a=v_total_sim_time//v_period
		reste=v_total_sim_time%v_period
		s=v_init_interval
		for i in range(a):
			lis_t.append(s)
			s=(i+1)*v_period
		if reste!=0:
			#s=li_t[len(li_t)-1]
			lis_t.append(v_total_sim_time)
		if lis_t[len(lis_t)-1]>v_total_sim_time:
			print("PROBLEME IN CL_STAT_VERIF,v_total_sim_time ",v_total_sim_time)
			import sys
			sys.exit()
		#print(lis_t)
		#import sys
		#sys.exit()
		return lis_t

#***************************************************************************************************************************************************************************************** 
	#method calculating and writing files witht he average travel time per period  for each entry-exit link 
	def fct_calcul_and_write_travel_time_per_time_period_entry_exit_lk(self,va_sim_dur,va_t_period,va_t_unit,va_round_prec,va_lis_phrases,\
	va_t_init,val_di_info_entry_exit_lk):
		
		#dict, key=(id entry link, id exit link), value=dict, key=(t_start period, t_end period),value= [mean travel time, nb vehicles]
		di=self.fct_creat_dict_mean_travel_time_entry_exit_link_per_per(v_sim_dur=va_sim_dur,v_t_period=va_t_period,\
		v_t_unit=va_t_unit,v_t_init=va_t_init,val_round_prec=va_round_prec,di_info_entry_exit_lk=val_di_info_entry_exit_lk)
		
		#we write the list of files
		self.fct_write_set_matrices_set_files_key_couple(name_file_to_write=self._file_travel_time_per_period_entry_exit_link,\
		di_key_nb_value_list_valeurs=di,lis_phrases=va_lis_phrases)
		
#*******************************************************************************************************************************************************************************************
	#method creating dict, key=(id entry, id exit link), value=dict, key=(t_start period, t_end period), value=[mean travelled distance, nb veh]
	#v_di_info_exit_veh=key is the vehicle id,value=list
	#[...,[t_vehicle_appearance_in_the_network, [id_entry_link, id_destination_link_1, id_destination_link_2,.... ],.. ]
	def fct_calcul_mean_travel_distance_per_period(self, v_di_info_exit_veh,v_sim_dur,v_t_period,v_t_unit,v_t_init,v_di_internal_lk_info):
		
		#li_t_interval=[..., [t start i period, t_end of ith period],...]
		li_t_interval=[]
		nb_interv=math.ceil(v_sim_dur/v_t_period)
		t_init=v_t_init
		for i in range(nb_interv):
			li_t_interval.append([t_init, t_init+v_t_period-v_t_unit])
			t_init=t_init+v_t_period
		
		
		#nb of time period intervals
		len_li_inter=len(li_t_interval)
		
		
		
		#di_key_id_entry_exit_lk_value_veh_info=dict, key=(id entry, id exit lk), 
		#value=[...,[t_vehicle_appearance_in_the_network, t veh exit, id_entry_link, id_destination_link_1, id_destination_link_2,.... , id exit link],...]
		di_key_id_entry_exit_lk_value_veh_info={}
		
		#print("here1.1", v_di_info_exit_veh)
		
		#v_di_info_exit_veh=dict, key=veh id,
		#value=  [t_vehicle_appearance_in_the_network, t veh exit, id_entry_link, id_destination_link_1, id_destination_link_2,.... , id exit link ]
		for m in v_di_info_exit_veh:
		
			id_ex_lk=len(v_di_info_exit_veh[m])
			
			#if the (id entry, id exit link) not in the dictionary
			if (v_di_info_exit_veh[m][2],v_di_info_exit_veh[m][id_ex_lk-1]) not in di_key_id_entry_exit_lk_value_veh_info:
			
				di_key_id_entry_exit_lk_value_veh_info[v_di_info_exit_veh[m][2],v_di_info_exit_veh[m][id_ex_lk-1]]=[v_di_info_exit_veh[m]]
			
			#if the (id entry, id exit link) is in the dictionary
			else:
				di_key_id_entry_exit_lk_value_veh_info[v_di_info_exit_veh[m][2],v_di_info_exit_veh[m][id_ex_lk-1]].append(v_di_info_exit_veh[m])
				
		for n in di_key_id_entry_exit_lk_value_veh_info:
			di_key_id_entry_exit_lk_value_veh_info[n].sort()
			
		#print("here1",di_key_id_entry_exit_lk_value_veh_info)
			
		#dict, key=(id entry, id exit lk), value=dict, key=(t_start_period, t_end_period), value=[som of (traveled distance), nb vehicles exited during current period]
		di_rep_info_per_period={}
		
		#di_key_id_entry_exit_lk_value_veh_info=dict, key=(id entry, id exit lk),
		#value=[...,[t_vehicle_appearance_in_the_network, t veh exit, id_entry_link, id_destination_link_1, id_destination_link_2,.... , id exit link],...]
		for k in di_key_id_entry_exit_lk_value_veh_info:
			di_rep_info_per_period[k]={}
			
			for p in di_key_id_entry_exit_lk_value_veh_info[k]:
				
			
				#the period interval to which belong the pth vehicle information
				nb_inter=math.floor(p[1]/v_t_period)+1
				
			
				if nb_inter> len_li_inter:
						if nb_inter==len_li_inter+1:
							nb_inter=nb_inter-1
						else:
							print("PROBL IN CL STAT ANALYSIS, FCT fct_calcul_mean_travel_distance_per_period, NUMBER TIME PERIOD INTERVALS ",\
							len_li_inter,"nb_inter",nb_inter)
							import sys
							sys.exit()
				#le=len(di_key_id_entry_exit_lk_value_veh_info[k][p])
				#print("p",p)
				le=len(p)
				le_1=le-1
				traveled_distance=0
				for f in 	p[3:le_1]:	
					#print("link",f,"length",v_di_internal_lk_info[f].get_length_link())
					traveled_distance+=v_di_internal_lk_info[f].get_length_link()
							
				if (li_t_interval[nb_inter-1][0], li_t_interval[nb_inter-1][1]) in di_rep_info_per_period[k]:
				
					di_rep_info_per_period[k][li_t_interval[nb_inter-1][0], li_t_interval[nb_inter-1][1]][0]+=traveled_distance
					
					di_rep_info_per_period[k][li_t_interval[nb_inter-1][0], li_t_interval[nb_inter-1][1]][1]+=1
				
				else:
					di={}
					di[li_t_interval[nb_inter-1][0], li_t_interval[nb_inter-1][1]]=[traveled_distance,1]
					
					di_rep_info_per_period[k].update(di)
		
		di_rep={}
		
		#print("di_rep_info_per_period",di_rep_info_per_period)
		#import sys
		#sys.exit()
		#di_rep_info_per_period=dict, key=(id entry, id exit lk), 
		#value=dict, key=(t_start_period, t_end_period), value=[som of (traveled distance), nb vehicles exited during current period]
		for q in di_rep_info_per_period:
			di_rep[q]={}
			for r in di_rep_info_per_period[q]:
			
				if di_rep_info_per_period[q][r][0]!=0:
					di_rep[q][r]=[round(di_rep_info_per_period[q][r][0]/di_rep_info_per_period[q][r][1],2),di_rep_info_per_period[q][r][1]]
				else:
					di_rep[q][r]=[0,0]
			
			#li_t_interval=[..., [t start i period, t_end of ith period],...]
			for g in li_t_interval:
				if (g[0],g[1]) not in di_rep[q]:
					di_rep[q][g[0],g[1]]=[0,0]
					
		return di_rep
		
#***************************************************************************************************************************************************************************************** 
	#method writing the mean travel distance (for the veh which exited the network)  per period
	def fct_write_mean_traveled_distance_per_period(self,\
	va_veh_final_dest_dynam_construct,va_name_Fres_folder,\
	va_sim_dur,va_t_period,va_t_unit,va_t_init,\
	va_di_internal_lk_info,lis_phrases):
	
	
		va_di_exited_veh_info=Global_Functions.fct_creating_dict_list_exited_veh_files_creat_by_sim_treat(\
		veh_final_dest_dynam_construct=va_veh_final_dest_dynam_construct,\
		name_Fres_folder=va_name_Fres_folder,\
		val_line_number_dyn_constr_veh_final_dest=7,val_line_number_initial_defined_veh_final_dest=8)



		#di=dict, key=(id entry, id exit link), value=dict, key=(t_start period, t_end period), value=[mean travelled distance, nb veh]
		di=self.fct_calcul_mean_travel_distance_per_period(v_di_info_exit_veh=va_di_exited_veh_info,v_sim_dur=va_sim_dur,\
		v_t_period=va_t_period,v_t_unit=va_t_unit,v_t_init=va_t_init,\
		v_di_internal_lk_info=va_di_internal_lk_info)
		
		#print("di",di)
		
		for i in di:
			file=open(self._name_folder_mean_traveled_distance_per_period_entry_exit_lk+"/"+\
			File_Stats_Anal_Folders_And_Files.name_file_traveled_dist_per_period_entry_exit_link+str(i)+".txt","w")
			
			file.write("%s\t \n"%(str(i)))
			
			for j in lis_phrases:
				file.write("%s\t"%(j))
			file.write("\n")
			
			#on trie les cles concerant le t start period
			sorted_keys=sorted(di[i].keys())
			
			for k in sorted_keys:
				file.write("%.2f\t %.2f\t %.2f\t %.2f\n"%(k[0],k[1],di[i][k][0],di[i][k][1]))
			file.close()

#***************************************************************************************************************************************************************************************** 
	#method writing the mean value of each queue in the associated file
	def fct_writing_file_average_length_each_queue_1(self,dict_key_movement_value_record_obj,\
	dict_key_mov_val_sorted_li_t_que_length,val_durat_sim):
	
		#di=self.fct_calcul_average_length_of_each_network_queue_1(dict_key_mov_value_record_obj=dict_key_movement_value_record_obj)
		
		di_2=self.fct_calcul_average_length_of_each_network_queue_2(di_key_mov_val_sorted_li_t_que_length=\
		dict_key_mov_val_sorted_li_t_que_length,val_dur_sim=val_durat_sim)
		
		#print(di_2)
		
		
		file=open(self._file_time_spent_by_veh_in_que+".txt","w")
		file.write("%s\t %s\t %s \n"%("ID CURRENT LINK (1)", "ID DEST LINK (2)", "MEAN QUE LEN"))
		for i in di:
			file.write("%s\t  %s\t %.2f \n"%(i[0],i[1],di[i]))
		file.close()
		

#*****************************************************************************************************************************************************************************************

	#method writing the mean value of each queue in the associated file
	def fct_writing_file_average_time_spent_by_veh_in_a_que_for_each_que(self,\
	di_key_movem_val_sorted_li_t_que_length,val_duration_sim):
	
		#li=[di, mean value of the aver que len], di=dict, key=que id, value=[the average length of the queue, nb of veh went through the que]
		#li=self.fct_calcul_average_time_spent_by_veh_in_a_que_for_each_que(dict_key_mov_value_record_obj=dict_key_movement_value_record_obj)
		
		#di_2=self.fct_calcul_average_time_spent_by_veh_in_a_que_for_each_que_2(di_key_mov_val_sorted_li_t_que_length=\
		#dict_key_mov_val_sorted_li_t_que_length,val_dur_sim=val_durat_sim)
		
		li=self.fct_calcul_average_time_spent_by_veh_in_a_que_for_each_que_2(\
		di_key_mov_val_sorted_li_t_que_length=di_key_movem_val_sorted_li_t_que_length,\
		val_durat_sim=val_duration_sim)
		
		#print(di_2)
		
		#print("HERE",li)
		file=open(self._file_mean_time_spent_by_veh_in_que+".txt","w")
		file.write("%s\t %s\t  %s\t  %s \n"%("ID CURRENT LINK (1)", "ID DEST LINK (2)", "MEAN TIME SPENT BY (ALL) VEHS IN QUE",\
		"TOTAL NB VEH STATIONED IN THE QUE"))
		for i in li[0]:
			file.write("%s\t  %s\t %.2f\t %d \n"%(i[0],i[1],li[0][i][0],li[0][i][1]))
		file.close()
		
		file1=open(self._file_mean_of_aver_sojourn_time+".txt","w")
		file1.write("%s\t  \n"%("AVERAGE OF MEAN SOJOURN TIME OF VEH IN QUEUES"))
		file1.write("%.2f\t "%(li[1]))
		file1.close()
#*****************************************************************************************************************************************************************************************
	#method writing a set of files each for each pair (entry, exit) link, indicating the mean travel time per period
	#lis_phrases="(id entry lk,  id exit link), period (in secs), other lines:  < time value (1st column), mean travel time, total nb veh  (2nd column) "
	def fct_write_set_matrices_set_files_key_couple(self,name_file_to_write,di_key_nb_value_list_valeurs,lis_phrases):


		#di_key_nb_value_list_valeurs=dict, key=(id entry link, id exit link), 
		#value=[[max_value_time of the corresponding interval, mean travel time 1st period, nb veh],
		#[[max_value_time of the corresponding interval,mean travel time 2nd period, nb veh],...]
		
		#for each entry, exit link
		for i in di_key_nb_value_list_valeurs:
		
			file=open(self._folder_stat_anal+"/"+File_Stats_Anal_Folders_And_Files.name_folder_travel_time_per_period_entry_exit_lk+"/"+\
			File_Stats_Anal_Folders_And_Files.name_file_travel_time_per_period_entry_exit_link+str(i)+".txt","w")
			
			file.write("%s\t \n"%(str(i)))
			
			for j in lis_phrases:
				file.write("%s\t "%(j))
			file.write("\n")
			
			#on trie les cles
			sorted_keys=sorted(di_key_nb_value_list_valeurs[i].keys())
			
			#for each period
			for k in sorted_keys:
				#we write the t_start, t_end of the period, the mean travel time, nb of vehicles exited during this period
				#for m in  di_key_nb_value_list_valeurs[i][k]:
				file.write("%.2f\t %.2f\t %.2f\t %d\n"%(k[0],k[1],di_key_nb_value_list_valeurs[i][k][0],\
				di_key_nb_value_list_valeurs[i][k][1]))
			file.close()
			
#*****************************************************************************************************************************************************************************************
	#method writing the file with the total actuation duration of each phase per period
	def fct_write_file_total_actutation_duration_per_period_each_phase(self, name_file_to_write,dict_phase_act_dur_info,lis_phrases):
	
		#dict_phase_act_dur_info=dict, key= id phase, value=dict, key=[t_start_period, t_end period] value=total act dration phase
		for i in dict_phase_act_dur_info:
		
			file=open(self._folder_stat_anal+"/"+File_Stats_Anal_Folders_And_Files.name_folder_phase_act_durat_per_period+"/"+\
			File_Stats_Anal_Folders_And_Files.name_file_total_act_duration_per_period_phase+str(i)+".txt","w")
			
			file.write("%s\t \n"%(str(i)))
			for j in lis_phrases:
				file.write("%s\t"%(j))
			file.write("\n")
			
			#on trie les cles
			sorted_keys=sorted(dict_phase_act_dur_info[i].keys())
			#for each period
			for k in sorted_keys:
				#we write the t_start, t_end of the period,  secs of the actuation duration
				file.write("%.2f\t %.2f\t %.2f\n"%(k[0],k[1],dict_phase_act_dur_info[i][k]))
			file.close()

#*****************************************************************************************************************************************************************************************


	#method write the files with the number of vehicle arrivals and departures per cycle
	def fct_write_files_nb_veh_arrivals_and_departures_per_cycle(self,val_di_veh_ap_ar_per_cycle,\
	val_di_veh_dep_per_cycle,val_cycle_durat,val_di_dep_minus_ar_per_cycle=None):
		
		#creation of the folder
		os.mkdir(self._folder_stat_anal+"/"+\
		self._module_name_importing_file_names_stat_anal.name_folder_nb_veh_ar_dep_per_cycle)
		
		self._folder_que_ar_dep=self._folder_stat_anal+"/"+\
		self._module_name_importing_file_names_stat_anal.name_folder_nb_veh_ar_dep_per_cycle
		
		#self._file_que_ar_dep=self._folder_que_ar_dep+"/"+\
		#self._module_name_importing_file_names_stat_anal.name_file_veh_ar_dep_per_cycle_que
		
		#if len(val_di_veh_ap_ar_per_cycle)!=len(val_di_veh_dep_per_cycle):
			#print("DS CL STAT ANAL, IN FCT fct_write_files_nb_veh_arrivals_and_departures_per_cycle, THE DICT OF VEH AR AND VEH DEP HAVE DIFFERENT SIZES",\
			#len(val_di_veh_ap_ar_per_cycle),len(val_di_veh_dep_per_cycle))
			#import sys
			#sys.exit()
		
		#dict, key=id phase , value=[..., nb veh ar at ith cycle,...]
		for i in val_di_veh_ap_ar_per_cycle:
			
			file=open(self._folder_que_ar_dep+"/"+File_Stats_Anal_Folders_And_Files.name_file_veh_ar_per_cycle_que+str(i)+".txt","w")
			file.write("%s %s  \n"%(" QUE ", str(i)))
			file.write("%s %s %s %s \n"%("VEH ARRIVALS IN QUE", str(i),", CYCLE DURATION ", val_cycle_durat))
			id_cycle=1
			for j in val_di_veh_ap_ar_per_cycle[i]:
				file.write("%d %d \n"%(id_cycle,j))
				id_cycle+=1
		for m in val_di_veh_dep_per_cycle:
			
			file1=open(self._folder_que_ar_dep+"/"+File_Stats_Anal_Folders_And_Files.name_file_veh_dep_per_cycle_que+str(m)+".txt","w")
			file1.write("%s %s  \n"%(" QUE ", str(m)))
			file1.write("%s %s %s %s \n"%("VEH  DEPARTURES FROM  QUE ", str(m),", CYCLE DURATION ", val_cycle_durat))
			id_cycle=1
			for n in val_di_veh_dep_per_cycle[m]:
				file1.write("%d  %d  \n"%(id_cycle, n))
				id_cycle+=1
		#for p in val_di_dep_minus_ar_per_cycle:
			#file2=open(self._folder_que_ar_dep+"/"+File_Stats_Anal_Folders_And_Files.name_file_dif_departs_minus_ar_per_cycle_que+str(p)+".txt","w")
			#file2.write("%s %s  \n"%(" QUE ", str(p)))
			#file2.write("%s %s %s %s \n"%("VEH  DEPARTURES MINUS ARRIVALS,  QUE ", str(p),", CYCLE DURATION ", val_cycle_durat))
			#id_cycle=1
			#for q in val_di_dep_minus_ar_per_cycle[p]:
				#file2.write("%s  %d \n"%(id_cycle,q))
				#id_cycle+=1

			
		file.close()
		file1.close()
		#file2.close()	
		
#*****************************************************************************************************************************************************************************************
	#method calculating the actuation duration of each phase (useful when  stages have different durations within a cycle)
	# it returns dict, key=id phase value=total actuation duration
	# val_dict_key_id_phase_value_li_t_start_ctrl_and_val_ctrl_and_type_ctrl=
	#dict, key=id phase, value=[[...,[temps, crl value, type contrl (0 si RC, 1 sinon]), nb decisions without RC,total nb controls],...]]
	def fct_calc_total_actuat_durat_each_phase(self, val_dict_key_id_phase_value_li_t_start_ctrl_and_val_ctrl_and_type_ctrl,val_t_end_sim):
	
		
	
		di_rep={}
		
		#val_dict_key_id_phase_value_li_t_start_ctrl_and_val_ctrl_and_type_ctrl = dict
		#key=id phase, value=[[...,[temps, crl value, type contrl (0 si RC, 1 sinon]), nb decisions without RC,total nb controls],...]]
		for i in val_dict_key_id_phase_value_li_t_start_ctrl_and_val_ctrl_and_type_ctrl:
			total_dur=0
			nb_ctrls=len(val_dict_key_id_phase_value_li_t_start_ctrl_and_val_ctrl_and_type_ctrl[i])-1
			#print(len(val_dict_key_id_phase_value_li_t_start_ctrl_and_val_ctrl_and_type_ctrl[i]),nb_ctrls)
			for j in range(nb_ctrls):
				#si le ctrl est 1
				if val_dict_key_id_phase_value_li_t_start_ctrl_and_val_ctrl_and_type_ctrl[i][j][1]==1:
					t_start=val_dict_key_id_phase_value_li_t_start_ctrl_and_val_ctrl_and_type_ctrl[i][j][0]
					t_fin=val_dict_key_id_phase_value_li_t_start_ctrl_and_val_ctrl_and_type_ctrl[i][j+1][0]
					dur=t_fin-t_start
					
					if dur <0:
						print("PROBLEM IN CL_STAT_ANAL,  fct_calc_total_actuat_durat_each_phase, CTRL DURATION: ",dur)
						import sys
						sys.exit()
						
					total_dur+=dur
					j=j+1
			#si le dernier ctrl est 1
			total_nb_ctrls=nb_ctrls
			if val_dict_key_id_phase_value_li_t_start_ctrl_and_val_ctrl_and_type_ctrl[i][total_nb_ctrls][1]==1:
				t_start=val_dict_key_id_phase_value_li_t_start_ctrl_and_val_ctrl_and_type_ctrl[i][total_nb_ctrls][0]
				duree=val_t_end_sim - t_start
				if duree<0:
					print("PROBLEM IN CL_STAT_ANAL,  fct_calc_total_actuat_durat_each_phase, CTRL DURAT: ",duree)
					import sys
					sys.exit()
				total_dur+=duree
			di_rep[i]=round(total_dur,2)
			
		return di_rep
				
#*****************************************************************************************************************************************************************************************
	#method returning a dictionary, key id node, value=dict, key = stage id, value=[...,[t start control, t_end control],...]
	#val_dict_ev_type=dict, key=event type, value= record object
	def fct_creat_di_evolution_stage_actuation_celle_qu_on_utilise_1(self,val_dict_ev_type):

		
		di_rep={}
		
		#di_nd=dict, key=id node, value=[...[t_start actuat of a stage, t_end actuat of a stage],..]
		di_nd={}
		
		for i in val_dict_ev_type[Cl_Event.TYPE_EV["type_ev_new_intersection_control"]]:
		
			#if the node id is in the dict
			if i.get_id_inters_node() in di_rep:
				#if the actuated stage is in the diction
				if i.get_id_actuated_stage() in di_rep[i.get_id_inters_node()]:
				
					di_rep[i.get_id_inters_node()][i.get_id_actuated_stage()].append([i.get_t_start_current_inters_control(),i.get_t_end_current_intersection_control()])
					
				#if the actuated stage is not in the dict
				else:
					di={}
					di[i.get_id_actuated_stage()]=[[i.get_t_start_current_inters_control(),i.get_t_end_current_intersection_control()]]
					di_rep[i.get_id_inters_node()].update(di)
			
				di_nd[i.get_id_inters_node()].append([i.get_t_start_current_inters_control(),i.get_t_end_current_intersection_control()])
				
			#if the node id is not in the diction
			else:
				di_rep[i.get_id_inters_node()]={}
				di={}
				di[i.get_id_actuated_stage()]=[[i.get_t_start_current_inters_control(),i.get_t_end_current_intersection_control()]]
				di_rep[i.get_id_inters_node()].update(di)
				
				di_nd[i.get_id_inters_node()]=[[i.get_t_start_current_inters_control(),i.get_t_end_current_intersection_control()]]
				
		#for each node		
		for m in di_nd:
			#for eac act period 
			for n in di_nd[m]:
				#if an act period is not in the dict of each stage we add it with 0 in order to show that during this period the current stage is not actuated
				for p in di_rep[m]:
					if n not in di_rep[m][p]:
						q=[n[0],n[1],0]
						di_rep[m][p].append(q)
					
		
		#for each node
		for r in di_rep:
			#for each stage
			for s in di_rep[r]:
				#for each	actuated period
				for t in  di_rep[r][s]:
					if len(t)==2:	
						t.append(1)
					
					elif  len(t)>3 or  len(t)<2:
						print("PROBLEM IN CL STT ANALYS,fct_creat_di_evolution_stage_actuation LEN INTERVAL:",len(t))
						import sys
						sys.exit()
		
		#for each node
		#for t in di_rep:
			#for each stage
			#for z in di_rep[t]:
				#we sort the times
				#di_rep[t][z].sort()
		#print(di_rep[1])
		#import sys
		#sys.exit()	
		
		di_rep_2={}
		
		#for each node
		for f in di_rep:
			di_rep_2[f]={}
		
			di={}
			#for each stage
			for g in di_rep[f]:
				di[g]=[]
				#for each period
				for p in di_rep[f][g]:
					di[g].append([p[0],p[2]])
					di[g].append([p[1],p[2]])
					
				di_rep_2[f].update(di)
			
		#for each node
		for t in di_rep_2:
			#for each stage
			for z in di_rep[t]:
				#we sort the times
				di_rep_2[t][z].sort()
				
		#print(di_rep_2[1])
		#import sys
		#sys.exit()	
				
		return di_rep_2
		
		
#*****************************************************************************************************************************************************************************************
	#method returning a dictionary, key id node, value=dict, key = stage id, value=[...,[t start control ot t_end ctrl,  indicator node if the  stage is actuates/0 otherwise],...]
	#val_dict_ev_type=dict, key=event type, value= record object
	def fct_creat_di_evolution_stage_actuation_5(self,val_dict_ev_type):

		
		di_rep={}
		
		#di_nb_nb=dict, key=node id, value=1 for the the first node, ..., i for the ith node, so it will be a distance between the plots of the stages for different nodes
		di_nb_nb={}
	
		
		#di_nd=dict, key=id node, value=[...[t_start actuat of a stage, t_end actuat of a stage],..]
		di_nd={}
		
		for i in val_dict_ev_type[Cl_Event.TYPE_EV["type_ev_new_intersection_control"]]:
		
			#if the node id is in the dict
			if i.get_id_inters_node() in di_rep:
				#if the actuated stage is in the diction
				if i.get_id_actuated_stage() in di_rep[i.get_id_inters_node()]:
				
					di_rep[i.get_id_inters_node()][i.get_id_actuated_stage()].append([i.get_t_start_current_inters_control(),i.get_t_end_current_intersection_control(),di_nb_nb[i.get_id_inters_node()]])
					
				#if the actuated stage is not in the dict
				else:
					di={}
					di[i.get_id_actuated_stage()]=[[i.get_t_start_current_inters_control(),i.get_t_end_current_intersection_control(),di_nb_nb[i.get_id_inters_node()]]]
					di_rep[i.get_id_inters_node()].update(di)
			
				di_nd[i.get_id_inters_node()].append([i.get_t_start_current_inters_control(),i.get_t_end_current_intersection_control()])
				
			#if the node id is not in the diction
			else:
			
				di_nb_nb[i.get_id_inters_node()]=i.get_id_inters_node()
				
				
				
				di_rep[i.get_id_inters_node()]={}
				di={}
				di[i.get_id_actuated_stage()]=[[i.get_t_start_current_inters_control(),i.get_t_end_current_intersection_control(),di_nb_nb[i.get_id_inters_node()]]]
				di_rep[i.get_id_inters_node()].update(di)
				
				di_nd[i.get_id_inters_node()]=[[i.get_t_start_current_inters_control(),i.get_t_end_current_intersection_control()]]
				
		#for each node		
		for m in di_nd:
			#for eac act period 
			for n in di_nd[m]:
				r=[n[0],n[1],di_nb_nb[m]]
				#if an act period is not in the dict of each stage we add it with 0 in order to show that during this period the current stage is not actuated
				for p in di_rep[m]:
					if r not in di_rep[m][p]:
						q=[n[0],n[1],0]
						di_rep[m][p].append(q)
					
		
		#for each node
		#for r in di_rep:
			#for each stage
			#for s in di_rep[r]:
				#for each	actuated period
				#for t in  di_rep[r][s]:
					#if len(t)==3:	
						#t.append(di_nb_nb[r])
					
					#elif  len(t)>4 or  len(t)<3:
						#print("PROBLEM IN CL STT ANALYS,fct_creat_di_evolution_stage_actuation LEN INTERVAL:",len(t))
						#import sys
						#sys.exit()
		
		#for each node
		#for t in di_rep:
			#for each stage
			#for z in di_rep[t]:
				#we sort the times
				#di_rep[t][z].sort()
		#print(di_rep[1])
		#import sys
		#sys.exit()	
		
		di_rep_2={}
		
		#for each node
		for f in di_rep:
			di_rep_2[f]={}
		
			di={}
			#for each stage
			for g in di_rep[f]:
				di[g]=[]
				#for each period
				for p in di_rep[f][g]:
					di[g].append([p[0],p[2]])
					di[g].append([p[1],p[2]])
					
				di_rep_2[f].update(di)
			
		#for each node
		for t in di_rep_2:
			#for each stage
			for z in di_rep[t]:
				#we sort the times
				di_rep_2[t][z].sort()
				
		#print(di_rep_2[1])
		#import sys
		#sys.exit()	
				
		return di_rep_2
		
		
#*****************************************************************************************************************************************************************************************
	#method returning a dictionary, key id node, value=dict, key = stage id, value=[...,[t,  indicator node if the  stage is actuates/0 otherwise],...]
	#val_dict_ev_type=dict, key=event type, value= record object
	def fct_creat_di_evolution_stage_actuation_7(self,val_dict_ev_type,val_t_unit):

		
		di_rep={}
		
		#di_nb_nb=dict, key=node id, value=1 for the the first node, ..., i for the ith node, so it will be a distance between the plots of the stages for different nodes
		di_nb_nb={}
	
		
		#di_nd=dict, key=id node, value=[...[t_start actuat of a stage, t_end actuat of a stage],..]
		di_nd={}
		
		for i in val_dict_ev_type[Cl_Event.TYPE_EV["type_ev_new_intersection_control"]]:
		
			#if the node id is in the dict
			if i.get_id_inters_node() in di_rep:
				#if the actuated stage is in the diction
				if i.get_id_actuated_stage() in di_rep[i.get_id_inters_node()]:
				
					di_rep[i.get_id_inters_node()][i.get_id_actuated_stage()].append([i.get_t_start_current_inters_control(),i.get_t_end_current_intersection_control(),di_nb_nb[i.get_id_inters_node()]])
					
				#if the actuated stage is not in the dict
				else:
					di={}
					di[i.get_id_actuated_stage()]=[[i.get_t_start_current_inters_control(),i.get_t_end_current_intersection_control(),di_nb_nb[i.get_id_inters_node()]]]
					di_rep[i.get_id_inters_node()].update(di)
			
				di_nd[i.get_id_inters_node()].append([i.get_t_start_current_inters_control(),i.get_t_end_current_intersection_control()])
				
			#if the node id is not in the diction
			else:
			
				di_nb_nb[i.get_id_inters_node()]=i.get_id_inters_node()
				
				
				
				di_rep[i.get_id_inters_node()]={}
				di={}
				di[i.get_id_actuated_stage()]=[[i.get_t_start_current_inters_control(),i.get_t_end_current_intersection_control(),di_nb_nb[i.get_id_inters_node()]]]
				di_rep[i.get_id_inters_node()].update(di)
				
				di_nd[i.get_id_inters_node()]=[[i.get_t_start_current_inters_control(),i.get_t_end_current_intersection_control()]]
				
		#for each node		
		for m in di_nd:
			#for eac act period 
			for n in di_nd[m]:
				r=[n[0],n[1],di_nb_nb[m]]
				#if an act period is not in the dict of each stage we add it with 0 in order to show that during this period the current stage is not actuated
				for p in di_rep[m]:
					if r not in di_rep[m][p]:
						q=[n[0],n[1],0]
						di_rep[m][p].append(q)
					
		
		#for each node
		#for r in di_rep:
			#for each stage
			#for s in di_rep[r]:
				#for each	actuated period
				#for t in  di_rep[r][s]:
					#if len(t)==3:	
						#t.append(di_nb_nb[r])
					
					#elif  len(t)>4 or  len(t)<3:
						#print("PROBLEM IN CL STT ANALYS,fct_creat_di_evolution_stage_actuation LEN INTERVAL:",len(t))
						#import sys
						#sys.exit()
		
		#for each node
		#for t in di_rep:
			#for each stage
			#for z in di_rep[t]:
				#we sort the times
				#di_rep[t][z].sort()
		#print(di_rep[1])
		#import sys
		#sys.exit()	
		
		di_rep_2={}
		
		#for each node
		for f in di_rep:
			di_rep_2[f]={}
		
			di={}
			#for each stage
			for g in di_rep[f]:
				di[g]=[]
				#for each period
				for p in di_rep[f][g]:
					di[g].append([p[0],p[2]])
					di[g].append([p[1],p[2]])
					
				di_rep_2[f].update(di)
			
		#for each node
		for t in di_rep_2:
			#for each stage
			for z in di_rep_2[t]:
				#we sort the times
				di_rep_2[t][z].sort()
		
		di_rep_3={}
		
		#for each node		
		for h in di_rep_2:
			di_rep_3[h]={}
			#for each stage of the node
			for e in di_rep_2[h]:
			
				di_rep_3[h][e]=[]
				#di_rep_2[h][e]=[...,[t_init ou t fin, valeur>0],...]
				le=int(len(di_rep_2[h][e])/2)
				
				pas=0
				
				#for each [t, valeur]
				for a in range(le):
					a1=int(a+pas)
					
					#di_rep_2[h][e][a1]=[temps, 0 or >0]
					if di_rep_2[h][e][a1][1]!=0:
					
						#we add the 2 elements [t init, >0], [t fin,>0] in the list of the dict
						di_rep_3[h][e].append([di_rep_2[h][e][a1][0],di_rep_2[h][e][a1][1]])
						di_rep_3[h][e].append([di_rep_2[h][e][a1+1][0],di_rep_2[h][e][a1+1][1]])
						
						#creation des pts interm
						#nb_times=(t_fin-t_int)/time unit
						nb_times=round((di_rep_2[h][e][a1+1][0]-di_rep_2[h][e][a1][0])/val_t_unit,1)
						nb_t=int(nb_times-2)
						for k1 in range(nb_t):
							li_1=[di_rep_2[h][e][a1][0]+ (k1+1)*val_t_unit,di_rep_2[h][e][a1][1]]
							
							#indice=a1+k1+1
							#di_rep_3[n][e].index([di_rep_2[h][e][a1][0],di_rep_2[h][e][a1][1]])
							#di_rep_2[h][e].insert(indice,li_1)
							
							di_rep_3[h][e].insert(len(di_rep_3[h][e])-1,li_1)
							
						pas+=1
						
					#if the valeur y=0:
					else:
						di_rep_3[h][e].append([di_rep_2[h][e][a1][0],di_rep_2[h][e][a1][1]])
						di_rep_3[h][e].append([di_rep_2[h][e][a1+1][0],di_rep_2[h][e][a1+1][1]])
						pas+=1
												
				
		#print(di_rep_2[1])
		#import sys
		#sys.exit()	
				
		return di_rep_3
		
		
#*****************************************************************************************************************************************************************************************
	#method returning a dictionary, key id node, value=dict, key = stage id, value=[...,[t,  indicator node if the  stage is actuates/0 otherwise],...]
	#val_dict_ev_type=dict, key=event type, value= record object
	def fct_creat_di_evolution_stage_actuation(self,val_dict_ev_type,val_t_unit):

		
		di_rep={}
		
		#di_nb_nb=dict, key=node id, value=1 for the the first node, ..., i for the ith node, so it will be a distance between the plots of the stages for different nodes
		di_nb_nb={}
	
		
		#di_nd=dict, key=id node, value=[...[t_start actuat of a stage, t_end actuat of a stage],..]
		di_nd={}
		
		for i in val_dict_ev_type[Cl_Event.TYPE_EV["type_ev_new_intersection_control"]]:
		
			#if the node id is in the dict
			if i.get_id_inters_node() in di_rep:
				#if the actuated stage is in the diction
				if i.get_id_actuated_stage() in di_rep[i.get_id_inters_node()]:
				
					di_rep[i.get_id_inters_node()][i.get_id_actuated_stage()].append([i.get_t_start_current_inters_control(),i.get_t_end_current_intersection_control(),di_nb_nb[i.get_id_inters_node()]])
					
				#if the actuated stage is not in the dict
				else:
					di={}
					di[i.get_id_actuated_stage()]=[[i.get_t_start_current_inters_control(),i.get_t_end_current_intersection_control(),di_nb_nb[i.get_id_inters_node()]]]
					di_rep[i.get_id_inters_node()].update(di)
			
				di_nd[i.get_id_inters_node()].append([i.get_t_start_current_inters_control(),i.get_t_end_current_intersection_control()])
				
			#if the node id is not in the diction
			else:
			
				di_nb_nb[i.get_id_inters_node()]=i.get_id_inters_node()
				
				
				
				di_rep[i.get_id_inters_node()]={}
				di={}
				di[i.get_id_actuated_stage()]=[[i.get_t_start_current_inters_control(),i.get_t_end_current_intersection_control(),di_nb_nb[i.get_id_inters_node()]]]
				di_rep[i.get_id_inters_node()].update(di)
				
				di_nd[i.get_id_inters_node()]=[[i.get_t_start_current_inters_control(),i.get_t_end_current_intersection_control()]]
				
		#for each node		
		for m in di_nd:
			#for eac act period 
			for n in di_nd[m]:
				r=[n[0],n[1],di_nb_nb[m]]
				#if an act period is not in the dict of each stage we add it with 0 in order to show that during this period the current stage is not actuated
				for p in di_rep[m]:
					if r not in di_rep[m][p]:
						q=[n[0],n[1],0]
						di_rep[m][p].append(q)
					
		
		#for each node
		#for r in di_rep:
			#for each stage
			#for s in di_rep[r]:
				#for each	actuated period
				#for t in  di_rep[r][s]:
					#if len(t)==3:	
						#t.append(di_nb_nb[r])
					
					#elif  len(t)>4 or  len(t)<3:
						#print("PROBLEM IN CL STT ANALYS,fct_creat_di_evolution_stage_actuation LEN INTERVAL:",len(t))
						#import sys
						#sys.exit()
		
		#for each node
		#for t in di_rep:
			#for each stage
			#for z in di_rep[t]:
				#we sort the times
				#di_rep[t][z].sort()
		#print(di_rep[1])
		#import sys
		#sys.exit()	
		
		di_rep_2={}
		
		#for each node
		for f in di_rep:
			di_rep_2[f]={}
		
			di={}
			#for each stage
			for g in di_rep[f]:
				di[g]=[]
				#for each period
				for p in di_rep[f][g]:
					di[g].append([p[0],p[2]])
					di[g].append([p[1],p[2]])
					
				di_rep_2[f].update(di)
			
		#for each node
		for t in di_rep_2:
			#for each stage
			for z in di_rep_2[t]:
				#we sort the times
				di_rep_2[t][z].sort()
		
		di_rep_3={}
		
		#for each node		
		for h in di_rep_2:
			di_rep_3[h]={}
			#for each stage of the node
			for e in di_rep_2[h]:
			
				di_rep_3[h][e]=[]
				#di_rep_2[h][e]=[...,[t_init ou t fin, valeur>0],...]
				le=int(len(di_rep_2[h][e])/2)
				
				pas=0
				
				#for each [t, valeur]
				for a in range(le):
					a1=int(a+pas)
					
					#di_rep_2[h][e][a1]=[temps, 0 or >0]
					if di_rep_2[h][e][a1][1]!=0:
					
						#we add the 2 elements [t init, >0], [t fin,>0] in the list of the dict
						di_rep_3[h][e].append([di_rep_2[h][e][a1][0],di_rep_2[h][e][a1][1]])
						di_rep_3[h][e].append([di_rep_2[h][e][a1+1][0],di_rep_2[h][e][a1+1][1]])
						
						#creation des pts interm
						#nb_times=(t_fin-t_int)/time unit
						nb_times=round((di_rep_2[h][e][a1+1][0]-di_rep_2[h][e][a1][0])/val_t_unit,1)
						nb_t=int(nb_times-1)
						for k1 in range(nb_t):
							li_1=[di_rep_2[h][e][a1][0]+ (k1+1)*val_t_unit,di_rep_2[h][e][a1][1]]
							
							#indice=a1+k1+1
							#di_rep_3[n][e].index([di_rep_2[h][e][a1][0],di_rep_2[h][e][a1][1]])
							#di_rep_2[h][e].insert(indice,li_1)
							
							di_rep_3[h][e].insert(len(di_rep_3[h][e])-1,li_1)
							
						pas+=1
						
					#if the valeur y=0:
					else:
						di_rep_3[h][e].append([di_rep_2[h][e][a1][0],di_rep_2[h][e][a1][1]])
						
						di_rep_3[h][e].append([di_rep_2[h][e][a1+1][0],di_rep_2[h][e][a1+1][1]])
						
						#creation of the intermediate values
						#nb_times=(t_fin-t_int)/time unit
						nb_tim=round((di_rep_2[h][e][a1+1][0]-di_rep_2[h][e][a1][0])/val_t_unit,1)
						nb_ti=int(nb_tim-1)
						for v1 in range(nb_ti):
							li_2=[di_rep_2[h][e][a1][0]+ (v1+1)*val_t_unit,di_rep_2[h][e][a1][1]]
							di_rep_3[h][e].insert(len(di_rep_3[h][e])-1,li_2)
						
						
						pas+=1
												
				
		#print(di_rep_2[1])
		#import sys
		#sys.exit()	
				
		return di_rep_3
		
		
#*****************************************************************************************************************************************************************************************
	
	#method returning a dictionary, key id node, value=dict, key = stage id, value=[...,[t start control, t_end control],...]
	#val_dict_ev_type=dict, key=event type, value= record object
	def fct_creat_di_evolution_stage_actuation_2(self,val_dict_ev_type):
	
		di_rep={}
		for i in val_dict_ev_type[Cl_Event.TYPE_EV["type_ev_new_intersection_control"]]:
			
			#if the node id is in the dict
			if i.get_id_inters_node() in di_rep:
				#if the actuated stage is in the diction
				if i.get_id_actuated_stage() in di_rep[i.get_id_inters_node()]:
				
					dur=round(i.get_t_end_current_intersection_control()-i.get_t_start_current_inters_control(),2)
					di_rep[i.get_id_inters_node()][i.get_id_actuated_stage()].append([i.get_t_start_current_inters_control(),dur])
				
				#if the actuated stage is not in the dict
				else:
					di={}
					dur=round(i.get_t_end_current_intersection_control()-i.get_t_start_current_inters_control(),2)
					di[i.get_id_actuated_stage()]=[[i.get_t_start_current_inters_control(),dur]]
					di_rep[i.get_id_inters_node()].update(di)
			
			#if the node id is not in the diction
			else:
				di_rep[i.get_id_inters_node()]={}
				di={}
				dur=round(i.get_t_end_current_intersection_control()-i.get_t_start_current_inters_control(),2)
				di[i.get_id_actuated_stage()]=[[i.get_t_start_current_inters_control(),dur]]
				di_rep[i.get_id_inters_node()].update(di)
		#print(di_rep)
		#import sys
		#sys.exit()
		return di_rep
#*****************************************************************************************************************************************************************************************
	#method returning a dictionary, key id node, value=dict, key = stage id, value=[...,[t start control, t_end control],...]
	#val_dict_ev_type=dict, key=event type, va-lue= record object
	def fct_creat_di_evolution_stage_actuation_3(self,val_dict_ev_type,v_t_unit=0.1):
	
		di_rep={}
		
		#di_nb_nb=dict, key=node id, value=1 for the the first node, ..., i for the ith node, so it will be a distance between the plots of the stages for different nodes
		di_nb_nb={}
		indicator_node=1
		
		#key=id node, value=dict, key=id stage, value =nb with wich the t_unit will be multiplied when computing if the same satge is conrinuously actuated
		#di_nds={}
		for i in val_dict_ev_type[Cl_Event.TYPE_EV["type_ev_new_intersection_control"]]:
			
			
			
			#if the node id is in the dict
			if i.get_id_inters_node() in di_rep:
				
				#if the actuated stage is in the diction
				if i.get_id_actuated_stage() in di_rep[i.get_id_inters_node()]:
				
					
					dur=round(i.get_t_end_current_intersection_control()-i.get_t_start_current_inters_control(),2)+v_t_unit
					
					
					le=len(di_rep[i.get_id_inters_node()][i.get_id_actuated_stage()])-1
					
					#print("di_rep[i.get_id_inters_node()][i.get_id_actuated_stage()][le][2]",di_rep[i.get_id_inters_node()][i.get_id_actuated_stage()][le])
					#if the current actuation continues the previous actuation (t_end+t_unit=t_start)
					if di_rep[i.get_id_inters_node()][i.get_id_actuated_stage()][le][2]+v_t_unit==i.get_t_start_current_inters_control():
					
						#we update the duration
						di_rep[i.get_id_inters_node()][i.get_id_actuated_stage()][le][1]+=dur
						
						#we update the t_end_previous control
						di_rep[i.get_id_inters_node()][i.get_id_actuated_stage()][le][2]=i.get_t_end_current_intersection_control()
						
						
					else:
					
						di_rep[i.get_id_inters_node()][i.get_id_actuated_stage()].append([i.get_t_start_current_inters_control(),dur,i.get_t_end_current_intersection_control(),\
						di_nb_nb[i.get_id_inters_node()]])
						
				#if i.get_id_inters_node()==1:
						#print("current dur'",dur, "dt_start:", \
						# di_rep[i.get_id_inters_node()][i.get_id_actuated_stage()][len(di_rep[i.get_id_inters_node()][i.get_id_actuated_stage()])-1][0])
						
				
				#if the actuated stage is not in the dict
				else:
					
					
					di={}
					dur=round(i.get_t_end_current_intersection_control()-i.get_t_start_current_inters_control(),2)+v_t_unit
					di[i.get_id_actuated_stage()]=[[i.get_t_start_current_inters_control(),dur,i.get_t_end_current_intersection_control(),di_nb_nb[i.get_id_inters_node()]]]
					di_rep[i.get_id_inters_node()].update(di)
					
					
					
					
			
			#if the node id is not in the diction
			else:
				di_nb_nb[i.get_id_inters_node()]=indicator_node
				
				indicator_node+=1
				
				di_rep[i.get_id_inters_node()]={}
				di={}
				dur=round(i.get_t_end_current_intersection_control()-i.get_t_start_current_inters_control(),2)+v_t_unit
				di[i.get_id_actuated_stage()]=[[i.get_t_start_current_inters_control(),dur,i.get_t_end_current_intersection_control(),di_nb_nb[i.get_id_inters_node()]]]
				di_rep[i.get_id_inters_node()].update(di)
				
				
		#print(di_rep)
		#print()
		di_rep_1={}
		for m in di_rep:
			di_rep_1[m]={}
			for n in di_rep[m]:
				di_1={}
				di_1[n]=[]
				for k in di_rep[m][n]:
					di_1[n].append([k[0],k[2],k[3]])
					di_rep_1[m].update(di_1)
		#print(di_rep_1)			
		#import sys
		#sys.exit()
		return di_rep_1
#*****************************************************************************************************************************************************************************************
	#method returning a dictionary, key id node, value=dict, key = stage id, value=[...,[t start control, t_end control, indicator corresponding to node for the plot],...]
	#val_dict_ev_type=dict, key=event type, value= record object
	def fct_creat_di_evolution_stage_actuation_4(self,val_dict_ev_type):
	
		di_rep={}
		
		#di_nb_nb=dict, key=node id, value=1 for the the first node, ..., i for the ith node, so it will be a distance between the plots of the stages for different nodes
		di_nb_nb={}
		indicator_node=1
		for i in val_dict_ev_type[Cl_Event.TYPE_EV["type_ev_new_intersection_control"]]:
			
			#if the node id is in the dict
			if i.get_id_inters_node() in di_rep:
				#if the actuated stage is in the diction
				if i.get_id_actuated_stage() in di_rep[i.get_id_inters_node()]:
				
					di_rep[i.get_id_inters_node()][i.get_id_actuated_stage()].append([i.get_t_start_current_inters_control(),i.get_t_end_current_intersection_control(),di_nb_nb[i.get_id_inters_node()]])
				
				#if the actuated stage is not in the dict
				else:
					di={}
					di[i.get_id_actuated_stage()]=[[i.get_t_start_current_inters_control(),i.get_t_end_current_intersection_control(),di_nb_nb[i.get_id_inters_node()]]]
					di_rep[i.get_id_inters_node()].update(di)
			
			#if the node id is not in the diction
			else:
			
				di_nb_nb[i.get_id_inters_node()]=indicator_node
				
				indicator_node+=1
			
				di_rep[i.get_id_inters_node()]={}
				di={}
				di[i.get_id_actuated_stage()]=[[i.get_t_start_current_inters_control(),i.get_t_end_current_intersection_control(),di_nb_nb[i.get_id_inters_node()]]]
				di_rep[i.get_id_inters_node()].update(di)
		
		return di_rep
#*****************************************************************************************************************************************************************************************
	#method returning a dictionary computing for each node the number of swithces from one stage to another oevr the entire sim duration
	#val_dict_ev_type=dict, key=event type, value= record object
	def fct_calcul_nb_stage_switches_per_inters(self, val_dict_ev_type):
	
		#di_rep=dict, key= id node, value nb of switches
		di_rep={}
		
		#di_id_nd_valeur_id_cur_stage=dict, key=node id, value=the current stage id 
		di_id_nd_valeur_id_cur_stage={}
		
		for i in val_dict_ev_type[Cl_Event.TYPE_EV["type_ev_new_intersection_control"]]:
		
			#if the node id is in the dictionary
			if i.get_id_inters_node() in di_rep:
			
				#if the current stage is different from te previous one
				if i.get_id_actuated_stage()!=di_id_nd_valeur_id_cur_stage[i.get_id_inters_node()]:
				
					di_rep[i.get_id_inters_node()]+=1
					
					di_id_nd_valeur_id_cur_stage[i.get_id_inters_node()]=i.get_id_actuated_stage()
			
			#if the node id is not in the dictionary
			else:
				di_rep[i.get_id_inters_node()]=1
				
				di_id_nd_valeur_id_cur_stage[i.get_id_inters_node()]=i.get_id_actuated_stage()
				
		#print(di_rep)
		#import sys
		#sys.exit()
				
		return di_rep
				
				

#*****************************************************************************************************************************************************************************************
	#method writing the files with the cotnrol evolution of each stage of each intersection
	def fct_write_files_control_evolution_per_intersection_1(self,val_dic_ev_type,val_li_phrases=["t_start or end stage act. duration (1st colm) value act. duration (2nd colm), value to plot"]):
	
		#di=ictionary, key id node, value=dict, key = stage id, value=[...,[t start control, t_end control],...]
		di=self.fct_creat_di_evolution_stage_actuation(val_dict_ev_type=val_dic_ev_type)
		
		di_1=self.fct_creat_di_evolution_stage_actuation_2(val_dict_ev_type=val_dic_ev_type)
		
		for i in di:
			#print("i",i)
			for j in di[i]:
				#print("j",j)
				file=open(self._folder_stage_evol_inters+"/"+File_Stats_Anal_Folders_And_Files.name_file_stage_evol_per_intersection+str(i)+"_"+str(j)+".txt","w")
				file.write("%s\t %s\t \n" %("id node",i))
				file.write("%s\t %s\t \n" %("id stage",j))
				for m in val_li_phrases:
					file.write("%s\t \n"%(m))
				for k in di[i][j]:
					#print("k",k)
					for n in k:
						file.write("%.2f\t"%(n))
					file.write("\n")
			file.close()
			
			
		for i in di_1:
			#print("i",i)
			for j in di_1[i]:
				#print("j",j)
				file=open(self._folder_stage_evol_nodes+"/"+"fi_stage_evol_per_node"+str(i)+"_"+str(j)+".txt","w")
				file.write("%s\t %s\t \n" %("id node",i))
				file.write("%s\t %s\t \n" %("id stage",j))
				for m in val_li_phrases:
					file.write("%s\t \n"%(m))
				for k in di_1[i][j]:
					#print("k",k)
					for n in k:
						file.write("%.2f\t"%(n))
					file.write("\n")
			file.close()


#*****************************************************************************************************************************************************************************************
	#method writing the files with the cotnrol evolution of each stage of each intersection
	def fct_write_files_control_evolution_per_intersection(self,val_dic_ev_type,val_time_unit,val_li_phrases=["time (1st colm), node indicator (>0 value) if the stage is actuated/0 otherwise (2nd colm)"]):
	
		#di=ictionary, key id node, value=dict, key = stage id, value=[...,[t start control, t_end control],...]
		di=self.fct_creat_di_evolution_stage_actuation(val_dict_ev_type=val_dic_ev_type,val_t_unit=val_time_unit)
		
		
		
		for i in di:
			#print("i",i)
			for j in di[i]:
				#print("j",j)
				file=open(self._folder_stage_evol_inters+"/"+File_Stats_Anal_Folders_And_Files.name_file_stage_evol_per_intersection+str(i)+"_"+str(j)+".txt","w")
				file.write("%s\t %s\t \n" %("id node",i))
				file.write("%s\t %s\t \n" %("id stage",j))
				for m in val_li_phrases:
					file.write("%s\t \n"%(m))
				for k in di[i][j]:
					#print("k",k)
					for n in k:
						file.write("%.2f\t"%(n))
					file.write("\n")
			file.close()
			

#*****************************************************************************************************************************************************************************************
	#method writing the file with the number of switches per  intersection node
	def fct_write_file_nb_stage_switches_per_inters(self,val_dic_ev_type,val_li_phrases=["id node (1st colm), nb stage switches (2nd colm)"]):
	
		#di=dict, key=node id value=number of switches
		di=self.fct_calcul_nb_stage_switches_per_inters(val_dict_ev_type=val_dic_ev_type)
		
		file=open(self._folder_stage_switches_per_intersection+"/"+File_Stats_Anal_Folders_And_Files.name_file_stage_switches_per_itnersection,"w")
		
		for m in val_li_phrases:
				file.write("%s\t \n"%(m))
		
		for i in di:
				file.write("%d\t %.2f\t \n"%(i,di[i]))
		file.close()
			
			

#*****************************************************************************************************************************************************************************************

	#method write files with the ctrl evolution
	def fct_write_files_ctrl_evolution_1(self,va_dict_db_key_id_event_type_val_record_obj,val_dict_veh_depart_per_cycle_per_phase,val_t_end_simul,val_cycle_durat):
	
		#dict, key=id phase, value=[[...,[temps, crl value, type contrl (0 si RC, 1 sinon]), nb decisions without RC,total nb controls],...]]
		di_rep=self.fct_creat_dict_ctrl_per_phase(dict_db_key_id_event_type_val_record_obj=va_dict_db_key_id_event_type_val_record_obj)
	

		
		
		#dict, key=id phase , value=Total actuat durat
		#di_id_phase_value_total_act_dur=self.fct_calc_total_actuat_durat_each_phase(\
		#val_dict_key_id_phase_value_li_t_start_ctrl_and_val_ctrl_and_type_ctrl=di_rep,val_t_end_sim=val_t_end_simul)
				
		#dict, key=id phase, value=[nb times actuated,[.., time ith actuation,..]]
		#di_nb_times_phase_act=self.fct_creat_dict_nb_times_actuat_phase(dict_key_id_phase_val_lis_time_and_ctrl_value=di_rep)
		
		#dict, key=id phase, value=nb control changes no RC incuded
		#di_ctrl_changes_per_phase=self.fct_calcul_nb_ctrl_changes_no_rc( di_key_id_phase_value_temps_and_ctrl_value_and_type_ctrl=di_rep)
		
		#dict, key=id phase, value=nb_act per cycly
		#di_nb_act_phase_per_cycle=self.fct_calcul_nb_actuation_per_cycle_each_phase(\
		#val_dict_ctrl_inf=di_rep,val_cycle_duration=val_cycle_durat,val_t_end_sim=val_t_end_simul)
		
		#dict, key=id phase, value=[ time actuat stage related per cycle,...]
		di_id_phase_value_nb_act_per_cycle=self.fct_calcul_nb_actuation_per_cycle_each_phase(\
		val_dict_ctrl_inf=di_rep,val_cycle_duration=val_cycle_durat,val_t_end_sim=val_t_end_simul)
		
		#print(di_id_phase_value_nb_act_per_cycle[13,14])
		#import sys
		#sys.exit()
		
		#val_dict_depart_per_cycle, duct key=id phase, value=[...,nb veh arrived at ith cycle,...]
		#on creera un dict, key=id phase, value=[...., [act dura of phase at ith cycle, nb departed veh at ith cycle],....]
		#di_id_phase_value_li_actat_dur_and_nb_dep_veh_per_cycle=self.fct_calcul_act_duration_and_nb_depart_veh_per_cycle_per_phase(\
		#va_dict_nb_dep_veh_per_cycle_per_phase=val_dict_veh_depart_per_cycle_per_phase,\
		#va_dict_act_durat_per_cycle_per_phase=di_id_phase_value_nb_act_per_cycle)
		
		di_id_phase_value_li_actat_dur_and_nb_dep_veh_per_cycle=self.fct_calcul_nb_depart_veh_over_act_dur_per_cycle_per_phase(\
		va_dict_nb_dep_veh_per_cycle_per_phase=val_dict_veh_depart_per_cycle_per_phase,\
		va_dict_act_durat_per_cycle_per_phase=di_id_phase_value_nb_act_per_cycle)
		
		
		
		#print(di_id_phase_value_li_actat_dur_and_nb_dep_veh_per_cycle[1,2])
		#import sys
		#sys.exit()
		
		#print(di_nb_times_phase_act[1,2][0])
		
		for i in di_rep:
			
			file=open(self._folder_ctrl_evol+"/"+File_Stats_Anal_Folders_And_Files.name_file_ctrl_evolution_phase+str(i)+".txt","w")
			file.write("%s\t  %s\t  %s\t  %d\t  %s\t  \n"%(\
			"PHASE", str(i),\
			", TOTAL NB CTRLS DURING SIM NO RC, ", di_rep[i][len(di_rep[i])-1][3],\
			", time, ctrl value, ctrl type 0: RC 1: otherwise, (1,2,3, clmns) "))
			
			#file1=open(self._folder_ctrl_evol+"/"+File_Stats_Anal_Folders_And_Files.name_file_time_actuation_phase+str(i)+".txt","w")
			#file1.write( "%s\t %s \n"%("actuation time of  phase ",str(i)))
			#for j in di_nb_times_phase_act[i][1]:
				#file1.write( "%.2f \n"%(j))
								

			for k in di_id_phase_value_nb_act_per_cycle:
				file2=open(self._folder_ctrl_evol+"/"+File_Stats_Anal_Folders_And_Files.name_file_nb_actuation_per_cycle_phase+str(k)+".txt","w")
				file2.write( "%s\t %s\t   %s \n"%("id cycle (1st colmn) actuation dyration per cycle of  phase (2nd column)  ","cycle duration",\
				val_cycle_durat))
				
				ind=0
				for m in di_id_phase_value_nb_act_per_cycle[k]:
					ind+=1
					file2.write( "%d\t %.2f \n"%(ind,m))
	
			for j in di_rep[i]:
				file.write("%.2f\t %d\t %d\n"%(j[0],j[1],j[2]))
				
				
			#we write the file with the act duration and the nb departed veh per phase per cycle
			for m in di_id_phase_value_li_actat_dur_and_nb_dep_veh_per_cycle:
				file3=open(self._folder_ctrl_evol+"/"+File_Stats_Anal_Folders_And_Files.name_file_act_dur_and_veh_depart_per_cycle_per_phase+str(m)+".txt","w")
				file3.write("%s\t \n"%("Phase Act duration per cycle (1st col), nb departed veh during cycle (2 col) "))
				file3.write("%s\t %s\t \n"%("Phase",str(m)))
				for n in di_id_phase_value_li_actat_dur_and_nb_dep_veh_per_cycle[m]:
					file3.write("%.2f\t %.2f\t \n"%(n[0],n[1]))
				
			file.close()
			#file1.close()
			file2.close()
			file3.close()
			
#*****************************************************************************************************************************************************************************************
	#method write files with the ctrl evolution
	#def fct_write_files_ctrl_evolution(self,va_dict_db_key_id_event_type_val_record_obj,val_dict_veh_depart_per_cycle_per_phase,val_t_end_simul,val_cycle_durat):
	def fct_write_files_ctrl_evolution(self,va_dict_db_key_id_event_type_val_record_obj):
	
		#dict, key=id phase, value=[[...,[temps, crl value, type contrl (0 si RC, 1 sinon]), nb decisions without RC,total nb controls],...]]
		#di_rep=self.(dict_db_key_id_event_type_val_record_obj=va_dict_db_key_id_event_type_val_record_obj)
		#print("here",di_rep)
		#print()
		#print(di_rep.keys())
		#import sys
		#sys.exit()
		
		#dict, key=id phase , value=Total actuat durat
		#di_id_phase_value_total_act_dur=self.fct_calc_total_actuat_durat_each_phase(\
		#val_dict_key_id_phase_value_li_t_start_ctrl_and_val_ctrl_and_type_ctrl=di_rep,val_t_end_sim=val_t_end_simul)
				
		#dict, key=id phase, value=[nb times actuated,[.., time ith actuation,..]]
		#di_nb_times_phase_act=self.fct_creat_dict_nb_times_actuat_phase(dict_key_id_phase_val_lis_time_and_ctrl_value=di_rep)
		
		#dict, key=id phase, value=nb control changes no RC incuded
		#di_ctrl_changes_per_phase=self.fct_calcul_nb_ctrl_changes_no_rc( di_key_id_phase_value_temps_and_ctrl_value_and_type_ctrl=di_rep)
		
		#dict, key=id phase, value=nb_act per cycly
		#di_nb_act_phase_per_cycle=self.fct_calcul_nb_actuation_per_cycle_each_phase(\
		#val_dict_ctrl_inf=di_rep,val_cycle_duration=val_cycle_durat,val_t_end_sim=val_t_end_simul)
		
		#dict, key=id phase, value=[ time actuat stage related per cycle,...]
		#di_id_phase_value_nb_act_per_cycle=self.fct_calcul_nb_actuation_per_cycle_each_phase(\
		#val_dict_ctrl_inf=di_rep,val_cycle_duration=val_cycle_durat,val_t_end_sim=val_t_end_simul)
		
		#print(di_id_phase_value_nb_act_per_cycle[13,14])
		#import sys
		#sys.exit()
		
		#val_dict_depart_per_cycle, duct key=id phase, value=[...,nb veh arrived at ith cycle,...]
		#on creera un dict, key=id phase, value=[...., [act dura of phase at ith cycle, nb departed veh at ith cycle],....]
		#di_id_phase_value_li_actat_dur_and_nb_dep_veh_per_cycle=self.fct_calcul_act_duration_and_nb_depart_veh_per_cycle_per_phase(\
		#va_dict_nb_dep_veh_per_cycle_per_phase=val_dict_veh_depart_per_cycle_per_phase,\
		#va_dict_act_durat_per_cycle_per_phase=di_id_phase_value_nb_act_per_cycle)
		
		#di_id_phase_value_li_actat_dur_and_nb_dep_veh_per_cycle=self.fct_calcul_nb_depart_veh_over_act_dur_per_cycle_per_phase(\
		#va_dict_nb_dep_veh_per_cycle_per_phase=val_dict_veh_depart_per_cycle_per_phase,\
		#va_dict_act_durat_per_cycle_per_phase=di_id_phase_value_nb_act_per_cycle)
		
		
		
		#print(di_id_phase_value_li_actat_dur_and_nb_dep_veh_per_cycle[1,2])
		#import sys
		#sys.exit()
		
		#print(di_nb_times_phase_act[1,2][0])
		
		for i in di_rep:
			
			file=open(self._folder_ctrl_evol+"/"+File_Stats_Anal_Folders_And_Files.name_file_ctrl_evolution_phase+str(i)+".txt","w")
			file.write("%s\t  %s\t  %s\t  %d\t  %s\t  \n"%(\
			"PHASE", str(i),\
			", TOTAL NB CTRLS DURING SIM NO RC, ", di_rep[i][len(di_rep[i])-1][3],\
			", time, ctrl value, ctrl type 0: RC 1: otherwise, (1,2,3, clmns) "))
			
			#file1=open(self._folder_ctrl_evol+"/"+File_Stats_Anal_Folders_And_Files.name_file_time_actuation_phase+str(i)+".txt","w")
			#file1.write( "%s\t %s \n"%("actuation time of  phase ",str(i)))
			#for j in di_nb_times_phase_act[i][1]:
				#file1.write( "%.2f \n"%(j))
								

			#for k in di_id_phase_value_nb_act_per_cycle:
				#file2=open(self._folder_ctrl_evol+"/"+File_Stats_Anal_Folders_And_Files.name_file_nb_actuation_per_cycle_phase+str(k)+".txt","w")
				#file2.write( "%s\t %s\t   %s \n"%("id cycle (1st colmn) actuation dyration per cycle of  phase (2nd column)  ","cycle duration",\
				#val_cycle_durat))
				
				#ind=0
				#for m in di_id_phase_value_nb_act_per_cycle[k]:
					#ind+=1
					#file2.write( "%d\t %.2f \n"%(ind,m))
	
			for j in di_rep[i]:
				file.write("%.2f\t %d\t %d\n"%(j[0],j[1],j[2]))
				
				
			#we write the file with the act duration and the nb departed veh per phase per cycle
			#for m in di_id_phase_value_li_actat_dur_and_nb_dep_veh_per_cycle:
				#file3=open(self._folder_ctrl_evol+"/"+File_Stats_Anal_Folders_And_Files.name_file_act_dur_and_veh_depart_per_cycle_per_phase+str(m)+".txt","w")
				#file3.write("%s\t \n"%("Phase Act duration per cycle (1st col), nb departed veh during cycle (2 col) "))
				#file3.write("%s\t %s\t \n"%("Phase",str(m)))
				#for n in di_id_phase_value_li_actat_dur_and_nb_dep_veh_per_cycle[m]:
					#file3.write("%.2f\t %.2f\t \n"%(n[0],n[1]))
				
			file.close()
			#file1.close()
			#file2.close()
			#file3.close()
			
#*****************************************************************************************************************************************************************************************
	#method calculating the number of actuation each phase per cycle
	#dict_ctrl_inf
	#key=id phase, value=[[...,[temps, crl value, type contrl (0 si RC, 1 sinon]), nb decisions without RC,total nb controls],...]]
	def fct_calcul_nb_actuation_per_cycle_each_phase1(self, val_dict_ctrl_inf,val_cycle_duration):
	
		di_rep={}
		#val_dict_ctrl_inf, key=id phase
		#value=[[...,[temps, crl value, type contrl (0 si RC, 1 sinon]), nb decisions without RC,total nb controls],...]]
		for i in  val_dict_ctrl_inf:
			di_rep[i]=[]
			
			t_fin_cycle_init=val_cycle_duration
			
			
			nb_ctrl=len( val_dict_ctrl_inf[i])
			
			nb_act_stage=0
			#print("i=",i)
			#print("val_dict_ctrl_inf[i]",val_dict_ctrl_inf[i])
			indice=0
			for j in val_dict_ctrl_inf[i]:
				indice+=1
				#if i[0]==1 and i[1]==2:
					#print("j",j,"nb_ctrl",nb_ctrl)
				#print("j=",j)
				#si le control est 1
				if j[1]==1:
				
					t_fin_cycle_correspondant_t_ctrl=\
					math.ceil(j[0]/val_cycle_duration)*val_cycle_duration
					
					#if i[0]==1 and i[1]==2:
						#print("t_fin_cycle_correspondant_t_ctrl",t_fin_cycle_correspondant_t_ctrl)
						
					#si on se  met a un nouveau cycle, on enregistre le nb d'actualisation et on commence nouvelle  enumerat
					if t_fin_cycle_correspondant_t_ctrl>t_fin_cycle_init:
						di_rep[i].append(nb_act_stage)
						#if i[0]==1 and i[1]==2:
							#print("HERE NEW CYC di_rep[i]",di_rep[i],"nb_act_stage",nb_act_stage)
							
						t_fin_cycle_init=t_fin_cycle_correspondant_t_ctrl
						nb_act_stage=1
					else:
						nb_act_stage+=1
					
			#si on est au dernier even du cycle courant, comme il n'y a pas de cycle proch on doit mettre le nb d'arrivees dans dict
			if indice==nb_ctrl-1:
				di_rep[i].append(nb_act_stage)
				#if i[0]==1 and i[1]==2:
					#print("j==nb_ctrl-1",indice,nb_ctrl-1)
					#print("di_rep[i]",di_rep[i])
			
		#print(di_rep[1,2])
		#import sys
		#sys.exit()	
		return di_rep
#*****************************************************************************************************************************************************************************************
	#method returning a dctionary, key= key=id phase, value=[ time actuat stage related per cycle, nb departed veh per cycle]...]
	def fct_calcul_act_duration_and_nb_depart_veh_per_cycle_per_phase(self,va_dict_nb_dep_veh_per_cycle_per_phase,\
	va_dict_act_durat_per_cycle_per_phase):
		
				
		#dict, key=id phase, value=[...,[act duration phase during ith cycle, nb deprt veh].,..]
		di_rep={}
			
		#va_dict_nb_dep_veh_per_cycle_per_phase=dict, key = id phase, value=[...,nb veh arrived at ith cycle,...]
		for i in va_dict_nb_dep_veh_per_cycle_per_phase:
			di_rep[i]=[]
			#va_dict_act_durat_per_cycle_per_phase= dict, key id phase, value=[...., act duration of phase at ith cycle]
			le=len(va_dict_nb_dep_veh_per_cycle_per_phase[i])
			for j in range(le):
				li=[va_dict_act_durat_per_cycle_per_phase[i][j], va_dict_nb_dep_veh_per_cycle_per_phase[i][j]]
				di_rep[i].append(li)
		return di_rep
				

#*****************************************************************************************************************************************************************************************
	#method returning a dctionary, key= key=id phase, value=[ id cycle, nb departed veh/phase total actuat duration during cycle ]...]
	def fct_calcul_nb_depart_veh_over_act_dur_per_cycle_per_phase(self,va_dict_nb_dep_veh_per_cycle_per_phase,\
	va_dict_act_durat_per_cycle_per_phase):
		
				
		#dict, key=id phase, value=[...,[act duration phase during ith cycle, nb deprt veh].,..]
		di_rep={}
			
		#va_dict_nb_dep_veh_per_cycle_per_phase=dict, key = id phase, value=[...,nb veh arrived at ith cycle,...]
		for i in va_dict_nb_dep_veh_per_cycle_per_phase:
			di_rep[i]=[]
			#va_dict_act_durat_per_cycle_per_phase= dict, key id phase, value=[...., act duration of phase at ith cycle]
			le=len(va_dict_nb_dep_veh_per_cycle_per_phase[i])
			for j in range(le):
				if len( va_dict_nb_dep_veh_per_cycle_per_phase[i])!=len(va_dict_act_durat_per_cycle_per_phase[i]):
					print("i=",i,"nb dep cycle",va_dict_nb_dep_veh_per_cycle_per_phase[i])
					print("i=",i,"nb dep veh /cycle",len(va_dict_nb_dep_veh_per_cycle_per_phase[i]))
					print("i=",i,"nb act dur cycle",len(va_dict_act_durat_per_cycle_per_phase[i]))
					print("PROBLEM IN CL STAT ANAL fct_calcul_nb_depart_veh_over_act_dur_per_cycle_per_phase,\
					NB CYCLES DIFFERENT FROM NB DEPARTURES PER CYCLE, PHASE", i)
					
					import sys
					sys.exit()
				if va_dict_nb_dep_veh_per_cycle_per_phase[i][j]>0 and va_dict_act_durat_per_cycle_per_phase[i][j]==0:
					print("PROBL IN CL STAT ANAL, fct_calcul_nb_depart_veh_over_act_dur_per_cycle_per_phase,\
					NB DEPARTED VEHI DURING CYCLE:",\
					va_dict_nb_dep_veh_per_cycle_per_phase[i][j],"ACT DURA OF PHASE DURING CYCLE",\
					va_dict_act_durat_per_cycle_per_phase[i][j],"phase",i,"cycle",j+1)
					import sys
					sys.exit()
				if va_dict_nb_dep_veh_per_cycle_per_phase[i][j]==0 and va_dict_act_durat_per_cycle_per_phase[i][j]==0:
					li=li=[j+1,0]
					
					di_rep[i].append(li)
				elif va_dict_nb_dep_veh_per_cycle_per_phase[i][j]>0 and va_dict_act_durat_per_cycle_per_phase[i][j]>0:
					li=[j+1, round(va_dict_nb_dep_veh_per_cycle_per_phase[i][j]/va_dict_act_durat_per_cycle_per_phase[i][j],2)]
					di_rep[i].append(li)
		#print("di_rep(1,2)",di_rep[1,2])
		return di_rep
				

#*****************************************************************************************************************************************************************************************
	#method calculating the duration of acuation of each phase per cycle
	#dict_ctrl_inf
	#key=id phase, value=[[...,[temps, crl value, type contrl (0 si RC, 1 sinon]), nb decisions without RC,total nb controls],...]]
	def fct_calcul_nb_actuation_per_cycle_each_phase(self, val_cycle_duration,val_t_end_sim):
	
		#dict, key=id phase, value=[[...,[temps, crl value, type contrl (0 si RC, 1 sinon]), nb decisions without RC,total nb controls],...]]
		val_dict_ctrl_inf=self.fct_creat_dict_ctrl_per_phase(dict_db_key_id_event_type_val_record_obj=\
		va_dict_db_key_id_event_type_val_record_obj)
	
		di_rep={}
		#val_dict_ctrl_inf, key=id phase
		#value=[[...,[temps, crl value, type contrl (0 si RC, 1 sinon]), nb decisions without RC,total nb controls],...]]
		#pour chaque phase
		for i in  val_dict_ctrl_inf:
			di_rep[i]=[]
			t_fin_cycle_init=val_cycle_duration
			indice=0
			total_dur=0
			
			le=len(val_dict_ctrl_inf[i])-1
			#if i[0]==1 and i[1]==2:
				#print("le",le)
			#pour chaque control de la phase
			for j in range(le):
				indice+=1
				
				t_fin_cycle_correspondant_t_ctrl=math.ceil(val_dict_ctrl_inf[i][j][0]/val_cycle_duration)*val_cycle_duration
				#if i[0]==1 and i[1]==2:
					#print("t_fin_cycle_correspondant_t_ctrl",t_fin_cycle_correspondant_t_ctrl)
				
				#si on se  met a un nouveau cycle, on enregistre le nb d'actualisation et on commence nouvelle  enumerat
				if t_fin_cycle_correspondant_t_ctrl>t_fin_cycle_init:
					#on met dans le dict l'actual deja calcule
					di_rep[i].append(round(total_dur,2))
					
					#si le control est un on mesure la duree
					if val_dict_ctrl_inf[i][j][1]==1:
						t_start=val_dict_ctrl_inf[i][j][0]
						t_fin=val_dict_ctrl_inf[i][j+1][0]
						total_dur=0
						dur=t_fin-t_start
						total_dur+=dur
						t_fin_cycle_init=t_fin_cycle_correspondant_t_ctrl
						j=j+1
						#if i[0]==1 and i[1]==2:
							#print("t_start",t_start,"t_fin",t_fin,"total_du",total_dur)
					
					#si le control est zero 
					else:
						total_dur=0
						t_fin_cycle_init=t_fin_cycle_correspondant_t_ctrl
				#si on ne se met pas a un nouveau cycle
				else:
					#si le control est un on mesure la duree
					if val_dict_ctrl_inf[i][j][1]==1:
						t_start=val_dict_ctrl_inf[i][j][0]
						t_fin=val_dict_ctrl_inf[i][j+1][0]
						dur=t_fin-t_start
						total_dur+=dur
						j=j+1
				#si on est au dernier even du cycle courant, comme il n'y a pas de cycle proch on doit mettre le temps dans le dcit
				if indice==le:
					#fin cycle dernier control
					t_fin_cycle_correspondant_t_ctrl=math.ceil(val_dict_ctrl_inf[i][j][0]/val_cycle_duration)*val_cycle_duration
					
					#si on commence un nouveau cycle
					if t_fin_cycle_correspondant_t_ctrl>t_fin_cycle_init:
						#on met dans le dict la valeur prec caclulee
						di_rep[i].append(round(total_dur,2))
						
						#si le control est un on mesure la duree
						if val_dict_ctrl_inf[i][j][1]==1:
							t_start=val_dict_ctrl_inf[i][j][0]
							t_fin=val_t_end_sim 
							dur=t_fin-t_start
							total_dur=0
							total_dur+=dur
							di_rep[i].append(round(total_dur,2))
						else:
							di_rep[i].append(0)
							
					#si on reste sur le meme cycle
					else:
						#si le control est un on mesure la duree
						if val_dict_ctrl_inf[i][j][1]==1:
							t_start=val_dict_ctrl_inf[i][j][0]
							t_fin=val_t_end_sim 
							dur=t_fin-t_start
							total_dur+=dur
							di_rep[i].append(round(total_dur,2))
						#si le control n'est pas un
						else:
							di_rep[i].append(round(total_dur,2))
						
		#print(di_rep[14,15])
		#import sys
		#sys.exit()	
		return di_rep					

#*****************************************************************************************************************************************************************************************
	
	#method write files with the ctrl evolution, WITHOUT TOTAL PHASE ACTUAT DURATION
	def fct_write_files_ctrl_evolution_1(self,va_dict_db_key_id_event_type_val_record_obj):
	
		#dict, key=id phase, value=[[...,[temps, crl value, type contrl (0 si RC, 1 sinon]), nb decisions without RC,total nb controls],...]]
		di_rep=self.fct_creat_dict_ctrl_per_phase(dict_db_key_id_event_type_val_record_obj=va_dict_db_key_id_event_type_val_record_obj)
		
				
		#dict, key=id phase, value=[nb times actuated,[.., time ith actuation,..]]
		di_nb_times_phase_act=self.fct_creat_dict_nb_times_actuat_phase(dict_key_id_phase_val_lis_time_and_ctrl_value=di_rep)
		
		#dict, key=id phase, value=nb control changes no RC incuded
		di_ctrl_changes_per_phase=self.fct_calcul_nb_ctrl_changes_no_rc( di_key_id_phase_value_temps_and_ctrl_value_and_type_ctrl=di_rep)
		
		#dict, key=id phase, value=nb_controls
		
		for i in di_rep:
			
			#si on a maj le control de la phase
			if i in di_nb_times_phase_act:
				file=open(self._folder_ctrl_evol+"/"+File_Stats_Anal_Folders_And_Files.name_file_ctrl_evolution_phase+str(i)+".txt","w")
				file.write("%s %s %s  %s %s  %d  %s %s %s \n"%("PHASE", str(i),", NB TIMES ACTUATED", di_nb_times_phase_act[i][0],\
				", NB CTRL CHANGES REGARDING THE FIRST VALUE NO RC",di_ctrl_changes_per_phase[i],\
				", TOTAL NB CTRLS DURING SIM NO RC, ", di_rep[i][len(di_rep[i])-1][3],\
				", time, ctrl value, ctrl type 0: RC 1: otherwise, (1,2,3, clmns) "))
				file1=open(self._folder_ctrl_evol+"/"+File_Stats_Anal_Folders_And_Files.name_file_time_actuation_phase+str(i)+".txt","w")
				file1.write( "%s\t %s \n"%("actuation time of  phase ",str(i)))
				for j in di_nb_times_phase_act[i][1]:
					file1.write( "%.2f \n"%(j))
			
			#si on n'a pas maj le ctrl de la phase
			else:
				file=open(self._folder_ctrl_evol+"/"+File_Stats_Anal_Folders_And_Files.name_file_ctrl_evolution_phase+str(i)+".txt","w")
				file.write("%s\t %s\t %s\t %s\t %s \n"%("PHASE", str(i),"NB TIMES	ACTUATED",0,",time, ctrl value, ctrl type (1,2,3 clmns) "))
				
			for j in di_rep[i]:
				file.write("%.2f\t %d\t %d\n"%(j[0],j[1],j[2]))
			file.close()
			file1.close()
			
#*****************************************************************************************************************************************************************************************
	#method write the files with the  evolution of each internal link
	def fct_write_files_entry_internal_link_evol(self,va_netw,va_dict_db_key_id_event_type_val_record_obj):
	
		#dict, key=id link, value=[...,[t,nb veh in link],...]
		di_rep=self.fct_creat_dict_current_nb_veh_in_link(\
		v_netw=va_netw,\
		dict_db_key_id_event_type_val_record_obj=va_dict_db_key_id_event_type_val_record_obj)
		
		for i in di_rep:
			file=open(self._folder_link_evol+"/"+File_Stats_Anal_Folders_And_Files.name_file_evolution_lk+str(i)+".txt","w")
			cap=va_netw.get_di_entry_internal_links()[i].get_capacity_link()
			#if the link is an entry link
			if i  in va_netw.get_di_entry_links_to_network():
				file.write("%s\t %s \n"%("LINK", str(i)))
				##if the link is not an entry link
			else:
				file.write("%s\t %s\t %s\t %s \n"%("LINK", str(i),"CAPACITÉ",cap))
			for j in di_rep[i]:
				if j[1]<0:
					print("PROBLEM IN CL_STAT ANAL fct_write_files_entry_internal_link_evol i=",i,j)
					import sys
					sys.exit()
				file.write("%.2f\t %d\n"%(j[0],j[1]))
			file.close()
		
#*****************************************************************************************************************************************************************************************
	#method writing a file with the sum of all queues during sim
	def fct_write_file_sum_que_t_sim(self):
		
		#list with  [.., [t, sum of queues],...]
		li=self.fct_calcul_sum_que_t_sim(val_path_list_files=self._folder_que_evol_files)
		
		file=open(self._file_sum_queue_evol+".txt","w")
		for i in li:
			#file.write("%d\t %d \n"%(i[0],i[1]))
			file.write("%.1f\t %d \n"%(i[0],i[1]))
			
		return li

#***************************************************************************************************************************************************************************************** 

	#method writing a file with the sum of all queues during sim
	def fct_write_file_average_sum_que_t_sim(self,val_total_nb_network_ques):
		
		#list with  [.., [t, sum of queues],...]
		li=self.fct_calcul_average_sum_que_t_sim(val_path_list_files=self._folder_que_evol_files,val_total_nb_network_queues=val_total_nb_network_ques)
		
		file=open(self._file_average_sum_queue_evol+".txt","w")
		for i in li:
			#file.write("%d\t %d \n"%(i[0],i[1]))
			file.write("%.1f\t %2f \n"%(i[0],i[1]))
			


#***************************************************************************************************************************************************************************************** 

	#function creating a file for each queue and writing the time, the number of vehicles in the queue, 
	#and the mean value of each phase
	def fct_writing_file_time_veh_queue_length(self,val_netwk,di_db_file):
		
		#we create a dictionary from the db file created by the sim
		#key=movement [l,m]
		#value=dict, key=time, value=  [ [nb of vehicles in the queue,ev type,id veh     ]   ]
		di_movem=self.fct_creat_dict_queue_lengths_during_sim(val_network=val_netwk,dict_db_file=di_db_file)
		
		#print(di_movem[12,8])
		
		#print("HERE",di_movem.keys())
		
		#we create a dictionary with the mean queue length of each movement (nb of veh/sec)
		#key=movement [l,m], value=average number of veh/sec
		#di_mean_que_length_mov={}
		#for k in di_movem:
			
			#som=0
			
			#for m in  di_movem[k]:
				#print()
				#print(di_movem[k][m][len(di_movem[k][m])-1][0])
				#som+=di_movem[k][m][len(di_movem[k][m])-1][0]
			#di_mean_que_length_mov[k]=som/len(di_movem[k])
			#print(di_mean_que_length_mov)
			
		
		#for each movement we create a file
		ind=1
		for i in di_movem:
			
			file=open(self._file_to_write_que_res+str(ind)+".txt","w")
			file.write("%s\t %s \n"%("QUE", str(i)))
			li_keys=[]
			for j  in di_movem[i].keys():
				li_keys.append(j)
			#print(li_keys)
			li_keys.sort()
			for k in li_keys:
				for m in di_movem[i][k]:
					#file.write("%d\t %d\t %d\n"%(k,m[0],m[1]))
					file.write("%.1f\t %d\t %d\n"%(k,m[0],m[1]))
			ind+=1
			file.close()
			
		
		
		#file1=open(self._file_mean_queue_length+".txt","w")
		#file1.write("%s\t %s \n"%("QUE", "MEAN LENGTH"))	
		#for j in di_mean_que_length_mov:
			#file1.write("%d\t %d\t %f\n"%(j[0],j[1],di_mean_que_length_mov[j]))
		#file1.close()
			
			
#***************************************************************************************************************************************************************************************** 

	#function creating a file for each queue and writing the time, the number of vehicles in the queue, 
	#and the mean value of each phase
	#it returns a dictionary; keu=mov, value=sorted list regard. time [time, que length, nb veh in que]
	def fct_writing_file_time_veh_queue_length_and_aver_que_length_1(self,val_netwk,di_db_file):
		
		#we create a dictionary from the db file created by the sim
		#key=movement [l,m]
		#value=dict, key=time, value=  [ [nb of vehicles in the queue,ev type,veh id     ]   ]
		di_movem=self.fct_creat_dict_queue_lengths_during_sim(val_network=val_netwk,dict_db_file=di_db_file)
		
		#print("HERE1",di_movem)
		
		
				
		di_key_mov_val_sorted_li_t_que_length={}
		
		#for each movement we create a file
		ind=1
		for i in di_movem:
			
			#list [ ...,[t, que length at t],...]
			li_li_t_que_len=[]
			
			file=open(self._file_to_write_que_res+str(ind)+".txt","w")
			file.write("%s\t %s \n"%("QUE", str(i)))
			li_keys=[]
			for j  in di_movem[i].keys():
				li_keys.append(j)
			#print(li_keys)
			li_keys.sort()
			nb_veh_que_prev_t=0
			nb_dep_veh=0
			for k in li_keys:
				for m in di_movem[i][k]:
					li_li_t_que_len.append([k,m[0]])
					#file.write("%d\t %d\t %d\n"%(k,m[0],m[1]))
					file.write("%.1f\t %d\t %d\n"%(k,m[0],m[1]))
					
					if m[1]==Cl_Event.TYPE_EV["type_ev_end_veh_departure_from_que"]:
						nb_dep_veh+=nb_veh_que_prev_t-m[0]
											
					nb_veh_que_prev_t=m[0]
					
			
			#print("i=",i,"nb_dep_veh",nb_dep_veh,m[0])			
			nb_dep_veh+=m[0]
					
			di_key_mov_val_sorted_li_t_que_length[i]=[li_li_t_que_len,nb_dep_veh]
			
			ind+=1
			file.close()
		#ind=1
		#for i in di_movem:
			#f=open(self._file_to_write_que_res_1+str(ind)+".txt","w")
			#f.write("%s\t %s \n"%("QUE", str(i)))
			#f.write("%s\t %s\t %s\t %s \n"%("TIME(1)", "QUE LEN (2)", "EVENT TYPE (3)","VEH ID(4)"))
			#f.write("%d\t %d \n"%(i[0],i[1]))
			#li_keys=[]
			#for j  in di_movem[i].keys():
				#li_keys.append(j)
			#print(li_keys)
			#li_keys.sort()
			#for k in li_keys:
				#for m in di_movem[i][k]:
					#f.write("%d\t %d\t %d\t %d \n"%(k,m[0],m[1],m[2]))
					#f.write("%.1f\t %d\t %d\t %d \n"%(k,m[0],m[1],m[2]))
			#ind+=1
			#f.close()
		#print("HERE2",di_key_mov_val_sorted_li_t_que_length)
		
		return di_key_mov_val_sorted_li_t_que_length 
		#file1=open(self._file_mean_queue_length+".txt","w")
		#file1.write("%s\t %s \n"%("QUE", "MEAN LENGTH"))	
		#for j in di_mean_que_length_mov:
			#file1.write("%d\t %d\t %f\n"%(j[0],j[1],di_mean_que_length_mov[j]))
		#file1.close()
			
			
#***************************************************************************************************************************************************************************************** 
	#function creating a file for each queue and writing the time, the number of vehicles in the queue, 
	#and the mean value of each phase
	#it returns a dictionary; keu=mov, value=sorted list regard. time [time, que length, nb veh in que]
	def fct_writing_file_time_veh_queue_length_and_aver_que_length(self,val_netwk,di_db_file):
		
		#we create a dictionary from the db file created by the sim
		#key=movement [l,m]
		#value=dict, key=time, value=  [ [nb of vehicles in the queue,ev type,veh id     ]   ]
		di_movem=self.fct_creat_dict_queue_lengths_during_sim(val_network=val_netwk,dict_db_file=di_db_file)
		
		#print("HERE1",di_movem)
		
		
				
		di_key_mov_val_sorted_li_t_que_length={}
		
		#for each movement we create a file
		ind=1
		for i in di_movem:
			
			#list [ ...,[t, que length at t],...]
			li_li_t_que_len=[]
			
			#file=open(self._file_to_write_que_res+str(ind)+".txt","w")
			file=open(self._file_to_write_que_res+str(i)+".txt","w")
			file.write("%s\t %s \n"%("QUE", str(i)))
			li_keys=[]
			for j  in di_movem[i].keys():
				li_keys.append(j)
			#print(li_keys)
			li_keys.sort()
			nb_veh_que_prev_t=0
			nb_dep_veh=0
			for k in li_keys:
				for m in di_movem[i][k]:
					li_li_t_que_len.append([k,m[0]])
					#file.write("%d\t %d\t %d\n"%(k,m[0],m[1]))
					file.write("%.1f\t %d\t %d\n"%(k,m[0],m[1]))
					
					if m[1]==Cl_Event.TYPE_EV["type_ev_end_veh_departure_from_que"] or \
					m[1]==Cl_Event.TYPE_EV["type_ev_end_veh_departure_from_que_nsi"]:
						nb_dep_veh+=nb_veh_que_prev_t-m[0]
											
					nb_veh_que_prev_t=m[0]
					
			
			#print("i=",i,"nb_dep_veh",nb_dep_veh,m[0])			
			nb_dep_veh+=m[0]
					
			di_key_mov_val_sorted_li_t_que_length[i]=[li_li_t_que_len,nb_dep_veh]
			
			ind+=1
			file.close()
		ind=1
		for i in di_movem:
			f=open(self._file_to_write_que_res_1+str(ind)+".txt","w")
			f.write("%s\t %s \n"%("QUE", str(i)))
			f.write("%s\t %s\t %s\t %s \n"%("TIME(1)", "QUE LEN (2)", "EVENT TYPE (3)","VEH ID(4)"))
			f.write("%d\t %d \n"%(i[0],i[1]))
			li_keys=[]
			for j  in di_movem[i].keys():
				li_keys.append(j)
			#print(li_keys)
			li_keys.sort()
			for k in li_keys:
				for m in di_movem[i][k]:
					#f.write("%d\t %d\t %d\t %d \n"%(k,m[0],m[1],m[2]))
					f.write("%.1f\t %d\t %d\t %d \n"%(k,m[0],m[1],m[2]))
			ind+=1
			f.close()
		#print("HERE2",di_key_mov_val_sorted_li_t_que_length)
		
		return di_key_mov_val_sorted_li_t_que_length 
		#file1=open(self._file_mean_queue_length+".txt","w")
		#file1.write("%s\t %s \n"%("QUE", "MEAN LENGTH"))	
		#for j in di_mean_que_length_mov:
			#file1.write("%d\t %d\t %f\n"%(j[0],j[1],di_mean_que_length_mov[j]))
		#file1.close()
			
			
#***************************************************************************************************************************************************************************************** 

	#function creating a file for each queue and writing the time, the number of vehicles in the queue, 
	#after the veh arrival/appearance events
	def fct_writing_file_time_veh_arrival_appear_queue_length(self,di_movem):
	
		#we create a dictionary from the db file created by the sim
		#key =movement, value=dict with key=the time, value=[nb of veh in the queue, ev type]
		#di_movem=self.fct_creat_dict_queue_veh_arrivals_ap_during_sim(val_network=val_netw,dict_db_file=di_db_file)
		
		#for each movement we create a file
		ind=1
		for i in di_movem:
			file=open(self._file_to_write_nb_veh_que_ar_ap+str(ind)+".txt","w")
			file.write("%s\t %s \n"%("QUE", str(i)))
			li_keys=[]
			for j in di_movem[i]:
				li_keys.append(j)
			li_keys.sort()
			for k in li_keys:
				for m in di_movem[i][k]:
					#print("HERE",j,di_movem[i])
					#file.write("%d\t  %d\t %d\n"%(k,m[0],m[1]))
					file.write("%.1f\t  %d\t %d\n"%(k,m[0],m[1]))
			ind+=1
			file.close()
#***************************************************************************************************************************************************************************************** 

	#function writing a file for each queue
	#each line corresponds to the number of vehicles in a queue, and the number of times that we had that number
	def fct_writing_file_nb_veh_queue_ar_ap_nb_of_times(self,di_movem):
		#dict, key=movement, value=dict, key=time, value= [..., [nb veh in queue during arriv/appear events,event type],...)
		#di_movem=self.fct_creat_dict_queue_veh_arrivals_ap_during_sim(val_network=val_netwk,dict_db_file=di_db_file)
		ind=1
		for i in di_movem:
			
			li_1=[]
			for k in di_movem[i]:
				for m in di_movem[i][k]:
					#print(di[i][k],"m",m[0])
					li_1.append(m[0])
				
			
			dict_1=self.fct_creat_dict_nb_occurences_elem_list(li=li_1)
			#print(di_1)
			di_1=self.fct_creat_dict_with_perc_val(val_dict=dict_1)
			file=open(self._file_nb_times_with_nb_veh_at_que_ar_ap+str(ind)+".txt","w")
			file.write("%s\t %s \n"%("QUE", str(i)))
			for j in di_1:
				#file.write("%d\t %d\t  %d%s\n"%(j,di_1[j][0],di_1[j][1],"%"))
				file.write("%.1f\t %d\t  %d%s\n"%(j,di_1[j][0],di_1[j][1],"%"))
			file.close()
			ind+=1
#***************************************************************************************************************************************************************************************** 

	#method writing for each queue: 
	#the number of vehicles in the queue, after the veh arrival/appearance events (each line of the file)
	#the number of vehicles in a queue, and the number of times that we had that number (each line of the file)
	#nb of files produces= nb of queues x 2
	def fct_writing_file_nb_veh_que_nb_t_veh_ar_ap_que_length(self,val_netwk,di_db_file):
	
		dict_movem=self.fct_creat_dict_queue_veh_arrivals_ap_during_sim(val_network=val_netwk,dict_db_file=di_db_file)
		
		self.fct_writing_file_nb_veh_queue_ar_ap_nb_of_times(di_movem=dict_movem)
		self.fct_writing_file_time_veh_arrival_appear_queue_length(di_movem=dict_movem)
		

#***************************************************************************************************************************************************************************************** 

	#function creating a file for each queue and writing the time, and the number of departing  vehicles, 
	def fct_writing_file_time_veh_departure_nb_dep_veh1(self,di_mov):
		
		#we create a dictionary from the db file created by the sim
		#di_mov=self.fct_creat_dict_queue_veh_depart_during_sim(dict_db_file=di_db_file)
		
		#for each movement we create a file
		ind=1
		for i in di_mov:

			#print("HERE",os.getcwd())
			file=open(self._file_nb_veh_dep_que+str(ind)+".txt","w")
			file.write("%s\t %s \n"%("QUE", str(i)))
			li_keys=[]
			for j in di_mov[i]:
				li_keys.append(j)
			li_keys.sort()
			#print(j)
			#print(di[i])
			for k in li_keys:
				for m in di_mov[i][k]:
					#file.write("%d\t  %d\n"%(k,m[0]))
					file.write("%.1f\t  %d\n"%(k,m[0]))
			ind+=1
			file.close()

#***************************************************************************************************************************************************************************************** 

	#function writing a file for each queue
	#each line corresponds to the number of vehicles departing from the  queue, and the number of times that we had that number
	def fct_writing_file_nb_veh_queue_dep_nb_of_times(self,di_mov):
		#dict_mov, key=movement, value=dict, key=time, value= [...,  [nb of dep veh, ev type  ] ,...)
		#print("HERE",di_mov)
		ind=1
		#for each queue
		for i in di_mov:
			#print("HERE",di[i])
			#print(i)
			li_1=[]
			#for each nb of dep veh, ev type  ]
			for k in di_mov[i]:
				#we add the nb of dep vehicles
				for m in di_mov[i][k]:
					#print(di[i][k],"m",m[0])
					li_1.append(m[0])
			
			#print(li_1)
			dict_1=self.fct_creat_dict_nb_occurences_elem_list(li=li_1)
			#print(di_1)
			di_1=self.fct_creat_dict_with_perc_val(val_dict=dict_1)
			
			file=open(self._file_nb_times_with_nb_dep_veh_from_que+str(ind)+".txt","w")
			file.write("%s\t %s \n"%("QUE", str(i)))
			for j in di_1:
				#file.write("%d\t %d\t  %.2f%s\n"%(j,di_1[j][0],di_1[j][1],"%"))
				file.write("%.1f\t %d\t  %.2f%s\n"%(j,di_1[j][0],di_1[j][1],"%"))
			file.close()
			ind+=1


#***************************************************************************************************************************************************************************************** 

	#method writing for each queue:
	#a file of which each line corresponds to the number of vehicles departing from the  queue, and the number of times that we had that number
	#a file of which each line is the time, and the number of departing  vehicles
	def fct_writing_file_nb_dep_veh_nb_times(self,val_netwk,di_db_file):
	
		dict_mov=self.fct_creat_dict_queue_veh_depart_during_sim(val_network=val_netwk,dict_db_file=di_db_file)
		
		#print(dict_mov[1,2])
		#print()
		#print(dict_mov[6,7])
		
		self.fct_writing_file_nb_veh_queue_dep_nb_of_times(di_mov=dict_mov)
		#self.fct_writing_file_time_veh_departure_nb_dep_veh(di_mov=dict_mov)
		

#***************************************************************************************************************************************************************************************** 
	def fct_writing_file_time_veh_queue_length_after_veh_dep(self,val_netwk,di_db_file):
	
		di_movem=self.fct_creat_dict_queue_evol_after_veh_depart_during_sim(val_network=val_netwk,dict_db_file=di_db_file)
		
		#for each movement we create a file
		ind=1
		for i in di_movem:
			
			file=open(self._file_queue_evol_after_veh_dep+str(ind)+".txt","w")
			file.write("%s\t %s \n"%("QUE", str(i)))
			li_keys=[]
			for j  in di_movem[i].keys():
				li_keys.append(j)
			li_keys.sort()
			for k in li_keys:
				for m in di_movem[i][k]:
					#file.write("%d\t %d\t %d\n"%(k,m[0],m[1]))
					file.write("%.1f\t %d\t %d\n"%(k,m[0],m[1]))
			ind+=1
			file.close()

#***************************************************************************************************************************************************************************************** 

	#function writing  a file with the mean travel time of each entry-exit link , (no turn movements are included) and the number of vehicles served
	#id entry link, id exit, link, mean travel time, nb veh served
	def fct_writing_file_mean_travel_time_entry_exit_lk_nb_veh_served(self,val_di_info_entry_exit_lk):
		
		#we create the dictionary; key=(entry,exit link), value=[mean travel time, nb veh served]
		di=self.fct_creat_dict_mean_travel_time_entry_exit_link(di_info_entry_exit_lk=val_di_info_entry_exit_lk)
		
		file=open(self._file_name_folder_mean_travel_time_entry_exit_lk,"w")
		
		file.write("%s\t %s\t  %s\t %s \n"%("ID ENTRY LK","ID EXIT LK","MEAN TR T","NB VEH SERVED"))
		for i in di:
			#print(i[0],di[i][0])
			#for j in di[i]:
				#file.write("%s\t %s\t %d\t %d \n"%(i[0],i[1],j[0],j[1]))
			file.write("%s\t %s\t %.1f\t %d \n"%(i[0],i[1],di[i][0],di[i][1]))
		
		file.close()
#*****************************************************************************************************************************************************************************************
	#method writing in a file, the number of vehicles (of the sum of queues) and the probability of having this number
	def fct_writing_prob_of_nb_veh_at_queue(self, val_li_t_que_len,val_durat_sim):
	
		#di=dict, key=nb_of_veh value=[ prob, time with this number of veh]
		di=self.fct_calc_prob_of_nb_veh_at_queue_and_duration(li_t_que_len=val_li_t_que_len,dur_sim=val_durat_sim)
		file=open(self._file_name_file_nb_veh_prob_sum_que,"w")
		file.write("%s\t %s\t  \n"%("NB OF VEH SUM_QUE","PROB"))
		for i in di:
			file.write("%d\t %f\n"%(i,di[i][0]))
			
		file.close()
		
		return di
	
#*****************************************************************************************************************************************************************************************
	#method writing a file with the weighted mean of the sum of queues withing a simulation
	def fct_writing_file_weighted_mean_sd_sum_que(self,val_dict_nb_veh_que_and_durat,val_durat_sim):
		
		#we open the file where the sum of queues is written during a sim
		#we read the file and do not use the appropriate dict in case we do not want do both calculations (sum of queues, mean and var) 
		#within the same stat anal
		#in case this analysis will be done in every run this part has to be added when calculate the sum of queues
		
		
			
		
		li_w_mean_sd=self.fct_calc_weighted_mean_sd_sum_que(dict_nb_veh_que_and_dur=val_dict_nb_veh_que_and_durat,\
		dur_sim=val_durat_sim)
		
		file=open(self._file_mean_length_sum_queues,"w")
		file.write("%s\t %s\t %s\t %s\t\n"%("WEIGHTED MEAN (1)", "STAND DEVIATION (2)", "WM-SD(3)" ,"WM+SD(4)"))
		
		file.write("%.2f\t %.2f\t %.2f\t %.2f\t\n"%(li_w_mean_sd[0],li_w_mean_sd[1],li_w_mean_sd[2],li_w_mean_sd[3]))
		file.close()
		

#*****************************************************************************************************************************************************************************************
	#function writing a file for each queue with :
	# --- the time and the number of vehicles in the queue, type of the event
	#--- the time, the number of vehicles in the queue, after the veh arrival/appearance events, event type
	#--- the time, the number of departing vehicles in the queue, after each veh departure events
	#---  the number of vehicles in a queue, and the number of times that we had that number
	def fct_writing_files_sa(self,val_netw,val_dur_sim,val_cycle_dur,val_t_end_sim,val_finite_lk_cap,val_t_period,\
	val_veh_final_dest_dynam_construct,val_name_Fres_folder,\
	val_t_unit,val_t_init,va_li_phrases=["1st line=(id entry lk,  id exit link),other lines:  < time value (1st column), mean travel time, total nb veh  (2nd column) "],\
	val_li_phrases_mean_trav_dist=["1st line=(id entry lk,  id exit link),other lines:  t_start, t_end period (1st, 2nd column), mean traveled distance, total nb veh  (3rd column) "]):
	
		#we create a  result sim treatment object
		treat_sim_obj=Cl_Treatment_Sim_Res.Treatment_Sim_Res(val_db_file_sim_res_to_treat=self._db_file)
		
		#dict, key=mov, value = [...,record obj,...]
		dict_db_file=treat_sim_obj.fct_creation_dictionary_key_movem_from_the_db_file()
		
		
		#dict, key=id event type, value=[..,record obj,...]
		#ATTENTION CE DICT EST AUSSI CALCULE (POUR UEN 2EME FOIS)  LORS CALCUL MEAN TRAVEL TIME, A CORRIGER 
		dict_db_file_1=treat_sim_obj.fct_creation_dictionary_from_the_db_file()
		
	
	
		 
		#di_ctrl_evol=self.fct_creat_di_evolution_stage_actuation(val_dict_ev_type= dict_db_file_1)
		#print(di_ctrl_evol)
		#print()
		#print(di_ctrl_evol.keys())
		#print()
		#print(di_ctrl_evol[1])
		#import sys
		#sys.exit()
		
		
		
		#we write the fiels with the evolution of each stage for each intersection
		#DECself.fct_write_files_control_evolution_per_intersection(val_dic_ev_type=dict_db_file_1,val_time_unit=val_t_unit,val_li_phrases=["t_start stage act. duration (1st colm) t_end stage act. duration (2nd colm"])
		#import sys
		#sys.exit()
		
		
		#we write the file with the number of stage switches per itnersection
		#DECself.fct_write_file_nb_stage_switches_per_inters(val_dic_ev_type=dict_db_file_1,val_li_phrases=["id node (1st colm), nb stage switches (2nd colm)"])
		
		
		
		#dec self.fct_write_mean_traveled_distance_per_period(\
		#dec va_veh_final_dest_dynam_construct=val_veh_final_dest_dynam_construct,\
		#dec va_name_Fres_folder=val_name_Fres_folder,\
		#dec va_sim_dur=val_dur_sim,va_t_period=val_t_period,va_t_unit=val_t_unit,\
		#dec va_t_init=val_t_init,\
		#dec va_di_internal_lk_info=val_netw.get_di_internal_links_to_network(),\
		#dec lis_phrases=val_li_phrases_mean_trav_dist)
		
		
		
		#dec val_dict_info_entry_exit_lk=self.fct_creat_dict_exit_link_info()
		
		#write the file with the average travel time per period
		#dec self.fct_calcul_and_write_travel_time_per_time_period_entry_exit_lk(\
		#dec va_sim_dur=val_dur_sim,va_t_period=val_t_period,va_t_unit=val_t_unit,va_round_prec=2,va_lis_phrases=va_li_phrases,\
		#dec va_t_init=val_t_init,val_di_info_entry_exit_lk=val_dict_info_entry_exit_lk)
		
		#the file with the mean travel time between entry-exit link
		#dec self.fct_writing_file_mean_travel_time_entry_exit_lk_nb_veh_served(val_di_info_entry_exit_lk=val_dict_info_entry_exit_lk)
		
		#dict, key=id phase, value=[...,nb veh arrived at ith cycle,...]
		#di_key_id_phase_value_nb_veh_ar_ap_per_cycle=self.fct_creat_dict_veh_arrival_at_phase_per_cycle(\
		#val_network=val_netw,val_dict_db_file=dict_db_file,val_cycle_duration=val_cycle_dur)
		
		#dictionary, key=id phase, value=[...,nb veh arrived at ith cycle,...]
		#di_key_id_phase_value_nb_veh_dep_per_cycle=self.fct_creat_dict_veh_depart_from_phase_per_cycle(\
		#val_network=val_netw,val_dict_db_file=dict_db_file,val_cycle_duration=val_cycle_dur)
		
		#dict, key=id phase, value=[...., nb_dep-nb_ar at ith cycle,...]
		#di_key_id_phase_value_dif_dep_minus_ar=self.fct_creat_dict_differ_depart_minus_ar(\
		#val_di_key_id_phase_val_ar_ap_per_cycle=di_key_id_phase_value_nb_veh_ar_ap_per_cycle,\
		#val_di_key_id_phase_val_dep_per_cycle=di_key_id_phase_value_nb_veh_dep_per_cycle)
		
		#files with the veh arrival and depart/cycle for each phase
		#self.fct_write_files_nb_veh_arrivals_and_departures_per_cycle(\
		#val_di_veh_ap_ar_per_cycle=di_key_id_phase_value_nb_veh_ar_ap_per_cycle,\
		#val_di_veh_dep_per_cycle=di_key_id_phase_value_nb_veh_dep_per_cycle,\
		#val_cycle_durat=val_cycle_dur)
		
		
		#files with the control of each phase
		#self.fct_write_files_ctrl_evolution(va_dict_db_key_id_event_type_val_record_obj=dict_db_file_1)
		
		#files with the actuation duration of  each phase
		#dec di_phase_act_dur_per_period=self.fct_creat_dict_phase_actuat(dict_db_key_id_event_type_val_record_obj=dict_db_file_1,\
		#dec v_sim_dur=val_dur_sim,\
		#dec v_t_period=val_t_period,\
		#dec v_t_unit=val_t_unit,v_t_init=val_t_init)
		
		#dec self.fct_write_file_total_actutation_duration_per_period_each_phase(name_file_to_write=self._folder_phase_act_durat_per_period+"/"+\
		#dec File_Stats_Anal_Folders_And_Files.name_file_total_act_duration_per_period_phase,\
		#dec dict_phase_act_dur_info=di_phase_act_dur_per_period,lis_phrases=["t start period (1st colm), t end period (2nd colm), total actuat duration (3rd colm)"])
		
		
		#if we have finite link capacity we present the link evolution
		#if val_finite_lk_cap==1:
		#files with the length of each link
		#dec self.fct_write_files_entry_internal_link_evol(va_netw=val_netw,va_dict_db_key_id_event_type_val_record_obj=dict_db_file_1)
		
		
		#files with lengths of each queue during sim
		#self.fct_writing_file_time_veh_queue_length(val_netwk=val_netw,di_db_file=dict_db_file)
		#di_1=dict, key=movem, value=[ ...[[time,que length],total number of veh arrived in que]...]
		di_1=self.fct_writing_file_time_veh_queue_length_and_aver_que_length(val_netwk=val_netw,di_db_file=dict_db_file)
		
		#print(di_1.keys())
		#print()
		
		#print(len(di_1.keys()))
		
		
	
	
		#file with the sum of queues during sim
		#li=[..,[t,length of sum of queues],..]
		li=self.fct_write_file_sum_que_t_sim()
		import sys
		sys.exit()
		
		#we write the file with the average value of the sum of the queues during the sim
		self.fct_write_file_average_sum_que_t_sim(val_total_nb_network_ques=len(di_1))
		import sys
		sys.exit()
		
		#file with the number pf departing veh and the percentage of times we have this number
		#self.fct_writing_file_nb_dep_veh_nb_times(val_netwk=val_netw,di_db_file=dict_db_file)
		
		
	
		
		#the file with the number of veh in the sum of queues and the prob of having that number
		#di=dict, key=nb_of_veh value=[ prob, time with this number of veh]
		#dec di=self.fct_writing_prob_of_nb_veh_at_queue(val_li_t_que_len=li,val_durat_sim=val_dur_sim)
		
		
		
		#the file with the weighted mean and the stand deviation of the sum of queues
		#self.fct_writing_file_weighted_mean_sd_sum_que(val_dict_nb_veh_que_and_durat=di,val_durat_sim=val_dur_sim)
		
		#the file with the stte of the queue after the eeh departure
		#self.fct_writing_file_time_veh_queue_length_after_veh_dep(val_netwk=val_netw,di_db_file=dict_db_file)
		
		#the file with the mean value of each queue
		#self.fct_calcul_average_time_spent_by_veh_in_a_que_for_each_que_2(\
		#di_key_mov_val_sorted_li_t_que_length=di_1,val_durat_sim=val_dur_sim)
		#self.fct_writing_file_average_time_spent_by_veh_in_a_que_for_each_que_1(dict_key_movement_value_record_obj=dict_db_file)
		#dec self.fct_writing_file_average_time_spent_by_veh_in_a_que_for_each_que(\
		#dec di_key_movem_val_sorted_li_t_que_length=di_1,\
		#dec val_duration_sim=val_dur_sim)
		
		#we create the dict
		
		#**********ICI
		
				
		#self.NOfct_writing_file_nb_veh_que_nb_t_veh_ar_ap_que_length(val_netwk=val_netw,di_db_file=dict_db_file)
		#self.fct_writing_file_nb_veh_que_dep_nb_of_t_and_t_veh_departure_nb_dep_veh(val_netwk=val_netw,di_db_file=dict_db_file)
		#self.fct_writing_file_time_veh_queue_length_after_veh_dep(val_netwk=val_netw,di_db_file=dict_db_file)
		#self.fct_writing_file_mean_travel_time_entry_exit_lk_nb_veh_served(val_net=val_netw)
		#self.fct_writing_file_sum_queus_during_sim()
		#li=self.fct_calc_weight_mean_sd_sum_que(1800)
		#li=self.fct_calc_weight_mean_sd_prob_que_val_sum_que(1800)
		#return li
		
#*****************************************************************************************************************************************************************************************
	#function writing a file for each queue with :
	# --- the time and the number of vehicles in the queue, type of the event
	#--- the time, the number of vehicles in the queue, after the veh arrival/appearance events, event type
	#--- the time, the number of departing vehicles in the queue, after each veh departure events
	#---  the number of vehicles in a queue, and the number of times that we had that number
	def fct_writing_files_sa_complete(self,val_netw,val_dur_sim,val_cycle_dur,val_t_end_sim,val_finite_lk_cap,val_t_period,\
	val_veh_final_dest_dynam_construct,val_name_Fres_folder,\
	val_t_unit,val_t_init,va_li_phrases=["1st line=(id entry lk,  id exit link),other lines:  < time value (1st column), mean travel time, total nb veh  (2nd column) "],\
	val_li_phrases_mean_trav_dist=["1st line=(id entry lk,  id exit link),other lines:  t_start, t_end period (1st, 2nd column), mean traveled distance, total nb veh  (3rd column) "]):
	
		#we create a  result sim treatment object
		treat_sim_obj=Cl_Treatment_Sim_Res.Treatment_Sim_Res(val_db_file_sim_res_to_treat=self._db_file)
		
		#dict, key=mov, value = [...,record obj,...]
		dict_db_file=treat_sim_obj.fct_creation_dictionary_key_movem_from_the_db_file()
		
		
		#dict, key=id event type, value=[..,record obj,...]
		#ATTENTION CE DICT EST AUSSI CALCULE (POUR UEN 2EME FOIS)  LORS CALCUL MEAN TRAVEL TIME, A CORRIGER 
		dict_db_file_1=treat_sim_obj.fct_creation_dictionary_from_the_db_file()
		
		self.fct_write_mean_traveled_distance_per_period(\
		va_veh_final_dest_dynam_construct=val_veh_final_dest_dynam_construct,\
		va_name_Fres_folder=val_name_Fres_folder,\
		va_sim_dur=val_dur_sim,va_t_period=val_t_period,va_t_unit=val_t_unit,\
		va_t_init=val_t_init,\
		va_di_internal_lk_info=val_netw.get_di_internal_links_to_network(),\
		lis_phrases=val_li_phrases_mean_trav_dist)
		
		
		
		val_dict_info_entry_exit_lk=self.fct_creat_dict_exit_link_info()
		
		#write the file with the average travel time per period
		self.fct_calcul_and_write_travel_time_per_time_period_entry_exit_lk(\
		va_sim_dur=val_dur_sim,va_t_period=val_t_period,va_t_unit=val_t_unit,va_round_prec=2,va_lis_phrases=va_li_phrases,\
		va_t_init=val_t_init,val_di_info_entry_exit_lk=val_dict_info_entry_exit_lk)
		
		#the file with the mean travel time between entry-exit link
		self.fct_writing_file_mean_travel_time_entry_exit_lk_nb_veh_served(val_di_info_entry_exit_lk=val_dict_info_entry_exit_lk)
		
		#dict, key=id phase, value=[...,nb veh arrived at ith cycle,...]
		#di_key_id_phase_value_nb_veh_ar_ap_per_cycle=self.fct_creat_dict_veh_arrival_at_phase_per_cycle(\
		#val_network=val_netw,val_dict_db_file=dict_db_file,val_cycle_duration=val_cycle_dur)
		
		#dictionary, key=id phase, value=[...,nb veh arrived at ith cycle,...]
		#di_key_id_phase_value_nb_veh_dep_per_cycle=self.fct_creat_dict_veh_depart_from_phase_per_cycle(\
		#val_network=val_netw,val_dict_db_file=dict_db_file,val_cycle_duration=val_cycle_dur)
		
		#dict, key=id phase, value=[...., nb_dep-nb_ar at ith cycle,...]
		#di_key_id_phase_value_dif_dep_minus_ar=self.fct_creat_dict_differ_depart_minus_ar(\
		#val_di_key_id_phase_val_ar_ap_per_cycle=di_key_id_phase_value_nb_veh_ar_ap_per_cycle,\
		#val_di_key_id_phase_val_dep_per_cycle=di_key_id_phase_value_nb_veh_dep_per_cycle)
		
		#files with the veh arrival and depart/cycle for each phase
		#self.fct_write_files_nb_veh_arrivals_and_departures_per_cycle(\
		#val_di_veh_ap_ar_per_cycle=di_key_id_phase_value_nb_veh_ar_ap_per_cycle,\
		#val_di_veh_dep_per_cycle=di_key_id_phase_value_nb_veh_dep_per_cycle,\
		#val_cycle_durat=val_cycle_dur)
		
		
		#files with the control of each phase
		#self.fct_write_files_ctrl_evolution(va_dict_db_key_id_event_type_val_record_obj=dict_db_file_1)
		
		#files with the actuation duration of  each phase
		di_phase_act_dur_per_period=self.fct_creat_dict_phase_actuat(dict_db_key_id_event_type_val_record_obj=dict_db_file_1,\
		v_sim_dur=val_dur_sim,\
		v_t_period=val_t_period,\
		v_t_unit=val_t_unit,v_t_init=val_t_init)
		
		self.fct_write_file_total_actutation_duration_per_period_each_phase(name_file_to_write=self._folder_phase_act_durat_per_period+"/"+\
		File_Stats_Anal_Folders_And_Files.name_file_total_act_duration_per_period_phase,\
		dict_phase_act_dur_info=di_phase_act_dur_per_period,lis_phrases=["t start period (1st colm), t end period (2nd colm), total actuat duration (3rd colm)"])
		
		
		#if we have finite link capacity we present the link evolution
		#if val_finite_lk_cap==1:
		#files with the length of each link
		self.fct_write_files_entry_internal_link_evol(va_netw=val_netw,va_dict_db_key_id_event_type_val_record_obj=dict_db_file_1)
		
		
		#files with lengths of each queue during sim
		#self.fct_writing_file_time_veh_queue_length(val_netwk=val_netw,di_db_file=dict_db_file)
		#di_1=dict, key=movem, value=[ ...[[time,que length],total number of veh arrived in que]...]
		di_1=self.fct_writing_file_time_veh_queue_length_and_aver_que_length(val_netwk=val_netw,di_db_file=dict_db_file)
		
		
		self.fct_write_files_control_evolution_per_intersection(val_dic_ev_type=dict_db_file_1,val_li_phrases=["t_start stage act. duration (1st colm) t_end stage act. duration (2nd colm"])
		
		#we write the file with the number of stage switches per itnersection
		self.fct_write_file_nb_stage_switches_per_inters(val_dic_ev_type=dict_db_file_1,val_li_phrases=["id node (1st colm), nb stage switches (2nd colm)"])

	
		#file with the sum of queues during sim
		#li=[..,[t,length of sum of queues],..]
		li=self.fct_write_file_sum_que_t_sim()
		
		
		#we write the file with the average value of the sum of the queues during the sim
		#self.fct_write_file_average_sum_que_t_sim(val_total_nb_network_ques=len(di_1))
		
		
		#file with the number pf departing veh and the percentage of times we have this number
		#self.fct_writing_file_nb_dep_veh_nb_times(val_netwk=val_netw,di_db_file=dict_db_file)
		
		
	
		
		#the file with the number of veh in the sum of queues and the prob of having that number
		#di=dict, key=nb_of_veh value=[ prob, time with this number of veh]
		di=self.fct_writing_prob_of_nb_veh_at_queue(val_li_t_que_len=li,val_durat_sim=val_dur_sim)
		
		
		
		#the file with the weighted mean and the stand deviation of the sum of queues
		self.fct_writing_file_weighted_mean_sd_sum_que(val_dict_nb_veh_que_and_durat=di,val_durat_sim=val_dur_sim)
		
		#the file with the stte of the queue after the eeh departure
		#self.fct_writing_file_time_veh_queue_length_after_veh_dep(val_netwk=val_netw,di_db_file=dict_db_file)
		
		#the file with the mean value of each queue
		#self.fct_calcul_average_time_spent_by_veh_in_a_que_for_each_que_2(\
		#di_key_mov_val_sorted_li_t_que_length=di_1,val_durat_sim=val_dur_sim)
		#self.fct_writing_file_average_time_spent_by_veh_in_a_que_for_each_que_1(dict_key_movement_value_record_obj=dict_db_file)
		self.fct_writing_file_average_time_spent_by_veh_in_a_que_for_each_que(\
		di_key_movem_val_sorted_li_t_que_length=di_1,\
		val_duration_sim=val_dur_sim)
		
		#we create the dict
		
		#**********ICI
		
				
		#self.NOfct_writing_file_nb_veh_que_nb_t_veh_ar_ap_que_length(val_netwk=val_netw,di_db_file=dict_db_file)
		#self.fct_writing_file_nb_veh_que_dep_nb_of_t_and_t_veh_departure_nb_dep_veh(val_netwk=val_netw,di_db_file=dict_db_file)
		#self.fct_writing_file_time_veh_queue_length_after_veh_dep(val_netwk=val_netw,di_db_file=dict_db_file)
		#self.fct_writing_file_mean_travel_time_entry_exit_lk_nb_veh_served(val_net=val_netw)
		#self.fct_writing_file_sum_queus_during_sim()
		#li=self.fct_calc_weight_mean_sd_sum_que(1800)
		#li=self.fct_calc_weight_mean_sd_prob_que_val_sum_que(1800)
		#return li
		
#*****************************************************************************************************************************************************************************************
	#function writing a file for each queue with :
	# --- the time and the number of vehicles in the queue, type of the event
	#--- the time, the number of vehicles in the queue, after the veh arrival/appearance events, event type
	#--- the time, the number of departing vehicles in the queue, after each veh departure events
	#---  the number of vehicles in a queue, and the number of times that we had that number
	def fct_writing_files_sa1(self,val_netw,val_dur_sim,val_cycle_dur,val_t_end_sim,val_finite_lk_cap):
	
		#we create a  result sim treatment object
		treat_sim_obj=Cl_Treatment_Sim_Res.Treatment_Sim_Res(val_db_file_sim_res_to_treat=self._db_file)
		
		#dict, key=mov, value = [...,record obj,...]
		dict_db_file=treat_sim_obj.fct_creation_dictionary_key_movem_from_the_db_file()
		
		
		#dict, key=id event type, value=[..,record obj,...]
		#ATTENTION CE DICT EST AUSSI CALCULE (POUR UEN 2EME FOIS)  LORS CALCUL MEAN TRAVEL TIME, A CORRIGER 
		dict_db_file_1=treat_sim_obj.fct_creation_dictionary_from_the_db_file()
		
		#dict, key=id phase, value=[...,nb veh arrived at ith cycle,...]
		di_key_id_phase_value_nb_veh_ar_ap_per_cycle=self.fct_creat_dict_veh_arrival_at_phase_per_cycle(\
		val_network=val_netw,val_dict_db_file=dict_db_file,val_cycle_duration=val_cycle_dur)
		
		#dictionary, key=id phase, value=[...,nb veh arrived at ith cycle,...]
		di_key_id_phase_value_nb_veh_dep_per_cycle=self.fct_creat_dict_veh_depart_from_phase_per_cycle(\
		val_network=val_netw,val_dict_db_file=dict_db_file,val_cycle_duration=val_cycle_dur)
		
		#dict, key=id phase, value=[...., nb_dep-nb_ar at ith cycle,...]
		#di_key_id_phase_value_dif_dep_minus_ar=self.fct_creat_dict_differ_depart_minus_ar(\
		#val_di_key_id_phase_val_ar_ap_per_cycle=di_key_id_phase_value_nb_veh_ar_ap_per_cycle,\
		#val_di_key_id_phase_val_dep_per_cycle=di_key_id_phase_value_nb_veh_dep_per_cycle)
		
		#files with the veh arrival and depart/cycle for each phase
		self.fct_write_files_nb_veh_arrivals_and_departures_per_cycle(\
		val_di_veh_ap_ar_per_cycle=di_key_id_phase_value_nb_veh_ar_ap_per_cycle,\
		val_di_veh_dep_per_cycle=di_key_id_phase_value_nb_veh_dep_per_cycle,\
		val_cycle_durat=val_cycle_dur)
		
		#files with the control of each phase
		self.fct_write_files_ctrl_evolution(va_dict_db_key_id_event_type_val_record_obj=dict_db_file_1,\
		val_dict_veh_depart_per_cycle_per_phase=di_key_id_phase_value_nb_veh_dep_per_cycle,\
		val_t_end_simul=val_t_end_sim,\
		val_cycle_durat=val_cycle_dur)
		
		#if we have finite link capacity we present the link evolution
		#if val_finite_lk_cap==1:
		#files with the length of each link
		#self.fct_write_files_entry_internal_link_evol(va_netw=val_netw,va_dict_db_key_id_event_type_val_record_obj=dict_db_file_1)
		
		
		#files with lengths of each queue during sim
		#self.fct_writing_file_time_veh_queue_length(val_netwk=val_netw,di_db_file=dict_db_file)
		#di_1=dict, key=movem, value=[ ...[[time,que length],total number of veh arrived in que]...]
		#di_1=self.fct_writing_file_time_veh_queue_length_and_aver_que_length(val_netwk=val_netw,di_db_file=dict_db_file)
		
		
	
	
		#file with the sum of queues during sim
		#li=[..,[t,length of sum of queues],..]
		#li=self.fct_write_file_sum_que_t_sim()
		
		
		
		#file with the number pf departing veh and the percentage of times we have this number
		#self.fct_writing_file_nb_dep_veh_nb_times(val_netwk=val_netw,di_db_file=dict_db_file)
		
		#the file with the mean travel time between entry-exit link
		#self.fct_writing_file_mean_travel_time_entry_exit_lk_nb_veh_served()
		
	
		
		#the file with the number of veh in the sum of queues and the prob of having that number
		#di=dict, key=nb_of_veh value=[ prob, time with this number of veh]
		#di=self.fct_writing_prob_of_nb_veh_at_queue(val_li_t_que_len=li,val_durat_sim=val_dur_sim)
		
		
		
		#the file with the weighted mean and the stand deviation of the sum of queues
		#self.fct_writing_file_weighted_mean_sd_sum_que(val_dict_nb_veh_que_and_durat=di,val_durat_sim=val_dur_sim)
		
		#the file with the stte of the queue after the eeh departure
		#self.fct_writing_file_time_veh_queue_length_after_veh_dep(val_netwk=val_netw,di_db_file=dict_db_file)
		
		#the file with the mean value of each queue
		#self.fct_calcul_average_time_spent_by_veh_in_a_que_for_each_que_2(\
		#di_key_mov_val_sorted_li_t_que_length=di_1,val_durat_sim=val_dur_sim)
		#self.fct_writing_file_average_time_spent_by_veh_in_a_que_for_each_que_1(dict_key_movement_value_record_obj=dict_db_file)
		#self.fct_writing_file_average_time_spent_by_veh_in_a_que_for_each_que(\
		#di_key_movem_val_sorted_li_t_que_length=di_1,\
		#val_duration_sim=val_dur_sim)
		
		#we create the dict
		
		#**********ICI
		
				
		#self.NOfct_writing_file_nb_veh_que_nb_t_veh_ar_ap_que_length(val_netwk=val_netw,di_db_file=dict_db_file)
		#self.fct_writing_file_nb_veh_que_dep_nb_of_t_and_t_veh_departure_nb_dep_veh(val_netwk=val_netw,di_db_file=dict_db_file)
		#self.fct_writing_file_time_veh_queue_length_after_veh_dep(val_netwk=val_netw,di_db_file=dict_db_file)
		#self.fct_writing_file_mean_travel_time_entry_exit_lk_nb_veh_served(val_net=val_netw)
		#self.fct_writing_file_sum_queus_during_sim()
		#li=self.fct_calc_weight_mean_sd_sum_que(1800)
		#li=self.fct_calc_weight_mean_sd_prob_que_val_sum_que(1800)
		#return li
		
#*****************************************************************************************************************************************************************************************
	
	
	#method returning a dictionary, key=veh id, value= dict, key=link id from which the veh has passed, 
	#value=[t arrival/ap at link, t join que, t start deprt from que,t_arrival_at_next_link, que size when veh joined que]
	#def fct_dict_key_veh_id_value_di_key_id_ap_ar_lk_value_li_t_ar_ap_t_join_que_t_start_dep_que_t_ar_next_lk_que_at_t_join_que
	def fct_dict_info_with_t_ar_dep_que_size_at_eack_veh_lk_location(self):
		
		#di, key=veh id, value=[...,[event time,event_type,veh. current link location, veh destination, time exit netw,\
		#time started departure, len(queue size if the event is arrival at link) -1 we substract -1 because we do not want to count the current vehicle,
		#-1 otherwise],...]
		di=self._treat_sim_res_obj.fct_dict_information_vehicles_sim_all_inf()
		#print(di[42])
		di_rep={}
		
		#for each vehicle
		for i in di:
			di_rep[i]={}
			for j in di[i]:
				#print("j",j)
				#if the event is veh appear
				if j[1]==Cl_Event.TYPE_EV["type_ev_veh_appearance"]:
					#di_rep[i][id locat]=[-1,-1,-1,-1,-1]
					di_rep[i][j[2]]=5*[-1]
					#on indique le temps appear
					di_rep[i][j[2]][0]=j[0]
					#on  indique le t_join_que
					di_rep[i][j[2]][1]=j[0]
					#on indique the que size
					di_rep[i][j[2]][4]=j[6]
					current_loc=j[2]
					dest_loc=j[3]
			
				#if the event is veh end departure
				elif j[1]==Cl_Event.TYPE_EV["type_ev_end_veh_departure_from_que"]:
					#on indique le t_start_dep
					di_rep[i][current_loc][2]=j[5]
					#on indique le t_arrival next link
					di_rep[i][current_loc][3]=j[0]
					
					current_loc=j[2]
					dest_loc=j[3]
					
					di_rep[i][j[2]]=5*[-1]
					#on indique le temps arrival at new link
					di_rep[i][current_loc][0]=j[0]
			
				#if the event is veh arrival at the end if the link (que)
				elif  j[1]==Cl_Event.TYPE_EV["type_ev_veh_arrived_at_que"]:
					
					#on  indique le t_join_que
					di_rep[i][j[2]][1]=j[0]
					#onindique le que size que le veh a rencontre
					di_rep[i][j[2]][4]=j[6]
					current_loc=j[2]
					dest_loc=j[3]
					
				#otherwise
				else:
					print("PROBLEM IN CL_STAT_ANAL,fct_dict_info_with_t_ar_dep_que_size_at_eack_veh_lk_location  TYPE EVENT=", j[1])
					import sys
					sys.exit()
		
		return di_rep

#*****************************************************************************************************************************************************************************************
	
	#method retuning a dictionary for a desired link of which the key=id veh, 
	#value=[t_ar_ap_link,t joined que,t_start_depart_from_que,t_ar_next_link, que size it met when joined queue]
	def fct_calc_history_veh_ap_ar_and_dep_and_que_size_from_given_lk(self,val_id_link):
		
		#dict, key=veh id, value=dict, key=link id from which the veh has passed, 
		#value=[t arrival/ap at link, t join que, t start deprt from que,t_arrival_at_next_link, que size when veh joined que]
		di=self.fct_dict_info_with_t_ar_dep_que_size_at_eack_veh_lk_location()
		
		
		di_rep={}
		#for each vehicle
		for i in di:
			#if the vehicle has passed from the desired link 
			if val_id_link in di[i]:
				di_rep[i]=di[i][val_id_link]
				
		#dict: key=event type, value= record obj
		#m1=0
		#di1=self._treat_sim_res_obj.fct_creation_dictionary_from_the_db_file()
		#for m in di1[Cl_Event.TYPE_EV["type_ev_veh_arrived_at_que"]]:
			#if m.get_id_current_link_veh_location()==8:
				#m1+=1
		#print("m=",m1,"di_rep",len(di_rep))
				
		return di_rep
				

#*****************************************************************************************************************************************************************************************
	
	#method creating a dictionary for the desired link id,
	#key=veh id, value=[t_ap_ar,t_next_ar, T=t_next_ar - t_ap_ar]
	def fct_calcul_history_veh_t_ar_current_and_next_lk_travel_time(self,va_id_link):
	
		#dict, key=veh id, value=[t_ar_ap_link,t joined que,t_start_depart_from_que,t_ar_next_link, que size the veh met when joined queue]
		di=self.fct_calc_history_veh_ap_ar_and_dep_and_que_size_from_given_lk(val_id_link=va_id_link)
		
		di_rep={}
		for i in di:
			#print(di[i][3])
			di_rep[i]=[di[i][0],di[i][3],di[i][3]-di[i][0]]
		return di_rep
			

#*****************************************************************************************************************************************************************************************
	#method creating a dictionary for the desired link id,
	#key=veh id, value=[t_ap_ar_lk, T=t_next_ar - t_ap_ar]
	def fct_calcul_history_veh_t_ar_ap_lk_travel_time(self,va_id_link):
	
		#dict, key=veh id, value=[t_ar_ap_link,t joined que,t_start_depart_from_que,t_ar_next_link, que size the veh met when joined queue]
		di=self.fct_calc_history_veh_ap_ar_and_dep_and_que_size_from_given_lk(val_id_link=va_id_link)
		
		di_rep={}
		for i in di:
			if di[i][3]>0:
				#print(di[i][3])
				di_rep[i]=[di[i][0],di[i][3]-di[i][0]]
		return di_rep
			

#*****************************************************************************************************************************************************************************************
	#method creating a dictionary for the desired link id,
	#key=veh id, value=[t_ar_next_link, T=t_next_ar - t_ap_ar]
	def fct_calcul_history_veh_t_ar_next_lk_travel_time(self,va_id_link):
	
		#dict, key=veh id, value=[t_ar_ap_link,t joined que,t_start_depart_from_que,t_ar_next_link, que size the veh met when joined queue]
		di=self.fct_calc_history_veh_ap_ar_and_dep_and_que_size_from_given_lk(val_id_link=va_id_link)
		
		di_rep={}
		for i in di:
			if di[i][3]>0:
				#print(di[i][3])
				di_rep[i]=[di[i][3],di[i][3]-di[i][0]]
		return di_rep
			

#*****************************************************************************************************************************************************************************************
	#method creating a dictionary  for the desired link id,
	#key=veh id, value=[q(t_joins que), T=t_next_ar - t_ap_ar]
	def fct_calcul_history_que_met_by_veh_at_que_ar_t_travel(self,va_id_link):
	
		#dict, key=veh id, value=[t_ar_ap_link,t joined que,t_start_depart_from_que,t_ar_next_link, que size the veh met when joined queue]
		di=self.fct_calc_history_veh_ap_ar_and_dep_and_que_size_from_given_lk(val_id_link=va_id_link)
		
		
		di_rep={}
		for i in di:
			if di[i][3]>0:
				#print(di[i][3])
				di_rep[i]=[di[i][4],di[i][3]-di[i][0]]
		return di_rep

		
#*****************************************************************************************************************************************************************************************
	#method returning a dictionary, key=veh id, 
	#value=[[t arrival/ap at link, t join que, t start deprt from que,t_arrival_at_next_link, que size when veh joined que]]
	#(=[t1,t2,t3,t4,q] paper)
	def fct_dict_info_with_t_ar_dep_que_size_at_given_que(self,id_origin_lk,id_destination_link):
		
		#di, key=veh id, value=[...,[event time,event_type,veh. current link location, veh destination, time exit netw,\
		#time started departure, len(queue size if the event is arrival at link) -1 we substract -1 because we do not want to count the current vehicle,
		#-1 otherwise],...]
		di=self._treat_sim_res_obj.fct_dict_information_vehicles_sim_all_inf()
		
		#the list of the veh id passed by queue [id_origin_lk,id_destination_link]
		li_veh_id=[]
		for m in di:
			#print("m=",di[m])
			for n in di[m]:
				#if the event type is vehicle arrival and veh. current link location=id_origin_lk and veh destination veh destination
				if n[1]==Cl_Event.TYPE_EV["type_ev_veh_arrived_at_que"] and n[2]==id_origin_lk and n[3]==id_destination_link:
					li_veh_id.append(m)
		#print(li_veh_id)
			
		
		#print(di[42])
		di_rep={}
		
		#for each vehicle
		for i in li_veh_id:
			di_rep[i]={}
			for j in di[i]:
			
				#if the event is veh appear
				if j[1]==Cl_Event.TYPE_EV["type_ev_veh_appearance"]:
					#di_rep[i][id locat]=[-1,-1,-1,-1,-1]
					di_rep[i][j[2]]=5*[-1]
					#on indique le temps appear
					di_rep[i][j[2]][0]=j[0]
					#on  indique le t_join_que
					di_rep[i][j[2]][1]=j[0]
					#on indique the que size
					di_rep[i][j[2]][4]=j[6]
					current_loc=j[2]
					dest_loc=j[3]
			
				#if the event is veh end departure
				elif j[1]==Cl_Event.TYPE_EV["type_ev_end_veh_departure_from_que"]:
					#on indique le t_start_dep
					di_rep[i][current_loc][2]=j[5]
					#on indique le t_arrival next link
					di_rep[i][current_loc][3]=j[0]
					
					current_loc=j[2]
					dest_loc=j[3]
					
					di_rep[i][j[2]]=5*[-1]
					#on indique le temps arrival at new link
					di_rep[i][current_loc][0]=j[0]
			
				#if the event is veh arrival at the end if the link (que)
				elif  j[1]==Cl_Event.TYPE_EV["type_ev_veh_arrived_at_que"]:
					
					#on  indique le t_join_que
					di_rep[i][j[2]][1]=j[0]
					#onindique le que size que le veh a rencontre
					di_rep[i][j[2]][4]=j[6]
					current_loc=j[2]
					dest_loc=j[3]
					
				#otherwise
				else:
					print("PROBLEM IN CL_STAT_ANAL,fct_dict_info_with_t_ar_dep_que_size_at_eack_veh_lk_location  TYPE EVENT=", j[1])
					import sys
					sys.exit()
		#print(di_rep.keys())
		
		return di_rep

#*****************************************************************************************************************************************************************************************
	#method creating a dictionary for the desired que
	#key=veh id, value=[t_ar_lk,t_next_lk_ar, T=t_next_lk_ar - t_ar_lk] (=[t1,t4,T] paper)
	#di=dict, key=veh id passed by que [va_id_orig_link,va_id_dest_link], value=dict, key =id link,
	#[t_ar_ap_link,t joined que,t_start_depart_from_que,t_ar_next_link, que size the veh met when joined queue, veh id]
	def fct_calcul_history_veh_t_ar_current_and_next_lk_travel_time_given_que(self,va_id_orig_link,va_id_dest_link,di,v_round_precision):
	
		#dict, key=veh id, value dict, key=lk id 
		#value=[t_ar_ap_link,t joined que,t_start_depart_from_que,t_ar_next_link, que size the veh met when joined queue]
		#di=self.fct_dict_info_with_t_ar_dep_que_size_at_given_que(id_origin_lk=va_id_orig_link,id_destination_link=va_id_dest_link)
		
		di_rep={}
		for i in di:
			#print(di[i][3])
			a=round(di[i][va_id_orig_link][3]-di[i][va_id_orig_link][0],v_round_precision)
			di_rep[i]=[di[i][va_id_orig_link][0],di[i][va_id_orig_link][3],a,i]
		return di_rep
			



#*****************************************************************************************************************************************************************************************
	#method creating a dictionary for the desired que
	#key=veh id, value=[t_ar_lk, T=t_next_ar - t_ar] (=[t1,T] paper)
	#di=dict, key=veh id, value=dict, key=lk id, 
	#value=[t_ar_ap_link,t joined que,t_start_depart_from_que,t_ar_next_link, que size the veh met when joined queue,veh id]
	def fct_calcul_history_veh_t_ar_lk_travel_time_given_que(self,va_id_orig_link,va_id_dest_link,di,v_round_precision):
	
		#dict, key=veh id, value=[t_ar_ap_link,t joined que,t_start_depart_from_que,t_ar_next_link, que size the veh met when joined queue]
		#di=self.fct_dict_info_with_t_ar_dep_que_size_at_given_que(id_origin_lk=va_id_orig_link,id_destination_link=va_id_dest_link)
		
		di_rep={}
		for i in di:
			if di[i][va_id_orig_link][3]>0:
				#print(di[i][3])
				a=round(di[i][va_id_orig_link][3]-di[i][va_id_orig_link][0],v_round_precision)
				di_rep[i]=[di[i][va_id_orig_link][0],a,i]
		return di_rep
			

#*****************************************************************************************************************************************************************************************
	#method creating a dictionary for the desired que,
	#key=veh id, value=[t_ar_next_link, T=t_next_ar - t_ap_ar] (=[t4,T] paper)
	#di=dict, key=veh id, value=dict, key=lk id, 
	#value=[t_ar_ap_link,t joined que,t_start_depart_from_que,t_ar_next_link, que size the veh met when joined queue,veh id]
	def fct_calcul_history_veh_t_ar_next_lk_travel_time_given_que(self,va_id_orig_link,va_id_dest_link,di,v_round_precision):
	
		#dict, key=veh id, value=[t_ar_ap_link,t joined que,t_start_depart_from_que,t_ar_next_link, que size the veh met when joined queue]
		#di=self.fct_dict_info_with_t_ar_dep_que_size_at_given_que(id_origin_lk=va_id_orig_link,id_destination_link=va_id_dest_link)
		
		di_rep={}
		for i in di:
			if di[i][va_id_orig_link][3]>0:
				#print(di[i][3])
				a=round(di[i][va_id_orig_link][3]-di[i][va_id_orig_link][0],v_round_precision)
				di_rep[i]=[di[i][va_id_orig_link][3],a,i]
		return di_rep
			

#*****************************************************************************************************************************************************************************************
	#method creating a dictionary for the desired que
	#dict, key=veh id, value=[t_ar_next_link, T=t_next_ar - t_ap_ar] (=[t4,T])
	#di=dict, key=veh id, value=[t_ar_ap_link,t joined que,t_start_depart_from_que,t_ar_next_link, que size the veh met when joined queue]
	#def fct_calcul_history_veh_t_ar_next_lk_travel_time_given_que(self,va_id_orig_link,va_id_dest_link,di):
	
		#dict, key=veh id, value=[t_ar_ap_link,t joined que,t_start_depart_from_que,t_ar_next_link, que size the veh met when joined queue]
		#di=self.fct_dict_info_with_t_ar_dep_que_size_at_given_que(id_origin_lk=va_id_orig_link,id_destination_link=va_id_dest_link)
		
		#di_rep={}
		#for i in di:
			#if di[i][va_id_orig_link][3]>0:
				#print(di[i][3])
				#di_rep[i]=[di[i][va_id_orig_link][3],di[i][va_id_orig_link][3]-di[i][va_id_orig_link][0]]
		#return di_rep
			

#*****************************************************************************************************************************************************************************************
	#method creating a dictionary  for the desired que,
	#key=veh id, value=[q(t_joins que), T=t_next_ar - t_ap_ar]
	#di=dict, key=veh id, value=dict key=lk id, 
	#value=[t_ar_ap_link,t joined que,t_start_depart_from_que,t_ar_next_link, que size the veh met when joined queue,veh id]
	def fct_calcul_history_que_met_by_veh_at_que_ar_t_travel_given_que(self,va_id_orig_link,va_id_dest_link,di,v_round_precision):
	
		#dict, key=veh id, value=[t_ar_ap_link,t joined que,t_start_depart_from_que,t_ar_next_link, que size the veh met when joined queue]
		#di=self.fct_calc_history_veh_ap_ar_and_dep_and_que_size_from_given_lk(id_origin_lk=va_id_orig_link,id_destination_link=va_id_dest_link)
		
		
		di_rep={}
		for i in di:
			if di[i][va_id_orig_link][3]>0:
				#print(di[i][3])
				a=round(di[i][va_id_orig_link][3]-di[i][va_id_orig_link][0],v_round_precision)
				di_rep[i]=[di[i][va_id_orig_link][4],a,i]
		return di_rep

		
#*****************************************************************************************************************************************************************************************



	#method calculating and writing the veh arrival/appear time, depart time(start-end),the arrival time at next link and the queue size
	#met by its arrival in a file
	
	def fct_calcul_and_write_history_link_veh_ar_ap_departs_and_que_size(self,va_link_id,va_name_file_to_write,\
	val_name_file_to_write_second_dict, val_name_file_to_write_second_dict_1,\
	val_name_file_to_write_third_dict,val_name_file_to_write_fourth_dict,\
	va_li_phrases,va_li_phrases_2,va_li_phrases_3,va_li_phrases_4,va_li_phrases_5):
	
		#dict, key=veh id, value=[t arrival/ap at link, t join que, t start deprt from que,t_arrival_at_next_link, que size when veh joined que]
		di=self.fct_calc_history_veh_ap_ar_and_dep_and_que_size_from_given_lk(val_id_link=va_link_id)
	
		
		#dict, key=veh id, value=[t arrival/ap at link,t_arrival_at_next_link,t_arrival_at_next_link-t arrival/ap at link] (=[t1,t4,T])
		di_1=self.fct_calcul_history_veh_t_ar_current_and_next_lk_travel_time(va_id_link=va_link_id)
		
		#dict, key=veh id, value=[t arrival/ap at link,t_arrival_at_next_link-t arrival/ap at link] (=[t1,T])
		di_2=self.fct_calcul_history_veh_t_ar_ap_lk_travel_time(va_id_link=va_link_id)
		
		#dict, key=veh id, value=[t_arrival_at_next_link,t_arrival_at_next_link-t arrival/ap at link](=[t4,T] paper)
		di_3=self.fct_calcul_history_veh_t_ar_next_lk_travel_time(va_id_link=va_link_id)
		
		#dict, key=veh id, value=[q(t_joins que), T=t_next_ar - t_ap_ar]
		di_4=self.fct_calcul_history_que_met_by_veh_at_que_ar_t_travel(va_id_link=va_link_id)
		
		#we will write the dict inform in a file, in a sorted order reagarding the t_veh_ap_ar
		#li= list [[t_veh_ap_or_ar,id veh]]
		li=[]
		for i in di:
			li.append([di[i][0],i])
			
		li.sort()
		
		li_id_veh=[]
		for j in li:
			li_id_veh.append(j[1])
		
		name_file_to_write_1=self._folder_stat_anal+"/"+va_name_file_to_write+str(va_link_id)+".txt"
				
		file=open(name_file_to_write_1,"w")
		
		file.write("%s\t %d \n"%("Link ID",va_link_id))
		
		for m in va_li_phrases:
			file.write("%s\t \n"%(m))
			
		
		for k in li_id_veh:
			file.write("%s\t"%(k))
			for n in di[k]:
				file.write("%.2f\t"%(n))
			file.write("\n")
		file.close()
		
		name_file_to_write_2=self._folder_stat_anal+"/"+val_name_file_to_write_second_dict+str(va_link_id)+".txt"
		file2=open(name_file_to_write_2,"w")
		file2.write("%s\t %d \n"%("Link ID",va_link_id))
		for q in va_li_phrases_2:
			file2.write("%s\t \n"%(q))
			
		for p in li_id_veh:
			file2.write("%s\t"%(p))
			for r in di_1[p]:
				file2.write("%.2f\t"%(r))
			file2.write("\n")
		file2.close()
		
		name_file_to_write_3=self._folder_stat_anal+"/"+val_name_file_to_write_second_dict_1+str(va_link_id)+".txt"
		file3=open(name_file_to_write_3,"w")
		file3.write("%s\t %d \n"%("Link ID",va_link_id))
		for s in va_li_phrases_3:
			file3.write("%s\t \n"%(s))
			
		for t in li_id_veh:
			#file2.write("%s\t"%(p))
			if t in di_2:
				for u in di_2[t]:
					file3.write("%.2f\t"%(u))
				file3.write("\n")
		file3.close()
		
		name_file_to_write_4=self._folder_stat_anal+"/"+val_name_file_to_write_third_dict+str(va_link_id)+".txt"
		file4=open(name_file_to_write_4,"w")
		file4.write("%s\t %d \n"%("Link ID",va_link_id))
		for v in va_li_phrases_4:
			file4.write("%s\t \n"%(v))
			
		for w in li_id_veh:
			#file2.write("%s\t"%(p))
			if w in di_3:
				for z in di_3[w]:
					file4.write("%.2f\t"%(z))
				file4.write("\n")
		file4.close()


		name_file_to_write_5=self._folder_stat_anal+"/"+val_name_file_to_write_fourth_dict+str(va_link_id)+".txt"
		file5=open(name_file_to_write_5,"w")
		file5.write("%s\t %d \n"%("Link ID",va_link_id))
		for c in va_li_phrases_5:
			file5.write("%s\t \n"%(c))
			
		for d in li_id_veh:
			#file2.write("%s\t"%(p))
			if d in di_4:
				for f in di_4[d]:
					file5.write("%.2f\t"%(f))
				file5.write("\n")
		file5.close()

		
		
			
		
#*****************************************************************************************************************************************************************************************

	#method calculating and writing the veh arrival/appear time, depart time(start-end),the arrival time at next link and the queue size
	#met by its arrival in a file
	
	def fct_calcul_and_write_history_link_veh_ar_ap_departs_and_que_size_given_que(self,\
	val_id_origin_link,val_id_destination_link,va_name_file_to_write,\
	val_name_file_to_write_second_dict, val_name_file_to_write_second_dict_1,\
	val_name_file_to_write_third_dict,val_name_file_to_write_fourth_dict,\
	va_li_phrases,va_li_phrases_2,va_li_phrases_3,va_li_phrases_4,va_li_phrases_5,va_round_precision):
	
		#dict, key=veh id, value=dict,
		#key=lk id, value=[t arrival/ap at link, t join que, t start deprt from que,t_arrival_at_next_link, que size when veh joined que]
		dict=self.fct_dict_info_with_t_ar_dep_que_size_at_given_que(id_origin_lk=val_id_origin_link,id_destination_link=val_id_destination_link)
		#print(dict[75])
		#import sys
		#sys.exit()
		
		#dict, key=veh id, value=[t arrival/ap at link,t_arrival_at_next_link,t_arrival_at_next_link-t arrival/ap at link] (=[t1,t4,T])
		di_1=self.fct_calcul_history_veh_t_ar_current_and_next_lk_travel_time_given_que(va_id_orig_link=val_id_origin_link,\
		va_id_dest_link=val_id_destination_link,di=dict,v_round_precision=va_round_precision)
		#print(di_1[2056])
		#import sys
		#sys.exit()
		
		#dict, key=veh id, value=[t arrival/ap at link,t_arrival_at_next_link-t arrival/ap at link] (=[t1,T])
		di_2=self.fct_calcul_history_veh_t_ar_lk_travel_time_given_que(va_id_orig_link=val_id_origin_link,va_id_dest_link=val_id_destination_link,\
		di=dict,v_round_precision=va_round_precision)
		#print(di_2[2056])
		#import sys
		#sys.exit()
		
		#dict, key=veh id, value=[t_arrival_at_next_link,t_arrival_at_next_link-t arrival/ap at link](=[t4,T] paper)
		di_3=self.fct_calcul_history_veh_t_ar_next_lk_travel_time_given_que(va_id_orig_link=val_id_origin_link,va_id_dest_link=val_id_destination_link,\
		di=dict,v_round_precision=va_round_precision)
		#print(di_3[2056])
		#import sys
		#sys.exit()
		
		#dict, key=veh id, value=[q(t_joins que), T=t_next_ar - t_ap_ar]
		di_4=self.fct_calcul_history_que_met_by_veh_at_que_ar_t_travel_given_que(va_id_orig_link=val_id_origin_link,\
		va_id_dest_link=val_id_destination_link,di=dict,v_round_precision=va_round_precision)
		#print(di_4[2056])
		#import sys
		#sys.exit()
		
		
		#we will write the dict inform in a file, in a sorted order reagarding the t_veh_ap_ar
		#li= list [[t_veh_ap_or_ar,id veh]]
		li=[]
		for i in dict:
			li.append([dict[i][val_id_origin_link][0],i])
		#print(dict[i][val_id_origin_link])
			
		li.sort()
		
		li_id_veh=[]
		for j in li:
			li_id_veh.append(j[1])
		
		name_file_to_write_1=self._folder_stat_anal+"/"+va_name_file_to_write+"("+str(val_id_origin_link)+","+str(val_id_destination_link)+")"+".txt"
				
		file=open(name_file_to_write_1,"w")
		
		file.write("%s %d %s %d %s \n"%("Que ID=(",val_id_origin_link,",",val_id_destination_link,")"))
		
		for m in va_li_phrases:
			file.write("%s\t \n"%(m))
			
		
		for k in li_id_veh:
			file.write("%s\t"%(k))
			for n in dict[k][val_id_origin_link]:
				file.write("%.2f\t"%(n))
			file.write("\n")
		file.close()
		
		name_file_to_write_2=self._folder_stat_anal+"/"+val_name_file_to_write_second_dict+"("+str(val_id_origin_link)+","+str(val_id_destination_link)+")"+".txt"
		file2=open(name_file_to_write_2,"w")
		file2.write("%s %d %s  %d %s \n"%("Que ID=(",val_id_origin_link,",",val_id_destination_link,")"))
		for q in va_li_phrases_2:
			file2.write("%s\t \n"%(q))
			
		for p in li_id_veh:
			file2.write("%s\t"%(p))
			for r in di_1[p]:
				file2.write("%.2f\t"%(r))
			file2.write("\n")
		file2.close()
		
		name_file_to_write_3=self._folder_stat_anal+"/"+val_name_file_to_write_second_dict_1+"("+str(val_id_origin_link)+","+str(val_id_destination_link)+")"+".txt"
		file3=open(name_file_to_write_3,"w")
		file3.write("%s %d %s  %d %s \n"%("Que ID=(",val_id_origin_link,",",val_id_destination_link,")"))
		for s in va_li_phrases_3:
			file3.write("%s\t \n"%(s))
			
		for t in li_id_veh:
			#file2.write("%s\t"%(p))
			if t in di_2:
				for u in di_2[t]:
					file3.write("%.2f\t"%(u))
				file3.write("\n")
		file3.close()
		
		name_file_to_write_4=self._folder_stat_anal+"/"+val_name_file_to_write_third_dict+"("+str(val_id_origin_link)+","+str(val_id_destination_link)+")"+".txt"
		file4=open(name_file_to_write_4,"w")
		file4.write("%s %d %s  %d %s \n"%("Que ID=(",val_id_origin_link,",",val_id_destination_link,")"))
		for v in va_li_phrases_4:
			file4.write("%s\t \n"%(v))
			
		for w in li_id_veh:
			#file2.write("%s\t"%(p))
			if w in di_3:
				for z in di_3[w]:
					file4.write("%.2f\t"%(z))
				file4.write("\n")
		file4.close()


		name_file_to_write_5=self._folder_stat_anal+"/"+val_name_file_to_write_fourth_dict+"("+str(val_id_origin_link)+","+str(val_id_destination_link)+")"+".txt"
		file5=open(name_file_to_write_5,"w")
		file5.write("%s %d %s  %d %s \n"%("Que ID=(",val_id_origin_link,",",val_id_destination_link,")"))
		for c in va_li_phrases_5:
			file5.write("%s\t \n"%(c))
			
		for d in li_id_veh:
			#file2.write("%s\t"%(p))
			if d in di_4:
				for f in di_4[d]:
					file5.write("%.2f\t"%(f))
				file5.write("\n")
		file5.close()

		
		
			
		
#*****************************************************************************************************************************************************************************************

#****************************************** set of  functions for the calc of the sum of Series_Sim-Longue_vraies_donnéesSeries_Sim-Longue_vraies_donnéesSeries_Sim-Longue_vraies_donnéesSeries_Sim-Longue_vraies_donnéesSeries_Sim-Longue_vraies_donnéesSeries_Sim-Longue_vraies_donnéesSeries_Sim-Longue_vraies_donnéesSeries_Sim-Longue_vraies_donnéesSeries_Sim-Longue_vraies_donnéesSeries_Sim-Longue_vraies_donnéesSeries_Sim-Longue_vraies_donnéesSeries_Sim-Longue_vraies_donnéesSeries_Sim-Longue_vraies_donnéesSeries_Sim-Longue_vraies_donnéesSeries_Sim-Longue_vraies_donnéesSeries_Sim-Longue_vraies_donnéesSeries_Sim-Longue_vraies_donnéesSeries_Sim-Longue_vraies_donnéesSeries_Sim-Longue_vraies_donnéesSeries_Sim-Longue_vraies_donnéesue values*************************************************************************

	
	#method returning a list of which the ith element is  a list with the first two args of the ith line of a file, 
	#if the ith line of the file is 1,2,3,4 then  [...,[1,2],....]
	def fct_li_file_information_args_first_two_col(self,name_file_read,nb_comment_lines=1):

		#we open the file
		file=open(name_file_read,"r")
	
		#indicator of the number of lines already read.
		ind=0
		li_line=[]
		for i in file.readlines():
			ind+=1
			if ind>nb_comment_lines:
				#li_line=[]
				a=i.rsplit()
				li_line.append([eval(a[0]),eval(a[1])])
	
		file.close()
	
		return li_line

#***************************************************************************************************************************************************************************************** 



	#method returning a list of which the ith element is  a list with the first two args of the ith line of a file, 
	#if the ith line of the file is 1,2,3,4 then  [...,[1,2],....]
	#in case of many lines ith the same first column, only the last one is recorded
	#ex line 1: 1, 2, line 2: 1,3 ,  line 3: 1,0, line 4: 1,1 then we keep [1,1] the value of lie 4
	def fct_li_file_u_information_args_first_two_col(self,name_file_read,nb_comment_lines=1):

		#we open the file
		file=open(name_file_read,"r")
	
		#indicator of the number of lines already read.
		ind=0
		#li_line=[]
		di_line_key_t={}
		for i in file.readlines():
			ind+=1
			if ind>nb_comment_lines:
				#li_line=[]
				a=i.rsplit()
				di_line_key_t[eval(a[0])]=[eval(a[0]),eval(a[1])]
	
		li_key=[]
		for j in di_line_key_t	:
			li_key.append(j)
		li_key.sort()
	
	
		li_line=[]
		for i in li_key:
			li_line.append(di_line_key_t[i])
			
	
		file.close()
		
	
		return li_line

#***************************************************************************************************************************************************************************************** 
	#method returning a list with the 1st args of a list of which each elem is a list, if [ [x1,y1], [x2,y2],....], it returns [x1,x2,..]
	#val_list=[ [x1,y1], [x2,y2],....]
	def fct_li_with_first_elem_of_each_list(self,val_list):
		li=[]
		for i in val_list:
			li.append(i[0])
		return li

#***************************************************************************************************************************************************************************************** 
	def fct_union_list(self,li_a,li_b):
		return list(set(li_a) | set(li_b))
#***************************************************************************************************************************************************************************************** 
	#method returning the union of a elements of a list of lists, [[x1,y1,z1],[x1,y2,z2],[x3,y1,z1]], returns [ x1,y1,y2,x3,z1,z2] sorted
	def fct_union_list_elem(self,val_li_lists):
	
		s1=[]
	
		for i in val_li_lists:
			#print("i=",i)
			#print("s1=",s1)
			s2=self.fct_union_list(s1,[i])
			s1=s2
			
		
		li=list(s1)
		li.sort()
		return li

#***************************************************************************************************************************************************************************************** 
	#method returning the a list [ a list with all sim times, li]
	#li=[ [....,[t_i, length of queue_1 at t_i],...], [....,[t_i, length of queue_2 at t_i],...], .....]
	#len(li)=number of queues
	def fct_sim_u_t_instances_and_que_inf(self,val_li_path_files):

		li=[]
	
		cur_dir=os.getcwd()
		os.chdir(val_li_path_files)
	
		#for each file we create a list with the first two elem of its lines
		for i in os.listdir('.'):
			#li_1=[...,[t_i,queue_legnth at t_i],...]
			li_1=self.fct_li_file_u_information_args_first_two_col(name_file_read=i,nb_comment_lines=1)
			li.append(li_1)
		
		os.chdir(cur_dir)
		
		#li=[ [inform file 1], [information file 2],...] with
		#inform file 1=[ ...., [t_i, legnth queue_1 et t_i],...]	
	
		#from each file we extract its first element which is the time
		li_t=[]
		for i in li:
			li_t.extend(self.fct_li_with_first_elem_of_each_list(val_list=i))
	
		#print("li_t",li_t)
		#li_t may contains the same time values multiple times, that's way we take the union of its elements and we sort them
		li_u_t= self.fct_union_list_elem(val_li_lists=li_t)
		
	
		return[ li_u_t,li]
	

#***************************************************************************************************************************************************************************************** 
	
#***************************************************************************************************************************************************************************************** 
#********************************************************************methods doing the SA of one or  multiple sims***********************************************************
#method doing the statistical analysis of a many sim results, FRes..., placed in a folder
#THE DSU FILE IS EMPLOYED FOR THE NETWORK ONLY, 
#if len(val_li_dsu_files)=1 then the same network is employed for all the sims of which the resutls we want to treat
def fct_stat_anal_multiple_sims(name_folder_FRes,network,v_durat_sim,v_cycle_dur,v_t_end_sim,v_finite_lk_cap,\
v_t_period,v_t_unit,v_t_init,v_veh_final_dest_dynam_construct):
		
			
	cur_dir=os.getcwd()
	os.chdir(name_folder_FRes)
		
	#for each FRes... in the folder we do the stat analysis
	for i in os.listdir('.'):
		if i != ".DS_Store":
			st=Stat_Analysis(val_folder_sim_files_for_stat_anal=i)
				
				
			st.fct_writing_files_sa(val_netw=network,val_dur_sim=v_durat_sim,val_cycle_dur=v_cycle_dur,\
			val_t_end_sim=v_t_end_sim,val_finite_lk_cap=v_finite_lk_cap,\
			val_t_period=v_t_period,\
			val_veh_final_dest_dynam_construct=v_veh_final_dest_dynam_construct,\
			val_name_Fres_folder=i,\
			val_t_unit=v_t_unit,val_t_init=v_t_init)
			
	os.chdir(cur_dir)
					


#*****************************************************************************************************************************************************************************************

#method doing the statistical analysis of files in folder val_name_folder_FRes="SA")

def fct_sa_one_or_series_sim(val_li_dsu_files,val_dur_sim,val_cycle_dur,val_name_folder_FRes,\
va_t_end_sim,va_finite_lk_cap,val_imported_module_dsu_fil,va_t_period,va_t_unit,va_t_init):

	for i in val_li_dsu_files:
		#creation of the network
		cr_netw=Cl_Creation_Network.Creation_Network(val_file_name_user_data=val_li_dsu_files[0])
		
		a=Cl_Decisions.Decisions()
		#val_creation_lis_ques_output_lk_ids=a.fct_exam_construction_li_id_output_links_of_all_queues_on_a_link(val_imported_module_dsu_file=\
		#val_imported_module_dsu_fil)
		#v_network=cr_netw.function_creation_network(val_creation_li_ques_output_lk_ids=val_creation_lis_ques_output_lk_ids)
		v_network=cr_netw.function_creation_network()
	
		if val_imported_module_dsu_fil.val_type_veh_final_dest==Cl_Decisions.TYPE_VEHICLE_FINAL_DESTINATION_AND_PATH["dynamically_defined"]:
			v_veh_fin_dest_dyn_constructed=1
		else:
			v_veh_fin_dest_dyn_constructed=0
			
		#we create all the files for each sim
		fct_stat_anal_multiple_sims(name_folder_FRes=val_name_folder_FRes,network=v_network,v_durat_sim=val_dur_sim,\
		v_cycle_dur=val_cycle_dur,v_t_end_sim=va_t_end_sim,v_finite_lk_cap=va_finite_lk_cap,\
		v_t_period=va_t_period,v_t_unit=va_t_unit,v_t_init=va_t_init,v_veh_final_dest_dynam_construct=v_veh_fin_dest_dyn_constructed)
			


#***************************************************************************************************************************************************************************************** 
#method writing in a file the  weighted mean and the standard deviation of a series of sims
def fct_write_file_wm_sd_series_sims(name_folder_FRes_series_sims,name_file_write,nb_comment_lines=1):

	

	cur_dir=os.getcwd()
	#folder_fres_ser_sim = folder with FRes.. files, ex "SA"
	os.chdir(name_folder_FRes_series_sims)
	
	
	
	
	li=[]
	for i in os.listdir('.'):
		#for each Fres file
		os.chdir(i)
		file=open("Stat_Anal/fi_mean_length_sum_ques")
		ind=0
		for j in file.readlines():
			ind+=1
			if ind>nb_comment_lines:
				#weighted mean, stan dev, wm-sd,wm+sd
				a=j.split()
				li.append([eval(a[0]),eval(a[1])])
				
		os.chdir(cur_dir)
		os.chdir(name_folder_FRes_series_sims)
		file.close()
		
	os.chdir(cur_dir)
	file1=open(name_folder_FRes_series_sims+"/"+name_file_write,"w")
	file1.write("%s\t %s \n"%("WEIGHTED MEAN (1)", "STAN. DEV (2)"))
	for i in li:
		file1.write("%.2f\t %.2f\t \n"%(i[0],i[1]))
	file1.close()
	
#*****************************************************************************************************************************************************************************************
#method writing in a file the  weighted mean and the standard deviation of a series of sims
def fct_write_file_wm_sd_and_mean_trav_time_series_sims(name_folder_FRes_series_sims,name_file_write,name_file_write2,\
nb_comment_lines=1):

	cur_dir=os.getcwd()
	#folder_fres_ser_sim = folder with FRes.. files, ex "SA"
	os.chdir(name_folder_FRes_series_sims)
	
	li=[]
	di_key_movm_val_mean_tr_t_nb_veh={}
	for i in os.listdir('.'):
		#print(i)
		#for each Fres file
		if i !=".DS_Store":
			os.chdir(i)
			file=open("Stat_Anal/fi_mean_length_sum_ques")
			ind=0
			for j in file.readlines():
				ind+=1
				if ind>nb_comment_lines:
					#weighted mean, stan dev, wm-sd,wm+sd
					a=j.split()
					li.append([eval(a[0]),eval(a[1])])
				
			file2=open("Stat_Anal/MEAN_TR_TIME_EN_EX_LK/fi_mean_trav_time_entry_exit_lk.txt")
			ind1=0
			for n in file2.readlines():
				ind1+=1
				if ind1>nb_comment_lines:
					a1=n.split()
				
					if (eval(a1[0]),eval(a1[1])) not in di_key_movm_val_mean_tr_t_nb_veh.keys():
						di_key_movm_val_mean_tr_t_nb_veh[eval(a1[0]),eval(a1[1])]=[[eval(a1[2]),eval(a1[3])]]
				
					else:
						di_key_movm_val_mean_tr_t_nb_veh[eval(a1[0]),eval(a1[1])].append([eval(a1[2]),eval(a1[3])])
						#print("HERE",di_key_movm_val_mean_tr_t_nb_veh[eval(a1[0]),eval(a1[1])])
					
			os.chdir(cur_dir)
			os.chdir(name_folder_FRes_series_sims)
			file.close()
			file2.close()
	
	#print("di_key_movm_val_mean_tr_t_nb_veh",di_key_movm_val_mean_tr_t_nb_veh)	
	#print()
	#print("li",li)
	
	di=Global_Functions.fct_calcul_mean_trav_time_and_nb_dep_veh_series_sims(dict_inf=di_key_movm_val_mean_tr_t_nb_veh)
		
	os.chdir(cur_dir)
	file1=open(name_folder_FRes_series_sims+"/"+name_file_write,"w")
	file1.write("%s\t %s \n"%("WEIGHTED MEAN SER (1)", "STAN. DEV SER (2)"))
	for i in li:
		file1.write("%.2f\t %.2f\t \n"%(i[0],i[1]))
	file1.close()
	
	file3=open(name_folder_FRes_series_sims+"/"+name_file_write2,"w")
	file3.write("%s\t %s\t %s\t %s \n"%("ID ENTRY LK (1)","ID EXIT LINK (2)","MEAN TRAVEL TIME SER (3)", "MEAN NB DEPART VEH SERIES (4)"))
	
	for i in di:
		file3.write("%d\t %d\t %.2f\t %.2f\t \n"%(i[0],i[1],di[i][0],di[i][1]))
	file1.close()
	
	
#*****************************************************************************************************************************************************************************************
#method writing the  mean travel time per period between entry exit link of a series of sims
#name_folder_FRes_series_sims=Series_Sim....
def fct_write_mean_trav_time_per_period_series_sims(name_folder_FRes_series_sims,val_name_Dsu_file,\
val_t_period,val_t_unit,val_round_prec,va_lis_phrases,va_initial_inter,va_ti_init):


	cur_dir=os.getcwd()
	#folder_fres_ser_sim = folder with FRes.. files, ex "SA"
	os.chdir(name_folder_FRes_series_sims)
	
	
	module_Dsu=__import__(val_name_Dsu_file)

	for i in os.listdir('.'):
		#sprint(i)
		#for each Fres file
		if i !=".DS_Store" and i !="fi_max_min_size_sum_ques_series_sims.txt" and i !="fi_max_size_each_sum_ques_series_sims.txt"\
		and i!="fi_mean_tr_t_nb_dep_veh_series_sims" and i!="fi_wm_sd_series_sim":
			
			#creation of a Stat Anal object
			a=Stat_Analysis(i)
			
			
			a.fct_calcul_and_write_travel_time_per_time_period_entry_exit_lk(\
			va_sim_dur=module_Dsu.t_simulation_duration,va_t_period=val_t_period,va_t_unit=val_t_unit,\
			va_round_prec=val_round_prec,va_lis_phrases=va_lis_phrases,va_init_interval=va_initial_inter,va_t_init=va_ti_init)	
								
			os.chdir(cur_dir)
			os.chdir(name_folder_FRes_series_sims)
			
	
		
	
#*****************************************************************************************************************************************************************************************

#method writing the max value of the sum of the queues for each sim
def fct_write_file_max_min_value_sum_ques_series_sims(name_folder_FRes_series_sims,name_file_write,name_file_write_1):

	cur_dir=os.getcwd()
	os.chdir(name_folder_FRes_series_sims)
	
	li=[]
	for i in os.listdir('.'):
		if i!="fi_mean_tr_t_nb_dep_veh_series_sims" and i!="fi_wm_sd_series_sim" and i!="wm-sd-series-sims.gif" and i!=".DS_Store":
			#print(i)
			#import sys
			#sys.exit()
			os.chdir(i)
			file=open("Stat_Anal/QUE_EVOL_SUM/fi_sum_evol_que.txt","r")
		
		
			li_1=[]
		
			#each line is: time, queue size
			for i in file.readlines():
				a=i.rsplit()
			
				li_1.append(eval(a[1]))
		
		
			li.append(max(li_1))
			file.close()
		os.chdir(cur_dir)
		os.chdir(name_folder_FRes_series_sims)
		#file.close()
		
	os.chdir(cur_dir)
	file1=open(name_folder_FRes_series_sims+"/"+name_file_write,"w")
	file1.write("%s\ \n"%("MAX LENGTH  EACH SUM QUE"))
	for i in li:
		file1.write("%.2f \n"%(i))
	file1.close()
	file2=open(name_folder_FRes_series_sims+"/"+name_file_write_1,"w")
	file2.write("%s\t  %s \n"%("MIN OF MAX LENGTH SUM QUES(1)","MAX LENGTH SUM QUES(2)"))
	a=min(li)
	b=max(li)
	file2.write("%.2f\t %.2f \n"%(a,b))
	file2.close()
	
	
#*****************************************************************************************************************************************************************************************





#the "Dsu_1" is employed for defing the network employed and the sim duration. 
#This info has to  be the same for all the sims  of a series.
#If we do  series of sims we can still employe the Dsu file of the 1st sim, since they are all employing the same network.
#ATTENTIOJN ALL THE SIMS OF THE SERIES SHOULD HAVE THE SAME VALUES IN THE DSU COCNERNING THE CYCLE DURATION  AND
#TYPE VEH FINAL DESTINATION, FINAL CAPACITY INTERNAL LINK
val_li_dsu_fi=["Dsu_1"]
module_Dsu=__import__("Dsu_1")
module_file_stat_anal_folders_and_files=__import__(File_Sim_Name_Module_Files.val_name_file_stat_anal_folders_and_files)

val_name_fol_FRes="S_FT_stab_dem_0.6partout"




#anal stat classique, on appelle fcts, fct_sa_one_or_series_sim,fct_write_file_wm_sd_and_mean_trav_time_series_sims,\
#fct_write_file_max_min_value_sum_ques_series_sims
val_t_start_sim=0
val_sim_dur=module_Dsu.t_simulation_duration
val_fin_sim=round(val_t_start_sim+val_sim_dur,2)

val_ti_period=300
val_ti_unit=0.1
val_round_precis=2
va_init_interval=0

#the start time of the sim.  IF A PREVIOUS SIM IS CONTINUED IT HAS TO USE THE T START OF THE SIM, OR THE T_END+T_UNIT
#OF THE PREVIOUS SIM
va_t_init=0

#print(val_fin_sim)
fct_sa_one_or_series_sim(val_li_dsu_files=val_li_dsu_fi,val_dur_sim=module_Dsu.t_simulation_duration,\
val_cycle_dur=module_Dsu.cycle_duration,\
val_name_folder_FRes=val_name_fol_FRes,\
va_t_end_sim=val_fin_sim,\
va_finite_lk_cap=module_Dsu.val_finite_capacity_internal_links,\
val_imported_module_dsu_fil=module_Dsu,\
va_t_period=val_ti_period,va_t_unit=val_ti_unit,va_t_init=va_t_init)

########
#fct_write_file_wm_sd_series_sims(name_folder_FRes_series_sims=val_name_fol_FRes,\
#name_file_write=module_file_stat_anal_folders_and_files.val_name_file_wm_sd_series_sim,nb_comment_lines=1)
########

fct_write_file_wm_sd_and_mean_trav_time_series_sims(name_folder_FRes_series_sims=val_name_fol_FRes,\
name_file_write=module_file_stat_anal_folders_and_files.val_name_file_wm_sd_series_sim,
name_file_write2=module_file_stat_anal_folders_and_files.val_name_file_mean_tr_t_nb_dep_veh_series_sims,nb_comment_lines=1)


fct_write_file_max_min_value_sum_ques_series_sims(name_folder_FRes_series_sims=val_name_fol_FRes,\
name_file_write=module_file_stat_anal_folders_and_files.val_name_file_max_size_each_sum_ques_series_sims,\
name_file_write_1=module_file_stat_anal_folders_and_files.val_name_file_max_min_size_sum_ques_series_sim)







###################################





#val_name_folder_FRes_series_sims="S_MP_10_ESTIM_TR_SD"
#val_name_Dsu_fi="Dsu_1"
#val_ti_period=300
#val_ti_period=120
#val_ti_unit=0.1
#val_round_precis=2
#va_init_interval=0

#the start time of the sim.  IF A PREVIOUS SIM IS CONTINUED IT HAS TO USE THE T START OF THE SIM, OR THE T_END+T_UNIT
#OF THE PREVIOUS SIM
#va_t_init=0
#va_li_phrases=["1st line=(id entry lk,  id exit link),other lines:  < time value (1st column), mean travel time, total nb veh  (2nd column) "]


#fct_write_mean_trav_time_per_period_series_sims(name_folder_FRes_series_sims=val_name_folder_FRes_series_sims,\
#val_name_Dsu_file=val_name_Dsu_fi,\
#val_t_period=val_ti_period,val_t_unit=val_ti_unit,val_round_prec=val_round_precis,va_lis_phrases=va_li_phrases,
#va_ti_init=va_t_init)




####################

#a=Stat_Analysis(val_folder_sim_files_for_stat_anal="Series_Sim-Wed-22-May-2013_11-42-52/FRes-Wed-22-May-2013_11-42-52")

#v_li_phrases=["veh id (1st col), t_ap_ar (2nd col), t_join_que (3rd col), t_start_dep_que (4th col), t_ar_next_lk (5th col), que  size at t_join_que (6th col)"]
#v_li_phrases_2=["veh id (1st col), t_ap_ar (2nd col), t_ar_next_lk (3rd col), T=t_ar_next_lk - t_ap_ar (4th col), veh ID (5th colm)"]
#v_li_phrases_3=["t_ap_ar (1st col), T=t_ar_next_lk - t_ap_ar (2nd col), veh ID (3rd colm)"]
#v_li_phrases_4=["t_ar_next_lk (1st col), T=t_ar_next_lk - t_ap_ar (2nd col),veh ID (3rd colm)"]
#v_li_phrases_5=["que size met by veh arrival at que (1st col), T=t_ar_next_lk - t_ap_ar (2nd col),veh ID (3rd colm)"]
#val_round_precision=2



#a.fct_calcul_and_write_history_link_veh_ar_ap_departs_and_que_size_given_que(val_id_origin_link=8,\
#val_id_destination_link=9,\
#va_name_file_to_write=File_Stats_Anal_Folders_And_Files.name_file_history_veh_ar_ap_dep_and_quesize_que,\
#val_name_file_to_write_second_dict=File_Stats_Anal_Folders_And_Files.name_file_history_veh_t_cur_and_next_ar_que,\
#val_name_file_to_write_second_dict_1=File_Stats_Anal_Folders_And_Files.name_file_history_veh_t_ar_t_trav_time_que,\
#val_name_file_to_write_third_dict=File_Stats_Anal_Folders_And_Files.name_file_history_veh_t_ar_next_lk_t_trav_time_que,\
#val_name_file_to_write_fourth_dict=File_Stats_Anal_Folders_And_Files.name_file_history_veh_que_size_t_ar_next_lk_t_trav_time_que,\
#va_li_phrases=v_li_phrases,va_li_phrases_2=v_li_phrases_2,\
#va_li_phrases_3=v_li_phrases_3,va_li_phrases_4=v_li_phrases_4,va_li_phrases_5=v_li_phrases_5,va_round_precision=val_round_precision)





