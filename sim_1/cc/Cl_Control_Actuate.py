import Control_Algos.Algorithm_FT_Control as Algorithm_FT_Control
import Control_Algos.Algorithm_FT_Control_Offset as Algorithm_FT_Control_Offset
import Control_Algos.Algorithm_MP_Control as Algorithm_MP_Control
#import Control_Algos.Algorithm_MIXED_Control as Algorithm_MIXED_Control
##import Control_Algos.Algorithm_Pressure_Stage_Duration_Control as Algorithm_Pressure_Stage_Duration_Control
#import Control_Algos.Algorithm_MP_Control_sans_output_ques as Algorithm_MP_Control_sans_output_ques
#import Control_Algos.Algorith_FA_no_red_clear_Control as Algorith_FA_no_red_clear_Control
#import Control_Algos.Algorith_FA_with_red_clear_Control as Algorith_FA_with_red_clear_Control
#import Control_Algos.Algorith_FA_Max_Green_Control as Algorith_FA_Max_Green_Control
##import Control_Algos.Algorithm_MP_MOD_Control as Algorithm_MP_MOD_Control
import Control_Algos.Algorithm_MP_PRAC_Control  as Algorithm_MP_PRAC_Control
import Control_Algos.Algorithm_MP_Control_without_red_clear as Algorithm_MP_Control_without_red_clear
import Control_Algos.Algorithm_MP_PRAC_Control_without_red_clear as Algorithm_MP_PRAC_Control_without_red_clear

#the control category related to the time at which the control should be revised
TYPE_CONTROL_T_REVISION_CATEGORY={"without_sensor_requirement_for_t_update":1,"sensor_requirement_for_t_update":0}

#type of control
#TYPE_CONTROL={0:"type_control_red_clear",1:"type_control_FT", 2:"type_control_FT_Offset", 3:"type_control_MP",4:"type_control_MIXED",\
#5:"type_control_MP_pro",6:"type_control_MP_pro_wasteful",\
#7:"type_control_PREDEFINED",8:"type_control_pressure_stage_duration",(1,3):"type_prev_sim_FT_type_contin_new_one_MP",
#9:"type_control_MP_No_output_que",10:"type_control_FA",11:"type_control_FA_Max_Green",\
#12:"type_control_MP_when_OD_matrices_considered",13:"type_control_MP_Practical"}

TYPE_CONTROL={0:"type_control_red_clear",1:"type_control_FT", 2:"type_control_FT_Offset", 3:"type_control_MP",4:"type_control_MIXED",\
5:"type_control_MP_pro",6:"type_control_MP_pro_wasteful",\
9:"type_control_MP_No_output_que",10:"type_control_FA_no_red_clear",11:"type_control_FA_Max_Green",\
12:"type_control_FA_with_red_clear",13:"type_control_MP_Practical",14:"type_control_MP_without_red_clear",\
15:"type_control_MP_Practical_without_rec_clear"}

#control to employe
#NAMES_CONTROL={"type_control_FT":Algorithm_FT_Control.admissible_intersection_control_objects_next_cycle_ft,\
#"type_control_FT_Offset":Algorithm_FT_Control_Offset.admissible_intersection_control_objects_next_cycle_ft_offset}

#list parameters of each control
#LI_PARAM_CONTROLS={"type_control_FT":[va_li_param_ft_ctrl,va_li_inters_control_matrix,va_li_intersection_stages,\
#va_t_end_current_intersection_control,va_t_unit,va_t_round_prec],\
#"type_control_FT_Offset":[va_li_param_ft_offset_ctrl,va_li_inters_control_matrix,va_li_intersection_stages,va_t_end_current_intersection_control,\
#va_t_unit,va_t_round_prec]}


