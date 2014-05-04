import List_Explicit_Values
import File_Sim_Name_Module_Files
import File_names_network_model
import File_Stats_Anal_Folders_And_Files
import Cl_Event
import math
import os
import random

#function definining the time between two vehicle appearances  at en entry link, when poisson process is employes
def fct_calcul_demand_entry_link_poisson_proc(param):
	return random.expovariate(param)
#*****************************************************************************************************************************************************************************************
#function defining the time between two successive vehicle appearances  at en entry link,	when stoch demand is considered
def fct_calcul_demand_entry_link_stoch_case(param):
	return fct_calcul_demand_entry_link_poisson_proc(param)
#*****************************************************************************************************************************************************************************************
#function defining the time between two successive vehicle appearances  at en entry link,	when deterministic demand is considered
def fct_calcul_demand_entry_link_deterministic_case(param):
	return param
#*****************************************************************************************************************************************************************************************
#method reading a dictionary of which key=[x,y],  the  value= [ [a1,b1],[a2,b2],...] and returns for each key 
#[the mean value of ai, mean value of bi].
#we use it for calculating the mean travel time and the mean number of departed vehicles from each pair (entry, exit link)
#of a series of sims
def fct_calcul_mean_trav_time_and_nb_dep_veh_series_sims(dict_inf,val_round_prec=1):

	dict={}
	for i in dict_inf:
		
		dict[i]=[]
		sum_mean=0
		sum_nb_veh=0
		for j in dict_inf[i]:
			
			sum_mean+=j[0]
			sum_nb_veh+=j[1]
		len1=len(dict_inf[i])
		dict[i]=[round(sum_mean/len1,val_round_prec),round(sum_nb_veh/len1)]
		
	return dict

#*****************************************************************************************************************************************************************************************
#method creating a dictionary containing the inform of all vehicles
#the key = veh id, value=[ ...,[time_event, type_event, id_current_link_location,id_destination_link,t_exit],...  ]
def fct_creating_complete_dict_veh_informaton_created_by_sim(path_list_files,val_line_number=7):
	
	di_veh_inform={}
	
	#we obtain the current directory
	cur_dir=os.getcwd()
	#we are placed in the direcroty where the vehicle files are
	os.chdir(path_list_files)
	
	for i in os.listdir('.'):
		
		di=fct_dict_veh_information_created_by_sim(name_veh_file_read=i,line_number=val_line_number)
		#print("HERE1",di)
		di_veh_inform.update(di)
	os.chdir(cur_dir)	
	return di_veh_inform
	

#*****************************************************************************************************************************************************************************************

#function defining the number of vehicles to leave in a micro management and the associated required time
#it returns [nb veh to leave, time toleave the queue]
# v_sat_flow = the value of the saturation flow expressed as number of vehicles that can go / time unit
def fct_defin_nb_veh_leave_mi_1(v_sat_flow,v_t_unit,v_round_prec=2):
	
	nb_veh_go_and_t=[]
	#if the sat flow is > 1
	if v_sat_flow>1:
		#nb_veh_go_and_t=[round(v_sat_flow, v_round_prec),v_t_unit]
		nb_veh_go_and_t=[math.ceil(v_sat_flow),v_t_unit]
	
	#if the sat flow =1
	elif v_sat_flow==1:
		nb_veh_go_and_t=[v_sat_flow,v_t_unit]
	
	#if the sat flow is <1
	else:
		#calc the required time for one veh to go
		t_req=round(v_t_unit/v_sat_flow, v_round_prec)
		#print("t_req",t_req,"v_t_unit",v_t_unit,"v_sat_flow",v_sat_flow)
		nb_veh_go_and_t=[math.ceil(v_sat_flow),t_req]
		
	return nb_veh_go_and_t
	
	

#*****************************************************************************************************************************************************************************************
#method  reading a vehicle file created by a sim (VEH_ID) and returning a dictionary of which key=vehicle id, 
#value= [ ...,[time_event, type_event, id_current_link_location,id_destination_link,t_exit],...  ] 
def fct_dict_single_que_information_created_by_sim(name_veh_file_read,line_number=3):
	
	
	#print("HERE",name_veh_file_read)
	#we open the file
	file=open(name_veh_file_read,"r")
		
	#we create the dict_que_inform, key= que id, value=[time,que length, event type,veh id]
	dict_que_inform={}
		
	#indicator of the number of lines already read.
	#A que file_# contains 2 lines with explanations, these lines will not be utilised for the creation of the dictionary,
	#they will be skipped.
	#the 3rd line is the que id
	ind=0
	
	for i in file.readlines():
		ind+=1
		if  ind==3:
			b=i.rsplit()
			dict_que_inform[eval(b[0]),eval(b[1])]=[]
			ind+=1
		else:
			if ind>line_number:
				a=i.rsplit()
				dict_que_inform[eval(b[0]),eval(b[1])].append([eval(a[0]),eval(a[1]),eval(a[2]),eval(a[3])])
				ind+=1
			
	file.close()
				
	return dict_que_inform

