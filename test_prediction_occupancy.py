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

df = pd.read_csv('sequences/occupancy_3.csv')
seq_names = ['light_code', 'temperature', 'occupancy']
df['ind'] = [x for x in range(len(df['light']))]
#df.set_index('ind')
#print (df.index.name)
df['date'] = pd.to_datetime(df['ind'], unit='m')
df['date'] = df['date'] + pd.DateOffset(years=48)
df['date'] = df['date'] + pd.DateOffset(months=7)
print(df.head())
from sklearn.preprocessing import LabelEncoder

lb = LabelEncoder()
df["light_code"] = lb.fit_transform(df["light"])

predict_ratio=0.73
base_seqs =[]

for name in seq_names:
    base_seqs.append(np.array(df[name]))

sequences = [[] for i in range(len(base_seqs))]
for nr in range(1):
    for i, seq in enumerate(sequences):
        sequences[i] = np.concatenate((seq, base_seqs[i]))

win_size = 20

detector2 = ZScoreDetector(window_size = 25, threshold=4)
# detector1 = ZScoreDetector(window_size = 30, threshold=5)
detector1 = ZScoreDetector(window_size = 30, threshold=4.5)
detector3 = ZScoreDetector(window_size = 30, threshold=4)

target_seq_index = 1

rules_detector = RulesDetector(target_seq_index=target_seq_index,
                               window_size=1440,
                               round_to=60,
                               type="all",
                               combined=False)

simulator = OnlineSimulator(rules_detector,
                            [detector1, detector2, detector3],
                            sequences,
                            seq_names,
                            round_to=60,
                            predict_ratio=predict_ratio)
simulator.label_encoder = lb
start_time = time.time()

simulator.run(plot=True, detect_rules=True, predict_seq=True)

discovered_rules = simulator.get_rules_sets()
# print_detected_change_points(simulator.get_detected_changes())
# print_rules(simulator.get_rules_sets(), 3)
print_best_rules(discovered_rules)
# print_rules(simulator.get_rules_sets(), 1)
#print_rules_for_attr(discovered_rules, 'light', 1)
end_time = time.time()
print(end_time - start_time)

print("Rules used for prediction")
for br in simulator.best_rules:
    print(br)


prediction_start = int(len(sequences[target_seq_index])*predict_ratio)
predicted = simulator.predictor.predicted[prediction_start:len(sequences[target_seq_index])]
real = sp.signal.medfilt(sequences[target_seq_index][prediction_start:],21)

plt.figure()
plt.plot(real, 'b')
plt.plot(predicted, 'r', linewidth=3.0)

fig, axes = plt.subplots(nrows=3, ncols=1, sharex=True,
                                     figsize=(12, 2*3))

axes[0].plot(df["light"], 'b.', markersize=3)
axes[0].plot(df["light"], 'b-', alpha=0.25)
for change_point in simulator.detected_change_points[0]:
    axes[0].axvline(change_point.at_, color='r', linestyle='--')
axes[0].set_title("Light")

axes[1].plot(sequences[1], 'b.', markersize=3)
axes[1].plot(sequences[1], 'b-', alpha=0.25)
for change_point in simulator.detected_change_points[1]:
    axes[1].axvline(change_point.at_, color='r', linestyle='--')
axes[1].set_title("Temperature")

axes[2].plot(sequences[2], 'b.', markersize=3)
axes[2].plot(sequences[2], 'b-', alpha=0.25)
for change_point in simulator.detected_change_points[2]:
    axes[2].axvline(change_point.at_, color='r', linestyle='--')
axes[2].set_title("Occupancy")

ticks_to_use = df.date[::120]
labels = [ i for i in ticks_to_use ]
axes[2].set_xticks(df.ind[::120])
axes[2].set_xticklabels(labels,rotation=90)

rmse = np.sqrt(((predicted - real) ** 2).mean())
print('Mean Squared Error: {}'.format(round(rmse, 5)))
print(df.head())


plt.show()