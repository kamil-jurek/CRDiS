import matplotlib.pyplot as plt
import numpy as np
import sys; sys.path.append('./detectors/')
import pandas as pd
import encoders as en
import scipy as sp
from scipy import signal
from detector import ChangeDetector
from detector import OnlineSimulator
from page_hinkley_detector import PageHinkleyDetector

def runningMean(x, N):
    return np.convolve(x, np.ones((N,))/N)[(N-1):]

#Numerical data
df = pd.read_csv('sequences/sequence_2017_11_24-20.16.00.csv')
signal = np.array(df['attr_1'])
#b, a = sp.signal.butter(3, 0.5)
#signal = sp.signal.filtfilt(b, a, signal, padlen=150)
#########
filtered = sp.signal.medfilt(signal,21)
#########
#signal = pd.rolling_mean(signal,5).tolist()
#########
# n = 15  # the larger n is, the smoother curve will be
# b = [1.0 / n] * n
# a = 1
# signal = sp.signal.lfilter(b,a,signal)
# signal = sp.signal.hilbert(signal)
#signal = runningMean(signal, 25)
#win = sp.signal.hann(51)
#filtered = sp.signal.convolve(signal, win, mode='full') / sum(win)

plt.plot(signal, 'b.')
#plt.plot(filtered, 'r.')

# Symbolic data
# df = pd.read_csv('sequences/sequence_2017_11_22-19.35.27.csv')
# signal = np.array(df['day_of_week'])
# signal = en.encode(signal)


detector = PageHinkleyDetector(delta=0.001, lambd=100, alpha=0.99)
simulator = OnlineSimulator(detector, signal)
simulator.run()

stops = simulator.get_detected_changes()
print(np.array(stops)- int(2/3 * len(signal)))
