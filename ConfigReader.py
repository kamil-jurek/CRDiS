import SequenceGenerator as sg
import matplotlib.pyplot as plt
import numpy
import math
import ast

with open('config') as f:
    lines = f.readlines()

config_list = []
for line in lines:
    line = line.replace(" ", "").replace("\n", "")
    config = {}
    for elem in line.split(';'):
        elem = elem.split('=')
        config[elem[0]] = elem[1]
    config_list.append(config)

li = []
for config in config_list:
    key = config['attr'].replace("'","")
    if not any(key in d['attr_name'] for d in li):
        dic = {}
        l = []
        l.append(config)
        dic['attr_name'] = key
        dic['value'] = l
        li.append(dic)
    else:
        di = [d for d in li if d['attr_name'] == key][0]
        di['value'].append(config)
        #print li
curr_state = max([abs(int(float(config_list[i]['from']))) for i in range(len(config_list)) if 'from' in config_list[i]])*2
last_state = curr_state + curr_state/2
seqs = []
k = len(li)
#f, axarr = plt.subplots(k)
j = 0
for config in li:
    cv = config['value']
    init_value = ast.literal_eval(cv[0]['domain'])[0]
    seq = [init_value for k in range(0, last_state)]
    domain = ast.literal_eval(cv[0]['domain'])
    operator = 'eq'
    for z in range(0,len(cv)):
        value = ast.literal_eval(cv[z]['value'])
        probability = float(cv[z]['probability'])
        fr = curr_state-curr_state
        to = curr_state-last_state
        if 'from' in cv[z]:
             fr = abs(int(float(cv[z]['from'])))
             if cv[z]['to'] != '0':
                 to = abs(int(float(cv[z]['to'])))

        seq = sg.generateSequence(seq, domain, value, operator, probability, curr_state-fr, curr_state-to)
        #sg.plotSequence(axarr[j], seq, domain, config['attr_name'], curr_state)
    j += 1
    seqs.append(seq)

#plt.show()
import csv
import time

timestr = time.strftime("%Y_%m_%d-%H:%M:%S")
with open('sequence_'+timestr+'.csv','wb') as csv_file:
    writer = csv.writer(csv_file, delimiter=',')
    writer.writerow([l['attr_name'] for l in li])
    for i in range(len(seqs[0])):
        writer.writerow([s[i] for s in seqs])
