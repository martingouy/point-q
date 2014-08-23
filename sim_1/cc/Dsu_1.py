#import File_Sim_Name_Module_Files
import Cl_Decisions
import Cl_Control_Actuate

#*****************************************************************************************************************************************************************************************
#the name of the folder where the netowrk files are registered
#val_name_folder_network_files="../SMALL_NETWS_2/RÉSEAUX/SMALL_DATA_2NDS"
#val_name_folder_network_files="../SMALL_DATA_NG_4NDS"
#val_name_folder_network_files="../SMALL_DATA_INTERS_2NDS_LK_CAP_PRIOR_PHASES"
#val_name_folder_network_files="../SMALL_NETWS_2/SMALL_round_about_jennie"
#val_name_folder_network_files="../SMALL_NETWS_2/SMALL_DATA_2NDS"
#val_name_folder_network_files="../SMALL_NETWS_2/SMALL_NETWORK_4NDS"
#val_name_folder_network_files="../SMALL_NETWS_2/SMALL_DATA_9NDS"
#val_name_folder_network_files="../SMALL_NETWS_2/SMALL_DATA_test"
#val_name_folder_network_files="../SMALL_NETWS_2/SMALL_DATA_2NDS_FIG_7"
#val_name_folder_network_files="../SMALL_NETWS_2/SMALL_DATA_2NDS_jennie"
#val_name_folder_network_files="../SMALL_NETWS_2/SMALL_round_about_jennie"
#val_name_folder_network_files="../SMALL_NETWS_2/SMALL_DATA_2NDS_FIG_1"
#val_name_folder_network_files="../SMALL_NETWS/reseaux_2/SMALL_DATA_SD"
#val_name_folder_network_files="../SMALL_NETWS/reseaux_3/SMALL_DATA_2NDS_FIG_7_papier_2"
#val_name_folder_network_files="../SMALL_NETWS/reseaux_3/SMALL_DATA_SD_sans_OD"
#val_name_folder_network_files="../SMALL_NETWS/reseaux_3/SMALL_DATA_SD_avec_OD"
val_name_folder_network_files="../SMALL_NETWS/huntington_colorado"
#val_name_folder_network_files="../SMALL_NETWS/reseaux_3/SMALL_DATA_reseau_15_nds"
#*****************************************************************************************************************************************************************************************

#variable indicating if we will  creat the text record file (value=1 the text file will be created,  0 otherwise)
# (where we write in a text file  the realisation of each event).if the value of this variable is  different from 0,1, there will be problems in the
#implementation
#creation_text_file_recording_sim_events_text=1
#creation_text_file_recording_sim_events_text=0

#*****************************************************************************************************************************************************************************************
#variable indicating if messages will be print on the terminal during the simulation (this variable does not concern the error messages, these ones
#will alwyas be printed). If its value=1  messages will be printed, 0 otherwise).if the value of this variable is  different from 0,1, there will be problems in the
#implementation
#print_messages_on_terminal=0
print_messages_on_terminal=1
#*****************************************************************************************************************************************************************************************
#variable  indicating the precision on  some rounds that we will use (depending on the t_unit)
val_precision_round_for_defin_time=1 
#*****************************************************************************************************************************************************************************************
#variable indicating the round precision on computations pressure etc.  related to control algos
val_precision_round=2
#*****************************************************************************************************************************************************************************************
#variable indicating the time unit considered
#val_t_unit=1
val_t_unit=0.1

#*****************************************************************************************************************************************************************************************
#variable indicating if we want to connect point-q simulator with the CTM simulator (1 -> yes, 0 -> no)
#val_ctm_connect = 1
val_ctm_connect = 0

#*****************************************************************************************************************************************************************************************
#variable indicating the path of the folder in which state infos exchanged with CTM will be
val_fol_ctm_connect = '../../../pq_ctm/shared'

#*****************************************************************************************************************************************************************************************

#variable indicating whether a stochastic or deterministic (1, 0)  demand is been employed
val_indicating_stoch_demand=0
#val_indicating_stoch_demand=1

#*****************************************************************************************************************************************************************************************
#variable indicating if we wish to create a new demand or not. If its value = 1, new vehicles will be generated to each entry link, 
#if  its value = 0, a previously generated demand will be employed,
#if  its value = -1, a given (generated) demand will be employed,
creation_new_demand=1
#creation_new_demand=0
#creation_new_demand=-1
#*****************************************************************************************************************************************************************************************

