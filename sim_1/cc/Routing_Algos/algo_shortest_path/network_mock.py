class Network_Link:
    def __init__(self, tail_node, head_node, cost, queues):
        self._id_head_intersection_node=head_node
        self._id_tail_intersection_node=tail_node
        self._queues = queues
        self.param_link_travel_duration_dyn_split_ratios = cost
    def get_id_head_intersection_node(self):
        return self._id_head_intersection_node
    def get_id_tail_intersection_node(self):
        return self._id_tail_intersection_node
    def get_li_output_links_queues(self):
        return self._queues
    def get_param_link_travel_duration_dyn_split_ratios(self):
        return self.param_link_travel_duration_dyn_split_ratios
    def set_param_link_travel_duration_dyn_split_ratios(self, cost):
        self.param_link_travel_duration_dyn_split_ratios = cost

class Intersection:
    def __init__(self, val_li_id_input_network_links_to_inters_node, val_li_id_output_network_links_from_inters_node):
        self._li_id_input_network_links_to_inters_node=val_li_id_input_network_links_to_inters_node
        self._li_id_output_network_links_from_inters_node=val_li_id_output_network_links_from_inters_node
    def get_li_id_input_network_links_to_inters_node(self):
        return self._li_id_input_network_links_to_inters_node
    def get_li_id_output_network_links_from_inters_node(self):
        return self._li_id_output_network_links_from_inters_node

class Network:
    def __init__(self, val_di_intersections, links, entry_links, exit_links):
        self._di_intersections=dict(val_di_intersections)
        self._di_internal_links_to_network=dict(links)
        self._di_entry_links_to_network = dict(entry_links)
        self._di_exit_links_from_network = dict(exit_links)
        self.di_all_links = dict(links.items() + entry_links.items() + exit_links.items())
    def get_di_intersections(self):
        return self._di_intersections
    def get_di_internal_links_to_network(self):
        return self._di_internal_links_to_network
    def get_di_entry_links_to_network(self):
        return self._di_entry_links_to_network
    def get_di_exit_links_from_network(self):
        return self._di_exit_links_from_network
    def get_di_all_links(self):
        return self.di_all_links

def constructNetwork():
    e = Network_Link(-1, "A", 1, list(["c","a"]))
    a = Network_Link("A", "B", 1, list(["b", "g"]))
    c = Network_Link("A", "D", 1, list(["h", "d"]))
    g = Network_Link("B", "D", 1, list(["j"]))
    h = Network_Link("D", "B", 1, list(["b"]))
    b = Network_Link("B", "C", 1, list(["f"]))
    d = Network_Link("D", "C", 1, list(["f"]))
    f = Network_Link("C", "-1", 1, list([]))
    j = Network_Link("D", "A", 1, list(['a', 'l']))
    k = Network_Link("C", "B", 1, list(['g']))
    l = Network_Link("A", "-1", 1, list([]))
    internal_links = {
        "a" : a,
        "b" : b,
        "c" : c,
        "d" : d,
        "g" : g,
        "h": h,
        "j": j,
        "k": k,
        "l": l
    }
    intersections = {
        "A": Intersection(["e"],["a","c"]),
        "B": Intersection(["a", "h"],["g","b"]),
        "C": Intersection(["b", "d"],["f"]),        
        "D": Intersection(["c", "g"],["h", "d"]),
    } 
    network = Network(intersections, internal_links, {"e":e}, {"f":f})
    return network


