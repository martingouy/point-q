###################################################################################################################
###                                       SQL FUNCTIONS														   ###
###################################################################################################################

import sqlite3
from lxml import etree
from tools import tools_data, tools_json
import csv
from django.conf import settings
import os
import json
import time

def list_sim_db():
	# we create the xml doc to store the list
	root = etree.Element('root')
	list_sim_name = []

	# connection database
	query = 'SELECT name FROM SQLITE_MASTER WHERE type=\'table\' ORDER BY name'
	
	query_answer = tools_data.query_sql([query], True, 'pointq_db')
	for line in query_answer:
		sim = etree.Element('sim')
		sim.text = line['name']
		root.append(sim)
		list_sim_name.append(line['name'])

        #return xml
	xml = etree.tostring(root)
	return [xml, list_sim_name]

def deltable(table_name):
	# connection database
	query_1 = 'DROP TABLE ' + str(table_name)	
	query_2 = 'DELETE FROM index_simul_network WHERE name_simul = \'' + str(table_name) + '\''
	tools_data.query_sql([query_2], False, 'network_db')
	return tools_data.query_sql([query_1], False, 'pointq_db')

def treat_simul_db(name, path):

	conn = sqlite3.connect(os.path.join(settings.BASE_DIR, 'pointq_db.sqlite3'))
	cursor = conn.cursor()
	name = str(name).lower()

	# We create the table
	cursor.execute('CREATE TABLE ' + name + ' (ev_time real, ev_type int, id_inter text, int_ctrl_mat text, veh_id int, c_link int, queue text, time_entry real, entry_id int, time_exit int, c_loc_link int)')
	#cursor.execute('CREATE TABLE ' + name + ' (ev_time real, ev_type int, veh_id int, c_link int, queue text)')
	conn.commit()

	# Conversion from csv to sqlite
	with open('%s/%s' % (settings.MEDIA_ROOT + str(path), str(name) + '.txt'), 'rt') as file:
		reader = csv.reader(file)
		for row in reader:
			if len(row)==11:
				#cursor.execute("INSERT INTO " + name + " VALUES (" + row[0] + " ," + row[1] + " ," + row[2] + " ," + row[3] + " ,'" + row[4] + "')")
				cursor.execute("INSERT INTO " + name + " VALUES (" + row[0] + " ," + row[1] + " ,'" + row[2] + "' ,'" + row[3] + "',"+ row[4] + " ," + row[5] + " ,'" + row[6] + "' ," + row[7] + " ," + row[8] + " ," + row[9] + " ," + row[10] + ")")
			else:
				#There's a typo in Jenny's Docs: Column 25 contains the id of the link associated with the current event. Due to 0-based indexing, it appears at 24 here
				#NOTE that there's a difference between Column 25 (id of link associated with current event) and Column 15(id of link where the vehicle is currently located)
				#cursor.execute("INSERT INTO " + name + " VALUES (" + row[0] + " ," + row[1] + " ," + row[11] + " ," + row[24] + " ,'" + row[18] + "')")
				cursor.execute("INSERT INTO " + name + " VALUES (" + row[0] + " ," + row[1] + " ,'" + row[2] + "' ,'" + row[8] + "',"+ row[11] + " ," + row[24] + " ,'" + row[18] + "' ," + row[12] + " ," + row[13] + " ," + row[23] + " ," + row[14] + ")")
		conn.commit()

	conn.close()

def treat_network_db(name,path):
	# we create the table index_network if it's not created
	query_1 = 'CREATE TABLE index_network (name text, geojson text, topjson text)'
	tools_data.query_sql([query_1], False, 'network_db')

	# we insert a new row in index_network
    #	query_2 = 'INSERT INTO index_network VALUES (\'' + name + '\',\'' + tools_json.xml2geojson(name) + '\')'
	query_2 = 'INSERT INTO index_network VALUES (\'' + name + '\',\'' + tools_json.xml2geojson(name) + '\',\'' + tools_json.xml2topjson(name) + '\')'
	tools_data.query_sql([query_2], False, 'network_db')