#*****************************************************************************************************************************************************************************************
#method  reading a vehicle file created by a sim (VEH_ID) and returning a dictionary of which key=vehicle id, 
#value= [ ...,[time_event, type_event, id_current_link_location,id_destination_link,t_exit],...  ] 
def fct_dict_veh_information_created_by_sim(name_veh_file_read,line_number=7):
	
	
	#print("HERE",name_veh_file_read)
	#we open the file
	file=open(name_veh_file_read,"r")
		
	#we create the dict_veh_inform
	dict_veh_inform={}
		
	#indicator of the number of lines already read.
	#A vehicle file contains 6 lines with explanations, these lines will not be utilised for the creation of the dictionary,
	#they will be skipped.
	ind=0
	
	for i in file.readlines():
		ind+=1
		if ind>line_number:
			a=i.rsplit()
			
			#the veh id is the 3rd column
			#if the veh id is not in the dict then we add it
			if (eval(a[2])) not in dict_veh_inform:
				dict_veh_inform[eval(a[2])]= [ [eval(a[0]),eval(a[1]),eval(a[3]),eval(a[4]),eval(a[5])]]
			#if the vehicle id is already in the dict then we simply add the new line
			else:
				dict_veh_inform[eval(a[2])].append( [eval(a[0]),eval(a[1]),eval(a[3]),eval(a[4]),eval(a[5])])
	file.close()			
	return dict_veh_inform

#*****************************************************************************************************************************************************************************************

#function reading a file (containing a matrix data) and returning a dictionary of which the key=number of line (starting with 1) 
#and the value is a list containing all elements of  each line of the file, converted to type 
#the file to read is one column (of type 1\n,2\n,...)
def function_reading_file_containing_matrix_one_column_data(file_name_read,type=int):

	#we open the file
	file=open(file_name_read,"r")
	
	#creation of the dictionary
	m_dict={}
	ind=1
	for i in file.readlines():
		a=i.rsplit()
		for j in a:
			m_dict[ind]=type(j)
		ind+=1
		
	file.close()
	return m_dict

#*****************************************************************************************************************************************************************************************
#function reading the file with the param of stoch travel time
#each such file is comprised of two colums, the fisrt is the link id, the second is the related value
def fct_reading_file_param_stoch_trav_time(file_name_read):
#we open the file
	file=open(file_name_read,"r")
	
	#creation of the dictionary
	dict_rep={}
	for i in file.readlines():
		a=i.rsplit()
		for j in a:
			dict_rep[eval(a[0])]=eval(a[1])
		
	file.close()
	return dict_rep



#*****************************************************************************************************************************************************************************************
#function reading a file and adds each line in a list.It returns a list of lists.
def fct_reading_file(name_file_read,nb_comment_lines):
	#we open the file
	file=open(name_file_read,"r")
	li=[]
	
	#indicator of the number of lines already read
	ind_line_read=0
	for i in file.readlines():
		ind_line_read+=1
		if ind_line_read>nb_comment_lines:
			a=i.rsplit()
			for j in a:
				li.append(eval(j))
	file.close()
	return li
#*****************************************************************************************************************************************************************************************
#function reading file "fi_id_entry_exit_lk_related_path.txt"
#it returns a dict, key =id entry-exit link, value=[ id links to follow to reach exit link]
def fct_reading_file_fi_id_entry_exit_lk_related_unique_path(name_file_read,nb_comment_lines):

	file=open(name_file_read,"r")
	
	di_rep={}
	
	#indicator of the number of lines already read
	ind_line_read=0
	for i in file.readlines():
		ind_line_read+=1
		if ind_line_read>nb_comment_lines:
			a=i.rsplit()
			a1=eval(a[0])
			a2=eval(a[1])
			for j in a[2:]:
				if (a1,a2) not in di_rep:
					di_rep[a1,a2]=[eval(j)]
				else:
					di_rep[a1,a2].append(eval(j))
				
	file.close()
	#print(di_rep)
	return di_rep

	

