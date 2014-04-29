point-q
=======

Point-queue simulator in Python3


Instructions for an implementation

 
1)  Fill the «  Dsu_1.py »  file (file located in folder cc)

2) In the folder « Control_Param_Files »  (folder in folder cc) indicate the file with the control parameters and the file indicating the the nice id  and the type of the employed control.

More precisely in the folder « Control_Param_Files » two files should  exist:

i) « fi_node_id_ctrl_type_category.txt »  

A priori each node may have a different type of control. 

File « fi_node_id_ctrl_type_category.txt »  indicates  which type of control  should be applied at each intersection node. 

Each  line of this file corresponds to a specific node.

For each line, four columns correspond.

The first column indicated the node id. 

The second column indicates the type of the control.

The control types available at this moment are:

0:"type_control_red_clear",
1:"type_control_FT", 
2:"type_control_FT_Offset", 
3:"type_control_MP",
10:"type_control_FA_no_red_clear",
11:"type_control_FA_Max_Green",\
12:"type_control_FA_with_red_clear",
13:"type_control_MP_Practical",
14:"type_control_MP_without_red_clear",\
15:"type_control_MP_Practical_without_rec_clear"

remarque: if there are missing numbers it is because there exist controls which are not currently employed (mixed, MP with boundary controls, MP without negative pressure etc).

The 3rd column may take two possible values:

a) « without_sensor_requirement » if the employed control is updated at predefined times (which do not depend from the current values of flows or queues. There are the FT control, FT with offsets, all versions of MP)

b) `` with_sensor_requirement ‘’ if the employed control is updated according to the current values of flows or queues (e.g. FA, FA with max green etc.).

The fourth column indicates if the turn ratios are going to be estimated (value 1) or not (value 0) during the implementation. This make sense for controls   selecting a stage  with use of the saturation flows (for exemple, MP, FA etc).


ii) A file indicating the control parameters

If  it is FT, FT with offsets or FA (not working yet….) only one file is required.
If a version of MP is employes two files will be required. 

More precisely.

a) For a FT this file  is called «File_FT_Control_Alg_Param.txt» 
b) For FT with offsets this file is called « File_FT_Offset_Control_Alg_Param.txt »
c) For MP these file are  called ``File_MP_Control_Alg_Param_res.txt ‘’ and ``File_MP_Qvalues_phases.txt »
d) for MP without red clearance, these files are called ``File_MP_without_rc_Control_Alg_Param.txt’’ and NOT YET completed
e) For MP Practical these files should be called ``File_MP_Practical_Control_Alg_Param.txt’’  and NOT YET completed
f) for FA with red clearance this file should be called ``File_FA_with_red_clear_Control_Alg_Param.txt »
g)for FA with red clearance this file should be called "File_FA_no_red_clear_Control_Alg_Param.txt"
h) for FA with max green, this file should be called "File_FA_MAX_GREEN_Control_Alg_Param.txt"


Here after is a short explanation of each file, for which there is also an exemple for the network of 15 nodes in the folder Control_Param_Files

a1) File_FT_Control_Alg_Param.txt

each line corresponds to a node.`
The first line of this file explains  each column

For any other line:

- the 1st column indicates the node id

- the second column indicates the stage id. A strictly positive number if the stage is not red clearance, 0 otherwise.
Stages are indicated in the file ``fi_stages_each_sign_inters.txt » included int he network folder.

- the 3rd column indicates the actuation duration of the stage (in secs)

- the 4th column indicates the cycle duration (this value however is not explicitly employed by the simulator).


b1)  ‘’File_FT_Offset_Control_Alg_Param.txt’’
The The first line of this file explains  each column.

The rest of the  lines.

2nd line indicates the master node id

3rd line indicates a sequence of (node id, value offset).

All other lines:

1st column: node id 

- the second column indicates the stage id. A strictly positive number if the stage is not red clearance, 0 otherwise.
Stages are indicated in the file ``fi_stages_each_sign_inters.txt » included int he network folder.

- the 3rd column indicates the actuation duration of the stage (in secs)

- the 4th column indicates the cycle duration (this value however is not explicitly employed by the simulator).



c1) File_MP_Control_Alg_Param_res.txt

The first line is comments

For all other lines: 

1st column: node id
2nd column : stage actuation duration
3rd column: duration of red clearance
 
All the other columns of the same line should be a sequence of (2nd column, 3rd column). 

c2) `File_MP_Qvalues_phases.txt »

First line should be a comment

next lines:

1st column:  id input link forming the phase
2nd column:  id ioutput link forming the phase
3rd column; Q(l,m) value


d1) ``File_MP_without_rc_Control_Alg_Param.txt’’

1st line s comments
Next lines:

1st column=id node
2nd column : control actuation duration

d2) NOT  YET





e1) ``File_MP_Practical_Control_Alg_Param.txt’’ 


1st line s comments
Next lines:

1st column: id node
2nd column stage actuation duration
3rd column: duration red clearance
4th column: parameter value for switching

e2) Not yet


f1) ``File_FA_with_red_clear_Control_Alg_Param.txt »
1st line s comments
Next lines:


1st column: id node
2nd column: max admissible queue size
3rd column: red clearance duration
4th column t start first control


g1) "File_FA_no_red_clear_Control_Alg_Param.txt"

1st line s comments
Next lines:
 
1st column: id node
2nd column: max admissible queue size
3rd column t start first control

h1) "File_FA_MAX_GREEN_Control_Alg_Param.txt"

1st line s comments
Next lines:
1st column: id node
2nd column: max admissible queue size
3rd column: red clearance duration
4th column t start first control
5th column: max green duration

3) Execute file SImulation.py

On a terminal or something equivalent (depending upon the operating system of the computer) you  move into folder  cc
 (e.g.. if you have named the simulation folder sim and you place it on the desktop , with the cd command you type

i) cd Desktop/sim/sim_1/cc and then you type enter
SO now you are in the folder cc where the python files are and also the file Simulation.py to execute (be careful, there is another file called Cl_Simulation.py. But what you have to execute  is the one called  Simulation and not Cl_Simulation.py).
ii) type python3.x Simulation.py  or time python3.x Simulation if you wish the time consumed by  your system to run the sim. 

python3.x stands for the python version you have. 3 indicates that you  can run the « .Q » with any version of python 3.

for exemple if you have python3.4 you can type:

python3.4 Simulation.py and then enter. 

The simulation starts. 

If you run the simulator with the Dsu_1.py file as I give it to you and without modifying anything in folder Control_Param_Files, you will run a new sim of 6000 secs, for a stabilising FT control. 


————————————

When a series of one or more simulations is implemented  a folder named Series_Sim_date is created.
Inside this folders there are folders named Fres_date corresponding to each simulation you run. 
Inside each folder Fres_date there are written many files employed by the current simulation (so as you will remember or verify the sim characteristics for this run).
Amongst these files there is a file named ``file_recording_event_db.txt »  with the recordings of the simulation.
This is the file I need to explain you so as to create your own statistical analysis. 



