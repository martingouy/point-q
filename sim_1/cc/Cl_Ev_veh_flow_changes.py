import Cl_Event
import Cl_Global_Functions
import Cl_Record_Database
from operator import itemgetter
import Cl_Decisions

TYPE_REASON_EVENT_HEV_FLOW_CHANGES={"demand_intensity_variation":1,\
"modification_turn_ratios":2,"turn_ratios_estim":3}

class Ev_veh_flow_changes(Cl_Event.Event):

	def __init__(self,val_ev_t,val_id_intersection_node=None,val_di_rp_mat_next_period={},val_di_mat_cum_rp_next_period={},\
	val_reason_event=None):
	
		gl_funct_obj=Cl_Global_Functions.Global_Functions()
		
		Cl_Event.Event.__init__(self,val_event_time=val_ev_t,\
		val_event_type=Cl_Event.TYPE_EV["ty_ev_veh_flow_changes"],\
		val_global_fct_obj=gl_funct_obj)
		
		#the related intersection node id
		self._id_intersection_node=val_id_intersection_node
		
			
		#the dictionary with the new values of the rout prob to employ (case when th turn ratios vary during the sim)
		self._di_rp_mat_next_period=val_di_rp_mat_next_period
							
																		
		#the dictionary with the values of the cumulative function for each entry-internal link, to employ for the next period
		#key=id entry-internal link, value=[...,[val cum rout prb, dest nd],...]
		self._di_mat_cum_rp_next_period=val_di_mat_cum_rp_next_period
		
		
		#the reason of the event (this variable will have a value from the dict TYPE_REASON_EVENT_HEV_FLOW_CHANGES)
		self._reason_event=val_reason_event
		
		
#*****************************************************************************************************************************************************************************************
	#method returning the intersection node id
	def get_id_intersection_node(self):
		return self._id_intersection_node
	
#*****************************************************************************************************************************************************************************************
	#method returning the diction with the new values of the rout prob
	def getdi_rp_mat_next_period(self):
		return self._di_rp_mat_next_period

#*****************************************************************************************************************************************************************************************
	#method returning the dictionary with the values of the cumulative function for each entry-internal link, of the intersection
	def get_di_mat_cum_rp_next_period(self):
		return self._di_mat_cum_rp_next_period
#*****************************************************************************************************************************************************************************************
	
	#method returning the reason fro this event
	def get_reason_event(self):
		return self._reason_event
#*****************************************************************************************************************************************************************************************
	#method modifying the intersection node id
	def set_id_intersection_node(self,n_v):
		self._id_intersection_node=n_v
	
#*****************************************************************************************************************************************************************************************
	#method modifying the diction with the new values of the rout prob
	def set_di_rp_mat_next_period(self,n_v):
		self._di_rp_mat_next_period=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the dictionary with the values of the cumulative function for each entry-internal link, of the intersection
	def set_di_mat_cum_rp_next_period(self,n_v):
		self._di_mat_cum_rp_next_period=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the dictionary with the values of the cumulative function for each entry-internal link, for the od matrix
	#def set_di_od_mat_cum_fct(self,n_v):
		#self._di_od_mat_cum_fct=n_v

#*****************************************************************************************************************************************************************************************
	
	#method modifying the reason fro this event
	def set_reason_event(self,n_v):
		self._reason_event=n_v
#*****************************************************************************************************************************************************************************************
	#method creating a dict, key=in input link, value=[...,[cum rout prob value, id dest link],...]
	#val_di_cum_rp= dict, key=id phase, value=cum rout prob
	def fct_creat_di_cum_rp_per_inp_lk(self,val_di_cum_rp):
	
		
		di_rep={}
		
		#val_di_cum_rp= dict, key=id phase, value=cum rout prob
		for i in val_di_cum_rp:
			#if the input lk of the phase is not in the dictionary
			if i[0] not in di_rep:
				di_rep[i[0]]=[[val_di_cum_rp[i],i[1]]]
			
			#if the input link of the phase is in the diction
			else:
				di_rep[i[0]].append([val_di_cum_rp[i],i[1]])
		
		
		#for each input link, if the max cum value is < 1 we make it 1
		for j in di_rep:
			#we take the element with the max cum rp
			#el=[max cum rp, id dest link]
			el=max(di_rep[j],key=itemgetter(0))
			
			if el[0]<1:
				el[0]=1
		
		
		return di_rep
		