#val_di_addition_param_mp_ctrl= dcit, key=id phases input output link related to the inter, value=Q valeu
#Control_Actuate will be an object of the network (created once) so either it should be  created correctly from the beginning or molified with the 
#appropriate "set" functions.
class Control_Actuate:
	
	def __init__(self,val_li_param_ft_ctrl=None,val_li_param_ft_offset_ctrl=None,val_li_param_mp_ctrl=None,\
	val_di_addition_param_mp_ctrl=None,
	val_li_param_ft_for_mixed_ctrl=None,val_li_param_mp_for_mixed_ctrl=None,val_li_param_psd_ctrl=None,\
	val_li_param_control_MP_no_output_que=None,val_li_param_control_FA_ctrl=None,\
	val_li_param_control_FA_with_red_clear_ctrl=None,\
	val_li_param_control_FA_Max_Green_ctrl=None,val_li_param_control_MP_Practical_ctrl=None,\
	val_di_addition_param_mp_pract_ctrl=None,\
	val_type_employed_ctrl=None,val_type_ctrl_categ=None,\
	val_li_param_control_MP_without_red_clear=None,val_di_addition_param_mp_without_red_clear_ctrl=None,\
	val_li_param_control_MP_Pract_without_red_clear=None,val_di_addition_param_mp_pract_without_red_clear_ctrl=None,\
	val_li_param_control_MP_Pract=None):
	#,val_turn_ratios_estim=None):
	
		#the li with the parameters if the FT control, key=id nd, value=list param related to the inter
		self._li_param_ft_ctrl=val_li_param_ft_ctrl
		
		#the lict with the parameters of the ft offset cotnrol (for the 1st cycle). For this type of ctnrol self._li_param_ft_ctrl must be lif of None
		self._li_param_ft_offset_ctrl=val_li_param_ft_offset_ctrl
		
		#the param of MP control; list=lict,
		#the lict with the paramet of MP control,list=[ [...,[duration MP icm, dur red clear],...], cycle duration,nb decicions,-1] 
		#le -1  sera utilise pour choisir la duree de MP icm dans la liste [...,[duration MP icm, dur red clear],...],
		#nb de durees d'actualisation=len([...,[duration MP icm, dur red clear],...])
		self._li_param_mp_ctrl=val_li_param_mp_ctrl
		
		#the additional param for MP with the Qvalues of each phase
		self._di_addition_param_mp_ctrl=val_di_addition_param_mp_ctrl
		
		#the dictionary with the param of FT control when mixed control is employed
		self._li_param_ft_for_mixed_ctrl=val_li_param_ft_for_mixed_ctrl
		
		
		#the dictionary with the param of MP control when mixed control is employed
		self._li_param_mp_for_mixed_ctrl=val_li_param_mp_for_mixed_ctrl
		
		#the list with the param of psd (pressure stage duration) cotrol
		self._li_param_psd_ctrl=val_li_param_psd_ctrl
		
		#the lict with the param of the MP control, which does not take into consideration the output que
		self._li_param_control_MP_no_output_que=val_li_param_control_MP_no_output_que
		
		#the list with the param of a fully actuated control without red clear
		self._li_param_control_FA_ctrl=val_li_param_control_FA_ctrl
		
		#the list of param of a fully actuated control with red clear
		self._li_param_control_FA_with_red_clear_ctrl=val_li_param_control_FA_with_red_clear_ctrl
		
		#the lict with the param of a fully actuated  with max green continuous duration permitted control
		self._li_param_control_FA_Max_Green_ctrl=val_li_param_control_FA_Max_Green_ctrl
		
		#the list with the param of MP Practical control
		self._li_param_control_MP_Practical_ctrl=val_li_param_control_MP_Practical_ctrl
		
		#the dict with the values of Q matrix for the Qweighted MP pract
		self._di_addition_param_mp_pract_ctrl=val_di_addition_param_mp_pract_ctrl
		
		
		#variable indicating the type of  the employed control at least during the next decision (for the next decisions it is the controller who will decide)
		self._type_employed_ctrl=val_type_employed_ctrl
		
		#variable indicating the control category
		self._type_ctrl_categ=val_type_ctrl_categ
		
		
		#the list with the paramet of MP - no red clearance
		self._li_param_control_MP_without_red_clear=val_li_param_control_MP_without_red_clear
		
		#the list with the param of MP -Pract-no red clear
		self._li_param_control_MP_Pract_without_red_clear=val_li_param_control_MP_Pract_without_red_clear
		
		#variable indicating whether turn ratios will be estimated at least during the first decision
		#self._turn_ratios_estim=val_turn_ratios_estim
		
		#the additional param for MP without red clear with the Qvalues of each phase
		self._di_addition_param_mp_without_red_clear_ctrl=val_di_addition_param_mp_without_red_clear_ctrl
		
		#the additional param witth the Qvalues for the phases, when	a MP pract without red clear is employed
		self._di_addition_param_mp_pract_without_red_clear_ctrl=val_di_addition_param_mp_pract_without_red_clear_ctrl
	
		
