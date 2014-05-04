#import Cl_Network_Control
#import Cl_Decisions
import List_Explicit_Values
import Control_Algos.Algorithm_FT_Control as Algorithm_FT_Control


#method returning a list [ list_intersection_control_objects, t_end_cycle,t_cycle_duration,t_end_current sequence_ncm, type of next control=1]
#val_li_param_ft_offset_ctrl=[ ...[id stage to actuate, actuation duration,cycle duration],...]
#val_dic_inters_control_matrix=dict, key-id phase of the intersection, value=0
#val_dic_intersection_stages=dict, key=id stage, value=[ [id phase i to actuate],[id phase j to actuate],...]
#During the first cycle we apply  the FT control with the offsets (extended cycle) and during the next cycles a FT control is employed.
def admissible_intersection_control_objects_next_cycle_ft_offset(\
val_li_param_ft_offset_ctrl,val_dic_inters_control_matrix,val_dic_intersection_stages,\
val_t_end_current_inters_control,val_ti_unit,val_ti_round_prec,v_val_dt):

	#print("val_li_param_ft_offset_ctrl",val_li_param_ft_offset_ctrl)

	#list of [list_intersection_control_objects, t_end_cycle,t_cycle_duration,t_end_current sequence_ncm, type of next control=1]
	rep=Algorithm_FT_Control.admissible_intersection_control_objects_next_cycle_ft(\
	val_li_param_ft_ctrl=val_li_param_ft_offset_ctrl,val_di_inters_control_matrix=val_dic_inters_control_matrix,\
	val_di_intersection_stages=val_dic_intersection_stages,\
	val_t_end_current_intersection_control=val_t_end_current_inters_control,\
	val_t_unit=val_ti_unit,val_t_round_prec=val_ti_round_prec,val_dt=v_val_dt)	
	
	
	#print(val_li_param_ft_offset_ctrl)
	#import sys
	#sys.exit()
	#we calculate the cycle duration after the offeset
	#cycle_dur=0
	#for i in val_li_param_ft_offset_ctrl:
		#cycle_dur+=i[1]
	#rep[2]=cycle_dur	
	return rep
	
#*****************************************************************************************************************************************************************************************
#import Cl_Creation_Network

#cr_nt= Cl_Creation_Network.Creation_Network(val_file_name_user_data="Dsu_1")
#network=cr_nt.function_creation_network()

#print("NB LINKS DICT:",network.get_di_all_links().keys())
#re=admissible_network_control_objects_next_cycle(val_di_id_all_links=network.get_di_all_links(),val_t_end_current_network_control_matrix=0,val_li_dur_each_ncm=[2,2,30],\
#li_phases_actuated_each_nco=[ [ [1,3], [2,3] ], [[3,4],  [8,9], [7,8],[12,8] ]  ])

#print(len(re))
#print("t_end_cycle",re[1],"cycle dur:",re[2])


#for i in re[0]:
	#print("Control ",i.get_di_network_control_mat(),"T strt control",i.get_t_start_control(),"Duration Control",i.get_t_duration_control())






































