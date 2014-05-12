import sys
import csv
import Cl_Record_Database
import shutil
import List_Explicit_Values
import Cl_Event
import Cl_Control_Actuate
import Cl_Decisions
import Cl_Network_Link




class Treatment_Sim_Res:

	def __init__(self,val_db_file_sim_res_to_treat=None,val_veh_file_to_write_res=None,val_veh_final_dest_dynam_constructed=None):
		
		#the file (already placed in the corresponding directory) where the recorded sim database
		#this file is created by the Cl_Creation_and_Treat_Sim_Files
		self._db_file_sim_res_to_treat=val_db_file_sim_res_to_treat
		
		#the file (already placed in the corresponding directory) where the veh results will be written
		#this file is created by the Cl_Creation_and_Treat_Sim_Files
		self._veh_file_to_write_res=val_veh_file_to_write_res
		
		#variable indicating whether the veh final destination will be defined by its appear (valeur differente de 1) or
		# will be dynamically constructed (valeur=1)
		self._veh_final_dest_dynam_constructed=val_veh_final_dest_dynam_constructed
	
	
		#the dictionary of which the key is the event type and the value is a list of database record objects
		self._dict_db_record_obj=self.fct_creation_dictionary_from_the_db_file()
		
		#the dictionary with the vehicle information
		#the key is the vehicle id
		#the value is [ ...,[ev_time,ev_type,id_veh,current_queue_location,t_exit_from_network   ] ,...     ]
		self._dict_veh_information=self.fct_dict_information_vehicles_sim()
		#print(self._dict_veh_information[1])
		#import sys
		#sys.exit()
		
		
			
				
#*****************************************************************************************************************************************************************************************
	#method returning the file (already placed in the corresponding directory) where the recorded sim database
	def get_db_file_sim_res_to_treat(self):
		return self._db_file_sim_res_to_treat

#*****************************************************************************************************************************************************************************************
	#method returning the file (already placed in the corresponding directory) where the veh results will be written
	def get_veh_file_to_write_res(self):
		return self._veh_file_to_write_res
#*****************************************************************************************************************************************************************************************
	#method returning the dictionary of which the key is the event type and the value is a list of database record objects
	def get_dict_db_record_obj(self):
		return self._dict_db_record_obj

#*****************************************************************************************************************************************************************************************
	#method returning the variable indicating whether the veh final destination will be defined by its appear (valeur differente de 1) or
	# will be dynamically constructed (valeur=1)
	def get_veh_final_dest_dynam_constructed(self):
		return self._veh_final_dest_dynam_constructed
#*****************************************************************************************************************************************************************************************

	#method returning the dictionary with the vehicle information
	def get_dict_veh_information(self):
		return self._dict_veh_information

#*****************************************************************************************************************************************************************************************
	

	#method modifying the file (already placed in the corresponding directory) where the recorded sim database
	def set_db_file_sim_res_to_treat(self,n_v):
		self._db_file_sim_res_to_treat=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the file (already placed in the corresponding directory) where the veh results will be written
	def set_veh_file_to_write_res(self,n_v):
		self._veh_file_to_write_res=n_v
#*****************************************************************************************************************************************************************************************
	#method  modifying the dictionary of which the key is the event type and the value is a list of database record objects
	def set_dict_db_record_obj(self,n_v):
		self._dict_db_record_obj=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying  the variable indicating whether the veh final destination will be defined by its appear (valeur differente de 1) or
	# will be dynamically constructed (valeur=1)
	def set_veh_final_dest_dynam_constructed(self,n_v):
		self._veh_final_dest_dynam_constructed=n_v
#*****************************************************************************************************************************************************************************************

	#method  modifying the dictionary with the vehicle information
	def set_dict_veh_information(self,n_v):
		self._dict_veh_information=n_v