#*****************************************************************************************************************************************************************************************
	#method returning the control type to apply
	#def get_type_control_to_employ(self):
		#return self._type_control_to_employ

#*****************************************************************************************************************************************************************************************
	#method molifying the control type to apply
	#def set_type_control_to_employ(self,n_v):
		#self._type_control_to_employ=n_v

#*****************************************************************************************************************************************************************************************
	#method returning the parameters of the FT control
	def get_li_param_ft_ctrl(self):
		return self._li_param_ft_ctrl

#*****************************************************************************************************************************************************************************************
	#method returning the lict with the parameters of the ft offset cotnrol (for the 1st cycle)
	def get_li_param_ft_offset_ctrl(self):
		return self._li_param_ft_offset_ctrl

#*****************************************************************************************************************************************************************************************
	#method returning the list with the param of MP control, 
	def get_li_param_mp_ctrl(self):
		return self._li_param_mp_ctrl
#*****************************************************************************************************************************************************************************************
	#method returning the dict with the addtion param of MP control (with the Qvalues of each phase)
	def get_di_addition_param_mp_ctrl(self):
		return self._di_addition_param_mp_ctrl

#*****************************************************************************************************************************************************************************************
	#method returning the lictionary with the param of FT control when mixed control is employed
	def get_li_param_ft_for_mixed_ctrl(self):
		return self._li_param_ft_for_mixed_ctrl
	
#*****************************************************************************************************************************************************************************************
	#method returning the lictionary with the param of MP control when mixed control is employed
	def get_li_param_mp_for_mixed_ctrl(self):
		return self._li_param_mp_for_mixed_ctrl
		
#*****************************************************************************************************************************************************************************************
	#method returning the lict  with the parem of psd cotnrol
	def get_li_param_psd_ctrl(self):
		return self._li_param_psd_ctrl
#*****************************************************************************************************************************************************************************************
	#method returning the lict with the param of the MP without take into consoder output que
	def get_li_param_control_MP_no_output_que(self):
		return self._li_param_control_MP_no_output_que
#*****************************************************************************************************************************************************************************************
	#method returning the list with the parem of a fully actuated control
	def get_li_param_control_FA_ctrl(self):
		return self._li_param_control_FA_ctrl
#*****************************************************************************************************************************************************************************************
	#method returning the list with the param of a FA control with red clear
	def get_li_param_control_FA_with_red_clear_ctrl(self):
		return self._li_param_control_FA_with_red_clear_ctrl
#*****************************************************************************************************************************************************************************************
	#method returning the lict with the parem of a fully actuated control
	def get_li_param_control_FA_Max_Green_ctrl(self):
		return self._li_param_control_FA_Max_Green_ctrl
#*****************************************************************************************************************************************************************************************
	#method returning the lict with the param of MP practical control
	def get_li_param_control_MP_Practical_ctrl(self):
		return self._li_param_control_MP_Practical_ctrl

#*****************************************************************************************************************************************************************************************
	#method returning the dict with the  values if the Q matrix for the Qweighted MP control
	def get_di_addition_param_mp_pract_ctrl(self):
		return self._di_addition_param_mp_pract_ctrl

#*****************************************************************************************************************************************************************************************
	#method returning the variable indicating the type of  the employed control
	def get_type_employed_ctrl(self):
		return self._type_employed_ctrl
	
#*****************************************************************************************************************************************************************************************
	#method returning the variable indicating the control catgory
	def get_type_ctrl_categ(self):
		return self._type_ctrl_categ
	
#*****************************************************************************************************************************************************************************************
	#method returning the list woth the param of the MPno red clear
	def get_li_param_control_MP_without_red_clear(self):
		return self._li_param_control_MP_without_red_clear

