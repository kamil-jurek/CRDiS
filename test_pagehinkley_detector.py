import numpy as np
import sys
sys.path.append('./detectors/')
sys.path.insert(0, './rules_mining/')
import pandas as pd
import math
import encoders as en
import scipy as sp
from scipy import signal
from detector import ChangeDetector
from sklearn.metrics import accuracy_score
from online_simulator import OnlineSimulator
from page_hinkley_detector import PageHinkleyDetector

def round_to_hundreds(x):
    return int(round(x / 100.0)) * 100

#Numerical data
#sequences/sequence_2017_11_28-18.07.57.csv
#df = pd.read_csv('sequences/sequence_2018_03_24-13.19.49.csv')
df = pd.read_csv('sequences/sequence_2018_03_25-17.24.22.csv')
seq1 = np.array(df['attr_1'])
seq2 = np.array(df['attr_2'])
seq3 = np.array(df['attr_3'])
seq4 = np.array(df['attr_4'])

# Symbolic data
# df = pd.read_csv('sequences/sequence_2017_11_22-19.35.27.csv')
# seq = np.array(df['day_of_week'])
# seq = en.encode(seq)
# seq = [np.abs(np.mean(e)) for e in seq]

detector1 = PageHinkleyDetector(delta=0.001, lambd=20, alpha=0.99)
detector2 = PageHinkleyDetector(delta=0.001, lambd=20, alpha=0.99)
detector3 = PageHinkleyDetector(delta=0.001, lambd=30, alpha=0.99)
detector4 = PageHinkleyDetector(delta=0.001, lambd=20, alpha=0.99)
simulator = OnlineSimulator(None,
                            [detector1, detector2, detector3, detector4],
                            [seq1, seq2, seq3, seq4],
                            ["attr_1", "attr_2", "attr_3", "attr_4"])
simulator.run(plot=True,detect_rules=False)

print(simulator.get_detected_changes())
detected_change_points = np.array(simulator.get_detected_changes())