#*****************************************************************************************************************************************************************************************
	

	#method creating a dictionary from the db file created by the simulation
	#the key of the dictionaty is the id of the phase, 
	#the value is a list of record database objects of event type 
	#dict[i]= [...,[record_database_obj_of_type_i_1,record_database_obj_of_type_i_2, ...  ]  ...]
	def fct_creation_dictionary_key_movem_from_the_db_file(self):
		
		file=open(self._db_file_sim_res_to_treat,"r")
		fc=csv.reader(file,delimiter=',',quotechar='"')
		
		dict={}
		
		for i in fc:
			
			#print("HEREE",(i[15]))
			#print("HERE",i[0],"NEXT",i[1],"NEXT",i[2],"NEXT",i[3],"NEXT",i[4])
			
			#we write the 30 first attributs of a record objet (see Cl_Record_Database)
			
			record_db_obj=Cl_Record_Database.Record_Database(\
			val_ev_time=eval(i[0]),\
			val_ev_type=eval(i[1]),\
			val_t_start_t_duration_sequence_next_inters_control_mat=eval(i[4]),\
			val_dt_min_margin_for_calcul_next_inters_control=eval(i[5]),\
			val_t_start_current_inters_control=eval(i[6]),\
			val_duration_current_inters_control=eval(i[7]),\
			val_current_inters_control_matrix=eval(i[8]),\
			val_current_inters_matrix_with_the_associated_link_of_phase=eval(i[9]),
			val_duration_current_cycle=eval(i[10]),\
			val_vehicle_id=int(i[11]),\
			val_time_veh_appearance_in_network=eval(i[12]),\
			val_id_veh_entry_link=eval(i[13]),\
			val_id_current_link_veh_location=eval(i[14]),\
			val_time_veh_arrival_at_current_link=eval(i[15]), \
			val_time_veh_start_departure_from_current_link=eval(i[16]),\
			val_time_veh_departure_from_current_link=eval(i[17]),
			val_veh_current_queue_location=eval(i[18]),\
			val_time_veh_arrival_at_current_queue=eval(i[19]),\
			val_time_veh_start_departure_from_current_queue=eval(i[20]),\
			val_time_veh_departure_from_current_queue=eval(i[21]),\
			val_veh_id_destination_link=eval(i[22]),\
			val_time_veh_exit_from_network=eval(i[23]),\
			val_id_event_link=eval(i[24]),\
			val_veh_can_leave_now=eval(i[25]),\
			val_t_vehicle_arrival_at_next_link_or_queue=eval(i[26]),\
			val_current_achieved_queue_service_rate_including_current_vehicle=eval(i[27]),\
			val_current_queue_service_rate=eval(i[28]),\
			val_li_id_vehicles_in_queue=eval(i[29]),\
			val_type_control=eval(i[37]),\
			val_t_end_current_intersection_control=eval(i[42]),\
			val_id_actuated_stage=eval(i[43]),\
			val_current_inters_cum_turn_ratio_val=eval(i[44]),\
			val_veh_added_when_que_state_update=eval(i[45]),\
			val_veh_suppressed_when_que_state_update=eval(i[46]))
			
			
			#val_total_veh_number_passed_by_queue_including_current_veh=eval(i[30]),\
			#val_nb_veh_appear_entry_link=eval(i[31]),\
			#val_nb_depart_veh_within_dep_ev=eval(i[32]))
			
			
			
			#if the event of type i is not in the dictionary, we create this key and its  value 
			#print("HERE",record_db_obj.get_veh_current_queue_location())
			#if record_db_obj.get_veh_current_queue_location() not in dict.keys():
			
			#if it is an event related to a vehicle
			if record_db_obj.get_veh_current_queue_location()!=-1:
				#print("record_db_obj.get_veh_current_queue_location()[0]",record_db_obj.get_veh_current_queue_location())
				#print("Veh id: ",record_db_obj.get_vehicle_id())
				#print("Even type: ",record_db_obj.get_ev_type())
				#print("Even time: ",record_db_obj.get_ev_time())
				#print("record_db_obj.get_veh_current_queue_location()[1",record_db_obj.get_veh_current_queue_location()[1])
				#if the queue (movement) is not in the dictionary, we create it
				if (record_db_obj.get_veh_current_queue_location()[0],record_db_obj.get_veh_current_queue_location()[1]) not in dict.keys():
					#print("HERE2")
					dict[(record_db_obj.get_veh_current_queue_location()[0],record_db_obj.get_veh_current_queue_location()[1])]=[record_db_obj]
				#if the movement (key of the dictionary) already exists, we simply add the value (record database obj) in the list
				else:
				
					dict[(record_db_obj.get_veh_current_queue_location()[0],record_db_obj.get_veh_current_queue_location()[1])].append(record_db_obj)
			#else:
				#print("type event:",record_db_obj.get_ev_type())
		file.close()
		
		
		return dict
				


