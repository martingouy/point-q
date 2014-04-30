import xml.etree.ElementTree as ET

#method parsing a specific format of network file.
#values of balises (attributs) are considered given. ATTENTION ( if these names change, results will be wrong,
#emtry values will be returned....) ! ! ! 

#we return a dict, key=nod id, value=dict having keys "li_output_links_id", "li_input_lk_id","type " (indicating if an intersection
#is/not signalised),"id" indicating the node id
#tree=Object de type Element ou on met la fichier lu, for ex: tree = ET.parse(val_name_file_to_read)
def fct_creating_di_node_inform(tree,\
val_name_elem_networklist="NetworkList",val_name_elem_nodelist="NodeList",\
val_name_elem_id_attrib="id",val_name_elem_inputs="inputs",val_name_elem_input="input",\
val_name_elem_link_id="link_id",val_name_elem_outputs="outputs",val_name_elem_output="output"):

	#lecture du fichier et on le stock dans un objet de type Element
	#tree = ET.parse(val_name_file_to_read)
	root = tree.getroot()

	#print("etiquette racine:",root.tag)

	#les attributs de la racine, 
	#print("balise racine:",root.attrib)

	#Element.findall() finds only elements with a tag which are direct children of the current element
	#reponse= objet de type Elements NetworkList et leurs adresses
	for j in root.findall(val_name_elem_networklist):
		#print("Element NetworkList:",j)
		for m in j:
			#print("m=",m)
			#liste d'elem NodeList,[...,Element NodeList et son adresse,...]
			nd_list=m.findall(val_name_elem_nodelist)
		
			#print("nd_lis",nd_list)
		
			#pour chaque element NodeList on recupere ses attributs
		
			#dict, key=id node, value=dict {'type'=si/nsi, "id"=integer}
			di={}
			#pour chaque NodeList
			for k in nd_list:
				#print("k=",k)
				#pour chaque enfant de NodeList (ses enfants=suite de nodes)
				for n in k:
					#print("n=",n)
					di_1={}
					#print(n.attrib["id"])
					di_1[eval(n.attrib[val_name_elem_id_attrib])]=n.attrib
					#print("di_1",di_1)
					
					#di.update(di_1)
					#print("di",di)
				
					#on cherche les balises "inputs" du noeud enfant
					input_lk=n.find(val_name_elem_inputs)
					#print("input_lk",input_lk)
					li_2=[]
					di_2={}
					for p in input_lk.iter(val_name_elem_input):
						#print("attributs input_lk",p.attrib)
						li_2.append(p.attrib[val_name_elem_link_id])
						#print()
					
					di_2["li_input_link_id"]=li_2
					di_1[eval(n.attrib[val_name_elem_id_attrib])].update(di_2)
					di.update(di_1)
					#print("di",di)
				
					#recherche de balises "outputs" du noeud enfant
					input_lk=n.find(val_name_elem_outputs)
					#print("input_lk",input_lk)
					li_2=[]
					di_2={}
					for q in input_lk.iter(val_name_elem_output):
						#print("attributs input_lk",p.attrib)
						li_2.append(q.attrib[val_name_elem_link_id])
						#print()
					
					di_2["li_output_link_id"]=li_2
					di_1[eval(n.attrib[val_name_elem_id_attrib])].update(di_2)
					di.update(di_1)
					#print("di",di)
	#print("di=",di.keys())
	#import sys
	#sys.exit()
	#print("di_nd",di)		
	return di
#**********************************************************************************************************************************************************
#tree=Object de type Element ou on met la fichier lu, for ex: tree = ET.parse(val_name_file_to_read)
#dict, key=link id, value=dict with keys :'dest_nd_id','length','lanes','origin_nd_id','type','id','in_sync',
#'lane_offset'
def fct_creating_di_link_infor(tree,\
val_name_elem_networklist="NetworkList",val_name_elem_linklist="LinkList",val_name_elem_id_attrib="id",\
val_name_elem_node_id="node_id",val_name_origin_node_attribut="begin",val_name_destination_node_attribut="end",\
val_name_attribut_origin_node_lk="origin_nd_id",val_name_attribut_dest_node_lk="dest_nd_id"):

	#lecture du fichier et on le stock dans un objet de type Element
	#tree = ET.parse(val_name_file_to_read)
	
	root = tree.getroot()
	
	#les attributs de la racine, rep={}
	#print("balise racine:",root.attrib)
	
	#Element.findall() finds only elements with a tag which are direct children of the current element
	#reponse= objet de type Elements NetworkList et leurs adresses
	for j in root.findall(val_name_elem_networklist):
		#print("Element NetworkList:",j)
		for m in j:
			#we recupere tous les elements Link
			#liste d'elem NodeList,[...,Element LinkList et son adresse,...]
			lk_list=m.findall(val_name_elem_linklist)
		
			#print("lk_lis",lk_list)
		
			#pour chaque element LinkList on recupere ses attributs
			di={}
			#pour chaque LinkList
			for k in lk_list:
				for n in k:
					#print("n=",n)
					di_1={}
					#print(n.attrib)
					di_1[eval(n.attrib[val_name_elem_id_attrib])]=n.attrib
					orig_nd=n.find(val_name_origin_node_attribut)
					dest_nd=n.find(val_name_destination_node_attribut)
					di_1[eval(n.attrib[val_name_elem_id_attrib])][val_name_attribut_origin_node_lk]=orig_nd.attrib[val_name_elem_node_id]
					di_1[eval(n.attrib[val_name_elem_id_attrib])][val_name_attribut_dest_node_lk]=dest_nd.attrib[val_name_elem_node_id]
					di.update(di_1)
					#movement=n.find(val_name_attribut_movement)
					
					#if movement!=None:
						#for p in movement:
							#print("id link",n.attrib[val_name_elem_id_attrib])
							#print("MOV",p.attrib)
							#if val_name_attribut_movement not in di_1[n.attrib[val_name_elem_id_attrib]]:
								#di_1[eval(n.attrib[val_name_elem_id_attrib])][val_name_attribut_movement]=[p.attrib]
							#else:
								#di_1[eval(n.attrib[val_name_elem_id_attrib])][val_name_attribut_movement].append(p.attrib)
							#di.update(di_1)
					#lanes=n.find(val_name_attribut_lane)
					#print("lanes",lanes)
					#for m in lanes:
						
						#if val_name_attribut_lane not in di_1[n.attrib[val_name_elem_id_attrib]]:
							#di_1[n.attrib[val_name_elem_id_attrib]][val_name_attribut_lane]=[m.attrib]
						
						#else:
							#print("di_1[n.attrib[val_name_elem_id_attrib]][val_name_attribut_lane]",di_1[n.attrib[val_name_elem_id_attrib]][val_name_attribut_lane])
							#di_1[n.attrib[val_name_elem_id_attrib]][val_name_attribut_lane].append(m.attrib)
						#di.update(di_1)	
						
						#if key movement not in dictionary
						#print("mov in dict",\
						#val_name_key_movement not in di_1[n.attrib[val_name_elem_id_attrib]])
						#if val_name_key_movement not in di_1[n.attrib[val_name_elem_id_attrib]]:
							#di_1[n.attrib[val_name_elem_id_attrib]][val_name_key_movement]=[movement.attrib]
						#if key movement in dictionary
						#else:
							#di_1[n.attrib[val_name_elem_id_attrib]][val_name_key_movement].append(movement.attrib)
						#di.update(di_1)
					#print(di)
					#print()
	#print("di_links",di['2'])
	#print("di_links",len(di['2']['lanes'][1]))
	#print("di lk info",di)
	#import sys
	#sys.exit()
	return di
