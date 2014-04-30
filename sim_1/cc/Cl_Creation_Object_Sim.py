#import random
import Cl_Creation_Network
import Cl_Simulation_System
import Cl_Simulation
import Cl_Event
import Cl_Control_Actuate
import Global_Functions
import Cl_Global_Functions
import List_Explicit_Values
import Cl_Creation_Network

class Creation_Object_Sim:
	"""class constructing the the simulation object to be implemented """
	
	def __init__(self,val_t_start_sim=-1,val_t_duration_sim=-1,\
	val_dict_param_fcts_event_treat={},val_heap_ev=[],val_new_vehicle_id=0,\
	val_index_vehicle_id_in_veh_ap_event=0,val_dict_information_vehicle_previous_sim={}):
		
		
		#the time at which the sim will start
		self._t_start_sim=val_t_start_sim
		
		#the sim duration
		self._t_duration_sim=val_t_duration_sim
		
		#the dictionary with the list of parameters  for each event treatment function
		self._dict_param_fcts_event_treat=val_dict_param_fcts_event_treat
		
		
		#the event list
		self._heap_ev=val_heap_ev
		
		#the vehicle id index (in the param list when of the event  vehicle appear)
		self._new_vehicle_id=val_new_vehicle_id
		
		#the index of the argument defining the vehicle id on the vehicle appearance event
		self._index_vehicle_id_in_veh_ap_event=val_index_vehicle_id_in_veh_ap_event
		
		#the dictionairy with the vehicle information of a previously made sim
		self._dict_information_vehicle_previous_sim=val_dict_information_vehicle_previous_sim
		
		
#*****************************************************************************************************************************************************************************************
	#method returning the time at which the sim will start
	def get_t_start_sim(self):
		return self._t_start_sim

#*****************************************************************************************************************************************************************************************
	#method returning the sim duration
	def get_t_duration_sim(self):
		return self._t_duration_sim
	
	
#*****************************************************************************************************************************************************************************************
	#method returning the dictionary with the list of parameters  for each event treatment function
	def get_dict_param_fcts_event_treat(self):
		return self._dict_param_fcts_event_treat

#*****************************************************************************************************************************************************************************************
	#method returning the event list
	def get_heap_ev(self):
		return self._heap_ev

#*****************************************************************************************************************************************************************************************
	#method returning the  new vehicle id 
	def get_new_vehicle_id(self):
		return self._new_vehicle_id
#*****************************************************************************************************************************************************************************************
	#method returning the index of the argument defining the vehicle id on the vehicle appearance event
	def get_index_vehicle_id_in_veh_ap_event(self):
		return self._index_vehicle_id_in_veh_ap_event

#*****************************************************************************************************************************************************************************************
	#method returning the dictionaire with the vehicle information of a previously made sim
	def get_dict_information_vehicle_previous_sim(self):
		return self._dict_information_vehicle_previous_sim
#*****************************************************************************************************************************************************************************************
	#method  modifying the time at which the sim will start
	def set_t_start_sim(self,n_v):
		self._t_start_sim=n_v

#*****************************************************************************************************************************************************************************************
	#method  modifying the sim duration
	def set_t_duration_sim(self,n_v):
		self._t_duration_sim=n_v
	
	
#*****************************************************************************************************************************************************************************************
	#method  modifying the dictionary with the list of parameters  for each event treatment function
	def set_dict_param_fcts_event_treat(self,n_n_v):
		self._dict_param_fcts_event_treat=n_v

#*****************************************************************************************************************************************************************************************
	#method  modifying the event list
	def set_heap_ev(self,n_v):
		self._heap_ev=n_v

#*****************************************************************************************************************************************************************************************
	#method  modifying the vehicle id index
	def set_new_vehicle_id(self,n_v):
		self._new_vehicle_id=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the index of the argument defining the vehicle id on the vehicle appearance event
	def set_index_vehicle_id_in_veh_ap_event(self,n_v):
		self._index_vehicle_id_in_veh_ap_event=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the dictionaire with the vehicle information of a previously made sim
	def set_dict_information_vehicle_previous_sim(self,n_v):
		self._dict_information_vehicle_previous_sim=n_v