#*****************************************************************************************************************************************************************************************
	#method calculating the  routing  cum proba from the realised turning ratios, of the related intersection
	#it returne a list of two dictionaries [d1,d2], 
	#d1=dict key=id_phase, value=[..., rout prob of phase at the ith period,...]
	#d2=dict key=id_phase, value=[..., cum out prob of phase at the ith period,...]
	#this method returns [ dict with the turn ratio values for each phase of the intersection,  dict with the cum values of the turn ratio for each phase of the intersection]
	
	def fct_calcul_estimated_turn_ratios_current_period_1(self,val_netw,val_lambda,val_considered_one_in_cum_fct=0.97):
	
		#print("ici, id nd",self._id_intersection_node,val_netw.get_di_intersections()[self._id_intersection_node].get_current_di_rout_prob())
	
		#di_rp_rep, dict, key=id phase,value=turn ratio
		di_rp_rep={}
		#i_cum_rp_rep, dict, key=id phase, value cum value of the turn ratio
		di_cum_rp_rep={}
	
		
		#dict, key=id input link, value=total nb of vehicles which left the input link and joined an output link during the period
		dict_id_input_link_value_total_nb_veh_left_link={}
		
		#for each internal intersection link on calcul the total number of veh  which left the input link and joined an output link, during the period, 
		#for that, we consider each outut link of the intersection
		for i in val_netw.get_di_intersections()[self._id_intersection_node].get_li_id_output_network_links_from_inters_node():
		
			#if self._id_intersection_node==49394:
				#print("id output link",i,"dict", val_netw.get_di_all_links()[i].get_di_ar_to_link_current_period())
			#if i==709:
				#print("di 709",val_netw.get_di_all_links()[i].get_di_ar_to_link_current_period())
			#di_ar_to_link_current_period= dict, associated with each internal or exit link (output links of a node) and of which
			#the key=id link from which vehicles arrived, (entry links excluded), value=nb of the arrived vehicles
			for j in val_netw.get_di_all_links()[i].get_di_ar_to_link_current_period():
				
				#if the (input) link is not in the dictionary
				if j not in dict_id_input_link_value_total_nb_veh_left_link:
					dict_id_input_link_value_total_nb_veh_left_link[j]=val_netw.get_di_all_links()[i].get_di_ar_to_link_current_period()[j]
				
				#if the link is on the dictionary
				else:
					dict_id_input_link_value_total_nb_veh_left_link[j]+=val_netw.get_di_all_links()[i].get_di_ar_to_link_current_period()[j]
			#if self._id_intersection_node==49394:
				#print("dict_id_input_link_value_total_nb_veh_left_link",dict_id_input_link_value_total_nb_veh_left_link)
				#print()
		
		
		#di_rp_rep_1=dict, key=id phase, value=rout prob
		di_rp_rep_1={}			
		#calcul of turn ratio for each input link to the intersection
		for k in val_netw.get_di_intersections()[self._id_intersection_node].get_li_id_input_network_links_to_inters_node():
			#if the link is an  itnernal one
			if k in  val_netw.get_di_intersections()[self._id_intersection_node].get_li_id_internal_links():
		
				#if no vehicle has left the link
				if dict_id_input_link_value_total_nb_veh_left_link[k]==0:
					#for all the queues of the link will have the previous values of the turn ratios
					for m in val_netw.get_di_entry_internal_links()[k].get_set_veh_queue().get_di_obj_veh_queue_at_link():
						di_rp_rep_1[m]=val_netw.get_di_intersections()[self._id_intersection_node].get_current_di_rout_prob()[m]
						#print("di_rp_rep_1[m]",di_rp_rep_1[m])
				#if at least one vehicle has left the link
				else:
					for n in val_netw.get_di_entry_internal_links()[k].get_set_veh_queue().get_di_obj_veh_queue_at_link():
						di_rp_rep_1[n[0],n[1]]=round(val_netw.get_di_all_links()[n[1]].get_di_ar_to_link_current_period()[n[0]]/dict_id_input_link_value_total_nb_veh_left_link[n[0]],2)
			#if the link is an entry one
			else:
				for r in val_netw.get_di_entry_internal_links()[k].get_set_veh_queue().get_di_obj_veh_queue_at_link():
					#print(val_netw.get_di_intersections()[self._id_intersection_node].get_current_di_rout_prob())
					#print("link",k)
					di_rp_rep_1[r]=val_netw.get_di_intersections()[self._id_intersection_node].get_current_di_rout_prob()[r]
				
		#if self._id_intersection_node==49394:
				#print("di_rp_rep_1",di_rp_rep_1)
				#print()			
		#the turn ratio value to return will be a convex combinaison of the current value and the new calculated value
		for p in di_rp_rep_1:
			#if the input link is internal
			if p[0] in  val_netw.get_di_intersections()[self._id_intersection_node].get_li_id_internal_links():
				di_rp_rep[p]=val_lambda*val_netw.get_di_intersections()[self._id_intersection_node].get_current_di_rout_prob()[p]+\
				(1-val_lambda)*di_rp_rep_1[p]
			#if the input link is an entry one
			#else:
				#di_rp_rep[p]=val_netw.get_di_intersections()[self._id_intersection_node].get_current_di_rout_prob()[p]
				
			
		#calcul of the cum values
		#for each input link to the node
		for n in val_netw.get_di_intersections()[self._id_intersection_node].get_li_id_input_network_links_to_inters_node():
			som=0
			#for each queue of the  link
			for q in val_netw.get_di_entry_internal_links()[n].get_set_veh_queue().get_di_obj_veh_queue_at_link():
				#print("lk",q[0],q[0] in val_netw.get_di_intersections()[self._id_intersection_node].get_li_id_internal_links())
				#if the input link is an entry one
				if q[0] in val_netw.get_di_intersections()[self._id_intersection_node].get_li_id_internal_links():
					som=round(som+di_rp_rep[q],2)
					di_cum_rp_rep[q]=som
				#else:
					#di_cum_rp_rep[q]=val_netw.get_di_intersections()[self._id_intersection_node].get_current_di_cum_rout_prob()[q[0]]
					#print(di_cum_rp_rep[q])
		#print(di_cum_rp_rep)
		#if the max element  of the dictionary is sup to 1 on le met a un
		key=max(di_cum_rp_rep,key=di_cum_rp_rep.get)
		if di_cum_rp_rep[key]>1:
			di_cum_rp_rep[key]=1
			
		
		di_cum_rp_rep_1=self.fct_creat_di_cum_rp_per_inp_lk(val_di_cum_rp=di_cum_rp_rep)
		
		
		#if there are entry links corresponding to the intersection, we add the corrrsponding rp and cum rp to the diction
		#if self._id_intersection_node in val_netw.get_dict_id_nds_with_entry_links():
			
			#for m in val_netw.get_dict_id_nds_with_entry_links()[self._id_intersection_node]:
				
				#print("here",val_netw.get_di_intersections()[self._id_intersection_node].get_current_di_rout_prob())
				
				#di_rp_rep[m]=val_netw.get_di_intersections()[self._id_intersection_node].get_current_di_rout_prob()[m]
				#di_cum_rp_rep_1=val_netw.get_di_intersections()[self._id_intersection_node].get_current_di_cum_rout_prob()[m]
				
		#we add the information of the entry links 
		for s in val_netw.get_di_intersections()[self._id_intersection_node].get_li_id_input_network_links_to_inters_node():
			if s not in di_cum_rp_rep_1:
				di_cum_rp_rep_1[s]=val_netw.get_di_intersections()[self._id_intersection_node].get_current_di_cum_rout_prob()[s]
				#print("lk",s,di_cum_rp_rep_1[s])
				
				for t in val_netw.get_di_entry_internal_links()[s].get_set_veh_queue().get_di_obj_veh_queue_at_link():
					di_rp_rep[t]=val_netw.get_di_intersections()[self._id_intersection_node].get_current_di_rout_prob()[t]
					#print(di_rp_rep)
					#import sys
					#sys.exit()
					
				 #print("here",val_netw.get_di_intersections()[self._id_intersection_node].get_current_di_rout_prob())
				 #import sys
				 #sys.exit()
				 #for t in val_netw.get_di_entry_internal_links()[k].get_set_veh_queue().get_di_obj_veh_queue_at_link():
					#print(val_netw.get_di_intersections()[self._id_intersection_node].get_current_di_rout_prob()[t])
					#di_rp_rep[t]=val_netw.get_di_intersections()[self._id_intersection_node].get_current_di_rout_prob()[t]
				
		
		#print(di_cum_rp_rep)
		return [di_rp_rep,di_cum_rp_rep_1]
				

