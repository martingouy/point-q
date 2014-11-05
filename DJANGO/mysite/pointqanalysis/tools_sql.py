###################################################################################################################
###                                       SQL FUNCTIONS														   ###
###################################################################################################################

import sqlite3
from lxml import etree
import tools_data
import tools_json
import csv
from django.conf import settings
import os
import json

def list_sim_db():
	# we create the xml doc to store the list
	root = etree.Element('root')

	# connection database
	query = 'SELECT name FROM SQLITE_MASTER WHERE type=\'table\' ORDER BY name'
	
	query_answer = tools_data.query_sql([query], True, 'pointq_db')
	for line in query_answer:
		sim = etree.Element('sim')
		sim.text = line['name']
		root.append(sim)

        #return xml
	xml = etree.tostring(root)
	return xml

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
	with open('%s/%s' % (settings.MEDIA_ROOT + str(path), str(name) + '.txt'), 'rb') as file:
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

def list_vehicle_traj(origin, dest, table, db):
	conn = sqlite3.connect(os.path.join(settings.BASE_DIR, db + '.sqlite3'))

	c = conn.cursor()

	c.execute("SELECT ev_time, veh_id FROM " + table + " WHERE c_loc_link = " +  origin + " AND (ev_type = 4 OR ev_type = 1)")

	# We obtain a list of dictionarys [{'ev_time': 12.2, 'veh_id': 46}, ...]
	vehicles_link_1 = tools_data.dictfetchall(c)

	# For each vehicle we check if they went through the second link later
	i = 0

	vehicles_link_1_link_2 = []
	for vehicle_link_1 in vehicles_link_1:
		veh_id = vehicle_link_1['veh_id']
		event_time_1 = vehicle_link_1['ev_time']
		c.execute("SELECT ev_time, ev_type FROM " + table + " WHERE c_loc_link = " + dest + " AND veh_id =" + str(veh_id))
		
		dic_temp = tools_data.dictfetchall(c)	
		for i in range(len(dic_temp)):

			event = dic_temp[i]
			event_time_2 = event['ev_time']
			if event_time_1 < event_time_2:
				if i + 1 in range(len(dic_temp)) and dic_temp[i + 1]['ev_type'] == 5:
					vehicle_link_1['ev_time_2'] = dic_temp[i + 1]['ev_time'] 
					vehicles_link_1_link_2.append(vehicle_link_1)
				else:
					vehicle_link_1['ev_time_2'] = event_time_2
					vehicles_link_1_link_2.append(vehicle_link_1)
				break

	# Now we determine the different routes available
	dic_routes = {}
	dic_vehicles = {}

	for vehicle in vehicles_link_1_link_2:
		route = []
		intersection = []
		dic_vehicles[str(vehicle['veh_id'])] = {}
		c.execute("SELECT c_loc_link, id_inter, ev_type, ev_time FROM " + table + " WHERE veh_id =" + str(vehicle['veh_id']) + " AND ev_time >= " + str(vehicle['ev_time']) + " AND ev_time <= " + str(vehicle['ev_time_2']))

		for link in tools_data.dictfetchall(c):

			if not str(link['c_loc_link']) in dic_vehicles[str(vehicle['veh_id'])].keys():
				dic_vehicles[str(vehicle['veh_id'])][str(link['c_loc_link'])] = {}

			if link['id_inter'] != '-1':
				intersection.append(int(str(link['id_inter']).replace("[", "").replace("]", "")))

			if link['ev_type'] == 1 or link['ev_type'] == 4:
				dic_vehicles[str(vehicle['veh_id'])][str(link['c_loc_link'])]['t_entry'] = link['ev_time']
				route.append(link['c_loc_link'])

			elif link['ev_type'] == 5:
				dic_vehicles[str(vehicle['veh_id'])][str(link['c_loc_link'])]['t_exit'] = link['ev_time']

		route = tuple(route)
		if not route in dic_routes.keys():
			dic_routes[route] = [[vehicle['veh_id']], intersection]
		else:
			dic_routes[route][0].append(vehicle['veh_id'])

	return [dic_routes, dic_vehicles]




	# We can also close the connection if we are done with it.
	# Just be sure any changes have been committed or they will be lost.
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