#*****************************************************************************************************************************************************************************************
	#method creating a dictionary from the db file created by the simulation
	#the key of the dictionary is the event type, 
	#the value is a list of record database objects of event type 
	#dict[i]= [...,[record_database_obj_of_type_i_1,record_database_obj_of_type_i_2, ...  ]  ...]
	def fct_creation_dictionary_from_the_db_file(self):
		
		file=open(self._db_file_sim_res_to_treat,"r",encoding="utf8")
		fc=csv.reader(file,delimiter=',',quotechar='"')
		
		dict={}
		
		for i in fc:
			
			#print("HEREE",(i[15]))
			#if eval(i[1])==1:
				#print("HERE",i[0],"NEXT",i[1],"NEXT",i[2],"NEXT",i[3],"NEXT",i[4])
				#print(i)
				#import sys
				#sys.exit()
				
			
			
			
			
			record_db_obj=Cl_Record_Database.Record_Database(\
			val_ev_time=eval(i[0]),\
			val_ev_type=eval(i[1]),\
			val_id_inters_node=eval(i[2]),\
			val_t_start_t_duration_sequence_next_inters_control_mat=eval(i[4]),\
			val_dt_min_margin_for_calcul_next_inters_control=eval(i[5]),\
			val_t_start_current_inters_control=eval(i[6]),\
			val_duration_current_inters_control=eval(i[7]),\
			val_current_inters_control_matrix=eval(i[8]),\
			val_current_inters_matrix_with_the_associated_link_of_phase=eval(i[9]),
			val_duration_current_cycle=eval(i[10]),\
			val_vehicle_id=int(i[11]),\
			val_time_veh_appearance_in_network=eval(i[12]),\
			val_id_veh_entry_link=eval(i[13]),\
			val_id_current_link_veh_location=eval(i[14]),\
			val_time_veh_arrival_at_current_link=eval(i[15]), \
			val_time_veh_start_departure_from_current_link=eval(i[16]),\
			val_time_veh_departure_from_current_link=eval(i[17]),
			val_veh_current_queue_location=eval(i[18]),\
			val_time_veh_arrival_at_current_queue=eval(i[19]),\
			val_time_veh_start_departure_from_current_queue=eval(i[20]),\
			val_time_veh_departure_from_current_queue=eval(i[21]),\
			val_veh_id_destination_link=eval(i[22]),\
			val_time_veh_exit_from_network=eval(i[23]),\
			val_id_event_link=eval(i[24]),\
			val_veh_can_leave_now=eval(i[25]),\
			val_t_vehicle_arrival_at_next_link_or_queue=eval(i[26]),\
			val_current_achieved_queue_service_rate_including_current_vehicle=eval(i[27]),\
			val_current_queue_service_rate=eval(i[28]),\
			val_li_id_vehicles_in_queue=eval(i[29]),\
			val_nb_veh_in_ar_lk=eval(i[34]),\
			val_nb_veh_in_dep_lk=eval(i[35]),\
			val_id_veh_final_dest_exit_lk=eval(i[36]),\
			val_type_control=eval(i[37]),\
			val_t_end_current_intersection_control=eval(i[42]),\
			val_id_actuated_stage=eval(i[43]),\
			val_current_inters_cum_turn_ratio_val=eval(i[44]),\
			val_veh_added_when_que_state_update=eval(i[45]),\
			val_veh_suppressed_when_que_state_update=eval(i[46]))
			#,val_t_end_current_intersection_control=eval(i[42]))	
			
			#record_db_obj=Cl_Record_Database.Record_Database(\
			#val_ev_time=eval(i[0]),\
			#val_ev_type=eval(i[1]),\
			#val_id_inters_node=eval(i[2]),\
			#val_type_inters_node=eval(i[3]),\
			#val_t_start_t_duration_sequence_next_inters_control_mat=eval(i[4]),\
			#val_dt_min_margin_for_calcul_next_inters_control=eval(i[5]),\
			#val_t_start_current_inters_control=eval(i[6]),\
			#val_duration_current_inters_control=eval(i[7]),\
			#val_current_inters_control_matrix=eval(i[8]),\
			#val_current_inters_matrix_with_the_associated_link_of_phase=eval(i[8]),\
			#val_duration_current_cycle=eval(i[10]),\
			#val_vehicle_id=int(i[11]),\
			#val_time_veh_appearance_in_network=eval(i[12]),\
			#val_id_veh_entry_link=eval(i[13]),\
			#val_id_current_link_veh_location=eval(i[14]),\
			#val_time_veh_arrival_at_current_link=eval(i[15]), \
			#val_time_veh_start_departure_from_current_link=eval(i[16]),\
			#val_time_veh_departure_from_current_link=eval(i[17]),
			#val_veh_current_queue_location=eval(i[18]),\
			#val_time_veh_arrival_at_current_queue=eval(i[19]),\
			#val_time_veh_start_departure_from_current_queue=eval(i[20]),\
			#val_time_veh_departure_from_current_queue=eval(i[21]),\
			#val_veh_id_destination_link=eval(i[22]),\
			#val_time_veh_exit_from_network=eval(i[23]),\
			#val_id_event_link=eval(i[24]),\
			#val_veh_can_leave_now=eval(i[25]),\
			#val_t_vehicle_arrival_at_next_link_or_queue=eval(i[26]),\
			#val_current_achieved_queue_service_rate_including_current_vehicle=eval(i[27]),\
			#val_current_queue_service_rate=eval(i[28]),\
			#val_li_id_vehicles_in_queue=eval(i[29]))
			
			
			#record_db_obj=Cl_Record_Database.Record_Database(val_ev_time=eval(i[0]),val_ev_type=eval(i[1]),\
			#val_li_inform_sequence_netw_control_matr_cycle_t_start_t_duration=eval(i[2]),\
			#val_dt_min_margin_for_calcul_next_netw_control_cycle=eval(i[3]),\
			#val_t_start_current_control=eval(i[4]),\
			#val_duration_current_control=eval(i[5]),\
			#val_current_network_control_matrix=eval(i[6]),\
			#val_current_network_control_matrix_with_the_associated_link_of_phase=eval(i[7]),\
			#val_duration_current_cycle=eval(i[8]),\
			#val_vehicle_id=int(i[9]),val_time_veh_appearance_in_network=eval(i[10]),\
			#val_id_veh_entry_link=eval(i[11]),\
			#val_id_current_link_veh_location=eval(i[12]),\
			#val_time_veh_arrival_at_current_link=eval(i[13]), \
			#val_time_veh_departure_from_current_link=eval(i[14]),\
			#val_veh_current_queue_location=eval(i[15]),\
			#val_time_veh_arrival_at_current_queue=eval(i[16]),\
			#val_time_veh_departure_from_current_queue=eval(i[17]),\
			#val_veh_id_destination_link=eval(i[15][1]),\
			#val_time_veh_exit_from_network=eval(i[18]),\
			#val_id_event_link=eval(i[19]),\
			#val_type_link_event=eval(i[20]),\
			#val_veh_can_leave_now=eval(i[21]),\
			#val_t_vehicle_arrival_at_next_link_or_queue=eval(i[22]),\
			#val_current_achieved_queue_service_rate_including_current_vehicle=eval(i[23]),\
			#val_current_queue_service_rate=eval(i[24]),\
			#val_li_id_vehicles_in_queue=eval(i[25]),\
			#val_total_veh_number_passed_by_queue_including_current_veh=eval(i[26]))
			#,\
			#val_li_network_control_matrices_for_next_cycle=int(i[27]))
			
			
			#if the event of type i is not in the dictionary, we create this key and its  value 
			if int(record_db_obj.get_ev_type()) not in dict.keys():
				#print("HERE2")
				dict[int(record_db_obj.get_ev_type())]=[record_db_obj]
			#if the type of this event (key of the dictionary) already exists, we simply add the value (record database obj) in the list
			else:
				
				dict[int(record_db_obj.get_ev_type())].append(record_db_obj)
				
		file.close()
		
		
		return dict
				


