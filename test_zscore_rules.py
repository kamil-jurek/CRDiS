import matplotlib.pyplot as plt
import numpy as np
import sys; sys.path.append('./detectors/')
import pandas as pd
import encoders as en
from detector import ChangeDetector
from detector import OnlineSimulator
from zscore_rules import ZScoreDetectorRules
from math import gcd

#Numerical data
# df = pd.read_csv('sequences/sequence_2017_11_28-18.07.57.csv')
# sequence = np.array(df['attr_1'])
df = pd.read_csv('sequences/sequence_2018_03_25-17.24.22.csv')
seq1 = np.array(df['attr_1'])
seq2 = np.array(df['attr_2'])
seq3 = np.array(df['attr_3'])
seq4 = np.array(df['attr_4'])

# Symbolic data
# df = pd.read_csv('sequences/sequence_2017_11_22-19.35.27.csv')
# sequence = np.array(df['day_of_week'])
# sequence = en.encode(sequence)

win_size = int(len(sequence)*(1/100))
print("win size:", win_size)

detector1 = ZScoreDetectorRules(window_size = win_size, threshold=2.5)
detector2 = ZScoreDetectorRules(window_size = win_size, threshold=2.5)
detector3 = ZScoreDetectorRules(window_size = win_size, threshold=2.5)
detector4 = ZScoreDetectorRules(window_size = win_size, threshold=2.5)
simulator = OnlineSimulator([detector1, detector2, detector3, detector4],
                            [seq1, seq2, seq3, seq4],
                            ["attr_1", "attr_2", "attr_3", "attr_4"])
simulator.run(plot=True)

#print(simulator.get_detected_changes())
detected_change_points = np.array(simulator.get_detected_changes())

sequences = [[] for i in range(len(detected_change_points))]
for k, attr_p in enumerate(detected_change_points):
    attr_name = attr_p[0].attr_name
    for i, p in enumerate(attr_p):
        #print(p.from_)
        #print(p.to_)

        prev = round_to_hundreds(attr_p[i-1].at_) if i > 0 else 0
        #print("fr:", prev)
        #print("to:", round_to_hundreds(p.at_))

        for j in range(prev, round_to_hundreds(p.at_), 100):
            elem = attr_name + ":" + str(p.from_)
            #print(elem)
            sequences[k].append(elem)
        #print(attr_name)

for seq in sequences:
    seq.append("attr_4:5")
    print(seq)