#*****************************************************************************************************************************************************************************************
	
	
	#function creating a simulation object
	#val_fi_name_user_data=Dsu
	def fct_creation_object_sim(self,val_fi_name_user_data,val_ind_queue=1):
	
		
		#a creation_network object
		creat_network=Cl_Creation_Network.Creation_Network(val_file_name_user_data=val_fi_name_user_data)
		#creation of the network
		network=creat_network.function_creation_network(val_ind_que=val_ind_queue)
		
		#creation of a simulation system object
		sim_sys= Cl_Simulation_System.Simulation_System(val_network=network,\
		val_dict_information_veh_previous_sim=self._dict_information_vehicle_previous_sim)
		
		
		#creation of the simulation object
		simul_obj= Cl_Simulation.Simulation(val_simul_system=sim_sys,val_t_start_simulation=self._t_start_sim,\
		val_t_duration_simulation=self._t_duration_sim,val_dict_parameters_fcts_event_treat=self._dict_param_fcts_event_treat,\
		val_number_event_types=len(Cl_Event.TYPE_EV),val_heap_even=self._heap_ev,val_new_veh_id=self._new_vehicle_id,\
		val_index_veh_id_in_veh_ap_event=self._index_vehicle_id_in_veh_ap_event)
		
		return simul_obj
		
