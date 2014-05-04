import Cl_Intersection_Control
import Cl_Network_Link
import Cl_Decisions
import Cl_Control_Actuate
import List_Explicit_Values
import math


#method calculating the time at which the control should be updated
def fct_calcul_t_update_ctrl(va_t_end_last_control_of_seq_ctrls, va_dt,va_t_round_precision,va_t_unit):
	return round(va_t_end_last_control_of_seq_ctrls-va_dt+va_t_unit,va_t_round_precision)

#*****************************************************************************************************************************************************************************************
#method returning the pressure exerted by an intersection control matrix
#val_intersection=the id of the intersection node
#val_inters_stage=list of the simult actuates phases
#if val_index_key_for_selecting_turn_ratio_values= 1 we will take the given from data turn ration values, 
#if val_index_key_for_selecting_turn_ratio_values= 1 we will take the estimated turn ratio values
def fct_calcul_pressure_exerted_by_an_inters_control_stage(val_intersection,val_inters_stage,val_network,di_id_phase_val_qweight,val_round_prec):
	
	pres_exerted=0

	
	#par example un inters stage [[7,8],[9,10]] actaul simult phases [7,8] et [9,10]
	#pour chaque  phase du  stage , (le stage actualise seulement les queues des phases qu'il contient), 
	for i in val_inters_stage:
		#if val_intersection.get_id_node()==2:
			#print()
		#print(" inter stage",i)
		# nombre des véhicules en que, q(l,m)
		le=len(val_network.get_di_entry_internal_links()[i[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()[i[0],i[1]].get_queue_veh())
		
		#calcul of the somme  sur les output links de la phase (queue length output link x routing prop), cad, 
		#somme sur p gamma(m,p) x q(m,p)
		som=0
		
		#si l'output link de la queue n'est pas exit on calcule  la somme sur p de gamma(m,p) x q(m,p))
		if val_network.get_di_all_links()[i[1]].get_type_network_link() != Cl_Network_Link.TYPE_NETWORK_LINK["exit"]:
		
			#pour chaque que de l'output link
			for j in val_network.get_di_entry_internal_links()[i[1]].get_set_veh_queue().get_di_obj_veh_queue_at_link():
				#if val_intersection.get_id_node()==2:
					#print("que de output link",i[1], "est",j)
					#print("val_intersection.get_di_key_id_phase_value_li_rout_prob()",\
					#val_network.get_di_intersections()[val_network.get_di_entry_internal_links()[i[1]].get_id_head_intersection_node()].\
					#get_di_key_id_phase_value_li_rout_prob())
				#print("node",val_network.get_di_entry_internal_links()[i[1]].get_id_head_intersection_node(),\
				#val_network.get_di_intersections()[val_network.get_di_entry_internal_links()[i[1]].get_id_head_intersection_node()].\
				#get_estimated_turn_ratios(),val_network.get_di_intersections()[val_network.get_di_entry_internal_links()[i[1]].get_id_head_intersection_node()].\
				#get_di_both_types_rp()[2].keys())	
				
				if di_id_phase_val_qweight[j[0],j[1]]!=1:
						print("id node", val_intersection.get_id_node(),"output que",j,"val_network.get_di_intersections()[val_network.get_di_entry_internal_links()[i[1]].get_id_head_intersection_node()].\
						get_di_both_types_rp()[2][j[0],j[1]]",val_network.get_di_intersections()[val_network.get_di_entry_internal_links()[i[1]].get_id_head_intersection_node()].\
						get_di_both_types_rp()[2][j[0],j[1]],"len",len(val_network.get_di_entry_internal_links()[i[1]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
						[j[0],j[1]].get_queue_veh()),di_id_phase_val_qweight[j[0],j[1]]**2,\
						val_network.get_di_intersections()[val_network.get_di_entry_internal_links()[i[1]].get_id_head_intersection_node()].\
						get_di_both_types_rp()[2][j[0],j[1]]*\
						len(val_network.get_di_entry_internal_links()[i[1]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
						[j[0],j[1]].get_queue_veh())*di_id_phase_val_qweight[j[0],j[1]]**2)
						import sys
						sys.exit()
					
				
				#if turn ratios will be estimated for the head node of the destination link
				if val_network.get_di_intersections()[val_network.get_di_entry_internal_links()[i[1]].get_id_head_intersection_node()].\
				get_estimated_turn_ratios()==1:
				
				
					#print("id nd",val_network.get_di_entry_internal_links()[i[1]].get_id_head_intersection_node(),\
					#val_network.get_di_intersections()[val_network.get_di_entry_internal_links()[i[1]].get_id_head_intersection_node()].\
					#get_estimated_turn_ratios())
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
					
				
				#a=val_network.get_di_intersections()[val_network.get_di_entry_internal_links()[i[1]].get_id_head_intersection_node()].\
				#get_current_di_rout_prob()[j[0],j[1]]*\
				#len(val_network.get_di_entry_internal_links()[i[1]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
				#[j[0],j[1]].get_queue_veh())
					
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
		(le*di_id_phase_val_qweight[i[0],i[1]]**2-som)*val_network.get_di_entry_internal_links()[i[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()[i[0],i[1]].get_sat_flow_queue())
			
		
		pres_exerted=pres_exerted+weight_queue
		#if val_intersection.get_id_node()==2:
			#print("pres_exerted",pres_exerted)
	
	pressure_exerted=round(pres_exerted,val_round_prec)
	#if val_intersection.get_id_node()==2:
		#print("pressure_exerted",pressure_exerted)
	return pressure_exerted

#*****************************************************************************************************************************************************************************************
#method selecting the mp intersection control matrix exerting the higher pressure
def fct_select_inters_control_stage_exerting_higher_pressure(va_intersection,va_network,va_round_prec,va_di_id_phase_val_qweight,va_init_small_val):
	
	#id stages possibles
	li_id_stages_inersection=list(va_intersection.get_di_stages_sign_intersection().keys())
		
	
	
	#print("stages inters",va_intersection.get_di_stages_sign_intersection())
	
	#initialisation de la matrice consideree
	max_pressure_inters_cm=va_intersection.get_di_stages_sign_intersection()[li_id_stages_inersection[0]]
	#print("max_pressure_inters_cm",max_pressure_inters_cm)
		
	#initialisation de la pression exercee
	pressure_exerted=va_init_small_val
	
	id_stage=-1
	#print()
	#if va_intersection.get_id_node()==2:	
		#print("max_pressure_inters_cm initial",max_pressure_inters_cm)
		
	#for each possible stage of the intersection, dict=id stage, value=[... ,id simult compatible phases,... ]
	for i in li_id_stages_inersection:
		
		#print()
		#on calcule  la pression exercee par le stage en question
		current_exerted_pression=fct_calcul_pressure_exerted_by_an_inters_control_stage(\
		val_intersection=va_intersection,\
		val_inters_stage=va_intersection.get_di_stages_sign_intersection()[i],val_network=va_network,\
		di_id_phase_val_qweight=va_di_id_phase_val_qweight,val_round_prec=2)
		#if va_intersection.get_id_node()==2:
			#print("icm examined", va_intersection.get_di_stages_sign_intersection()[i])
		
		#if va_intersection.get_id_node()==2:
			#print("current_exerted_pression",current_exerted_pression)
			
			
		if current_exerted_pression>pressure_exerted:
			pressure_exerted=current_exerted_pression
			max_pressure_inters_cm=va_intersection.get_di_stages_sign_intersection()[i]
			id_stage=i
			
	#print("here",max_pressure_inters_cm)	
	#if va_intersection.get_id_node()==2:
		#print("pressure_exerted",pressure_exerted)
		#print("max_pressure_inters_cm",max_pressure_inters_cm)
		
	return [max_pressure_inters_cm,id_stage]
			
#*****************************************************************************************************************************************************************************************
#method returning the mp intersection control object for the next period
#on retourne une liste d' inters control objet and le type du prochain controle a appliquer par le (prochain) even en_decision_icm
#duration_icm= le temps d'actualisation de l'icm
#param_control=list [stage actuation duration]
def admissible_intersection_control_object_next_period_mp_without_rc(v_intersection,v_network,param_control,v_round_prec,v_t_round_prec,\
v_t_end_current_network_control_matrix,v_t_unit,v_dt,val_di_id_phase_val_qweight,v_init_small_val=-10**10):
	
	
	
	#on selectionne le mp stage, list [.., id sim compatible phases,...]
	#mp_inters_control_stage=[icm, id stage]
	mp_inters_control_stage=fct_select_inters_control_stage_exerting_higher_pressure(\
	va_intersection=v_intersection,va_network=v_network,va_round_prec=v_round_prec,va_di_id_phase_val_qweight=val_di_id_phase_val_qweight,\
	va_init_small_val=v_init_small_val)
	
	
		
	#inter control matrix
	icm=dict(v_intersection.get_di_intersection_control_matrix())
	
		
	#on initiliase a un chaque phase que le mp stage active
	for i in mp_inters_control_stage[0]:
		icm[i[0],i[1]]=1
	
	#li_param_control=list
	#value=[ [...,[duration MP icm, dur red clear],...], cycle duration, nb decisions,indice pour choisir la duree de mp icm cet indice doir etre incremente de un]
	#print("li_param_contro",li_param_control)
	#import sys
	#sys.exit()
	
	#on increment de un l'indice de choix des durees	
	
	#print("here id nd,",v_intersection.get_id_node(),li_param_control)
	
	#indice_choix_duree=li_param_control[3]+1
	
	
	###########################computations for the icm######################################################
	
	#li_stage_actuation_duration_and_idle_time=v_network.get_control_actuate_obj().\
	#get_di_param_mp_ctrl()[v_intersection.get_id_node()][0][indice_choix_duree]
	
	#[stage act duration, idle time]
	#li_stage_actuation_duration_and_idle_time=li_param_control[0][indice_choix_duree]
	#print(li_stage_actuation_duration_and_idle_time)
	
	t_start=round(v_t_end_current_network_control_matrix+v_t_unit,v_t_round_prec) 
	
	t_end_current_icm=round(t_start+param_control[0]-v_t_unit,v_t_round_prec)
	
	#the time at which the control decision will be updated
	t_upd_ctrl=fct_calcul_t_update_ctrl(va_t_end_last_control_of_seq_ctrls=t_end_current_icm, va_dt=v_dt,va_t_round_precision=v_t_round_prec,\
	va_t_unit=v_t_unit)

	
	#duration_cycle=v_network.get_control_actuate_obj().get_di_param_mp_ctrl()[v_intersection.get_id_node()][1]
	#duration_cycle=li_param_control[1]

	
		 


		
	#creation d'un objet intersection control, pour le MP controle,  le prochain type de controle sera rd clear, on n'a pas besoin ici d type
	#mais on l'indique quand meme pour le moment. Ensuite on va l'enlever
	inters_control_obj_mp=Cl_Intersection_Control.Intersection_Control(\
	val_di_intersection_control_mat=icm,val_t_start_control= t_start, \
	val_type_control=Cl_Control_Actuate.TYPE_CONTROL[14],\
	val_type_control_related_to_t_revision=Cl_Control_Actuate.TYPE_CONTROL_T_REVISION_CATEGORY["without_sensor_requirement_for_t_update"],\
	val_t_end_control= t_end_current_icm,val_duration_control=param_control[0],\
	val_estim_turn_ratios_with_current_ctrl=v_network.get_di_intersections()[v_intersection.get_id_node()].get_estimated_turn_ratios(),\
	val_id_actuated_stage=mp_inters_control_stage[1],val_t_update_ctrl=t_upd_ctrl)
	
	
		
	#calcul de l'indice de la liste des param de MP a utiser la prochaine fois
	#si l'indice courant est l'avant dernier (le dernier= duree cycle)
	#if indice_choix_duree==v_network.get_control_actuate_obj().\
	#get_di_param_mp_ctrl()[v_intersection.get_id_node()][2]-1:
		#indice_choix_duree=-1
		
	#if indice_choix_duree==li_param_control[2]-1:
		#indice_choix_duree=-1

		
		
	#on maj l'indice  pour le prochain choix de durees dans control actuate objet
	#v_network.get_control_actuate_obj().get_di_param_mp_ctrl()[v_intersection.get_id_node()][3]=indice_choix_duree
	#li_param_control[3]=indice_choix_duree
		
		
	
	li_ico=[inters_control_obj_mp]
	
	
	
		
	#on retourne une liste d' inters control objet, le type du prochain controle a appliquer lors du (prochain) even en_decision_icm]
	#we return [[li ico], type next control, indicator that an event end decis should be created,indicator,
	#0 or 1 for indicating whether turn ratios will/not be estimated at the next decision]
	return[li_ico, List_Explicit_Values.initialisation_value_to_fourteen,List_Explicit_Values.initialisation_value_to_one,\
	v_network.get_di_intersections()[v_intersection.get_id_node()].get_estimated_turn_ratios()]
		
		

#*****************************************************************************************************************************************************************************************

















