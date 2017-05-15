import numpy

def generateSequence(domain, value, op, probability, numberOfSamples, next=False):
    if op == 'eq':
        prob = [(1.0 - probability) / (len(domain) - 1) for i in domain]
        prob[domain.index(value)] = probability

        seq = [numpy.random.choice(domain, p = prob) for j in range(0, numberOfSamples)]

        return seq

def testSequence(seq, value, prob):
    counter = seq.count(value)

    print "Should be about: ", len(seq)*prob
    print "Is: ", counter