#*****************************************************************************************************************************************************************************************
#method examining if there are simultaneous vehicle departures from one queue case when micro sim is employed
#dict_single_que_info=dictionary, key=que id, value=[...,[time,que length, event type, veh id],...]
def fct_verifying_veh_dep_from_single_que_micro_manag(dict_single_que_info):
	#we extract the veh dep events, and we return a dict, key=time, value=event type.
	di_t_dep_ev={}
	for i in dict_single_que_info:
		print("QUE",i)
		for j in dict_single_que_info[i]:
			#if the type is end departure
			if j[2]==Cl_Event.TYPE_EV["type_ev_end_veh_departure_from_que"]:
				#if the time is not in the dict
				if j[0] not in di_t_dep_ev:
					di_t_dep_ev[j[0]]=[j[2]]
				#if the time is in the dictionary
				else:
					#if the type is end veh departure
						if di_t_dep_ev[j[0]]==Cl_Event.TYPE_EV["type_ev_end_veh_departure_from_que"]:
							print("PROBLEM IN QUE: ", i, "AT T:",j[0],"TWO EV END VEH DEP")
							import sys
							sys.exit()
					
					

#*****************************************************************************************************************************************************************************************

#function writing a list of lists in a file. Each element of the list (east list) will be writtnen on one line
def fct_writing_list_of_lists(name_file_to_write,li_valeurs, li_phrases,ty="%.1f\t"):

	file=open(name_file_to_write,"w")
	
	for i in lis_phrases:
		file.write("%s\t \n"%(i))
		
	for j in li_li_valeurs:
		for k in j:
			file.write(ty%(k))
		file.write("\n")
	file.close()

#*****************************************************************************************************************************************************************************************
#*****************************************************************************************************************************************************************************************
#*****************************************************************************************************************************************************************************************
#method reading a list of (vehicle)  files and for each of them creating a dictionary  of which the key is the vehicle id and
#the value is a list [t_vehicle_appearance_in_the_network, [id_entry_link, id_destination_link_1, id_destination_link_2,.... ] ]
#we consider that in the list_files each file is aready placed in the appropriate dictionary
#path_list_files="./FRes-Tue-24-Jul-2012_23-24-22/Sim_Treat/VEH_RES"
#val_line_number=7 when the veh final destination is dynamically constructed
def fct_creating_dict_list_veh_files_creat_by_sim_treat(veh_final_dest_dynam_construct,path_list_files,\
val_line_number_dyn_constr_veh_final_dest=7,val_line_number_initial_defined_veh_final_dest=8):
	
	#we create the dict with the veh information
	dict_vehicle_inform={}
		
	#we are placed in the direcroty where the vehicle files are
	#os.chdir("./Sim_Treat/VEH_RES")
	cur_dir=os.getcwd()
	#print("HEEREE",path_list_files)
	os.chdir(path_list_files)
	#print( len(os.listdir('.')))
	#for i in os.listdir('.'):
		#print(i)
	#print( len(os.listdir('.')))
	
	#if the veh final destination will dynamically be constructed
	if veh_final_dest_dynam_construct==List_Explicit_Values.initialisation_value_to_one:	
		#val_line_number_dyn_constr_veh_final_dest=7
		for i in os.listdir('.'):
			di=fct_creating_dict_veh_inform_from_veh_file_creat_by_sim_treat_when_final_dest_dynam_constructed(\
			name_file_read=i,line_number=val_line_number_dyn_constr_veh_final_dest)
			dict_vehicle_inform.update(di)
		os.chdir(cur_dir)	
	#if the veh final destination will  be defined by the veh appearance
	else:
		#val_line_number_initial_defined_veh_final_dest=8
		for i in os.listdir('.'):
			di= fct_creating_dict_veh_inform_from_veh_file_creat_by_sim_treat_when_veh_final_dest_initially_defined(\
			name_file_read=i,line_number=val_line_number_initial_defined_veh_final_dest)
			dict_vehicle_inform.update(di)
		os.chdir(cur_dir)
	
	#print("HERE",dict_vehicle_inform.keys())	
	return dict_vehicle_inform
			

#*****************************************************************************************************************************************************************************************
#method reading a list of (vehicle)  files and for each of them creating a dictionary  of which the key is the vehicle id and
#the value is a list [t_vehicle_appearance_in_the_network, [id_entry_link, id_destination_link_1, id_destination_link_2,.... ] ]
#we consider that in the list_files each file is aready placed in the appropriate dictionary
#path_list_files="./FRes-Tue-24-Jul-2012_23-24-22/Sim_Treat/VEH_RES"