#**********************************************************************************************************************************************************

#method reading an xml  file and returning [dict_nd_info, dict_lk_info]
def fct_creat_li_di_node_and_link_info(\
val_name_file_to_read="scenario_example.xml",\
va_name_elem_networklist="NetworkList",va_name_elem_nodelist="NodeList",\
va_name_elem_id_attrib="id",va_name_elem_inputs="inputs",va_name_elem_input="input",\
va_name_elem_link_id="link_id",va_name_elem_outputs="outputs",va_name_elem_output="output",\
va_name_elem_linklist="LinkList",\
va_name_elem_node_id="node_id",va_name_origin_node_attribut="begin",va_name_destination_node_attribut="end",\
va_name_attribut_origin_node_lk="origin_nd_id",va_name_attribut_dest_node_lk="dest_nd_id"):

	#lecture du fichier et on le stock dans un objet de type Element
	v_tree = ET.parse(val_name_file_to_read)
	
	#creation dict of nodes
	#dict, key=nod id, value=dict having keys "li_output_links_id", "li_input_lk_id","type " (indicating if an intersection
	#is/not signalised),"id" indicating the node id
	di_nd_info=fct_creating_di_node_inform(tree=v_tree,\
	val_name_elem_networklist=va_name_elem_networklist,val_name_elem_nodelist=va_name_elem_nodelist,\
	val_name_elem_id_attrib=va_name_elem_id_attrib,val_name_elem_inputs=va_name_elem_inputs,\
	val_name_elem_input=va_name_elem_input,\
	val_name_elem_link_id=va_name_elem_link_id,val_name_elem_outputs=va_name_elem_outputs,\
	val_name_elem_output=va_name_elem_output)
	
	#creation dict of links
	#dict, key=link id, value=dict with keys :'dest_nd_id','length','lanes','origin_nd_id','type','id','in_sync',
	#'lane_offset'
	di_lk_info=fct_creating_di_link_infor(tree=v_tree,\
	val_name_elem_networklist=va_name_elem_networklist,val_name_elem_linklist=va_name_elem_linklist,\
	val_name_elem_id_attrib=va_name_elem_id_attrib,val_name_elem_node_id=va_name_elem_node_id,\
	val_name_origin_node_attribut=va_name_origin_node_attribut,\
	val_name_destination_node_attribut=va_name_destination_node_attribut,\
	val_name_attribut_origin_node_lk=va_name_attribut_origin_node_lk,\
	val_name_attribut_dest_node_lk=va_name_attribut_dest_node_lk)
	
	li_rep=[di_nd_info,di_lk_info]
	#li_rep=[di_nd_info]
	
	return li_rep
#**********************************************************************************************************************************************************	

#fct creating  network files related to entry links
def fct_creat_di_id_node_li_entry_links(di_nd_infor,di_lk_infor,val_name_attribut_type_node="type",val_name_terminal_node="terminal",\
val_name_output_links="li_output_link_id",val_name_dest_node="dest_nd_id"):

	#on choisit les nodes terminal, on prend ceux ayant input links, ils sont les entry 
	
	#di_nd_info=key=id node, value= dict ayant cles="li_output_links_id", "li_input_lk_id", "type " (indicating if an intersection
	#is/not signalised),"id" indicating the node id
	di_key_id_node_value_li_entry_links={}
	
	#pour chaque noeud 
	for i in di_nd_infor:
		#print()
		#print("id noeud=",i)
		#if the node type is terminal
		if di_nd_infor[i][val_name_attribut_type_node]==val_name_terminal_node:
			#print("id terminal noeud",i)
		
			#si le noeud a des output links
			if di_nd_infor[i][val_name_output_links]!=[]:
				#print("output links noeud term: ",di_nd_infor[i][val_name_output_links])
				#print()
				
			
				#di_lk_infor= dict, key=link id, value=dict with keys :'dest_nd_id','length','lanes','origin_nd_id','type','id'
				#pour chaque output arc du noeud terminal
				if di_nd_infor[i][val_name_output_links]!=[]:
					#print("ici nd terminal avec output",di_nd_infor[i][val_name_output_links])
					for j in di_nd_infor[i][val_name_output_links]:
						#print("output link nd terminal",j)
						#on recupere son noeud de destination
						id_nd=eval(di_lk_infor[eval(j)][val_name_dest_node])
						#print("id_dest nd",id_nd)
						#print("dest nd link",id_nd)
						#print("di",di_key_id_node_value_li_entry_links)
						#print("id_nd not in di",id_nd not in di_key_id_node_value_li_entry_links)
						#print()
						if id_nd not in di_key_id_node_value_li_entry_links:
							di_key_id_node_value_li_entry_links[id_nd]=[eval(j)]
						else:
							di_key_id_node_value_li_entry_links[id_nd].append(eval(j))
						
				#di_key_id_node_value_li_entry_links.update(di)
	#print("di_key_id_node_value_li_entry_links",di_key_id_node_value_li_entry_links)
	#import sys
	#sys.exit()			
	return di_key_id_node_value_li_entry_links	

#**********************************************************************************************************************************************************
#fct creating  network files related to exit links
def fct_creat_di_id_node_li_exit_links(di_nd_infor,di_lk_infor,val_name_attribut_type_node="type",val_name_terminal_node="terminal",\
val_name_input_links="li_input_link_id",val_name_origin_node="origin_nd_id"):

	#on choisit les nodes terminal, on prend ceux ayant intput links, ils sont les exit 
	
	#di_nd_info=key=id node, value= dict ayant cles="li_output_links_id", "li_input_lk_id", "type " (indicating if an intersection
	#is/not signalised),"id" indicating the node id
	di_key_id_node_value_li_exit_links={}
	
	#pour chaque noeud de type terminal
	for i in di_nd_infor:
		#if the node type is terminal
		if di_nd_infor[i][val_name_attribut_type_node]==val_name_terminal_node:
			#print("id terminal noeud",i)
		
			#si le noeud a des input links
			if di_nd_infor[i][val_name_input_links]!=[]:
				#print("input links noeud term: ",di_nd_infor[i][val_name_input_links])
				#print()
				
			
				#di_lk_infor= dict, key=link id, value=dict with keys :'dest_nd_id','length','lanes','origin_nd_id','type','id'
				#pour chaque input arc du noeud terminal
				for j in di_nd_infor[i][val_name_input_links]:
					#print("j",j)
					#on recupere son noeud de destination
					id_nd=eval(di_lk_infor[eval(j)][val_name_origin_node])
					#print("dest nd link",id_nd)
					#print("di",di_key_id_node_value_li_entry_links)
					#print("id_nd not in di",id_nd not in di_key_id_node_value_li_entry_links)
					#print()
					if id_nd not in di_key_id_node_value_li_exit_links:
						di_key_id_node_value_li_exit_links[id_nd]=[eval(j)]
					else:
						di_key_id_node_value_li_exit_links[id_nd].append(eval(j))
						
				#di_key_id_node_value_li_entry_links.update(di)
	#print("di_key_id_node_value_li_exit_links",di_key_id_node_value_li_exit_links)			
	return di_key_id_node_value_li_exit_links	

