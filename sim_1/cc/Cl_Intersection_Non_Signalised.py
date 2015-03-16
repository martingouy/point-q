import Cl_Intersection
import List_Explicit_Values


class Intersection_Non_Signalised(Cl_Intersection.Intersection):

	def __init__(self,va_id_nd=-1,va_li_id_input_network_links_to_inters_node=[],va_li_id_output_network_links_from_inters_node=[],\
	val_current_dict_rout_prob={},val_current_dict_cum_rout_prob={},val_current_dict_cum_mod={},\
	val_estim_turn_ratios=None,\
	val_di_li_compatible_phases={},val_lis_param_estim_turn_ratios=[],\
	val_dict_estimat_rp={},val_dict_estimat_cum_rp={}):
	
		Cl_Intersection.Intersection.__init__(self,val_id_nd=va_id_nd,\
		val_li_id_input_network_links_to_inters_node=va_li_id_input_network_links_to_inters_node,\
		val_li_id_output_network_links_from_inters_node=va_li_id_output_network_links_from_inters_node,\
		val_current_di_rout_prob=val_current_dict_rout_prob,\
		val_current_di_cum_rout_prob=val_current_dict_cum_rout_prob,\
		val_current_di_cum_mod=val_current_dict_cum_mod,\
		val_estimated_turn_ratios=val_estim_turn_ratios,\
		val_type_intersection=Cl_Intersection.TYPE_INTERSECTION["non_signalised_intersection"],\
		val_li_param_estim_turn_ratios=val_lis_param_estim_turn_ratios,\
		val_di_estimat_rp=val_dict_estimat_rp,val_di_estimat_cum_rp=val_dict_estimat_cum_rp)
		
		
		#dict key=id list compatible phases, value= list compatible phases, NO RIGHT TURNS INCLUDED
		#the key is created by simple incrementation NO RIGHT TURNS INCLUDED
		#ex di={1:[ (1,2),(3,4)], 2: [(5,6),(7,8)]}
		self._di_li_compatible_phases=val_di_li_compatible_phases
		
		#RIGHT TURNS ARE NOT EMPLOYED IN A NSI
		
		#dict, key=id phase, value=list compatible phases, 
		self._di_key_id_phase_value_li_compatible_phases=self.fct_creat_di_key_id_phase_value_li_compatible_phases()
		
		#dict, key=id phase, value=list non compatible phases, 
		#the compatible phases of an intersection related to each phase of the intersection
		self._di_key_id_phase_value_li_non_compatible_phases=self.fct_creat_di_key_id_phase_value_li_non_compatible_phases()
		
		#dict, key=id phase, value list vehicles sorted by their end hold  time, 
		self._di_key_id_phase_value_heap_veh=self.fct_creat_di_key_id_phase_value_empty_list()
		
		#dict, key=id phase of veh crossing the intersection, value=[val_t_end_veh_dep,val_start_dep_crossing_veh, duree veh depart]. 
		#If no veh crosses, this dict will be empty and it wil be updated when a 
		#veh startsand finishes  its departure, 
		self._di_indicating_id_phase_cros_veh={}
		
#*****************************************************************************************************************************************************************************************

	#method  returning the dict key=id list compatible stages, value= list compatible stages
	def get_di_li_compatible_phases(self):
		return self._di_li_compatible_phases
#*****************************************************************************************************************************************************************************************
	#method  returning the dict, key=id phase, value=list compatible phases
	def get_di_key_id_phase_value_li_compatible_phases(self):
		return self._di_key_id_phase_value_li_compatible_phases
#*****************************************************************************************************************************************************************************************
	#method returning  the dict, key=id phase, value=list non compatible phases
	def get_di_key_id_phase_value_li_non_compatible_phases(self):
		return self._di_key_id_phase_value_li_non_compatible_phases
#*****************************************************************************************************************************************************************************************
	#method returning the dict, key=id phase, value list of vehicles sorted by their end hold time
	def get_di_key_id_phase_value_heap_veh(self):
		return self._di_key_id_phase_value_heap_veh
#*****************************************************************************************************************************************************************************************
	#method  returning the dict, key=id phase of veh crossing the intersection, value=[val_t_end_veh_dep,val_start_dep_crossing_veh, duree veh depart]
	def get_di_indicating_id_phase_cros_veh(self):
		return self._di_indicating_id_phase_cros_veh
#*****************************************************************************************************************************************************************************************
	#method  modifying the dict key=id list compatible stages, value= list compatible stages
	def set_di_li_compatible_phases(self,n_v):
		self._di_li_compatible_phases=n_v
#*****************************************************************************************************************************************************************************************
	#method  modifying the dict, key=id phase, value=list compatible phases
	def set_di_key_id_phase_value_li_compatible_phases(self,n_v):
		self._di_key_id_phase_value_li_compatible_phases=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying  the dict, key=id phase, value=list non compatible phases
	def set_di_key_id_phase_value_li_non_compatible_phases(self,n_v):
		self._di_key_id_phase_value_li_non_compatible_phases=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the dict, key=id phase, value list of vehicles sorted by their end hold time
	def set_di_key_id_phase_value_heap_veh(self,n_v):
		self._di_key_id_phase_value_heap_veh=n_v
