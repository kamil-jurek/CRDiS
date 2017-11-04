import matplotlib.pyplot as plt
import numpy as np
import sys; sys.path.append('../src/')
import pandas as pd
from change_detector import ChangeDetector
from change_detector import OnlineSimulator
from mean_detector import MeanDetector
from page_hinkley_detector import PageHinkleyDetector
from zscore_detector import ZScoreDetector
from stack_zscore_detector import StackZScoreDetector
from ddm_detector import DDMDetector

df = pd.read_csv('sequences/sequence_2017_11_01-21:24:04.csv')
signal = np.array(df['attr_1'])

# Create detector
#detector = MeanDetector(threshold=0.3)
#detector = ZScoreDetector(window_size = 5, threshold=2)
#detector = StackZScoreDetector(signal, lag=55, threshold=1, influence=0.3)
#detector = PageHinkleyDetector(delta=0.005, lambd=4, alpha=0.99)
detector = DDMDetector(m_p=1, m_n=1, m_s=0)

OnlineSimulator(detector, signal).run()
