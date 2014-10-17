###################################################################################################################
###                                       JSON FUNCTIONS														   ###
###################################################################################################################

import tools_data
import geojson
import json
from xml.dom import minidom
from django.conf import settings

def json_get_output_links(node):
    to_return = {'links': 'sam'}
    return to_return

def json_plot_flow(link, t_start, t_end, granul, sim_name):
	# granularity sanity check
	if t_end - t_start >= granul :

		# number of iteration
		iter = int((t_end - t_start) / granul)

		# we start to iterate to create dataPoints
		dataPoints = []
		for i in range(iter):
			query = 'SELECT COUNT(ev_time) FROM ' + sim_name + ' WHERE c_link = ' + str(link) + ' AND ev_type =4 AND ev_time >= ' + str(t_start + i  * granul) + ' AND ev_time < ' + str(t_start + (i  + 1) * granul)
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

	json_output='{"NodeList":['+', '.join(['{"id":"' + str(k) + '", "inputs":"'+str(v[0])+'", "outputs":"' + str(v[1])+ '"}' for k,v in nodes.iteritems()])+ \
    '], "LinkList":['+', '.join(['{"link_id":"' + str(k) + '", "outputs":"' + str(v)+ '"}' for k,v in link_outs.iteritems() if k!=-1])+']}'


	return json_output

