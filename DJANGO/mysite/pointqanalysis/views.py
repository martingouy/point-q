from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from forms import Form_upload_fil,  Form_upload_xml , Form_delete_xml
from lxml import etree
import sqlite3
import json
import os
import csv
import geojson
from xml.dom import minidom
from django.db import connections
from django.conf import settings


###################################################################################################################
###                                       TOOL FUNCTIONS														   ###
###################################################################################################################

def dictfetchall(cursor):
	desc = cursor.description
	return [
	    dict(zip([col[0] for col in desc], row))
	    for row in cursor.fetchall()
	]

def save_file(file, name, path='', extension='.txt'):
	fd = open('%s/%s' % (settings.MEDIA_ROOT + str(path), str(name) + extension), 'wb')
	for chunk in file.chunks():
		fd.write(chunk)
	fd.close()

def query_sql(querys, return_dic, db):
	# connection database
	conn = sqlite3.connect(r"/Users/martingouy/Desktop/Martin/GitHub/point-q/DJANGO/mysite/"+ db +".sqlite3")
	cursor = conn.cursor()

	# query
	for query in querys:
		try:
			cursor.execute(query)
			conn.commit()
		except:
			return False

	if return_dic== True:
		output = dictfetchall(cursor)
		conn.close()
		return output
	else:
		conn.close()
		return True

def query_sql_debug(querys, return_dic, db):
	# connection database
	conn = sqlite3.connect(r"/Users/martingouy/Desktop/Martin/GitHub/point-q/DJANGO/mysite/"+ db +".sqlite3")
	cursor = conn.cursor()

	# query
	for query in querys:
		
		cursor.execute(query)
		conn.commit()
	

	if return_dic== True:
		output = dictfetchall(cursor)
		conn.close()
		return output
	else:
		conn.close()
		return True


###################################################################################################################
###                                       JSON FUNCTIONS														   ###
###################################################################################################################

def json_plot_flow(link, t_start, t_end, granul, sim_name):
	# granularity sanity check
	if t_end - t_start > granul :

		# number of iteration
		iter = int((t_end - t_start) / granul)

		# we start to iterate to create dataPoints
		dataPoints = []
		for i in range(iter):
			query = 'SELECT COUNT(ev_time) FROM ' + sim_name + ' WHERE c_link = ' + str(link) + ' AND ev_type =4 AND ev_time >= ' + str(t_start + i  * granul) + ' AND ev_time < ' + str(t_start + (i  + 1) * granul)
			output = query_sql([query], True, 'pointq_db')
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
	output = query_sql_debug([query], True, 'pointq_db')

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

###################################################################################################################
###                                       SQL FUNCTIONS														   ###
###################################################################################################################

def list_sim_db():
	# we create the xml doc to store the list
	root = etree.Element('root')

	# connection database
	query = 'SELECT name FROM SQLITE_MASTER WHERE type=\'table\' ORDER BY name'
	
	query_answer = query_sql([query], True, 'pointq_db')
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
	query_sql([query_2], False, 'network_db')
	return query_sql([query_1], False, 'pointq_db')

def treat_simul_db(name, path):

	conn = sqlite3.connect(r"/Users/martingouy/Desktop/Martin/GitHub/point-q/DJANGO/mysite/pointq_db.sqlite3")
	cursor = conn.cursor()
	name = str(name).lower()

	# We create the table
	cursor.execute('CREATE TABLE ' + name + ' (ev_time real, ev_type int, veh_id int, c_link int, queue text)')
	conn.commit()

	# Conversion from csv to sqlite
	with open('%s/%s' % (settings.MEDIA_ROOT + str(path), str(name) + '.txt'), 'rb') as file:
		reader = csv.reader(file)
		for row in reader:
			cursor.execute("INSERT INTO " + name + " VALUES (" + row[0] + " ," + row[1] + " ," + row[11] + " ," + row[24] + " ,'" + row[18] + "')")
		conn.commit()

	conn.close()

def treat_network_db(name,path):

	# we create the table index_network if it's not created
	query_1 = 'CREATE TABLE index_network (name text, geojson text)'
	query_sql([query_1], False, 'network_db')

	# we insert a new row in index_network
	query_2 = 'INSERT INTO index_network VALUES (\'' + name + '\',\'' + xml2geojson(name) + '\')'
	query_sql([query_2], False, 'network_db')





###################################################################################################################
###                                                                    VIEWS													   ###
###################################################################################################################

