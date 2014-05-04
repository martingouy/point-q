import csv
import os,shutil
import sys
import itertools
import datetime
from datetime import *
import time
from time import *
import Cl_Event
import File_Sim_Name_Module_Files


class Record_and_Treat_Sim_File_Names:

	"""class creating all the files for recording during the simulation and treating the sim results when this is desired """
	
	def __init__(self,val_name_sim_record_file_names="Record_and_Treat_Sim_File_Names",\
	val_open_mode_file_recording_sim_text="w",val_open_mode_file_recording_sim_db="w",val_folder_series_sims=None):
	
	
		#the name of the file where the name of the recording files are written
		self._name_sim_record_file_names=val_name_sim_record_file_names
	
		#the name of the module importing the file where the name of the recording files are written
		self._module_name_sim_record_file_names=__import__(self._name_sim_record_file_names)
		
		self._folder_series_sims=val_folder_series_sims
		
		#the file with the names of the folders and files for the stat analysis, "File_Stats_Anal_Folders_And_Files"
		#self._file_stats_name_files=File_Sim_Name_Module_Files.val_name_file_stat_anal_folders_and_files
		
		#the module importing the file with the names of folders/files for the stat anaylis
		#self._module_name_importing_file_names_stat_anal=__import__(self._file_stats_name_files)
	
	#***************************************************************  names of the folders ************************************************************************************ 
	
		#the name of the folder where the sim results will be saved, FRes
		self._name_folder_res_sim=self._module_name_sim_record_file_names.val_name_folder_res_sim
	
		#the name of the folder containing the files produced by the treatement procedure of a simulation,"Sim_Treat"
		self._name_folder_with_files_created_by_sim_treat=self._module_name_sim_record_file_names.val_name_folder_with_files_created_by_sim_treat
	
		#the name of the folder containing the vehicle files created by  the sim treatement 
		#"VEH_RES"
		self._name_folder_with_files_created_by_sim_veh_treat=self._module_name_sim_record_file_names.val_name_folder_with_files_created_by_sim_veh_treat
	
	#***************************************************************  names of the files ****************************************************************************************** 
	  
		#the name of the file where  the simulation events will be recorded as a text document,"f"
		self._name_file_recording_sim_ev_text=self._module_name_sim_record_file_names.val_name_file_recording_sim_ev_text
	
	
		#the name of the file where we stock the final state of the  network in the simulation object,
		#employed when we wish to continue a previously made sim, "f_netw_obj_sim"
		self._name_file_recording_network_obj_sim=self._module_name_sim_record_file_names.val_name_file_recording_network_obj_sim
		
		
		#the name of the file where we store the final state of the event pile in the simulation object
		self._name_file_recording_pile_even_obj_sim=self._module_name_sim_record_file_names.val_name_file_recording_pile_even_obj_sim
		
		#the name of the file where we stock the next vehicle id, by the end of a sim
		self._name_file_recording_next_veh_id_obj_sim=self._module_name_sim_record_file_names.val_name_file_recording_next_veh_id_obj_sim
	
		#the name of the file where  each event will be recorded for the database,"file_recording_event_db.txt"
		self._name_file_recording_event_db=self._module_name_sim_record_file_names.val_name_file_recording_event_db
	
	
		#the name of the file  where we register the information of the veh appearance events "f_pile_even_obj_sim "
		#remaining in the event pile by the end of the sim (these are the future veh appear starting after the end of the sim)
		#"file_veh_appear_event_remain_in_event_list_end_sim.txt"
		self._name_file_recording_veh_appear_event_remaining_in_ev_list_by_end_sim_before_open=\
		self._module_name_sim_record_file_names.val_name_file_recording_veh_appear_event_remaining_in_ev_list_by_end_sim
	
	
		#the name of the file with the each veh hist,"Historic_Veh_"
		#when a sim will be treated we will create a file for each vehicle, containing the evh info during the sim.
		#This will the name of the veh file, associated with the veh id,ex "Historic_Veh_1"
		self._name_file_veh_res=self._module_name_sim_record_file_names.val_name_file_veh_res
		
		
	
	#***************************************************************  creation of the folders and their associated files *************************************************************************
	
	
		#creation of the folder where to place the Fres files when one or more sims are done
		#creation of a folder where we place all the Fres files created by the series of sims
		#b=strftime("-%a-%d-%b-%Y_%H-%M-%S",localtime())
		#os.mkdir(self._module_name_importing_file_names_stat_anal.name_folder_series_sims+b)
		
		#self._folder_series_sims=self._module_name_importing_file_names_stat_anal.name_folder_series_sims+b
		
		#creation of the folder where the simulations results will be placed, FRes_date
		b=strftime("-%a-%d-%b-%Y_%H-%M-%S",localtime())
		os.mkdir(self._folder_series_sims+"/"+self._name_folder_res_sim+b)
	
		self._folder_res_sim=self._folder_series_sims+"/"+self._name_folder_res_sim+b
	
		#the file where we stock tthe final state of the  network in the simulation object
		self._file_recording_network_obj_sim=self._folder_res_sim+"/"+self._name_file_recording_network_obj_sim
		
		#the file  where we register the information of the veh appearance events "f_pile_even_obj_sim "
		self._file_recording_pile_even_obj_sim=self._folder_res_sim+"/"+self._name_file_recording_pile_even_obj_sim
		
		#the file where we stock the next vehicle id, by the end of a sim
		self._file_recording_next_veh_id_obj_sim=self._folder_res_sim+"/"+self._name_file_recording_next_veh_id_obj_sim
	
		# the opening mode of the text file where the sim events (sim evolution) are written explicitly 
		self._open_mode_file_recording_sim_text=val_open_mode_file_recording_sim_text
		
		#the file where the sim events are written explicitly (text), placed in the corresponding directory
		self._file_recording_sim_text_before_open=self._folder_res_sim+"/"+self._name_file_recording_sim_ev_text
	
		#the open mode of the file where each event will be recorded for the database
		self._open_mode_file_recording_sim_db=val_open_mode_file_recording_sim_db
		
		#the file where each event will be recorded for the database,before opening the file already placed in the appropriate directory
		#FRes-Thu-26-Jul-2012_19-20-23/file_recording_event_db.txt
		self._file_recording_event_db_before_open=self._folder_res_sim+"/"+self._name_file_recording_event_db
	
		#the folder containing the files created when the simulation results will be treated ("Sim_Treat")
		os.mkdir(self._folder_res_sim+"/"+self._name_folder_with_files_created_by_sim_treat)
	
		self._folder_with_files_created_by_sim_treat=self._folder_res_sim+"/"+self._name_folder_with_files_created_by_sim_treat
	
		#creation of the folder containing the vehicle files created by the treatment of a sim treatement 
		#"Sim_Treat"/"VEH_RES"
		os.mkdir(self._folder_with_files_created_by_sim_treat+"/"+self._name_folder_with_files_created_by_sim_veh_treat)
	
		#the folder with the veh results when we are already in the Fres.. folder
		#FRes_date/"Sim_Treat"/"VEH_RES"
		self._folder_with_veh_files_created_by_sim_treat=\
		self._folder_with_files_created_by_sim_treat+"/"+self._name_folder_with_files_created_by_sim_veh_treat
		
		#the folder with the veh results when we are already in the Fres.. folder
		#"Sim_Treat"/"VEH_RES"
		#we shall use it when a previously generated  veh demand will be employed for a sim run
		self._folder_with_veh_files_created_by_sim_treat_1=\
		self._name_folder_with_files_created_by_sim_treat+"/"+self._name_folder_with_files_created_by_sim_veh_treat
		
		
	
		#the file with the vehicle appearance events remained in the event list by the end in the simulation, 
		#this file is placed in the appropriate directory (Fres_date)
		self._file_recording_veh_appear_event_remaining_in_ev_list_by_end_sim_before_open=\
		self._folder_res_sim+"/"+self._name_file_recording_veh_appear_event_remaining_in_ev_list_by_end_sim_before_open
		
		
		#the file already place in the appropriate directory where the veh results will be written "Historic_Veh_"
		self._file_veh_res=self._folder_with_veh_files_created_by_sim_treat+"/"+self._name_file_veh_res
	
	