#**********************************************************************************************************************************************************
#fct creat liste non-signalised and signalised entry links
#it returns a dictionary; key=1 or 0 according to when the link is.not signalised, , value=list entry links
def fct_creat_di_s_and_ns_entry_links(val_di_id_nd_value_li_id_entry_links,val_di_node_info,val_name_node_type="type",\
val_name_signalised_nd="signalized",val_name_nonsignalised_nd="unsignalized",val_indicator_sign_lk=1,\
val_indicator_nonsign_lk=0):

	di_rep={}
	
	#pour chaque noeud
	for i in val_di_id_nd_value_li_id_entry_links:
		#print("i=",i, val_di_id_nd_value_li_id_entry_links.keys())
		#val_di_node_info= dict, key id node, value dict having keys 
		#"li_output_links_id", "li_input_lk_id","type " (indicating if an intersection
		#is/not signalised),"id" indicating the node id
		if val_di_node_info[i][val_name_node_type]==val_name_signalised_nd:
			if val_indicator_sign_lk not in di_rep:
				di_rep[val_indicator_sign_lk]=val_di_id_nd_value_li_id_entry_links[i]
			else:
				di_rep[val_indicator_sign_lk].extend(val_di_id_nd_value_li_id_entry_links[i])
		
		elif val_di_node_info[i][val_name_node_type]==val_name_nonsignalised_nd:
			if val_indicator_nonsign_lk not in di_rep:
				di_rep[val_indicator_nonsign_lk]=val_di_id_nd_value_li_id_entry_links[i]
			else:
				di_rep[val_indicator_nonsign_lk].extend(val_di_id_nd_value_li_id_entry_links[i])
				
	return di_rep
#**********************************************************************************************************************************************************
#fct creating dict, key=link id, 
#value=[link capacity as defined in the xml file, jam density, free flow speed, stand deviat of free flow speed]
def fct_creat_di_id_lk_id_value_li_lk_cap_jam_dens_ffs_stan_dev_as_indicated_in_xml(tree,\
val_name_elem_fundamentaldiagramset="FundamentalDiagramSet",val_name_fundamentaldiagram="fundamentalDiagram",\
val_name_attribut_link_id="link_id",val_name_attribut_capacity="capacity",val_name_attribut_jam_density="jam_density",\
val_name_attribut_free_flow_speed="free_flow_speed",val_name_attribut_std_dev_free_flow_speed="std_dev_free_flow_speed"):

	root = tree.getroot()
	
	for i in root.findall(val_name_elem_fundamentaldiagramset):
		#print("i=",i)
		#les attributs de chaque noeud de "FundamentalDiagramSet", cad, les attributs de "fundamentalDiagramProfile" = link id
		di={}
		for j in i:
			#print("attrib",j.attrib)
			#j.attrib=dict, key="link_id", value= link id as string
			#di[j.attrib]=[]
			for m in j.findall(val_name_fundamentaldiagram):
				#print("m=",m,m.attrib)
				di[eval(j.attrib[val_name_attribut_link_id])]=[m.attrib[val_name_attribut_capacity],m.attrib[val_name_attribut_jam_density],\
				m.attrib[val_name_attribut_free_flow_speed],m.attrib[val_name_attribut_std_dev_free_flow_speed]]
				#print("di",di)
		#for j in i:
			#print("i=",i)
	#di=dict, key=id link, value=[sat flow, jam density,vitesse moyenne,stand deviat ffs]
	#jam=veh/meter/lane a peu pres ma capacite
	#print("di_ja",di)
	#import sys
	#sys.exit()
	return di

#**********************************************************************************************************************************************************
#method creating di key=id link, value=[id origin nd, id dest nd, length link, capacity lk, param travel duration]
#length link= (total nb of lanes) x length
#capacity lk= length link x (nb of lanes) x jam density
def fct_creat_di_id_lk_value_li_id_orig_dest_nd_length_lk_capacity_lk_param_travel_duration(\
di_key_id_lk_value_li_sat_flow_jam_density_mean_spead_stan_dev,di_key_id_lk_value_nb_lanes,di_lk_inform,\
val_name_attribute_id_dest_node="dest_nd_id",val_name_attribute_id_origin_node="origin_nd_id",val_name_attribute_length="length",val_round_prec_lk_length=0,\
val_round_prec_vit_moy=1):

	di_rep={}

	#print(di_lk_inform)
	
	#di_key_id_lk_value_li_sat_flow_jam_density_mean_spead_stan_dev= dict, key=link id
	#valeur=[sat flow, jam density,vitesse moyenne,stand deviat ffs]
	
	for i in di_key_id_lk_value_li_sat_flow_jam_density_mean_spead_stan_dev:
		#print()
		#print("lk id",i)
	
		#if the link is not an exit one,di_lk_inform=dict, key=id link, value=dict={...,"dest_nd_id"=, "orugin nd id="=,...}
		if eval(di_lk_inform[i][val_name_attribute_id_dest_node])!=-1:
		
			#if it is not en entry link
			if eval(di_lk_inform[i][val_name_attribute_id_origin_node])!=-1:
				# we calculate the length of the link, (total nb of lanes) x length
				length_lk=round(di_key_id_lk_value_nb_lanes[i] * eval (di_lk_inform[i][val_name_attribute_length]),val_round_prec_lk_length)
				#print("nb lanes",di_key_id_lk_value_nb_lanes[i], "length/lane",eval (di_lk_inform[i][val_name_attribute_length]))
				#print("length_lk",length_lk)
			
				#we calculate the link capacity=length x jam 
				link_cap=length_lk * eval(di_key_id_lk_value_li_sat_flow_jam_density_mean_spead_stan_dev[i][1])
				#print("link_cap",link_cap)
			
				#vitesse moyenne, si leur ffs=veh/hour 
				#print("A VOIR DANS PARSE_NETWORK _XML,fct_creat_di_id_lk_value_li_id_orig_dest_nd_length_lk_capacity_lk_param_travel_duration,\
				#valeur vitesse moyenne=est mesuree en metres/sec ")
				vit_moy=round(length_lk / eval(di_key_id_lk_value_li_sat_flow_jam_density_mean_spead_stan_dev[i][2]),val_round_prec_vit_moy)
				#print("vit_moy",vit_moy)
			
				di_rep[i]=[eval(di_lk_inform[i][val_name_attribute_id_origin_node]),eval(di_lk_inform[i][val_name_attribute_id_dest_node]),\
				length_lk,link_cap,vit_moy]
			
			#if it is an entry link
			else:
				di_rep[i]=[eval(di_lk_inform[i][val_name_attribute_id_origin_node]),eval(di_lk_inform[i][val_name_attribute_id_dest_node]),\
				-1,-1,-1]
		#if the link is an exit one
		else:
			#print("hi")
			di_rep[i]=[eval(di_lk_inform[i][val_name_attribute_id_origin_node]),eval(di_lk_inform[i][val_name_attribute_id_dest_node]),\
			-1,-1,-1]
		
		
	#print(di_rep)
	return di_rep	

