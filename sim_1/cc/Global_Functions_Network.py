import List_Explicit_Values
import File_Sim_Name_Module_Files
import File_names_network_model
import Parse_network_xml_files
import Cl_Event
import math
import os
import random

#Global functions employed when the netwwork is  constructed
#*****************************************************************************************************************************************************************************************
#method creat a dict with the link id and the related mean travel time from a file containing this info
def fct_creat_di_id_link_mean_trav_time_from_tet_file(name_file_to_read,nb_comment_lines):
	#we open the file
	file=open(name_file_to_read,"r")
	ind=0
	di_rep={}
	
	for i in file.readlines():
		ind+=1
		if ind>nb_comment_lines:
			a=i.rsplit()
			di_rep[eval(a[0])]=eval(a[len(a)-1])
			
	file.close()
	
	#for i in di_rep:
		#print("i",i,"di_rep",di_rep[i])
		
	return di_rep
	

#*****************************************************************************************************************************************************************************************
#method computing the param of the lognormal distrib for computing stoch travel time
def fct_comput_lognormal_param(di_id_link_mean_travel_time,sigma=0.974174,b=0.8):

	#dict, key=id link, value= mu or sigma or shift
	di_mu={}
	di_sigma={}
	di_shift={}
	
	for i in di_id_link_mean_travel_time:
		di_mu[i]=math.log(0.124438*di_id_link_mean_travel_time[i])
		di_sigma[i]=sigma
		di_shift[i]=b*di_id_link_mean_travel_time[i]
		
	return[di_mu,di_sigma,di_shift]
		
#*****************************************************************************************************************************************************************************************
#method returning a list [di_mu,di_sigma,di_shift] with the param of the lognormal distribution when calcul stoch mean travel time for the arcs
def fct_creat_dict_param_stoch_travel_time_from_text_file_all_links(v_name_file_to_read,v_nb_comment_lines,v_sigma=0.974174,v_b=0.8):

	di_id_lk_mean_trav_time= fct_creat_di_id_link_mean_trav_time_from_tet_file(name_file_to_read=v_name_file_to_read,nb_comment_lines=v_nb_comment_lines)
	
	li_dict=fct_comput_lognormal_param(di_id_link_mean_travel_time=di_id_lk_mean_trav_time,sigma=v_sigma,b=v_b)
	
	return li_dict
	
#*****************************************************************************************************************************************************************************************


#function reading the file with the sensor(presence or que size)  information and returns a dict, key=id que, value=[position 1 sensor in the que,....]
def fct_creat_dict_key_id_que_value_lis_init_position_que_size_sensor_in_que(name_file_to_read,number_lines_to_read):

	di={}
	#each line of this file is : id origin lk, id dest lk, position of sensor in the que
	file=open(name_file_to_read,"r")
	
	ind=0
	for i in file.readlines():
		ind+=1
		if ind>number_lines_to_read:
			a=i.rsplit()
			if (eval(a[0]),eval(a[1])) not in di:
				di[eval(a[0]),eval(a[1])]=[]
				for j in a[2:len(a)]:
					di[eval(a[0]),eval(a[1])].append(eval(j))
			
			else:
				di[eval(a[0]),eval(a[1])].append(eval(a[2]))
	file.close()
	return di

	
#*****************************************************************************************************************************************************************************************
#function reading the file with the sensor(presence or que size)  information and returns a dict, key=id que, value=[position 1 sensor in the que,....]
def fct_creat_dict_key_id_que_value_lis_init_and_final_position_presence_sensor_in_que(name_file_to_read,number_lines_to_read):

	di={}
	#each line of this file is : id origin lk, id dest lk, position of sensor in the que
	file=open(name_file_to_read,"r")
	
	ind=0
	for i in file.readlines():
		ind+=1
		if ind>number_lines_to_read:
			a=i.rsplit()
			if (eval(a[0]),eval(a[1])) not in di:
				di[eval(a[0]),eval(a[1])]=[[eval(a[2]),eval(a[3])]]
			
			else:
				di[eval(a[0]),eval(a[1])].append([eval(a[2]),eval(a[3])])
	file.close()
	return di

	
#*****************************************************************************************************************************************************************************************
#function reading the file with the sensor(presence or que size)  information and returns a dict, key=id que, value=[position 1 sensor in the que,....]
def fct_creat_dict_key_id_que_value_lis_init_position_que_size_sensor_in_que_1(name_file_to_read,number_lines_to_read):

	di={}
	#each line of this file is : id origin lk, id dest lk, position of sensor in the que
	file=open(name_file_to_read,"r")
	
	ind=0
	for i in file.readlines():
		ind+=1
		if ind>number_lines_to_read:
			a=i.rsplit()
			if (eval(a[0]),eval(a[1])) not in di:
				di[eval(a[0]),eval(a[1])]=[eval(a[2])]
			
			else:
				di[eval(a[0]),eval(a[1])].append(eval(a[2]))
	file.close()
	return di

	
#*****************************************************************************************************************************************************************************************
#function reading file "fi_id_phase_rout_prop.txt" and returns  [dict_1,dict_2,dict_3], EXPLICIT VALUE 0.98
#dict_1, key=id entry_internal lk, value=[...,prob_corresponding phase,...]
#dict_2, key=id entry_internal lk, value=[...,cum fct,...]
#dict_3,key=id entry_internal lk, value=[...,id dest,...]
#thus dict_1[key][i] is the  probability of phase (key, dict_2[key][i])
#val_considered_one_in_cum_fct=0.98 when we som after this value the approx will be 1
def fct_creat_dicts_rp_mat_1(name_file_read,nb_comment_lines,val_considered_one_in_cum_fct):
	#print("name_file_read",name_file_read)
	#we open the file
	file=open(name_file_read,"r")
	di_prob={}
	di_id_dest_lk={}
	ind_nb_line_read=0
	for i in file.readlines():
		ind_nb_line_read+=1
		if ind_nb_line_read>nb_comment_lines:
			a=i.rsplit()
			#print("a=",a)
			#print()
			b=eval(a[0])
			if b not in di_prob:
				di_prob[b]=[eval(a[2])]
			else:
				di_prob[b].append(eval(a[2]))
				#if name_file_read=="fi_mod_id_phase_prob_dest_lk9.txt":
					#print("b=",b,"di_id_dest_lk",di_id_dest_lk)
			if b not in di_id_dest_lk:
				di_id_dest_lk[b]=[int(eval(a[1]))]
			else:
				di_id_dest_lk[b].append((eval(a[1])))
	#if name_file_read=="fi_mod_id_phase_prob_dest_lk9.txt":
		#print(di_id_dest_lk)
		#import sys
		#sys.exit()
	#creation of the dict with the cum values
	di_cum={}
	#di_prob, dict, key=id entry_intern lk, value=list prob
	for i in di_prob:
		s=0
		di_cum[i]=[s]
		for j in di_prob[i]:
			s+=j
			if s>val_considered_one_in_cum_fct:
				s=1
			di_cum[i].append(s)
	
	#print(di_cum)
	return[di_prob,di_cum,di_id_dest_lk]	
	
#*****************************************************************************************************************************************************************************************
#li_liste=[[1,2],[2,3],[5,4],[5,5]]
#on retourne un dict des elements ayant eg la prem coordonnee
#key=5, value=[[5,4],[5,5]]
def fct_entry_intenal_links_having_at_least_two_output_links(li_liste):
	
	li_1=list(li_liste)
	
	#print("li_1",li_1)
	
	lon=len(li_1)
	

	di_rep={}

	for i in range(lon):
		li_2=list(li_1)
		li_2.remove(li_1[i])
		
		#print("li_2",li_2)
		#import sys
		#sys.exit()
		for j in li_2:
			
			#print("j=",j)
			if li_1[i][0]==j[0]:
				#print("li_1[i] not in li_rep",di_[i] not in di_rep)
				if li_1[i][0] not in di_rep:
					di_rep[li_1[i][0]]=[li_1[i]]
				if j not in di_rep[j[0]]:
					di_rep[j[0]].append(j)
			#print("li_rep=",di_rep)
	#print("HERE 2 di_rep",di_rep)
	#import sys
	#sys.exit()
	return di_rep

#*****************************************************************************************************************************************************************************************

#function calculating  the cummulative  values of rout prob  

#it returns di_cum, key:entry-internal link, value=[...,[li_cum prob, id dest link],...] where
#for ex li_cum prob=[0.1,0.2,0.7,0.9] that means that during the first period (period duration is indicated in the dict witht the rout prob)
#the cum prob of the related  dest link values 0.1, during the second period it values 0.2 etc.

#dict_cum_rp_mat: dict, key=id entry-internal link , value==[...,[cum prob, id related dest link],...]
#val_dict_rp_mat= dict, key=phase id, value=[ ....,[list values rout prop,duration],....]
def  fct_creat_dict_cum_rp_mat_from_text_file(val_name_file_rout_prop_to_read,\
nb_comment_lines=1,val_considered_one_in_cum_fct=0.97):


	#we open the file
	file=open(val_name_file_rout_prop_to_read,"r")
	di_prob={}
	ind_nb_line_read=0
	for i in file.readlines():
		ind_nb_line_read+=1
		if ind_nb_line_read>nb_comment_lines:
			a=i.rsplit()
			#print("a=",a)
			#print()
			a1=eval(a[0])
			a2=eval(a[1])
			b=(a1,a2)
			if b not in di_prob:
				cle=list(b)
				
				#di_prob[a1,a2]=[eval(a[2])]
				di_prob[a1,a2]=eval(a[2])
			else:
				print(" PROBLEM IN GLOB FCT NETW, fct_creat_dict_cum_rp_mat_from_text_file, KEY PHASE ", b,\
				"EXISTS IN DICT PHASES PROB ",di_prob.keys())
				import sys
				sys.exit()
				#di_prob[a1,a2].append(eval(a[2]))
				#di_prob[a1,a2].append(eval(a[2]))
				#if name_file_read=="fi_mod_id_phase_prob_dest_lk9.txt":
			
	file.close()			
	#print("di_prob",di_prob)
	#print()
	
	v_li_keys=list(di_prob.keys())
	#print("v_li_keys",v_li_keys)
	#print()
	
		
	#phases with at least two output links
	#key=common input link to phases, value phases, ex di={4:[(4,5),(4,6)]}
	di_entry_internal_with_at_least_two_outp_lks=fct_entry_intenal_links_having_at_least_two_output_links(li_liste=v_li_keys)
	#print("di_entry_internal_with_at_least_two_outp_lks",di_entry_internal_with_at_least_two_outp_lks)
	#print()
	
	
	
	#dict, key:entry-internal link, value=[...,[cum prob, id dest link],...]
	di_cum={}
	
	for i in di_entry_internal_with_at_least_two_outp_lks:
		som=0
		#print()
		#print("i=",i)
		#print()
		di_cum[i]=[]
		
		#print("di_entry_internal_with_at_least_two_outp_lks[i][0]]",di_entry_internal_with_at_least_two_outp_lks[i][0])
		#print()
		
		#print("HERE",di_prob[di_entry_internal_with_at_least_two_outp_lks[i][0]])
		
		#val_dict_rp_mat[di_entry_internal_with_at_least_two_outp_lks[i][0]][0]=list des valeurs de  rout prob of phase i
		#lon=len(di_prob[di_entry_internal_with_at_least_two_outp_lks[i][0]])
		
		#li_init=[0]*lon
		#print("li_init",li_init)
		#for each phase with at least two outp links, di_phases_with_at_least_two_outp_lks[i]=[(4,5),(4,6)]
		for j in di_entry_internal_with_at_least_two_outp_lks[i]:
			#print("j=",j)
			#print("di_prob[j]",di_prob[j])
			som+=di_prob[j]
			
			
			#s=[x+y for x,y in zip(li_init,di_prob[j])]
			#print("s=",s)
			#di_cum[i].append([s,j[1]])
			di_cum[i].append([som,j[1]])
			#print("s=",s)
			#li_init=s
		

	#print("di_cum",di_cum)
	#import sys
	#sys.exit()
		
	#all phases
	li_all_phases=list(di_prob.keys())
	#li_all_phases_1=val_dict_rp_mat.keys()
	#print(li_all_phases)

	
	#wer emove from the list of all phases the ones who correspond to entry-internal links with at least two output links
	for m in di_entry_internal_with_at_least_two_outp_lks:
		for n in di_entry_internal_with_at_least_two_outp_lks[m]:
			#print("n=",n)
			#print(li_all_phases)
			li_all_phases.remove(n)
		
	#print(li_all_phases,lon)
		
	#the cum prob for the remained phases is one
	#li=[1]*lon
	li=1
	for p in li_all_phases:
		di_cum[p[0]]=[[li,p[1]]]
	
	#print(di_cum)
	
	
	#li_dur=[]
	# val_dict_rp_mat dict, key=phase id, value=[ ....,[list values rout prop,duration],....]
	#print("val_dict_rp_mat",val_dict_rp_mat)
	#for  q in val_dict_rp_mat:
		#print("q=",q)
		#for r in val_dict_rp_mat[q][1]:
		#print("r=",r)
		#li_dur.append(val_dict_rp_mat[q][1])
	#print(li_dur)
	
	for m in di_cum:
	
		if di_cum[m][len(di_cum[m])-1][0]>val_considered_one_in_cum_fct:
			di_cum[m][len(di_cum[m])-1][0]=1
		
		
		
	return di_cum
	
	
#*****************************************************************************************************************************************************************************************

#function calculating  the cummulative  values of rout prob  

#it returns di_cum, key:entry-internal link, value=[...,[li_cum prob, id dest link],...] where
#for ex li_cum prob=[0.1,0.2,0.7,0.9] that means that during the first period (period duration is indicated in the dict witht the rout prob)
#the cum prob of the related  dest link values 0.1, during the second period it values 0.2 etc.

#dict_cum_rp_mat: dict, key=id entry-internal link , value==[...,[cum prob, id related dest link],...]
#val_dict_rp_mat= dict, key=phase id, value=[ ....,[list values rout prop,duration],....]
def  fct_creat_dict_cum_rp_mat(val_dict_rp_mat,val_considered_one_in_cum_fct):

	v_li_keys=list(val_dict_rp_mat.keys())
	#print("val_dict_rp_mat",val_dict_rp_mat)
	
		
	#phases with at least two output links
	#key=common input link to phases, value phases, ex di={4:[(4,5),(4,6)]}
	di_entry_internal_with_at_least_two_outp_lks=fct_entry_intenal_links_having_at_least_two_output_links(li_liste=v_li_keys)
	
	#dict, key:entry-internal link, value=[...,[cum prob, id dest link],...]
	di_cum={}
	
	for i in di_entry_internal_with_at_least_two_outp_lks:
		
		di_cum[i]=[]
		
		#print("HERE",val_dict_rp_mat[di_entry_internal_with_at_least_two_outp_lks[i][0]])
		#val_dict_rp_mat[di_entry_internal_with_at_least_two_outp_lks[i][0]][0]=list des valeurs de  rout prob of phase i
		lon=len(val_dict_rp_mat[di_entry_internal_with_at_least_two_outp_lks[i][0]][0])
		li_init=[0]*lon
		#print("li_init",li_init)
		#for each phase with at least two outp links, di_phases_with_at_least_two_outp_lks[i]=[(4,5),(4,6)]
		for j in di_entry_internal_with_at_least_two_outp_lks[i]:
			#print("j=",j)
			#print("val_dict_rp_mat[j]",val_dict_rp_mat[j])
			
			s=[x+y for x,y in zip(li_init,val_dict_rp_mat[j][0])]
			di_cum[i].append([s,j[1]])
			#print("s=",s)
			li_init=s
		#print("di_cum",di_cum)
		
	#all phases
	li_all_phases=list(val_dict_rp_mat.keys())
	#li_all_phases_1=val_dict_rp_mat.keys()
	#print(li_all_phases)

	
	#wer emove from the list of all phases the ones who correspond to entry-internal links with at least two output links
	for m in di_entry_internal_with_at_least_two_outp_lks:
		for n in di_entry_internal_with_at_least_two_outp_lks[m]:
			#print("n=",n)
			#print(li_all_phases)
			li_all_phases.remove(n)
		
	#print(li_all_phases,lon)
		
	#the cum prob for the remained phases is one
	#li=[1]*lon
	li=[1]
	for p in li_all_phases:
		di_cum[p[0]]=[[li,p[1]]]
	
	#print(di_cum)
	
	#li_dur=[]
	# val_dict_rp_mat dict, key=phase id, value=[ ....,[list values rout prop,duration],....]
	#print("val_dict_rp_mat",val_dict_rp_mat)
	#for  q in val_dict_rp_mat:
		#print("q=",q)
		#for r in val_dict_rp_mat[q][1]:
		#print("r=",r)
		#li_dur.append(val_dict_rp_mat[q][1])
	#print(li_dur)
		
	return di_cum
	
	
#*****************************************************************************************************************************************************************************************
#method reading file "fi_id_entry_exit_lk_related_path.txt" and return a dictionary
#key=id intersection node, value=dict, key=(id entry link, id exit link) path to follow
def fct_creat_dict_unique_paths(val_name_file_to_read,val_nb_comment_lines,val_netw):
	
	#we open the file
	file=open(val_name_file_to_read,"r")
	
	di_rep={}
	
	#key=id phase, value=[..., link id to follow,...]
	di_rep_1={}
	ind_nb_line_read=0
	for i in file.readlines():
		ind_nb_line_read+=1
		if ind_nb_line_read>val_nb_comment_lines:
			a=i.rsplit()
			#print("a=",a)
			#print()
			a1=eval(a[0])
			a2=eval(a[1])
			b=(a1,a2)
			if b not in di_rep_1:
				di_rep_1[a1,a2]=[]
				for j in a[2:]:
					di_rep_1[a1,a2].append(eval(j))
				di_rep_1[a1,a2].append(a2)
			
			else:
				for j in a[2:]:
					di_rep_1[a1,a2].append(eval(j))
				di_rep_1[a1,a2].append(a2)
	
	for j in di_rep_1:
		
		if val_netw.get_di_entry_internal_links()[j[0]].get_id_head_intersection_node() not in di_rep:
		
			di_rep[val_netw.get_di_entry_internal_links()[j[0]].get_id_head_intersection_node()]={}
			
			di={}
			#print("di_rep_1[j]",di_rep_1[j])
			di[j]=di_rep_1[j]
			
			di_rep[val_netw.get_di_entry_internal_links()[j[0]].get_id_head_intersection_node()].update(di)
			
		
		#if the related network node is in the dictionary
		else:
			di={}
			di[j]=di_rep_1[j]
			di_rep[val_netw.get_di_entry_internal_links()[j[0]].get_id_head_intersection_node()].update(di)
	

	file.close()
	return di_rep
#*****************************************************************************************************************************************************************************************

#method reading a set of files "fi_id_phase_prob_rout_prop.txt" or a set of file "fi_id_phase_val_cum_funct_rout_prop.txt", and returns a list of diction.
#each such dict has  key=id entry_internal lk, value=[.., id dest lk,...]
def fct_creating_li_rp_mat_1(v_name_file_read, v_nb_files,v_nb_comment_lines):
	
	li_di=[]
	for i in range(v_nb_files):
	
		v_file=v_name_file_read+str(i+1)+".txt"
		dic=function_reading_id_entry_intern_lk_id_dest_lk(name_file_read=v_file,nb_comment_lines=v_nb_comment_lines)
		
		li_di.append(dic)
		
	return li_di
	
#*****************************************************************************************************************************************************************************************

#function reading a file and returning a dictionary of which the key is the 1st column and the value is a list containing the elements starting from the
#2nd column. This function will be used fro creating the network. The related files have as a first column an id (of a node, or link) 
#and the following elements
#are the id of entering/leaving/exiting links or the id of the origin node and the destination node of the link etc.
def function_reading_file_containing_nd_or_link_information(file_name_read,type=int):
	#if file_name_read=="../../SMALL_DATA_2NDS/fi_id_link_id_sublinks.txt":
		#print("HERE")
		
	#we open the file
	file=open(file_name_read,"r")
	#print("FILE NAME",file_name_read)
	
	#creation of the dictionary
	m_dict={}
	for i in file.readlines():
		#variable indicating that we shall construct the list after reading the first element of each line, (the 1s column corresponds to an id)
		ind_starting_append=List_Explicit_Values.initialisation_value_to_zero
		a=i.rsplit()
		#print("a",a)
		m_dict[eval(a[List_Explicit_Values.initialisation_value_to_zero])]=[]
		for j in a:
			#print("HERE,",j)
			
			ind_starting_append+=List_Explicit_Values.initialisation_value_to_one
			if ind_starting_append>List_Explicit_Values.initialisation_value_to_one:
				m_dict[eval(a[List_Explicit_Values.val_first_element_of_list])].append(eval(j))
	
	#if file_name_read=="../../SMALL_DATA_2NDS/fi_id_link_id_sublinks.txt":
		#print(m_dict)
		#import sys
		#sys.exit()
	file.close()
	return m_dict

#*****************************************************************************************************************************************************************************************
#function reading a file and returning a dictionary of which the key=(i,j) where i,j= the value of the 1st and 2nd columne, that is the pahse id
# the value is a list [max queue size, phase saturation flow, que type]

def function_reading_file_containing_id_all_phases_andmax_queue_size_andsat_flow_andque_type(\
name_file_read=None,type=int,nb_comment_lines=-1):
	#we open the file to read
	file_rd=open(name_file_read,"r")
	
	dict={}
	ind=0
	for  i in file_rd.readlines():
		ind+=1
		if ind>nb_comment_lines:
			a=i.rsplit()		
		
			dict[(type(a[0]),type(a[1]))]=[eval(a[2]),eval(a[3]),eval(a[4])]
			
			#dict[(type(a[0]),type(a[1]))].append(type_1(a[j+2]))
			#dict[(type(a[0]),type(a[1]))].append(type_1(a[j+3]))
			#dict[(type(a[0]),type(a[1]))].append(type_1(a[j+4]))
			
			
			#print("dict[a[0]]",dict)
		
	file_rd.close()
	#print("DICT: ",dict)
	#import sys
	#sys.exit()

	return dict	
#*****************************************************************************************************************************************************************************************
#fct reading file "fi_duration_each_rp_mat.txt" with the duration of each routing prob of each phase
#it returns a dictionary, key=id phase, value=[...,duarion of the ith rout prob,..]
def fct_reading_file_fi_duration_each_rp_mat(name_file_read,nb_comment_lines):
	
	#print("name_file_read",name_file_read)
	#we open the file
	file=open(name_file_read,"r")
	
	di_rep={}
	ind=0
	for  i in file.readlines():
		ind+=1
		if ind>nb_comment_lines:
			a=i.rsplit()
			
			di_rep[eval(a[0])]=[]
			
			for j in a[1:]:
				di_rep[eval(a[0])].append(eval(j))
	return di_rep
				

#*****************************************************************************************************************************************************************************************
#fct reading file fi_id_prior_phase_id_min_phase
#it returns a dictionary, key=id of the minor phase,
#value= list with the prior phases related to the minor phase
#1st, 2nd column= id minor phase, columns 3-4 id prior phase
def fct_reading_file_fi_id_minor_phase_id_prior_phase(name_file_read,nb_comment_lines):

	#we open the file
	file=open(name_file_read,"r")
	
	
	di_key_id_minor_phase_value_li_id_prior_ph={}
	
	#indicator of the number of lines already read.
	ind=0
	ind_line_read=0
	
	for i in file.readlines():
		ind+=1
		if ind>nb_comment_lines:
			a=i.rsplit()
			
			id_1=eval(a[0])
			id_2=eval(a[1])
			id_minor_phase=(id_1,id_2)
			#print("id_nd",id_nd)
			#print(di_key_id_nd_value_dict, id_nd not in di_key_id_nd_value_dict)
			#If the minor phase id is not in the dictionary
			if id_minor_phase not in di_key_id_minor_phase_value_li_id_prior_ph:
				
				#if the prior phase is not in the dictionary
				
				di_key_id_minor_phase_value_li_id_prior_ph[id_1,id_2]=[[eval(a[2]),eval(a[3])]]
				
				#di_key_id_nd_value_dict.update(di_key_id_nd_value_dict_1)
				#print("HERE",di_key_id_nd_value_dict)	
			#if the minor phase is  in the dictionary
			else:
				di_key_id_minor_phase_value_li_id_prior_ph[id_1,id_2].append([eval(a[2]),eval(a[3])])
				
	
	file.close()
	
	return di_key_id_minor_phase_value_li_id_prior_ph

	

#****************************************************************************************************************************************************************
#function reading a file of which the first  lines are comments, and 
#this method returns a dictionary: key = id side phase, value =list [.., [id main phase],...]
def function_reading_fille_id_side_phase_id_main_phases(name_file_read,nb_comment_lines):

	#we open the file
	file=open(name_file_read,"r")
	
	li=[]
	
	#indicator of the number of lines already read.
	ind=0
	ind_line_read=0
	for i in file.readlines():
		ind+=1
		if ind>nb_comment_lines:
			li_line=[]
			#li_dur=[]
			a=i.rsplit()
			for j in a:
				li_line.append(eval(j))
			li.append(li_line)
	file.close()
	
	di={}	
	#li=[...,[ith line],...]
	for k in li[0:]:
		
		
		li_np=[]
		m_init=0
		m_fin=2
		
		
		di[k[0],k[1]]=[]
		a=int((len(k)-2)/2)
		
		m_init=2
		m_fin=4
		
		
		for m in range(a):
			di[k[0],k[1]].append(k[m_init:m_fin])
			#print(di)
			m_init=m_fin
			m_fin+=2
		#print(di)
		#import sys
		#sys.exit()
			
	
	return di
	

#*****************************************************************************************************************************************************************************************
#function reading file "fi_id_entry_intern_lk_id_dest_lk.txt", that is  the MRP
#it returns a dictionary, key=id entry_internal lk, value=[.., id dest lk,...]
def function_reading_id_entry_intern_lk_id_dest_lk(name_file_read,nb_comment_lines):

	#print("name_file_read",name_file_read)
	#we open the file
	file=open(name_file_read,"r")
	
	di={}
	
	#indicator of the number of lines already read
	ind_line_read=0
	for i in file.readlines():
		ind_line_read+=1
		if ind_line_read>nb_comment_lines:
			a=i.rsplit()
			b=int(eval(a[0]))
			di[(b)]=[]
			c=len(a)
			for j in a[1:c]:
				di[b].append(eval(j))
	return di
	file.close()

#*****************************************************************************************************************************************************************************************
#function reading fle fi_id_phase_val_cum_funct_rout_prop 
#it returns a dict, key=id entry_internal link, value, value =[ values cum fct ]
def function_reading_file_id_phase_val_cum_funct_rout_prop_1(name_file_read,nb_comment_lines):

	#we open the file
	file=open(name_file_read,"r")
	
	di={}
	
	#indicator of the number of lines already read
	ind_line_read=0
	for i in file.readlines():
		ind_line_read+=1
		if ind_line_read>nb_comment_lines:
			a=i.rsplit()
			b=int(eval(a[0]))
			di[b]=[]
			c=len(a)
			for j in a[1:c]:
				di[b].append(eval(j))
	file.close()
	return di
	
#*****************************************************************************************************************************************************************************************
#function reading file with the id of merging ques. The first column of this file is the current origin link, thta is link l if  phase (l,m), and the 
#next columns are the destination links, for ex m
#It returns a dictionary of which key= the orgin link l, value= [..., destination link,...]
def function_reading_file_merging_ques(name_file_read,nb_comment_lines):
	#we open the file
	file=open(name_file_read,"r")
	
	#indicator of the number of lines already read.
	ind=0
	
	#list,  ith elem is a list with the ith line of the file
	li=[]
	for i in file.readlines():
		ind+=1
		if ind>nb_comment_lines:
			li_line=[]
			a=i.rsplit()
			for j in a:
				#print("j=",j,"a=",a)
				li_line.append(eval(j))
			li.append(li_line)
	file.close()
	
	di={}
	for i in li:
		for j in i:
			di[i[:1][0]]=i[1:len(i)]
	return di
			
#*****************************************************************************************************************************************************************************************
#method reading file "val_name_file_mat_rp_id_phase_prob_dest_lk" with the  turn prob of each phase
def fct_read_file_rout_prob(name_file_read,nb_comment_lines):
	file=open(name_file_read,"r")
	
	di_rep={}
	
	ind=0
	for i in file.readlines():
		ind+=1
		if ind>nb_comment_lines:
			a=i.split()
			di_rep[eval(a[0]), eval(a[1])]=eval(a[2])
	file.close()
	return di_rep
	

