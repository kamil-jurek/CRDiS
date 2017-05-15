import numpy
import matplotlib.pyplot as plt
from scipy import stats

args = [1, 2, 3, 4, 5, 6]
args_op = ['eq','eq','eq','eq','eq','eq']
args_prob = [0.1, 0.8, 1.0, 0.6, 0.5, 0.93]
args_len = [100, 50, 30, 20, 10, 50]

seq = [[] for i in range(0, len(args))]

for i in range(0, len(args)):
    seq[i] = [numpy.random.choice(args) for j in range(0, max(args_len))]

for i in range(0, len(args)):
    if args_op[i] == 'eq':
        prob = [(1-args_prob[i]) / (len(args)-1) for j in args]
        prob[i] = args_prob[i]

        seq[i][max(args_len)-args_len[i]:max(args_len)] = \
            [numpy.random.choice(args, p = prob) for j in range(0, args_len[i])]

for i in range(len(seq)):
    print seq[i]

for i in range(0,len(args)):
    plt.plot(range((max(args_len)-args_len[i]),max(args_len)),
        seq[i][(max(args_len)-args_len[i]):max(args_len)],
        'ro',
        color=numpy.random.rand(3,1))

counter = [0 for i in range(0, len(args))]
for i in range(0,len(args)):
    for j in range(max(args_len)-args_len[i],max(args_len)):
        if seq[i][j] == args[i]:
            counter[i] += 1;

for i in range(0, len(args)):
    print "Should be about: ", args_len[i]*args_prob[i]
    print counter[i]

plt.xlabel('liczba probek')
plt.show()
