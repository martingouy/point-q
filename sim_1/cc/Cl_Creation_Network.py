import Cl_Network
import Global_Functions
import Cl_Network_Link
import Cl_Network_Entry_Link
import Cl_Network_Exit_Link
import Cl_Network_Internal_Link
import Cl_Set_Vehicle_Queues_Link
import Cl_Intersection
import Cl_Intersection_Signalised
import Cl_Intersection_Non_Signalised
import Cl_Control_Actuate
import List_Explicit_Values
import Global_Functions
import Global_Functions_Network
import Global_Functions_Controls
import File_Sim_Name_Module_Files
import File_names_network_model
import Cl_System_Model
import Cl_Decisions


import random
import pickle


class Creation_Network:

	""" class creating a network object from data files"""
	
	
	def __init__(self,val_file_name_user_data,val_name_file_containing_file_names_model_network="File_names_network_model"):
	
		
		#a=Cl_System_Model.System_Model()
		#the object for modelling the system
		#self._sys_model_obj=a
		
		#the name of the module importing the file with the user data, val_file_name_user_data=Dsu
		self._module_name_import_sim_user_data=__import__(val_file_name_user_data)
		
		
		#the name of the module importing the file with the files names modelling the network, 
		self._module_name_import_file_names_model_network=__import__(val_name_file_containing_file_names_model_network)
	
		#the name of the folder containing the data files for modelling the network,"SMALL_DATA_INTERS_3"
		self._name_data_folder=self._module_name_import_sim_user_data.val_name_folder_network_files
	
		#the name of the file containing the id of the node and the id of the entering links to the node
		#this file will be employed when constructing the intersection nodes 
		self._file_name_id_node_id_entering_links_to_node=self._module_name_import_file_names_model_network.val_file_name_id_node_id_entering_links_to_node
	
	
		#the name of the file containing the id of the node and the id of the leaving links from the node
		#this file will be employed when constructing the intersection nodes
		self._file_name_id_node_id_leaving_links_from_node=self._module_name_import_file_names_model_network.val_file_name_id_node_id_leaving_links_from_node
	
		#the name of the file containing the id of the (head node) and the id of the corresponding entry links to  the network
		#it will be employed for the construction of the entry links of the network
		self._file_name_id_node_id_entry_links_to_network=self._module_name_import_file_names_model_network.val_file_name_id_node_id_entry_links_to_network
		
		#the name of the file containing the id of the (tail node) and the id of the corresponding exit links from the network
		#it will be employed for the construction of the exti links of the network
		self._file_name_id_node_id_exit_links_from_network=self._module_name_import_file_names_model_network.val_file_name_id_node_id_exit_links_from_network
	
		#the name of the file containing the id of the internal link and the id of the corresponding head and tail nodes of the link
		#it will be employed for the construction of the internal links of the network
		self._file_name_id_internal_link_id_orig_dest_node=self._module_name_import_file_names_model_network.val_file_name_id_internal_link_id_orig_dest_node
		
		
		#the name of the file defining the the max queue size, the saturation flow and the que type of each phase (queue, (l,m))
		#the first column is the id of a network link, the 2nd column is the id of the output link (phase), 
		#the 3rd column is the the max queue size of the link (1st column) and the 4th column is the 
		#saturation flow of the phase and the 5th column is 1 or 0 according as if the (l,m) movement
		#is/not a right turn
		self._file_name_id_all_phases_max_queue_size_and_sat_flow_queue_type=\
		self._module_name_import_file_names_model_network.\
		val_file_name_id_all_phases_max_queue_size_and_sat_flow_queue_type
		
		
		#the name of the file containing the id of all network links, the id of their origin and destination nodes, the lenght of the link and the
		#param of travel duration
		self._file_name_id_all_network_link_id_orig_dest_node_length_link_capacity_link_param_travel_duration=\
		self._module_name_import_file_names_model_network.\
		val_file_name_id_all_network_link_id_orig_dest_node_length_link_capacity_link_param_travel_duration
		
		#the name of the file containing the id of the  links and the id of the asociated entry links.
		#self._file_name_id_link_id_sublinks=self._module_name_import_file_names_model_network.val_file_name_id_link_id_sublinks
		
		#the name of the file containing the demand parameter of an entry link
		self._file_name_demand_param_entry_link=File_names_network_model.val_file_name_demand_param_entry_link
		
		#the name of the file with the id of all network links the id of the origin and destination nodes of the link and the length of the link
		self._id_all_network_link_id_orig_dest_node_length_link_capacity_link_param_travel_duration=\
		self._file_name_id_all_network_link_id_orig_dest_node_length_link_capacity_link_param_travel_duration
		
		#the name of the file with the id of the minor phases and their associat prior phases
		#self._name_file_id_nd_id_minor_phase_id_prior_phase=self._module_name_import_file_names_model_network.\
		#val_name_file_id_nd_id_minor_phase_id_prior_phase
#*****************************************************************************************************************************************************************************************

	#method returning the the object for modelling the system
	#def get_sys_model_obj(self):
		#return self._sys_model_obj
#*****************************************************************************************************************************************************************************************

	#method returning the name of he folder containing the data
	def get_name_data_folder(self):
		return self._name_data_folder

#*****************************************************************************************************************************************************************************************
	#method returning the name of the file containing the id of the node and the id of the entering links to the node
	def get_file_name_id_node_id_entering_links_to_node(self):
		return self._file_name_id_node_id_entering_links_to_node
	
	
#*****************************************************************************************************************************************************************************************
	#method returning the name of the file containing the id of the node and the id of the leaving links from the node
	def get_file_name_id_node_id_leaving_links_from_node(self):
		return self._file_name_id_node_id_leaving_links_from_node

#*****************************************************************************************************************************************************************************************
	#method returning the name of the file containing the id of the (head node) and the id of the corresponding entry links to  the network
	def get_file_name_id_node_id_entry_links_to_network(self):
		return self._file_name_id_node_id_entry_links_to_network

#*****************************************************************************************************************************************************************************************
	#method returning the name of the file containing the id of the (tail node) and the id of the corresponding exit links from the network
	def get_file_name_id_node_id_exit_links_from_network(self):
		return self._file_name_id_node_id_exit_links_from_network
	

#*****************************************************************************************************************************************************************************************
	#method returning the name of the file containing the id of the internal link and the id of the corresponding head and tail nodes of the link
	def get_file_name_id_internal_link_id_orig_dest_node(self):
		return self._file_name_id_internal_link_id_orig_dest_node
	
#*****************************************************************************************************************************************************************************************

	#method returning the name of the file defining the the max queue size, the saturation flow and the que type of each phase (queue, (l,m))
	def get_file_name_id_all_phases_max_queue_size_and_sat_flow_queue_type(self):
		return self._file_name_id_all_phases_max_queue_size_and_sat_flow_queue_type
#*****************************************************************************************************************************************************************************************		
	#method returning the name of the file containing the id of all links, their origin and destination node and their length
	def get_file_name_id_all_network_link_id_orig_dest_node_length_link_capacity_link_param_travel_duration(self):
		return self._file_name_id_all_network_link_id_orig_dest_node_length_link_capacity_link_param_travel_duration
#*****************************************************************************************************************************************************************************************
	#method returning the name of the module importing the file with the user data
	def get_module_name_import_sim_user_data(self):
		return self._module_name_import_sim_user_data
#*****************************************************************************************************************************************************************************************
	#methid returning  the name of the module importing the file with the files names modelling the network, 
	def get_module_name_import_file_names_model_network(self):
		return self._module_name_import_file_names_model_network
#*****************************************************************************************************************************************************************************************
	#method returning the name of the file containing the id of the  links and the id of the asociated entry links
	def get_file_name_id_link_id_sublinks(self):
		return self._file_name_id_link_id_sublinks
#*****************************************************************************************************************************************************************************************
	#method returning the name of the file containing the demand parameter of an entry link
	def get_file_name_demand_param_entry_link(self):
		return self._file_name_demand_param_entry_link
#*****************************************************************************************************************************************************************************************
	#method returning the name of the file with the id of all network links 
	#the id of the origin and destination nodes of the link and the length of the link
	def get_id_all_network_link_id_orig_dest_node_length_link_param_travel_duration(self):
		return self._id_all_network_link_id_orig_dest_node_length_link_param_travel_duration	
#*****************************************************************************************************************************************************************************************
	#method retunring the name of the file with the id of the minor phases and their associat prior phases
	def get_name_file_id_nd_id_minor_phase_id_prior_phase(self):
		return self._name_file_id_nd_id_minor_phase_id_prior_phase
#*****************************************************************************************************************************************************************************************
	#method modifying the the object for modelling the system
	#def set_sys_model_obj(self,n_v):
		#self._sys_model_obj=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the name of he folder containing the data
	def set_name_data_folder(self,n_v):
		self._name_data_folder=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the name of the file containing the id of the node and the id of the entering links to the node
	def set_file_name_id_node_id_entering_links_to_node(self,n_v):
		self._file_name_id_node_id_entering_links_to_node=n_v
	
	
#*****************************************************************************************************************************************************************************************
	#method modifying the name of the file containing the id of the node and the id of the leaving links from the node
	def set_file_name_id_node_id_leaving_links_from_node(self,n_v):
		self._file_name_id_node_id_leaving_links_from_node=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the name of the file containing the id of the (head node) and the id of the corresponding entry links to  the network
	def set_file_name_id_node_id_entry_links_to_network(self,n_v):
		self._file_name_id_node_id_entry_links_to_network=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the name of the file containing the id of the (tail node) and the id of the corresponding exit links from the network
	def set_file_name_id_node_id_exit_links_from_network(self,n_v):
		self._file_name_id_node_id_exit_links_from_network=n_v
	

#*****************************************************************************************************************************************************************************************
	#method modifying the name of the file containing the id of the internal link and the id of the corresponding head and tail nodes of the link
	def set_file_name_id_internal_link_id_orig_dest_node(self,n_v):
		self._file_name_id_internal_link_id_orig_dest_node=n_v
	
	
#*****************************************************************************************************************************************************************************************

	#method modifying the name of the file defining the the max queue size, the saturation flow and the que type of each phase (queue, (l,m))
	def set_file_name_id_all_phases_max_queue_size_and_sat_flow_queue_type(self,n_v):
		self._file_name_id_all_phases_max_queue_size_and_sat_flow_queue_type=n_v
#*****************************************************************************************************************************************************************************************	
	#method modifying the name of the file defining the the max queue size and saturation flow of each phase (queue, (l,m))
	def set_file_name_id_all_network_link_id_orig_dest_node_length_link_capacity_link_param_travel_duration(self,n_v):
		self._file_name_id_all_network_link_id_orig_dest_node_length_link_capacity_link_param_travel_duration=n_v
#*****************************************************************************************************************************************************************************************		
	#method modifying the name of the file containing the id of all links, their origin and destination node and their length
	def set_file_name_id_all_network_link_id_orig_dest_node_length_link_capacity_link_param_travel_duration(self):
		self._file_name_id_all_network_link_id_orig_dest_node_length_link_capacity_link_param_travel_duration=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the name of the file containing the id of the  links and the id of the asociated entry links
	def set_file_name_id_link_id_sublinks(self,n_v):
		self._file_name_id_link_id_sublinks=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the name of the file containing the demand parameter of an entry link
	def set_file_name_demand_param_entry_link(self,n_v):
		self._file_name_demand_param_entry_link=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the name of the file with the id of all network links 
	#the id of the origin and destination nodes of the link and the length of the link
	def set_id_all_network_link_id_orig_dest_node_length_link(self,n_v):
		self._id_all_network_link_id_orig_dest_node_length_link=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the name of the file with the id of the minor phases and their associat prior phases
	def set_name_file_id_nd_id_minor_phase_id_prior_phase(self,n_v):
		self._name_file_id_nd_id_minor_phase_id_prior_phase=n_v
