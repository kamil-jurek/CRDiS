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

from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
import category_encoders as ce

def encode2(data):
    # Specify the columns to encode then fit and transform
    #encoder = ce.polynomial.PolynomialEncoder()
    #encoder = ce.OneHotEncoder()
    #encoder = ce.BackwardDifferenceEncoder()
    #encoder = ce.BinaryEncoder( ) #obiecujacy
    #encoder = ce.HashingEncoder( )
    encoder = ce.HelmertEncoder( ) #obiecujacy
    #encoder = ce.OrdinalEncoder( ) #simple but working
    #encoder = ce.SumEncoder()
    encoder.fit(data, verbose=1)
    data = encoder.transform(data)
    data = data.values.tolist()

    print(data[:5])
    return data

def encode(data):
    values = np.array(data)
    #print("Values:", values)
    # integer encode
    label_encoder = LabelEncoder()
    integer_encoded = label_encoder.fit_transform(values)+1
    #print("Integer encoded:", integer_encoded)
    # binary encode
    #onehot_encoder = OneHotEncoder(sparse=False)
    #integer_encoded = integer_encoded.reshape(len(integer_encoded), 1)
    #onehot_encoded = onehot_encoder.fit_transform(integer_encoded)
    #print("One hot encoded:", onehot_encoded)

    return integer_encoded
    #return onehot_encoded

# df = pd.read_csv('sequences/sequence_2017_11_05-14.11.15.csv')
# signal = np.array(df['attr_1'])

# df = pd.read_csv('sequences/sequence_2017_11_05-18.43.29.csv')
# signal = np.array(df['attr_1'])

# df = pd.read_csv('sequences/sequence_2017_11_05-18.43.33.csv')
# signal = np.array(df['attr_1'])

# df = pd.read_csv('sequences/sequence_2017_11_05-18.50.48.csv')
# signal = np.array(df['attr_1'])

df = pd.read_csv('sequences/sequence_2017_11_08-22.06.35.csv')
signal = np.array(df['attr_1'])
signal = encode2(signal)

# Create detector
#detector = MeanDetector(threshold=0.3)
detector = ZScoreDetector(window_size = 5, threshold=2)
#detector = StackZScoreDetector(signal, lag=55, threshold=1, influence=0.3)
#detector = PageHinkleyDetector(delta=0.001, lambd=4.5, alpha=0.99)
#detector = DDMDetector(m_p=1, m_s=0)
#detector = CusumDetector(delta=0.005, lambd=5)
#detector = AdwinDetector(delta = 0.01)
OnlineSimulator(detector, signal).run()

adwin =  AdwinDetector(delta = 0.01)
data_stream = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.7]

# for data in data_stream:
#   if (adwin.update(data)):
#     print("Change has been detected in data: ", str(data))
#   print(data, "E:",adwin.getEstimation()) # Prints the next value of the estimated form of data_s
