import numpy as np
import sys; sys.path.append('./detectors/')
import pandas as pd
import encoders as en
from detector import ChangeDetector
from detector import OnlineSimulator
from zscore_detector import ZScoreDetector

def round_to_hundreds(x):
    return int(round(x / 100.0)) * 100


#Numerical data
#df = pd.read_csv('sequences/sequence_2017_11_28-18.07.57.csv')
#seq = np.array(df['attr_1'])
df = pd.read_csv('sequences/sequence_2018_03_25-17.24.22.csv')
seq1 = np.array(df['attr_1'])
seq2 = np.array(df['attr_2'])
seq4 = np.array(df['attr_4'])

# Symbolic data
# df = pd.read_csv('sequences/sequence_2017_11_22-19.35.27.csv')
# sequence = np.array(df['day_of_week'])
# sequence = en.encode(sequence)

win_size = int(len(seq1)*(1/100))
print("win size:", win_size)

detector1 = ZScoreDetector(window_size = win_size, threshold=3)
detector2 = ZScoreDetector(window_size = win_size, threshold=3.5)
detector4 = ZScoreDetector(window_size = win_size, threshold=3)

simulator = OnlineSimulator([detector1, detector2, detector4],
                            [seq1, seq2, seq4],
                            ["attr_1", "attr_2", "attr_4"])
simulator.run(plot=False)

#print(simulator.get_detected_changes())
detected_change_points = np.array(simulator.get_detected_changes())

for cps in detected_change_points:
    print(cps)