def ajax(request):
	if request.GET.get('action', '') == 'listsim':
		xml = list_sim_db()
		return HttpResponse(xml)

	elif request.GET.get('action', '') == 'deltable':
		table = request.GET.get('table_name', '')
		return HttpResponse(deltable(table))

	elif request.GET.get('action', '') == 'set_cookie':
		sim_name = request.GET.get('sim_name', '')
		response = HttpResponse('Cookie')
		response.set_cookie(key = 'sim_name', value = sim_name)
		return response

	elif request.GET.get('action', '') == 'redirect':
		redirection = request.GET.get('redirection', '')
		return HttpResponse(reverse('pointqanalysis:' + redirection))

	elif request.GET.get('action', '') == 'generate_json_plot':
		# we treat the parameters
		type_anal = request.GET.get('type', '')
		t_start = int(request.GET.get('t_start', ''))
		t_end = int(request.GET.get('t_end', ''))
		sim_name = request.COOKIES['sim_name']
		# first case: flows
		if type_anal == 'flow':
			granul = int(request.GET.get('granul', ''))
			links = request.GET.get('links', '')
			list_links = links.split('-')
			data = []

			for link_id in list_links:
				data.append(json_plot_flow(link_id, t_start, t_end, granul, sim_name))

			title = {'text': 'Flows'}
			axisX = {'title': "Time interval (s)", 'titleFontWeight': "lighter", 'titleFontSize': '17'}
			axisY = {'title': "Number of veh. (veh)", 'titleFontWeight': "lighter", 'titleFontSize': '17'}
			answer = {'title': title, 'axisX': axisX, 'axisY': axisY, 'data': data}
			return HttpResponse(json.dumps(answer, indent=4), content_type="application/json")
		# second case : queues
		elif type_anal == 'queue':

			queues = request.GET.get('queues', '')
			list_queues = queues.split('-')
			list_queues_treated = []
			for queue in list_queues:
				list_queues_treated.append('[' + queue.split('.')[0] + ', ' + queue.split('.')[1] + ']')

			data = []

			for queue in list_queues_treated:
				data.append(json_plot_queue(queue, t_start, t_end, sim_name))

			title = {'text': 'Queues'}
			axisX = {'title': "Seconds (s)", 'titleFontWeight': "lighter", 'titleFontSize': '17'}
			axisY = {'title': "Queue length (veh)", 'titleFontWeight': "lighter", 'titleFontSize': '17'}
			answer = {'zoomEnabled': 'true', 'title': title, 'axisX': axisX, 'axisY': axisY, 'data': data}
			return HttpResponse(json.dumps(answer, indent=4), content_type="application/json")



	else:
		return False
	

def analysis(request):
	# First step : create a list of the available links:
	try:
		if request.COOKIES['sim_name'] in list_sim_db():

			# we create maxtimesim
			sim_name = request.COOKIES['sim_name']
			query = 'SELECT MAX(ev_time) AS max_time FROM ' + sim_name
			output = query_sql([query], True, 'pointq_db')
			maxtimesim = int(round(output[0]['max_time']))

			# which network is associated with the simulation
			query_1 = 'SELECT name_network FROM index_simul_network WHERE name_simul = \'' + str(sim_name) + '\''
			associated_network = query_sql([query_1], True, 'network_db')[0]['name_network']

			# we load the geojson of the associated network
			query_2 = 'SELECT geojson FROM index_network WHERE name = \'' + str(associated_network) + '\''
			geojson_associated_network = query_sql([query_2], True, 'network_db')[0]['geojson']

			template = loader.get_template('pointqanalysis/index.html')
		    	context = RequestContext(request, {'maxtimesim': maxtimesim, 'geojson': geojson_associated_network})

		    	return HttpResponse(template.render(context))
		else:
			return HttpResponseRedirect(reverse('pointqanalysis:simulations'))
			
	except:
		return HttpResponseRedirect(reverse('pointqanalysis:simulations'))

def simul_manag(request):

	# If we receive a POST request : the form has been submitted
	if request.method == 'POST':

	    form = Form_upload_fil(request.POST, request.FILES)

	    # if the form is valid (no error)
	    if form.is_valid() and form.is_multipart():

		name_simul = form.cleaned_data['name_simul']
		name_network = form.cleaned_data['name_network']

		# we save the upload
		save_file(request.FILES['simul_txt_db'], name_simul , '/upload/txt_db', '.txt')
		status = 'Thanks for uploading the text database'

		# we convert the db
		treat_simul_db(name_simul , '/upload/txt_db')

		# we create the table index_network if it's not created
		query_1 = 'CREATE TABLE index_simul_network (name_simul text, name_network text)'
		query_sql([query_1], False, 'network_db')

		# we insert a new row in index_network
		query_2 = 'INSERT INTO index_simul_network VALUES (\'' + name_simul + '\',\'' + name_network+ '\')'
		query_sql([query_2], False, 'network_db')

		# we delete the upload
		os.remove(settings.MEDIA_ROOT + '/upload/txt_db/' + str(name_simul) + '.txt')

	    else:
		status = ''
	# Else: the request is type GET: we print the form
	else:
		form = Form_upload_fil()
		status =''

	template = loader.get_template('pointqanalysis/upload.html')
    	context = RequestContext(request, {'form': form, 'status':status, 'upload_xml': reverse('pointqanalysis:upload_xml')})
	return HttpResponse(template.render(context))

def upload_xml(request):

	status = 'unposted'
	# If we receive a POST request : the form has been submitted
	if request.method == 'POST':

		form = Form_upload_xml(request.POST, request.FILES)
		form2 = Form_delete_xml(request.POST, request.FILES)

		# if the form upload is valid (no error)
		if form.is_valid() and form.is_multipart():

			# we set delete form to normal
			form2 = Form_delete_xml()

			name_network= form.cleaned_data['name_network']

			# we save the upload
			save_file(request.FILES['network_xml'], name_network , '/upload/network_xml', '.xml')

			# we convert the network
			treat_network_db(name_network, '/upload/network_xml')

			# we delete the upload
			os.remove(settings.MEDIA_ROOT + '/upload/network_xml/' + str(name_network) + '.xml')

			status = 'posted'

		# if form delete is valid
		elif form2.is_valid() and form.is_multipart():

			# we set upload form to normal
			form = Form_upload_xml()

			name_network_delete= form2.cleaned_data['name_network_delete']

			# we build the query to delete the network from the database
			query = 'DELETE FROM index_network WHERE name = \'' + name_network_delete + '\''

			# we delete the row from the table
			query_sql_debug([query], False, 'network_db')

			status = 'posted'


	# Else: the request is type GET: we print the form
	else:
		form = Form_upload_xml()
		form2 = Form_delete_xml()

	template = loader.get_template('pointqanalysis/uploadxml.html')
    	context = RequestContext(request, {'form': form, 'form2': form2, 'status': status})
	return HttpResponse(template.render(context))