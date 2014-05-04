import Global_Functions_Network
import File_Sim_Name_Module_Files
import copy

#***************************************************fcts calculating all network FT controls with offsets**********************************************************************

#methode calcul decalage negatif. On cherche quel est le control pour t in [ v_decalage,t_start_control)
#li_id_duree=[...,[id stage a actualiser, duree,cycle duree],...]
#cette methode retourne [l'indice du control dans la liste (si ind=2 c'est le 3eme element), duree d'actualisation du control]
def  fct_decalage_negatif_1(li_id_duree,longeur_li_id_duree,v_decalage,t_start_control):
 
	print("li_id_duree",li_id_duree)
	print("longeur_li_id_duree",longeur_li_id_duree)
	print("v_decalage",v_decalage)
	som=v_decalage
	#on cherche l'interval auquel le t_start_control appartient, sachant que le premier control de la li_id_duree, s'appliquera a t_start control
	
	
	print("li_id_duree",li_id_duree)
	#on parcourt la liste des durees, li_id_duree=[...,[id stage a actualiser, duree],...]
	for i in range(longeur_li_id_duree):
		
		b=longeur_li_id_duree-i-1
		#maj de la somme des durees
		#print("som avant",som,"i[1]",li_id_duree[i][1])
		som+=li_id_duree[b][1]
		#print("som apres",som)
		#print()
		
		#si la somme =t_start control
		if som==t_start_control:
			#l'indice du control dans la liste
			#ind=b
			
			#duree d'actualisation
			dur=li_id_duree[ind][1]
			print("ind,dur",li_id_duree[b][1],dur)
			import sys
			sys.exit()
			return[li_id_duree[b][1],dur]
		
		#si la somme >t_start control
		elif som>t_start_control:
			#l'indice du control dans la liste
			#ind=b
			
			#a=v_decallage-som
			#print("a=",a)
			#duree d'actualisation
			dur=som-t_start_control
			print("ind,dur",li_id_duree[b][0],dur)
			import sys
			sys.exit()
			return[li_id_duree[b][1],dur]
		
#*****************************************************************************************************************************************************************************************
#methode calcul decalage negatif. On cherche quel est le control pour t in [ v_decalage,t_start_control)
#li_id_duree=[...,[id stage a actualiser, duree,cycle duree],...]
#cette methode retourne [l'indice du control dans la liste (si ind=2 c'est le 3eme element), duree d'actualisation du control]
def  fct_decalage_negatif(li_id_duree,longeur_li_id_duree,v_decalage):
 
	#print("li_id_duree",li_id_duree)
	#print("longeur_li_id_duree",longeur_li_id_duree)
	#print("v_decalage",v_decalage)
	
	#temps restant=Cycle - valeir decalage, on considee que le cycle est fixe
	#temps_restant=longeur_li_id_duree[0][1]-v_decalage
	
	som=0
	#on cherche l'interval auquel le t_start_control appartient, sachant que le premier control de la li_id_duree, s'appliquera a t_start control
	
	
	#print("li_id_duree",li_id_duree)
	#on parcourt la liste des durees, li_id_duree=[...,[id stage a actualiser, duree actualisation, duree cycle],...]
	for i in range(longeur_li_id_duree):
		
		#on somme chaque duree d'actualisation
		som+=li_id_duree[i][1]
		#print("som <0",som,som==v_decalage,v_decalage)
		#si la somme = v_decalage
		if som==abs(v_decalage):
			#print("i+1,li_id_duree[i+1][1]",i+1,li_id_duree[i+1][1])
			return [i+1,li_id_duree[i+1][1]]
		
		#si la somme > v_decalage
		elif som>v_decalage:
			dur=som-v_decalage
			#on retourne [indice element selectionne, duree stage]
			return[i,dur]
		
