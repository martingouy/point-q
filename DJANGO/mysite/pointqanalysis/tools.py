###################################################################################################################
###                                       TOOL FUNCTIONS														   ###
###################################################################################################################
import sqlite3

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