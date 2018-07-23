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

df = pd.read_csv('sequences/sequence_2018_07_21-22.24.18.csv')
seq_names = ['attr_1', 'attr_4' ]

predict_ratio=0.8

base_seqs =[]

for name in seq_names:
    base_seqs.append(np.array(df[name]))

sequences = [[] for i in range(len(base_seqs))]
for nr in range(1):
    for i, seq in enumerate(sequences):
        sequences[i] = np.concatenate((seq, base_seqs[i]))

win_size = 20
detector1 = ZScoreDetector(window_size = 30, threshold=5)
detector4 = ZScoreDetector(window_size = win_size, threshold=4)

rules_detector = RulesDetector(target_seq_index=1,
                               window_size=0,
                               round_to=100,
                               type="all",
                               combined=False)

simulator = OnlineSimulator(rules_detector,
                            [detector1, detector4],
                            sequences,
                            seq_names,
                            predict_ratio=predict_ratio)

start_time = time.time()

simulator.run(plot=True, detect_rules=True, predict_seq=True)

#print_detected_change_points(simulator.get_detected_changes())
#print_rules(simulator.get_rules_sets(), 0)
print("------------------------------------------------------------------------------------------")
#print_combined_rules(simulator.get_combined_rules(), 0)

end_time = time.time()
print(end_time - start_time)

for k, p in enumerate(simulator.predictor.predictions):
    print(k ,":", p)

pr = int(len(sequences[1])*predict_ratio) + 20
predicted = simulator.predictor.predicted[pr:len(sequences[1])]
real = sp.signal.medfilt(sequences[1][pr:],21)

plt.figure()
plt.plot(real, 'b')
plt.plot(predicted, 'r', linewidth=3.0)

mse = np.mean((real - predicted)**2)
print("pred len:", real)
print("real len:", predicted)
print("mse:", mse)
rmse = np.sqrt(((predicted - real) ** 2).mean())
print('Mean Squared Error: {}'.format(round(rmse, 5)))



plt.show()