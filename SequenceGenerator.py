import numpy
import math

def generateSequence(sequence, domain, value, operator, probability, fr, to):
    if operator == 'eq':
        prob = [(1.0 - probability) / (len(domain) - 1) for i in domain]
        prob[domain.index(value)] = probability

        for i in range(fr, to):
            sequence[i] = numpy.random.choice(domain, p = prob)

        return sequence

def testSequence(seq, value, prob):
    counter = seq.count(value)

    print "Should be about: ", len(seq)*prob
    print "Is: ", counter

def plotSequence(axarr, seq, domain, attrName, curr_state):
    N = 1
    colors = [numpy.random.rand(3,1) for i in domain]
    ind = numpy.arange(N)    # the x locations for the groups

    p = [0 for i in domain]
    for i in range(0, len(seq)):
        for j in range(0, len(domain)):
            if seq[i] == domain[j]:
                p[j] = axarr.barh(ind, 1, left=i, color=colors[j] )

    axarr.set_xlabel('State nr')
    axarr.set_ylabel('Attribute '+str(attrName))
    axarr.set_yticks([])
    axarr.set_yticklabels(['Attr_1'])

    axarr.set_xticklabels(numpy.arange(-curr_state, len(seq)-curr_state+1, 10),minor=False)
    axarr.set_xticks(numpy.arange(0, len(seq)+1, 10),minor=False)
    axarr.legend((p), (domain))