#*****************************************************************************************************************************************************************************************
	#method creating a dictionary from the db, key =id entry link, value=[..., t_veh_appear,...]
	def fct_creation_dictionary_key_id_entry_lk_value_li_t_veh_ap_1_1(self):
	
		#key event type, value event
		di_key_ev_type=self.fct_creation_dictionary_from_the_db_file()
		
		di={}
		
		#for each veh ap event
		for i in di_key_ev_type[Cl_Event.TYPE_EV["type_ev_veh_appearance"]]:
		
			#print(i)
			#print(i.get_id_event_link())
			#import sys
			#sys.exit()
			
			if i.get_id_event_link() not in di:
				di[i.get_id_event_link()]=[i.get_ev_time()]
			
			else:
				di[i.get_id_event_link()].append(i.get_ev_time())
		return di

#*****************************************************************************************************************************************************************************************
	#method creating a dictionary from the db, key =id entry link, value=[..., t_veh_ar,...]
	def fct_creation_dictionary_key_id_exit_lk_value_li_t_veh_ar_1_1(self):
	
		#key event type, value event
		di_key_ev_type=self.fct_creation_dictionary_from_the_db_file()
		
		di={}
		
		#for each veh ap event
		for i in di_key_ev_type[Cl_Event.TYPE_EV["type_ev_veh_arrived_at_lk"]]:
		
			#print(i)
			#print(i.get_id_event_link())
			#import sys
			#sys.exit()
			if i.get_type_link_event()==Cl_Network_Link.TYPE_NETWORK_LINK["exit"]:
				if i.get_id_event_link() not in di:
					di[i.get_id_event_link()]=[i.get_ev_time()]
			
				else:
					di[i.get_id_event_link()].append(i.get_ev_time())
		return di

#*****************************************************************************************************************************************************************************************
	#method creating a dictionary from the db, key =id entry link, value=[..., t_veh_ar,...]
	def fct_creation_dictionary_key_id_internal_lk_value_li_t_veh_ar_1_1(self):
	
		#key event type, value event
		di_key_ev_type=self.fct_creation_dictionary_from_the_db_file()
		
		di={}
		
		#for each veh ap event
		for i in di_key_ev_type[Cl_Event.TYPE_EV["type_ev_veh_arrived_at_lk"]]:
		
			#print(i)
			#print(i.get_id_event_link())
			#import sys
			#sys.exit()
			if i.get_type_link_event()==Cl_Network_Link.TYPE_NETWORK_LINK["internal"]:
				if i.get_id_event_link() not in di:
					di[i.get_id_event_link()]=[i.get_ev_time()]
			
				else:
					di[i.get_id_event_link()].append(i.get_ev_time())
		return di

#*****************************************************************************************************************************************************************************************


	#method reading the db file created by sim and returns a dictionary with the vehicle information.
	#the key of the dictionary is the id of the vehicle
	#value= [...,[event time,event_type,veh id, veh. current link location, veh destination, time exit netw],...]
	def fct_dict_information_vehicles_sim_1_1(self):
	
		""" method returning a dictionary with the vehilce information"""
		
		dict_veh={}
		#we are going to extract from the db dictionary the events of type veh appearance, veh arrival and veh departure
		#these are elements corresponding to keys 1, 5 and 4
		#self._dict_db_record_obj[id_event_type]= [ ..., record_database_obj,...       ]
		for i in [ Cl_Event.TYPE_EV["type_ev_veh_appearance"], Cl_Event.TYPE_EV["type_ev_end_veh_departure_from_queue_link"],\
		Cl_Event.TYPE_EV["type_ev_veh_arrived_at_lk"]]:

			#self._dict_db_record_obj= dict, key =evnt type, value record obj
			if int(i) in self._dict_db_record_obj.keys():
		
		
				for j in self._dict_db_record_obj[int(i)]:
			
					#if the veh id is not in the dict
					if j.get_vehicle_id() not in dict_veh.keys():
						dict_veh[j.get_vehicle_id()]=[[(j.get_ev_time()),j.get_ev_type(), j.get_vehicle_id(),\
						j.get_id_current_link_veh_location(),j.get_veh_id_destination_link(),j.get_time_veh_exit_from_network() ]]
				
					#if the vehicle id is in the dict
					else:
						#dict_veh[j.get_vehicle_id()].append([j.get_ev_time(),j.get_ev_type(), j.get_vehicle_id(),j.get_time_veh_appearance_in_network(),\
						#j.get_id_veh_entry_link(),j.get_veh_current_queue_location(),j.get_time_veh_exit_from_network() ])
						dict_veh[j.get_vehicle_id()].append([j.get_ev_time(),j.get_ev_type(), j.get_vehicle_id(),\
						j.get_id_current_link_veh_location(),j.get_veh_id_destination_link(),j.get_time_veh_exit_from_network() ])
					
		return dict_veh
