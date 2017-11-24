import matplotlib.pyplot as plt
import numpy as np
import sys; sys.path.append('./detectors/')
import pandas as pd
import encoders as en
from detector import ChangeDetector
from detector import OnlineSimulator
from zscore_detector import ZScoreDetector


#Numerical data
df = pd.read_csv('sequences/sequence_2017_11_22-19.55.44.csv')
signal = np.array(df['attr_1'])

# Symbolic data
# df = pd.read_csv('sequences/sequence_2017_11_22-19.35.27.csv')
# signal = np.array(df['day_of_week'])
# signal = en.encode(signal)
#signal = sp.signal.medfilt(signal,21)

win_size = int(len(signal)*(5/200))
print("win size:", win_size)

detector = ZScoreDetector(window_size = win_size, threshold=2)
simulator = OnlineSimulator(detector, signal)
simulator.run()

stops = simulator.get_detected_changes()
print(np.array(stops)- int(2/3 * len(signal)))
