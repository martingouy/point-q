import Cl_Creation_Sim_Sequence_And_Treats


obj_sim_sequence_and_treat=Cl_Creation_Sim_Sequence_And_Treats.Creation_Sim_Sequence_And_Treats()

v_nb_comment_lines_ft=2
v_nb_comment_lines_mp=1
v_nb_comment_lines_psd=1
v_nb_comment_lines_ft_off=1
v_nb_comment_lines_fa=1
v_nb_comment_lines_fa_max_green=1
v_va_di_param_ctrl_mp_practical_ctrl=1

#li=[]
#lis=obj_sim_sequence_and_treat.fct_sim_treat(*obj_sim_sequence_and_treat.creation_args_fct_sim_treat())
li=obj_sim_sequence_and_treat.creation_args_fct_sim_treat()


#obj_sim_sequence_and_treat.fct_sim_treat(*li)
obj_sim_sequence_and_treat.fct_sim_treat(\
list_data_files=li,\
va_nb_comment_lines_ft=v_nb_comment_lines_ft,\
va_nb_comment_lines_mp=v_nb_comment_lines_mp,\
va_nb_comment_lines_psd=v_nb_comment_lines_psd,\
va_nb_comment_lines_ft_off=v_nb_comment_lines_ft_off,\
va_nb_comment_lines_fa=v_nb_comment_lines_fa,\
va_nb_comment_lines_fa_max_green=v_nb_comment_lines_fa_max_green,\
va_di_param_ctrl_mp_practical_ctrl=v_va_di_param_ctrl_mp_practical_ctrl)

#obj_sim_sequence_and_treat.fct_sim_treat(*obj_sim_sequence_and_treat.creation_args_fct_sim_treat())
#lis=obj_sim_sequence_and_treat.fct_sim_treat(*obj_sim_sequence_and_treat.creation_args_fct_sim_treat())
#for i in lis:
	#print("hi",len(lis))