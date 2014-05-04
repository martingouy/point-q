#*****************************************************************************************************************************************************************************************
#the name of the folder with the veh files 
name_folder_veh_inform="Sim_Treat"
#*****************************************************************************************************************************************************************************************
#the name fo the folder  with the veh files
name_folder_veh_files="VEH_RES"
#*****************************************************************************************************************************************************************************************
#the name of the folder where the folders of the stat analysis will be placed
name_folder_stat_anal="Stat_Anal"

#*****************************************************************************************************************************************************************************************
#the name of the folder where the folders of the stat verification will be placed
name_folder_stat_verif_anal="Stat_Verif_Anal"
#*****************************************************************************************************************************************************************************************
#the name of the folder with the control evolution
name_folder_ctrl_evol="CTRL_EVOL"
#*****************************************************************************************************************************************************************************************
#the name of the folder with the evolution of each stage of each intersection
name_folder_stage_evol_per_intersection="STAGE_EVOL_INTERS"
#*****************************************************************************************************************************************************************************************
#the name of the folder with the files indicating the number of stage  switches for ech intersection
name_folder_stage_switches_per_intersection="STAGE_SWITCHES_INTERS"
#*****************************************************************************************************************************************************************************************
#the name of the folder with the actuation duration of each phase per period
name_folder_phase_act_durat_per_period="PHASE_ACT_DURATION_PER_PERIOD"
#*****************************************************************************************************************************************************************************************
#the name of the folder with the files describing the evolution of each link
name_folder_link_evol="LINK_EVOL"
#*****************************************************************************************************************************************************************************************

#the name of the folder to write the files for the evolution of each queue during sim
name_folder_queue_evol="QUE_EVOL"

#*****************************************************************************************************************************************************************************************
#the name of the folder to write the files for the evolution of each queue during sim
name_folder_queue_evol_1="QUE_EVOL_1"

#*****************************************************************************************************************************************************************************************
#the name of the folder to place the file with the sum  values of all queues during sim
name_folder_sum_queues_evol="QUE_EVOL_SUM"
#*****************************************************************************************************************************************************************************************
#the name of the folder with the avearga values of the sum of queues during the sim (sum of queeus (t)/total nb of veh queues in the netwrok)
name_folder_average_sum_queues_evol="QUE_EVOL_AVERAGE_SUM"
#*****************************************************************************************************************************************************************************************
#the name of the folder to write the the average (over the nb of time instances belonging in the period) sum of the queues per period
name_folder_average_sum_ques_per_period_over_nb_t_instances_within_period="QUE_EVOL_AVERAGE_SUM_PER_PERIOD"
#*****************************************************************************************************************************************************************************************


#the name of the folder to write the files, representing the number of veh arrival/appear at each queue
name_folder_nb_veh_que_ar_ap="QUE_EVOL_VEH_AR_AP"

#*****************************************************************************************************************************************************************************************

#the name of the folder to wirte the files, representing the number of veh departing from each queue
name_folder_nb_veh_dep_que="QUE_EVOL_VEH_DEP"
#*****************************************************************************************************************************************************************************************
#the name of the folder with the files indicating the veh arrivals and departures per cycle
name_folder_nb_veh_ar_dep_per_cycle="QUE_AR_DEP_PER_CYCLE"
#*****************************************************************************************************************************************************************************************
#the name of the folder to write the files, representing the number of times that the queue had a "number" of vehicles, after veh arrival/appear events
name_folder_nb_times_with_nb_veh_at_que_ar_ap="QUE_NB_TIMES_NB_VEH_AR_AP"

#*****************************************************************************************************************************************************************************************
#the name of the folder to write the files, representing the number of times that the queue had a "number" of vehicles, after veh depart events
name_folder_nb_times_with_nb_veh_dep_que="QUE_NB_TIMES_NB_VEH_DEP"

#*****************************************************************************************************************************************************************************************
#the name of the folder to write the files, representing the queue evolution after each veh departure
name_folder_queue_evol_after_veh_dep="QUE_EVOL_AFTER_VEH_DEP"

#*****************************************************************************************************************************************************************************************

