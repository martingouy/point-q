import Cl_Vehicle_Queue
import Cl_Set_Vehicle_Queues_Link

TYPE_LINK={"network":1,"sublink":2}

class Link:
	"""class defining a Link object : network and sublink type"""
	def __init__(self,val_id_link=-1,val_type_link=-1,val_li_id_input_links_to_link=[],val_li_id_output_links_from_link=[],\
	val_set_veh_queue=None,val_length_link=-1,val_capacity_link=None,val_current_nb_veh_link=0,\
	val_li_output_links_queues=None):
	
		#the id of the link
		self._id_link=val_id_link
		
		#the type of the link
		self._type_link=val_type_link
		
		#the list with the id of the input links to this link (for a sublink it will be the set of id of the input sublinks to this sublink)
		self._li_id_input_links_to_link=val_li_id_input_links_to_link
		
		#the list with the id of the output links from this link
		self._li_id_output_links_from_link=val_li_id_output_links_from_link
		
		#the set of veh queues at the link (object of type Set_Vehicle_Queues_Link)
		self._set_veh_queue=val_set_veh_queue
		
		#the length of the link
		self._length_link=val_length_link
		
		#the capacity of the link
		self._capacity_link=val_capacity_link
		
		#the current nb of vehicles  in the link(at any time)
		self._current_nb_veh_link=val_current_nb_veh_link
		
		#the list with the ids of all the output links of queues
		self._li_output_links_queues=val_li_output_links_queues
		
		#the available places at the link
		#self._nb_avail_link_places=self._capacity_link
		
#*****************************************************************************************************************************************************************************************
	#method returning the id of the link
	def get_id_link(self):
		return self._id_link

#*****************************************************************************************************************************************************************************************
	#method returning the type of the link
	def get_type_link(self):
		return self._type_link
#*****************************************************************************************************************************************************************************************
	#method returning the list with the id of the input links to this link
	def get_li_id_input_links_to_link(self):
		return self._li_id_input_links_to_link

#*****************************************************************************************************************************************************************************************
	#method returning the list with the id of the output links from this link
	def get_li_id_output_links_from_link(self):
		return self._li_id_output_links_from_link

#*****************************************************************************************************************************************************************************************
	#method returning the set of veh queues at the link
	def get_set_veh_queue(self):
		return self._set_veh_queue

#*****************************************************************************************************************************************************************************************
	
	#method returning the length of the link
	def get_length_link(self):
		return self._length_link
#*****************************************************************************************************************************************************************************************
	#method returning the link capacity
	def get_capacity_link(self):
		return self._capacity_link
#*****************************************************************************************************************************************************************************************
	#method returning the current nb  of veh in the link
	def get_current_nb_veh_link(self):
		return self._current_nb_veh_link
#*****************************************************************************************************************************************************************************************
	#method returning the ids of all the output links of the queues related on this link
	def get_li_output_links_queues(self):
		return self._li_output_links_queues

#*****************************************************************************************************************************************************************************************
	#method returning the available places at the link
	#def get_nb_avail_link_places(self):
		#return self._nb_avail_link_places
#*****************************************************************************************************************************************************************************************
	#method modifying the id of the link
	def set_id_link(self,n_v):
		self._id_link=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the type of the link
	def set_type_link(self,n_v):
		self._type_link=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the list with the id of the input links to this link
	def set_li_id_input_links_to_link(self,n_v):
		self._li_id_input_links_to_link=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying  the list with the id of the output links from this link
	def set_li_id_output_links_from_link(self,n_v):
		self._li_id_output_links_from_link=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the set of veh queues at the link
	def set_set_veh_queue(self,n_v):
		self._set_veh_queue=n_v

#*****************************************************************************************************************************************************************************************
	
	#method modifying the length of the link
	def set_length_link(self,n_v):
		self._length_link=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the link capacity
	def set_capacity_link(self,n_v):
		self._capacity_link=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the current nb of veh in the link 
	def set_current_nb_veh_link(self,n_v):
		self._current_nb_veh_link=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the ids of all the output links of the queues related on this link
	def set_li_output_links_queues(self,n_v):
		self._li_output_links_queues=n_v

#*****************************************************************************************************************************************************************************************
	#method intitialising the dicttionary with the values of the number of vehicles joined the current link, from each other input link to the link
	#def fct_initialise_di_ar_to_link_current_period(self,val=0):
		#for i in self._di_ar_to_link_current_period:
			#self._di_ar_to_link_current_period[i]=val

#*****************************************************************************************************************************************************************************************
	#method modifying the available places at the link
	#def set_nb_avail_link_places(self,n_v):
		#self._nb_avail_link_places=n_v
#*****************************************************************************************************************************************************************************************

	#method returning 1 if at least one of the related queues is nonempty, zero otherwise
	#def  fct_exam_existence_nonempty_que(self):
		#rep=0
		#for i in self._set_veh_queue.get_di_obj_veh_queue_at_link():
			
			#if len(self._set_veh_queue.get_di_obj_veh_queue_at_link()[i].get_queue_veh())>0:
				#return  1
		#if rep==0:
			#return 0
				
#*****************************************************************************************************************************************************************************************

	#method returning 1 if at least one of the related queues with the link has flows > f_min permitted, zero otherwise
	#def  fct_exam_existence_que_with_flow_sup_to_the_perm_value_1(self,val_fmin_perm):
		#rep=0
		#for i in self._set_veh_queue.get_di_obj_veh_queue_at_link():
			
			#if len(self._set_veh_queue.get_di_obj_veh_queue_at_link()[i].get_queue_veh())>val_fmin_perm:
				#return  1
		#if rep==0:
			#return 0
				
#*****************************************************************************************************************************************************************************************
	


#ex
#set_v_q=Cl_Set_Vehicle_Queues_Link.Set_Vehicle_Queues_Link(val_id_assoc_link=21,val_nb_leaving_nodes_from_head_nd_link=23,val_index_queue=1)

#lk=Link(val_id_link=21,val_type_link=TYPE_LINK["network"],val_set_veh_queue=set_v_q)

#print("",lk.get_id_link(),len(lk.get_set_veh_queue().get_li_obj_veh_queue_at_link()))


