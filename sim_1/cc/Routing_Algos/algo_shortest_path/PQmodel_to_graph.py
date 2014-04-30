#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  network.py
#
#  Copyright 2014 Agata G.
#
#  Mapper a point queue model to a graph
#
#
import os
import random
from Routing_Algos.algo_shortest_path import *
from Routing_Algos.algo_shortest_path.network_mock import *
#from network_mock import *

class Graph:
     ## An edge with this cost signifies that it has been removed from the graph.
    # This value implies that any edge in the graph must be very small in 
    # comparison.
    INFINITY = 10000
    
    ## Represents a NULL predecessor.
    UNDEFINDED = None

    def __init__(self, network):
        self._network = network

    def getTailNode(self, link):
        node_id = link.get_id_tail_intersection_node()
        return node_id

    def getTailNodeFromLinkID(self, link_id):
        node_id = None
        if link_id in self._network.get_di_all_links().keys():
            link = self._network.get_di_all_links()[link_id]
            node_id = link.get_id_tail_intersection_node()
        return node_id

    def getHeadNode(self, link):
        node_id = link.get_id_tail_intersection_node()
        return node_id

    def getAllLinks(self):
        return self._network.get_di_all_links()

    def getAllNodes(self):
        return self._network.get_di_intersections()

    def getLink(self, link_id):
        link = self.UNDEFINDED
        if link_id in self._network.get_di_all_links().keys():
            link = self._network.get_di_all_links()[link_id]
        return link

    def getOutAllowedEdges(self, link):
        links = link.get_li_output_links_queues()
        if links == self.UNDEFINDED:
            links = []
        return links

    def getPathCapacity(self, link_ids):
        minCapacity = self.INFINITY
        for link_id in link_ids:
            link = self.getLink(link_id)
            if link == self.UNDEFINDED:
                return self.UNDEFINDED
            capacity = self.getLinkCapacity(link)
            if capacity > 0 and capacity < minCapacity:
                minCapacity = capacity
        return minCapacity

    def getLinkCapacity(self, link):
        capacity = link.get_capacity_link()
        return capacity

    def getLinkCost(self, link):
        toQueueCost = link.get_param_link_travel_duration_dyn_split_ratios()
        if toQueueCost == self.INFINITY:
            return self.INFINITY
        defaultCost = link.get_param_link_travel_duration()
        capacity = self.getLinkCapacity(link)
        if toQueueCost == None or capacity == 0:
            toQueueCost = 0
        if defaultCost == None or capacity == 0:
            defaultCost = 0
        cost =  defaultCost + (defaultCost - toQueueCost)
        if toQueueCost > defaultCost or cost == self.UNDEFINDED:
            cost = 0
        # print("cost", cost, "toQueueCost", toQueueCost, "defaultCost", defaultCost)
        return cost

    def getLinkCost2(self, link):
        cost = link.get_param_link_travel_duration_dyn_split_ratios()
        capacity = self.getLinkCapacity(link)
        if capacity == 0:
            cost = 0
        return cost

    # def getLinkCostFromLinkID(self, link_id):
    #     cost = 0
    #     if link_id in self._network.get_di_all_links().keys():
    #         link = self._network.get_di_all_links()[link_id]
    #         cost = self.getLinkCost2(link)
    #         if cost == self.UNDEFINDED:
    #             cost = 0
    #     return cost

    def getOutAllowedEdgesFromLinkId(self, link_id):
        link = self.getLink(link_id)
        if link == self.UNDEFINDED:
            return self.UNDEFINDED
        links = link.get_li_output_links_queues()
        if links == self.UNDEFINDED:
            links = []
        return links

    def setLinkCost(self, link_id, newCost):
        link = self.getLink(link_id)
        if link == self.UNDEFINDED:
            return self.UNDEFINDED
        oldCost = link.get_param_link_travel_duration_dyn_split_ratios()
        link.set_param_link_travel_duration_dyn_split_ratios(newCost)
        return oldCost

    def setLinkCost2(self, link_id, newCost):
        link = self.getLink(link_id)
        if link == self.UNDEFINDED:
            return self.UNDEFINDED
        oldCost = link.get_param_link_travel_duration_dyn_split_ratios()
        link.set_param_link_travel_duration_dyn_split_ratios(newCost)
        return oldCost

    ## Removes an edge from the graph.
    #
    # @param self The object pointer.
    # @param node_from The node that the edge starts at.
    # @param node_to The node that the edge terminates at.
    # @param cost The cost of the edge, if the cost is not specified all edges
    # between the nodes are removed.
    # @retval int The cost of the edge that was removed. If the nodes of the 
    # edge does not exist, or the cost of the edge was found to be infinity, or 
    # if the specified edge does not exist, then -1 is returned.
    #
    def removeEdge(self, link_id):
        cost = self.setLinkCost(link_id, self.INFINITY)
        if cost == None:
            cost = 0
        return cost
        
    def removeEdge2(self, link_id):
        cost = self.setLinkCost2(link_id, self.INFINITY)
        if cost == None:
            cost = 0
        return cost

    ## Adds a edge to the graph.
    #
    # @post The two nodes specified exist within the graph and their exist an
    # edge between them of the specified value.
    #
    # @param self The object pointer.
    # @param node_from The node that the edge starts at.
    # @param node_to The node that the edge terminates at.
    # @param cost The cost of the edge, if the cost is not specified a random
    # cost is generated from 1 to 10.
    #
    def addEdge(self, link_id, cost=None):
        if not cost:
            cost = 0
        if self.setLinkCost(link_id, cost) == cost:                
            return cost
        else:
            return self.UNDEFINDED

    def addEdge2(self, link_id, cost=None):
        if not cost:
            cost = 0
        if self.setLinkCost2(link_id, cost) == cost:                
            return cost
        else:
            return self.UNDEFINDED

    def printLinks(self):
        for linkId in self.getAllLinks():
            link = self.getLink(linkId)
            print (linkId, "cost with queue", self.getLinkCost(link), "total cost", self.getLinkCost2(link), self.getOutAllowedEdgesFromLinkId(linkId))


