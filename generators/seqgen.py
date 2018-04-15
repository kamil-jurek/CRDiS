import argparse
import sequence_generator as sg
import matplotlib.pyplot as plt
import numpy
import ast
import time
import random

past_states = 1.0
future_states = 1.5

parser = argparse.ArgumentParser(description='Sequence Generator.')
parser.add_argument('-i','--input', help='Config input file name',required=True)
parser.add_argument('-s','--save', action="store_true", help='Save generated sequence?', default=False, required=False)
parser.add_argument('-p','--plot', action="store_true", help='Plot generated sequence?', default=False, required=False)
parser.add_argument('-r','--random', action="store_true", help='Random initialization?', default=False, required=False)
args = parser.parse_args()

with open(args.input) as f:
    lines = f.readlines()

config_list = []
for line in lines:
    line = line.replace(" ", "").replace("\n", "")
    config = {}
    for elem in line.split(';'):
        elem = elem.split('=')
        config[elem[0]] = elem[1]
    config_list.append(config)

grouped_config_list = []
for config in config_list:
    key = config['attr'].replace("'","")
    if not any(key in d['attr_name'] for d in grouped_config_list):
        attr_dict = {}
        values_list = []
        values_list.append(config)
        attr_dict['attr_name'] = key
        attr_dict['value'] = values_list
        grouped_config_list.append(attr_dict)
    else:
        attr_dict = [d for d in grouped_config_list if d['attr_name'] == key][0]
        attr_dict['value'].append(config)

# for conf in grouped_config_list:
#     for key, value in conf.items():
#         print key,": ", value if key == 'attr_name' else ' '
#         if key != 'attr_name':
#             for v in value:
#                 print "\t", v
#     print

curr_state = int(max([abs(int(float(config_list[i]['from']))) for i in range(len(config_list)) if 'from' in config_list[i]])*past_states)
last_state = int(curr_state+300)
seqs = [[] for i in range(len(grouped_config_list))]
k = len(grouped_config_list)
f, axarr = plt.subplots(k)
j = 0
for x in range(3):
    rand_len = random.randint(1, 3) * 100
    for config_ind, config in enumerate(grouped_config_list):
        config_values = config['value']
        domain = ast.literal_eval(config_values[0]['domain'])
        init_value = domain[0]
        print(init_value)

        if args.random:
            seq = [numpy.random.choice(domain) for k in range(0, last_state)]
        else:
            seq = [init_value for k in range(0, last_state)]

        operator = 'eq'
        for z in range(0,len(config_values)):
            value = ast.literal_eval(config_values[z]['value'])
            probability = float(config_values[z]['probability'])
            fr = curr_state - curr_state
            to = curr_state - last_state
            if 'from' in config_values[z]:
                fr = abs(int(float(config_values[z]['from'])))
                if config_values[z]['to'] != '0':
                    to = abs(int(float(config_values[z]['to'])))
                else:
                    to = 0

            seq = sg.generateSequence(seq, domain, value, operator, probability, curr_state-fr, curr_state-to)

            if(args.plot):
                sg.plotSequence(axarr[j], seq, domain, config['attr_name'], curr_state)
        j += 1
        rand_seq = [numpy.random.choice([0,1]) for i in range(rand_len)]
        seqs[config_ind] = numpy.concatenate((seqs[config_ind], seq))
        seqs[config_ind] = numpy.concatenate((seqs[config_ind], rand_seq))
    #seqs = np.concatenate((seqs, )
if args.plot:
    plt.show()
    timestr = time.strftime("%Y_%m_%d-%H.%M.%S")
    plt.savefig("plots/plot_" + timestr + '.png')

if args.save:
    sg.saveToCsv(grouped_config_list, seqs)
