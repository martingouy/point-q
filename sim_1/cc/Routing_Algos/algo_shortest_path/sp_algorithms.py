#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  algorithms.py
#  
#  Copyright 2014 Agata G.

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
from operator import itemgetter
from Routing_Algos.algo_shortest_path import *
from Routing_Algos.algo_shortest_path.prioritydictionary import priorityDictionary
#from prioritydictionary import priorityDictionary
from Routing_Algos.algo_shortest_path.PQmodel_to_graph import Graph
#from PQmodel_to_graph import Graph

## @package YenKSP
# Computes K-Shortest Paths using Yen's Algorithm.
#
# Yen's algorithm computes single-source K-shortest loopless paths for a graph 
# with non-negative edge cost. The algorithm was published by Jin Y. Yen in 1971
# and implores any shortest path algorithm to find the best path, then proceeds 
# to find K-1 deviations of the best path.

## Computes K paths from a source to a sink in the supplied graph.
#
# @param graph A graph of class Graph.
# @param start The source node of the graph.
# @param sink The sink node of the graph.
# @param K The amount of paths being computed.
#
# @retval [] Array of paths, where [0] is the shortest, [1] is the next 
# shortest, and so on.
#
def sp_algorithms_ksp_yen(graph, node_start, node_end, max_k=2):
    distances, previous = sp_algorithms_dijkstra(graph, node_start)
    
    A = [{'cost': distances[node_end], 
          'path': sp_algorithms_path(previous, node_start, node_end)}]
    B = []
    
    if not A[0]['path']: return A
    
    for k in range(1, max_k):
        for i in range(0, len(A[-1]['path']) - 1):
            node_spur = A[-1]['path'][i]
            path_root = A[-1]['path'][:i+1]
            
            edges_removed = []
            for path_k in A:
                curr_path = path_k['path']
                if len(curr_path) > i and path_root == curr_path[:i+1]:
                    cost = graph.remove_edge(curr_path[i], curr_path[i+1])
                    if cost == -1:
                        continue
                    edges_removed.append([curr_path[i], curr_path[i+1], cost])
            
            path_spur = sp_algorithms_dijkstra(graph, node_spur, node_end)
            
            if path_spur['path']:
                path_total = path_root[:-1] + path_spur['path']
                dist_total = distances[node_spur] + path_spur['cost']
                potential_k = {'cost': dist_total, 'path': path_total}
            
                if not (potential_k in B):
                    B.append(potential_k)
            
            for edge in edges_removed:
                graph.add_edge(edge[0], edge[1], edge[2])
        
        if len(B):
            B = sorted(B, key=itemgetter('cost'))
            A.append(B[0])
            B.pop(0)
        else:
            break
    
    return A

## @package YenKSP
# Computes K-Shortest Paths using Yen's Algorithm.
#
# Yen's algorithm computes single-source K-shortest loopless paths for a graph 
# with non-negative edge cost. The algorithm was published by Jin Y. Yen in 1971
# and implores any shortest path algorithm to find the best path, then proceeds 
# to find K-1 deviations of the best path.

## Computes K paths from a source to a sink in the supplied graph.
#
# @param graph A graph.
# @param start The source node of the graph.
# @param sink The sink node of the graph.
# @param K The amount of paths being computed.
#
# @retval [] Array of paths, where [0] is the shortest, [1] is the next 
# shortest, and so on.
#
def sp_algorithms_ksp_yen_with_turn_restricted_dijkstra(graph, node_start, node_end, max_k=2, use_total_travel_time=False):
    distances, previous, queue = sp_algorithms_turn_restricted_dijkstra(graph, node_start, None, use_total_travel_time)
    
    A = [{'cost': distances[node_end], 
          'path': sp_algorithms_path(previous, node_start, node_end)
         }]
    B = []
    
    if not A[0]['path']: return A
    
    for k in range(1, max_k):
        for i in range(0, len(A[-1]['path']) - 1):
            node_spur = A[-1]['path'][i]
            path_root = A[-1]['path'][:i+1]
            
            edges_removed = []
            for path_k in A:
                curr_path = path_k['path']
                if len(curr_path) > i and path_root == curr_path[:i+1]:
                    if use_total_travel_time == True:
                        cost = graph.removeEdge2(curr_path[i+1])
                    else:
                        cost = graph.removeEdge(curr_path[i+1])
                    # print "removing edge {0}, of cost {1}".format(curr_path[i+1], cost)
                    if cost == -1:
                        continue
                    edges_removed.append([curr_path[i+1], cost])
            
            path_spur = sp_algorithms_turn_restricted_dijkstra(graph, node_spur, node_end, use_total_travel_time)
            
            if path_spur['path']:
                path_total = path_root[:-1] + path_spur['path']
                dist_total = distances[node_spur] + path_spur['cost']
                potential_k = {'cost': dist_total, 'path': path_total}
            
                if not (potential_k in B):
                    B.append(potential_k)
            if use_total_travel_time == True:
                for edge in edges_removed:
                    graph.addEdge2(edge[0], edge[1])
            else:
                for edge in edges_removed:
                    # print ("add edge ", edge[0], edge[1])
                    graph.addEdge(edge[0], edge[1])
        
        if len(B):
            B = sorted(B, key=itemgetter('cost'))
            A.append(B[0])
            B.pop(0)
        else:
            break
    
    return A

