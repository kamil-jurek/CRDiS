import matplotlib.pyplot as plt
import numpy as np
import sys; sys.path.append('./detectors/')
import pandas as pd
import encoders as en
from detector import ChangeDetector
from detector import OnlineSimulator
from zscore_detector import ZScoreDetector
from math import gcd

def myround(x, base=10):
    return int(base * round(float(x)/base))

#Numerical data
#df = pd.read_csv('sequences/sequence_2017_11_22-19.55.44.csv')
df = pd.read_csv('sequences/sequence_2017_11_28-18.07.57.csv')
#df = pd.read_csv('sequences/sequence_2017_12_01-22.11.54.csv')
sequence = np.array(df['attr_1'])

# Symbolic data
# df = pd.read_csv('sequences/sequence_2017_11_22-19.35.27.csv')
# sequence = np.array(df['day_of_week'])
# sequence = en.encode(sequence)
#sequence = sp.signal.medfilt(sequence,21)

win_size = int(len(sequence)*(1/100))
print("win size:", win_size)

detector = ZScoreDetector(window_size = win_size, threshold=2.5)
simulator = OnlineSimulator(detector, sequence)
simulator.run()

stops = simulator.get_detected_changes()
print(np.array(stops)- int(2/3 * len(sequence)))
print(np.array(stops))

subseqs = []
indexes = []
gcd_ = stops[0]

roundTo = 10
first = myround(stops[0], roundTo)
for i in np.arange(0, len(stops)-1):
    s = myround(stops[i], roundTo)
    e = myround(stops[i+1], roundTo)

    indexes.append(s-first)
    if i == len(stops)-2:
        indexes.append(e-first)

    gcd_ = gcd(gcd_,e)
    print(s, e)
    subseq = sequence[s:e]

    m = round(np.mean(subseq))
    seq = [m for i in np.arange(s-first, e-first)]
    subseqs.append(seq)
    plt.plot(np.arange(s, e), seq, '.')

gcd_ = 50
print("gcd:", gcd_)
indexes = np.array(indexes) / gcd_
print("indexes:", indexes)

shortSeq = []
for s in subseqs:
    shortSeq.append(s[0:int(len(s)/gcd_)])

with open('shortSeq.txt', 'w') as f:
    for seq in shortSeq:
        for  elem in seq:
            f.write(str(int(elem)) + ', ')
            #f.write(str(int(elem)) + ' -1 ')
    #f.write('-2\n')

print(shortSeq)




plt.show()
