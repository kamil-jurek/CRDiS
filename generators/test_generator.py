# The MIT License
# Copyright (c) 2018 Kamil Jurek
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from generators import sequence_generator as sg
import matplotlib.pyplot as plt

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

plt.show()