#*****************************************************************************************************************************************************************************************
	#method creating the dictionary with the control param for each intersection, when ruled by the same control 
	#it returns a dictionary, key=type of control, value=dict, key=id node, value=di with param, key =nb id, value list param
	def fct_creat_dict_control_param_for_given_ctrl_type(self,v_type_control,v_nb_comment_lines_ft,v_nb_comment_lines_mp,\
	v_nb_comment_lines_ft_off,v_nb_comment_lines_fa,v_nb_comment_lines_fa_max_green):
	
		
		di_rep={}
		#if the type of the control is FT and  a new simulation is implemented or a  previous one is being continued 
		#using the same type of control
		if Cl_Control_Actuate.TYPE_CONTROL[v_type_control]==Cl_Control_Actuate.TYPE_CONTROL[1]:
			
			#we read the file with the parameters of the FT control
			va_di_file_par_ft_control=Global_Functions_Network.fct_reading_file_parameters_FT_control(name_file_to_read=\
			File_Sim_Name_Module_Files.val_name_folder_with_control_param_files+"/"+
			File_Sim_Name_Module_Files.val_name_file_values_ft_control,nb_comment_lines=v_nb_comment_lines_ft)
			
			di_rep[v_type_control]=va_di_file_par_ft_control
			
			return di_rep
			
			
		
		#if the type of the control is FT with offsets and  a new simulation is implemented or a  previous one is being continued 
		#using the same type of control
		elif Cl_Control_Actuate.TYPE_CONTROL[v_type_control]==Cl_Control_Actuate.TYPE_CONTROL[2]:
					
			#we read the file with the parameters of the FT offset control,
			#va_di_file_par_ft_offset_control=[les parm de FT offset, param FT sans offset]
			va_di_file_par_ft_offset_control=Global_Functions_Controls.fct_ft_ctrls_network(
			v_path_and_name_file_read=File_Sim_Name_Module_Files.\
			val_name_folder_with_control_param_files+"/"+
			File_Sim_Name_Module_Files.val_name_file_values_ft_offset_control,v_nb_comment_lines_ft_offs1=v_nb_comment_lines_ft_off)
			
			
			
			#di_rep[v_type_control]==[ list FT offset, list FT]
			di_rep[v_type_control]=va_di_file_par_ft_offset_control
			
			#print(di_rep[2][1])
			#print()
			#print(di_rep[2][0])
			#import sys
			#sys.exit()
			#di_rep=dict, key=id type control, value=[      ]
			return di_rep
						
			
			
		#if the type of the control is MP and  a new simulation is implemented or a  previous one is being continued 
		#using the same type of control
		elif Cl_Control_Actuate.TYPE_CONTROL[v_type_control]==Cl_Control_Actuate.TYPE_CONTROL[3]:
			#or \
			#v_type_control==Cl_Control_Actuate.TYPE_CONTROL[12]:
		
			va_di_file_par_mp_control_1=Global_Functions_Network.fct_reading_file_parameters_MP_control(\
			name_file_to_read=File_Sim_Name_Module_Files.val_name_folder_with_control_param_files+"/"+\
			File_Sim_Name_Module_Files.val_name_file_values_mp_control,\
			nb_comment_lines=v_nb_comment_lines_mp)
			
			
			#dict, key_id_node, value=dict, key=id phase, value=Qvalue
			
			val_di_ad_file_param_mp_control=Global_Functions_Network.fct_creat_dict_Qvalues_for_MP_ctrl(\
			val_name_file_to_read=File_Sim_Name_Module_Files.val_name_folder_with_control_param_files+"/"+\
			File_Sim_Name_Module_Files.val_name_addit_file_mp_control,\
			val_number_lines_to_read=v_nb_comment_lines_mp)
			
			va_di_file_par_mp_control={}
			
			#for each node with MP cotnrol
			for i in va_di_file_par_mp_control_1:
				va_di_file_par_mp_control[i]=[va_di_file_par_mp_control_1[i],val_di_ad_file_param_mp_control]
					
									
			
			di_rep[v_type_control]=va_di_file_par_mp_control
			
			
			return di_rep
			
			
			
		#if  we contirnue a previous sim  employing FT and the new sim will employe MP
		#we create both parameter sets for FT and MP
		#elif v_type_control==Cl_Control_Actuate.TYPE_CONTROL[(1,3)]:
			
			#va_di_file_par_ft_control=Global_Functions_Network.fct_reading_file_parameters_FT_control(name_file_to_read=\
			#File_Sim_Name_Module_Files.val_name_folder_with_control_param_files+"/"+
			#File_Sim_Name_Module_Files.val_name_file_values_ft_control,nb_comment_lines=v_nb_comment_lines_ft)
		
			#va_di_file_par_mp_control=Global_Functions_Network.fct_reading_file_parameters_MP_control(\
			#name_file_to_read=File_Sim_Name_Module_Files.val_name_folder_with_control_param_files+"/"+\
			#File_Sim_Name_Module_Files.val_name_file_values_mp_control,\
			#nb_comment_lines=v_nb_comment_lines_mp)
			
			#di_rep[v_type_control]=[va_di_file_par_ft_control,va_di_file_par_mp_control]
			
			#return di_rep
			
			
			
		#if we start a new sim using MIXED control
		elif Cl_Control_Actuate.TYPE_CONTROL[v_type_control]==Cl_Control_Actuate.TYPE_CONTROL[4]:
		
			print("IL FAUT CREER FICHIERS CTRLS PARAM")
			import sys
			sys.exit()
		
			va_di_file_par_ft_for_mixed_control=Global_Functions_Network.fct_reading_file_parameters_FT_control(name_file_to_read=\
			File_Sim_Name_Module_Files.val_name_folder_with_control_param_files+"/"+
			File_Sim_Name_Module_Files.val_name_file_values_ft_param_for_mixed_control,nb_comment_lines=v_nb_comment_lines_ft)
		
			va_di_file_par_mp_for_mixed_control=Global_Functions_Network.fct_reading_file_parameters_MP_control(\
			name_file_to_read=File_Sim_Name_Module_Files.val_name_folder_with_control_param_files+"/"+\
			File_Sim_Name_Module_Files.val_name_file_values_mp_param_for_mixed_control,\
			nb_comment_lines=v_nb_comment_lines_mp)
			
			di_rep[v_type_control]=[va_di_file_par_ft_for_mixed_control,va_di_file_par_mp_for_mixed_control]
			
			return di_rep
			
			
			
		#if we do a Presure Stage Actuation Control
		#elif v_type_control==Cl_Control_Actuate.TYPE_CONTROL[8]:
		
			#va_di_file_par_psd=Global_Functions_Network.fct_reading_file_psd_control(name_file_to_read=\
			#File_Sim_Name_Module_Files.val_name_folder_with_control_param_files+"/"+\
			#File_Sim_Name_Module_Files.val_name_File_Pres_Stage_Duration_Control_Alg_Param,nb_comment_lines=v_nb_comment_lines_psd)
			
			#di_rep[v_type_control]=va_di_file_par_psd
			
			#return di_rep
			
			
			
		#if the type of the control is MP without output queue  and  a new simulation is implemented or a  previous one is being continued 
		#using the same type of control
		elif Cl_Control_Actuate.TYPE_CONTROL[v_type_control]==Cl_Control_Actuate.TYPE_CONTROL[9]:
		
			va_di_file_par_mp_control_no_output_que=Global_Functions_Network.fct_reading_file_parameters_MP_control(\
			name_file_to_read=File_Sim_Name_Module_Files.val_name_folder_with_control_param_files+"/"+\
			File_Sim_Name_Module_Files.val_name_file_values_mp_control_no_output_queues,\
			nb_comment_lines=v_nb_comment_lines_mp)
			
			di_rep[v_type_control]= va_di_file_par_mp_control_no_output_que
			
			
			
			#indice_choix_duree=-1
			return di_rep
			
			
		#if the type of the control is fully actuated no red clearance
		elif Cl_Control_Actuate.TYPE_CONTROL[v_type_control]==Cl_Control_Actuate.TYPE_CONTROL[10]:	 
		
			va_di_file_fa_control=Global_Functions_Network.fct_reading_file_fa_control_no_rec_clear(\
			name_file_to_read=File_Sim_Name_Module_Files.val_name_folder_with_control_param_files+"/"+
			File_Sim_Name_Module_Files.val_name_File_fa_no_red_clear_control,nb_comment_lines=v_nb_comment_lines_fa)
			
			di_rep[v_type_control]=va_di_file_fa_control
			
			return di_rep
			
			
			
		#if the type of the control is fully actuated wiht max green 
		elif Cl_Control_Actuate.TYPE_CONTROL[v_type_control]==Cl_Control_Actuate.TYPE_CONTROL[11]:	 
		
			va_di_file_fa_max_green_control=Global_Functions_Network.fct_reading_file_fa_control_max_green(\
			name_file_to_read=File_Sim_Name_Module_Files.val_name_folder_with_control_param_files+"/"+
			File_Sim_Name_Module_Files.val_name_File_fa_max_green_control,nb_comment_lines=v_nb_comment_lines_fa)
			
			di_rep[v_type_control]=va_di_file_fa_max_green_control
			return di_rep
			
		#if the type of the control is fully actuated with red clearance
		elif Cl_Control_Actuate.TYPE_CONTROL[v_type_control]==Cl_Control_Actuate.TYPE_CONTROL[12]:	 
		
			va_di_file_fa_control=Global_Functions_Network.fct_reading_file_fa_control_with_red_clear(\
			name_file_to_read=File_Sim_Name_Module_Files.val_name_folder_with_control_param_files+"/"+
			File_Sim_Name_Module_Files.val_name_File_fa_with_red_clear_control,nb_comment_lines=v_nb_comment_lines_fa)
			
			di_rep[v_type_control]=va_di_file_fa_control
			
			return di_rep	
			
		#if the type of control is MP Practical
		elif Cl_Control_Actuate.TYPE_CONTROL[v_type_control]==Cl_Control_Actuate.TYPE_CONTROL[13]:
		
			va_di_file_par_mp_practical_control_1=Global_Functions_Network.fct_reading_file_MP_Pract_control(\
			name_file_to_read=File_Sim_Name_Module_Files.val_name_folder_with_control_param_files+"/"+\
			File_Sim_Name_Module_Files.val_name_file_values_mp_practical_control,\
			nb_comment_lines=v_nb_comment_lines_mp)
			
			
			val_di_ad_file_param_mp_pract_control=Global_Functions_Network.fct_creat_dict_Qvalues_for_MP_ctrl(\
			val_name_file_to_read=File_Sim_Name_Module_Files.val_name_folder_with_control_param_files+"/"+\
			File_Sim_Name_Module_Files.val_name_addit_file_mp_pract_control,\
			val_number_lines_to_read=v_nb_comment_lines_mp)
			
			va_di_file_par_mp_practical_control={}
			
			#for each node with MP cotnrol
			for i in va_di_file_par_mp_practical_control_1:
				va_di_file_par_mp_practical_control[i]=[va_di_file_par_mp_practical_control_1[i],val_di_ad_file_param_mp_pract_control]
			
			di_rep[v_type_control]=va_di_file_par_mp_practical_control
			
			return di_rep
			
		#if the type of control is MP no red clear
		elif Cl_Control_Actuate.TYPE_CONTROL[v_type_control]==Cl_Control_Actuate.TYPE_CONTROL[14]:
			va_di_param_mp_without_rc=Global_Functions_Network.fct_reading_file_MP_without_rc_control(\
			name_file_to_read=File_Sim_Name_Module_Files.val_name_folder_with_control_param_files+"/"+\
			File_Sim_Name_Module_Files.val_name_file_values_mp_without_rc_control,\
			nb_comment_lines=v_nb_comment_lines_mp)
			
			#dict, key_id_node, value=dict, key=id phase, value=Qvalue
			val_di_ad_file_param_mp_without_rc_control=Global_Functions_Network.fct_creat_dict_Qvalues_for_MP_ctrl(\
			val_name_file_to_read=File_Sim_Name_Module_Files.val_name_folder_with_control_param_files+"/"+\
			File_Sim_Name_Module_Files.val_name_addit_file_mp_without_rc_control,\
			val_number_lines_to_read=v_nb_comment_lines_mp)
			
			
			
			va_di_file_par_mp_control={}
			
			#for each node with MP cotnrol
			for i in va_di_param_mp_without_rc:
				
				va_di_file_par_mp_control[i]=[va_di_param_mp_without_rc[i],val_di_ad_file_param_mp_without_rc_control]
				
			di_rep[v_type_control]=va_di_file_par_mp_control
			
			return di_rep
			
		#if the type of control is MP-Pract no red clear
		elif Cl_Control_Actuate.TYPE_CONTROL[v_type_control]==Cl_Control_Actuate.TYPE_CONTROL[15]:
			va_di_param_mp_pract_without_rc_1=Global_Functions_Network.fct_reading_file_MP_pract_without_rc_control(\
			name_file_to_read=File_Sim_Name_Module_Files.val_name_folder_with_control_param_files+"/"+\
			File_Sim_Name_Module_Files.val_name_file_values_mp_pract_without_rc_control,\
			nb_comment_lines=v_nb_comment_lines_mp)
			
			
			val_di_ad_file_param_mp_pract_without_rc_control=Global_Functions_Network.fct_creat_dict_Qvalues_for_MP_ctrl(\
			val_name_file_to_read=File_Sim_Name_Module_Files.val_name_folder_with_control_param_files+"/"+\
			File_Sim_Name_Module_Files.val_name_addit_file_mp_pract_without_rc_control,\
			val_number_lines_to_read=v_nb_comment_lines_mp)
			
			va_di_file_par_mp_practical_no_red_clear_control={}
			
			#for each node with MP-Pract no red clear cotnrol
			for i in va_di_param_mp_pract_without_rc_1:
				va_di_file_par_mp_practical_no_red_clear_control[i]=[va_di_param_mp_pract_without_rc_1[i],val_di_ad_file_param_mp_pract_without_rc_control]
			
			di_rep[v_type_control]=va_di_file_par_mp_practical_no_red_clear_control
			
			return di_rep
			
		

#*****************************************************************************************************************************************************************************************
	#method creating a dictionary, key=control type, value= dict, key=id node, value=li ctl param
	def fct_creat_dict_ctrl_param_per_inters(self,li_types_ctrl,va_nb_comment_lines_ft,va_nb_comment_lines_mp,\
	va_nb_comment_lines_ft_off,va_nb_comment_lines_fa,va_nb_comment_lines_fa_max_green):
	
		#print("di_key_id_node_value_type_nd",di_key_id_node_value_type_nd)		
		#list containing the different types of controls
		#li_types_ctrl=[]
		#di_key_id_node_value_type_nd=dict, key=id node, value=[type ctrl, string control categ with/out sens]
		#for i in di_key_id_node_value_type_nd:
			#if di_key_id_node_value_type_nd[i][0] not in li_types_ctrl:
				#li_types_ctrl.append(di_key_id_node_value_type_nd[i][0])
		
		
		di_rep={}
		#for each type of control,	we create a dictonary 
		for i in li_types_ctrl:
			#print("i=",i)
			di_rep_1=self.fct_creat_dict_control_param_for_given_ctrl_type(\
			v_type_control=i,\
			v_nb_comment_lines_ft=va_nb_comment_lines_ft,\
			v_nb_comment_lines_mp=va_nb_comment_lines_mp,\
			v_nb_comment_lines_ft_off=va_nb_comment_lines_ft_off,\
			v_nb_comment_lines_fa=va_nb_comment_lines_fa,\
			v_nb_comment_lines_fa_max_green=va_nb_comment_lines_fa_max_green)
			
			di_rep.update(di_rep_1)
			
			
		return di_rep
#*****************************************************************************************************************************************************************************************
	#method creating an control actuate_object for a particular intersection acoording to the employed control 
	#if the cotnrol is FT with offsets, v_li_param_inters_ctrl=[li_param_offset,li_parm ft]
	#if the control is mixed, IT DOES NOT WORK, MODEL PARAM FILE BEFORE
	def fct_creat_inters_control_actuat_obj(self,v_type_control,v_control_categ,v_li_param_inters_ctrl):
	#,val_turn_ratios_estimated):
	
		#print("v_type_control",v_type_control)
		
		#if the type of the control is FT and  a new simulation is implemented or a  previous one is being continued 
		#using the same type of control
		if Cl_Control_Actuate.TYPE_CONTROL[v_type_control]==Cl_Control_Actuate.TYPE_CONTROL[1]:
		
	
		
			ctrl_act_obj=Cl_Control_Actuate.Control_Actuate(val_li_param_ft_ctrl=v_li_param_inters_ctrl,\
			val_type_employed_ctrl=v_type_control,val_type_ctrl_categ=v_control_categ)
			#,\
			#val_turn_ratios_estim=val_turn_ratios_estimated)
			
			return ctrl_act_obj
		
		#if the type of the control is FT with offsets and  a new simulation is implemented or a  previous one is being continued 
		#using the same type of control
		elif Cl_Control_Actuate.TYPE_CONTROL[v_type_control]==Cl_Control_Actuate.TYPE_CONTROL[2]:
		
			#print()
			#print("v_li_param_inters_ctrl",v_li_param_inters_ctrl[0],v_li_param_inters_ctrl[1])
			#print()
			#print("ici FTO",v_li_param_inters_ctrl[0])
			#print()
			#print("ici1",v_li_param_inters_ctrl[1])
			#import sys
			#sys.exit()
			
			
			ctrl_act_obj=Cl_Control_Actuate.Control_Actuate(val_li_param_ft_ctrl=v_li_param_inters_ctrl[1],\
			val_type_employed_ctrl=v_type_control,val_li_param_ft_offset_ctrl=v_li_param_inters_ctrl[0],val_type_ctrl_categ=v_control_categ)
			
			return ctrl_act_obj
			
		#if the type of the control is MP and  a new simulation is implemented or a  previous one is being continued 
		#using the same type of control
		elif Cl_Control_Actuate.TYPE_CONTROL[v_type_control]==Cl_Control_Actuate.TYPE_CONTROL[3]:
			#or \
			#v_type_control==Cl_Control_Actuate.TYPE_CONTROL[12]:
			
			#indice_choix_duree=-1
			ctrl_act_obj=Cl_Control_Actuate.Control_Actuate(val_li_param_mp_ctrl=v_li_param_inters_ctrl[0],\
			val_di_addition_param_mp_ctrl=v_li_param_inters_ctrl[1],\
			val_type_employed_ctrl=v_type_control,val_type_ctrl_categ=v_control_categ)
			#,\
			#val_turn_ratios_estim=val_turn_ratios_estimated)
			
			return ctrl_act_obj
			
		#if we start a new sim using MIXED control
		elif Cl_Control_Actuate.TYPE_CONTROL[v_type_control]==Cl_Control_Actuate.TYPE_CONTROL[4]:
			
			print("A FAIRE LES FICH PARAM")
			import sys
			sys.exit()
		
			ctrl_act_obj=Cl_Control_Actuate.Control_Actuate(val_di_param_ft_for_mixed_ctrl=v_li_param_inters_ctrl[0],\
			val_di_param_mp_for_mixed_ctrl=v_li_param_inters_ctrl[1])
			
			return ctrl_act_obj
			
		#if we do a Presure Stage Actuation Control
		#elif v_type_control==Cl_Control_Actuate.TYPE_CONTROL[8]:
		
			#va_di_file_par_psd=Global_Functions_Network.fct_reading_file_psd_control(name_file_to_read=\
			#File_Sim_Name_Module_Files.val_name_folder_with_control_param_files+"/"+\
			#File_Sim_Name_Module_Files.val_name_File_Pres_Stage_Duration_Control_Alg_Param,nb_comment_lines=v_nb_comment_lines_psd)
			
			
			#ctrl_act_obj=Cl_Control_Actuate.Control_Actuate(val_di_param_psd_ctrl=va_di_file_par_psd)
			
		#if the type of the control is MP without output queue  and  a new simulation is implemented or a  previous one is being continued 
		#using the same type of control
		elif Cl_Control_Actuate.TYPE_CONTROL[v_type_control]==Cl_Control_Actuate.TYPE_CONTROL[9]:
		
			#indice_choix_duree=-1
			ctrl_act_obj=Cl_Control_Actuate.Control_Actuate(val_di_param_control_MP_no_output_que=v_li_param_inters_ctrl,\
			val_type_employed_ctrl=v_type_control,val_type_ctrl_categ=v_control_categ)
			
			return ctrl_act_obj
			
		#if the type of the control is fully actuated withour red clear
		elif Cl_Control_Actuate.TYPE_CONTROL[v_type_control]==Cl_Control_Actuate.TYPE_CONTROL[10]:	 
		
			ctrl_act_obj=Cl_Control_Actuate.Control_Actuate(val_li_param_control_FA_ctrl=v_li_param_inters_ctrl,\
			val_type_employed_ctrl=v_type_control,val_type_ctrl_categ=v_control_categ)
			#,\
			#val_turn_ratios_estim=val_turn_ratios_estimated)
				
			return ctrl_act_obj
			
		#if the type of the control is fully actuated wiht max green 
		elif Cl_Control_Actuate.TYPE_CONTROL[v_type_control]==Cl_Control_Actuate.TYPE_CONTROL[11]:	 
			
			ctrl_act_obj=Cl_Control_Actuate.Control_Actuate(val_li_param_control_FA_Max_Green_ctrl=v_li_param_inters_ctrl,\
			val_type_employed_ctrl=v_type_control,val_type_ctrl_categ=v_control_categ)
			#,\
			#val_turn_ratios_estim=val_turn_ratios_estimated)
			
			return ctrl_act_obj
			
		#if the type of the control is fully actuated with red clear
		elif Cl_Control_Actuate.TYPE_CONTROL[v_type_control]==Cl_Control_Actuate.TYPE_CONTROL[12]:	 
			
			ctrl_act_obj=Cl_Control_Actuate.Control_Actuate(val_li_param_control_FA_with_red_clear_ctrl=v_li_param_inters_ctrl,\
			val_type_employed_ctrl=v_type_control,val_type_ctrl_categ=v_control_categ)
			#,\
			#val_turn_ratios_estim=val_turn_ratios_estimated)
			
			return ctrl_act_obj
			
		#if the type of control is MP Practical
		elif Cl_Control_Actuate.TYPE_CONTROL[v_type_control]==Cl_Control_Actuate.TYPE_CONTROL[13]:
		
			#indice_choix_duree=-1
			ctrl_act_obj=Cl_Control_Actuate.Control_Actuate(val_li_param_control_MP_Practical_ctrl=v_li_param_inters_ctrl[0],\
			val_type_employed_ctrl=v_type_control,val_type_ctrl_categ=v_control_categ,\
			val_di_addition_param_mp_pract_ctrl=v_li_param_inters_ctrl[1])
			#,\
			#val_turn_ratios_estim=val_turn_ratios_estimated)
			
			return ctrl_act_obj
			
		#if the type of the cotnrol is MP without red clearance
		elif Cl_Control_Actuate.TYPE_CONTROL[v_type_control]==Cl_Control_Actuate.TYPE_CONTROL[14]:
		
			
			
			ctrl_act_obj=Cl_Control_Actuate.Control_Actuate(val_li_param_control_MP_without_red_clear=v_li_param_inters_ctrl[0],\
			val_type_employed_ctrl=v_type_control,val_type_ctrl_categ=v_control_categ,\
			val_di_addition_param_mp_without_red_clear_ctrl=v_li_param_inters_ctrl[1])
			
			return ctrl_act_obj
			
		#if the type of the control is MP Pract without red clear
		elif Cl_Control_Actuate.TYPE_CONTROL[v_type_control]==Cl_Control_Actuate.TYPE_CONTROL[15]:
		
			ctrl_act_obj=Cl_Control_Actuate.Control_Actuate(val_li_param_control_MP_Pract_without_red_clear=v_li_param_inters_ctrl[0],\
			val_type_employed_ctrl=v_type_control,val_type_ctrl_categ=v_control_categ,\
			val_di_addition_param_mp_pract_without_red_clear_ctrl=v_li_param_inters_ctrl[1])
			
			return ctrl_act_obj
			


