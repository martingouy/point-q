###################################################################################################################
###                                       JSON FUNCTIONS														   ###
###################################################################################################################

from xml.dom import minidom
from django.conf import settings
from tools import tools_data
import geojson
import os
import json
import sqlite3


def json_get_output_links(node):
	to_return = {'links': 'sam'}
	return to_return

def json_list_simulations():
	# We want to generate a json containing the list of all simulations, their associated network and their description
	query = 'SELECT name_simul, desc_simul, name_network, date_simul FROM index_simul_network'
	output = tools_data.query_sql([query], True, 'network_db')
	json_output = []
	if output:
		for simul in output:
			json_simul = {'name': simul['name_simul'], 'description': simul['desc_simul'].replace('\r\n', '\\r\\n'), 'associatedNetwork': simul['name_network'], 'date': simul['date_simul']}
			json_output.append(json_simul)
	return json.dumps(json_output)

def json_plot_flow(link, t_start, t_end, granul, sim_name, topjson):
	# granularity sanity check
	if t_end - t_start >= granul :

		# number of iteration
		iter = int((t_end - t_start) / granul)

		# we check if the link is an exit link
		topjson = json.loads(topjson)
		topjson_list_links = topjson["LinkList"]
		is_exit = False

		for link_json in topjson_list_links:
			if link_json["link_id"] == str(link) and link_json["outputs"] == "[-1]":
				is_exit = True

		column = 'c_link'
		if is_exit:
			column = "c_loc_link"

		# we start to iterate to create dataPoints
		dataPoints = []
		for i in range(iter):
			query = 'SELECT COUNT(ev_time) FROM ' + sim_name + ' WHERE '+ column +' = ' + str(link) + ' AND ev_type =4 AND ev_time >= ' + str(t_start + i  * granul) + ' AND ev_time < ' + str(t_start + (i  + 1) * granul)
			output = tools_data.query_sql([query], True, 'pointq_db')
			dataPoints.append({'y': float(output[0]['COUNT(ev_time)']), 'label': '['+ str(t_start + i * granul) + '-' + str(t_start + (i  + 1) * granul) + ']'})
		#print(dataPoints)

		serie = {'type': 'column', 'showInLegend': 'true', 'legendText': str(link), 'dataPoints': dataPoints}
		return serie
	else:
		return '{}'

def json_plot_queue(queue, t_start, t_end, sim_name):
	
	dataPoints = []
	nb_veh_queue = 0

	query = 'SELECT ev_time, ev_type FROM ' + sim_name + ' WHERE queue = \'' + queue + '\' AND (ev_type = 4 OR ev_type = 1 OR ev_type = 5)'
	output = tools_data.query_sql([query], True, 'pointq_db')

	for event in output:
		if (event['ev_type'] == 1 or event['ev_type'] == 5):
			nb_veh_queue += 1
		else:
			nb_veh_queue -= 1

		if (event['ev_time'] >= t_start and event['ev_time'] <= t_end):
			dataPoints.append({'x': float(event['ev_time']), 'y': int(nb_veh_queue)})
	

	serie = {'type': 'line', 'showInLegend': 'true', 'legendText': queue, 'dataPoints': dataPoints}
	return serie

def json_plot_link_occupancy(dict_link_occupancy, t_start, t_end, sim_name):

	list_serie = []

	# for each link we want to plot the occupancy
	for link in dict_link_occupancy.keys():
		dataPoints = []
		nb_veh_queue = 0

		# we build the query
		query_partial = '('

		for second_link in dict_link_occupancy[link]:
			if second_link == dict_link_occupancy[link][0]:
				query_partial += 'queue = \'[' + str(link) + ', ' + str(second_link) + ']\''
			else:
				query_partial += ' OR queue = \'[' + str(link) + ', ' + str(second_link) + ']\''

		query_partial += ')'

		query = 'SELECT ev_time, ev_type FROM ' + sim_name + ' WHERE ' + query_partial + ' AND (ev_type = 4 OR ev_type = 1 OR ev_type = 5)'
		output = tools_data.query_sql([query], True, 'pointq_db')

		for event in output:
			if (event['ev_type'] == 1 or event['ev_type'] == 5):
				nb_veh_queue += 1
			else:
				nb_veh_queue -= 1

			if (event['ev_time'] >= t_start and event['ev_time'] <= t_end):
				dataPoints.append({'x': float(event['ev_time']), 'y': int(nb_veh_queue)})
	

		serie = {'type': 'line', 'showInLegend': 'true', 'legendText': 'Link ' + link + ' occupancy', 'dataPoints': dataPoints}
		list_serie.append(serie)

	return list_serie