#*****************************************************************************************************************************************************************************************
	#method calculating the  routing   proba from the realised turning ratios, of the related intersection
	#this method returns dict with the turn ratio values for each phase of the intersection,
	
	def fct_calcul_estimated_turn_ratios_current_period_2(self,val_netw,val_lambda):
	
	
		#di_rp_rep, dict, key=id phase,value=turn ratio
		di_rp_rep={}
	
		
		#dict, key=id input link, value=total nb of vehicles which left the input link and joined an output link during the period
		dict_id_input_link_value_total_nb_veh_left_link={}
		
		#for each internal intersection link on calcul the total number of veh  which left the input link and joined an output link, during the period, 
		#for that, we consider each outut link of the intersection
		for i in val_netw.get_di_intersections()[self._id_intersection_node].get_li_id_output_network_links_from_inters_node():
		
			#di_ar_to_link_current_period= dict, associated with each internal or exit link (output links of a node) and of which
			#the key=id link from which vehicles arrived, (entry links excluded), value=nb of the arrived vehicles
			for j in val_netw.get_di_all_links()[i].get_di_ar_to_link_current_period():
				
				#if the (input) link is not in the dictionary
				if j not in dict_id_input_link_value_total_nb_veh_left_link:
					dict_id_input_link_value_total_nb_veh_left_link[j]=val_netw.get_di_all_links()[i].get_di_ar_to_link_current_period()[j]
				
				#if the link is on the dictionary
				else:
					dict_id_input_link_value_total_nb_veh_left_link[j]+=val_netw.get_di_all_links()[i].get_di_ar_to_link_current_period()[j]
			
		
		
		#di_rp_rep_1=dict, key=id phase, value=rout prob
		di_rp_rep_1={}			
		#calcul of turn ratio for each input link to the intersection
		for k in val_netw.get_di_intersections()[self._id_intersection_node].get_li_id_input_network_links_to_inters_node():
			#if the link is an  itnernal one
			if k in  val_netw.get_di_intersections()[self._id_intersection_node].get_li_id_internal_links():
		
				#if no vehicle has left the link
				if dict_id_input_link_value_total_nb_veh_left_link[k]==0:
					#for all the queues of the link will have the previous values of the turn ratios
					for m in val_netw.get_di_entry_internal_links()[k].get_set_veh_queue().get_di_obj_veh_queue_at_link():
						di_rp_rep_1[m]=val_netw.get_di_intersections()[self._id_intersection_node].get_current_di_rout_prob()[m]
						#print("di_rp_rep_1[m]",di_rp_rep_1[m])
				#if at least one vehicle has left the link
				else:
					for n in val_netw.get_di_entry_internal_links()[k].get_set_veh_queue().get_di_obj_veh_queue_at_link():
						di_rp_rep_1[n[0],n[1]]=round(val_netw.get_di_all_links()[n[1]].get_di_ar_to_link_current_period()[n[0]]/dict_id_input_link_value_total_nb_veh_left_link[n[0]],2)
			#if the link is an entry one
			else:
				for r in val_netw.get_di_entry_internal_links()[k].get_set_veh_queue().get_di_obj_veh_queue_at_link():
					#print(val_netw.get_di_intersections()[self._id_intersection_node].get_current_di_rout_prob())
					#print("link",k)
					di_rp_rep_1[r]=val_netw.get_di_intersections()[self._id_intersection_node].get_current_di_rout_prob()[r]
				
			
		#the estimated turn ratio value to return will be a convex combinaison of the current value and the new calculated value
		for p in di_rp_rep_1:
			#if the input link is internal
			#if p[0] in  val_netw.get_di_intersections()[self._id_intersection_node].get_li_id_internal_links():
			di_rp_rep[p]=val_lambda*val_netw.get_di_intersections()[self._id_intersection_node].get_current_di_rout_prob()[p]+\
			(1-val_lambda)*di_rp_rep_1[p]
			#if the input link is an entry one
			#else:
				#di_rp_rep[p]=val_netw.get_di_intersections()[self._id_intersection_node].get_current_di_rout_prob()[p]
				
				
		#print(di_cum_rp_rep)
		return di_rp_rep
				

