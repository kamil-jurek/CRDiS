import numpy as np
import sys
sys.path.append('./detectors/')
sys.path.insert(0, './rules_mining/')
import pandas as pd
import matplotlib.pyplot as plt

from page_hinkley_detector import PageHinkleyDetector
from apriori import *
from rules_miner import RulesMiner
from online_simulator import OnlineSimulator
from zscore_detector import ZScoreDetector
from rules_detector import RulesDetector
from change_point import ChangePoint
from page_hinkley_detector import PageHinkleyDetector
from adwin_detector import AdwinDetector
from cusum_detector import CusumDetector
from geometric_moving_average_detector import GeometricMovingAverageDetector
from utils import *

import encoders as en

def round_to_hundreds(x):
    return int(round(x / 100.0)) * 100


# Symbolic data
df = pd.read_csv('sequences/sequence_2017_11_22-19.35.27.csv')
seq1 = np.array(df['day_of_week'])
seq1 = en.encode(seq1)
seq1 = [np.abs(np.mean(e)) for e in seq1]


#Numerical data
# df = pd.read_csv('sequences/sequence_2018_04_13-22.33.30.csv')
# df = pd.read_csv('sequences/sequence_2018_05_03-16.54.37.csv')
# df = pd.read_csv('sequences/sequence_2018_07_21-20.53.53.csv')

# df = pd.read_csv('sequences/sequence_2018_07_21-22.24.18.csv')
# seq1 = np.array(df['attr_1'])
# seq2 = np.array(df['attr_2'])
# seq3 = np.array(df['attr_3'])
# seq4 = np.array(df['attr_4'])

win_size = 20
detector1 = ZScoreDetector(window_size = 30, threshold=5.0)
detector2 = PageHinkleyDetector(delta=0.001, lambd=20, alpha=0.99)
detector3 = AdwinDetector(delta = 0.005)
detector4 = CusumDetector(delta=0.0001, lambd=50)
detector5 = GeometricMovingAverageDetector(threshold=0.65)

rules_detector = RulesDetector(target_seq_index=5, type="generate_discretized")

simulator = OnlineSimulator(None,
                            [detector1, detector2, detector3, detector4, detector5],
                            [seq1, seq1, seq1, seq1, seq1],
                            ["ZScoreDetector(window_size = 30, threshold=5.0)",
                             "PageHinkleyDetector(delta=0.001, lambd=20, alpha=0.99)",
                             "AdwinDetector(delta = 0.005)",
                             'CusumDetector(delta=0.0001, lambd=50)',
                            'GeometricMovingAverageDetector(threshold=0.65)'
                            ],
                            plot_change_detectors=True)

simulator.run(plot=True, detect_rules=False)

print("-----------------------------------------------------------------------------------------------------------")
detected_change_points = np.array(simulator.get_detected_changes())
for cps in detected_change_points:
    print(cps[1:])
print("-----------------------------------------------------------------------------------------------------------")


# L, suppData = aprioriAlgo(simulator.discretized_sequences, minSupport=0.0)
# rules, rulesDict = generateRules(L,suppData, "?", minConf=0.0)
# print("-----------------------------------------------------------------------------------------------------------")
# for k, ar in rulesDict.items():
#     ar.sort(key=lambda t: t.supp, reverse=True)
#     for r in ar:
#         print(r)
# print("-----------------------------------------------------------------------------------------------------------")

# max_window_size = 20
# min_sup = 1
# gcd = 100
#
# rules_miner = RulesMiner(simulator.discretized_sequences, min_sup, max_window_size)
# rules_miner.prefix_span()
# rules = rules_miner.getRules()
# rules_miner.print_rules()


# actual_change_points = np.array([0,400,800,1500,1600,2000,2400,3100,3500,3900,4300,5400,5800,6200,6900,7100,7500,7900,9000])
# evaluate_change_detectors(simulator, actual_change_points)
#
plt.show()