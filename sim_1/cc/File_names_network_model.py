
#the name of the file indicating the names of the files for the network modelling
val_file_name_demand_param_entry_link="fi_demand_param_entry_link.txt"

#*****************************************************************************************************************************************************************************************
#the name of the file containing the id of the node and the id of the entering links to the node
#this file will be employed when constructing the intersection nodes 
val_file_name_id_node_id_entering_links_to_node="fi_id_node_id_entering_links_to_node.txt"

#*****************************************************************************************************************************************************************************************
#the name of the file containing the id of the node and the id of the leaving links from the node
#this file will be employed when constructing the intersection nodes
val_file_name_id_node_id_leaving_links_from_node="fi_id_node_id_leaving_links_from_node.txt"

#*****************************************************************************************************************************************************************************************
#the name of the file containing the id of the (head node) and the id of the corresponding entry links to  the network
#it will be employed for the construction of the entry links of the network
val_file_name_id_node_id_entry_links_to_network="fi_id_node_id_entry_links_to_network.txt"

#*****************************************************************************************************************************************************************************************
#the name of the file containing the id of the (tail node) and the id of the corresponding exit links from the network
#it will be employed for the construction of the exti links of the network
val_file_name_id_node_id_exit_links_from_network="fi_id_node_id_exit_links_from_network.txt"

#*****************************************************************************************************************************************************************************************
#the name of the file indicating the node id, the parameter for estim the turn ratios and  the duration of the estim turn ratio values
#val_name_file_if_node_andparam_estim_turn_ratio_andduration_turn_ratio="fi_id_node_estim_turn_ratio_param_dur_turn_ratios.txt"

#*****************************************************************************************************************************************************************************************
#the name of the file containing the id of the internal link and the id of the corresponding head and tail nodes of the link
#it will be employed for the construction of the internal links of the network
val_file_name_id_internal_link_id_orig_dest_node="fi_id_internal_link_id_orig_dest_node.txt"
#*****************************************************************************************************************************************************************************************
#the name of the file defining the the max queue size, the saturation flow of each phase (queue, (l,m))
#and the queue type
#the first column is the id of a network link, the 2nd column is the id of the output link (phase), 
#the 3rd column is the the max queue size of the link (1st column) and the 4th column is the 
#saturation flow of the phase and the 5th column is the que type
val_file_name_id_all_phases_max_queue_size_and_sat_flow_queue_type=\
"fi_id_all_phases_max_queue_size_sat_flow_queue_type.txt"
#*****************************************************************************************************************************************************************************************
#the name of the file defining for each phase the intial, final position captured by each detector associated with the queue ainsi que the nb of positions captured 
#by the detector
val_file_name_id_all_phases_init_fin_detect_posit_nb_posit_captured="fi_id_all_phases_init_fin_detect_posit_nb_posit_captured.txt"
#*****************************************************************************************************************************************************************************************

#the name of the file containing the is of all network links, the id of their origin and destination nodes as well as the lenght of the link
val_file_name_id_all_network_link_id_orig_dest_node_length_link_capacity_link_param_travel_duration=\
"fi_id_all_network_link_id_orig_dest_node_length_link_capacity_link_param_travel_duration.txt"
#*****************************************************************************************************************************************************************************************
#the name of the file containing the id of the  links and the id of the asociated entry links.
#val_file_name_id_all_network_link_id_orig_dest_node_length_link="fi_id_all_network_link_id_orig_dest_node_length_link.txt"
#*****************************************************************************************************************************************************************************************
#the name of the file containing the demand parameter of an entry link
val_file_name_id_link_id_sublinks="fi_id_link_id_sublinks.txt"
#*****************************************************************************************************************************************************************************************
#the name of the file with the id of all network links the id of the origin and destination nodes of the link and the length of the link
val_file_id_all_network_link_id_orig_dest_node_length_link="fi_id_all_network_link_id_orig_dest_node_length_link.txt"
#*****************************************************************************************************************************************************************************************
#the name of the file with the id of minor phases and their associated  prior phases, for each intersection
#val_name_file_id_minor_phase_id_prior_phase="fi_id_minor_phase_id_prior_phase.txt"
#*****************************************************************************************************************************************************************************************
#the name of the file with the id of prior phases and their associated  minor phases,
#val_name_file_id_prior_phase_id_minor_phase="fi_id_prior_phase_id_minor_phase.txt"
#*****************************************************************************************************************************************************************************************
#the name of the file with the id of  side phases and their associated  main phases
#val_name_file_id_side_phase_id_main_phase="fi_id_side_phase_id_main_phase.txt"
#*****************************************************************************************************************************************************************************************
#the name of the file with the id of main phases and their associated side phases
#val_name_file_id_main_phase_id_side_phase="fi_id_main_phase_id_side_phase.txt"
#*****************************************************************************************************************************************************************************************
#the name of the fime with the merging queues of each link
#val_name_file_id_merging_ques="fi_id_merging_ques"
#*****************************************************************************************************************************************************************************************
#the name of the file with the mu parameter of each entry or itnernal link when stoch travel times are eployed (shifted lognormal distrib)
val_name_file_param_mu_entry_internal_link="matrix_mu.txt"
#*****************************************************************************************************************************************************************************************
#the name of the file with the sigma parameter of each entry or itnernal link when stoch travel times are eployed (shifted lognormal distrib)
val_name_file_param_sift_entry_internal_link="matrix_sigma.txt"
#*****************************************************************************************************************************************************************************************
#the name of the file woth the shift parameter of each entry or itnernal link when stoch travel times are eployed (shifted lognormal distrib)
val_name_file_param_shift_entry_internal_link="matrix_shift.txt"
#*****************************************************************************************************************************************************************************************
#the name of the file with the routing proportions of each phase (of which the st flow is >0)