#*****************************************************************************************************************************************************************************************
#method reading the file  "fi_mrp_cum.txt" with the cum prob values of each phase 
#it returns a dict, key=id entry-internal link, value=[...,[cum prob iths period, id related dest link],...]
def fct_reading_file_cum_rout_prob(name_file_read,nb_comment_lines):


	file=open(name_file_read,"r")
	
	di_rep={}
	di={}
	
	#indicator of the number of lines already read
	ind_line_read=0
	for i in file.readlines():
		ind_line_read+=1
		if ind_line_read>nb_comment_lines:
			a=i.rsplit()
			id_input_link=int(eval(a[0]))
			id_output_link=int(eval(a[1]))
			di[id_input_link,id_output_link]=[]
			c=len(a)
			for j in a[2:c]:
				di[id_input_link,id_output_link].append([eval(j),id_output_link])
	#print("di=",di)
	
	# phases with  meme input link
	v_li_keys=list(di.keys())
	di_entry_internal_with_at_least_two_outp_lks=fct_entry_intenal_links_having_at_least_two_output_links(li_liste=v_li_keys)
	#print()
	#print("di_entry_internal_with_at_least_two_outp_lks",di_entry_internal_with_at_least_two_outp_lks)
	#print()
	for m in di_entry_internal_with_at_least_two_outp_lks:
		#print("m=",m)
		#print()
		#di_rep[m]=[]
		li_valeurs_cum_prob=[]

		#print(di[di_entry_internal_with_at_least_two_outp_lks[m][0]])
		#print()	
		#for n in di_entry_internal_with_at_least_two_outp_lks[m][0]:
		#print("HEREdi[di_entry_internal_with_at_least_two_outp_lks[m]][0]",len(di[di_entry_internal_with_at_least_two_outp_lks[m][0]]))
		nb_variat_rout_prop_phase=len(di[di_entry_internal_with_at_least_two_outp_lks[m][0]])
		#print("nb_variat_rout_prop_phase",nb_variat_rout_prop_phase)
		#import sys
		#sys.exit()
		
		li_phases_lk=list(di_entry_internal_with_at_least_two_outp_lks[m])
		#print("li_phases_lk",li_phases_lk)
		
		li=[]
		for n in range(nb_variat_rout_prop_phase):
			for p in li_phases_lk:
				li.append(di[p][n])
			#li_valeurs_cum_prob.append(li)
			li_valeurs_cum_prob.extend(li)
			di_rep[m]=li_valeurs_cum_prob
			#print()
			#print(li_valeurs_cum_prob)
			#print()
			#print("di_rep",di_rep)
			li=[]
		
	
	#print()
	#print("AVANT v_li_keys",v_li_keys)
			
	#les phases qui ne varient pas
	for q in di_entry_internal_with_at_least_two_outp_lks:
		for r in di_entry_internal_with_at_least_two_outp_lks[q]:
			v_li_keys.remove(r)
	#print()
	#print("v_li_keys",v_li_keys)
	
	#print()
	#print("di=",di)
	for s in v_li_keys:
		#print("s=",s)
		#print("di[di_entry_internal_with_at_least_two_outp_lks[s]",di[s])
		#nb_variat_rout_prop_phase=len(di[s])
		#print("nb_variat_rout_prop_phase",nb_variat_rout_prop_phase)	
		#for 	
		di_rep[s[0]]=di[s]	
		#print()
	file.close()
		
	
	for i in di_rep:
		di_rep[i].sort()
	#print("HERE di_rep",di_rep)
	
	return di_rep
	
	

#*****************************************************************************************************************************************************************************************

#function reading a file of which the first  lines are comments, and 
#the order of the next lines indicate the order of the associated intersectio control matrices, 
#each line correspond to an intersection control matrix
#it returns a dictionary of which the key=intersection id, value= list of which the ith elem  is a possible intersection control matrix,
# value = [[1,2], [3,4] ], [[7,8],[9,10] ]],[1,2], [3,4]]=one possible intersection control matrix, [[7,8],[9,10]]=another possible inters control matrix


def function_reading_file_intersection_stages(path_and_name_file_read,nb_comment_lines):


	di={}
	
	#we open the file
	file=open(path_and_name_file_read,"r")
	
	li=[]
	
	#indicator of the number of lines already read
	ind=0
	ind_line_read=0
	for i in file.readlines():
		ind+=1
		if ind>nb_comment_lines:
			li_line=[]
			#li_dur=[]
			a=i.rsplit()
			for j in a:
				li_line.append(eval(j))
			li.append(li_line)
	file.close()
		
	#for each list indicating the movements to be acutated during period j
	#print("HERE",(li[1:]))
	
	#print(li)
		
	#for k in li[1:]:
	#ind_stage=1
	for k in li:
		#print("li",li,"k=",k)
		
		li_np=[]
		m_init=1
		m_fin=3
		#print("len(k)/2",int((len(k))/(2)),(len(k)-1)/2)
		for m in range(int((len(k)-1)/2)):
			#print("m=",m)
			#print("k=",k,"len(k)",len(k),"m_init",m_init,"m_fin",m_fin)
			li_mp=k[m_init:m_fin]
			#print("mouvem a joindre:",li_mp)
			
			m_init=m_fin
			m_fin=m_init+2
						
			li_np.append(li_mp)
			#print("li_np,",li_np)
		if k[0]  not in di:
			ind_stage=1
			di[k[0]]={}
			di[k[0]][ind_stage]=li_np
			ind_stage+=1
		else:
			d={}
			d[ind_stage]=li_np
			di[k[0]].update(d)
			ind_stage+=1
		
				
			
	#print(di)
	#import sys
	#sys.exit()
	return di
#*****************************************************************************************************************************************************************************************
#function reading the file of the compatible phases for each nsi
def fct_read_file_compatible_phases_nsi(name_file_read,nb_comment_lines):	

	di={}
	
	#we open the file
	file=open(name_file_read,"r")
	
	li=[]
	
	#indicator of the number of lines already read
	ind=0
	ind_line_read=0
	for i in file.readlines():
		ind+=1
		if ind>nb_comment_lines:
			li_line=[]
			#li_dur=[]
			a=i.rsplit()
			for j in a:
				li_line.append(eval(j))
			li.append(li_line)
	file.close()
		
	#for each list indicating the movements to be acutated during period j
	#print("HERE",(li[1:]))
	
	#print(li)
	
		
	#for k in li[1:]:
	#ind_stage=1
	for k in li:
		#print("li",li,"k=",k)
		
		li_np=[]
		m_init=1
		m_fin=3
		#print("len(k)/2",int((len(k))/(2)),(len(k)-1)/2)
		for m in range(int((len(k)-1)/2)):
			#print("m=",m)
			#print("k=",k,"len(k)",len(k),"m_init",m_init,"m_fin",m_fin)
			li_mp=k[m_init:m_fin]
			#print("mouvem a joindre:",li_mp)
			
			m_init=m_fin
			m_fin=m_init+2
						
			li_np.append(li_mp)
			#print("li_np,",li_np)
		
		if k[0]  not in di:
			ind_stage=1
			di[k[0]]={}
			di[k[0]][ind_stage]=li_np
			ind_stage+=1

			#di[k[0]]=[li_np]
			
		else:
			d={}
			d[ind_stage]=li_np
			di[k[0]].update(d)
			ind_stage+=1
			
			#di[k[0]].append(li_np)
			
		#print(di)
	#import sys
	#sys.exit()		
			
	#print(di)
	#import sys
	#sys.exit()
	return di
#*****************************************************************************************************************************************************************************************
#function reading file with the node id and the type and category of the employed control
#it returns a  list [dict1, dict2]
#dict1, key=id node, value=[type control, with/out sensor, 1/0 wit/out turn ratios estim]
#dict2, key=id node with estim turn ratios, value=1
def fct_reading_fi_id_node_type_control(val_name_file_to_read,nb_comment_lines):
	#we open the file
	file=open(val_name_file_to_read,"r",encoding="utf8")
	di_rep={}
	
	di_rep_with_turn_ratios_estim={}
	
	ind=0
	for i in file.readlines():
		ind+=1
		if ind>nb_comment_lines:
			a=i.rsplit()
			id_nd=eval(a[0])
			b=eval(a[3])
			di_rep[id_nd]=[eval(a[1]),str(a[2]),b]
			
			if b==1:
				di_rep_with_turn_ratios_estim[id_nd]=b
			
	return [di_rep,di_rep_with_turn_ratios_estim]

#*****************************************************************************************************************************************************************************************
#function reading file with the parameters of FT control. It returns a dictionary: key = id node, 
#value=[..., [id stage to actuate at step i, actuation duration, cycle duration],...]
def fct_reading_file_parameters_FT_control(name_file_to_read,nb_comment_lines):

	#we open the file
	file=open(name_file_to_read,"r")
	
	di_rep={}
	
	ind=0
	for i in file.readlines():
		ind+=1
		if ind>nb_comment_lines:
			#a= id node, id stage, actuation duration, actuation duration of the red clear ctrl, cycle duration)
			a=i.rsplit()
			#if the node id is not in the dictionary
			id_nd=eval(a[0])
			
			if id_nd not in di_rep:
				di_rep[id_nd]=[ [eval(a[1]),eval(a[2]),eval(a[3])]]
			
			#if the node id is  in the dictionary
			else:
				di_rep[id_nd].append( [eval(a[1]),eval(a[2]),eval(a[3])])
	
				
	return di_rep
		


#*****************************************************************************************************************************************************************************************

#function reading file with the parameters of FT control. It returns a list=[[valeurs decal pour chaque nd],dictionary: key = id node, 
#value=[..., [id stage to actuate at step i, actuation duration, actuattion duration of the rec cloearance, cycle duration],...]
def fct_reading_file_parameters_FT_control_offset_1(name_file_to_read,nb_comment_lines,v_nb_line_master_nd_info,v_nb_line_t_start_ctrl_info):

	#we open the file
	file=open(name_file_to_read,"r")
	
	li_mast_nd_info=[]
	di_rep={}
	t_start_control=None
	ind=0
	for i in file.readlines():
		ind+=1
		#print("ind",ind,"v_nb_line_t_start_ctrl_info",v_nb_line_t_start_ctrl_info,ind==v_nb_line_t_start_ctrl_info,"v_nb_line_master_nd_info",v_nb_line_master_nd_info)
		#lecture de la ligne t start control
		if ind==v_nb_line_t_start_ctrl_info:
			a=i.rsplit()
			t_start_control=eval(a[0])
		
			
		#si on lit la seconde ligne apres les commentaires
		if ind==v_nb_line_master_nd_info:
			a=i.rsplit()
			#print("HERE",eval(a[1]),a)
			for j in a:
				li_mast_nd_info.append(eval(j))
					
				#li_mast_nd_info=[eval(a[0]),eval(a[1])]
		elif ind>nb_comment_lines+2:
			#a= id node, id stage, actuation duration, actuation duration of the red clear ctrl, cycle duration)
			a=i.rsplit()
			#if the node id is not in the dictionary
			id_nd=eval(a[0])
			if id_nd not in di_rep:
				di_rep[id_nd]=[ [eval(a[1]),eval(a[2]),eval(a[3])]]
			
			#if the node id is  in the dictionary
			else:
				di_rep[id_nd].append( [eval(a[1]),eval(a[2]),eval(a[3])])
					
	li_rep=[li_mast_nd_info,di_rep,t_start_control]
				
	return li_rep
#*****************************************************************************************************************************************************************************************
#function reading file with the parameters of FT control with offsets. 
#it returns [li_valeurs_decalage chaque nd,di_param_FT]
#nb_comment_lines=1, v_nb_line_id_master_nd=2,v_nb_line_val_dec=3
def fct_reading_file_parameters_FT_control_offset_2(name_file_to_read,nb_comment_lines_ft_offs):

	#we open the file
	file=open(name_file_to_read,"r")
	
	#the id of the master node, since we may have more than one nodes having 0 time of decalage
	#id_master_nd=None
	
	#the list withthe decalage param
	li_val_dec=[]
	

	
	#dict, key=id node, value=[id stage, act duration, cycle duration]
	di_rep={}
	
	#v_nb_line_id_master_nd=nb_comment_lines+1
	
	v_nb_line_val_dec=nb_comment_lines_ft_offs+2
	#nb_line_param_FT=v_nb_line_val_dec+1
	
	ind=0
	for i in file.readlines():
		ind+=1
	
					
		#si on lit la premiere ligne apres les commentaires, c'est le id du master nd
		#if ind==v_nb_line_id_master_nd:
			#a=i.rsplit()
			#id_master_nd=eval(a[0])
			
			#for j in a:
				#li_mast_nd_info.append(eval(j))
					
				#li_mast_nd_info=[eval(a[0]),eval(a[1])]
		
		
		#lecture de la ligne avec les valeurs  de dec pour chaque nd
		if ind==v_nb_line_val_dec:
		
			a=i.rsplit()
			
			for j in a:
				
				li_val_dec.append(eval(j))
	
		elif ind>v_nb_line_val_dec:
			#a= id node, id stage, actuation duration, actuation duration of the red clear ctrl, cycle duration)
			a=i.rsplit()
			#if the node id is not in the dictionary
			id_nd=eval(a[0])
			if id_nd not in di_rep:
				di_rep[id_nd]=[ [eval(a[1]),eval(a[2]),eval(a[3])]]
			
			#if the node id is  in the dictionary
			else:
				di_rep[id_nd].append( [eval(a[1]),eval(a[2]),eval(a[3])])
					
	#li_rep=[li_mast_nd_info,di_rep,t_start_control]
	
	li_rep=[li_val_dec,di_rep]	
	#print("li_rep",li_rep)
	#import sys
	#sys.exit()		
	return li_rep
#*****************************************************************************************************************************************************************************************

#function reading file with the parameters of FT control with offsets. 
#it returns [li_valeurs_decalage chaque nd,di_param_FT]
#nb_comment_lines=1, v_nb_line_id_master_nd=2,v_nb_line_val_dec=3
def fct_reading_file_parameters_FT_control_offset(name_file_to_read,nb_comment_lines_ft_offs):

	#we open the file
	file=open(name_file_to_read,"r")
	
	
	
	#the list withthe decalage param
	#li_val_dec=[]
	
	#the list withthe decalage param,key=id nd, value= decalage
	di_val_dec={}
	

	
	#dict, key=id node, value=[id stage, act duration, cycle duration]
	di_rep={}
	
	#v_nb_line_id_master_nd=nb_comment_lines+1
	
	v_nb_line_val_dec=nb_comment_lines_ft_offs+2
	#nb_line_param_FT=v_nb_line_val_dec+1
	
	ind=0
	for i in file.readlines():
		ind+=1
	
					
		#si on lit la premiere ligne apres les commentaires, c'est le id du master nd
		#if ind==v_nb_line_id_master_nd:
			#a=i.rsplit()
			#id_master_nd=eval(a[0])
			
			#for j in a:
				#li_mast_nd_info.append(eval(j))
					
				#li_mast_nd_info=[eval(a[0]),eval(a[1])]
		
		
		#lecture de la ligne avec les valeurs  de dec pour chaque nd
		if ind==v_nb_line_val_dec:
		
			a=i.rsplit()
			
			v_init=0
			v_pas=2
			v_fin=v_init+1
			nb_fois=int(len(a)/2)
			for i in range(nb_fois):	
				di_val_dec[eval(a[v_init])]=eval(a[v_fin])
				v_init=v_fin+1
				v_fin=v_init+1
				
	
		elif ind>v_nb_line_val_dec:
			#a= id node, id stage, actuation duration, actuation duration of the red clear ctrl, cycle duration)
			a=i.rsplit()
			#if the node id is not in the dictionary
			id_nd=eval(a[0])
			if id_nd not in di_rep:
				di_rep[id_nd]=[ [eval(a[1]),eval(a[2]),eval(a[3])]]
			
			#if the node id is  in the dictionary
			else:
				di_rep[id_nd].append( [eval(a[1]),eval(a[2]),eval(a[3])])
					
	#li_rep=[li_mast_nd_info,di_rep,t_start_control]
	
	li_rep=[di_val_dec,di_rep]	
	#print("DS CL_GLOBAL_FCT_NET, FCT fct_reading_file_parameters_FT_control_offset, li_rep",li_rep)
	#import sys
	#sys.exit()		
	return li_rep
#*****************************************************************************************************************************************************************************************
#fct reading file paameters MP control and returns dict, key=id node, 
#value=[ ..., [mp icm actuation duration, red clear duration],..., cycle duration]
def fct_reading_file_parameters_MP_control(name_file_to_read,nb_comment_lines):

	#we open the file
	file=open(name_file_to_read,"r")
	
	di_rep={}
	
	ind=0
	for i in file.readlines():
		ind+=1
		if ind>nb_comment_lines:
			#a= id node, actuation duration, actuation duration of the red clear ctrl, cycle duration)
			a=i.rsplit()
			#print("a=",a)
			#if the node id is not in the dictionary
			id_nd=eval(a[0])
			
			if id_nd not in di_rep:
				#di_rep[id_nd]=[eval(a[1]),eval(a[2]),eval(a[3])]
				#di_rep[id_nd]=[]
				ind_init=1
				pas=2
				ind_fin=ind_init+pas
				long=int((len(a[1:])-1)/2)
				#print("long",long,"ind_init",ind_init)
				
				li_1=[]
				for k in range(long):
					li=[]
					for j in a[ind_init:ind_fin]:
						#print("j=",j)
						li.append(eval(j))
						#print("li",li)
						#print()
					li_1.append(li)
					#print("li_1",li_1)
					#di_rep[id_nd].append(li)
					ind_init=ind_fin
					ind_fin+=pas
					#print("ind_init",ind_init)
				#li_1.append(eval(a[ind_init]))	
				#li_1.append(-1)
				#print("eval(a[ind_init])",eval(a[ind_init]))
				li_2=[li_1,eval(a[ind_init]),len(li_1),-1]
				di_rep[id_nd]=li_2

			#if the node id is  in the dictionary
			else:
				print("PROBLEM IN GLOB FCT NETWORK, fct_reading_file_parameters_MP_control, ID NODE ", id_nd,\
				"ALREADY IN DICT " , list(di_rep.keys()))
				import sys
				sys.exit()
				#di_rep[id_nd].append( [eval(a[1]),eval(a[2]),eval(a[3])])
	#print(di_rep)
	#import sys
	#sys.exit()			
	return di_rep
		
#*****************************************************************************************************************************************************************************************
#method creating a dictionary with  Qvalues equal to one, for the MP control when a not Q-weight version will be employed:#it returns a dict,  key:phase id, value=dict, key=phase id, value=1
#di_inter=dict, key=id inters, value=inters
def fct_creat_Qvalues_for_weighted_MP_equal_one(di_inter,di_id_link_val_link):
	
	di_rep={}
		
	for i in di_inter:
		di_rep[i]={}
		di={}
		for j in di_inter[i].get_li_id_input_network_links_to_inters_node():
			for m in di_inter[i].get_li_id_input_network_links_to_inters_node()[j].get_set_veh_queue().get_di_obj_veh_queue_at_link():
				di[m]=1
		di_rep[i].update(di)
					
	return di_rep
	
#*****************************************************************************************************************************************************************************************	
#metho creating the dict with the Qvalues for the MP algo
#it returns a dictionary, key=node id, value= dict, key=que id, value=Q valeur
def fct_creat_dict_Qvalues_for_MP_ctrl_1(val_name_file_to_read,val_number_lines_to_read):

	di_rep={}
		
	#each file of this line is id node (1st colm), id phase (2-3 colm) value (4th colm)
	file=open(val_name_file_to_read,"r")
		
	ind=0
	for i in file.readlines():
		ind+=1
		if ind>val_number_lines_to_read:
			a=i.rsplit()
			#if the ndoe id is not in the dict
			nd_id=eval(a[0])
			if nd_id not in di_rep:
				di_rep[nd_id]={}
				di={}
				di[eval(a[1]),eval(a[2])]=eval(a[3])
				di_rep[nd_id].update(di)
				
			#if the node id is in the dict
			else:
				di={}
				di[eval(a[1]),eval(a[2])]=eval(a[3])
				di_rep[nd_id].update(di)
				
	
	return di_rep
		


#*****************************************************************************************************************************************************************************************
#method creating the dict with the Qvalues for the MP algo
#it returns a dictionary,dict, key=que id, value=Q valeur
def fct_creat_dict_Qvalues_for_MP_ctrl(val_name_file_to_read,val_number_lines_to_read):

	di_rep={}
		
	#each file of this line is id node (1st colm), id phase (2-3 colm) value (4th colm)
	file=open(val_name_file_to_read,"r")
		
	ind=0
	for i in file.readlines():
		ind+=1
		if ind>val_number_lines_to_read:
			a=i.rsplit()
			#if the ndoe id is not in the dict
			
			di_rep[eval(a[0]),eval(a[1])]=eval(a[2])
			
				
	
	return di_rep
		
#*****************************************************************************************************************************************************************************************
#method reading the parameters of MP Pract control
def fct_reading_file_MP_Pract_control(name_file_to_read,nb_comment_lines):

	file=open(name_file_to_read,"r")
	di_rep={}
	
	ind=0
	for i in file.readlines():
		ind+=1
		if ind>nb_comment_lines:
			#a=id node, type node
			a=i.rsplit()
			di_rep[eval(a[0])]=[eval(a[1]),eval(a[2]),eval(a[3])]
			#for j in a[1:]:
				#di_rep
	file.close()
	return di_rep

#*****************************************************************************************************************************************************************************************
#method reading the parameters of MP without red clear control
def fct_reading_file_MP_without_rc_control(name_file_to_read,nb_comment_lines):

	file=open(name_file_to_read,"r")
	di_rep={}
	
	ind=0
	for i in file.readlines():
		ind+=1
		if ind>nb_comment_lines:
			#a=id node, type node
			a=i.rsplit()
			di_rep[eval(a[0])]=[eval(a[1])]
			#for j in a[1:]:
				#di_rep
	file.close()
	return di_rep

#*****************************************************************************************************************************************************************************************
#method reading the parameters of MP without red clear control
def fct_reading_file_MP_pract_without_rc_control(name_file_to_read,nb_comment_lines):

	file=open(name_file_to_read,"r")
	di_rep={}
	
	ind=0
	for i in file.readlines():
		ind+=1
		if ind>nb_comment_lines:
			#a=id node, type node
			a=i.rsplit()
			di_rep[eval(a[0])]=[eval(a[1]),eval(a[2])]
			#for j in a[1:]:
				#di_rep
	file.close()
	return di_rep

#*****************************************************************************************************************************************************************************************
#fct reading the param of pressure stage duration cotnrol
#it returns a dict, key=i node, value=[cycle duration, red clear duration]
def fct_reading_file_psd_control(name_file_to_read,nb_comment_lines):

	file=open(name_file_to_read,"r")
	di_rep={}
	
	ind=0
	for i in file.readlines():
		ind+=1
		if ind>nb_comment_lines:
			#a=id node, type node
			a=i.rsplit()
			#b=eval(a[1])
			di_rep[eval(a[0])]=[eval(a[1]),eval(a[2])]
	return di_rep
	
#*****************************************************************************************************************************************************************************************
#fcr reading the parametrs of a fully actuted cotnrol
#we return di, key=id  node, value=[min value of allowed flow, idle time, t first control]
def fct_reading_file_fa_control_with_red_clear(name_file_to_read,nb_comment_lines):
	file=open(name_file_to_read,"r")
	di_rep={}
	
	ind=0
	for i in file.readlines():
		ind+=1
		if ind>nb_comment_lines:
			#a=id node, type node
			a=i.rsplit()
			#b=eval(a[1])
			di_rep[eval(a[0])]=[eval(a[1]),eval(a[2]),eval(a[3])]
	return di_rep
#*****************************************************************************************************************************************************************************************
#fcr reading the parametrs of a fully actuted cotnrol
#we return di, key=id  node, value=[min value of allowed flow, t first control]
def fct_reading_file_fa_control_no_rec_clear(name_file_to_read,nb_comment_lines):
	file=open(name_file_to_read,"r")
	di_rep={}
	
	ind=0
	for i in file.readlines():
		ind+=1
		if ind>nb_comment_lines:
			#a=id node, type node
			a=i.rsplit()
			#b=eval(a[1])
			di_rep[eval(a[0])]=[eval(a[1]),eval(a[2])]
	return di_rep
#*****************************************************************************************************************************************************************************************
#fcr reading the parametrs of a fully actuted cotnrol
#we return di, key=id  node, value=[min value of allowed flow,idle time, t first control,max green duration]
def fct_reading_file_fa_control_max_green(name_file_to_read,nb_comment_lines):
	file=open(name_file_to_read,"r")
	di_rep={}
	
	ind=0
	for i in file.readlines():
		ind+=1
		if ind>nb_comment_lines:
			#a=id node, type node
			a=i.rsplit()
			#b=eval(a[1])
			di_rep[eval(a[0])]=[eval(a[1]),eval(a[2]),eval(a[3]),eval(a[4])]
	return di_rep
#*****************************************************************************************************************************************************************************************
#fcr reading the parametrs of a fully actuted cotnrol
#we return di, key=id  node, value=[min value of allowed flow, idle time, t first control,max green duration]
def fct_reading_file_fa_control_max_green_with_red_clear(name_file_to_read,nb_comment_lines):
	file=open(name_file_to_read,"r")
	di_rep={}
	
	ind=0
	for i in file.readlines():
		ind+=1
		if ind>nb_comment_lines:
			#a=id node, type node
			a=i.rsplit()
			#b=eval(a[1])
			di_rep[eval(a[0])]=[eval(a[1]),eval(a[2]),eval(a[3]),eval(a[4])]
	return di_rep
#*****************************************************************************************************************************************************************************************
#fct read file fi_id_intersection_node_type_inters.txt	
def fct_read_fi_id_intersection_node_type_inters(name_file_to_read,nb_comment_lines):
	#we open the file
	file=open(name_file_to_read,"r")
	di_sign_ints={}
	di_non_sign_ints={}
	
	ind=0
	for i in file.readlines():
		ind+=1
		if ind>nb_comment_lines:
			#a=id node, type node
			a=i.rsplit()
			b=eval(a[1])
			if b==1:
				di_sign_ints[eval(a[0])]=b
			else:
				di_non_sign_ints[eval(a[0])]=b
	#di_sign_ints=dict, key =id sign inters, value=1
	#di_non_sign_ints=dict, key =id non sign inters, value=1		
	li_di=[di_sign_ints,di_non_sign_ints]		
	return li_di
#*****************************************************************************************************************************************************************************************
#fct read file fi_id_entry_link_type_lk
def fct_read_fi_id_entry_link_type_lk(name_file_to_read,nb_comment_lines):

	#we open the file
	file=open(name_file_to_read,"r")
	
	di={}
	ind=0
	
	for i in file.readlines():
		ind+=1
		if ind>nb_comment_lines:
			a=i.rsplit()
			
			di[eval(a[0])]=eval(a[1])
	return di

#*****************************************************************************************************************************************************************************************
#function reading  file fi_id_all_phases_init_fin_detect_posit_nb_posit_captured
#it returns a dict, key=id phase, value= dict, key=id sensor, value=[init position sensor, final posit sensor, nb positions captured by sensor], or -1, or n>0,
def fct_read_fi_id_all_phases_init_fin_detect_posit_nb_posit_captured_1(name_file_to_read,nb_comment_lines):

	file=open(name_file_to_read,"r")
	#list_valeurs=
	#[....,[id input link phase, id output link phase, id sensor, init posit captured by detector, final position captured by detector, nb positions captured (final-initit position+1)],.....]
	#each line of the  file will be:
	#input lk, output lk of the phase,id sensor, initial position captured by detector, final position, nb posit capured by the capteur,
	#or
	#input lk, output lk of the phase,id sensor, -1 if the capteur captures the entire queue size
	#or
	#input lk, output lk of the phase, id sensor, n>0 if the capteur covers the entire queue starting from the nth position
	
	di_rep={}
	ind=0
	for i in file.readlines():
		
		ind+=1
		if ind>nb_comment_lines:
			
			a=i.rsplit()
			id_phase=(eval(a[0]),eval(a[1]))
			
			#if the phase is not in the dictionary
			if id_phase not in di_rep:
				
				di_1={}
				di_1[id_phase]=[]
				di_2={}
				di_2[eval(a[2])]=[]
				for j in a[3:]:
					di_2[eval(a[2])].append(eval(j))
				di_1[id_phase].append(di_2)
				di_rep.update(di_1)
			#if the phase is in the dictionary
			else:
				di_2={}
				di_2[eval(a[2])]=[]
				for j in a[3:]:
					di_2[eval(a[2])].append(eval(j))
				
				di_rep[id_phase][0].update(di_2)
		
	file.close()
	return di_rep
#*****************************************************************************************************************************************************************************************
#function reading  file fi_id_all_phases_init_fin_detect_posit_nb_posit_captured
#it returns a dict, key=id phase, value= dict, key=id sensor, value=[init position sensor, final posit sensor, nb positions captured by sensor], or -1, or n>0,
def fct_read_fi_id_all_phases_init_fin_detect_posit_nb_posit_captured(name_file_to_read,nb_comment_lines):

	file=open(name_file_to_read,"r")
	#list_valeurs=
	#[....,[id input link phase, id output link phase, id sensor, init posit captured by detector, final position captured by detector, nb positions captured (final-initit position+1)],.....]
	#each line of the  file will be:
	#input lk, output lk of the phase,id sensor, initial position captured by detector, final position, nb posit capured by the capteur,
	#or
	#input lk, output lk of the phase,id sensor, -1 if the capteur captures the entire queue size
	#or
	#input lk, output lk of the phase, id sensor, n>0 if the capteur covers the entire queue starting from the nth position
	
	di_rep={}
	ind=0
	for i in file.readlines():
		
		ind+=1
		if ind>nb_comment_lines:
			
			a=i.rsplit()
			id_phase=(eval(a[0]),eval(a[1]))
			
			#if the phase is not in the dictionary
			if id_phase not in di_rep:
				
				di_1={}
				di_1[eval(a[2])]=[]
				for j in a[3:]:
					di_1[eval(a[2])].append(eval(j))
				di_rep[id_phase]=di_1
			#if the phase is in the dictionary
			else:
				di_1={}
				di_1[eval(a[2])]=[]
				for j in a[3:]:
					di_1[eval(a[2])].append(eval(j))
				
				di_rep[id_phase].update(di_1)
		
	file.close()
	return di_rep
