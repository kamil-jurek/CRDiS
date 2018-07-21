import numpy as np
import sys; sys.path.append('./detectors/')
import pandas as pd
import encoders as en
from detector import ChangeDetector
from online_simulator import OnlineSimulator
from mean_detector import MeanDetector
from rules_detector import RulesDetector
import matplotlib.pyplot as plt

#Numerical data
df = pd.read_csv('sequences/sequence_2017_11_28-18.07.57.csv')
seq = np.array(df['attr_1'])

# Symbolic data
#df = pd.read_csv('sequences/sequence_2017_11_22-19.35.27.csv')
#seq = np.array(df['day_of_week'])
#seq = en.encode(signal)

detector = MeanDetector(threshold=0.005)
detector2 = MeanDetector(threshold=0.005)

rules_detector = RulesDetector(target_seq_index=1, type="generate_discretized")

simulator = OnlineSimulator(rules_detector,
                            [detector, detector2],
                            [seq, seq],
                            ['attr_1', 'arttt'])
simulator.run(plot=True, detect_rules=False)

detected_change_points = simulator.get_detected_changes()
print(np.array(detected_change_points))
plt.show()