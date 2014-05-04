import string
import heapq
from heapq import *
import Cl_Event
import Cl_Simulation_System
import Cl_Creation_Network
import Cl_Vehicle
import Cl_Network
import Cl_Network_Entry_Link
import Cl_Ev_veh_appearance
import Cl_Ev_veh_appearance_nsi
import Cl_Ev_end_decision_next_intersection_control
import Cl_Intersection
import Cl_Ev_veh_flow_changes
import Cl_Decisions
import List_Explicit_Values
import pickle



#import Creation_parameters_event_treatment_event_list

class Simulation:

	def __init__(self,val_simul_system=None,val_t_start_simulation=-1,val_t_duration_simulation=-1,\
	val_t_current=-1,val_dict_parameters_fcts_event_treat={},val_number_event_types=-1,\
	val_heap_even=[],val_new_veh_id=0,val_index_veh_id_in_veh_ap_event=List_Explicit_Values.initialisation_value_to_zero):
	
		#the system to be simulated
		self._simul_system=val_simul_system
	
		#the time at which the simulation starts
		self._t_start_simulation=val_t_start_simulation
	
		#the duration of the simulation
		self._t_duration_simulation=val_t_duration_simulation
	
		#the current simulation time
		self._t_current=val_t_current
	
		# the dictionary with the parameters for the event treatment
		self._dict_parameters_fcts_event_treat=val_dict_parameters_fcts_event_treat
	
		#the number indicating the different types of event
		self._number_event_types=val_number_event_types
	
		#the event set
		self._heap_even=val_heap_even
	
		#the new vehicle id
		self._new_veh_id=val_new_veh_id
		
		#the position of the argument identifying the vehicle id in args list of the function treating the vehicle appearance event
		self._index_veh_id_in_veh_ap_event=val_index_veh_id_in_veh_ap_event
	
#*****************************************************************************************************************************************************************************************
	#method returning the system to be simulated
	def get_simul_system(self):
		return self._simul_system

#*****************************************************************************************************************************************************************************************
	#method returning the time at which the simulation starts
	def get_t_start_simulation(self):
		return self._t_start_simulation
#*****************************************************************************************************************************************************************************************
	#method returning the duration of the simulation
	def get_t_duration_simulation(self):
		return self._t_duration_simulation
	
#*****************************************************************************************************************************************************************************************
	#method returning the current simulation time
	def get_t_current(self):
		return self._t_current
#*****************************************************************************************************************************************************************************************
	#method returning the dictionary with the parameters for the event treatment
	def get_dict_parameters_fcts_event_treat(self):
		return self._dict_parameters_fcts_event_treat
#*****************************************************************************************************************************************************************************************
	#method returning the number indicating the different types of event
	def get_number_event_types(self):
		return self._number_event_types
	
#*****************************************************************************************************************************************************************************************
	#method returning the event set
	def get_heap_even(self):
		return self._heap_even
#*****************************************************************************************************************************************************************************************
	#method returning the new vehicle id
	def get_new_veh_id(self):
		return self._new_veh_id

#*****************************************************************************************************************************************************************************************
	#method returning the position of the argument identifying the vehicle id in args list of the function treating the vehicle appearance event
	def get_index_veh_id_in_veh_ap_event(self):
		return self._index_veh_id_in_veh_ap_event

#*****************************************************************************************************************************************************************************************
	#method modifying the system to be simulated
	def set_simul_system(self,n_v):
		self._simul_system=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the time at which the simulation starts
	def set_t_start_simulation(self,n_v):
		self._t_start_simulation=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the duration of the simulation
	def set_t_duration_simulation(self,n_v):
		self._t_duration_simulation=n_v
	
#*****************************************************************************************************************************************************************************************
	#method modifying the current simulation time
	def set_t_current(self,n_v):
		self._t_current=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the dictionary with the parameters for the event treatment
	def set_dict_parameters_fcts_event_treat(self,n_v):
		self._dict_parameters_fcts_event_treat=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the number indicating the different types of event
	def set_number_event_types(self,n_v):
		self._number_event_types=n_v
	
#*****************************************************************************************************************************************************************************************
	#method modifying the event set
	def set_heap_even(self,n_v):
		self._heap_even=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the new created vehicle id
	def set_new_veh_id(self,n_v):
		self._new_veh_id=n_v

#*****************************************************************************************************************************************************************************************

	#method modifying the position of the argument identifying the vehicle id in args list of the function treating the vehicle appearance event
	def set_index_veh_id_in_veh_ap_event(self,n_v):
		self._index_veh_id_in_veh_ap_event=n_v