#*****************************************************************************************************************************************************************************************
	#method returning the name of the file where the name of the recording files are written
	def get_name_sim_record_file_names(self):
		return self._name_sim_record_file_names

#*****************************************************************************************************************************************************************************************
	#method returning the name of the module importing the file where the name of the recording files are written
	def get_module_name_sim_record_file_names(self):
		return self._module_name_sim_record_file_names
#*****************************************************************************************************************************************************************************************
	#method returning the name of the folder where the sim results will be saved, FRes
	def get_name_folder_res_sim(self):
		return self._name_folder_res_sim

#*****************************************************************************************************************************************************************************************
	#method returning the name of the folder containing the files produced by the treatement procedure of a simulation,"Sim_Treat"
	def get_name_folder_with_files_created_by_sim_treat(self):
		return self._name_folder_with_files_created_by_sim_treat

#*****************************************************************************************************************************************************************************************
	#method returning the name of the folder containing the vehicle files created by  the sim treatement "VEH_RES"
	def get_name_folder_with_files_created_by_sim_veh_treat(self):
		return self._name_folder_with_files_created_by_sim_veh_treat

#*****************************************************************************************************************************************************************************************
	#method returning the name of the file where  the simulation events will be recorded as a text document,"f"
	def get_name_file_recording_sim_ev_text(self):
		return self._name_file_recording_sim_ev_text