#*****************************************************************************************************************************************************************************************
#method reading file fi_id_node_estim_turn_ratio_param_dur_turn_ratios
#it returns a dict, key=id node, value=[param convex combin turn ratio values, duration turn ratio values]
def fct_read_fi_id_node_estim_turn_ratio_param_dur_turn_ratios(name_file_to_read,nb_comment_lines):

	di_rep={}
	file=open(name_file_to_read,"r")
	
	ind=0
	for i in file.readlines():
		ind+=1
		if ind>nb_comment_lines:
			a=i.rsplit()
			di_rep[eval(a[0])]=[eval(a[1]),eval(a[2])]
			
	file.close()
	return di_rep
#*****************************************************************************************************************************************************************************************
#method reading file fi_init_state_que.txt
#it returns a dict, key=id node, value=dict, key=id phase, value= [nb veh, id veh final dest]
def fct_read_file_fi_init_state_que(name_file_to_read,nb_comment_lines):

	di_rep={}
	file=open(name_file_to_read,"r")
	
	ind=0
	for i in file.readlines():
		ind+=1
		if ind>nb_comment_lines:
			a=i.rsplit()
			id_nd=eval(a[0])
			#if the nd id is in the dict
			if id_nd in di_rep:
				di={}
				di[eval(a[1]),eval(a[2])]=[eval(a[3])]
				li=[]
				for j in a[4:]:
					
					li.append(eval(j))
					di[eval(a[1]),eval(a[2])].append(li)
					
				di_rep[id_nd].update(di)
		
			#if the nd is not in the dict
			else:
				di_rep[id_nd]={}
				di={}
				di[eval(a[1]),eval(a[2])]=[eval(a[3])]
				li=[]
				for j in a[4:]:
					
					li.append(eval(j))
					di[eval(a[1]),eval(a[2])].append(li)
				di_rep[id_nd].update(di)
				
	return di_rep

#*****************************************************************************************************************************************************************************************
#method reading filefi_phase_interference.txt
#it returns a dict, key=id node, value=dict, key=id phase, value= [id  affecting phase, param]
def fct_read_file_fi_init_state_que(name_file_to_read,nb_comment_lines):

	di_rep={}
	file=open(name_file_to_read,"r")
	
	ind=0
	for i in file.readlines():
		ind+=1
		if ind>nb_comment_lines:
			a=i.rsplit()
			id_nd=eval(a[0])
			#if the nd id is in the dict
			if id_nd in di_rep:
			
				#if the phase id is in the dictionary
				if (eval(a[1]),eval(a[2])) in di_rep[id_nd]:
					di_rep[id_nd][eval(a[1]),eval(a[2])].append([eval(a[3]),eval(a[4]),eval(a[5])])
				
				#if the phase is not in the dict
				else:
					di={}
					di[eval(a[1]),eval(a[2])]=[[eval(a[3]),eval(a[4]),eval(a[5])]]
					
					di_rep[id_nd].update(di)
		
			#if the nd is not in the dict
			else:
				di_rep[id_nd]={}
				di={}
				di[eval(a[1]),eval(a[2])]=[[eval(a[3]),eval(a[4]),eval(a[5])]]
				di_rep[id_nd].update(di)
				
	return di_rep

#*****************************************************************************************************************************************************************************************
#fct reading  file fi_rout_type_entry_lk_mixed_manag.txt
#it returns a dict, key=id entry link, value= type of routing managem
def fct_read_file_fi_rout_type_entry_lk_mixed_manag(name_file_to_read,nb_comment_lines):

	di_rep={}
	file=open(name_file_to_read,"r")
	
	ind=0
	for i in file.readlines():
		ind+=1
		if ind>nb_comment_lines:
			a=i.rsplit()
			di_rep[eval(a[0])]=eval(a[1])
	return di_rep


#*****************************************************************************************************************************************************************************************
#method returning a dictionary, key=id link, value=dict, key=id phase associated with link, 
#value=-1 if sensor captures the entire que, or
#value=n>0 if sensor captures the whole que from the nth position (1st position indicated by zero) or
#value=[id initial posit cpatures by sensor, id final position captured by sensor, nb positions captrured by sensor]
def fct_creat_dict_sensor_information_per_link(val_dict_sensor_inform_per_phase):

	di_rep={}
	
	#val_dict_sensor_insorm_per_phase=dict, key=id phase,
	#value=-1 if sensor captures the entire que, or
	#value=n>0 if sensor captures the whole que from the nth position (1st position indicated by zero) or
	#value=[id initial posit cpatures by sensor, id final position captured by sensor, nb positions captrured by sensor]
	
	#for chaque phase id (id input lk, id output lk)
	for i in val_dict_sensor_inform_per_phase:
		#if the input lk is not in the dict
		if i[0] not in di_rep:
			di_rep[i[0]]={}
			di_rep[i[0]][i]=(val_dict_sensor_inform_per_phase[i])
			#if i[0]==708:
				#print("hr")
				#print(di_rep)
				#print("here1",val_dict_sensor_inform_per_phase)
				
			
		
		#if the input lk is in the dictionary
		else:
			#if i[0]==708:
				#print(di_rep[i[0]])
			di_rep[i[0]][i]=(val_dict_sensor_inform_per_phase[i])
			#if i[0]==708:
				#print(di_rep[i[0]])
			
	return di_rep
#*****************************************************************************************************************************************************************************************
#method returning a dictionary, key=id link, value=dict, key=id phase associated with link, 
#value=-1 if sensor captures the entire que, or
#value=n>0 if sensor captures the whole que from the nth position (1st position indicated by zero) or
#value=[id initial posit cpatures by sensor, id final position captured by sensor, nb positions captrured by sensor]
def fct_creation_dict_sensor_information_per_link(val_name_file_to_read,val_nb_comment_lines):
	
	#dict_sensor_insorm_per_phase=dict, key=id phase,
	#value=-1 if sensor captures the entire que, or
	#value=n>0 if sensor captures the whole que from the nth position (1st position indicated by zero) or
	#value=[id initial posit cpatures by sensor, id final position captured by sensor, nb positions captrured by sensor]
	dict_sensor_inform_per_phase=fct_read_fi_id_all_phases_init_fin_detect_posit_nb_posit_captured(\
	name_file_to_read=val_name_file_to_read,nb_comment_lines=val_nb_comment_lines)
	
	#print(dict_sensor_inform_per_phase)
	
	di_rep=fct_creat_dict_sensor_information_per_link(val_dict_sensor_inform_per_phase=dict_sensor_inform_per_phase)		
		
	return di_rep


#*****************************************************************************************************************************************************************************************
#fct reading file "fi_mrp.txt", ti returns a dictionary
#key=id node,  dict, key=id phase value=rout prop at ith period
def fct_reading_file_fi_mrp(name_file_to_read,nb_comment_lines,va_netw):

	#we open the file
	file=open(name_file_to_read,"r")
	
	#di=dict, key=id phase, value=[...,rout prop at ith period, ...]
	di={}
	ind=0
	
	for i in file.readlines():
		ind+=1
		if ind>nb_comment_lines:
			a=i.rsplit()
			
			di[eval(a[0]),round(eval(a[1]))]=[]
		
			
			le=len(a)
			for j in a[2:le]:
			
				di[eval(a[0]),round(eval(a[1]))].append(eval(j))
				
	di_rep=fct_creat_di_id_node_value_di_rout_prob(di_key_id_phase_val_li_rout_prob=di,val_netw=va_netw)
	file.close()
	return di_rep
				
#*****************************************************************************************************************************************************************************************
#method reading the file with the demand parameters when the demand intensity varies within the simulation
#it returns a dictionary, key=id arc, value=[...[valeur lambda, time to start],...]
def fct_reading_file_fi_demand_param_variation(name_file_to_read,nb_comment_lines):

		#we open the file
		file=open(name_file_to_read,"r")
		
		#dict: key=id arc, value=[...[valeur lambda, time to start],...]
		di_rep={}
		
		ind=0
		#each line of the file is: 1st column=link id, 2nd column= valeur lambda, 3rd column=t start, next columns= sequence of columns 2 and 3
		for i in file.readlines():
			ind+=1
			if ind>nb_comment_lines:
				a=i.rsplit()
				di_rep[eval(a[0])]=[]
				b=int((len(a)-1)/2)
				c=1
				pas=2
				for j in range(b):
					d=c+pas
					e=a[c:d]
					di_rep[eval(a[0])].append([eval(e[0]),eval(e[1])])
					c=c+pas
		file.close()
		return di_rep
				
#*****************************************************************************************************************************************************************************************
#function reading file fi_id_all_network_link_id_orig_dest_node_length_link_capacity_link_param_travel_duration.txt and extracting the mean travel time
def fct_write_fi_id_link_mean_travel_time(name_file_to_read,name_file_to_write_1,name_file_to_write_2,nb_comment_lines):

	#we open the file
	file=open(name_file_to_read,"r")
	file1=open(name_file_to_write_1,"w")
	file2=open(name_file_to_write_2,"w")
	
	ind=0
	di_rep={}
	
	for i in file.readlines():
		ind+=1
		if ind>nb_comment_lines:
			a=i.rsplit()
			di_rep[eval(a[0])]=eval(a[len(a)-1])

	for i in di_rep:
			file1.write("%d\t %.2f\t \n"%(i, di_rep[i]))
			file2.write("%.2f\t "%(di_rep[i]))
	
	
	file.close()
	file1.close()
	file2.close()
	

#*****************************************************************************************************************************************************************************************
#methode qui retourne un dict, key=id noeud, valeur=di, cle=id phase, valeur=rout prob periode i
def fct_creat_di_id_node_value_di_rout_prob(di_key_id_phase_val_li_rout_prob,val_netw):
	di_rep={}
	#print("di_key_id_phase_val_li_rout_prob",di_key_id_phase_val_li_rout_prob[i[0],i[1]])
	for i in di_key_id_phase_val_li_rout_prob:
		
		#on recupere le noeud de l'input link de la phase
		#si le noeud n'est pas dans la dict
		if val_netw.get_di_entry_internal_links()[i[0]].get_id_head_intersection_node() not in di_rep:
		
			di_rep[val_netw.get_di_entry_internal_links()[i[0]].get_id_head_intersection_node()]={}
			
			di_rep[val_netw.get_di_entry_internal_links()[i[0]].get_id_head_intersection_node()]\
			[i[0],i[1]]=di_key_id_phase_val_li_rout_prob[i[0],i[1]][0]
			
			
		
		#si le noeud est  dans la dict
		else:
			di_rep[val_netw.get_di_entry_internal_links()[i[0]].get_id_head_intersection_node()]\
			[i[0],i[1]]=di_key_id_phase_val_li_rout_prob[i[0],i[1]][0]
	return di_rep

#*****************************************************************************************************************************************************************************************
#fct reading the file with the series of the cum rout prob when varying rout prob
#it returns a [dict_1,dict_2]
#dict_1, key=node id, value=dict, key=id period valeur= dict, key=id phase, valeur= rp for the corresponding period
#dict_2, key=node id, value=dict, key=id period valeur:duration previous values rp
def fct_read_file_fi_series_cum_val_varying_rp(name_file_to_read,nb_comment_lines):

	#we open the file
	file=open(name_file_to_read,"r")
	
	ind=0
	
	#di_rep={}
	
	#di_rep_1=dict, key=id node, valeur=dict, key=id period valeur= dict, key=id phase, valeur= rp for the corresponding period
	di_rep_1={}
	
	#di_rep_2=dict, key=id node, valeur=dict, key=id period: valeur=duree rp previous period
	di_rep_2={}
	
	for i in file.readlines():
		ind+=1
		if ind>nb_comment_lines:
		
			#a= id node, id input link, id output link, duration of the previous values of the rout prob, rout prob next period, ...., )
			a=i.rsplit()
			
			id_nd=eval(a[0])
			#if id_nd==37612:
				#print("id node", id_nd)
				#print()
				#if eval(a[1])==737:
					#print("phase",eval(a[1]),eval(a[2]))
					#print()
					
			#le=int((len(a[1:])-1)/2)
			le=int((len(a[3:]))/2)
			#print("le",le)
			indice=3
			pas=0
			#if the node id is not in the dictionary
			if id_nd not in di_rep_1:
				#if id_nd==37612:
					#if eval(a[1])==737:
						#print("here3")
						
			
				di_rep_1[id_nd]={}
				
				di_rep_2[id_nd]={}
				
				#di=dict, key=id phase, val=rp, 
				di={}
				
				for j in range(le):
					duree=eval(a[indice+pas])
					di[eval(a[1]),eval(a[2])]=eval(a[indice+pas+1])
					
					di_rep_1[id_nd][j+1]={}
					di_rep_1[id_nd][j+1].update(di)
					#if id_nd==37612:
						#if eval(a[1])==737:
							#print("here1")
							#print(di_rep_1[id_nd][j+1])
							#print()
					
							
					
					di_rep_2[id_nd][j+1]=duree
					
					pas+=2
					
			#if the node id is in the dictionary
			else:
				#print("id nd",id_nd,di_rep_1)
				
				for j in range(le):
				
					di={}
					duree=eval(a[indice+pas])
					di[eval(a[1]),eval(a[2])]=eval(a[indice+pas+1])
					
					#if the corresponding period is already in the dictionary
					if j+1 in  di_rep_1[id_nd]:
						#if id_nd==37612:
							#if eval(a[1])==737:
								#print("here1")
					
						#print("period",j+1,"node",id_nd)
						#print(di_rep_1[id_nd])
						#print(di)
						
						di_rep_1[id_nd][j+1].update(di)
					
					#if the corrresponding period is not in the dictionary
					else:
								
						di_rep_1[id_nd][j+1]={}
						di_rep_1[id_nd][j+1].update(di)
					
						di_rep_2[id_nd][j+1]=duree
					pas=+2
				#if id_nd==37612:
					#if eval(a[1])==737:
						#print("di_rep_1[id_nd]",di_rep_1[id_nd])
						#print()
	#print(len(di_rep_1[37872][1]))
	#print()
	#print(len(di_rep_2[37872]))
	
	di_rep_cum_rp={}
	
	#print(di_rep_1[37612])
	
	di_entry_internal_with_at_least_two_outp_lks={}
	#for each node
	for nd in di_rep_1:
		#print()
		#print("nod",nd)
		di_rep_cum_rp[nd]={}
		#for each period
		for pe in di_rep_1[nd]:
		
			di_rep_cum_rp[nd][pe]={}
			
			#phases of node nd in period pe
			v_li_keys=list(di_rep_1[nd][pe].keys())
			#print()
			#print("periode",pe)
			#print()
			#print("v_li_keys",v_li_keys)
	
			#di_entry_internal_with_at_least_two_outp_lks=dict, key=id input lk, value=[...,(key, output lik),...]
			di_entry_internal_with_at_least_two_outp_lks=fct_entry_intenal_links_having_at_least_two_output_links(li_liste=v_li_keys)
			#print()
			#print("di_entry_internal_with_at_least_two_outp_lks",di_entry_internal_with_at_least_two_outp_lks)
			#print()
			for m in di_entry_internal_with_at_least_two_outp_lks:
			
				#print("m=",m,di_entry_internal_with_at_least_two_outp_lks[m][0])
				#print("m",m)
				#print()
				
				di_rep_cum_rp[nd][pe][m]=[]
				#print("di_rep_1[nd][pe]",di_rep_1[nd][pe])
				#print()
				
				li=[]
				#dict, key=id input link value=[...[key, output link],...]
				for n in di_entry_internal_with_at_least_two_outp_lks[m]:
					#print("n",n)
					li_1=[di_rep_1[nd][pe][n],n[1]]
					li.append(li_1)
				li.sort()
				di_rep_cum_rp[nd][pe][m]=li
				#print()
				#print("di_rep_cum_rp[nd][pe].keys()",di_rep_cum_rp[nd][pe].keys())
				#print()
				#print("di_rep_cum_rp[nd][pe]",di_rep_cum_rp[nd][pe])
	
	#AVERIFIER CETTE PARTIE
	if  di_entry_internal_with_at_least_two_outp_lks!={}:				
							
		#les phases qui ne varient pas
		for q in di_entry_internal_with_at_least_two_outp_lks:
			#print()
			#print("q",q)
			#print()
			#print("di_entry_internal_with_at_least_two_outp_lks[q]",di_entry_internal_with_at_least_two_outp_lks[q])
			#print()
			#print("v_li_keys avant",v_li_keys)
			for r in di_entry_internal_with_at_least_two_outp_lks[q]:
				v_li_keys.remove(r)	
			#print()
			#print("v_li_keys apres",v_li_keys)
			#import sys
			#sys.exit()
		for s in v_li_keys:
			di_rep_cum_rp[nd][pe][s[0]]=[di_rep_1[nd][pe][s],s[1]]
					
		#print()
		#print("di_rep_cum_rp",di_rep_cum_rp[37612])	
		#import sys
		#sys.exit()
	
		
	return [di_rep_cum_rp,di_rep_2]
					
#*****************************************************************************************************************************************************************************************
#fct reading the file with the series of the rout prob when varying rout prob
#it returns a dict, key=node id, value=dict, key=id period valeur= dict, key=id phase, valeur= rp for the corresponding period
def fct_read_file_fi_series_varying_rout_prob(name_file_to_read,nb_comment_lines):

	#we open the file
	file=open(name_file_to_read,"r")
	
	ind=0
	
	#di_rep={}
	
	#di_rep_1=dict, key=id node, valeur=dict, key=id period valeur= dict, key=id phase, valeur= rp for the corresponding period
	di_rep_1={}
	
	for i in file.readlines():
		ind+=1
		if ind>nb_comment_lines:
		
			#a= id node, id input link, id output link, duration of the previous values of the rout prob, rout prob next period, ...., )
			a=i.rsplit()
			
			id_nd=eval(a[0])
			
			le=int((len(a[3:])))
			#print("le",le)
			indice=3
			pas=0
			#if the node id is not in the dictionary
			if id_nd not in di_rep_1:
			
				di_rep_1[id_nd]={}
				
				
				#di=dict, key=id phase, val=rp, 
				di={}
				
				for j in range(le):
					duree=eval(a[indice+pas])
					di[eval(a[1]),eval(a[2])]=eval(a[indice+pas])
					
					di_rep_1[id_nd][j+1]={}
					di_rep_1[id_nd][j+1].update(di)
				
					
					pas=+1
					
			#if the node id is in the dictionary
			else:
				#print("id nd",id_nd,di_rep_1)
				
				for j in range(le):
				
					di={}
					duree=eval(a[indice+pas])
					di[eval(a[1]),eval(a[2])]=eval(a[indice+pas])
					
					#if the corresponding period is already in the dictionary
					if j+1 in  di_rep_1[id_nd]:
					
						#print("period",j+1,"node",id_nd)
						#print(di_rep_1[id_nd])
						#print(di)
						
						di_rep_1[id_nd][j+1].update(di)
					
					#if the corrresponding period is not in the dictionary
					else:
						di_rep_1[id_nd][j+1]={}
						di_rep_1[id_nd][j+1].update(di)
				
					pas=+1
	#print(len(di_rep_1[37872][1]))
	#print()
	#print(len(di_rep_2[37872]))
	#print(di_rep_1[37872].keys())
	return di_rep_1
					
				
	
		

#*****************************************************************************************************************************************************************************************
#fct writing the file f id all network link, id_origin_destination node_length_link link capacity
def fct_write_fi_id_all_network_link_id_orig_destination_node_length_link_capacity_link_param_travel_duration(name_file_to_write,list_valeurs=[]):

	file=open(name_file_to_write,"w")

	#for i in list_valeurs:
		#for j in i:
			#file.write(
	for i in list_valeurs:
		
		file.write("%d\t %d\t %d\t %.2f\t  %.2f\t %.2f\t \n"%(i[0],i[1],i[2],i[3],i[4],i[5]))
		
	file.close()
		

	
#*****************************************************************************************************************************************************************************************
#function writ file fi_id_internal_link_id_orig_dest_node
def fct_write_fi_id_internal_link_id_orig_dest_node(name_file_to_write,list_valeurs=[]):

	file=open(name_file_to_write,"w")

	for i in list_valeurs:
		
		file.write("%d\t %d\t %d\t  \n"%(i[0],i[1],i[2]))
		
	file.close()


#*****************************************************************************************************************************************************************************************
#fct writ file fi_id_node_id_entering_links_to_node or fi_id_node_id_leaving_links_from_node

def fct_write_fi_id_node_id_entering_or_leaving_links_to_node(name_file_to_write,list_valeurs=[]):

	file=open(name_file_to_write,"w")

	for i in list_valeurs:
		for j in i:
			file.write("%d\t"%(j))
		file.write("\n")
		
			#file.write("%d\t %d\t  %d\t  %d\t %d\t \n"%(i[0],i[1],i[2],i[3],i[4]))
		
	file.close()


#*****************************************************************************************************************************************************************************************
#funct writ file fi_id_merging queues
def fct_write_fi_id_merging_ques(name_file_to_write,list_phrases,list_valeurs=[]):
	file=open(name_file_to_write,"w")
	
	for i in list_phrases:
		file.write("%s\t \n"%(i))
		
	for i in list_valeurs:
		for j in i:
			file.write("%d\t"%(j))
		file.write("\n")

#*****************************************************************************************************************************************************************************************
#function writing files matrix_mu, matrix_sigma et matrix_shift when stoch travel times are employed  (prob law shifted lognormal)
def fct_write_fi_matrix_mu_and_sigma_and_shift(name_file_to_write_mu,name_file_to_write_sigma,name_file_to_write_shift,\
list_valeurs_mu=[],list_valeurs_sigma=[],list_valeurs_shift=[]):

	file_mu=open(name_file_to_write_mu,"w")
	file_sigma=open(name_file_to_write_sigma,"w")
	file_shift=open(name_file_to_write_shift,"w")
	
	for i in list_valeurs_mu:
		for j in i:
			file_mu.write("%d\t"%(j))
		file_mu.write("\n")
		
	for k in list_valeurs_sigma:
		for m in k:
			file_sigma.write("%d\t"%(m))
		file_sigma.write("\n")
		
	for n in list_valeurs_shift:
		for p in n:
			file_shift.write("%d\t"%(p))
		file_shift.write("\n")
		
	file_mu.close()
	file_sigma.close()
	file_shift.close()

	
#*****************************************************************************************************************************************************************************************
#fct write file fi_id_nd_id_minor_phase_id_prior_phase
def fct_write_fi_id_nd_id_minor_phase_id_prior_phase(name_file_to_write,list_phrases,list_valeurs=[]):
	file=open(name_file_to_write,"w")
	
	for i in list_phrases:
		file.write("%s\t \n"%(i))		
	for i in list_valeurs:
		for j in i:
			file.write("%d\t"%(j))
		file.write("\n")
	file.close()

#*****************************************************************************************************************************************************************************************
#function writing file fi_id_all_phases_max_queue_size_sat_flow_queue_type_param_travel_duration for network data
def fct_write_fi_id_phases_max_queue_size_sat_flow_queue_type_param_travel_dur_1(name_file_to_write,list_valeurs=[]):

	file=open(name_file_to_write,"w")

	for i in list_valeurs:
		#print("i=",i)
		
		file.write("%d\t %d\t %d\t %.3f\t %d\t  %d\t \n"%(i[0],i[1],i[2],i[3],i[4],i[5]))
		
	file.close()
#*****************************************************************************************************************************************************************************************
#function writing file fi_id_all_phases_max_queue_size_sat_flow_queue_type for network data
def fct_write_fi_id_phases_max_queue_size_sat_flow_queue_type(name_file_to_write,li_phrases=[],list_valeurs=[]):

	file=open(name_file_to_write,"w")
	
	for k in li_phrases:
		file.write("%s\t \n"%(k))	

	for i in list_valeurs:
		#print("i=",i)
		
		file.write("%d\t %d\t %d\t %.3f\t %d \n"%(i[0],i[1],i[2],i[3],i[4]))
		
	file.close()
#*****************************************************************************************************************************************************************************************
#function writing  file fi_id_all_phases_init_fin_detect_posit_nb_posit_captured
def fct_write_fi_id_all_phases_init_fin_detect_posit_nb_posit_captured(name_file_to_write,list_phrases=[],list_valeurs=[]):
	file=open(name_file_to_write,"w")
	#list_valeurs=
	#[....,[id input link phase, id output link phase, init posit captured by detector, final position captured by detector, nb positions captured (final-initit position+1)],.....]
	#each line of the  file will be:
	#input lk, output lk of the phase, initial position captured by detector, final position, nb posit capured by the capteur,
	#or
	#input lk, output lk of the phase, -1 if the capteur captures the entire queue size
	#or
	#input lk, output lk of the phase, n>0 if the capteur covers the entire queue starting from the nth position
	
	for i in list_phrases:
		file.write("%s\t \n"%(i))	
		
	for j in list_valeurs:
		for k in j:
			file.write("%d\t"%(k))
		file.write("\n")
		
	
	file.close()
#*****************************************************************************************************************************************************************************************
#fct writing files fi_mrp_id_phase_prob_dest_lk_nb.txt, indicating the rout prop of each phase. 
#As many files as variations of the rout propab during the sim
#and also file fi_duration_each_rp_mat.txt, key=id input link to node, value=[...,duration of the iths split ratio,...]
#val_dict_key_id_phase_value_lis_li_rp_mat_and_duration, dict, key=id phase, value=[ ....,[list values rout prop,duration],....]
def fct_write_files_rout_prob_and_duration(name_file_to_write_rp,name_file_to_write_duration,\
list_phrases_fi_rp=["id phase (1-2 colm), rout probab(3rd col)"],list_phrases_fi_dur=[" id input link to node (1-column), durat of the rout prop prob (next colms)"],\
val_dict_key_id_phase_value_lis_li_rp_mat_and_duration={}):

	
	#cur_dir=os.getcwd()
	#print("cur_dir",cur_dir)
	#os.chdir(val_name_folder_mrp)
	
	#creation of two folders 
	
	#folder with the files of the rout prob
	#os.mkdir(cur_dir+"/"+File_names_network_model.val_name_folder_rout_prob)
	
	#name_directory_rout_prob=cur_dir+"/"+File_names_network_model.val_name_folder_rout_prob
	
	#fold containing the files of cum rout prob
	#os.mkdir(cur_dir+"/"+File_names_network_model.val_name_folder_mat_rout_prob_cum)
	
	#name_directory_rout_prob=cur_dir+"/"+File_names_network_model.val_name_folder_mat_rout_prob_cum
	
	#we write as many files as the  nb of variations of the split ratios
	#val_dict_key_id_phase_value_lis_li_rp_mat_and_duration= dict, key=id phase, value=[ ....,[list values rout prop,duration],....]
	
	#the number of variations of the split ratio,li_phases_id=[ ...., id phase,...] with id_phase=[id input lk, id ourp link]
	#li_phases_id=list(val_dict_key_id_phase_value_lis_li_rp_mat_and_duration.keys())
	#nb_variat_rp=len(li_phases_id)
	
	#we create the file with the duration of each split ratio values for each phase and write  comments
	
	file_phase_dur_rp=open(name_file_to_write_duration,"w")
	
	for i in list_phrases_fi_dur:
		file_phase_dur_rp.write("%s\t \n"%(i))
		
	
	#creation of the file with the rout prob of each phase and write comment line
	file_phase_rp=open(name_file_to_write_rp,"w")
	
	for j in list_phrases_fi_rp:
			file_phase_rp.write("%s\t \n"%(j))
	
	
	#print("here",val_dict_key_id_phase_value_lis_li_rp_mat_and_duration)
	#import sys
	#sys.exit()
	
	
	# list with the id of input node links for which the rout prob duration is already written 
	li_id_lk_written_dur=[]
	
	
	#val_dict_key_id_phase_value_lis_li_rp_mat_and_duration, dict, key=id phase, value=[ ....,[list values rout prop,duration],....]
	#print(val_dict_key_id_phase_value_lis_li_rp_mat_and_duration)
	#for each phase 
	for m in val_dict_key_id_phase_value_lis_li_rp_mat_and_duration:
	
		file_phase_rp.write("%d\t %d\t"%(m[0],m[1]))
		
		#print("val_dict_key_id_phase_value_lis_li_rp_mat_and_duration[m][0",val_dict_key_id_phase_value_lis_li_rp_mat_and_duration[m][0])
		#for p in list(val_dict_key_id_phase_value_lis_li_rp_mat_and_duration[m][0]):
		for p in val_dict_key_id_phase_value_lis_li_rp_mat_and_duration[m][0]:
			#print("p=",p)
			#for p1 in p:
			#print(p)
			file_phase_rp.write("%.2f\t"%(p))
		file_phase_rp.write("\n")
		
		
		#if we have not written the split ratio duration of the input link, then we write it
		if m[0] not in li_id_lk_written_dur:
			file_phase_dur_rp.write("%d\t"%(m[0]))
		
			#print("HERE",val_dict_key_id_phase_value_lis_li_rp_mat_and_duration[m][1])	
			for q in val_dict_key_id_phase_value_lis_li_rp_mat_and_duration[m][1]:
				#print("q=",q)
				file_phase_dur_rp.write("%.2f\t"%(q))
			file_phase_dur_rp.write("\n")
			
		#we indicate that the split ration of the input link is written
		li_id_lk_written_dur.append(m[0])
			
	file_phase_dur_rp.close	
	file_phase_rp.close()		
#*****************************************************************************************************************************************************************************************
#function wirting the file with the rout prob of each phase
def fct_write_file_rout_prob_each_phase(val_name_file_to_write, val_li_phrases,val_li_rout_prob_values):

	file=open(val_name_file_to_write,"w")
	
	for i in val_li_phrases:
		file.write("%s\t \n"%(i))
		
	#val_li_rout_prob_values=[...., [ id input link phase, id output link phase,  routing prob 2nd period,routing prob 3rd period,...],...]
	for j in val_li_rout_prob_values:
		file.write("%d\t %d\t "%(j[0],j[1]))
		for k in j[2:]:
			file.write("%.2f\t "%(k))
		file.write("\n")

