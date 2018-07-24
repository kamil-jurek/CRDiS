import sys; sys.path.append('./detectors/')
import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy as sp
from scipy import signal

from online_simulator import OnlineSimulator
from rules_detector import RulesDetector
from utils import *
from zscore_detector import ZScoreDetector

#df = pd.read_csv('sequences/sequence_2018_04_30-14.42.37.csv')
#df = pd.read_csv('sequences/sequence_2018_05_03-16.54.37.csv')
#df = pd.read_csv('sequences/sequence_2018_05_07-19.06.27.csv')
#df = pd.read_csv('sequences/sequence_2018_07_21-20.53.53.csv')
df = pd.read_csv('sequences/sequence_2018_07_21-22.24.18.csv')
seq_names = ['attr_1', 'attr_2', 'attr_3','attr_4' ]

base_seqs =[]

for name in seq_names:
    base_seqs.append(np.array(df[name]))
    #sequences.append(np.array(df[name]))

sequences = [[] for i in range(len(base_seqs))]
for nr in range(1):
    for i, seq in enumerate(sequences):
        sequences[i] = np.concatenate((seq, base_seqs[i]))

win_size = 20
detector1 = ZScoreDetector(window_size = 30, threshold=5)
detector2 = ZScoreDetector(window_size = win_size, threshold=4.5)
detector3 = ZScoreDetector(window_size = win_size, threshold=5.5)
detector4 = ZScoreDetector(window_size = win_size, threshold=4)

rules_detector = RulesDetector(target_seq_index=3,
                               window_size=0,
                               round_to=100,
                               type="all",
                               combined=True)

simulator = OnlineSimulator(rules_detector,
                            [detector1, detector2, detector3, detector4],
                            sequences,
                            seq_names)

start_time = time.time()

simulator.run(plot=True, detect_rules=True, predict_seq=False)

print_detected_change_points(simulator.get_detected_changes())

generate_classical_dataset(simulator.get_detected_changes())
#print_rules(simulator.get_rules_sets(), 0)
# print("------------------------------------------------------------------------------------------")
# print_combined_rules(simulator.get_combined_rules(), 0)
#
# end_time = time.time()
# print(end_time - start_time)

plt.show()