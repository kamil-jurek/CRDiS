import sys; sys.path.append('./detectors/')
import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy as sp
from scipy import signal

import encoders as en
#from rules_detector_2 import RulesDetector
from adwin_detector import AdwinDetector
from online_simulator import OnlineSimulator
from rules_detector import RulesDetector
from utils import *
from zscore_detector import ZScoreDetector

#df = pd.read_csv('sequences/sequence_2018_04_30-14.42.37.csv')
df = pd.read_csv('sequences/sequence_2018_05_03-16.54.37.csv')
#df = pd.read_csv('sequences/sequence_2018_05_07-19.06.27.csv')
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
                            sequences,
                            seq_names)

start_time = time.time()

simulator.run(plot=True, detect_rules=True, predict_seq=True)
#print_detected_change_points(simulator.get_detected_changes())
print_rules(simulator.get_rules_sets(), 5)
#print_combined_rules(simulator.get_combined_rules(), 0)

end_time = time.time()
print(end_time - start_time)

for k, p in enumerate(simulator.predictor.predictions):
    print(k ,":", p)

pr = int(len(sequences[3])*0.9) + 20
predicted = simulator.predictor.predicted[pr:len(sequences[3])]
real = sp.signal.medfilt(sequences[3][pr:],21)

plt.figure()
plt.plot(real, 'b')
plt.plot(predicted, 'r', linewidth=3.0)

# mse = np.mean((real - predicted)**2)
# print("pred len:", real)
# print("real len:", predicted)
# print("mse:", mse)
rmse = np.sqrt(((predicted - real) ** 2).mean())
print('Mean Squared Error: {}'.format(round(rmse, 5)))

# print("pred:", simulator.predictor.predicted[-1420:])
# print("real:", sequences[3][-1420:])

plt.show()