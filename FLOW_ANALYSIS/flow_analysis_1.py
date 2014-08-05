import os

# we create the dictionary

dic_node = {}


def int_list(list):
  # int_list converts each element of a list to an int
  # if the element isn't a number, it will be deleted
  list_suppr = []
  for i in range(len(list)):
    try:
      list[i] = int(list[i])
    except ValueError:
      list_suppr.append(list[i])
  for i in list_suppr:
    list.remove(i)

# we open output link from network file
list_output_links = []
with open('../SMALL_NETWS/huntington_colorado/fi_id_node_id_exit_links_from_network.txt', 'rU') as f:
  for line in f:
    line_split = line.split('\t')
    int_list(line_split)
    for i in line_split[1:]:
      list_output_links.append(i)

# we open node entering links text file

with open('../SMALL_NETWS/huntington_colorado/fi_id_node_id_entering_links_to_node.txt', 'rU') as f:
  for line in f:
    line_split = line.split('\t')
    int_list(line_split)
    dic_node[int(line_split[0])] = {}
    dic_node[int(line_split[0])]['entering'] = line_split[1:]

with open('../SMALL_NETWS/huntington_colorado/fi_id_node_id_leaving_links_from_node.txt', 'rU') as f:
  for line in f:
    line_split = line.split('\t')
    int_list(line_split)
    dic_node[int(line_split[0])]['leaving'] = line_split[1:]


# we create a dictionary with all the link evolution

path = '/Users/martingouy/Desktop/Martin/GitHub/point-q-dev/sim_1/cc/Series_Sim-Wed-09-Jul-2014_23-08-40/FRes-Wed-09-Jul-2014_23-08-40/Stat_Anal/LINK_EVOL'

dic_link = {}

# we list all the link evolution text files
for file in os.listdir(path):
  if file.endswith(".txt"):
    with open(path + '/' + file, 'rU') as f:
      i = 1
      list_evol = []
      for line in f:
        if not line[0] == 'L':
          line_split = line.split('\t')
          list_evol.append([float(line_split[0]), int(line_split[1])])
      dic_link[int(file[len('fi_evol_lk_'):-4])] = list_evol


def index_list(link_id, time):
  index = -1
  for i in range(len(dic_link[link_id])):
    if dic_link[link_id][i][0] <= time:
      index = i
  return index


# we create a function that returns the flow of a given link

def flow(link_id, t_start, t_step, choice):
  count = 0
  index_1 = index_list(link_id, t_start)
  index_2 = index_list(link_id, t_start + t_step)
  if link_id in list_output_links:
    if index_1 == -1 and index_2 == -1:
      count = 0
    elif index_1 == -1 and index_2 >= 0:
      count = dic_link[link_id][index_2][1]
    else:
      count = dic_link[link_id][index_2][1] - dic_link[link_id][index_1][1]
  else:
    if choice == 'leaving':
      if index_1 == -1 and index_2 == -1:
        return 0
      elif index_1 == -1 and index_2 >= 0:
        count = dic_link[link_id][0][1]
        index_1 = 0
      else:
        pass
      if len(dic_link[link_id][index_1:index_2 + 1]) > 1:
        for i in range(index_1, index_2):
          diff = dic_link[link_id][i][1] - dic_link[link_id][i + 1][1]
          if diff < 0:
            count += - diff
    else:
      if index_1 == -1 and index_2 == -1:
        return 0
      elif index_1 == -1 and index_2 >= 0:
        index_1 = 0
      else:
        pass
      if len(dic_link[link_id][index_1:index_2 + 1]) > 1:
        for i in range(index_1, index_2):
          diff = dic_link[link_id][i][1] - dic_link[link_id][i + 1][1]
          if diff > 0:
            count += diff
  return count

# iteration over the nodes

for node in dic_node:
  sum_entering = 0
  sum_leaving = 0
  for entering_link in dic_node[node]['entering']:
    if entering_link in dic_link.keys():
      sum_entering += flow(entering_link, 0, 5000, 'entering')
  for leaving_link in dic_node[node]['leaving']:
    if leaving_link in dic_link.keys():
      sum_leaving += flow(leaving_link, 0, 5000, 'leaving')
  if sum_entering == sum_leaving:
    print ('OK FOR NODE:', node, 'SUM', sum_entering)
  else:
    print ('PROBLEM WITH NODE', node, 'entering', sum_entering, 'leaving', sum_leaving)

# sum = 0
# nb = 0
# while i < 2800:
#
#   sum += flow(200014, i, 200, 'entering')
#   nb += 1
#   i += 200
#
# print nb
# print sum / nb * 18
print flow(100066, 0, 3600, 'entering')
print 'yes'