#variable indicating the path folder containing the results of the previously generated demand, (variable to be filled if 'creation_new_demand'=0)
#path_prev_generated_veh_demand="./FRes-Thu-26-Jul-2012_13-10-29/veh_appearance_after_end_sim_in_event_list"
#path_prev_generated_veh_demand="./SIMS_2ND_MP_D2=FT/FRes-Fri-19-Oct-2012_17-19-25"
#path_prev_generated_veh_demand="./FRes-Thu-18-Oct-2012_00-31-32"
#path_prev_generated_veh_demand="FRes-Fri-16-Nov-2012_21-45-55"
#path_prev_generated_veh_demand="./Series_Sim-Wed-07-Aug-2013_20-24-54/FRes-Wed-07-Aug-2013_20-24-54"
#path_prev_generated_veh_demand="./S_RP_8dec_2e_implem_3h/FRes-Thu-19-Sep-2013_10-28-28"
#path_prev_generated_veh_demand="./S_FA_MAX_GREEN_res_2nds/FRes-Fri-03-Jan-2014_11-58-35"
path_prev_generated_veh_demand="./Series_Sim-Fri-02-May-2014_19-18-23/FRes-Fri-02-May-2014_19-18-23"
#*****************************************************************************************************************************************************************************************
#variable indicating the reason of employing a previously generated demand (variable to be filled if 'creation_new_demand'=0)
#if Cl_Decisions.TYPE_REASON_EMPLOYING_PREVIOUS_DEMAND["CTRL_EVAL"] is selected  it is because a signal control policy will be evaluated
# If  Cl_Decisions.TYPE_REASON_EMPLOYING_PREVIOUS_DEMAND["ROUT_ALGO_EVAL"] is selected  it is because a routing policy will be evaluated
#in which case, val_type_veh_final_dest=Cl_Decisions.TYPE_VEHICLE_FINAL_DESTINATION_AND_PATH["initially_defined_and_path_dyn_constructed"]

reason_employing_previous_demand=Cl_Decisions.TYPE_REASON_EMPLOYING_PREVIOUS_DEMAND["CTRL_EVAL"]
#reason_employing_previous_demand=Cl_Decisions.TYPE_REASON_EMPLOYING_PREVIOUS_DEMAND["ROUT_ALGO_EVAL"]
#*****************************************************************************************************************************************************************************************
#variable indicating if we wish to do a new simulation  or not. If its value = 1 a new simulation will be realised, if its value =0 a previous one 
#will be continued.if the value of this variable is  different from 0,1, there will be problems in the
#implementation
new_simulation=1
#new_simulation=0
#*****************************************************************************************************************************************************************************************
#the path folder where the  files with the final state of a simulation are registered, utilised when we wish to continue a previously made simulation
#this variable will be utilised when new_simulation=0, (variable to be filled if 'new_simulation'=0)
#path_name_folder_results_sim_to_be_continued="./FRes-Tue-23-Oct-2012_22-12-26"
#path_name_folder_results_sim_to_be_continued="./SIMS_2ND_FT_D2_L2/FRes-Fri-19-Oct-2012_11-56-46"
#path_name_folder_results_sim_to_be_continued="./Series_Sim-Fri-16-Aug-2013_22-42-11/FRes-Fri-16-Aug-2013_22-42-11"
path_name_folder_results_sim_to_be_continued="./Series_Sim-Fri-02-May-2014_19-18-23/FRes-Fri-02-May-2014_19-18-23"
#*****************************************************************************************************************************************************************************************
#the time at which we wish to start a new simulation.
#this variable will be utilised when new_simulation=1
t_start_new_simulation=0

#*****************************************************************************************************************************************************************************************
#the time during which we wish to simulate
#t_simulation_duration=10
#t_simulation_duration=50
#t_simulation_duration=70
#t_simulation_duration=100
#t_simulation_duration=150
#t_simulation_duration=200
#t_simulation_duration=270
#t_simulation_duration=250
#t_simulation_duration=300
#t_simulation_duration=320
#t_simulation_duration=420
#t_simulation_duration=500
#25 cycles
#t_simulation_duration=700
#t_simulation_duration=900
#t_simulation_duration=930
#t_simulation_duration=1000
#each cycle is 24 sec, we sim for 50 cycles
#t_simulation_duration=1200
#t_simulation_duration=1280
#t_simulation_duration=1800
#t_simulation_duration=1802
#t_simulation_duration=2370
#t_simulation_duration=2400
#t_simulation_duration=2703
#t_simulation_duration=3000
#t_simulation_duration=3600
#t_simulation_duration=5000
#t_simulation_duration=6000
#t_simulation_duration=10000
#t_simulation_duration=10800
t_simulation_duration=18000
#t_simulation_duration=21600
#t_simulation_duration=7200
#t_simulation_duration=36000
#t_simulation_duration=28800

#*****************************************************************************************************************************************************************************************
#the min margin at which the new network control object (for the next cycle) mut be returned.
#It T is the cycle duration, the new event end decision network control must be realised at T-dt, not later than that
#margin_dt=1
margin_dt=2
#margin_dt=4
#margin_dt=9
#margin_dt=10
#margin_dt=15
#margin_dt=20
#margin_dt=0