#*****************************************************************************************************************************************************************************************
	#method returning the name of the file where we stock the final state of the  network in the simulation object,
	#employed when we wish to continue a previously made sim, "f_netw_obj_sim"
	def get_name_file_recording_network_obj_sim(self):
	
		return self._name_file_recording_network_obj_sim

#*****************************************************************************************************************************************************************************************
	#method returning the name of the file where we store the final state of the event pile in the simulation object
	def get_name_file_recording_pile_even_obj_sim(self):
		return self._name_file_recording_pile_even_obj_sim
#*****************************************************************************************************************************************************************************************
	#method returning the name of the file where we stock the next vehicle id, by the end of a sim
	def get_name_file_recording_next_veh_id_obj_sim(self):
		return self._name_file_recording_next_veh_id_obj_sim

#*****************************************************************************************************************************************************************************************
	#method returning the name of the file where  each event will be recorded for the database,"file_recording_event_db.txt"
	def get_name_file_recording_event_db(self):
		return self._name_file_recording_event_db

#*****************************************************************************************************************************************************************************************
	#method returning the name of the file  where we register the information of the veh appearance events 
	#remaining in the event pile by the end of the sim (these are the future veh appear starting after the end of the sim)
	#"file_veh_appear_event_remain_in_event_list_end_sim.txt"
	
	def get_name_file_recording_veh_appear_event_remaining_in_ev_list_by_end_sim_before_open(self):
		return self._name_file_recording_veh_appear_event_remaining_in_ev_list_by_end_sim_before_open

#*****************************************************************************************************************************************************************************************
	#method returning the name of the file with the each veh hist,"Historic_Veh_"
	#when a sim will be treated we will create a file for each vehicle, containing the evh info during the sim.
	#This will the name of the veh file, associated with the veh id,ex "Historic_Veh_1"
	def get_name_file_veh_res(self):
		return self._name_file_veh_res
#*****************************************************************************************************************************************************************************************
	#method returning the folder where to place the Fres files when one or more sims are done
	def get_folder_series_sims(self):
		return self._folder_series_sims

#*****************************************************************************************************************************************************************************************
	#method returning the folder where the simulations results will be placed, FRes_date
	def get_folder_res_sim(self):
		return self._folder_res_sim

#*****************************************************************************************************************************************************************************************
	#method returning the file where we stock the final state of the network in the simulation object (placed in the appropriate directory)
	def get_file_recording_network_obj_sim(self):
		return self._file_recording_network_obj_sim
#*****************************************************************************************************************************************************************************************
	#method returning the file  where we register the information of the veh appearance events "f_pile_even_obj_sim "
	def get_file_recording_pile_even_obj_sim(self):
		return self._file_recording_pile_even_obj_sim
#*****************************************************************************************************************************************************************************************
	#method returning the file where we stock the next vehicle id, by the end of a sim
	def get_file_recording_next_veh_id_obj_sim(self):
		return self._file_recording_next_veh_id_obj_sim
	
#*****************************************************************************************************************************************************************************************
	#method returning the  opening mode of the text file where the sim events (sim evolution) are written explicitly 
	def get_open_mode_file_recording_sim_text(self):
		return self._open_mode_file_recording_sim_text

#*****************************************************************************************************************************************************************************************
	#method returning the file where the sim events are written explicitly (text), placed in the corresponding directory
	def get_file_recording_sim_text_before_open(self):
		return self._file_recording_sim_text_before_open

#*****************************************************************************************************************************************************************************************
	#method returning the open mode of the file where each event will be recorded for the database
	def get_open_mode_file_recording_sim_db(self):
		return self._open_mode_file_recording_sim_db

#*****************************************************************************************************************************************************************************************
	#method returning the file where each event will be recorded for the database,before opening the file already placed in the appropriate directory
	#FRes-Thu-26-Jul-2012_19-20-23/file_recording_event_db.txt
	def get_file_recording_event_db_before_open(self):
		return self._file_recording_event_db_before_open