#*****************************************************************************************************************************************************************************************
	
	#method returning the the additional param for MP without red clear with the Qvalues of each phase
	def get_di_addition_param_mp_without_red_clear_ctrl(self):
		return self._di_addition_param_mp_without_red_clear_ctrl
	
#*****************************************************************************************************************************************************************************************
	#method returning the additional param witth the Qvalues for the phases, when	a MP pract without red clear is employed
	def get_di_addition_param_mp_pract_without_red_clear_ctrl(self):
		return self._di_addition_param_mp_pract_without_red_clear_ctrl


#*****************************************************************************************************************************************************************************************
	
	#method returning the variable indicating whether turn ratios will be estimated at least during the first decision
	#def get_turn_ratios_estim(self):
		#return self._turn_ratios_estim


#*****************************************************************************************************************************************************************************************

	#method molifying the parameters of the FT control
	def set_li_param_ft_ctrl(self,n_v):
		self._li_param_ft_ctrl=n_v

#*****************************************************************************************************************************************************************************************
	#method molifying the lict with the parameters of the ft offset cotnrol (for the 1st cycle)
	def set_li_param_ft_offset_ctrl(self,n_v):
		self._li_param_ft_offset_ctrl=n_v

#*****************************************************************************************************************************************************************************************
	#method molifying the lict with the param of MP control, 
	def set_li_param_mp_ctrl(self,n_v):
		self._li_param_mp_ctrl=n_v
		
#*****************************************************************************************************************************************************************************************
	#method modifying the dict with the addtion param of MP control (with the Qvalues of each phase)
	def set_di_addition_param_mp_ctrl(self,n_v):
		self._di_addition_param_mp_ctrl=n_v

#*****************************************************************************************************************************************************************************************

	#method molifying the lictionary with the param of FT control when mixed control is employed
	def set_li_param_ft_for_mixed_ctrl(self,n_v):
		self._li_param_ft_for_mixed_ctrl=n_v
	
#*****************************************************************************************************************************************************************************************
	#method returning the lictionary with the param of MP control when mixed control is employed
	def set_li_param_mp_for_mixed_ctrl(self,n_v):
		self._li_param_mp_for_mixed_ctrl=n_v
		
#*****************************************************************************************************************************************************************************************
	#method molifying the lict  with the parem of psd cotnrol
	def set_li_param_psd_ctrl(self,n_v):
		self._li_param_psd_ctrl=n_v
#*****************************************************************************************************************************************************************************************
	#method molifying the lict with the param of the MP without take into consoder output que
	def set_li_param_control_MP_no_output_que(self,n_v):
		self._li_param_control_MP_no_output_que=n_v
#*****************************************************************************************************************************************************************************************
	#method  molifying the lict with the parem of a fully actuated control
	def set_li_param_control_FA_ctrl(self,n_v):
		self._li_param_control_FA_ctrl=n_v
	
#*****************************************************************************************************************************************************************************************
	#method modifying the list with the param of a FA control with red clear
	def set_li_param_control_FA_with_red_clear_ctrl(self,n_v):
		self._li_param_control_FA_with_red_clear_ctrl=n_v
#*****************************************************************************************************************************************************************************************
	#method  molifying  the lict with the parem of a fully actuated control
	def set_li_param_control_FA_Max_Green_ctrl(self):
		self._li_param_control_FA_Max_Green_ctrl=n_v


#*****************************************************************************************************************************************************************************************
	#method molifying the lict with the param of MP practical control
	def set_li_param_control_MP_Practical_ctrl(self,n_v):
		self._li_param_control_MP_Practical_ctrl=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the dict with the  values if the Q matrix for the Qweighted MP control
	def set_di_addition_param_mp_pract_ctrl(self,n_v):
		self._di_addition_param_mp_pract_ctrl=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the variable indicating the type of  the employed control
	def set_type_employed_ctrl(self,n_v):
		self._type_employed_ctrl=n_v
	
#*****************************************************************************************************************************************************************************************
	#method modifyiing the variable indicating the control catgory
	def set_type_ctrl_categ(self,n_v):
		self._type_ctrl_categ=n_v
	
