import matplotlib.pyplot as plt
import numpy as np
import sys; sys.path.append('./detectors/')
import pandas as pd
import encoders as en
from detector import ChangeDetector
from detector import OnlineSimulator
from zscore_rules import ZScoreDetectorRules
from math import gcd

#Numerical data
#df = pd.read_csv('sequences/sequence_2017_11_22-19.55.44.csv')
df = pd.read_csv('sequences/sequence_2017_11_28-18.07.57.csv')
#df = pd.read_csv('sequences/sequence_2017_12_01-22.11.54.csv')
#df = pd.read_csv('sequences/sequence_2018_01_15-19.44.57.csv')
sequence = np.array(df['attr_1'])

# Symbolic data
# df = pd.read_csv('sequences/sequence_2017_11_22-19.35.27.csv')
# sequence = np.array(df['day_of_week'])
# sequence = en.encode(sequence)
#sequence = sp.signal.medfilt(sequence,21)

win_size = int(len(sequence)*(1/100))
print("win size:", win_size)

detector = ZScoreDetectorRules(window_size = win_size, threshold=2.5)
simulator = OnlineSimulator(detector, sequence)
simulator.run()
