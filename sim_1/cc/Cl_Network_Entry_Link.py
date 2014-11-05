import Cl_Network_Link
import Cl_Set_Vehicle_Queues_Link
import List_Explicit_Values

#TYPE_NETWORK_ENTRY_LINK={"signalised_entry_link":1,"non_signalised_entry_link":0}
TYPE_ROUTING_NETWORK_ENTRY_LINK_WHEN_MIXED_MANAGEMENT={\
"od_and_initial_given_path_when_mixed_manag":1,"od_and_dynamically_defined_path_when_mixed_manag":2}

class Network_Entry_Link(Cl_Network_Link.Network_Link):

	"""class defining a network entry link bringing vehicles into network.  There are no input links to an entry link"""
	
	def __init__(self,val_id_lnk=-1,val_li_id_output_links_from_lnk=[],val_set_vehicle_que=None,val_length_lnk=-1,\
	val_capacity_lnk=-1,val_id_head_intersection_nd=-1,val_li_id_sublks=[],val_fct_creating_demand_entry_link=None,\
	val_lis_parameters_fct_creating_demand_entry_link=[],val_type_entry_link=1,val_li_output_lks_queues=None,\
	val_type_routing_entry_lk_when_mixed_management=-1,val_demand_variation_actuate_obj=None):
	
		Cl_Network_Link.Network_Link.__init__(self,val_id_nwlink=val_id_lnk,val_li_id_output_links_from_nwlink=val_li_id_output_links_from_lnk,\
		val_set_vehicle_queue_nwlink=val_set_vehicle_que,val_length_nwlink=val_length_lnk,val_capacity_nwlink=val_capacity_lnk,\
		val_type_network_link=Cl_Network_Link.TYPE_NETWORK_LINK["entry"],val_id_head_intersection_node=val_id_head_intersection_nd,\
		val_lis_output_links_queues=val_li_output_lks_queues)
		
		#the function generating the demand of the entry link (nb veh /time unit)
		self._fct_creating_demand_entry_link=val_fct_creating_demand_entry_link
		
		
		
		#the list of the parameters of the function creating the demand
		self._lis_parameters_fct_creating_demand_entry_link=val_lis_parameters_fct_creating_demand_entry_link 
		
		#the type of the routing  of an entry link when a mixed rout management is employed
		self._type_routing_entry_lk_when_mixed_management=val_type_routing_entry_lk_when_mixed_management
		
		
		#the list with the param of the demand  when the time and demand variate, val_li_param_when_demand_variate=[....,[t,demand param],...]
		#self._li_param_when_demand_variate=val_li_param_when_demand_variate
		
		#an object for selecting the algorthm computing the demand 
		self._demand_variation_actuate_obj=val_demand_variation_actuate_obj
		
		
		#the number of vehicles appeared at this entry link, initialised at zero and updated after every new vehicle appearance
		#self._nb_vehicle_appearance_at_entry_link=List_Explicit_Values.initialisation_value_to_zero
		
		#the type of the entry link
		#self._type_entry_link=val_type_entry_link
		
#*****************************************************************************************************************************************************************************************
	#method returning the function generating the demand  of the entry link
	def get_fct_creating_demand_entry_link(self):
		return self._fct_creating_demand_entry_link

#*****************************************************************************************************************************************************************************************
	#method returning the list of the parameters of the function creating the demand
	def get_lis_parameters_fct_creating_demand_entry_link(self):
		return self._lis_parameters_fct_creating_demand_entry_link
#*****************************************************************************************************************************************************************************************
	#method returning the number of vehicles appeared at this entry link, initialised at zero and updated after every new vehicle appearance
	def get_nb_vehicle_appearance_at_entry_link(self):
		return self._nb_vehicle_appearance_at_entry_link
#*****************************************************************************************************************************************************************************************
	#method returning the type of the routing  of an entry link when a mixed rout management is employed
	def get_type_routing_entry_lk_when_mixed_management(self):
		return self._type_routing_entry_lk_when_mixed_management

#*****************************************************************************************************************************************************************************************
	#method returning the list with the param of the demand  when the time and demand variate
	#def get_li_param_when_demand_variate(self):
		#return self._li_param_when_demand_variate

#*****************************************************************************************************************************************************************************************
	#method returning the object for selecting the algorthm computing the demand 
	def get_demand_variation_actuate_obj(self):
		return self._demand_variation_actuate_obj

#*****************************************************************************************************************************************************************************************
	#method returning the type  of the entry link
	#def get_type_entry_link(self):
		#return self._type_entry_link
#*****************************************************************************************************************************************************************************************
	#method modifying  the function generating the demand  of the entry link
	def set_fct_creating_demand_entry_link(self,n_v):
		self._fct_creating_demand_entry_link=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the list of the parameters of the function creating the demand
	def set_lis_parameters_fct_creating_demand_entry_link(self,n_v):
		self._lis_parameters_fct_creating_demand_entry_link=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the number of vehicles appeared at this entry link, initialised at zero and updated after every new vehicle appearance
	def set_nb_vehicle_appearance_at_entry_link(self,n_v):
		self._nb_vehicle_appearance_at_entry_link=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the type  of the entry link
	def set_type_entry_link(self,n_v):
		self._type_entry_link=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the type of the routing  of an entry link when a mixed rout management is employed
	def set_type_routing_entry_lk_when_mixed_management(self,n_v):
		self._type_routing_entry_lk_when_mixed_management=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the list with the param of the demand  when the time and demand variate
	#def set_li_param_when_demand_variate(self,n_v):
		#self._li_param_when_demand_variate=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the object for selecting the algorthm computing the demand 
	def set_demand_variation_actuate_obj(self,n_v):
		self._demand_variation_actuate_obj=n_v

#*****************************************************************************************************************************************************************************************
	#method creating the demand of the entry link
	def fct_creating_demand_entry_link(self):
		self._demand_entry_link=self._fct_creating_demand_entry_link(*self._lis_parameters_fct_creating_demand_entry_link)
		return self._demand_entry_link

#*****************************************************************************************************************************************************************************************

	#method increasing  the number of vehicles appearing in this link
	def fct_increasing_nv_veh_appearances_at_entry_link(self,value=List_Explicit_Values.initialisation_value_to_one):
	
		self._nb_vehicle_appearance_at_entry_link+=value
	

#*****************************************************************************************************************************************************************************************
		
#ex

#set_v_q=Cl_Set_Vehicle_Queues_Link.Set_Vehicle_Queues_Link(val_id_assoc_link=1,val_nb_leaving_nodes_from_head_nd_link=3,\
#val_index_queue=1)

#lk=Network_Entry_Link(val_id_lik=9,val_set_vehicle_que=set_v_q,val_id_head_intersection_nd=23)


#print("ID LINK, TYPE LINK, TYPE NETWORK LINK, ID HEAD INTERSECTION NODE,LIST ID SUBLINKS, ID VEH QUEUE: ",\
#lk.get_id_link(),lk.get_type_link(),lk.get_type_network_link(),lk.get_id_head_intersection_node(),\
#lk.get_li_id_sublinks(),len(lk.get_set_veh_queue().get_li_obj_veh_queue_at_link()))