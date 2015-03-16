import Cl_Intersection_Control
import Cl_Network_Link
import Cl_Decisions
import Cl_Control_Actuate
import List_Explicit_Values
import math
import Control_Algos.Algorithm_FT_Control as Algorithm_FT_Control
import Control_Algos.Algorithm_MP_Control as Algorithm_MP_Control


#*****************************************************************************************************************************************************************************************
#[li ico, type of  next control,  1 to indicate that an even end decis will be genereted ]
def admissible_intersection_control_object_next_period_mixed(\
v_li_param_ft_for_mixed_ctrl,v_di_inters_control_matrix,v_di_intersection_stages,\
v_t_end_current_intersection_control,val_t_unit,val_round_prec,val_t_round_prec,\
val_intersection,val_network,\
va_init_small_val=-10**10):



	#si le param de choix de la duree de mp icm est - 1:
	if val_network.get_control_actuate_obj().get_di_param_mp_for_mixed_ctrl()[val_intersection.get_id_node()][3]==-1:
	
		#on cree la suite de FT et le premier (et/ou unique ?) MP ics

		#creat the FT icm
		#li_inter_control_obj_ft=[ list_intersection_control_objects, type of next control=1]
		li_inter_control_obj_ft=Algorithm_FT_Control.admissible_intersection_control_objects_next_cycle_ft(\
		val_li_param_ft_ctrl=v_li_param_ft_for_mixed_ctrl,val_di_inters_control_matrix=v_di_inters_control_matrix,\
		val_di_intersection_stages=v_di_intersection_stages,\
		val_t_end_current_intersection_control=v_t_end_current_intersection_control,val_t_unit=val_t_unit,\
		val_t_round_prec=val_t_round_prec)
	
		#liste de FT inters control objets (red clear inclus)
		li_inter_control_obj_ft_for_mixed=li_inter_control_obj_ft[0]
	
		t_end_ft_controls=li_inter_control_obj_ft_for_mixed[len(li_inter_control_obj_ft_for_mixed)-1].get_t_end_control()
	
		li_inter_control_obj_mp=Algorithm_MP_Control.admissible_intersection_control_object_next_period_mp(\
		v_intersection=val_intersection,v_network=val_network,\
		di_param_control=val_network.get_control_actuate_obj().get_di_param_mp_for_mixed_ctrl(),\
		v_round_prec=val_round_prec,\
		v_t_round_prec=val_t_round_prec,\
		v_t_end_current_network_control_matrix=t_end_ft_controls,\
		v_t_unit=val_t_unit,v_init_small_val=va_init_small_val)
	
	
		li_inter_control_obj=li_inter_control_obj_ft_for_mixed
		li_inter_control_obj.extend(li_inter_control_obj_mp[0])
	
	
	#si l'indice de choix de la duree de mp icm est  different - 1:
	else:
		li_inter_control_obj_mp=Algorithm_MP_Control.admissible_intersection_control_object_next_period_mp(\
		v_intersection=val_intersection,v_network=val_network,\
		di_param_control=val_network.get_control_actuate_obj().get_di_param_mp_for_mixed_ctrl(),\
		v_round_prec=val_round_prec,\
		v_t_round_prec=val_t_round_prec,\
		v_t_end_current_network_control_matrix=v_t_end_current_intersection_control,\
		v_t_unit=val_t_unit,v_init_small_val=va_init_small_val)
	
	
		
		li_inter_control_obj=li_inter_control_obj_mp[0]
	
	#[li ico, type of  next control,  1 to indicate that an even end decis will be genereted ]
	return [li_inter_control_obj,List_Explicit_Values.initialisation_value_to_four,List_Explicit_Values.initialisation_value_to_one] 
	
	
	
	#calcul of mp icm
	


#*****************************************************************************************************************************************************************************************