#*****************************************************************************************************************************************************************************************
	#method reading the db file created by sim and returns a dictionary with the vehicle information, when the veh final destination will
	#dyanamically be constructed.
	#the key of the dictionary is the id of the vehicle
	#value= [...,[event time,event_type,veh id, veh. current link location, veh destination, time exit netw],...]
	def fct_dict_information_vehicles_sim_when_final_dest_dynam_constructed(self):
	
		""" method returning a dictionary with the vehilce information"""
		
		dict_veh={}
		#we are going to extract from the db dictionary the events of type veh appearance, veh arrival and veh departure
		#these are elements corresponding to keys 1, 5 and 4
		#self._dict_db_record_obj[id_event_type]= [ ..., record_database_obj,...       ]
		for i in [ Cl_Event.TYPE_EV["type_ev_veh_appearance"], Cl_Event.TYPE_EV["type_ev_end_veh_departure_from_que"],\
		Cl_Event.TYPE_EV["type_ev_veh_arrived_at_que"],Cl_Event.TYPE_EV["type_ev_veh_appearance_nsi"],\
		Cl_Event.TYPE_EV["type_ev_end_veh_departure_from_que_nsi"],\
		Cl_Event.TYPE_EV["type_ev_veh_arrived_at_que_nsi"]]:

			#self._dict_db_record_obj= dict, key =evnt type, value record obj
			if int(i) in self._dict_db_record_obj.keys():
		
		
				for j in self._dict_db_record_obj[int(i)]:
			
					#if the veh id is not in the dict
					if j.get_vehicle_id() not in dict_veh.keys():
						#dict_veh[j.get_vehicle_id()]=[[j.get_ev_time(),j.get_ev_type(), j.get_vehicle_id(),\
						#j.get_id_current_link_veh_location(),j.get_veh_id_destination_link(),j.get_time_veh_exit_from_network(),\
						#j.get_time_veh_start_departure_from_current_queue()]]
						dict_veh[j.get_vehicle_id()]=[[j.get_ev_time(),j.get_ev_type(), j.get_vehicle_id(),\
						j.get_id_current_link_veh_location(),j.get_veh_id_destination_link(),j.get_time_veh_exit_from_network()]]
				
					#if the vehicle id is in the dict
					else:
						#dict_veh[j.get_vehicle_id()].append([j.get_ev_time(),j.get_ev_type(), j.get_vehicle_id(),j.get_time_veh_appearance_in_network(),\
						#j.get_id_veh_entry_link(),j.get_veh_current_queue_location(),j.get_time_veh_exit_from_network() ])
						#dict_veh[j.get_vehicle_id()].append([j.get_ev_time(),j.get_ev_type(), j.get_vehicle_id(),\
						#j.get_id_current_link_veh_location(),j.get_veh_id_destination_link(),j.get_time_veh_exit_from_network(),\
						#j.get_time_veh_start_departure_from_current_queue()])
						dict_veh[j.get_vehicle_id()].append([j.get_ev_time(),j.get_ev_type(), j.get_vehicle_id(),\
						j.get_id_current_link_veh_location(),j.get_veh_id_destination_link(),j.get_time_veh_exit_from_network()])
						#if j.get_ev_type()==4 and j.get_vehicle_id()==43:
							#print(j.get_time_veh_start_departure_from_current_queue())
							#print("j.get_ev_time()",j.get_ev_time(),"j.get_id_current_link_veh_location()",j.get_id_current_link_veh_location(),\
							#",j.get_veh_id_destination_link()",j.get_veh_id_destination_link(),"j.get_time_veh_exit_from_network()",
							#j.get_time_veh_exit_from_network())
							#import sys
							#sys.exit()
					
		return dict_veh
#*****************************************************************************************************************************************************************************************
	#method reading the db file created by sim and returns a dictionary with the vehicle information, when the veh final dest 
	#is defined by the veh appearance.
	#the key of the dictionary is the id of the vehicle
	#value= [...,[event time,event_type,veh id, veh. current link location, next veh destination, time exit netw,id_exit lk],...]
	def fct_dict_information_vehicles_sim_when_final_dest_defined_by_veh_ap(self):
	
		""" method returning a dictionary with the vehilce information"""
		
		dict_veh={}
		#we are going to extract from the db dictionary the events of type veh appearance, veh arrival and veh departure
		#these are elements corresponding to keys 1, 5 and 4
		#self._dict_db_record_obj[id_event_type]= [ ..., record_database_obj,...       ]
		for i in [ Cl_Event.TYPE_EV["type_ev_veh_appearance"], Cl_Event.TYPE_EV["type_ev_end_veh_departure_from_que"],\
		Cl_Event.TYPE_EV["type_ev_veh_arrived_at_que"],Cl_Event.TYPE_EV["type_ev_veh_appearance_nsi"],\
		Cl_Event.TYPE_EV["type_ev_end_veh_departure_from_que_nsi"],\
		Cl_Event.TYPE_EV["type_ev_veh_arrived_at_que_nsi"]]:

			#self._dict_db_record_obj= dict, key =evnt type, value record obj
			if int(i) in self._dict_db_record_obj.keys():
				
		
				for j in self._dict_db_record_obj[int(i)]:
					
			
					#if the veh id is not in the dict
					if j.get_vehicle_id() not in dict_veh.keys():
						#dict_veh[j.get_vehicle_id()]=[[j.get_ev_time(),j.get_ev_type(), j.get_vehicle_id(),\
						#j.get_id_current_link_veh_location(),j.get_veh_id_destination_link(),j.get_time_veh_exit_from_network(),\
						#j.get_time_veh_start_departure_from_current_queue()]]
						dict_veh[j.get_vehicle_id()]=[[j.get_ev_time(),j.get_ev_type(), j.get_vehicle_id(),\
						j.get_id_current_link_veh_location(),j.get_veh_id_destination_link(),j.get_time_veh_exit_from_network(),\
						j.get_id_veh_final_dest_exit_lk()]]
						
							
				
					#if the vehicle id is in the dict
					else:
						#dict_veh[j.get_vehicle_id()].append([j.get_ev_time(),j.get_ev_type(), j.get_vehicle_id(),j.get_time_veh_appearance_in_network(),\
						#j.get_id_veh_entry_link(),j.get_veh_current_queue_location(),j.get_time_veh_exit_from_network() ])
						#dict_veh[j.get_vehicle_id()].append([j.get_ev_time(),j.get_ev_type(), j.get_vehicle_id(),\
						#j.get_id_current_link_veh_location(),j.get_veh_id_destination_link(),j.get_time_veh_exit_from_network(),\
						#j.get_time_veh_start_departure_from_current_queue()])
						dict_veh[j.get_vehicle_id()].append([j.get_ev_time(),j.get_ev_type(), j.get_vehicle_id(),\
						j.get_id_current_link_veh_location(),j.get_veh_id_destination_link(),j.get_time_veh_exit_from_network(),\
						j.get_id_veh_final_dest_exit_lk()])
						#if j.get_ev_type()==4 and j.get_vehicle_id()==43:
							#print(j.get_time_veh_start_departure_from_current_queue())
							#print("j.get_ev_time()",j.get_ev_time(),"j.get_id_current_link_veh_location()",j.get_id_current_link_veh_location(),\
							#",j.get_veh_id_destination_link()",j.get_veh_id_destination_link(),"j.get_time_veh_exit_from_network()",
							#j.get_time_veh_exit_from_network())
							#import sys
							#sys.exit()
				
		
		#print("dict_veh",dict_veh)
		#print(j.get_id_veh_final_dest_exit_lk(),j.get_ev_type())
		
		return dict_veh