#name_Fres_folder=FRes-Tue-24-Jul-2012_23-24-22
def fct_creating_dict_list_exited_veh_files_creat_by_sim_treat(veh_final_dest_dynam_construct,name_Fres_folder,\
val_line_number_dyn_constr_veh_final_dest=7,val_line_number_initial_defined_veh_final_dest=8):


	path_list_files=name_Fres_folder+"/"+File_Stats_Anal_Folders_And_Files.name_folder_veh_inform+"/"+File_Stats_Anal_Folders_And_Files.name_folder_veh_files
	
	#we create the dict with the veh information
	dict_vehicle_inform={}
		
	#we are placed in the direcroty where the vehicle files are
	#os.chdir("./Sim_Treat/VEH_RES")
	cur_dir=os.getcwd()
	#print("HEEREE",path_list_files)
	os.chdir(path_list_files)
	#print( len(os.listdir('.')))
	#for i in os.listdir('.'):
		#print(i)
	#print( len(os.listdir('.')))
	
	#if the veh final destination will dynamically be constructed
	if veh_final_dest_dynam_construct==List_Explicit_Values.initialisation_value_to_one:	
		#val_line_number_dyn_constr_veh_final_dest=7
		for i in os.listdir('.'):
			di=fct_creating_dict_exited_veh_inform_from_veh_file_creat_by_sim_treat(\
			name_file_read=i,line_number=val_line_number_dyn_constr_veh_final_dest)
			dict_vehicle_inform.update(di)
		os.chdir(cur_dir)	
	#if the veh final destination will  be defined by the veh appearance
	else:
		#val_line_number_initial_defined_veh_final_dest=8
		for i in os.listdir('.'):
			di=fct_creating_dict_exited_veh_inform_from_veh_file_creat_by_sim_treat(\
			name_file_read=i,line_number=val_line_number_initial_defined_veh_final_dest)
			dict_vehicle_inform.update(di)
		os.chdir(cur_dir)
	
	#print("HERE",dict_vehicle_inform.keys())	
	return dict_vehicle_inform
			

#*****************************************************************************************************************************************************************************************
#method creting a dict of the exited veh, key=(id entry, exit link), value=[t_veh_ap, t_veh_exit, 

#*****************************************************************************************************************************************************************************************
#method reading a file (created by a sim treatement) and creating a dictionary of which the key is the vehicle id and
#the value is a list [t_vehicle_appearance_in_the_network, [id_entry_link, id_destination_link_1, id_destination_link_2,.... ] ]
#line_number=7 when the veh final destination will dynam be constructed	
def fct_creating_dict_veh_inform_from_veh_file_creat_by_sim_treat_when_final_dest_dynam_constructed(name_file_read,line_number):
	
	#we open the file
	file=open(name_file_read,"r")
		
	#we create the dict_veh_inform
	dict_veh_inform={}
		
	#indicator of the number of lines already read.
	#A vehicle file contains 6 lines with explanations, these lines will not be utilised for the creation of the dictionary,
	#they will be skipped.
	ind=0

	
	for i in file.readlines():
		ind+=1
		if ind>line_number:
			a=i.rsplit()
			#if a vehicle appearance event, this imply that the vehicle (consequently son id=key of the dictionary)
			#does not exist in the dictionary
			if (eval(a[1]))==Cl_Event.TYPE_EV["type_ev_veh_appearance"]:
				#the columns of the reading file are: [event_time,event_type,veh_id,current_veh_id_location,id_destination_link,t_exit_from_netwk]

				dict_veh_inform[eval(a[2])]=[eval(a[0]), [eval(a[3]),eval(a[4]) ] ]
				
				
			#if the event type is a vehicle arrival
			elif eval(a[1])==Cl_Event.TYPE_EV["type_ev_veh_arrived_at_que"]:
				#we add the new current location, in the  2nd element of the list
				#print("HERE",a,dict_veh_inform.keys())
				dict_veh_inform[eval(a[2])][1].append(eval(a[4]) )
			
	file.close()
	
	
	#for i in dict_veh_inform:
		#dict_veh_inform[i].sort()
	#print("HERE1",dict_veh_inform[1])
	#import sys
	#sys.exit()
	
	return dict_veh_inform
				