def json_plot_queue_origin(queue, t_start, t_end, sim_name):
	dataPoints = []
	nb_veh_queue = 0
	origin_link = queue[0]
	str_queue = '[' + queue[1] + ', ' + queue[2] + ']'

	query = 'SELECT ev_time, ev_type FROM ' + sim_name + ' WHERE queue = \'' + str_queue + '\' AND (ev_type = 4 OR ev_type = 1 OR ev_type = 5) AND entry_id = \'' + origin_link + '\''
	output = tools_data.query_sql([query], True, 'pointq_db')

	for event in output:
		if (event['ev_type'] == 1 or event['ev_type'] == 5):
			nb_veh_queue += 1
		else:
			nb_veh_queue -= 1

		if (event['ev_time'] >= t_start and event['ev_time'] <= t_end):
			dataPoints.append({'x': float(event['ev_time']), 'y': int(nb_veh_queue)})
	

	serie = {'type': 'line', 'showInLegend': 'true', 'legendText': str_queue + ' from ' + str(origin_link), 'dataPoints': dataPoints}
	return serie

def json_plot_TT(orig, dest, t_start, t_end, sim_name):
	query = 'SELECT time_entry, time_exit FROM ' + sim_name + ' WHERE entry_id = ' + str(orig) + ' AND c_loc_link = ' + str(dest) + ' AND time_entry >= ' + str(t_start) + ' AND time_entry <= ' +str(t_end)
	output = tools_data.query_sql([query], True, 'pointq_db')
	dataPoints=[]
	for event in output:
		#dataPoints.append({'x':1, 'y':2})
		dataPoints.append({'x':float(event['time_entry']), 'y':(float(event['time_exit']-float(event['time_entry'])))});
	
	# we sort datapoints by x values to avoid the bug
	dataPoints.sort(key=lambda item:item['x'])
	serie = {'type': 'line', 'showInLegend': 'true', 'legendText': str(orig)+' to '+str(dest), 'dataPoints': dataPoints}
	return serie

def xml2geojson(name_network):
	xmldoc = minidom.parse(settings.MEDIA_ROOT + '/upload/network_xml/' + str(name_network) + '.xml')
	xml_nodelist = xmldoc.getElementsByTagName('node') 
	xml_linklist = xmldoc.getElementsByTagName('link') 

	feature_collection= []

	for node in xml_nodelist:
		node_id = node.attributes['id'].value
		point_lat = float(node.getElementsByTagName('point')[0].attributes['lat'].value)
		point_lng = float(node.getElementsByTagName('point')[0].attributes['lng'].value)
		point = geojson.Point((point_lng, point_lat))
		feature = geojson.Feature(properties = {'id': node_id}, geometry = point, id = 'node_'+node_id)
		feature_collection.append(feature)

	for link in xml_linklist:
		link_id = link.attributes['id'].value
		link_length = link.attributes['length'].value
		line = []
		for point in link.getElementsByTagName('point'):
			point_lat = float(point.attributes['lat'].value)
			point_lng = float(point.attributes['lng'].value)
			line.append((point_lng, point_lat))
		line_string = geojson.LineString(line)
		feature = geojson.Feature(properties = {'id': link_id, 'length': link_length}, geometry = line_string, id = 'link_'+link_id)
		feature_collection.append(feature)

	feature_collection = geojson.FeatureCollection(feature_collection)
	return geojson.dumps(feature_collection)

