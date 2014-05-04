import Cl_Intersection_Control
import Cl_Network_Link
import Cl_Decisions
import Cl_Control_Actuate
import List_Explicit_Values
import math


#method calculating the time at which the control should be updated
def fct_calcul_t_update_ctrl(va_t_end_last_control_of_seq_ctrls, va_dt,va_t_round_precision):
	return round(va_t_end_last_control_of_seq_ctrls-va_dt,va_t_round_precision)

#*****************************************************************************************************************************************************************************************
#method returning the pressure exerted by an intersection control matrix
#val_intersection=the id of the intersection node
#val_inters_stage=list of the simult actuates phases
def fct_calcul_pressure_exerted_by_an_inters_control_stage(val_intersection,val_inters_stage,val_network,di_id_phase_val_qweight,val_round_prec):
	
	#if val_intersection.get_id_node()==37593:
		#print("stage",val_inters_stage)
	pres_exerted=0
	
	#if val_intersection.get_id_node()==1:
		#print()
		#print("val_intersection",val_intersection.get_id_node())
		#print("val_inters_stage",val_inters_stage)
	
	#par example un inters stage [[7,8],[9,10]] actaul simult phases [7,8] et [9,10]
	#pour chaque  phase du  stage , (le stage actualise seulement les queues des phases qu'il contient), 
	for i in val_inters_stage:
	
		#veh in  que, q(l,m)
		le=len(val_network.get_di_entry_internal_links()[i[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()[i[0],i[1]].get_queue_veh())
		
		#if val_intersection.get_id_node()==37593:
			#print("que",i)
			
		#calcule de la somme  sur les output links de la phase (queue length output link x routing prop), cad, 
		#somme sur p gamma(m,p) x q(m,p)
		som=0
		
		#if le>0:
		#if the output link is not an exit,  calcul   of the  somme sur p of gamma(m,p) x q(m,p))
		if val_network.get_di_all_links()[i[1]].get_type_network_link() != Cl_Network_Link.TYPE_NETWORK_LINK["exit"]:
		
			#pour chaque que de l'output link
			for j in val_network.get_di_entry_internal_links()[i[1]].get_set_veh_queue().get_di_obj_veh_queue_at_link():
			
					#if val_intersection.get_id_node()==2:
					#print("que de output link",i[1], "est",j)
					#print("val_intersection.get_di_key_id_phase_value_li_rout_prob()",\
					#val_network.get_di_intersections()[val_network.get_di_entry_internal_links()[i[1]].get_id_head_intersection_node()].\
					#get_di_key_id_phase_value_li_rout_prob())
				
				#if turn ratios will be estimated for the head node of the destination link
				if val_network.get_di_intersections()[val_network.get_di_entry_internal_links()[i[1]].get_id_head_intersection_node()].\
				get_estimated_turn_ratios()==1:
				
					
									
					#the product of the turn ratio x queue length (gamma(m,p) x q(m,p))
					a=val_network.get_di_intersections()[val_network.get_di_entry_internal_links()[i[1]].get_id_head_intersection_node()].\
					get_di_both_types_rp()[2][j[0],j[1]]*\
					len(val_network.get_di_entry_internal_links()[i[1]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
					[j[0],j[1]].get_queue_veh())*di_id_phase_val_qweight[j[0],j[1]]**2
				else:
					#the product of the turn ratio x queue length (gamma(m,p) x q(m,p))
					a=val_network.get_di_intersections()[val_network.get_di_entry_internal_links()[i[1]].get_id_head_intersection_node()].\
					get_di_both_types_rp()[1][j[0],j[1]]*\
					len(val_network.get_di_entry_internal_links()[i[1]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
					[j[0],j[1]].get_queue_veh())*di_id_phase_val_qweight[j[0],j[1]]**2
					
				#if val_intersection.get_id_node()==37593:
					#print("que output link", j,"som",som,"a",a)

					
				som+=a
				#if val_intersection.get_id_node()==37593:
					#print("som",som)
					
			#if val_intersection.get_id_node()==1:
				#print("som",som)


			# [ q(l,m) - sum_p(gamma(m,p) x q(m,p)) ] x s(l,m)xU(l,m), weight_queue=[ q(l,m) - sum_p(gamma(m,p) x q(m,p)) ]
			#si sum sur p de (gamma(m,p) x q(m,p)) <  q(l,m) alors on calcule la weight sinon weight=0
			#if val_intersection.get_id_node()==1:
				#print("le>som",le>som)
							
		#weight_queue=[ q(l,m) - sum_p(gamma(m,p) x q(m,p)) ] x  s(l,m) x U_n(l,m)
		weight_queue=(\
		(le*di_id_phase_val_qweight[i[0],i[1]]**2-som)*val_network.get_di_entry_internal_links()[i[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()[i[0],i[1]].get_sat_flow_queue())
		
		pres_exerted=pres_exerted+weight_queue
		#if val_intersection.get_id_node()==37593:
			#print("len:",le,"som",som,"que:",i,"sat flow que",val_network.get_di_entry_internal_links()[i[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()[i[0],i[1]].get_sat_flow_queue(),"weight que",weight_queue,"pres_exerted",pres_exerted)
			#print()
	
	pressure_exerted=round(pres_exerted,val_round_prec)
	#if val_intersection.get_id_node()==2:
		#print("pressure_exerted",pressure_exerted)
	return pressure_exerted

#*****************************************************************************************************************************************************************************************

#method selecting the mp intersection control matrix exerting the higher pressure
#it returns the [max_pressure_inters_cm,id_stage, exerted pressure]
def fct_select_inters_control_stage_exerting_higher_pressure(va_intersection,va_network,va_di_id_phase_val_qweight,va_round_prec,va_init_small_val):
	
	#id stages possibles
	li_id_stages_inersection=list(va_intersection.get_di_stages_sign_intersection().keys())
		
	
	#print("stages inters",va_intersection.get_di_stages_sign_intersection())
	
	#initialisation de la matrice consideree
	max_pressure_inters_cm=va_intersection.get_di_stages_sign_intersection()[li_id_stages_inersection[0]]
	#print("max_pressure_inters_cm",max_pressure_inters_cm)
		
	#initialisation de la pression exercee
	pressure_exerted=va_init_small_val
	#print()
	#if va_intersection.get_id_node()==2:	
		#print("max_pressure_inters_cm initial",max_pressure_inters_cm)
	
	id_stage=-1
	#for each possible stage of the intersection, dict=id stage, value=[... ,id simult compatible phases,... ]
	for i in li_id_stages_inersection:
		
		#print()
		#on calcule  la pression exercee par le stage en question
		current_exerted_pression=fct_calcul_pressure_exerted_by_an_inters_control_stage(\
		val_intersection=va_intersection,\
		val_inters_stage=va_intersection.get_di_stages_sign_intersection()[i],val_network=va_network,\
		di_id_phase_val_qweight=va_di_id_phase_val_qweight,\
		val_round_prec=2)
		
		
		#if va_intersection.get_id_node()==2:
			#print("current_exerted_pression",current_exerted_pression)
			
		#if va_intersection.get_id_node()==37593:
			#print("current pression", pressure_exerted,"id stage tempra selecred:", id_stage)	
			
		if current_exerted_pression>pressure_exerted:
			pressure_exerted=current_exerted_pression
			max_pressure_inters_cm=va_intersection.get_di_stages_sign_intersection()[i]
			id_stage=i
			
		#if va_intersection.get_id_node()==37593:
			#print("icm examined", va_intersection.get_di_stages_sign_intersection()[i],"exerted pres by exam stage:",current_exerted_pression,"current pression", pressure_exerted,\
			#"id stage tempra selecred:", id_stage)
	#print("here",max_pressure_inters_cm)	
	#if va_intersection.get_id_node()==2:
		#print("pressure_exerted",pressure_exerted)
		#print("max_pressure_inters_cm",max_pressure_inters_cm)
		
	return [max_pressure_inters_cm,id_stage,pressure_exerted]
			
#*****************************************************************************************************************************************************************************************
#method defining whether a new stage should be employed or not
#it returns 1 if the nex selected stage should be employed, 0 otherwise
def fct_defining_whether_new_stage_employed(val_intersect,val_netw, val_exerted_pres_new_selected_stage,\
val_param_comparaison,val_di_id_phase_val_qweight,val_round_precision,val_init_small_val):

	#calcul of the exerted pression by the currently employed stage
	pres_cur_stage=fct_calcul_pressure_exerted_by_an_inters_control_stage(val_intersection=val_intersect,\
	val_inters_stage=val_intersect.get_di_stages_sign_intersection()[val_intersect.get_intersection_control_obj().get_id_actuated_stage()],\
	val_network=val_netw,\
	di_id_phase_val_qweight=val_di_id_phase_val_qweight,\
	val_round_prec=val_round_precision)
	
	fct_select_inters_control_stage_exerting_higher_pressure(\
	va_intersection=val_intersect,va_network=val_netw,\
	va_di_id_phase_val_qweight=val_di_id_phase_val_qweight,\
	va_round_prec=val_round_precision,va_init_small_val=val_init_small_val)
	
	#if val_intersect.get_id_node()==37593:
		#print("pres_cur_stage",pres_cur_stage,val_exerted_pres_new_selected_stage,val_param_comparaison,\
		#val_exerted_pres_new_selected_stage-pres_cur_stage > val_param_comparaison*pres_cur_stage)

	if val_exerted_pres_new_selected_stage-pres_cur_stage > val_param_comparaison*pres_cur_stage:
		
		return 1
	else:
		return 0
	
	
	
	


#*****************************************************************************************************************************************************************************************
#method returning the mp intersection control object for the next period without red clearance
#we return [inters control objet, type of next control to employe next time , indicator for estimated or not turn ratios]

#li_param_control=[actuation durationn of a stage] 
#parameter comparison exerted pressure betwenne current stage and new selected stage]

#mp_inters_control_stagen_and_id_stage=[max_pressure_inters_cm,id_stage]
def admissible_intersection_control_object_next_period_mp_practical(v_intersection,v_network,mp_inters_control_stage_and_id_stage,\
li_param_control,v_round_prec,v_t_round_prec,\
v_t_end_current_network_control_matrix,v_t_unit,v_dt,v_init_small_val=-10**10):
	
	
	#if v_intersection.get_id_node()==37593:
		#print("id current stage",v_intersection.get_intersection_control_obj().get_id_actuated_stage())
		#print("id stage select:",mp_inters_control_stage_and_id_stage[1])
		#print()
		
		
	#inter control matrix
	icm=dict(v_intersection.get_di_intersection_control_matrix())
		
	#init of every phase que actuated by the mp stage
	for i in mp_inters_control_stage_and_id_stage[0]:
		icm[i[0],i[1]]=1
	
	
	################## computation times ctrl ##############################
	
	t_start=round(v_t_end_current_network_control_matrix+v_t_unit,v_t_round_prec) 
	
	#li_param_control=[actuation durationn of a stage, duration of red clearance, 
	#parameter comparison exerted pressure betwenne current stage and new selected stage]
		
	t_end_current_icm=round(t_start+li_param_control[0]-v_t_unit,v_t_round_prec)
		
	################## computation times icm  ##############################
	
	#if  v_intersection.get_id_node()==37593:
		#print("t_start_red_clear",t_start_red_clear,"t_end_current_icm_rc",t_end_current_icm_rc)
		#import sys
		#sys.exit()
	
	
	#durat_ctrl=li_param_control[0]
	
	
		
	#the time at which the control decision will be updated
	t_upd_ctrl=fct_calcul_t_update_ctrl(va_t_end_last_control_of_seq_ctrls=t_end_current_icm, va_dt=v_dt,va_t_round_precision=v_t_round_prec)	
		

		
			
	#creation d'un objet intersection control, pour le MP controle,  le prochain type de controle sera rd clear, on n'a pas besoin ici du type
	#mais on l'indique quand meme pour le moment. Ensuite on va l'enlever
	inters_control_obj_mp=Cl_Intersection_Control.Intersection_Control(\
	val_di_intersection_control_mat=icm,val_t_start_control= t_start, \
	val_type_control=Cl_Control_Actuate.TYPE_CONTROL[15],\
	val_type_control_related_to_t_revision=Cl_Control_Actuate.TYPE_CONTROL_T_REVISION_CATEGORY["without_sensor_requirement_for_t_update"],\
	val_t_end_control= t_end_current_icm,val_duration_control=li_param_control[0],\
	val_estim_turn_ratios_with_current_ctrl=v_network.get_di_intersections()[v_intersection.get_id_node()].get_estimated_turn_ratios(),\
	val_id_actuated_stage=mp_inters_control_stage_and_id_stage[1],val_t_update_ctrl=t_upd_ctrl)
		
	
		
	li_ico=[inters_control_obj_mp]
		

		
	#we return [inters control objet, le type du prochain controle a appliquer par le (prochain) even en_decision_icm, indicator for estimated or not turn ratios]
	return[li_ico, List_Explicit_Values.initialisation_value_to_fifteen, List_Explicit_Values.initialisation_value_to_one,\
	v_network.get_di_intersections()[v_intersection.get_id_node()].get_estimated_turn_ratios()]
		
		

#*****************************************************************************************************************************************************************************************

#method returning 
#[inters control objet, le type du prochain controle a appliquer par le (prochain) even en_decision_icm, indicator for estimated or not turn ratios]
#v_li_param_control=[actuation durationn of a stage,parameter comparison exerted pressure betwenne current stage and new selected stage]

def admissible_intersection_control_object_next_period_mp_pract_without_red_clear(t_actuel,t_start_sim,v_sim_dur,v_inters,v_netwk,\
v_li_param_control,val_dict_id_phase_val_qweight,v_round_precis,\
v_t_round_precis,v_t_end_current_netwk_control_matrix,v_ti_unit,v_marge_dt,v_initial_small_val=-10**10):

	#print("v_di_param_control[v_inters.get_id_node()][4]",v_di_param_control[4])
	#import sys
	#sys.exit()

	#if  t_current = t_start new sim
	if t_actuel==t_start_sim:	
		
		li_id_stages=list(v_inters.get_di_stages_sign_intersection().keys())
		
		id_stage=li_id_stages[0]
		
		
		#inter control matrix
		icm=dict(v_inters.get_di_intersection_control_matrix())
	
		#on initiliase a un chaque phase que le stage selectionne  actualise
		for i in  v_inters.get_di_stages_sign_intersection()[id_stage]:
			icm[i[0],i[1]]=1
		
		
		t_start=round(t_actuel+v_ti_unit,v_t_round_precis) 
		
		
		t_end_current_icm=round(t_start+v_li_param_control[0]-v_ti_unit,v_t_round_precis)
		
		
		#the time at which the control decision will be updated
		t_upd_ctrl=fct_calcul_t_update_ctrl(va_t_end_last_control_of_seq_ctrls=t_end_current_icm, va_dt=v_marge_dt,va_t_round_precision=v_t_round_precis)
		
		#creation d'un objet intersection control, 
		inters_control_obj_mp_pract=Cl_Intersection_Control.Intersection_Control(\
		val_di_intersection_control_mat=icm,\
		val_t_start_control= t_start,\
		val_type_control=Cl_Control_Actuate.TYPE_CONTROL[15],\
		val_type_control_related_to_t_revision=Cl_Control_Actuate.TYPE_CONTROL_T_REVISION_CATEGORY["without_sensor_requirement_for_t_update"],\
		val_t_end_control=t_end_current_icm,\
		val_duration_control=v_li_param_control[0],\
		val_estim_turn_ratios_with_current_ctrl=v_netwk.get_di_intersections()[v_inters.get_id_node()].get_estimated_turn_ratios(),\
		val_id_actuated_stage=id_stage,val_t_update_ctrl=t_upd_ctrl)
		#,\
		#val_id_actuated_stage=id_stage)
		 
		
		li_ico=[inters_control_obj_mp_pract]
		
		#we return [inters control objet, le type du prochain controle a appliquer par le (prochain) even en_decision_icm, indicator for estimated or not turn ratios]
		return[li_ico, List_Explicit_Values.initialisation_value_to_fifteen, List_Explicit_Values.initialisation_value_to_one,\
		v_netwk.get_di_intersections()[v_inters.get_id_node()].get_estimated_turn_ratios()]
		
	#if  t_current > t_start new sim
	else:
		
		#the new selected stage, 
		#li_select_stage_info=[max_pressure_inters_cm,id_stage, exerted pressure]
		li_select_stage_info=fct_select_inters_control_stage_exerting_higher_pressure(va_intersection=v_inters,va_network=v_netwk,\
		va_di_id_phase_val_qweight=val_dict_id_phase_val_qweight,\
		va_round_prec=v_round_precis,va_init_small_val=v_initial_small_val)
		
		#if v_inters.get_id_node()==37593:
			#print("id selected stage", li_select_stage_info[1],"id current stage",v_inters.get_intersection_control_obj().get_id_actuated_stage())
		
		#print("v_li_param_control",v_li_param_control)
		
		#if the decision should be updated
		if fct_defining_whether_new_stage_employed(val_intersect=v_inters,val_netw=v_netwk, \
		val_exerted_pres_new_selected_stage=li_select_stage_info[2],\
		val_param_comparaison=v_li_param_control[1],\
		val_di_id_phase_val_qweight=val_dict_id_phase_val_qweight,\
		val_round_precision=v_round_precis,val_init_small_val=v_initial_small_val)==1:
		
			
			return admissible_intersection_control_object_next_period_mp_practical(\
			v_intersection=v_inters,v_network=v_netwk,\
			mp_inters_control_stage_and_id_stage=li_select_stage_info,\
			li_param_control=v_li_param_control,v_round_prec=v_round_precis,\
			v_t_round_prec=v_t_round_precis,\
			v_t_end_current_network_control_matrix=v_t_end_current_netwk_control_matrix,\
			v_dt=v_marge_dt,\
			v_t_unit=v_ti_unit,v_init_small_val=v_initial_small_val)
		
	
		#if we will not update the previously made decision
		else:
			
			#creation inters control obj
			
			t_start=round(v_t_end_current_netwk_control_matrix+v_ti_unit,v_t_round_precis) 
	
			t_end_current_icm=round(t_start+v_li_param_control[0]-v_ti_unit,v_t_round_precis)
			
			
			#the time at which the control decision will be updated
			t_upd_ctrl=fct_calcul_t_update_ctrl(va_t_end_last_control_of_seq_ctrls=t_end_current_icm, va_dt=v_marge_dt,va_t_round_precision=v_t_round_precis)
			
			#creation d'un objet intersection control, pour le MP controle,  le prochain type de controle sera rd clear, on n'a pas besoin ici du type
			#mais on l'indique quand meme pour le moment. Ensuite on va l'enlever
			inters_control_obj_mp_pract=Cl_Intersection_Control.Intersection_Control(\
			val_di_intersection_control_mat=\
			v_netwk.get_di_intersections()[v_inters.get_id_node()].get_intersection_control_obj().get_di_intersection_control_mat(),\
			val_t_start_control=t_start,\
			val_type_control=Cl_Control_Actuate.TYPE_CONTROL[15],\
			val_type_control_related_to_t_revision=Cl_Control_Actuate.TYPE_CONTROL_T_REVISION_CATEGORY["without_sensor_requirement_for_t_update"],\
			val_t_end_control=t_end_current_icm,val_duration_control=v_li_param_control[0],\
			val_estim_turn_ratios_with_current_ctrl=v_netwk.get_di_intersections()[v_inters.get_id_node()].get_estimated_turn_ratios(),\
			val_id_actuated_stage=v_netwk.get_di_intersections()[v_inters.get_id_node()].get_intersection_control_obj().get_id_actuated_stage(),\
			val_t_update_ctrl=t_upd_ctrl)
			
	
			li_ico=[inters_control_obj_mp_pract]
			
			#on retourne une liste d' inters control objet, le type du prochain controle a appliquer par le (prochain) even en_decision_icm]
			#we return [[li ico], type next control, indicator that an event end decis should be created]
			return[li_ico, List_Explicit_Values.initialisation_value_to_fifteen, List_Explicit_Values.initialisation_value_to_one,\
			v_netwk.get_di_intersections()[v_inters.get_id_node()].get_estimated_turn_ratios()]
			

			