#*****************************************************************************************************************************************************************************************
	

	#method initialising the event list with the vehicle appearance events when starting a new simulation
	#val_t_start_veh_appearance=indicates after how much time from the beginining of the simulation,
	#we will calculate the tie at which vehicles will start to appear
	
	#val_dict_veh_inform_previous_sim= a dict, key=veh id, value=[ t_appear, [id_entry_link, id_destination_link_1, id_destination_link_2,.... ] ]
	
	#val_dict_entry_link_info_previous_sim= dict, key=id_entry_link, 
	#value=[ [..., [t_appearance_veh, veh_id, [id_current_link_location_1,id_destination_link_1,...]     ]  ]  
	
	#val_dict_entry_link_info_given_data dict key =id entry-internal link, value= [...,t_veh_appear,...]
	#this dict contains given data
	
	def initialisation_event_list_veh_appearance_events(self,val_veh_prev_demand_have_dynam_constructed_final_dest,\
	val_creat_new_veh_demand=None,val_t_start_calcul_veh_appearance=-1,\
	val_dict_veh_inform_previous_sim={},val_dict_entry_link_info_previous_sim={},val_dict_entry_link_info_given_data={},\
	val_t_round_precis=1):
	
		#if new demand will be created
		if val_creat_new_veh_demand==1:
		
			#for each entry link we calculate the demand (time veh appearance)
			for i in self._simul_system.get_network().get_di_entry_links_to_network():
			
				#print(self._simul_system.get_network().get_di_entry_links_to_network()[i].get_lis_parameters_fct_creating_demand_entry_link())
				#if the demand parameter is >0:
				if self._simul_system.get_network().get_di_entry_links_to_network()[i].get_lis_parameters_fct_creating_demand_entry_link()[0]>0:
					#li_veh=[]
					#the time duration after which a new vehicle will be appeared at the entry link i 
					t_veh_ap=round(val_t_start_calcul_veh_appearance+\
					self._simul_system.get_network().get_di_entry_links_to_network()[i].get_fct_creating_demand_entry_link()(\
					*self._simul_system.get_network().get_di_entry_links_to_network()[i].get_lis_parameters_fct_creating_demand_entry_link()),\
					val_t_round_precis)
				
					#creation of the associated vehicle (no id yet)
				
					veh=Cl_Vehicle.Vehicle(val_t_veh_appearance_at_network=t_veh_ap,val_id_entry_link_veh_ap=i)
				
					
					#creation of the vehicle appearance event
				
					#if the entry link is related to a signalised intersection
					if self._simul_system.get_network().get_di_intersections()[\
					self._simul_system.get_network().get_di_entry_links_to_network()[i].get_id_head_intersection_node()].\
					get_type_intersection()==Cl_Intersection.TYPE_INTERSECTION["signalised_intersection"]:
				
				
						ev_veh_ap=Cl_Ev_veh_appearance.Ev_veh_appearance(val_event_t=t_veh_ap,val_vehicle=veh)
					
					
					
						#insertion of the event in the event list 
						heappush(self._heap_even,ev_veh_ap)
				
					#if the entry link is related to a non-signalised intersection
					else:
						ev_veh_ap_nsi=Cl_Ev_veh_appearance_nsi.Ev_veh_appearance_nsi(val_event_t=t_veh_ap,val_vehicle=veh)
					
						#insertion of the event in the event list 
						heappush(self._heap_even,ev_veh_ap_nsi)
				
		
		#if previous veh demand will be employed
		elif val_creat_new_veh_demand==0:
		
			
			
			#for each entry link we calculate the demand
			for i in self._simul_system.get_network().get_di_entry_links_to_network():
			
				#if the demand parameter is >0:
				if self._simul_system.get_network().get_di_entry_links_to_network()[i].get_lis_parameters_fct_creating_demand_entry_link()[0]>0:
			
				
					#the time duration after which a new vehicle will be appeared at the entry link i 
								
					#if the veh final destination will dynamically be costructed
					if val_veh_prev_demand_have_dynam_constructed_final_dest==1:
				
						#val_dict_entry_link_info_previous_sim = dict, key=id entry link
						#value = [ [t_appearance,veh_id]  ]  

						#print("HERE",val_dict_entry_link_info_previous_sim.keys(),i)
						t_veh_ap=val_dict_entry_link_info_previous_sim[i][0][0]
				
						#creation of the associated vehicle (no id yet)
						#the entry link is the 1st element of the 3rd element of the diction
						veh=Cl_Vehicle.Vehicle(val_t_veh_appearance_at_network=t_veh_ap,val_id_entry_link_veh_ap=i)
					
						#creation of the vehicle appearance event
						#if the entry link is related to a signalised intersection
						if self._simul_system.get_network().get_di_intersections()[\
						self._simul_system.get_network().get_di_entry_links_to_network()[i].get_id_head_intersection_node()].\
						get_type_intersection()==Cl_Intersection.TYPE_INTERSECTION["signalised_intersection"]:
				
							ev_veh_ap=Cl_Ev_veh_appearance.Ev_veh_appearance(val_event_t=t_veh_ap,val_vehicle=veh,\
							val_current_veh_id_demand_previous_sim=val_dict_entry_link_info_previous_sim[i][0][1])
					
							#insertion of the event in the event list 
							heappush(self._heap_even,ev_veh_ap)
			
						#if the entry link is related to a non-signalises intersection
						else:
							ev_veh_ap_nsi=Cl_Ev_veh_appearance.Ev_veh_appearance_nsi(val_event_t=t_veh_ap,val_vehicle=veh,\
							val_current_veh_id_demand_previous_sim=val_dict_entry_link_info_previous_sim[i][0][1])
					
							#insertion of the event in the event list 
							heappush(self._heap_even,ev_veh_ap_nsi)
					#if the veh final destination will  be defined by the veh appearance
					else:
				
						#val_dict_entry_link_info_previous_sim = dict, key=id entry link
						#value = [..., [t_appearance,veh_id],...]  
					
						t_veh_ap=val_dict_entry_link_info_previous_sim[i][0][0]
					
						#creation of the associated vehicle (no id yet)
						veh=Cl_Vehicle.Vehicle(val_t_veh_appearance_at_network=t_veh_ap,val_id_entry_link_veh_ap=i)
				
						#creation of the vehicle appearance event
						#if the entry link is related to a signalised intersection
						if self._simul_system.get_network().get_di_intersections()[\
						self._simul_system.get_network().get_di_entry_links_to_network()[i].get_id_head_intersection_node()].\
						get_type_intersection()==Cl_Intersection.TYPE_INTERSECTION["signalised_intersection"]:
				
							ev_veh_ap=Cl_Ev_veh_appearance.Ev_veh_appearance(val_event_t=t_veh_ap,val_vehicle=veh,\
							val_current_veh_id_demand_previous_sim=val_dict_entry_link_info_previous_sim[i][0][1])
					
							#insertion of the event in the event list 
							heappush(self._heap_even,ev_veh_ap)
			
						#if the entry link is related to a non-signalises intersection
						else:
							ev_veh_ap_nsi=Cl_Ev_veh_appearance.Ev_veh_appearance_nsi(val_event_t=t_veh_ap,val_vehicle=veh,\
							val_current_veh_id_demand_previous_sim=val_dict_entry_link_info_previous_sim[i][1])
					
							#insertion of the event in the event list 
							heappush(self._heap_even,ev_veh_ap_nsi)
					
				
					#print("DI AVANT",val_dict_entry_link_info_previous_sim[i][0],val_dict_entry_link_info_previous_sim[i][1])
				
					#we delete the first element of the list corrresponding to the associated entry link
					val_dict_entry_link_info_previous_sim[i].remove(val_dict_entry_link_info_previous_sim[i][0])
				
					#print("DI APRES",val_dict_entry_link_info_previous_sim[i][0],val_dict_entry_link_info_previous_sim[i][1])
					#import sys
					#sys.exit()
		#if a given  veh demand will be employed
		elif val_creat_new_veh_demand==-1:
		
			#for each entry link we calculate the veh appearance
			for i in self._simul_system.get_network().get_di_entry_links_to_network():
			
				#val_dict_entry_link_info_given_sim=dict, key=id entry-internal link, value=[...,t veh appear,...]
				t_veh_ap=val_dict_entry_link_info_given_data[i][0]
				
				#we delete the first element of the list corresponfing to the associated list
				val_dict_entry_link_info_given_data[i].remove(val_dict_entry_link_info_given_data[i][0])
				
				#creation of the associated vehicle (no id yet)
				veh=Cl_Vehicle.Vehicle(val_t_veh_appearance_at_network=t_veh_ap,val_id_entry_link_veh_ap=i)
				
				if  self._simul_system.get_network().get_di_intersections()[\
				self._simul_system.get_network().get_di_entry_links_to_network()[i].get_id_head_intersection_node()].\
				get_type_intersection()==Cl_Intersection.TYPE_INTERSECTION["signalised_intersection"]:
					#creation of the vehicle appearance event
					ev_veh_ap=Cl_Ev_veh_appearance.Ev_veh_appearance(val_event_t=t_veh_ap,val_vehicle=veh)
					#,\
					#val_current_veh_id_demand_previous_sim= )
				
					#insertion of the event in the event list 
					heappush(self._heap_even,ev_veh_ap)
				else:
					#creation of the vehicle appearance event
					ev_veh_ap_nsi=Cl_Ev_veh_appearance_nsi.Ev_veh_appearance_nsi(val_event_t=t_veh_ap,val_vehicle=veh)
					#,\
					#val_current_veh_id_demand_previous_sim= )
				
					#insertion of the event in the event list 
					heappush(self._heap_even,ev_veh_ap)
					
		
		#if none of the previous demands is considered there is a problem
		else:
			print("PROBLEM IN CL_SIMULATION, val_creat_new_veh_demand=",val_creat_new_veh_demand)
			import sys
			sys.exit()
			
				