#*****************************************************************************************************************************************************************************************
	#method creating the related  dict to the cum values of the rout prob and updating the dict of intersections
	#val_di_cum_rp=dict, keu=id link, value=[...,[cum value rp, id associated link],....]
	def fct_creat_dict_cum_rp(self,val_di_cum_rp,val_netw):
	
		#print(val_di_cum_rp)
		#import sys
		#sys.exit()
	
		#dict with the current cum values of rp for each node
		#key=node id, value= dict, key=id input link, value=[..,[ [cum value at ith stage, id dest lk _1],...,[cum value at ith stage, id dest lk _n]] ,....]
		dict_cur_cum_rp_per_node={}
			
					
		
		dict_key_id_entry_intern_lk_value_li_cum_rout_prob_and_id_dest_lk={}
		
		#val_di_cum_r=dict, key =id entry internal link, value=[...,[cum rout prob, id dest link],...]
		
		#for each entry - internal link
		for i in val_di_cum_rp:
			
			#if the head node is not in the dict	
			if val_netw.get_di_entry_internal_links()[i].get_id_head_intersection_node() not in \
			dict_key_id_entry_intern_lk_value_li_cum_rout_prob_and_id_dest_lk:
				
				dict_key_id_entry_intern_lk_value_li_cum_rout_prob_and_id_dest_lk[\
				val_netw.get_di_entry_internal_links()[i].get_id_head_intersection_node()]={}
					
				di={}
				di[i]=val_di_cum_rp[i]
					
			
				dict_key_id_entry_intern_lk_value_li_cum_rout_prob_and_id_dest_lk[\
				val_netw.get_di_entry_internal_links()[i].get_id_head_intersection_node()].update(di)
					
			#if the head node of the link is in the dict
			else:
				di={}
				di[i]=\
				val_di_cum_rp[i]
										
				dict_key_id_entry_intern_lk_value_li_cum_rout_prob_and_id_dest_lk[\
				val_netw.get_di_entry_internal_links()[i].get_id_head_intersection_node()].update(di)
					
			#we associate the dict with the current cum rout prob to each intersection
		
		#print("dict_key_id_entry_intern_lk_value_li_cum_rout_prob_and_id_dest_lk",dict_key_id_entry_intern_lk_value_li_cum_rout_prob_and_id_dest_lk)
		#import sys
		#sys.exit()
		#for t in dict_key_id_entry_intern_lk_value_li_cum_rout_prob_and_id_dest_lk:
		
			#val_netw.get_di_intersections()[t].set_current_di_cum_rout_prob(\
			#dict_key_id_entry_intern_lk_value_li_cum_rout_prob_and_id_dest_lk[t])
			
		return dict_key_id_entry_intern_lk_value_li_cum_rout_prob_and_id_dest_lk
			
#*****************************************************************************************************************************************************************************************
	#fucntion completing the param of MP Qweight or not control
	def fct_comp_param_MP_QWeight(self,val_di_ctrl_param_inters,val_dict_id_node_type_and_control_categ,\
	val_dict_id_node_id_entering_links_to_node,val_dict_id_link_val_link,val_dict_id_node_id_leaving_links_from_node,val_li_param_inters_ctrl,\
	id_inters):
		
		
		#if a Qweighted version will be considered
		if val_di_ctrl_param_inters[val_dict_id_node_type_and_control_categ[id_inters][0]][id_inters][1]!={}:
		
	 
			va_di_addition_param_mp_ctrl_1=val_di_ctrl_param_inters[val_dict_id_node_type_and_control_categ[id_inters][0]][id_inters][1]
		
			va_di_addition_param_mp_ctrl={}
		
			#for each input link tp node
			for lk in val_dict_id_node_id_entering_links_to_node[id_inters]:
				#for each que
				for q in val_dict_id_link_val_link[lk].get_set_veh_queue().get_di_obj_veh_queue_at_link():
			
					va_di_addition_param_mp_ctrl[q]=va_di_addition_param_mp_ctrl_1[q]
				
			#if the link is not an exit one
			for lk1 in val_dict_id_node_id_leaving_links_from_node[id_inters]:
				if val_dict_id_link_val_link[lk1].get_type_network_link()!=Cl_Network_Link.TYPE_NETWORK_LINK["exit"]:
			
					for q1 in val_dict_id_link_val_link[lk1].get_set_veh_queue().get_di_obj_veh_queue_at_link():
				
						va_di_addition_param_mp_ctrl[q1]=va_di_addition_param_mp_ctrl_1[q1]
			
	
		#if a not Qweighted version will be considered
		else:
			va_di_addition_param_mp_ctrl={}
		
			#for each input link tp node
			for lk in val_dict_id_node_id_entering_links_to_node[id_inters]:
				#for each que
				for q in val_dict_id_link_val_link[lk].get_set_veh_queue().get_di_obj_veh_queue_at_link():
					va_di_addition_param_mp_ctrl[q]=1
					#if the link is not an exit one
					for lk1 in val_dict_id_node_id_leaving_links_from_node[id_inters]:
						if val_dict_id_link_val_link[lk1].get_type_network_link()!=Cl_Network_Link.TYPE_NETWORK_LINK["exit"]:

							for q1 in val_dict_id_link_val_link[lk1].get_set_veh_queue().get_di_obj_veh_queue_at_link():
								va_di_addition_param_mp_ctrl[q1]=1
		
	
		val_li_param_inters_ctrl[1]=va_di_addition_param_mp_ctrl
			
		
		
