from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from .forms import Form_upload_fil,  Form_upload_xml , Form_delete_xml
from django.conf import settings
import json
import os
import re
import time
import sqlite3
import gzip
from pointqanalysis.tasks import birdeye, birdeye_micro
from tools import tools_data, tools_json, tools_sql



###################################################################################################################
###                                                                    VIEWS					   			   ###
###################################################################################################################

@csrf_exempt
def ajax(request):
	if request.method == 'POST':
		if request.POST.get("action", "") == 'veh_trajectory':
			links = json.loads(request.POST.get("links", ""))
			max_nb_veh = json.loads(request.POST.get("max_nb_veh", ""))
			id_route_analyse = json.loads(request.POST.get("id_route_analyse", ""))
			tmin_analysis = json.loads(request.POST.get("tmin_analysis", ""))
			tmax_analysis = json.loads(request.POST.get("tmax_analysis", ""))

			# First we calculate the length of each link
			try:
				sim_name = request.COOKIES['sim_name']
				# which network is associated with the simulation
				query_1 = 'SELECT name_network FROM index_simul_network WHERE name_simul = \'' + str(sim_name) + '\''
				associated_network = tools_data.query_sql([query_1], True, 'network_db')[0]['name_network']
				
				result = tools_sql.plot_vehicle_traj(links[0], links[len(links) - 1], tmin_analysis, tmax_analysis, id_route_analyse, max_nb_veh, sim_name, "pointq_db", associated_network)

				return HttpResponse(json.dumps(result))
			except:
				return HttpResponse('False')

		elif request.POST.get("action", "") == 'stage_actuation':
			nodes_plotted = json.loads(request.POST.get("nodes_plotted", ""))
			sim_name = request.COOKIES['sim_name']
			dic_node_stage_actuation = {}

			for node in nodes_plotted:
				# which network is associated with the simulation
				query_1 = 'SELECT ev_time, int_ctrl_mat FROM \'' + str(sim_name) + '\' WHERE ev_type = 3 AND id_inter = '+ str(node)
				stage_actuation_node = tools_data.query_sql_debug([query_1], True, 'pointq_db')
				dic_node_stage_actuation[str(node)] = stage_actuation_node

			return HttpResponse(json.dumps(dic_node_stage_actuation))

	else:

		if request.GET.get('action', '') == 'deltable':
			table = request.GET.get('table_name', '')
			return HttpResponse(tools_sql.deltable(table))

		elif request.GET.get('action', '') == 'bird_traj':
			try : 
				sim_name = request.COOKIES['sim_name']
				conn = sqlite3.connect(os.path.join(settings.BASE_DIR, 'network_db.sqlite3'))
				c = conn.cursor()
				c.execute('SELECT bird_traj, bird_occupation FROM index_simul_network WHERE name_simul = \'' + sim_name + '\'')
				result = c.fetchone()
				vehicles = result[0]
				occupation = result[1]
				conn.close()
				if vehicles == 'False' or occupation == 'False':
					bird_traj = '{"vehicles":false, "occupation": false}'
				else:
					bird_traj = '{"vehicles":' + vehicles + ', "occupation": ' + occupation + '}'

				bird_traj = bird_traj.encode('utf-8')
				bird_traj = gzip.compress(bird_traj)
			except:
				bird_traj = 'Error while querying the database'

			response = HttpResponse(bird_traj)
			response['Content-Encoding'] = 'gzip'
			return response

		elif request.GET.get('action', '') == 'set_cookie':
			sim_name = request.GET.get('sim_name', '')
			response = HttpResponse('Cookie')
			response.set_cookie(key = 'sim_name', value = sim_name)
			return response

		elif request.GET.get('action', '') == 'redirect':
			redirection = request.GET.get('redirection', '')
			return HttpResponse(reverse('pointqanalysis:' + redirection))

		elif request.GET.get('action', '') == 'get_from_node':
			node_id = request.GET.get('node_id', '')
			type_anal = request.GET.get('type', '')
			if type_anal == 'flow':
				answer = tools_json.json_get_output_links(node_id)
			return HttpResponse(json.dumps(answer,indent=4), content_type="application/json")

		elif request.GET.get('action', '') == 'list_vehicle_traj':
			ori_link = request.GET.get('ori_link', '')
			dest_link = request.GET.get('dest_link', '')
			sim_name = request.COOKIES['sim_name']
			answer = tools_sql.list_vehicle_traj(ori_link, dest_link, sim_name, 'pointq_db')
			dic_routes = answer[0]
			time =  answer[1]
			output = [[list(x), dic_routes[x][0], dic_routes[x][1]] for x in  dic_routes.keys()]
			json_output = json.dumps({'routes': output, 'time': time})
			return HttpResponse(json_output, content_type="application/json")

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

				# which network is associated with the simulation
				query_1 = 'SELECT name_network FROM index_simul_network WHERE name_simul = \'' + str(sim_name) + '\''
				associated_network = tools_data.query_sql([query_1], True, 'network_db')[0]['name_network']

				# get the top_json associated with the simulation
				query_2 = 'SELECT topjson FROM index_network WHERE name = \'' + str(associated_network) + '\''
				topjson = tools_data.query_sql([query_2], True, 'network_db')[0]['topjson']

				for link_id in list_links:
					data.append(tools_json.json_plot_flow(link_id, t_start, t_end, granul, sim_name, topjson))

				title = {'text': 'Flows'}
				axisX = {'title': "Time interval [s]", 'titleFontWeight': "lighter", 'titleFontSize': '17'}
				axisY = {'title': "Flow [veh per interval]", 'titleFontWeight': "lighter", 'titleFontSize': '17'}
				answer = {'title': title, 'exportEnabled': 'true', 'axisX': axisX, 'axisY': axisY, 'data': data}
				return HttpResponse(json.dumps(answer, indent=4), content_type="application/json")

			# second case : queues
			elif type_anal == 'queue':
				link_occupancy = request.GET.get('link_occupancy', '')
				sep_queues_origin = request.GET.get('sep_queues_origin', '')
				queues = request.GET.get('queues', '')
				list_queues = queues.split('-')
				queues_occupancy = {}
				queues_origin = []

				list_queues_treated = []
				for queue in list_queues:
					list_queues_treated.append('[' + queue.split('.')[0] + ', ' + queue.split('.')[1] + ']')

				if link_occupancy == 'true':
					list_first_link = []
					for queue in list_queues_treated:
						list_first_link.append(queue.split(',')[0][1:])

					list_first_link_occupancy = set()
					for first_link in list_first_link:
						if (list_first_link.count(first_link) > 1):
							list_first_link_occupancy.add(first_link)

					for link in list_first_link_occupancy:
						queues_occupancy[link] = []

					for queue in list_queues_treated:
						first_link = queue.split(',')[0][1:]
						second_link = int(queue.split(',')[1][:-1])
						if first_link in list_first_link_occupancy:
							queues_occupancy[first_link].append(second_link)

					# we delete keys of queues occupancy from list_queus treated
					# queues_occupancy -> we want to plot the total occupancy of a link
					# list_queues_treated -> we want to plot independant queues
					
					list_queues_treated = [x for x in list_queues_treated if x.split(',')[0][1:] not in queues_occupancy.keys()]

				elif sep_queues_origin == 'true':
					# we reset list_queues_treated
					list_queues_treated = []

					# we create the string to plot queues without any separation
					for queue in list_queues:
						list_queues_treated.append('[' + queue.split('.')[1] + ', ' + queue.split('.')[2] + ']')

					# we create an array to plot origin based separated queues
					for queue in list_queues:
						temp = []
						temp.append(queue.split('.')[0])
						temp.append(queue.split('.')[1])
						temp.append(queue.split('.')[2])
						queues_origin.append(temp)

				data = []

				# we generate the plots for independant queues
				for queue in list_queues_treated:
					data.append(tools_json.json_plot_queue(queue, t_start, t_end, sim_name))

				# we generate the plots for the total occupancy of links
				if link_occupancy == 'true':
					list_series = tools_json.json_plot_link_occupancy(queues_occupancy, t_start, t_end, sim_name)

					for serie in list_series:
						data.append(serie)

				# we generate the plots for origin based queues
				if sep_queues_origin == 'true':
					for queue in queues_origin:
						data.append(tools_json.json_plot_queue_origin(queue, t_start, t_end, sim_name))

				title = {'text': 'Queues'}
				axisX = {'title': "Time [s]", 'titleFontWeight': "lighter", 'titleFontSize': '17'}
				axisY = {'title': "Queue length [veh]", 'titleFontWeight': "lighter", 'titleFontSize': '17'}
				answer = {'zoomEnabled': 'true', 'exportEnabled': 'true', 'title': title, 'axisX': axisX, 'axisY': axisY, 'data': data}
				return HttpResponse(json.dumps(answer, indent=4), content_type="application/json")
			#last case :  ODs
			elif type_anal == 'OD':
				pairs = request.GET.get('ODs', '')
				list_pairs = pairs.split('-')
				list_pairs_treated = []
				for pair in list_pairs:
					list_pairs_treated.append(pair.split('.'))

				data=[]
				for pair in list_pairs_treated:
					data.append(tools_json.json_plot_TT(int(pair[0]), int(pair[1]), t_start, t_end, sim_name))
				title = {'text': 'Travel Time'}
				axisX = {'title': "Entry Time [s]", 'titleFontWeight': "lighter", 'titleFontSize': '17'}
				axisY = {'title': "Travel Time [s]", 'titleFontWeight': "lighter", 'titleFontSize': '17'}
				answer = {'zoomEnabled': 'true', 'exportEnabled': 'true', 'title': title, 'axisX': axisX, 'axisY': axisY, 'data': data}
				return HttpResponse(json.dumps(answer, indent=4), content_type="application/json")

		else:
			return False
		

