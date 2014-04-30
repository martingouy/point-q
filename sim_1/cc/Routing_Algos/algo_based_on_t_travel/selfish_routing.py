#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  routing.py
#  
#  Copyright 2014 Agata Grzybek <agatagrzybek@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#

# import profile
from Routing_Algos.algo_shortest_path import *
from Routing_Algos.algo_shortest_path.PQmodel_to_graph import *
from Routing_Algos.algo_shortest_path import sp_algorithms as sp
import profile

def fct_calc_queue_id(val_netw, id_veh_current_lk, id_final_destination_lk):
	graph = Graph(val_netw)
	path = sp.sp_algorithms_turn_restricted_dijkstra(graph, id_veh_current_lk, id_final_destination_lk)
	queue_id = sp.sp_algrithms_get_queue_id_from_path(path['path'])
	# print "Turn allowed {0}-{1}, cost: {2}, {3}, reduced cost: {4}, queue: {5}".format(id_veh_current_lk, id_final_destination_lk, path['cost'], "->".join(path['path']), path['cost_reduced'], queue_id)
	return queue_id


# def main():
# 	val_netw = constructNetwork()
# 	curr_link = "e"
# 	dest_link = "f"

# 	# a vehicle 	
# 	# print "Vehicle {0} goes from {1} to {2}".format(veh_id, curr_link, dest_link)
# 	# queue_id = fct_calc_queue_id(val_netw, curr_link, dest_link) 
# 	# while queue_id and queue_id != dest_link:
# 	# 	curr_link = queue_id
# 	# 	queue_id = fct_calc_queue_id(val_netw, queue_id, dest_link) 
		
# 	vehCount = 500

# 	runVehicles(0, vehCount, val_netw, curr_link, dest_link)

# 	# seconds = 100
# 	# for i in range(0, seconds):
# 	# 	runVehicles(i, vehCount, val_netw, curr_link, dest_link)

# 	return 0

# def runVehicles(second, vehCount, val_netw, curr_link, dest_link):
# 	# multiple vehicles every second
# 	for j in range(1, vehCount):
# 		# print "Second {3}. Vehicle {0} goes from {1} to {2}".format(j, curr_link, dest_link, second)
# 		queue_id = fct_calc_queue_id(val_netw, curr_link, dest_link) 
	
# if __name__ == '__main__':
#     # main()
#     profile.run('main()')

 