#**********************************************************************************************************************************************************
#fct creating dict, key= id phase, value=[...,[rout_prop_i,duree rout prop]...]
def fct_creat_di_id_phase_value_li_rout_prob(tree,\
val_name_elem_splitratioset="SplitRatioSet",val_name_splitRatioProfile="splitRatioProfile",val_name_duration_rout_prop_dt="dt",\
val_name_elem_splitratio="splitratio",val_name_attrib_inputlink="link_in",val_name_attrib_outputlink="link_out"):

	root=tree.getroot()
	for i in root.findall(val_name_elem_splitratioset):
		di={}
		
		for j in i:
			#print("j=",j,j.attrib)
			val_duration_rout_prop=j.attrib[val_name_duration_rout_prop_dt]
			eval_val_duration_rout_prop=eval(val_duration_rout_prop)
			#print("val_duration_rout_prop",val_duration_rout_prop)
			for m in j.findall(val_name_elem_splitratio):
				#print("m=",m)
				#print(m.attrib)
				#print("m.text",eval(m.text))
				
				#print("m.attrib[val_name_attrib_inputlink]:",m.attrib[val_name_attrib_inputlink])
				#print("m.attrib[val_name_attrib_outputlink]:",m.attrib[val_name_attrib_outputlink])
				id_input_lk=eval(m.attrib[val_name_attrib_inputlink]) 
				
				#eval_value_rp=eval(m.text)
				
				#if the duration of the value of the rout prob is int or float, 
				if isinstance(eval_val_duration_rout_prop,int) or isinstance(eval_val_duration_rout_prop,float):
				
				
					di[eval(m.attrib[val_name_attrib_inputlink]),eval(m.attrib[val_name_attrib_outputlink])]=\
					[[eval(m.text)],[eval_val_duration_rout_prop]]
					
						
				#si on a plus qu'une duree
				else:
					#print("eval_val_duration_rout_prop",eval_val_duration_rout_prop)
					#li=[]
					#a=list(eval(m.text))
					#print("a=",a)
					#for p in a:
						#li.append(p)
					#print("li=",li)
					if isinstance(eval(m.text),int) or isinstance(eval(m.text),float):
						#print("here",[eval(m.text)])
						di[eval(m.attrib[val_name_attrib_inputlink]),eval(m.attrib[val_name_attrib_outputlink])]=\
						[[eval(m.text)],list(eval_val_duration_rout_prop)]
					else:
						di[eval(m.attrib[val_name_attrib_inputlink]),eval(m.attrib[val_name_attrib_outputlink])]=\
						[list(eval(m.text)),list(eval_val_duration_rout_prop)]
					
				
				
				#a=eval(val_duration_rout_prop)
				#print("lena",len(a))
				#print(a==tuple)
				
				
				
				
				#di[eval(m.attrib[val_name_attrib_inputlink]),eval(m.attrib[val_name_attrib_outputlink])]=\
				#[eval(m.text),eval(val_duration_rout_prop)]
				#print("di=",di)
				#a=di[1,3][0][2]+di[1,3][0][1]
				#print("a=",a)
				#print("a=",a,di[1,3][2],di[1,3][1])
				#print(di[1,3][2])
		#di=dict, key=phase id, value=[ [...,valeurs de splitratio,...],[...,duree,...]]
		#print("di avant",di)
		#if for a phase  we have multiple times the same value if of split ratio, we  keep one value and add the corresponding durations
		#if there exist multiple values too
		for i in di:
			li=[di[i][0][0]]*len(di[i][0])
			if li==di[i][0]:
				li_rep=[di[i][0][0]]
				li_dur=[sum(di[i][1])]
				di[i]=[li_rep,li_dur]
		#print()		
		#print("di apres", di)
		#import sys
		#sys.exit()
		return di
#**********************************************************************************************************************************************************
#method returning [ dict for the non signal intersection stages, dict for the signalalised intersection stages]
#each dict, key=id noeud, value=dict, cle=id stage (the stage id indicates its  line in the simulator corresponding file)
#value=[ id phases..] for ex { 1:{1:[7,8],2:[1,2,3,4]}, ...} intersection 1 has a stage 1 actuating phase [7,8] and
#another  stage 2 actuating  phases [1,2] and [3,4]
def fct_creat_intersection_stages(tree,val_di_id_nd_info,val_name_elem_ControllerSet="ControllerSet",val_name_attrib_node_id="id",\
val_name_attrib_row_id="id",val_name_attribute_type_nd="type",val_name_attribute_signal_nd="signalized",\
val_name_attribute_non_signal_nd="unsignalized"):

	root=tree.getroot()
	di_cle_id_nd={}
	
	for i in root.findall(val_name_elem_ControllerSet):
		#print("ControllerSet i=",i)
		for j in i:
			#print("Controller j=",j)
			#print()
			#print("j=",j.attrib)
			id_nd=eval(j.attrib[val_name_attrib_node_id])
			di_cle_id_nd[id_nd]={}
			#print("di_cle_id_nd",di_cle_id_nd)
			for m in j:
				#print("m",m)
				for n in m:
					#print("n",n)
					#print("n.attrib",n.attrib)
					id_stage_id=eval(n.attrib[val_name_attrib_row_id])
					di={}
					di[id_stage_id]=[]
					#print("di",di)
					for p in n:
						#print("p=",p)
						#print("p=",p.text)
						di[id_stage_id]=list(eval(p.text))
						#print("di[id_stage_id]",di[id_stage_id])
						di_cle_id_nd[id_nd].update(di)
						#print("di_cle_id_nd",di_cle_id_nd)
	#print()					
	#print("di_cle_id_nd",di_cle_id_nd.keys())
	#print()
	#print("di_cle_id_nd",di_cle_id_nd[3])
	di_id_nsi={}
	di_id_si={}
	#print(val_di_id_nd_info)
	for i in di_cle_id_nd:
		if val_di_id_nd_info[i][val_name_attribute_type_nd]==val_name_attribute_signal_nd:
				di_id_si[i]={}
				di_id_si[i].update(di_cle_id_nd[i])
		elif val_di_id_nd_info[i][val_name_attribute_type_nd]==val_name_attribute_non_signal_nd:
			di_id_nsi[i]={}
			di_id_nsi[i].update(di_cle_id_nd[i])
	#print()
	#print("di_id_nsi",di_id_nsi)
	#print()
	#print("di_id_si",di_id_si)
	#import sys
	#sys.exit()
	li_di_nsi_and_si_stages=[di_id_nsi,di_id_si]
	return li_di_nsi_and_si_stages
	#return di_cle_id_nd
	