#*****************************************************************************************************************************************************************************************
	#method returns dict with the turn ratio values for each phase of the intersection
	def fct_calcul_estimated_turn_ratios_current_period_final_destin_dyn_defined(self,val_netw,val_lambda):
	
		#di_rp_rep, dict, key=id phase,value=turn ratio
		di_rp_rep={}
		
		#dict, key=id input link, value=total nb of vehicles which left the input link and joined an output link during the period
		#if when creating the di_ar_to_link_current_period (dict,  key=id link from which vehicles arrived, value=nb of the arrived vehicles)
		#of each internal or exit link, we had considered the entry links (case when OD) then the entrly link ids will be in 
		#the dict dict_id_input_link_value_total_nb_veh_left_link
		dict_id_input_link_value_total_nb_veh_left_link={}
		
		#for each internal intersection link on calcul the total number of veh  which left the input link and joined an output link, during the period, 
		#for that, we consider each outut link of the intersection
		for i in val_netw.get_di_intersections()[self._id_intersection_node].get_li_id_output_network_links_from_inters_node():
		
			#di_ar_to_link_current_period= dict,  key=id link from which vehicles arrived, value=nb of the arrived vehicles
			for j in val_netw.get_di_all_links()[i].get_di_ar_to_link_current_period():
				
				#if the (input) link is not in the dictionary
				if j not in dict_id_input_link_value_total_nb_veh_left_link:
					#if self._id_intersection_node==37593 and self._event_time==2700.1:
						#print("i",i,"j",j,val_netw.get_di_all_links()[i].get_di_ar_to_link_current_period()[j])
					dict_id_input_link_value_total_nb_veh_left_link[j]=val_netw.get_di_all_links()[i].get_di_ar_to_link_current_period()[j]
				
				#if the link is on the dictionary
				else:
					#if self._id_intersection_node==37593 and self._event_time==2700.1:
						#print("i",i,"j",j,val_netw.get_di_all_links()[i].get_di_ar_to_link_current_period()[j])
					dict_id_input_link_value_total_nb_veh_left_link[j]+=val_netw.get_di_all_links()[i].get_di_ar_to_link_current_period()[j]
					
		#di_rp_rep_1=dict, key=id phase, value=rout prob
		di_rp_rep_1={}	
		
		for k in dict_id_input_link_value_total_nb_veh_left_link:
			
			#if no vehicel has left the link, all its ques will have 0 proba
			if dict_id_input_link_value_total_nb_veh_left_link[k]==0:
				for m in  val_netw.get_di_entry_internal_links()[k].get_set_veh_queue().get_di_obj_veh_queue_at_link():
					di_rp_rep_1[m]=0
			#if at least one veh has left the que, we compute the proba
			else:
				for n in val_netw.get_di_entry_internal_links()[k].get_set_veh_queue().get_di_obj_veh_queue_at_link():
				
					di_rp_rep_1[n[0],n[1]]=round(val_netw.get_di_all_links()[n[1]].get_di_ar_to_link_current_period()[n[0]]/dict_id_input_link_value_total_nb_veh_left_link[n[0]],2)
					
		#the estimated turn ratio value to return will be a convex combinaison of the current estimated value and the new calculated one
		for p in di_rp_rep_1:
			#if self._id_intersection_node==37593 and self._event_time==2700.1:
				#print("phase",p,val_netw.get_di_intersections()[self._id_intersection_node].get_di_both_types_rp()[2][p],di_rp_rep_1[p],\
				#round(val_lambda*val_netw.get_di_intersections()[self._id_intersection_node].get_di_both_types_rp()[2][p]+\
				#(1-val_lambda)*di_rp_rep_1[p],2))
				
				
			di_rp_rep[p]=round(val_lambda*val_netw.get_di_intersections()[self._id_intersection_node].get_di_both_types_rp()[2][p]+\
			(1-val_lambda)*di_rp_rep_1[p],2)
		
		#if self._id_intersection_node==37593 and self._event_time==2700.1:
			#import sys
			#sys.exit()
		#if there are links for which  the nb departed veh is not calculated (these will be the entry links), we add the turn ratios from the given value
		#this is because we treat the case when the veh final dest will be dynamically decided (and consequently the demand should not be modified)
		#li_id_input_lks=list(list(dict_id_input_link_value_total_nb_veh_left_link.keys()))
		if len(list(dict_id_input_link_value_total_nb_veh_left_link.keys()))!=len(val_netw.get_di_intersections()[self._id_intersection_node].get_li_id_input_network_links_to_inters_node()):
			#for each entry link of the node
			for q in val_netw.get_dict_id_nds_with_entry_links()[self._id_intersection_node]:
				#li_id_input_lks.append(q)
				for r in val_netw.get_di_entry_links_to_network()[q].get_set_veh_queue().get_di_obj_veh_queue_at_link():
					di_rp_rep[r]=val_netw.get_di_intersections()[self._id_intersection_node].get_di_both_types_rp()[1][r]
					
		#if len(li_id_input_lks)!=len(val_netw.get_di_intersections()[self._id_intersection_node].get_li_id_input_network_links_to_inters_node()):
			#print("PROBLEM IN CL_EV_VEH_FLOW_CHANGES,  AT INTERSECTION:",self._id_intersection_node,\
			#"LINK ID FOR WHICH TURN RATIOS ESTIMATED=",li_id_input_lks,\
			# "input link ids to the intersection:",val_netw.get_di_intersections()[self._id_intersection_node].get_li_id_input_network_links_to_inters_node(),)
			#import sys
			#sys.exit()
			
			
		return di_rp_rep
					
