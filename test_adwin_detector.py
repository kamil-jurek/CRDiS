import matplotlib.pyplot as plt
import numpy as np
import sys; sys.path.append('./detectors/')
import pandas as pd
import encoders as en
import scipy as sp
from scipy import signal
from detector import ChangeDetector
from detector import OnlineSimulator
from adwin_detector import AdwinDetector


#Numerical data
df = pd.read_csv('sequences/sequence_2017_11_24-20.16.00.csv')
signal = np.array(df['attr_1'])

# Symbolic data
# df = pd.read_csv('sequences/sequence_2017_11_22-19.35.27.csv')
# signal = np.array(df['day_of_week'])
# signal = en.encode(signal)

#Filtered data
signal = sp.signal.medfilt(signal,21)

detector = AdwinDetector(delta = 0.01)
simulator = OnlineSimulator(detector, signal)
simulator.run()

stops = simulator.get_detected_changes()
print(np.array(stops)- int(2/3 * len(signal)))