#*****************************************************************************************************************************************************************************************

#function writing file "fi_mrp_cum.txt" with the cum  rout prob
def fct_write_file_cum_rout_prob(name_file_to_write,di_key_id_entry_intern_lk_value_lis_li_rout_prob_and_id_dest_lk,\
li_phrases=["id phase (1-2 columns), cum rout prob (next colm)"]):

	file_phase_cum_rp=open(name_file_to_write,"w")
	
	for i in li_phrases:
		file_phase_cum_rp.write("%s\t \n"%(i))
	
	#print("di_key_id_entry_intern_lk_value_lis_li_rout_prob_and_id_dest_lk",di_key_id_entry_intern_lk_value_lis_li_rout_prob_and_id_dest_lk)
	#di_key_id_entry_intern_lk_value_lis_li_rout_prob_and_id_dest_lk=dict, key=id entry_intern link, value=[...,[list cum rout prob, id dest link],...]
	for j in di_key_id_entry_intern_lk_value_lis_li_rout_prob_and_id_dest_lk:
		#print("j=",j)
		#print("di_key_id_entry_intern_lk_value_lis_li_rout_prob_and_id_dest_lk[j]",di_key_id_entry_intern_lk_value_lis_li_rout_prob_and_id_dest_lk[j])
		for k in di_key_id_entry_intern_lk_value_lis_li_rout_prob_and_id_dest_lk[j]:
			#print("k=",k)
		

		#we write the phase id
		#print("di_key_id_entry_intern_lk_value_lis_li_rout_prob_and_id_dest_lk[j]",di_key_id_entry_intern_lk_value_lis_li_rout_prob_and_id_dest_lk[j])
		#file_phase_cum_rp.write("%d\t %d\t"%(j,di_key_id_entry_intern_lk_value_lis_li_rout_prob_and_id_dest_lk[j][1]))
			file_phase_cum_rp.write("%d\t %d\t"%(j,k[1]))
			
		#we write the cum rout prob values
		#print("di_key_id_entry_intern_lk_value_lis_li_rout_prob_and_id_dest_lk[j][0]",di_key_id_entry_intern_lk_value_lis_li_rout_prob_and_id_dest_lk[j][0])
		#for m in di_key_id_entry_intern_lk_value_lis_li_rout_prob_and_id_dest_lk[j][0]:
			#print("k=",k)
			#for m in k[0]:
			#for m in k:
				#print("m=",m)
				#print()
			file_phase_cum_rp.write("%.2f\t"%(k[0]))
				
			file_phase_cum_rp.write("\n")
			
				
	file_phase_cum_rp.close()	

#*****************************************************************************************************************************************************************************************
#methode qui lis les valeur rout prob, calcule les val cum et les ecrit
def fct_calcul_and_write_cum_rp(val_name_file_rout_propab_to_read,val_name_file_to_write,val_nb_comment_lines=1,val_considered_one_in_cum_fctn=0.99):

	di_cum_rp=fct_creat_dict_cum_rp_mat_from_text_file(val_name_file_rout_prop_to_read=val_name_file_rout_propab_to_read,\
	nb_comment_lines=val_nb_comment_lines,val_considered_one_in_cum_fct=val_considered_one_in_cum_fctn)
	
	fct_write_file_cum_rout_prob(name_file_to_write=val_name_file_to_write,di_key_id_entry_intern_lk_value_lis_li_rout_prob_and_id_dest_lk=di_cum_rp,\
	li_phrases=["id phase (1-2 columns), cum rout prob (next colm)"])
	
	

#*****************************************************************************************************************************************************************************************

#function write the two files "fi_stages_each_non_sign_inters.txt" and "fi_id_entry_exit_lk_related_path.txt"
def fct_write_files_stages_si_and_nsi_prev(name_file_to_write_stages_nsi,name_file_to_write_stages_si,di_stages_nsi,di_stages_si,\
li_phrases_nsi=["for each line, 1st column: id nsi inters, next columns phases to actuate"],\
li_phrases_si=["for each line, 1st column: id sign inters, next columns phases to actuate"]):

	file_nsi=open(name_file_to_write_stages_nsi,"w")
	
	file_si=open(name_file_to_write_stages_si,"w")
	
	for i in li_phrases_nsi:
		file_nsi.write("%s\t \n"%(i))
		
	for i in li_phrases_si:
		file_si.write("%s\t \n"%(i))
	
	#print(di_stages_nsi)
	#print()
	#print(di_stages_si)
	#we write the file with the nsi stages	
	#di_stages_nsi=dict, key= id node, value= [...,[...,li compatble phases, ...],...]
	for i in di_stages_nsi:
		
		for j in di_stages_nsi[i]:
			file_nsi.write("%d\t"%(i))
			for k in j:
				file_nsi.write("%d\t"%(k))
			file_nsi.write("\n")
			 
	for i in di_stages_si:
		
		for j in di_stages_si[i]:
			file_si.write("%d\t"%(i))
			for k in j:
				file_si.write("%d\t"%(k))
			file_si.write("\n")	
			
		
	
	
	file_nsi.close()
	file_si.close()


#*****************************************************************************************************************************************************************************************
#function write the two files "fi_stages_each_non_sign_inters.txt" and "fi_id_entry_exit_lk_related_path.txt"
def fct_write_files_stages_si_and_nsi(name_file_to_write_stages_nsi,name_file_to_write_stages_si,di_stages_nsi,di_stages_si,\
li_phrases_nsi=["for each line, 1st column: id nsi inters, next columns phases to actuate"],\
li_phrases_si=["for each line, 1st column: id sign inters, next columns phases to actuate"]):

	file_nsi=open(name_file_to_write_stages_nsi,"w")
	
	file_si=open(name_file_to_write_stages_si,"w")
	
	for i in li_phrases_nsi:
		file_nsi.write("%s\t \n"%(i))
		
	for i in li_phrases_si:
		file_si.write("%s\t \n"%(i))
	
	#print(di_stages_nsi)
	#print()
	#print(di_stages_si)
	#we write the file with the nsi stages	
	#di_stages_nsi=dict, key= id node, value= dict, key=id stage which will be the line to be written [...,[...,li compatble phases, ...],...]
	for i in di_stages_nsi:
		li_id_stages=list(di_stages_nsi[i].keys())
		li_id_stages.sort()
		for j in li_id_stages:
			file_nsi.write("%d\t"%(i))
			for m in di_stages_nsi[i][j]:
				
				file_nsi.write("%d\t"%(m))
			file_nsi.write("\n")	
					 
	for i in di_stages_si:
		li_id_stages=list(di_stages_si[i].keys())
		li_id_stages.sort()
		for j in li_id_stages:
			file_si.write("%d\t"%(i))
			for m in di_stages_si[i][j]:
				file_si.write("%d\t"%(m))
			file_si.write("\n")
		
		
		#for j in di_stages_si[i]:
			#file_si.write("%d\t"%(i))
			#for k in j:
				#file_si.write("%d\t"%(k))
			#file_si.write("\n")	
			
		
	
	
	file_nsi.close()
	file_si.close()


#*****************************************************************************************************************************************************************************************


#function writing file "fi_mrp_cum.txt" with the cum  rout prob
def fct_write_file_cum_rout_prob_from_text_file(name_file_to_write,di_key_id_entry_intern_lk_value_lis_li_rout_prob_and_id_dest_lk,\
li_phases=["id phase (1-2 columns), cum rout prob (next colm)"]):

	file_phase_cum_rp=open(name_file_to_write,"w")
	
	for i in li_phases:
		file_phase_cum_rp.write("%s\t \n"%(i))
	
	
	
	#di_key_id_entry_intern_lk_value_lis_li_rout_prob_and_id_dest_lk= dict, key=phase id, value=[..,[cum rout prob,id dest link],..]
	#for eeach phase
	for j in di_key_id_entry_intern_lk_value_lis_li_rout_prob_and_id_dest_lk:
		
		#print("di_key_id_entry_intern_lk_value_lis_li_rout_prob_and_id_dest_lk[j]",di_key_id_entry_intern_lk_value_lis_li_rout_prob_and_id_dest_lk[j])
		for k in di_key_id_entry_intern_lk_value_lis_li_rout_prob_and_id_dest_lk[j]:
			
		
		#we write the phase id
		#print("di_key_id_entry_intern_lk_value_lis_li_rout_prob_and_id_dest_lk[j]",di_key_id_entry_intern_lk_value_lis_li_rout_prob_and_id_dest_lk[j])
		#file_phase_cum_rp.write("%d\t %d\t"%(j,di_key_id_entry_intern_lk_value_lis_li_rout_prob_and_id_dest_lk[j][1]))
			file_phase_cum_rp.write("%d\t %d\t %.2f\n"%(j,k[1],k[0]))
			
		
		#we write the cum rout prob values
		#print("di_key_id_entry_intern_lk_value_lis_li_rout_prob_and_id_dest_lk[j][0]",di_key_id_entry_intern_lk_value_lis_li_rout_prob_and_id_dest_lk[j][0])
		#for m in di_key_id_entry_intern_lk_value_lis_li_rout_prob_and_id_dest_lk[j][0]:
			
			#for m in k[0]:
				#print("m=",m)
				#print()
				#file_phase_cum_rp.write("%.2f\t"%(m))
				
			#file_phase_cum_rp.write("\n")
			
				
	file_phase_cum_rp.close()	

#*****************************************************************************************************************************************************************************************

#function write file fi_id_que_position_presence_detector.txt
def fct_write_fi_id_que_position_presence_detector(name_file_to_write,\
list_phrases=[" id origin-dest lk(1,2,colmsn), initial position sensor in que, (1st position corresponds to 1)  (3 col), final  position sensor in que (4 col)"],\
list_valeurs=[]):

	file=open(name_file_to_write,"w")
	
	for i in list_phrases:
		file.write("%s\t \n"%(i))
		
	#A SUIVRE....
	
#*****************************************************************************************************************************************************************************************
#fct write file fi_id_que_position_que_size_detector.txt
def fct_fi_id_que_position_que_size_detector(name_file_to_write,\
list_phrases=[" id origin-dest lk(1,2,colmsn), initial position sensor in que, (1st position corresponds to 1)  (3,4.. col)"],\
list_valeurs=[]):
	file=open(name_file_to_write,"w")
	
	for i in list_phrases:
		file.write("%s\t \n"%(i))
		
	#A SUIVRE....

#*****************************************************************************************************************************************************************************************
#fct write file "fi_id_phase_prob_rout_prop.txt"
def fct_write_fi_id_phase_prob_dest_lk(name_file_to_write,list_phrases,list_valeurs=[]):
	file=open(name_file_to_write,"w")
	
	for i in list_phrases:
		file.write("%s\t \n"%(i))
		
	for i in list_valeurs:
		file.write("%d\t"%(i[0]))
		a=len(i)
		for j in i[1:a]:
			file.write("%.2f\t"%(j))
		file.write("\n")
	file.close()
#*****************************************************************************************************************************************************************************************


#function reading file "fi_id_entry_lk_t_veh_appear.txt".
#it returns a dictionary, key=id entry_internal link, value=[...,time veh appear,...]
def fct_creat_dict_key_id_entry_lk_value_lis_t_veh_appear_given_demand(name_file_read,nb_comment_lines):
	
	#we open the file
	file=open(name_file_read,"r")
	#print("HERE")
	#import sys
	#sys.exit()
	
	di={}
	#indicator of the number of lines already read
	ind_line_read=0
	for i in file.readlines():
		ind_line_read+=1
		if ind_line_read>nb_comment_lines:
			a=i.rsplit()
			#print("a=",a)
			#import sys
			#sys.exit()
			b=int(eval(a[0]))
			if b not in di:
				di[b]=[eval(a[1])]
				
			else:
				di[b].append(eval(a[1]))
	for j in di:
		di[j].sort()
	#print(di[1])
	#import sys
	#sys.exit()
	file.close()
	return di
#*****************************************************************************************************************************************************************************************

#fct writing files "fi_id_phase_val_cum_funct_rout_prop.txt" and ''fi_id_entry_intern_lk_id_dest_lk.txt), from file mat od
#li_list_phrases=[list phrases for cum file, [list phrases for id dest lk file]
def fct_write_files_fi_id_phase_val_cum_funct_rout_prop_and_fi_id_entry_intern_lk_id_dest_lk(name_file_read,\
name_file_to_write_cum,name_file_to_write_id_dest_lk,li_list_phrases,v_nb_comment_lines,v_considered_one_in_cum_fct=0.98):

	file_cum=open(name_file_to_write_cum,"w")
	
	file_dest=open(name_file_to_write_id_dest_lk,"w")
	
	for p in li_list_phrases[0]:
		file_cum.write("%s\t \n"%(p))
		
	for k in li_list_phrases[1]:
		file_dest.write("%s\t \n"%(k))
	
	#li_di=[di_prob,di_cum,di_id_dest_lk]
	li_di=fct_creat_dicts_rp_mat(name_file_read,v_nb_comment_lines,v_considered_one_in_cum_fct)
	#print("name_file_read",name_file_read)
	#print()
	#print(li_di[0])
	#print()
	#print(li_di[1])
	#print()
	#print(li_di[2])
	#import sys
	#sys.exit()
	
	#li_di[1]; dict, key=id entry_internal lk, value=[.., cum value,...]
	for i in li_di[1]:
		file_cum.write("%d\t"%(i))
		for j in li_di[1][i]:
			file_cum.write("%.3f\t"%(j))
		file_cum.write("\n")
		
	#li_di[2] dict, key=id entry_internal lk, value=[...,id_dest, lk]
	for m in li_di[2]:
		file_dest.write("%d\t"%(m))
		#if name_file_read=="fi_mod_id_phase_prob_dest_lk9.txt" and m==2:
			#print(li_di[2][m])
			#print()
			#for n in li_di[2][m]:
				#print(n)
		for n in li_di[2][m]:
			file_dest.write("%d\t"%(n))
		file_dest.write("\n")
		#if name_file_read=="fi_mod_id_phase_prob_dest_lk9.txt" and m==7:
			#print("HERE key=",m,"value write=",n," li_di[2][m]", li_di[2][m])
			
		
			
		
		
	file_cum.close()
	file_dest.close()		
		
#*****************************************************************************************************************************************************************************************

#function writing  the file with the parameters of FT control
#li_valeurs=[...,[id nd, id stage, act duration, cycle duration],...], for the red clearance he id of the stage will be zero
def fct_write_file_parameters_ft_control(name_file_to_write,li_valeurs, li_phrases):
	
	file=open(name_file_to_write,"w")
	
	for i in li_phrases:
		file.write("%s\t \n"%(i))
		
	le=len(li_valeurs)
	#we write the line with the offsets, as many cilumns as node ids
	for i in li_valeurs[0]:
		file.write("%d\t"%(i))
	file.write("\n")
	
	#file.write("%d\t %.1f \n"%( li_valeurs[0][0], li_valeurs[0][1]))
		
	for j in li_valeurs[1:le-1]:
		file.write("%d\t %d\t %.1f\t %.1f \n"%(j[0],j[1],j[2],j[3]))
	file.close()
#*****************************************************************************************************************************************************************************************
#function writing  the file with the parameters of MP control
def fct_write_file_parameters_ft_control(name_file_to_write,li_phrases,li_valeurs):
	file=open(name_file_to_write,"w")
	for i in li_phrases:
		file.write("%s\t \n"%(i))
		
	for i in li_valeurs:
		for j in i:
			file.write("%.2f\t "%(j))
		file.write("\n")
	
	file.close()
	

#*****************************************************************************************************************************************************************************************
#fct write file "fi_id_phase_prob_rout_prop.txt"
def fct_write_fi_id_phase_prob_dest_lk(name_file_to_write,list_phrases,list_valeurs=[]):
	file=open(name_file_to_write,"w")
	
	for i in list_phrases:
		file.write("%s\t \n"%(i))
		
	for i in list_valeurs:
		file.write("%d\t"%(i[0]))
		a=len(i)
		for j in i[1:a]:
			file.write("%.2f\t"%(j))
		file.write("\n")
	file.close()
#*****************************************************************************************************************************************************************************************
#fct write  file "fi_id_non_signalised_intersection_nodes.txt"
#list_valeurs=[...,[id nd, type inters],...]
def fct_write_fi_id_intersection_nodes_type_inters(name_file_to_write,list_phrases,list_valeurs=[]):

	file=open(name_file_to_write,"w")
	
	for i in list_phrases:
		file.write("%s\t \n"%(i))
		
	for j in list_valeurs:
		file.write("%d\t %d \n"%(j[0],j[1]))
	file.close()
#*****************************************************************************************************************************************************************************************
#fct write file fi_id_entry_link_type_lk,
#list_valeurs=[...[id entry lk, type],..]
def fct_write_fi_id_entry_link_type_lk(name_file_to_write,list_phrases,list_valeurs=[]):

	file=open(name_file_to_write,"w")
	
	for i in list_phrases:
		file.write("%s\t \n"%(i))
		
	for j in list_valeurs:
		
		file.write("%d\t %d \n"%(j[0],j[1]))
	file.close()

#*****************************************************************************************************************************************************************************************
#function writing file id node id entry link to node
def fct_write_fi_id_node_id_entry_links_to_netw(name_file_to_write,val_dict_id_nd_li_id_entry_links):

	file=open(name_file_to_write,"w")
	
	#val_dict_id_nd_li_id_entry_links= dict, key=string(node id), value=list string link id
	#print(val_dict_id_nd_li_id_entry_links)
	
	for i in val_dict_id_nd_li_id_entry_links:
		file.write("%d\t"%(i))
		for j in val_dict_id_nd_li_id_entry_links[i]:
			file.write("%d\t"%(j))
		file.write("\n")
	file.close()
#*****************************************************************************************************************************************************************************************

#fct writing file id entry link type link
def fct_write_fi_id_entry_lk_type_lk(name_file_to_write,li_phrases,val_dict_s_and_ns_links):

	file=open(name_file_to_write,"w")
	
	for m in li_phrases:
		file.write("%s\t \n"%(m))
	
	#val_dict_s_and_ns_links=dict, ley =1/0 for singnalised/non signalised links, value= list  string ink id
	#val_dict_s_and_ns_links= {1: [..,"id link",...], 0: [..,"id link",...] }
	for i in val_dict_s_and_ns_links:
		for j in val_dict_s_and_ns_links[i]:
			file.write("%d\t %d\n"%(eval(j),i))
	file.close()
						
#*****************************************************************************************************************************************************************************************	
#function writing file fi_id_node_id_exit_links_from_network.txt
def fct_write_fi_id_node_id_exit_links_from_network(name_file_to_write,val_dict_id_nd_li_id_exit_links):

	file=open(name_file_to_write,"w")
	
	#val_dict_id_nd_li_id_exit_linkss= dict, key=string(node id), value=list string exit link id
	
	for i in val_dict_id_nd_li_id_exit_links:
		file.write("%d\t"%(i))
		for j in val_dict_id_nd_li_id_exit_links[i]:
			file.write("%d\t"%(j))
		file.write("\n")
	file.close()

#*****************************************************************************************************************************************************************************************
#fct write file fi_id_nd_id_minor_phase_id_prior_phase
def fct_write_fi_id_nd_id_minor_phase_id_prior_phase(name_file_to_write,list_phrases,list_valeurs=[]):
	file=open(name_file_to_write,"w")
	
	for i in list_phrases:
		file.write("%s\t \n"%(i))		
	for i in list_valeurs:
		for j in i:
			file.write("%d\t"%(j))
		file.write("\n")
	file.close()

#*****************************************************************************************************************************************************************************************
#funct writ file fi_id_merging queues
def fct_write_fi_id_merging_ques(name_file_to_write,list_phrases,list_valeurs=[]):
	file=open(name_file_to_write,"w")
	
	for i in list_phrases:
		file.write("%s\t \n"%(i))
		
	for i in list_valeurs:
		for j in i:
			file.write("%d\t"%(j))
		file.write("\n")
		
	file.close()

#*****************************************************************************************************************************************************************************************
#funct write file fi_demand_param_entry_link
def fct_write_fi_demand_param_entry_link(name_file_to_write,list_valeurs=[]):

		file=open(name_file_to_write,"w")
		
		for i in list_valeurs:
			
			file.write("%d\t %.3f\t \n"%(i[0],i[1]))
			
		
		file.close()

#*****************************************************************************************************************************************************************************************
#funct wtite file fi_id_node_type_node
def fct_write_fi_id_node_type_node_cas_nds_sign(name_file_to_write,list_phrases,list_valeurs=[]):

	file=open(name_file_to_write,"w")
	for i in list_phrases:
		file.write("%s\t \n"%(i))
		
	for i in list_valeurs:
			
			file.write("%d\t %d\t \n"%(i,1))
	
	file.close()


#*****************************************************************************************************************************************************************************************
#funct wtite file fi_id_node_type_ctrl_category
def fct_write_fi_id_node_type_ctrl_categoryr(name_file_to_write,list_phrases=[" id node (1st collm), type control ,(2nd colm)1: \"type_control_FT\", 2:\"type_control_FT_Offset\", \
3:\"type_control_MP\" , 10: \``type_control_FA _no red clear\‘’,11:\"type_control_FA_Max_Green\" ,12: \``type_control_FA _with_red lrear\",1\
3:\"type_control_MP_Practical \‘’,(3rd colm): control category indicates if the ctrl is updated accroding to flows or not, sensor_requirement for controls requiring sensor monitoring (FA,FAmax green),\
without_sensor_requirement for controls not requiring sensors (FT, MP, etc),(4th column): 1 if turn ratios are going to be estimated with the employed control, 0 otherwise"],list_valeurs=[]):

	file=open(name_file_to_write,"w")
	for i in list_phrases:
		file.write("%s\t \n"%(i))
		
	for j in list_valeurs:
			
			file.write("%d\t %d\t  %s\t %d\n"%(j[0],j[1],j[2],j[3]))
	
	file.close()


#*****************************************************************************************************************************************************************************************
def fct_write_file_intersection_stages(name_file_to_write,list_phrases,list_valeurs=[]):

	file=open(name_file_to_write,"w")
	
	for i in list_phrases:
		file.write("%s\t \n"%(i))

	for i in list_valeurs:
		for j in i:
			
			file.write("%d\t"%(j))
		file.write("\n")
		
	file.close()

#*****************************************************************************************************************************************************************************************
#fct wiritng the compatible phases for each intersection
#list_valeurs=[...,[id nd, id phases..],..]
def fct_write_file_compatible_phases_nsi(name_file_to_write,list_phrases,list_valeurs=[]):
	file=open(name_file_to_write,"w")
	
	for i in list_phrases:
		file.write("%s\t \n"%(i))

	for i in list_valeurs:
		for j in i:
		
			file.write("%d\t"%(j))
		file.write("\n")
		
	file.close()

#*****************************************************************************************************************************************************************************************
#method writing file "fi_id_all_network_link_id_orig_dest_node_length_link_capacity_link_param_travel_duration.txt"
def fct_write_fi_id_all_network_link_id_orig_dest_node_length_link_capacity_link_param_travel_duration(name_file_to_write,\
di_id_lk_value_li_orig_dest_nd_length_cap_mean_travel_param):
	file=open(name_file_to_write,"w")
	for i in di_id_lk_value_li_orig_dest_nd_length_cap_mean_travel_param:
		file.write(" %d\t %d\t %d\t %.2f\t %.2f\t  %.2f\n"%(i,di_id_lk_value_li_orig_dest_nd_length_cap_mean_travel_param[i][0],\
		di_id_lk_value_li_orig_dest_nd_length_cap_mean_travel_param[i][1],di_id_lk_value_li_orig_dest_nd_length_cap_mean_travel_param[i][2],\
		di_id_lk_value_li_orig_dest_nd_length_cap_mean_travel_param[i][3],di_id_lk_value_li_orig_dest_nd_length_cap_mean_travel_param[i][4]))
	file.close()
#*****************************************************************************************************************************************************************************************
#fct writing file "fi_id_all_phases_max_queue_size_sat_flow_queue_type.txt"
def fct_write_file_fi_id_all_phases_max_queue_size_sat_flow_queue_type(name_file_to_write,di_phase_info):
	file=open(name_file_to_write,"w")
	
	#di_phase_info=dict, key=id phase, valeur=[max que size, sat flow, que type]
	for i in di_phase_info:
		file.write("%s\t  %s\t"%(i[0],i[1]))
		
		file.write("%d\t %.2f\t %d\n"%(di_phase_info[i][0],di_phase_info[i][1],di_phase_info[i][2]))
	
	file.close()
	
#*****************************************************************************************************************************************************************************************
#fct writing file fi_init_state_que.txt
#li_valeurs=[...,[id nd, id input lk, id outp lk, nb veh>0],...]
def fct_write_file_fi_init_state_que(name_file_to_write,li_valeurs,\
li_phrases=["id node (1st clmn), id phase (2nd, 3rd clmn), nb veh (3rd clmn), id veh final dest (>0 when OD, -1 otherwise, next columns) IF YOU REMOVE VEH FROM QUEUE THE REMAINING VEH WILL KEEP THEIR FINAL DEST"]):

	file=open(name_file_to_write,"w")
	
	for i in li_phrases:
		file.write("%s\t \n"%(i))
		
	for j in li_valeurs:
		for m in j:
			file.write("%d\t"%(m))
		file.write("\n")
			
	file.close()

#*****************************************************************************************************************************************************************************************
#fct writing  the file with the phase interference
def fct_write_file_fi_phase_interference(name_file_to_write,li_valeurs,\
li_phrases=["id node (1 colm), id phase  affected (2-3 colm), id affecting phase (4-5 colm), param affected phase (6 colm)"]):

	file=open(name_file_to_write,"w")
	
	for i in li_phrases:
		file.write("%s\t \n"%(i))
		
	for j in li_valeurs:
		
		file.write("%d\t %d\t  %d\t %d\t %d\t %.2f  \n"%(j[0],j[1],j[2],j[3],j[4],j[5]))
		
			
	file.close()

#*****************************************************************************************************************************************************************************************
#fct write the file with the routing type of entry links associated with od and given paths or dynamically computed ones
def fct_write_file_fi_rout_type_entry_lk_mixed_manag(name_file_to_write,li_valeurs,\
li_phrases=["id lk (1st column), rout. type (2nd column) 1: od and given path, 2: od and dynam computed path"]):

	file=open(name_file_to_write,"w")
	
	for i in li_phrases:
		file.write("%s\t \n"%(i))
		
	for j in li_valeurs:
		
		file.write("%d\t %d  \n"%(j[0],j[1]))
	
	file.close()
	


#*****************************************************************************************************************************************************************************************
#*****************************************************************************************************************************************************************************************
#***********************************************creat netw files from xml*********************************************************************************************************

#*****************************************************************************************************************************************************************************************
#method calculating the link capacity (max nb of vehicles than can be stored in the link) from the link information included  in the xml file
#xml definition of jam_density=nb of vehciles/mile  that can be stored on a lane
#".Q" definition of link capacity= nb of vehicles that can be contained along the link 
def fct_calculating_link_capacity_from_jam_density_and_link_length_1(val_jam_density,val_lk_length, val_nb_lanes,val_round_prec):
		return round(val_jam_density*val_lk_length*val_nb_lanes,val_round_prec)

#*****************************************************************************************************************************************************************************************
#method calculating the link capacity (max nb of vehicles than can be stored in the link) from the link information included  in the xml file
#xml definition of jam_density=nb of vehciles/mile  that can be stored on a lane
#".Q" definition of link capacity= nb of vehicles that can be contained along the link 
def fct_calculating_link_capacity_from_jam_density_and_link_length(val_jam_density,val_lk_length,val_round_prec):
		return round(val_jam_density*val_lk_length,val_round_prec)

#*****************************************************************************************************************************************************************************************
#method calculating the travel duration (in secs) of a link using the related mean  speed value (ffs)
def fct_calcul_link_travel_duration_from_mean_speed_value(val_link_length,val_mean_speed,val_round_prec):
	return round(val_link_length *3600/val_mean_speed,val_round_prec)

#*****************************************************************************************************************************************************************************************

