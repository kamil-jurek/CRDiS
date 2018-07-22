import matplotlib.pyplot as plt
import numpy as np
import sys; sys.path.append('./detectors/')
import pandas as pd
from detector import ChangeDetector
from detector import OnlineSimulator
from mean_detector import MeanDetector
from page_hinkley_detector import PageHinkleyDetector
from zscore_detector import ZScoreDetector
from stack_zscore_detector import StackZScoreDetector
from ddm_detector import DDMDetector
from cusum_detector import CusumDetector
from adwin_detector import AdwinDetector
from entropy_detector import EntropyDetector

from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
import category_encoders as ce

import scipy as sp
from scipy import signal

def encode(data):
    #encoder = ce.BinaryEncoder( ) #obiecujacy
    encoder = ce.HelmertEncoder( ) #obiecujacy
    #encoder = ce.OrdinalEncoder( ) #simple but working

    #encoder = ce.polynomial.PolynomialEncoder()
    #encoder = ce.OneHotEncoder()
    #encoder = ce.BackwardDifferenceEncoder()
    #encoder = ce.HashingEncoder( )
    #encoder = ce.SumEncoder()
    encoder.fit(data, verbose=1)
    data = encoder.transform(data)
    data = data.values.tolist()

    #print(data[len(signal)-1])
    return data

def encode_int(data):
    values = np.array(data)
    label_encoder = LabelEncoder()
    integer_encoded = label_encoder.fit_transform(values)+1

    return integer_encoded

data = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
print("Encode", encode(data))


df = pd.read_csv('sequences/sequence_2017_11_24-20.16.00.csv')
signal = np.array(df['attr_1'])

# df = pd.read_csv('sequences/sequence_2017_11_05-18.43.29.csv')
# signal = np.array(df['attr_1'])

# df = pd.read_csv('sequences/sequence_2017_11_05-18.43.33.csv')
# signal = np.array(df['attr_1'])

#df = pd.read_csv('sequences/sequence_2017_11_22-20.43.46..csv')
#signal = np.array(df['attr_1'])

# Symbolic data
#df = pd.read_csv('sequences/sequence_2017_11_22-19.27.01.csv')
#df = pd.read_csv('sequences/sequence_2017_11_11-12.16.43.csv')
#df = pd.read_csv('sequences/sequence_2017_11_11-12.17.26.csv')
#df = pd.read_csv('sequences/sequence_2017_11_08-22.06.35.csv')
#signal = np.array(df['day_of_week'])
#signal = encode_int(signal)
#signal = sp.signal.medfilt(signal,21)
#print(signal)

win_size = int(len(signal)*(5/250))
print("win size:", win_size)
# Create detector
#detector = GeometricMovingAverageDetector(threshold=0.85)
detector = ZScoreDetector(window_size = win_size, threshold=2.5)
#detector = StackZScoreDetector(signal, lag=55, threshold=1, influence=0.3)
#detector = PageHinkleyDetector(delta=0.001, lambd=15, alpha=0.99)
#detector = DDMDetector(lambd=20)
#detector = CusumDetector(delta=0.005, lambd=20)
#detector = AdwinDetector(delta = 0.01)
#detector = EntropyDetector(threshold=1)
simulator = OnlineSimulator(detector, signal)
simulator.run()
stops = simulator.get_detected_changes()
print(np.array(stops)- int(2/3 * len(signal)))

#adwin =  AdwinDetector(delta = 0.01)
#data_stream = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.7]
# for data in data_stream:
#   if (adwin.update(data)):
#     print("Change has been detected in data: ", str(data))
#   print(data, "E:",adwin.getEstimation()) # Prints the next value of the estimated form of data_s
