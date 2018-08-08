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

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# import encoders as en

from online_simulator import OnlineSimulator
from zscore_detector import ZScoreDetector
from rules_detector import RulesDetector
from page_hinkley_detector import PageHinkleyDetector
from rules_miner import RulesMiner
from page_hinkley_detector import PageHinkleyDetector
from adwin_detector import AdwinDetector
from cusum_detector import CusumDetector
from geometric_moving_average_detector import GeometricMovingAverageDetector
from ddm_detector import DDMDetector
from utils import *
from apriori import *

#Numerical data
# Baisic
# df = pd.read_csv('sequences/sequence_2018_07_21-22.24.18.csv')

# 100%
# df = pd.read_csv('sequences/sequence_2018_07_27-18.40.39.csv')

# 95%
df = pd.read_csv('sequences/sequence_2018_07_27-18.47.08.csv')

# 90%
# df = pd.read_csv('sequences/sequence_2018_07_27-18.49.21.csv')

# 85%
# df = pd.read_csv('sequences/sequence_2018_07_27-18.51.10.csv')

# 80%
# df = pd.read_csv('sequences/sequence_2018_07_27-18.58.50.csv')

# 75%
# df = pd.read_csv('sequences/sequence_2018_07_27-19.01.12.csv')

# 70%
# df = pd.read_csv('sequences/sequence_2018_07_27-19.04.49.csv')

# 65%
# df = pd.read_csv('sequences/sequence_2018_07_27-19.19.47.csv')

# 60%
# df = pd.read_csv('sequences/sequence_2018_07_27-19.26.50.csv')
seq1 = np.array(df['attr_1'])
seq2 = np.array(df['attr_2'])
seq3 = np.array(df['attr_3'])
seq4 = np.array(df['attr_4'])

win_size = 20
detector1 = ZScoreDetector(window_size = 30, threshold=5.0)
detector2 = PageHinkleyDetector(delta=0.001, lambd=20, alpha=0.99)
detector3 = AdwinDetector(delta = 0.005)
detector4 = CusumDetector(delta=0.0001, lambd=50)
# detector5 = DDMDetector(delta=0.0001, lambd=50)
# detector6 = GeometricMovingAverageDetector(threshold=0.65)

rules_detector = RulesDetector(target_seq_index=5, type="generate_discretized")

simulator = OnlineSimulator(None,
                            # [detector1, detector2, detector3, detector4, detector5, detector6],
                            [detector1, detector2, detector3, detector4],
                            # [seq1, seq1, seq1, seq1, seq1, seq1],
                            [seq1, seq1, seq1, seq1],
                            ["ZScoreDetector(window_size = 30, threshold=5.0)",
                             "PageHinkleyDetector(delta=0.001, lambd=20, alpha=0.99)",
                             "AdwinDetector(delta = 0.005)",
                             'CusumDetector(delta=0.0001, lambd=50)'
                             # 'DDMDetector(lambd=25)',
                             # 'GeometricMovingAverageDetector(threshold=0.65)'
                            ],
                            plot_change_detectors=True)

simulator.run(plot=True, detect_rules=False)

points = []
for p in simulator.get_detected_changes()[0]:
    points.append(p.at_)
    print(p.at_)
print(points)
#actual_change_points = np.array([0,400,800,1500,1600,2000,2400,3100,3500,3900,4300,5400,5800,6200,6900,7100,7500,7900,9000])
actual_change_points = np.array([0, 400, 800, 1500, 1800, 2200, 2600, 3300, 3600, 4000, 4400, 5100, 5400, 5800, 6200, 6900, 7200, 7600, 8000, 8700, 9000])
evaluate_change_detectors(simulator, actual_change_points)

plt.show()