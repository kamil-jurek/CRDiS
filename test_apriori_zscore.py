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
from mean_detector import MeanDetector

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
detector2 = PageHinkleyDetector(delta=0.001, lambd=20, alpha=0.99)
detector3 = AdwinDetector(delta = 0.005)
detector4 = CusumDetector(delta=0.0001, lambd=50)
#detector5 = MeanDetector(threshold=1)
#detector2 = ZScoreDetector(window_size = 20, threshold=4)
#detector3 = ZScoreDetector(window_size = win_size, threshold=5.5)
detector6 = ZScoreDetector(window_size = win_size, threshold=4)

# detector1 = PageHinkleyDetector(delta=0.001, lambd=20, alpha=0.99)
# detector2 = PageHinkleyDetector(delta=0.001, lambd=20, alpha=0.99)
# detector3 = PageHinkleyDetector(delta=0.001, lambd=30, alpha=0.99)
# detector4 = PageHinkleyDetector(delta=0.001, lambd=20, alpha=0.99)

# detector1 = AdwinDetector(delta = 0.005)
# detector2 = AdwinDetector(delta = 0.01)
# detector3 = AdwinDetector(delta = 0.01)
# detector4 = AdwinDetector(delta = 0.01)


rules_detector = RulesDetector(target_seq_index=5, type="generate_discretized")

simulator = OnlineSimulator(rules_detector,
                            [detector1, detector2, detector3, detector4, detector6],
                            [seq1, seq1, seq1, seq1, seq4],
                            ["ZScoreDetector(window_size = 30, threshold=5.0)",
                             "PageHinkleyDetector(delta=0.001, lambd=20, alpha=0.99)",
                             "AdwinDetector(delta = 0.005)",
                             'CusumDetector(delta=0.0001, lambd=50)',
                             #'MeanDetector(threshold=1)',
                             'attr_4'])

simulator.run(plot=True, detect_rules=True)

print("-----------------------------------------------------------------------------------------------------------")
detected_change_points = np.array(simulator.get_detected_changes())
for cps in detected_change_points:
    print(cps[1:])
print("-----------------------------------------------------------------------------------------------------------")

for s in simulator.discretized_sequences:
    print(s)


# offset = 500
# filtered_change_points = [[] for i in range(len(detected_change_points))]
# for cps1 in detected_change_points:
#     for cps2 in detected_change_points:
#         for cp1 in cps1:
#             for cp2 in cps2:
#                 if cps1 != cps2 and abs(round_to_hundreds(cp1.at_) - round_to_hundreds(cp2.at_)) <= offset:
#                     filtered_change_points.append()
#                     print(cp1)
#                     print(cp2)
#                     print()


# def generateSeq(change_points):
#     sequences = [[] for i in range(len(change_points))]
#     for k, attr_cps in enumerate(change_points):
#         #print("attr_p:",attr_p)
#         attr_cps = attr_cps[1:]
#         attr_name = attr_cps[0].attr_name
#         for i, point in enumerate(attr_cps):
#             prev = round_to_hundreds(attr_cps[i-1].at_) if i > 0 else 0
#
#             if i < len(attr_cps)-1:
#                 for j in range(prev, round_to_hundreds(point.at_), 100):
#                     elem = attr_name + ":" + str(point.prev_value)
#                     sequences[k].append(elem)
#     return sequences
#
# sequences = generateSeq(detected_change_points)
#
# observed = 'attr_4'
# observed_index = 3
# target = 'attr_4:' + str(detected_change_points[observed_index][1].curr_value)
# print("target:", target)
# print("-----------------------------------------------------------------------------------------------------------")
#
# for seq in sequences:
#     seq.append(target)
#     print(seq)

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

plt.show()
actual_change_points = np.array([0,400,800,1500, 1600,2000,2400,3100,3500,3900,4300,5400,5800,6200,6900,7100,7500,7900, 9000])
for k in range(len(simulator.sequences)-1):
    detected_change_points = np.array(simulator.get_detected_changes())[k]
    detected_change_points = [x.at_ for x in detected_change_points]

    print("Actual change points:   ", actual_change_points)
    print("Detected change points: ", detected_change_points)


    delta = np.abs(actual_change_points - detected_change_points)
    print(np.array(detected_change_points))


    print("Diffrerence: ", delta, " sum: ", np.sum(delta), "avg: ", np.sum(delta)/len(detected_change_points))

    rmse = np.sqrt(((detected_change_points - actual_change_points) ** 2).mean())
    print('Mean Squared Error: {}'.format(round(rmse, 5)))

