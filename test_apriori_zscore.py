import numpy as np
import sys
sys.path.append('./detectors/')
sys.path.insert(0, './rules_mining/')
import pandas as pd

from page_hinkley_detector import PageHinkleyDetector
from apriori import *
from online_simulator import OnlineSimulator
from zscore_detector import ZScoreDetector
from rules_detector import RulesDetector
from change_point import ChangePoint

def round_to_hundreds(x):
    return int(round(x / 100.0)) * 100

#Numerical data
df = pd.read_csv('sequences/sequence_2018_04_13-22.33.30.csv')
seq1 = np.array(df['attr_1'])
seq2 = np.array(df['attr_2'])
seq3 = np.array(df['attr_3'])
seq4 = np.array(df['attr_4'])

for i in range(1):
    seq1 = np.concatenate((seq1, seq1))
    seq2 = np.concatenate((seq2, seq2))
    seq3 = np.concatenate((seq3, seq3))
    seq4 = np.concatenate((seq4, seq4))

# Symbolic data
# df = pd.read_csv('sequences/sequence_2017_11_22-19.35.27.csv')
# seq = np.array(df['day_of_week'])
# seq = en.encode(seq)
# seq = [np.abs(np.mean(e)) for e in seq]

detector1 = PageHinkleyDetector(delta=0.001, lambd=20, alpha=0.99)
detector2 = PageHinkleyDetector(delta=0.001, lambd=20, alpha=0.99)
detector3 = PageHinkleyDetector(delta=0.001, lambd=30, alpha=0.99)
detector4 = PageHinkleyDetector(delta=0.001, lambd=20, alpha=0.99)

rules_detector = RulesDetector(target_seq_index=3)

simulator = OnlineSimulator(rules_detector,
                            [detector1, detector2, detector3, detector4],
                            [seq1, seq2, seq3, seq4],
                            ["attr_1", "attr_2", "attr_3", "attr_4"])
simulator.run(plot=False, detect_rules=False)

print("-----------------------------------------------------------------------------------------------------------")
detected_change_points = np.array(simulator.get_detected_changes())
for cps in detected_change_points:
    print(cps[1:])
print("-----------------------------------------------------------------------------------------------------------")

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


def generateSeq(change_points):
    sequences = [[] for i in range(len(detected_change_points))]
    for k, attr_p in enumerate(detected_change_points):
        attr_p = attr_p[1:]
        attr_name = attr_p[0].attr_name
        for i, p in enumerate(attr_p):
            prev = round_to_hundreds(attr_p[i-1].at_) if i > 0 else 0

            if i < len(attr_p)-1:
                for j in range(prev, round_to_hundreds(p.at_), 100):
                    elem = attr_name + ":" + str(p.prev_value)
                    sequences[k].append(elem)
    return sequences

sequences = generateSeq(detected_change_points)

observed = 'attr_4'
observed_index = 3
target = 'attr_4:' + str(detected_change_points[observed_index][1].curr_value)
print(target)
print("-----------------------------------------------------------------------------------------------------------")

for seq in sequences:
    seq.append(target)
    print(seq)

dataSet = sequences
L, suppData = aprioriAlgo(dataSet, minSupport=0.0)
rules, rulesDict = generateRules(L,suppData, target, minConf=0.0)

# for r in rules:
#     print(r)
print("-----------------------------------------------------------------------------------------------------------")
for k, ar in rulesDict.items():
    ar.sort(key=lambda t: len(t.lhs), reverse=True)
    for r in ar:
        print(r)
print("-----------------------------------------------------------------------------------------------------------")

# actual_change_points = np.array([600, 800, 1000, 1300, 1500, 1800])
# detected_change_points = np.array(simulator.get_detected_changes())
# delta = np.abs(actual_change_points - detected_change_points)
# #print(np.array(detected_change_points)- int(2/3 * len(seq)))
#
# print("Actual change points: ", actual_change_points)
# print("Detected change points: ", detected_change_points)
# print("Diffrerence: ", delta, " sum: ", np.sum(delta))