def xml2topjson(name_network):
	xmldoc = minidom.parse(settings.MEDIA_ROOT + '/upload/network_xml/' + str(name_network) + '.xml')
	xml_nodelist = xmldoc.getElementsByTagName('node') 
	xml_linklist = xmldoc.getElementsByTagName('link') 
	nodes={}
	link_outs={}
	for s in xml_nodelist:
		nodes[int(s.attributes['id'].value)]=([int(t.attributes['link_id'].value) for t in s.getElementsByTagName('input')],[int(t.attributes['link_id'].value) for t in s.getElementsByTagName('output')])
		for t in s.getElementsByTagName('input'):
			link_outs[int(t.attributes['link_id'].value)]=[int(u.attributes['link_id'].value) for u in s.getElementsByTagName('output')]

	json_output='{"NodeList":['+', '.join(['{"id":"' + str(k) + '", "inputs":"'+str(v[0])+'", "outputs":"' + str(v[1])+ '"}' for k,v in nodes.items()])+ \
    '], "LinkList":['+', '.join(['{"link_id":"' + str(k) + '", "outputs":"' + str(v)+ '"}' for k,v in link_outs.items() if k!=-1])+']}'


	return json_output

def birdeye_filter(sim_name, conf):

	# Load the configuration parameters
	type_filter = conf['filter']
	paths = conf['paths']
	t_start = conf['t_start']
	t_end = conf['t_end']
	ods = conf['ods']

	# Connection to DB to get the birdeye data to filter
	conn = sqlite3.connect(os.path.join(settings.BASE_DIR, 'network_db.sqlite3'))
	c = conn.cursor()
	c.execute('SELECT bird_traj FROM index_simul_network WHERE name_simul = \'' + sim_name + '\'')
	data = c.fetchone()[0]
	conn.close()

	if data == 'False':
		return 'False'

	data = json.loads(data)


	def issublist(sublist, list_full):
		# is path a sublist of path_veh ?
		for i, link in enumerate(list_full):
			if link == sublist[0]:
				try:
					if list_full[i: i + len(sublist)] == sublist:
						return True
					else:
						pass
				except:
					pass
		return False

	# We want to build the list of the vehicles that went through the path
	def filter_path(record):
		filtered_veh = []

		for vehicle, hist_veh in record.items():
			try:
				path_veh = [str(x['link']) for x in hist_veh['hist']]

				for path in paths:
					if issublist(path, path_veh):
						filtered_veh.append(vehicle)
						break
			except:
				pass

		return {key: value for (key, value) in record.items() if key in filtered_veh}

	def filter_od(record):
		filtered_veh = []

		for vehicle, hist_veh in record.items():
			for od in ods:
				origin = od[0]
				destination = od[1]
				if str(hist_veh['hist'][0]['link']) ==  origin and str(hist_veh['hist'][len(hist_veh['hist']) - 1]['link']) == destination:
					filtered_veh.append(vehicle)
					break
				
		return {key: value for (key, value) in record.items() if key in filtered_veh}

	def filter_time(record):

		filtered_veh = []
		list_veh = record['list_vehicles']

		for vehicle in list_veh:
			t_entry_network = record[vehicle]['t_en_netw']
			t_exit_network = record[vehicle]['t_ex_netw']

			if t_exit_network < t_start:
				pass

			elif t_entry_network > t_end:
				break

			elif t_start <= t_entry_network and t_entry_network < t_end:
				filtered_veh.append(vehicle)

		return {key: value for (key, value) in record.items() if key in filtered_veh}

	time_filtered = filter_time(data)

	if type_filter == 'none':
		time_filtered['list_vehicles']  = [int(x) for x in time_filtered.keys()]
		time_filtered['list_vehicles'].sort()
		return time_filtered

	elif type_filter == 'path':
		path_filtered = filter_path(time_filtered)
		path_filtered['list_vehicles']  = [int(x) for x in path_filtered.keys()]
		path_filtered['list_vehicles'].sort()
		return path_filtered

	elif type_filter == 'od':
		od_filtered = filter_od(time_filtered)
		od_filtered['list_vehicles']  = [int(x) for x in od_filtered.keys()]
		od_filtered['list_vehicles'].sort()
		return od_filtered
	

	return 1






