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
sys.path.insert(0, './rules_mining/')
import pandas as pd
import numpy as np
from page_hinkley_detector import PageHinkleyDetector
from online_simulator import OnlineSimulator
from zscore_detector import ZScoreDetector
from rules_detector import RulesDetector
from rules_miner import RulesMiner
from change_point import ChangePoint
from apriori import *
from utils import *

#Numerical data
df = pd.read_csv('sequences/sequence_2018_04_13-22.33.30.csv')
seq1 = np.array(df['attr_1'])
seq2 = np.array(df['attr_2'])
seq3 = np.array(df['attr_3'])
seq4 = np.array(df['attr_4'])

for i in range(0):
    seq1 = np.concatenate((seq1, seq1))
    seq2 = np.concatenate((seq2, seq2))
    seq3 = np.concatenate((seq3, seq3))
    seq4 = np.concatenate((seq4, seq4))

detector1 = PageHinkleyDetector(delta=0.001, lambd=20, alpha=0.99)
detector2 = PageHinkleyDetector(delta=0.001, lambd=20, alpha=0.99)
detector3 = PageHinkleyDetector(delta=0.001, lambd=30, alpha=0.99)
detector4 = PageHinkleyDetector(delta=0.001, lambd=20, alpha=0.99)

rules_detector = RulesDetector(target_seq_index=3, type="generate_discretized")

simulator = OnlineSimulator(rules_detector,
                            [detector1, detector2, detector3, detector4],
                            [seq1, seq2, seq3, seq4],
                            ["attr_1", "attr_2", "attr_3", "attr_4"])

simulator.run(plot=False, detect_rules=True)

detected_change_points = np.array(simulator.get_detected_changes())
print_detected_change_points(detected_change_points)

sequences = simulator.discretized_sequences
# print(sequences)

max_window_size = 20
min_sup = 1
gcd = 100

rules_miner = RulesMiner(sequences, min_sup, max_window_size)
rules_miner.prefix_span()
rules = rules_miner.getRules()

rules_miner.print_rules()