#*****************************************************************************************************************************************************************************************
#method calcul control cas decalage strict. posit. On cherche quel est le control pour t in [t_start_control, v_decalage)
#li_id_duree=[...,[indice element dans la liste de stages selectionne a actualiser, duree actual],...]
def fct_decalage_strict_positif_1(li_id_duree,longeur_li_id_duree,v_decalage):
 
	som=0
	#print("li_id_duree",li_id_duree)
	#print("longeur_li_id_duree",longeur_li_id_duree)
	#print("v_decalage",v_decalage)
	#on parcourt la liste des durees en commencant par le dernier element de la liste vers le premier, li_id_duree=[...,[id stage a actualiser, duree],...]
	for i in range(longeur_li_id_duree):
	
		#b=longeur_li_id_duree-i-1
		#print("b",b,"li_id_duree[b][1]",li_id_duree[b][1])
		#som+=li_id_duree[b][1]
		som+=li_id_duree[i][1]
		#print("som",som)
		
		#si la somme=v_decalage
		if som==v_decalage:
		
			#l'indice du control dans la liste
			ind=b
			
			#duree d'actualisation
			dur=li_id_duree[ind][1]
			#print("dur",dur,"ind,",ind)
			#import sys
			#sys.exit()
			return[ind,dur]
			
		#si la somme >decalage
		elif som>v_decalage:
		
			#l'indice du control dans la liste
			ind=i
			
			#duree d'actualisation
			##print("v_decalage",v_decalage,"som-li_id_duree[b][1]",som-li_id_duree[b][1])
			#dur=v_decalage-(som-li_id_duree[i][1])
			dur=som-v_decalage
			#print("dur",dur,"ind",ind)
			#import sys
			#sys.exit()
			return[ind,dur]
		
#*****************************************************************************************************************************************************************************************
#method calcul control cas decalage strict. posit. On cherche quel est le control pour t in [t_start_control, v_decalage)
#li_id_duree=[...,[id stage a actualiser, duree],...]
def fct_decalage_strict_positif(li_id_duree,longeur_li_id_duree,v_decalage):
 
	som=0
	
	som_prec=0
	
	
	#print("longeur_li_id_duree",longeur_li_id_duree)
	#print("li_id_duree",li_id_duree)
	#on parcourt la liste des durees en commencant par le dernier element de la liste vers le premier, 
	#li_id_duree=[...,[id stage a actualiser, duree actual, duree cycle],...]
	for i in range(longeur_li_id_duree):
		#print()
		#print("tour",i)
		#on commence a sommer par le fin
		b=longeur_li_id_duree-i-1
		som+=li_id_duree[b][1]
		#print("som",som)
		#print("v_decalage",v_decalage)
		
		#si la somme=v_decalage
		if som==v_decalage:
		
			#l'indice du control dans la liste
			
			
			#duree d'actualisation
			dur=li_id_duree[b][1]
			#print("dur",dur,"ind,",ind)
			#import sys
			#sys.exit()
			return[b,dur]
			
		#si la somme >decalage
		elif som>v_decalage:
		
			
			t_rest=v_decalage-som_prec
			
			#print("dur",dur,"ind",ind)
			#import sys
			#sys.exit()
			return[b,t_rest]
		else:
			som_prec=som
			#print("here",som_prec)
			
		
