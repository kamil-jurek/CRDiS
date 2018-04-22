import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import argparse

parser = argparse.ArgumentParser(description='Plotting sequence')
parser.add_argument('-i','--input', help='Sequence input file name',required=True)
parser.add_argument('-s','--start', help='Start', default=800, required=False)
parser.add_argument('-a','--attribute', help='Single attribute name', default='', required=False)
args = parser.parse_args()

curr_state = int(args.start) *1.0

seqName = args.input
df = pd.read_csv(seqName)

seqLen = (len(df.index))

step = 10
if seqLen <= 50:
    step = 1
elif seqLen <= 500:
    step = 10
elif seqLen <= 5000:
    step = 100
elif seqLen <= 50000:
    step = 1000

j = 0
colors = {}
pLegend = []


if args.attribute:
    plt.figure(figsize=(15,7))
    seq = np.array(df[args.attribute])
    N = 1
    ind = np.arange(N)    # the x locations for the groups

    for i in range(0, len(seq)):
        if not seq[i] in colors:
            colors[seq[i]] = np.random.rand(1,3)
            p = plt.barh(ind, 1, left=i, color=colors[seq[i]])
            pLegend.append(p)
        else:
            plt.barh(ind, 1, left=i, color=colors[seq[i]])


    plt.xlabel('State index')
    plt.ylabel(str(args.attribute))
    plt.yticks([], [args.attribute])
    plt.xticks(np.arange(0, len(seq)+1, step), np.arange(-curr_state, len(seq)-curr_state+1, step))

    #plt.plot(signal)
    plt.legend((pLegend), list(colors.keys()), bbox_to_anchor=(1, 1.0))
    plt.savefig("plots/plot_" + seqName.rsplit('/')[1][:-4]+'_'+ args.attribute + '.png')
    plt.show()

else:
    k = len(df.columns)
    f, axarr = plt.subplots(k, figsize=(15,7))
    for column in df:
        seq = np.array(df[column])
        N = 1
        ind = np.arange(N)    # the x locations for the groups

        for i in range(0, len(seq)):
            if not seq[i] in colors:
                colors[seq[i]] = np.random.rand(1,3)
                p = axarr[j].barh(ind, 1, left=i, color=colors[seq[i]])
                pLegend.append(p)
            else:
                axarr[j].barh(ind, 1, left=i, color=colors[seq[i]])
            #print(column, i)

        axarr[j].set_xlabel('State index')
        axarr[j].set_ylabel(str(column))
        axarr[j].set_yticks([])
        axarr[j].set_yticklabels([column])
        axarr[j].set_xticklabels(np.arange(-curr_state, len(seq)-curr_state+1, step),minor=False)
        axarr[j].set_xticks(np.arange(0, len(seq)+1, step))

        j += 1
    #plt.plot(signal)
    axarr[0].legend((pLegend), list(colors.keys()), bbox_to_anchor=(1, 1.0))
    plt.savefig("../plots/plot_" + seqName.rsplit('/')[1][:-4] + '.png')
    plt.show()
