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
from simple_rules_generator import SimpleRulesGenerator
from all_rules_generator import AllRulesGenerator
from closed_rules_generator import ClosedRulesGenerator
from discretized_dataset_generator import DiscretizedDatasetGenerator

predict_ratio = 0.8
# df = pd.read_csv('sequences/sequence_2018_08_08-11.42.05.csv')
df = pd.read_csv('sequences/sequence_2018_07_21-22.24.18.csv')
# df = pd.read_csv('sequences/sequence_2018_05_03-16.54.37.csv')
seq_names = ['attr_1', 'attr_2', 'attr_3','attr_4']

# df = pd.read_csv('sequences/occupancy_3.csv')
# seq_names = ['temperature', 'light_code','occupancy']

# from sklearn.preprocessing import LabelEncoder
# lb = LabelEncoder()
# df["light_code"] = lb.fit_transform(df["light"])

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
detector4 = ZScoreDetector(window_size = 30, threshold=4.5)

target_seq_index = 3

# rules_detector = RulesDetector(target_seq_index=target_seq_index,
#                                window_size=0,
#                                round_to=100,
#                                type="simple")

# rules_detector = SimpleRulesGenerator(target_seq_index=target_seq_index,
#                                       window_size=0,
#                                       round_to=100)

rules_detector = AllRulesGenerator(target_seq_index=target_seq_index,
                                      window_size=0,
                                      round_to=100)

# rules_detector = ClosedRulesGenerator(target_seq_index=target_seq_index,
#                                       window_size=0,
#                                       round_to=100)

rules_detector = DiscretizedDatasetGenerator(target_seq_index=target_seq_index,
                                             window_size=0,
                                             round_to=100)

simulator = OnlineSimulator(rules_detector,
                            [detector1, detector2, detector3, detector4],
                            sequences,
                            seq_names
                            )

# simulator.label_encoder = lb

start_time = time.time()

simulator.run(plot=True, detect_rules=True, predict_seq=False)

discovered_rules = simulator.get_rules_sets()
#print_detected_change_points(simulator.get_detected_changes())
# print_rules(simulator.get_rules_sets(), 5)
# print_combined_rules(simulator.get_combined_rules(), 0)
# print_rules(discovered_rules, 1)
#print_best_rules(discovered_rules)
# print_rules_for_attr(discovered_rules, 'light', 1)

for dd in rules_detector.discretized_dataset:
    print(dd)

end_time = time.time()
print(end_time - start_time)

plot_sequences_on_one_figure(sequences, seq_names, simulator, target_seq_index)

plt.show()