#*****************************************************************************************************************************************************************************************

	#method returning the folder containing the files created when the simulation results will be treated ("Sim_Treat")
	def get_folder_with_files_created_by_sim_treat(self):
		return self._folder_with_files_created_by_sim_treat

#*****************************************************************************************************************************************************************************************
	#method returning the folder containing the vehicle files created by the treatment of a sim treatement 
	#/FRes_date/"Sim_Treat"/"VEH_RES"
	def get_folder_with_veh_files_created_by_sim_treat(self):
		return self._folder_with_veh_files_created_by_sim_treat
	
#*****************************************************************************************************************************************************************************************
	#method returning the folder containing the vehicle files created by the treatment of a sim treatement 
	#"Sim_Treat"/"VEH_RES"
	def get_folder_with_veh_files_created_by_sim_treat_1(self):
		return self._folder_with_veh_files_created_by_sim_treat_1
#*****************************************************************************************************************************************************************************************
	#method returning the file with the vehicle appearance events remained in the event list by the end in the simulation, 
	#this file is placed in the appropriate directory (Fres_date)
	def get_fle_recording_veh_appear_event_remaining_in_ev_list_by_end_sim_before_open(self):
		return self._fle_recording_veh_appear_event_remaining_in_ev_list_by_end_sim_before_open
#*****************************************************************************************************************************************************************************************
	#method returning the file already place in the appropriate directory where the veh results will be written "Historic_Veh_"
	def get_file_veh_res(self):
		return self._file_veh_res

#*****************************************************************************************************************************************************************************************
	
	#method modifying the name of the file where the name of the recording files are written
	def set_name_sim_record_file_names(self,n_v):
		self._name_sim_record_file_names=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the name of the module importing the file where the name of the recording files are written
	def set_module_name_sim_record_file_names(self,n_v):
		self._module_name_sim_record_file_names=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the folder where to place the Fres files when one or more sims are done
	def set_folder_series_sims(self,n_v):
		self._folder_series_sims=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the name of the folder where the sim results will be saved, FRes
	def set_name_folder_res_sim(self,n_v):
		self._name_folder_res_sim=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the name of the folder containing the files produced by the treatement procedure of a simulation,"Sim_Treat"
	def set_name_folder_with_files_created_by_sim_treat(self,n_v):
		elf._name_folder_with_files_created_by_sim_treat=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the name of the folder containing the vehicle files created by  the sim treatement "VEH_RES"
	def set_name_folder_with_files_created_by_sim_veh_treat(self,n_v):
		self._name_folder_with_files_created_by_sim_veh_treat=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the folder containing the vehicle files created by the treatment of a sim treatement 
	#"Sim_Treat"/"VEH_RES"
	def set_folder_with_veh_files_created_by_sim_treat_1(self,n_v):
		self._folder_with_veh_files_created_by_sim_treat_1=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the name of the file where  the simulation events will be recorded as a text document,"f"
	def set_name_file_recording_sim_ev_text(self,n_v):
		self._name_file_recording_sim_ev_text=n_v


#*****************************************************************************************************************************************************************************************
	#method modifying the name of the file where we stock the final state of the network in the simulation object,
	#employed when we wish to continue a previously made sim, "f_netw_obj_sim"
	def set_name_file_recording_network_obj_sim(self,n_v):
		self._name_file_recording_network_obj_sim=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the name of the file where we store the final state of the event pile in the simulation object
	def set_name_file_recording_pile_even_obj_sim(self,n_v):
		self._name_file_recording_pile_even_obj_sim=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the name of the file where we stock the next vehicle id, by the end of a sim
	def set_name_file_recording_next_veh_id_obj_sim(self,n_v):
		self._name_file_recording_next_veh_id_obj_sim=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the name of the file where  each event will be recorded for the database,"file_recording_event_db.txt"
	def set_name_file_recording_event_db(self,n_v):
		self._name_file_recording_event_db=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the name of the file  where we register the information of the veh appearance events 
	#remaining in the event pile by the end of the sim (these are the future veh appear starting after the end of the sim)
	#"file_veh_appear_event_remain_in_event_list_end_sim.txt"
	
	def set_name_file_recording_veh_appear_event_remaining_in_ev_list_by_end_sim_before_open(self,n_v):
		self._name_file_recording_veh_appear_event_remaining_in_ev_list_by_end_sim_before_open=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the name of the file with the each veh hist,"Historic_Veh_"
	#when a sim will be treated we will create a file for each vehicle, containing the evh info during the sim.
	#This will the name of the veh file, associated with the veh id,ex "Historic_Veh_1"
	def set_name_file_veh_res(self,n_v):
		self._name_file_veh_res=n_v