#*****************************************************************************************************************************************************************************************
	#method reading the db file created by sim and returns a dictionary with the vehicle information,
	def fct_dict_information_vehicles_sim(self):
		#if the vehicle final destination will dynamically be constructed
		if self._veh_final_dest_dynam_constructed==List_Explicit_Values.initialisation_value_to_one:
		
			di_rep=self.fct_dict_information_vehicles_sim_when_final_dest_dynam_constructed()
		
		#if the vehicle final destination will  be defined by the veh appearance
		else:
			di_rep=self.fct_dict_information_vehicles_sim_when_final_dest_defined_by_veh_ap()
			
		return di_rep

#*****************************************************************************************************************************************************************************************
	#method reading the db file created by sim and returns a dictionary with the vehicle information.
	#the key of the dictionary is the id of the vehicle
	#value=[...,[event time,event_type,veh id, veh. current link location, veh destination, time exit netw,\
	#time started departure, len(queue size if the event is arrival at link) -1 we substract -1 because we do not want to count the current vehicle,-1 otherwise],...]
	def fct_dict_information_vehicles_sim_all_inf(self):
	
		""" method returning a dictionary with the vehilce information"""
		
		dict_veh={}
		#we are going to extract from the db dictionary the events of type veh appearance, veh arrival and veh departure
		#these are elements corresponding to keys 1, 5 and 4
		#self._dict_db_record_obj[id_event_type]= [ ..., record_database_obj,...       ]
		for i in [ Cl_Event.TYPE_EV["type_ev_veh_appearance"], Cl_Event.TYPE_EV["type_ev_end_veh_departure_from_que"],\
		Cl_Event.TYPE_EV["type_ev_veh_arrived_at_que"],Cl_Event.TYPE_EV["type_ev_veh_appearance_nsi"],\
		Cl_Event.TYPE_EV["type_ev_end_veh_departure_from_que_nsi"],Cl_Event.TYPE_EV["type_ev_veh_arrived_at_que_nsi"]]:

			#self._dict_db_record_obj= dict, key =evnt type, value record obj
			if int(i) in self._dict_db_record_obj.keys():
		
		
				for j in self._dict_db_record_obj[int(i)]:
			
					#if the veh id is not in the dict
					if j.get_vehicle_id() not in dict_veh.keys():
						#if the event is veh arrival at the end of the link or appear
						if j.get_ev_type()==Cl_Event.TYPE_EV["type_ev_veh_arrived_at_que"] or\
						j.get_ev_type()==Cl_Event.TYPE_EV["type_ev_veh_appearance"] or\
						j.get_ev_type()==Cl_Event.TYPE_EV["type_ev_veh_arrived_at_que_nsi"] or\
						j.get_ev_type()==Cl_Event.TYPE_EV["type_ev_veh_appearance_nsi"]:
							if j.get_li_id_vehicles_in_queue()!=-1:
								a=len(j.get_li_id_vehicles_in_queue())-1
							else:
								a=-1
						
							dict_veh[j.get_vehicle_id()]=[[j.get_ev_time(),j.get_ev_type(),\
							j.get_id_current_link_veh_location(),j.get_veh_id_destination_link(),j.get_time_veh_exit_from_network(),\
							j.get_time_veh_start_departure_from_current_link(),a]]
						#if the event is not a veh arrival at the end of the link or veh appear
						else:
							dict_veh[j.get_vehicle_id()]=[[j.get_ev_time(),j.get_ev_type(),\
							j.get_id_current_link_veh_location(),j.get_veh_id_destination_link(),j.get_time_veh_exit_from_network(),\
							j.get_time_veh_start_departure_from_current_link(),-1]]
				
					#if the vehicle id is in the dict
					else:
						#if the event is veh arrival at the end of the link
						if j.get_ev_type()==Cl_Event.TYPE_EV["type_ev_veh_arrived_at_que"] or\
						j.get_ev_type()==Cl_Event.TYPE_EV["type_ev_veh_appearance"] or\
						j.get_ev_type()==Cl_Event.TYPE_EV["type_ev_veh_arrived_at_que_nsi"] or\
						j.get_ev_type()==Cl_Event.TYPE_EV["type_ev_veh_appearance_nsi"]:
							if j.get_li_id_vehicles_in_queue()!=-1:
								a=len(j.get_li_id_vehicles_in_queue())-1
							else:
								a=-1
						
							dict_veh[j.get_vehicle_id()].append([j.get_ev_time(),j.get_ev_type(),\
							j.get_id_current_link_veh_location(),j.get_veh_id_destination_link(),j.get_time_veh_exit_from_network(),\
							j.get_time_veh_start_departure_from_current_link(),a])
						#if the event is not a veh arrival at the end of the link (or appear, in this case it cannot be appear since the lk id
						#is l	ready in the dict, but...)
						else:
							dict_veh[j.get_vehicle_id()].append([j.get_ev_time(),j.get_ev_type(),\
							j.get_id_current_link_veh_location(),j.get_veh_id_destination_link(),j.get_time_veh_exit_from_network(),\
							j.get_time_veh_start_departure_from_current_link(),-1])
				for m in dict_veh:
					dict_veh[m].sort()
						
					
		return dict_veh
