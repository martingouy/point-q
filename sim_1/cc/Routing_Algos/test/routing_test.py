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
#  MA 02110-1self.shortestCost01, USA.
#
#

import profile
import unittest
import json

# from shortest_path import sp_algorithms as sp
# from shortest_path.PQmodel_to_graph import Graph
# from shortest_path.network_mock import *


from operator import itemgetter
from Routing_Algos.algo_shortest_path import *
from Routing_Algos.algo_shortest_path.prioritydictionary import priorityDictionary
#from prioritydictionary import priorityDictionary
from Routing_Algos.algo_shortest_path.PQmodel_to_graph import Graph

class TestTurnRestrictedDijkstraFunctions(unittest.TestCase):
    
    def setUp(self):
        self.network = constructNetwork()
        self.graph = Graph(self.network)
        self.sourceEdge = "e"
        self.destinationEdge = "f"
        self.sourceNode = "A"
        self.destinationNode = "C"
        self.shortestCost = 3


    def testGraphConstructionLinkCollections(self):
        for elem in self.network.get_di_all_links():
            self.assert_(elem in self.graph.getAllLinks())

    def testGraphConstructionNodeCollections(self):
        for elem in self.network.get_di_intersections():
            self.assert_(elem in self.graph.getAllNodes())

    def resetGraphCost(self):
        self.graph.setLinkCost('a', 1)
        self.graph.setLinkCost('b', 1)
        self.graph.setLinkCost('c', 1)
        self.graph.setLinkCost('d', 1)
        self.graph.setLinkCost('e', 1)
        self.graph.setLinkCost('f', 1)
        self.graph.setLinkCost('g', 1)
        self.graph.setLinkCost('h', 1)
        self.graph.setLinkCost('j', 1)
        self.graph.setLinkCost('k', 1)

    def testUpdateGraph(self):
        self.resetGraphCost()
        val = self.shortestCost
        self.graph.setLinkCost('a', val)
        link = self.graph.getLink('a')
        self.assertEqual(self.graph.getLinkCost(link), val)

        self.graph.setLinkCost('b', val)
        self.assertEqual(self.graph.getLinkCostFromLinkID('b'), val)

    # def testOrygDijkstra(self):
    #     self.resetGraphCost()
    #     path = sp.sp_algorithms_dijkstra(self.diGraph, self.sourceNode, self.destinationNode)
    #     print "DSP {0}-{1}, cost: {2}, {3}".format(self.sourceNode, self.destinationNode, path['cost'], "->".join(path['path']))
    #     self.assertEqual(path['cost'], 6)

    def testTRDijkstraFindsShortestEdgesEF(self):
        # equal routes
        self.resetGraphCost()
        path = sp.sp_algorithms_turn_restricted_dijkstra(self.graph, self.sourceEdge, self.destinationEdge)
        queue_id = sp.sp_algrithms_get_queue_id_from_path(path['path'])
        print "TRDSP {0}-{1}, cost: {2}, path: {3}, queue: {4}".format(self.sourceEdge, self.destinationEdge, path['cost'], "->".join(path['path']), queue_id)
        self.assertEqual(path['cost'], self.shortestCost)
        self.assertEqual(path['cost_reduced'], self.shortestCost-1)
        self.assertEqual(path['path'], ['e', 'a','b', 'f'])
        # self.assertEqual(path['path_node'], ['A','B','C'])
        self.assertEqual(queue_id, 'a')

        # set one edge more costly - should return the upper route
        self.graph.setLinkCost('a', 3)
        path = sp.sp_algorithms_turn_restricted_dijkstra(self.graph, self.sourceEdge, self.destinationEdge)
        queue_id = sp.sp_algrithms_get_queue_id_from_path(path['path'])
        print "TRDSP {0}-{1}, cost: {2}, path: {3}, queue: {4}".format(self.sourceEdge, self.destinationEdge, path['cost'], "->".join(path['path']), queue_id)
        self.assertEqual(path['cost'], self.shortestCost)
        self.assertEqual(path['path'], ['e', 'c','d', 'f'])
        self.assertEqual(queue_id, 'c')

        # set another edge more costly - returns again the first result edge
        self.resetGraphCost()
        self.graph.setLinkCost('c', 3)
        path = sp.sp_algorithms_turn_restricted_dijkstra(self.graph, 'd', self.destinationEdge)
        queue_id = sp.sp_algrithms_get_queue_id_from_path(path['path'])
        print "TRDSP {0}-{1}, cost: {2}, path: {3}, queue: {4}".format('d', self.destinationEdge, path['cost'], "->".join(path['path']), queue_id)
        self.assertEqual(path['cost'], 1)
        self.assertEqual(path['path'], ['d', 'f'])
        self.assertEqual(queue_id, 'f')

        # set edge-edge with the result of length 1
        self.resetGraphCost()
        path = sp.sp_algorithms_turn_restricted_dijkstra(self.graph, 'c', 'd')
        queue_id = sp.sp_algrithms_get_queue_id_from_path(path['path'])
        print "TRDSP {0}-{1}, cost: {2}, path: {3}, queue: {4}".format('c', 'd', path['cost'], "->".join(path['path']), queue_id)
        self.assertEqual(path['cost'], 1)
        self.assertEqual(path['path'], ['c', 'd'])
        self.assertEqual(queue_id, 'd')

    # # todo what should return? cost 0 ans empty path?
    def testTRDijkstraFindsShortestEdges1Len(self):
        self.resetGraphCost()
        path = sp.sp_algorithms_turn_restricted_dijkstra(self.graph, self.sourceEdge, self.destinationEdge)
        queue_id = sp.sp_algrithms_get_queue_id_from_path(path['path'])
        print "TRDSP {0}-{1}, cost: {2}, path: {3}, queue: {4}".format(self.sourceEdge, self.destinationEdge, path['cost'], "->".join(path['path']), queue_id)
        self.assertEqual(path['cost'], self.shortestCost)
        self.assertEqual(path['path'], ['e', 'a','b', 'f'])


    def testTRDijkstraSourceSource(self):
        self.resetGraphCost()
        # enter link
        path = sp.sp_algorithms_turn_restricted_dijkstra(self.graph, self.sourceEdge, self.sourceEdge)
        queue_id = sp.sp_algrithms_get_queue_id_from_path(path['path'])
        print "TRDSP {0}-{1}, cost: {2}, path: {3}, queue: {4}".format(self.sourceEdge, self.sourceEdge, path['cost'], "->".join(path['path']), queue_id)
        self.assertEqual(path['cost'], 0)
        self.assertEqual(path['path'], [])

        # exit link
        path = sp.sp_algorithms_turn_restricted_dijkstra(self.graph, self.destinationEdge, self.destinationEdge)
        queue_id = sp.sp_algrithms_get_queue_id_from_path(path['path'])
        print "TRDSP {0}-{1}, cost: {2}, path: {3}, queue: {4}".format(self.destinationEdge, self.destinationEdge, path['cost'], "->".join(path['path']), queue_id)
        self.assertEqual(path['cost'], 0)
        self.assertEqual(path['path'], [])
        # middle link
        path = sp.sp_algorithms_turn_restricted_dijkstra(self.graph, 'c', 'c')
        queue_id = sp.sp_algrithms_get_queue_id_from_path(path['path'])
        print "TRDSP {0}-{1}, cost: {2}, path: {3}, queue: {4}".format('c', 'd', path['cost'], "->".join(path['path']), queue_id)
        self.assertEqual(path['cost'], 0)
        self.assertEqual(path['path'], [])
        

    def testTRDijkstraNoPath(self):
        self.resetGraphCost()
        # because of direction
        path = sp.sp_algorithms_turn_restricted_dijkstra(self.graph, "b", "a")
        queue_id = sp.sp_algrithms_get_queue_id_from_path(path['path'])
        print "No path {0}-{1}, cost: {2}, path: {3}, queue: {4}".format("b", "a", path['cost'], "->".join(path['path']), queue_id)
        self.assertEqual(path['cost'], self.graph.INFINITY)
        self.assertEqual(path['path'], [])
        # from an exit link
        path = sp.sp_algorithms_turn_restricted_dijkstra(self.graph, "f", "b")
        queue_id = sp.sp_algrithms_get_queue_id_from_path(path['path'])
        print "No path {0}-{1}, cost: {2}, path: {3}, queue: {4}".format("f", "b", path['cost'], "->".join(path['path']), queue_id)
        self.assertEqual(path['cost'], self.graph.INFINITY)
        self.assertEqual(path['path'], [])
       
        # because of infinity
        self.graph.setLinkCost('a', self.graph.INFINITY)
        self.graph.setLinkCost('b', 1)
        self.graph.setLinkCost('c', self.graph.INFINITY)
        self.graph.setLinkCost('d', 1)
        path = sp.sp_algorithms_turn_restricted_dijkstra(self.graph, self.sourceEdge, self.destinationEdge)
        queue_id = sp.sp_algrithms_get_queue_id_from_path(path['path'])
        print "No path {0}-{1}, cost: {2}, path: {3}, queue: {4}".format(self.sourceEdge, self.destinationEdge, path['cost'], "->".join(path['path']), queue_id)
        self.assertEqual(path['cost'], self.graph.INFINITY)
        # self.assertEqual(path['path'], [])
        # self.assertEqual(path['path_node'], [])
        self.assertEqual(queue_id, None)
    
    def testTRDijkstraNoTurnEdgesEF(self):

        self.resetGraphCost()
        self.graph.setLinkCost('b', 10)
        self.graph.setLinkCost('c', 20)
        # impose high cost on b so diskjtra would choose a-g-d,with cost 4 but the turn is not allowed, so take the longer allowed routr
        path = sp.sp_algorithms_turn_restricted_dijkstra(self.graph, self.sourceEdge, self.destinationEdge)
        queue_id = sp.sp_algrithms_get_queue_id_from_path(path['path'])
        print "Turn not allowed {0}-{1}, cost: {2}, path: {3}, queue: {4}".format(self.sourceEdge, self.destinationEdge, path['cost'], "->".join(path['path']), queue_id)
        self.assertEqual(path['cost'], self.shortestCost + 9)
        self.assertEqual(path['path'], ['e', 'a','b', 'f'])
        self.assert_(True)

    def testTRDijkstraTurnEdgesEF(self):
        self.resetGraphCost()
        self.graph.setLinkCost('d', 20)
        # self.graph.printLinks()
        
        # impose high cost on a and d so diskjtra would choose c-h-b, the turn is not allowed, so this is the correct result
        path = sp.sp_algorithms_turn_restricted_dijkstra(self.graph, 'k', self.destinationEdge)
        queue_id = sp.sp_algrithms_get_queue_id_from_path(path['path'])
        print "Turn allowed {0}-{1}, cost: {2}, path: {3}, queue: {4}".format('k', self.destinationEdge, path['cost'], "->".join(path['path']), queue_id)
        self.assertEqual(path['cost'], self.shortestCost + 2)
        self.assertEqual(path['path'], ['k', 'g', 'j', 'a', 'b', 'f'])
        self.assert_(True)

    def testTRDijkstraTurnEdgesEFJennie(self):
        self.resetGraphCost()
        self.graph.printLinks()
        
        # impose high cost on a and d so diskjtra would choose c-h-b, the turn is not allowed, so this is the correct result
        path = sp.sp_algorithms_turn_restricted_dijkstra(self.graph, 'e', 'l')
        queue_id = sp.sp_algrithms_get_queue_id_from_path(path['path'])
        print "Turn allowed {0}-{1}, cost: {2}, path: {3}, queue: {4}".format('e', 'l', path['cost'], "->".join(path['path']), queue_id)
        self.assertEqual(path['cost'], self.shortestCost+1)
        self.assertEqual(path['path'], ['e', 'a', 'g', 'j', 'l'])
        # self.assert_(True)

    # def testCalculateKShortestPathDijkstra(self):
    #     k = 5
    #     paths = sp.sp_algorithms_ksp_yen(self.diGraph, self.sourceNode, self.destinationNode, k)
    #     for path in paths:
    #         print "path {0}".format(path['path'])
    #     return paths

    def testKShortestPathRestricted(self):
        k = 5
        paths = sp.sp_algorithms_ksp_yen_with_turn_restricted_dijkstra(self.graph, self.sourceEdge, self.destinationEdge, k)
        print "Found {0} shortest paths:".format(len(paths))
        for path in paths:
            queue_id = sp.sp_algrithms_get_queue_id_from_path(path['path'])
            # print "shortest path: {0}-{1}, cost: {2}, path: {3}, queue: {4}".format(self.sourceEdge, self.destinationEdge, path['cost'], "->".join(path['path']), queue_id)
            print "shortest path: {0}-{1}, cost: {2}, {3}".format(self.sourceEdge, self.destinationEdge, path['cost'], "->".join(path['path']))
        
        paths = sp.sp_algorithms_ksp_yen_with_turn_restricted_dijkstra(self.graph, 'c', self.destinationEdge, k)
        print "Found {0} shortest paths:".format(len(paths))
        for path in paths:
            queue_id = sp.sp_algrithms_get_queue_id_from_path(path['path'])
            # print "shortest path: {0}-{1}, cost: {2}, path: {3}, queue: {4}".format(self.sourceEdge, self.destinationEdge, path['cost'], "->".join(path['path']), queue_id)
            print "shortest path: {0}-{1}, cost: {2}, {3}".format('c', self.destinationEdge, path['cost'], "->".join(path['path']))
        
        paths = sp.sp_algorithms_ksp_yen_with_turn_restricted_dijkstra(self.graph, 'd', self.destinationEdge, k)
        print "Found {0} shortest paths:".format(len(paths))
        for path in paths:
            # print "shortest path: {0}-{1}, cost: {2}, path: {3}, queue: {4}".format(self.sourceEdge, self.destinationEdge, path['cost'], "->".join(path['path']), queue_id)
            print "shortest path: {0}-{1}, cost: {2}, {3}".format('d', self.destinationEdge, path['cost'], "->".join(path['path']))
              

if __name__ == '__main__':
    unittest.main()
    # profile.run('main()')          