#*****************************************************************************************************************************************************************************************
	#method initialising the event list by creating the network control event
	def initialisation_event_list_end_decision_intersection_control_events(self):
	
		#creation of the event end decision network control
		#t_end_current_cycle=-1
		#t_end_current_cycle=0
		
		
		
		#for each nsi intersection we create an event Ev_end_decision_next_intersection_control
		for i in self._simul_system.get_network().get_di_intersections():
			if self._simul_system.get_network().get_di_intersections()[i].get_type_intersection()==\
			Cl_Intersection.TYPE_INTERSECTION["signalised_intersection"]:
			
				ev=Cl_Ev_end_decision_next_intersection_control.\
				Ev_end_decision_next_intersection_control(val_ev_time=self._t_start_simulation,\
				val_id_intersection_node=i,\
				val_t_end_last_intersection_control_matrix=self._t_start_simulation,\
				val_type_control_to_employ=self._simul_system.get_network().get_di_intersections()[i].get_ctrl_actuate_obj().
				get_type_employed_ctrl(),\
				val_indicat_whether_estim_turn_ratio_values=self._simul_system.get_network().get_di_intersections()[i].get_estimated_turn_ratios())
				#insertion of the event in the event list 
				heappush(self._heap_even,ev)
#*****************************************************************************************************************************************************************************************
	#method creat the events related tit ge estim of the turn ratios of a single intersection
	
	def initialisation_ev_list_veh_flow_changes_split_ratio_est_single_intersection(self,id_inter_nd,t_start_sim,\
	period_estim,t_unit,v_round_prec=1):
	
		
		t=round(t_start_sim+period_estim+t_unit,v_round_prec)
		
		ev=Cl_Ev_veh_flow_changes.Ev_veh_flow_changes(val_ev_t=t,\
		val_id_intersection_node=id_inter_nd,val_reason_event=Cl_Ev_veh_flow_changes.TYPE_REASON_EVENT_HEV_FLOW_CHANGES["turn_ratios_estim"])
			
		heappush(self._heap_even,ev)
			
		
#*****************************************************************************************************************************************************************************************
	#method adding in the event list the events  corresponding to  the flow changes when estim turn ratios, for all intersections
	def initialisation_event_list_sim_veh_flow_changes_events_network(self,t_un,val_round_prec):
	
		#for each intersection node for which turn ratios are going to be estimated
		for i in self._simul_system.get_network().get_di_id_intersections_with_estim_turn_ratios():
		
			#print(i,self._simul_system.get_network().get_di_intersections()[i].get_li_param_estim_turn_ratios())
			
			self.initialisation_ev_list_veh_flow_changes_split_ratio_est_single_intersection(\
			id_inter_nd=i,t_start_sim=self._t_start_simulation,\
			period_estim=self._simul_system.get_network().get_di_intersections()[i].get_li_param_estim_turn_ratios()[1],\
			t_unit=t_un,v_round_prec=val_round_prec)
			
			

#*****************************************************************************************************************************************************************************************
	#method	adding in the event list the events corresponding to the rout prob variation
	def initialisation_ev_list_veh_flow_changes_turn_ratios_single_intersection(self, id_inters,t_modif_tr,t_unit,\
	val_dic_rp_mat_next_period,val_dic_mat_cum_rp_next_period,v_round_prec=1):
	
		#t=round(t_start+duration_previous_turn_ratios_val+t_unit,v_round_prec)
		
		ev=Cl_Ev_veh_flow_changes.Ev_veh_flow_changes(val_ev_t=t_modif_tr,\
		val_id_intersection_node=id_inters,val_di_rp_mat_next_period=val_dic_rp_mat_next_period,\
		val_di_mat_cum_rp_next_period=val_dic_mat_cum_rp_next_period,\
		val_reason_event=Cl_Ev_veh_flow_changes.TYPE_REASON_EVENT_HEV_FLOW_CHANGES["modification_turn_ratios"])
		
		heappush(self._heap_even,ev)