def plot_vehicle_traj(origin, dest, t_min, t_max, id_route, max_nb_veh, table, db, associated_network):

	###############################################################################################################
	#####                    WE CREATE THE DIC OF ROUTES WITH TIME RESTRICTION
	###############################################################################################################

	start = time.clock()
	conn = sqlite3.connect(os.path.join(settings.BASE_DIR, db + '.sqlite3'))

	c = conn.cursor()

	query_all = "SELECT ev_time, c_loc_link, veh_id, id_inter, ev_type FROM " + table + " WHERE ev_type = 4 OR ev_type = 1 OR ev_type = 5 AND ev_time >= " + str(t_min) + " AND ev_time <= " + str(t_max)
	c.execute(query_all)
	temp = time.clock() -start
	dic_vehicles = {}
	for event in c:

		veh_id = event[2]
		ev_time = event[0]
		c_loc_link = event[1]
		id_inter = event[3]
		ev_type = event[4]

		if str(veh_id) in dic_vehicles.keys():
			vehicle = dic_vehicles[str(veh_id)]

			if str(c_loc_link) in vehicle.keys():
				vehicle[str(c_loc_link)]["t_exit"] = ev_time

				if id_inter != '-1' and (not id_inter in vehicle['intersections']):
					vehicle['intersections'].append(int(str(id_inter).replace("[", "").replace("]", "")))

			else:
				vehicle[str(c_loc_link)] = {}
				vehicle[str(c_loc_link)]["t_entry"] = ev_time
				vehicle['route'].append(c_loc_link)

				if id_inter != '-1' and (not id_inter in vehicle['intersections']):
					vehicle['intersections'].append(int(str(id_inter).replace("[", "").replace("]", "")))

		else:
			dic_vehicles[str(veh_id)] = {}
			vehicle = dic_vehicles[str(veh_id)]
			vehicle[str(c_loc_link)] = {}
			vehicle[str(c_loc_link)]["t_entry"] = ev_time
			vehicle['route'] = [c_loc_link]
			vehicle['intersections'] = []
			if id_inter != '-1' and (not id_inter in vehicle['intersections']):
				vehicle['intersections'].append(int(str(id_inter).replace("[", "").replace("]", "")))

	dic_routes = {}
	origin = int(origin)
	dest = int(dest)

	for vehicle in sorted(dic_vehicles.keys()):
		route = dic_vehicles[vehicle]['route']
		intersections = dic_vehicles[vehicle]['intersections']
		if (dest in route and origin in route):
			if route.index(origin) < route.index(dest):
				if 't_entry' in dic_vehicles[vehicle][str(origin)].keys() and 't_entry' in dic_vehicles[vehicle][str(dest)].keys():
					if dic_vehicles[vehicle][str(origin)]['t_entry'] >= t_min and dic_vehicles[vehicle][str(dest)]['t_entry'] <= t_max:
						truncated_route = tuple([x for x in route if route.index(origin) <= route.index(x) and route.index(x) <= route.index(dest)])
						if not truncated_route in dic_routes:
							truncated_intersections = [x for x in intersections if route.index(origin) <= intersections.index(x) and intersections.index(x) <= route.index(dest)]
							dic_routes[truncated_route] = [[vehicle], truncated_intersections]
						else:
							dic_routes[truncated_route][0].append(vehicle)

	conn.close()

	###############################################################################################################
	#####                    WE NOW HAVE dic_routes AND dic_vehicles, lets build the json for the graph
	############################################################################################################### 

	try: 
		links = list(dic_routes.keys())[id_route]
		vehicles = sorted([ int(x) for x in dic_routes[tuple(links)][0]])
		vehicles = [str(x) for x in vehicles]
		dic_length = length_links(links, associated_network)

		#we start building the JSON for the plot
		json_plot = {'zoomEnabled': 'true', 'exportEnabled': 'true', 'title': {'text': "Vehicles Trajectory"}, 'axisX': {'title': "Time (s)"}, 'axisY': {'title': "Traveled distance (m)"}, 'data': []}

		# we iterate over the vehicles:
		nb_plotted_veh = 0
		for i in range(len(vehicles)):

			if nb_plotted_veh >= max_nb_veh:
				break
			else:
				#We create the JSON for the vehicle
				vehicle = vehicles[i]

				if dic_vehicles[vehicle][str(links[0])]['t_entry'] >= t_min and dic_vehicles[vehicle][str(links[len(links) - 1])]['t_entry'] <= t_max:
					temp_json = {'type': "line", 'dataPoints': []}
					y_init = 0

					# We iterate over the links
					for j in range(len(links)):

						link = str(links[j])

						# we check if the link is an internal link
						if  't_entry' in dic_vehicles[vehicle][link] and 't_exit' in dic_vehicles[vehicle][link]:
							x_entry = dic_vehicles[vehicle][link]['t_entry']
							x_exit = dic_vehicles[vehicle][link]['t_exit']
							if  x_entry > t_min and x_exit < t_max:
								length = float(dic_length[str(link)]);
								temp_json['dataPoints'].append({'x': x_entry, 'y': round(y_init)});
								temp_json['dataPoints'].append({'x': x_exit, 'y': round(y_init + length)});
								y_init += length
					nb_plotted_veh = nb_plotted_veh + 1

					json_plot['data'].append(temp_json)

		#*****************************************************************************************
		# We want to create a dictionary:  key: distance / value: corresponding node for the tooltip
		#*****************************************************************************************


			# we create a list of the links that will be plotted:
			links_plotted = []
			nodes_plotted = dic_routes[tuple(links)][1]
			index_not_plotted = []

			# We iterate over the links
			for j in range(len(links)):

				link = links[j]
				vehicle = vehicles[0]

				# we check if the link is an internal link
				if 't_entry' in dic_vehicles[vehicle][str(link)] and 't_exit' in dic_vehicles[vehicle][str(link)]:
					links_plotted.append(link)
				
				else:
					index_not_plotted.append(j);

			try : 
				index_not_plotted.index(0)
				nodes_plotted = nodes_plotted[1:]
			except:
				pass

			dic_dist_node = {}
			dic_node_dist = {}
			temp_length = 0

			for i in range(len(nodes_plotted)):
				temp_length += float(dic_length[str(links_plotted[i])])
				dic_dist_node[str(round(temp_length))] = nodes_plotted[i]
				dic_node_dist[str(nodes_plotted[i])] = str(round(temp_length))


		return {'dic_node_dist': dic_node_dist, 'dic_dist_node': dic_dist_node, 'json': json_plot, 'nodes_plotted': nodes_plotted, 'links_plotted': links_plotted}

	except:
		return {'dic_node_dist': {}, 'dic_dist_node': {}, 'json': {}, 'nodes_plotted': [], 'links_plotted': []}