#*****************************************************************************************************************************************************************************************
#method reading a file (created by a sim treatement) and creating a dictionary of which the key is the vehicle id and
#the value is a list [t_vehicle_appearance_in_the_network, t veh exit, id_entry_link, id_destination_link_1, id_destination_link_2,.... , id exit link ]
#line_number=7 when the veh final destination will dynam be constructed	
def fct_creating_dict_exited_veh_inform_from_veh_file_creat_by_sim_treat(name_file_read,line_number):
	
	#we open the file
	file=open(name_file_read,"r")
	#print("file",file)
		
	#we create the dict_veh_inform
	dict_veh_inform={}
		
	#indicator of the number of lines already read.
	#A vehicle file contains 6 lines with explanations, these lines will not be utilised for the creation of the dictionary,
	#they will be skipped.
	ind=0

	nb_lines=len(file.readlines())
	
	file=open(name_file_read,"r")
	
	#print("nb_lines",nb_lines)
	for i in file.readlines():
		ind+=1
		#print("nb_lines",nb_lines,"ind",ind)
		
		if ind>line_number:
			a=i.rsplit()
			#if a vehicle appearance event, this imply that the vehicle (consequently son id=key of the dictionary)
			#does not exist in the dictionary
			if (eval(a[1]))==Cl_Event.TYPE_EV["type_ev_veh_appearance"]:
				#the columns of the reading file are: [event_time,event_type,veh_id,current_veh_id_location,id_destination_link,t_exit_from_netwk]

				#dict_veh_inform[eval(a[2])]=[eval(a[0]), [eval(a[3]),eval(a[4]) ] ]
				
				#key=veh id, value[event time, id current location, id dest link}
				dict_veh_inform[eval(a[2])]=[eval(a[0]), eval(a[3]),eval(a[4])]
				
				
			#if the event type is a vehicle arrival
			elif (eval(a[1]))==Cl_Event.TYPE_EV["type_ev_veh_arrived_at_que"]:
				#we add the new current location, in the  2nd element of the list
				#print("HERE",a,dict_veh_inform.keys())
				
				dict_veh_inform[eval(a[2])].append(eval(a[4]) )
			#if we read the last line
			if ind==nb_lines:
				#print("ind==nb_lines",ind==nb_lines,eval(a[1]))
				if (eval(a[1]))==Cl_Event.TYPE_EV["type_ev_end_veh_departure_from_que"]:
					#if the vehicle exited we will consider it 
					t_exit=eval(a[5])
					if t_exit>0:
						dict_veh_inform[eval(a[2])].insert(1,t_exit)
					elif t_exit==-1:
						del dict_veh_inform[eval(a[2])]
			
					else:
						print("PROBLE IN GLOBAL FUNCTIONS, fct_creating_dict_exited_veh_inform_from_veh_file_creat_by_sim_treat, t_exit", t_exit)
						import sys
						sys.exit()
				else:
					del dict_veh_inform[eval(a[2])]
		
				
			
	file.close()
	
	
	#for i in dict_veh_inform:
		#dict_veh_inform[i].sort()
	#print("HERE1",dict_veh_inform[1])
	#import sys
	#sys.exit()
	
	return dict_veh_inform
				


#*****************************************************************************************************************************************************************************************
#method reading a file (created by a sim treatement) and creating a dictionary of which the key is the vehicle id and
#the value is a list [t_vehicle_appearance_in_the_network, id_entry_link,id_final_dest_link ]
#line_number=8	
def fct_creating_dict_veh_inform_from_veh_file_creat_by_sim_treat_when_veh_final_dest_initially_defined(name_file_read,line_number):
	
	#we open the file
	file=open(name_file_read,"r")
		
	#we create the dict_veh_inform
	dict_veh_inform={}
		
	#indicator of the number of lines already read.
	#A vehicle file contains 6 lines with explanations, these lines will not be utilised for the creation of the dictionary,
	#they will be skipped.
	ind=0

	
	for i in file.readlines():
		ind+=1
		if ind>line_number:
			a=i.rsplit()
			
			#if a vehicle appearance event, this imply that the vehicle (consequently son id=key of the dictionary)
			#does not exist in the dictionary
			
			if (eval(a[1]))==Cl_Event.TYPE_EV["type_ev_veh_appearance"]:
				#the columns of the reading file are: [event_time,event_type,veh_id,current_veh_id_location,id_destination_link,t_exit_from_netwk,id_veh_final_dest]

				dict_veh_inform[eval(a[2])]=[eval(a[0]),eval(a[3]),eval(a[6])]
			
	file.close()
	
	
	#for i in dict_veh_inform:
		#dict_veh_inform[i].sort()
	#print("HERE1",dict_veh_inform[1])
	#import sys
	#sys.exit()
	
	return dict_veh_inform
				


#*****************************************************************************************************************************************************************************************
#method reading a file (created by a sim treatement) and creating a dictionary of which the key is the vehicle id and
#the value is a list [[t_ev,type_ev, id_current_veh_lk_location,id_dest_link_loc,t_exit_from_netw ],....]
	
def fct_creating_dict_veh_inform_from_veh_file_creat_by_sim_treat_all_inf(name_file_read,line_number=7):
	
	#we open the file
	file=open(name_file_read,"r")
		
	#we create the dict_veh_inform
	dict_veh_inform={}
		
	#indicator of the number of lines already read.
	#A vehicle file contains 6 lines with explanations, these lines will not be utilised for the creation of the dictionary,
	#they will be skipped.
	ind=0

	
	for i in file.readlines():
		ind+=1
		if ind>line_number:
			a=i.rsplit()
			li=[]
			li.append([eval(a[0]),eval(a[1]),eval(a[3]),eval(a[4]),eval(a[5])])
				
	di_veh_inform[eval(eval(a[2]))]=li			
			
			
	file.close()
	
	
	#for i in dict_veh_inform:
		#dict_veh_inform[i].sort()
	#print("HERE1",dict_veh_inform[1])
	#import sys
	#sys.exit()
	
	return dict_veh_inform
				


