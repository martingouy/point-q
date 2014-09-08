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
	cursor.execute('CREATE TABLE ' + name + ' (ev_time real, ev_type int, veh_id int, c_link int, queue text, time_entry real, entry_id int, time_exit int, c_loc_link int)')
	#cursor.execute('CREATE TABLE ' + name + ' (ev_time real, ev_type int, veh_id int, c_link int, queue text)')
	conn.commit()

	# Conversion from csv to sqlite
	with open('%s/%s' % (settings.MEDIA_ROOT + str(path), str(name) + '.txt'), 'rb') as file:
		reader = csv.reader(file)
		for row in reader:
			if len(row)==9:
				#cursor.execute("INSERT INTO " + name + " VALUES (" + row[0] + " ," + row[1] + " ," + row[2] + " ," + row[3] + " ,'" + row[4] + "')")
				cursor.execute("INSERT INTO " + name + " VALUES (" + row[0] + " ," + row[1] + " ," + row[2] + " ," + row[3] + " ,'" + row[4] + "' ," + row[5] + " ," + row[6] + " ," + row[7] + " ," + row[8] + ")")
			else:
				#There's a typo in Jenny's Docs: Column 25 contains the id of the link associated with the current event. Due to 0-based indexing, it appears at 24 here
				#NOTE that there's a difference between Column 25 (id of link associated with current event) and Column 15(id of link where the vehicle is currently located)
				#cursor.execute("INSERT INTO " + name + " VALUES (" + row[0] + " ," + row[1] + " ," + row[11] + " ," + row[24] + " ,'" + row[18] + "')")
				cursor.execute("INSERT INTO " + name + " VALUES (" + row[0] + " ," + row[1] + " ," + row[11] + " ," + row[24] + " ,'" + row[18] + "' ," + row[12] + " ," + row[13] + " ," + row[23] + " ," + row[14] + ")")
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
