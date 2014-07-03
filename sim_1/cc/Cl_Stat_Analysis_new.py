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


    # the file with the names of the folders and files for the stat analysis, "File_Stats_Anal_Folders_And_Files"
    self._file_stats_name_files = File_Sim_Name_Module_Files.val_name_file_stat_anal_folders_and_files

    #the module importing the file with the names of folders/files for the stat anaylis
    self._module_name_importing_file_names_stat_anal = __import__(self._file_stats_name_files)


    #the file name with  the file names for the recording during the sim,"Record_and_Treat_Sim_File_Names"
    self._file_name_record_and_sim_treat_files = File_Sim_Name_Module_Files.val_name_file_record_and_sim_treat_files


    #the module importing the file with the file names for the recording during the sim
    self._module_name_importing_file_name_record_and_sim_treat_files = __import__(
      self._file_name_record_and_sim_treat_files)


    #the  folder containing the files produced by the desired analysing sim
    #for ex "./FRes-Mon-10-Sep-2012_23-04-37"
    self._folder_sim_files_for_stat_anal = val_folder_sim_files_for_stat_anal


    #the folder where will be placed the folders with the various files produced by the stat analysis
    os.mkdir(
      self._folder_sim_files_for_stat_anal + "/" + self._module_name_importing_file_names_stat_anal.name_folder_stat_anal)

    self._folder_stat_anal = self._folder_sim_files_for_stat_anal + "/" + \
                             self._module_name_importing_file_names_stat_anal.name_folder_stat_anal

    #the db file produced by the sim,  "file_recording_event_db.txt"
    self._db_file = self._folder_sim_files_for_stat_anal + "/" + self._module_name_importing_file_name_record_and_sim_treat_files. \
      val_name_file_recording_event_db

    #a Treatment_Sim_Res objet
    self._treat_sim_res_obj = Cl_Treatment_Sim_Res.Treatment_Sim_Res(val_db_file_sim_res_to_treat=self._db_file)

    #the folder with the vehicle information Sim_Treat
    #self._folder_veh_info=self._folder_sim_files_for_stat_anal+"/"+self._module_name_importing_file_name_record_and_sim_treat_files.\
    #val_name_folder_with_files_created_by_sim_treat

    #File_Sim_Name_Module_Files.val_name_file_record_and_sim_treat_files.\
    #val_name_file_recording_event_db

    #the folder where to add the files containg the evolution of each queue, during the analysed  sim,
    #"/FRes-Mon-10-Sep-2012_23-04-37/QUE_EVOL"
    os.mkdir(self._folder_stat_anal + "/" + \
             self._module_name_importing_file_names_stat_anal.name_folder_queue_evol)

    self._folder_que_evol_files = self._folder_stat_anal + "/" + \
                                  self._module_name_importing_file_names_stat_anal.name_folder_queue_evol



    #the file to write the res (already placed in the correct directory)
    #/FRes-Mon-10-Sep-2012_23-04-37/QUE_EVOL/"fi_evol_que_"
    self._file_to_write_que_res = self._folder_que_evol_files + "/" + self._module_name_importing_file_names_stat_anal. \
      name_file_queue_evol

    #****************** test with more info for each veh que **************************

    #the folder where to add the files containg the evolution of each queue, during the analysed  sim,
    #"/FRes-Mon-10-Sep-2012_23-04-37/QUE_EVOL"
    #os.mkdir(self._folder_stat_anal+"/"+\
    #self._module_name_importing_file_names_stat_anal.name_folder_queue_evol_1)
    os.mkdir(self._folder_sim_files_for_stat_anal + "/" + \
             self._module_name_importing_file_names_stat_anal.name_folder_queue_evol_1)


    #self._folder_que_evol_files_1=self._folder_stat_anal+"/"+\
    #self._module_name_importing_file_names_stat_anal.name_folder_queue_evol_1
    self._folder_que_evol_files_1 = self._folder_sim_files_for_stat_anal + "/" + \
                                    self._module_name_importing_file_names_stat_anal.name_folder_queue_evol_1

    self._file_to_write_que_res_1 = self._folder_que_evol_files_1 + "/" + self._module_name_importing_file_names_stat_anal. \
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
    os.mkdir(self._folder_stat_anal + "/" + \
             self._module_name_importing_file_names_stat_anal.name_folder_nb_times_with_nb_veh_dep_que)

    self._folder_nb_times_with_nb_veh_dep_que = self._folder_stat_anal + "/" + \
                                                self._module_name_importing_file_names_stat_anal.name_folder_nb_times_with_nb_veh_dep_que

    #the file with the number of depart vehicles from the queue and the number of times, (already placed in the correct directory)
    #"FRes-Mon-10-Sep-2012_23-04-37/QUE_NB_TIMES_NB_VEH_DEP/fi_nb_veh_dep_que_"
    self._file_nb_times_with_nb_dep_veh_from_que = self._folder_nb_times_with_nb_veh_dep_que + "/" + \
                                                   self._module_name_importing_file_names_stat_anal.name_file_nb_times_nb_veh_dep_que

    #the folder to add the files with the mean travel time of each entry exit link
    os.mkdir(self._folder_stat_anal + "/" + \
             self._module_name_importing_file_names_stat_anal.name_folder_mean_travel_time_entry_exit_lk)

    self._folder_mean_travel_time_entry_exit_lk = self._folder_stat_anal + "/" + \
                                                  self._module_name_importing_file_names_stat_anal.name_folder_mean_travel_time_entry_exit_lk

    self._file_name_folder_mean_travel_time_entry_exit_lk = self._folder_mean_travel_time_entry_exit_lk + "/" + \
                                                            self._module_name_importing_file_names_stat_anal.name_file_mean_travel_time_entry_exit_lk



    #the file with the mean travel time between entry-exit links
    os.mkdir(self._folder_stat_anal + "/" + \
             self._module_name_importing_file_names_stat_anal.name_folder_traveled_dist_per_period_entry_exit_lk)

    #the folder with the files with the mean traveled distance between entry-exit link per period
    self._name_folder_mean_traveled_distance_per_period_entry_exit_lk = self._folder_stat_anal + "/" + \
                                                                        self._module_name_importing_file_names_stat_anal.name_folder_traveled_dist_per_period_entry_exit_lk

    #the folder to add the files with the evolution of each phase
    os.mkdir(self._folder_stat_anal + "/" + \
             self._module_name_importing_file_names_stat_anal.name_folder_ctrl_evol)

    self._folder_ctrl_evol = self._folder_stat_anal + "/" + \
                             self._module_name_importing_file_names_stat_anal.name_folder_ctrl_evol


    #the folder to add the files with the evolutuon of each stage of each intersection
    os.mkdir(self._folder_stat_anal + "/" + \
             self._module_name_importing_file_names_stat_anal.name_folder_stage_evol_per_intersection)

    self._folder_stage_evol_inters = self._folder_stat_anal + "/" + \
                                     self._module_name_importing_file_names_stat_anal.name_folder_stage_evol_per_intersection

    #the folder to add the files with the evolutuon of each stage type 2 of each intersection
    #os.mkdir(self._folder_stat_anal+"/"+"STAGE_EVOL_NDS")

    #self._folder_stage_evol_nodes=self._folder_stat_anal+"/"+"STAGE_EVOL_nds"


    #the folder with the files indicating  the number ofstage  switches per itnersection node
    os.mkdir(
      self._folder_stat_anal + "/" + self._module_name_importing_file_names_stat_anal.name_folder_stage_switches_per_intersection)

    self._folder_stage_switches_per_intersection = self._folder_stat_anal + "/" + self._module_name_importing_file_names_stat_anal.name_folder_stage_switches_per_intersection




    #the folder to add the files  describing the evolution of each link
    os.mkdir(self._folder_stat_anal + "/" + \
             self._module_name_importing_file_names_stat_anal.name_folder_link_evol)

    self._folder_link_evol = self._folder_stat_anal + "/" + \
                             self._module_name_importing_file_names_stat_anal.name_folder_link_evol

    #the folder to add the files with the queue evolution after each veh departure
    os.mkdir(self._folder_stat_anal + "/" + \
             self._module_name_importing_file_names_stat_anal.name_folder_queue_evol_after_veh_dep)

    self._folder_queue_evol_after_veh_dep = self._folder_stat_anal + "/" + \
                                            self._module_name_importing_file_names_stat_anal.name_folder_queue_evol_after_veh_dep

    #the file with he queue evolution after each veh departure
    self._file_queue_evol_after_veh_dep = self._folder_queue_evol_after_veh_dep + "/" + \
                                          self._module_name_importing_file_names_stat_anal.name_file_queue_evol_after_veh_dep


    # the folder for the sum of all queue values during the sim
    os.mkdir(self._folder_stat_anal + "/" + \
             self._module_name_importing_file_names_stat_anal.name_folder_sum_queues_evol)

    self._folder_sum_queues_evol = self._folder_stat_anal + "/" + \
                                   self._module_name_importing_file_names_stat_anal.name_folder_sum_queues_evol


    #the file with the values of the sum of all queues during sim
    self._file_sum_queue_evol = self._folder_sum_queues_evol + "/" + \
                                self._module_name_importing_file_names_stat_anal.name_file_sum_queue_evol


    #the file with the values of the sum of all queues during sim
    self._file_sum_desired_queue_evol = self._folder_sum_queues_evol + "/" + \
                                        self._module_name_importing_file_names_stat_anal.name_file_sum_desired_queue_evol

    #the folder with the average value of the sum of the queues (sum of queues (t)/total number of vehicle queues)
    os.mkdir(self._folder_stat_anal + "/" + \
             self._module_name_importing_file_names_stat_anal.name_folder_average_sum_queues_evol)

    self.folder_average_sum_queue_evol = self._folder_stat_anal + "/" + \
                                         self._module_name_importing_file_names_stat_anal.name_folder_average_sum_queues_evol

    #the file with the values of the sum of all queues during sim
    self._file_average_sum_queue_evol = self.folder_average_sum_queue_evol + "/" + \
                                        self._module_name_importing_file_names_stat_anal.name_file_average_sum_queue_evol



    #the name of the file with the weighted mean  of the sum of queues
    self._file_mean_length_sum_queues = self._folder_stat_anal + "/" + \
                                        self._module_name_importing_file_names_stat_anal.name_file_mean_length_sum_queues


    #the file containing the number of veh in the sum of queues and the prob of having this number
    self._file_name_file_nb_veh_prob_sum_que = self._folder_stat_anal + "/" + \
                                               self._module_name_importing_file_names_stat_anal.name_file_nb_veh_prob_sum_que

    #the file containing the number of veh in the sum of queues and the prob of having this number
    self._file_name_file_nb_veh_prob_sum_que = self._folder_stat_anal + "/" + \
                                               self._module_name_importing_file_names_stat_anal.name_file_nb_veh_prob_sum_que

    #the folder with the file where the the file with the mean length of each queue is written
    os.mkdir(self._folder_stat_anal + "/" + \
             self._module_name_importing_file_names_stat_anal.name_folder_mean_time_spent_by_veh_in_que)

    self._folder_mean_value_each_queue = self._folder_stat_anal + "/" + \
                                         self._module_name_importing_file_names_stat_anal.name_folder_mean_time_spent_by_veh_in_que



    #the file with the mean  value spent by veh, for every queue
    self._file_mean_time_spent_by_veh_in_que = self._folder_mean_value_each_queue + "/" + \
                                               self._module_name_importing_file_names_stat_anal.name_file_mean_time_spent_by_veh_in_que

    #the file with the mean value of the average time spent by veh in ques
    self._file_mean_of_aver_sojourn_time = self._folder_mean_value_each_queue + "/" + \
                                           self._module_name_importing_file_names_stat_anal.val_name_file_mean_of_aver_sojourn_time

    #thefolder with the average sum of the queues per period (over the nb of t instances within the period)
    os.mkdir(self._folder_stat_anal + "/" + \
             self._module_name_importing_file_names_stat_anal.name_folder_average_sum_ques_per_period_over_nb_t_instances_within_period)

    self._folder_average_sum_ques_per_period = self._folder_stat_anal + "/" + \
                                               self._module_name_importing_file_names_stat_anal.name_folder_average_sum_ques_per_period_over_nb_t_instances_within_period


    #the folder with the veh of trav time evolution per time period, for each entry exit link
    os.mkdir(self._folder_stat_anal + "/" + \
             self._module_name_importing_file_names_stat_anal.name_folder_travel_time_per_period_entry_exit_lk)

    self._folder_travel_time_per_period_entry_exit_lk = self._folder_stat_anal + "/" + \
                                                        self._module_name_importing_file_names_stat_anal.name_folder_travel_time_per_period_entry_exit_lk

    #the file with the trav time evolution per time period, for an entry exit link
    self._file_travel_time_per_period_entry_exit_link = self._folder_travel_time_per_period_entry_exit_lk + "/" + \
                                                        self._module_name_importing_file_names_stat_anal.name_file_travel_time_per_period_entry_exit_link


    #the folder with the files with the total actuation duration per period of each phase
    os.mkdir(self._folder_stat_anal + "/" + \
             self._module_name_importing_file_names_stat_anal.name_folder_phase_act_durat_per_period)

    self._folder_phase_act_durat_per_period = self._folder_stat_anal + "/" + \
                                              self._module_name_importing_file_names_stat_anal.name_folder_phase_act_durat_per_period


  # *****************************************************************************************************************************************************************************************	

  #method returning the file with the names of the folders and files for the stat analysis
  def get_file_stats_name_files(self):
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
  #method returning the file with the values of the sum of the desired l queues during sim
  def get_file_sum_desired_queue_evo(self):
    return self._file_sum_desired_queue_evo

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
  def set_file_stats_name_files(self, n_v):
    self._file_stats_name_files = n_v

  #*****************************************************************************************************************************************************************************************
  #method modifying  the folder with the files  describing the evolution of each link
  def set_folder_link_evol(self, n_v):
    self._folder_link_evol = n_v

  #*****************************************************************************************************************************************************************************************
  #method modifying the name of the folder with the files  describing the evolution of each link
  def set_folder_link_evol(self, n_v):
    self._folder_link_evol = n_v

  #*****************************************************************************************************************************************************************************************
  #method modifying the the module importing the file with the names of folders/files for the stat anaylis
  def set_module_name_importing_file_names_stat_anal(self, n_v):
    self._module_name_importing_file_names_stat_anal = n_v

  #*****************************************************************************************************************************************************************************************
  #method modifying the folder containing the files for the stat analysis
  def set_folder_stat_anal(self, n_v):
    self._folder_stat_anal = n_v

  #*****************************************************************************************************************************************************************************************
  #method modifying the db file produced by the sim,  "file_recording_event_db.txt"
  def set_db_file(self, n_v):
    self._db_file = n_v

  #*****************************************************************************************************************************************************************************************
  #method returning the treat_sim_res object
  def set_treat_sim_res_obj(self, n_v):
    self._treat_sim_res_obj = n_v

  #*****************************************************************************************************************************************************************************************
  #method modifying the folder with the veh information
  #def set_folder_veh_info(self,n_v):
  #self._folder_veh_info=n-v
  #*****************************************************************************************************************************************************************************************

  #method modifying the  file name with  the file names for the recording during the sim
  def set_file_name_record_and_sim_treat_files(self, n_v):
    self._file_name_record_and_sim_treat_files = n_v

  #*****************************************************************************************************************************************************************************************
  #method modifying the module importing the file with the file names for the recording during the sim
  def set_module_name_importing_file_name_record_and_sim_treat_files(self, n_v):
    self._module_name_importing_file_name_record_and_sim_treat_files = n_v

  #*****************************************************************************************************************************************************************************************
  #method modifying the   folder where the sim results, wished to be treated are recorded
  def set_folder_sim_files_for_stat_anal(self, n_v):
    self._folder_sim_files_for_stat_anal = n_v

  #*****************************************************************************************************************************************************************************************
  #method modifying the the folder where to add the files containg the evolution of each queue, during the analysed  sim
  def set_folder_que_evol_files(self, n_v):
    self._folder_que_evol_files = n_v

  #*****************************************************************************************************************************************************************************************
  #method modifying the file to write the res (already placed in the correct directory)
  def set_file_to_write_que_res(self, n_v):
    self._file_to_write_que_res = n_v

  #*****************************************************************************************************************************************************************************************
  #method modifying the folder where to add the files containg the files with the number of veh in queue after each veh arrival/appearance
  def set_folder_nb_veh_que_ar_ap(self, n_v):
    self._folder_nb_veh_que_ar_ap = n_v

  #*****************************************************************************************************************************************************************************************
  #method modifying the file where to write the queue evol after each veh arrival/appear, (already placed in the correct directory)
  def set_file_to_write_nb_veh_que_ar_ap(self, n_v):
    self._file_to_write_nb_veh_que_ar_ap = n_v

  #*****************************************************************************************************************************************************************************************
  #method modifying folder where to add the files  with the number of departing veh from a que
  def set_folder_nb_veh_dep_que(self, n_v):
    self._folder_nb_veh_dep_que = n_v

  #*****************************************************************************************************************************************************************************************
  #method modifying the file with the number of departing veh from a que (already placed in the correct directory)
  def set_file_nb_veh_dep_que(self, n_v):
    self._file_nb_veh_dep_que = n_v

  #*****************************************************************************************************************************************************************************************

  #method modifying the file to write the queue length during a vehicle arrival or appearance event, already placed in the correct directory)
  def set_file_to_write_que_res_veh_arrival_appear(self, n_v):
    self._file_to_write_que_res_veh_arrival_appear = n_v

  #*****************************************************************************************************************************************************************************************
  #method modifying the file to write the number of vehicles in the queue and the number of times that we had this nb of veh, during the sim
  def set_file_write_nb_veh_ar_ap_queue_nb_times(self, n_v):
    self._file_write_nb_veh_ar_ap_queue_nb_times = n_v

  #*****************************************************************************************************************************************************************************************
  #method modifying the file to write the neumber of departing vehicles of a queue
  def set_file_write_nb_veh_depart_queue_nb(self, n_v):
    self._file_write_nb_veh_depart_queue_nb = n_v

  #*****************************************************************************************************************************************************************************************
  #method modifying the name of the file to write the veh id and the veh travel time
  def set_file_write_veh_id_and_travel_time(self, n_v):
    self._file_write_veh_id_and_travel_time = n_v

  #*****************************************************************************************************************************************************************************************
  #method modifying the folder  where to add the files  with the number of departing vehicles from the queue and the number of times
  def set_folder_nb_times_with_nb_veh_dep_que(self, n_v):
    self._folder_nb_times_with_nb_veh_dep_que = n_v

  #*****************************************************************************************************************************************************************************************
  #method modifying the file with the number of depart vehicles from the queue and the number of times, (already placed in the correct directory)
  def set_file_nb_times_with_nb_dep_veh_from_que(self, n_v):
    self._file_nb_times_with_nb_dep_veh_from_que = n_v

  #*****************************************************************************************************************************************************************************************
  #method modifying the folder to add the files with the mean travel time of each entry exit link
  def set_folder_mean_travel_time_entry_exit_lk(self, n_v):
    self._folder_mean_travel_time_entry_exit_lk = n_v

  #*****************************************************************************************************************************************************************************************
  #method modifying the name of the file with the mean travel time between entry-exit links
  def set_file_name_folder_mean_travel_time_entry_exit_lk(self, n_v):
    self._file_name_folder_mean_travel_time_entry_exit_lk = n_v

  #*****************************************************************************************************************************************************************************************
  #method modifying the name of the folder  to add the files with the queue evolution after each veh departure
  def set_folder_queue_evol_after_veh_dep(self, n_v):
    self._folder_queue_evol_after_veh_dep = n_v

  #*****************************************************************************************************************************************************************************************
  #method modifying the name of the file with he queue evolution after each veh departure
  def set_file_queue_evol_after_veh_dep(self, n_v):
    self._file_queue_evol_after_veh_dep = n_v

  #*****************************************************************************************************************************************************************************************
  #method returning the file with the mean  length of each queue
  def set_file_time_spent_by_veh_in_que(self, n_v):
    self._file_time_spent_by_veh_in_que = n_v

  #*****************************************************************************************************************************************************************************************

  #method modifying the folder for the sum of all queue values during the sim
  def set_folder_sum_queues_evol(self, n_v):
    self._folder_sum_queues_evol = n_v

  #*****************************************************************************************************************************************************************************************
  #method modifying the folder for the average value of the sum of all queue values during the sim
  def set_folder_average_sum_queue_evol(self):
    return self._folder_average_sum_queue_evol

  #*****************************************************************************************************************************************************************************************
  #method modifying the file with the values of the sum of all queues during sim
  def set_file_sum_queue_evol_end_cycle(self, n_v):
    self._file_sum_queue_evol = n_v

  #*****************************************************************************************************************************************************************************************
  #method modifying the file with the values of the sum of the desired l queues during sim
  def set_file_sum_desired_queue_evo(self, n_v):
    self._file_sum_desired_queue_evol = n_v

  #*****************************************************************************************************************************************************************************************

  #method modifying the file with the average values of the sum of all queues during sim
  def set_file_average_sum_queue_evol(self, n_v):
    self._file_average_sum_queue_evol = n_file_average_sum_queue_evo

  #*****************************************************************************************************************************************************************************************
  #method modifying the file with the weighted mean  of the sum of queues
  def set_file_mean_length_sum_queues(self, n_v):
    self._file_mean_length_sum_queues = n_v

  #*****************************************************************************************************************************************************************************************
  #method modifying the name of the folder with the files indicating the number of stage switches per itnersection
  def set_folder_stage_switches_per_intersection(self, n_v):
    self._folder_stage_switches_per_intersection = n_v

  #*****************************************************************************************************************************************************************************************
  #method modifying the file containing the number of veh in the sum of queues and the prob of having this number
  def set_file_name_file_nb_veh_prob_sum_que(self, n_v):
    self._file_name_file_nb_veh_prob_sum_que = n_v

  #*****************************************************************************************************************************************************************************************
  #method modifying the file with the mean  length of each queue
  def set_file_time_spent_by_veh_in_que(self, n_v):
    self._file_time_spent_by_veh_in_que = n_v

  #*****************************************************************************************************************************************************************************************
  #method modifying the folder with the veh of trav time evolution per time period, for each entry exit link
  def set_folder_travel_time_per_period_entry_exit_lk(self, n_v):
    self._folder_travel_time_per_period_entry_exit_lk = n_v

  #*****************************************************************************************************************************************************************************************
  #method modifying the file with the trav time evolution per time period, for an entry exit link
  def set_file_travel_time_per_period_entry_exit_link(self, n_v):
    self._file_travel_time_per_period_entry_exit_link = n_v

  #*****************************************************************************************************************************************************************************************
  #merhod modifying the  folder with the files with the total actuation duration per period of each phase
  def set_folder_phase_act_durat_per_period(self, n_v):
    self._folder_phase_act_durat_per_period = n_v

  #*****************************************************************************************************************************************************************************************
  #method modifying the folder to add the files with the evolutuon of each stage of each intersection
  def set_folder_stage_evol_inters(self, n_v):
    self._folder_stage_evol_inters = n_v

  #*****************************************************************************************************************************************************************************************
  #method modifying the folder with the files with the mean traveled distance between entry-exit link per period
  def set_name_folder_mean_traveled_distance_per_period_entry_exit_lk(self, n_v):
    self._name_folder_mean_traveled_distance_per_period_entry_exit_lk = n_v

  #*****************************************************************************************************************************************************************************************

  #method reading a file with the lengths of a queue and returns the maximum length
  def fct_calcul_max_que_size(self, name_file_read):

    #we open the file
    file = open(name_file_read, "r")

    li = []

    #each line is: time, queue size
    for i in file.readlines():
      a = i.rsplit()

      li.append(eval(a[1]))

    return max(li)


  #***************************************************************************************************************************************************************************************** 
  #method creating a dictionary, key=the movement [l,m]
  #the value=dict, key=time, value= [   [nb of vehicles in the queue,ev type,veh id     ]  ]

  def fct_creat_dict_queue_lengths_during_sim(self, val_network, dict_db_file):

    #print("dict_db_file",dict_db_file[(10003, 10004)][0])


    #for each movement we associate of this event type we exctract the time, the queue id in the form of a movement [l,m], the number of vehicles in the queue at this time
    #dictionary, key = the movement id (l,m), value =[ time, number of vehicles in the queue]
    dict_id_queue = {}

    #for each movement, dict_db_file=dict, key=movement,value=record object
    for i in dict_db_file:
      #print("val_network.get_di_all_links()[i[0]]",val_network.get_di_all_links()[i[0]])

      #if the movement is not a right turn we create the movement and calculate the queue length
      if val_network.get_di_all_links()[i[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()[
        i[0], i[1]].get_type_veh_queue() != \
          Cl_Vehicle_Queue.TYPE_VEHICLE_QUEUE["right_turn"]:

        #we create the associated element of the dictionary to return 
        dict_id_queue[i] = {}
        for j in dict_db_file[i]:
          #if the event we wish to add is of type veh arrival
          if j.get_ev_type() == Cl_Event.TYPE_EV["type_ev_veh_arrived_at_que"] or \
                  j.get_ev_type() == Cl_Event.TYPE_EV["type_ev_veh_appearance"] or \
                  j.get_ev_type() == Cl_Event.TYPE_EV["type_ev_veh_arrived_at_que_nsi"] or \
                  j.get_ev_type() == Cl_Event.TYPE_EV["type_ev_veh_appearance_nsi"]:

            #if the time is not already in the dictionary, then we add
            if j.get_ev_time() not in dict_id_queue[i]:
              dict_id_queue[i][j.get_ev_time()] = [
                [len(j.get_li_id_vehicles_in_queue()), j.get_ev_type(), j.get_vehicle_id()]]

            #if the time is  already in the dictionary, if the existing event is of the same type then we use the new value of the que
            else:
              dict_id_queue[i][j.get_ev_time()].append(
                [len(j.get_li_id_vehicles_in_queue()), j.get_ev_type(), j.get_vehicle_id()])

          #if the event we wish to add is veh end departure
          elif j.get_ev_type() == Cl_Event.TYPE_EV["type_ev_end_veh_departure_from_que"] or \
                  j.get_ev_type() == Cl_Event.TYPE_EV["type_ev_end_veh_departure_from_que_nsi"]:
            #if the time is not already in the dictionary, then we add
            if j.get_ev_time() not in dict_id_queue[i]:
              dict_id_queue[i][j.get_ev_time()] = [
                [len(j.get_li_id_vehicles_in_queue()), j.get_ev_type(), j.get_vehicle_id()]]
            #if the event time is already in the dictionary, we add the event only if the value of the queue length is different
            else:

              if dict_id_queue[i][j.get_ev_time()][len(dict_id_queue[i][j.get_ev_time()]) - 1][0] != len(
                  j.get_li_id_vehicles_in_queue()):
                dict_id_queue[i][j.get_ev_time()].append(
                  [len(j.get_li_id_vehicles_in_queue()), j.get_ev_type(), j.get_vehicle_id()])

          #if the event we wish to add is end  veh hold at que
          elif j.get_ev_type() == Cl_Event.TYPE_EV["ty_ev_end_veh_hold_at_que"] or \
                  j.get_ev_type() == Cl_Event.TYPE_EV["ty_ev_end_veh_hold_at_que_nsi"]:
            pass

          #if the event we wish to add is of any other type
          else:
            print("PROB, CL_STAT, FCT fct_creat_dict_queue_lengths_during_sim, EVENT TYPE TO ADD ", \
                  j.get_ev_type())
            import sys

            sys.exit()

    #print('dic id queue', dict_id_queue)
    return dict_id_queue

  #*****************************************************************************************************************************************************************************************
  #function creating a file for each queue and writing the time, the number of vehicles in the queue, 
  #and the mean value of each phase
  #it returns a dict, key=phase id, value=[list, nb departed veh]
  #list=sorted list regard. time [time, que length, nb veh in que]

  #di_movem=dict, key=time, value=  [..., [nb of vehicles in the queue,ev type,veh id],...   ]
  def fct_writing_file_time_veh_queue_length_and_file_que_length_and_veh_id(self, di_movem):

    #we create a dictionary from the db file created by the sim
    #key=movement [l,m]
    #value=dict, key=time, value=  [ [nb of vehicles in the queue,ev type,veh id     ]   ]
    #di_movem=self.fct_creat_dict_queue_lengths_during_sim(val_network=val_netwk,dict_db_file=di_db_file)



    di_key_mov_val_sorted_li_t_que_length = {}

    #for each movement we create a file
    ind = 1
    for i in di_movem:

      #list [ ...,[t, que length at t],...]
      li_li_t_que_len = []

      #file=open(self._file_to_write_que_res+str(ind)+".txt","w")
      file = open(self._file_to_write_que_res + str(i) + ".txt", "w")
      file.write("%s\t %s \n" % ("QUE", str(i)))
      li_keys = []
      for j in di_movem[i].keys():
        li_keys.append(j)
      #print(li_keys)
      li_keys.sort()
      nb_veh_que_prev_t = 0
      nb_dep_veh = 0
      for k in li_keys:
        for m in di_movem[i][k]:
          li_li_t_que_len.append([k, m[0]])
          #file.write("%d\t %d\t %d\n"%(k,m[0],m[1]))
          file.write("%.1f\t %d\t %d\n" % (k, m[0], m[1]))

          if m[1] == Cl_Event.TYPE_EV["type_ev_end_veh_departure_from_que"] or \
                  m[1] == Cl_Event.TYPE_EV["type_ev_end_veh_departure_from_que_nsi"]:
            nb_dep_veh += nb_veh_que_prev_t - m[0]

          nb_veh_que_prev_t = m[0]


      #print("i=",i,"nb_dep_veh",nb_dep_veh,m[0])			
      nb_dep_veh += m[0]

      di_key_mov_val_sorted_li_t_que_length[i] = [li_li_t_que_len, nb_dep_veh]

      ind += 1
      file.close()
    ind = 1
    for i in di_movem:
      f = open(self._file_to_write_que_res_1 + str(ind) + ".txt", "w")
      f.write("%s\t %s \n" % ("QUE", str(i)))
      f.write("%s\t %s\t %s\t %s \n" % ("TIME(1)", "QUE LEN (2)", "EVENT TYPE (3)", "VEH ID(4)"))
      f.write("%d\t %d \n" % (i[0], i[1]))
      li_keys = []
      for j in di_movem[i].keys():
        li_keys.append(j)
      #print(li_keys)
      li_keys.sort()
      for k in li_keys:
        for m in di_movem[i][k]:
          #f.write("%d\t %d\t %d\t %d \n"%(k,m[0],m[1],m[2]))
          f.write("%.1f\t %d\t %d\t %d \n" % (k, m[0], m[1], m[2]))
      ind += 1
      f.close()
    #print("HERE2",di_key_mov_val_sorted_li_t_que_length)

    return di_key_mov_val_sorted_li_t_que_length

  #file1=open(self._file_mean_queue_length+".txt","w")
  #file1.write("%s\t %s \n"%("QUE", "MEAN LENGTH"))	
  #for j in di_mean_que_length_mov:
  #file1.write("%d\t %d\t %f\n"%(j[0],j[1],di_mean_que_length_mov[j]))
  #file1.close()


  #***************************************************************************************************************************************************************************************** 
  #method computing the distinct time instances at which at least one queue size was modified
  #val_di_que_evol=dict, key=id phase, value=dict, key=time, value=[que size, event type, veh id]
  #it returns a list with the time instances at which at least one que state was modified
  def fct_calcul_li_t_instances_all_que_evol(self, val_di_que_evol):

    li_rep = []

    for i in val_di_que_evol:
      li_1 = list(val_di_que_evol[i])
      li_rep = list(set(li_1) | set(li_rep))
    li_rep.sort()

    return li_rep

  #***************************************************************************************************************************************************************************************** 
  #method computing the distinct time instances at which at least one queue size was modified, from a given set of queues
  #val_di_que_evol=dict, key=id phase, value=dict, key=time, value=[que size, event type, veh id]
  #it returns a list with the time instances at which at least one que state was modified
  #li_id_considered_phases=list with the id of the desired phases, [...,[id input linkn id output link],...]
  def fct_calcul_li_t_instances_some_que_evol(self, val_di_que_evol, li_id_considered_phases):

    li_rep = []
    #print(li_id_considered_phases)
    #print(val_di_que_evol)

    for i in li_id_considered_phases:

      if (i[0], i[1]) in val_di_que_evol:
        li_1 = list(val_di_que_evol[i[0], i[1]])
        li_rep = list(set(li_1) | set(li_rep))
      else:
        print("ATTENTION, NO OBSERVATION FOR QUE", i,)
    li_rep.sort()

    return li_rep

  #*****************************************************************************************************************************************************************************************
  #method returning a dictionary key=id phase, value=[..,[t, queue size],...] with t unique value
  #val_dict_que_evol=dict, key=phasev id,  value=[list,nb_veh], list=[ ..,[t, que size],..]
  #list=sorted list regard. time [time, que length, nb veh in que]
  def fct_creat_dict_que_evol_unique_t_instances(self, val_dict_que_evol):

    #print('val dic:', val_dict_que_evol)
    di_rep = {}
    for i in val_dict_que_evol:
      di_rep[i] = []
      nb_o = len(val_dict_que_evol[i][0])
      for j in range(nb_o):
        #if the next obesr exists
        if j + 1 != nb_o:
          if val_dict_que_evol[i][0][j][0] != val_dict_que_evol[i][0][j + 1][0]:
            di_rep[i].append([val_dict_que_evol[i][0][j][0], val_dict_que_evol[i][0][j][1]])

        #if the next observ does not exist
        else:

          #if the  observ time does not belong to the list
          if val_dict_que_evol[i][0][j][0] != di_rep[i][-1][0]:
          	di_rep[i].append([val_dict_que_evol[i][0][j][0], val_dict_que_evol[i][0][j][1]])

    return di_rep

  #*****************************************************************************************************************************************************************************************
  #method returning a dictionary key=id phase, value=[..,[t, queue size],...] with t unique value
  #val_dict_que_evol=dict, key=phasev id,  value=[list,nb_veh], list=[ ..,[t, que size],..]
  #list=sorted list regard. time [time, que length, nb veh in que]
  #li_id_considered_phases=list with the id of the desired phases, [...,[id input linkn id output link],...]
  def fct_creat_dict_some_que_evol_unique_t_instances(self, val_dict_que_evol, li_id_considered_phases):

    di_rep = {}
    for i in li_id_considered_phases:
      if (i[0], i[1]) in val_dict_que_evol:
        di_rep[i[0], i[1]] = []
        nb_o = len(val_dict_que_evol[i[0], i[1]][0])
        for j in range(nb_o):
          #if the next obesr exists
          if j + 1 != nb_o:
            if val_dict_que_evol[i[0], i[1]][0][j][0] != val_dict_que_evol[i[0], i[1]][0][j + 1][0]:
              di_rep[i[0], i[1]].append(
                [val_dict_que_evol[i[0], i[1]][0][j][0], val_dict_que_evol[i[0], i[1]][0][j][1]])

          #if the next observ does not exist
          else:

            #if the  observ time does not belong to the list
            if val_dict_que_evol[i[0], i[1]][0][j][0] != di_rep[i[0], i[1]][-1][0]:
              di_rep[i[0], i[1]].append(
                [val_dict_que_evol[i[0], i[1]][0][j][0], val_dict_que_evol[i[0], i[1]][0][j][1]])

    return di_rep

  #*****************************************************************************************************************************************************************************************
  #method calculating the sum of	all the queues
  #it returns a list [..[t, sum of ques],...]
  #val_di_key_id_phase_val_di_key_time_val_li_info)=dict, key=id phase, value=dict, key=time, value=[que size, event type, veh id]
  #val_di_que_evol_t_unique=dict, key=phasev id,  value=[list,nb_veh], list=[ ..,[t, que size],..]
  def fct_sum_all_queues(self, val_di_key_id_phase_val_di_key_time_val_li_info, val_di_que_evol_t_unique):

    li_rep = []

    #li_t=list [..., t at which at least one que state chenged,...]
    li_t = self.fct_calcul_li_t_instances_all_que_evol(val_di_que_evol=val_di_key_id_phase_val_di_key_time_val_li_info)

    #for each time 
    for i in li_t:
      val_s_at_t = 0

      #for each que
      for j in val_di_que_evol_t_unique:

        nb_times = len(val_di_que_evol_t_unique[j])

        #for each observed instance
        for k in range(nb_times):

          #if the considered time is inferior to the observed time
          if i < val_di_que_evol_t_unique[j][k][0]:
            #if we are not in the first observ
            if k > 0:
              val_s_at_t += val_di_que_evol_t_unique[j][k - 1][1]
              break

            #if we are in the first observation
            else:
              break
          #if the considered time equals to the observed time
          elif i == val_di_que_evol_t_unique[j][k][0]:
            val_s_at_t += val_di_que_evol_t_unique[j][k][1]
            break
          #if the considered time is superior to the observed one 
          else:
            if k + 1 == nb_times:
              val_s_at_t += val_di_que_evol_t_unique[j][k][1]

      li_rep.append([i, val_s_at_t])

    return li_rep

  #***************************************************************************************************************************************************************************************** 
  #method calculating the sum of	somel the queues
  #it returns a list [..[t, sum of ques],...]

  #val_di_que_evol_t_unique=dict, key=phasev id,  value=[list,nb_veh], list=[ ..,[t, que size],..] for the desirerd queeus
  #li_t=list [..., t at which at least one que state chenged,...] for the desired queeus 
  def fct_sum_some_queues(self, val_di_que_evol_t_unique, li_t):

    li_rep = []

    #li_t=list [..., t at which at least one que state chenged,...]
    #li_t=self.fct_calcul_li_t_instances_all_que_evol(val_di_que_evol=val_di_key_id_phase_val_di_key_time_val_li_info)

    #for each time 
    for i in li_t:
      val_s_at_t = 0

      #for each que
      for j in val_di_que_evol_t_unique:

        nb_times = len(val_di_que_evol_t_unique[j])

        #for each observed instance
        for k in range(nb_times):

          #if the considered time is inferior to the observed time
          if i < val_di_que_evol_t_unique[j][k][0]:
            #if we are not in the first observ
            if k > 0:
              val_s_at_t += val_di_que_evol_t_unique[j][k - 1][1]
              break

            #if we are in the first observation
            else:
              break
          #if the considered time equals to the observed time
          elif i == val_di_que_evol_t_unique[j][k][0]:
            val_s_at_t += val_di_que_evol_t_unique[j][k][1]
            break
          #if the considered time is superior to the observed one 
          else:
            if k + 1 == nb_times:
              val_s_at_t += val_di_que_evol_t_unique[j][k][1]

      li_rep.append([i, val_s_at_t])

    return li_rep

  #***************************************************************************************************************************************************************************************** 
  #method writing a file with the sum of all queues during sim.
  #this method also returns the lsit with the sum of the queues
  #li=list with  [.., [t, sum of queues],...]
  def fct_write_file_sum_que_t_sim(self, li, val_name_file_write):

    #list with  [.., [t, sum of queues],...]
    #li=self.fct_calcul_sum_que_t_sim(val_path_list_files=self._folder_que_evol_files)

    file = open(val_name_file_write + ".txt", "w")
    for i in li:
      #file.write("%d\t %d \n"%(i[0],i[1]))
      file.write("%.1f\t %d \n" % (i[0], i[1]))
    file.close()

  #return li

  #***************************************************************************************************************************************************************************************** 	
  #method computing the average sum of the queues per given period
  #v_li_sum_ques==[...,[time, queue value],...]
  #it returns a dict,  key=[ t start period, t end period], valu = mean value of the sum of the queues 
  def fct_calcul_average_sum_que_per_period(self, v_li_sum_ques, v_sim_dur, v_t_period, v_t_unit, v_t_init):


    #v_li_sum_ques=[...,[time, queue value],...]

    di_rep = {}
    t_start_period = 0

    som = 0
    nb_val = 0

    for i in v_li_sum_ques:

      #calcul of the corresponding number of period cotnaining time
      nb_period = math.floor(i[0] / v_t_period) + 1

      #calcul  of the t_start of the interval containing time
      t_start_interval = (nb_period - 1) * v_t_period

      #if the t_start_interval = t_start_period
      if t_start_interval == t_start_period:

        som += i[1]
        nb_val += 1



      #if the t_start_interval is different from the  t_start_period
      else:

        #calcul of the t_end of the itnerval

        t_end_period_prec = (nb_period - 1) * v_t_period - v_t_unit

        #calcul of the mean value of the sum 
        moy = som / nb_val

        di_rep[t_start_period, t_end_period_prec] = moy

        t_start_period = t_start_interval
        som = i[1]
        nb_val = 1

    #print(di_rep)
    #import sys
    #sys.exit()
    return di_rep

  #*****************************************************************************************************************************************************************************************
  #method  writing the file with the average sum of queues per period (average over the number of the time instances belonging in each period)
  def fct_write_average_sum_ques_per_period_over_nb_t_instances_within_period(self, va_li_sum_ques, va_sim_dur,
                                                                              va_t_period, va_t_unit, va_t_init, \
                                                                              val_name_file, val_li_phrases=[
        "t start/t end period, avearage value of the sum of the queues"]):

    #di= dict, key=[ t start period, t end period], valu = mean value of the sum of the queues 
    di = self.fct_calcul_average_sum_que_per_period(v_li_sum_ques=va_li_sum_ques, v_sim_dur=va_sim_dur,
                                                    v_t_period=va_t_period, v_t_unit=va_t_unit, v_t_init=va_t_init)

    li_sorted_t = list(di.keys())

    li_sorted_t.sort()

    file = open(self._folder_average_sum_ques_per_period + "/" + val_name_file, "w")

    for i in val_li_phrases:
      file.write("%s\t \n" % (i))

    for j in li_sorted_t:
      file.write("%s\t %.2f \n" % (j[0], di[j]))
      file.write("%s\t %.2f \n" % (j[1], di[j]))

    file.close()


  #***************************************************************************************************************************************************************************************** 
  #method returning a dictionary, key id node, value=dict, key = stage id, value=[...,[t,  indicator node if the  stage is actuates/0 otherwise],...]
  #val_dict_ev_type=dict, key=event type, value= record object
  def fct_creat_di_evolution_stage_actuation(self, val_dict_ev_type, val_t_unit):


    di_rep = {}

    #di_nb_nb=dict, key=node id, value=1 for the the first node, ..., i for the ith node, so it will be a distance between the plots of the stages for different nodes
    di_nb_nb = {}


    #di_nd=dict, key=id node, value=[...[t_start actuat of a stage, t_end actuat of a stage],..]
    di_nd = {}

    for i in val_dict_ev_type[Cl_Event.TYPE_EV["type_ev_new_intersection_control"]]:

      #if the node id is in the dict
      if i.get_id_inters_node() in di_rep:
        #if the actuated stage is in the diction
        if i.get_id_actuated_stage() in di_rep[i.get_id_inters_node()]:

          di_rep[i.get_id_inters_node()][i.get_id_actuated_stage()].append(
            [i.get_t_start_current_inters_control(), i.get_t_end_current_intersection_control(),
             di_nb_nb[i.get_id_inters_node()]])

        #if the actuated stage is not in the dict
        else:
          di = {}
          di[i.get_id_actuated_stage()] = [
            [i.get_t_start_current_inters_control(), i.get_t_end_current_intersection_control(),
             di_nb_nb[i.get_id_inters_node()]]]
          di_rep[i.get_id_inters_node()].update(di)

        di_nd[i.get_id_inters_node()].append(
          [i.get_t_start_current_inters_control(), i.get_t_end_current_intersection_control()])

      #if the node id is not in the diction
      else:

        di_nb_nb[i.get_id_inters_node()] = i.get_id_inters_node()

        di_rep[i.get_id_inters_node()] = {}
        di = {}
        di[i.get_id_actuated_stage()] = [
          [i.get_t_start_current_inters_control(), i.get_t_end_current_intersection_control(),
           di_nb_nb[i.get_id_inters_node()]]]
        di_rep[i.get_id_inters_node()].update(di)

        di_nd[i.get_id_inters_node()] = [
          [i.get_t_start_current_inters_control(), i.get_t_end_current_intersection_control()]]

    #for each node		
    for m in di_nd:
      #for eac act period 
      for n in di_nd[m]:
        r = [n[0], n[1], di_nb_nb[m]]
        #if an act period is not in the dict of each stage we add it with 0 in order to show that during this period the current stage is not actuated
        for p in di_rep[m]:
          if r not in di_rep[m][p]:
            q = [n[0], n[1], 0]
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

    di_rep_2 = {}

    #for each node
    for f in di_rep:
      di_rep_2[f] = {}

      di = {}
      #for each stage
      for g in di_rep[f]:
        di[g] = []
        #for each period
        for p in di_rep[f][g]:
          di[g].append([p[0], p[2]])
          di[g].append([p[1], p[2]])

        di_rep_2[f].update(di)

    #for each node
    for t in di_rep_2:
      #for each stage
      for z in di_rep_2[t]:
        #we sort the times
        di_rep_2[t][z].sort()

    di_rep_3 = {}

    #for each node		
    for h in di_rep_2:
      di_rep_3[h] = {}
      #for each stage of the node
      for e in di_rep_2[h]:

        di_rep_3[h][e] = []
        #di_rep_2[h][e]=[...,[t_init ou t fin, valeur>0],...]
        le = int(len(di_rep_2[h][e]) / 2)

        pas = 0

        #for each [t, valeur]
        for a in range(le):
          a1 = int(a + pas)

          #di_rep_2[h][e][a1]=[temps, 0 or >0]
          if di_rep_2[h][e][a1][1] != 0:

            #we add the 2 elements [t init, >0], [t fin,>0] in the list of the dict
            di_rep_3[h][e].append([di_rep_2[h][e][a1][0], di_rep_2[h][e][a1][1]])
            di_rep_3[h][e].append([di_rep_2[h][e][a1 + 1][0], di_rep_2[h][e][a1 + 1][1]])

            #creation des pts interm
            #nb_times=(t_fin-t_int)/time unit
            nb_times = round((di_rep_2[h][e][a1 + 1][0] - di_rep_2[h][e][a1][0]) / val_t_unit, 1)
            nb_t = int(nb_times - 1)
            for k1 in range(nb_t):
              li_1 = [di_rep_2[h][e][a1][0] + (k1 + 1) * val_t_unit, di_rep_2[h][e][a1][1]]

              #indice=a1+k1+1
              #di_rep_3[n][e].index([di_rep_2[h][e][a1][0],di_rep_2[h][e][a1][1]])
              #di_rep_2[h][e].insert(indice,li_1)

              di_rep_3[h][e].insert(len(di_rep_3[h][e]) - 1, li_1)

            pas += 1

          #if the valeur y=0:
          else:
            di_rep_3[h][e].append([di_rep_2[h][e][a1][0], di_rep_2[h][e][a1][1]])

            di_rep_3[h][e].append([di_rep_2[h][e][a1 + 1][0], di_rep_2[h][e][a1 + 1][1]])

            #creation of the intermediate values
            #nb_times=(t_fin-t_int)/time unit
            nb_tim = round((di_rep_2[h][e][a1 + 1][0] - di_rep_2[h][e][a1][0]) / val_t_unit, 1)
            nb_ti = int(nb_tim - 1)
            for v1 in range(nb_ti):
              li_2 = [di_rep_2[h][e][a1][0] + (v1 + 1) * val_t_unit, di_rep_2[h][e][a1][1]]
              di_rep_3[h][e].insert(len(di_rep_3[h][e]) - 1, li_2)

            pas += 1


    #print(di_rep_2[1])
    #import sys
    #sys.exit()	

    return di_rep_3


  #*****************************************************************************************************************************************************************************************
  #method writing the files with the cotnrol evolution of each stage of each intersection
  #di=ictionary, key id node, value=dict, key = stage id, value=[...,[t start control, t_end control],...]
  def fct_write_files_control_evolution_per_intersection(self, di, \
                                                         val_li_phrases=[
                                                           "time (1st colm), node indicator (>0 value) if the stage is actuated/0 otherwise (2nd colm)"]):

    #di=dictionary, key id node, value=dict, key = stage id, value=[...,[t start control, t_end control],...]
    #di=self.fct_creat_di_evolution_stage_actuation(val_dict_ev_type=val_dic_ev_type,val_t_unit=val_time_unit)


    for i in di:
      #print("i",i)
      for j in di[i]:
        #print("j",j)
        file = open(
          self._folder_stage_evol_inters + "/" + File_Stats_Anal_Folders_And_Files.name_file_stage_evol_per_intersection + str(
            i) + "_" + str(j) + ".txt", "w")
        file.write("%s\t %s\t \n" % ("id node", i))
        file.write("%s\t %s\t \n" % ("id stage", j))
        for m in val_li_phrases:
          file.write("%s\t \n" % (m))
        for k in di[i][j]:
          #print("k",k)
          for n in k:
            file.write("%.2f\t" % (n))
          file.write("\n")
      file.close()


    #*****************************************************************************************************************************************************************************************

  #method returning a dictionary computing for each node the number of swithces from one stage to another oevr the entire sim duration
  #val_dict_ev_type=dict, key=event type, value= record object
  def fct_calcul_nb_stage_switches_per_inters(self, val_dict_ev_type):

    #di_rep=dict, key= id node, value nb of switches
    di_rep = {}

    #di_id_nd_valeur_id_cur_stage=dict, key=node id, value=the current stage id 
    di_id_nd_valeur_id_cur_stage = {}

    for i in val_dict_ev_type[Cl_Event.TYPE_EV["type_ev_new_intersection_control"]]:

      #if the node id is in the dictionary
      if i.get_id_inters_node() in di_rep:

        #if the current stage is different from te previous one
        if i.get_id_actuated_stage() != di_id_nd_valeur_id_cur_stage[i.get_id_inters_node()]:
          di_rep[i.get_id_inters_node()] += 1

          di_id_nd_valeur_id_cur_stage[i.get_id_inters_node()] = i.get_id_actuated_stage()

      #if the node id is not in the dictionary
      else:
        di_rep[i.get_id_inters_node()] = 1

        di_id_nd_valeur_id_cur_stage[i.get_id_inters_node()] = i.get_id_actuated_stage()

    #print(di_rep)
    #import sys
    #sys.exit()

    return di_rep


  #*****************************************************************************************************************************************************************************************
  #method writing the file with the number of switches per  intersection node
  def fct_write_file_nb_stage_switches_per_inters(self, val_dic_ev_type,
                                                  val_li_phrases=["id node (1st colm), nb stage switches (2nd colm)"]):

    #di=dict, key=node id value=number of switches
    di = self.fct_calcul_nb_stage_switches_per_inters(val_dict_ev_type=val_dic_ev_type)

    file = open(
      self._folder_stage_switches_per_intersection + "/" + File_Stats_Anal_Folders_And_Files.name_file_stage_switches_per_itnersection,
      "w")

    for m in val_li_phrases:
      file.write("%s\t \n" % (m))

    for i in di:
      file.write("%d\t %.2f\t \n" % (i, di[i]))
    file.close()


  #*****************************************************************************************************************************************************************************************
  #function creating a dictionary with exit link information, key=[id of entry link,id of exit link], value= [,...[t veh_ap,t_veh_exit],...]
  #di_db_file=dict, key= event type, value =[...,record obj,....]		A VOIR !!!!
  def fct_creat_dict_exit_link_info(self):

    treat_sim_obj = Cl_Treatment_Sim_Res.Treatment_Sim_Res(val_db_file_sim_res_to_treat=self._db_file)

    #dict key= event type, value =record obj
    dict_db_file = treat_sim_obj.fct_creation_dictionary_from_the_db_file()

    di = {}

    #from al the arrival events, we choose those for which the time_veh_exit_from_network, is >0
    #for each arrival at a signalised intersection object
    for i in dict_db_file[Cl_Event.TYPE_EV["type_ev_end_veh_departure_from_que"]]:

      #if the exit time is >0
      if i.get_time_veh_exit_from_network() > 0:

        #if the movement (entry link, exit link) is not in the dict
        if (i.get_id_veh_entry_link(), i.get_id_current_link_veh_location()) not in di:

          di[i.get_id_veh_entry_link(), i.get_id_current_link_veh_location()] = \
            [[i.get_time_veh_appearance_in_network(), i.get_time_veh_exit_from_network()]]


        #if the movement (entry link, exit link) is  in the dict
        else:
          di[i.get_id_veh_entry_link(), i.get_id_current_link_veh_location()].append( \
            [i.get_time_veh_appearance_in_network(), i.get_time_veh_exit_from_network()])

    if Cl_Event.TYPE_EV["type_ev_end_veh_departure_from_que_nsi"] in dict_db_file:
      #for each arrival at a non-signalised intersection object			
      for j in dict_db_file[Cl_Event.TYPE_EV["type_ev_end_veh_departure_from_que_nsi"]]:

        #if the exit time is >0
        if j.get_time_veh_exit_from_network() > 0:

          #if the movement (entry link, exit link) is not in the dict
          if (j.get_id_veh_entry_link(), j.get_id_current_link_veh_location()) not in di:

            di[j.get_id_veh_entry_link(), j.get_id_current_link_veh_location()] = \
              [[j.get_time_veh_appearance_in_network(), j.get_time_veh_exit_from_network()]]


          #if the movement (entry link, exit link) is  in the dict
          else:
            di[j.get_id_veh_entry_link(), j.get_id_current_link_veh_location()].append( \
              [j.get_time_veh_appearance_in_network(), j.get_time_veh_exit_from_network()])

    else:
      print(
      "ATTENTION,  AUCUN EVEN end_veh_departure_from_que_ns TROUVE, IN CL_STAT_ANALYSIS,  fct_creat_dict_exit_link_info")

    return di

  #***************************************************************************************************************************************************************************************** 
  #function creating a dictionary, key=[id of entry link,id of exit link], value=[mean travel time,nb_veh_exit]
  def fct_creat_dict_mean_travel_time_entry_exit_link(self, di_info_entry_exit_lk, val_round_prec=2):


    di = {}
    #for each (entry, exit lin,k)
    for i in di_info_entry_exit_lk:
      som = 0
      for j in di_info_entry_exit_lk[i]:
        som += j[1] - j[0]
        #print(i,"j[0]",j[0],"j[1]",j[1],"som",som)
        if som < 0:
          print("PROBLEM ", j[0], j[1], j[1] - j[0])
          import sys

          sys.exit()
      #print("som=",som)
      a = len(di_info_entry_exit_lk[i])
      mean = round(som / a, val_round_prec)
      #mean=round(som/a,2)
      #print(mean)
      #print("mean=",mean)
      di[i] = [mean, a]
    #print()
    #print("di=",di)
    return di

  #***************************************************************************************************************************************************************************************** 
  #function writing  a file with the mean travel time of each entry-exit link , (no turn movements are included) and the number of vehicles served
  #id entry link, id exit, link, mean travel time, nb veh served
  #di=dictionary; key=(entry,exit link), value=[mean travel time, nb veh served]
  def fct_writing_file_mean_travel_time_entry_exit_lk_nb_veh_served(self, di):

    #we create the dictionary; key=(entry,exit link), value=[mean travel time, nb veh served]
    #di=self.fct_creat_dict_mean_travel_time_entry_exit_link(di_info_entry_exit_lk=val_di_info_entry_exit_lk)

    file = open(self._file_name_folder_mean_travel_time_entry_exit_lk, "w")

    file.write("%s\t %s\t  %s\t %s \n" % ("ID ENTRY LK", "ID EXIT LK", "MEAN TR T", "NB VEH SERVED"))
    for i in di:
      #print(i[0],di[i][0])
      #for j in di[i]:
      #file.write("%s\t %s\t %d\t %d \n"%(i[0],i[1],j[0],j[1]))
      file.write("%s\t %s\t %.1f\t %d \n" % (i[0], i[1], di[i][0], di[i][1]))

    file.close()

  #*****************************************************************************************************************************************************************************************
  #function creating a dictionary, key=[id of entry link,id of exit link], value=dict, key=(t_start period, t_end period),
  #value= [mean travel time, nb vehicles]
  def fct_creat_dict_mean_travel_time_entry_exit_link_per_per(self, v_sim_dur, v_t_period, v_t_unit, v_t_init,
                                                              val_round_prec, di_info_entry_exit_lk):

    #di_info_entry_exit_lk= dict, key=[id of entry link,id of exit link], value= [,...[t veh_ap,t_veh_exit],...]
    #di_info_entry_exit_lk=self.fct_creat_dict_exit_link_info()

    #li_t_interval=[..., [t start i period, t_end of ith period],...]
    li_t_interval = []
    nb_interv = math.ceil(v_sim_dur / v_t_period)
    t_init = v_t_init
    for i in range(nb_interv):
      li_t_interval.append([t_init, t_init + v_t_period - v_t_unit])
      t_init = t_init + v_t_period
    #print(li_t_interval)
    #import sys
    #sys.exit()




    #dict, key=(id entry, id exit lk), value=dict, key=(t_start_period, t_end_period), value=[som of (t_exit-t_entry corresponding period), nb vehicles exited during current period]
    di_rep_info_per_period = {}

    for i in di_info_entry_exit_lk:

      #dict, key=(t_start_period, t_end_period), value=[som of (t_exit-t_entry corresponding period), nb vehicles exited during current period]
      di_rep_info_per_period[i] = {}

      #di_info_entry_exit_lk= dict, key=[id of entry link,id of exit link], value= [,...[t veh_ap,t_veh_exit],...]
      di_info_entry_exit_lk[i].sort()

      ind = 0
      som_t_total_veh_travel = 0
      nb_veh_exited_period = 0

      #di_info_entry_exit_lk= dict, key=[id of entry link,id of exit link], value= [,...[t veh_ap,t_veh_exit],...]
      for j in di_info_entry_exit_lk[i]:

        #numero interval to which belong the t_exit
        num_inter = math.floor(j[1] / v_t_period) + 1

        if (li_t_interval[num_inter - 1][0], li_t_interval[num_inter - 1][1]) in di_rep_info_per_period[i]:

          new_dur = j[1] - j[0]

          #we update the som of (t_exit- t_ap)
          #print("ici avant",di_rep_info_per_period[i][li_t_interval[num_inter-1][0],li_t_interval[num_inter-1][1]])

          di_rep_info_per_period[i][li_t_interval[num_inter - 1][0], li_t_interval[num_inter - 1][1]][0] += new_dur

          #we update the corresponding number of vehicles
          di_rep_info_per_period[i][li_t_interval[num_inter - 1][0], li_t_interval[num_inter - 1][1]][1] += 1

        #print("ici apres",di_rep_info_per_period[i][li_t_interval[num_inter-1][0],li_t_interval[num_inter-1][1]])

        else:
          new_dur = j[1] - j[0]

          nb_veh = 1
          di = {}

          #we update the som of (t_exit- t_ap)
          di[li_t_interval[num_inter - 1][0], li_t_interval[num_inter - 1][1]] = [new_dur, 1]

          di_rep_info_per_period[i].update(di)
        for k in li_t_interval:
          if (k[0], k[1]) not in di_rep_info_per_period[i]:
            di_rep_info_per_period[i][k[0], k[1]] = [0, 0]

    #print(di_info_entry_exit_lk[2370, 2351])
    #print()		
    #print(di_rep_info_per_period[2370, 2351])	
    #import sys
    #sys.exit()

    #di_rep_mean_travel_time=dict, key=(id entry, id exit link), value=dict, key=(t_start_time period, t_end_time period)
    #value=[som (t_exit-t_entry), nb veh)]
    di_rep_mean_travel_time = {}

    for m in di_rep_info_per_period:
      di_rep_mean_travel_time[m] = {}
      for n in di_rep_info_per_period[m]:
        di = {}
        if di_rep_info_per_period[m][n][0] != 0:
          #if m[0]==2370  and m[1]==2351:
          #print("n",n)
          #print(di_rep_info_per_period[m][n][1],di_rep_info_per_period[m][n][0],\
          #round(di_rep_info_per_period[m][n][0]/di_rep_info_per_period[m][n][1],2))
          di[n] = [round(di_rep_info_per_period[m][n][0] / di_rep_info_per_period[m][n][1], 2),
                   di_rep_info_per_period[m][n][1]]
        else:
          di[n] = [0, 0]
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
  #method writing a set of files each for each pair (entry, exit) link, indicating the mean travel time per period
  #lis_phrases="(id entry lk,  id exit link), period (in secs), other lines:  < time value (1st column), mean travel time, total nb veh  (2nd column) "
  def fct_write_set_matrices_set_files_key_couple(self, name_file_to_write, di_key_nb_value_list_valeurs, lis_phrases):


    #di_key_nb_value_list_valeurs=dict, key=(id entry link, id exit link), 
    #value=[[max_value_time of the corresponding interval, mean travel time 1st period, nb veh],
    #[[max_value_time of the corresponding interval,mean travel time 2nd period, nb veh],...]

    #for each entry, exit link
    for i in di_key_nb_value_list_valeurs:

      file = open(
        self._folder_stat_anal + "/" + File_Stats_Anal_Folders_And_Files.name_folder_travel_time_per_period_entry_exit_lk + "/" + \
        File_Stats_Anal_Folders_And_Files.name_file_travel_time_per_period_entry_exit_link + str(i) + ".txt", "w")

      file.write("%s\t \n" % (str(i)))

      for j in lis_phrases:
        file.write("%s\t " % (j))
      file.write("\n")

      #on trie les cles
      sorted_keys = sorted(di_key_nb_value_list_valeurs[i].keys())

      #for each period
      for k in sorted_keys:
        #we write the t_start, t_end of the period, the mean travel time, nb of vehicles exited during this period
        #for m in  di_key_nb_value_list_valeurs[i][k]:
        file.write("%.2f\t %.2f\t %.2f\t %d\n" % (k[0], k[1], di_key_nb_value_list_valeurs[i][k][0], \
                                                  di_key_nb_value_list_valeurs[i][k][1]))
      file.close()

    #*****************************************************************************************************************************************************************************************

  #method calculating and writing files witht he average travel time per period  for each entry-exit link 
  def fct_calcul_and_write_travel_time_per_time_period_entry_exit_lk(self, va_sim_dur, va_t_period, va_t_unit,
                                                                     va_round_prec, va_lis_phrases, \
                                                                     va_t_init, val_di_info_entry_exit_lk):

    #dict, key=(id entry link, id exit link), value=dict, key=(t_start period, t_end period),value= [mean travel time, nb vehicles]
    di = self.fct_creat_dict_mean_travel_time_entry_exit_link_per_per(v_sim_dur=va_sim_dur, v_t_period=va_t_period, \
                                                                      v_t_unit=va_t_unit, v_t_init=va_t_init,
                                                                      val_round_prec=va_round_prec,
                                                                      di_info_entry_exit_lk=val_di_info_entry_exit_lk)



    #we write the list of files
    self.fct_write_set_matrices_set_files_key_couple(
      name_file_to_write=self._file_travel_time_per_period_entry_exit_link, \
      di_key_nb_value_list_valeurs=di, lis_phrases=va_lis_phrases)

  #*******************************************************************************************************************************************************************************************	

  #method calcul the prob of a existing n vehicles at  the sum of queues
  #returns a dictionary, key=nb of veh, value=[prob, time with this number of veh at queue]
  #li_t_que_len=[....[time, queue length at time t]...]
  def fct_calc_prob_of_nb_veh_at_queue_and_duration(self, li_t_que_len, dur_sim):

    li_1 = list(li_t_que_len)
    #print("li_1",li_1)
    #print(li_t_que_len)

    #we add a 3rd elem to li_1 indicating the duartion of the time with this que length
    for i in range(len(li_1) - 1):
      li_1[i].append(li_1[i + 1][0] - li_1[i][0])
    #we add 1 sec for the last time

    li_1[len(li_1) - 1].append(1)

    #print()
    #print("li_1 after",li_1)

    #di=dict, key=queue length, value=[dur 1, dur2,..]]	
    di = {}
    #li_1=[[t,queue length,duration of this queue length],..] ex li_1=[[4,3,3],[7,1,1]...]
    #print("li_1",li_1)
    for i in li_1:
      #print("i=",i)
      if i[1] not in di:
        di[i[1]] = [i[2]]
      else:
        di[i[1]].append(i[2])
    #print()
    #print("di",di)
    #di_1=dict, key=nb of veh in the que, value=[prob of having this number of veh in the que, total time with this nb of veh in the queue]
    #prob of having this number of veh in the que=total time with this number of veh in the que/sim duration		
    di_1 = {}
    for i in di:
      dur = sum(di[i])
      di_1[i] = [dur / dur_sim, dur]
    #print("i",i,"dur",dur,"dur_sim",dur_sim,"dur/dur_sim",dur/dur_sim)
    #print(di)
    return di_1

  #***************************************************************************************************************************************************************************************** 
  #method writing in a file, the number of vehicles (of the sum of queues) and the probability of having this number
  #di=dict, key=nb_of_veh value=[ prob, time with this number of veh]
  def fct_writing_prob_of_nb_veh_at_queue(self, di):

    #di=dict, key=nb_of_veh value=[ prob, time with this number of veh]
    #di=self.fct_calc_prob_of_nb_veh_at_queue_and_duration(li_t_que_len=val_li_t_que_len,dur_sim=val_durat_sim)

    file = open(self._file_name_file_nb_veh_prob_sum_que, "w")
    file.write("%s\t %s\t  \n" % ("NB OF VEH SUM_QUE", "PROB"))
    for i in di:
      file.write("%d\t %f\n" % (i, di[i][0]))

    file.close()

  #return di

  #*****************************************************************************************************************************************************************************************
  #method calculating the weight mean and stan dev of sum of queues and returns a list 
  #[weighted mean, stand deviat, mean-stan dev, mean+stan dev]
  #dict_nb_veh_que_and_dur=dict, key=number of veh at queue, value=[ prob of having that number, time duration with this number]
  def fct_calc_weighted_mean_sd_sum_que(self, dict_nb_veh_que_and_dur, dur_sim, val_round_prec=1):


    w_s = 0
    v_s = 0

    for i in dict_nb_veh_que_and_dur:
      w_s += i * dict_nb_veh_que_and_dur[i][1]
      v_s += (i ** 2) * dict_nb_veh_que_and_dur[i][1]
    #print("w_s=",w_s,"v_s=",v_s)
    #print()


    #print("w_s=",w_s,"sd_s=",v_s)
    #sd=math.sqrt(var)
    #print(" [w_s/dur_sim,sd]",w_s/dur_sim,sd)
    #a=round(w_s/dur_sim,2)
    #b=round(sd,2)
    #print("a=",a,"b=",b)
    #return [a,b,a-b,a+b]

    moy = w_s / dur_sim
    #print(moy,moy**2)

    var = (v_s / dur_sim) - (moy ** 2)
    #print(var)
    #print("var=",var)
    sd = math.sqrt(var)
    a = round(moy, val_round_prec)
    b = round(sd, val_round_prec)
    c = round(a - b, val_round_prec)
    d = round(a + b, val_round_prec)
    #print([a,b,c,d])
    #print("v_s",v_s,"dur_sim",dur_sim,"v_s/dur_sim",v_s/dur_sim,"moy",moy)
    return [a, b, c, d]

  #***************************************************************************************************************************************************************************************** 
  #method writing a file with the weighted mean of the sum of queues withing a simulation
  #li_w_mean_sd=[weighted mean, stand deviat, mean-stan dev, mean+stan dev]
  def fct_writing_file_weighted_mean_sd_sum_que(self, li_w_mean_sd):

    #we open the file where the sum of queues is written during a sim
    #we read the file and do not use the appropriate dict in case we do not want do both calculations (sum of queues, mean and var) 
    #within the same stat anal
    #in case this analysis will be done in every run this part has to be added when calculate the sum of queues




    #li_w_mean_sd=self.fct_calc_weighted_mean_sd_sum_que(dict_nb_veh_que_and_dur=val_dict_nb_veh_que_and_durat,\
    #dur_sim=val_durat_sim)

    file = open(self._file_mean_length_sum_queues, "w")
    file.write("%s\t %s\t %s\t %s\t\n" % ("WEIGHTED MEAN (1)", "STAND DEVIATION (2)", "WM-SD(3)", "WM+SD(4)"))

    file.write("%.2f\t %.2f\t %.2f\t %.2f\t\n" % (li_w_mean_sd[0], li_w_mean_sd[1], li_w_mean_sd[2], li_w_mean_sd[3]))
    file.close()

  #*****************************************************************************************************************************************************************************************
  #method calculating the avearge length value of a queue, returns [average time spent by veh in que, nb_veh]
  #employed formula sum ni x ti / sum ni, where ni=observed value of queue length, ti=total time during which the queue had this length
  #di_key_nb_veh_que_value_prob_and_dur_time list= [dict,
  #dict, key=nb of veh, 
  #value= [ [prob, time with this number of veh at queue], total nb veh]
  def fct_calcul_average_time_spent_by_veh_in_a_que(self, di_key_nb_veh_que_value_prob_and_dur_time, \
                                                    val_round_prec=1):

    som = 0

    #print("HERE3",di_key_nb_veh_que_value_prob_and_dur_time)

    #print()


    for i in di_key_nb_veh_que_value_prob_and_dur_time[0]:
      #sum ni x ti
      som += di_key_nb_veh_que_value_prob_and_dur_time[0][i][1] * i
    #print(di_key_nb_veh_que_value_prob_and_dur_time[0])

    if di_key_nb_veh_que_value_prob_and_dur_time[1] != 0:

      #print(round(som/di_key_nb_veh_que_value_prob_and_dur_time[1],2),i)

      #we return the number of vehicles in the queue for the plot
      #print(i)
      #import sys
      #sys.exit()
      #return [round(som/di_key_nb_veh_que_value_prob_and_dur_time[1],2),i]
      return [round(som / di_key_nb_veh_que_value_prob_and_dur_time[1], val_round_prec),
              di_key_nb_veh_que_value_prob_and_dur_time[1]]
    else:
      return 0
    #***************************************************************************************************************************************************************************************** 

  #method calculating the average length of each queue of the network
  #it returns a a list, [ dict, the mean value of the average time spent by veh in queues]

  #di_key_mov_val_sorted_li_t_que_length= dict, key=mov, 
  #value =list [  [ ...,sorted li,...]=[ ..[t, que length at t],..], nb of depart veh + veh remained in the que by the end of sim ]
  def fct_calcul_average_time_spent_by_veh_in_a_que_for_each_que(self, di_key_mov_val_sorted_li_t_que_length,
                                                                 val_durat_sim, \
                                                                 val_round_prec=1):

    di_1 = {}
    som = 0
    #print(di_key_mov_val_sorted_li_t_que_length)
    #import sys
    #sys.exit()
    for i in di_key_mov_val_sorted_li_t_que_length:
      #if i[0]==9 and i[1]==14:
      #print(di_key_mov_val_sorted_li_t_que_length[i])


      #di=key nb of veh in queue i, value =[prob, time with this number of veh at queue]
      di = self.fct_calc_prob_of_nb_veh_at_queue_and_duration(li_t_que_len=di_key_mov_val_sorted_li_t_que_length[i][0], \
                                                              dur_sim=val_durat_sim)
      #if i[0]==9 and i[1]==14:
      #print(di)


      lis = [di, di_key_mov_val_sorted_li_t_que_length[i][1]]
      #print("lis",lis)



      #di_1[i]=list [average time spend by veh in the queue i , nb of veh arrived in  queue]
      di_1[i] = self.fct_calcul_average_time_spent_by_veh_in_a_que(di_key_nb_veh_que_value_prob_and_dur_time=lis)

      #if i[0]==9 and i[1]==14:
      #print(di_1[i])
      #import sys
      #sys.exit()

      #print("i=",i,"di_1[i]",di_1[i])
      som += di_1[i][0]

    #print("HERE1","i: ",i, "di_1[i]", di_1[i],"som/len(di_key_mov_val_sorted_li_t_que_length",som/len(di_key_mov_val_sorted_li_t_que_length))
    #print()
    #print("HERE5",di_1)
    return [di_1, round(som / len(di_key_mov_val_sorted_li_t_que_length), val_round_prec)]


  #*****************************************************************************************************************************************************************************************
  #method writing the mean value of each queue in the associated file
  #li=[list  dict, the mean value of the average time spent by veh in queues]
  #di_key_mov_val_sorted_li_t_que_length= dict, key=mov, 
  #value =list [  [ ...,sorted li,...]=[ ..[t, que length at t],..], nb of depart veh + veh remained in the que by the end of sim ]
  def fct_writing_file_average_time_spent_by_veh_in_a_que_for_each_que(self, li):


    #li=self.fct_calcul_average_time_spent_by_veh_in_a_que_for_each_que(\
    #di_key_mov_val_sorted_li_t_que_length=di_key_movem_val_sorted_li_t_que_length,\
    #val_durat_sim=val_duration_sim)

    #print(di_2)

    #print("HERE",li)
    file = open(self._file_mean_time_spent_by_veh_in_que + ".txt", "w")
    file.write(
      "%s\t %s\t  %s\t  %s \n" % ("ID CURRENT LINK (1)", "ID DEST LINK (2)", "MEAN TIME SPENT BY (ALL) VEHS IN QUE", \
                                  "TOTAL NB VEH STATIONED IN THE QUE"))
    for i in li[0]:
      file.write("%s\t  %s\t %.2f\t %d \n" % (i[0], i[1], li[0][i][0], li[0][i][1]))
    file.close()

    file1 = open(self._file_mean_of_aver_sojourn_time + ".txt", "w")
    file1.write("%s\t  \n" % ("AVERAGE OF MEAN SOJOURN TIME OF VEH IN QUEUES"))
    file1.write("%.2f\t " % (li[1]))
    file1.close()

  #*****************************************************************************************************************************************************************************************
  #fct creating a dictionary with the number of vehicles in each internal link,
  #key=id link, value=[...,[temps,nb veh link],...]
  def fct_creat_dict_current_nb_veh_in_link(self, v_netw, dict_db_key_id_event_type_val_record_obj):

    di_rep = {}

    #for each evet_end_veh_departure
    for i in dict_db_key_id_event_type_val_record_obj[Cl_Event.TYPE_EV["type_ev_end_veh_departure_from_que"]]:


      #if the origin link of the veh (its location when the departure started) is not in the dictionary
      if i.get_veh_current_queue_location()[0] not in di_rep:
        di_rep[i.get_veh_current_queue_location()[0]] = [[i.get_ev_time(), i.get_nb_veh_in_dep_lk()]]

      #if the origin link of the veh (its location when the departure started) is in the dictionary
      else:
        di_rep[i.get_veh_current_queue_location()[0]].append([i.get_ev_time(), i.get_nb_veh_in_dep_lk()])

      #si le veh n'est pas arrive a un arc de sortie, on ecrit le nb des veh trouves a sa nouvelle position
      if i.get_veh_current_queue_location()[1] not in v_netw.get_di_exit_links_from_network():

        #if the current veh location is not in the dict
        if i.get_veh_current_queue_location()[1] not in di_rep:
          di_rep[i.get_veh_current_queue_location()[1]] = [[i.get_ev_time(), i.get_nb_veh_in_ar_lk()]]

        #if the current veh location is in the dict
        else:
          di_rep[i.get_veh_current_queue_location()[1]].append([i.get_ev_time(), i.get_nb_veh_in_ar_lk()])

    if Cl_Event.TYPE_EV["type_ev_end_veh_departure_from_que_nsi"] in dict_db_key_id_event_type_val_record_obj:

      #  CHECK THAT ev ty_ev_end_veh_hold_at_que_nsi should register THIS INFO ! 
      for j in dict_db_key_id_event_type_val_record_obj[Cl_Event.TYPE_EV["type_ev_end_veh_departure_from_que_nsi"]]:

        #if the origin link of the veh (its location when the departure started) is not in the dictionary
        if j.get_veh_current_queue_location()[0] not in di_rep:
          di_rep[j.get_veh_current_queue_location()[0]] = [[j.get_ev_time(), j.get_nb_veh_in_dep_lk()]]

        #if the origin link of the veh (its location when the departure started) is in the dictionary
        else:
          di_rep[j.get_veh_current_queue_location()[0]].append([j.get_ev_time(), j.get_nb_veh_in_dep_lk()])

        #si le veh n'est pas arrive a un arc de sortie, on  ecrit le nb des veh trouves a sa nouvelle position
        if j.get_veh_current_queue_location()[1] not in v_netw.get_di_exit_links_from_network():

          #if the current veh location is not in the dict
          if j.get_veh_current_queue_location()[1] not in di_rep:
            di_rep[j.get_veh_current_queue_location()[1]] = [[j.get_ev_time(), j.get_nb_veh_in_ar_lk()]]

          #if the current veh location is in the dict
          else:
            di_rep[j.get_veh_current_queue_location()[1]].append([j.get_ev_time(), j.get_nb_veh_in_ar_lk()])

    for i in dict_db_key_id_event_type_val_record_obj[Cl_Event.TYPE_EV["type_ev_veh_appearance"]]:

      #si le veh n'est pas parti d'un arc d'entree, on ecrit le nombre des veh sur l'arc d'ou il est parti
      #if i.get_veh_current_queue_location()[0] not in v_netw.get_di_entry_links_to_network():
      #if the origin link of the veh (its location when the departure started) is not in the dictionary
      if i.get_veh_current_queue_location()[0] not in di_rep:
        di_rep[i.get_veh_current_queue_location()[0]] = [[i.get_ev_time(), i.get_nb_veh_in_ar_lk()]]

      #if the origin link of the veh (its location when the departure started) is in the dictionary
      else:
        di_rep[i.get_veh_current_queue_location()[0]].append([i.get_ev_time(), i.get_nb_veh_in_ar_lk()])

    if Cl_Event.TYPE_EV["type_ev_veh_appearance_nsi"] in dict_db_key_id_event_type_val_record_obj:
      for j in dict_db_key_id_event_type_val_record_obj[Cl_Event.TYPE_EV["type_ev_veh_appearance_nsi"]]:
        print("IN CLASSE STAT ANAL,  CHECK IF EV _ev_veh_appearance_nsI RECORD IS MADE CORRECTLY")
        import sys

        sys.exit()
        #if the origin link of the veh (its location when the departure started) is not in the dictionary
        if j.get_veh_current_queue_location()[0] not in di_rep:
          di_rep[j.get_veh_current_queue_location()[0]] = [[j.get_ev_time(), j.get_nb_veh_in_ar_lk()]]

        #if the origin link of the veh (its location when the departure started) is in the dictionary
        else:
          di_rep[j.get_veh_current_queue_location()[0]].append([j.get_ev_time(), j.get_nb_veh_in_ar_lk()])

    for i in di_rep:
      di_rep[i].sort()

    return di_rep


  #***************************************************************************************************************************************************************************************** 	
  #method write the files with the  evolution of each internal link
  #di_Rep=dict, key=id link, value=[...,[t,nb veh in link],...]
  def fct_write_files_entry_internal_link_evol(self, di_rep, va_netw):

    #dict, key=id link, value=[...,[t,nb veh in link],...]
    #di_rep=self.fct_creat_dict_current_nb_veh_in_link(\
    #v_netw=va_netw,\
    #dict_db_key_id_event_type_val_record_obj=va_dict_db_key_id_event_type_val_record_obj)

    for i in di_rep:
      file = open(
        self._folder_link_evol + "/" + File_Stats_Anal_Folders_And_Files.name_file_evolution_lk + str(i) + ".txt", "w",
        encoding="utf8")
      cap = va_netw.get_di_entry_internal_links()[i].get_capacity_link()
      #if the link is an entry link
      if i in va_netw.get_di_entry_links_to_network():
        file.write("%s\t %s \n" % ("LINK", str(i)))
      ##if the link is not an entry link
      else:
        file.write("%s\t %s\t %s\t %s \n" % ("LINK", str(i), "CAPACITÉ", cap))
      for j in di_rep[i]:
        if j[1] < 0:
          print("PROBLEM IN CL_STAT ANAL fct_write_files_entry_internal_link_evol i=", i, j)
          import sys

          sys.exit()
        file.write("%.2f\t %d\n" % (j[0], j[1]))
      file.close()

    #*****************************************************************************************************************************************************************************************

    #*****************************************************************************************************************************************************************************************

    #*****************************************************************************************************************************************************************************************

  #method writing the files of a statistical analysis 
  def fct_writing_files_sa_complete(self, val_netw, val_dur_sim, val_cycle_dur, val_t_end_sim, val_finite_lk_cap,
                                    val_t_period, val_t_period_for_average_sum_ques, \
                                    val_veh_final_dest_dynam_construct, val_name_Fres_folder, \
                                    val_t_unit, val_t_init, va_li_phrases=[
        "1st line=(id entry lk,  id exit link),other lines:  < time value (1st column), mean travel time, total nb veh  (2nd column) "], \
                                    val_li_phrases_mean_trav_dist=[
                                      "1st line=(id entry lk,  id exit link),other lines:  t_start, t_end period (1st, 2nd column), mean traveled distance, total nb veh  (3rd column) "]):


    #we create a  result sim treatment object
    treat_sim_obj = Cl_Treatment_Sim_Res.Treatment_Sim_Res(val_db_file_sim_res_to_treat=self._db_file)


    #dict, key=mov, value = [...,record obj,...]
    val_dict_db_file = treat_sim_obj.fct_creation_dictionary_key_movem_from_the_db_file()


    #dict, key=id event type, value=[..,record obj,...]
    #ATTENTION CE DICT EST AUSSI CALCULE (POUR UEN 2EME FOIS)  LORS CALCUL MEAN TRAVEL TIME, A CORRIGER 
    val_dict_db_file_1 = treat_sim_obj.fct_creation_dictionary_from_the_db_file()


    #*********************
    #we write the file with the evolution of each queue
    #dict, key=phase id, value=dict, key=time, value=  [ [nb of vehicles in the queue,ev type,id veh     ]   ]
    val_di_movem = self.fct_creat_dict_queue_lengths_during_sim(val_network=val_netw, dict_db_file=val_dict_db_file)


    #val_di_movem_val_sorted_times_and_sizes=dict, key=phase id value=[list, nb departed veh]
    #list=sorted list regard. time [time, que length, nb veh in que]
    val_di_movem_val_sorted_times_and_sizes = self.fct_writing_file_time_veh_queue_length_and_file_que_length_and_veh_id(
      di_movem=val_di_movem)
    #*********************

    #we write the file with the sum of all the queues
    val_di_key_id_phase_val_que_ev_t_unique = self.fct_creat_dict_que_evol_unique_t_instances(
      val_dict_que_evol=val_di_movem_val_sorted_times_and_sizes)

    #li_val_sum=[..., [t, sum of ques],...]
    li_val_sum = self.fct_sum_all_queues(val_di_key_id_phase_val_di_key_time_val_li_info=val_di_movem, \
                                         val_di_que_evol_t_unique=val_di_key_id_phase_val_que_ev_t_unique)

    self.fct_write_file_sum_que_t_sim(li=li_val_sum, val_name_file_write=self._file_sum_queue_evol)
    #********************
    #we write the file with the sum of the desired queues 
    li_t_instances = self.fct_calcul_li_t_instances_some_que_evol(val_di_que_evol=val_di_movem, li_id_considered_phases= \
      [[10003, 10008], [100011, 100014]])

    val_dict_que_evol_t_unique = self.fct_creat_dict_some_que_evol_unique_t_instances(val_dict_que_evol= \
                                                                                        val_di_movem_val_sorted_times_and_sizes, \
                                                                                      li_id_considered_phases= \
                                                                                        [[10003, 10008], [100011, 100014]])

    li_some_sum_ques = self.fct_sum_some_queues(val_di_que_evol_t_unique=val_dict_que_evol_t_unique,
                                                li_t=li_t_instances)

    self.fct_write_file_sum_que_t_sim(li=li_some_sum_ques, val_name_file_write=self._file_sum_desired_queue_evol)
    #*********************
    #we write the file with the average sum of the desired list of queues per period

    self.fct_write_average_sum_ques_per_period_over_nb_t_instances_within_period(va_li_sum_ques=li_some_sum_ques,
                                                                                 va_sim_dur=val_dur_sim, \
                                                                                 va_t_period=val_t_period_for_average_sum_ques,
                                                                                 va_t_unit=val_t_unit,
                                                                                 va_t_init=val_t_init, \
                                                                                 val_name_file= \
                                                                                   File_Stats_Anal_Folders_And_Files.name_file_average_sum_desired_ques_per_period_over_nb_t_instances_within_period, \
                                                                                 val_li_phrases=[
                                                                                   "t start/t end period, avearage value of the sum of the queues"])


    #*********************
    #we write the file with the average sum of all the queues per period

    self.fct_write_average_sum_ques_per_period_over_nb_t_instances_within_period(va_li_sum_ques=li_val_sum,
                                                                                 va_sim_dur=val_dur_sim, \
                                                                                 va_t_period=val_t_period_for_average_sum_ques,
                                                                                 va_t_unit=val_t_unit,
                                                                                 va_t_init=val_t_init, val_name_file= \
        File_Stats_Anal_Folders_And_Files.name_file_average_sum_ques_per_period_over_nb_t_instances_within_period, \
                                                                                 val_li_phrases=[
                                                                                   "t start/t end period, avearage value of the sum of the queues"])

    #*********************
    #we write the file with the cotnrol evolution at each node
    #di_ctrl_evol_per_nd=ictionary, key id node, value=dict, key = stage id, value=[...,[t start control, t_end control],...]
    di_ctrl_evol_per_nd = self.fct_creat_di_evolution_stage_actuation(val_dict_db_file_1, val_t_unit)

    self.fct_write_files_control_evolution_per_intersection(di=di_ctrl_evol_per_nd, \
                                                            val_li_phrases=[
                                                              "time (1st colm), node indicator (>0 value) if the stage is actuated/0 otherwise (2nd colm)"])

    #*********************
    #we write the fiel with the number switches per intersection
    self.fct_write_file_nb_stage_switches_per_inters(val_dic_ev_type=val_dict_db_file_1, val_li_phrases=[
      "id node (1st colm), nb stage switches (2nd colm)"])
    #*********************

    #we write the file with the mean travel time of each entry-exit link 

    #val_di_info_entry_exit_lk=dict, key=(entry,exit link), value=[mean travel time, nb veh served]
    val_dict_info_entry_exit_lk = self.fct_creat_dict_exit_link_info()

    #val_di_info_mtt_entry_exit_lk=dictionary, key=[id of entry link,id of exit link], value=[mean travel time,nb_veh_exit]
    val_di_info_mtt_entry_exit_lk = self.fct_creat_dict_mean_travel_time_entry_exit_link(
      di_info_entry_exit_lk=val_dict_info_entry_exit_lk, val_round_prec=2)

    self.fct_writing_file_mean_travel_time_entry_exit_lk_nb_veh_served(di=val_di_info_mtt_entry_exit_lk)
    #*********************
    #write the file with the average travel time per period
    self.fct_calcul_and_write_travel_time_per_time_period_entry_exit_lk( \
      va_sim_dur=val_dur_sim, va_t_period=val_t_period, va_t_unit=val_t_unit, va_round_prec=2,
      va_lis_phrases=va_li_phrases, \
      va_t_init=val_t_init, val_di_info_entry_exit_lk=val_dict_info_entry_exit_lk)

    #*********************
    #we wrte file with the number of vehicles (of the sum of all the queues) and the probability of having this number	

    #di_prob_que_size=dict, key=nb of veh, value=[prob, time with this number of veh at queue]
    di_prob_que_size = self.fct_calc_prob_of_nb_veh_at_queue_and_duration(li_t_que_len=li_val_sum, dur_sim=val_dur_sim)

    self.fct_writing_prob_of_nb_veh_at_queue(di=di_prob_que_size)

    #*********************
    #we wrtie the file with the weighted mean and standard deviation of queues

    #li_weight_mean_and_sd=list 
    #[weighted mean, stand deviat, mean-stan dev, mean+stan dev]
    li_weight_mean_and_sd = self.fct_calc_weighted_mean_sd_sum_que(dict_nb_veh_que_and_dur=di_prob_que_size,
                                                                   dur_sim=val_dur_sim, val_round_prec=1)

    self.fct_writing_file_weighted_mean_sd_sum_que(li_w_mean_sd=li_weight_mean_and_sd)

    #*********************
    #file with the average time spent by each veh in ques
    #li_t_aver_spent_by_veh_in_que= list, [ dict, the mean value of the average time spent by veh in queues]
    # di_key_mov_val_sorted_li_t_que_length= dict, key=mov,
    #value =list [  [ ...,sorted li,...]=[ ..[t, que length at t],..], nb of depart veh + veh remained in the que by the end of sim ]
    li_t_aver_spent_by_veh_in_que = self.fct_calcul_average_time_spent_by_veh_in_a_que_for_each_que( \
      di_key_mov_val_sorted_li_t_que_length=val_di_movem_val_sorted_times_and_sizes, val_durat_sim=val_dur_sim, \
      val_round_prec=1)

    self.fct_writing_file_average_time_spent_by_veh_in_a_que_for_each_que(li=li_t_aver_spent_by_veh_in_que)


    #*********************
    #we write the file with the entry internal link evolution

    #di_nb_veh_lk=key=id link, value=[...,[temps,nb veh link],...]
    di_nb_veh_lk = self.fct_creat_dict_current_nb_veh_in_link(v_netw=val_netw,
                                                              dict_db_key_id_event_type_val_record_obj=val_dict_db_file_1)

    self.fct_write_files_entry_internal_link_evol(di_rep=di_nb_veh_lk, va_netw=val_netw)

  #*********************
  #import sys
  #sys.exit() 



  #import sys
  #sys.exit()

  #*****************************************************************************************************************************************************************************************
  #method writing the files of a statistical analysis 
  def fct_writing_files_sa(self, val_netw, val_dur_sim, val_cycle_dur, val_t_end_sim, val_finite_lk_cap, val_t_period,
                           val_t_period_for_average_sum_ques, \
                           val_veh_final_dest_dynam_construct, val_name_Fres_folder, \
                           val_t_unit, val_t_init, va_li_phrases=[
        "1st line=(id entry lk,  id exit link),other lines:  < time value (1st column), mean travel time, total nb veh  (2nd column) "], \
                           val_li_phrases_mean_trav_dist=[
                             "1st line=(id entry lk,  id exit link),other lines:  t_start, t_end period (1st, 2nd column), mean traveled distance, total nb veh  (3rd column) "]):


    #we create a  result sim treatment object
    treat_sim_obj = Cl_Treatment_Sim_Res.Treatment_Sim_Res(val_db_file_sim_res_to_treat=self._db_file)


    #dict, key=mov, value = [...,record obj,...]
    val_dict_db_file = treat_sim_obj.fct_creation_dictionary_key_movem_from_the_db_file()


    #dict, key=id event type, value=[..,record obj,...]
    #ATTENTION CE DICT EST AUSSI CALCULE (POUR UEN 2EME FOIS)  LORS CALCUL MEAN TRAVEL TIME, A CORRIGER 
    val_dict_db_file_1 = treat_sim_obj.fct_creation_dictionary_from_the_db_file()


    #*********************
    #we write the file with the evolution of each queue
    #dict, key=phase id, value=dict, key=time, value=  [ [nb of vehicles in the queue,ev type,id veh     ]   ]
    val_di_movem = self.fct_creat_dict_queue_lengths_during_sim(val_network=val_netw, dict_db_file=val_dict_db_file)


    #val_di_movem_val_sorted_times_and_sizes=dict, key=phase id value=[list, nb departed veh]
    #list=sorted list regard. time [time, que length, nb veh in que]
    val_di_movem_val_sorted_times_and_sizes = self.fct_writing_file_time_veh_queue_length_and_file_que_length_and_veh_id(
      di_movem=val_di_movem)
    #*********************

    #we write the file with the sum of all the queues
    val_di_key_id_phase_val_que_ev_t_unique = self.fct_creat_dict_que_evol_unique_t_instances(
      val_dict_que_evol=val_di_movem_val_sorted_times_and_sizes)

    #li_val_sum=[..., [t, sum of ques],...]
    li_val_sum = self.fct_sum_all_queues(val_di_key_id_phase_val_di_key_time_val_li_info=val_di_movem, \
                                         val_di_que_evol_t_unique=val_di_key_id_phase_val_que_ev_t_unique)

    self.fct_write_file_sum_que_t_sim(li=li_val_sum, val_name_file_write=self._file_sum_queue_evol)
    #********************
    #we write the file with the sum of the desired queues 
    li_t_instances = self.fct_calcul_li_t_instances_some_que_evol(val_di_que_evol=val_di_movem, li_id_considered_phases= \
      [[10003, 10008], [100011, 100014]])

    val_dict_que_evol_t_unique = self.fct_creat_dict_some_que_evol_unique_t_instances(val_dict_que_evol= \
                                                                                        val_di_movem_val_sorted_times_and_sizes, \
                                                                                      li_id_considered_phases= \
                                                                                        [[10003, 10008], [100011, 100014]])

    li_some_sum_ques = self.fct_sum_some_queues(val_di_que_evol_t_unique=val_dict_que_evol_t_unique,
                                                li_t=li_t_instances)

    self.fct_write_file_sum_que_t_sim(li=li_some_sum_ques, val_name_file_write=self._file_sum_desired_queue_evol)
    #*********************
    #we write the file with the average sum of the desired list of queues per period

    self.fct_write_average_sum_ques_per_period_over_nb_t_instances_within_period(va_li_sum_ques=li_some_sum_ques,
                                                                                 va_sim_dur=val_dur_sim, \
                                                                                 va_t_period=val_t_period_for_average_sum_ques,
                                                                                 va_t_unit=val_t_unit,
                                                                                 va_t_init=val_t_init, \
                                                                                 val_name_file= \
                                                                                   File_Stats_Anal_Folders_And_Files.name_file_average_sum_desired_ques_per_period_over_nb_t_instances_within_period, \
                                                                                 val_li_phrases=[
                                                                                   "t start/t end period, avearage value of the sum of the queues"])


    #*********************
    #we write the file with the average sum of all the queues per period

    #self.fct_write_average_sum_ques_per_period_over_nb_t_instances_within_period(va_li_sum_ques=li_val_sum,va_sim_dur=val_dur_sim,\
    #va_t_period=val_t_period_for_average_sum_ques,va_t_unit=val_t_unit,va_t_init=val_t_init,val_name_file=\
    #File_Stats_Anal_Folders_And_Files.name_file_average_sum_ques_per_period_over_nb_t_instances_within_period,\
    #val_li_phrases=["t start/t end period, avearage value of the sum of the queues"])

    #*********************
    #we write the file with the cotnrol evolution at each node

    #di_ctrl_evol_per_nd=ictionary, key id node, value=dict, key = stage id, value=[...,[t start control, t_end control],...]
    di_ctrl_evol_per_nd = self.fct_creat_di_evolution_stage_actuation(val_dict_db_file_1, val_t_unit)

    self.fct_write_files_control_evolution_per_intersection(di=di_ctrl_evol_per_nd, \
                                                            val_li_phrases=[
                                                              "time (1st colm), node indicator (>0 value) if the stage is actuated/0 otherwise (2nd colm)"])

    #*********************
    #we write the filE with the number switches per intersection
    #self.fct_write_file_nb_stage_switches_per_inters(val_dic_ev_type=val_dict_db_file_1,val_li_phrases=["id node (1st colm), nb stage switches (2nd colm)"])
    #*********************

    #we write the file with the mean travel time of each entry-exit link 

    #val_di_info_entry_exit_lk=dict, key=(entry,exit link), value=[mean travel time, nb veh served]
    val_dict_info_entry_exit_lk = self.fct_creat_dict_exit_link_info()

    #val_di_info_mtt_entry_exit_lk=dictionary, key=[id of entry link,id of exit link], value=[mean travel time,nb_veh_exit]
    val_di_info_mtt_entry_exit_lk = self.fct_creat_dict_mean_travel_time_entry_exit_link(
      di_info_entry_exit_lk=val_dict_info_entry_exit_lk, val_round_prec=2)

    self.fct_writing_file_mean_travel_time_entry_exit_lk_nb_veh_served(di=val_di_info_mtt_entry_exit_lk)
    #*********************
    #write the file with the average travel time per period
    #self.fct_calcul_and_write_travel_time_per_time_period_entry_exit_lk(\
    #va_sim_dur=val_dur_sim,va_t_period=val_t_period,va_t_unit=val_t_unit,va_round_prec=2,va_lis_phrases=va_li_phrases,\
    #va_t_init=val_t_init,val_di_info_entry_exit_lk=val_dict_info_entry_exit_lk)

    #*********************
    #we wrte file with the number of vehicles (of the sum of all the queues) and the probability of having this number	

    #di_prob_que_size=dict, key=nb of veh, value=[prob, time with this number of veh at queue]
    di_prob_que_size = self.fct_calc_prob_of_nb_veh_at_queue_and_duration(li_t_que_len=li_val_sum, dur_sim=val_dur_sim)

    #self.fct_writing_prob_of_nb_veh_at_queue(di=di_prob_que_size)

    #*********************
    #we wrtie the file with the weighted mean and standard deviation of queues

    #li_weight_mean_and_sd=list 
    #[weighted mean, stand deviat, mean-stan dev, mean+stan dev]
    li_weight_mean_and_sd = self.fct_calc_weighted_mean_sd_sum_que(dict_nb_veh_que_and_dur=di_prob_que_size,
                                                                   dur_sim=val_dur_sim, val_round_prec=1)

    self.fct_writing_file_weighted_mean_sd_sum_que(li_w_mean_sd=li_weight_mean_and_sd)

    #*********************
    #file with the average time spent by each veh in ques
    #li_t_aver_spent_by_veh_in_que= list, [ dict, the mean value of the average time spent by veh in queues]
    #di_key_mov_val_sorted_li_t_que_length= dict, key=mov, 
    #value =list [  [ ...,sorted li,...]=[ ..[t, que length at t],..], nb of depart veh + veh remained in the que by the end of sim ]
    li_t_aver_spent_by_veh_in_que = self.fct_calcul_average_time_spent_by_veh_in_a_que_for_each_que( \
      di_key_mov_val_sorted_li_t_que_length=val_di_movem_val_sorted_times_and_sizes, val_durat_sim=val_dur_sim, \
      val_round_prec=1)

    self.fct_writing_file_average_time_spent_by_veh_in_a_que_for_each_que(li=li_t_aver_spent_by_veh_in_que)


    #*********************
    #we write the file with the entry internal link evolution

    #di_nb_veh_lk=key=id link, value=[...,[temps,nb veh link],...]
    di_nb_veh_lk = self.fct_creat_dict_current_nb_veh_in_link(v_netw=val_netw,
                                                              dict_db_key_id_event_type_val_record_obj=val_dict_db_file_1)

    self.fct_write_files_entry_internal_link_evol(di_rep=di_nb_veh_lk, va_netw=val_netw)

  #*********************


# *****************************************************************************************************************************************************************************************
#*****************************************************************************************************************************************************************************************



#********************************************************************methods doing the SA of one or  multiple sims***********************************************************
#method doing the statistical analysis of a many sim results, FRes..., placed in a folder
#THE DSU FILE IS EMPLOYED FOR THE NETWORK ONLY, 
#if len(val_li_dsu_files)=1 then the same network is employed for all the sims of which the resutls we want to treat
def fct_stat_anal_multiple_sims(name_folder_FRes, network, v_durat_sim, v_cycle_dur, v_t_end_sim, v_finite_lk_cap, \
                                v_t_period, v_t_unit, v_t_init, v_veh_final_dest_dynam_construct,
                                v_t_period_for_average_sum_ques):
  cur_dir = os.getcwd()
  os.chdir(name_folder_FRes)

  #for each FRes... in the folder we do the stat analysis
  for i in os.listdir('.'):
    if i != ".DS_Store":
      st = Stat_Analysis(val_folder_sim_files_for_stat_anal=i)

      st.fct_writing_files_sa(val_netw=network, val_dur_sim=v_durat_sim, val_cycle_dur=v_cycle_dur, \
                              val_t_end_sim=v_t_end_sim, val_finite_lk_cap=v_finite_lk_cap, \
                              val_t_period=v_t_period, \
                              val_t_period_for_average_sum_ques=v_t_period_for_average_sum_ques, \
                              val_veh_final_dest_dynam_construct=v_veh_final_dest_dynam_construct, \
                              val_name_Fres_folder=i, \
                              val_t_unit=v_t_unit, val_t_init=v_t_init)

  os.chdir(cur_dir)


#*****************************************************************************************************************************************************************************************
#method doing the statistical analysis of files in folder val_name_folder_FRes="SA")

def fct_sa_one_or_series_sim(val_li_dsu_files, val_dur_sim, val_cycle_dur, val_name_folder_FRes, \
                             va_t_end_sim, va_finite_lk_cap, val_imported_module_dsu_fil, va_t_period, va_t_unit,
                             va_t_init, va_t_period_for_average_sum_ques):
  for i in val_li_dsu_files:
    #creation of the network
    cr_netw = Cl_Creation_Network.Creation_Network(val_file_name_user_data=val_li_dsu_files[0])

    a = Cl_Decisions.Decisions()
    #val_creation_lis_ques_output_lk_ids=a.fct_exam_construction_li_id_output_links_of_all_queues_on_a_link(val_imported_module_dsu_file=\
    #val_imported_module_dsu_fil)
    #v_network=cr_netw.function_creation_network(val_creation_li_ques_output_lk_ids=val_creation_lis_ques_output_lk_ids)
    v_network = cr_netw.function_creation_network()

    if val_imported_module_dsu_fil.val_type_veh_final_dest == Cl_Decisions.TYPE_VEHICLE_FINAL_DESTINATION_AND_PATH[
      "dynamically_defined"]:
      v_veh_fin_dest_dyn_constructed = 1
    else:
      v_veh_fin_dest_dyn_constructed = 0

    #we create all the files for each sim
    fct_stat_anal_multiple_sims(name_folder_FRes=val_name_folder_FRes, network=v_network, v_durat_sim=val_dur_sim, \
                                v_cycle_dur=val_cycle_dur, v_t_end_sim=va_t_end_sim, v_finite_lk_cap=va_finite_lk_cap, \
                                v_t_period=va_t_period, v_t_unit=va_t_unit, v_t_init=va_t_init,
                                v_veh_final_dest_dynam_construct=v_veh_fin_dest_dyn_constructed, \
                                v_t_period_for_average_sum_ques=va_t_period_for_average_sum_ques)


#***************************************************************************************************************************************************************************************** 
#method writing in a file the  weighted mean and the standard deviation of a series of sims
def fct_write_file_wm_sd_and_mean_trav_time_series_sims(name_folder_FRes_series_sims, name_file_write, name_file_write2, \
                                                        nb_comment_lines=1):
  cur_dir = os.getcwd()
  #folder_fres_ser_sim = folder with FRes.. files, ex "SA"
  os.chdir(name_folder_FRes_series_sims)

  li = []
  di_key_movm_val_mean_tr_t_nb_veh = {}
  for i in os.listdir('.'):
    #print(i)
    #for each Fres file
    if i != ".DS_Store":
      os.chdir(i)
      file = open("Stat_Anal/fi_mean_length_sum_ques.txt")
      ind = 0
      for j in file.readlines():
        ind += 1
        if ind > nb_comment_lines:
          #weighted mean, stan dev, wm-sd,wm+sd
          a = j.split()
          li.append([eval(a[0]), eval(a[1])])

      file2 = open("Stat_Anal/MEAN_TR_TIME_EN_EX_LK/fi_mean_trav_time_entry_exit_lk.txt")
      ind1 = 0
      for n in file2.readlines():
        ind1 += 1
        if ind1 > nb_comment_lines:
          a1 = n.split()

          if (eval(a1[0]), eval(a1[1])) not in di_key_movm_val_mean_tr_t_nb_veh.keys():
            di_key_movm_val_mean_tr_t_nb_veh[eval(a1[0]), eval(a1[1])] = [[eval(a1[2]), eval(a1[3])]]

          else:
            di_key_movm_val_mean_tr_t_nb_veh[eval(a1[0]), eval(a1[1])].append([eval(a1[2]), eval(a1[3])])
          #print("HERE",di_key_movm_val_mean_tr_t_nb_veh[eval(a1[0]),eval(a1[1])])

      os.chdir(cur_dir)
      os.chdir(name_folder_FRes_series_sims)
      file.close()
      file2.close()

  #print("di_key_movm_val_mean_tr_t_nb_veh",di_key_movm_val_mean_tr_t_nb_veh)	
  #print()
  #print("li",li)

  di = Global_Functions.fct_calcul_mean_trav_time_and_nb_dep_veh_series_sims(dict_inf=di_key_movm_val_mean_tr_t_nb_veh)

  os.chdir(cur_dir)
  file1 = open(name_folder_FRes_series_sims + "/" + name_file_write, "w")
  file1.write("%s\t %s \n" % ("WEIGHTED MEAN SER (1)", "STAN. DEV SER (2)"))
  for i in li:
    file1.write("%.2f\t %.2f\t \n" % (i[0], i[1]))
  file1.close()

  file3 = open(name_folder_FRes_series_sims + "/" + name_file_write2, "w")
  file3.write("%s\t %s\t %s\t %s \n" % (
  "ID ENTRY LK (1)", "ID EXIT LINK (2)", "MEAN TRAVEL TIME SER (3)", "MEAN NB DEPART VEH SERIES (4)"))

  for i in di:
    file3.write("%d\t %d\t %.2f\t %.2f\t \n" % (i[0], i[1], di[i][0], di[i][1]))
  file1.close()


#*****************************************************************************************************************************************************************************************
#method writing the max value of the sum of the queues for each sim
def fct_write_file_max_min_value_sum_ques_series_sims(name_folder_FRes_series_sims, name_file_write, name_file_write_1):
  cur_dir = os.getcwd()
  os.chdir(name_folder_FRes_series_sims)

  li = []
  for i in os.listdir('.'):
    if i != "fi_mean_tr_t_nb_dep_veh_series_sims.txt" and i != "fi_wm_sd_series_sim.txt" and i != "wm-sd-series-sims.gif" and i != ".DS_Store":
      #print(i)
      #import sys
      #sys.exit()
      os.chdir(i)
      file = open("Stat_Anal/QUE_EVOL_SUM/fi_sum_evol_que.txt", "r")

      li_1 = []

      #each line is: time, queue size
      for i in file.readlines():
        a = i.rsplit()

        li_1.append(eval(a[1]))

      li.append(max(li_1))
      file.close()
    os.chdir(cur_dir)
    os.chdir(name_folder_FRes_series_sims)
  #file.close()

  os.chdir(cur_dir)
  file1 = open(name_folder_FRes_series_sims + "/" + name_file_write, "w")
  file1.write("%s\ \n" % ("MAX LENGTH  EACH SUM QUE"))
  for i in li:
    file1.write("%.2f \n" % (i))
  file1.close()
  file2 = open(name_folder_FRes_series_sims + "/" + name_file_write_1, "w")
  file2.write("%s\t  %s \n" % ("MIN OF MAX LENGTH SUM QUES(1)", "MAX LENGTH SUM QUES(2)"))
  a = min(li)
  b = max(li)
  file2.write("%.2f\t %.2f \n" % (a, b))
  file2.close()


#*****************************************************************************************************************************************************************************************


#the "Dsu_1" is employed for defing the network employed and the sim duration. 
#This info has to  be the same for all the sims  of a series.
#If we do  series of sims we can still employe the Dsu file of the 1st sim, since they are all employing the same network.
#ATTENTIOJN ALL THE SIMS OF THE SERIES SHOULD HAVE THE SAME VALUES IN THE DSU COCNERNING THE CYCLE DURATION  AND
#TYPE VEH FINAL DESTINATION, FINAL CAPACITY INTERNAL LINK
val_li_dsu_fi = ["Dsu_1"]
module_Dsu = __import__("Dsu_1")
module_file_stat_anal_folders_and_files = __import__(
  File_Sim_Name_Module_Files.val_name_file_stat_anal_folders_and_files)

val_name_fol_FRes = "Series_Sim-Wed-02-Jul-2014_23-06-21"




#anal stat classique, on appelle fcts, fct_sa_one_or_series_sim,fct_write_file_wm_sd_and_mean_trav_time_series_sims,\
#fct_write_file_max_min_value_sum_ques_series_sims
val_t_start_sim = 0
val_sim_dur = module_Dsu.t_simulation_duration
val_fin_sim = round(val_t_start_sim + val_sim_dur, 2)

val_ti_period = 300
#val_ti_period_for_average_sum_ques=10
val_ti_period_for_average_sum_ques = 300
val_ti_unit = 0.1
val_round_precis = 2
va_init_interval = 0

#the start time of the sim.  IF A PREVIOUS SIM IS CONTINUED IT HAS TO USE THE T START OF THE SIM, OR THE T_END+T_UNIT
#OF THE PREVIOUS SIM
va_t_init = 0

#print(val_fin_sim)
fct_sa_one_or_series_sim(val_li_dsu_files=val_li_dsu_fi, val_dur_sim=module_Dsu.t_simulation_duration, \
                         val_cycle_dur=module_Dsu.cycle_duration, \
                         val_name_folder_FRes=val_name_fol_FRes, \
                         va_t_end_sim=val_fin_sim, \
                         va_finite_lk_cap=module_Dsu.val_finite_capacity_internal_links, \
                         val_imported_module_dsu_fil=module_Dsu, \
                         va_t_period=val_ti_period, va_t_unit=val_ti_unit, va_t_init=va_t_init, \
                         va_t_period_for_average_sum_ques=val_ti_period_for_average_sum_ques)

########
#fct_write_file_wm_sd_series_sims(name_folder_FRes_series_sims=val_name_fol_FRes,\
#name_file_write=module_file_stat_anal_folders_and_files.val_name_file_wm_sd_series_sim,nb_comment_lines=1)
########

fct_write_file_wm_sd_and_mean_trav_time_series_sims(name_folder_FRes_series_sims=val_name_fol_FRes, \
                                                    name_file_write=module_file_stat_anal_folders_and_files.val_name_file_wm_sd_series_sim,
                                                    name_file_write2=module_file_stat_anal_folders_and_files.val_name_file_mean_tr_t_nb_dep_veh_series_sims,
                                                    nb_comment_lines=1)

fct_write_file_max_min_value_sum_ques_series_sims(name_folder_FRes_series_sims=val_name_fol_FRes, \
                                                  name_file_write=module_file_stat_anal_folders_and_files.val_name_file_max_size_each_sum_ques_series_sims, \
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






























