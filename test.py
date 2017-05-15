import numpy
import matplotlib.pyplot as plt
from scipy import stats

args = [1, 2, 3, 4, 5, 6]
args_prob = [0.3, 0.8, 1.0, 0.6, 0.8, 0.2]
args_len = [100, 50, 30, 20, 10, 5]

seq = []
for i in range(0, len(args)):
    print i
    prob = [(1-args_prob[i]) / (len(args)-1) for j in args]
    prob[i] = args_prob[i]

    if len(seq) < args_len[i]:
        seq = [numpy.random.choice(args, p = prob) for j in range(0, args_len[i])]
    else:
        seq[len(seq)-args_len[i]:len(seq)] = [numpy.random.choice(args, p = prob) for j in range(0, args_len[i])]
        #seq += [numpy.random.choice(args, p = prob) for j in range(0, args_len[i])]
print seq
print stats.describe(seq)

def stats():
    count = [0,0,0,0,0,0]
    begin = 0
    end = 0
    for i in range(0, len(args)):
        begin = end;
        end = begin + args_len[i]
        for j in range(begin, end):
            if seq[j] == args[i]:
                count[i] += 1
    return count

for i in range(0, len(args)):
    print "Should be about: ", args_len[i]*args_prob[i]
#print stats()

#begin = 0
#end = 100
#for i in range(0, len(args)):
#    begin = 100-args[i]-1;
#    end = 100
#    plt.plot(range(begin,end),seq[begin:end], 'ro', color=numpy.random.rand(3,1))

#plt.plot(seq, 'ro', color=numpy.random.rand(3,1))
plt.plot(range(0,50),seq[0:50], 'ro', color=numpy.random.rand(3,1))
plt.plot(range(50,70),seq[50:70], 'ro', color=numpy.random.rand(3,1))
plt.plot(range(70,80),seq[70:80], 'ro', color=numpy.random.rand(3,1))
plt.plot(range(80,90),seq[80:90], 'ro', color=numpy.random.rand(3,1))
plt.plot(range(90,95),seq[90:95], 'ro', color=numpy.random.rand(3,1))
plt.plot(range(95,100),seq[95:100], 'ro', color=numpy.random.rand(3,1))
plt.ylabel('arguments')
plt.show()
 