#*****************************************************************************************************************************************************************************************

	
	#method writting in a file the veh information when the vehicle final destin is dynamically constructed
	#(time_event,type_event,veh_id,id_current_link,id_destination_link,t_exit_from_netw)
	#for each vehicle we create a separate file
	
	def fct_write_file_vehicles_sim_when_final_dest_dynam_constructed(self,val_open="w"):
	
		#dict with the names of veh files
		dict_names_veh_files={}
		
		#the key is the vehicle id, 
		#the value is [...,[time_event,type_event,veh_id,id_current_link,id_destination_link,t_exit_from_netw],...]
		
		for j in self._dict_veh_information:
			b=self._veh_file_to_write_res+str(j)+".txt"
			file=open(b,"w")
			
			file.write("%s\t %d\t \n"%(" VEH ID:",j))
	
			file.write("%s\t \n" %("Event Time(1)"))
			file.write("%s\t \n" %(" Even Type(2)"))
			file.write("%s\t \n" %("ID VEH(3)"))
			file.write("%s\t \n" %("ID Current Veh Id Link Location(4)"))
			file.write("%s\t \n" %("ID  Veh  Id Destination Link Location(5)"))
			file.write("%s\t \n" %("T Exit from Network (6)"))
			file.close()
			
			#We add the file in the dictionary 
			#dict_names_veh_files[j]=self._veh_file_to_write_res+str(j)
			dict_names_veh_files[j]=b

		
		#for each vehicle we open the associated file
		for i in self._dict_veh_information:
			
			file=open(dict_names_veh_files[i],"a")
			
			self._dict_veh_information[i].sort()
			
			
			#for each veh event
			for m in range(len(self._dict_veh_information[i])):
				#if i==65:
					#print("self._dict_veh_information[i][m][0]",self._dict_veh_information[i][m][0])
					#print("self._dict_veh_information[i][m][0]",self._dict_veh_information[i][m][1])
					#print("self._dict_veh_information[i][m][0]",self._dict_veh_information[i][m][2])
					#print("self._dict_veh_information[i][m][0]",self._dict_veh_information[i][m][3])
					#print("self._dict_veh_information[i][m][0]",self._dict_veh_information[i][m][4])
					#print("self._dict_veh_information[i][m][0]",self._dict_veh_information[i][m][5])
				#we write the event
				#print([j for j in self._dict_veh_information[i][m]])
				file.write("%.1f\t %d\t %d\t %d\t %d\t %.1f\t \n"%(self._dict_veh_information[i][m][0],self._dict_veh_information[i][m][1],\
				self._dict_veh_information[i][m][2],self._dict_veh_information[i][m][3],self._dict_veh_information[i][m][4],\
				self._dict_veh_information[i][m][5]))
				#file.write(["%s\t %s\t %s\t %s\t %s\t \n"%(self._dict_veh_information[i][m][j] for j in self._dict_veh_information[i][m])])
			#if i==65:
				#print(self._dict_veh_information[65])
				#import sys
				#sys.exit()
					
			file.close()
		
		