#*****************************************************************************************************************************************************************************************
#creation suite de controls lors de decallage
def fct_suite_ctrl_lors_decalage_1(li_id_dur,v_dec):
	
	
	li_id_dur_1=copy.deepcopy(li_id_dur)
	
	v_len=len(li_id_dur)
	#si la valeur du decallage est >0
	if v_dec>0:
		#[index ctrl a partir duquel on va repeter, duree d'actualisation]
		rep=fct_decalage_strict_positif(li_id_duree=li_id_dur,longeur_li_id_duree=v_len,v_decalage=v_dec)
		#print("rep",rep)
		
		
		li_1=li_id_dur_1[rep[0]:v_len]
		#print(li_1)
		#print()	
		#li=[]
		#for i in li_id_dur:
			#li_2=list(i)
			#li.append(li_2)
		
		#on modofie la duree du  premier stage a appliquer
		li_1[0][1]=rep[1]
		li_1=[li_1]
		#print(li_1)
		#print()	
		#on ajoute le stages du cycle
		#li_1.extend(li_id_dur)
		#print("li_id_dur",li_id_dur)
		#print()
		li_1.append(li_id_dur)
		#print(li_1)
		#print()
		#print("li_id_dur",li_id_dur)
		#import sys
		#sys.exit()
		
		return li_1
	#si la valeur du decallage est <0
	elif v_dec<0:
		print("A VERIFIER QUE DEC NEGATIF MARCHE BIEN IN GLOBAL FCT COTNROLS,fct_suite_ctrl_lors_decalage")
		import sys
		sys.exit()
		rep=fct_decalage_negatif(li_id_duree=li_id_dur,longeur_li_id_duree=v_len,v_decalage=v_dec)
		#print("rep cas <0",rep)
		#li=list(li_id_dur[rep[0]:v_len])
		li=li_id_dur_1[rep[0]:v_len]
		li[0][1]=rep[1]
		li=[li_1]
		
		return li
	#si la valeur du decallage est =0
	else:
		#print("herrr")
		#import sys
		#sys.exit()
		return None
		#return li_id_dur
	#return li
	
#*****************************************************************************************************************************************************************************************
#creation suite de controls lors de decallage
def fct_suite_ctrl_lors_decalage(li_id_dur,v_dec):
	
	
	li_id_dur_1=copy.deepcopy(li_id_dur)
	
	v_len=len(li_id_dur)
	#si la valeur du decallage est >0
	if v_dec>0:
		#[index ctrl a partir duquel on va repeter, duree d'actualisation]
		rep=fct_decalage_strict_positif(li_id_duree=li_id_dur,longeur_li_id_duree=v_len,v_decalage=v_dec)
		#print("rep",rep)
		
		
		li_1=li_id_dur_1[rep[0]:v_len]
		#print(li_1)
		#print()	
		#li=[]
		#for i in li_id_dur:
			#li_2=list(i)
			#li.append(li_2)
		
		#on modofie la duree du  premier stage a appliquer
		li_1[0][1]=rep[1]
		#li_1=[li_1]
		#print(li_1)
		
		#print()	
		#on ajoute le stages du cycle
		#li_1.extend(li_id_dur)
		#print("li_id_dur",li_id_dur)
		#print()
		#li_1.append(li_id_dur)
		li_1.extend(li_id_dur)
		#print(li_1)
		#import sys
		#sys.exit()
		#print()
		#print("li_id_dur",li_id_dur)
		#import sys
		#sys.exit()
		
		return li_1
	#si la valeur du decallage est <0
	elif v_dec<0:
		print("A VERIFIER QUE DEC NEGATIF MARCHE BIEN IN GLOBAL FCT COTNROLS,fct_suite_ctrl_lors_decalage")
		import sys
		sys.exit()
		rep=fct_decalage_negatif(li_id_duree=li_id_dur,longeur_li_id_duree=v_len,v_decalage=v_dec)
		#print("rep cas <0",rep)
		#li=list(li_id_dur[rep[0]:v_len])
		li=li_id_dur_1[rep[0]:v_len]
		li[0][1]=rep[1]
		#li=[li_1]
		li=li_1
		
		return li
	#si la valeur du decallage est =0
	else:
		#print("herrr")
		#import sys
		#sys.exit()
		return None
		#return li_id_dur
	#return li
	
