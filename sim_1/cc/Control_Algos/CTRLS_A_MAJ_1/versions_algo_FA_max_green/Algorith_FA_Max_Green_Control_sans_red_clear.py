import List_Explicit_Values
import Cl_Intersection_Control
import Cl_Control_Actuate


#method calculating the time at which the control should be updated
def fct_calcul_t_update_ctrl_fa_mg(va_t_start_ctrl, va_max_dur,va_t_unit,va_t_round_precision):
	#return round(va_t_end_last_control_of_seq_ctrls-va_dt,va_t_round_precision)
	return round(va_t_start_ctrl+va_max_dur-va_t_unit,va_t_round_precision)
#*****************************************************************************************************************************************************************************************
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
		
	#si on a plus que un stage
	if len(li_id_stages_inersection_1)>List_Explicit_Values.initialisation_value_to_one:
	
		#on enleve le id du stage courant, et on a la liste des stage candidats
		li_id_stages_inersection=list(li_id_stages_inersection_1)
	
		li_id_stages_inersection.remove(va_intersection.get_intersection_control_obj().get_id_actuated_stage())
	
	#si on a un seul stage
	else:
		li_id_stages_inersection=list(li_id_stages_inersection_1)
		

	#initialisation du stage considere
	fa_pressure_inters_cm=None
	
	#initialisation de la pression exercee
	pressure_exerted=va_init_small_val
	
	#l'indice du stage selectionne
	id_stage=-1
	
	#print("li_id_stages_inersection",li_id_stages_inersection)
	
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
#method defining the control when it is selected amongst all stages
#v_li_param_control=[v_admissible_limit_flow, idle time, t_prem_ctrl, lim actuat duration]
def fct_define_ctrl_amongst_all_stages(t_act,v_inters,v_netw,v_li_param_ctrl,v_ti_unit,v_dt,v_round_precis,v_t_round_prec,v_initial_small_val):

	#if a ctrl currently rules the network (not beg of sim)
	if v_inters.get_intersection_control_obj()!=None:
	
		#rep=[fa_pressure_inters_cm,id_stage]
		rep=fct_select_intersection_FA_stage_amongst_all_stages(\
		va_intersection=v_inters,va_network=v_netw,va_round_precis=v_round_precis,va_init_small_val=v_initial_small_val)
	
		
		#if a different stage from the current one is been selected
		if rep[1]!=v_inters.get_intersection_control_obj().get_id_actuated_stage():
		
			#inter control matrix
			icm=dict(v_inters.get_di_intersection_control_matrix())
			
			#on initiliase a un chaque phase que le mp stage actualise
			for i in rep[0]:
				icm[i[0],i[1]]=1
				
			t_start=round(t_act+v_ti_unit,v_t_round_prec)
			
			t_end_ctrl=fct_calcul_t_update_ctrl_fa_mg(va_t_start_ctrl=t_start, va_max_dur=v_li_param_ctrl[2],va_t_unit=v_ti_unit,va_t_round_precision=v_t_round_prec)
			
			
			#the time at which the control decision will be updated
			t_upd_ctrl=t_end_ctrl
			
			#print("id current stage: ",v_inters.get_intersection_control_obj().get_id_actuated_stage(),"id selected stage:",rep[1],"t upd ctrl:",t_upd_ctrl)
			#creation d'un objet intersection control
			inters_control_obj_fa_mg=Cl_Intersection_Control.Intersection_Control(\
			val_di_intersection_control_mat=icm,\
			val_t_start_control= t_start, \
			val_t_end_control=t_end_ctrl,\
			val_duration_control=v_li_param_ctrl[2],\
			val_type_control=Cl_Control_Actuate.TYPE_CONTROL[11],\
			val_id_actuated_stage=rep[1],\
			val_t_update_ctrl=t_upd_ctrl)
			
			#we return [[li ico], type of  next control, indicator that an event end decis should be created]
			return[[inters_control_obj_fa_mg], List_Explicit_Values.initialisation_value_to_eleven,List_Explicit_Values.initialisation_value_to_one]
		
		#if the same stage is been selected
		else:
			#t_start=round(t_act+v_ti_unit,v_t_round_prec)
			#t_end=round(t_start+v_li_param_ctrl[3]-v_ti_unit,v_t_round_prec)
			#t_end=round(t_act+v_li_param_ctrl[3]-v_ti_unit,v_t_round_prec)
				
			#creation d'un objet intersection control
			inters_control_obj_fa_mg=Cl_Intersection_Control.Intersection_Control(\
			val_di_intersection_control_mat=v_inters.get_intersection_control_obj().get_di_intersection_control_mat(),\
			val_t_start_control= t_act, \
			val_t_end_control=v_inters.get_intersection_control_obj().get_t_end_control(),\
			val_duration_control=v_li_param_ctrl[2],\
			val_type_control=Cl_Control_Actuate.TYPE_CONTROL[11],\
			val_id_actuated_stage=v_inters.get_intersection_control_obj().get_id_actuated_stage(),\
			val_t_update_ctrl=v_inters.get_intersection_control_obj().get_t_update_ctrl())
			
			#print("id current stage: ",v_inters.get_intersection_control_obj().get_id_actuated_stage(),"id selected stage:",rep[1],"t upd ctrl:",v_inters.get_intersection_control_obj().get_t_update_ctrl())
				
			return[[inters_control_obj_fa_mg], List_Explicit_Values.initialisation_value_to_eleven,List_Explicit_Values.initialisation_value_to_zero]
	
	#if no ctrl rules the network (we start a new sim)
	else:
		li_id_stages=list(v_inters.get_di_stages_sign_intersection().keys())
		
		id_stage=li_id_stages[0]
		
		#inter control matrix
		icm=dict(v_inters.get_di_intersection_control_matrix())
	
		#on initiliase a un chaque phase que le stage selectionne  actualise
		for i in  v_inters.get_di_stages_sign_intersection()[id_stage]:
			icm[i[0],i[1]]=1
	
		t_start=round(t_act+v_ti_unit,v_t_round_prec)
						
		#li_param_control=[v_admissible_limit_flow, idle time, t_prem_ctrl, lim actuat duration]
		#on definit le temps limite du stage comme t_end_cotnrol
		t_end_ctrl=fct_calcul_t_update_ctrl_fa_mg(va_t_start_ctrl=t_start, va_max_dur=v_li_param_ctrl[2],va_t_unit=v_ti_unit,va_t_round_precision=v_t_round_prec)
		
		#round(t_act+v_li_param_ctrl[3]-v_ti_unit,v_t_round_prec)
	
	
		#the time at which the control decision will be updated
		t_upd_ctrl=t_end_ctrl
		
		
		#creation d'un objet intersection control, pour la RC, de duree li_param_control[2]
		inters_control_obj_fa_mg=Cl_Intersection_Control.Intersection_Control(\
		val_di_intersection_control_mat=icm,\
		val_t_start_control= t_start,\
		val_t_end_control=t_end_ctrl,\
		val_duration_control=v_li_param_ctrl[2],\
		val_type_control=Cl_Control_Actuate.TYPE_CONTROL[11],\
		val_id_actuated_stage=id_stage,\
		val_t_update_ctrl=t_upd_ctrl)
		
		#we return [[li ico], type next control, indicator that an event end decis should be created]
		return[[inters_control_obj_fa_mg], List_Explicit_Values.initialisation_value_to_eleven, List_Explicit_Values.initialisation_value_to_one]

