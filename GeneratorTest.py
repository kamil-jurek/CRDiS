import SequenceGenerator as sg
import matplotlib.pyplot as plt
import numpy
import math

domain1 = ['a', 'b','z']
domain2 = ['c', 'd']
domain3 = ['e', 'f']

states_len = [40, 30]
curr_state = max(states_len)*2
last_state = curr_state + max(states_len)

seq01 = ['a' for i in range(0, last_state)]
seq1 = sg.generateSequence(seq01, domain1, 'b','eq',0.9, curr_state-states_len[0], last_state)
seq1 = sg.generateSequence(seq1, domain1, 'z','eq',0.8, curr_state-60, curr_state-40)

seq02 = ['c' for i in range(0, last_state)]
seq2 = sg.generateSequence(seq02, domain2,'d','eq',0.9, curr_state-states_len[1], last_state)

seq03 = ['e' for i in range(0, last_state)]
seq3 = sg.generateSequence(seq03, domain3,'f','eq',1.0, curr_state, last_state)

f, axarr = plt.subplots(3)

sg.plotSequence(axarr[0], seq1, domain1, '1', curr_state)
sg.plotSequence(axarr[1], seq2, domain2, '2', curr_state)
sg.plotSequence(axarr[2], seq3, domain3, '3', curr_state)

#f.set_size_inches(w=10,h=5)
plt.show()