#*****************************************************************************************************************************************************************************************
	#method returns dict with the turn ratio values for each phase of the intersection
	def fct_calcul_estimated_turn_ratios_current_period_final_destin_init_defined(self,val_netw,val_lambda):
	
	
		#di_rp_rep, dict, key=id phase,value=turn ratio
		di_rp_rep={}
		
		#dict, key=id input link, value=total nb of vehicles which left the input link and joined an output link during the period
		#if when creating the di_ar_to_link_current_period (dict,  key=id link from which vehicles arrived, value=nb of the arrived vehicles)
		#of each internal or exit link, we had considered the entry links (case when OD) then the entrly link ids will be in 
		#the dict dict_id_input_link_value_total_nb_veh_left_link
		dict_id_input_link_value_total_nb_veh_left_link={}
		
		#for each internal intersection link on calcul the total number of veh  which left the input link and joined an output link, during the period, 
		#for that, we consider each outut link of the intersection
		for i in val_netw.get_di_intersections()[self._id_intersection_node].get_li_id_output_network_links_from_inters_node():
		
			#di_ar_to_link_current_period= dict,  key=id link from which vehicles arrived, value=nb of the arrived vehicles
			for j in val_netw.get_di_all_links()[i].get_di_ar_to_link_current_period():
				
				#if the (input) link is not in the dictionary
				if j not in dict_id_input_link_value_total_nb_veh_left_link:
					dict_id_input_link_value_total_nb_veh_left_link[j]=val_netw.get_di_all_links()[i].get_di_ar_to_link_current_period()[j]
				
				#if the link is on the dictionary
				else:
					dict_id_input_link_value_total_nb_veh_left_link[j]+=val_netw.get_di_all_links()[i].get_di_ar_to_link_current_period()[j]
					
		#di_rp_rep_1=dict, key=id phase, value=rout prob
		di_rp_rep_1={}	
		
		for k in dict_id_input_link_value_total_nb_veh_left_link:
			
			#if no vehicel has left the link, all its ques will have 0 proba
			if dict_id_input_link_value_total_nb_veh_left_link[k]==0:
				for m in  val_netw.get_di_entry_internal_links()[k].get_set_veh_queue().get_di_obj_veh_queue_at_link():
					di_rp_rep_1[m]=0
			#if at least one veh has left the que, we compute the proba
			else:
				for n in val_netw.get_di_entry_internal_links()[k].get_set_veh_queue().get_di_obj_veh_queue_at_link():
				
					di_rp_rep_1[n[0],n[1]]=round(val_netw.get_di_all_links()[n[1]].get_di_ar_to_link_current_period()[n[0]]/dict_id_input_link_value_total_nb_veh_left_link[n[0]],2)
					
		#the estimated turn ratio value to return will be a convex combinaison of the current estimated value and the new calculated one
		for p in di_rp_rep_1:
			
			di_rp_rep[p]=round(val_lambda*val_netw.get_di_intersections()[self._id_intersection_node].get_di_both_types_rp()[2][p]+\
			(1-val_lambda)*di_rp_rep_1[p],2)
		
		
		#if htere are links for which the number of departed vehicles is not calculated we print a message and stop. When veh final destin initially defined veh departures 
		#are measured for all links so there is a problem. If no vehicle departed during this time, perhaos the estimation period should be increased. 
		if len(list(dict_id_input_link_value_total_nb_veh_left_link.keys()))!=len(val_netw.get_di_intersections()[self._id_intersection_node].get_li_id_input_network_links_to_inters_node()):
			print("PROBLEM IN CL_EV_VEH_FLOW_CHANGES, IN fct_calcul_estimated_turn_ratios_current_period_final_destin_init_defined, THERE ARE LINKS  for which the number of departed vehicles is not calculated,\
			NB LINKS FOR WHICH TURN RATIOS ARE MEASURED):",len(list(dict_id_input_link_value_total_nb_veh_left_link.keys()),\
			"NB INCOMING LINKS TO NODE",len(val_netw.get_di_intersections()[self._id_intersection_node].get_li_id_input_network_links_to_inters_node())))
			import sys
			sys.exit()
		
		
		
		#if there are links for which  the nb departed veh is not calculated (these will be the entry links), we add the turn ratios from the given value
		#this is because we treat the case when the veh final dest will be dynamically decided
		#li_id_input_lks=list(list(dict_id_input_link_value_total_nb_veh_left_link.keys()))
		#if len(list(dict_id_input_link_value_total_nb_veh_left_link.keys()))!=len(val_netw.get_di_intersections()[self._id_intersection_node].get_li_id_input_network_links_to_inters_node()):
	
			#for each entry link of the node
			#for q in val_netw.get_dict_id_nds_with_entry_links()[self._id_intersection_node]:
				#li_id_input_lks.append(q)
				#for r in val_netw.get_di_entry_links_to_network()[q].get_set_veh_queue().get_di_obj_veh_queue_at_link():
					#di_rp_rep[r]=val_netw.get_di_intersections()[self._id_intersection_node].get_di_both_types_rp()[2][r]
					
		#if len(li_id_input_lks)!=len(val_netw.get_di_intersections()[self._id_intersection_node].get_li_id_input_network_links_to_inters_node()):
			#print("PROBLEM IN CL_EV_VEH_FLOW_CHANGES,  AT INTERSECTION:",self._id_intersection_node,\
			#"LINK ID FOR WHICH TURN RATIOS ESTIMATED=",li_id_input_lks,\
			# "input link ids to the intersection:",val_netw.get_di_intersections()[self._id_intersection_node].get_li_id_input_network_links_to_inters_node(),)
			#import sys
			#sys.exit()
			
			
		return di_rp_rep
					