#*****************************************************************************************************************************************************************************************
	#method modifying the list woth the param of the MPno red clear
	def set_li_param_control_MP_without_red_clea(self,n_v):
		self._li_param_control_MP_without_red_clear=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the list with the param of MP Pract without red cleat
	def set_li_param_control_MP_Pract_without_red_clear(self,n_v):
		self._li_param_control_MP_Pract_without_red_clear=n_v



#*****************************************************************************************************************************************************************************************
	#method modifying the variable indicating whether turn ratios will be estimated at least during the first decision
	#def set_turn_ratios_estim(self,n_v):
		#self._turn_ratios_estim=n_v


#*****************************************************************************************************************************************************************************************
	#method modifying the the additional param for MP without red clear with the Qvalues of each phase
	def set_di_addition_param_mp_without_red_clear_ctrl(self,n_v):
		self._di_addition_param_mp_without_red_clear_ctrl=n_v
	

#*****************************************************************************************************************************************************************************************
	#method modifying the addit param for the weighted MP-pract
	def set_li_param_control_MP_Pract(self,n_v):
		self._li_param_control_MP_Pract=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the additional param witth the Qvalues for the phases, when	a MP pract without red clear is employed
	def set_di_addition_param_mp_pract_without_red_clear_ctrl(self,n_v):
		self._di_addition_param_mp_pract_without_red_clear_ctrl=n_v


#*****************************************************************************************************************************************************************************************
	#method returning the list of the controls requiring sensor monitoring and for which there exist a limited continuous actuation duration for each stage
	#(the contrls generate an event end decicion next intersection control)
	def fct_list_ctrl_types_generating_future_ctrl_decision(self):
		return[TYPE_CONTROL[11]]

#*****************************************************************************************************************************************************************************************
	#method returning the list of the controls requiring sensor monitoring without a limited continuous actuation duration for each stage
	#(these cotrls do  not generate an event end decicion next intersection control)
	def fct_list_ctrl_types_without_generating_future_ctrl_decision(self):
		return[TYPE_CONTROL[10],TYPE_CONTROL[12]]

#*****************************************************************************************************************************************************************************************
	#method returning the list with control types requiring sensor monitoring (the control decision update depends upon the flow value) 
	def fct_list_ctrl_types_requiring_sensor_monit_and_having_first_param_permited_flow_value(self):
		return [TYPE_CONTROL[10],TYPE_CONTROL[11],TYPE_CONTROL[12]]
#*****************************************************************************************************************************************************************************************
	#method returning the min allowed flow of each control requiring sensor monitoring
	def fct_min_allow_flow_sensor_requir_control(self,val_type_ctrl):
	
		#if the type of the control is FA without red clear
		if TYPE_CONTROL[val_type_ctrl]==TYPE_CONTROL[10]:
			return self._li_param_control_FA_ctrl[0]
		
		#if the type of the control is FA with red clear
		elif  TYPE_CONTROL[val_type_ctrl]==TYPE_CONTROL[12]:
			return self._li_param_control_FA_with_red_clear_ctrl[0]
		
		#if the type of the control is FA with max green duration and red clearance
		elif TYPE_CONTROL[val_type_ctrl]==TYPE_CONTROL[11]:
			return self._li_param_control_FA_Max_Green_ctrl[0]
		
		#if no of the previous cases
		else:
			print("PROBLEM IN CL CONTROL ACTUATE, IN FCT fct_min_allow_flow_sensor_requir_control, TYPE CTRL:",TYPE_CONTROL[val_type_ctrl])
			import sys
			sys.exit()

