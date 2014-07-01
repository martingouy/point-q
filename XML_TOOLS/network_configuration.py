# import xml / excel tools library
from xml.dom import minidom
from xlwt import Workbook

# creates lists links/nodes xml elements
xmldoc = minidom.parse('network.xml')
xml_nodelist = xmldoc.getElementsByTagName('node') 
xml_linklist = xmldoc.getElementsByTagName('link') 

# creates excel Workbook
network = Workbook()

# creates new sets for links
all_links_set = set()
in_links_set = set()
out_links_set = set()
intern_links_set = set()
out_network_nodes = set()

# determines nodes out of the network
for s in xml_nodelist :
  for t in s.getElementsByTagName('output'):
    if t.attributes['link_id'].value == '-1':
      out_network_nodes.add(s.attributes['id'].value)
  for t in s.getElementsByTagName('input'):
    if t.attributes['link_id'].value == '-1':
      out_network_nodes.add(s.attributes['id'].value)

# determines out links
for s in xml_nodelist :
  for t in s.getElementsByTagName('output'):
    if t.attributes['link_id'].value == '-1':
      for u in s.getElementsByTagName('input'):
        out_links_set.add(u.attributes['link_id'].value)

# determines in links
for s in xml_nodelist :
  for t in s.getElementsByTagName('input'):
    if t.attributes['link_id'].value == '-1':
      for u in s.getElementsByTagName('output'):
        in_links_set.add(u.attributes['link_id'].value)
# determines intern links        
for s in xml_linklist :
  all_links_set.add(s.attributes['id'].value)

intern_links_set = all_links_set.difference(in_links_set)
intern_links_set = intern_links_set.difference(out_links_set)


#################################################
# File 1: fi_demand_param_entry_link            #
#################################################

sheet1 = network.add_sheet('1')
row_nb = 0

for s in xml_linklist:
  if s.attributes['id'].value in in_links_set:
   sheet1.write(row_nb, 0, int(s.attributes['id'].value))
   row_nb += 1

# saves the workbook
network.save('network.xls')


##############################################################################################################
# File 2: fi_id_all_network_link_id_orig_dest_node_length_link_capacity_link_param_travel_duration           #
##############################################################################################################

sheet2 = network.add_sheet('2')
row_nb = 0

for s in xml_linklist:
  if s.attributes['id'].value in in_links_set:
    sheet2.write(row_nb, 0, int(s.attributes['id'].value))
    sheet2.write(row_nb, 1, -1)
    sheet2.write(row_nb, 2, int(s.getElementsByTagName('end')[0].attributes['node_id'].value))
    sheet2.write(row_nb, 3, float(s.attributes['length'].value))
    sheet2.write(row_nb, 4, 0)
    # Hypothesis: mean speed : 30 miles/hour
    sheet2.write(row_nb, 5, float(s.attributes['length'].value) / 13.4112)
  elif s.attributes['id'].value in out_links_set:
    sheet2.write(row_nb, 0, int(s.attributes['id'].value))
    sheet2.write(row_nb, 1, int(s.getElementsByTagName('begin')[0].attributes['node_id'].value))
    sheet2.write(row_nb, 2, -1)
    sheet2.write(row_nb, 3, float(s.attributes['length'].value))
    sheet2.write(row_nb, 4, 0)
    # Hypothesis: mean speed : 30 miles/hour
    sheet2.write(row_nb, 5, float(s.attributes['length'].value) / 13.4112)
  else:
    sheet2.write(row_nb, 0, int(s.attributes['id'].value))
    sheet2.write(row_nb, 1, int(s.getElementsByTagName('begin')[0].attributes['node_id'].value))
    sheet2.write(row_nb, 2, int(s.getElementsByTagName('end')[0].attributes['node_id'].value))
    sheet2.write(row_nb, 3, float(s.attributes['length'].value))
    # Hypothesis: mean vehicule length = 7m
    sheet2.write(row_nb, 4, int(float(s.attributes['length'].value) / 7))
    # Hypothesis: mean speed = 30 miles/hour
    sheet2.write(row_nb, 5, float(s.attributes['length'].value) / 13.4112)

  sheet2.flush_row_data()
  row_nb += 1

# saves the workbook
network.save('network.xls')


##########################################################################
# File 3: fi id all phases max queue size sat flow queue type           #
#########################################################################

# creates the sheet in the network xls file

sheet3 = network.add_sheet('3')

row_nb = 1
sheet3.write(0, 0, 'incoming link')
sheet3.write(0, 1, 'outcoming link')
sheet3.write(0, 2, 'max alllowed size of queue')
sheet3.write(0, 3, 'saturation flow')
sheet3.write(0, 4, 'type')

for s in xml_nodelist:
  if not s.attributes['id'].value in out_network_nodes:
    for t in s.getElementsByTagName('input'):
      for u in s.getElementsByTagName('output'):
        sheet3.write(row_nb, 0, int(t.attributes['link_id'].value))
        sheet3.write(row_nb, 1, int(u.attributes['link_id'].value))
        sheet3.write(row_nb, 2, -1)
        sheet3.write(row_nb, 3, 0.5)
        sheet3.write(row_nb, 4, 1)
        row_nb += 1


    # flushes the memory
    sheet3.flush_row_data()