#*****************************************************************************************************************************************************************************************
	#method treating this event if it is called for updating  rout prob
	def fct_treat_case_modif_turn_ratios_val(self,val_network,val_dict_turn_prob, val_dict_cum_turn_prob,val_file_recording_event_db):
	
		
		#we update the dictionary of the values of the cum  fct ( for the rout prop of each network phase)
		#val_network.set_current_di_cum_rout_prob_input_lk(self._di_rp_mat_cum_fct_inters)
		val_network.get_di_intersections()[self._id_intersection_node].fct_update_intersection_case_modif_turn_ratios(\
		val_di_turn_prob=val_dict_turn_prob,val_di_cum_turn_prob=val_dict_cum_turn_prob)
		
		
		
		
		#we record the event
		record_db_obj=Cl_Record_Database.Record_Database(\
		val_file_db=val_file_recording_event_db,\
		val_id_inters_node=self._id_intersection_node,\
		val_ev_time=self._event_time,val_ev_type=self._event_type,\
		val_current_inters_turn_ratio_val=val_network.get_di_intersections()[self._id_intersection_node].get_current_di_rout_prob(),\
		val_current_inters_cum_turn_ratio_val=val_network.get_di_intersections()[self._id_intersection_node].get_current_di_cum_rout_prob())
		#val_mat_rp_cum_netw=val_network.get_dict_mat_rp_cum_key_entry_intern_lk_value_list_cum_fct_values())
		
		
		#we record the event in the db 
		record_db_obj.fct_write_object_in_db_file()
		