#*****************************************************************************************************************************************************************************************
	

	#functioning selecting the appropriate control to apply and
	#returns [[li ico], type of  next control,  0 to inlicate that no even end decis will be genereted by en even end dec]
	#val_indicator_whether_estim_rout_prob_during_first_decis 0 or 1
	def fct_select_appropriate_control(self,va_id_nd,va_type_control_to_employ,val_indicator_whether_estim_rout_prob_during_first_decis,\
	va_di_inters_control_matrix,va_di_intersection_stages,va_t_end_current_intersection_control,va_t_unit,va_round_precis,va_t_round_prec,\
	va_network,va_init_small_val=-10**10,val_t_current=-1,va_sim_dur=-1,va_marge_dt=None,va_t_start_sim=0):
		
		
		#if the control type to apply is FT
		if TYPE_CONTROL[va_type_control_to_employ]==TYPE_CONTROL[1]:
			
			
			re=Algorithm_FT_Control.admissible_intersection_control_objects_next_cycle_ft(\
			val_li_param_ft_ctrl=self._li_param_ft_ctrl,val_di_inters_control_matrix=va_di_inters_control_matrix,\
			val_di_intersection_stages=va_di_intersection_stages,val_t_end_current_intersection_control=va_t_end_current_intersection_control,\
			val_t_unit=va_t_unit,val_t_round_prec=va_t_round_prec,val_dt=va_marge_dt)
			#,\
			#val_indicator_whether_estim_rout_prob_next_control=val_indicator_whether_estim_rout_prob_during_first_decis)
			
			
			return re
			
		#if the control type to apply is FT with offset
		elif TYPE_CONTROL[va_type_control_to_employ]==TYPE_CONTROL[2]:
		
			#print("va_id_nd",va_id_nd)
		
			re=Algorithm_FT_Control_Offset.admissible_intersection_control_objects_next_cycle_ft_offset(\
			val_li_param_ft_offset_ctrl=self._li_param_ft_offset_ctrl,\
			val_dic_inters_control_matrix=va_di_inters_control_matrix,\
			val_dic_intersection_stages=va_di_intersection_stages,\
			val_t_end_current_inters_control=va_t_end_current_intersection_control,\
			val_ti_unit=va_t_unit,val_ti_round_prec=va_t_round_prec,\
			v_val_dt=va_marge_dt)
			
			
			return re
			
		#if the control to apply is MP
		elif TYPE_CONTROL[va_type_control_to_employ]==TYPE_CONTROL[3]:
		
			#print(self._li_param_mp_ctrl[va_id_nd])
			#the lict with the paramet of MP control, key=id node, value=[duration MP icm, dur red clear, cycle duration]
			#self._li_param_mp_ctrl
			#re=Algorithm_MP_Control.admissible_intersection_control_object_next_period_mp(\
			#v_intersection=va_network.get_li_intersections()[va_id_nd],v_network=va_network,\
			#li_param_control=va_network.get_control_actuate_obj().get_li_param_mp_ctrl(),\
			#v_round_prec=va_round_precis,\
			#v_t_round_prec=va_t_round_prec,\
			#v_t_end_current_network_control_matrix=va_t_end_current_intersection_control,\
			#v_t_unit=va_t_unit,v_init_small_val=va_init_small_val)
			
			#if turn ratios will not be estimated
			if val_indicator_whether_estim_rout_prob_during_first_decis==0:
				v_key_for_selecting_turn_ratio_values=1
			#if turn ratios will be estimated
			else:
				v_key_for_selecting_turn_ratio_values=2
			
			re=Algorithm_MP_Control.admissible_intersection_control_object_next_period_mp(\
			v_intersection=va_network.get_di_intersections()[va_id_nd],v_network=va_network,\
			li_param_control=self._li_param_mp_ctrl,\
			v_round_prec=va_round_precis,\
			v_t_round_prec=va_t_round_prec,\
			v_t_end_current_network_control_matrix=va_t_end_current_intersection_control,\
			v_t_unit=va_t_unit,v_init_small_val=va_init_small_val,\
			val_di_id_phase_val_qweight=self._di_addition_param_mp_ctrl,\
			v_dt=va_marge_dt,)
			
			return re
		
		#if the control to apply is MIXED
		elif TYPE_CONTROL[va_type_control_to_employ]==TYPE_CONTROL[4]:	
		
			re=Algorithm_MIXED_Control.admissible_intersection_control_object_next_period_mixed(\
			v_li_param_ft_for_mixed_ctrl=self._li_param_ft_for_mixed_ctrl[va_id_nd],\
			v_di_inters_control_matrix=va_di_inters_control_matrix,\
			v_di_intersection_stages=va_di_intersection_stages,\
			v_t_end_current_intersection_control=va_t_end_current_intersection_control,\
			val_t_unit=va_t_unit,\
			val_round_prec=va_round_precis,\
			val_t_round_prec=va_t_round_prec,\
			val_intersection=va_network.get_li_intersections()[va_id_nd],\
			val_network=va_network,\
			va_init_small_val=va_init_small_val)
					
			return re
		#if the control is Pressure Stage durarion
		#elif va_type_control_to_employ==TYPE_CONTROL[8]:
		
			#re=Algorithm_Pressure_Stage_Duration_Control.admissible_intersection_control_object_next_period_psd(\
			#v_intersection=va_network.get_li_intersections()[va_id_nd],v_network=va_network,\
			#li_ctrl_param_duree_cycle_and_red_clear=self._li_param_psd_ctrl[va_id_nd],\
			#v_round_prec=va_round_precis,\
			#v_t_round_precis=va_t_round_prec,\
			#v_t_end_current_network_control_matrix=va_t_end_current_intersection_control,\
			#v_t_unit=va_t_unit)
			
			#return re
		
		#if the control is MP continuing a prev sim of FT control
		#elif va_type_control_to_employ==TYPE_CONTROL[(1,3)]:
			
			
			#re=Algorithm_MP_Control.admissible_intersection_control_object_next_period_mp(\
			#v_intersection=va_network.get_li_intersections()[va_id_nd],v_network=va_network,\
			#li_param_control=va_network.get_control_actuate_obj().get_li_param_mp_ctrl(),\
			#v_round_prec=va_round_precis,\
			#v_t_round_prec=va_t_round_prec,\
			#v_t_end_current_network_control_matrix=va_t_end_current_intersection_control,\
			#v_t_unit=va_t_unit,v_init_small_val=va_init_small_val)
			
			#return re
		#if the control is MP without taking into consideration the output que
		elif TYPE_CONTROL[va_type_control_to_employ]==TYPE_CONTROL[9]:
		
			re=Algorithm_MP_Control_sans_output_ques.admissible_intersection_control_object_next_period_mp_no_output_que(\
			v_intersection=va_network.get_di_intersections()[va_id_nd],v_network=va_network,\
			li_param_control=va_network.get_control_actuate_obj().get_li_param_control_MP_no_output_que(),\
			v_round_prec=va_round_precis,\
			v_t_round_prec=va_t_round_prec,\
			v_t_end_current_network_control_matrix=va_t_end_current_intersection_control,\
			v_t_unit=va_t_unit,v_dt=va_marge_dt,v_init_small_val=va_init_small_val)
			
			return re
			
		#if the control is  Fully Actuated with no red clearance
		elif TYPE_CONTROL[va_type_control_to_employ]==TYPE_CONTROL[10]:
		
			re=Algorith_FA_no_red_clear_Control.admissible_intersection_control_object_fa_no_rc(\
			t_actuel=val_t_current,\
			v_intersection=va_network.get_di_intersections()[va_id_nd],\
			v_network=va_network,\
			li_param_control=self._li_param_control_FA_ctrl,\
			v_sim_dur=va_sim_dur,\
			v_t_unit=va_t_unit,\
			v_t_round_prec=va_round_precis)
			
			
			
			
			
			return re
		#if the control is  Fully Actuated with Max Green 
		elif TYPE_CONTROL[va_type_control_to_employ]==TYPE_CONTROL[11]:
		
			re=Algorith_FA_Max_Green_Control.admissible_intersection_control_object_fa_max_green(\
			t_actuel=val_t_current,\
			v_intersection=va_network.get_di_intersections()[va_id_nd],\
			v_network=va_network,\
			li_param_control=self._li_param_control_FA_Max_Green_ctrl,\
			v_t_unit=va_t_unit,\
			v_round_prec=va_round_precis,\
			v_t_round_precision=va_t_round_prec,
			v_marge_dt=va_marge_dt,\
			v_init_small_val=va_init_small_val)
			
			
			
			return re
			
		#if the control is  Fully Actuated with red clear
		elif TYPE_CONTROL[va_type_control_to_employ]==TYPE_CONTROL[12]:
		
			re=Algorith_FA_with_red_clear_Control.admissible_intersection_control_object_fa_with_rc(\
			t_actuel=val_t_current,\
			v_intersection=va_network.get_di_intersections()[va_id_nd],\
			v_network=va_network,\
			li_param_control=self._li_param_control_FA_with_red_clear_ctrl,\
			v_sim_dur=va_sim_dur,\
			v_t_unit=va_t_unit,\
			v_t_round_prec=va_round_precis)
			
			return re
			
		#if the control is MP when consdering od matrices
		#elif va_type_control_to_employ==TYPE_CONTROL[12]:
		
			#re=Algorithm_MP_MOD_Control.admissible_intersection_control_object_next_period_mp_mod(\
			#v_intersection=va_network.get_di_intersections()[va_id_nd],v_network=va_network,\
			#li_param_control=va_network.get_control_actuate_obj().get_li_param_mp_ctrl(),\
			#v_round_prec=va_round_precis,\
			#v_t_round_prec=va_t_round_prec,\
			#v_t_end_current_network_control_matrix=va_t_end_current_intersection_control,\
			#v_t_unit=va_t_unit,v_init_small_val=va_init_small_val)
			
			#return re
			
		#if the type of control is MP Practical
		elif TYPE_CONTROL[va_type_control_to_employ]==TYPE_CONTROL[13]:
		
			re= Algorithm_MP_PRAC_Control.admissible_intersection_control_object_next_period_mp_pract(\
			t_actuel=val_t_current,\
			t_start_sim=va_t_start_sim,\
			v_sim_dur=va_sim_dur,\
			v_inters=va_network.get_di_intersections()[va_id_nd],\
			v_netwk=va_network,\
			v_li_param_control=self._li_param_control_MP_Practical_ctrl,\
			v_round_precis=va_round_precis,\
			v_t_round_precis=va_t_round_prec,\
			v_t_end_current_netwk_control_matrix=va_t_end_current_intersection_control,\
			v_ti_unit=va_t_unit,\
			val_dic_id_phase_val_qweight=self._di_addition_param_mp_pract_ctrl,\
			v_initial_small_val=va_init_small_val,\
			v_marge_dt=va_marge_dt)
			
			return re
			
		#if the type of the control is MP-No rd clear
		elif  TYPE_CONTROL[va_type_control_to_employ]==TYPE_CONTROL[14]:
			
			re=Algorithm_MP_Control_without_red_clear.admissible_intersection_control_object_next_period_mp_without_rc(\
			v_intersection=va_network.get_di_intersections()[va_id_nd],\
			v_network=va_network,\
			param_control=self._li_param_control_MP_without_red_clear,\
			v_round_prec=va_round_precis,v_t_round_prec=va_t_round_prec,\
			v_t_end_current_network_control_matrix=va_t_end_current_intersection_control,\
			v_t_unit=va_t_unit,v_dt=va_marge_dt,\
			val_di_id_phase_val_qweight=self._di_addition_param_mp_without_red_clear_ctrl,\
			v_init_small_val=va_init_small_val)
			
			return re
	
		#if the type of the control is MP-Pract without red clear
		elif  TYPE_CONTROL[va_type_control_to_employ]==TYPE_CONTROL[15]:
			re=Algorithm_MP_PRAC_Control_without_red_clear.admissible_intersection_control_object_next_period_mp_pract_without_red_clear(\
			t_actuel=val_t_current,\
			t_start_sim=va_t_start_sim,\
			v_sim_dur=va_sim_dur,\
			v_inters=va_network.get_di_intersections()[va_id_nd],\
			v_netwk=va_network,\
			v_li_param_control=self._li_param_control_MP_Pract_without_red_clear,\
			val_dict_id_phase_val_qweight=self._di_addition_param_mp_pract_without_red_clear_ctrl,\
			v_round_precis=va_round_precis,\
			v_t_round_precis=va_t_round_prec,\
			v_t_end_current_netwk_control_matrix=va_t_end_current_intersection_control,\
			v_ti_unit=va_t_unit,\
			v_initial_small_val=va_init_small_val,\
			v_marge_dt=va_marge_dt)
			
			return re


				

#*****************************************************************************************************************************************************************************************
