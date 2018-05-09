import numpy as np
import sys; sys.path.append('./detectors/')
import pandas as pd
import encoders as en
from detector import ChangeDetector
from online_simulator import OnlineSimulator
from zscore_detector import ZScoreDetector

#Numerical data
df = pd.read_csv('sequences/sequence_2017_11_28-18.07.57.csv')
seq = np.array(df['attr_1'])

# Symbolic data
# df = pd.read_csv('sequences/sequence_2017_11_22-19.35.27.csv')
# sequence = np.array(df['day_of_week'])
# sequence = en.encode(sequence)

win_size = int(len(seq)*(1/100))
print("win size:", win_size)

detector = ZScoreDetector(window_size = win_size, threshold=2.5)
simulator = OnlineSimulator(None,
                            [detector],
                            [seq],
                            ["attr_1"])
simulator.run(plot=False, detect_rules=False)

detected_change_points = simulator.get_detected_changes()
print(np.array(detected_change_points))