import numpy as np
import sys; sys.path.append('./detectors/')
import pandas as pd

import encoders as en

from utils import *
from online_simulator import OnlineSimulator
from zscore_detector import ZScoreDetector

from rules_detector import RulesDetector
#from rules_detector_2 import RulesDetector

from adwin_detector import AdwinDetector

def round_to_hundreds(x):
    return int(round(x / 100.0)) * 100

#Numerical data
#df = pd.read_csv('sequences/sequence_2018_04_29-15.35.45.csv')
# seq1 = np.array(df['light'])
# seq1 = en.encode_int(seq1)
# seq2 = np.array(df['temperature'])
# seq3 = np.array(df['occupancy'])

#df = pd.read_csv('sequences/sequence_2018_04_30-14.42.37.csv')
#df = pd.read_csv('sequences/sequence_2018_05_03-16.54.37.csv')
df = pd.read_csv('sequences/sequence_2018_05_07-19.06.27.csv')
seq1 = np.array(df['attr_1'])
seq2 = np.array(df['attr_2'])
seq3 = np.array(df['attr_3'])
seq4 = np.array(df['attr_4'])

for i in range(0):
    seq1 = np.concatenate((seq1, seq1))
    seq2 = np.concatenate((seq2, seq2))
    seq3 = np.concatenate((seq3, seq3))
    seq4 = np.concatenate((seq4, seq4))

print("seq len:", len(seq1))
win_size = 20
print("win size:", win_size)

detector1 = ZScoreDetector(window_size = win_size, threshold=4.5)
detector2 = ZScoreDetector(window_size = win_size, threshold=4.5)
detector3 = ZScoreDetector(window_size = win_size, threshold=5.5)
detector4 = ZScoreDetector(window_size = win_size, threshold=4)

# detector1 = AdwinDetector()
# detector2 = AdwinDetector()
# detector3 = AdwinDetector()
# detector4 = AdwinDetector()

rules_detector = RulesDetector(target_seq_index=3, 
                               window_size=0,
                               round_to=100,
                               type="all")

simulator = OnlineSimulator(rules_detector,
                            [detector1, detector2, detector3, detector4],
                            [seq1, seq2, seq3, seq4],
                            ["attr_1", "attr_2", "attr_3", "attr_4"])


import time
start_time = time.time()

simulator.run(plot=True, detect_rules=True)
print_detected_change_points(simulator.get_detected_changes())
print_rules(simulator.get_rules_sets(), 0)
print_combined_rules(simulator.get_combined_rules(), 0)

end_time = time.time()
print(end_time - start_time)