# saves the workbook
network.save('network.xls')

#################################################
# File 5: fi_id_internal_link_id_orig_dest_node #
#################################################

sheet5 = network.add_sheet('5')
row_nb = 0

for s in xml_linklist:
  if s.attributes['id'].value in intern_links_set:
    sheet5.write(row_nb, 0, int(s.attributes['id'].value))
    sheet5.write(row_nb, 1, int(s.getElementsByTagName('begin')[0].attributes['node_id'].value))
    sheet5.write(row_nb, 2, int(s.getElementsByTagName('end')[0].attributes['node_id'].value))
    row_nb += 1
  
# saves the workbook
network.save('network.xls')
    

#############################################
# File 7: fi_id_node_entering_links_to_node #
#############################################

# creates the sheet in the network xls file

sheet7 = network.add_sheet('7')

row_nb = 0

for s in xml_nodelist :
  column_nb = 1 
  
  if not s.attributes['id'].value in out_network_nodes:  
    sheet7.write(row_nb, 0, int(s.attributes['id'].value))
    
    for t in s.getElementsByTagName('input'):      
      sheet7.write(row_nb, column_nb, int(t.attributes['link_id'].value))
      column_nb = column_nb + 1  
      
    # flushes the memory
    sheet7.flush_row_data()
    row_nb = row_nb + 1

# saves the workbook
network.save('network.xls')

################################################
# File 8: fi_id_node_id_entry_links_to_network #
################################################

# creates the sheet in the network workbook

sheet8 = network.add_sheet('8')

row_nb = 0

for s in xml_nodelist :
  entry_links = False
  column_nb = 1
  
  if not s.attributes['id'].value in out_network_nodes:
    for t in s.getElementsByTagName('input'):
      if t.attributes['link_id'].value in in_links_set:
        sheet8.write(row_nb, column_nb, int(t.attributes['link_id'].value))
        column_nb = column_nb + 1
        entry_links = True
      
    if entry_links:
      sheet8.write(row_nb, 0, int(s.attributes['id'].value))
  
      # flushes the memory
      sheet8.flush_row_data()
      row_nb = row_nb + 1

# saves the workbook
network.save('network.xls')

##########################################################
# File 9: fi_id_node_id_exit_links_from_network          #
##########################################################

# creates the sheet in the network workbook

sheet9 = network.add_sheet('9')

row_nb = 0

for s in xml_nodelist :
  exit_links = False
  column_nb = 1
  
  if not s.attributes['id'].value in out_network_nodes:
    for t in s.getElementsByTagName('output'):
      if t.attributes['link_id'].value in out_links_set:
        sheet9.write(row_nb, column_nb, int(t.attributes['link_id'].value))
        column_nb = column_nb + 1
        exit_links = True
      
    if exit_links:
      sheet9.write(row_nb, 0, int(s.attributes['id'].value))
  
      # flushes the memory
      sheet9.flush_row_data()
      row_nb = row_nb + 1

# saves the workbook
network.save('network.xls')


##########################################################
# File 10: fi_id_node_id_leaving_links_from_node         #
##########################################################

# creates the sheet in the network workbook

sheet10 = network.add_sheet('10')

row_nb = 0

for s in xml_nodelist :
  column_nb = 1
  
  if not s.attributes['id'].value in out_network_nodes:
    sheet10.write(row_nb, 0, int(s.attributes['id'].value))
    for t in s.getElementsByTagName('output'): 
      sheet10.write(row_nb, column_nb, int(t.attributes['link_id'].value))
      column_nb = column_nb + 1      
  
    # flushes the memory
    sheet10.flush_row_data()
    row_nb = row_nb + 1

# saves the workbook
network.save('network.xls')

##########################################################
# File 11: fi_id_node_type_node                          #
##########################################################

sheet11 = network.add_sheet('11')

row_nb = 0

for s in xml_nodelist :

  if not s.attributes['id'].value in out_network_nodes:
    sheet11.write(row_nb, 0, int(s.attributes['id'].value))
    row_nb = row_nb + 1

# saves the workbook
network.save('network.xls')

##########################################################
# File 13: fi_mrp_cum                                    #
##########################################################

sheet13 = network.add_sheet('13')
sheet13.write(0, 0, 'input link')
sheet13.write(0, 1, 'output link')
sheet13.write(0, 2, 'cumulative probability')
row_nb = 1

for s in xml_nodelist:
  if not s.attributes['id'].value in out_network_nodes:
    for t in s.getElementsByTagName('input'):
      for u in s.getElementsByTagName('output'):
        sheet13.write(row_nb, 0, int(t.attributes['link_id'].value))
        sheet13.write(row_nb, 1, int(u.attributes['link_id'].value))
        row_nb += 1
      sheet13.flush_row_data()

network.save('network.xls')

##########################################################
# File 20: fi_stages_each_sign_inters                    #
##########################################################

sheet20 = network.add_sheet('20')
sheet20.write(0,0, 'node id')
row_nb = 1

for s in xml_nodelist:
  if not s.attributes['id'].value in out_network_nodes:
    sheet20.write(row_nb, 0, int(s.attributes['id'].value))
    row_nb += 1
  sheet20.flush_row_data()

network.save('network.xls')
