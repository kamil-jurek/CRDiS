import numpy as np
import sys; sys.path.append('./detectors/')
import pandas as pd
import encoders as en

from detector import OnlineSimulator
from adwin_detector import AdwinDetector


#Numerical data
#df = pd.read_csv('sequences/sequence_2017_11_24-20.16.00.csv')
df = pd.read_csv('sequences/sequence_2017_11_28-18.07.57.csv')
seq = np.array(df['attr_1'])

# Symbolic data
# df = pd.read_csv('sequences/sequence_2017_11_22-19.35.27.csv')
# seq = np.array(df['day_of_week'])
# seq = en.encode(seq)
# seq = [np.abs(np.mean(e)) for e in seq]

detector = AdwinDetector(delta = 0.01)
simulator = OnlineSimulator(detector, seq)
simulator.run()

detected_change_points = simulator.get_detected_changes()
print(np.array(detected_change_points)- int(2/3 * len(seq)))