#*****************************************************************************************************************************************************************************************
	#function returning a dictionary of intersections, 
	#key= the id of the intersection node
	#value= the intersection object
	#dict_id_node_li_si_stages= dictionary <ith the staged of each signalised intersection
	#dict_id_node_li_nsi_stages=dictionary  with the stages of  each non signalised intersection	
	#val_exist_od_mat=1 if we have ods, 0 otherwise double check since if it values 0, dict dict_current_cum_mod will be empty
	def funct_creating_dict_intersections(self,val_exist_od_mat,dict_id_node_id_entering_links_to_node={},dict_id_node_id_leaving_links_from_node={},\
	val_li_types_ctrl=[],di_id_nd_type_and_ctrl_categ={},di_id_nd_val_dic_rp={},di_id_nd_val_di_cum_rp={},dict_current_cum_mod={},\
	dict_id_node_li_si_stages={},dict_id_node_li_nsi_stages={},di_id_sign_inters_nd_value_one={},di_id_non_sign_inters_nd_value_zero={},\
	v_nb_comment_lines_ft=-1,v_nb_comment_lines_mp=-1,\
    v_nb_comment_lines_ft_off=-1,v_nb_comment_lines_fa=-1,v_nb_comment_lines_fa_max_green=-1,\
	dict_id_nd_param_turn_ratio_estim={},val_dict_estim_rp={},val_di_id_link_val_link={}):
	
		di_inters={}
		
		#creat of the dict, key=id node, value=[type ctrl ctrl category]
		#di_id_nd_type_and_ctrl_categ=self.fct_creat_di_key_id_node_value_type_and_ctrl_category()
		
		
		
		#creation of the dict with the control param for each intersection
		#dict, key=ctrl type, value=either dict,
		#key=id node, value=li parameters realted ctrl
		#or value=[dict key id node, value li parma contrl, di ikey d node value list additional param cotnrol], case when MP
		di_ctrl_param_inters=self.fct_creat_dict_ctrl_param_per_inters(\
		li_types_ctrl=val_li_types_ctrl,\
		va_nb_comment_lines_ft=v_nb_comment_lines_ft,\
		va_nb_comment_lines_mp=v_nb_comment_lines_mp,\
		va_nb_comment_lines_ft_off=v_nb_comment_lines_ft_off,\
		va_nb_comment_lines_fa=v_nb_comment_lines_fa,\
		va_nb_comment_lines_fa_max_green=v_nb_comment_lines_fa_max_green)
		#print()
		
		#print()
		#print("di_id_nd_type_and_ctrl_categ",di_id_nd_type_and_ctrl_categ)
		#import sys
		#sys.exit()
	
		
		
		#print("di_id_sign_inters_nd_value_one",di_id_sign_inters_nd_value_one.keys())	
		#print()
		#print(len(di_ctrl_param_inters[di_id_nd_type_and_ctrl_categ[1][0]]))
		#print()
		#print("FT o",di_ctrl_param_inters[di_id_nd_type_and_ctrl_categ[1][0]][0])
		#print()
		#print("FT",di_ctrl_param_inters[di_id_nd_type_and_ctrl_categ[1][0]][1])
			
		# signalised intersections
		for k in di_id_sign_inters_nd_value_one:
		
			#print("di_ctrl_param_inters",di_ctrl_param_inters.keys())
			#print()
			#print("node ici",k,"di_id_nd_type_and_ctrl_categ[k][0]",di_id_nd_type_and_ctrl_categ[k][0])
			#print()
			#print("di_ctrl_param_inters[di_id_nd_type_and_ctrl_categ[k][0]]",di_ctrl_param_inters[di_id_nd_type_and_ctrl_categ[k][0]][0][k])
			#import sys
			#sys.exit()
			
			
			#when MP Pract, len(di_ctrl_param_inters[di_id_nd_type_and_ctrl_categ[k][0]])==2
			#if len(di_ctrl_param_inters[di_id_nd_type_and_ctrl_categ[k][0]])==2:
				#va_li_param_inters_ctrl=di_ctrl_param_inters[di_id_nd_type_and_ctrl_categ[k][0]][0][k]
			#else:
				#va_li_param_inters_ctrl=di_ctrl_param_inters[di_id_nd_type_and_ctrl_categ[k][0]][k]

			
			#va_li_param_inters_ctrl=di_ctrl_param_inters[di_id_nd_type_and_ctrl_categ[k][0]][k]
			
			#print()
			#print("va_li_param_inters_ctrl",va_li_param_inters_ctrl)
			#print()
			#print(len(di_ctrl_param_inters[di_id_nd_type_and_ctrl_categ[k][0]]))
			#import sys
			#sys.exit()
			
			
			#if a weighted MP will be considered
			if Cl_Control_Actuate.TYPE_CONTROL[di_id_nd_type_and_ctrl_categ[k][0]]==Cl_Control_Actuate.TYPE_CONTROL[3]:
			
				va_li_param_inters_ctrl=di_ctrl_param_inters[di_id_nd_type_and_ctrl_categ[k][0]][k]
			
				#print("avant",va_li_param_inters_ctrl)
				#print()
				#import sys
				#sys.exit()
				self.fct_comp_param_MP_QWeight(\
				val_di_ctrl_param_inters=di_ctrl_param_inters,\
				val_dict_id_node_type_and_control_categ=di_id_nd_type_and_ctrl_categ,\
				val_dict_id_node_id_entering_links_to_node=dict_id_node_id_entering_links_to_node,\
				val_dict_id_link_val_link=val_di_id_link_val_link,\
				val_dict_id_node_id_leaving_links_from_node=dict_id_node_id_leaving_links_from_node,\
				val_li_param_inters_ctrl=va_li_param_inters_ctrl,id_inters=k)
				#print(va_li_param_inters_ctrl)
				#import sys
				#sys.exit()
			#if a weighted MP withour red clear will be considered
			elif Cl_Control_Actuate.TYPE_CONTROL[di_id_nd_type_and_ctrl_categ[k][0]]==Cl_Control_Actuate.TYPE_CONTROL[14]:
				va_li_param_inters_ctrl=di_ctrl_param_inters[di_id_nd_type_and_ctrl_categ[k][0]][k]
				
				#print("avant",va_li_param_inters_ctrl)
				#print()
				self.fct_comp_param_MP_QWeight(\
				val_di_ctrl_param_inters=di_ctrl_param_inters,\
				val_dict_id_node_type_and_control_categ=di_id_nd_type_and_ctrl_categ,\
				val_dict_id_node_id_entering_links_to_node=dict_id_node_id_entering_links_to_node,\
				val_dict_id_link_val_link=val_di_id_link_val_link,\
				val_dict_id_node_id_leaving_links_from_node=dict_id_node_id_leaving_links_from_node,\
				val_li_param_inters_ctrl=va_li_param_inters_ctrl,id_inters=k)
				
				#print("apres",va_li_param_inters_ctrl)
				#import sys
				#sys.exit()
				
			#if a weighted MP-Pract will be considered
			elif Cl_Control_Actuate.TYPE_CONTROL[di_id_nd_type_and_ctrl_categ[k][0]]==Cl_Control_Actuate.TYPE_CONTROL[13]:
			
				va_li_param_inters_ctrl=di_ctrl_param_inters[di_id_nd_type_and_ctrl_categ[k][0]][k]
			
			
				self.fct_comp_param_MP_QWeight(\
				val_di_ctrl_param_inters=di_ctrl_param_inters,\
				val_dict_id_node_type_and_control_categ=di_id_nd_type_and_ctrl_categ,\
				val_dict_id_node_id_entering_links_to_node=dict_id_node_id_entering_links_to_node,\
				val_dict_id_link_val_link=val_di_id_link_val_link,\
				val_dict_id_node_id_leaving_links_from_node=dict_id_node_id_leaving_links_from_node,\
				val_li_param_inters_ctrl=va_li_param_inters_ctrl,id_inters=k)
				
			#if a weighted MP-Pract without red clear will be considered
			elif Cl_Control_Actuate.TYPE_CONTROL[di_id_nd_type_and_ctrl_categ[k][0]]==Cl_Control_Actuate.TYPE_CONTROL[15]:
			
				va_li_param_inters_ctrl=di_ctrl_param_inters[di_id_nd_type_and_ctrl_categ[k][0]][k]
								
				self.fct_comp_param_MP_QWeight(\
				val_di_ctrl_param_inters=di_ctrl_param_inters,\
				val_dict_id_node_type_and_control_categ=di_id_nd_type_and_ctrl_categ,\
				val_dict_id_node_id_entering_links_to_node=dict_id_node_id_entering_links_to_node,\
				val_dict_id_link_val_link=val_di_id_link_val_link,\
				val_dict_id_node_id_leaving_links_from_node=dict_id_node_id_leaving_links_from_node,\
				val_li_param_inters_ctrl=va_li_param_inters_ctrl,id_inters=k)

			#if a FT control will be  considered 
			elif Cl_Control_Actuate.TYPE_CONTROL[di_id_nd_type_and_ctrl_categ[k][0]]==Cl_Control_Actuate.TYPE_CONTROL[1]:
				va_li_param_inters_ctrl=di_ctrl_param_inters[di_id_nd_type_and_ctrl_categ[k][0]][k]
				
			#if a FT with offsets control 
			elif Cl_Control_Actuate.TYPE_CONTROL[di_id_nd_type_and_ctrl_categ[k][0]]==Cl_Control_Actuate.TYPE_CONTROL[2]:
			
				#va_li_param_inters_ctrl_1=list [dict parm FT ofs,dict parm FT ]
				va_li_param_inters_ctrl_1=di_ctrl_param_inters[di_id_nd_type_and_ctrl_categ[k][0]]
				va_li_param_inters_ctrl=[va_li_param_inters_ctrl_1[0][k],va_li_param_inters_ctrl_1[1][k]]
				#print(va_li_param_inters_ctrl[1])
				
				
				

			
				#print("here",di_ctrl_param_inters[di_id_nd_type_and_ctrl_categ[k][0]][k][1])
				#if di_ctrl_param_inters[di_id_nd_type_and_ctrl_categ[k][0]][k][1]!={}:
				
					#va_di_addition_param_mp_ctrl_1=di_ctrl_param_inters[di_id_nd_type_and_ctrl_categ[k][0]][k][1]
					
					#va_di_addition_param_mp_ctrl={}
					
				
					
					#for each input link tp node
					#for lk in dict_id_node_id_entering_links_to_node[k]:
						#for each que
						#for q in val_di_id_link_val_link[lk].get_set_veh_queue().get_di_obj_veh_queue_at_link():
							
							#va_di_addition_param_mp_ctrl[q]=va_di_addition_param_mp_ctrl_1[q]
							
					#if the link is not an exit one
					
					#for lk1 in dict_id_node_id_leaving_links_from_node[k]:
					
						#if val_di_id_link_val_link[lk1].get_type_network_link()!=Cl_Network_Link.TYPE_NETWORK_LINK["exit"]:

							#for q1 in val_di_id_link_val_link[lk1].get_set_veh_queue().get_di_obj_veh_queue_at_link():
								
								#va_di_addition_param_mp_ctrl[q1]=va_di_addition_param_mp_ctrl_1[q1]
			
				#if not a weighted MP will be considered
				#else:
					#va_di_addition_param_mp_ctrl={}
									
					##for each input link tp node
					#for lk in dict_id_node_id_entering_links_to_node[k]:
						#for each que
						#for q in val_di_id_link_val_link[lk].get_set_veh_queue().get_di_obj_veh_queue_at_link():
							#va_di_addition_param_mp_ctrl[q]=1
					#if the link is not an exit one
					#for lk1 in dict_id_node_id_leaving_links_from_node[k]:
						#if val_di_id_link_val_link[lk1].get_type_network_link()!=Cl_Network_Link.TYPE_NETWORK_LINK["exit"]:

							#for q1 in val_di_id_link_val_link[lk1].get_set_veh_queue().get_di_obj_veh_queue_at_link():
								#va_di_addition_param_mp_ctrl[q1]=1
						
				
				#va_li_param_inters_ctrl[1]=va_di_addition_param_mp_ctrl
				
				#print("va_li_param_inters_ctrl",va_li_param_inters_ctrl)
				#import sys
				#sys.exit()
					
				
			#creation of a control actuate object
			ctr_act_obj=self.fct_creat_inters_control_actuat_obj(v_type_control=di_id_nd_type_and_ctrl_categ[k][0],\
			v_control_categ=di_id_nd_type_and_ctrl_categ[k][1],v_li_param_inters_ctrl=\
			va_li_param_inters_ctrl)
			#,\
			#val_turn_ratios_estimated=di_id_nd_type_and_ctrl_categ[k][2])
			
			#if for this intersection the turn ratios will be estimated
			if k in dict_id_nd_param_turn_ratio_estim:
			
				
				di=dict(val_dict_estim_rp[k])
				
				#if we have od matrices
				if val_exist_od_mat==1:
				
					if k in dict_current_cum_mod:
					
						inters=Cl_Intersection_Signalised.Intersection_Signalised(va_id_nd=k,\
						va_li_id_input_network_links_to_inters_node=dict_id_node_id_entering_links_to_node[k],\
						va_li_id_output_network_links_from_inters_node=dict_id_node_id_leaving_links_from_node[k],\
						val_current_dict_rout_prob=di_id_nd_val_dic_rp[k],\
						val_current_dict_cum_rout_prob=di_id_nd_val_di_cum_rp[k],\
						val_current_dict_cum_mod=dict_current_cum_mod[k],\
						val_estim_turn_ratios=1,\
						val_di_stages_sign_intersection=dict_id_node_li_si_stages[k],val_ctrl_actuate_obj=ctr_act_obj,\
						val_lis_param_estim_turn_ratios=dict_id_nd_param_turn_ratio_estim[k],val_dict_estimat_rp=di)
						
					else:
						inters=Cl_Intersection_Signalised.Intersection_Signalised(va_id_nd=k,\
						va_li_id_input_network_links_to_inters_node=dict_id_node_id_entering_links_to_node[k],\
						va_li_id_output_network_links_from_inters_node=dict_id_node_id_leaving_links_from_node[k],\
						val_current_dict_rout_prob=di_id_nd_val_dic_rp[k],\
						val_current_dict_cum_rout_prob=di_id_nd_val_di_cum_rp[k],\
						val_estim_turn_ratios=1,\
						val_di_stages_sign_intersection=dict_id_node_li_si_stages[k],val_ctrl_actuate_obj=ctr_act_obj,\
						val_lis_param_estim_turn_ratios=dict_id_nd_param_turn_ratio_estim[k],val_dict_estimat_rp=di)

					di_inters[k]=inters
					
				#if we do not have od mat
				elif val_exist_od_mat==0:
				
					#print("node",k, dict_id_node_li_si_stages[k])
					#print()
					#import sys
					#sys.exit()
					inters=Cl_Intersection_Signalised.Intersection_Signalised(va_id_nd=k,\
					va_li_id_input_network_links_to_inters_node=dict_id_node_id_entering_links_to_node[k],\
					va_li_id_output_network_links_from_inters_node=dict_id_node_id_leaving_links_from_node[k],\
					val_current_dict_rout_prob=di_id_nd_val_dic_rp[k],\
					val_current_dict_cum_rout_prob=di_id_nd_val_di_cum_rp[k],\
					val_estim_turn_ratios=1,\
					val_di_stages_sign_intersection=dict_id_node_li_si_stages[k],val_ctrl_actuate_obj=ctr_act_obj,\
					val_lis_param_estim_turn_ratios=dict_id_nd_param_turn_ratio_estim[k],val_dict_estimat_rp=di)

					di_inters[k]=inters
				
			#if for this intersection the turn ratios will not be estimated
			else:
				#if we have od matrices
				if val_exist_od_mat==1:
				
					
					if k in dict_current_cum_mod:
						
						if k in di_id_nd_val_di_cum_rp:
						
							inters=Cl_Intersection_Signalised.Intersection_Signalised(va_id_nd=k,\
							va_li_id_input_network_links_to_inters_node=dict_id_node_id_entering_links_to_node[k],\
							va_li_id_output_network_links_from_inters_node=dict_id_node_id_leaving_links_from_node[k],\
							val_current_dict_rout_prob=di_id_nd_val_dic_rp[k],\
							val_current_dict_cum_rout_prob=di_id_nd_val_di_cum_rp[k],\
							val_current_dict_cum_mod=dict_current_cum_mod[k],\
							val_estim_turn_ratios=0,\
							val_di_stages_sign_intersection=dict_id_node_li_si_stages[k],val_ctrl_actuate_obj=ctr_act_obj)
						
						#if k not in di_id_nd_val_di_cum_rp
						else:
							inters=Cl_Intersection_Signalised.Intersection_Signalised(va_id_nd=k,\
							va_li_id_input_network_links_to_inters_node=dict_id_node_id_entering_links_to_node[k],\
							va_li_id_output_network_links_from_inters_node=dict_id_node_id_leaving_links_from_node[k],\
							val_current_dict_cum_mod=dict_current_cum_mod[k],\
							val_estim_turn_ratios=0,\
							val_di_stages_sign_intersection=dict_id_node_li_si_stages[k],val_ctrl_actuate_obj=ctr_act_obj)
						
					else:
						inters=Cl_Intersection_Signalised.Intersection_Signalised(va_id_nd=k,\
						va_li_id_input_network_links_to_inters_node=dict_id_node_id_entering_links_to_node[k],\
						va_li_id_output_network_links_from_inters_node=dict_id_node_id_leaving_links_from_node[k],\
						val_current_dict_rout_prob=di_id_nd_val_dic_rp[k],\
						val_current_dict_cum_rout_prob=di_id_nd_val_di_cum_rp[k],\
						val_estim_turn_ratios=0,\
						val_di_stages_sign_intersection=dict_id_node_li_si_stages[k],val_ctrl_actuate_obj=ctr_act_obj)
				
					di_inters[k]=inters
					
				#if we do not have od mat
				elif val_exist_od_mat==0:
				
					inters=Cl_Intersection_Signalised.Intersection_Signalised(va_id_nd=k,\
					va_li_id_input_network_links_to_inters_node=dict_id_node_id_entering_links_to_node[k],\
					va_li_id_output_network_links_from_inters_node=dict_id_node_id_leaving_links_from_node[k],\
					val_current_dict_rout_prob=di_id_nd_val_dic_rp[k],\
					val_current_dict_cum_rout_prob=di_id_nd_val_di_cum_rp[k],\
					val_estim_turn_ratios=0,\
					val_di_stages_sign_intersection=dict_id_node_li_si_stages[k],val_ctrl_actuate_obj=ctr_act_obj)
					di_inters[k]=inters
				
		for j in di_id_non_sign_inters_nd_value_zero:
		
			#if the turn ratios will be estimated
			if j in dict_id_nd_param_turn_ratio_estim:
			
				di=dict(di_id_nd_val_dic_rp[j])
				
				#if we have od matrices
				if val_exist_od_mat==1:
				
					if j in dict_current_cum_mod:
						inters=Cl_Intersection_Non_Signalised.Intersection_Non_Signalised(va_id_nd=j,\
						va_li_id_input_network_links_to_inters_node=dict_id_node_id_entering_links_to_node[j],\
						va_li_id_output_network_links_from_inters_node=dict_id_node_id_leaving_links_from_node[j],\
						val_current_dict_rout_prob=di_id_nd_val_dic_rp[j],\
						val_current_dict_cum_rout_prob=di_id_nd_val_di_cum_rp[j],\
						val_current_dict_cum_mod=dict_current_cum_mod[j],\
						val_estim_turn_ratios=1,\
						val_di_li_compatible_phases=dict_id_node_li_nsi_stages[j],\
						val_dict_estimat_rp=di)
					else:
						inters=Cl_Intersection_Non_Signalised.Intersection_Non_Signalised(va_id_nd=j,\
						va_li_id_input_network_links_to_inters_node=dict_id_node_id_entering_links_to_node[j],\
						va_li_id_output_network_links_from_inters_node=dict_id_node_id_leaving_links_from_node[j],\
						val_current_dict_rout_prob=di_id_nd_val_dic_rp[j],\
						val_current_dict_cum_rout_prob=di_id_nd_val_di_cum_rp[j],\
						val_estim_turn_ratios=1,\
						val_di_li_compatible_phases=dict_id_node_li_nsi_stages[j],\
						val_dict_estimat_rp=di)
					
				#if we do not have od mat
				elif val_exist_od_mat==0:
				
					inters=Cl_Intersection_Non_Signalised.Intersection_Non_Signalised(va_id_nd=j,\
					va_li_id_input_network_links_to_inters_node=dict_id_node_id_entering_links_to_node[j],\
					va_li_id_output_network_links_from_inters_node=dict_id_node_id_leaving_links_from_node[j],\
					val_current_dict_rout_prob=di_id_nd_val_dic_rp[j],\
					val_current_dict_cum_rout_prob=di_id_nd_val_di_cum_rp[j],\
					val_estim_turn_ratios=1,\
					val_di_li_compatible_phases=dict_id_node_li_nsi_stages[j],\
					val_dict_estimat_rp=di)
				
			#if the turn ratios wil not be estimated
			else:
				#if we have od matrices
				if val_exist_od_mat==1:
				
					if j in dict_current_cum_mod:
						inters=Cl_Intersection_Non_Signalised.Intersection_Non_Signalised(va_id_nd=j,\
						va_li_id_input_network_links_to_inters_node=dict_id_node_id_entering_links_to_node[j],\
						va_li_id_output_network_links_from_inters_node=dict_id_node_id_leaving_links_from_node[j],\
						val_current_dict_rout_prob=di_id_nd_val_dic_rp[j],\
						val_current_dict_cum_rout_prob=di_id_nd_val_di_cum_rp[j],\
						val_current_dict_cum_mod=dict_current_cum_mod[j],\
						val_estim_turn_ratios=0,\
						val_di_li_compatible_phases=dict_id_node_li_nsi_stages[j])
					else:
						inters=Cl_Intersection_Non_Signalised.Intersection_Non_Signalised(va_id_nd=j,\
						va_li_id_input_network_links_to_inters_node=dict_id_node_id_entering_links_to_node[j],\
						va_li_id_output_network_links_from_inters_node=dict_id_node_id_leaving_links_from_node[j],\
						val_current_dict_rout_prob=di_id_nd_val_dic_rp[j],\
						val_current_dict_cum_rout_prob=di_id_nd_val_di_cum_rp[j],\
						val_estim_turn_ratios=0,\
						val_di_li_compatible_phases=dict_id_node_li_nsi_stages[j])
					
				#if we do not have od mat
				elif val_exist_od_mat==0:
				
					inters=Cl_Intersection_Non_Signalised.Intersection_Non_Signalised(va_id_nd=j,\
					va_li_id_input_network_links_to_inters_node=dict_id_node_id_entering_links_to_node[j],\
					va_li_id_output_network_links_from_inters_node=dict_id_node_id_leaving_links_from_node[j],\
					val_current_dict_rout_prob=di_id_nd_val_dic_rp[j],\
					val_current_dict_cum_rout_prob=di_id_nd_val_di_cum_rp[j],\
					val_estim_turn_ratios=0,\
					val_di_li_compatible_phases=dict_id_node_li_nsi_stages[j])
			
				
			di_inters[j]=inters
			
			
		
		#for i in dict_id_node_id_entering_links_to_node:
		
			#if the node id corresponds to a non sgnalised intersection
			#if i in di_id_non_signal_inters:
				#inters=Cl_Intersection_Non_Signalised.Intersection_Non_Signalised(val_id_nd=i,\
				#val_li_id_input_network_links_to_inters_node=dict_id_node_id_entering_links_to_node[i],\
				#val_li_id_output_network_links_from_inters_node=dict_id_node_id_leaving_links_from_node[i],\
				#val_di_stages_intersection=dict_id_node_li_stages[i])
			
			#if the node id corresponds to a  sgnalised intersection
			#else:
				#inters=Cl_Intersection_Signalised.Intersection_Signalised(val_id_nd=i,\
				#val_li_id_input_network_links_to_inters_node=dict_id_node_id_entering_links_to_node[i],\
				#val_li_id_output_network_links_from_inters_node=dict_id_node_id_leaving_links_from_node[i],\
				#val_di_stages_intersection=dict_id_node_li_stages[i])
			
			#di_inters[i]=inters
		
		return di_inters