# def sp_algorithms_ksp_yen_with_turn_restricted_dijkstra(graph, node_start, node_end, max_k=2):
#     distances, previous, queue = sp_algorithms_turn_restricted_dijkstra(graph, node_start)
    
#     A = [{'cost': distances[node_end], 
#           'path': sp_algorithms_path(previous, node_start, node_end)
#          }]
#     B = []
    
#     if not A[0]['path']: return A
    
#     for k in range(1, max_k):
#         for i in range(0, len(A[-1]['path']) - 1):
#             node_spur = A[-1]['path'][i]
#             path_root = A[-1]['path'][:i+1]
            
#             edges_removed = []
#             for path_k in A:
#                 curr_path = path_k['path']
#                 if len(curr_path) > i and path_root == curr_path[:i+1]:
#                     cost = graph.removeEdge(curr_path[i+1])
#                     # print "removing edge {0}, of cost {1}".format(curr_path[i+1], cost)
#                     if cost == -1:
#                         continue
#                     edges_removed.append([curr_path[i+1], cost])
            
#             path_spur = sp_algorithms_turn_restricted_dijkstra(graph, node_spur, node_end)
            
#             if path_spur['path']:
#                 path_total = path_root[:-1] + path_spur['path']
#                 dist_total = distances[node_spur] + path_spur['cost']
#                 potential_k = {'cost': dist_total, 'path': path_total}
            
#                 if not (potential_k in B):
#                     B.append(potential_k)
            
#             for edge in edges_removed:
#                 graph.addEdge(edge[0], edge[1])
        
#         if len(B):
#             B = sorted(B, key=itemgetter('cost'))
#             A.append(B[0])
#             B.pop(0)
#         else:
#             break
    
#     return A

## Computes the shortest path from a source to a sink in the supplied graph.
#
# @param graph A graph.
# @param node_start The source node of the graph.
# @param node_end The sink node of the graph.
#
# @retval {} Dictionary of path and cost or if the node_end is not specified,
# the distances and previous lists are returned.
#
def sp_algorithms_dijkstra(graph, node_start, node_end=None):
    distances = {}      
    previous = {}       
    Q = priorityDictionary()
    
    for v in graph:
        distances[v] = graph.INFINITY
        previous[v] = graph.UNDEFINDED
        Q[v] = graph.INFINITY
    
    distances[node_start] = 0
    Q[node_start] = 0
    
    for v in Q:
        if v == node_end: break

        for u in graph[v]:
            cost_vu = distances[v] + graph[v][u]
            
            if cost_vu < distances[u]:
                distances[u] = cost_vu
                Q[u] = cost_vu
                previous[u] = v

    if node_end:
        return {'cost': distances[node_end], 
                'path': sp_algorithms_path(previous, node_start, node_end)}
    else:
        return (distances, previous)


## Dijkstra for graph with turn restrictions
## Computes the shortest path from a start edge to an end edge.
#
# @param network A network of a queue point model.
# @param start_link_id The origin edge of the graph.
# @param end_link_id The destination edge of the graph.
#
# @retval {} Dictionary of path and cost or if the node_end is not specified,
# the distances and previous lists are returned.
#
def sp_algorithms_turn_restricted_dijkstra(graph, start_link_id, end_link_id=None, use_total_travel_time=False):
    links = graph.getAllLinks()
    
    distances = {}      
    previous = {}       
    Q = priorityDictionary()
    
    for link_id in links.keys():
        distances[link_id] = graph.INFINITY
        previous[link_id] = graph.UNDEFINDED
        Q[link_id] = graph.INFINITY
    
    distances[start_link_id] = 0
    Q[start_link_id] = 0
    
    for v_link_id in Q:
        if v_link_id == end_link_id: break
        v_link = graph.getLink(v_link_id)
        queues_out = graph.getOutAllowedEdges(v_link)
        for u_link_id in queues_out:
            u_link = graph.getLink(u_link_id)
            if use_total_travel_time == True:
                cost_vu = graph.getLinkCost2(u_link)
            else:
                cost_vu = graph.getLinkCost(u_link)
            cost_vu = distances[v_link_id] + cost_vu
            if cost_vu < distances[u_link_id]:
                distances[u_link_id] = cost_vu
                Q[u_link_id] = cost_vu
                previous[u_link_id] = v_link_id
            # print "queues out from {0}: {1}, cost: {2}, {3}:{4}".format(v_link_id, u_link_id, cost_vu, u_link_id,distances[u_link_id])
            
    if end_link_id:
        # path = sp_algorithms_path_in_nodes(graph, previous, start_link_id, end_link_id)
        start_link = graph.getLink(start_link_id)
        return {'cost': distances[end_link_id], 
                # 'cost_reduced': distances[end_link_id] - graph.getLinkCost(start_link),
                'path': sp_algorithms_path(previous, start_link_id, end_link_id),
                # 'path': path['route'],
                # 'path_node': path['route_node'],
                # 'queue': sp_algrithms_get_queue_id_from_path(path['route']) 
                }
    else:
        return (distances, previous, sp_algrithms_get_queue_id_from_path)