#*****************************************************************************************************************************************************************************************
	#method  modifying the dict, key=id phase of veh crossing the intersection, value=[val_t_end_veh_dep,val_start_dep_crossing_veh, duree veh depart]
	def set_di_indicating_id_phase_cros_veh(self,n_v):
		self._di_indicating_id_phase_cros_veh=n_v
#*****************************************************************************************************************************************************************************************
	#fct creation dict key=id phase, value=list compatible phases
	def fct_creat_di_key_id_phase_value_li_compatible_phases(self):
		di_rep={}
		
		di={}
		#ex di={1:[ (1,2),(3,4)], 2: [(5,6),(7,8)]}
		#print("self._di_li_compatible_phases",self._di_li_compatible_phases)
		for i in self._di_li_compatible_phases:
			#print("i=",i)
			for j in self._di_li_compatible_phases[i]:
				#print("j=",j,j[0],self._di_li_compatible_phases[i])
				di[j[0],j[1]]=list(self._di_li_compatible_phases[i])
				#print("di",di)
				di[j[0],j[1]].remove([j[0],j[1]])
				#print(di)
				di_rep.update(di)
		#print("di_rep",di_rep)
		return di_rep
		
#*****************************************************************************************************************************************************************************************
	#fct creation dict key=id phase, value=list non compatible phases
	def fct_creat_di_key_id_phase_value_li_non_compatible_phases(self):
	
		di_rep={}
		
		di={}
		#list_keys=[1,2]
		list_keys=list(self._di_li_compatible_phases.keys())
		
		#ex di={1:[ (1,2),(3,4)], 2: [(5,6),(7,8)]} (1,2) compatible avec (3,4), (5,6) compatible avec (7,8)
		
		li_keys=list(list_keys)
		#nb_keys=len(li_keys)
		#for each key
		li_keys_2=list(li_keys)
		for i in li_keys:
			li_keys_2.remove(i)
			for p in li_keys_2:
				#j=[1,2]
				for j in self._di_li_compatible_phases[i]:
					#print("j=",j,j[0],j[1])
					if (j[0],j[1]) not in di:
						di[j[0],j[1]]=self._di_li_compatible_phases[p]
						di_rep.update(di)
					else:
						di[j[0],j[1]].append(self._di_li_compatible_phases[p])
						di_rep.update(di)
			li_keys_2.append(i)
		#print(di)
		#print(di_rep)
		#import sys
		#sys.exit()
			
		
		#for i in self._di_li_compatible_phases:
			#print("i",i)
			#li_keys=list(list_keys)
			#print("li_keys avant",li_keys)
			#li_keys.remove(i)
			#print("li_keys apres",li_keys)
			#for j in self._di_li_compatible_phases[i]:
				#print("j=",j)
				#di[j]=[]
				#for m in li_keys():
					#di[j].extend(self._di_li_compatible_phases[m])
				#di_rep.update(di)
		#return di_rep
		

#*****************************************************************************************************************************************************************************************
	#fct creation dict, key=id phase, value=[] dans cette liste on mettra les veh tries par leur t arrivee
	def fct_creat_di_key_id_phase_value_empty_list(self):
		di_rep={}
		for i in self._di_li_compatible_phases:
			for j in self._di_li_compatible_phases[i]:
				di_rep[j[0],j[1]]=[]
		return di_rep

#*****************************************************************************************************************************************************************************************
	#method examining if at least one vehicle crosses the intersection and in this case it compared the type of the phase with the given one 
	#compatible or not 
	#it returns 1 if at leaste one  vehicle from a non compatible movements crosses, 0 if a vehicle from comp mv crosses, -1 if none cross
	#id_phase=[id input lk, id output lk]
	def fct_exam_whether_veh_cross_inters_and_related_type_phase(id_phase):
	
		#self._di_indicating_id_phase_cros_veh= dict, key=id phase from which a veh crosses, 
		
		#if a veh crosses the intersection
		if self._di_indicating_id_phase_cros_veh !={}:
		
			for j in self._di_indicating_id_phase_cros_veh:
				#if the phase related to the veh which is about to cross the intersection is not compatible with the given phase
				if j in self._di_key_id_phase_value_li_non_compatible_phases[id_phase[0],id_phase[1]]:
				
					return List_Explicit_Values.initialisation_value_to_one
				
				#if the phase related to the veh which is about to cross is  compatible with the given phase
				else:
					return List_Explicit_Values.initialisation_value_to_zero
		
		#if no veh crosses the intersection
		else:
			return List_Explicit_Values.initialisation_value_to_minus_one
		
		
		
		
		

#*****************************************************************************************************************************************************************************************

	
	





