#*****************************************************************************************************************************************************************************************
#the cycle duration in secs, employed inthe stat analysis, when calc nb veh ar/dep per cycle, 
#il n'est pas ds Cl_Data
cycle_duration=60
#cycle_duration=90
#cycle_duration=74
#cycle_duration=62
#*****************************************************************************************************************************************************************************************
#variable indicating if  internal links have (not) finite capacity (it is employed by the stat analysis. Thsi value is also indicated in the network data model)
#also employed by the event end veh depart
#val_finite_capacity_internal_links=1 #if internal  lks have finite capacity, 0 otherwise
#val_finite_capacity_internal_links=0
val_finite_capacity_internal_links=1
#*****************************************************************************************************************************************************************************************

#the min hold time of a vehicle in a queue
#val_min_hold_t_veh_in_que=1
val_min_hold_t_veh_in_que=0.1
#val_min_hold_t_veh_in_que=0

#*****************************************************************************************************************************************************************************************


#the marge of time, starting from the begining of the simulation, from which we will count the time duration after which a new vehicle will be appeared
#at an entry link.
#for ex: if this time is x sec after the begining of the sim, vehicles will start to appear at  x+ the time duration defined by the Poisson process 
#(t_start_sim+marge=0+120sec=120 sec)
#val_t_marge_start_calcul_veh_appearance=4
#val_t_marge_start_calcul_veh_appearance=2
val_t_marge_start_calcul_veh_appearance=0.2
#*****************************************************************************************************************************************************************************************

#variable indicating if we wish to treat the sim resutls or not (writ veh hist files)
#val_treat_sim_res=0
val_treat_sim_res=1

#****************************************************************************************************************************************************************************************

#variable indicating if each intersection control  matrix (control) is read (case when cotnrol is given) or calculated within the sim
#val_ncm_read=1 if we read the ctrl matrices for the entire sim,val_ncm_read=0 if we calculate the ctrl within every cycle or period
#val_ncm_read=1
val_each_icm_read=0
#*****************************************************************************************************************************************************************************************
#variable indicating the type of each vehicle regarding its final destination
#"dynamically_defined"=when give proba are attributes to each phase and the veh final destination is not inti defined (no OD mat)
#"initially_defined_and_path_given"=when the final dest and the whole path are defined (OD mat)
#"initially_defined_and_path_dyn_constructed"=when the veh final dest is initially defined but the routing is dynam computed

val_type_veh_final_dest=Cl_Decisions.TYPE_VEHICLE_FINAL_DESTINATION_AND_PATH["dynamically_defined"]
#val_type_veh_final_dest=Cl_Decisions.TYPE_VEHICLE_FINAL_DESTINATION_AND_PATH["initially_defined_and_path_given"]
#val_type_veh_final_dest=Cl_Decisions.TYPE_VEHICLE_FINAL_DESTINATION_AND_PATH["initially_defined_and_path_dyn_constructed"]
#*****************************************************************************************************************************************************************************************

#variable indicating how (the algo)  paths are computed when OD matrice and path dyn computed


#ii)"dynam_based_on_t_trav_OD"=case when we have OD matrices (we know the veh final destination from its appearance) 
#the split ratios are dynamically calculated by an algo based on  current link travel times
#iii) "dynam_based_on_prob_and_t_trav_OD"= when OD matrices (final destination initial defined),the next destin is selected 
#according the  t_travel proportionnaly to all the possible routings.


#val_type_rout_algo_when_given_od_and_dyn_computed_paths=Cl_Decisions.TYPE_CALCUL_ROUT_PROP["dynam_based_on_t_trav_OD"]
val_type_rout_algo_when_given_od_and_dyn_computed_paths=Cl_Decisions.TYPE_CALCUL_ROUT_PROP["dynam_based_on_prob_t_trav_OD"]


#*****************************************************************************************************************************************************************************************
#variable indicatinf if a fixed (1) or stochastic time (2) travel duration is employed 
#fixed travel duration
val_type_trav_duration_managament=Cl_Decisions.TYPE_TRAVEL_DURAT_MANAG[1]
#stochastic travel duration
#val_type_trav_duration_managament=Cl_Decisions.TYPE_TRAVEL_DURAT_MANAG[2]
#*****************************************************************************************************************************************************************************************
#*****************************************************************************************************************************************************************************************
#********************************VAL PRÉCÉD**************************************************************************************************************************************************

#variable indicating if the turn ratios are/not going to be estimated, if 1 turn ratios will be estimated, 0 otherwise
#val_turn_ratios_estimated=1
#val_turn_ratios_estimated=0
#*****************************************************************************************************************************************************************************************

