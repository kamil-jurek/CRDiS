import numpy as np
import sys; sys.path.append('./detectors/')
import pandas as pd
import encoders as en

from utils import *
from online_simulator import OnlineSimulator
from adwin_detector import AdwinDetector
from rules_detector import RulesDetector


#Numerical data
#df = pd.read_csv('sequences/sequence_2017_11_24-20.16.00.csv')
df = pd.read_csv('sequences/sequence_2018_04_15-22.22.16.csv')
seq_1 = np.array(df['attr_1'])
seq_2 = np.array(df['attr_4'])

# Symbolic data
# df = pd.read_csv('sequences/sequence_2017_11_22-19.35.27.csv')
# seq_1 = np.array(df['day_of_week'])
# seq_1 = en.encode_int(seq_1)
# seq_2 = np.array(df['attr_2'])
# seq_2 = en.encode_int(seq_2)


detector_1 = AdwinDetector(delta = 0.01)
detector_2 = AdwinDetector(delta = 0.01)

rules_detector = RulesDetector(target_seq_index=1)

simulator = OnlineSimulator(rules_detector,
                            [detector_1, detector_2],
                            [seq_1, seq_2],
                            ['attr_1', 'attr_2'])

simulator.run(plot=True, detect_rules=True)

print_rules(simulator.get_rules_sets())
print_combined_rules(simulator.get_combined_rules())
