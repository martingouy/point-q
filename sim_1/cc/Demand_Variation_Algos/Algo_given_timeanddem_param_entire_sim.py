

#method calculating the parameters of demand when it varies. 
#It returns [ demand parameter_actuel,type algo to employ next decision]
#val_li_t_and_dem_param=[....,[t, demand param],...]
def fct_calcul_t_and_param_demand_variation_entire_sim(val_li_t_and_dem_param):

	print("ici",val_li_t_and_dem_param)

	a=val_li_t_and_dem_param[0][1]
	
	if val_li_t_and_dem_param!=[]:
		del val_li_t_and_dem_param[0]
		
		return [a,1]
	else:
		return [a,1]

#*****************************************************************************************************************************************************************************************