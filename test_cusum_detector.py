import matplotlib.pyplot as plt
import numpy as np
import sys; sys.path.append('./detectors/')
import pandas as pd
import encoders as en
from detector import ChangeDetector
from detector import OnlineSimulator
from cusum_detector import CusumDetector


#Numerical data
# df = pd.read_csv('sequences/sequence_2017_11_24-20.16.00.csv')
# signal = np.array(df['attr_1'])

# Symbolic data
df = pd.read_csv('sequences/sequence_2017_11_22-19.35.27.csv')
signal = np.array(df['day_of_week'])
signal = en.encode(signal)
#signal = sp.signal.medfilt(signal,21)

detector = CusumDetector(delta=0.005, lambd=20)
simulator = OnlineSimulator(detector, signal)
simulator.run()

stops = simulator.get_detected_changes()
print(np.array(stops)- int(2/3 * len(signal)))
