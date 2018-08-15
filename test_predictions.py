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

# df = pd.read_csv('sequences/sequence_2018_05_03-16.54.37.csv')
# df = pd.read_csv('sequences/sequence_2018_07_21-22.24.18.csv')
df = pd.read_csv('sequences/sequence_2018_07_30-17.55.58.csv')
seq_names = ['attr_1', 'attr_2', 'attr_3','attr_4']

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
detector4 = ZScoreDetector(window_size=win_size, threshold=5)

target_seq_index = 3

rules_detector = RulesDetector(target_seq_index=target_seq_index,
                               window_size=0,
                               round_to=100,
                               type="all",
                               combined=False)

simulator = OnlineSimulator(rules_detector,
                            [detector1, detector2, detector3,detector4],
                            sequences,
                            seq_names,
                            predict_ratio=predict_ratio)
simulator.random_subsequences = False

start_time = time.time()

simulator.run(plot=True, detect_rules=True, predict_seq=True)

#print_detected_change_points(simulator.get_detected_changes())
#print_rules(simulator.get_rules_sets(), 0)

end_time = time.time()


print("Rules used for prediction:")
for br in simulator.best_rules:
    print(br)

prediction_start = int(len(sequences[target_seq_index])*predict_ratio)
predicted = simulator.predictor.predicted[prediction_start:len(sequences[target_seq_index])]
real = sp.signal.medfilt(sequences[target_seq_index][prediction_start:],21)
rmse = np.sqrt(((predicted - real) ** 2).mean())
print('Mean Squared Error: {}'.format(round(rmse, 5)))

plot_sequences_on_one_figure(sequences, seq_names, simulator, target_seq_index)

print("Time:", end_time - start_time)

plt.show()