#*****************************************************************************************************************************************************************************************

#method defiing the control amongst the stages different from the currently employed one
#v_li_param_control=[v_admissible_limit_flow, idle time, t_prem_ctrl, lim actuat duration]
def fct_define_ctrl_diferent_from_current_one(v_t_act,v_inters,v_netw,v_li_param_ctrl,v_dt,v_ti_unit,v_round_precis,v_t_round_prec,v_initial_small_val):
	

	#rep=[fa_pressure_inters_cm,id_stage]
	rep=fct_select_different_intersection_FA_stage(\
	va_intersection=v_inters,va_network=v_netw,va_round_precis=v_round_precis,va_init_small_val=v_initial_small_val)
	

	#print("id current stage: ",v_inters.get_intersection_control_obj().get_id_actuated_stage(),"id selected stage:",rep[1])
		
	#inter control matrix
	icm=dict(v_inters.get_di_intersection_control_matrix())
		
	#on initiliase a un chaque phase que le mp stage actualise
	for i in rep[0]:
		icm[i[0],i[1]]=1
	
	#t_start=round(v_inters.get_intersection_control_obj().get_t_end_control()+v_ti_unit,v_t_round_prec)
	t_start=round(v_t_act+v_ti_unit,v_t_round_prec)
	
	#on calcul le t_end du stage, = max green duree	
	#if v_val_t_start_nc==v_inters.get_intersection_control_obj().get_t_update_ctrl():
		#t_end_ctrl=fct_calcul_t_update_ctrl(va_t_act=v_val_t_start_nc, va_max_dur=v_li_param_ctrl[3],va_t_unit=v_ti_unit,va_t_round_precision=v_t_round_prec)
	#else:
		
		#t_end_ctrl=fct_calcul_t_update_ctrl(va_t_act=t_start, va_max_dur=v_li_param_ctrl[3],va_t_unit=v_ti_unit,va_t_round_precision=v_t_round_prec)
		
	t_end_ctrl=fct_calcul_t_update_ctrl_fa_mg(va_t_start_ctrl=t_start, va_max_dur=v_li_param_ctrl[2],va_t_unit=v_ti_unit,va_t_round_precision=v_t_round_prec)
	
	
	#the time at which the control decision will be updated
	t_upd_ctrl=t_end_ctrl
	#print("t_act",v_t_act,"t_end_ctrl",t_upd_ctrl)
	#print()
	#import sys
	#sys.exit()
	#print("id current stage: ",v_inters.get_intersection_control_obj().get_id_actuated_stage(),"id selected stage:",rep[1],"tctrl update",t_upd_ctrl)	
	
	#creation d'un objet intersection control
	inters_control_obj_fa_mg=Cl_Intersection_Control.Intersection_Control(\
	val_di_intersection_control_mat=icm,\
	val_t_start_control= t_start, \
	val_t_end_control=t_end_ctrl,\
	val_duration_control=v_li_param_ctrl[2],\
	val_type_control=Cl_Control_Actuate.TYPE_CONTROL[11],\
	val_id_actuated_stage=rep[1],\
	val_t_update_ctrl=t_upd_ctrl)
		
	#we return [[li ico], type of  next control, indicator that an event end decis should be created]
	return[[inters_control_obj_fa_mg], List_Explicit_Values.initialisation_value_to_eleven,List_Explicit_Values.initialisation_value_to_one]
	