#*****************************************************************************************************************************************************************************************
#method creating a dictionary, key=id_of_entry_link
#value= [..., [t_appearance_veh, veh_id, [id_current_link_location_1,id_destination_link_1,...]     ]  ]  
#this dictionary will be employed when  we do a new sim emloying a previously created demand, so as to 
#create the veh appearance events
#dict_vehicle_inform= dict with key the vehicle id and value [t_appearance, [id_current_link_location_1,id_destination_link_1,...] ]
#name_file_with_veh_ap_ev_end_sim_to_read= file containing the t_appearance, id_entry_link 

def fct_creat_dict_veh_appearance_info_entry_link_when_final_dest_dynam_constructed_1(\
dict_vehicle_inform,name_file_with_veh_ap_ev_end_sim_to_read):
	
	dict_entry_link_info={}
	
	#dict_vehicle_inform is a dict with key=veh_id, value=[t_veh_ap,[id_entry_link,id_dest_link_1,id_dest_link_2,...]]
	for i in dict_vehicle_inform:
		#if the id of the entry link is not in the doctionary
		if dict_vehicle_inform[i][1][0] not in dict_entry_link_info:
			#we add a new elem in the dict,
			dict_entry_link_info[dict_vehicle_inform[i][1][0]] =[ [dict_vehicle_inform[i][0],i, dict_vehicle_inform[i][1]] ]
		
		#if the id of the entry link is in the dictionary
		else:
			dict_entry_link_info[dict_vehicle_inform[i][1][0]].append([dict_vehicle_inform[i][0],i, dict_vehicle_inform[i][1] ])
	
	#print(dict_vehicle_inform)
	#import sys
	#sys.exit()
	#we open the file with the veh appear inform event  remaining in the event list by the end of the sim
	
	file=open(name_file_with_veh_ap_ev_end_sim_to_read,"r")
	#print("name_file_with_veh_ap_ev_end_sim_to_read",name_file_with_veh_ap_ev_end_sim_to_read)
	
	for i in file.readlines():
		#print()
		#print("HERE",i)
		#print("HERE1",eval(i)[1])
		#print("HERE2",dict_entry_link_info.keys())
		#import sys
		#sys.exit()
		#print("HERE4",eval(i),dict_entry_link_info.keys(),eval(i)[1])
		dict_entry_link_info[eval(i)[1]].append([eval(i)[0],-1,[eval(i)[1]] ])
		#if eval(i)[1] in dict_entry_link_info:
			#dict_entry_link_info[eval(i)[1]].append([eval(i)[0],-1,[eval(i)[1]] ])
		#else:
			#dict_entry_link_info[eval(i)[1]]=[[eval(i)[0],-1,[eval(i)[1]] ]]
			#print("HERE",dict_entry_link_info[eval(i)[1]])
	
		
	file.close()
	for i in dict_entry_link_info:
		#print(dict_entry_link_info[i])
		#import sys
		#sys.exit()
		dict_entry_link_info[i].sort()
			

	return dict_entry_link_info

#*****************************************************************************************************************************************************************************************
#method creating a dictionary, key=id_of_entry_link
#value= [..., [t_appearance_veh, veh_id],...]  
#this dictionary will be employed when  we do a new sim emloying a previously created demand, so as to 
#create the veh appearance events
#dict_vehicle_inform= dict with key the vehicle id and value [t_appearance, [id_current_link_location_1,id_destination_link_1,...] ]
#name_file_with_veh_ap_ev_end_sim_to_read= file containing the t_appearance, id_entry_link 