#*****************************************************************************************************************************************************************************************
	#method adding in the event list the events  corresponding to  the flow changes when varying turn ratios, for all intersections
	def initialisation_event_list_sim_veh_flow_changes_var_tr_events_network(self,t_start_sim,t_un,v_round_precis=1):
	
		#for each intersection node for which turn ratios are going vary
		for i in self._simul_system.get_network().get_di_intersections_with_var_turn_ratios():
		
			#for ech period with varying rp related to this intersection
			li_sorted_periods=list(self._simul_system.get_network().get_di_inters_periods_with_var_turn_ratios()[i].keys())
			li_sorted_periods.sort()
		
			t_init=round(t_start_sim+t_un,v_round_precis)
			for j in li_sorted_periods:
				
				t=round(t_init+self._simul_system.get_network().get_di_inters_periods_with_var_turn_ratios()[i][j],v_round_precis)
				
				self.initialisation_ev_list_veh_flow_changes_turn_ratios_single_intersection(\
				id_inters=i,t_modif_tr=t,t_unit=t_un,\
				val_dic_rp_mat_next_period=self._simul_system.get_network().get_di_intersections_with_var_turn_ratios()[i][j],\
				val_dic_mat_cum_rp_next_period=self._simul_system.get_network().get_di_intersections_with_var_cum_turn_ratios()[i][j],
				v_round_prec=v_round_precis)
				
				t_init=t
