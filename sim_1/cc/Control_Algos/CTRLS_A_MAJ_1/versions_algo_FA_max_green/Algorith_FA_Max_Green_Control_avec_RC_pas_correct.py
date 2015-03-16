import List_Explicit_Values
import Cl_Intersection_Control
import Cl_Control_Actuate


#method returning the  sum of product que length x sat flow of all the  queues of a given stage
def fct_calcul_product_que_and_sat_flow_single_stage(v_va_intersection,v_va_stage,v_va_network,v_va_round_precis):

	som=0

	#par example un inters stage [[7,8],[9,10]] actual simult phases [7,8] et [9,10]
	for i in v_va_stage:
		#pour chaque que de l'input link du stage
		for k in v_va_network.get_di_entry_internal_links()[i[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link():
		
			#prod=queue length * sat flow of the queue
			prod=len(v_va_network.get_di_entry_internal_links()[i[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
			[k[0],k[1]].get_queue_veh())*v_va_network.get_di_entry_internal_links()[i[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
			[k[0],k[1]].get_sat_flow_queue()
			
			
			
			#on somme les prod de toutes les queues de tous les  input links du stage
			som+=prod
			
	#print()
	#sort of pressure exerted by  the stage	
	som_1=round(som,v_va_round_precis)
	#if va_intersection.get_id_node()==2:
		#print("prod", prod,"som",som,som_1)
		#print()
	return som_1
#*****************************************************************************************************************************************************************************************
#method selecting an  intersection stage amongst all the possible stages
def fct_select_intersection_FA_stage_amongst_all_stages(va_intersection,va_network,va_round_precis,va_init_small_val):

	#id stages possibles
	li_id_stages_inersection=list(va_intersection.get_di_stages_sign_intersection().keys())
	
	
	#initialisation du stage consideree
	fa_pressure_inters_cm=None
	
	#initialisation de la pression exercee
	pressure_exerted=va_init_small_val
	
	#l'indice du stage selectionne
	id_stage=-1
	
	#for each possible stage of the intersection, dict=id stage, value=[... ,id simult compatible phases,... ]
	for i in li_id_stages_inersection:
	
		#on calcule  la pression exercee par le stage en question
		current_exerted_pression=fct_calcul_product_que_and_sat_flow_single_stage(v_va_intersection=va_intersection,\
		v_va_stage=va_intersection.get_di_stages_sign_intersection()[i],v_va_network=va_network,v_va_round_precis=va_round_precis)
		
		
		if current_exerted_pression>pressure_exerted:
		
			pressure_exerted=current_exerted_pression
			
			fa_pressure_inters_cm=va_intersection.get_di_stages_sign_intersection()[i]
			
			id_stage=i
	

	return [fa_pressure_inters_cm,id_stage]

#*****************************************************************************************************************************************************************************************
#method selecting a  different intersection stage, from the currently employed  one, (case when the continuously permitted actuation duration is exceeded)
def fct_select_different_intersection_FA_stage(va_intersection,va_network,va_round_precis,va_init_small_val):
	

	#id stages possibles
	li_id_stages_inersection_1=list(va_intersection.get_di_stages_sign_intersection().keys())
	#if va_inters.get_id_node()==2:
		#print(li_id_stages_inersection)
		
	#on enleve le id du stage courant, et on a la liste des stage candidats
	li_id_stages_inersection=list(li_id_stages_inersection_1)
	li_id_stages_inersection.remove(va_intersection.get_intersection_control_obj().get_id_actuated_stage())
	
	
	#initialisation du stage considere
	fa_pressure_inters_cm=None
	
	#initialisation de la pression exercee
	pressure_exerted=va_init_small_val
	
	#l'indice du stage selectionne
	id_stage=-1
	
	#for each possible stage of the intersection, dict=id stage, value=[... ,id simult compatible phases,... ]
	for i in li_id_stages_inersection:
	
		#on calcule  la pression exercee par le stage en question
		current_exerted_pression=fct_calcul_product_que_and_sat_flow_single_stage(v_va_intersection=va_intersection,\
		v_va_stage=va_intersection.get_di_stages_sign_intersection()[i],v_va_network=va_network,v_va_round_precis=va_round_precis)
		
		
		if current_exerted_pression>pressure_exerted:
		
			pressure_exerted=current_exerted_pression
			
			fa_pressure_inters_cm=va_intersection.get_di_stages_sign_intersection()[i]
			
			id_stage=i
	

	return [fa_pressure_inters_cm,id_stage]

#*****************************************************************************************************************************************************************************************

#method selecting the stage with the higher som of prodcuts queue length x sat flow
#it returns [fa_pressure_inters_cm,id_stage]
def fct_select_intersection_stage_with_max_prod(va_t_actuel,va_inters,va_netw,va_round_precision,va_dt,va_initial_small_val):
	
	#print("va_t_actue",va_t_actuel,"va_inters.get_intersection_control_obj().get_t_lim_icm()",va_inters.get_intersection_control_obj().get_t_lim_icm())

	
	#si on n'est pas en RC (RC control n'a pas de t_lim_icm, son t_lim_icm=-1, RC a seuelement duree et t_end ctrl) 
	if va_inters.get_intersection_control_obj().get_t_lim_icm()>0:
	
		#if the current time is < t_lim of the currently actuated stage, all  possible stages of the intersection will be examined
		if va_t_actuel<va_inters.get_intersection_control_obj().get_t_lim_icm():
		
	
			#rep=[fa_pressure_inters_cm,id_stage]
			rep=fct_select_intersection_FA_stage_amongst_all_stages(\
			va_intersection=va_inters,va_network=va_netw,va_round_precis=va_round_precision,va_init_small_val=va_initial_small_val)
	
	
		#if the current time is = t_lim of the currently actuated stage, the currently employed stage will not be actuated
		elif  va_t_actuel==va_inters.get_intersection_control_obj().get_t_lim_icm():
		
			#print("here3")
			
	
			#rep=[fa_pressure_inters_cm,id_stage]
			rep=fct_select_different_intersection_FA_stage(\
			va_intersection=va_inters,va_network=va_netw,va_round_precis=va_round_precision,va_init_small_val=va_initial_small_val)
			#print("rep",rep[1])
			#import sys
			#sys.exit()
	
	
		#if the current time is > t_lim PROBLEM 
		else:
			print("PROBLEME IN ALGO_FA_MAX_GREEN_CONTROL, va_t_actuel", va_t_actuel, \
			"t lim current control", va_inters.get_intersection_control_obj().get_t_lim_icm())
			import sys
			sys.exit()
		
	#si le t_lim de l'incm <0,  on est en RC
	#si on est en RC, le t_lim de l'incm <0
	elif va_inters.get_intersection_control_obj().get_t_lim_icm()<0:
	
		#rep=[fa_pressure_inters_cm,id_stage]
		rep=fct_select_intersection_FA_stage_amongst_all_stages(\
		va_intersection=va_inters,va_network=va_netw,va_round_precis=va_round_precision,va_init_small_val=va_initial_small_val)
		
	#si  t_lim de l'incm=0 PROBLEM
	else:
		print("PROBLEM DS ALGO_FA_MAX_GREEN CTRL, t_lim_icm",va_inters.get_intersection_control_obj().get_t_lim_icm())
		import sys
		sys.exit()
		
	return rep

#*****************************************************************************************************************************************************************************************
#li_param_control=[v_admissible_limit_flow, idle time, t_prem_ctrl, lim actuat duration]
#on retourne [li_ico, List_Explicit_Values.initialisation_value_to_eleven, 1 ou 0 according as if an event end_next_decision control will be/not generated]
def admissible_intersection_control_object_fa_max_green(t_actuel,v_intersection,v_network,li_param_control,v_t_unit,v_round_prec,\
v_t_round_precision,v_dt,v_init_small_val=-10**10):


	#si on commence la sim on le ctrl sera 1 pour le premier stage par defaut,
	if t_actuel==li_param_control[2]:
		
	
		li_id_stages=list(v_intersection.get_di_stages_sign_intersection().keys())
		
		id_stage=li_id_stages[0]
		
		#inter control matrix
		icm=dict(v_intersection.get_di_intersection_control_matrix())
	
		#on initiliase a un chaque phase que le stage selectionne  actualise
		for i in  v_intersection.get_di_stages_sign_intersection()[id_stage]:
			icm[i[0],i[1]]=1
		
		#if v_intersection.get_id_node()==2:
			#print(icm)
			#import sys
			#sys.exit()
			
				
		#li_param_control=[v_admissible_limit_flow, idle time, t_prem_ctrl, lim actuat duration]
		#on definit le temps limite du stage
		t_lim_permitted=round(t_actuel+li_param_control[3]-v_t_unit,v_t_round_precision)
		
		#creation d'un objet intersection control, pour la RC, de duree li_param_control[2]
		inters_control_obj=Cl_Intersection_Control.Intersection_Control(\
		val_di_intersection_control_mat=icm,\
		val_t_start_control= t_actuel,\
		val_t_end_control=t_lim_permitted,\
		val_duration_control=li_param_control[3],\
		val_type_control=Cl_Control_Actuate.TYPE_CONTROL[11],\
		val_t_lim_icm=t_lim_permitted,\
		val_id_actuated_stage=id_stage)
		
		return[[inters_control_obj], List_Explicit_Values.initialisation_value_to_eleven, List_Explicit_Values.initialisation_value_to_one]
	
	#si on ne commence pas la sim, li_param_control=[v_admissible_limit_flow, idle time, t_prem_ctrl, lim actuat duration]
	elif t_actuel>li_param_control[2]:
	
		#choix du stage, rep=[fa_stage,id_stage]
		rep=fct_select_intersection_stage_with_max_prod(\
		va_t_actuel=t_actuel,\
		va_inters=v_intersection,va_netw=v_network,\
		va_round_precision=v_round_prec,\
		va_dt=v_dt,\
		va_initial_small_val=v_init_small_val)
		
		#inter control matrix
		icm=dict(v_intersection.get_di_intersection_control_matrix())
			
		#on initiliase a un chaque phase que le mp stage actualise
		for i in rep[0]:
			icm[i[0],i[1]]=1
			
		#si on est en red clear, on cree directement le  control sans  nouveaux ctrl pour RC
		if v_intersection.get_intersection_control_obj().get_type_control()==Cl_Control_Actuate.TYPE_CONTROL[0]:
		
			t_start=round(t_actuel+v_t_unit,v_t_round_precision)
			
			#on calcul le t_lim perm du stage
			t_lim_perm= round(t_actuel+li_param_control[3]-v_t_unit,v_t_round_precision)
			
			#creation d'un objet intersection control
			inters_control_obj_fa=Cl_Intersection_Control.Intersection_Control(\
			val_di_intersection_control_mat=icm,\
			val_t_start_control= t_start, \
			val_t_end_control=t_lim_perm,\
			val_duration_control=li_param_control[3],\
			val_type_control=Cl_Control_Actuate.TYPE_CONTROL[11],\
			val_t_lim_icm=t_lim_perm,val_id_actuated_stage=rep[1])
			
			return[[inters_control_obj_fa], List_Explicit_Values.initialisation_value_to_eleven,List_Explicit_Values.initialisation_value_to_one]
		
		#si on n'est pas en red clear
		else:
			#si on a choisi le meme stage que actuel applique, on  ne cree pas de RC
			if rep[1]==v_intersection.get_intersection_control_obj().get_id_actuated_stage():
				
				t_start=round(t_actuel+v_t_unit,v_t_round_precision)
				
				#creation d'un objet intersection control
				inters_control_obj_fa=Cl_Intersection_Control.Intersection_Control(\
				val_di_intersection_control_mat=icm,\
				val_t_start_control= t_start, \
				val_t_end_control=v_intersection.get_intersection_control_obj().get_t_lim_icm(),\
				val_duration_control=li_param_control[3],\
				val_type_control=Cl_Control_Actuate.TYPE_CONTROL[11],\
				val_t_lim_icm=v_intersection.get_intersection_control_obj().get_t_lim_icm(),\
				val_id_actuated_stage=v_intersection.get_intersection_control_obj().get_id_actuated_stage())
				
				return[[inters_control_obj_fa], List_Explicit_Values.initialisation_value_to_eleven, List_Explicit_Values.initialisation_value_to_zero]
			
			#si on a choisi un autre stage, on va creer une matrice RC
			else:
				#le temps auquel RC commencera
				t_st=round(t_actuel+v_t_unit,v_t_round_precision)
				
				#temps fin RC
				#li_param_control=[v_admissible_limit_flow, idle time, t_prem_ctrl, lim actuat duration]
				t_end_current_icm_rc=round(t_st+li_param_control[1]-v_t_unit,v_t_round_precision)
				
				
				#creation d'un objet intersection control, pour la RC,
				inters_control_obj_rc=Cl_Intersection_Control.Intersection_Control(\
				val_di_intersection_control_mat=v_intersection.get_di_intersection_control_matrix(),\
				val_t_start_control= t_st,\
				val_t_end_control=t_end_current_icm_rc,\
				val_duration_control=li_param_control[1],\
				val_type_control=Cl_Control_Actuate.TYPE_CONTROL[0])
				
				#le temps auquel le ctrl  va commencer
				t_start=round(t_end_current_icm_rc+v_t_unit,v_t_round_precision)
				
				# li_param_control=[v_admissible_limit_flow, idle time, t_prem_ctrl, lim actuat duration]
				#on calcul le t_lim permis du nouveau stage
				t_lim_perm= round(t_start+li_param_control[3]-v_t_unit,v_t_round_precision)
				
				#creation d'un objet intersection control
				inters_control_obj_fa=Cl_Intersection_Control.Intersection_Control(\
				val_di_intersection_control_mat=icm,val_t_start_control= t_start, \
				val_t_end_control=t_lim_perm,\
				val_duration_control=li_param_control[3],\
				val_type_control=Cl_Control_Actuate.TYPE_CONTROL[11],\
				val_t_lim_icm=t_lim_perm,\
				val_id_actuated_stage=rep[1])
		
				li_ico=[inters_control_obj_rc,inters_control_obj_fa]
		
				return[li_ico, List_Explicit_Values.initialisation_value_to_eleven,List_Explicit_Values.initialisation_value_to_one]
				
#*****************************************************************************************************************************************************************************************








