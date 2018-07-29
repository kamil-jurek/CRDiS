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

import sys
sys.path.append('./detectors/')
import time
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy as sp
from scipy import signal
from online_simulator import OnlineSimulator
from rules_detector import RulesDetector
from utils import *
from zscore_detector import ZScoreDetector

df = pd.read_csv('sequences/sequence_2018_05_03-16.54.37.csv')
# df = pd.read_csv('sequences/sequence_2018_07_21-22.24.18.csv')
seq_names = ['attr_1', 'attr_4']

predict_ratio=0.75
base_seqs =[]

for name in seq_names:
    base_seqs.append(np.array(df[name]))

sequences = [[] for i in range(len(base_seqs))]
for nr in range(1):
    for i, seq in enumerate(sequences):
        sequences[i] = np.concatenate((seq, base_seqs[i]))

win_size = 20
detector1 = ZScoreDetector(window_size=30, threshold=5)
detector2 = ZScoreDetector(window_size=win_size, threshold=4)
detector3 = ZScoreDetector(window_size=win_size, threshold=4)
detector4 = ZScoreDetector(window_size=win_size, threshold=4)

rules_detector = RulesDetector(target_seq_index=1,
                               window_size=0,
                               round_to=100,
                               type="all",
                               combined=False)

simulator = OnlineSimulator(rules_detector,
                            [detector1, detector4],
                            sequences,
                            seq_names,
                            predict_ratio=predict_ratio)

start_time = time.time()

simulator.run(plot=True, detect_rules=True, predict_seq=True)

#print_detected_change_points(simulator.get_detected_changes())
#print_rules(simulator.get_rules_sets(), 0)

end_time = time.time()
print(end_time - start_time)

for k, p in enumerate(simulator.predictor.predictions):
    print(k ,":", p)

pr = int(len(sequences[1])*predict_ratio) + 20
predicted = simulator.predictor.predicted[pr:len(sequences[1])]
real = sp.signal.medfilt(sequences[1][pr:],21)

plt.figure()
plt.plot(real, 'b')
plt.plot(predicted, 'r', linewidth=3.0)


fig, axes = plt.subplots(nrows=2, ncols=1, sharex=False,
                                     figsize=(12, 2*3))

axes[0].plot(sequences[0], 'b.', markersize=3)
axes[0].plot(sequences[0], 'b-', alpha=0.25)
for change_point in simulator.detected_change_points[0]:
    axes[0].axvline(change_point.at_, color='r', linestyle='--')
axes[0].set_xticks(np.arange(0, len(sequences[1]), 500))


axes[1].plot(sequences[1], 'b.', markersize=3)
axes[1].plot(sequences[1], 'b-', alpha=0.25)
for change_point in simulator.detected_change_points[1]:
    axes[1].axvline(change_point.at_, color='r', linestyle='--')

axes[1].plot(simulator.predictor.predicted, 'r', linewidth=3.0)

axes[1].set_xticks(np.arange(0, len(sequences[1]), 500))
# plt.figure()
# plt.plot(sequences[1], 'b')
# plt.plot(simulator..predictor.predicted, 'r', linewidth=3.0)


#mse = np.mean((real - predicted)**2)
# print("pred len:", real)
# print("real len:", predicted)
#print("mse:", mse)
#rmse = np.sqrt(((predicted - real) ** 2).mean())
#print('Mean Squared Error: {}'.format(round(rmse, 5)))



plt.show()