def fct_creat_dict_veh_appearance_info_entry_link_when_final_dest_dynam_constructed(\
dict_vehicle_inform,name_file_with_veh_ap_ev_end_sim_to_read):
	
	dict_entry_link_info={}
	
	#dict_vehicle_inform is a dict with key=veh_id, value=[t_veh_ap,[id_entry_link,id_dest_link_1,id_dest_link_2,...]]
	for i in dict_vehicle_inform:
		#if the id of the entry link is not in the doctionary
		if dict_vehicle_inform[i][1][0] not in dict_entry_link_info:
			#we add a new elem in the dict,
			dict_entry_link_info[dict_vehicle_inform[i][1][0]] =[[dict_vehicle_inform[i][0],i]]
		
		#if the id of the entry link is in the dictionary
		else:
			dict_entry_link_info[dict_vehicle_inform[i][1][0]].append([dict_vehicle_inform[i][0],i])
	
	#print(dict_vehicle_inform)
	#import sys
	#sys.exit()
	#we open the file with the veh appear inform event  remaining in the event list by the end of the sim
	
	file=open(name_file_with_veh_ap_ev_end_sim_to_read,"r")
	#print("name_file_with_veh_ap_ev_end_sim_to_read",name_file_with_veh_ap_ev_end_sim_to_read)
	
	#each line = t_veh_appearance, id_entry_lk, -1
	for i in file.readlines():
		#print()
		#print("HERE",i)
		#print("HERE1",eval(i)[1])
		#print("HERE2",dict_entry_link_info[1])
		#import sys
		#sys.exit()
		#print("HERE4",eval(i),dict_entry_link_info.keys(),eval(i)[1])
		dict_entry_link_info[eval(i)[1]].append([eval(i)[0],-1])
		#if eval(i)[1] in dict_entry_link_info:
			#dict_entry_link_info[eval(i)[1]].append([eval(i)[0],-1,[eval(i)[1]] ])
		#else:
			#dict_entry_link_info[eval(i)[1]]=[[eval(i)[0],-1,[eval(i)[1]] ]]
			#print("HERE",dict_entry_link_info[eval(i)[1]])
	
		
	file.close()
	for i in dict_entry_link_info:
		#print(dict_entry_link_info[i])
		#import sys
		#sys.exit()
		dict_entry_link_info[i].sort()
			

	return dict_entry_link_info

#*****************************************************************************************************************************************************************************************
#method creating a dictionary, key=id_of_entry_link
#value= [..., [t_appearance_veh, veh_id],..  ]  
#IN THIS CASE WE COSIDER THAT THE PATH FROM THE  VEH ORIGIN TO THE VEH FINAL DEST IS UNIQUE
#this dictionary will be employed when  we do a new sim emloying a previously created demand, so as to 
#create the veh appearance events
#dict_vehicle_inform is a dict with key=veh_id, value=[t_veh_ap,id_entry_link,id_veh_final_dest_link]]
#name_file_with_veh_ap_ev_end_sim_to_read= file containing the t_appearance, id_entry_link 

def fct_creat_dict_veh_appearance_info_entry_link_when_veh_final_dest_initially_defined(\
dict_vehicle_inform,name_file_with_veh_ap_ev_end_sim_to_read):
	
	#dict_entry_link_info = dict, key=id entry link, value= [..., [t_appearance_veh, veh_id],..  ] 
	dict_entry_link_info={}
	
	#dict_vehicle_inform is a dict with key=veh_id, value=[t_veh_ap,id_entry_link,id_veh_final_dest_link]]
	for i in dict_vehicle_inform:
	
		#if the id of the entry link is not in the doctionary
		if dict_vehicle_inform[i][1] not in dict_entry_link_info:
			#we add a new elem in the dict,
			dict_entry_link_info[dict_vehicle_inform[i][1]] =[ [dict_vehicle_inform[i][0],i] ]
		
		#if the id of the entry link is in the dictionary
		else:
			dict_entry_link_info[dict_vehicle_inform[i][1]].append([dict_vehicle_inform[i][0],i])

	
	file=open(name_file_with_veh_ap_ev_end_sim_to_read,"r")
	#print("name_file_with_veh_ap_ev_end_sim_to_read",name_file_with_veh_ap_ev_end_sim_to_read)
	#print("dict_entry_link_info.keys",dict_entry_link_info.keys())
	
	#each line, t_veh_ap, id_entry_lk, veh final dest=-1 pas encore decidee
	for i in file.readlines():
		#print()
		#print("HERE",i,eval(i)[1])
		#print("HERE1",eval(i)[1])
		#print("HERE2",dict_entry_link_info.keys())
		
		#print("HERE4",eval(i),dict_entry_link_info.keys(),eval(i)[1])
		dict_entry_link_info[eval(i)[1]].append([eval(i)[0],-1])
		#if eval(i)[1] in dict_entry_link_info:
			#dict_entry_link_info[eval(i)[1]].append([eval(i)[0],-1,[eval(i)[1]] ])
		#else:
			#dict_entry_link_info[eval(i)[1]]=[[eval(i)[0],-1,[eval(i)[1]] ]]
			#print("HERE",dict_entry_link_info[eval(i)[1]])
	file.close()
	for i in dict_entry_link_info:
		#print(dict_entry_link_info[i])
		#import sys
		#sys.exit()
		dict_entry_link_info[i].sort()
			
	#print("dict_entry_link_info",dict_entry_link_info)
	#print("dict_entry_link_info",dict_entry_link_info.keys())
	#print("dict_entry_link_info",dict_entry_link_info[8])
	#import sys
	#sys.exit()
	return dict_entry_link_info