#***************************************************************************************************************************************************************************************
#li_info=[ di_key_id_nd_value_val_dec, di_key_id_nd_value_li_ctrs ]
#di_key_id_nd_value_li_ctrs=dict, key=id node, value=[...[id stage ith period, actuation duartion, cycle duration],..]
#on retourne dict, cle=id node, value=[...,[id stage, duree actualisation, duree cycle],...]
def fct_suite_ctrl_lors_decalage_serie_nds_1(li_info):

	#di_rep={}
	#print("li_info",li_info)
	
	#pour chaque intersection on creera ses controles decales (si elle n'est pas l'inters master, si elle est on la laisse intact),
	#a=nb des noeuds avec decalages
	#a=len(li_info[0])
	#b=list(li_info[0].keys())
	#for i in range(a):
		#print("i=",i)
		#di={}
		
		#li_id_dur=[id stage a actual, duree]
		#li=fct_suite_ctrl_lors_decalage(li_id_dur=li_info[1][b[i]],v_dec=li_info[0][i])
		#di[b[i]]=li
		#di_rep.update(di)
		#return di_rep
		
		di_rep={}
		#pour chaque intersection on creera ses controles decales (si elle n'est pas l'inters master, si elle est on la laisse intacte),
		#di_key_id_nd_value_val_dec=dict, key=id node, valeur= valeur decalage 
		for i in li_info[0]:
			#print()
			#print("id nd",i)
			
			
			#si la valeur du decalage est superieure du cycle on prend comme valeur cycle - offset modulo cycle
			#print("li_info",li_info[1][i])
			if li_info[0][i]>li_info[1][i][0][2]:
				modulo=li_info[0][i]%li_info[1][i][0][2]
				if modulo>0:
					val_dec= li_info[1][i][0][2] - li_info[0][i]%li_info[1][i][0][2]
				else:
					val_dec=0
			#si la valeur de dec est egale a cette du cycle
			elif li_info[0][i]==li_info[1][i][0][2]:
				val_dec=0
			else:
				val_dec=li_info[0][i]
				
			#print("val dec",val_dec)	
			#si la valeur de decalagee st 0 on a la meeme liste
			if val_dec==0:	
				di_rep[i]=[li_info[1][i],li_info[1][i]]
			#si la valeur de dec est dif de zero
			else:
				#li_id_dur=[id stage a actual, duree]
				li=fct_suite_ctrl_lors_decalage(li_id_dur=li_info[1][i],v_dec=val_dec)
				if li !=None:
					di_rep[i]=li
				else:
					#print("i",i,"li_info[1][i]",li_info[1][i])
					di_rep[i]=li_info[1][i]
			#di_rep_1.update(di_rep)
		#print("IN GLOBA FCTS CTRL fct_suite_ctrl_lors_decalage_serie_nds",di_rep)
		#import sys
		#sys.exit()
		return di_rep
		
#*****************************************************************************************************************************************************************************************
#li_info=[ di_key_id_nd_value_val_dec, di_key_id_nd_value_li_ctrs ]
#di_key_id_nd_value_li_ctrs=dict, key=id node, value=[...[id stage ith period, actuation duartion, cycle duration],..]
#on retourne dict, cle=id node, value=[...,[id stage, duree actualisation, duree cycle],...]
def fct_suite_ctrl_lors_decalage_serie_nds(li_info):

	#di_rep={}
	#print("li_info",li_info)
	
	#pour chaque intersection on creera ses controles decales (si elle n'est pas l'inters master, si elle est on la laisse intact),
	#a=nb des noeuds avec decalages
	#a=len(li_info[0])
	#b=list(li_info[0].keys())
	#for i in range(a):
		#print("i=",i)
		#di={}
		
		#li_id_dur=[id stage a actual, duree]
		#li=fct_suite_ctrl_lors_decalage(li_id_dur=li_info[1][b[i]],v_dec=li_info[0][i])
		#di[b[i]]=li
		#di_rep.update(di)
		#return di_rep
		
		di_rep={}
		#pour chaque intersection on creera ses controles decales (si elle n'est pas l'inters master, si elle est on la laisse intacte),
		#di_key_id_nd_value_val_dec=dict, key=id node, valeur= valeur decalage 
		for i in li_info[0]:
			#print()
			#print("id nd",i)
			
			
			#si la valeur du decalage est superieure du cycle on prend comme valeur cycle - offset modulo cycle
			#print("li_info",li_info[1][i])
			if li_info[0][i]>li_info[1][i][0][2]:
				modulo=li_info[0][i]%li_info[1][i][0][2]
				if modulo>0:
					val_dec= li_info[1][i][0][2] - li_info[0][i]%li_info[1][i][0][2]
				else:
					val_dec=0
			#si la valeur de dec est egale a cette du cycle
			elif li_info[0][i]==li_info[1][i][0][2]:
				val_dec=0
			else:
				val_dec=li_info[0][i]
				
			#print("val dec",val_dec)	
			#si la valeur de decalagee st 0 on a la meeme liste
			if val_dec==0:	
				#di_rep[i]=[li_info[1][i]]
				di_rep[i]=li_info[1][i]
			#si la valeur de dec est dif de zero
			else:
				#li_id_dur=[id stage a actual, duree]
				li=fct_suite_ctrl_lors_decalage(li_id_dur=li_info[1][i],v_dec=val_dec)
				if li !=None:
					di_rep[i]=li
				else:
					#print("i",i,"li_info[1][i]",li_info[1][i])
					di_rep[i]=li_info[1][i]
			#di_rep_1.update(di_rep)
		
		return di_rep
		