#*****************************************************************************************************************************************************************************************
	#method initialising the initial state of single queue at the beginning of a new simulation
	#IT MAKES SENS ONLY FOR A NEW DEMAND
	#li_veh_final_dest_id=[-1] or [,...>0,...]
	def initialisation_single_que_state_new_sim(self, val_id_que,val_nb_veh,li_veh_final_dest_id,t_start_sim):
	
		#creation of the appropriate nb of veh
		for i in range(val_nb_veh):	
		
			self._new_veh_id+=List_Explicit_Values.initialisation_value_to_one
			
			
		
			
			#creation of the veh
			#if the veh final dest and consequently the next will be defined according to turn ratios
			if li_veh_final_dest_id[0]==-1:
			
				
				
			
				vehicle=Cl_Vehicle.Vehicle(val_id_veh=self._new_veh_id,val_t_veh_appearance_at_network=t_start_sim,\
				val_current_id_link_veh_location=val_id_que[0],val_t_vehicle_arrival_at_current_link=t_start_sim,\
				val_veh_current_queue_location=val_id_que,val_t_vehicle_arrival_at_current_queue=t_start_sim,\
				val_vehicle_id_destination_link=val_id_que[1],\
				val_type_vehicle_final_destination=Cl_Vehicle.TYPE_VEH_FINAL_DESTINATION["dynam_constructed_final_dest"],\
				val_t_end_veh_hold_time_que=t_start_sim,\
				val_id_veh_final_destination_link=-1,val_veh_added_when_que_update=1)
			else:
				
				vehicle=Cl_Vehicle.Vehicle(val_id_veh=self._new_veh_id,val_t_veh_appearance_at_network=t_start_sim,\
				val_current_id_link_veh_location=val_id_que[0],val_t_vehicle_arrival_at_current_link=t_start_sim,\
				val_veh_current_queue_location=val_id_que,val_t_vehicle_arrival_at_current_queue=t_start_sim,\
				val_vehicle_id_destination_link=val_id_que[1],\
				val_type_vehicle_final_destination=Cl_Vehicle.TYPE_VEH_FINAL_DESTINATION["initially_defined_final_dest"],\
				val_t_end_veh_hold_time_que=t_start_sim,\
				val_id_veh_final_destination_link=li_veh_final_dest_id[i],val_veh_added_when_que_update=1)
			
			#we update the queue
		
			self._simul_system.get_network().get_di_all_links()[val_id_que[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
			[val_id_que[0],val_id_que[1]].\
			fct_update_veh_queue_when_veh_prohibited_to_leave_no_mod(vehicle)
						
		
				
		#if finite link capacities (and veh current link different from entry, exit)  we update the link
		if self._simul_system.get_network().get_di_all_links()[val_id_que[0]].get_capacity_link()>0:
			
			self._simul_system.get_network()[val_id_que[1]].set_current_nb_veh_link(\
			self._simul_system.get_network().get_di_all_links()[val_nb_veh])
				
#*****************************************************************************************************************************************************************************************
	#method initialising the initial state of single queue at the beginning of a previously continued simulation
	#IT MAKES SENS ONLY FOR A NEW DEMAND
	#li_veh_final_dest_id=[-1] or [,...>0,...]
	def initialisation_single_que_state_previous_sim(self, val_id_que,val_nb_veh,li_veh_final_dest_id,t_start_sim):
	
		
			
		nb_veh_q=len(self._simul_system.get_network().get_di_all_links()[val_id_que[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[val_id_que[0],val_id_que[1]].get_queue_veh())
			
		#if the number of vehicles is >  desired nb of vehicles
		if nb_veh_q>val_nb_veh:
			
			self._simul_system.get_network().get_di_all_links()[val_id_que[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
			[val_id_que[0],val_id_que[1]].set_queue_veh(self._simul_system.get_network().get_di_all_links()\
			[val_id_que[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
			[val_id_que[0],val_id_que[1]].get_queue_veh()[:val_nb_veh])
				
				
			#if finite link capacities (and veh current link different from entry, exit)  we update the link
			if self._simul_system.get_network().get_di_all_links()[val_id_que[0]].get_capacity_link()>0:
			
				self._simul_system.get_network()[val_id_que[1]].set_current_nb_veh_link(val_nb_veh)
			
		#if the number of vehicles is <  desired nb of vehicles
		elif  nb_veh_q<val_nb_veh:
		
			nb_veh_a=int(val_nb_veh-nb_veh_q)
			
			for i in range(nb_veh_a):
	
				self._new_veh_id+=List_Explicit_Values.initialisation_value_to_one
		
				#creation of the veh
				#if the veh final dest and consequently the next will be defined according to turn ratios
				if li_veh_final_dest_id[0]==-1:
			
					vehicle=Cl_Vehicle.Vehicle(val_id_veh=self._new_veh_id,val_t_veh_appearance_at_network=t_start_sim,\
					val_current_id_link_veh_location=val_id_que[0],val_t_vehicle_arrival_at_current_link=t_start_sim,\
					val_veh_current_queue_location=val_id_que,val_t_vehicle_arrival_at_current_queue=t_start_sim,\
					val_vehicle_id_destination_link=val_id_que[1],\
					val_type_vehicle_final_destination=Cl_Vehicle.TYPE_VEH_FINAL_DESTINATION["dynam_constructed_final_dest"],\
					val_t_end_veh_hold_time_que=t_start_sim,\
					val_id_veh_final_destination_link=-1,val_veh_added_when_que_update=1)
				else:
				
					vehicle=Cl_Vehicle.Vehicle(val_id_veh=self._new_veh_id,val_t_veh_appearance_at_network=t_start_sim,\
					val_current_id_link_veh_location=val_id_que[0],val_t_vehicle_arrival_at_current_link=t_start_sim,\
					val_veh_current_queue_location=val_id_que,val_t_vehicle_arrival_at_current_queue=t_start_sim,\
					val_vehicle_id_destination_link=val_id_que[1],\
					val_type_vehicle_final_destination=Cl_Vehicle.TYPE_VEH_FINAL_DESTINATION["initially_defined_final_dest"],\
					val_t_end_veh_hold_time_que=t_start_sim,\
					val_id_veh_final_destination_link=li_veh_final_dest_id[i],val_veh_added_when_que_update=1)
			
				#we update the queue
		
				self._simul_system.get_network().get_di_all_links()[val_id_que[0]].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
				[val_id_que[0],val_id_que[1]].\
				fct_update_veh_queue_when_veh_prohibited_to_leave_no_mod(vehicle)
						
			#if finite link capacities (and veh current link different from entry, exit)  we update the link
			if self._simul_system.get_network().get_di_all_links()[val_id_que[0]].get_capacity_link()>0:
			
				self._simul_system.get_network()[val_id_que[1]].set_current_nb_veh_link(\
				self._simul_system.get_network()[val_id_que[1]].get_current_nb_veh_link()+val_nb_veh)
				
#*****************************************************************************************************************************************************************************************
	#method initialising the initial state of the queues at the beginning of a new simulation
	#di_que_state_info= dict, key=node id, value=dict, key=id phase, value=[nb veh, [...,id dest  lk,...] ]
	def initialisation_que_state_new_sim(self, di_que_state_info,ti_start_sim):
	
		#for each node
		for i in di_que_state_info:
			#for each phase
			for j in di_que_state_info[i]:
			
				self.initialisation_single_que_state_new_sim(val_id_que=[j[0],j[1]],val_nb_veh=di_que_state_info[i][j][0],\
				li_veh_final_dest_id=di_que_state_info[i][j][1],\
				t_start_sim=ti_start_sim)
				

#*****************************************************************************************************************************************************************************************
	#method initialising the initial state of the queues when continue a previous simulation
	#di_que_state_info= dict, key=node id, value=dict, key=id phase, value=[nb veh, [...,id dest  lk,...] ]
	def initialisation_que_state_prev_sim(self, di_que_state_info,ti_start_sim):
	
		#for each node
		for i in di_que_state_info:
			#for each phase
			for j in di_que_state_info[i]:
			
				self.initialisation_single_que_state_previous_sim(val_id_que=[j[0],j[1]],val_nb_veh=di_que_state_info[i][j][0],\
				li_veh_final_dest_id=di_que_state_info[i][j][1],t_start_sim=ti_start_sim)
			

#*****************************************************************************************************************************************************************************************
	
	#method initialising the event list
	def initialisation_event_list_sim(self,\
	val_veh_prev_demand_have_dynam_constr_final_dest,\
	val_t_round_precision,val_creat_new_vehicle_demand=-1,\
	val_t_start_calcul_vehicle_appearance=-1,\
	val_dict_vehicle_inform_previous_sim={},val_dict_entry_link_inform_previous_sim={},\
	val_dict_entry_link_inform_given_data={},\
	v_t_start_sim=None,v_t_unit=None):
	
		""" method initialising the event heap"""
		
		
		#initialising the event list with the network control event
		self.initialisation_event_list_end_decision_intersection_control_events()
		#,\
		#val_type_first_control_when_mixed_policy=val_type_first_cont_when_mixed_policy)
		
		#initialisation of the list with the veh appearance events
		self.initialisation_event_list_veh_appearance_events(\
		val_veh_prev_demand_have_dynam_constructed_final_dest=val_veh_prev_demand_have_dynam_constr_final_dest,\
		val_creat_new_veh_demand=val_creat_new_vehicle_demand,\
		val_t_start_calcul_veh_appearance=val_t_start_calcul_vehicle_appearance,\
		val_dict_veh_inform_previous_sim=val_dict_vehicle_inform_previous_sim,\
		val_dict_entry_link_info_previous_sim=val_dict_entry_link_inform_previous_sim,\
		val_dict_entry_link_info_given_data=val_dict_entry_link_inform_given_data,\
		val_t_round_precis=val_t_round_precision)
		
		
		#if the ques initial state is not empty 
		if self._simul_system.get_network().get_di_intersections_with_non_empty_init_que_state() !={}:
		
			self.initialisation_que_state_new_sim(di_que_state_info=self._simul_system.get_network().get_di_intersections_with_non_empty_init_que_state(),\
			ti_start_sim=v_t_start_sim)
		
		
		
		
		#print(self._simul_system.get_network().get_li_id_intersections_with_estim_turn_ratios())
		#import sys
		#sys.exit()
		#inti with the event for estim turn ratios if they vary
		if  self._simul_system.get_network().get_di_id_intersections_with_estim_turn_ratios() !={}:
		
			self.initialisation_event_list_sim_veh_flow_changes_events_network(t_un=v_t_unit,val_round_prec=val_t_round_precision)
		
		#if varying rp mat are considered
		#if v_varying_mat_rp==List_Explicit_Values.initialisation_value_to_one:
			#self.initialisation_event_list_sim_veh_flow_changes_events_network(\
			#t_start_sim=v_t_start_sim,t_un=v_t_unit)
			
		#if varying turn ratios
		
		if self._simul_system.get_network().get_di_intersections_with_var_turn_ratios()!={}:
		
			self.initialisation_event_list_sim_veh_flow_changes_var_tr_events_network(t_start_sim=v_t_start_sim,t_un=v_t_unit,v_round_precis=1)
			
		

#*****************************************************************************************************************************************************************************************
	#method doing a new simulation
	def simulation_1(self,\
	val_veh_previous_demand_have_dynam_constr_final_dest=None,\
	val_creation_new_vehicle_demand=List_Explicit_Values.initialisation_value_to_minus_one,\
	val_di_veh_inform_previous_sim={},val_di_entry_link_info_previous_sim={},val_di_entry_link_info_given_data={},\
	val_file_record_netw_obj_sim=None,val_file_record_pile_event_obj_sim=None,\
	val_file_record_next_veh_id=None,\
	val_print_messages_on_terminal=List_Explicit_Values.initialisation_value_to_minus_one,\
	val_t_start_calcul_veh_appearance=List_Explicit_Values.initialisation_value_to_minus_one,\
	val_t_round_prec=1,\
	val_t_start_sim=None,val_li_additional_matrices_rp_id_lk=[],\
	val_li_additional_rp_cum_matrices=[],val_li_duration_each_rp_mat=[],val_t_unit=None):
		
		#if the number of parameter lists equals the number of the event type
		if len(self._dict_parameters_fcts_event_treat)==self._number_event_types:
		
			#definition of the limit sim time
			t_end_simulation=round(self._t_start_simulation+self._t_duration_simulation,val_t_round_prec)
			
			#if we print messages on the terminal (screen) we print the simulation limit time
			if (val_print_messages_on_terminal)==List_Explicit_Values.initialisation_value_to_one:
				print ("t_end_simulation",t_end_simulation)
				
			#initialisation of the event list
			self.initialisation_event_list_sim(\
			val_veh_prev_demand_have_dynam_constr_final_dest=val_veh_previous_demand_have_dynam_constr_final_dest,\
			val_t_round_precision=val_t_round_prec,\
			val_creat_new_vehicle_demand=val_creation_new_vehicle_demand,\
			val_t_start_calcul_vehicle_appearance=val_t_start_calcul_veh_appearance,\
			val_dict_vehicle_inform_previous_sim=val_di_veh_inform_previous_sim,\
			val_dict_entry_link_inform_previous_sim=val_di_entry_link_info_previous_sim,\
			val_dict_entry_link_inform_given_data=val_di_entry_link_info_given_data,\
			v_t_start_sim=val_t_start_sim,v_t_unit=val_t_unit)
			
			#print("LEN EVENT LIST IN CL SIM:",len(self._heap_even))
			#if the event list is not empty
			if len(self._heap_even)>List_Explicit_Values.initialisation_value_to_zero:
			
				#we update the current sim time
				self._t_current=self._heap_even[List_Explicit_Values.val_first_element_of_list].get_event_time()
				print("CURRENT TIME IN SIM:",self._t_current)
				
				#while the simulation time is inferior to the limit simulation time 
				while(self._t_current<t_end_simulation and len(self._heap_even)>0):
				
					#if wished we print the type of the event to be treated  
					if(val_print_messages_on_terminal)==List_Explicit_Values.initialisation_value_to_one:
					
						print("we will treat an event of type: ",self._heap_even[List_Explicit_Values.val_first_element_of_list].get_event_type())
						#,\"time of the event: ",self._heap_even[List_Explicit_Values.val_first_element_of_list].get_event_time())
						
					#if the first event of the event list is a of type "vehicle appearance"	
					if self._heap_even[List_Explicit_Values.val_first_element_of_list].get_event_type()==Cl_Event.TYPE_EV["type_ev_veh_appearance"] or\
					self._heap_even[List_Explicit_Values.val_first_element_of_list].get_event_type()==Cl_Event.TYPE_EV["type_ev_veh_appearance_nsi"]:
						#if we create new demand
						if val_creation_new_vehicle_demand==List_Explicit_Values.initialisation_value_to_one:
							#we update the vehicle id variable
							self._new_veh_id+=List_Explicit_Values.initialisation_value_to_one
							#we attribute the updated value  to the variable defining the vehicle id in the list of arguments
							#of he function treating the vehicle appearance event 
							self._dict_parameters_fcts_event_treat[self._heap_even[List_Explicit_Values.val_first_element_of_list].get_event_type()][1][\
							self._index_veh_id_in_veh_ap_event]=self._new_veh_id
						#if we employ a previously generated demand demand
						elif val_creation_new_vehicle_demand==List_Explicit_Values.initialisation_value_to_zero:
							self._new_veh_id=self._heap_even[List_Explicit_Values.val_first_element_of_list].get_current_veh_id_demand_previous_sim()
							#print("In CL_SIMULATION WE DO NOT TREAT YET NEW SIM PREVIOUS DEMAND")
							#import sys
							#sys.exit()
						#if we wish to employ a given demand
						elif val_creation_new_vehicle_demand==List_Explicit_Values.initialisation_value_to_minus_one:
							self._new_veh_id+=List_Explicit_Values.initialisation_value_to_one
							#we attribute the updated value  to the variable defining the vehicle id in the list of arguments
							#of he function treating the vehicle appearance event 
							self._dict_parameters_fcts_event_treat[self._heap_even[List_Explicit_Values.val_first_element_of_list].get_event_type()][\
							self._index_veh_id_in_veh_ap_event]=self._new_veh_id
							
							
						#if none of the previous cases for the demand is considered, there is a problem
						#else:
							print("PROBLEM IN CL_SIMULATION, val_creation_new_vehicle_demand: ",val_creation_new_vehicle_demand)
							import sys
							sys.exit()
					
					#print("self._dict_parameters_fcts_event_treat",self._dict_parameters_fcts_event_treat[1][0])
					#print("icic 1",self._dict_parameters_fcts_event_treat[self._heap_even[\
					#List_Explicit_Values.val_first_element_of_list].get_event_type()])
					
					#we treat the event
					self._heap_even[List_Explicit_Values.val_first_element_of_list].event_treat(*(self._dict_parameters_fcts_event_treat[self._heap_even[\
					List_Explicit_Values.val_first_element_of_list].get_event_type()]))
				
				
					#we delete the event from the event pile
					#if we print messages on a terminal (screen) we  print the type of the deleted event
					if (val_print_messages_on_terminal)==List_Explicit_Values.initialisation_value_to_one:
						print ("deletion of the event type and time: ", self._heap_even[List_Explicit_Values.val_first_element_of_list].get_event_type(),\
						self._heap_even[List_Explicit_Values.val_first_element_of_list].get_event_time())
						
					heappop(self._heap_even)
					#for i in self._heap_even:
						#print("type- time of event",i.get_event_type(),i.get_event_time())
					
					#if the event heap is not empty, after the deletion of the event
					if len(self._heap_even)>List_Explicit_Values.initialisation_value_to_zero:
					
						#we update the simulation time
						self._t_current=self._heap_even[List_Explicit_Values.val_first_element_of_list].get_event_time()
							
						#if we print messages on the terminal we print the current simulation time
						if (val_print_messages_on_terminal)==List_Explicit_Values.initialisation_value_to_one:
							print ("t_CURRENT IN  sim  (after delet of treated event) : ",self._t_current)
						
						#TODO
				
						
						
						#FILE=open(val_file_record_netw_obj_sim,"wb")
						#FILE_P=open(val_file_record_pile_event_obj_sim,"wb")
						#FILE_V=open(val_file_record_next_veh_id,"wb")
						#pickle.dump(self._simul_system.get_network(),FILE)
						#pickle.dump(self._heap_even,FILE_P)
						#pickle.dump(self._new_veh_id,FILE_V)
						#FILE.close()
						#FILE_P.close()
						#FILE_V.close()
				

					#if the event heap is  empty, after the deletion of the event
					else:
						#we print a message and stop the simulation
						print("PROBLEME IN CL_SIMULATION, AFTER DELETING THE TREATED EVENT, THE LENTH OF THE EVENT LIST: ",\
						len(self._heap_even))
						import sys
						sys.exit()
				
				
				FILE=open(val_file_record_netw_obj_sim,"wb")
				FILE_P=open(val_file_record_pile_event_obj_sim,"wb")
				FILE_V=open(val_file_record_next_veh_id,"wb")
				self._simul_system.get_network().set_control_actuate_obj(None)
				pickle.dump(self._simul_system.get_network(),FILE)
				pickle.dump(self._heap_even,FILE_P)
				pickle.dump(self._new_veh_id,FILE_V)
				FILE.close()
				FILE_P.close()
				FILE_V.close()
			
			#if the event list is empty, we print a message and interrupt the simulation
			else:
				#we  print a message and interrupt the simulation
				print("PROBLEME IN CL_SIMULATION, AFTER INITIALISATION OF THE EVENT LIST, ITS LENGTH IS : ", len(self._heap_even))
				import sys
				sys.exit()
		
		#if the number of the parameter lists is different from the number of the event types
		else:
			#we print a message and interrupt the simulation
			print("PROBLEME IN CL_SIMULATION, NB OF PARAM LIST: ",len(self._dict_parameters_fcts_event_treat),\
			"NB OF EVENT TYPES:",self._number_event_types)
			
		#for i in self._heap_even:
			#i.print_even_base()
		#print("NB EVENTS IN THE EVENT LIST:",len(self._heap_even))
		
		#li_e_l=[]
		#for i in self._simul_system.get_network().get_di_entry_links_to_network():
			#li_e_l.append(self._simul_system.get_network().get_di_entry_links_to_network()[i].get_nb_vehicle_appearance_at_entry_link())
		#file_name=("t3")
		#lfile=open(file_name,"w")
		#lfile.write("\n %s\t\n"%(li_e_l))
		#lfile.close()
		
			
			
		
	
#*****************************************************************************************************************************************************************************************


	#method continuing a previous simulation
	def simulation_2(self,\
	val_file_record_netw_obj_sim=None,val_file_record_pile_event_obj_sim=None,\
	val_file_record_next_veh_id=None,\
	val_print_messages_on_terminal=List_Explicit_Values.initialisation_value_to_minus_one,val_t_round_prec=1):
	
		#if the number of parameter lists equals the number of the event type
		if len(self._dict_parameters_fcts_event_treat)==self._number_event_types:
		
			#definition of the limit sim time
			t_end_simulation=round(self._t_start_simulation+self._t_duration_simulation,val_t_round_prec)
			
			#if we print messages on the terminal (screen) we print the simulation limit time
			if (val_print_messages_on_terminal)==List_Explicit_Values.initialisation_value_to_one:
				print ("t_end_simulation",t_end_simulation)
				
			#if the ques initial state is not empty 
			if self._simul_system.get_network().get_di_intersections_with_non_empty_init_que_state() !={}:
			
				self.initialisation_que_state_prev_sim(di_que_state_info=self._simul_system.get_network().get_di_intersections_with_non_empty_init_que_state(),\
				ti_start_sim=self._t_start_simulation)

			
			#print("LEN EVENT LIST IN CL SIM:",len(self._heap_even))
			#if the event list is not empty
			if len(self._heap_even)>List_Explicit_Values.initialisation_value_to_zero:
			
				#we update the current sim time
				self._t_current=self._heap_even[List_Explicit_Values.val_first_element_of_list].get_event_time()
				print("CURRENT TIME IN SIM:",self._t_current)
				
				
				
				#while the simulation time is inferior to the limit simulation time 
				while(self._t_current<t_end_simulation and len(self._heap_even)>0):
				
					#if wished we print the type of the event to be treated  
					if(val_print_messages_on_terminal)==List_Explicit_Values.initialisation_value_to_one:
					
						print("we will treat an event of type: ",self._heap_even[List_Explicit_Values.val_first_element_of_list].get_event_type())
						#,\"time of the event: ",self._heap_even[List_Explicit_Values.val_first_element_of_list].get_event_time())
						
					#if the first event of the event list is a of type "vehicle appearance"	
					if self._heap_even[List_Explicit_Values.val_first_element_of_list].get_event_type()==Cl_Event.TYPE_EV["type_ev_veh_appearance"] or\
					self._heap_even[List_Explicit_Values.val_first_element_of_list].get_event_type()==Cl_Event.TYPE_EV["type_ev_veh_appearance_nsi"]:
						
						
						#we update the vehicle index
						self._new_veh_id+=List_Explicit_Values.initialisation_value_to_one
						#we attribute the updated value  to the variable defining the vehicle id in the list of arguments
						#of he function treating the vehicle appearance event 
						self._dict_parameters_fcts_event_treat[self._heap_even[List_Explicit_Values.val_first_element_of_list].get_event_type()][1][\
						self._index_veh_id_in_veh_ap_event]=self._new_veh_id
												
					#we treat the event
					self._heap_even[List_Explicit_Values.val_first_element_of_list].event_treat(*(self._dict_parameters_fcts_event_treat[self._heap_even[\
					List_Explicit_Values.val_first_element_of_list].get_event_type()]))
				
				
					#we delete the event from the event pile
					#if we print messages on a terminal (screen) we  print the type of the deleted event
					if (val_print_messages_on_terminal)==List_Explicit_Values.initialisation_value_to_one:
						print ("deletion of the event type and time: ", self._heap_even[List_Explicit_Values.val_first_element_of_list].get_event_type(),\
						self._heap_even[List_Explicit_Values.val_first_element_of_list].get_event_time())
						
					heappop(self._heap_even)
					#for i in self._heap_even:
						#print("type- time of event",i.get_event_type(),i.get_event_time())
					
					#if the event heap is not empty, after the deletion of the event
					if len(self._heap_even)>List_Explicit_Values.initialisation_value_to_zero:
					
						#we update the simulation time
						self._t_current=self._heap_even[List_Explicit_Values.val_first_element_of_list].get_event_time()
							
						#if we print messages on the terminal we print the current simulation time
						if (val_print_messages_on_terminal)==List_Explicit_Values.initialisation_value_to_one:
							print ("t_CURRENT IN  sim : ",self._t_current)
						
						#TODO
				
						
						#FILE=open(val_file_record_netw_obj_sim,"wb")
						#FILE_P=open(val_file_record_pile_event_obj_sim,"wb")
						#FILE_V=open(val_file_record_next_veh_id,"wb")
						#pickle.dump(self._simul_system.get_network(),FILE)
						#pickle.dump(self._heap_even,FILE_P)
						#pickle.dump(self._new_veh_id,FILE_V)
						#FILE.close()
						#FILE_P.close()
						#FILE_V.close()

					#if the event heap is  empty, after the deletion of the event
					else:
						#we print a message and stop the simulation
						print("PROBLEME IN CL_SIMULATION, AFTER DELETING THE TREATED EVENT, THE LENTH OF THE EVENT LIST: ",\
						len(self._heap_even))
						import sys
						sys.exit()
				
				FILE=open(val_file_record_netw_obj_sim,"wb")
				FILE_P=open(val_file_record_pile_event_obj_sim,"wb")
				FILE_V=open(val_file_record_next_veh_id,"wb")
				self._simul_system.get_network().set_control_actuate_obj(None)
				pickle.dump(self._simul_system.get_network(),FILE)
				pickle.dump(self._heap_even,FILE_P)
				pickle.dump(self._new_veh_id,FILE_V)
				FILE.close()
				FILE_P.close()
				FILE_V.close()
			
			#if the event list is empty, we print a message and interrupt the simulation
			else:
				#we  print a message and interrupt the simulation
				print("PROBLEME IN CL_SIMULATION, AFTER INITIALISATION OF THE EVENT LIST, ITS LENGTH IS : ", len(self._heap_even))
				import sys
				sys.exit()
		
		#if the number of the parameter lists is different from the number of the event types
		else:
			#we print a message and interrupt the simulation
			print("PROBLEME IN CL_SIMULATION, NB OF PARAM LIST: ",len(self._dict_parameters_fcts_event_treat),\
			"NB OF EVENT TYPES:",self._number_event_types)
			
		#for i in self._heap_even:
			#i.print_even_base()
		#print("NB EVENTS IN THE EVENT LIST:",len(self._heap_even))
		
		#li_e_l=[]
		#for i in self._simul_system.get_network().get_di_entry_links_to_network():
			#li_e_l.append(self._simul_system.get_network().get_di_entry_links_to_network()[i].get_nb_vehicle_appearance_at_entry_link())
		#file_name=("t3")
		#lfile=open(file_name,"w")
		#lfile.write("\n %s\t\n"%(li_e_l))
		#lfile.close()
		
		
		
	
#*****************************************************************************************************************************************************************************************
	
#cr_netw=Cl_Creation_Network.Creation_Network()
#netw=cr_netw.function_creation_network()
#print(netw.get_di_intersections())
#sim_sys=Cl_Simulation_System.Simulation_System(val_network=netw)
#sim=Simulation(val_simul_system=sim_sys,val_t_start_simulation=0,val_t_duration_simulation=1000,val_dict_parameters_fcts_event_treat={1:[3]},\
#val_number_event_types=1)
#sim.initialisation_event_list_veh_appearance_events()
#sim.simulation_1(val_creation_new_vehicle_demand=1)






































