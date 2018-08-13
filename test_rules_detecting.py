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
# import encoders as en
from adwin_detector import AdwinDetector
from online_simulator import OnlineSimulator
from rules_detector import RulesDetector
from utils import *
from zscore_detector import ZScoreDetector


predict_ratio = 0.8
#df = pd.read_csv('sequences/sequence_2018_08_08-11.42.05.csv')
# df = pd.read_csv('sequences/sequence_2018_07_21-22.24.18.csv')
# seq_names = ['attr_1', 'attr_2', 'attr_3','attr_4' ]


# df = pd.read_csv('sequences/ocupancy.csv')
# df['date'] = pd.to_datetime(df['date'])
# df.set_index('date').plot()




# seq_names = ['Temperature', 'Humidity', 'Light','Occupancy']
# df['Temperature'] = df['Temperature'].apply(lambda x: round_to(x, 2))
# df['Humidity'] = df['Humidity'].apply(lambda x: round_to(x, 5))
# df['Light'] = df['Light'].apply(lambda x: round_to(x, 200))
# df.plot(x='date', y=['Temperature','Occupancy'])
# print(df['date'])

df = pd.read_csv('sequences/sequence_2018_08_09-18.23.01.csv')
seq_names = ['temperature', 'light_code','occupancy']

from sklearn.preprocessing import LabelEncoder

lb = LabelEncoder()
df["light_code"] = lb.fit_transform(df["light"])


# df = pd.read_csv('sequences/shuttle.csv')
# seq_names = ['A', 'B', 'C','label']

base_seqs =[]
for name in seq_names:
    base_seqs.append(np.array(df[name]))

sequences = [[] for i in range(len(base_seqs))]
for nr in range(1):
    for i, seq in enumerate(sequences):
        sequences[i] = np.concatenate((seq, base_seqs[i]))

win_size = 20
detector1 = ZScoreDetector(window_size = 30, threshold=3.5)
# detector1 = ZScoreDetector(window_size = 30, threshold=5)
detector2 = ZScoreDetector(window_size = 30, threshold=4.5)
#detector3 = ZScoreDetector(window_size = win_size, threshold=5.5)
detector3 = ZScoreDetector(window_size = 30, threshold=3.5)

rules_detector = RulesDetector(target_seq_index=2,
                               window_size=0,
                               round_to=60,
                               type="all")

simulator = OnlineSimulator(rules_detector,
                            [detector1, detector2, detector3],
                            sequences,
                            seq_names,
                            predict_ratio=predict_ratio)
simulator.label_encoder = lb

start_time = time.time()

simulator.run(plot=True, detect_rules=True, predict_seq=False)

print_detected_change_points(simulator.get_detected_changes())
# print_rules(simulator.get_rules_sets(), 5)
# print_combined_rules(simulator.get_combined_rules(), 0)
print_best_rules(simulator.get_rules_sets())

#print_rules(simulator.get_rules_sets(), 1)
discovered_rules = simulator.get_rules_sets()
#print_rules_for_attr(discovered_rules, 'light', 1)

end_time = time.time()
print(end_time - start_time)

# for rs in simulator.get_rules_sets():
#     print(list(rs)[0].lhs[0].attr_name_, ":", len(rs))

# for k, p in enumerate(simulator.predictor.predictions):
#     print(k ,":", p)
#
# pr = int(len(sequences[3])*predict_ratio) + 20
# predicted = simulator.predictor.predicted[pr:len(sequences[3])]
# real = sp.signal.medfilt(sequences[3][pr:],21)
#
# plt.figure()
# plt.plot(real, 'b')
# plt.plot(predicted, 'r', linewidth=3.0)

# rmse = np.sqrt(((predicted - real) ** 2).mean())
# print('Mean Squared Error: {}'.format(round(rmse, 5)))

plt.show()