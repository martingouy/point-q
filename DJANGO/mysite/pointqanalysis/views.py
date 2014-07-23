from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.shortcuts import render_to_response
from forms import Form_upload_fil
from lxml import etree
import sqlite3
import os
import csv
import pygal
from pygal.style import DarkSolarizedStyle
from django.db import connections
from django.conf import settings


def dictfetchall(cursor):
	desc = cursor.description
	return [
	    dict(zip([col[0] for col in desc], row))
	    for row in cursor.fetchall()
	]

def save_file(file, name, path=''):
	fd = open('%s/%s' % (settings.MEDIA_ROOT + str(path), str(name) + '.txt'), 'wb')
	for chunk in file.chunks():
		fd.write(chunk)
	fd.close()

def list_sim_db():
	# we create the xml doc to store the list
	root = etree.Element('root')

	# connection database
	conn = sqlite3.connect(r"/Users/martingouy/Desktop/Martin/GitHub/point-q/DJANGO/mysite/pointq_db.sqlite3")
	cursor = conn.cursor()

	# query
	cursor.execute('SELECT name FROM SQLITE_MASTER WHERE type=\'table\' ORDER BY name')
	for line in dictfetchall(cursor):
		sim = etree.Element('sim')
		sim.text = line['name']
		root.append(sim)

	conn.close()
	#return xml
	xml = etree.tostring(root)
	return xml

def treat_simul_db(name, path):

	conn = sqlite3.connect(r"/Users/martingouy/Desktop/Martin/GitHub/point-q/DJANGO/mysite/pointq_db.sqlite3")
	cursor = conn.cursor()
	name = str(name).lower()

	# We create the table
	#cursor.execute('DROP TABLE ' + name)
	cursor.execute('CREATE TABLE ' + name + ' (ev_time real, ev_type int, veh_id int)')
	conn.commit()

	# Conversion from csv to sqlite
	with open('%s/%s' % (settings.MEDIA_ROOT + str(path), str(name) + '.txt'), 'rb') as file:
		reader = csv.reader(file)
		for row in reader:
			cursor.execute("INSERT INTO " + name + " VALUES (" + row[0] + " ," + row[1] + " ," + row[11] + " )")
		conn.commit()

	conn.close()


def ajax(request):
	if request.GET.get('action', '') == 'listsim':
		xml = list_sim_db()
		return HttpResponse(xml)
	else:
		return False
	

def index(request):
	# First step : create a list of the available links:
	list_links = []
	path = '/Users/martingouy/Desktop/Django/QUE_EVOL'
	for file in os.listdir(path):
	  	if file.endswith(".txt"):
	    		line_split = file[13:-5].split(',')
	    		list_links.append([int(line_split[0]), int(line_split[1])])
	template = loader.get_template('pointqanalysis/index.html')
    	context = RequestContext(request, {'list_queues': list_links})
    	return HttpResponse(template.render(context))

def upload(request):
	if request.method == 'POST':
	    form = Form_upload_fil(request.POST, request.FILES)
	    if form.is_valid() and form.is_multipart():
		name = form.cleaned_data['name']
		save_file(request.FILES['simul_txt_db'], name , '/txt_db')
		status = 'Thanks for uploading the text database'
		treat_simul_db(name , '/txt_db')
	    else:
		status = ''
	else:
		form = Form_upload_fil()
		status =''

	template = loader.get_template('pointqanalysis/upload.html')
    	context = RequestContext(request, {'form': form, 'status':status})
	return HttpResponse(template.render(context))
 
def avail_databases(request):
	cursor = connections['pointq_db'].cursor()

	list_sim = []
	cursor.execute("SELECT * FROM simul1 WHERE veh_id = 1")
	for line in dictfetchall(cursor):
		list_sim.append(line['ev_time'])

	template = loader.get_template('pointqanalysis/avail_db.html')
    	context = RequestContext(request, {'list_db': list_sim})
    	return HttpResponse(template.render(context))

def detail(request, link1, link2):
	list_que_evol = []
	with open('/Users/martingouy/Desktop/Django/QUE_EVOL/fi_evol_que_(' + str(link1) + ', '+ str(link2) +').txt', 'rU') as f:
		count = 0
		for line in f:
			if line[0] != 'Q' :
				line_split = line.split('\t')
				if float(line_split[0]) < 2000:
					list_que_evol.append((float(line_split[0]), int(line_split[1])))
			count += 1

	line_chart = pygal.XY(style = DarkSolarizedStyle, disable_xml_declaration = True)
	line_chart.title = 'Queue ' + '(' + str(link1) +', ' + str(link2) + ') evolution : '
	line_chart.add('(' + str(link1) +', ' + str(link2) + ')', list_que_evol)
	svg = line_chart.render()
	return HttpResponse(svg)