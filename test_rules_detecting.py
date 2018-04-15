import numpy as np
import sys; sys.path.append('./detectors/')
import pandas as pd
import random
import encoders as en
from detector import ChangeDetector
from detector import OnlineSimulator
from zscore_detector import ZScoreDetector

def round_to_hundreds(x):
    return int(round(x / 100.0)) * 100


#Numerical data
#df = pd.read_csv('sequences/sequence_2017_11_28-18.07.57.csv')
#seq = np.array(df['attr_1'])
#df = pd.read_csv('sequences/sequence_2018_03_25-17.24.22.csv')
df = pd.read_csv('sequences/sequence_2018_04_13-22.33.30.csv')

seq1 = np.array(df['attr_1'])
seq2 = np.array(df['attr_2'])
seq3 = np.array(df['attr_3'])
seq4 = np.array(df['attr_4'])
for i in range(4):
    # rand = [random.randint(1,6) for i in range(random.randint(0,3)+50)]
    # seq1_rand = np.concatenate((seq1, rand))
    # seq1 = np.concatenate((seq1_rand, seq1))
    #
    # rand = [random.randint(1,6) for i in range(random.randint(0,3)+50)]
    # seq2_rand = np.concatenate((seq2, rand))
    # seq2 = np.concatenate((seq2_rand, seq2))
    #
    # rand = [random.randint(1,6) for i in range(random.randint(0,3)+50)]
    # seq3_rand = np.concatenate((seq3, rand))
    # seq3 = np.concatenate((seq3_rand, seq3))
    #
    # rand = [random.randint(1,6) for i in range(random.randint(0,3)+50)]
    # seq4_rand = np.concatenate((seq4, rand))
    # seq4 = np.concatenate((seq4_rand, seq4))

    seq1 = np.concatenate((seq1, seq1))
    seq2 = np.concatenate((seq2, seq2))
    seq3 = np.concatenate((seq3, seq3))
    seq4 = np.concatenate((seq4, seq4))

print("seq len:", len(seq1))
# Symbolic data
# df = pd.read_csv('sequences/sequence_2017_11_22-19.35.27.csv')
# sequence = np.array(df['day_of_week'])
# sequence = en.encode(sequence)

win_size = int(len(seq1)*(1/100))
win_size = 15
print("win size:", win_size)

detector1 = ZScoreDetector(window_size = win_size, threshold=5)
detector2 = ZScoreDetector(window_size = win_size, threshold=3.5)
#detector3 = ZScoreDetector(window_size = win_size, threshold=3)
detector4 = ZScoreDetector(window_size = win_size, threshold=3)

simulator = OnlineSimulator([detector1, detector2, detector4],
                            [seq1, seq2, seq4],
                            ["attr_1", "attr_2", "attr_4"])
simulator.run(plot=False, detect_rules=True)

#print(simulator.get_detected_changes())
detected_change_points = np.array(simulator.get_detected_changes())

# for cps in detected_change_points:
#     print(cps)

print()
print("------------------------------------------------------------------------")
for rules_sets in simulator.get_rules():
    for rule in rules_sets:
        print(rule)
    print("------------------------------------------------------------------------")