def list_vehicle_traj(origin, dest, table, db):
	start = time.clock()
	conn = sqlite3.connect(os.path.join(settings.BASE_DIR, db + '.sqlite3'))

	c = conn.cursor()

	query_all = "SELECT ev_time, c_loc_link, veh_id, id_inter, ev_type FROM " + table + " WHERE ev_type = 4 OR ev_type = 1 OR ev_type = 5"
	c.execute(query_all)
	temp = time.clock() -start
	dic_vehicles = {}
	for event in c:
		# veh_id = event['veh_id']
		# ev_time = event['ev_time']
		# c_loc_link = event['c_loc_link']
		# id_inter = event['id_inter']
		# ev_type = event['ev_type']

		veh_id = event[2]
		ev_time = event[0]
		c_loc_link = event[1]
		id_inter = event[3]
		ev_type = event[4]

		if str(veh_id) in dic_vehicles.keys():
			vehicle = dic_vehicles[str(veh_id)]

			if str(c_loc_link) in vehicle.keys():
				vehicle[str(c_loc_link)]["t_exit"] = ev_time

				if id_inter != '-1' and (not id_inter in vehicle['intersections']):
					vehicle['intersections'].append(int(str(id_inter).replace("[", "").replace("]", "")))

			else:
				vehicle[str(c_loc_link)] = {}
				vehicle[str(c_loc_link)]["t_entry"] = ev_time
				vehicle['route'].append(c_loc_link)

				if id_inter != '-1' and (not id_inter in vehicle['intersections']):
					vehicle['intersections'].append(int(str(id_inter).replace("[", "").replace("]", "")))

		else:
			dic_vehicles[str(veh_id)] = {}
			vehicle = dic_vehicles[str(veh_id)]
			vehicle[str(c_loc_link)] = {}
			vehicle[str(c_loc_link)]["t_entry"] = ev_time
			vehicle['route'] = [c_loc_link]
			vehicle['intersections'] = []
			if id_inter != '-1' and (not id_inter in vehicle['intersections']):
				vehicle['intersections'].append(int(str(id_inter).replace("[", "").replace("]", "")))

	dic_routes = {}
	origin = int(origin)
	dest = int(dest)

	for vehicle in dic_vehicles.keys():
		route = dic_vehicles[vehicle]['route']
		intersections = dic_vehicles[vehicle]['intersections']
		if (dest in route and origin in route):
			if route.index(origin) < route.index(dest):
				truncated_route = tuple([x for x in route if route.index(origin) <= route.index(x) and route.index(x) <= route.index(dest)])
				if not truncated_route in dic_routes:
					truncated_intersections = [x for x in intersections if route.index(origin) <= intersections.index(x) and intersections.index(x) <= route.index(dest)]
					dic_routes[truncated_route] = [[vehicle], truncated_intersections]
				else:
					dic_routes[truncated_route][0].append(vehicle)


	return [dic_routes, time.clock() - start]

	conn.close()

def length_links(links, associated_network):
	lengths = {}

	# we recover the json of the network from the database
	query = "SELECT geojson FROM index_network WHERE name = \'" + associated_network + "\'"
	geojson = tools_data.query_sql([query], True, 'network_db')[0]['geojson']
	geojson = json.loads(geojson)

	for feature in geojson['features']:
		if int(feature['properties']['id']) in links and feature['geometry']['type'] == 'LineString':
			lengths[str(feature['properties']['id'])] = feature['properties']['length']
	return lengths