#*****************************************************************************************************************************************************************************************		
	#function creating a simulation object from a previous ended simulation
	def fct_recreation_object_sim_prev_sim(self,val_fi_record_network_prev_sim,val_fi_record_ev_pile_prev_sim,\
	val_fi_record_next_veh_id_prev_sim,val_name_data_folder, val_file_name_demand_param_entry_link,\
	val_name_file_user_data,val_nb_comment_lines_ft,val_nb_comment_lines_ft_off,\
	val_nb_comment_lines_mp,val_nb_comment_lines_fa,\
	val_nb_comment_lines_fa_max_green):
	
		
		
		
		#we retrieve the network of the sim we wish to continue, the event list as well and the veh id
		
		a_1=Cl_Global_Functions.Global_Functions()
		
		netw_network=a_1.retrieve_object_previous_sim(file_saved_object=val_fi_record_network_prev_sim)
		
		#creation of a  creation_network object
		creat_netw_obj=Cl_Creation_Network.Creation_Network(val_file_name_user_data=val_name_file_user_data,\
		val_name_file_containing_file_names_model_network="File_names_network_model")
		
		#val_di_id_nd_type_and_ctrl_categ=[dict1, dict2]
		#dict1, key=id node, value=[ctrl type, ctrl categ, indicator for estimated or not turn ratios]
		val_di_id_nd_type_and_ctrl_categ=creat_netw_obj.fct_creat_di_key_id_node_value_type_and_ctrl_category()
		
		val_lis_types_ctrl=[]
		for p in val_di_id_nd_type_and_ctrl_categ[0]:
			if val_di_id_nd_type_and_ctrl_categ[0][p][0] not in val_lis_types_ctrl:
				val_lis_types_ctrl.append(val_di_id_nd_type_and_ctrl_categ[0][p][0])
		
		#creation of the dict with the control param for each intersection
		#dict, key=ctrl type, value=dict,
		#key=id node, value=li parameters realted ctrl
		val_di_ctrl_param_inters=creat_netw_obj.fct_creat_dict_ctrl_param_per_inters(\
		li_types_ctrl=val_lis_types_ctrl,\
		va_nb_comment_lines_ft=val_nb_comment_lines_ft,\
		va_nb_comment_lines_mp=val_nb_comment_lines_mp,\
		va_nb_comment_lines_ft_off=val_nb_comment_lines_ft_off,\
		va_nb_comment_lines_fa=val_nb_comment_lines_fa,\
		va_nb_comment_lines_fa_max_green=val_nb_comment_lines_fa_max_green)
		
		for m in netw_network.get_di_intersections():
			#creation of a control actuate object
			ctr_act_obj=creat_netw_obj.fct_creat_inters_control_actuat_obj(v_type_control=val_di_id_nd_type_and_ctrl_categ[0][m][0],\
			v_control_categ=val_di_id_nd_type_and_ctrl_categ[0][m][1],v_li_param_inters_ctrl=\
			val_di_ctrl_param_inters[val_di_id_nd_type_and_ctrl_categ[0][m][0]][m])
			#,\
			#val_turn_ratios_estimated=val_di_id_nd_type_and_ctrl_categ[m][2])
			
			netw_network.get_di_intersections()[m].set_ctrl_actuate_obj(ctr_act_obj)
			
			#we indicate the network if the turn ratios will be or not estimted during this run 
			netw_network.get_di_intersections()[m].set_estimated_turn_ratios(val_di_id_nd_type_and_ctrl_categ[0][m][2])
		
		#we indicate the network the new types of the employed ctrl
		netw_network.set_li_employed_ctrl_types(val_lis_types_ctrl)
		
		#creation of an control actuate object
		#control_act_obj=creat_netw_obj.fct_creat_control_actuat_obj(\
		#v_nb_comment_lines_ft=val_nb_comment_lines_ft,\
		#v_nb_comment_lines_mp=val_nb_comment_lines_mp,\
		#v_nb_comment_lines_psd=val_nb_comment_lines_psd,\
		#v_nb_comment_lines_ft_off=val_nb_comment_lines_ft_off,\
		#v_nb_comment_lines_fa=val_nb_comment_lines_fa,\
		#v_nb_comment_lines_fa_max_green=val_nb_comment_lines_fa_max_green)
		
		
		#netw_network.set_control_actuate_obj(control_act_obj)
		
		
		#we recreate the dictionary: key=the id of the entry link, value the list of parameters for calculating the demand of the entry link
		#so if the demand has changed to take into consideration the new 
		dic_demand_param_entry_link=Global_Functions.function_reading_file_containing_nd_or_link_information(file_name_read=\
		val_name_data_folder+"/"+val_file_name_demand_param_entry_link,type=float)
		
		
		
		#for each entry link we associate the list with the demand parameters
		for i in dic_demand_param_entry_link:
			netw_network.get_di_entry_links_to_network()[i].set_lis_parameters_fct_creating_demand_entry_link(\
			dic_demand_param_entry_link[i])
			
			
			
		
		
		#retrieve_network_obj_prevous_sim(file_saved_network=val_file_saved_network_previous_sim)
		
		new_event_list=a_1.retrieve_object_previous_sim(file_saved_object=val_fi_record_ev_pile_prev_sim)
		
		#retrieve_event_list_previous_sim(file_saved_pile_event=val_file_saved_event_pile_prev_sim)
		
		next_veh_id=a_1.retrieve_object_previous_sim(file_saved_object=val_fi_record_next_veh_id_prev_sim)
		
		#creation of a simulation system object
		sim_sys= Cl_Simulation_System.Simulation_System(val_network=netw_network,\
		val_dict_information_veh_previous_sim=self._dict_information_vehicle_previous_sim)
	
		
		
		#creation of the simulation object
		simul_obj= Cl_Simulation.Simulation(val_simul_system=sim_sys,\
		val_t_start_simulation=new_event_list[List_Explicit_Values.val_first_element_of_list].get_event_time(),\
		val_t_duration_simulation=self._t_duration_sim,val_dict_parameters_fcts_event_treat=self._dict_param_fcts_event_treat,\
		val_number_event_types=len(Cl_Event.TYPE_EV),val_heap_even=new_event_list,val_new_veh_id=next_veh_id,\
		val_index_veh_id_in_veh_ap_event=self._index_vehicle_id_in_veh_ap_event)
		
		
		
		return simul_obj

#*****************************************************************************************************************************************************************************************		
		
	#function  reconstructing the event heap from a previously ended simulation
	def fct_recreation_event_pile_sim_prev_sim(self,val_fi_record_network_prev_sim,val_fi_record_ev_pile_prev_sim):
	
		
		
		
		#we retrieve the network of the sim we wish to continue, the event list as well and the veh id
		
		a_1=Cl_Global_Functions.Global_Functions()
		
		netw_network=a_1.retrieve_object_previous_sim(file_saved_object=val_fi_record_network_prev_sim)
		
				
		
		#retrieve_network_obj_prevous_sim(file_saved_network=val_file_saved_network_previous_sim)
		
		new_event_list=a_1.retrieve_object_previous_sim(file_saved_object=val_fi_record_ev_pile_prev_sim)
		
		
		
		return new_event_list



#*****************************************************************************************************************************************************************************************


