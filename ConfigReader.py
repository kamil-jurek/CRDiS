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
        #b={elem[0]:elem[1]}
        config[elem[0]] = elem[1]
    config_list.append(config)

print config_list[0]['probability']

curr_state = max([abs(int(float(config_list[i]['from']))) for i in range(len(config_list)) if 'from' in config_list[i]])*2
last_state = curr_state + curr_state/2

seqs = []
f, axarr = plt.subplots(len(config_list))
j = 0
for config in config_list:
    domain = ast.literal_eval(config['domain'])
    value = ast.literal_eval(config['arg']) #.replace("'","")
    operator = 'eq'
    probability = float(config['probability'])
    fr = curr_state-curr_state
    to = curr_state-last_state

    if 'from' in config:
        fr = abs(int(float(config['from'])))
        if to == 0:
            to = abs(int(float(config['to'])))

    seq0 = [domain[0] for i in range(0, last_state)]
    seq = sg.generateSequence(seq0, domain, value, operator, probability, curr_state-fr, curr_state-to)
    sg.plotSequence(axarr[j], seq, domain, value, curr_state)
    j += 1

plt.show()
