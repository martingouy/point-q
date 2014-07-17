from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
import os
import pygal
from pygal.style import DarkSolarizedStyle

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