#*****************************************************************************************************************************************************************************************
	#method treatingt he case when the reason of this event is for updating the  initial values of veh arrivals at links and queues,
	# when dyn computing  the realised values of split ratios
	def fct_treat_case_estimated_values_turn_ratios_veh_final_dest_dyn_defined(self,\
	val_network,val_prec_round,val_li_ev,val_file_recording_event_db):
		
		#calcul the new employed values of turn prob
		#li_di_rout_proba_and_di_cum_rout_proba=dict,
		# key=id_phase, value=rout prob of phase at the ith period
		li_di_estimated_turn_ratios=self.fct_calcul_estimated_turn_ratios_current_period_final_destin_dyn_defined(val_netw=val_network,\
		val_lambda=val_network.get_di_intersections()[self._id_intersection_node].get_li_param_estim_turn_ratios()[0])
		
		
		#we record the event before updating the intersection so as to have the current values of the  turn ratios
		record_db_obj=Cl_Record_Database.Record_Database(\
		val_file_db=val_file_recording_event_db,\
		val_ev_time=self._event_time,val_ev_type=self._event_type,\
		val_id_inters_node=self._id_intersection_node,
		val_mat_rp_cum_netw=val_network.get_di_intersections()[self._id_intersection_node].get_current_di_cum_rout_prob(),\
		val_current_inters_turn_ratio_val=val_network.get_di_intersections()[self._id_intersection_node].get_current_di_rout_prob(),\
		val_new_estim_inters_turn_turn_ratio_val=li_di_estimated_turn_ratios,\
		val_current_estim_inters_turn_ratio_val=val_network.get_di_intersections()[self._id_intersection_node].get_di_both_types_rp()[2])
		#,\
		#val_mat_estimated_rp_cum_netw=li_di_turn_ratios_and_di_cum_turn_ratios[1])
		
			
		#we record the event in the db 
		record_db_obj.fct_write_object_in_db_file()
		
		
		#if self._id_intersection_node==37872:
			#print("di rp avant",val_network.get_di_intersections()[self._id_intersection_node].get_current_di_rout_prob())
			#print()
			#print("di rp cum avant",val_network.get_di_intersections()[self._id_intersection_node].get_current_di_cum_rout_prob())
		#update the intersection 
		val_network.get_di_intersections()[self._id_intersection_node].\
		fct_update_intersection_case_estimated_turn_ratios(val_di_turn_ratios=li_di_estimated_turn_ratios,val_netwk=val_network)
		#if self._id_intersection_node==37872:
			#print("di rp apres",val_network.get_di_intersections()[self._id_intersection_node].get_current_di_rout_prob())
			#print()
			#print("di rp cum apres",val_network.get_di_intersections()[self._id_intersection_node].get_current_di_cum_rout_prob())
		
		
		#creation of the next event for updating the estimated rout prop
		t_ev=round(self._event_time+val_network.get_di_intersections()[self._id_intersection_node].get_li_param_estim_turn_ratios()[1],val_prec_round)
		
		ev_veh_flow_changes=Ev_veh_flow_changes(val_ev_t=t_ev,val_id_intersection_node=self._id_intersection_node,val_reason_event=self._reason_event)
		ev_veh_flow_changes.fct_insertion_even_in_event_list(event_list=val_li_ev,\
		message="IN CL_EV_VEH_flow whanges IN FUNCT \
		fct_treat_case_estimated_values_turn_ratios \
		NEXT  EVENT VEH FLOW CHANGES HAS TIME < TIME FIRST EVENT IN THE LIST")
		
		
		
