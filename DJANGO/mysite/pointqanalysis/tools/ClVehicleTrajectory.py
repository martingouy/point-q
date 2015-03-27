import sqlite3

class VehicleTrajectory:

    def __init__(self, network, veh_id, simu_id):


        ## VEH HISTORY ##
        # we query the sql database to recover the vehicle history
        conn = sqlite3.connect('pointq_db.sqlite3')
        c = conn.cursor()

        query = 'SELECT ev_time, c_loc_link, t_arrival_c_link, t_start_departure, t_leave, t_arrival_queue FROM ' + simu_id + ' WHERE veh_id = ' + veh_id

        c.execute(query)
        self.veh_history = c.fetchall()
        conn.close()

        ## NETWORK ##
        self.network = network

        ## LIST LINKS ##
        self.list_links = self.links_trajectory()

        ## DIC TEMPORAL HISTORY ##
        self.time_exit_network = 0
        self.time_entry_network = 0
        self.dic_temporal_history = self.temporal_history()


    def links_trajectory(self):

        list_links = []

        for row in self.veh_history:
            link = row[1];

            if not link in list_links:
                list_links.append(link)

        return list_links

    def temporal_history(self):

        array_light = []

        for i, row in enumerate(self.veh_history):

            link = row[1]
            t_arrival_c_link = row[2]
            t_start_departure = row[3]
            t_leave = row[4]
            t_arrival_queue = row[5]

            if i == 0:
                self.time_entry_network = t_arrival_c_link
            self.time_exit_network = t_arrival_c_link

            if t_start_departure == -1:
                array_light.append({"link": link, "t_arrival_c_link": t_arrival_c_link})

            else:
                # we want to determine which is the next link
                index_link = self.list_links.index(link)
                dic_temp_link = array_light[index_link - 1]
                dic_temp_link["t_arrival_queue"] = t_arrival_queue
                dic_temp_link["t_start_departure"] = t_start_departure
                dic_temp_link["t_leave"] = t_leave    

        # We add the exit link
        exit_link = self.veh_history[-1][1]
        array_light.append({"link": exit_link})

        return array_light

