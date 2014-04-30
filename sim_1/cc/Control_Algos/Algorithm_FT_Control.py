#import Cl_Network_Control
#import Cl_Decisions
import List_Explicit_Values
import Cl_Intersection_Control
import Cl_Control_Actuate
#import Cl_Decisions

#method calculating the time at which the FT control should be updated
def fct_calcul_t_update_FT_ctrl(va_t_end_last_control_of_seq_ctrls, va_dt,va_t_round_precision):
	return round(va_t_end_last_control_of_seq_ctrls-va_dt,va_t_round_precision)

#*****************************************************************************************************************************************************************************************
#method returning a list [ list_intersection_control_objects, t_end_cycle,t_cycle_duration,t_end_current sequence_ncm, type of next control=1]
#val_li_param_ft_ctrl=[ ...[id stage to actuate, actuation duration, duration  of the following red clear matrix,cycle duration],...]
#val_ di_inters_control_matrix=dict, key=id phase of the intersection, value=0
#val_di_intersection_stages=dict, key=id stage, value=[ [id phase i to actuate],[id phase j to actuate],...]
#val_indicator_key_for_selecting_rout_prob=1or 2 for selecting the real or estimated values of the rout prob to employ at the next  decisions
##on retourne 
#[li_ico, List_Explicit_Values.initialisation_value_to_eleven=type next control to employ, 
#1 ou 0 according as if an event end_next_decision control will /not be generated,
#0 or 1 for selecting which rout prob (estimated or not) will be employed at thenext intersection cotnrol]
def admissible_intersection_control_objects_next_cycle_ft(\
val_li_param_ft_ctrl,val_di_inters_control_matrix,val_di_intersection_stages,\
val_t_end_current_intersection_control,val_t_unit,val_t_round_prec,val_dt):
#,\
#val_indicator_whether_estim_rout_prob_next_control):


	#creation of a sequecne of intersection control objects for the entire cycle
	
	li_intersection_control_obj=[]
	
	t_end=val_t_end_current_intersection_control
	
	t_start_cycle=round(t_end+val_t_unit,val_t_round_prec)
	
	
	
	
	#val_li_param_ft_ctrl=[ ...[id intersection stage to actuate, actuation duration, cycle duration],...]
	
	#print("val_li_param_ft_ctrl",val_li_param_ft_ctrl)
	for i in val_li_param_ft_ctrl:
		#print("i=",i)
		t_start=round(t_end+val_t_unit,val_t_round_prec)
		
		#print("t_end avant",t_end)
		t_end=round(t_start+i[1]-val_t_unit,val_t_round_prec)
		#print("t_end apres",t_end)
		
		di_inters_control_matrix=dict(val_di_inters_control_matrix)
		 
		#print("val_di_intersection_stages[i[0]]",val_di_intersection_stages[i[0]])
		#si stage n'est pas red clearance, on actualise la phase
		if i[0]>0:
		
			for j in val_di_intersection_stages[i[0]]:
				#print("j",j)
				di_inters_control_matrix[j[0],j[1]]=1
	
			#creation	of the intersection control
			inters_ctrl=Cl_Intersection_Control.Intersection_Control(\
			val_di_intersection_control_mat=di_inters_control_matrix,	val_t_start_control=t_start,\
			val_type_control=Cl_Control_Actuate.TYPE_CONTROL[1],\
			val_type_control_related_to_t_revision=Cl_Control_Actuate.TYPE_CONTROL_T_REVISION_CATEGORY["without_sensor_requirement_for_t_update"],\
			val_t_end_control=t_end,val_duration_control=i[1],val_t_start_cycle_associated_with_control=t_start_cycle,\
			val_cycle_duration_associated_with_control=i[2],val_estim_turn_ratios_with_current_ctrl=0,val_id_actuated_stage=i[0])
			#,\
			#val_t_update_ctrl=t_upd_ctrl)
		#si le id du stage  est zero
		elif i[0]==0:
			inters_ctrl=Cl_Intersection_Control.Intersection_Control(\
			val_di_intersection_control_mat=val_di_inters_control_matrix,val_t_start_control=t_start,\
			val_type_control=Cl_Control_Actuate.TYPE_CONTROL[0],\
			val_type_control_related_to_t_revision=Cl_Control_Actuate.TYPE_CONTROL_T_REVISION_CATEGORY["without_sensor_requirement_for_t_update"],\
			val_t_end_control=t_end,val_duration_control=i[1],val_t_start_cycle_associated_with_control=t_start_cycle,\
			val_cycle_duration_associated_with_control=i[2],val_estim_turn_ratios_with_current_ctrl=0,val_id_actuated_stage=i[0])
			#,\
			#val_t_update_ctrl=t_upd_ctrl)
		#sinon il y a un probleme,il faut arreter la sim
		else:
			print("PROBLEME DS ALGO FT CONTROL, fct admissible_intersection_control_objects_next_cycle_ft( id stage: ",i[0])
			import sys
			sys.exit()
		
		li_intersection_control_obj.append(inters_ctrl)
		
		
	#the time at which the control decision will be updated
	t_upd_ctrl=fct_calcul_t_update_FT_ctrl(va_t_end_last_control_of_seq_ctrls=t_end, va_dt=val_dt,va_t_round_precision=val_t_round_prec)
	#print(t_upd_ctrl)
	
	li_intersection_control_obj[len(li_intersection_control_obj)-1].set_t_update_ctrl(t_upd_ctrl)
	
	#we return [ list_intersection_control_objects,type of next control=1, 1 for indicating that an event end decis will be created,
	#0 or 1 for indicating whhether rout probab will be estimated at next cotnrol]
	return [li_intersection_control_obj,List_Explicit_Values.initialisation_value_to_one,List_Explicit_Values.initialisation_value_to_one,\
	List_Explicit_Values.initialisation_value_to_zero] 
	
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






