#*****************************************************************************************************************************************************************************************
#methode qui lit le fichier des param de FT et retourne 	dict, cle=id node, value=[...,[id stage, duree actualisation, duree cycle],...]
#v_path_and_name_file_read="./Control_Param_Files"+"/"+File_Sim_Name_Module_Files.val_name_file_values_ft_control
#this will be used for the first cycle, then the FT control  as written in the parameter file will be followed.
def fct_ft_ctrls_network(v_path_and_name_file_read,v_nb_comment_lines_ft_offs1):
	
	#rep=[[valeurs decal pour chaque nd],dictionary: key = id node, 
	#value=[..., [id stage to actuate at step i, actuation duration, actuattion duration of the rec cloearance, cycle duration],...]
	
	
	#rep_fi=[[di_valeurs_decalage chaque nd, di_param_FT]
	rep_fi=Global_Functions_Network.fct_reading_file_parameters_FT_control_offset(name_file_to_read=v_path_and_name_file_read,\
	nb_comment_lines_ft_offs=v_nb_comment_lines_ft_offs1)
	
	
	#dict, cle=id node, value=[...,[index stage in sequence, duree actualisation, duree cycle],...]
	rep=fct_suite_ctrl_lors_decalage_serie_nds(li_info=rep_fi)
	#print("rep",rep)
	#import sys
	#sys.exit()
	#print()
	#print(rep_fi_1)
	
	#import sys
	#sys.exit()
	
	#on retourne [les parm de FT offeset, param FT sans offset]
	reponse= [rep,rep_fi[1]]
	#print()
	#print("ICI",reponse)
	#import sys
	#sys.exit()
	return reponse
	
#*****************************************************************************************************************************************************************************************	
	
#*****************************************************************************************************************************************************************************************	
#*****************************************************************************************************************************************************************************************
#test
#li_3=[[1,15],[0,3],[2,35],[0,7]]
#li=fct_decalage_negatif(li_id_duree=li_3,longeur_li_id_duree=4,v_decalage=-15,t_start_control=0.1)
#print(li)
#li_4=[[1,32],[0,7],[2,8],[0,3]]
#li=fct_decalage_strict_positif(li_id_duree=li_4,longeur_li_id_duree=4,v_decalage=12,t_start_control=0.1)
#print(li)

#di= fct_suite_ctrl_lors_decalage(li_id_dur=li_3,v_dec=0,t_start_ctrl=1)

#li=[[-15,0,10],{1: [[1,15,60],[0,3,60],[2,35,60],[0,7,60]],2:[[1,15,60],[0,3,60],[2,35,60],[0,7,60]],3:[[1,25,60],[0,5,60],[2,25,60],[0,5,60]]}]
#di=fct_suite_ctrl_lors_decalage_serie_nds(li_info=li,v_t_start_ctrl=0)
#print(di)
#di=fct_ft_ctrls_network(v_path_and_name_file_read="./Control_Param_Files"+"/"+File_Sim_Name_Module_Files.val_name_file_values_ft_control,\
#v_nb_comment_lines=3,v_nb_line_master_nd_inform=4,v_ti_start_ctrl=0.1)
#print(di)

#**********************************************end calcul network FT with offsets***********************************************************************************************