#*****************************************************************************************************************************************************************************************
	#method treatingt he case when the reason of this event is for updating the  initial values of veh arrivals at links and queues,
	# when dyn computing  the realised values of split ratios
	def fct_treat_case_estimated_values_turn_ratios_veh_final_dest_initial_defined(self,\
	val_network,val_prec_round,val_li_ev,val_file_recording_event_db):
		
		#calcul the new employed values of turn prob
		#li_di_rout_proba_and_di_cum_rout_proba=dict,
		# key=id_phase, value=rout prob of phase at the ith period
		li_di_estimated_turn_ratios=self.fct_calcul_estimated_turn_ratios_current_period_final_destin_init_defined(val_netw=val_network,\
		val_lambda=val_network.get_di_intersections()[self._id_intersection_node].get_li_param_estim_turn_ratios()[0])
		
		
		#we record the event before updating the intersection so as to have the current values of the  turn ratios
		record_db_obj=Cl_Record_Database.Record_Database(\
		val_file_db=val_file_recording_event_db,\
		val_ev_time=self._event_time,val_ev_type=self._event_type,\
		val_id_inters_node=self._id_intersection_node,
		val_mat_rp_cum_netw=val_network.get_di_intersections()[self._id_intersection_node].get_current_di_cum_rout_prob(),\
		val_current_inters_turn_ratio_val=val_network.get_di_intersections()[self._id_intersection_node].get_current_di_rout_prob(),\
		val_new_estim_inters_turn_turn_ratio_val=li_di_estimated_turn_ratios,\
		val_current_estim_inters_turn_ratio_val=val_network.get_di_intersections()[self._id_intersection_node].get_di_both_types_rp()[2])
		#,\
		#val_mat_estimated_rp_cum_netw=li_di_turn_ratios_and_di_cum_turn_ratios[1])
		
			
		#we record the event in the db 
		record_db_obj.fct_write_object_in_db_file()
		
		
		#if self._id_intersection_node==37872:
			#print("di rp avant",val_network.get_di_intersections()[self._id_intersection_node].get_current_di_rout_prob())
			#print()
			#print("di rp cum avant",val_network.get_di_intersections()[self._id_intersection_node].get_current_di_cum_rout_prob())
		#update the intersection 
		val_network.get_di_intersections()[self._id_intersection_node].\
		fct_update_intersection_case_estimated_turn_ratios(val_di_turn_ratios=li_di_estimated_turn_ratios,val_netwk=val_network)
		#if self._id_intersection_node==37872:
			#print("di rp apres",val_network.get_di_intersections()[self._id_intersection_node].get_current_di_rout_prob())
			#print()
			#print("di rp cum apres",val_network.get_di_intersections()[self._id_intersection_node].get_current_di_cum_rout_prob())
		
		
		#creation of the next event for updating the estimated rout prop
		t_ev=round(self._event_time+val_network.get_di_intersections()[self._id_intersection_node].get_li_param_estim_turn_ratios()[1],val_prec_round)
		
		ev_veh_flow_changes=Ev_veh_flow_changes(val_ev_t=t_ev,val_id_intersection_node=self._id_intersection_node,val_reason_event=self._reason_event)
		ev_veh_flow_changes.fct_insertion_even_in_event_list(event_list=val_li_ev,\
		message="IN CL_EV_VEH_flow whanges IN FUNCT \
		fct_treat_case_estimated_values_turn_ratios \
		NEXT  EVENT VEH FLOW CHANGES HAS TIME < TIME FIRST EVENT IN THE LIST")
		
		
		
#*****************************************************************************************************************************************************************************************
	#method treating the event 
	
	def event_treat_1(self,val_netwrk=None,file_recording_event_db=None,val_li_event=None):
		pass
		
	def event_treat(self,val_netwrk=None,val_precis_round=None,veh_final_dest_dyn_defined=None,file_recording_event_db=None,val_li_event=None):
		
		#if the reson of this event  is for updating the turn ratios
		if self._reason_event==TYPE_REASON_EVENT_HEV_FLOW_CHANGES["modification_turn_ratios"]:
		
			
			
			self.fct_treat_case_modif_turn_ratios_val(\
			val_network=val_netwrk,\
			val_dict_turn_prob=self._di_rp_mat_next_period, val_dict_cum_turn_prob=self._di_mat_cum_rp_next_period,\
			val_file_recording_event_db=file_recording_event_db)
			
			
		#if the reason of this event is for updating the  initial values of veh arrivals at links and queues, when dyn computing  the realised values of split ratios
		elif self._reason_event==\
		TYPE_REASON_EVENT_HEV_FLOW_CHANGES["turn_ratios_estim"]:
			
			#if the veh final dest is dyn defined
			if veh_final_dest_dyn_defined==Cl_Decisions.TYPE_VEHICLE_FINAL_DESTINATION_AND_PATH["dynamically_defined"]:
						
				self.fct_treat_case_estimated_values_turn_ratios_veh_final_dest_dyn_defined(\
				val_network=val_netwrk,val_prec_round=val_precis_round,val_li_ev=val_li_event,val_file_recording_event_db=file_recording_event_db)
			else:
				
				self.fct_treat_case_estimated_values_turn_ratios_veh_final_dest_initial_defined(\
				val_network=val_netwrk,val_prec_round=val_precis_round,val_li_ev=val_li_event,val_file_recording_event_db=file_recording_event_db)

	
#*****************************************************************************************************************************************************************************************














