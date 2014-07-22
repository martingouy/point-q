from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.shortcuts import render_to_response
from forms import Form_upload_fil
import os
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
	        save_file(request.FILES['simul_txt_db'], '/txt_db')
	        status = 'Thanks for uploading the text database'
	    else:
	        status = ''
	else:
	    form = Form_upload_fil()
	    status =''

	template = loader.get_template('pointqanalysis/upload.html')
    	context = RequestContext(request, {'form': form, 'status':status})
	return HttpResponse(template.render(context))
 
def save_file(file, path=''):
	filename = file._get_name()
	fd = open('%s/%s' % (settings.MEDIA_ROOT + str(path), str(filename)), 'wb')
	for chunk in file.chunks():
	    fd.write(chunk)
	fd.close()


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