#*****************************************************************************************************************************************************************************************
	#method returning a dictionary with the entry links, and the value of the queue id, (so as the queues will have consequent increasing values),
	#key=id of the entry link, value= the entry link object
	#val_dict_id_node_id_entry_links_to_network= dict, key = node id, 
	#value = list of id of entry links to the network, entering at this node
	#val_dict_id_node_id_leaving_links_from_node=dict, key=id node, value= list with the link id leaving from this node
	#val_dict_id_all_phases_max_queue_size_et_sat_flow_queue_type, key=(id link, id output link)
	#the value= list [max queue size, saturation flow of the phase,queue_type]
	#val_dict_id_all_network_link_id_orig_dest_node_length_link=dictionary, key= the link id,
	#value=[id origin node, id destination node, length link]
	#val_di_parameters_fct_creating_demand_entry_link= a dictionary, key=the id of the entry link, value is a list with the 
	#parameters fo the function creating the demand at the entry link
	#val_di_id_entry_link_li_id_sublinks, dictionary, key = the id of the entry link, value list id sublinks
	#val_ind_q=the value for the id of the first queue
	#val_di_id_entry_link_demand_param_entry_link= dictionary, key =id link, value= the poisson param for veh arrival
	#val_di_key_id_lk_value_list_id_merging_ques= dict, key= link id, value=list [...,id_dest_link,..]
	#thus phases [link_id,m] for m in value have merging queues (merging queues are ques locqted in the same link,
	#of which their vehicles can be mixed, notion corresponding to shared lanes)
	
	#val_dic_sensor_inform_associated_to_ques_of_links=dict,  key=id link, value=dict, key=id phase associated with link, 
	#value=-1 if sensor captures the entire que, or
	#value=n>0 if sensor captures the whole que from the nth position (1st position indicated by zero) or
	#value=[id initial posit cpatures by sensor, id final position captured by sensor, nb positions captrured by sensor]

	def funct_creating_dict_entry_links_to_network(self, \
	val_time_unit,\
	val_creat_new_demand=None,val_dict_id_node_id_entry_links_to_network={},\
	val_dict_id_node_id_leaving_links_from_node={},\
	val_dict_id_all_phases_max_queue_size_et_sat_flow_queue_type={},\
	val_dict_id_all_network_link_id_orig_dest_node_length_link_capacity_link_param_travel_duration={},\
	val_fct_calcul_demand_entry_link=None,\
	val_di_parameters_fct_creating_demand_entry_link={},val_ind_queue=1,\
	val_di_id_entry_link_demand_param_entry_link={},\
	val_dic_key_que_id_value_li_pos_value_pres_detector={},val_dic_key_que_id_value_li_pos_value_que_size_detector={},\
	val_dic_key_id_non_sign_inters_value_zero={},\
	val_sim_duration=None,val_round_prec=2,val_di_id_nd_with_estim_turn_ratios=None,val_indicat_type_veh_final_dest=None,\
	val_di_key_id_nd_val_dict_id_phase_val_li_interf_phase_and_param={},val_di_key_id_lk_value_type_rout_manag={}):
	
		dict_entry_link={}
		val_que_id=val_ind_queue
		
		#print("val_dict_id_node_id_entry_links_to_network",val_dict_id_node_id_entry_links_to_network)
		#for each head node of an entry link
		for i in val_dict_id_node_id_entry_links_to_network:
			
			#for each entry link associated with the node
			for j in val_dict_id_node_id_entry_links_to_network[i]:
			
			
				#the list of veh queues, as many elements as the output links from the node
				li_veh_q=[]
				for m in val_dict_id_node_id_leaving_links_from_node[i]:
					li_veh_q.append([])
					
				#creation of the dictionary with the max queue size and saturation flow and queue type for each phase (queue,movement)
				#associated with link j
				#print("val_dict_id_all_phases_max_queue_size_et_sat_flow_queue_type",val_dict_id_all_phases_max_queue_size_et_sat_flow_queue_type.keys())
				
				di_queue_max_queue_size_et_sat_flow_phases_queue_type_entry_lk={}
				for m in val_dict_id_node_id_leaving_links_from_node[i]:
					#print(j,m)
					di_queue_max_queue_size_et_sat_flow_phases_queue_type_entry_lk[(j,m)]=\
					val_dict_id_all_phases_max_queue_size_et_sat_flow_queue_type[(j,m)]
					
					total_que_serv_rate=-1
					#if the node corresponds to a non signalised intersection we calculate the total que service rate 
					if i in val_dic_key_id_non_sign_inters_value_zero:
						#print("i=",i,di_queue_max_queue_size_et_sat_flow_phases_queue_type_entry_lk_param_tr_dur[(j,m)][1],val_sim_duration)
					
						total_que_serv_rate=round(\
						di_queue_max_queue_size_et_sat_flow_phases_queue_type_entry_lk[(j,m)][1] *\
						val_sim_duration,val_round_prec)
				
				
				if i in val_di_key_id_nd_val_dict_id_phase_val_li_interf_phase_and_param:
					
					di_interf_phases=val_di_key_id_nd_val_dict_id_phase_val_li_interf_phase_and_param[i]
					
				else:
					di_interf_phases={}
					
				set_q_obj=Cl_Set_Vehicle_Queues_Link.Set_Vehicle_Queues_Link(\
				val_ti_unit=val_time_unit,\
				val_queue_id=val_que_id,val_id_assoc_link=j,\
				val_li_id_associated_output_links_from_link=val_dict_id_node_id_leaving_links_from_node[i],\
				val_li_queue_veh=li_veh_q,\
				val_dict_queue_max_queue_size_et_sat_flow_queue_type=\
				di_queue_max_queue_size_et_sat_flow_phases_queue_type_entry_lk,\
				val_cur_service_rate=total_que_serv_rate,val_dict_phase_interference=di_interf_phases)

				
				#if we need to calculate the list with the output links of all the queues
				if i in val_di_id_nd_with_estim_turn_ratios or \
				val_indicat_type_veh_final_dest!=Cl_Decisions.TYPE_VEHICLE_FINAL_DESTINATION_AND_PATH["dynamically_defined"]:
					v_li_id_outp_lks=set_q_obj.get_li_output_lk_ids_associated_with_ques()
				#if we do not need to calculate the list with the output links of all the queues
				else:
					v_li_id_outp_lks=None
				
								
				#update the queue index
				val_que_id=set_q_obj.get_queue_id()
				
				
				#creation of the entry link
				#the  number of veh passages by the queue is initialised to -1
				
				
				#if a new demand will be generated
				if  val_creat_new_demand==List_Explicit_Values.initialisation_value_to_one:
				
					#if a mixed rout management is associated with the link
					if j in val_di_key_id_lk_value_type_rout_manag:
					
						entry_lk=Cl_Network_Entry_Link.Network_Entry_Link(\
						val_id_lnk=j,val_li_id_output_links_from_lnk=val_dict_id_node_id_leaving_links_from_node[i],\
						val_set_vehicle_que=set_q_obj,\
						val_length_lnk=\
						val_dict_id_all_network_link_id_orig_dest_node_length_link_capacity_link_param_travel_duration[j][\
						List_Explicit_Values.val_third_element_of_list],\
						val_capacity_lnk=val_dict_id_all_network_link_id_orig_dest_node_length_link_capacity_link_param_travel_duration[j]\
						[List_Explicit_Values.val_fourth_element_of_list],\
						val_id_head_intersection_nd=i,\
						val_fct_creating_demand_entry_link=val_fct_calcul_demand_entry_link,\
						val_lis_parameters_fct_creating_demand_entry_link=val_di_parameters_fct_creating_demand_entry_link[j],\
						val_li_output_lks_queues=v_li_id_outp_lks,val_type_routing_entry_lk_when_mixed_management=val_di_key_id_lk_value_type_rout_manag[j])
					
					#if not a mixed rout management is associated with the link
					else:
				
						entry_lk=Cl_Network_Entry_Link.Network_Entry_Link(\
						val_id_lnk=j,val_li_id_output_links_from_lnk=val_dict_id_node_id_leaving_links_from_node[i],\
						val_set_vehicle_que=set_q_obj,\
						val_length_lnk=\
						val_dict_id_all_network_link_id_orig_dest_node_length_link_capacity_link_param_travel_duration[j][\
						List_Explicit_Values.val_third_element_of_list],\
						val_capacity_lnk=val_dict_id_all_network_link_id_orig_dest_node_length_link_capacity_link_param_travel_duration[j]\
						[List_Explicit_Values.val_fourth_element_of_list],\
						val_id_head_intersection_nd=i,\
						val_fct_creating_demand_entry_link=val_fct_calcul_demand_entry_link,\
						val_lis_parameters_fct_creating_demand_entry_link=val_di_parameters_fct_creating_demand_entry_link[j],\
						val_li_output_lks_queues=v_li_id_outp_lks)
				#if a previous or given demand will be employed
				elif val_creat_new_demand==List_Explicit_Values.initialisation_value_to_zero or\
					val_creat_new_demand==List_Explicit_Values.initialisation_value_to_minus_one:
					
					#if a mixed rout management is associated with the link
					if j in val_di_key_id_lk_value_type_rout_manag:
					
						entry_lk=Cl_Network_Entry_Link.Network_Entry_Link(\
						val_id_lnk=j,val_li_id_output_links_from_lnk=val_dict_id_node_id_leaving_links_from_node[i],\
						val_set_vehicle_que=set_q_obj,\
						val_length_lnk=\
						val_dict_id_all_network_link_id_orig_dest_node_length_link_capacity_link_param_travel_duration[j][\
						List_Explicit_Values.val_third_element_of_list],\
						val_capacity_lnk=val_dict_id_all_network_link_id_orig_dest_node_length_link_capacity_link_param_travel_duration[j]\
						[List_Explicit_Values.val_fourth_element_of_list],\
						val_id_head_intersection_nd=i,\
						val_fct_creating_demand_entry_link=val_fct_calcul_demand_entry_link,\
						val_lis_parameters_fct_creating_demand_entry_link=val_di_parameters_fct_creating_demand_entry_link[j],\
						val_li_output_lks_queues=v_li_id_outp_lks,val_type_routing_entry_lk_when_mixed_management=val_di_key_id_lk_value_type_rout_manag[j])
					
					#if not a mixed rout management is associated with the link
					else:
					
						entry_lk=Cl_Network_Entry_Link.Network_Entry_Link(\
						val_id_lnk=j,val_li_id_output_links_from_lnk=val_dict_id_node_id_leaving_links_from_node[i],\
						val_set_vehicle_que=set_q_obj,\
						val_length_lnk=\
						val_dict_id_all_network_link_id_orig_dest_node_length_link_capacity_link_param_travel_duration[j][\
						List_Explicit_Values.val_third_element_of_list],\
						val_capacity_lnk=val_dict_id_all_network_link_id_orig_dest_node_length_link_capacity_link_param_travel_duration[j]\
						[List_Explicit_Values.val_fourth_element_of_list],\
						val_id_head_intersection_nd=i,\
						val_fct_creating_demand_entry_link=val_fct_calcul_demand_entry_link,\
						val_lis_parameters_fct_creating_demand_entry_link=val_di_parameters_fct_creating_demand_entry_link[j],\
						val_li_output_lks_queues=v_li_id_outp_lks)
					#,\
					#val_fct_creating_demand_entry_link=Global_Functions.fct_calcul_demand_entry_link)
				else:
					print("PROBLEM IN CL_CREAT_NET, CREAT ENTRY LKS NOT SBLKS, val_creat_new_demand",val_creat_new_demand)
				
				dict_entry_link[entry_lk.get_id_link()]=entry_lk
			
		return [dict_entry_link,val_que_id]

#*****************************************************************************************************************************************************************************************
	#method returing a dictionary with the exit links from the network (key=entry link id, value=entry link)
	#dict_exit_links_from_network_nd is a dictionary of which the key is the id of the node, 
	# the value is a list of the id of the exit nodes at this node
	
	def funct_creating_dict_exit_links_from_network(self,val_dict_id_node_id_exit_links_from_network={},\
	val_dict_id_node_id_entering_links_to_node={},val_dict_id_all_network_link_id_orig_dest_node_length_link={},\
	val_dict_id_all_phases_max_queue_size_sat_flow_queue_type={}):
	
		dict_exit_link={}
		#we copy the dictionaty with the id of the leaving links from each node
		#val_dict_id_node_id_entering_links_to_node=dict(val_dict_id_node_id_entering_links_to_node)


		
		#for each tail node of an exit link
		for i in val_dict_id_node_id_exit_links_from_network:
		
			#for each id of exit link
			for j in val_dict_id_node_id_exit_links_from_network[i]:
				li_id_input_links=self.fct_creat_input_lks_to_lk(\
				li_input_lks_to_lk=val_dict_id_node_id_entering_links_to_node[i],\
				id_lk=j,dict_id_all_phases_max_queue_size_sat_flow_queue_type=\
				val_dict_id_all_phases_max_queue_size_sat_flow_queue_type)
					
				#creation of the exit link
				#exit_link=Cl_Network_Exit_Link.Network_Exit_Link(val_id_lnk=j,val_li_id_input_links_to_lnk=val_dict_id_node_id_entering_links_to_node[i],\
				#val_length_lnk=val_dict_id_all_network_link_id_orig_dest_node_length_link[j][List_Explicit_Values.val_third_element_of_list],\
				#val_id_tail_intersection_nd=i)
				exit_link=Cl_Network_Exit_Link.Network_Exit_Link(val_id_lnk=j,val_li_id_input_links_to_lnk=li_id_input_links,\
				val_length_lnk=val_dict_id_all_network_link_id_orig_dest_node_length_link[j][List_Explicit_Values.val_third_element_of_list],\
				val_capacity_lnk=val_dict_id_all_network_link_id_orig_dest_node_length_link[j][List_Explicit_Values.val_fourth_element_of_list],\
				val_id_tail_intersection_nd=i)
				
				dict_exit_link[exit_link.get_id_link()]=exit_link
		

			
		return dict_exit_link
		