#*****************************************************************************************************************************************************************************************

	#method writting in a file the veh information when the veh final destination is defined by its appearance
	#(time_event,type_event,veh_id,id_current_link,id_destination_link,t_exit_from_netw)
	#for each vehicle we create a separate file
	
	def fct_write_file_vehicles_sim_when_final_dest_defined_by_veh_ap(self,val_open="w"):
	
		#dict with the names of veh files
		dict_names_veh_files={}
		
		#self._dict_veh_information, dict, the key is the vehicle id, 
		#the value is [...,[[event time,event_type,veh id, veh.current link location, veh destination, time exit netw,time started departure,id_exit lk],...]
		
		
		for j in self._dict_veh_information:
			b=self._veh_file_to_write_res+str(j)+".txt"
			file=open(b,"w")
			
			file.write("%s\t %d\t \n"%(" VEH ID:",j))
	
			file.write("%s\t \n" %("Event Time(1)"))
			file.write("%s\t \n" %(" Even Type(2)"))
			file.write("%s\t \n" %("ID VEH(3)"))
			file.write("%s\t \n" %("ID Current Veh Id Link Location(4)"))
			file.write("%s\t \n" %("ID  Veh  Id Destination Link Location(5)"))
			file.write("%s\t \n" %("T Exit from Network (6)"))
			file.write("%s\t \n" %("ID LK  VEH FINAL DESTINATION  (7)"))
			file.close()
			
			#We add the file in the dictionary 
			#dict_names_veh_files[j]=self._veh_file_to_write_res+str(j)
			dict_names_veh_files[j]=b

		
		#for each vehicle we open the associated file
		for i in self._dict_veh_information:
			
			file=open(dict_names_veh_files[i],"a")
			
			self._dict_veh_information[i].sort()
			
			
			#for each veh event
			for m in range(len(self._dict_veh_information[i])):
				#print("self._dict_veh_information[i]",self._dict_veh_information[1])
				#import sys
				#sys.exit()
				#if i==65:
					#print("self._dict_veh_information[i][m][0]",self._dict_veh_information[i][m][0])
					#print("self._dict_veh_information[i][m][0]",self._dict_veh_information[i][m][1])
					#print("self._dict_veh_information[i][m][0]",self._dict_veh_information[i][m][2])
					#print("self._dict_veh_information[i][m][0]",self._dict_veh_information[i][m][3])
					#print("self._dict_veh_information[i][m][0]",self._dict_veh_information[i][m][4])
					#print("self._dict_veh_information[i][m][0]",self._dict_veh_information[i][m][5])
				#we write the event
				#print([j for j in self._dict_veh_information[i][m]])
				file.write("%.1f\t %d\t %d\t %d\t %d\t %.1f\t %d \n"%(self._dict_veh_information[i][m][0],self._dict_veh_information[i][m][1],\
				self._dict_veh_information[i][m][2],self._dict_veh_information[i][m][3],self._dict_veh_information[i][m][4],\
				self._dict_veh_information[i][m][5],self._dict_veh_information[i][m][6]))
				#file.write(["%s\t %s\t %s\t %s\t %s\t \n"%(self._dict_veh_information[i][m][j] for j in self._dict_veh_information[i][m])])
			#if i==65:
				#print(self._dict_veh_information[65])
				#import sys
				#sys.exit()
					
			file.close()
		
		
#*****************************************************************************************************************************************************************************************
	#method writting in a file the veh information
	def fct_write_file_vehicles_sim(self):
		#if the vehicle final destination  is dynamically constructed
		#if self._veh_final_dest_dynam_constructed==List_Explicit_Values.initialisation_value_to_one:
		if self._veh_final_dest_dynam_constructed==Cl_Decisions.TYPE_VEHICLE_FINAL_DESTINATION_AND_PATH["dynamically_defined"]:
		
			self.fct_write_file_vehicles_sim_when_final_dest_dynam_constructed()
		
		#if the vehicle final destination  is  defined by its appearance
		else:
			
			self.fct_write_file_vehicles_sim_when_final_dest_defined_by_veh_ap()
		
		

#*****************************************************************************************************************************************************************************************
	#method writting in a file the veh information (time_event,type_event,veh_id,id_current_link,id_destination_link,t_exit_from_netw)
	#for each vehicle we create a separate file
	
	def fct_write_file_vehicles_sim_1(self,val_open="w"):
	
		#dict with the names of veh files
		dict_names_veh_files={}
		
		#the key is the vehicle id, 
		#the value is [...,[time_event,type_event,veh_id,id_current_link,id_destination_link,t_exit_from_netw, t start veh departure],...]
		
		for i in self._dict_veh_information:
			file=open(self._veh_file_to_write_res+str(i),"w")
			
			file.write("%s\t %d\t \n"%(" VEH ID:",i))
	
			file.write("%s\t \n" %("Event Time(1)"))
			file.write("%s\t \n" %(" Even Type(2)"))
			file.write("%s\t \n" %("ID VEH(3)"))
			file.write("%s\t \n" %("ID Current Veh Id Link Location(4)"))
			file.write("%s\t \n" %("ID  Veh  Id Destination Link Location(5)"))
			file.write("%s\t \n" %("T Exit from Network (6)"))
			#file.write("%s\t \n" %("T Start Veh Departure, (value valid for eve type 4,otherwise =-1) (6)"))
			file.write("%s\t \n" %("T Start Veh Depart, (6)"))

			file.close()
			
			#We add the file in the dictionary 
			dict_names_veh_files[i]=self._veh_file_to_write_res+str(i)

		
		#for each vehicle we open the associated file
		#self._dict_veh_information=dict, key=veh id, 
		#val=[...,[event time,event_type,veh id, veh. current link location, veh destination, time exit netw, t start departure]...]
		for i in self._dict_veh_information:
			
			file=open(dict_names_veh_files[i],"a")
			
			#print("self._dict_veh_information[i]=",self._dict_veh_information[i])
			
			self._dict_veh_information[i].sort()
			
			#for each veh event
			for m in range(len(self._dict_veh_information[i])):
						
				#we write the event
				#print([j for j in self._dict_veh_information[i][m]])
				#file.write("%d\t %d\t %d\t %s\t %s\t %d\t \n"%(self._dict_veh_information[i][m][0],self._dict_veh_information[i][m][1],\
				#self._dict_veh_information[i][m][2],self._dict_veh_information[i][m][3],self._dict_veh_information[i][m][4],\
				#self._dict_veh_information[i][m][5]))
				file.write("%.1f\t %d\t %d\t %d\t %d\t %.1f\t %.1f\t\n"%(self._dict_veh_information[i][m][0],self._dict_veh_information[i][m][1],\
				self._dict_veh_information[i][m][2],self._dict_veh_information[i][m][3],self._dict_veh_information[i][m][4],\
				self._dict_veh_information[i][m][5],self._dict_veh_information[i][m][6]))
				#file.write(["%s\t %s\t %s\t %s\t %s\t \n"%(self._dict_veh_information[i][m][j] for j in self._dict_veh_information[i][m])])
			file.close()
		
		
#*****************************************************************************************************************************************************************************************			
		
		
		
		
















































