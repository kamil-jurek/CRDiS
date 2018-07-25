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


import numpy
import math
import csv
import time
import matplotlib.pyplot as plt

def generateSequence(sequence, domain, value, operator, probability, fr, to):
    if operator == 'eq':
        prob = [(1.0 - probability) / (len(domain) - 1) for i in domain]
        prob[domain.index(value)] = probability
        seq = list(sequence)
        for i in range(fr, to):
            seq[i] = numpy.random.choice(domain, p = prob)

        return seq

def testSequence(seq, value, prob):
    counter = seq.count(value)

    print("Should be about: ", len(seq)*prob)
    print("Is: ", counter)

def plotSequence(axarr, seq, domain, attrName, curr_state):
    N = 1
    colors = [numpy.random.rand(1,3) for i in domain]
    ind = numpy.arange(N)    # the x locations for the groups

    p = [0 for i in domain]
    for i in range(0, len(seq)):
        for j in range(0, len(domain)):
            if seq[i] == domain[j]:
                p[j] = axarr.barh(ind, 1, left=i, color=colors[j] )

    axarr.set_xlabel('State nr')
    axarr.set_ylabel(str(attrName))
    axarr.set_yticks([])
    axarr.set_yticklabels(['Attr_1'])

    step = determine_step(seq)

    axarr.set_xticks(numpy.arange(0, len(seq) + 1, step), minor=False)
    #print(numpy.arange(0, len(seq) + 1, step))
    axarr.set_xticklabels(numpy.arange(-curr_state, len(seq)-curr_state+1, step),minor=False)
    #print(numpy.arange(-curr_state, len(seq)-curr_state+1, step))

    axarr.legend((p), (domain))


def saveToCsv(listOfConfigs, sequences):
    timestr = time.strftime("%Y_%m_%d-%H.%M.%S")
    filename = '../sequences/sequence_'+timestr+'.csv'
    with open(filename,'w') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        #print(listOfConfigs)
        writer.writerow([config['attr_name'] for config in listOfConfigs])
        for i in range(len(sequences[0])):
            writer.writerow([seq[i] for seq in sequences])
    print(filename)

def determine_step(seq):
    step = 10
    seqLen = len(seq)
    if seqLen <= 50:
        step = 1
    elif seqLen <= 500:
        step = 10
    elif seqLen <= 5000:
        step = 100
    elif seqLen <= 50000:
        step = 1000

    return step