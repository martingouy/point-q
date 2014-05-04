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
def fct_calcul_pressure_exerted_by_an_inters_control_stage(val_intersection,val_inters_stage,val_network,val_round_prec):
	
	pres_exerted=0
	
	#if val_intersection.get_id_node()==1:
		#print()
		#print("val_intersection",val_intersection.get_id_node())
		#print("val_inters_stage",val_inters_stage)
	
	#par example un inters stage [[7,8],[9,10]] actaul simult phases [7,8] et [9,10]
	#pour chaque  phase du  stage , (le stage actualise seulement les queues des phases qu'il contient), 
	for i in val_inters_stage:
		#if val_intersection.get_id_node()==2:
			#print()
		print(" inter stage",i)
		# nombre des véhicules en que, q(l,m)
		le=len(val_network.get_di_entry_internal_links()[i[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()[i[0],i[1]].get_queue_veh())
		#if val_intersection.get_id_node()==1:
			#print("length que",le)
		#if val_intersection.get_id_node()==2:
			#print("le",le)
		#calcule de la somme  sur les output links de la phase (queue length output link x routing prop), cad, 
		#somme sur p gamma(m,p) x q(m,p)
		som=0
		
		#if le>0:
		#si l'output link de la queue n'est pas exit on calcule  la somme sur p de gamma(m,p) x q(m,p))
		if val_network.get_di_all_links()[i[1]].get_type_network_link() != Cl_Network_Link.TYPE_NETWORK_LINK["exit"]:
		
			#pour chaque que de l'output link
			for j in val_network.get_di_entry_internal_links()[i[1]].get_set_veh_queue().get_di_obj_veh_queue_at_link():
				#if val_intersection.get_id_node()==2:
					#print("que de output link",i[1], "est",j)
					#print("val_intersection.get_di_key_id_phase_value_li_rout_prob()",\
					#val_network.get_di_intersections()[val_network.get_di_entry_internal_links()[i[1]].get_id_head_intersection_node()].\
					#get_di_key_id_phase_value_li_rout_prob())
					
				#the product of the turn ratio x queue length (gamma(m,p) x q(m,p))
				a=val_network.get_di_intersections()[val_network.get_di_entry_internal_links()[i[1]].get_id_head_intersection_node()].\
				get_di_key_id_phase_value_li_rout_prob()[j[0],j[1]][0] *\
				len(val_network.get_di_entry_internal_links()[i[1]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
				[j[0],j[1]].get_queue_veh())
					
				#if val_intersection.get_id_node()==2:
					#print("som",som,"a",a)
					
				som+=a
				#if val_intersection.get_id_node()==2:
					#print("som",som)
					
			#if val_intersection.get_id_node()==1:
				#print("som",som)


			# [ q(l,m) - sum_p(gamma(m,p) x q(m,p)) ] x s(l,m)xU(l,m), weight_queue=[ q(l,m) - sum_p(gamma(m,p) x q(m,p)) ]
			#si sum sur p de (gamma(m,p) x q(m,p)) <  q(l,m) alors on calcule la weight sinon weight=0
			#if val_intersection.get_id_node()==1:
				#print("le>som",le>som)
							
		#weight_queue=[ q(l,m) - sum_p(gamma(m,p) x q(m,p)) ] x  s(l,m) x U_n(l,m)
		weight_queue=(\
		(le-som)*val_network.get_di_entry_internal_links()[i[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()[i[0],i[1]].get_sat_flow_queue())
		
		pres_exerted=pres_exerted+weight_queue
		#if val_intersection.get_id_node()==2:
			#print("pres_exerted",pres_exerted)
	
	pressure_exerted=round(pres_exerted,val_round_prec)
	#if val_intersection.get_id_node()==2:
		#print("pressure_exerted",pressure_exerted)
	return pressure_exerted

#*****************************************************************************************************************************************************************************************
#method selecting the mp intersection control matrix exerting the higher pressure
def fct_select_inters_control_stage_exerting_higher_pressure(va_intersection,va_network,va_round_prec,va_init_small_val):
	
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
		
	#for each possible stage of the intersection, dict=id stage, value=[... ,id simult compatible phases,... ]
	for i in li_id_stages_inersection:
		
		#print()
		#on calcule  la pression exercee par le stage en question
		current_exerted_pression=fct_calcul_pressure_exerted_by_an_inters_control_stage(\
		val_intersection=va_intersection,\
		val_inters_stage=va_intersection.get_di_stages_sign_intersection()[i],val_network=va_network,val_round_prec=2)
		#if va_intersection.get_id_node()==2:
			#print("icm examined", va_intersection.get_di_stages_sign_intersection()[i])
		
		#if va_intersection.get_id_node()==2:
			#print("current_exerted_pression",current_exerted_pression)
			
			
		if current_exerted_pression>pressure_exerted:
			pressure_exerted=current_exerted_pression
			max_pressure_inters_cm=va_intersection.get_di_stages_sign_intersection()[i]
	#print("here",max_pressure_inters_cm)	
	#if va_intersection.get_id_node()==2:
		#print("pressure_exerted",pressure_exerted)
		#print("max_pressure_inters_cm",max_pressure_inters_cm)
		
	return max_pressure_inters_cm
			
#*****************************************************************************************************************************************************************************************
#method returning the mp intersection control object for the next period
#on retourne une liste d' inters control objet and le type du prochain controle a appliquer par le (prochain) even en_decision_icm
#duration_icm= le temps d'actualisation de l'icm
#li_param_MP_control=[...,[intersection stage actuat duration ith period, durat red,clear],..., cycle duration]
def admissible_intersection_control_object_next_period_mp(v_intersection,v_network,di_param_control,v_round_prec,v_t_round_prec,\
v_t_end_current_network_control_matrix,v_t_unit,v_dt,v_init_small_val=-10**10):
	
	
	#on selectionne le mp stage, list [.., id sim compatible phases,...]
	mp_inters_control_stage=fct_select_inters_control_stage_exerting_higher_pressure(\
	va_intersection=v_intersection,va_network=v_network,va_round_prec=v_round_prec,va_init_small_val=v_init_small_val)
	
	
		
	#inter control matrix
	icm=dict(v_intersection.get_di_intersection_control_matrix())
	
		
	#on initiliase a un chaque phase que le mp stage actualise
	for i in mp_inters_control_stage:
		icm[i[0],i[1]]=1
	
	#v_network.get_control_actuate_obj().get_di_param_mp_ctrl()=
	#dict, key=id node, 
	#value=[ [...,[duration MP icm, dur red clear],...], cycle duration,, len([...,[duration MP icm, dur red clear],...]),indice pour choisir la duree de mp icm cet indice doir etre incremente de un]
	
	#on increment de un l'indice de choix des durees	
	#di_param_control=dict, key = id node , value=list[list stage actuat dura and red clear dura, cycle duration, len(list stage actuat dura and red clear dura),\
	#ddice choix list stage actuat dura and red cleat
	#indice_choix_duree=v_network.get_control_actuate_obj().get_di_param_mp_ctrl()[v_intersection.get_id_node()][3]+1
	#print("di_param_control[v_intersection.get_id_node()]",di_param_control)
	indice_choix_duree=di_param_control[v_intersection.get_id_node()][3]+1
	
	
	#li_stage_actuation_duration_and_idle_time=v_network.get_control_actuate_obj().\
	#get_di_param_mp_ctrl()[v_intersection.get_id_node()][0][indice_choix_duree]
	
	li_stage_actuation_duration_and_idle_time=di_param_control[v_intersection.get_id_node()][0][indice_choix_duree]
	
	t_start=round(v_t_end_current_network_control_matrix+v_t_unit,v_t_round_prec) 
	
	t_end_current_icm=round(t_start+li_stage_actuation_duration_and_idle_time[0]-v_t_unit,v_t_round_prec)
	
	#duration_cycle=v_network.get_control_actuate_obj().get_di_param_mp_ctrl()[v_intersection.get_id_node()][1]
	duration_cycle=di_param_control[v_intersection.get_id_node()][1]
	
	t_end_cycle=round(math.ceil( t_end_current_icm/duration_cycle)*duration_cycle,v_t_round_prec)
	
	#the time at which the control decision will be updated
	t_upd_ctrl=fct_calcul_t_update_ctrl(va_t_end_last_control_of_seq_ctrls=t_end_current_icm, va_dt=v_dt,va_t_round_precision=v_t_round_prec)
		 
		
	#creation d'un objet intersection control, pour le MP controle,  le prochain type de controle sera rd clear, on n'a pas besoin ici du type
	#mais on l'indique quand meme pour le moment. Ensuite on va l'enlever
	inters_control_obj_mp=Cl_Intersection_Control.Intersection_Control(\
	val_di_intersection_control_mat=icm,val_t_start_control= t_start, \
	val_t_end_control= t_end_current_icm,val_duration_control=li_stage_actuation_duration_and_idle_time[0],\
	val_cycle_duration_associated_with_control=duration_cycle,val_type_control=Cl_Control_Actuate.TYPE_CONTROL[3],\
	val_t_update_ctrl=t_upd_ctrl)
		
		
	#creation d'un type de controle red clear
	t_start_red_clear=round(t_end_current_icm+v_t_unit,v_t_round_prec)
	
	duration_idle_time=	li_stage_actuation_duration_and_idle_time[1]
		
	t_end_current_icm_rc=round(t_start_red_clear+duration_idle_time-v_t_unit,v_t_round_prec)
		
		
	t_end_cycle=round(math.ceil( t_end_current_icm_rc/duration_cycle)*duration_cycle,v_t_round_prec)
		 
		 
	#creation d'un objet intersection control, pour la RC, le prochain type de controle sera MP
	inters_control_obj_rc=Cl_Intersection_Control.Intersection_Control(\
	val_di_intersection_control_mat=v_intersection.get_di_intersection_control_matrix(),\
	val_t_start_control= t_start_red_clear, \
	val_t_end_control= t_end_current_icm_rc,val_duration_control=duration_idle_time,\
	val_cycle_duration_associated_with_control=duration_cycle,val_type_control=Cl_Control_Actuate.TYPE_CONTROL[0],\
	val_t_update_ctrl=t_upd_ctrl)
	
	#calcul de l'indice de la liste des param de MP a utiser la prochaine fois
	#si l'indice courant est l'avant dernier (le dernier= duree cycle)
	#if indice_choix_duree==v_network.get_control_actuate_obj().\
	#get_di_param_mp_ctrl()[v_intersection.get_id_node()][2]-1:
		#indice_choix_duree=-1
		
	if indice_choix_duree==di_param_control[v_intersection.get_id_node()][2]-1:
		indice_choix_duree=-1

		
		
	#on maj l'indice  pour le prochain choix de durees dans control actuate objet
	#v_network.get_control_actuate_obj().get_di_param_mp_ctrl()[v_intersection.get_id_node()][3]=indice_choix_duree
	di_param_control[v_intersection.get_id_node()][3]=indice_choix_duree
		
		
	
	li_ico=[inters_control_obj_mp,inters_control_obj_rc]
		
	#on retourne une liste d' inters control objet, le type du prochain controle a appliquer par le (prochain) even en_decision_icm]
	#we return [[li ico], type next control, indicator that an event end decis should be created]
	return[li_ico, List_Explicit_Values.initialisation_value_to_three,List_Explicit_Values.initialisation_value_to_one]
		
		

#*****************************************************************************************************************************************************************************************

