#*****************************************************************************************************************************************************************************************

	#function creating a dictionary with the internal links
	#it returns  a list, [dictionary with the internal links, the index for the numerotation of queue links]
	#val_ind_q=the value for the id of the first queue
	
	#val_dic_sensor_inform_associated_to_ques_of_links=dict,  key=id link, value=dict, key=id phase associated with link, 
	#value=-1 if sensor captures the entire que, or
	#value=n>0 if sensor captures the whole que from the nth position (1st position indicated by zero) or
	#value=[id initial posit cpatures by sensor, id final position captured by sensor, nb positions captrured by sensor]
	
	def funct_creating_dict_internal_links_to_network(self,\
	val_time_unit,\
	val_dict_id_internal_link_id_orig_dest_node={},\
	val_dict_id_node_id_entering_links_to_node={},\
	val_dict_id_node_id_leaving_links_from_node={},\
	val_dict_id_all_phases_max_queue_size_et_sat_flow_queue_type={},\
	val_dict_id_all_network_link_id_orig_dest_node_length_link_capacity_link_param_travel_duration={},\
	val_ind_queue=1,\
	val_dic_key_que_id_value_li_pos_value_pres_detector={},val_dic_key_que_id_value_li_pos_value_que_size_detector={},\
	val_indicat_type_veh_final_dest=None,val_di_id_nd_with_estim_turn_ratios=None,\
	val_di_key_id_nd_val_dict_id_phase_val_li_interf_phase_and_param={}):
		
			
		dict_intern_lk={}
		val_que_id=val_ind_queue
		
		
		#for each internal  link id
		for i in val_dict_id_internal_link_id_orig_dest_node:
			
			#if turn ratios are going to be estimated of the origin node of the link (then the li with the ids of links of the the output queues should be defined)
			if val_dict_id_internal_link_id_orig_dest_node[i][List_Explicit_Values.val_second_element_of_list] in val_di_id_nd_with_estim_turn_ratios:
		
				#the list of veh queues, as many elements as the queues of the entry link
				#(this is the number of the leaving queues from the head node of the link)
				li_veh_q=[]
				for m in val_dict_id_node_id_leaving_links_from_node[\
				val_dict_id_internal_link_id_orig_dest_node[i][List_Explicit_Values.val_second_element_of_list]]:
					li_veh_q.append([])
				
				#creation of the dictionary with the max queue size and saturation flow for each phase (queue,movement)
				#associated with link j
				di_queue_max_queue_size_et_sat_flow_phases_queue_type={}
				#print("HERE:",val_dict_id_all_phases_max_queue_size_et_sat_flow.keys())
				for m in val_dict_id_node_id_leaving_links_from_node[val_dict_id_internal_link_id_orig_dest_node[i]\
				[List_Explicit_Values.val_second_element_of_list]]:
					#print(j,m)
					di_queue_max_queue_size_et_sat_flow_phases_queue_type[(i,m)]=\
					val_dict_id_all_phases_max_queue_size_et_sat_flow_queue_type[(i,m)]
				
				if val_dict_id_internal_link_id_orig_dest_node[i][ List_Explicit_Values.val_second_element_of_list] in val_di_key_id_nd_val_dict_id_phase_val_li_interf_phase_and_param:
					di_interf_phases=val_di_key_id_nd_val_dict_id_phase_val_li_interf_phase_and_param[i]
				else:
					di_interf_phases={}
						
				set_q_obj=Cl_Set_Vehicle_Queues_Link.Set_Vehicle_Queues_Link(\
				val_ti_unit=val_time_unit,\
				val_queue_id=val_que_id,val_id_assoc_link=i,\
				val_li_id_associated_output_links_from_link=val_dict_id_node_id_leaving_links_from_node[\
				val_dict_id_internal_link_id_orig_dest_node[i][List_Explicit_Values.val_second_element_of_list]],\
				val_li_queue_veh=li_veh_q,\
				val_dict_queue_max_queue_size_et_sat_flow_queue_type=\
				di_queue_max_queue_size_et_sat_flow_phases_queue_type,val_dict_phase_interference=di_interf_phases)
			
				#update the queue index
				val_que_id=set_q_obj.get_queue_id()
			
				v_li_id_outp_lks=set_q_obj.get_li_output_lk_ids_associated_with_ques()
				
				
				li_id_input_links=self.fct_creat_input_lks_to_lk(\
				li_input_lks_to_lk=val_dict_id_node_id_entering_links_to_node[\
				val_dict_id_internal_link_id_orig_dest_node[i][ List_Explicit_Values.val_first_element_of_list]],\
				id_lk=i,dict_id_all_phases_max_queue_size_sat_flow_queue_type=\
				val_dict_id_all_phases_max_queue_size_et_sat_flow_queue_type)
				
				
				intern_lk=Cl_Network_Internal_Link.Network_Internal_Link(val_id_lnk=i,\
				val_li_id_input_links_to_lnk=li_id_input_links,
				val_li_id_output_links_from_lnk=val_dict_id_node_id_leaving_links_from_node[\
				val_dict_id_internal_link_id_orig_dest_node[i][ List_Explicit_Values.val_second_element_of_list]],\
				val_set_vehicle_que=set_q_obj,\
				val_length_lnk=val_dict_id_all_network_link_id_orig_dest_node_length_link_capacity_link_param_travel_duration[i][\
				List_Explicit_Values.val_third_element_of_list],\
				val_capacity_lnk=\
				val_dict_id_all_network_link_id_orig_dest_node_length_link_capacity_link_param_travel_duration[i][\
				List_Explicit_Values.val_fourth_element_of_list],\
				val_id_head_intersection_nd=val_dict_id_internal_link_id_orig_dest_node[i][ List_Explicit_Values.val_second_element_of_list],\
				val_id_tail_intersection_nd=val_dict_id_internal_link_id_orig_dest_node[i][List_Explicit_Values.val_first_element_of_list],\
				val_param_lk_travel_duration=\
				val_dict_id_all_network_link_id_orig_dest_node_length_link_capacity_link_param_travel_duration[i][List_Explicit_Values.val_fifth_element_of_list],\
				val_li_output_lks_queues=v_li_id_outp_lks)

				dict_intern_lk[intern_lk.get_id_link()]=intern_lk
				
				
			
			#if turn ratios will not be estimated for the head node of the link, then we need to examine whether the list with the id of the output links of the queues will be  created
			else:
			
				#the list of veh queues, as many elements as the queues of the entry link
				#(this is the number of the leaving queues from the head node of the link)
				li_veh_q=[]
				for m in val_dict_id_node_id_leaving_links_from_node[\
				val_dict_id_internal_link_id_orig_dest_node[i][List_Explicit_Values.val_second_element_of_list]]:
					li_veh_q.append([])
				
				#creation of the dictionary with the max queue size and saturation flow for each phase (queue,movement)
				#associated with link j
				di_queue_max_queue_size_et_sat_flow_phases_queue_type={}
				#print("HERE:",val_dict_id_all_phases_max_queue_size_et_sat_flow.keys())
				for m in val_dict_id_node_id_leaving_links_from_node[val_dict_id_internal_link_id_orig_dest_node[i]\
				[List_Explicit_Values.val_second_element_of_list]]:
					#print(j,m)
					di_queue_max_queue_size_et_sat_flow_phases_queue_type[(i,m)]=\
					val_dict_id_all_phases_max_queue_size_et_sat_flow_queue_type[(i,m)]
					
				
				if val_dict_id_internal_link_id_orig_dest_node[i][ List_Explicit_Values.val_second_element_of_list] in val_di_key_id_nd_val_dict_id_phase_val_li_interf_phase_and_param:
					di_interf_phases=val_di_key_id_nd_val_dict_id_phase_val_li_interf_phase_and_param[i]
				else:
					di_interf_phases={}	
					
				set_q_obj=Cl_Set_Vehicle_Queues_Link.Set_Vehicle_Queues_Link(\
				val_ti_unit=val_time_unit,\
				val_queue_id=val_que_id,val_id_assoc_link=i,\
				val_li_id_associated_output_links_from_link=val_dict_id_node_id_leaving_links_from_node[\
				val_dict_id_internal_link_id_orig_dest_node[i][List_Explicit_Values.val_second_element_of_list]],\
				val_li_queue_veh=li_veh_q,\
				val_dict_queue_max_queue_size_et_sat_flow_queue_type=\
				di_queue_max_queue_size_et_sat_flow_phases_queue_type,val_dict_phase_interference=di_interf_phases)
			
				#update the queue index
				val_que_id=set_q_obj.get_queue_id()
			
			
				#if the vehicle final destination is not dynamicl defined we need to calculate the list with the output links of all the queues
				if val_indicat_type_veh_final_dest!=Cl_Decisions.TYPE_VEHICLE_FINAL_DESTINATION_AND_PATH["dynamically_defined"]:
					v_li_id_outp_lks=set_q_obj.get_li_output_lk_ids_associated_with_ques()
				#if we do not need to calculate the list with the output links of all the queues
				else:
					v_li_id_outp_lks=None
			
				
				
				li_id_input_links=self.fct_creat_input_lks_to_lk(\
				li_input_lks_to_lk=val_dict_id_node_id_entering_links_to_node[\
				val_dict_id_internal_link_id_orig_dest_node[i][ List_Explicit_Values.val_first_element_of_list]],\
				id_lk=i,dict_id_all_phases_max_queue_size_sat_flow_queue_type=\
				val_dict_id_all_phases_max_queue_size_et_sat_flow_queue_type)
				
				
				intern_lk=Cl_Network_Internal_Link.Network_Internal_Link(val_id_lnk=i,\
				val_li_id_input_links_to_lnk=li_id_input_links,
				val_li_id_output_links_from_lnk=val_dict_id_node_id_leaving_links_from_node[\
				val_dict_id_internal_link_id_orig_dest_node[i][ List_Explicit_Values.val_second_element_of_list]],\
				val_set_vehicle_que=set_q_obj,\
				val_length_lnk=val_dict_id_all_network_link_id_orig_dest_node_length_link_capacity_link_param_travel_duration[i][\
				List_Explicit_Values.val_third_element_of_list],\
				val_capacity_lnk=\
				val_dict_id_all_network_link_id_orig_dest_node_length_link_capacity_link_param_travel_duration[i][\
				List_Explicit_Values.val_fourth_element_of_list],\
				val_id_head_intersection_nd=val_dict_id_internal_link_id_orig_dest_node[i][ List_Explicit_Values.val_second_element_of_list],\
				val_id_tail_intersection_nd=val_dict_id_internal_link_id_orig_dest_node[i][List_Explicit_Values.val_first_element_of_list],\
				val_param_lk_travel_duration=\
				val_dict_id_all_network_link_id_orig_dest_node_length_link_capacity_link_param_travel_duration[i][List_Explicit_Values.val_fifth_element_of_list],\
				val_li_output_lks_queues=v_li_id_outp_lks)

				dict_intern_lk[intern_lk.get_id_link()]=intern_lk
		
		return [dict_intern_lk,val_que_id]
						
#*****************************************************************************************************************************************************************************************
	#funtcion creating for each internal, exit link  a dictionary indicating the number of veh arrivals and the related link id, (case for estim turn ratios)
	#val_di_nd_with_turn_ratios_estim=dict, key=id nod with estim turn ratios, value=1
	def fct_creat_di_id_ar_lk_val_nb_ar_veh_for_internal_exit_lks(self, val_netw,val_di_nd_with_turn_ratios_estim):
		
		#for each node with estimated turn ratios
		for i in val_di_nd_with_turn_ratios_estim:
			#for each intput link of the node (exit or internal netw link)
			for j in val_netw.get_di_intersections()[i].get_li_id_input_network_links_to_inters_node():
			
				#if the internal link is not an entry one
				if j in val_netw.get_di_internal_links_to_network():
					#for each output queue of the internal link 
					for k in val_netw.get_di_internal_links_to_network()[j].get_li_output_links_queues():
					
						if val_netw.get_di_all_links()[k].get_di_ar_to_link_current_period() !=None:
							val_netw.get_di_all_links()[k].get_di_ar_to_link_current_period()[j]=0
						else:
							val_netw.get_di_all_links()[k].set_di_ar_to_link_current_period(n_v={})
							val_netw.get_di_all_links()[k].get_di_ar_to_link_current_period()[j]=0

		

#*****************************************************************************************************************************************************************************************
	#funtcion creating for each entry, internal, exit link  a dictionary indicating the number of veh arrivals and the related link id, (case for estim turn ratios-with OD)
	def fct_creat_di_id_ar_lk_val_nb_ar_veh_for_all_lks(self, val_netw,val_di_nd_with_turn_ratios_estim):
	
		#for each entry, exit internal link of the network we create the dict with the veh arrivals and their origin links
		#for each node with estimated turn ratios
		for i in val_di_nd_with_turn_ratios_estim:
			#for each intput link of the node (exit or internal netw link)
			for j in val_netw.get_di_intersections()[i].get_li_id_input_network_links_to_inters_node():
			
				#for each output queue of the internal link 
				for k in val_netw.get_di_internal_links_to_network()[j].get_li_output_links_queues():
					
					if val_netw.get_di_all_links()[k].get_di_ar_to_link_current_period() !=None:
						val_netw.get_di_all_links()[k].get_di_ar_to_link_current_period()[j]=0
					else:
						val_netw.get_di_all_links()[k].set_di_ar_to_link_current_period(n_v={})
						val_netw.get_di_all_links()[k].get_di_ar_to_link_current_period()[j]=0


#*****************************************************************************************************************************************************************************************
	#method creating the related  dict to the cum values of the prob of exit link and updating the dict of intersections
	def fct_creat_dict_cum_mod_without_varying_values_and_update_intersections(self,val_di_cum_mod,val_netw):
	
		dict_key_id_entry_intern_lk_value_li_cum_prob_final_dest_lk_and_id_lk={}
		#val_di_cum_mod=dict, key =id entry internal link, value=[...,[cum  prob final dest link, id final dest link],...]
		for i in val_di_cum_mod:
			#print("id entry link", i) 
			#if the head node of the link is not in the dict
			if val_netw.get_di_entry_links_to_network()[i].get_id_head_intersection_node() not in \
			dict_key_id_entry_intern_lk_value_li_cum_prob_final_dest_lk_and_id_lk:
			
				dict_key_id_entry_intern_lk_value_li_cum_prob_final_dest_lk_and_id_lk[\
				val_netw.get_di_entry_internal_links()[i].get_id_head_intersection_node()]={}
				
				di={}
				di[i]=\
				val_di_cum_mod[i]
				
				dict_key_id_entry_intern_lk_value_li_cum_prob_final_dest_lk_and_id_lk[\
				val_netw.get_di_entry_internal_links()[i].get_id_head_intersection_node()].update(di)
				
			
			#if the head node of the link is  in the dict
			else:
				di={}
				di[i]=\
				val_di_cum_mod[i]
										
				dict_key_id_entry_intern_lk_value_li_cum_prob_final_dest_lk_and_id_lk[\
				val_netw.get_di_entry_internal_links()[i].get_id_head_intersection_node()].update(di)
			
			
			#we associate the dict with the current cum rout prob to each intersection
			for t in dict_key_id_entry_intern_lk_value_li_cum_prob_final_dest_lk_and_id_lk:
				val_netw.get_di_intersections()[t].set_current_di_cum_mod(\
				dict_key_id_entry_intern_lk_value_li_cum_prob_final_dest_lk_and_id_lk[t])
	
			
#*****************************************************************************************************************************************************************************************
	#method returning a list [dict1, dict 2]
	#dict1=dictionary,key=node id, value=[type control, control category(string), 1/0 turn ratios estimated/not estimated]
	#dict2, key=id node with estim turn ratios, value=1
	def fct_creat_di_key_id_node_value_type_and_ctrl_category(self):
	
		di=Global_Functions_Network.fct_reading_fi_id_node_type_control(\
		val_name_file_to_read=File_Sim_Name_Module_Files.val_name_folder_with_control_param_files+"/"+\
		File_Sim_Name_Module_Files.val_name_file_node_id_control_type_category,nb_comment_lines=1)
		
		return di