#*****************************************************************************************************************************************************************************************
#variable indicating the parameter defining the  latest time for a vehicle to leave 
#when another veh of a compatible phase crosses an unsignalised intersection
# (if t_current < epsilon x t_end_depart_veh_crossing_inters,  the other veh will go)
#val_param_epsilon_t_latest_for_veh_to_leave_compatible_phase_nsi=0.33
#*****************************************************************************************************************************************************************************************
#variable indicating if merging ques are considered in the network model
#val_merging_ques=1 if merging ques are consider, 0 or any other value otherwise
#val_merging_ques=1
#val_merging_ques_considered=0
#*****************************************************************************************************************************************************************************************
#variable indicating the name of the file  where the parameters of the FT or MX control are written
#we apply MP control
#val_name_fi_values_ft_mp_control=File_Sim_Name_Module_Files.val_name_file_values_mp_control
#val_name_fi_values_ft_mp_control=File_Sim_Name_Module_Files.val_name_file_values_ft_control
#*****************************************************************************************************************************************************************************************
#variable indicating the type of the control policy applied in this simulation
#type_control_policy can take 
#1: "type_control_FT",2: "type_control_FT_Offset",  3: "type_control_MP",4:"type_control_MIXED"} 
#5: "type_control_MP_pro",
#6: "type_control_MP_pro_wasteful", these values are indicated in Cl_Decisions
#7:"type_control_PREDEFINED"
#(1,3):"type_prev_sim_FT_type_contin_new_one_MP", if a previous sim of FT is been continued with a MP control
#8="type Pressure Stage_Actuate Control"
#9:"type_control_MP_No_output_que"
#10:"type_control_FA"
#11:"type_control_FA_Max_Green"
#12:":"type_control_MP_when_OD_matrices_considered""
#13: "type_control_MP_Practical"

#val_type_control_policy=Cl_Control_Actuate.TYPE_CONTROL[1]
#val_type_control_policy=Cl_Control_Actuate.TYPE_CONTROL[2]
#val_type_control_policy=Cl_Control_Actuate.TYPE_CONTROL[3]
#val_type_control_policy=Cl_Control_Actuate.TYPE_CONTROL[4]
#val_type_control_policy=Cl_Control_Actuate.TYPE_CONTROL[5]
#val_type_control_policy=Cl_Control_Actuate.TYPE_CONTROL[6]
#val_type_control_policy=Cl_Control_Actuate.TYPE_CONTROL[8]
#val_type_control_policy=Cl_Control_Actuate.TYPE_CONTROL[1,3]
#val_type_control_policy=Cl_Control_Actuate.TYPE_CONTROL[9]
#val_type_control_policy=Cl_Control_Actuate.TYPE_CONTROL[10]
#val_type_control_policy=Cl_Control_Actuate.TYPE_CONTROL[11]
#val_type_control_policy=Cl_Control_Actuate.TYPE_CONTROL[12]
#val_type_control_policy=Cl_Control_Actuate.TYPE_CONTROL[13]
#*****************************************************************************************************************************************************************************************
#variable indicating the category  of the control (the one indicated above) at the beginning of the sim 
#possibility of changing ctrl types within the sim duration, 
#FA, FA max green demand a crl revision according to flow variation so they require sensors 
#val_type_ctrl_category_at_the_beg_of_sim=Cl_Control_Actuate.TYPE_CONTROL_CATEGORY["sensor_requirement"]
#val_type_ctrl_category_at_the_beg_of_sim=Cl_Control_Actuate.TYPE_CONTROL_CATEGORY["without_sensor_requirement"]

#*****************************************************************************************************************************************************************************************
#variable indicating the type first control when a mixed control moilicy is employed
#this variable wil be used in the initialisation of a new simulation
#it takes 1: "type_control_FT",  2: "type_control_MP"
#val_type_first_control_when_mixed_control_policy=Cl_Control_Actuate.TYPE_CONTROL[1]
#*****************************************************************************************************************************************************************************************
#variable indicating the type of simulator, macro, micro (for the veh departure)
#it takes two values, 1:"macro", 2:"micro"
#Cl_Decisions.TYPE_SIMULATOR_MANAGEMENT[1] = macro, Cl_Decisions.TYPE_SIMULATOR_MANAGEMENT[2] = micro
#val_type_sim_management=Cl_Decisions.TYPE_SIMULATOR_MANAGEMENT[1]
#val_type_sim_management=Cl_Decisions.TYPE_SIMULATOR_MANAGEMENT[2]

#*****************************************************************************************************************************************************************************************

#variable indicating if the  turnratios are going to be estimated during the sim or not
#if val_turn_ratios_estimated=0 the turn prob are not going to be estim, if val_turn_ratios_estimated=1 they will
#val_turn_ratios_estimated=0
#val_turn_ratios_estimated=1

#*****************************************************************************************************************************************************************************************






