#*****************************************************************************************************************************************************************************************
	#method modifying the folder where the simulations results will be placed, FRes_date
	def set_folder_res_sim(self,n_v):
		self._folder_res_sim=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the file where we stock the final state of the network in the simulation object (placed in the appropriate directory)
	def set_file_recording_network_obj_sim(self,n_v):
		self._file_recording_network_obj_sim=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the file  where we register the information of the veh appearance events "f_pile_even_obj_sim "
	def set_file_recording_pile_even_obj_sim(self,n_v):
		self._file_recording_pile_even_obj_sim=n_v
	
#*****************************************************************************************************************************************************************************************
	#method modifying the file where we stock the next vehicle id, by the end of a sim
	def set_file_recording_next_veh_id_obj_sim(self,n_v):
		self._file_recording_next_veh_id_obj_sim=n_v      
	
#*****************************************************************************************************************************************************************************************
	#method modifying the  opening mode of the text file where the sim events (sim evolution) are written explicitly 
	def set_open_mode_file_recording_sim_text(self,n_v):
		self._open_mode_file_recording_sim_text=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the file where the sim events are written explicitly (text), placed in the corresponding directory
	def set_file_recording_sim_text_before_open(self,n_v):
		self._file_recording_sim_text_before_open=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the open mode of the file where each event will be recorded for the database
	def set_open_mode_file_recording_sim_db(self,n_v):
		self._open_mode_file_recording_sim_db=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the file where each event will be recorded for the database,before opening the file already placed in the appropriate directory
	#FRes-Thu-26-Jul-2012_19-20-23/file_recording_event_db.txt
	def set_file_recording_event_db_before_open(self,n_v):
		self._file_recording_event_db_before_open=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the folder containing the files created when the simulation results will be treated ("Sim_Treat")
	def set_folder_with_files_created_by_sim_treat(self,n_v):
		self._folder_with_files_created_by_sim_treat=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the folder containing the vehicle files created by the treatment of a sim treatement 
	#"Sim_Treat"/"VEH_RES"
	def set_folder_with_veh_files_created_by_sim_treat(self,n_v):
		self._folder_with_veh_files_created_by_sim_treat=n_v
	
#*****************************************************************************************************************************************************************************************
	#method modifying the file with the vehicle appearance events remained in the event list by the end in the simulation, 
	#this file is placed in the appropriate directory (Fres_date)
	def set_file_recording_veh_appear_event_remaining_in_ev_list_by_end_sim_before_open(self,n_v):
		self._fle_recording_veh_appear_event_remaining_in_ev_list_by_end_sim_before_open=n_v


#*****************************************************************************************************************************************************************************************
	#method modifying the file already place in the appropriate directory where the veh results will be written "Historic_Veh_"
	def set_file_veh_res(self,n_v):
		self._file_veh_res=n_v

#*****************************************************************************************************************************************************************************************
	
	#method preparing the record files before starting a simulation (we are opening them)
	def preparation_record_files_before_start_sim(self):
		
		#creation of the self._file_recording_sim_text_before_open, open state
		self._file_recording_sim_text=open(self._file_recording_sim_text_before_open,self._open_mode_file_recording_sim_text)
	
		#creation of the self._file_recording_event_db_before_open, open state, 
		self._file_recording_event_db_csv=open(self._file_recording_event_db_before_open,self._open_mode_file_recording_sim_db)
		
		#(we pass it to cvs)
		self._file_recording_event_db=csv.writer(self._file_recording_event_db_csv)
		
		#the file where we write the veh appear event infor remained in the event list by the end of the sim
		self._file_recording_veh_appear_event_remaining_in_ev_list_by_end_sim_cvs=open(\
		self._file_recording_veh_appear_event_remaining_in_ev_list_by_end_sim_before_open,self._open_mode_file_recording_sim_db)
		
		#we pass it to cvs
		self._file_recording_veh_appear_event_remaining_in_ev_list_by_end_sim=csv.writer(\
		self._file_recording_veh_appear_event_remaining_in_ev_list_by_end_sim_cvs)
