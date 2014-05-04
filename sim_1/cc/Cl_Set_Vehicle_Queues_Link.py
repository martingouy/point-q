import Cl_Vehicle_Queue
import List_Explicit_Values

class Set_Vehicle_Queues_Link:

	"""this class construct the set of queues at a link """
	def __init__(self, val_ti_unit,val_queue_id=-1,val_id_assoc_link=-1,val_li_id_associated_output_links_from_link=[],\
	val_li_queue_veh=[],val_dict_queue_max_queue_size_et_sat_flow_queue_type={},\
	val_dict_phase_interference={},\
	val_cur_service_rate=-1,val_cur_reached_service_rate=0):
	
		# the id of the first queue object
		self._queue_id=val_queue_id
		
		#the id of the associated link
		self._id_assoc_link=val_id_assoc_link
		
		#the list of the id of the output links from the associated link to this queue
		self._li_id_associated_output_links_from_link=val_li_id_associated_output_links_from_link
		
		#the list of the veh queue at  each queue of the link
		self._li_queue_veh=val_li_queue_veh
		
		#the dictionary, key is the phase (l,m), value is  a list [max size of the queue, saturation flow of the queue,routing proportion] 
		self._dict_queue_max_queue_size_et_sat_flow_queue_type=\
		val_dict_queue_max_queue_size_et_sat_flow_queue_type
		
		#the service rate of each queue initialise a -1, ev_new_inters_control le mettra a jour pour les si
		# for a non signalised inters it will be the total service rate during the entire sim et il sera initialise par creat_netw
		self._cur_service_rate=val_cur_service_rate
		
		
		#the currently reached service rate by each  queue
		self._cur_reached_service_rate=val_cur_reached_service_rate
		
		
		#construction of the set of the queues,
		#it is a dictionary of which the id is the [l,m]=[input link, output link from link] and the value is the vehicle queue
		#the number of queues of a queue depends on the number of leaving links from the head node of the link
		dict_obj_veh_queue_at_link={}
		
		
		for i in range(len(self._li_id_associated_output_links_from_link)):
		
			#if the saturation flow of the associated  phase is not zero then we create the movement
			#ATTENTION THIS TEST HAS ALSO BEEN MADE IN CREAT ENTRY-INTERNAL LINKS.
			#WHEN VALIDATE THE CORRECT FCT OF THE SIM IT MAY BE DELETED....
			if self._dict_queue_max_queue_size_et_sat_flow_queue_type[(self._id_assoc_link,\
			self._li_id_associated_output_links_from_link[i])]\
			[List_Explicit_Values.val_second_element_of_list] != List_Explicit_Values.initialisation_value_to_zero:
				
				#print("HERE",self._dict_queue_max_queue_size_et_sat_flow_queue_type_rout_prop_param_trav_durat[(self._id_assoc_link,\
				#self._li_id_associated_output_links_from_link[i])])
				
				#val_dict_phase_interference=dict, key=id phase, val=[...,[id phasen param],...]
				#if the phase interfere with another one
				#if self._id_assoc_link==2 and self._li_id_associated_output_links_from_link[i]==3:
					#print((self._id_assoc_link,self._li_id_associated_output_links_from_link[i]) in val_dict_phase_interference,val_dict_phase_interference.keys())
					#import sys
					#sys.exit()
				if (self._id_assoc_link,self._li_id_associated_output_links_from_link[i]) in val_dict_phase_interference:
				
					di={}
					for m in val_dict_phase_interference[self._id_assoc_link,self._li_id_associated_output_links_from_link[i]]:
						di[m[0],m[1]]=m[2]
										 
					v_q=Cl_Vehicle_Queue.Vehicle_Queue(\
					val_t_unit=val_ti_unit,\
					val_id_queue=self._queue_id,\
					val_id_associated_link=self._id_assoc_link,\
					val_id_associated_output_link=self._li_id_associated_output_links_from_link[i],\
					val_queue_veh=self._li_queue_veh[i],\
					val_max_veh_queue_size=\
					self._dict_queue_max_queue_size_et_sat_flow_queue_type[(self._id_assoc_link,\
					self._li_id_associated_output_links_from_link[i])]\
					[List_Explicit_Values.val_first_element_of_list],\
					val_sat_flow_queue=\
					self._dict_queue_max_queue_size_et_sat_flow_queue_type[(self._id_assoc_link,\
					self._li_id_associated_output_links_from_link[i])]\
					[List_Explicit_Values.val_second_element_of_list],\
					val_type_veh_queue=\
					self._dict_queue_max_queue_size_et_sat_flow_queue_type[(self._id_assoc_link,\
					self._li_id_associated_output_links_from_link[i])]\
					[List_Explicit_Values.val_third_element_of_list],\
					val_current_queue_service_rate=self._cur_service_rate,\
					val_current_reached_service_rate=self._cur_reached_service_rate,\
					val_di_phase_interference=di)
				
				#if the phase does not interfere with another one
				else:
					v_q=Cl_Vehicle_Queue.Vehicle_Queue(\
					val_t_unit=val_ti_unit,\
					val_id_queue=self._queue_id,\
					val_id_associated_link=self._id_assoc_link,\
					val_id_associated_output_link=self._li_id_associated_output_links_from_link[i],\
					val_queue_veh=self._li_queue_veh[i],\
					val_max_veh_queue_size=\
					self._dict_queue_max_queue_size_et_sat_flow_queue_type[(self._id_assoc_link,\
					self._li_id_associated_output_links_from_link[i])]\
					[List_Explicit_Values.val_first_element_of_list],\
					val_sat_flow_queue=\
					self._dict_queue_max_queue_size_et_sat_flow_queue_type[(self._id_assoc_link,\
					self._li_id_associated_output_links_from_link[i])]\
					[List_Explicit_Values.val_second_element_of_list],\
					val_type_veh_queue=\
					self._dict_queue_max_queue_size_et_sat_flow_queue_type[(self._id_assoc_link,\
					self._li_id_associated_output_links_from_link[i])]\
					[List_Explicit_Values.val_third_element_of_list],\
					val_current_queue_service_rate=self._cur_service_rate,\
					val_current_reached_service_rate=self._cur_reached_service_rate)
				
									
				dict_obj_veh_queue_at_link[self._id_assoc_link,self._li_id_associated_output_links_from_link[i]]=v_q
			
				self._queue_id+=List_Explicit_Values.initialisation_value_to_one
			
		#the set of queues at a link (the list of  vehicle queue objects at a link)
		#key =[input link, output link], value=queue	
		self._di_obj_veh_queue_at_link=dict_obj_veh_queue_at_link
		
