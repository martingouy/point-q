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
from Routing_Algos.algo_shortest_path import sp_algorithms as sp
from Routing_Algos.algo_shortest_path.PQmodel_to_graph import Graph
from Routing_Algos.algo_shortest_path.network_mock import *
from bisect import bisect
from random import random

def fct_calc_queue_id(val_netw, id_veh_current_lk, id_final_destination_lk):
	graph = Graph(val_netw)
	k = 2
	paths = sp.sp_algorithms_ksp_yen_with_turn_restricted_dijkstra(graph, id_veh_current_lk, id_final_destination_lk, k, False)
	# print "Found {0} shortest paths:".format(len(paths))
	# for path in paths:
		# print "shortest path: {0}-{1}, cost: {2}, {3}, {4}, reduced cost: {5}, queue: {6}".format(self.sourceEdge, self.destinationEdge, path['cost'], "->".join(path['path']), "->".join(path['path_node']), path['cost_reduced'], path['queue'])
		# print "shortest path: {0}-{1}, cost: {2}, {3}".format(id_veh_current_lk, id_final_destination_lk, path['cost'], "->".join(path['path']))
		# todo reduce cost 
	path_index = choose_path_with_inverse_probability_to_travel_times_on_paths_with_capacity(graph, paths)
	queue_id = sp.sp_algrithms_get_queue_id_from_path(paths[path_index]['path'])
	# print "Selected route {0}, queue {1}".format(path_index, queue_id)
	return queue_id

def choose_path_with_inverse_probability_to_travel_times_on_paths_with_capacity(graph, paths):
	if len(paths) == 0:
		return None
	if len(paths) == 1:
		return 0
	
	# calculate capacity weight
	sumCapacityWeight = 0
	for path in paths:
		path['capacity'] = graph.getPathCapacity(path['path'])
		sumCapacityWeight += path['capacity']
	# print("paths", paths)
	for path in paths:
		path['capacityWeight'] = float(path['capacity'])/sumCapacityWeight
	# print "path capacities {0}".format(paths)

	# calculate inverse weights and sum weighs
	sumWeight = 0
	weights = []
	for path in paths:
		if path['cost'] == 0:
			weight = path['capacityWeight']
		else:
			weight = (float(1) / float(path['cost'])) * path['capacityWeight']
		weights.append(weight)
		sumWeight += weight
	# calculate probabilities (inversed)
	probabilities = []
	i = 0
	for weight in weights:
		probabilities.append(weight / sumWeight)
		i += 1
	index = get_index(probabilities)
	# print probabilities
	# test_index(probabilities)
	return index

def choose_path_with_inverse_probability_to_travel_times_on_paths(paths):
	# calculate inverse weights and sum weight
	sumWeight = 0
	weights = []
	for path in paths:
		weight = float(1) / float(path['cost'])
		weights.append(weight)
		sumWeight += weight
	# calculate probabilities (inversed)
	probabilities = []
	i = 0
	for weight in weights:
		probabilities.append(weight / sumWeight)
		i += 1
	index = get_index(probabilities)
	# test_index(probabilities)
	return index

def test_index(probabilities):
	indexes = {}
	print("probabilities", probabilities)
	for i in range(0,10000):
		index = get_index(probabilities)
		if index not in indexes:
			indexes[index] = 0
		indexes[index] += 1
	print("indexes {0}",format(indexes))

def get_index(probabilities):
	if not probabilities or len(probabilities) < 1:
		return -1
	# build cdf
	cdf = [probabilities[0]]
	for i in range(1, len(probabilities)):
	    cdf.append(cdf[-1] + probabilities[i])
	# find index
	index = bisect(cdf,random())
	return index

# def main():
# 	val_netw = constructNetwork()
# 	curr_link = "e"
# 	dest_link = "f"

# 	print("Vehicle goes from {0} to {1}",format(curr_link, dest_link))
# 	queue_id = fct_calc_queue_id(val_netw, curr_link, dest_link) 
# 	while queue_id and queue_id != dest_link:
# 		curr_link = queue_id
# 		queue_id = fct_calc_queue_id(val_netw, curr_link, dest_link) 
		
# 	return 0

# if __name__ == '__main__':
#     main()
    # profile.run('main()')

 