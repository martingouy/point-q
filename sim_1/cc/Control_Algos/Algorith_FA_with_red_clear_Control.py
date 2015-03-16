#import Cl_Network_Control
#import Cl_Decisions
import List_Explicit_Values
import Cl_Intersection_Control
import Cl_Control_Actuate

#*****************************************************************************************************************************************************************************************

#method returning the  sum of product que length x sat flow of all the  queues of a stage
def fct_select_product_que_and_sat_flow_single_stage(va_intersection,va_stage,va_network,va_round_precis):

	som=0

	#par example un inters stage [[7,8],[9,10]] actaul simult phases [7,8] et [9,10]
	for i in va_stage:
	
		#if va_intersection.get_id_node()==1 and va_stage[0][0]==4 and va_stage[0][1]==5:
			#print(i)
		#for each queue actuated by the stage, on calcule le produit  queue length x sat flow of the queue
		
		
		#prod=queue length * sat flow of the queue
		prod=len(va_network.get_di_entry_internal_links()[i[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[i[0],i[1]].get_queue_veh())*va_network.get_di_entry_internal_links()[i[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[i[0],i[1]].get_sat_flow_queue()
		
		#if va_intersection.get_id_node()==1 and va_stage[0][0]==4 and va_stage[0][1]==5:
			#print("length",len(va_network.get_di_entry_internal_links()[i[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
			#[i[0],i[1]].get_queue_veh()),"sat flow",va_network.get_di_entry_internal_links()[i[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
			#[i[0],i[1]].get_sat_flow_queue(),"prod",prod)
		
		#on somme les prod of all the queues of all the input links du stage
		som+=prod
		
		#if va_intersection.get_id_node()==1 and va_stage[0][0]==4 and va_stage[0][1]==5:
			#print("som",som)
			
	#print()
	
	#pressure exerted by  the stage	
	som_1=round(som,va_round_precis)
	
	#if va_intersection.get_id_node()==1 and va_stage[0][0]==4 and va_stage[0][1]==5:
		#print("prod", prod,"som",som,som_1)
		#print()
		
	return som_1
#*****************************************************************************************************************************************************************************************
#method selecting the stage with the higher som of prodcuts queue length x sat flow
def fct_select_intersection_stage_with_max_prod(va_inters,va_netw,va_round_precision,va_init_small_val):


	#id stages possibles
	li_id_stages_inersection=list(va_inters.get_di_stages_sign_intersection().keys())
		
	
	#initialisation de la matrice consideree
	fa_pressure_inters_cm=va_inters.get_di_stages_sign_intersection()[li_id_stages_inersection[0]]
	
	#initialisation de la pression exercee
	pressure_exerted_fa=va_init_small_val
	
	#l'indice du stage selectionne
	id_stage=-1
	
	#for each possible stage of the intersection, dict=id stage, value=[... ,id simult compatible phases,... ]
	for i in li_id_stages_inersection:
	
		if va_inters.get_id_node()==1:
			print("on examine stage ", i)
		#on calcule  la pression exercee par le stage en question
		current_exerted_pression_fa=fct_select_product_que_and_sat_flow_single_stage(va_intersection=va_inters,\
		va_stage=va_inters.get_di_stages_sign_intersection()[i],va_network=va_netw,va_round_precis=va_round_precision)
		
		if current_exerted_pression_fa>pressure_exerted_fa:
		
			pressure_exerted_fa=current_exerted_pression_fa
			
			fa_pressure_inters_cm=va_inters.get_di_stages_sign_intersection()[i]
			
			id_stage=i
		#if va_inters.get_id_node()==2:
			#print("i",i,"current_exerted_pression",current_exerted_pression,"pressure_exerted",pressure_exerted)
			#print()
	
	return [fa_pressure_inters_cm,id_stage]

#*****************************************************************************************************************************************************************************************

#li_param_control=[v_admissible_limit_flow, idle time, t_prem_ctrl_start_sim]
#it returns  [li ico, type of  next control,  0 to indicate that no even end decis will be genereted by en even end dec]
#the type of ctrl shoul dbe indicated in this algo
def admissible_intersection_control_object_fa_with_rc(t_actuel,v_intersection,v_network,li_param_control,v_sim_dur,v_t_unit,v_t_round_prec,\
v_init_small_val=-10**10):

	
	
	#si on commence la sim on le ctrl sera 1 pour le premier stage,
	if t_actuel==li_param_control[2]:
		
	
		li_id_stages=list(v_intersection.get_di_stages_sign_intersection().keys())
		
		id_stage=li_id_stages[0]
		
		
		#inter control matrix
		icm=dict(v_intersection.get_di_intersection_control_matrix())
	
		#on initiliase a un chaque phase que le stage selectionne  actualise
		for i in  v_intersection.get_di_stages_sign_intersection()[id_stage]:
			icm[i[0],i[1]]=1
		
		t_start=round(t_actuel+v_t_unit,v_t_round_prec)
		#if v_intersection.get_id_node()==2:
			#print(icm)
			#import sys
			#sys.exit()
		t_end_ctrl=round(v_sim_dur+t_actuel,v_t_round_prec)
		
		
		#creation d'un objet intersection control, pour la RC, de duree li_param_control[2]
		inters_control_obj=Cl_Intersection_Control.Intersection_Control(\
		val_di_intersection_control_mat=icm,\
		val_t_start_control= t_start,\
		val_t_end_control=t_end_ctrl,\
		val_duration_control=v_sim_dur,\
		val_type_control=Cl_Control_Actuate.TYPE_CONTROL[12],\
		val_id_actuated_stage=id_stage)
		
		return[[inters_control_obj], List_Explicit_Values.initialisation_value_to_twelve,List_Explicit_Values.initialisation_value_to_zero]
	
	#si on ne commence pas la sim, li_param_control=[v_admissible_limit_flow, idle time, t_prem_ctrl]
	elif t_actuel>li_param_control[2]:
		
		#on selectionne le stage, fa_stage= [fa_pressure_inters_cm,id_stage]
		fa_stage=fct_select_intersection_stage_with_max_prod(va_inters=v_intersection,va_netw=v_network,\
		va_round_precision=v_t_round_prec,va_init_small_val=v_init_small_val)
		
			
		#si on n'est pas en red clear
		if v_intersection.get_intersection_control_obj().get_type_control()!=Cl_Control_Actuate.TYPE_CONTROL[0]:
			#si le stage selectionne est different  of the currently emloyed stage
			if fa_stage[1]!=v_intersection.get_intersection_control_obj().get_id_actuated_stage():
			
				t_st=round(t_actuel+v_t_unit,v_t_round_prec)
				#li_param_control=[v_admissible_limit_flow, idle time, t_prem_ctrl]
				t_end_current_icm_rc=round(t_st+li_param_control[1]-v_t_unit,v_t_round_prec)
				
				#creation d'un objet intersection control, pour la RC,
				inters_control_obj_rc=Cl_Intersection_Control.Intersection_Control(\
				val_di_intersection_control_mat=v_intersection.get_di_intersection_control_matrix(),\
				val_t_start_control= t_st,\
				val_t_end_control=t_end_current_icm_rc,\
				val_duration_control=li_param_control[1],\
				val_type_control=Cl_Control_Actuate.TYPE_CONTROL[0],\
				val_id_actuated_stage=0)
				
				#inter control matrix
				icm=dict(v_intersection.get_di_intersection_control_matrix())
			
				#on initiliase a un chaque phase que le mp stage actualise
				for i in fa_stage[0]:
					icm[i[0],i[1]]=1
					
				t_start=round(t_end_current_icm_rc+v_t_unit,v_t_round_prec)
				t_end=round(t_start+v_sim_dur-v_t_unit,v_t_round_prec)
				
				#creation d'un objet intersection control
				inters_control_obj_fa=Cl_Intersection_Control.Intersection_Control(\
				val_di_intersection_control_mat=icm,val_t_start_control= t_start, \
				val_t_end_control=t_end,\
				val_duration_control=v_sim_dur,\
				val_type_control=Cl_Control_Actuate.TYPE_CONTROL[12],\
				val_id_actuated_stage=fa_stage[1])
				
				li_ico=[inters_control_obj_rc,inters_control_obj_fa]
				
				return[li_ico, List_Explicit_Values.initialisation_value_to_twelve,List_Explicit_Values.initialisation_value_to_zero]
			#if the selected stage is the current one 
			else:
				#t_start=round(t_actuel+v_t_unit,v_t_round_prec)
				#t_end=round(t_start+v_sim_dur-v_t_unit,v_t_round_prec)
				t_end=round(t_actuel+v_sim_dur-v_t_unit,v_t_round_prec)
				
				#creation d'un objet intersection control
				inters_control_obj_fa=Cl_Intersection_Control.Intersection_Control(\
				val_di_intersection_control_mat=v_intersection.get_intersection_control_obj().get_di_intersection_control_mat(),\
				val_t_start_control= t_actuel, \
				val_t_end_control=t_end,\
				val_duration_control=v_sim_dur,\
				val_type_control=Cl_Control_Actuate.TYPE_CONTROL[12],\
				val_id_actuated_stage=fa_stage[1])
				
				
				return[[inters_control_obj_fa], List_Explicit_Values.initialisation_value_to_twelve,List_Explicit_Values.initialisation_value_to_zero]
				
		#si on est en red clear
		else:
			print("PROBLEM IN ALGO FA WITH RED CLEAR, CURRENT STAGE IS RED CLEAR, TYPE CTRL :",v_intersection.get_intersection_control_obj().get_type_control())
			import sys
			sys.exit()	
	else:
		print("PROBLEM DS ALGORITHM_FA_CONTROL, t_act, t_first_ctrl", t_actuel,li_param_control[2])
		import sys
		sys.exit()

				
#*****************************************************************************************************************************************************************************************