#*****************************************************************************************************************************************************************************************
	#method returning the id of the first queue object
	def get_queue_id(self):
		return self._queue_id
#*****************************************************************************************************************************************************************************************
	#method returning the id of the associated link
	def get_id_assoc_link(self):
		return self._id_assoc_link
	
#*****************************************************************************************************************************************************************************************
	#method returning the number of leaving links from the headnode of the associated link
	def get_li_id_associated_output_links_from_link(self):
		return self._li_id_associated_output_links_from_link
#*****************************************************************************************************************************************************************************************
	#method returning the list of the veh queue at  each queue of the link
	def get_li_queue_veh(self):
		return self._li_queue_veh

#*****************************************************************************************************************************************************************************************
	#method returning the dictionary, key is the phase (l,m), value is  a list [max size of the queue, saturation flow of the queue]  
	def get_dict_queue_max_queue_size_et_sat_flow_queue_type(self):
		return self._dict_queue_max_queue_size_et_sat_flow_queue_type
#*****************************************************************************************************************************************************************************************
	#method returning the service rate of each queue (for a non signalised inters it will be the total service rate during the entire sim)
	def get_cur_service_rate(self):
		return self._cur_service_rate
#*****************************************************************************************************************************************************************************************
	#method returning the currently reached service rate by each queue
	def get_cur_reached_service_rate(self):
		return self._cur_reached_service_rate

#*****************************************************************************************************************************************************************************************
	#method returning the set of queues at a link (the dictionary of  vehicle queue objects at a link)
	def get_di_obj_veh_queue_at_link(self):
		return self._di_obj_veh_queue_at_link

#*****************************************************************************************************************************************************************************************
	#method returning the dictionary with the sensor information
	def get_di_detector_associated_to_link_ques(self):
		return self._di_detector_associated_to_link_ques

#*****************************************************************************************************************************************************************************************
	#method returning the list with the ids of all the output links relates with the queues
	def get_li_output_lk_ids_associated_with_ques(self):
		li=[]
		
		for i in list(self._di_obj_veh_queue_at_link.keys()):
			li.append(i[1])
		return li

#*****************************************************************************************************************************************************************************************
	#method modifying the id of the first queue object
	def set_first_queue_id(self,n_v):
		self._first_queue_id=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the id of the associated link
	def set_id_assoc_link(self,n_v):
		self._id_assoc_link=n_v
	
#*****************************************************************************************************************************************************************************************
	#method modifying the number of leaving links from the headnode of the associated link
	def set_li_id_associated_output_links_from_link(self,n_v):
		self._li_id_associated_output_links_from_link=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the list of the veh queue at  each queue of the link
	def set_li_queue_veh(self,n_v):
		self._li_queue_veh=n_v


#*****************************************************************************************************************************************************************************************
	#methodmodifying the service rate of each queue (for a non signalised inters it will be the total service rate during the entire sim)
	def set_cur_service_rate(self,n_v):
		self._cur_service_rate=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the currently reached service rate by each queue
	def set_cur_reached_service_rate(self,n_v):
		self._cur_reached_service_rate=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the dictionary, key is the phase (l,m), value is  a list [max size of the queue, saturation flow of the queue]  
	def set_dict_queue_max_queue_size_et_sat_flow_queue_type(self,n_v):
		self._dict_queue_max_queue_size_et_sat_flow_queue_type=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the set of queues at a link (the list of  vehicle queue objects at a link)
	def set_di_obj_veh_queue_at_link(self,n_v):
		self._li_obj_veh_queue_at_link=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the dictionary with the sensor information
	def set_di_detector_associated_to_link_ques(self,n_v):
		self._di_detector_associated_to_link_ques=n_v

#*****************************************************************************************************************************************************************************************
	


#ex
#id_lk=1
#nb_leav_nd=6
#ind_q=1

#set_veh_q_link=Set_Vehicle_Queues_Link(val_id_assoc_link=id_lk,val_nb_leaving_nodes_from_head_nd_link=nb_leav_nd, val_index_queue=ind_q)
#print("ID ASOC LINK, QUEUES",set_veh_q_link.get_id_assoc_link(),len(set_veh_q_link.get_li_obj_veh_queue_at_link()))




