#**********************************************************************************************************************************************************
#method creating dict with each intersection stages
#it returns a  list [ dict of non signal intersections, dict  signal intersections]
def fct_creat_intersection_stages_previous(tree,di_key_id_nd_value_di_nd_attrib,di_phase_inform=None,\
val_name_elem_signalList="SignalList",val_name_elem_signal="signal",\
val_name_attribute_node_id="node_id",val_name_attribute_nema="nema",val_name_attribute_lk_id="id",\
val_name_attribute_lane_dest_lk="link_to",\
di_key_id_nema_nb_value_compatible_nema_nb={1:[5,6],2:[5,6],3:[7,8],4:[7,8],5:[1,2],6:[1,2],7:[3,4],8:[3,4]},\
val_name_attribut_type_node="type",val_name_attribut_type_nsi="unsignalized",\
val_name_attribut_type_si="signalized"):

	root=tree.getroot()
	di_nd_id={}
	for i in root.findall(val_name_elem_signalList):
		#for each signal
		for j in i:
			#print("j=",j)
			#print("node id",j.attrib[val_name_attribute_node_id])
			di_nd_id[eval(j.attrib[val_name_attribute_node_id])]={}
			
			di_stages_key_nema_nb={}
			#for each element ohase (mes stages) we obtain its nema number
			for k in j:
				#print("k=",k)
				#print("nema nb of the stage",k.attrib[val_name_attribute_nema])
				di_stages_key_nema_nb[eval(k.attrib[val_name_attribute_nema])]=[]
				
				#for ech stage we obtain the link references
				for m in k:
					#print("m",m)
					#we obtain the link reference, each link reference refers to one link
					for n in m:
						#print("n=",n)
						#print("lk id=",n.attrib[val_name_attribute_lk_id])
						input_lk_id=n.attrib[val_name_attribute_lk_id]
						li_comp_phases=[]
						#for each lane we obtain its dest link
						for p in n:
							#print("p=",p.attrib[val_name_attribute_lane_dest_lk])
							
							id_output_lk=p.attrib[val_name_attribute_lane_dest_lk]
							
							if [eval(input_lk_id),eval(id_output_lk)] not in li_comp_phases:
								li_comp_phases.append([eval(input_lk_id),eval(id_output_lk)])
								
						di_stages_key_nema_nb[eval(k.attrib[val_name_attribute_nema])]=li_comp_phases
						#print(di_stages_key_nema_nb)
						#print()
				
			di_nd_id[eval(j.attrib[val_name_attribute_node_id])].update(di_stages_key_nema_nb)
	
	#di_nd_id= dict, key=id node, valeut=dict, key=id nema, value=[...[input, out link],..] (compatible movements)
	#print(di_nd_id.keys())
	#print(di_nd_id[1])
	#print(di_nd_id[3])
	#print(di_nd_id[4])
	#print()
	
	#for each intersection we obtain the sim compatible stages
	#di_nd_id= dict, key = id intersection, value=dict, key=id nema movement, value=[..,sim compat phases, ...]
	di_key_id_nd_value_li_comp_actuated_nema_mv_given_nd={}
	for r in  di_nd_id:
		#print()
		#print("node=",r)
		di_key_id_nd_value_li_comp_actuated_nema_mv_given_nd[r]=[]
		li_nema_mv=list(di_nd_id[r])
		#print("li nema nb related to node",li_nema_mv)
		li_comp_actuated_nema_mv_given_nd=[]
		#for each nema id:
		for s in li_nema_mv:
			#print("s=",s)
			#print("comp nema to s",di_key_id_nema_nb_value_compatible_nema_nb[s])
			#print(di_key_id_nema_nb_value_compatible_nema_nb.keys())
			
			for s1 in di_key_id_nema_nb_value_compatible_nema_nb[s]:
				if s1 in li_nema_mv:
					li_comp_actuated_nema_mv_given_nd.append([s,s1])
					#print("li_comp_actuated_nema_mv_given_nd",li_comp_actuated_nema_mv_given_nd)	
					li_nema_mv.remove(s)
					li_nema_mv.remove(s1)
					#print("li_nema_mv",li_nema_mv)
				#else:
					#li_comp_actuated_nema_mv_given_nd.append([s1])
					#li_nema_mv.remove(s1)
					#print("li_comp_actuated_nema_mv_given_nd",li_comp_actuated_nema_mv_given_nd)
				if len(li_nema_mv)==1:
					li_comp_actuated_nema_mv_given_nd.append([li_nema_mv[0]])
				
			di_key_id_nd_value_li_comp_actuated_nema_mv_given_nd[r].extend(li_comp_actuated_nema_mv_given_nd)
				
	#print("di_key_id_nd_value_li_comp_actuated_nema_mv_given_nd",di_key_id_nd_value_li_comp_actuated_nema_mv_given_nd)
	#import sys
	#sys.exit()
	di_key_id_node_value_li_compatible_phases={}
	
	#di_key_id_nd_value_li_comp_actuated_nema_mv_given_nd= dict, key= id intersection, 
	#value=[..[...,id nema compat phases,..],...]
	#for each intersection
	for i in di_key_id_nd_value_li_comp_actuated_nema_mv_given_nd:
		#print()
		#print("node",i)
		di_key_id_node_value_li_compatible_phases[i]=[]
		for j in di_key_id_nd_value_li_comp_actuated_nema_mv_given_nd[i]:
			#print("j=",j)
			li_1=[]
			for m in j:
				#print("m=",m)
				elem=di_nd_id[i][m]
				#print("elem",elem)
				li_1.extend(elem)
			#print("li_1",li_1)
			di_key_id_node_value_li_compatible_phases[i].append(li_1)
	
	#print(di_key_id_node_value_li_compatible_phases)
	#print()
	di_key_id_node_value_li_compatible_phases_rep={}
	for  i in di_key_id_node_value_li_compatible_phases:
		#print()
		#print("i=",i)
		di_key_id_node_value_li_compatible_phases_rep[i]=[]
		for j in di_key_id_node_value_li_compatible_phases[i]:
			#print("j=",j)
			li=[]
			for m in j:
				#print("m=",m)
				#si la phase n'est pas un RT on l'ajoute,di_phase_inform=dict,key=id phase, value=[max que size, sat flow, que type]
				if di_phase_inform[m[0],m[1]][2]!=1:
					li.extend(m)
				#print("li",li)
			di_key_id_node_value_li_compatible_phases_rep[i].append(li)
	
	#print(di_key_id_node_value_li_compatible_phases_rep)
	
	di_key_id_nsi_value_li_compatible_phases={}
	
	di_key_id_si_value_li_compatible_phases={}
	
	for i in di_key_id_node_value_li_compatible_phases_rep:
		#if the node type is ns i
		#print("HERE",di_key_id_nd_value_di_nd_attrib)
		if di_key_id_nd_value_di_nd_attrib[i][val_name_attribut_type_node]==val_name_attribut_type_nsi:
			di_key_id_nsi_value_li_compatible_phases[i]=di_key_id_node_value_li_compatible_phases_rep[i]
		elif di_key_id_nd_value_di_nd_attrib[i][val_name_attribut_type_node]==val_name_attribut_type_si:
			di_key_id_si_value_li_compatible_phases[i]=di_key_id_node_value_li_compatible_phases_rep[i]
		else:
			print("PROBLEM IN PARSE_NETW_XML_FILES, FCT fct_creat_intersection_stages(tree,val_name_elem_signalList,\
			node type=",di_key_id_nd_value_di_nd_attrib[i][val_name_attribut_type_node])
			import sys
			sys.exit()
	
	#print()		
	#print(di_key_id_nsi_value_li_compatible_phases)
	#print()
	#print(di_key_id_si_value_li_compatible_phases)
	#import sys
	#sys.exit()
	return [di_key_id_nsi_value_li_compatible_phases, di_key_id_si_value_li_compatible_phases]
	#maintenant je dois savoir quels nema nb sont compatibles entre eux.
	#Par example le nema 5 est compatible aven nema 2.
