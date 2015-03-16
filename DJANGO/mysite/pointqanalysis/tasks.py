from __future__ import absolute_import
from celery import shared_task
import sqlite3
import json
import os
from django.conf import settings
from tools import tools_sql
from tools.ClVehicleTrajectory import VehicleTrajectory

@shared_task
def birdeye(network, simu):
	# global variables
	internal_links = []
	history_network = {}
	length_internal_links = {}
	time_step = 5

	# First step: Create a list of internal links
	conn = sqlite3.connect(os.path.join(settings.BASE_DIR, 'network_db.sqlite3'))

	c = conn.cursor()
	c.execute('SELECT topjson FROM "index_network" WHERE name = \''+ network +'\'')
	topjson = json.loads(c.fetchone()[0])
	conn.close()

	## We parse the json to determine internal links

	for link in topjson["LinkList"]:
		# !!!! Currently wrong , we have to add inputs into topjson
		if link["outputs"] != "[-1]":
			internal_links.append(link["link_id"])

	length_internal_links = tools_sql.length_links([int(x) for x in internal_links], network)

	# Second step: We analyse each link
	conn = sqlite3.connect(os.path.join(settings.BASE_DIR, 'pointq_db.sqlite3'))
	c = conn.cursor()

	def add_2_history(time, link, nb_veh):
		if not str(time) in history_network.keys():
			history_network[str(time)] = {}

		history_network[str(time)][str(link)] = nb_veh

	for link in internal_links:
		query = "SELECT ev_time, ev_type, c_loc_link FROM "+ simu +" WHERE c_loc_link = " + link
		c.execute(query)

		history_link = c.fetchall()
		time_cursor = 0
		nb_veh_link = 0
		history_time_step = []

		for event in history_link:
			ev_time = event[0]
			ev_type = event[1]
			c_loc_link = event[2]

			if ev_time >= time_cursor + time_step:
				while ev_time >= time_cursor + time_step:

					if len(history_time_step) == 0:
						mean = nb_veh_link
					else:
						mean = sum(history_time_step)/len(history_time_step)

					length_c_loc_link = float(length_internal_links[str(c_loc_link)])
					add_2_history(time_cursor, c_loc_link, mean * 8 / length_c_loc_link)
					history_time_step = []
					time_cursor += time_step

			if ev_type == 4:
				nb_veh_link += 1
			if ev_type == 5:
				nb_veh_link -= 1

			history_time_step.append(nb_veh_link)
	conn.close()

	# Third step: We update the database with history_network

	conn = sqlite3.connect(os.path.join(settings.BASE_DIR, 'network_db.sqlite3'))
	c = conn.cursor()
	c.execute('UPDATE index_simul_network SET  bird_occupation = \'' + json.dumps(history_network) + '\'WHERE name_simul = \''+ simu +'\'')
	conn.commit()
	conn.close()


@shared_task
def birdeye_micro(network, simu):

	# First step: the network
	conn = sqlite3.connect(os.path.join(settings.BASE_DIR, 'network_db.sqlite3'))

	c = conn.cursor()
	c.execute('SELECT geojson FROM "index_network" WHERE name = \''+ network +'\'')
	geojson = json.loads(c.fetchone()[0])
	conn.close()

	# Second step, we build the list of all vehicles
	conn = sqlite3.connect(os.path.join(settings.BASE_DIR, 'pointq_db.sqlite3'))
	c = conn.cursor()
	c.execute('SELECT DISTINCT veh_id FROM \''+ simu +'\' WHERE veh_id != -1')
	list_vehicles = c.fetchall()
	conn.close()


	list_vehicles = [str(x[0]) for x in list_vehicles]
	
	# We build the global history dictionary

	global_history = {}
	global_history["list_vehicles"] = list_vehicles

	# we iterate over the vehicles
	for i, vehicle in enumerate(list_vehicles):

		try:
			vehicle_trajectory = VehicleTrajectory(geojson, vehicle, simu)
			global_history[str(vehicle)] = {"t_en_netw":vehicle_trajectory.time_entry_network, "t_ex_netw":vehicle_trajectory.time_exit_network, "hist":vehicle_trajectory.dic_temporal_history}
			print(i/len(list_vehicles))
		except:
			print(vehicle)

	# Save in the database
	conn = sqlite3.connect(os.path.join(settings.BASE_DIR, 'network_db.sqlite3'))
	c = conn.cursor()
	c.execute('UPDATE index_simul_network SET bird_traj = \'' + json.dumps(global_history) + '\' WHERE name_simul = \'' + simu + '\'')
	conn.commit()
	conn.close()


