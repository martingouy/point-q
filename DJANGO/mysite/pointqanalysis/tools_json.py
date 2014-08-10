###################################################################################################################
###                                       JSON FUNCTIONS														   ###
###################################################################################################################

import tools_data
import geojson
import json
from xml.dom import minidom
from django.conf import settings

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
		feature = geojson.Feature(properties = {'id': node_id}, geometry = point)
		feature_collection.append(feature)

	for link in xml_linklist:
		link_id = link.attributes['id'].value
		line = []
		for point in link.getElementsByTagName('point'):
			point_lat = float(point.attributes['lat'].value)
			point_lng = float(point.attributes['lng'].value)
			line.append((point_lng, point_lat))
		line_string = geojson.LineString(line)
		feature = geojson.Feature(properties = {'id': link_id}, geometry = line_string)
		feature_collection.append(feature)

	feature_collection = geojson.FeatureCollection(feature_collection)
	return geojson.dumps(feature_collection)