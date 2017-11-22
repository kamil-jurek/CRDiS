import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

domain = [1,2,3,4]
#domain = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
attrName = ""
curr_state = 1.5 * 800

seqName = "2017_11_22-19.55.44"
df = pd.read_csv('sequences/sequence_' + seqName + '.csv')
seq = np.array(df['attr_1'])
#seq = np.array(df['day_of_week'])
#print(seq)
N = 1
colors = [np.random.rand(1,3) for i in domain]
ind = np.arange(N)    # the x locations for the groups

p = [0 for i in domain]
for i in range(0, len(seq)):
    for j in range(0, len(domain)):
        if seq[i] == domain[j]:
            p[j] = plt.barh(ind, 1, left=i, color=colors[j] )

plt.xlabel('State nr')
plt.ylabel(str(attrName))
plt.yticks([],['day_of_week'])
#plt.xticklabels(numpy.arange(-curr_state, len(seq)-curr_state+1, 100),minor=False)
plt.xticks(np.arange(0, len(seq)+1, 100), np.arange(-curr_state, len(seq)-curr_state+1, 100))
plt.legend((p), (domain))

#plt.plot(signal)
plt.savefig("plots/plot_" + seqName + '.png')
plt.show()