#**********************************************************************************************************************************************************
#method creating dict with the phase id its max que size saturation flow and the queue type (RT or not)
# A FAIRE TYPE QUEUE
def fct_creat_phase_inform(tree,val_di_id_lk_value_lk_cap,val_di_node_inform,val_name_elem_signalList="SignalList",\
val_name_attribut_lk_id="id",val_name_attribut_dest_lk="link_to",val_name_attribut_knob="knob",val_round_prec=2,val_t_unit=0.1,\
val_name_attribut_li_input_lk="li_input_link_id",val_name_attribut_li_output_lk="li_output_link_id",val_name_attribut_type_phase="movement",\
val_name_indicator_right_turn="r"):

	root=tree.getroot()
	di_phase_li_knob_values_que_type={}
	
	for i in root.findall(val_name_elem_signalList):
		
		#on obtient les signals
		for j in i:
			#print()
			#print("j=",j)
			#les phases
			for m in j:
				#print("m=",m)
				#les link references
				for n in m:
					#print("n",n)
					#les link reference
					for p in n:
						#print("p=",p)
						#print("p=",p.attrib)
						id_origin_lk=eval(p.attrib[val_name_attribut_lk_id])
						#di[id_origin_lk]={}
						#print("di",di)
						#di_phase_li_knob_values={}
						for r in p:
							#print("r=",r)
							#print("r=",r.attrib)
							id_dest_lk=eval(r.attrib[val_name_attribut_dest_lk])
							if (id_origin_lk,	id_dest_lk) not in di_phase_li_knob_values_que_type:
								#if the attribut movement exist and values "r", then the que is RT
								if val_name_attribut_type_phase in r.attrib:
									if r.attrib[val_name_attribut_type_phase]==val_name_indicator_right_turn:
										que_type=1
									else:
										que_type=0
								else:
									que_type=0
								di_phase_li_knob_values_que_type[id_origin_lk,id_dest_lk]=[[eval(r.attrib[val_name_attribut_knob]),que_type]]
							
							else:	
								di_phase_li_knob_values_que_type[id_origin_lk,id_dest_lk].append([eval(r.attrib[val_name_attribut_knob]),que_type])
								
								
	#print(di_phase_li_knob_values_que_type)
	#print()
	#di_phase_li_knob_values_que_type= dict, key=phase id, value=[..., [knob value, que type],...]
	
	di_id_phase_value_li_max_que_size_sat_flow_que_type={}
	
	#for each phase
	for i in di_phase_li_knob_values_que_type:
		#calculation of the phase sat flow, somme sur i de( capacity de input link de la phase x valeur i de knob )
		#val_di_id_lk_value_lk_cap= dict, key = id lk, value=['lk capacity" cad sat flow pour moi, etc]
		#print("val_di_id_lk_value_lk_cap[i[0]]",val_di_id_lk_value_lk_cap[i[0]])
		sat_flow_phase=0
		#for each knob value
		for j in di_phase_li_knob_values_que_type[i]:
			#sat flow= som de knob x sat flow input link to phase
			sat_flow_phase+=j[0]* eval(val_di_id_lk_value_lk_cap[i[0]][0])
			
		#sat flow_phase=veh/sec, sat_flow=veh/t_unit
		sat_flow=round(sat_flow_phase*val_t_unit,val_round_prec)
		di_id_phase_value_li_max_que_size_sat_flow_que_type[i[0],i[1]]=[-1,sat_flow,j[1]]
		
	#print(di_id_phase_value_li_max_que_size_sat_flow_que_type)
	#print()
	
	#on cherche si il y a des phases non permises dont le taux de sat sera zero
	#val_di_node_inform=dict, key=id node, valeur=dict={...,"li_input_link"=[],"li_output_link"=[], etc.}
	#pour chaque nd dont la liste "li_input_link" n'est pas vide, on examine les (input lk, output link)
	for i in val_di_node_inform:
		if val_di_node_inform[i][val_name_attribut_li_input_lk]!=[] and\
		val_di_node_inform[i][val_name_attribut_li_output_lk]!=[]:
			for j in val_di_node_inform[i][val_name_attribut_li_input_lk]:
				for m in val_di_node_inform[i][val_name_attribut_li_output_lk]:
					if (eval(j),eval(m)) not in di_id_phase_value_li_max_que_size_sat_flow_que_type:
						di_id_phase_value_li_max_que_size_sat_flow_que_type[eval(j),eval(m)]=[-1,0,0]
						
		
	
	#print(di_id_phase_value_li_max_que_size_sat_flow_que_type)
	return di_id_phase_value_li_max_que_size_sat_flow_que_type
	
#**********************************************************************************************************************************************************
#fct creating a dictionary key =id link, value nb lanes
def fct_creat_di_key_id_lk_val_nb_lanes(tree,val_name_elem_signalList="SignalList",val_name_attribut_lk_id="id",\
val_name_attribut_lane_id="id"):
	
	root=tree.getroot()
	
	di={}
	di_rep={}
	
	for i in root.findall(val_name_elem_signalList):
		for j in i:
			for m in j:
				for n in m:
					for p in n:
						#print()
						#print("p=",p)
						#print("p.attrib=",p.attrib)
						id_lk=eval(p.attrib[val_name_attribut_lk_id])
						#print("id_lk",id_lk)
						di[id_lk]=[]
						for q in p:
							#print("q=",q)
							#print("q=",q.attrib[val_name_attrib_lk_id])
							lk_id=eval(q.attrib[val_name_attribut_lane_id])
							if lk_id not in di[id_lk]:
								di[id_lk].append(lk_id)
								
						
	#print(di)
	
	for i in di:
		di_rep[i]=len(di[i])
		
	#print(di_rep)
	
	return di_rep

#**********************************************************************************************************************************************************

