import numpy as np
import sys; sys.path.append('./detectors/')
import pandas as pd
import math
import encoders as en
import scipy as sp
from scipy import signal
from detector import ChangeDetector
from sklearn.metrics import accuracy_score
from detector import OnlineSimulator
from page_hinkley_detector import PageHinkleyDetector


def round_to_hundreds(x):
    return int(round(x / 100.0)) * 100

#Numerical data
#sequences/sequence_2017_11_28-18.07.57.csv
#df = pd.read_csv('sequences/sequence_2018_03_24-13.19.49.csv')
df = pd.read_csv('sequences/sequence_2018_03_25-17.24.22.csv')
seq1 = np.array(df['attr_1'])
seq2 = np.array(df['attr_2'])
seq3 = np.array(df['attr_3'])
seq4 = np.array(df['attr_4'])

# Symbolic data
# df = pd.read_csv('sequences/sequence_2017_11_22-19.35.27.csv')
# seq = np.array(df['day_of_week'])
# seq = en.encode(seq)
# seq = [np.abs(np.mean(e)) for e in seq]

detector1 = PageHinkleyDetector(delta=0.001, lambd=20, alpha=0.99)
detector2 = PageHinkleyDetector(delta=0.001, lambd=20, alpha=0.99)
detector3 = PageHinkleyDetector(delta=0.001, lambd=30, alpha=0.99)
detector4 = PageHinkleyDetector(delta=0.001, lambd=20, alpha=0.99)
simulator = OnlineSimulator([detector1, detector2, detector3, detector4],
                            [seq1, seq2, seq3, seq4],
                            ["attr_1", "attr_2", "attr_3", "attr_4"])
simulator.run(plot=False)

print(simulator.get_detected_changes())
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

# actual_change_points = np.array([600, 800, 1000, 1300, 1500, 1800])
# detected_change_points = np.array(simulator.get_detected_changes())
# delta = np.abs(actual_change_points - detected_change_points)
# #print(np.array(detected_change_points)- int(2/3 * len(seq)))
#
# print("Actual change points: ", actual_change_points)
# print("Detected change points: ", detected_change_points)
# print("Diffrerence: ", delta, " sum: ", np.sum(delta))