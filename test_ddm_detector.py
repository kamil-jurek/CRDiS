import matplotlib.pyplot as plt
import numpy as np
import sys; sys.path.append('./detectors/')
import pandas as pd
import encoders as en
import scipy as sp
from scipy import signal
from detector import ChangeDetector
from online_simulator import OnlineSimulator
from ddm2_detector import DDMDetector


#Numerical data
df = pd.read_csv('sequences/sequence_2017_11_28-18.07.57.csv')
seq = np.array(df['attr_1'])

# Symbolic data
# df = pd.read_csv('sequences/sequence_2017_11_22-19.35.27.csv')
# seq = np.array(df['day_of_week'])
# seq = en.encode(signal)

detector = DDMDetector(lambd=25)

simulator = OnlineSimulator(None,
                            [detector],
                            [seq],
                            ['attr_1'])
simulator.run(plot=True, detect_rules=False)


