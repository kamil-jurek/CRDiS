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

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import argparse
from collections import OrderedDict

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
colors = OrderedDict()
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
    print(colors.keys())
    plt.legend((pLegend), list(colors.keys()), bbox_to_anchor=(1, 1.0))
    plt.savefig("../plots/plot_" + seqName.rsplit('/')[1][:-4]+'_'+ args.attribute + '.png')
    plt.show()

else:
    k = len(df.columns)
    f, axarr = plt.subplots(k, figsize=(15,7))
    for column in df:
        seq = np.array(df[column])
        N = 1
        ind = np.arange(N)    # the x locations for the groups

        print("Plotting ", column)
        for i in range(0, len(seq)):
            print("index:", i) if i % 1000 == 0 else None
            if not seq[i] in colors:
                colors[seq[i]] = np.random.rand(1,3)
                p = axarr[j].barh(ind, 1, left=i, color=colors[seq[i]])
                pLegend.append(p)
            else:
                axarr[j].barh(ind, 1, left=i, color=colors[seq[i]])


        axarr[j].set_xlabel('State index')
        axarr[j].set_ylabel(str(column))
        axarr[j].set_yticks([])
        axarr[j].set_yticklabels([column])
        axarr[j].set_xticklabels(np.arange(-curr_state, len(seq)-curr_state+1, step),minor=False)
        axarr[j].set_xticks(np.arange(0, len(seq)+1, step))

        j += 1

    axarr[0].legend((pLegend), list(colors.keys()), bbox_to_anchor=(1, 1.0))
    plt.savefig("../plots/plot_" + seqName.split('/')[2] + '.png')
    plt.show()