#the name of the folder to write the files with the mean travel time between entry-exit links
name_folder_mean_travel_time_entry_exit_lk="MEAN_TR_TIME_EN_EX_LK"
#*****************************************************************************************************************************************************************************************
#the name of the folder with the fiile with the mean value of each queue
name_folder_mean_time_spent_by_veh_in_que="MEAN_TIME_SPENT_BY_VEH_IN_QUE"

#*****************************************************************************************************************************************************************************************
#the name of the folsed with the veh of the veh flow per time period of each entry link, of the sim results
name_folder_val_name_file_cum_veh_flow_per_period_lk_sim_res="VEH_FLOW_PER_PERIOD_IN_ENTRY_LK_SIM_RES"
#*****************************************************************************************************************************************************************************************
#the name of the folsed with the veh of the veh flow per time period of each exit link, for the given demand
name_folder_val_name_file_cum_veh_flow_per_period_lk_given_demand="VEH_FLOW_PER_PERIOD_IN_ENTRY_LK_SIM_RES_GIVEN_DEMAND"
#*****************************************************************************************************************************************************************************************
#the name of the folsed with the veh of the veh flow per time period of each entry  link, of the sim results
name_folder_val_name_file_cum_veh_flow_per_period_exit_lk_sim_res="VEH_FLOW_PER_PERIOD_IN_EXIT_LK_SIM_RES"
#*****************************************************************************************************************************************************************************************
#the name of the folsed with the veh of the veh flow per time period of each internal  link, of the sim results
name_folder_val_name_file_cum_veh_flow_per_period_internal_lk_sim_res="VEH_FLOW_PER_PERIOD_IN_INTERNAL_LK_SIM_RES"
#*****************************************************************************************************************************************************************************************
#the name of the folsed with the veh of the veh flow per time period of each exit  link, for the given demand
name_folder_val_name_file_cum_veh_flow_per_period_exit_lk_given_demand="VEH_FLOW_PER_PERIOD_IN_EXIT_LK_SIM_RES_GIVEN_DEMAND"
#*****************************************************************************************************************************************************************************************
#the name of the folder with the veh of trav time evolution per time period, for each entry exit link
name_folder_travel_time_per_period_entry_exit_lk="TRAVEL_TIME_PER_PERIOD_ENTRY_EXIT_LINK"
#*****************************************************************************************************************************************************************************************
#the name of the folder with the traveled distance per period, for each entry exit link
name_folder_traveled_dist_per_period_entry_exit_lk="TRAVELED_DISTANCE_PER_PERIOD_ENTRY_EXIT_LINK"
#*****************************************************************************************************************************************************************************************

#name folder where we place FRes files of series of sims
name_folder_series_sims="Series_Sim"
#*****************************************************************************************************************************************************************************************
#the name of the file with the ctrl evol of each phase
name_file_ctrl_evolution_phase="fi_ctrl_evol_phase_"
#*****************************************************************************************************************************************************************************************
#the name of the file with the times at which the phase was actuated
name_file_time_actuation_phase="fi_t_actuation_phase_"
#*****************************************************************************************************************************************************************************************
#the name of the file with the evolution of each link
name_file_evolution_lk="fi_evol_lk_"
#*****************************************************************************************************************************************************************************************
#the name of the file representing the queue evolution during sim
name_file_queue_evol="fi_evol_que_"
#*****************************************************************************************************************************************************************************************
#the name of the file representing the queue evolution during sim
name_file_queue_evol_1="fi_evol_que_1_"
#*****************************************************************************************************************************************************************************************

#the name of the FILE to write file with the value of the sum ofll  the queue during the sim
name_file_sum_queue_evol="fi_sum_evol_que"
#*****************************************************************************************************************************************************************************************
#the name of the FILE to write file with the value of the sum of the deired queues during the sim
name_file_sum_desired_queue_evol="fi_sum_evol_desired_ques"
#*****************************************************************************************************************************************************************************************
#the name of the FILE to write  the average (over the total nb of the network ques) value of the sum of the queue 
name_file_average_sum_queue_evol="fi_average_sum_evol_ques"
#*****************************************************************************************************************************************************************************************

