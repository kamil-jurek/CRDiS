import numpy as np
import sys; sys.path.append('./detectors/')
import pandas as pd

import encoders as en

from utils import *
from online_simulator import OnlineSimulator
from zscore_detector import ZScoreDetector
from rules_detector import RulesDetector

def round_to_hundreds(x):
    return int(round(x / 100.0)) * 100


#Numerical data
df = pd.read_csv('sequences/sequence_2018_04_15-22.22.16.csv')
#df = pd.read_csv('sequences/sequence_2018_04_22-17.15.32.csv')
#df = pd.read_csv('sequences/sequence_2018_04_13-22.33.30.csv')

seq1 = np.array(df['attr_1'])
seq2 = np.array(df['attr_2'])
seq3 = np.array(df['attr_3'])
seq4 = np.array(df['attr_4'])

for i in range(3):
    seq1 = np.concatenate((seq1, seq1))
    seq2 = np.concatenate((seq2, seq2))
    seq3 = np.concatenate((seq3, seq3))
    seq4 = np.concatenate((seq4, seq4))

print("seq len:", len(seq1))
win_size = 15
print("win size:", win_size)

detector1 = ZScoreDetector(window_size = win_size, threshold=3)
detector2 = ZScoreDetector(window_size = win_size, threshold=4)
detector3 = ZScoreDetector(window_size = win_size, threshold=4)
detector4 = ZScoreDetector(window_size = win_size, threshold=3)

rules_detector = RulesDetector(target_seq_index=3)

simulator = OnlineSimulator(rules_detector,
                            [detector1, detector2, detector3, detector4],
                            [seq1, seq2, seq3, seq4],
                            ["attr_1", "attr_2", "attr_3", "attr_4"])

simulator.run(plot=False, detect_rules=True)

print_rules(simulator.get_rules_sets())
print_combined_rules(simulator.get_combined_rules())