#method reading an xml  file and returning
# [dict_nd_info, dict_lk_info,di_id_node_li_entry_lk,di_s_and_ns_entry_links,di_id_node_li_exit_lk,\
#di_id_lk_id_value_li_lk_cap_jam_dens_ffs_stan_dev_as_indicated_in_xml,di_key_id_phase_value_li_rout_prop,\
#li_di_nsi_and_si_stages,di_phase_info,di_id_lk_value_li_orig_dest_nd_length_cap_mean_travel_param], 
#dict_nd_info=dict, key = id node, value dict with node info
#dict_lk_info=dict, key = id link, value dict with link info
#di_id_node_li_entry_lk= dict, key=id nodes having entry links, value =list id entry links
#di_s_and_ns_entry_links, dict, key=1 or 0 according to when the head node of the link is/not sigalised/nonsignalised,
#value=list link ids 
#=di_id_node_li_exit_lk, dict, key=id nodes having exit links, value =list id exit links
#di_id_lk_id_value_li_lk_cap_jam_dens_ffs_stan_dev_as_indicated_in_xml ,dict, key=link id, 
#value=[link capacity as defined in the xml file, jam density, free flow speed, stand deviat of free flow speed]
#we adapt the boundary nodes existing in the xml file and indicated as "terminal", to the ".Q" convention indicated by -1 
#di_key_id_phase_value_li_rout_prop=dict with the rout prop (split ratios) of each phase
#key= id phase, value=[...,[rout_prop_i,duree rout prop]...]
def fct_creat_li_di_node_and_link_info_corrected(\
val_name_file_to_read="scenario_example.xml",\
va_name_elem_networklist="NetworkList",va_name_elem_nodelist="NodeList",\
va_name_elem_id_attrib="id",va_name_elem_inputs="inputs",va_name_elem_input="input",\
va_name_elem_link_id="link_id",va_name_elem_outputs="outputs",va_name_elem_output="output",\
va_name_elem_linklist="LinkList",\
va_name_elem_node_id="node_id",\
va_name_origin_node_attribut="begin",va_name_destination_node_attribut="end",\
va_name_attribut_origin_node_lk="origin_nd_id",va_name_attribut_dest_node_lk="dest_nd_id",\
va_name_attribut_type_node="type",va_type_boundary_node="terminal",va_name_output_links="li_output_link_id",\
va_name_signalised_nd="signalized",va_name_nonsignalised_nd="unsignalized",va_indicator_sign_lk=1,\
va_indicator_nonsign_lk=0,va_name_input_links="li_input_link_id",va_name_origin_node="origin_nd_id",\
va_name_elem_fundamentaldiagramset="FundamentalDiagramSet",va_name_fundamentaldiagram="fundamentalDiagram",\
va_name_attribut_capacity="capacity",va_name_attribut_jam_density="jam_density",\
va_name_attribut_free_flow_speed="free_flow_speed",va_name_attribut_std_dev_free_flow_speed="std_dev_free_flow_speed",\
va_name_elem_splitratioset="SplitRatioSet",va_name_splitRatioProfile="splitRatioProfile",va_name_duration_rout_prop_dt="dt",\
va_name_elem_splitratio="splitratio",va_name_attrib_inputlink="link_in",va_name_attrib_outputlink="link_out",\
va_name_elem_signalList="SignalList",va_name_elem_signal="signal",\
va_name_attribute_node_id="node_id",va_name_attribute_nema="nema",va_name_attribute_lk_id="id",\
va_name_attribute_lane_dest_lk="link_to",\
va_name_attribut_type_nsi="unsignalized",va_name_attribut_type_si="signalized",\
va_name_attribut_knob="knob",va_round_prec=2,va_t_unit=0.1,\
va_name_attribut_type_phase="movement",\
va_name_indicator_right_turn="r",\
va_name_attribute_length="length",va_round_prec_lk_length=0,\
va_round_prec_vit_moy=1,\
va_name_elem_ControllerSet="ControllerSet",va_name_attrib_node_id="id",va_name_attrib_row_id="id"):

	#lecture du fichier et on le stock dans un objet de type Element
	v_tree = ET.parse(val_name_file_to_read)
	
	#creation dict of nodes
	#dict, key=nod id, value=dict having keys "li_output_links_id", "li_input_lk_id","type " (indicating if an intersection
	#is/not signalised),"id" indicating the node id
	#we do not modify anything here
	di_nd_info=fct_creating_di_node_inform(tree=v_tree,\
	val_name_elem_networklist=va_name_elem_networklist,val_name_elem_nodelist=va_name_elem_nodelist,\
	val_name_elem_id_attrib=va_name_elem_id_attrib,val_name_elem_inputs=va_name_elem_inputs,\
	val_name_elem_input=va_name_elem_input,\
	val_name_elem_link_id=va_name_elem_link_id,val_name_elem_outputs=va_name_elem_outputs,\
	val_name_elem_output=va_name_elem_output)
	
	#print("di_nd_info HERE",di_nd_info)
	
	#creation dict of links
	#dict, key=link id, value=dict with keys :'dest_nd_id','length','lanes','origin_nd_id','type','id','in_sync',
	#'lane_offset'
	di_lk_info=fct_creating_di_link_infor(tree=v_tree,\
	val_name_elem_networklist=va_name_elem_networklist,val_name_elem_linklist=va_name_elem_linklist,\
	val_name_elem_id_attrib=va_name_elem_id_attrib,val_name_elem_node_id=va_name_elem_node_id,\
	val_name_origin_node_attribut=va_name_origin_node_attribut,\
	val_name_destination_node_attribut=va_name_destination_node_attribut,\
	val_name_attribut_origin_node_lk=va_name_attribut_origin_node_lk,\
	val_name_attribut_dest_node_lk=va_name_attribut_dest_node_lk)
	
	for i in di_lk_info:
		#print("i=",i)
	
		#print("di_lk_info[i]",di_lk_info[i])
		#print("HERE1",di_lk_info[i][va_name_attribut_origin_node_lk])
		#print("HERE2",di_nd_info[eval(di_lk_info[i][va_name_attribut_origin_node_lk])])
		if di_nd_info[ eval(di_lk_info[i][va_name_attribut_origin_node_lk])][va_name_attribut_type_node]==\
		va_type_boundary_node:
			di_lk_info[i][va_name_attribut_origin_node_lk]="-1"
		elif di_nd_info[ eval(di_lk_info[i][va_name_attribut_dest_node_lk])][va_name_attribut_type_node]==\
		va_type_boundary_node:
			di_lk_info[i][va_name_attribut_dest_node_lk]="-1"
	
	#dict, key=id node, value=list non empty of the entry_link ids heading to the node
	di_id_node_li_entry_lk=fct_creat_di_id_node_li_entry_links(di_nd_infor=di_nd_info,di_lk_infor=di_lk_info,\
	val_name_attribut_type_node=va_name_attribut_type_node,val_name_terminal_node=va_type_boundary_node,\
	val_name_output_links=va_name_output_links,val_name_dest_node=va_name_attribut_dest_node_lk)
	
	#print("HERE",di_id_node_li_entry_lk.keys())
	
	#dict,key=1 or 0 indicating signalised or non-sign entry links, value=list id entry link
	#di_s_and_ns_entry_links=fct_creat_di_s_and_ns_entry_links(\
	#val_di_id_nd_value_li_id_entry_links=di_id_node_li_entry_lk,\
	#val_di_node_info=di_nd_info,val_name_node_type=va_name_attribut_type_node,\
	#val_name_signalised_nd=va_name_signalised_nd,val_name_nonsignalised_nd=va_name_nonsignalised_nd,\
	#val_indicator_sign_lk=va_indicator_sign_lk,val_indicator_nonsign_lk=va_indicator_nonsign_lk)
	
	#dict, key=id node, value=list non empty of the exit_link ids heading to the node
	di_id_node_li_exit_lk=fct_creat_di_id_node_li_exit_links(di_nd_infor=di_nd_info,di_lk_infor=di_lk_info,\
	val_name_attribut_type_node=va_name_attribut_type_node,val_name_terminal_node=va_type_boundary_node,\
	val_name_input_links=va_name_input_links,val_name_origin_node=va_name_attribut_origin_node_lk)
	
	#dict, key=link id
	##value=[link capacity as defined in the xml file, jam density, free flow speed, stand deviat of free flow speed]
	di_id_lk_id_value_li_lk_cap_jam_dens_ffs_stan_dev_as_indicated_in_xml=\
	fct_creat_di_id_lk_id_value_li_lk_cap_jam_dens_ffs_stan_dev_as_indicated_in_xml(tree=v_tree,\
	val_name_elem_fundamentaldiagramset=va_name_elem_fundamentaldiagramset,\
	val_name_fundamentaldiagram=va_name_fundamentaldiagram,\
	val_name_attribut_link_id=va_name_elem_link_id,val_name_attribut_capacity=va_name_attribut_capacity,\
	val_name_attribut_jam_density=va_name_attribut_jam_density,\
	val_name_attribut_free_flow_speed=va_name_attribut_free_flow_speed,\
	val_name_attribut_std_dev_free_flow_speed=va_name_attribut_std_dev_free_flow_speed)
	
	
	#we create a dict with the rout prop (split ratios) of each phase
	#dict, key= id phase, value=[...,[rout_prop_i,duree rout prop]...]
	di_key_id_phase_value_li_rout_prop=fct_creat_di_id_phase_value_li_rout_prob(tree=v_tree,\
	val_name_elem_splitratioset=va_name_elem_splitratioset,val_name_splitRatioProfile=va_name_splitRatioProfile,\
	val_name_duration_rout_prop_dt=va_name_duration_rout_prop_dt,\
	val_name_elem_splitratio=va_name_elem_splitratio,val_name_attrib_inputlink=va_name_attrib_inputlink,\
	val_name_attrib_outputlink=va_name_attrib_outputlink)

	#li_rep=[di_nd_info,di_lk_info,di_id_node_li_entry_lk,di_s_and_ns_entry_links,di_id_node_li_exit_lk,\
	#di_id_lk_id_value_li_lk_cap_jam_dens_ffs_stan_dev_as_indicated_in_xml,di_key_id_phase_value_li_rout_prop]
	
	#li_rep=[di_nd_info]
	
	#fct_creat_di_id_phase_value_li_rout_prob(tree=v_tree)
	
	#print(len(li_rep))
	#import sys
	#sys.exit()
	
	#method creating dict with the phase id its max que size saturation flow and the queue type (RT or not)
	di_phase_info=fct_creat_phase_inform(tree=v_tree,\
	val_di_id_lk_value_lk_cap=di_id_lk_id_value_li_lk_cap_jam_dens_ffs_stan_dev_as_indicated_in_xml,\
	val_di_node_inform=di_nd_info,\
	val_name_elem_signalList=va_name_elem_signalList,val_name_attribut_lk_id=va_name_attribute_lk_id,\
	val_name_attribut_dest_lk=va_name_attribute_lane_dest_lk,\
	val_name_attribut_knob=va_name_attribut_knob,val_round_prec=va_round_prec,val_t_unit=va_t_unit,\
	val_name_attribut_li_input_lk=va_name_input_links,\
	val_name_attribut_li_output_lk=va_name_output_links,\
	val_name_attribut_type_phase=va_name_attribut_type_phase,val_name_indicator_right_turn=va_name_indicator_right_turn)
	
	#li_di_nsi_and_nsi_stages [ dict of non signal intersections, dict  signal intersections]
	#li_di_nsi_and_nsi_stages=fct_creat_intersection_stages(\
	#tree=v_tree,di_key_id_nd_value_di_nd_attrib=di_nd_info,\
	#di_phase_inform=di_phase_info,\
	#val_name_elem_signalList=va_name_elem_signalList,\
	#val_name_elem_signal=va_name_elem_signal,\
	#val_name_attribute_node_id=va_name_attribute_node_id,\
	#val_name_attribute_nema=va_name_attribute_nema,\
	#val_name_attribute_lk_id=va_name_attribute_lk_id,\
	#val_name_attribute_lane_dest_lk=va_name_attribute_lane_dest_lk,\
	#di_key_id_nema_nb_value_compatible_nema_nb=va_di_key_id_nema_nb_value_compatible_nema_nb,\
	#val_name_attribut_type_node=va_name_attribut_type_node,\
	#val_name_attribut_type_nsi=va_name_attribut_type_nsi,\
	##val_name_attribut_type_si=va_name_attribut_type_si)
	

	dict_key_id_lk_value_nb_lanes=fct_creat_di_key_id_lk_val_nb_lanes(tree=v_tree,val_name_elem_signalList="SignalList",\
	val_name_attribut_lk_id="id",val_name_attribut_lane_id="id")
	
	
	di_id_lk_value_li_orig_dest_nd_length_cap_mean_travel_param=\
	fct_creat_di_id_lk_value_li_id_orig_dest_nd_length_lk_capacity_lk_param_travel_duration(\
	di_key_id_lk_value_li_sat_flow_jam_density_mean_spead_stan_dev=\
	di_id_lk_id_value_li_lk_cap_jam_dens_ffs_stan_dev_as_indicated_in_xml,\
	di_key_id_lk_value_nb_lanes=dict_key_id_lk_value_nb_lanes,\
	di_lk_inform=di_lk_info,\
	val_name_attribute_id_dest_node=va_name_attribut_dest_node_lk,\
	val_name_attribute_id_origin_node=va_name_attribut_origin_node_lk,\
	val_name_attribute_length=va_name_attribute_length,\
	val_round_prec_lk_length=va_round_prec_lk_length,\
	val_round_prec_vit_moy=va_round_prec_vit_moy)
	
	
	li_di_intersection_stages=fct_creat_intersection_stages(tree=v_tree,\
	val_di_id_nd_info=di_nd_info,
	val_name_elem_ControllerSet=va_name_elem_ControllerSet,\
	val_name_attrib_node_id=va_name_attrib_node_id,val_name_attrib_row_id=va_name_attrib_row_id,\
	val_name_attribute_type_nd=va_name_attribut_type_node,\
	val_name_attribute_signal_nd=va_name_signalised_nd,\
	val_name_attribute_non_signal_nd=va_name_nonsignalised_nd)
	
	#li_rep=[di_nd_info,di_lk_info,di_id_node_li_entry_lk,di_id_node_li_exit_lk,\
	#di_id_lk_id_value_li_lk_cap_jam_dens_ffs_stan_dev_as_indicated_in_xml,di_key_id_phase_value_li_rout_prop,\
	#li_di_nsi_and_nsi_stages,di_phase_info,di_id_lk_value_li_orig_dest_nd_length_cap_mean_travel_param]
	
	li_rep=[di_nd_info,di_lk_info,di_id_node_li_entry_lk,di_id_node_li_exit_lk,\
	di_id_lk_id_value_li_lk_cap_jam_dens_ffs_stan_dev_as_indicated_in_xml,di_key_id_phase_value_li_rout_prop,\
	li_di_intersection_stages,di_phase_info,di_id_lk_value_li_orig_dest_nd_length_cap_mean_travel_param]
	
	return li_rep
	
	

