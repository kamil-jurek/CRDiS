import matplotlib.pyplot as plt
import numpy as np
import sys; sys.path.append('../src/')
import pandas as pd
from change_detector import ChangeDetector
from change_detector import OnlineSimulator
from change_detector import MeanDetector
from change_detector import ZScoreDetector

df = pd.read_csv('sequences/sequence_2017_11_01-21:24:04.csv')
signal = df['attr_1']

# Create detector
#detector = MeanDetector(threshold=0.1)
detector = ZScoreDetector(window_size = 10, threshold=0.5)
OnlineSimulator(detector, signal).run()
