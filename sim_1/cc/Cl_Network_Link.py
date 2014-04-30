import Cl_Link
import List_Explicit_Values

TYPE_NETWORK_LINK={"entry":1,"exit":2,"internal":3}

class Network_Link(Cl_Link.Link):


	"""class defining the network type of link employed for the construction of a network """
	
	def __init__(self,val_id_nwlink=-1,val_li_id_input_links_to_nwlink=[],val_li_id_output_links_from_nwlink=[],\
	val_set_vehicle_queue_nwlink=None,val_length_nwlink=-1,val_capacity_nwlink=None,\
	val_type_network_link=-1,\
	val_id_head_intersection_node=-1,val_id_tail_intersection_node=-1,\
	val_param_link_travel_duration=None,val_lis_output_links_queues=None,val_di_ar_to_link_current_period=None):
	
		Cl_Link.Link.__init__(self,val_id_link=val_id_nwlink, val_type_link=Cl_Link.TYPE_LINK["network"],\
		val_li_id_input_links_to_link=val_li_id_input_links_to_nwlink,\
		val_li_id_output_links_from_link=val_li_id_output_links_from_nwlink,\
		val_set_veh_queue=val_set_vehicle_queue_nwlink,\
		val_length_link=val_length_nwlink,val_capacity_link=val_capacity_nwlink,\
		val_li_output_links_queues=val_lis_output_links_queues)
		
	
		#the type of a network link
		self._type_network_link=val_type_network_link
		
		#the if od the node heading the link
		self._id_head_intersection_node=val_id_head_intersection_node
		
		#the if of the node at the tail of the link
		self._id_tail_intersection_node=val_id_tail_intersection_node
		
		
		#the param for the link travel duration
		self._param_link_travel_duration=val_param_link_travel_duration
		
		#the param for the link travel duration when split ratios are dynamically computed
		self._param_link_travel_duration_dyn_split_ratios=val_param_link_travel_duration
		
		#dict, key=id  link  bringing vehicles to this link, value=nb vehicles joined  this link during the current period
		self._di_ar_to_link_current_period=val_di_ar_to_link_current_period
		
		#variable indicating the number of vehicles joined the link durning the current period
		#this variable will be employed when the turn ratios are estimated
		#self._current_nb_veh_arrived_link_during_period=val_current_nb_veh_arrived_link_during_period

		
		
#*****************************************************************************************************************************************************************************************
	#method returning the type of a network link
	def get_type_network_link(self):
		return self._type_network_link
	
#*****************************************************************************************************************************************************************************************
	#method returning the if od the node heading the link
	def get_id_head_intersection_node(self):
		return self._id_head_intersection_node
#*****************************************************************************************************************************************************************************************
	#method returning the if of the node at the tail of the link
	def get_id_tail_intersection_node(self):
		return self._id_tail_intersection_node
#*****************************************************************************************************************************************************************************************
	
	#method returning the list of the if of the sublinks to which the current link is divided
	#def get_li_id_sublinks(self):
		#return self._li_id_sublinks

#*****************************************************************************************************************************************************************************************

	#method returning the param if the link travel duration
	def get_param_link_travel_duration(self):
		return self._param_link_travel_duration

#*****************************************************************************************************************************************************************************************
	#method returning the variable indicating the param for the link travel duration when split ratios are dynamically computed
	def get_param_link_travel_duration_dyn_split_ratios(self):
		return self._param_link_travel_duration_dyn_split_ratios
	
#*****************************************************************************************************************************************************************************************
	#method returning  the dict indicating how many vehicles join the current link from the input links to this link(for internal exit and links)
	def get_di_ar_to_link_current_period(self):
		return self._di_ar_to_link_current_period
#*****************************************************************************************************************************************************************************************
	#method returning the variable indicating the number of vehicles joined the link during the current perido
	#def get_current_nb_veh_arrived_link_during_period(self):
		#return self._current_nb_veh_arrived_link_during_period
#*****************************************************************************************************************************************************************************************
	#method modifying the type of a network link
	def set_type_network_link(self,n_v):
		self._type_network_link=n_v
	
#*****************************************************************************************************************************************************************************************
	#method modifying the id of the node heading the link
	def set_id_head_intersection_node(self,n_v):
		self._id_head_intersection_node=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the if of the node at the tail of the link
	def set_id_tail_intersection_node(self,n_v):
		self._id_tail_intersection_node=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the list of the id of the sublinks to which the current link is divided
	#def set_li_id_sublinks(self,n_v):
		#self._li_id_sublinks=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the param if the link travel duration
	def set_param_link_travel_duration(self,n_v):
		self._param_link_travel_duration=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the variable indicating the param for the link travel duration when split ratios are dynamically computed
	def set_param_link_travel_duration_dyn_split_ratios(self,n_v):
		self._param_link_travel_duration_dyn_split_ratios=n_v
	
#*****************************************************************************************************************************************************************************************
	#method modifying  the dict indicating how many vehicles join the current link from the input links to this link
	def set_di_ar_to_link_current_period(self,n_v):
		self._di_ar_to_link_current_period=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the variable indicating the number of vehicles joined the link during the current perido
	#def set_current_nb_veh_arrived_link_during_period(self,n_v):
		#self._current_nb_veh_arrived_link_during_period=n_v
#*****************************************************************************************************************************************************************************************
	#method updating thhe travel time of a network link when split ratios are dynamically computed
	#it is the travel time employed by the routuing algo and not the mean value of the travel time emmployed by the  .Q
	def fct_update_link_when_split_ratios_dyn_computed(self,val_new_trav_time):
		self._param_link_travel_duration_dyn_split_ratios=val_new_trav_time
		

#*****************************************************************************************************************************************************************************************
	#method intitialising the dicttionary with the values of the number of vehicles joined the current link, from each other input link to the link
	def fct_initialise_di_ar_to_link_current_period_1(self,val=0):
		
		for i in self._di_ar_to_link_current_period:
			self._di_ar_to_link_current_period[i]=val

#*****************************************************************************************************************************************************************************************
	#method intitialising the dicttionary with the values of the number of vehicles joined the current link, from each other input link to the link
	def fct_initialise_di_ar_to_link_current_period(self,val=0):
		
		for i in self._di_ar_to_link_current_period:
			self._di_ar_to_link_current_period[i]=val

#*****************************************************************************************************************************************************************************************
	#merhod updating the number of vehicles joined the link during the current period (case when split ratios wil be estimated)
	#def fct_update_current_nb_veh_arrived_link_during_period(self,n_v=1):
		#self._current_nb_veh_arrived_link_during_period+=current_nb_veh_arrived_link_during_period

#*****************************************************************************************************************************************************************************************
	

#ex
#lk=Network_Link(val_id_lk=12,val_type_network_link=TYPE_NETWORK_LINK["entry"])
#print("ID LINK, TYPE NETW LINK",lk.get_id_link(),lk.get_type_network_link())
#lk.set_id_head_intersection_node(4)
#print("ID HEAD NODE",lk.get_id_head_intersection_node())
