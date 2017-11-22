import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

curr_state = 1.5 * 800

seqName = "2017_11_22-19.55.44"
df = pd.read_csv('sequences/sequence_' + seqName + '.csv')
colName = 'attr_1'

seq = np.array(df[colName])

step = 100
N = 1
colors = {}
ind = np.arange(N)    # the x locations for the groups
pLegend = []

plt.figure(figsize=(20,5))
for i in range(0, len(seq)):
    if not seq[i] in colors:
        colors[seq[i]] = np.random.rand(1,3)
        p = plt.barh(ind, 1, left=i, color=colors[seq[i]])
        pLegend.append(p)
    else:
        plt.barh(ind, 1, left=i, color=colors[seq[i]])

plt.xlabel('State nr')
plt.ylabel(str(colName))
plt.yticks([],[colName])
#plt.xticklabels(numpy.arange(-curr_state, len(seq)-curr_state+1, 100),minor=False)
plt.xticks(np.arange(0, len(seq)+1, step), np.arange(-curr_state, len(seq)-curr_state+1, step))
plt.legend((pLegend), list(colors.keys()))

#plt.plot(signal)
plt.savefig("plots/plot_" + seqName + '.png')
plt.show()