def analysis(request):
	#First step : create a list of the available links:
	try:
		if request.COOKIES['sim_name'].lower() in tools_sql.list_sim_db():

			# we create maxtimesim
			sim_name = request.COOKIES['sim_name']
			query = 'SELECT MAX(ev_time) AS max_time FROM ' + sim_name
			output = tools_data.query_sql([query], True, 'pointq_db')
			maxtimesim = int(round(output[0]['max_time']))

			# which network is associated with the simulation
			query_1 = 'SELECT name_network FROM index_simul_network WHERE name_simul = \'' + str(sim_name) + '\''
			associated_network = tools_data.query_sql([query_1], True, 'network_db')[0]['name_network']

			# we load the geojson of the associated network
			query_2 = 'SELECT geojson FROM index_network WHERE name = \'' + str(associated_network) + '\''
			geojson_associated_network = tools_data.query_sql([query_2], True, 'network_db')[0]['geojson']

			# we load the topology json of the associated network
			query_3 = 'SELECT topjson FROM index_network WHERE name = \'' + str(associated_network) + '\''
			topjson_associated_network = tools_data.query_sql([query_3], True, 'network_db')[0]['topjson']
			template = loader.get_template('pointqanalysis/index.html')
			context = RequestContext(request, {'maxtimesim': maxtimesim, 'geojson': geojson_associated_network, 'topjson':topjson_associated_network, 'sim_name': sim_name})

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
			name_simul = re.sub('[^a-zA-Z0-9]', '_', name_simul).lower()
			desc_simul = form.cleaned_data['description_simul']
			name_network = form.cleaned_data['name_network']
			date = time.strftime("%m/%d/%Y")

			# we save the upload
			tools_data.save_file(request.FILES['simul_txt_db'], name_simul , '/upload/txt_db', '.txt')
			status = 'Thanks for uploading the text database'

			# we convert the db
			tools_sql.treat_simul_db(name_simul , '/upload/txt_db')

			# we create the table index_network if it's not created
			query_1 = 'CREATE TABLE index_simul_network (name_simul text, name_network text, desc_simul text, date_simul text, bird_occupation text, bird_traj text)'
			tools_data.query_sql([query_1], False, 'network_db')

			# we insert a new row in index_network
			query_2 = 'INSERT INTO index_simul_network VALUES (\'' + name_simul + '\',\'' + name_network+ '\',\'' + desc_simul + '\',\'' + date+ '\' ,\'False\',\'False\')'
			tools_data.query_sql([query_2], False, 'network_db')

			# we delete the upload
			os.remove(settings.MEDIA_ROOT + '/upload/txt_db/' + str(name_simul) + '.txt')

			# we create the aynchronous request for the birdeye view
			birdeye.delay(name_network, name_simul)
			birdeye_micro.delay(name_network, name_simul)

			json_simulations = tools_json.json_list_simulations()

		else:
			status = ''
			json_simulations = tools_json.json_list_simulations()
	# Else: the request is type GET: we print the form
	else:
		form = Form_upload_fil()
		status =''
		json_simulations = tools_json.json_list_simulations()

	template = loader.get_template('pointqanalysis/upload.html')
	context = RequestContext(request, {'form': form, 'status':status,'json_simulations': json_simulations, 'upload_xml': reverse('pointqanalysis:upload_xml')})
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
			tools_data.save_file(request.FILES['network_xml'], name_network , '/upload/network_xml', '.xml')

			# we convert the network
			tools_sql.treat_network_db(name_network, '/upload/network_xml')

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
			tools_data.query_sql([query], False, 'network_db')

			status = 'posted'


	# Else: the request is type GET: we print the form
	else:
		form = Form_upload_xml()
		form2 = Form_delete_xml()

	template = loader.get_template('pointqanalysis/uploadxml.html')
	context = RequestContext(request, {'form': form, 'form2': form2, 'status': status})
	return HttpResponse(template.render(context))

