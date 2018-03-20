import numpy as np
import sys; sys.path.append('./detectors/')
import pandas as pd
import encoders as en
import scipy as sp
from scipy import signal
from detector import ChangeDetector
from detector import OnlineSimulator
from page_hinkley_detector import PageHinkleyDetector

#Numerical data
df = pd.read_csv('sequences/sequence_2017_11_28-18.07.57.csv')
seq = np.array(df['attr_1'])

# Symbolic data
# df = pd.read_csv('sequences/sequence_2017_11_22-19.35.27.csv')
# seq = np.array(df['day_of_week'])
# seq = en.encode(seq)
# seq = [np.abs(np.mean(e)) for e in seq]

detector = PageHinkleyDetector(delta=0.001, lambd=20, alpha=0.99)
simulator = OnlineSimulator(detector, seq)
simulator.run()

detected_change_points = simulator.get_detected_changes()
print(np.array(detected_change_points)- int(2/3 * len(seq)))