#the name of the file to write the the average (over the nb of time instances belonging in the period) sum of all the queues per period
name_file_average_sum_ques_per_period_over_nb_t_instances_within_period="fi_average_sum_ques_per_period_over_nb_t_instances_within_period.txt"

#*****************************************************************************************************************************************************************************************
#the name of the file to write the the average (over the nb of time instances belonging in the period) sum of the desired queues per period
name_file_average_sum_desired_ques_per_period_over_nb_t_instances_within_period="fi_average_sum_desired_ques_per_period_over_nb_t_instances_within_period.txt"

#*****************************************************************************************************************************************************************************************

#the name of the file with the number of vehicles in the queue after each veh arrival/appearance
name_file_nb_veh_que_ar_ap="fi_qevol_after_veh_ar_ap_que_"


#*****************************************************************************************************************************************************************************************
#the name of the file with the number of the departing vehicles from the que 
name_file_nb_veh_dep_que="fi_nb_veh_dep_que_"

#*****************************************************************************************************************************************************************************************
#the name of the file containing the nb of veh at a queue (after each veh arrival/departure event) and the number of times
#during which the queue had this number of veh
name_file_nb_times_nb_veh_que_ar_ap="fi_pie_qevol_after_veh_ar_ap_que_"
#*****************************************************************************************************************************************************************************************
#the name of the file containing the nb of departing veh from a queue  and the number of times
#during which the queue had this number of veh
name_file_nb_times_nb_veh_dep_que="fi_nb_times_nb_veh_dep_que_"
#*****************************************************************************************************************************************************************************************
#the name of the file with the number of vehicles in the queue after each veh departure
name_file_queue_evol_after_veh_dep="fi_qevol_after_veh_dep_que_"

#*****************************************************************************************************************************************************************************************
#the name of the file where we write the mean travel time between entry and exit link
name_file_mean_travel_time_entry_exit_lk="fi_mean_trav_time_entry_exit_lk.txt"
#*****************************************************************************************************************************************************************************************
#name of the file with the mean length of the sum of queues 
name_file_mean_length_sum_queues="fi_mean_length_sum_ques.txt"
#*****************************************************************************************************************************************************************************************
#the name of the file with the mean length of each queue
name_file_mean_time_spent_by_veh_in_que="fi_mean_time_spent_by_veh_in_que"

#*****************************************************************************************************************************************************************************************
#the name of the file with the mean value of the mean travel time spent by vehicles in queues
val_name_file_mean_of_aver_sojourn_time="fi_mean_of_aver_soj_time.txt" 
#*****************************************************************************************************************************************************************************************

#name of the file containing the number of veh in queue and the probability of having this number, for the sum of queues of one sim
name_file_nb_veh_prob_sum_que="fi_nb_veh_prob_sum_ques.txt"

#*****************************************************************************************************************************************************************************************
val_name_file_wm_sd_series_sim="fi_wm_sd_series_sim.txt"
#*****************************************************************************************************************************************************************************************
#the name of the file with the mean travel time and the departed vehicles of the series of sims
val_name_file_mean_tr_t_nb_dep_veh_series_sims="fi_mean_tr_t_nb_dep_veh_series_sims.txt"

#*****************************************************************************************************************************************************************************************
#the name of the file with the max length of the sum of each queue,  of a series of sims
val_name_file_max_size_each_sum_ques_series_sims="fi_max_size_each_sum_ques_series_sims.txt"

#*****************************************************************************************************************************************************************************************
#the name of the file with the max and min value of the sum of queues of a series of sims 
val_name_file_max_min_size_sum_ques_series_sim="fi_max_min_size_sum_ques_series_sims.txt"
#*****************************************************************************************************************************************************************************************
#the name of the file with the cum value of the veh flow of an exit link for the sim res
val_name_file_cum_veh_flow_per_period_entry_lk_sim_res="fi_veh_flow_per_per_entry_lk_sim_res"

#*****************************************************************************************************************************************************************************************
#the name of the file with the cum value of the veh flow of a  exit link for the given demane
val_name_file_cum_veh_flow_per_period_exit_lk_sim_res="fi_veh_flow_per_per_exit_lk_sim_res"

