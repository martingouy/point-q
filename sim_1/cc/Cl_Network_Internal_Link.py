import Cl_Network_Link
import Cl_Set_Vehicle_Queues_Link

class Network_Internal_Link(Cl_Network_Link.Network_Link):

	"""class defining an internal link of the network. An internal link has both input and output links and consequently head and tail nodes. """

	def __init__(self,val_id_lnk=-1,val_li_id_input_links_to_lnk=[],val_li_id_output_links_from_lnk=[],\
	val_set_vehicle_que=None,val_length_lnk=-1,val_capacity_lnk=-1,\
	val_id_head_intersection_nd=-1,val_id_tail_intersection_nd=-1,\
	val_param_lk_travel_duration=None,val_li_output_lks_queues=None):
	
	
		Cl_Network_Link.Network_Link.__init__(self,val_id_nwlink=val_id_lnk,val_li_id_input_links_to_nwlink=val_li_id_input_links_to_lnk,\
		val_li_id_output_links_from_nwlink=val_li_id_output_links_from_lnk,
		val_set_vehicle_queue_nwlink=val_set_vehicle_que,\
		val_length_nwlink=val_length_lnk,val_capacity_nwlink=val_capacity_lnk,\
		val_type_network_link=Cl_Network_Link.TYPE_NETWORK_LINK["internal"],\
		val_id_head_intersection_node=val_id_head_intersection_nd,\
		val_id_tail_intersection_node=val_id_tail_intersection_nd,\
		val_param_link_travel_duration=val_param_lk_travel_duration,\
		val_lis_output_links_queues=val_li_output_lks_queues)
#*****************************************************************************************************************************************************************************************

#
#ex

#set_v_q=Cl_Set_Vehicle_Queues_Link.Set_Vehicle_Queues_Link(val_id_assoc_link=1,val_nb_leaving_nodes_from_head_nd_link=3,\
#val_index_queue=1)

#lk=Network_Internal_Link(val_id_lik=9,val_set_vehicle_que=set_v_q,val_id_head_intersection_nd=12,val_id_tail_intersection_nd=23)


#print("ID LINK, TYPE LINK, TYPE NETWORK LINK, ID TAIL INTERSECTION NODE,LIST ID SUBLINKS, ID VEH QUEUE: ",\
#lk.get_id_link(),lk.get_type_link(),lk.get_type_network_link(),lk.get_id_tail_intersection_node(),\
#lk.get_li_id_sublinks(),len(lk.get_set_veh_queue().get_li_obj_veh_queue_at_link()))