def vehtraj(request):
	try:
		if request.COOKIES['sim_name'].lower() in tools_sql.list_sim_db():

			sim_name = request.COOKIES['sim_name']

			# we create maxtimesim
			sim_name = request.COOKIES['sim_name']
			query = 'SELECT MAX(ev_time) AS max_time FROM ' + sim_name
			output = tools_data.query_sql([query], True, 'pointq_db')
			maxtimesim = int(round(output[0]['max_time']))

			# which network is associated with the simulation
			query_1 = 'SELECT name_network FROM index_simul_network WHERE name_simul = \'' + str(sim_name) + '\''
			associated_network = tools_data.query_sql([query_1], True, 'network_db')[0]['name_network']

			# we load the geojson of the associated network
			query_2 = 'SELECT geojson FROM index_network WHERE name = \'' + str(associated_network) + '\''
			geojson_associated_network = tools_data.query_sql([query_2], True, 'network_db')[0]['geojson']

			# we load the topology json of the associated network
			query_3 = 'SELECT topjson FROM index_network WHERE name = \'' + str(associated_network) + '\''
			topjson_associated_network = tools_data.query_sql([query_3], True, 'network_db')[0]['topjson']

			template = loader.get_template('pointqanalysis/vehicle_traj.html')
			context = RequestContext(request, {'geojson': geojson_associated_network, 'topjson':topjson_associated_network, 'maxtimesim':maxtimesim, 'sim_name': sim_name})

			return HttpResponse(template.render(context))
		else:
			return HttpResponseRedirect(reverse('pointqanalysis:simulations'))

			
	except:
		return HttpResponseRedirect(reverse('pointqanalysis:simulations'))

