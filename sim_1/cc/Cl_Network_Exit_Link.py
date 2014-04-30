import Cl_Network_Link
import Cl_Set_Vehicle_Queues_Link

class Network_Exit_Link(Cl_Network_Link.Network_Link):

	"""class defining an  exit link. It extracts vehicles from the network. There are no output links from an exit link."""

	def __init__(self,val_id_lnk=-1,val_li_id_input_links_to_lnk=[],val_length_lnk=-1,val_capacity_lnk=None,\
	val_id_tail_intersection_nd=-1,val_li_id_sublks=[]):
	
		Cl_Network_Link.Network_Link.__init__(self,val_id_nwlink=val_id_lnk,val_li_id_input_links_to_nwlink=val_li_id_input_links_to_lnk,\
		val_length_nwlink=val_length_lnk,val_capacity_nwlink=val_capacity_lnk,\
		val_type_network_link=Cl_Network_Link.TYPE_NETWORK_LINK["exit"],val_id_tail_intersection_node=val_id_tail_intersection_nd)
	
		
#*****************************************************************************************************************************************************************************************

#ex

#set_v_q=Cl_Set_Vehicle_Queues_Link.Set_Vehicle_Queues_Link(val_id_assoc_link=1,val_nb_leaving_nodes_from_head_nd_link=3,\
#val_index_queue=1)

#lk=Network_Exit_Link(val_id_lik=9,val_set_vehicle_que=set_v_q,val_id_tail_intersection_nd=23)


#print("ID LINK, TYPE LINK, TYPE NETWORK LINK, ID TAIL INTERSECTION NODE,LIST ID SUBLINKS, ID VEH QUEUE: ",\
#lk.get_id_link(),lk.get_type_link(),lk.get_type_network_link(),lk.get_id_tail_intersection_node(),\
#lk.get_li_id_sublinks(),len(lk.get_set_veh_queue().get_li_obj_veh_queue_at_link()))