#method creating the list of values for fct "fct_write_fi_id_all_network_link_id_orig_dest_node_length_link_capacity_link_param_trav_dur"
#val_di_id_link_value_li_lk_capacity_jam_density_ff_speed_stan_dev_from_xml= dictionary key =id link,  value is a list
#[link capacity (def as used in the xml file),jam density, free flow speed, stan deviation of the ffs]
def fct_creat_li_val_fct_write_fi_id_all_network_link_id_orig_dest_node_length_link_capacity_link_param_travel_durat_1(v_dict_lk_info_from_xml_file,\
val_name_origin_nd_id="origin_nd_id",val_name_dest_nd_id="dest_nd_id",val_name_length="length",\
val_di_id_link_value_li_lk_capacity_jam_density_ff_speed_stan_dev_from_xml={},val_round_precision=2,val_name_attribut_lanes="lanes",\
val_round_prec_calc_lk_travel_dur=1):

	#v_dict_nd_info_from_xml_file=dict, key=nod id, value=dict having keys "li_output_links_id", "li_input_lk_id","type " (indicating if an intersection
	#is/not signalised),"id" indicating the node id
	#we create a list [...,[id_lk, id origin nd, id dest_nd, lk length,lk capacity],...]
	li_rep=[]
	
	#print("v_dict_lk_info_from_xml_file",v_dict_lk_info_from_xml_file)
	#for each  link id we extract the required info
	#v_dict_lk_info_from_xml_file=dict, key=link id, value=dict keys= "length","dest_nd_id", "origin_nd_id","id","lanes"
	for i in v_dict_lk_info_from_xml_file:
		#if the link is not an exit link
		#print("i=",i,v_dict_lk_info_from_xml_file[i][val_name_dest_nd_id])
		#print("v_dict_lk_info_from_xml_file[i][val_name_dest_nd_id]",v_dict_lk_info_from_xml_file[i][val_name_dest_nd_id])
		
		
		
		link_length=eval(v_dict_lk_info_from_xml_file[i][val_name_length])
		#print("HERE",i)
		#print(val_di_id_link_value_li_lk_capacity_jam_density_ff_speed_stan_dev_from_xml)
		#val_di_id_link_value_li_lk_capacity_jam_density_ff_speed_stan_dev_from_xml= dict,key =id link,  value is a list
		#[link capacity (def as used in the xml file),jam density, free flow speed, stan deviation of the ffs]
		
		#print("IN GLOB FUNCT NET fct_creat_li_val_fct_write_fi_id_all_network_link_id_orig_dest_node_length_link_capacity_link_param_travel_dura",val_di_id_link_value_li_lk_capacity_jam_density_ff_speed_stan_dev_from_xml)
		#we calculate the link capacity 
		#lk_cap=fct_calculating_link_capacity_from_jam_density_and_link_length(\
		#val_jam_density=eval(val_di_id_link_value_li_lk_capacity_jam_density_ff_speed_stan_dev_from_xml[i][1]),\
		#val_lk_length=link_length,val_nb_lanes=eval(v_dict_lk_info_from_xml_file[i][val_name_attribut_lanes]),val_round_prec=val_round_precision)
		
		#A FAIRE !!!!!
		lk_cap=fct_calculating_link_capacity_from_jam_density_and_link_length(\
		val_jam_density=eval(val_di_id_link_value_li_lk_capacity_jam_density_ff_speed_stan_dev_from_xml[i][1]),\
		val_lk_length=link_length,val_round_prec=val_round_precision)
		
		#we calculate the mean travel time of the link using the mean speed,  (ffs of the xml file)
		param_link_travel_duration=fct_calcul_link_travel_duration_from_mean_speed_value(\
		val_link_length=link_length,\
		val_mean_speed=eval(val_di_id_link_value_li_lk_capacity_jam_density_ff_speed_stan_dev_from_xml[i][2]),\
		val_round_prec=val_round_prec_calc_lk_travel_dur)
		
		
		
		
		#li=id link, id origine node, id destination node, length link, link capacity
		#li=[eval(i),eval(v_dict_lk_info_from_xml_file[i][val_name_origin_nd_id]),eval(v_dict_lk_info_from_xml_file[i][val_name_dest_nd_id]),\
		#link_length,lk_cap,param_link_travel_duration]
		li=[i,eval(v_dict_lk_info_from_xml_file[i][val_name_origin_nd_id]),eval(v_dict_lk_info_from_xml_file[i][val_name_dest_nd_id]),\
		link_length,lk_cap,param_link_travel_duration]
		
		li_rep.append(li)

	return li_rep
#*****************************************************************************************************************************************************************************************

#method creat list values for "fct_write_fi_id_internal_link_id_orig_dest_node" A VERIFIER COMMENT  ENTRY/EXIT LINKS SONT INDIQUES !!!
def fct_creat_li_val_fct_write_fi_id_internal_link_id_orig_dest_node(v_dict_lk_info_from_xml_file,\
val_name_origin_nd_id="origin_nd_id",val_name_dest_nd_id="dest_nd_id"):

	#dict_lk_info=dict, key=link id, value=dict with keys :'dest_nd_id','length','lanes','origin_nd_id','type','id','in_sync',
	#'lane_offset'
	#we create a list [...,[id_internal lk, id origin nd, id dest_nd],...]
	li_rep=[]
	#for each  link id we extract the required info
	#print(v_dict_lk_info_from_xml_file)
	for i in v_dict_lk_info_from_xml_file:
		if eval(v_dict_lk_info_from_xml_file[i][val_name_origin_nd_id]) >0 and eval(v_dict_lk_info_from_xml_file[i][val_name_dest_nd_id])>0:
			li=[i,eval(v_dict_lk_info_from_xml_file[i][val_name_origin_nd_id]),eval(v_dict_lk_info_from_xml_file[i][val_name_dest_nd_id])]
			li_rep.append(li)
	return li_rep

#*****************************************************************************************************************************************************************************************	
#method creat list values for  fct_write_fi_id_node_id_entering_or_leaving_links_to_node
def fct_creat_li_val_fct_write_fi_id_node_id_entering_links_to_node(v_dict_nd_info_from_xml_file,\
val_name_type="type",val_name_nd_terminal_type="terminal",val_name_attribut_li_input_link_id="li_input_link_id"):

	#v_dict_nd_info_from_xml_file=dict, key=nod id, value=dict having keys "li_output_links_id", "li_input_lk_id","type " (indicating if an intersection
	#is/not signalised),"id" indicating the node id
	#we create a list [...,[id_node, id entering lk_1 to node,  id entering lk_2 to node,...],...]
	li_rep=[]
	#for each node we extract the required info
	
	for i in v_dict_nd_info_from_xml_file:
		#if the node is not a terminal one
		if v_dict_nd_info_from_xml_file[i][val_name_type]!=val_name_nd_terminal_type:
			li_1=[i]
			li_1.extend([eval(j) for j in v_dict_nd_info_from_xml_file[i][val_name_attribut_li_input_link_id]])
			li_rep.append(li_1)
	return li_rep
		
		
		
#*****************************************************************************************************************************************************************************************
#method creat list values for  fct_write_fi_id_node_id_entering_or_leaving_links_to_node
def fct_creat_li_val_fct_write_fi_id_node_id_leaving_links_to_node(v_dict_nd_info_from_xml_file,\
val_name_type="type",val_name_nd_terminal_type="terminal",val_name_attribut_li_output_link_id="li_output_link_id"):

	#v_dict_nd_info_from_xml_file=dict, key=nod id, value=dict having keys "li_output_links_id", "li_input_lk_id","type " (indicating if an intersection
	#is/not signalised),"id" indicating the node id
	#we create a list [...,[id_node, id entering lk_1 to node,  id entering lk_2 to node,...],...]
	li_rep=[]
	#print(v_dict_nd_info_from_xml_file)
	#for each node we extract the required info
	for i in v_dict_nd_info_from_xml_file:
		#if the node is not a terminal one
		if v_dict_nd_info_from_xml_file[i][val_name_type]!=val_name_nd_terminal_type:
			li_1=[i]
			li_1.extend([eval(j) for j in v_dict_nd_info_from_xml_file[i][val_name_attribut_li_output_link_id]])
			li_rep.append(li_1)
	return li_rep
#*****************************************************************************************************************************************************************************************
#method creating list values for fct_write_fi_id_intersection_nodes_type_inters
def fct_creat_li_val_fct_write_fi_id_intersection_nodes_type_inters(v_dict_nd_info_from_xml_file,\
val_name_type="type",val_attribut_name_signalised_node="signalized",val_attribut_name_unsignalised_node="unsignalized"):

	#v_dict_nd_info_from_xml_file=dict, key=nod id, value=dict having keys "li_output_links_id", "li_input_lk_id","type " (indicating if an intersection
	#is/not signalised),"id" indicating the node id
	#we create a list [...,[id_node, id entering lk_1 to node,  id entering lk_2 to node,...],...]
	li_rep=[]
	#for each node we extract the required info
	#print(v_dict_nd_info_from_xml_file)
	for i in v_dict_nd_info_from_xml_file:
		
		if v_dict_nd_info_from_xml_file[i][val_name_type]==val_attribut_name_signalised_node:
			li_1=[i,1]
			li_rep.append(li_1)
		elif v_dict_nd_info_from_xml_file[i][val_name_type]==val_attribut_name_unsignalised_node:
			li_1=[i,0]
			li_rep.append(li_1)
	return li_rep
#*****************************************************************************************************************************************************************************************

#method writing the network  files when the network information is obtained from .xml files
def fct_write_network_files_from_xml_file_information(v_name_file_to_read="scenario_example.xml",\
v_name_elem_networklist="NetworkList",v_name_elem_nodelist="NodeList",\
v_name_elem_id_attrib="id",v_name_elem_inputs="inputs",v_name_elem_input="input",\
v_name_elem_link_id="link_id",v_name_elem_outputs="outputs",v_name_elem_output="output",\
v_name_elem_linklist="LinkList",\
v_name_elem_node_id="node_id",val_name_network_folder="NETWORK_DATA",\
v_name_origin_node_attribut="begin",v_name_destination_node_attribut="end",\
v_name_attribut_origin_node_lk="origin_nd_id",v_name_attribut_dest_node_lk="dest_nd_id",\
v_name_attribut_type_node="type",v_type_boundary_node="terminal",v_name_length="length",\
v_name_attribut_li_input_link_id="li_input_link_id",v_name_attribut_li_output_link_id="li_output_link_id",\
v_attribut_name_signalised_node="signalized",v_attribut_name_unsignalised_node="unsignalized",\
v_indicator_sign_lk=1,v_indicator_nonsign_lk=0,v_name_attribut_lanes="lanes",v_round_precision=0,va_round_prec_calc_lk_travel_dur=1,\
v_name_elem_fundamentaldiagramset="FundamentalDiagramSet",v_name_fundamentaldiagram="fundamentalDiagram",\
v_name_attribut_capacity="capacity",v_name_attribut_jam_density="jam_density",v_name_attribut_free_flow_speed="free_flow_speed",\
v_name_attribut_std_dev_free_flow_speed="std_dev_free_flow_speed",v_name_elem_splitratioset="SplitRatioSet",\
v_name_splitRatioProfile="splitRatioProfile",v_name_duration_rout_prop_dt="dt",\
v_name_elem_splitratio="splitratio",v_name_attrib_inputlink="link_in",v_name_attrib_outputlink="link_out",\
v_considered_one_in_cum_fct=0.98,\
v_li_phases_cum_rp=["id phase (1-2 columns), cum rout prob (next colm)"],\
v_name_elem_signalList="SignalList",v_name_elem_signal="signal",\
v_name_attribute_node_id="node_id",v_name_attribute_nema="nema",v_name_attribute_lk_id="id",\
v_name_attribute_lane_dest_lk="link_to",\
v_name_attribut_type_nsi="unsignalized",v_name_attribut_type_si="signalized",\
v_name_attribut_knob="knob",v_round_prec=2,v_t_unit=0.1,v_name_attribut_type_phase="movement",\
v_name_indicator_right_turn="r",\
v_name_attribute_length="length",v_round_prec_lk_length=0,\
v_round_prec_vit_moy=1,\
v_name_elem_ControllerSet="ControllerSet",v_name_attrib_node_id="id",v_name_attrib_row_id="id"):

	#creation du dossier NETWORK_DATA  ou on mettra mes fichiers du reseau
	os.mkdir(val_name_network_folder)
	folder_network_files=val_name_network_folder
	#print(folder_network_files)
	
	#li_rep=[di_nd_info,di_lk_info,di_id_node_li_entry_lk,di_id_node_li_exit_lk,\
	#di_id_lk_id_value_li_lk_cap_jam_dens_ffs_stan_dev_as_indicated_in_xml,di_key_id_phase_value_li_rout_prop,\
	#li_di_nsi_and_nsi_stages,di_phase_info,di_id_lk_value_li_orig_dest_nd_length_cap_mean_travel_param] 
	
	#dict_nd_info=dict, key = id node, value dict with node info having keys "li_output_links_id", "li_input_lk_id","type " 
	#(indicating if an intersection is/not signalised),"id" indicating the node id
	#dict_lk_info=dict, key = id link, value dict with link info,keys :'dest_nd_id','length','lanes','origin_nd_id','type','id'
	#di_id_node_li_entry_lk= dict, key=id nodes having entry links, value =list id entry links
	#di_s_and_ns_entry_links, dict, key=1 or 0 according to when the head node of the link is/not sigalised/nonsignalised,
	#di_id_node_li_exit_lk=dict, key=id nodes having exit links, value =list id exit links
	##di_id_lk_id_value_li_lk_cap_jam_dens_ffs_stan_dev_as_indicated_in_xml=dict, key=link id, 
	#value=[link capacity as defined in the xml file, jam density, free flow speed, stand deviat of free flow speed]
	#we adapt the boundary nodes existing in the xml file and indicated as "terminal", to the ".Q" convention indicated by -1
	#value=list link ids 
	#di_key_id_phase_value_li_rout_prop=dict with the rout prop (split ratios) of each phase
	#key= id phase, value=[...,[rout_prop_i,duree rout prop]...]
	li_nd_and_lk_info=Parse_network_xml_files.fct_creat_li_di_node_and_link_info_corrected(\
	val_name_file_to_read=v_name_file_to_read,\
	va_name_elem_networklist=v_name_elem_networklist,va_name_elem_nodelist=v_name_elem_nodelist,\
	va_name_elem_id_attrib=v_name_elem_id_attrib,va_name_elem_inputs=v_name_elem_inputs,va_name_elem_input=v_name_elem_input,\
	va_name_elem_link_id=v_name_elem_link_id,va_name_elem_outputs=v_name_elem_outputs,va_name_elem_output=v_name_elem_output,\
	va_name_elem_linklist=v_name_elem_linklist,\
	va_name_elem_node_id=v_name_elem_node_id,\
	va_name_origin_node_attribut=v_name_origin_node_attribut,\
	va_name_destination_node_attribut=v_name_destination_node_attribut,\
	va_name_attribut_origin_node_lk=v_name_attribut_origin_node_lk,\
	va_name_attribut_dest_node_lk=v_name_attribut_dest_node_lk,\
	va_name_attribut_type_node=v_name_attribut_type_node,\
	va_type_boundary_node=v_type_boundary_node,\
	va_name_output_links=v_name_attribut_li_output_link_id,\
	va_name_signalised_nd=v_attribut_name_signalised_node,\
	va_name_nonsignalised_nd=v_attribut_name_unsignalised_node,\
	va_indicator_sign_lk=v_indicator_sign_lk,\
	va_indicator_nonsign_lk=v_indicator_nonsign_lk,va_name_input_links=v_name_attribut_li_input_link_id,\
	va_name_origin_node=v_name_attribut_origin_node_lk,\
	va_name_elem_fundamentaldiagramset=v_name_elem_fundamentaldiagramset,\
	va_name_fundamentaldiagram=v_name_fundamentaldiagram,\
	va_name_attribut_capacity=v_name_attribut_capacity,va_name_attribut_jam_density=v_name_attribut_jam_density,\
	va_name_attribut_free_flow_speed=v_name_attribut_free_flow_speed,\
	va_name_attribut_std_dev_free_flow_speed=v_name_attribut_std_dev_free_flow_speed,\
	va_name_elem_splitratioset=v_name_elem_splitratioset,va_name_splitRatioProfile=v_name_splitRatioProfile,\
	va_name_duration_rout_prop_dt=v_name_duration_rout_prop_dt,\
	va_name_elem_splitratio=v_name_elem_splitratio,va_name_attrib_inputlink=v_name_attrib_inputlink,\
	va_name_attrib_outputlink=v_name_attrib_outputlink,\
	va_name_elem_signalList=v_name_elem_signalList,va_name_elem_signal=v_name_elem_signal,\
	va_name_attribute_node_id=v_name_attribute_node_id,va_name_attribute_nema=v_name_attribute_nema,\
	va_name_attribute_lk_id=v_name_attribute_lk_id,\
	va_name_attribute_lane_dest_lk=v_name_attribute_lane_dest_lk,\
	va_name_attribut_type_nsi=v_name_attribut_type_nsi,\
	va_name_attribut_type_si=v_name_attribut_type_si,\
	va_name_attribut_knob=v_name_attribut_knob,\
	va_round_prec=v_round_prec,va_t_unit=v_t_unit,\
	va_name_attribut_type_phase=v_name_attribut_type_phase,\
	va_name_indicator_right_turn=v_name_indicator_right_turn,\
	va_name_attribute_length=v_name_attribute_length,va_round_prec_lk_length=v_round_prec_lk_length,\
	va_round_prec_vit_moy=v_round_prec_vit_moy,\
	va_name_elem_ControllerSet=v_name_elem_ControllerSet,\
	va_name_attrib_node_id=v_name_attrib_node_id,va_name_attrib_row_id=v_name_attrib_row_id)
	#print(li_nd_and_lk_info[0].keys())
	#print(li_nd_and_lk_info[6])
	#import sys
	#sys.exit()


	#print("li_nd_and_lk_info[5]",li_nd_and_lk_info[4])
	#import sys
	#sys.exit()
	
	#creat liste args for "fct_write_fi_id_all_network_link_id_orig_dest_node_length_link_capacity_link_param_travel_duration"
	
	#li_valeurs_fct_write_fi_id_all_network_link_id_orig_dest_node_length_link_capacity_link=\
	#fct_creat_li_val_fct_write_fi_id_all_network_link_id_orig_dest_node_length_link_capacity_link_param_travel_durat(\
	#v_dict_lk_info_from_xml_file=li_nd_and_lk_info[1],\
	#val_name_origin_nd_id=v_name_attribut_origin_node_lk,val_name_dest_nd_id=v_name_attribut_dest_node_lk,val_name_length=v_name_length,\
	#val_di_id_link_value_li_lk_capacity_jam_density_ff_speed_stan_dev_from_xml=li_nd_and_lk_info[4],\
	#val_round_precision=v_round_precision,val_name_attribut_lanes=v_name_attribut_lanes,\
	#val_round_prec_calc_lk_travel_dur=va_round_prec_calc_lk_travel_dur)
	#print(li_valeurs_fct_write_fi_id_all_network_link_id_orig_dest_node_length_link_capacity_link)
	
		
	#we write the file  fi_id_all_network_link_id_orig_dest_node_length_link_capacity_link_param_travel_duration
	fct_write_fi_id_all_network_link_id_orig_dest_node_length_link_capacity_link_param_travel_duration(\
	name_file_to_write=folder_network_files+"/"+\
	File_names_network_model.val_file_name_id_all_network_link_id_orig_dest_node_length_link_capacity_link_param_travel_duration,\
	di_id_lk_value_li_orig_dest_nd_length_cap_mean_travel_param=li_nd_and_lk_info[8])
	
	#creat list args for fct_write_fi_id_internal_link_id_orig_dest_node	 A VERIFIER ENTRY/EXIT LINKS !!!!!!!!!!!!!
	li_valeurs_fct_write_fi_id_internal_link_id_orig_dest_node=\
	fct_creat_li_val_fct_write_fi_id_internal_link_id_orig_dest_node(v_dict_lk_info_from_xml_file=li_nd_and_lk_info[1],\
	val_name_origin_nd_id=v_name_attribut_origin_node_lk,val_name_dest_nd_id=v_name_attribut_dest_node_lk)
	
	# we write the file fi_id_internal_link_id_orig_dest_node
	fct_write_fi_id_internal_link_id_orig_dest_node(name_file_to_write=\
	folder_network_files+"/"+\
	File_names_network_model.val_file_name_id_internal_link_id_orig_dest_node,\
	list_valeurs=li_valeurs_fct_write_fi_id_internal_link_id_orig_dest_node)
	
	#we write the file fi_id_node_id_entry_links_to_network 
	fct_write_fi_id_node_id_entry_links_to_netw(name_file_to_write=\
	folder_network_files+"/"+\
	File_names_network_model.val_file_name_id_node_id_entry_links_to_network,\
	val_dict_id_nd_li_id_entry_links=li_nd_and_lk_info[2])
	
	#li_phrases_fi_ty_entry_lk=["id link (1st col), type link (1=signal, 0=non sign, 2nd col)"]
	#we write the file fi_id_entry_link_type_lk.txt
	#fct_write_fi_id_entry_lk_type_lk(name_file_to_write=\
	#folder_network_files+"/"+\
	#File_names_network_model.val_name_file_fi_id_entry_link_type_lk,
	#li_phrases=li_phrases_fi_ty_entry_lk,\
	#val_dict_s_and_ns_links=li_nd_and_lk_info[3])
	
	#we write the file id node id entering links to node
	#li_val fct_write_fi_id_node_id_entering_or_leaving_links_to_node
	li_val_fct_write_fi_id_node_id_entering_links_to_node=\
	fct_creat_li_val_fct_write_fi_id_node_id_entering_links_to_node(v_dict_nd_info_from_xml_file=li_nd_and_lk_info[0],\
	val_name_type=v_name_attribut_type_node,val_name_nd_terminal_type=v_type_boundary_node,\
	val_name_attribut_li_input_link_id=v_name_attribut_li_input_link_id)
	
	fct_write_fi_id_node_id_entering_or_leaving_links_to_node(name_file_to_write=\
	folder_network_files+"/"+\
	File_names_network_model.val_file_name_id_node_id_entering_links_to_node,\
	list_valeurs=li_val_fct_write_fi_id_node_id_entering_links_to_node)
	
	#we write file fi_id_node_id_leaving_links_from_node
	li_val_fct_creat_fct_write_fi_id_node_id_leaving_links_to_node=\
	fct_creat_li_val_fct_write_fi_id_node_id_leaving_links_to_node(v_dict_nd_info_from_xml_file=li_nd_and_lk_info[0],\
	val_name_type=v_name_attribut_type_node,\
	val_name_nd_terminal_type=v_type_boundary_node,val_name_attribut_li_output_link_id=v_name_attribut_li_output_link_id)
	
	fct_write_fi_id_node_id_entering_or_leaving_links_to_node(name_file_to_write=\
	folder_network_files+"/"+\
	File_names_network_model.val_file_name_id_node_id_leaving_links_from_node,\
	list_valeurs=li_val_fct_creat_fct_write_fi_id_node_id_leaving_links_to_node)
	
	# we write file fi_id_phases_max_queue_size_sat_flow_queue_type_param_travel_dur
	
	
	#we write the file id node id exit links from network
	fct_write_fi_id_node_id_exit_links_from_network(name_file_to_write=\
	folder_network_files+"/"+\
	File_names_network_model.val_file_name_id_node_id_exit_links_from_network,
	val_dict_id_nd_li_id_exit_links=li_nd_and_lk_info[3])
	
	#we write the file with the stages of each intersection
	
	
	#we write "fi_id_intersection_node_type_inters.txt"
	li_phrases=["node id (1st col), type inters. (1:sign., 0: non sign., 2nd col)"]
	
	li_val_fct_write_fi_id_node_type_node=fct_creat_li_val_fct_write_fi_id_intersection_nodes_type_inters(\
	v_dict_nd_info_from_xml_file=li_nd_and_lk_info[0],\
	val_name_type=v_name_attribut_type_node,\
	val_attribut_name_signalised_node=v_attribut_name_signalised_node,val_attribut_name_unsignalised_node=v_attribut_name_unsignalised_node)
	
	fct_write_fi_id_intersection_nodes_type_inters(name_file_to_write=\
	folder_network_files+"/"+\
	File_names_network_model.val_name_file_fi_id_node_type_node,\
	list_phrases=li_phrases,list_valeurs=li_val_fct_write_fi_id_node_type_node)
	
	#we write  file "fi_compatible_phases_nsi.txt"
	

	#a voir pour d'autres fichiers....
	
	#we write file fi_id_main_phase_id_side_phase.txt
	li_phrases_fi_id_main_phase_id_side_phase=["Id main phase (1-2 columns), id side phases (3-last colmsn)"]
	
	fct_write_fi_id_nd_id_minor_phase_id_prior_phase(name_file_to_write=\
	folder_network_files+"/"+\
	File_names_network_model.val_name_file_id_main_phase_id_side_phase,\
	list_phrases=li_phrases_fi_id_main_phase_id_side_phase,list_valeurs=[])
	
	#we write file fi_id_side_phase_id_main_phase.txt
	li_phrases_fi_id_side_phase_id_main_phase=["Id side phase (1-2 columns), id main phases (3-end colmsn)"]
	
	fct_write_fi_id_nd_id_minor_phase_id_prior_phase(name_file_to_write=\
	folder_network_files+"/"+\
	File_names_network_model.val_name_file_id_side_phase_id_main_phase,\
	list_phrases=li_phrases_fi_id_side_phase_id_main_phase,list_valeurs=[])
	
	#we write file fi_id_minor_phase_id_prior_phase.txt
	li_phrases_fi_id_minor_phase_id_prior_phase=["id minor phase (1,2,colmsn), id prior phase (4,5,.. colmns)"]
	
	fct_write_fi_id_nd_id_minor_phase_id_prior_phase(name_file_to_write=\
	folder_network_files+"/"+\
	File_names_network_model.val_name_file_id_minor_phase_id_prior_phase,\
	list_phrases=li_phrases_fi_id_minor_phase_id_prior_phase,list_valeurs=[])
	
	#we write file fi_id_prior_phase_id_minor_phase.txt
	li_phrases_fi_id_prior_phase_id_minor_phase=["id prior phase (1-2 columns), id minor phase (2,3 colmsn)"]
	
	fct_write_fi_id_nd_id_minor_phase_id_prior_phase(name_file_to_write=\
	folder_network_files+"/"+\
	File_names_network_model.val_name_file_id_prior_phase_id_minor_phase,\
	list_phrases=li_phrases_fi_id_prior_phase_id_minor_phase,list_valeurs=[])
	
	#we write file fi_id_que_position_presence_detector.txt
	fct_write_fi_id_que_position_presence_detector(name_file_to_write=
	folder_network_files+"/"+\
	File_names_network_model.val_name_file_id_que_position_pres_detector)
	
	#we write file fi_id_que_position_que_size_detector.txt
	fct_fi_id_que_position_que_size_detector(name_file_to_write=\
	folder_network_files+"/"+\
	File_names_network_model.val_name_file_fi_id_que_position_que_size_detector)
	
	#we write the files with the parameters fo each entry_internal link when stochastic travel times are employed
	fct_write_fi_matrix_mu_and_sigma_and_shift(\
	name_file_to_write_mu=\
	folder_network_files+"/"+\
	File_names_network_model.val_name_file_param_mu_entry_internal_link,\
	name_file_to_write_sigma=\
	folder_network_files+"/"+\
	File_names_network_model.val_name_file_param_sift_entry_internal_link,\
	name_file_to_write_shift=\
	folder_network_files+"/"+\
	File_names_network_model.val_name_file_param_shift_entry_internal_link,\
	list_valeurs_mu=[],\
	list_valeurs_sigma=[],\
	list_valeurs_shift=[])
	
	#we write files fi_mrp_id_phase_prob_dest_lk_nb.txt and 
	fct_write_files_rout_prob_and_duration(\
	name_file_to_write_rp=folder_network_files+"/"+File_names_network_model.val_name_file_mat_rp_id_phase_prob_dest_lk,\
	name_file_to_write_duration=folder_network_files+"/"+File_names_network_model.val_name_file_duration_each_rp_mat,\
	val_dict_key_id_phase_value_lis_li_rp_mat_and_duration=li_nd_and_lk_info[5])
	
	#we create the dicts with the cum rout prob 	
	#li_di_cum_rp_and_id_dest_lk=dict, key=id entry_internal link, value=[...,[list cum rout prob, id dest link],...]	
	li_di_cum_rp_and_id_dest_lk=fct_creat_dict_cum_rp_mat(\
	val_dict_rp_mat=li_nd_and_lk_info[5],val_considered_one_in_cum_fct=v_considered_one_in_cum_fct)
	
	
	#we write the file with the cum rout prob
	fct_write_file_cum_rout_prob(\
	name_file_to_write=folder_network_files+"/"+File_names_network_model.val_name_file_mat_rp_cum,\
	di_key_id_entry_intern_lk_value_lis_li_rout_prob_and_id_dest_lk=li_di_cum_rp_and_id_dest_lk)
	
	

	#we write file "fi_id_all_phases_max_queue_size_sat_flow_queue_type.txt"
	fct_write_file_fi_id_all_phases_max_queue_size_sat_flow_queue_type(\
	name_file_to_write=folder_network_files+"/"+File_names_network_model.val_file_name_id_all_phases_max_queue_size_and_sat_flow_queue_type,\
	di_phase_info=li_nd_and_lk_info[7])
	
	#print(li_nd_and_lk_info[6])
	#we write the file with the stages of nsi and si 
	fct_write_files_stages_si_and_nsi(\
	name_file_to_write_stages_nsi=folder_network_files+"/"+File_names_network_model.val_name_file_stages_each_non_signalised_inters,\
	name_file_to_write_stages_si=folder_network_files+"/"+File_names_network_model.val_name_file_stages_each_signalised_inters,\
	di_stages_nsi=li_nd_and_lk_info[6][0],di_stages_si=li_nd_and_lk_info[6][1])


	
	#FICHIERS MANQUANTS
	#fi_demand_param_entry_link.txt
	#"fi_compatible_phases_nsi.txt"
	
	
	#print(li_di_cum_rp_and_id_dest_lk)
	
	
	#print(li_di_cum_rp_and_di_id_dest_lk[0])
	#print()
	#print(li_di_cum_rp_and_di_id_dest_lk[1])
#*****************************************************************************************************************************************************************************************
#method reading a file and wriitng the same file with enumaration  of the line in the 1st column
def fct_reading_fi_mp_and_write_nb_line_and_values(name_file_read,name_file_write="fi_values_dif_mp_stages.txt"):
	file=open(name_file_read,"r")
	li=[]
	int=0
	for i in file.readlines():
		int+=1
		if int>1:
			a=i.rsplit()
			li.append([int-1,eval(a[0]),eval(a[1]),eval(a[2]),eval(a[3])])
	file.close()
	
	file1=open(name_file_write,"w")
	for j in li:
		for k in j:
			file1.write("%.2f\t"%(k))
		file1.write("\n")
	file1.close()
