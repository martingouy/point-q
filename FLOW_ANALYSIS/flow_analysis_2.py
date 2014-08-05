import os

# we open output link from network file
count = 0
link_1 = 200021
link2 = 200020
link_1 = str(link_1)
link2 = str(link2)
ratio = 1

with open('/Users/martingouy/Desktop/Martin/GitHub/point-q-dev/sim_1/cc/Series_Sim-Mon-14-Jul-2014_15-53-50/FRes-Mon-14-Jul-2014_15-53-50/Stat_Anal/QUE_EVOL/fi_evol_que_(' + link_1 + ', '+ link2 +').txt', 'rU') as f:
  for line in f:
    line_split = line.split('\t')
    if len(line_split) > 2:
      if int(line_split[2]) == 4:
        count += 1

print count
print count * 3600 / 1200 / ratio

