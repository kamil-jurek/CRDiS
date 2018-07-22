import numpy as np
import sys; sys.path.append('./detectors/')
import pandas as pd
import matplotlib.pyplot as plt

import encoders as en
from detector import ChangeDetector
from online_simulator import OnlineSimulator
from geometric_moving_average_detector import GeometricMovingAverageDetector
from rules_detector import RulesDetector


#Numerical data
df = pd.read_csv('sequences/sequence_2017_11_28-18.07.57.csv')
seq = np.array(df['attr_1'])


detector = GeometricMovingAverageDetector(threshold=0.75)
simulator = OnlineSimulator(None,
                            [detector],
                            [seq],
                            ['attr_1'])

simulator.run(plot=True, detect_rules=False)

detected_change_points = simulator.get_detected_changes()
print(np.array(detected_change_points))
plt.show()