#*****************************************************************************************************************************************************************************************
#we write the file  fi_id_all_network_link_id_orig_dest_node_length_link_capacity_link



# we write the file fi_id_internal_link_id_orig_dest_node
#v_li_val=[
#[2,1,2],
#[3,2,3],
#[6,4,5],
#[7,5,6],
#[10,7,8],
#[11,8,9],
#[14,1,4],
#[15,4,7],
#[18,2,5],
#[19,5,8],
#[22,3,6],
#[23,6,9]
#]
#fct_write_fi_id_internal_link_id_orig_dest_node(name_file_to_write=File_names_network_model.val_file_name_id_internal_link_id_orig_dest_node,\
#list_valeurs=v_li_val)


#we write the file fi_id_node_id_entry_links_to_network
#v_li_val=[
#[1,1,13],
#[2,17],
#[3,21],
#[4,5],
#[7,9]
#]
#fct_write_fi_id_node_id_entering_or_leaving_links_to_node(name_file_to_write=\
#File_names_network_model.val_file_name_id_node_id_entry_links_to_network,list_valeurs=v_li_val)


#we write the file id node id entering links to node
#val_li_val=[
#[1,1,13],
#[2,2,17],
#[3,3,21],
#[4,5,14],
#[5,6,18],
#[6,7,22],
#[7,9,15],
#[8,10,19],
#[9,11,23]
##]
#fct_write_fi_id_node_id_entering_or_leaving_links_to_node(name_file_to_write=\
#File_names_network_model.val_file_name_id_node_id_entering_links_to_node,list_valeurs=val_li_val)

#we write file fi_id_node_id_leaving_links_from_node
#val_li_val=[
#[1,2,14],
#[2,3,18],
#[3,4,22],
#[4,6,15],
#[5,7,19],
#[6,8,23],
#[7,10,16],
#[8,11,20],
#[9,12,24]
#]
#fct_write_fi_id_node_id_entering_or_leaving_links_to_node(name_file_to_write=\
#File_names_network_model.val_file_name_id_node_id_leaving_links_from_node,list_valeurs=val_li_val)

#we write the file id entry link, id exit link, max que size, sat flow, que type, rout prop, param travel dur
#que type=1 if queue RT, 0 otherwise
# sat flow=0 if no permit Uturn,
#rout prop=0 if Uturn
#id entry link, id exit link, max que size, sat flow, que type, param travel dur
#v_li_val=[
#[1,2,-1,0.033,0,30],
#[1,14,-1,0,0,30],
#[13,2,-1,0.033,1,30],
#[13,14,-1,0.033,0,30],
#[2,3,-1,0.033,0,30],
#[2,18,-1,0,0,30],
#[17,3,-1,0.033,1,30],
#[17,18,-1,0.033,0,30],
#[3,4,-1,0.033,0,30],
#[3,22,-1,0,0,0,30],
#[21,4,-1,0.033,1,30],
#[21,22,-1,0.033,0,30],
#[5,6,-1,0.033,0,30],
#[5,15,-1,0,0,30],
#[14,6,-1,0.033,1,30],
#[14,15,-1,0.033,0,30],
#[6,7,-1,0.033,0,30],
#[6,19,-1,0,0,30],
#[18,7,-1,0.033,1,30],
#[18,19,-1,0.033,0,30],
#[7,8,-1,0.033,0,30],
#[7,23,-1,0,0,30],
#[22,8,-1,0.033,1,30],
#[22,23,-1,0.033,0,30],
#[9,10,-1,0.033,0,30],
#[9,16,-1,0,0,30],
#[15,10,-1,0.033,1,30],
#[15,16,-1,0.033,0,30],
#[10,11,-1,0.033,0,30],
#[10,20,-1,0,0,30],
#[19,11,-1,0.033,1,30],
#[19,20,-1,0.033,0,30],
#[11,12,-1,0.033,0,30],
#[11,24,-1,0,0,30],
#[23,12,-1,0.033,1,30],
#[23,24,-1,0.033,0,30]
#]

#ATTENTION !!!!!!!!!! METTRE , taux de  sat, 
#[20476,737,-1,0.033,0],[20476,742,-1,0.033,1]]
v_li_val=[\
[708,831,-1,0.042,0],[708,2371,-1,0.042,1],[708,23003,-1,0.042,0],[708,709,-1,0,0],\
[1497559,709,-1,0.042,0],[1497559,2371,-1,0.042,0],[1497559,23003,-1,0.042,1],[1497559,831,-1,0,0],\
[2370,23003,-1,0.028,0],[2370,831,-1,0.028,1],[2370,709,-1,0.028,0],[2370,2371,-1,0,0],\
[23004,831,-1,0.028,0],[23004,2371,-1,0.028,0],[23004,709,-1,0.028,1],[23004,23003,-1,0,0],\
[23003,24549,-1,0.084,0],[23003,23004,-1,0,0],\
[24550,23004,-1,0.084,1],[24550,24549,-1,0,0],\
[709,1206,-1,0.028,0],[709,732,-1,0.028,0],[709,1085,-1,0.028,1],[709,708,-1,0,0],\
[216323,1085,-1,0.07,0],[216323,708,-1,0.07,0],[216323,1206,-1,0.07,1],[216323,732,-1,0,0],\
[1204,732,-1,0.042,1],[1204,708,-1,0.042,0],[1204,1085,-1,0.042,0],[1204,1206,-1,0.042,0],\
[1205,708,-1,0.084,1],[1205,732,-1,0.084,0],[1205,1085,-1,0.084,0],[1205,1206,-1,0,0],\
[23006,24550,-1,0.042,0],[23006,1752109,-1,0.042,1],[23006,1752108,-1,0.042,0],[23006,23005,-1,0,0],\
[24549,1752109,-1,0.042,0],[24549,23005,-1,0.042,0],[24549,1752108,-1,0.042,1],[24549,24550,-1,0,1],\
[1752111,24550,-1,0.042,1],[1752111,1752108,-1,0.042,0],[1752111,23005,-1,0.042,0],[1752111,1752109,-1,0,0],\
[1752107,1752109,-1,0.028,0],[1752107,23005,-1,0.028,1],[1752107,24550,-1,0.028,0],[1752107,1752108,-1,0,0],\
[727,216323,-1,0.063,0],[727,16462,-1,0.063,1],[727,728,-1,0,0],\
[732,216323,-1,0.028,0],[732,16462,-1,0.028,0],[732,728,-1,0.028,0],\
[216305,728,1,0.063,0],[216305,216323,-1,0.063,1],[216305,16462,-1,0,0],\
[216440,1204,-1,0.098,0],[216440,20482,-1,0.098,1],[216440,23006,-1,0.098,0],[216440,1201,-1,0,0],\
[1085,1204,-1,0.042,0],[1085,20482,-1,0.042,0],[1085,23006,-1,0.042,1],[1085,1201,-1,0.042,0],\
[23005,1201,-1,0.053,1],[23005,1204,-1,0.053,0],[23005,20482,-1,0.053,0],[23005,23006,-1,0.053,0],
[20481,1204,-1,0.028,1],[20481,23006,-1,0.028,0],[20481,1201,-1,0.028,0],[20481,20482,-1,0,0],\
[728,217793,-1,0.042,0],[728,734,-1,0.042,0],[728,16467,-1,0.042,1],[728,727,-1,0,0],\
[733,217793,-1,0.042,1],[733,16467,-1,0.042,0],[733,727,-1,0.042,0],[733,734,-1,0,0],\
[16468,727,-1,0.042,0],[16468,734,-1,0.042,1],[16468,217793,-1,0.042,0],[16468,16467,-1,0,0],\
[217794,727,-1,0.014,1],[217794,16467,-1,0.014,0],[217794,734,-1,0.014,0],[217794,217793,-1,0,0],\
[20477,16468,-1,0.042,1],[20477,20481,-1,0.042,0],[20477,20478,-1,0,0],\
[16467,16468,-1,0.028,0],[16467,20481,-1,0.028,1],[16467,20478,-1,0.028,0],\
[20482,20478,-1,0.063,0],[20482,16468,-1,0.063,0],[20482,20481,-1,0,0],\
[734,738,-1,0.042,0],[734,2351,-1,0.042,0],[734,20471,-1,0.042,1],[734,733,-1,0,0],\
[737,20471,-1,0.056,0],[737,733,-1,0.056,0],[737,2351,-1,0.056,1],[737,738,-1,0,0],\
[2350,738,-1,0.042,0],[2350,733,-1,0.042,1],[2350,20471,-1,0.042,0],[2350,2351,-1,0,0],\
[20472,733,-1,0.028,0],[20472,738,-1,0.028,1],[20472,2351,-1,0.028,0],[20472,20471,-1,0,0],\
[20471,20477,-1,0.014,1],[20471,24565,-1,0.014,0],[20471,217802,-1,0.014,0],[20471,20472,-1,0,0],\
[20478,20472,-1,0.042,0],[20478,24565,-1,0.042,0],[20478,217802,-1,0.042,1],[20478,20477,-1,0,0],\
[24564,20472,-1,0.042,1],[24564,20477,-1,0.042,0],[24564,217802,-1,0.042,0],[24564,24565,-1,0,0],\
[217801,20472,-1,0.028,0],[217801,20477,-1,0.028,0],[217801,24565,-1,0.028,1],[217801,217802,-1,0,0],\
[24562,24564,-1,0.084,0],[24562,24563,-1,0,0],\
[24565,24563,-1,0.126,0],[24565,24564,-1,0,0],\
[20475,24562,-1,0.042,0],[20475,1721893,-1,0.042,1],[20475,20476,-1,0,0],\
[24563,20476,-1,0.063,0],[24563,1721893,-1,0.063,0],[24563,24562,-1,0,0],\
[1721892,20476,-1,0.021,0],[1721892,24562,-1,0.021,1],[1721892,1721893,-1,0,0],\
[738,742,-1,0.042,0],[738,20475,-1,0.042,1],[738,737,-1,0.042,0],\
[741,737,-1,0.084,0],[741,20475,-1,0.084,0],[741,742,-1,0,0],\
[20476,737,-1,0.063,0],[20476,742,-1,0.063,1],[20476,20475,-1,0,0]]

#fct_write_fi_id_phases_max_queue_size_sat_flow_queue_type(name_file_to_write=\
#File_names_network_model.val_file_name_id_all_phases_max_queue_size_and_sat_flow_queue_type,list_valeurs=v_li_val)


#we write the file id node id exit links from network
#val_li_val=[
#[3,4],
#[6,8],
#[9,12,24],
#[7,16],
#[8,20]
#]
#fct_write_fi_id_node_id_entering_or_leaving_links_to_node(name_file_to_write=\
#File_names_network_model.val_file_name_id_node_id_exit_links_from_network,list_valeurs=val_li_val)


#we write the file with the stages of each intersection
#val_list_phrases=["for each line, 1st column: id inters, next columns phases to actuate"]
#val_li_val=[
#[1,1,2],
#[1,13,14],
#[2,2,3],
#[2,17,18],
#[3,3,4],
#[3,21,22],
#[4,5,6],
#[4,14,15],
#[5,6,7],
#[5,18,19],
#[6,7,8],
#[6,22,23],
#[7,9,10],
#[7,15,16],
#[8,10,11],
#[8,19,20],
#[9,11,12],
#[9,23,24]
#]

#[[\
#[37593,23004,831,2370,709],[37593,23004,831,23004,2371],[37593,2370,23003,2370,709],[37593,2370,23003,23004,2371],\
#[37593,1497559,2371,708,23003],[37593,1497559,2371,1497559,709],[37593,708,831,708,23003,],[37593,708,831,1497559,709],\
#[49394,23003,24549],\
#[37605,1204,708,1204,1085,1205,732],[37605,1204,708,1204,1085,1204,1206],[37605,1205,1085,1205,732],[37605,1205,1085,1204,1206],\
#[37605,709,1206,216323,1085],[37605,709,1206,709,732],[37605,216323,708,216323,1085],[37605,216323,708,709,732],\
#[49395,1752107,24550,1752111,23005],[49395,1752107,24550,1752107,1752109],[49395,1752111,1752108,1752111,23005],[49395,1752111,1752108,1752107,1752109],\
#[49395,24549,1752109,23006,1752108],[49395,24549,1752109,24549,23005],[49395,23006,24550,23006,1752108],[49395,23006,24550,24549,23005],\
#[37607,216305,728],\
#[37607,732,16462,732,216323,732,728],\
#[37607,727,216323,732,728],\
#[37872,216440,23006,1085,20482,1085,1204],[37872,216440,23006,216440,1204],[37872,1085,1201,1085,20482,1085,1204],[37872,1085,1201,216440,1204],\
#[37872,23005,1204,20481,1201],[37872,23005,1204,23005,20482,23005,23006],[37872,20481,23006,20481,1201],[37872,20481,23006,23005,20482,23005,23006],\
#[37606,16468,727,217794,734],[37606,16468,727,16468,217793],[37606,217794,16467,217794,734],[37606,217794,16467,16468,217793],\
#[37606,728,217793,733,16467],[37606,728,217793,728,734],[37606,733,727,733,16467],[37606,733,727,728,734],\
#[48494,16467,16468,16467,20478],\
#[48494,20482,16468,20482,20478],\
#[48494,20477,20481,20482,20478],\
#[37610,20472,733,2350,738],[37610,20472,733,20472,2351],[37610,2350,20471,2350,738],[37610,2350,20471,20472,2351],
#[37610,734,2351,737,20471],[37610,734,2351,734,738],[37610,737,733,737,20471],[37610,737,733,734,738],\
#[48492,217801,20477,20471,24565], [48492,217801,20477,217801,20472],[48492,20471,217802,20471,24565], [48492,20471,217802,217801,20472],\
#[48492,20478,20472,24564,217802],  [48492,20478,20472,20478,24565], [48492,24564,20477,24564,217802],[48492,24564,20477,20478,24565],\
#[49954,24562,24564,24565,24563],\
#[48493,1721892,20476],\
#[48493,24563,1721893,24563,20476],\
#[48493,20475,24562,24563,20476],\
#[37612,20476,737],\
#[37612,741,737,741,20475],[37612,741,737,738,742,738,737]]

#stages pour FT, reseau SD
#v_li_val=[\
#[37593,23004,831,2370,709],[37593,2370,23003,23004,2371],\
#[37593,1497559,2371,708,23003],[37593,708,831,1497559,709],\
#[49394,23003,24549],\
#[37605,1204,708,1204,1085,1205,732],[37605,1205,1085,1204,1206],\
#[37605,709,1206,216323,1085],[37605,216323,708,709,732],\
#[49395,1752107,24550,1752111,23005],[49395,1752111,1752108,1752107,1752109],\
#[49395,24549,1752109,23006,1752108],[49395,23006,24550,24549,23005],\
#[37607,216305,728],\
#[37607,732,16462,732,216323,732,728],\
#[37607,727,216323,732,728],\
#[37872,216440,23006,1085,20482,1085,1204],[37872,1085,1201,216440,1204],\
#[37872,23005,1204,20481,1201],[37872,20481,23006,23005,20482,23005,23006],\
#[37606,16468,727,217794,734],[37606,217794,16467,16468,217793],\
#[37606,728,217793,733,16467],[37606,733,727,728,734],\
#[48494,16467,16468,16467,20478],\
#[48494,20482,16468,20482,20478],\
#[48494,20477,20481,20482,20478],\
#[37610,20472,733,2350,738],[37610,2350,20471,20472,2351],\
#[37610,734,2351,737,20471],[37610,737,733,734,738],\
#[48492,217801,20477,217801,20472], [48492,20471,217802,20471,24565],\
#[48492,20478,20472,24564,217802],[48492,24564,20477,20478,24565],\
#[49954,24562,24564,24565,24563],\
#[48493,1721892,20476],\
#[48493,24563,1721893,24563,20476],\
#[48493,20475,24562,24563,20476],\
#[37612,20476,737],\
#[37612,741,737,741,20475],[37612,741,737,738,742,738,737]
#]




#fct_write_file_intersection_stages(name_file_to_write=File_names_network_model.val_name_file_stages_each_signalised_inters,\
#list_phrases=val_list_phrases,list_valeurs=v_li_val)


#we write file "fi_id_all_phases_init_fin_detect_posit_nb_posit_captured.txt"
v_li_phrases=["id phase (1,2 column), id sensor (3rd column) final, intial detector position (4,5th column), nb posit captured by detect(6th column),case detect with limit position, \
or \
id phase (1,2 column), id sensor (3rd column), -1 (4th column) case when detector captures the whole que, or \
id phase (1,2 column), d sensor (3rd column), a positive number (4th column) indicating that the detecror captures\
 the whole que starting from the position indicated by the number- when a part of que is measured position 1 is indicated by 0 and so forth"]
v_li_val=[\
[708,831,1,-1],\
[708,2371,1,-1],\
[708,23003,1,-1],\
[708,709,1,-1],\
[1497559,709,1,-1],\
[1497559,2371,1,-1],\
[1497559,23003,1,-1],\
[1497559,831,1,-1],\
[2370,23003,1,-1],\
[2370,831,1,-1],\
[2370,709,1,-1],\
[2370,2371,1,-1],\
[23004,831,1,-1],\
[23004,2371,1,-1],\
[23004,709,1,-1],\
[23004,23003,1,-1],\
[23003,24549,1,-1],\
[23003,23004,1,-1],\
[24550,23004,1,-1],\
[24550,24549,1,-1],\
[709,1206,1,-1],\
[709,732,1,-1],\
[709,1085,1,-1],\
[709,708,1,-1],\
[216323,1085,1,-1],\
[216323,708,1,-1],\
[216323,1206,1,-1],\
[216323,732,1,-1],\
[1204,732,1,-1],\
[1204,708,1,-1],\
[1204,1085,1,-1],\
[1204,1206,1,-1],\
[1205,708,1,-1],\
[1205,732,1,-1],\
[1205,1085,1,-1],\
[1205,1206,1,-1],\
[23006,24550,1,-1],\
[23006,1752109,1,-1],\
[23006,1752108,1,-1],\
[23006,23005,1,-1],\
[24549,1752109,1,-1],\
[24549,23005,1,-1],\
[24549,1752108,1,-1],\
[24549,24550,1,-1],\
[1752111,24550,1,-1],\
[1752111,1752108,1,-1],\
[1752111,23005,1,-1],\
[1752111,1752109,1,-1],\
[1752107,1752109,1,-1],\
[1752107,23005,1,-1],\
[1752107,24550,1,-1],\
[1752107,1752108,1,-1],\
[727,216323,1,-1],\
[727,16462,1,-1],\
[727,728,1,-1],\
[732,216323,1,-1],\
[732,16462,1,-1],\
[732,728,1,-1],\
[216305,728,1,1],\
[216305,216323,1,-1],\
[216305,16462,1,-1],\
[216440,1204,1,-1],\
[216440,20482,1,-1],\
[216440,23006,1,-1],\
[216440,1201,1,-1],\
[1085,1204,1,-1],\
[1085,20482,1,-1],\
[1085,23006,1,-1],\
[1085,1201,1,-1],\
[23005,1201,1,-1],\
[23005,1204,1,-1],\
[23005,20482,1,-1],\
[23005,23006,1,-1],\
[20481,1204,1,-1],\
[20481,23006,1,-1],\
[20481,1201,1,-1],\
[20481,20482,1,-1],\
[728,217793,1,-1],\
[728,734,1,-1],\
[728,16467,1,-1],\
[728,727,1,-1],\
[733,217793,1,-1],\
[733,16467,1,-1],\
[733,727,1,-1],\
[733,734,1,-1],\
[16468,727,1,-1],\
[16468,734,1,-1],\
[16468,217793,1,-1],\
[16468,16467,1,-1],\
[217794,727,1,-1],\
[217794,16467,1,-1],\
[217794,734,1,-1],\
[217794,217793,1,-1],\
[20477,16468,1,-1],\
[20477,20481,1,-1],\
[20477,20478,1,-1],\
[16467,16468,1,-1],\
[16467,20481,1,-1],\
[16467,20478,1,-1],\
[20482,20478,1,-1],\
[20482,16468,1,-1],\
[20482,20481,1,-1],\
[734,738,1,-1],\
[734,2351,1,-1],\
[734,20471,1,-1],\
[734,733,1,-1],\
[737,20471,1,-1],\
[737,733,1,-1],\
[737,2351,1,-1],\
[737,738,1,-1],\
[2350,738,1,-1],\
[2350,733,1,-1],\
[2350,20471,1,-1],\
[2350,2351,1,-1],\
[20472,733,1,-1],\
[20472,738,1,-1],\
[20472,2351,1,-1],\
[20472,20471,1,-1],\
[20471,20477,1,-1],\
[20471,24565,1,-1],\
[20471,217802,1,-1],\
[20471,20472,1,-1],\
[20478,20472,1,-1],\
[20478,24565,1,-1],\
[20478,217802,1,-1],\
[20478,20477,1,-1],\
[24564,20472,1,-1],\
[24564,20477,1,-1],\
[24564,217802,1,-1],\
[24564,24565,1,-1],\
[217801,20472,1,-1],\
[217801,20477,1,-1],\
[217801,24565,1,-1],\
[217801,217802,1,-1],\
[24562,24564,1,-1],\
[24562,24563,1,-1],\
[24565,24563,1,-1],\
[24565,24564,1,-1],\
[20475,24562,1,-1],\
[20475,1721893,1,-1],\
[20475,20476,1,-1],\
[24563,20476,1,-1],\
[24563,1721893,1,-1],\
[24563,24562,1,-1],\
[1721892,20476,1,-1],\
[1721892,24562,1,-1],\
[1721892,1721893,1,-1],\
[738,742,1,-1],\
[738,20475,1,-1],\
[738,737,1,-1],\
[741,737,1,-1],\
[741,20475,1,-1],\
[741,742,1,-1],\
[20476,737,1,-1],\
[20476,742,1,-1],\
[20476,20475,1,-1]]

#fct_write_fi_id_all_phases_init_fin_detect_posit_nb_posit_captured(\
#name_file_to_write=File_names_network_model.val_file_name_id_all_phases_init_fin_detect_posit_nb_posit_captured,\
#list_phrases=v_li_phrases,list_valeurs=v_li_val)


#we read file _id_all_phases_init_fin_detect_posit_nb_posit_captured
#di=fct_read_fi_id_all_phases_init_fin_detect_posit_nb_posit_captured(\
#name_file_to_read="../../SMALL_NETWS/reseaux_3/SMALL_DATA_SD_sans_OD"+"/"+
#File_names_network_model.val_file_name_id_all_phases_init_fin_detect_posit_nb_posit_captured,\
#nb_comment_lines=1)
#di=fct_creation_dict_sensor_information_per_link(\
#val_name_file_to_read="../../SMALL_NETWS/reseaux_3/SMALL_DATA_SD_sans_OD"+"/"+
#File_names_network_model.val_file_name_id_all_phases_init_fin_detect_posit_nb_posit_captured,\
#val_nb_comment_lines=1)

#print(di[708])
#print(di[708,831])
#import sys
#sys.exit()


#we write the file "fi_mrp.txt"
#li_phrases=["Id phase (1-2 columns), prob of the phase (3rd column)"]
#li_valeurs=[
#[1,2,1],
#[13,2,0.5],
#[13,14,0.5],
#[2,3,1],
#[17,3,0.5],
#[17,18,0.5],
#[3,4,1],
#[21,4,0.5],
#[21,22,0.5],
#[5,6,1],
#[14,6,0.5],
#[14,15,0.5],
#[6,7,1],
#[18,7,0.5],
#[18,19,0.5],
#[7,8,1],
#[22,8,0.5],
#[22,23,0.5],
#[9,10,1],
#[15,10,0.5],
#[15,16,0.5],
#[10,11,1],
#[19,11,0.5],
#[19,20,0.5],
#[11,12,1],
#[23,12,0.5],
#[23,24,0.5]
#]


#
#li_valeurs=[\
#[708,831,0.33],[708,2371,0.33],[708,23003,0.33],\
#[1497559,709,0.33],[1497559,2371,0.33],[1497559,23003,0.33],\
#[2370,23003,0.33],[2370,831,0.33],[2370,709,0.33],\
#[23004,831,0.33],[23004,2371,0.33],[23004,709,0.33],\
#[23003,24549,1],\
#[24550,23004,1],\
#[709,1206,0.33],[709,732,0.33],[709,1085,0.33],\
#[216323,1085,0.33],[216323,708,0.33],[216323,1206,0.33],\
#[1204,732,0.25],[1204,708,0.25],[1204,1085,0.25],[1204,1206,0.25],\
#[1205,708,0.33],[1205,732,0.33],[1205,1085,0.33],\
#[23006,24550,0.33],[23006,1752109,0.33],[23006,1752108,0.33],\
#[24549,1752109,0.33],[24549,23005,0.33],[24549,1752108,0.33],\
#[1752111,24550,0.33],[1752111,1752108,0.33],[1752111,23005,0.33],\
#[1752107,1752109,0.33],[1752107,23005,0.33],[1752107,24550,0.33],\
#[727,216323,0.5],[727,16462,0.5],\
#[732,216323,0.33],[732,16462,0.33],[732,728,0.33],\
#[216305,728,0.5],[216305,216323,0.5],\
#[216440,1204,0.33],[216440,20482,0.33],[216440,23006,0.33],\
#[1085,1204,0.25],[1085,20482,0.25],[1085,23006,0.25],[1085,1201,0.25],\
#[23005,1201,0.25],[23005,1204,0.25],[23005,20482,0.25],[23005,23006,0.25],
#[20481,1204,0.33],[20481,23006,0.33],[20481,1201,0.33],\
#[728,217793,0.33],[728,734,0.33],[728,16467,0.33],\
#[733,217793,0.33],[733,16467,0.33],[733,727,0.33],\
#[16468,727,0.33],[16468,734,0.33],[16468,217793,0.33],\
#[217794,727,0.33],[217794,16467,0.33],[217794,734,0.33],\
#[20477,16468,0.5],[20477,20481,0.5],\
#[16467,16468,0.33],[16467,20481,0.33],[16467,20478,0.33],\
#[20482,20478,0.5],[20482,16468,0.5],\
#[734,738,0.33],[734,2351,0.33],[734,20471,0.33],\
#[737,20471,0.33],[737,733,0.33],[737,2351,0.33],\
#[2350,738,0.33],[2350,733,0.33],[2350,20471,0.33],\
#[20472,733,0.33],[20472,738,0.33],[20472,2351,0.33],\
#[20471,20477,0.33],[20471,24565,0.33],[20471,217802,0.33],\
#[20478,20472,0.33],[20478,24565,0.33],[20478,217802,0.33],\
#[24564,20472,0.33],[24564,20477,0.33],[24564,217802,0.33],\
#[217801,20472,0.33],[217801,20477,0.33],[217801,24565,0.33],\
#[24562,24564,1],\
#[24565,24563,1],\
#[20475,24562,0.5],[20475,1721893,0.5],\
#[24563,20476,0.5],[24563,1721893,0.5],\
#[1721892,20476,0.5],[1721892,24562,0.5],\
#[738,742,0.33],[738,20475,0.33],[738,737,0.33],\
#[741,737,0.5],[741,20475,0.5],\
#[20476,737,0.5],[20476,742,0.5]]


#fct_write_fi_id_phase_prob_dest_lk(name_file_to_write=File_names_network_model.val_name_file_mat_rp_id_phase_prob_dest_lk,\
#list_phrases=li_phrases,list_valeurs=li_valeurs) #A VOIR LES FCT D'ECRIT POUR LE XML VERSION !!!!