#*****************************************************************************************************************************************************************************************
	#method creating the input links to a link
	def fct_creat_input_lks_to_lk(self,li_input_lks_to_lk,id_lk,dict_id_all_phases_max_queue_size_sat_flow_queue_type):
		li_rep=[]
		#print(li_input_lks_to_lk)
		#for each input link to link
		for i in li_input_lks_to_lk:
			if dict_id_all_phases_max_queue_size_sat_flow_queue_type[i,id_lk][1]>0:
				#print(dict_id_all_phases_max_queue_size_sat_flow_queue_type_param_travel_duration[i,id_lk][1])
				#print()
				li_rep.append(i)
		return li_rep


#*****************************************************************************************************************************************************************************************
	#method updating the path dictionary of each intersection when the model requires a choice fo an initial final destination from the  beginning 
	#and a given unique path is considered
	#di_paths_all_intersections= dict, key = node id, value = dict, key=(id entry, id exit link), value=[..., node to follow,...]
	def fct_update_path_dict_each_related_intersection(self,di_paths_all_intersections,val_network):
		for i in di_paths_all_intersections:
			val_network.get_di_intersections()[i].set_current_di_unique_paths(di_paths_all_intersections[i])



	#function creating a network object from the data file
	def function_creation_network(self,\
	val_id_netw=1,val_ind_que=1,val_nb_comment_lines=1,val_nb_lines_to_read_sensor_files=1,\
	val_nb_comment_lines_ft=2,val_nb_comment_lines_ft_off=1,va_nb_line_master_nd_info=5,val_nb_comment_lines_fi_durat_rp_mat=2,\
	val_nb_comment_lines_fi_mod=1,val_nb_comment_lines_mp=1,val_nb_comment_lines_psd=1,val_nb_comment_lines_fa=1,\
	val_nb_comment_lines_fa_max_green=1,val_nb_comment_lines_mp_practical=1):
	
		#creation of the dictionary of which the key is the node id and the value is a list containing the id of the entering links to the node
		dic_id_node_id_entering_links_to_node=Global_Functions_Network.function_reading_file_containing_nd_or_link_information(file_name_read=\
		"../"+self._name_data_folder+"/"+self._file_name_id_node_id_entering_links_to_node)
		
		
		#creation of the dictionary of which the key is the id of the node and the value is a list of the id of the leaving links from the node
		dic_id_node_id_leaving_links_from_node=Global_Functions_Network.function_reading_file_containing_nd_or_link_information(file_name_read=\
		"../"+self._name_data_folder+"/"+self._file_name_id_node_id_leaving_links_from_node)
		
	
		
		#creation of the dictionary of which the key is the id of node and the value is the list of the id of the entry links to this node
		dic_id_node_id_entry_links_to_network=Global_Functions_Network.function_reading_file_containing_nd_or_link_information(file_name_read=\
		"../"+self._name_data_folder+"/"+self._file_name_id_node_id_entry_links_to_network)
		
		#if the turn ratios are going to be 
		
		#creation of the dictionary of which the key is the id of node and the value is the list of the id of the exit links from this node
		dic_id_node_id_exit_links_to_network=Global_Functions_Network.function_reading_file_containing_nd_or_link_information(file_name_read=\
		"../"+self._name_data_folder+"/"+self._file_name_id_node_id_exit_links_from_network)
		
		
		#creation of the dictionary with the sublinks : key= link id, value is a list with the id of sublinks associated to the link
		#dic_id_link_id_sublinks=Global_Functions_Network.function_reading_file_containing_nd_or_link_information(file_name_read=\
		#"../"+self._name_data_folder+"/"+self._file_name_id_link_id_sublinks)
		
		#creation of the dictionary: key= phase (l,m) where m is output link from link l, 
		#value=[max queue size of phase, the saturation flow of the file, que type]
		dic_id_all_phases_max_queue_size_et_sat_flow_queue_type=Global_Functions_Network.\
		function_reading_file_containing_id_all_phases_andmax_queue_size_andsat_flow_andque_type(\
		name_file_read=\
		"../"+self._name_data_folder+"/"+self._file_name_id_all_phases_max_queue_size_and_sat_flow_queue_type,\
		nb_comment_lines=1)
		
		#creation of the dictionary :  key=id link, value=dict, key=id phase associated with link, 
		#value=-1 if sensor captures the entire que, or
		#value=n>0 if sensor captures the whole que from the nth position (1st position indicated by zero) or
		#value=[id initial posit cpatures by sensor, id final position captured by sensor, nb positions captrured by sensor]
		#di_id_link_sensor_inform_associated_to_phases=Global_Functions_Network.\
		#fct_creation_dict_sensor_information_per_link(\
		#val_name_file_to_read="../"+self._name_data_folder+"/"+\
		#self._module_name_import_file_names_model_network.val_file_name_id_all_phases_init_fin_detect_posit_nb_posit_captured,\
		#val_nb_comment_lines=1)
		
		#print(self._file_name_demand_param_entry_link)
		#the dictionary: key=the id of the entry link, value the list of parameters for calculating the demand of the entry link
		dic_demand_param_entry_link=Global_Functions_Network.function_reading_file_containing_nd_or_link_information(file_name_read=\
		"../"+self._name_data_folder+"/"+self._file_name_demand_param_entry_link,type=float)
		
		
		
		#the dictionary with the id of all links, the id of their origin and destination node and their length
		dic_id_all_network_link_id_orig_dest_node_length_link_capacity_link_param_travel_duration=Global_Functions_Network.\
		function_reading_file_containing_nd_or_link_information(file_name_read=\
		"../"+self._name_data_folder+"/"+self._id_all_network_link_id_orig_dest_node_length_link_capacity_link_param_travel_duration)
		
		
		#the dictionary: key= the id of the internal links,value is a list of [id origin node, id destination node]
		dic_id_internal_link_id_or_dest_node=Global_Functions_Network.function_reading_file_containing_nd_or_link_information(file_name_read=\
		"../"+self._name_data_folder+"/"+self._file_name_id_internal_link_id_orig_dest_node)
		
		
		#dictionary key=id phase ,value=rout prop
		#dict_mat_rp=Global_Functions_Network.fct_read_file_rout_prob(name_file_read=\
		#"../"+self._name_data_folder+"/"+self._module_name_import_file_names_model_network.val_name_file_mat_rp_id_phase_prob_dest_lk,\
		#nb_comment_lines=1)
		#print(dict_mat_rp)
		#import sys
		#sys.exit()
		
		
		#dictionary: key=id entry-internal link, value=[...,[ cum fct for rout prop, id dest lk],..]
		#value has as many elements as variations of the rp
		dict_mat_rp_cum_key_entry_intern_lk_value_list_cum_fct_val=Global_Functions_Network.\
		fct_reading_file_cum_rout_prob(name_file_read=\
		"../"+self._name_data_folder+"/"+self._module_name_import_file_names_model_network.val_name_file_mat_rp_cum,\
		nb_comment_lines=1)
		#print(dict_mat_rp_cum_key_entry_intern_lk_value_list_cum_fct_val[2350])
		#import sys
		#sys.exit()
		
		
		#li_dict_intersections_with_var_turn_ratios=[dict_intersections_with_var_turn_ratios,dict_inters_periods_with_var_turn_ratios]
		#dict_intersections_with_var_turn_ratios=dict, key=id node, value=dict, key=id period, value=dict, key=id phase, value=rout prob at related period
		#dict_inters_periods_with_var_turn_ratios=dict key=node id, value=dict, key=id period valeur:duration previous values rp
		li_dict_intersections_with_var_turn_ratios=Global_Functions_Network.\
		fct_read_file_fi_series_cum_val_varying_rp(name_file_to_read="../"+self._name_data_folder+"/"+\
		self._module_name_import_file_names_model_network.val_name_file_series_cum_values_varying_rout_prob,\
		nb_comment_lines=1)
		
		#dict key=node id, value=dict, key=id period valeur:duration previous values rp
		dict_di_intersections_with_var_turn_ratios=Global_Functions_Network.\
		fct_read_file_fi_series_varying_rout_prob(name_file_to_read="../"+self._name_data_folder+"/"+\
		self._module_name_import_file_names_model_network.val_name_file_series_varying_rout_prob,\
		nb_comment_lines=1)
		
		#dict, key=id node, value=dict, key=id phase, value =nb veh at the beg
		dict_di_init_state_ques=Global_Functions_Network.\
		fct_read_file_fi_init_state_que(name_file_to_read="../"+self._name_data_folder+"/"+\
		self._module_name_import_file_names_model_network.val_name_file_init_state_que,\
		nb_comment_lines=1)
		
		#dict, key=id node, value=dict, key=id phase, value=[...,[id phase, param a],...]
		dict_id_nd_interf_phases=Global_Functions_Network.\
		fct_read_file_fi_init_state_que(name_file_to_read="../"+self._name_data_folder+"/"+\
		self._module_name_import_file_names_model_network.name_file_phase_interference,nb_comment_lines=1)
		
		
				
		#if self._module_name_import_sim_user_data.val_type_veh_final_dest!=\
		#Cl_Decisions.TYPE_VEHICLE_FINAL_DESTINATION_AND_PATH["dynamically_defined"]:
		
			#dictionary, key=id entry link, value=[...[cum prob value of exit link, id of related exit link],...]
			#dict_mod_key_id_entry_lk_value_li_cum_prob_and_id_related_exit_lk=Global_Functions_Network.\
			#fct_reading_file_cum_rout_prob(name_file_read=\
			#"../"+self._name_data_folder+"/"+self._module_name_import_file_names_model_network.val_name_file_cum_mod,\
			#nb_comment_lines=val_nb_comment_lines_fi_mod)
			
		
		#else:
			#dictionary, key=id entry link, value=[...[cum prob value of exit link, id of related exit link],...]
			#dict_mod_key_id_entry_lk_value_li_cum_prob_and_id_related_exit_lk={}
					
		
			
		#li_di_signal_and_non_signal_intersections=[di id sign interes, value=1, di id non sign interes, value=0]
		li_di_signal_and_non_signal_intersections=Global_Functions_Network.\
		fct_read_fi_id_intersection_node_type_inters(name_file_to_read="../"+self._name_data_folder+"/"+\
		File_names_network_model.val_name_file_fi_id_node_type_node,nb_comment_lines=1)
		
		
		#dictionaire, key=node id, value=dict, key=id signalised intersection stage, value=list id simultanesously compatible phases (stages)
		dict_intersection_signalised_stages=Global_Functions_Network.\
		function_reading_file_intersection_stages(path_and_name_file_read="../"+self._name_data_folder+"/"+\
		File_names_network_model.val_name_file_stages_each_signalised_inters,nb_comment_lines=val_nb_comment_lines)
		
		#dictionaire, key=node id, value=dict, key=id non signalised intersection stage, value=list id simultanesously compatible phases (stages)
		dict_intersection_non_signalised_stages=Global_Functions_Network.\
		function_reading_file_intersection_stages(path_and_name_file_read="../"+self._name_data_folder+"/"+\
		File_names_network_model.val_name_file_stages_each_non_signalised_inters,nb_comment_lines=val_nb_comment_lines)
		
		#dictionaire, key=id entry link, value=type rout managem when mixed management
		dict_key_id_lk_value_type_rout_manag=Global_Functions_Network.\
		fct_read_file_fi_rout_type_entry_lk_mixed_manag(name_file_to_read="../"+self._name_data_folder+"/"+\
		File_names_network_model.val_name_file_rout_type_entry_lk_mixed_manag,nb_comment_lines=1)
		
		#if stoch demand
		if self._module_name_import_sim_user_data.val_indicating_stoch_demand==1:

			val_fct_calcul_dem_entry_link=Global_Functions.fct_calcul_demand_entry_link_stoch_case
			
		else:
			val_fct_calcul_dem_entry_link=Global_Functions.fct_calcul_demand_entry_link_deterministic_case
			
		#rep_di=[dict1,dict2]
		#dict1, key=id node, value=[control type, cotnrol categ (with/out sensor require), 1/0 for indicating if turn ratios will/not be estimated)
		#dict2=id node with estim turn ratios, value=1
		rep_di=self.fct_creat_di_key_id_node_value_type_and_ctrl_category()
		
		val_di_id_nd_type_and_ctrl_categ=rep_di[0]
		
		#dict, key=id nd with estim turn ratios, value=1
		val_di_id_nd_with_estimated_turn_ratios=rep_di[1]
		
		
		#list with all the control types currently employed in the network
		val_lis_types_ctrl=[]
		for m in val_di_id_nd_type_and_ctrl_categ:
			if val_di_id_nd_type_and_ctrl_categ[m][0] not in val_lis_types_ctrl:
				val_lis_types_ctrl.append(val_di_id_nd_type_and_ctrl_categ[m][0])

		

		#creation of the entry links, li_di_entry_lk=[dict_entry_link,val_que_id]
		li_di_entry_lk=self.funct_creating_dict_entry_links_to_network(\
		val_time_unit=self._module_name_import_sim_user_data.val_t_unit,\
		val_creat_new_demand=self._module_name_import_sim_user_data.creation_new_demand,\
		val_dict_id_node_id_entry_links_to_network=dic_id_node_id_entry_links_to_network,\
		val_dict_id_node_id_leaving_links_from_node=dic_id_node_id_leaving_links_from_node,\
		val_dict_id_all_phases_max_queue_size_et_sat_flow_queue_type=\
		dic_id_all_phases_max_queue_size_et_sat_flow_queue_type,\
		val_dict_id_all_network_link_id_orig_dest_node_length_link_capacity_link_param_travel_duration=\
		dic_id_all_network_link_id_orig_dest_node_length_link_capacity_link_param_travel_duration,\
		val_fct_calcul_demand_entry_link=val_fct_calcul_dem_entry_link,\
		val_di_parameters_fct_creating_demand_entry_link=dic_demand_param_entry_link,val_ind_queue=val_ind_que,\
		val_di_id_entry_link_demand_param_entry_link=dic_demand_param_entry_link,\
		val_dic_key_id_non_sign_inters_value_zero=li_di_signal_and_non_signal_intersections[1],\
		val_sim_duration=self._module_name_import_sim_user_data.t_simulation_duration,\
		val_round_prec=self._module_name_import_sim_user_data.val_precision_round_for_defin_time,\
		val_di_id_nd_with_estim_turn_ratios=val_di_id_nd_with_estimated_turn_ratios,\
		val_indicat_type_veh_final_dest=self._module_name_import_sim_user_data.val_type_veh_final_dest,\
		val_di_key_id_nd_val_dict_id_phase_val_li_interf_phase_and_param=dict_id_nd_interf_phases,\
		val_di_key_id_lk_value_type_rout_manag=dict_key_id_lk_value_type_rout_manag)
		
		
		#the dictionary of the entry links of the network 
		dict_entry_links=li_di_entry_lk[List_Explicit_Values.val_first_element_of_list]
		
	
		#creation of the dictionary of the exit links of the network
		#creation of the dictionary of the exit links of the network
		dict_exit_links=self.funct_creating_dict_exit_links_from_network(\
		val_dict_id_node_id_exit_links_from_network=dic_id_node_id_exit_links_to_network,\
		val_dict_id_node_id_entering_links_to_node=dic_id_node_id_entering_links_to_node,\
		val_dict_id_all_network_link_id_orig_dest_node_length_link=dic_id_all_network_link_id_orig_dest_node_length_link_capacity_link_param_travel_duration,\
		val_dict_id_all_phases_max_queue_size_sat_flow_queue_type=\
		dic_id_all_phases_max_queue_size_et_sat_flow_queue_type)
		
		#if we have more than one intersection nodes (this is if we have not an isolated intersection) 
		#we create the  dictionary of internal links
		if len(val_di_id_nd_type_and_ctrl_categ)>List_Explicit_Values.initialisation_value_to_one:
		
			#creation of the dictionary of the internal links of the network
			#this method returns a list [dictionary of the internal link, the index with the number for the queue id]
			li_di_internal_lk=self.funct_creating_dict_internal_links_to_network(\
			val_time_unit=self._module_name_import_sim_user_data.val_t_unit,\
			val_dict_id_internal_link_id_orig_dest_node=dic_id_internal_link_id_or_dest_node,\
			val_dict_id_node_id_entering_links_to_node=dic_id_node_id_entering_links_to_node,\
			val_dict_id_node_id_leaving_links_from_node=dic_id_node_id_leaving_links_from_node,\
			val_dict_id_all_phases_max_queue_size_et_sat_flow_queue_type=\
			dic_id_all_phases_max_queue_size_et_sat_flow_queue_type,\
			val_dict_id_all_network_link_id_orig_dest_node_length_link_capacity_link_param_travel_duration=\
			dic_id_all_network_link_id_orig_dest_node_length_link_capacity_link_param_travel_duration,\
			val_ind_queue=li_di_entry_lk[List_Explicit_Values.val_second_element_of_list],\
			val_indicat_type_veh_final_dest=self._module_name_import_sim_user_data.val_type_veh_final_dest,\
			val_di_id_nd_with_estim_turn_ratios=val_di_id_nd_with_estimated_turn_ratios,\
			val_di_key_id_nd_val_dict_id_phase_val_li_interf_phase_and_param=dict_id_nd_interf_phases)
			
			
		
			#the dictionary of the internal links of the network 
			dict_internal_links=li_di_internal_lk[List_Explicit_Values.val_first_element_of_list]
			
		
		#if we have an isolated intersection
		else:
			dict_internal_links={}
			
	
			
		#if stochastic travel times are considered
		if self._module_name_import_sim_user_data.val_type_trav_duration_managament==Cl_Decisions.TYPE_TRAVEL_DURAT_MANAG[2]:
		
			#print(self._name_data_folder)
			li_di_mu_sigma_shift=Global_Functions_Network.fct_creat_dict_param_stoch_travel_time_from_text_file_all_links(\
			v_name_file_to_read="../"+self._name_data_folder+"/"+self._file_name_id_all_network_link_id_orig_dest_node_length_link_capacity_link_param_travel_duration,\
			v_nb_comment_lines=0,v_sigma=0.974174,v_b=0.8)
		
		
			#the dictionary indicating the mean value of the lognormal distribution of each edge, when calcul the travel duration
			#key=id edge, value=[shift]
			#di_mean_val=Global_Functions.\
			#function_reading_file_containing_matrix_one_column_data(file_name_read="../../SMALL_DATA_INTERS_2/matrix_mu",type=float)
			#di_mean_val=Global_Functions.\
			#function_reading_file_containing_matrix_one_column_data(file_name_read="../"+self._name_data_folder\
			#+"/matrix_mu",type=float)
			di_mean_val=li_di_mu_sigma_shift[0]
			

		
			#the dictionary indicating the sigma (stan deviation) value of the shifted lognormal law of each edge, when calcul the travel duration
			#key=id edge, value=[shift]
			#di_sigma_val=Global_Functions.\
			#function_reading_file_containing_matrix_one_column_data(file_name_read="../../SMALL_DATA_INTERS_2/matrix_sigma",type=float)
			#di_sigma_val=Global_Functions.\
			#function_reading_file_containing_matrix_one_column_data(file_name_read="../"+self._name_data_folder\
			#+"/matrix_sigma",type=float)
			di_sigma_val=li_di_mu_sigma_shift[1]
		
		
			#the dictionary indicating the shift value of the lognormal law of each edge, when calcul the travel duration
			#key=id edge, value=[shift]
			#di_shift_val=Global_Functions.\
			#function_reading_file_containing_matrix_one_column_data(file_name_read="../../SMALL_DATA_INTERS_2/matrix_shift",type=float)
			#di_shift_val=Global_Functions.\
			#function_reading_file_containing_matrix_one_column_data(file_name_read="../"+self._name_data_folder\
			#+"/matrix_shift",type=float)
			di_shift_val=li_di_mu_sigma_shift[2]
		
		#if fixed mean travel times are considered
		else:
			di_mean_val={}
			di_sigma_val={}
			di_shift_val={}
			
		if li_dict_intersections_with_var_turn_ratios!=[]:
			#the network objet to return
			#we consider that the number of vehicles passed by each queue is -1 since this is the network for a new simulation
			#the network cotrol cycle object=None
			network=Cl_Network.Network(val_id_network=val_id_netw,\
			val_di_entry_links_to_network=dict_entry_links,val_di_exit_links_from_network=dict_exit_links,\
			val_di_internal_links_to_network=dict_internal_links,\
			val_di_id_intersections_with_estim_turn_ratios=val_di_id_nd_with_estimated_turn_ratios,\
			val_di_travel_durat_param_mu=di_mean_val,\
			val_di_travel_durat_param_sigma=di_sigma_val,\
			val_di_travel_durat_param_shift=di_shift_val,\
			val_li_employed_ctrl_types=val_lis_types_ctrl,\
			val_di_intersections_with_var_turn_ratios=dict_di_intersections_with_var_turn_ratios,\
			val_di_intersections_with_var_cum_turn_ratios=li_dict_intersections_with_var_turn_ratios[0],\
			val_di_inters_periods_with_var_turn_ratios=li_dict_intersections_with_var_turn_ratios[1],\
			val_di_intersections_with_non_empty_init_que_state=dict_di_init_state_ques)
		else:
			#the network objet to return
			#we consider that the number of vehicles passed by each queue is -1 since this is the network for a new simulation
			#the network cotrol cycle object=None
			network=Cl_Network.Network(val_id_network=val_id_netw,\
			val_di_entry_links_to_network=dict_entry_links,val_di_exit_links_from_network=dict_exit_links,\
			val_di_internal_links_to_network=dict_internal_links,\
			val_di_id_intersections_with_estim_turn_ratios=val_di_id_nd_with_estimated_turn_ratios,\
			val_di_travel_durat_param_mu=di_mean_val,\
			val_di_travel_durat_param_sigma=di_sigma_val,\
			val_di_travel_durat_param_shift=di_shift_val,\
			val_li_employed_ctrl_types=val_lis_types_ctrl,\
			val_di_intersections_with_non_empty_init_que_state=dict_di_init_state_ques)

		
		
		
		
		#we calculate the dict, key=id intersection, valeur=dict, key =id  pahse, valeur=rout prob
		di_id_nd_val_di_rout_prob=Global_Functions_Network.fct_reading_file_fi_mrp(\
		name_file_to_read="../"+self._name_data_folder+"/"+File_names_network_model.val_name_file_mat_rp_id_phase_prob_dest_lk,\
		nb_comment_lines=1,va_netw=network)
		
		#di with the cum rout prob of each intersection
		#val_di_cum_rp=dict_mat_rp_cum_key_entry_intern_lk_value_list_cum_fct_val,val_netw=network)
		di_cum_rp_per_inters=self.fct_creat_dict_cum_rp(val_di_cum_rp=dict_mat_rp_cum_key_entry_intern_lk_value_list_cum_fct_val,\
		val_netw=network)
		
		if self._module_name_import_sim_user_data.val_type_veh_final_dest!=\
		Cl_Decisions.TYPE_VEHICLE_FINAL_DESTINATION_AND_PATH["dynamically_defined"]:
		
			#dictionary, key=id entry link, value=[...[cum prob value of exit link, id of related exit link],...]
			dict_mod_key_id_entry_lk_value_li_cum_prob_and_id_related_exit_lk=Global_Functions_Network.\
			fct_reading_file_cum_rout_prob(name_file_read=\
			"../"+self._name_data_folder+"/"+self._module_name_import_file_names_model_network.val_name_file_cum_mod,\
			nb_comment_lines=val_nb_comment_lines_fi_mod)
			
			#di with the cum  mod per node
			dict_cum_mod_per_inters=self.fct_creat_dict_cum_rp(val_di_cum_rp=dict_mod_key_id_entry_lk_value_li_cum_prob_and_id_related_exit_lk,\
			val_netw=network)
			
		
		else:
			#dictionary, key=id entry link, value=[...[cum prob value of exit link, id of related exit link],...]
			dict_mod_key_id_entry_lk_value_li_cum_prob_and_id_related_exit_lk={}
			
			dict_cum_mod_per_inters={}

		
		
		#if (at least some) turn ratios will be estimated
		if val_di_id_nd_with_estimated_turn_ratios!={}:
				
			#dict, key=id intersection node, value= list with the parameters for the estim  of the turn ratios (param combinaison convexe, duration estim periode)
			di_id_nd_val_li_param_estim_turn_ratios=Global_Functions_Network.\
			fct_read_fi_id_node_estim_turn_ratio_param_dur_turn_ratios(name_file_to_read=\
			File_Sim_Name_Module_Files.val_name_folder_with_control_param_files+"/"+\
			File_Sim_Name_Module_Files.val_name_file_if_node_andparam_estim_turn_ratio_andduration_turn_ratio,\
			nb_comment_lines=1)	
			
			#we calculate the dict, key=id intersection, valeur=dict, key =id  pahse, valeur=init value for the estimated rout prob
			#di_id_nd_val_initial_value_estimated_di_rout_prob=Global_Functions_Network.fct_reading_file_fi_mrp(\
			#name_file_to_read="../"+self._name_data_folder+"/"+File_names_network_model.val_name_file_estim_mat_rp_id_phase_prob_dest_lk,\
			#nb_comment_lines=1,va_netw=network)
			
			#we calculate the dict, key=id intersection, valeur=dict, key =id  pahse, valeur=initial value for estimated rout prob
			di_id_nd_val_di_initial_value_estim_rout_prob=Global_Functions_Network.fct_reading_file_fi_mrp(\
			name_file_to_read=File_Sim_Name_Module_Files.val_name_folder_with_control_param_files+"/"+\
			File_Sim_Name_Module_Files.val_name_file_estim_mat_rp_id_phase_prob_dest_lk,\
			nb_comment_lines=1,va_netw=network)
			
			
			
						
		#if no turn ratio will be estimated
		else:
			di_id_nd_val_li_param_estim_turn_ratios={}
			di_id_nd_val_di_initial_value_estim_rout_prob={}
			
		
				
		if self._module_name_import_sim_user_data.val_type_veh_final_dest==\
		Cl_Decisions.TYPE_VEHICLE_FINAL_DESTINATION_AND_PATH["dynamically_defined"]:
			val_exist_od_matr=0
		else:
			val_exist_od_matr=1
		
		#print("di_id_nd_val_di_rout_prob",di_id_nd_val_di_rout_prob.keys())
		#import sys
		#sys.exit()
		#creation of the dictionary of the intersections
		dict_intersections=self.funct_creating_dict_intersections(\
		val_exist_od_mat=val_exist_od_matr,\
		dict_id_node_id_entering_links_to_node=dic_id_node_id_entering_links_to_node,\
		dict_id_node_id_leaving_links_from_node=dic_id_node_id_leaving_links_from_node,\
		val_li_types_ctrl=val_lis_types_ctrl,\
		di_id_nd_type_and_ctrl_categ=val_di_id_nd_type_and_ctrl_categ,\
		di_id_nd_val_dic_rp=di_id_nd_val_di_rout_prob,\
		di_id_nd_val_di_cum_rp=di_cum_rp_per_inters,\
		dict_current_cum_mod=dict_cum_mod_per_inters,\
		dict_id_node_li_si_stages=dict_intersection_signalised_stages,\
		dict_id_node_li_nsi_stages=dict_intersection_non_signalised_stages,\
		di_id_sign_inters_nd_value_one=li_di_signal_and_non_signal_intersections[0],\
		di_id_non_sign_inters_nd_value_zero=li_di_signal_and_non_signal_intersections[1],\
		v_nb_comment_lines_ft=val_nb_comment_lines_ft,v_nb_comment_lines_mp=val_nb_comment_lines_mp,\
		v_nb_comment_lines_ft_off=val_nb_comment_lines_ft_off,v_nb_comment_lines_fa=val_nb_comment_lines_fa,\
		v_nb_comment_lines_fa_max_green=val_nb_comment_lines_fa_max_green,\
		dict_id_nd_param_turn_ratio_estim=di_id_nd_val_li_param_estim_turn_ratios,\
		val_dict_estim_rp=di_id_nd_val_di_initial_value_estim_rout_prob,val_di_id_link_val_link=network.get_di_all_links())
		
		
		
		network.set_di_intersections(dict_intersections)

		
		#if the vehicle final destination will be dynamically computed
		if self._module_name_import_sim_user_data.val_type_veh_final_dest ==\
		Cl_Decisions.TYPE_VEHICLE_FINAL_DESTINATION_AND_PATH["dynamically_defined"]:
			
			#if there exist intersections with estimated turn ratios
			if val_di_id_nd_with_estimated_turn_ratios!={}:
			
				# we indicate the nodes with entry links
				network.set_dict_id_nds_with_entry_links(n_v=dic_id_node_id_entry_links_to_network)
				
				#we indicate the internal links for each intersection
				#self.fct_creat_di_internal_links_and_update_intersection(val_di_key_id_nd_value_li_id_entry_lks=dic_id_node_id_entry_links_to_network,\
				#val_network=network)
				
				#we indicate the network  which nodes will have estimated turn ratios so as to creatthe evn veh_flow_change_events
				#li_1=list(val_di_id_nd_with_estimated_turn_ratios.keys())
				#network.set_li_id_intersections_with_estim_turn_ratios(n_v=li_1)
				
				#creat of the diction witht he nb of vehicles joining each link as well as their origin link
				self.fct_creat_di_id_ar_lk_val_nb_ar_veh_for_internal_exit_lks(val_netw=network,\
				val_di_nd_with_turn_ratios_estim=val_di_id_nd_with_estimated_turn_ratios)
		
		#if the vehicle final destination is computed by OD matrices
		elif self._module_name_import_sim_user_data.val_type_veh_final_dest !=\
		Cl_Decisions.TYPE_VEHICLE_FINAL_DESTINATION_AND_PATH["dynamically_defined"]:
		
			self.fct_creat_dict_cum_mod_without_varying_values_and_update_intersections(\
			val_di_cum_mod=dict_mod_key_id_entry_lk_value_li_cum_prob_and_id_related_exit_lk,val_netw=network)
		
			#if there exist intersections with estimated turn ratios
			if val_di_id_nd_with_estimated_turn_ratios!={}:
				
				#li_1=list(val_di_id_nd_with_estimated_turn_ratios.keys())
				#we indicate the network  which nodes will have estimated turn ratios so as to creatthe evn veh_flow_change_events
				#network.set_li_id_intersections_with_estim_turn_ratios(n_v=li_1)
				
				# we indicate the nodes with entry links
				network.set_dict_id_nds_with_entry_links(n_v=dic_id_node_id_entry_links_to_network)
				
				
				#creat of the diction witht he nb of vehicles joining each link as well as their origin link
				self.fct_creat_di_id_ar_lk_val_nb_ar_veh_for_all_lks(val_netw=network,\
				val_di_nd_with_turn_ratios_estim=val_di_id_nd_with_estimated_turn_ratios)
		
		#If we have ODs and given paths
		if self._module_name_import_sim_user_data.val_type_veh_final_dest==\
		Cl_Decisions.TYPE_VEHICLE_FINAL_DESTINATION_AND_PATH["initially_defined_and_path_given"] or\
		self._module_name_import_sim_user_data.val_type_veh_final_dest==\
		Cl_Decisions.TYPE_VEHICLE_FINAL_DESTINATION_AND_PATH["mixed_dyndefined_or_odwithgiven_path"]:
		
			#dict, key=id inters node, value=dict, key=(id entry link, id exit link) value=[..., id link to follow,...]
			di_unique_paths_all_inters=Global_Functions_Network.fct_creat_dict_unique_paths(\
			val_name_file_to_read="../"+self._name_data_folder+"/"+File_names_network_model.val_name_file_id_entry_exit_link_path,\
			val_nb_comment_lines=1,val_netw=network)
		
			#we attribute eachpath dictionary to each  intersection 
			self.fct_update_path_dict_each_related_intersection(di_paths_all_intersections=di_unique_paths_all_inters,val_network=network)
				
		return network
		

				
			
			



		
		

		










