# def sp_algorithms_turn_restricted_dijkstra(graph, start_link_id, end_link_id=None):
#     links = graph.getAllLinks()
    
#     distances = {}      
#     previous = {}       
#     Q = priorityDictionary()
    
#     for link_id in links.keys():
#         distances[link_id] = graph.INFINITY
#         previous[link_id] = graph.UNDEFINDED
#         Q[link_id] = graph.INFINITY
    
#     distances[start_link_id] = 0
#     Q[start_link_id] = 0
    
#     for v_link_id in Q:
#         if v_link_id == end_link_id: break
#         v_link = graph.getLink(v_link_id)
#         queues_out = graph.getOutAllowedEdges(v_link)
#         for u_link_id in queues_out:
#             u_link = graph.getLink(u_link_id)
#             cost_vu = graph.getLinkCost(u_link)
#             # print "queues out from {0}: {1}, cost: {2}".format(v_link_id, u_link_id, cost_vu)
#             cost_vu = distances[v_link_id] + cost_vu
#             if cost_vu < distances[u_link_id]:
#                 distances[u_link_id] = cost_vu
#                 Q[u_link_id] = cost_vu
#                 previous[u_link_id] = v_link_id

#     if end_link_id:
#         # path = sp_algorithms_path_in_nodes(graph, previous, start_link_id, end_link_id)
#         start_link = graph.getLink(start_link_id)
#         return {'cost': distances[end_link_id], 
#                 'cost_reduced': distances[end_link_id] - graph.getLinkCost(start_link),
#                 'path': sp_algorithms_path(previous, start_link_id, end_link_id),
#                 # 'path': path['route'],
#                 # 'path_node': path['route_node'],
#                 # 'queue': sp_algrithms_get_queue_id_from_path(path['route']) 
#                 }
#     else:
#         return (distances, previous, sp_algrithms_get_queue_id_from_path)

def sp_algrithms_get_queue_id_from_path(route):
    if len(route) > 1:
        return route[1]
    return None

## Finds a paths from a source to a sink using a supplied previous node list.
#
# @param previous A list of node predecessors.
# @param node_start The source node of the graph.
# @param node_end The sink node of the graph.
#
# @retval [] Array of nodes if a path is found, an empty list if no path is 
# found from the source to sink.
#
def sp_algorithms_path(previous, node_start, node_end):
    route = []

    node_curr = node_end    
    while True:
        route.append(node_curr)
        if previous[node_curr] == node_start:
            route.append(node_start)
            break
        elif previous[node_curr] == Graph.UNDEFINDED:
            return []
        
        node_curr = previous[node_curr]
    
    route.reverse()
    return route

## Finds a paths from a source to a sink using a supplied previous node list.
#
# @param previous A list of node predecessors.
# @param node_start The source node of the graph.
# @param node_end The sink node of the graph.
#
# @retval [] Array of nodes if a path is found, an empty list if no path is 
# found from the source to sink.
#
def sp_algorithms_path_in_nodes(graph, previous, node_start, node_end):
    route = []
    routeNode = []
    node_curr = node_end    
    while True:
        # if node_curr != node_end:
        route.append(node_curr)
        tailNodeId = graph.getTailNodeFromLinkID(node_curr)
        if tailNodeId != -1:
            routeNode.append(tailNodeId)
        if previous[node_curr] == node_start:
            route.append(node_start)
            break
        elif previous[node_curr] == graph.UNDEFINDED:
            return {"route":[], "route_node":[]}
        node_curr = previous[node_curr]
    route.reverse()
    routeNode.reverse()
    return {"route":route, "route_node":routeNode}