val_name_file_mat_rp_id_phase_prob_dest_lk="fi_mrp.txt"

#*****************************************************************************************************************************************************************************************
#the name of the file with the values of routing prob for each period (the inital values are in file  "fi_mrp.txt", case when varying routing prob
val_name_file_series_varying_rout_prob="fi_series_varying_rp.txt"

#*****************************************************************************************************************************************************************************************

#the name of the file with the prob of each exit link
val_name_file_mod="fi_mod.txt"
#*****************************************************************************************************************************************************************************************

#the name of the file with the id of the entry-internal link and the associates id of destination links
#val_name_file_id_entry_internal_lk_id_dest_links="fi_id_entry_lk_t_veh_appear_given_demand"
#val_name_file_id_entry_internal_lk_id_dest_links="fi_id_entry_intern_lk_id_dest_lk"

#*****************************************************************************************************************************************************************************************

#the name of the file with the cum function for the routing proportions of each phase (of which the st flow is >0)
val_name_file_mat_rp_cum="fi_mrp_cum.txt"
#*****************************************************************************************************************************************************************************************
#the name of the file with the cum values of routing prob for each period (the inital values are in file  "fi_mrp.txt", case when varying routing prob
val_name_file_series_cum_values_varying_rout_prob="fi_series_cum_val_varying_rp.txt"

#*****************************************************************************************************************************************************************************************
#the name of the file with the cum value of the mod
val_name_file_cum_mod="fi_mod_cum.txt"
#*****************************************************************************************************************************************************************************************
#the name of the file with the duration of each rp (routing proportion) matrix  including the current one already included in the network
#if only one od matrix will be considered it is already included in the network. If more than one  od matrices are considered
#then we will update the network at given instants
#in this file we include the duration of the od matrix already included in the network
val_name_file_duration_each_rp_mat="fi_duration_each_rp_mat.txt"
#*****************************************************************************************************************************************************************************************
#the name of the file with the id of entry link and the time of veh appearance when external demand is been considered
val_name_file_id_entry_lk_t_veh_appear_given_demand="fi_id_entry_lk_t_veh_appear_given_demand.txt"
#*****************************************************************************************************************************************************************************************
#the name of the file with the presence detectors information
val_name_file_pres_detector="fi_presence_detector.txt"
#*****************************************************************************************************************************************************************************************
##the name of the file with the que size detectors information
val_name_file_fi_que_size_detector="fi_que_size_detector.txt"
#*****************************************************************************************************************************************************************************************
#the name fo the file with the id of the non signalised intersection nodes
val_name_file_fi_id_node_type_node="fi_id_node_type_node.txt"
#*****************************************************************************************************************************************************************************************
#the name of the file indicating the type of each entry link
val_name_file_fi_id_entry_link_type_lk="fi_id_entry_link_type_lk.txt"
#*****************************************************************************************************************************************************************************************
#the name fo the file with the compatible phases for nsi
val_name_file_compatible_phases_nsi="fi_compatible_phases_nsi.txt"
#*****************************************************************************************************************************************************************************************
#the name of the file with the stages of each sigbalised intersection
val_name_file_stages_each_signalised_inters="fi_stages_each_sign_inters.txt"
#*****************************************************************************************************************************************************************************************
#the name of the file with the stages of each non sigbalised intersection
val_name_file_stages_each_non_signalised_inters="fi_stages_each_non_sign_inters.txt"
#*****************************************************************************************************************************************************************************************
#the name of the file defining the path to follow when given entry exit link
val_name_file_id_entry_exit_link_path="fi_id_entry_exit_lk_related_path.txt"
#*****************************************************************************************************************************************************************************************
#the name of the file with the demand param values when the demand varies during the sim
val_fi_demand_param_variation="fi_demand_param_variation.txt"
#*****************************************************************************************************************************************************************************************
#the name of the file with he link id and the related mean travel time, employed when calc stoch trav time
val_name_file_id_link_mean_trav_time="fi_id_link_mean_trav_time.txt"

#*****************************************************************************************************************************************************************************************
#the name of the file with he link id and the related mean travel time, employed when calc stoch trav time
val_name_file_link_mean_trav_time="fi_link_mean_trav_time.txt"

#*****************************************************************************************************************************************************************************************
#the name of the file indicating  the initial state of each queue
val_name_file_init_state_que="fi_init_state_que.txt"

#*****************************************************************************************************************************************************************************************
#the name of the file indicating the phase interference
name_file_phase_interference="fi_phase_interference.txt"
#*****************************************************************************************************************************************************************************************


#*****************************************************************************************************************************************************************************************
#*****************************************************************************************************************************************************************************************

#**********************************************************NAMES OF FOLDERS***************************************************************************************************

#*****************************************************************************************************************************************************************************************
#the name of the folder with the fiels of the demand param when varying demand
val_name_folder_with_files_demand_param_when_varying_demand="fi_demand_param_variation"

