#**********************************************************************************************************************************************************		
	
#di_nd=fct_creating_di_node_inform()
#print()
#print("di_nd_inform:",di_nd)
#print()
#val_tree = ET.parse('scenario_example.xml')
#di_lk=fct_creating_di_link_infor(tree=val_tree)
#print("di_lk",di_lk)
#**********************************************************************************************************************************************************	
#**********************************************************************************************************************************************************	

#va_name_file_to_read="/Users/jennie/Desktop/travail_vsim_int/PARSER_FI_XML/test_parser_3/scenario_example_5.xml"
#va_name_file_to_read="/Users/jennie/Desktop/scenario_test.xml"
#************************
#val_tree = ET.parse(va_name_file_to_read)

#di_nd=fct_creating_di_node_inform(val_tree)
#fct_creat_intersection_stages(tree=val_tree,di_key_id_nd_value_di_nd_attrib=di_nd)
#li=fct_creat_li_di_node_and_link_info(val_name_file_to_read=va_name_file_to_read)
#************************
#li=fct_creat_li_di_node_and_link_info_corrected(val_name_file_to_read=va_name_file_to_read)
#************************
#print("di nd info",li[0])
#print()
#print("di lk info",li[1])
#print("di lk info",li[1]["-2113402"])
#print("di nd info",li[2])
#print()
#print("di nd info",li[3])
#print(len(li[0]),len(li[1]))
#print("di nd info",li[5])

#print("di nd info",li[6])



