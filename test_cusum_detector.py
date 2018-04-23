import numpy as np
import sys; sys.path.append('./detectors/')
import pandas as pd
import encoders as en
from detector import ChangeDetector
from online_simulator import OnlineSimulator
from cusum_detector import CusumDetector


#Numerical data
df = pd.read_csv('sequences/sequence_2017_11_28-18.07.57.csv')
seq_1 = np.array(df['attr_1'])
seq_2 = np.array(df['attr_2'])

# Symbolic data
# df = pd.read_csv('sequences/sequence_2017_11_22-19.35.27.csv')
# seq = np.array(df['day_of_week'])
# seq = en.encode(seq)
# seq = [np.abs(np.mean(e)) for e in seq]

detector_1 = CusumDetector(delta=0.005, lambd=25)
detector_2 = CusumDetector(delta=0.005, lambd=25)

simulator = OnlineSimulator(None,
                            [detector_1, detector_2],
                            [seq_1,seq_2],
                            ['attr_1', 'attr_2'])
simulator.run(plot=True, detect_rules=False)