#*****************************************************************************************************************************************************************************************
#the name of the file with the cum value of the veh flow of an internal  link for the given demane
val_name_file_cum_veh_flow_per_period_internal_lk_sim_res="fi_veh_flow_per_per_internal_lk_sim_res"

#*****************************************************************************************************************************************************************************************
#the name of the file with the cum value of the veh flow of an entry link when given demand
val_name_file_cum_veh_flow_per_period_lk_given_dem="fi_veh_flow_per_per_entry_lk_given_demand"
#*****************************************************************************************************************************************************************************************
#the name of the file with the total nb veh arrivales appear depar queue sizes and veh departing after end sim , for each node
val_name_veh_flow_conservation="fi_veh_flow_conservation.txt"

#*****************************************************************************************************************************************************************************************
#the name of the file with the ith the veh of trav time evolution per time period, between and entry exit link
name_file_travel_time_per_period_entry_exit_link="fi_travel_time_per_period_entry_exit_lk_"
#*****************************************************************************************************************************************************************************************
#the name of the file with the traveled distance per period between entry and exit link
name_file_traveled_dist_per_period_entry_exit_link="fi_traveled_distance_per_period_entry_exit_lk_"

#*****************************************************************************************************************************************************************************************
#the name of the file with the vehicle id and the arrival_appear, departure times (start-end), que size for a given link
name_file_history_veh_ar_ap_dep_and_quesize_que="fi_history_veh_on_que_"
#*****************************************************************************************************************************************************************************************
#the name of the file with the vehicle id and the t arrival_appear, t arrival next link, t arrival next link - t arrival_appear
name_file_history_veh_t_cur_and_next_ar_que="fi_history_veh_t_cur_and_next_ar_que_"
#*****************************************************************************************************************************************************************************************
#the name of the file with  t arrival_appear, t arrival next link - t arrival_appear
name_file_history_veh_t_ar_t_trav_time_que="fi_history_veh_t_ar_t_trav_time_que_"
#*****************************************************************************************************************************************************************************************
#the name of the file with  t arrival_next link , t arrival next link - t arrival_appear
name_file_history_veh_t_ar_next_lk_t_trav_time_que="fi_history_veh_t_ar_next_lk_t_trav_time_que_"
#*****************************************************************************************************************************************************************************************
#the name of the file with  que size metby veh at its arrival in the que , t arrival next link - t arrival_appear
name_file_history_veh_que_size_t_ar_next_lk_t_trav_time_que="fi_history_veh_que_size_t_ar_next_lk_t_trav_time_que_"
#*****************************************************************************************************************************************************************************************
#the name of the file with the veh arrivals  per cycle per phase
name_file_veh_ar_per_cycle_que="fi_veh_ar_per_cycle_que_"
#*****************************************************************************************************************************************************************************************
#the name of the file with the veh departures  per cycle per phase
name_file_veh_dep_per_cycle_que="fi_veh_dep_per_cycle_que_"
#*****************************************************************************************************************************************************************************************
#the name of of the file with the difference deprts minus arrivals per cycle
name_file_dif_departs_minus_ar_per_cycle_que="fi_dif_departs_minus_ar_per_cycle_que_"

#*****************************************************************************************************************************************************************************************
#the name of the file with the number of actuations each phase per cycle
name_file_nb_actuation_per_cycle_phase="fi_nb_actuation_per_cycle_phase_"
#*****************************************************************************************************************************************************************************************
#the name of the file with the total actuation duration per period of a phase
name_file_total_act_duration_per_period_phase="fi_total_act_duration_per_period_phase_" 

#*****************************************************************************************************************************************************************************************
#the name fo the file with the number of act durat and departed veh per phase per ccyle
name_file_act_dur_and_veh_depart_per_cycle_per_phase="fi_act_dur_and_veh_depart_per_cycle_per_phase_"
#*****************************************************************************************************************************************************************************************
#the name of the file with the stage evolution_per_intersection
name_file_stage_evol_per_intersection="fi_stage_evol_per_intersection_"

#*****************************************************************************************************************************************************************************************
#the name of the file with the stage switches per intersection
name_file_stage_switches_per_itnersection="fi_stage_switches_intersection.txt"

#*****************************************************************************************************************************************************************************************