def dashboard(request):
	try:
		if request.COOKIES['sim_name'].lower() in tools_sql.list_sim_db():

			sim_name = request.COOKIES['sim_name'].lower()

			# we create maxtimesim
			sim_name = request.COOKIES['sim_name']
			query = 'SELECT MAX(ev_time) AS max_time FROM ' + sim_name
			output = tools_data.query_sql([query], True, 'pointq_db')
			maxtimesim = int(round(output[0]['max_time']))

			# which network is associated with the simulation
			query_1 = 'SELECT name_network FROM index_simul_network WHERE name_simul = \'' + str(sim_name) + '\''
			associated_network = tools_data.query_sql([query_1], True, 'network_db')[0]['name_network']

			# we load the geojson of the associated network
			query_2 = 'SELECT geojson FROM index_network WHERE name = \'' + str(associated_network) + '\''
			geojson_associated_network = tools_data.query_sql([query_2], True, 'network_db')[0]['geojson']

			# # we load the birdeye json
			# query_4 = 'SELECT bird_occupation FROM index_simul_network WHERE name_simul = \'' + str(sim_name) + '\''
			# json_birdeye = tools_data.query_sql([query_4], True, 'network_db')[0]['bird_occupation']

			# if json_birdeye == 'False':
			# 	json_birdeye = True

			template = loader.get_template('pointqanalysis/dashboard.html')
			context = RequestContext(request, {'geojson': geojson_associated_network, 'maxtimesim':maxtimesim, 'sim_name': sim_name})

			return HttpResponse(template.render(context))
		else:
			return HttpResponseRedirect(reverse('pointqanalysis:simulations'))

			
	except:
		return HttpResponseRedirect(reverse('pointqanalysis:simulations'))
