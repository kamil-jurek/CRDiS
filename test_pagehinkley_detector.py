import numpy as np
import sys; sys.path.append('./detectors/')
import pandas as pd
import encoders as en
import scipy as sp
from scipy import signal
from detector import ChangeDetector
from sklearn.metrics import accuracy_score
from detector import OnlineSimulator
from page_hinkley_detector import PageHinkleyDetector

#Numerical data
#sequences/sequence_2017_11_28-18.07.57.csv
df = pd.read_csv('sequences/sequence_2018_03_24-13.19.49.csv')
seq1 = np.array(df['attr_1'])
seq2 = np.array(df['attr_2'])

# Symbolic data
# df = pd.read_csv('sequences/sequence_2017_11_22-19.35.27.csv')
# seq = np.array(df['day_of_week'])
# seq = en.encode(seq)
# seq = [np.abs(np.mean(e)) for e in seq]

detector1 = PageHinkleyDetector(delta=0.001, lambd=20, alpha=0.99)
detector2 = PageHinkleyDetector(delta=0.001, lambd=20, alpha=0.99)
simulator = OnlineSimulator([detector1, detector2], [seq1, seq2], ["attr_1", "attr_2"])
simulator.run()

actual_change_points = np.array([600, 800, 1000, 1300, 1500, 1800])
detected_change_points = np.array(simulator.get_detected_changes())
delta = np.abs(actual_change_points - detected_change_points)
#print(np.array(detected_change_points)- int(2/3 * len(seq)))

print("Actual change points: ", actual_change_points)
print("Detected change points: ", detected_change_points)
print("Diffrerence: ", delta, " sum: ", np.sum(delta))