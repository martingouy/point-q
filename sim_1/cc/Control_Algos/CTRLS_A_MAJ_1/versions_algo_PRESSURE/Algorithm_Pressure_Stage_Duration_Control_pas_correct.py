import Cl_Intersection_Control
import Cl_Control_Actuate
import Cl_Network_Link
import Cl_Decisions
import List_Explicit_Values
import math




#*****************************************************************************************************************************************************************************************
#method returning the pressure exerted by an intersection control matrix
#val_intersection=the id of the intersection node
#val_inters_stage=list of the simult actuates phases
def fct_calcul_pressure_exerted_by_an_inters_control_matrix(val_intersection,val_inters_stage,val_network,val_round_prec):
	
	pres_exerted=0
	
	#if val_intersection.get_id_node()==1:
		#print()
		#print("val_intersection",val_intersection.get_id_node())
		#print("val_inters_stage",val_inters_stage)
	
	#par example un inters stage [[7,8],[9,10]] actaul simult phases [7,8] et [9,10]
	#pour chaque  phase du  stage , (le stage actualise seulement les queues des phases qu'il contient), 
	for i in val_inters_stage:
		if val_intersection.get_id_node()==2:
			print()
			print(" inter stage",i)
		# nombre des véhicules en que, q(l,m)
		le=len(val_network.get_di_entry_internal_links()[i[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()[i[0],i[1]].get_queue_veh())
		#if val_intersection.get_id_node()==1:
			#print("length que",le)
		if val_intersection.get_id_node()==2:
			print("le",le)
		#calcule de la somme  sur les output links de la phase (queue length output link x routing prop), cad, 
		#somme sur p gamma(m,p) x q(m,p)
		som=0
		
		#if le>0:
		#si l'output link de la queue n'est pas exit on calcule  la somme
		if val_network.get_di_all_links()[i[1]].get_type_network_link() != Cl_Network_Link.TYPE_NETWORK_LINK["exit"]:
		
			#pour chaque que de l'output link`
			for j in val_network.get_di_entry_internal_links()[i[1]].get_set_veh_queue().get_di_obj_veh_queue_at_link():
				if val_intersection.get_id_node()==2:
					print("que de output link",i[1], "est",j)
					print("val_intersection.get_di_key_id_phase_value_li_rout_prob()",\
					val_network.get_di_intersections()[val_network.get_di_entry_internal_links()[i[1]].get_id_head_intersection_node()].\
					get_di_key_id_phase_value_li_rout_prob())
					
				#the product of the turn ratio x queue length (gamma(m,p) x q(m,p))
				a=val_network.get_di_intersections()[val_network.get_di_entry_internal_links()[i[1]].get_id_head_intersection_node()].\
				get_di_key_id_phase_value_li_rout_prob()[j[0],j[1]][0] *\
				len(val_network.get_di_entry_internal_links()[i[1]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
				[j[0],j[1]].get_queue_veh())
					
				if val_intersection.get_id_node()==2:
					print("som",som,"a",a)
					
				som+=a
				if val_intersection.get_id_node()==2:
					print("som",som)
					
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
		if val_intersection.get_id_node()==2:
			print("pres_exerted",pres_exerted)
	
	pressure_exerted=round(pres_exerted,val_round_prec)
	if val_intersection.get_id_node()==2:
		print("pressure_exerted",pressure_exerted)
	return pressure_exerted

#*****************************************************************************************************************************************************************************************
#method calculating the actuation duration of each intersection stage
#it returns a dictionary, key= id intersection stage, value=actuation duartion
#va_duree_idle_time=total duree red clear par cycle
#va_negative_pres= the defautl value to attribu to a pressure of a stage when its value is negative
def fct_calculation_actuation_duration_each_intesection_stage(va_inters,va_netw,va_duree_cycle,va_duree_idle_time,va_round_precis,va_t_round_precis,\
va_negative_pres=0):

	di_key_id_stage_value_actuat_duration={}
	
	di_key_id_intersection_stage_value_exerted_pressure={}
	
	#la somme de toutes les pressions
	som_p=0
	
	#pour chaque stage de l'intersection, on calcule la pression exerce
	for i in va_inters.get_di_stages_sign_intersection():
	
		exerted_pressure=fct_calcul_pressure_exerted_by_an_inters_control_matrix(\
		val_intersection=va_inters,val_inters_stage=va_inters.get_di_stages_sign_intersection()[i],\
		val_network=va_netw,val_round_prec=va_round_precis)
		
		if exerted_pressure<0:
			exerted_pressure=va_negative_pres
			
		di_key_id_intersection_stage_value_exerted_pressure[i]=exerted_pressure
		
		#print("exerted_pressure",exerted_pressure)
		
		#on calcule la somme de toutes les pressions (de tous les stages)
		som_p+=exerted_pressure
		#print("som_p",som_p)
	
	if va_inters.get_id_node()==2:
		print("exerted_pressure",exerted_pressure)
		print("som_p",som_p)
		
	#som_duree_act=0
	
	nb_stages=len(va_inters.get_di_stages_sign_intersection())
	
	avail_time=va_duree_cycle-va_duree_idle_time
	if va_inters.get_id_node()==2:
		print("avail_time",avail_time)
	
	#la duree d'actualisation de chaque stage si on  attribue a chaque stage la meme duree
	duree_act_1=round(avail_time/nb_stages,va_t_round_precis)
	

	for j in va_inters.get_di_stages_sign_intersection():
		
		#si la somme de toutes les pressions >0
		if som_p>0:
			#on calcul la duree d'actualisation du stage
			duree_act=round((di_key_id_intersection_stage_value_exerted_pressure[j]/som_p)*avail_time,va_round_precis)
			if duree_act==0:
				print("duree_act lors qom>0: ",duree_act,di_key_id_intersection_stage_value_exerted_pressure[j],som_p,\
				di_key_id_intersection_stage_value_exerted_pressure[j]/som_p,som_p)
				#import sys
				#sys.exit()
			di_key_id_stage_value_actuat_duration[j]=duree_act
		elif som_p<0:	
			print("PROBLEME IN ALGORITH PD SOM TOUTES PRESSIONS <0, A REFLECHIR , som_p: ",som_p)
			import sys
			sys.exit()
		#si la som_p de toutes les pressions =0
		else:
			
			di_key_id_stage_value_actuat_duration[j]=duree_act_1
			if duree_act_1==0:
				print("avail_time",avail_time,"nb_stages",nb_stages,avail_time/nb_stages)
				import sys
				sys.exit()
		
			
		if va_inters.get_id_node()==2:
			print("di_key_id_stage_value_actuat_duration",di_key_id_stage_value_actuat_duration)
		#som_duree_act+=duree_act
	
	#if som_duree_act==0:
		#duree_act_chaque_stage=(va_duree_cycle-va_duree_idle_time)/len(va_inters.get_di_stages_sign_intersection(),va_round_precis)
	
	#for m in di_key_id_stage_value_actuat_duration:
		#di_key_id_stage_value_actuat_duration[i]=duree_act_chaque_stage
	
	s=0
	for m in di_key_id_stage_value_actuat_duration:
		s+=di_key_id_stage_value_actuat_duration[m]
	if s==0:
		print("di_key_id_stage_value_actuat_duration",di_key_id_stage_value_actuat_duration)
		import sys
		sys.exit()
	return di_key_id_stage_value_actuat_duration
		
		
#*****************************************************************************************************************************************************************************************
#method returning the mp intersection control object for the next period
#on retourne une liste d' inters control objet and le type du prochain controle a appliquer par le (prochain) even en_decision_icm

def admissible_intersection_control_object_next_period_psd(v_intersection,v_network,li_ctrl_param_duree_cycle_and_red_clear,\
v_round_prec,v_t_round_precis,v_t_end_current_network_control_matrix,v_t_unit):
	
	#list with the intersection control objects we will return 
	li_ico=[]

	#dict, key=id stage, valeur= duree d'actulaisation
	di_key_id_stage_val_act_dur=fct_calculation_actuation_duration_each_intesection_stage(\
	va_inters=v_intersection,va_netw=v_network,va_duree_cycle=li_ctrl_param_duree_cycle_and_red_clear[0],\
	va_duree_idle_time=li_ctrl_param_duree_cycle_and_red_clear[1],va_round_precis=v_round_prec,va_t_round_precis=v_t_round_precis)
	
		
	
	#calcul de la duree de RC (par stage)
	duree_red_clear=round(li_ctrl_param_duree_cycle_and_red_clear[1]/len(di_key_id_stage_val_act_dur),v_t_round_precis)
		
		
	#duree additionnelle red_clear, lorsque  duree d'un  stage vaut 0
	t_addit_rc=duree_red_clear
	
	va_t_end_current_network_control_matrix=v_t_end_current_network_control_matrix
	
	#avail_time=va_duree_cycle-va_duree_idle_time
	avail_time=li_ctrl_param_duree_cycle_and_red_clear[0]-li_ctrl_param_duree_cycle_and_red_clear[1]
	
	for i in di_key_id_stage_val_act_dur:
		#si la duree d'actualis d'un stage est strict positive
		if di_key_id_stage_val_act_dur[i]>0:
		
			#creat d'une matrice controle intersection
			icm=dict(v_intersection.get_di_intersection_control_matrix())
			
			for j in  v_intersection.get_di_stages_sign_intersection()[i]:
				icm[j[0],j[1]]=1
				
			t_start=round(va_t_end_current_network_control_matrix+v_t_unit,v_t_round_precis)
			
			t_end_current_icm=round(t_start+di_key_id_stage_val_act_dur[i]-v_t_unit,v_t_round_precis)
			
			duration_cycle=li_ctrl_param_duree_cycle_and_red_clear[0]
			
			t_end_cycle=round(math.ceil( t_end_current_icm/duration_cycle)*duration_cycle,v_t_round_precis)
			
			#creation d'un objet intersection control, pour le MP controle,  le prochain type de controle sera rd clear, bien qu'on n'a pas besoin ici du type
			#on l'indique quand meme pour le moment. Ensuite on va l'enlever
			inters_control_obj_psd=Cl_Intersection_Control.Intersection_Control(\
			val_di_intersection_control_mat=icm,val_t_start_control= t_start, \
			val_t_end_control= t_end_current_icm,val_duration_control=di_key_id_stage_val_act_dur[i],\
			val_cycle_duration_associated_with_control=duration_cycle,val_type_control=Cl_Control_Actuate.TYPE_CONTROL[8])
			
			li_ico.append(inters_control_obj_psd)
			
			#creation d'un type de controle red clear
			t_start_red_clear=round(t_end_current_icm+v_t_unit,v_t_round_precis)
		
		
			#t_end_cycle=round(math.ceil( t_end_current_icm/duration_cycle)*duration_cycle,v_round_prec)
		 
			#si on a n'a pas saute un stage, la duree d'actual de rc sera duree_red_clear
			if t_addit_rc==duree_red_clear:
				#si la duree du stage n'est pas egale a T-L, cas lorsque tout le temps disponible est 
				#attribue au  premier stage
				if di_key_id_stage_val_act_dur[i] !=avail_time:
			
					t_end_current_icm_rc=round(t_start_red_clear+duree_red_clear-v_t_unit,v_t_round_precis)
				
					#creation d'un objet intersection control, pour la RC, le prochain type de controle sera MP
					inters_control_obj_rc=Cl_Intersection_Control.Intersection_Control(\
					val_di_intersection_control_mat=v_intersection.get_di_intersection_control_matrix(),\
					val_t_start_control= t_start_red_clear, \
					val_t_end_control= t_end_current_icm_rc,val_duration_control=duree_red_clear,\
					val_cycle_duration_associated_with_control=duration_cycle,val_type_control=Cl_Control_Actuate.TYPE_CONTROL[0])
				else:
					
					
					dur_rc=li_ctrl_param_duree_cycle_and_red_clear[1]
					
					t_end_current_icm_rc=round(t_start_red_clear+dur_rc-v_t_unit,v_t_round_precis)
					
					#creation d'un objet intersection control, pour la RC, le prochain type de controle sera MP
					inters_control_obj_rc=Cl_Intersection_Control.Intersection_Control(\
					val_di_intersection_control_mat=v_intersection.get_di_intersection_control_matrix(),\
					val_t_start_control= t_start_red_clear, \
					val_t_end_control= t_end_current_icm_rc,val_duration_control=dur_rc,\
					val_cycle_duration_associated_with_control=duration_cycle,val_type_control=Cl_Control_Actuate.TYPE_CONTROL[0])
			
			#si on a  saute un stage, la duree d'actual de rc sera t_addit_rc 
			else:
				
				
				
				t_end_current_icm_rc=round(t_start_red_clear+t_addit_rc-v_t_unit,v_t_round_precis)
				
				#creation d'un objet intersection control, pour la RC, le prochain type de controle sera MP
				inters_control_obj_rc=Cl_Intersection_Control.Intersection_Control(\
				val_di_intersection_control_mat=v_intersection.get_di_intersection_control_matrix(),\
				val_t_start_control= t_start_red_clear, \
				val_t_end_control= t_end_current_icm_rc,val_duration_control=t_addit_rc,\
				val_cycle_duration_associated_with_control=duration_cycle,val_type_control=Cl_Control_Actuate.TYPE_CONTROL[0])
				
				#maj du temps addition de RC
				t_addit_rc=duree_red_clear
	
			li_ico.append(inters_control_obj_rc)
		
			va_t_end_current_network_control_matrix=t_end_current_icm_rc
			
		#si la duree d'actualis d'un stage est zero
		elif di_key_id_stage_val_act_dur[i]==0:
			#maj  du temps de red clear
			t_addit_rc+=duree_red_clear
		
		#si la duree d'actualis d'un stage est negative
		else:
			print("PROBLEME DS ALGO PRESSURE STAGE ACT DUR CONTROL, FCT admissible_intersection_control_object_next_period_psd,\
			duree act stage negative: ",di_key_id_stage_val_act_dur[i])
			import sys
			sys.exit()
			
	#on retourne une liste d' inters control objet, le type du prochain controle a appliquer par le (prochain) even en_decision_icm]
	
	return[li_ico, List_Explicit_Values.initialisation_value_to_eight]

#*****************************************************************************************************************************************************************************************

















