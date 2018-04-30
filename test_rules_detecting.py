import numpy as np
import sys; sys.path.append('./detectors/')
import pandas as pd

import encoders as en

from utils import *
from online_simulator import OnlineSimulator
from zscore_detector import ZScoreDetector
from rules_detector import RulesDetector

def round_to_hundreds(x):
    return int(round(x / 100.0)) * 100


# df = pd.read_csv('air.csv')
# #Date;Time;CO(GT);PT08.S1(CO);NMHC(GT);C6H6(GT);PT08.S2(NMHC);NOx(GT);PT08.S3(NOx);NO2(GT);PT08.S4(NO2);PT08.S5(O3);T;RH;AH;;
# seq1 = np.array(df['CO'][:1000].apply(np.round))
# seq2 = np.array(df['PT08.S1'][:1000].apply(np.round))
# seq3 = np.array(df['NMHC'][:1000].apply(np.round))
# seq4 = np.array(df['C6H6'][:1000].apply(np.round))
# seq5 = np.array(df['PT08.S2'][:1000].apply(np.round))
# seq6 = np.array(df['NOx'][:1000].apply(np.round))


df = pd.read_csv('ocupancy.csv')
#"nr","date","Temperature","Humidity","Light","CO2","HumidityRatio","Occupancy"
seq1 = np.array(df['Temperature'].apply(np.round))
seq2 = np.array(df['Humidity'].apply(np.round))
seq3 = np.array(df['Light'].apply(np.round))
seq4 = np.array(df['CO2'].apply(np.round))
seq5 = np.array(df['HumidityRatio'])
seq6 = np.array(df['Occupancy'])

#Numerical data
#df = pd.read_csv('sequences/sequence_2018_04_15-22.22.16.csv')
#df = pd.read_csv('sequences/sequence_2018_04_22-17.15.32.csv')
#df = pd.read_csv('sequences/sequence_2018_04_13-22.33.30.csv')
#df = pd.read_csv('electricity.csv')
#date,day,period,nswprice,nswdemand,vicprice,vicdemand,transfer,class
# df = pd.read_csv('ords.csv')
# seq1 = np.array(df['a1'])
# seq2 = np.array(df['a2'])
# seq3 = np.array(df['a3'])
# seq4 = np.array(df['a4'])
# seq5 = np.array(df['a5'])
# seq6 = np.array(df['a6'])
# seq7 = np.array(df['a7'])
# seq8 = np.array(df['a8'])
# seq9 = np.array(df['a9'])
# seq12 = np.array(df['bass'])
# seq12 = en.encode_int(seq12)
# seq13 = np.array(df['meter'])
# seq14 = np.array(df['cord'])
# seq14 = en.encode_int(seq14)
for i in range(0):
    seq1 = np.concatenate((seq1, seq1))
    seq2 = np.concatenate((seq2, seq2))
    seq3 = np.concatenate((seq3, seq3))
    seq4 = np.concatenate((seq4, seq4))

print("seq len:", len(seq1))
win_size = 15
print("win size:", win_size)

detector1 = ZScoreDetector(window_size = win_size, threshold=6)
detector2 = ZScoreDetector(window_size = win_size, threshold=6)
detector3 = ZScoreDetector(window_size = win_size, threshold=6)
detector4 = ZScoreDetector(window_size = win_size, threshold=6)
detector5 = ZScoreDetector(window_size = win_size, threshold=6)
detector6 = ZScoreDetector(window_size = win_size, threshold=6)
# detector7 = ZScoreDetector(window_size = win_size, threshold=2)
# detector8 = ZScoreDetector(window_size = win_size, threshold=2)
# detector9 = ZScoreDetector(window_size = win_size, threshold=2)
# detector12 = ZScoreDetector(window_size = win_size, threshold=2)
# detector13 = ZScoreDetector(window_size = win_size, threshold=2)
# detector14 = ZScoreDetector(window_size = win_size, threshold=2)

rules_detector = RulesDetector(target_seq_index=5)

# simulator = OnlineSimulator(rules_detector,
#                             [detector1, detector2, detector3, detector4,detector5, detector6, detector7, detector8,detector9, detector12, detector13, detector14],
#                             [seq1, seq2, seq3, seq4,seq5, seq6, seq7, seq8,seq9, seq12, seq13, seq14],
#                             ["a1", "a2", "a3", "a4","5", "a6", "a7", "a8","a9", "a12", "a13", "a14"])
simulator = OnlineSimulator(rules_detector,
                            [detector1, detector2, detector3, detector4,detector5, detector6],
                            [seq1, seq2, seq3, seq4,seq5, seq6],
                            ["Temperature", "Humidity", "Light", "CO2","HumidityRatio", "Occupancy"])

# simulator = OnlineSimulator(rules_detector,
#                             [detector1, detector2, detector3, detector4,detector5, detector6],
#                             [seq1, seq2, seq3, seq4,seq5, seq6],
#                             ["CO","PT08.S1","NMHC","C6H6","PT08.S2","NOx"])
simulator.run(plot=True, detect_rules=True)

print_rules(simulator.get_rules_sets())
print_combined_rules(simulator.get_combined_rules())