#val_li_phrases=[Id phase (1-2 columns), prob of the phase 2nd period (3rd column) and so on. The initial values of the rout prob are in file ``fi_mrp.txt''] 
#val_li_rout_prob=[\	 
#708,	831.00	0.5	0.2
#708,	2371.00	0.2	0.5
#708,	23003.00	0.3	0.3	
#1497559,	709.00	0.1	 0.50	
#1497559,	2371.00	0.50	 0.1	
#1497559,	23003.00	0.4	 0.4	
#2370,	23003.00	0.33	 0.13	
#2370,	831.00	0.13  0.54	
#2370,	709.00	0.54	 0.33
#23004,	831.00	0.23	 0.54
#23004,	2371.00	0.23	 0.23
#23004,	709.00	0.54	 0.23
#23003,	24549.00	1.00	 1.00
#24550,	23004.00	1.00  1.00	
#709,	1206.00	0.4	0.5	
#709,	732.00	0.5	0.4	
#709,	1085.00	0.1	0.1	
#216323,	1085.00	0.17	 0.4
#216323,	708.00	0.43	 0.17
#216323,	1206.00	0.4 	 0.43
#1204,	732.00	0.2  0.1	
#1204,	708.00	0.2  0.2
#1204,	1085.00	0.1  0.2	
#1204,	1206.00	0.5 	0.23	
#1205,	708.00	0.23  0.54	
#1205,	732.00	0.23	 0.23
#1205,	1085.00	0.54	 0.23
#23006,	24550.00	0.1 0.5	
#23006,	1752109  0.5 0.4
#23006, 1752108.00 0.4 0.1	
#24549,	1752109.00	0.14  0.16	
#24549,	23005.00	0.16 	0.7	
#24549,	1752108.00	0.7 	0.14	
#1752111,	24550.00	0.7	0.15	
#1752111,	1752108.00	0.15 	0.7	
#1752111,	23005.00	0.15 	0.15	
#1752107,	1752109.00	0.15	0.15
#1752107,	23005.00	0.7 0.15 	0.7
#1752107,	24550.00	0.15	 0.15
#727,	216323.00	0.20	 0.8
#727,	16462.00	0.80	 0.2
#732,	216323.00	0.4 0.4	
#732,	16462.00	0.4 0.2
#732,	728.00	0.2 0.4	
#216305,	728.00	0.9 0.1	
#216305,	216323.00	0.1 0.9	
#216440,	1204.00	0.5 0.25	
#216440,	20482.00	0.25 0.5	
#216440,	23006.00	0.25	0.25
#1085,	1204.00	0.6 0.15	
#1085,	20482.00	0.1 0.15	
#1085,	23006.00	0.15 0.4	
#1085,	1201.00	0.15 0.3	
#23005,	1201.00	0.15	0.6
#23005,	1204.00	0.35	0.1
#23005,	20482      0.15	 0.2
#23005,	23006.00	0.35 0.1	
#20481,	1204.00	0.2
#20481,	23006.00	0.4	
#20481,	1201.00	0.4	
#728,	217793.00	0.1	
#728,	734.00	0.1
#728,	16467.00	0.8
#733,	217793.00	0.8	
#733,	16467.00	0.1	
#733,	727.00	0.1	
#16468,	727.00	0.4
#16468,	734.00	0.4
#16468,	217793.00	0.2
#217794,	727.00	0.2	
#217794,	16467.00	0.4	
#217794,	734.00	0.4
#20477,	16468.00	0.8	
#20477,	20481.00	0.2	
#16467,	16468.00	0.7
#16467,	20481.00	0.2
#16467,	20478.00	0.1	
#20482,	20478.00	0.6	
#20482,	16468.00	0.4
#734,	738.00	0.2	
#734,	2351.00	0.3
#734,	20471.00,	0.5	
#737,	20471.00	,0.3	
#737,	733.00	,0.1	
#737,	2351.00,	0.6
#2350,	738.00	0.8	
#2350,	733.00,	0.1	
#2350,	20471.00,	0.1
#20472,	733.00,	0.4	
#20472,	738.00,	0.1	
#20472,	2351.00,	0.5
#20471,	20477.00,	0.3	
#20471,	24565.00,	0.2
#20471,	217802.00	,0.5
#20478,	20472.00	,0.4	
#20478,	24565.00,	0.3	
#20478,	217802.00 ,	0.3],
#24564,	20472.00,	0.3],	
#24564,	20477.00,	0.3],
#24564,	217802.00,	0.4],	
#217801,	20472.00,	0.8],
#217801,	20477.00	0.1],,	
#217801,	24565.00	,0.1],	
#24562,	24564.00	,1.00],	
#24565,	24563.00	,],1.00	
#20475,	24562.00	,0.3],	
#20475,	1721893.00	,0.7],	
#24563,	20476.00,	0.7],	
#24563,	1721893.00,	0.3	],
#1721892,	20476.00,	0.4	],
#1721892,	24562.00,	0.6],	
#738,	742.00,	0.3],	
#738,	20475.00,	0.6],
#738	737.00,	0.1],
#741,	737.00,	0.2],
#741,	20475.00	,0.8],	
#20476,	737.00,	0.8],
#20476,	742.00,	0.2]








#we calculate the dict with the rout prob
#di_key_id_phase_value_cum_rp=fct_creat_dict_cum_rp_mat_from_text_file(val_name_file_rout_prop_to_read=\
#"fi_mrp.txt",nb_comment_lines=1,val_considered_one_in_cum_fct=0.97)


#we write  the file with the cum values of the rout prob
#fct_write_file_cum_rout_prob_from_text_file(name_file_to_write=File_names_network_model.val_name_file_mat_rp_cum,\
#di_key_id_entry_intern_lk_value_lis_li_rout_prob_and_id_dest_lk=di_key_id_phase_value_cum_rp,\
#li_phases=["id phase (1-2 columns), cum rout prob (next colm)"])



#we write the cum values for the rout prop and the corresponding files for the  link ids
# A VOIR LES FCT D'ECRIT POUR LE XML VERSION !!!!
#fct_write_li_files_fi_id_phase_val_cum_funct_rout_prop_and_fi_id_entry_intern_lk_id_dest_lk(va_name_folder_mrp=\
#"../../SMALL_NETWS_2/SMALL_DATA_9NDS/"+File_names_network_model.val_name_folder_rout_prob,\
#v_nb_fi_mrp_id_phase_prob_dest_lk=1,va_nb_comment_lines=1,va_considered_one_in_cum_fct=0.98) 
#di_cum_mrp=fct_creat_dict_cum_rp_mat_from_text_file(val_name_file_rout_prop_to_read="./fi_mrp.txt",\
#nb_comment_lines=1,val_considered_one_in_cum_fct=0.97)

#fct_write_file_cum_rout_prob(name_file_to_write=File_names_network_model.val_name_file_cum_mod,\
#di_key_id_entry_intern_lk_value_lis_li_rout_prob_and_id_dest_lk=di_cum_mrp,\
#li_phrases=["id phase (1-2 columns), cum rout prob (next colm)"])









#we write "fi_id_intersection_node_type_inters.txt"
#li_phrases=["node id (1st col), type inters. (1:sign., 0: non sign., 2nd col)"]
#li_valeurs=[[1,1],[2,1],[3,0],[4,1],[5,1],[6,1],[7,0],[8,1],[9,1]]
#fct_write_fi_id_intersection_nodes_type_inters(name_file_to_write=File_names_network_model.val_name_file_fi_id_intersection_node_type_inters,\
#list_phrases=li_phrases,list_valeurs=li_valeurs)

#li=fct_read_fi_id_intersection_node_type_inters(name_file_to_read=File_names_network_model.val_name_file_fi_id_intersection_node_type_inters,\
#nb_comment_lines=1)
#print(li[0])
#print(li[1])


#write file fi_id_entry_link_type_lk.txt
#li_phrases=["id link (1st col), type link (1=signal, 0=non sign, 2nd col)"]
#li_valeurs=[[1,1],[5,0],[9,0],[13,0],[17,1],[21,0]]
#fct_write_fi_id_entry_link_type_lk(name_file_to_write=File_names_network_model.val_name_file_fi_id_entry_link_type_lk,\
#list_phrases=li_phrases,list_valeurs=li_valeurs)

#we read file  file fi_id_entry_link_type_lk
#di=fct_read_ffi_id_entry_link_type_lk(name_file_to_read=File_names_network_model.val_name_file_fi_id_entry_link_type_lk,nb_comment_lines=1)
#print(di)


#we write  file fi_demand_param_entry_link
#val_list_valeurs=[\
#[1497559, 0.007],\
#[2370,0.009],\
#[1205,0.028],\
#[1721892,0.009],\
#[1752111,0.002],\
#[1752107,0.005],\
#[216305,0.01],\
#[216440,0.063],\
#[217794,0.001],\
#[2350, 0.015],\
#[217801,0.002],\
#[741,0.018]
#]
#fct_write_fi_demand_param_entry_link(name_file_to_write=File_names_network_model.val_file_name_demand_param_entry_link,list_valeurs=val_list_valeurs)


#we write  file fi_id_node_type_node
#val_list_phrases=["node id (1st col), type inters. (1:sign., 0: non sign., 2nd col)"]
#val_list_valeurs=[37593,49394,37605,49395,37607,37872,48494,37606,37610,48492,49954,48493,37612]
#fct_write_fi_id_node_type_node_cas_nds_sign(name_file_to_write=File_names_network_model.val_name_file_fi_id_node_type_node,\
#list_phrases=val_list_phrases,list_valeurs=val_list_valeurs)








#we write the file with the compatible stages of each non-signalised itnersection
#li_phrases=["id non sgnalised intersection node (1st col), id phases (( 2nd, 3rd) and next col), RT are not included"]
#li_valeurs=[[3,3,4,21,22],[7,9,10],[7,15,16]]
#li_valeurs=[[3,3,4],[3,21,22],[7,9,10],[7,15,16]]
#fct_write_file_compatible_phases_nsi(name_file_to_write=File_names_network_model.val_name_file_compatible_phases_nsi,\
#list_phrases=li_phrases,list_valeurs=li_valeurs)

#we read the file with the compatible stages of each non-signalised itnersection
#di=fct_read_file_compatible_phases_nsi(name_file_read=File_names_network_model.val_name_file_compatible_phases_nsi,nb_comment_lines=1)
#print(di)





#we write the file with the parameters of the FT  control
lis_phrases=[["id nd (1st colm),id stage (2nd colm, if id=0 it is rd cleat), actuat durat (3rd colm),cycle duration (5th colm), 1st line"],\
["for a given inersection the order of stage id is related to  their priority within the cycle" ]]
#lis_valeurs=[
#[1,1,26,62],
#[1,0,5,62],
#[1,2,26,62],
#[1,0,5,62],
#[2,1,26,62],
#[2,0,5,62],
#[2,2,26,62],
#[2,0,5,62],
#[3,1,26,62],
#[3,0,5,62],
#[3,2,26,62],
#[3,0,5,62],
#[4,1,26,62],
#[4,0,5,62],
#[4,2,26,62],
#[4,0,5,62],
#[5,1,26,62],
#[5,0,5,62],
#[5,2,26,62],
#[5,0,5,62],
#[6,1,26,62],
#[6,0,5,62],
#[6,2,26,62],
#[6,0,5,62],
#[7,1,26,62],
#[7,0,5,62],
#[7,2,26,62],
#[7,0,5,62],
#[8,1,26,62],
#[8,0,5,62],
#[8,2,26,62],
#[8,0,5,62],
#[9,1,26,62],
#[9,0,5,62],
#[9,2,26,62],
#[9,0,5,62]
#]
lis_valeurs=[\
[37593,1,26.2,90],\
[37593,0,2,90],\
[37593,2,18.9,90],\
[37593,0,2,90],\
[37593,3,17.1,90],\
[37593,0,2,90],\
[37593,4,19.8,90],\
[37593,0,2,90],\
[49394,1,20.5,90],\
[49394,0,2,90],\
[49394,1,20.5,90],\
[49394,0,2,90],\
[49394,1,20.5,90],\
[49394,0,2,90],\
[49394,1,20.5,90],\
[49394,0,2,90],\
[37605,1,19.8,90],\
[37605,0,2,90],\
[37605,2,18,90],\
[37605,0,2,90],\
[37605,3,21.7,90],\
[37605,0,2,90],\
[37605,4,22.5,90],\
[37605,0,2,90],\
[49395,1,24.3,90],\
[49395,0,2,90],\
[49395,2,5.5,90],\
[49395,0,2,90],\
[49395,3,26.1,90],\
[49395,0,2,90],\
[49395,4,26.1,90],\
[49395,0,2,90],\
[37607,1,27,90],\
[37607,0,2.6,90],\
[37607,2,36,90],\
[37607,0,2.7,90],\
[37607,3,19,90],\
[37607,0,2.8,90],\
[37872,1,36,90],\
[37872,0,2,90],\
[37872,2,24.3,90],\
[37872,0,2,90],\
[37872,3,8.9,90],\
[37872,0,2,90],\
[37872,4,12.8,90],\
[37872,0,2,90],\
[37606,1,27,90],\
[37606,0,2,90],\
[37606,2,18,90],\
[37606,0,2,90],\
[37606,3,15.3,90],\
[37606,0,2,90],\
[37606,4,21.7,90],\
[37606,0,2,90],\
[48494,1,36,90],\
[48494,0,2.6,90],\
[48494,2,24.3,90],\
[48494,0,2.7,90],\
[48494,3,21.7,90],\
[48494,0,2.8,90],\
[37610,1,36,90],\
[37610,0,2,90],\
[37610,2,17.2,90],\
[37610,0,2,90],\
[37610,3,16.2,90],\
[37610,0,2,90],\
[37610,4,12.6,90],\
[37610,0,2,90],\
[48492,1,21.7,90],\
[48492,0,2,90],\
[48492,2,33.3,90],\
[48492,0,2,90],\
[48492,3,13.5,90],\
[48492,0,2,90],\
[48492,4,13.5,90],\
[48492,0,2,90],\
[49954,1,20.5,90],\
[49954,0,2,90],\
[49954,1,20.5,90],\
[49954,0,2,90],\
[49954,1,20.5,90],\
[49954,0,2,90],\
[49954,1,20.5,90],\
[49954,0,2,90],\
[48493,1,36,90],\
[48493,0,2.6,90],\
[48493,2,18,90],\
[48493,0,2.7,90],\
[48493,3,28,90],\
[48493,0,2.8,90],\
[37612,1,45,90],\
[37612,0,2.6,90],\
[37612,2,18,90],\
[37612,0,2.7,90],\
[37612,3,19,90],\
[37612,0,2.8,90]\
]

#fct_write_file_parameters_ft_control(name_file_to_write=File_Sim_Name_Module_Files.val_name_file_values_ft_control,li_valeurs=lis_valeurs,\
#li_phrases=lis_phrases)






#we write the file with the parameters of the FT offset control
#lis_phrases=[[" offset values - column related to the node  id according to the order of the lines showing stage duration, 1st line"],["id nd (1st colm),\
##id stage (2nd colm, if id=0 it is rd cleat), actuat durat (3rd colm),t end cycle(5th colm), 2nd line"],\
#["for a given inersection the order of stage id is related to  their priority within the cycle" ]]
#lis_valeurs=[[0,10],[1,1,15,60],[1,0,3,60],[1,2,35,60],[1,0,7,60],[2,1,25,60],[2,0,5,60],[2,2,25,5,60],[2,0,5,60]]
#lis_valeurs=[[-15,0,10],[1,1,15,60],[1,0,3,60],[1,2,35,60],[1,0,7,60],[2,1,15,60],[2,0,3,60],[2,2,35,60],[2,0,7,60],[3,1,25,60],[3,0,5,60],[3,2,25,5,60],[3,0,5,60]]
#fct_write_file_parameters_ft_control(name_file_to_write=File_Sim_Name_Module_Files.val_name_file_values_ft_control,li_valeurs=lis_valeurs,\
#li_phrases=lis_phrases)


#we read the file with the parameters of the FT control
#li=fct_reading_file_parameters_FT_control(name_file_to_read="./Control_Param_Files"+"/"+\
#File_Sim_Name_Module_Files.val_name_file_values_ft_control,nb_comment_lines=3,v_nb_line_master_nd_info=4)
#print(li)

#we write the parameters of MP
#val_li_phrases=[" id node (1st cllm), stage actuation duration idle time L (next colms),  cycle duration T  (last col)"]
#li_valeurs=[\
#[37593,40,5,40,5,90],\
#[49394,40,5,40,5,90],\
#[37605,40,5,40,5,90],\
#[49395,40,5,40,5,90],\
#[37607,40,5,40,5,90],\
#[37872,40,5,40,5,90],\
#[48494,40,5,40,5,90],\
#[37606,40,5,40,5,90],\
#[37610,40,5,40,5,90],\
#[48492,40,5,40,5,90],\
#[49954,40,5,40,5,90],\
#[48493,40,5,40,5,90],\
#[37612,40,5,40,5,90]]
#li_valeurs=[\
#[37593,20.5,2,20.5,2,20.5,2,20.5,2,90],
#[49394,20.5,2,20.5,2,20.5,2,20.5,2,90],
#[37605,20.5,2,20.5,2,20.5,2,20.5,2,90],
#[49395,20.5,2,20.5,2,20.5,2,20.5,2,90],
#[37607,20.5,2,20.5,2,20.5,2,20.5,2,90],
#[37872,20.5,2,20.5,2,20.5,2,20.5,2,90],
#[48494,20.5,2,20.5,2,20.5,2,20.5,2,90],
#[37606,20.5,2,20.5,2,20.5,2,20.5,2,90],
#[37610,20.5,2,20.5,2,20.5,2,20.5,2,90],
#[48492,20.5,2,20.5,2,20.5,2,20.5,2,90],
#[49954,20.5,2,20.5,2,20.5,2,20.5,2,90],
#[48493,20.5,2,20.5,2,20.5,2,20.5,2,90],
#[37612,20.5,2,20.5,2,20.5,2,20.5,2,90]]

#li_valeurs=[\
#[37593,13.6,1.3,13.6,1.3,13.6,1.3,13.6,1.3,13.6,1.3,14,1.5,90],
#[49394,13.6,1.3,13.6,1.3,13.6,1.3,13.6,1.3,13.6,1.3,14,1.5,90],
#[37605,13.6,1.3,13.6,1.3,13.6,1.3,13.6,1.3,13.6,1.3,14,1.5,90],
#[49395,13.6,1.3,13.6,1.3,13.6,1.3,13.6,1.3,13.6,1.3,14,1.5,90],
#[37607,13.6,1.3,13.6,1.3,13.6,1.3,13.6,1.3,13.6,1.3,14,1.5,90],
#[37872,13.6,1.3,13.6,1.3,13.6,1.3,13.6,1.3,13.6,1.3,14,1.5,90],
#[48494,13.6,1.3,13.6,1.3,13.6,1.3,13.6,1.3,13.6,1.3,14,1.5,90],
#[37606,13.6,1.3,13.6,1.3,13.6,1.3,13.6,1.3,13.6,1.3,14,1.5,90],
#[37610,13.6,1.3,13.6,1.3,13.6,1.3,13.6,1.3,13.6,1.3,14,1.5,90],
#[48492,13.6,1.3,13.6,1.3,13.6,1.3,13.6,1.3,13.6,1.3,14,1.5,90],
#[49954,13.6,1.3,13.6,1.3,13.6,1.3,13.6,1.3,13.6,1.3,14,1.5,90],
#[48493,13.6,1.3,13.6,1.3,13.6,1.3,13.6,1.3,13.6,1.3,14,1.5,90],
#[37612,13.6,1.3,13.6,1.3,13.6,1.3,13.6,1.3,13.6,1.3,14,1.5,90]]
#li_valeurs=[\
#[37593,10,1,10,1,10,1,10,1,10,1,10,1,10,1,12,1,90],
#[49394,10,1,10,1,10,1,10,1,10,1,10,1,10,1,12,1,90],
#[37605,10,1,10,1,10,1,10,1,10,1,10,1,10,1,12,1,90],
#[49395,10,1,10,1,10,1,10,1,10,1,10,1,10,1,12,1,90],
#[37607,10,1,10,1,10,1,10,1,10,1,10,1,10,1,12,1,90],
#[37872,10,1,10,1,10,1,10,1,10,1,10,1,10,1,12,1,90],
#[48494,10,1,10,1,10,1,10,1,10,1,10,1,10,1,12,1,90],
#[37606,10,1,10,1,10,1,10,1,10,1,10,1,10,1,12,1,90],
#[37610,10,1,10,1,10,1,10,1,10,1,10,1,10,1,12,1,90],
#[48492,10,1,10,1,10,1,10,1,10,1,10,1,10,1,12,1,90],
#[49954,10,1,10,1,10,1,10,1,10,1,10,1,10,1,12,1,90],
#[48493,10,1,10,1,10,1,10,1,10,1,10,1,10,1,12,1,90],
#[37612,10,1,10,1,10,1,10,1,10,1,10,1,10,1,12,1,90]]

#li_valeurs=[\
#[37593,8.2,0.8,8.2,0.8,8.2,0.8,8.2,0.8,8.2,0.8,8.2,0.8,8.2,0.8,8.2,0.8,8.2,0.8,8.2,0.8,90],
#[49394,8.2,0.8,8.2,0.8,8.2,0.8,8.2,0.8,8.2,0.8,8.2,0.8,8.2,0.8,8.2,0.8,8.2,0.8,8.2,0.8,90],
#[37605,8.2,0.8,8.2,0.8,8.2,0.8,8.2,0.8,8.2,0.8,8.2,0.8,8.2,0.8,8.2,0.8,8.2,0.8,8.2,0.8,90],
#[49395,8.2,0.8,8.2,0.8,8.2,0.8,8.2,0.8,8.2,0.8,8.2,0.8,8.2,0.8,8.2,0.8,8.2,0.8,8.2,0.8,90],
#[37607,8.2,0.8,8.2,0.8,8.2,0.8,8.2,0.8,8.2,0.8,8.2,0.8,8.2,0.8,8.2,0.8,8.2,0.8,8.2,0.8,90],
#[37872,8.2,0.8,8.2,0.8,8.2,0.8,8.2,0.8,8.2,0.8,8.2,0.8,8.2,0.8,8.2,0.8,8.2,0.8,8.2,0.8,90],
#[48494,8.2,0.8,8.2,0.8,8.2,0.8,8.2,0.8,8.2,0.8,8.2,0.8,8.2,0.8,8.2,0.8,8.2,0.8,8.2,0.8,90],
#[37606,8.2,0.8,8.2,0.8,8.2,0.8,8.2,0.8,8.2,0.8,8.2,0.8,8.2,0.8,8.2,0.8,8.2,0.8,8.2,0.8,90],
#[37610,8.2,0.8,8.2,0.8,8.2,0.8,8.2,0.8,8.2,0.8,8.2,0.8,8.2,0.8,8.2,0.8,8.2,0.8,8.2,0.8,90],
#[48492,8.2,0.8,8.2,0.8,8.2,0.8,8.2,0.8,8.2,0.8,8.2,0.8,8.2,0.8,8.2,0.8,8.2,0.8,8.2,0.8,90],
#[49954,8.2,0.8,8.2,0.8,8.2,0.8,8.2,0.8,8.2,0.8,8.2,0.8,8.2,0.8,8.2,0.8,8.2,0.8,8.2,0.8,90],
#[48493,8.2,0.8,8.2,0.8,8.2,0.8,8.2,0.8,8.2,0.8,8.2,0.8,8.2,0.8,8.2,0.8,8.2,0.8,8.2,0.8,90],
#[37612,8.2,0.8,8.2,0.8,8.2,0.8,8.2,0.8,8.2,0.8,8.2,0.8,8.2,0.8,8.2,0.8,8.2,0.8,8.2,0.8,90]]

#fct_write_file_parameters_ft_control(name_file_to_write=File_Sim_Name_Module_Files.val_name_file_values_mp_control,li_phrases=val_li_phrases,\
#li_valeurs=li_valeurs)



#we read the file with the parameters of the MP control
#di=fct_reading_file_parameters_MP_control(name_file_to_read="./Control_Param_Files"+"/"+\
#File_Sim_Name_Module_Files.val_name_file_values_mp_control,nb_comment_lines=1)
#print("di",di)

#we read the file wirh the parem of pressure stage actuat contror
#di=fct_reading_file_psd_control(name_file_to_read="./Control_Param_Files"+"/"+\
#File_Sim_Name_Module_Files.val_name_File_Pres_Stage_Duration_Control_Alg_Param,nb_comment_lines=1)
#print("di",di)


#di_key_id_phase_value_cum_rp=fct_creat_dict_cum_rp_mat_from_text_file(val_name_file_rout_prop_to_read=\
#"/Users/jennie/Desktop/travail_vsim_int/sim_vint_4/SMALL_NETWS_2/SMALL_round_about_jennie/fi_mrp.txt",\
#nb_comment_lines=1,val_considered_one_in_cum_fct=0.97)

#we write  the file with the cum values of the rout prob
#fct_write_file_cum_rout_prob_from_text_file(name_file_to_write=File_names_network_model.val_name_file_mat_rp_cum,\
#di_key_id_entry_intern_lk_value_lis_li_rout_prob_and_id_dest_lk=di_key_id_phase_value_cum_rp,\
#li_phases=["id phase (1-2 columns), cum rout prob (next colm)"])
#*********************************************************************************************************************************************************************************************************************************************************************
#*********************************************************************************************************************************************************************************************************************************************************************
#*********************************************************************************************************************************************************************************************************************************************************************


#**************************************************************************Fichiers reseau **********************************************************************************************************************************

#*********************************************************************************************************************************************************************************************************************************************************************
#we write file fi_demand_param_entry_link
val_list_valeurs_1=[
[1,0.5],
[17,0.5],
[19,0.5],
[21,0.5],
[23,0.5],
[25,0.5],
[27,0.5],
[29,0.5],
[31,0.5],
[33,0.5],
[35,0.5],
[37,0.5],
[39,0.5],
[41,0.5],
[43,0.5],
[45,0.5]]

val_list_valeurs_=[
[1,0.9],
[4,0.9],
[6,0.9]
]
#fct_write_fi_demand_param_entry_link(name_file_to_write=File_names_network_model.val_file_name_demand_param_entry_link,list_valeurs=val_list_valeurs)


#we write file fi_id_all_network_link_id_orig_dest_node_length_link_capacity_link_param_travel_duration

val_list_valeurs_1_=[\
[1,-1,1,1,0,0],\
[2,1,2,1,-1,30],\
[3,2,3,1,-1,30],\
[4,3,4,1,-1,30],\
[5,4,5,1,-1,30],\
[6,5,6,1,-1,30],\
[7,6,7,1,-1,30],\
[8,7,8,1,-1,30],\
[9,8,9,1,-1,30],\
[10,9,10,1,-1,30],\
[11,10,11,1,-1,30],\
[12,11,12,1,-1,30],\
[13,12,13,1,-1,30],\
[14,13,14,1,-1,30],\
[15,14,15,1,-1,30],\
[16,15,-1,1,-1,0],\
[17,-1,1,1,0,0],\
[18,1,-1,1,0,0],\
[19,-1,2,1,0,0],\
[20,2,-1,1,0,0],\
[21,-1,3,1,0,0],\
[22,3,-1,1,0,0],\
[23,-1,4,1,0,0],\
[24,4,-1,1,0,0],\
[25,-1,5,1,0,0],\
[26,5,-1,1,0,0],\
[27,-1,6,1,0,0],\
[28,6,-1,1,0,0],\
[29,-1,7,1,0,0],\
[30,7,-1,1,0,0],\
[31,-1,8,1,0,0],\
[32,8,-1,1,0,0],\
[33,-1,9,1,0,0],\
[34,9,-1,1,0,0],\
[35,-1,10,1,0,0],\
[36,10,-1,1,0,0],\
[37,-1,11,1,0,0],\
[38,11,-1,1,0,0],\
[39,-1,12,1,0,0],\
[40,12,-1,1,0,0],\
[41,-1,13,1,0,0],\
[42,13,-1,1,0,0],\
[43,-1,14,1,0,0],\
[44,14,-1,1,0,0],\
[45,-1,15,1,0,0],\
[46,15,-1,1,-1,0]]

val_list_valeurs_1=[
[1,-1,1,10, 0,15],
[2,1,2,10,80,15],
[3,2,-1,10, 0,15],
[4,-1,1,10,0,15],
[5,1,-1,10,0,15],
[6,-1,2,10, 0,15],
[7,2,1,10,0,15]
]

#fct_write_fi_id_all_network_link_id_orig_destination_node_length_link_capacity_link_param_travel_duration(\
#name_file_to_write=\
#File_names_network_model.val_file_name_id_all_network_link_id_orig_dest_node_length_link_capacity_link_param_travel_duration,\
#list_valeurs=val_list_valeurs_1)




#we write file   fi_id_all_phases_max_queue_size_sat_flow_queue_type
val_list_valeurs_2_=[
[1,2,-1,0.15,0],
[1,18,0,0,0],
[2,3,-1,0.15,0],
[2,20,0,0,0],
[3,4,-1,0.15,0],
[3,22,0,0,0],
[4,5,-1,0.15,0],
[4,24,0,0,0],
[5,6,-1,0.15,0],
[5,26,0,0,0],
[6,7,-1,0.15,0],
[6,28,0,0,0],
[7,8,-1,0.15,0],
[7,30,0,0,0],
[8,9,-1,0.15,0],
[8,32,0,0,0],
[9,10,-1,0.15,0],
[9,34,0,0,0],
[10,11,-1,0.15,0],
[10,36,0,0,0],
[11,12,-1,0.15,0],
[11,38,0,0,0],
[12,13,-1,0.15,0],
[12,40,0,0,0],
[13,14,-1,0.15,0],
[13,42,0,0,0],
[14,15,-1,0.15,0],
[14,44,0,0.0,0],
[15,16,-1,0.15,0],
[15,46,0,0,0],
[17,18,-1,0.15,0],
[17,2,0,0,0],
[19,20,-1,0.15,0],
[19,3,0,0,0],
[21,22,-1,0.15,0],
[21,4,0,0,0],
[23,24,-1,0.15,0],
[23,5,0,0,0],
[25,26,-1,0.15,0],
[25,6,0,0,0],
[27,28,-1,0.15,0],
[27,7,0,0,0],
[29,30,-1,0.15,0],
[29,8,0,0,0],
[31,32,-1,0.15,0],
[31,9,0,0,0],
[33,34,-1,0.15,0],
[33,10,0,0,0],
[35,36,-1,0.15,0],
[35,11,0,0,0],
[37,12,-1,0.15,0],
[37,17,0,0,0],
[39,40,-1,0.15,0],
[39,13,0,0,0],
[41,42,-1,0.15,0],
[41,14,0,0,0],
[43,44,-1,0.15,0],
[43,15,0,0,0],
[45,46,-1,0.15,0],
[45,16,0,0,0],
]

val_list_valeurs_2=[
[1,2,0,1,0],
[1,5,0,1,0],
[4,2,0,1,0],
[4,5,0,1,0],
[2,3,30,1,0],
[2,7,30,1,0],
[6,3,0,1,0],
[6,7,0,1,0],
]

#val_li_ph_=["IF QUE TYPE=1 PHASE=RT, OTHERWISE  QUE TYPE=0"]
#fct_write_fi_id_phases_max_queue_size_sat_flow_queue_type(name_file_to_write=\
#File_names_network_model.val_file_name_id_all_phases_max_queue_size_and_sat_flow_queue_type,\
#li_phrases=val_li_ph,list_valeurs=val_list_valeurs_2)