#*****************************************************************************************************************************************************************************************
	
	#method returning the file where the sim events will be registered  as a text file. 
	#This file is created in function preparation_record_files_before_start_sim
	def get_file_recording_sim_text(self):
		return self._file_recording_sim_text
	
#*****************************************************************************************************************************************************************************************
	#method returing the cvs file for the db event recording 
	def get_file_recording_event_db_csv(self):
		return self._file_recording_event_db_csv
#*****************************************************************************************************************************************************************************************
	#method returing the file for the db event recording
	def get_file_recording_event_db(self):
		return self._file_recording_event_db
#*****************************************************************************************************************************************************************************************
	#method returning the cvs file containing the veh appearance infor remained in the event list by the end of sim
	def get_file_recording_veh_appear_event_remaining_in_ev_list_by_end_sim_cvs(self):
		return self._file_recording_veh_appear_event_remaining_in_ev_list_by_end_sim_cvs

#*****************************************************************************************************************************************************************************************
	#method returning the file containing the veh appearance infor remained in the event list by the end of sim
	def get_file_recording_veh_appear_event_remaining_in_ev_list_by_end_sim(self):
		return self._file_recording_veh_appear_event_remaining_in_ev_list_by_end_sim
	
#*****************************************************************************************************************************************************************************************
	#method modifying the file where the sim events will be registered  as a text file. 
	#This file is created in function preparation_record_files_before_start_sim
	def set_file_recording_sim_text(self,n_v):
		self._file_recording_sim_text=n_v
	
#*****************************************************************************************************************************************************************************************
	#method modifying the cvs file for the db event recording 
	def set_file_recording_event_db_csv(self,n_v):
		self._file_recording_event_db_csv=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the file for the db event recording
	def set_file_recording_event_db(self,n_v):
		self._file_recording_event_db=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the cvs file containing the veh appearance infor remained in the event list by the end of sim
	def set_file_recording_veh_appear_event_remaining_in_ev_list_by_end_sim_cvs(self,n_v):
		self._file_recording_veh_appear_event_remaining_in_ev_list_by_end_sim_cvs=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the file containing the veh appearance infor remained in the event list by the end of sim
	def set_file_recording_veh_appear_event_remaining_in_ev_list_by_end_sim(self,n_v):
		self._file_recording_veh_appear_event_remaining_in_ev_list_by_end_sim=n_v
	
#*****************************************************************************************************************************************************************************************
	
	#method preparing the record files by the end of the sim
	def preparation_record_files_after_end_sim(self):
		
		#we close the file where the sim evolution is written in words
		self._file_recording_sim_text.close()
		
		#we close the cvs file for the db event recording
		self._file_recording_event_db_csv.close()
		
		#we close the cvs file where we write the veh appear inform remained in the event list after the end of sim
		self._file_recording_veh_appear_event_remaining_in_ev_list_by_end_sim_cvs.close

#*****************************************************************************************************************************************************************************************
	#method writing in a file the information of  the veh appearance events remained in the event list by the end of the sim
	#this info will be used when we wish to do a new sim employing a previsouly generated veh demand
	def fct_write_information_veh_appearance_event_in_ev_list_end_sim(self,val_event_list):
	
		for i in val_event_list:
			if i.get_event_type()==Cl_Event.TYPE_EV["type_ev_veh_appearance"]:
				self._file_recording_veh_appear_event_remaining_in_ev_list_by_end_sim.writerow([i.get_event_time(),\
				i.get_id_entry_link(),i.get_current_veh_id_demand_previous_sim()])

#*****************************************************************************************************************************************************************************************
	
	#method copying a txt  file into the sim res folder created by sim, FRes_data..
	def fct_copy_file_in_sim_res_folder(self,name_folder_name_file,name_file,val_name):
		#a=os.getcwd()
		#print("here",a)
		#print(name_folder_name_file+"/"+name_file)
		
		shutil.copy(name_folder_name_file+"/"+name_file,self._folder_res_sim+"/"+val_name)
		

#*****************************************************************************************************************************************************************************************
	#method copying a python file into the sim res folder created by sim, FRes_date..
	def fct_copy_file_in_sim_res_folder1(self,name_file,val_name):
		shutil.copy(name_file+".py",self._folder_res_sim+"/"+val_name)
		

#*****************************************************************************************************************************************************************************************
#method copying a python file into the sim res folder created by sim, FRes_date..
	def fct_copy_file_in_sim_res_folder2(self,name_file,val_name):
		shutil.copy(name_file,self._folder_res_sim+"/"+val_name)
		

#*****************************************************************************************************************************************************************************************	
















	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	