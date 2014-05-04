
class Node:

	def __init__(self,val_id_node=-1):
		
		#the node id
		self._id_node=val_id_node
		
#*****************************************************************************************************************************************************************************************
	#method returning the node id
	def get_id_node(self):
		return self._id_node
#*****************************************************************************************************************************************************************************************	
	#method modifying the node type
	def set_type_node(self,n_v):
		self._type_node=n_v
#*****************************************************************************************************************************************************************************************

#ex
#nd=Node(val_id_node=2)	
#print("ID-TYPE ND BEFORE:",nd.get_id_node())

#nd.set_type_node(TYPE_NODE["internal_link_node"])

#print("ID-TYPE ND AFTER:",nd.get_id_node(),nd.get_type_node())