#*****************************************************************************************************************************************************************************************
#li_param_control=[v_admissible_limit_flow, idle time, t_prem_ctrl, lim actuat duration]
#this method returns
#[li_ico, List_Explicit_Values.initialisation_value_to_eleven=type next control to employ, \
#1 ou 0 according as if an event end_next_decision control will /not be generated]
#NO RED CLEARANCE IS BEEN CONSIDERED
def admissible_intersection_control_object_fa_max_green(t_actuel,v_intersection,v_network,li_param_control,\
v_t_unit,v_round_prec,v_t_round_precision,v_marge_dt,v_init_small_val=-10**10):

	#time at which the new control will start
	val_t_star_new_ctrl=round(t_actuel+v_t_unit,v_round_prec)
	
	#print("ID NODE", v_intersection.get_id_node()," IN ALFG FA val_t_star_new_ctrl",val_t_star_new_ctrl,"ico",v_intersection.get_intersection_control_obj())
	#print()
	
	#if a control currently rules the  network
	if v_intersection.get_intersection_control_obj()!=None:
	
		#print(" IN ALFG FA val_t_star_new_ctrl",val_t_star_new_ctrl,"t current update",v_intersection.get_intersection_control_obj().get_t_update_ctrl())
	
		#If t current < t control update
		#if t_actuel <v_intersection.get_intersection_control_obj().get_t_update_ctrl():
		
		# if time at which the new control will start < t control update
		if val_t_star_new_ctrl <v_intersection.get_intersection_control_obj().get_t_update_ctrl():
		
			return fct_define_ctrl_amongst_all_stages(t_act=t_actuel,v_inters=v_intersection,v_netw=v_network,\
			v_li_param_ctrl=li_param_control,v_ti_unit=v_t_unit,v_dt=v_marge_dt,v_round_precis=v_round_prec,\
			v_t_round_prec=v_t_round_precision,v_initial_small_val=v_init_small_val)
		
		#if t current = t control update
		#elif t_actuel==v_intersection.get_intersection_control_obj().get_t_update_ctrl():
		# if time at which the new control will start  t control update= t control update
		
		# if time at which the new control will start =  t control update
		elif val_t_star_new_ctrl ==v_intersection.get_intersection_control_obj().get_t_update_ctrl() or\
		t_actuel==v_intersection.get_intersection_control_obj().get_t_update_ctrl():
			
			#print("iN ALGO FA val_t_star_new_ctrl",val_t_star_new_ctrl,"t_actuel",t_actuel,"t crl update",v_intersection.get_intersection_control_obj().get_t_update_ctrl())
			#print()
			return fct_define_ctrl_diferent_from_current_one(v_t_act=t_actuel,v_inters=v_intersection,v_netw=v_network,\
			v_li_param_ctrl=li_param_control,v_dt=v_marge_dt,v_ti_unit=v_t_unit,v_round_precis=v_round_prec,v_t_round_prec=v_t_round_precision,\
			v_initial_small_val=v_init_small_val)
		
		# if time at which the new control will start >  t control update
		else:
			#print("PROBLEM IN FA MAX GREEN ALGO, FCT admissible_intersection_control_object_fa_max_green, T_start new ctr:",\
			#val_t_star_new_ctrl,"t crrl update: ",v_intersection.get_intersection_control_obj().get_t_update_ctrl())
			#import sys
			#sys.exit()
			
			t_end=round(t_actuel+li_param_control[2]-v_t_unit,v_t_round_precision)
				
			#creation d'un objet intersection control
			inters_control_obj_fa_mg=Cl_Intersection_Control.Intersection_Control(\
			val_di_intersection_control_mat=v_intersection.get_intersection_control_obj().get_di_intersection_control_mat(),\
			val_t_start_control= t_actuel, \
			val_t_end_control=t_end,\
			val_duration_control=li_param_control[2],\
			val_type_control=Cl_Control_Actuate.TYPE_CONTROL[11],\
			val_id_actuated_stage=v_intersection.get_intersection_control_obj().get_id_actuated_stage(),\
			val_t_update_ctrl=v_intersection.get_intersection_control_obj().get_t_update_ctrl())
				
			return[[inters_control_obj_fa_mg], List_Explicit_Values.initialisation_value_to_eleven,List_Explicit_Values.initialisation_value_to_zero]

	
	#if no control currently rules  the network
	else:
	
		#if we do not start a new sim
		if t_actuel!=li_param_control[1]:
		
			print("PROBLEM IN FA MAX GREEN ALGO, FCT admissible_intersection_control_object_fa_max_green, T_CURRENT:",\
			t_actuel,"CTRL: ",v_intersection.get_intersection_control_obj(),"t_actue",t_actue,"t_start sim",li_param_control[1])
			import sys
			sys.exit()
			
		return fct_define_ctrl_amongst_all_stages(t_act=t_actuel,v_inters=v_intersection,v_netw=v_network,\
		v_li_param_ctrl=li_param_control,\
		v_ti_unit=v_t_unit,v_dt=v_marge_dt,v_round_precis=v_round_prec,\
		v_t_round_prec=v_t_round_precision,v_initial_small_val=v_init_small_val)
			
		
















#*****************************************************************************************************************************************************************************************
	

	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
