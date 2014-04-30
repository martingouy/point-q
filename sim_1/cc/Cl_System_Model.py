import Global_Functions
#import Cl_Intersection_Control_Matrices


class System_Model:

	def __init__(self):
		pass
#*****************************************************************************************************************************************************************************************

#method creating a dicitonary with the intersection controls for all the intersection nodes
#key=id intersection node,  value= dict, key=id phase, value=0
def fct_creation_di_all_intersection_stages(val_di_intersections):

	di_rep={}
	for i in val_di_intersections:
		di_rep[i]=val_di_intersections[i].fct_creat_di_key_id_phase_value_zero()
	return di_rep


#*****************************************************************************************************************************************************************************************
#method creating a dictionary: key =id intersection node, value= the intersection control object (intersection control matrix initialised à 0)
#def fct_creat_di_id_intersecton_nd_value_intersection_control_obj(val_di_intersections):
	#di_rep={}
	f#or i in val_di_intersections:
	

#*****************************************************************************************************************************************************************************************