#we write file fi_id_internal_link_id_orig_dest_node
val_list_valeurs_3_=[
[2,1,2],
[3,2,3],
[4,3,4],
[5,4,5],
[6,5,6],
[7,6,7],
[8,7,8],
[9,8,9],
[10,9,10],
[11,10,11],
[12,11,12],
[13,12,13],
[14,13,14],
[15,14,15]
]

val_list_valeurs_3=[
[2,1,2]
]

fct_write_fi_id_internal_link_id_orig_dest_node(name_file_to_write=File_names_network_model.val_file_name_id_internal_link_id_orig_dest_node,list_valeurs=val_list_valeurs_3)


#we write file fi_id_node_id_entering_links_to_node
val_list_valeurs_4_=[
[1,1,17],
[2,2,19],
[3,3,21],
[4,4,23],
[5,5,25],
[6,6,27],
[7,7,29],
[8,8,31],
[9,9,33],
[10,10,35],
[11,11,37],
[12,12,39],
[13,13,41],
[14,14,43],
[15,15,45]
]


val_list_valeurs_4=[
[1,1,4],
[2,2,6]
]

#fct_write_fi_id_node_id_entering_or_leaving_links_to_node(name_file_to_write=File_names_network_model.val_file_name_id_node_id_entering_links_to_node,list_valeurs=val_list_valeurs_4)

val_list_valeurs_5_=[
[1,2,18],
[2,3,20],
[3,4,22],
[4,5,24],
[5,6,26],
[6,7,28],
[7,8,30],
[8,9,32],
[9,10,34],
[10,11,36],
[11,12,38],
[12,13,40],
[13,14,42],
[14,15,44],
[15,16,46]
]


val_list_valeurs_5=[
[1,2,5],
[2,3,7]
]
#we write the file fi_id_node_id_leavings_links_from_node 
#fct_write_fi_id_node_id_entering_or_leaving_links_to_node(name_file_to_write=File_names_network_model.val_file_name_id_node_id_leaving_links_from_node,list_valeurs=val_list_valeurs_5)

val_list_valeurs_6_=[
[1,1,17],
[2,19],
[3,21],
[4,23],
[5,25],
[6,27],
[7,29],
[8,31],
[9,33],
[10,35],
[11,37],
[12,39],
[13,41],
[14,43],
[15,45]
]


val_list_valeurs_6=[
[1,1,4],
[2,6]
]
#we write the file fi_id_node_id_entry_links_to_network
#fct_write_fi_id_node_id_entering_or_leaving_links_to_node(name_file_to_write=File_names_network_model.val_file_name_id_node_id_entry_links_to_network,list_valeurs=val_list_valeurs_6)

#we write file fi_id_node_id_exit_links_from_network
val_list_valeurs_7_=[
[1,18],
[2,20],
[3,22],
[4,24],
[5,26],
[6,28],
[7,30],
[8,32],
[9,34],
[10,36],
[11,38],
[12,40],
[13,42],
[14,44],
[15,46,16]
]


val_list_valeurs_7=[
[1,5],
[2,3,7]
]
#fct_write_fi_id_node_id_entering_or_leaving_links_to_node(name_file_to_write=File_names_network_model.val_file_name_id_node_id_exit_links_from_network,\
#list_valeurs=val_list_valeurs_7)


#we write  file fi_id_node_type_node
val_list_phrases_8=["node id (1st col), type inters. (1:sign., 0: non sign., 2nd col)"]
#val_list_valeurs_8=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]

val_list_valeurs_8=[1,2]
#fct_write_fi_id_node_type_node_cas_nds_sign(name_file_to_write=File_names_network_model.val_name_file_fi_id_node_type_node,list_phrases=val_list_phrases_8,\
#list_valeurs=val_list_valeurs_8)


#we write file fi_mrp
val_li_phrases_9=["Id phase (1-2 columns), prob of the phase (3rd column)"]

val_li_rout_prob_values_9_=[
[1,2,1],
[2,3,1],
[3,4,1],
[4,5,1],
[5,6,1],
[6,7,1],
[7,8,1],
[8,9,1],
[9,10,1],
[10,11,1],
[11,12,1],
[12,13,1],
[13,14,1],
[14,15,1],
[15,16,1],
[17,18,1],
[19,20,1],
[21,22,1],
[23,24,1],
[25,26,1],
[27,28,1],
[29,30,1],
[31,32,1],
[33,34,1],
[35,36,1],
[37,38,1],
[39,40,1],
[41,42,1],
[43,44,1],
[45,46,1]]

val_li_rout_prob_values_9=[
[1,2,0.5],
[1,5,0.5],
[4,2,0.5],
[4,5,0.5],
[2,3,0.5],
[2,7,0.5],
[6,3,0.5],
[6,7,0.5]
]

#fct_write_file_rout_prob_each_phase(val_name_file_to_write=File_names_network_model.val_name_file_mat_rp_id_phase_prob_dest_lk,\
#val_li_phrases=val_li_phrases_9,val_li_rout_prob_values=val_li_rout_prob_values_9)


#we write file fi_stages_each_sign_inters
val_list_phrases_10=["for each line, 1st column: id inters, next columns phases to actuate"]

val_list_valeurs_10_=[
[1,1,2],
[1,17,18],
[2,2,3],
[2,19,20],
[3,3,4],
[3,21,22],
[4,4,5],
[4,23,24],
[5,5,6],
[5,25,26],
[6,6,7],
[6,27,28],
[7,7,8],
[7,29,30],
[8,8,9],
[8,31,32],
[9,9,10],
[9,33,34],
[10,10,11],
[10,35,36],
[11,11,12],
[11,37,38],
[12,12,13],
[12,39,40],
[13,13,14],
[13,41,42],
[14,14,15],
[14,43,44],
[15,15,16],
[15,45,46]
]


val_list_valeurs_10=[
[1,1,2,1,5],
[1,4,5,4,2],
[2,2,3,2,7],
[2,6,7,6,3]
]

#fct_write_file_intersection_stages(name_file_to_write=File_names_network_model.val_name_file_stages_each_signalised_inters,\
#list_phrases=val_list_phrases_10,list_valeurs=val_list_valeurs_10)


#file write the file with the rout prob to apply at different periods
val_li_phrases_11=["id node (1st colm), id input lk (2nd colm), id output lk (3nd colm), rout prob next period (5th colm) etc."]

val_li_rout_prob_values_11=[
[37593,708,	831.00,		0.8,		0.1],	
[37593,708,	2371.00,		0.1,		0.1],	
[37593,708,	23003.00,		0.1,		0.8],	
[37593,1497559,	709.00,		0.1,		0.1],
[37593,1497559,	2371.00,		0.1,		0.8],
[37593,1497559,	23003.00,	0.8,		0.1],	
[37593,2370,	23003.00,		0.1,		0.1],	
[37593,2370,	831.00,		0.1,		0.7],	
[37593,2370,	709.00,		0.8,		0.2],
[37593,23004,	831.00	,	0.7,		 0.6],	
[37593,23004,	2371.00,		0.15,		 0.3],
[37593,23004,	709.00,		0.15,		 0.1],	
[37605,709,	1206.00,		0.15,	0.1],
[37605,709,	732.00	,	0.24,		 0.6],
[37605,709,	1085.00,		0.61,	 0.3],
[37605,216323,	1085.00,	0.61,	 0.2	],
[37605,216323,	708.00,	0.15,		 0.7],
[37605,216323,	1206.00,	0.24,		 0.1],
[37605,1204,	732.00,	0.7,		0.3],	
[37605,1204,	708.00, 0.1,		0.1],	
[37605,1204,	1085.00,	0.1,		0.5],	
[37605,1204,	1206.00,	0.1,		0.1],
[37605,1205,	708.00,	0.14,		 0.2],
[37605,1205,	732.00, 0.24,		 0.4],
[37605,1205,	1085.00,	0.62,		 0.4],
[49395,23006,	24550.00,		0.62,  	0.3],	
[49395,23006,	1752109, 		0.14, 	0.5],
[49395,23006,	1752108.00,	0.24,  	0.2],
[49395,24549,	1752109.00,	0.8,	0.1],	
[49395,24549,	23005.00,	 	0.1,	0.1],	
[49395,24549,1752108.00,	0.1,	0.8],
[49395,1752111,	24550.00,	0.18,		0.8],	
[49395,1752111,	1752108.00,	0.22,	0.1],
[49395,1752111,	23005.00,		0.6,		0.1],
[49395,1752107,	1752109.00,	0.6,	 	0.6],
[49395,1752107,	23005.00,		0.22, 	0.2],	
[49395,1752107,	24550.00,		0.18, 	0.2],	
[37607,727,	216323.00,	0.9, 	0.8],
[37607,727,	216323.00,	0.1, 	0.2],
[37607,732,	16462.00,		0.4,0.7],
[37607,732,	728.00,		0.6,	 	0.3],	
[37607,216305,	728.00,		0.1,	0.8],
[37607,216305,	216323.00,	0.9, 	0.2],
[37872,216440,	1204.00,		0.7,		0.1],
[37872,216440,	20482.00,	0.15,		0.6],	
[37872,216440,	23006.0,		0.15,		0.3],
[37872,1085,	1204.00,		0.5, 	0.1],	
[37872,1085,	20482.00,	0.1 ,	0.4],
[37872,1085,	23006.00,	0.1, 0.4],	
[37872,1085,	1201.00,		0.3 ,	0.1],
[37872,23005,	1201.00,		0.1,	 	0.3],
[37872,23005,	1204.00,		0.1,	 	0.3],
[37872,23005,	20482,	      	0.7,	 	0.2],
[37872,23005,	23006.00,	0.1,		0.2],
[37872,20481,	1204.00,		0.15, 	0.4],	
[37872,20481,	23006.00,		0.24, 	0.3],	
[37872,20481,	1201.00,		0.61, 	0.3],
[37606,728,	217793.00,	0.2,		0.1],
[37606,728,	734.00,		0.6,		0.8],		
[37606,728,	16467.00,	0.2,		0.1],
[37606,733,	217793.00,	0.8,		0.3],	
[37606,733,	16467.00,		0.1,		0.6],
[37606,733,	727.00	,	      0.1,		0.1],
[37606,16468,	727.00,	0.1,		0.3],	
[37606,16468,	734.00	,	0.8,		0.4],
[37606,16468,	217793.00,	0.1,		0.3],
[37606,217794,	727.00	,	0.14	,	0.1],	
[37606,217794,	16467.00,		0.62,		0.6],
[37606,217794,	734.00	,	0.24,		0.3],
[48494,20477,	16468.0,		0.9,		0.6],	
[48494,20477,	20481.00,	0.1,	0.4],
[48494,16467,	16468.00,	0.22,		0.6],
[48494,16467,	20481.00,	0.6,		0.1],
[48494,16467,	20478.00,		0.18	,	0.3],	
[48494,20482,	20478.00,		0.70,		0.3],	
[48494,20482,	16468.00	,	0.30,		0.7],
[37610,734,	738.00,		0.7,		0.1],	
[37610,734,	2351.00,		0.2,		0.1],	
[37610,734,	20471.00,	0.1,		0.8],	
[37612,737,	20471.00,	0.1,		0.6],
[37612,737,	733.00,	0.7,		0.1],	
[37612,737,  2351.00,		0.2,		0.3],	
[37610,2350,	738.00,		0.8,		0.1],	
[37610,2350,	733.00,	0.1,		0.6],
[37610,2350,	20471.00,		0.1,		0.3],
[37610,20472,	733.00,	0.1,		0.7],	
[37610,20472,	738.00,	0.8,		0.1],
[37610,20472,	2351.00,0.1,		0.2],	
[48492,20471,	20477.00,		0.6,		0.1],	
[48492,20471,	24565.00,		0.3,		0.6],	
[48492,20471,	217802.00,	0.1,		0.3],	
[48492,20478	,20472.00,		0.7,		0.1],	
[48492,20478,	24565.00,		0.2,		0.6],	
[48492,20478,	217802.00,	0.1,		0.3],
[48492,24564	,20472.00,		0.2,		0.7],	
[48492,24564,	20477.00,		0.7,		0.1],
[48492,24564	,217802.00,	0.1,		0.2],
[48492,217801,20472.00, 0.14,	0.62],
[48492,217801,20477.00,	0.24,	0.14	],
[48492,217801,	24565.00	,	0.62,0.24],
[48493,20475,	24562.00,		0.20,	0.8],	
[48493,20475,	1721893.00,	0.80,	0.2],
[48493,24563,	20476.00,		0.3,		0.7],	
[48493,24563,	1721893.00,	0.7,		0.3],
[48493,1721892,	20476.00,		0.7,	0.3],
[48493,1721892,	24562.00,		0.3,	0.7],
[37612,738,	742.00,	0.2,		0.7],
[37612,738,	20475.00,	0.7,	0.1],	
[37612,738,	737.00,	0.1,		0.2],
[37612, 741,	737.00,	0.6,		0.4],
[37612,741,	20475.00,	0.4,	0.6],	
[37612,20476,	737.00,0.3,0.1],
[37612,20476,	742.00	,0.7,0.9]]



#fct_write_file_rout_prob_each_phase(val_name_file_to_write=File_names_network_model.val_name_file_series_varying_rout_prob,\
#val_li_phrases=val_li_phrases_11,val_li_rout_prob_values=val_li_rout_prob_values_11)

#file write the file with the rout prob to apply at different periods
val_li_phrases_12=["id node (1st colm), id input lk (2nd colm), id output lk (3nd colm), duree previous  rout prob value (4th colm),\
cum rout prob 2nd period (5th colm), duree previous (6th colm), cum rout prob (7th colm) etc."]

val_li_rout_prob_values_12=[
[37593,708,	831.00,	1500,	0.8,	1500,	0.1],	
[37593,708,	2371.00,	1500,	0.9,	1500,	0.2],	
[37593,708,	23003.00,1500,	1.0,	1500,1.0],	
[37593,1497559,	709.00,1500,		0.1,	1500,	0.1],
[37593,1497559,	2371.00,	1500,	0.9,	1500,	0.9],
[37593,1497559,	23003.00,1500,	1.0,	1500,	1.0],	
[37593,2370,	23003.00,1500,	0.1,	1500,	0.1],	
[37593,2370,	831.00,	1500,	0.2,	1500,	0.8],	
[37593,2370,	709.00,1500,		1.0,	1500,	1.0],
[37593,23004,	831.00	,1500,	0.7,	1500,	 0.6],	
[37593,23004,	2371.00,1500,	0.85, 1500,	 0.9],
[37593,23004,	709.00,1500,	1.0,	1500,	 1.0],	
[37605,709,	1206.00,	1500,	0.15,1500,	0.1],
[37605,709,	732.00	,	1500,  0.39,	1500,	 0.7],
[37605,709,	1085.00,	1500,	1.0,1500,	 1.0],
[37605,216323,	1085.00,	1500,0.61,1500, 0.2	],
[37605,216323,	708.00,1500,	0.76,1500,	0.9],
[37605,216323,	1206.00,	1500,1.0,	1500,	1.0],
[37605,1204,	732.00,1500,	0.7,	1500,	0.3],	
[37605,1204,	708.00, 1500,0.8,	1500,	0.4],	
[37605,1204,	1085.00,1500,	0.9,1500,		0.9],	
[37605,1204,	1206.00,	1500,1.0,	1500,	1.0],
[37605,1205,	708.00,1500,	0.14,	1500, 0.2],
[37605,1205,	732.00, 1500,0.38,	1500,	 0.6],
[37605,1205,	1085.00,	1500,1.0,	1500,	 1.0],
[49395,23006,	24550.00,1500,		0.62,1500,  	0.3],	
[49395,23006,	1752109, 1500,		0.76,1500, 	0.8],
[49395,23006,	1752108.00,1500,	1.0, 1500, 	1.0],
[49395,24549,	1752109.00,1500,	0.8,1500,	0.1],	
[49395,24549,	23005.00,	1500, 	0.9,1500,	0.2],	
[49395,24549,1752108.00,1500,	1.0,1500,	1.0],
[49395,1752111,	24550.00,1500,	0.18,1500,		0.8],	
[49395,1752111,	1752108.00,1500,	0.4,	1500,0.9],
[49395,1752111,	23005.00,1500,		1.0,	1500,	1.0],
[49395,1752107,	1752109.00,1500,	0.6,	1500, 	0.6],
[49395,1752107,	23005.00,1500,		0.82, 1500,	0.8],	
[49395,1752107,	24550.00,1500,		1.0, 1500,	1.0],	
[37607,727,	216323.00,	1500,0.9, 1500,	0.8],
[37607,727,	216323.00,	1500,1.0,1500, 	1.0],
[37607,732,	16462.00,	500,	0.4,1500,0.7],
[37607,732,	728.00,1500,	1.0,	1500, 	1.0],	
[37607,216305,	728.00,1500,		0.1,1500,	0.8],
[37607,216305,	216323.00,	1500,1.0, 1500,1.0],
[37872,216440,	1204.00,	1500,	0.7,	1500,	0.1],
[37872,216440,	20482.00,1500,	0.85,1500,	0.7],	
[37872,216440,	23006.0,	1500,	1.0,	1500,	1.0],
[37872,1085,	1204.00,	1500,	0.5, 1500,0.1],	
[37872,1085,	20482.00,1500,	0.6 ,1500,0.5],
[37872,1085,	23006.00,1500,	0.7, 1500, 0.9],	
[37872,1085,	1201.00,	1500,	1.0 ,1500,1.0],
[37872,23005,	1201.00,	1500,	0.1,	1500, 	0.3],
[37872,23005,	1204.00,1500,		0.2,1500,	 	0.6],
[37872,23005,	20482,	 1500,     	0.9,	1500, 	0.8],
[37872,23005,	23006.00,1500,	1.0,	1500,	1.0],
[37872,20481,	1204.00,	1500,	0.15, 	1500,0.4],	
[37872,20481,	23006.00,	1500,0.39, 1500,	0.7],	
[37872,20481,	1201.00,	1500,	1.00, 1500,	1.0],
[37606,728,	217793.00,1500,	0.2,	1500,	0.1],
[37606,728,	734.00,	1500,	0.8,	1500,	0.9],		
[37606,728,	16467.00,1500,	1.0,	1500,	1.0],
[37606,733,	217793.00,	1500,0.8,	1500,	0.3],	
[37606,733,	16467.00,	1500,	0.9,	1500,	0.9],
[37606,733,	727.00	,1500,   1.0,	1500,	1.0],
[37606,16468,	727.00,1500,	0.1,	1500,	0.3],	
[37606,16468,	734.00	,1500,	0.9,	1500,	0.7],
[37606,16468,	217793.00,	1500,1.0,	1500,1.0],
[37606,217794,	727.00	,1500,	0.14,1500,	0.1],	
[37606,217794,	16467.00,1500,0.76,1500,	0.7],
[37606,217794,	734.00	,1500,	1.0,1500,		1.0],
[48494,20477,	16468.0,	1500,	0.9,	1500,	0.6],	
[48494,20477,	20481.00,1500,	1.0,1500,	1.0],
[48494,16467,	16468.00,1500,0.22,1500,	0.6],
[48494,16467,	20481.00,1500,0.82,1500,	0.7],
[48494,16467,	20478.00,1500,1.0,1500,	1.0],	
[48494,20482,	20478.00,1500,0.70,1500,	0.3],	
[48494,20482,	16468.00	,1500,1.0,1500,	1.0],
[37610,734,	738.00,	1500,	0.7,	1500,	0.1],	
[37610,734,	2351.00,	1500,	0.9,	1500,	0.2],	
[37610,734,	20471.00,1500,	1.0,1500,	1.0],	
[37610,737,	20471.00,1500,0.1,	1500,	0.6],
[37610,737,	733.00,1500,	0.8,	1500,	0.7],	
[37610,737,  2351.00,	1500,1.0,	1500,	1.0],	
[37610,2350,	738.00,1500,	0.8,	1500,0.1],	
[37610,2350,	733.00,1500,	0.9,	1500,	0.7],
[37610,2350,	20471.00,1500,1.0,	1500,	1.0],
[37610,20472,	733.00,1500,	0.1,	1500,	0.7],	
[37610,20472,	738.00,1500,	0.9,	1500,	0.8],
[37610,20472,	2351.00,1500,1.0,1500,		1.0],	
[48492,20471,	20477.00,1500,	0.6,1500,		0.1],	
[48492,20471,	24565.00,1500,	0.9,	1500,	0.7],	
[48492,20471,	217802.00,1500,	1.0,	1500,	1.0],	
[48492,20478,20472.00,1500,	0.7,	1500,	0.1],	
[48492,20478,	24565.00,1500,	0.9,	1500,	0.7],	
[48492,20478,	217802.00,1500,1.0,	1500,	1.0],
[48492,24564,20472.00,	1500,	0.2,1500,	0.7],	
[48492,24564,20477.00,	1500,	0.9,1500,	0.8],
[48492,24564,217802.00,1500,	1.0,1500,	1.0],
[48492,217801,20472.00,1500, 0.14,1500,	0.62],
[48492,217801,20477.00,1500,	0.38,1500,0.76],
[48492,217801,24565.00	,1500,	1.0,1500,	1.0],
[48493,20475,	24562.00,	1500,	0.20,1500, 0.8],	
[48493,20475,	1721893.00,1500,	1.0,1500,	1.0],
[48493,24563,	20476.00,	1500,	0.3,	1500,	0.7],	
[48493,24563,	1721893.00,1500,	1.0,	1500,	1.0],
[48493,1721892,	20476.00,	1500,	0.7,1500,	0.3],
[48493,1721892,	24562.00,	1500,	1.0,1500,	1.0],
[37612,738,	742.00,1500,0.2,1500,0.7],
[37612,738,	20475.00,1500,0.9,1500,0.8],	
[37612,738,	737.00,1500,1.0,1500,1.0],
[37612,741,	737.00,1500,0.6,	1500,	0.4],
[37612,741,	20475.00,1500,1.0,1500,1.0],	
[37612,20476,	737.00,1500,0.3,1500,0.1],
[37612,20476,	742.00	,1500,1.0,1500,1.0],
]

#fct_write_file_rout_prob_each_phase(val_name_file_to_write=\
#File_names_network_model.val_name_file_series_cum_values_varying_rout_prob,\
#val_li_phrases=val_li_phrases_12,val_li_rout_prob_values=val_li_rout_prob_values_12)

#val_name_file_rout_prop_to_read=File_names_network_model.val_name_file_mat_rp_id_phase_prob_dest_lk
#val_name_file_to_write_cum_rp=File_names_network_model.val_name_file_mat_rp_cum
#fct_calcul_and_write_cum_rp(val_name_file_rout_propab_to_read=val_name_file_rout_prop_to_read,val_name_file_to_write=val_name_file_to_write_cum_rp,val_nb_comment_lines=1,\
#val_considered_one_in_cum_fctn=0.99)


#li_di=fct_read_file_fi_series_cum_val_varying_rp(name_file_to_read=File_names_network_model.val_name_file_series_cum_values_varying_rout_prob,\
#nb_comment_lines=1)

#print(li_di[0][37612])
#print()
#print(li_di[1])

#di_2=fct_read_file_fi_series_varying_rout_prob(name_file_to_read=File_names_network_model.val_name_file_series_varying_rout_prob,nb_comment_lines=1)
#print(di_2)

#we write the file with the init state of the system
val_li_valeurs=[
[1,1,2,2,-1], [1,17,18,4,-1],[15,15,16,1,-1],[15,45,46,2,-1]
]
#fct_write_file_fi_init_state_que(name_file_to_write=File_names_network_model.val_name_file_init_state_que,li_valeurs=val_li_valeurs,\
#li_phrases=["id node (1st clmn), id phase (2nd, 3rd clmn), nb veh (3rd clmn), id veh final dest\
#(>0 when OD, -1 otherwise, next columns) IF YOU REMOVE VEH FROM QUEUE THE REMAINING VEH WILL KEEP THEIR FINAL DEST"])

#we read the file with the init state of the system
#di_rep=fct_read_file_fi_init_state_que(name_file_to_read=File_names_network_model.val_name_file_init_state_que,nb_comment_lines=1)

#print(di_rep)

#we write file fi_phase_interference.txt
val_li_valeurs=[[1,1,18,1,2,0.5],[1,1,2,1,18,0.75],[2,2,20,2,3,0.5],[2,2,3,2,20,0.75],[3,3,22,3,4,0.5],[3,3,4,3,22,0.75]]

#fct_write_file_fi_phase_interference(name_file_to_write=File_names_network_model.name_file_phase_interference,li_valeurs=val_li_valeurs,\
#li_phrases=["id node (1 colm), id phase  affected (2-3 colm), id affecting phase (4-5 colm), param affected phase (6 colm)"])

#di_rep=fct_read_file_fi_init_state_que(name_file_to_read=File_names_network_model.name_file_phase_interference,nb_comment_lines=1)
#print(di_rep)

#*********************************************************************************************************************************************************************************************************************************************************************

#*************************************************************************fcts ecrit param controles************************************************************************************************************************************************************

#on ecrit  les param du FT ctrl
li_val_ft=[\
[1,1,50,100],
[1,2,50,100],
[2,1,50,100],
[2,2,50,100],
]
 
li_phrases_ft=["'id nd (1st colm),id stage (2nd colm, if id=0 it is rd cleat), actuat durat (3rd colm),cycle duration (5th colm), 1st line","for a given inersection the order of stage id is related to  their priority within the cycle'"]

#fct_write_file_parameters_ft_control(name_file_to_write=File_Sim_Name_Module_Files.val_name_file_values_ft_control,li_valeurs=li_val_ft, li_phrases=li_phrases_ft)


#on ecrit fi_id_nd_type_ctrl_category
list_valeurs_fi_id_nd_type_ctrl_cat=[
[1,1, "without_sensor_requirement",0],
[2,1, "without_sensor_requirement",0],
]


#fct_write_fi_id_node_type_ctrl_categoryr(name_file_to_write=File_Sim_Name_Module_Files.val_name_file_node_id_control_type_category,\
#list_phrases=[" id node (1st collm), type control ,(2nd colm)1: \"type_control_FT\", 2:\"type_control_FT_Offset\", \
#3:\"type_control_MP\" , 10: \``type_control_FA _no red clear\‘’,11:\"type_control_FA_Max_Green\" ,12: \``type_control_FA _with_red lrear\",1\
#3:\"type_control_MP_Practical \‘’,(3rd colm): control category indicates if the ctrl is updated accroding to flows or not, sensor_requirement for controls requiring sensor monitoring (FA,FAmax green),\
#without_sensor_requirement for controls not requiring sensors (FT, MP, etc),(4th column): 1 if turn ratios are going to be estimated with the employed control, 0 otherwise"],list_valeurs=list_valeurs_fi_id_nd_type_ctrl_cat)

#*********************************************************************************************************************************************************************************************************************************************************************




#*********************************************************************************************************************************************************************************************************************************************************************


#*********************************************************************************************************************************************************************************************************************************************************************


#*********************************************************************************************************************************************************************************************************************************************************************
#va_name_file_to_read="/Users/jennie/Desktop/travail_vsim_int/PARSER_FI_XML/test_parser_3/scenario_example_5.xml"


#fct_write_network_files_from_xml_file_information(v_name_file_to_read=va_name_file_to_read)

#fct_reading_file_cum_rout_prob(name_file_read="NETWORK_DATA/fi_mrp_cum.txt",nb_comment_lines=1)

#we write file fi_mp
#fct_reading_fi_mp_and_write_nb_line_and_values(name_file_read="./Series_MP_10_mod_cap_finie/file_MP.txt",name_file_write="fi_values_dif_mp_stages.txt")

#we read the file with the param of the demand variation (case when the demand varies)
#di=fct_reading_file_fi_demand_param_variation(name_file_to_read="../../SMALL_NETWS_2/reseaux_2/SMALL_DATA_2NDS_FIG_7"+"/"+\
#File_names_network_model.val_name_folder_with_files_demand_param_when_varying_demand+"/"+File_names_network_model.\
#val_fi_demand_param_variation,nb_comment_lines=1)
#print(di)


#we write the file with the link id and mean trav time
#fct_write_fi_id_link_mean_travel_time(\
#name_file_to_read=File_names_network_model.val_file_name_id_all_network_link_id_orig_dest_node_length_link_capacity_link_param_travel_duration,\
#name_file_to_write_1=File_names_network_model.val_name_file_id_link_mean_trav_time,\
#name_file_to_write_2=File_names_network_model.val_name_file_link_mean_trav_time,\
#nb_comment_lines=0)


#li_di_mu_sigma_shift=fct_creat_dict_param_stoch_travel_time_from_text_file_all_links(\
#v_name_file_to_read=File_names_network_model.val_file_name_id_all_network_link_id_orig_dest_node_length_link_capacity_link_param_travel_duration,\
#v_nb_comment_lines=0,v_sigma=0.974174,v_b=0.8)

#print(li_di_mu_sigma_shift[0])

# we write the file with the routing type of entry links associated with od and given paths or dynamically computed ones

#val_li_valeurs=[[8,1],[5,1]]
#fct_write_file_fi_rout_type_entry_lk_mixed_manag(name_file_to_write=File_names_network_model.val_name_file_rout_type_entry_lk_mixed_manag,li_valeurs=val_li_valeurs,\
#li_phrases=["id lk (1st column), rout. type (2nd column) 1: od and given path, 2: od and dynam computed path"])

#di_rep=fct_read_file_fi_rout_type_entry_lk_mixed_manag(name_file_to_read=File_names_network_model.val_name_file_rout_type_entry_lk_mixed_manag,nb_comment_lines=1)
#print(di_rep)