#*****************************************************************************************************************************************************************************************
#method returning a dict with the veh information for each entry link, key = id entry link, 
#if the  sim cosntruct the veh final destination by the veh appear, value= [..., [t_appearance_veh, veh_id],..  ]  
#if the veh final dest is dynam constructed, value= [..., [t_appearance_veh, veh_id, [id_current_link_location_1,id_destination_link_1,...]     ]  ] 
def  fct_creat_dict_information_entry_link_prev_sim(v_veh_final_dest_dynam_construct,\
v_dict_vehicle_inform,v_name_file_with_veh_ap_ev_end_sim_to_read):

	#if the veh final dest will dynam be contructed
	if v_veh_final_dest_dynam_construct==List_Explicit_Values.initialisation_value_to_one:
		di_rep=fct_creat_dict_veh_appearance_info_entry_link_when_final_dest_dynam_constructed(\
		dict_vehicle_inform=v_dict_vehicle_inform,\
		name_file_with_veh_ap_ev_end_sim_to_read=v_name_file_with_veh_ap_ev_end_sim_to_read)
	
	#if the veh final dest will be defined by the veh appearance
	else:
		di_rep=fct_creat_dict_veh_appearance_info_entry_link_when_veh_final_dest_initially_defined(\
		dict_vehicle_inform=v_dict_vehicle_inform,\
		name_file_with_veh_ap_ev_end_sim_to_read=v_name_file_with_veh_ap_ev_end_sim_to_read)
		
	return di_rep
	
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
#*****************************************************************************************************************************************************************************************
#*****************************************************************************************************************************************************************************************
#*****************************************************************************************************************************************************************************************
#*****************************************************************************************************************************************************************************************
#we write the file with the parameters of the FT control
#lis_phrases=[["id nd (1st colm), id stage (2nd colm, if id=0 it is rd cleat), actuat durat (3rd colm),t end cycle(5th colm)"],\
#["for a given inersection the order of stage id is related to  their priority within the cycle" ]]
#lis_valeurs=[[1,1,15,60],[1,0,3,60],[1,2,35,60],[1,0,7,60],[2,1,25,60],[2,0,5,60],[2,2,25,5,60],[2,0,5,60]]
#fct_write_file_parameters_ft_control(name_file_to_write=File_Sim_Name_Module_Files.val_name_file_values_ft_control,li_valeurs=lis_valeurs,li_phrases=lis_phrases)

#we read the file with the parameters of the FT control
#di=fct_reading_file_parameters_FT_control(name_file_to_read="./Control_Param_Files"+"/"+File_Sim_Name_Module_Files.val_name_file_values_ft_control,nb_comment_lines=2)
#print(di)

#we read the file with the intersection stages
#di_s=function_reading_file_intersection_stages(path_and_name_file_read="../../SMALL_DATA_2NDS/"+\
#File_Sim_Name_Module_Files.val_name_file_stages_each_inters,nb_comment_lines=1)
#print(di_s)



#we wrtie the file fi_mrp_id_phase_prob_dest_lk
#li_phrases=["Id phase (1-2 columns), prob rout proportion (3rd column)"]
#li_valeurs=[ [1,2,1],[2,3,1],[4,5,0.5],[4,10,0.5],[5,6,0.5],[5,8,0.5],[7,2,0.33],[7,6,0.33],[7,8,0.33],[9,3,0.33],[9,5,0.33],[9,10,0.33]  ]
#fct_write_fi_id_phase_prob_dest_lk(name_file_to_write=File_names_network_model.val_name_file_mat_rp_id_phase_prob_dest_lk+".txt",\
#list_phrases=li_phrases,list_valeurs=li_valeurs)

#we write two files,  "fi_mrp_cum_id_lk_val_cum_funct_dest_lk" and ''fi_id_entry_intern_lk_id_dest_lk.txt)
#fct_write_li_files_fi_id_phase_val_cum_funct_rout_prop_and_fi_id_entry_intern_lk_id_dest_lk(\
#va_name_folder_mrp="../../SMALL_DATA_2NDS/ROUT_PROB",\
#v_nb_fi_mrp_id_phase_prob_dest_lk=1,va_nb_comment_lines=1,va_considered_one_in_cum_fct=0.98)


#fct_reading_file_fi_id_entry_exit_lk_related_unique_path(name_file_read="fi_id_entry_exit_lk_related_path.txt",nb_comment_lines=1)





















	
	

#*****************************************************************************************************************************************************************************************


