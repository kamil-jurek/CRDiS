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

def round_to_hundreds(x):
    return int(round(x / 100.0)) * 100

#Numerical data
df = pd.read_csv('sequences/sequence_2018_04_13-22.33.30.csv')
df = pd.read_csv('sequences/sequence_2018_05_03-16.54.37.csv')
df = pd.read_csv('sequences/sequence_2018_07_21-20.53.53.csv')
df = pd.read_csv('sequences/sequence_2018_07_21-22.24.18.csv')
seq1 = np.array(df['attr_1'])
seq2 = np.array(df['attr_2'])
seq3 = np.array(df['attr_3'])
seq4 = np.array(df['attr_4'])

for i in range(0):
    seq1 = np.concatenate((seq1, seq1))
    seq2 = np.concatenate((seq2, seq2))
    seq3 = np.concatenate((seq3, seq3))
    seq4 = np.concatenate((seq4, seq4))

# Symbolic data
# df = pd.read_csv('sequences/sequence_2017_11_22-19.35.27.csv')
# seq = np.array(df['day_of_week'])
# seq = en.encode(seq)
# seq = [np.abs(np.mean(e)) for e in seq]

win_size = 20
detector1 = ZScoreDetector(window_size = 30, threshold=5.0)
detector2 = ZScoreDetector(window_size = 20, threshold=4)
detector3 = ZScoreDetector(window_size = win_size, threshold=5.5)
detector4 = ZScoreDetector(window_size = win_size, threshold=4)

rules_detector = RulesDetector(target_seq_index=3, type="generate_discretized")

simulator = OnlineSimulator(rules_detector,
                            [detector1, detector2, detector3, detector4],
                            [seq1, seq2, seq3, seq4],
                            ["attr_1",
                             "attr_2",
                             "attr_3",
                             'attr_4'])

simulator.run(plot=True, detect_rules=True)

print("-----------------------------------------------------------------------------------------------------------")
detected_change_points = np.array(simulator.get_detected_changes())
for cps in detected_change_points:
    print(cps[1:])
print("-----------------------------------------------------------------------------------------------------------")

for s in simulator.discretized_sequences:
    print(s)

# APRIORI
# L, suppData = aprioriAlgo(simulator.discretized_sequences, minSupport=0.0)
# rules, rulesDict = generateRules(L,suppData, "?", minConf=0.0)
# print("-----------------------------------------------------------------------------------------------------------")
# for k, ar in rulesDict.items():
#     ar.sort(key=lambda t: t.supp, reverse=True)
#     for r in ar:
#         print(r)
# print("-----------------------------------------------------------------------------------------------------------")

# PREFIXSPAN
max_window_size = 20
min_sup = 5
gcd = 100

rules_miner = RulesMiner(simulator.discretized_sequences, min_sup, max_window_size)
rules_miner.prefix_span()
rules = rules_miner.getRules()
rules_miner.print_rules()

plt.show()

