import numpy as np

from collections import deque
from change_detector import ChangeDetector

class ZScoreDetector(ChangeDetector):
    def __init__(self, window_size = 100, threshold=0.05):
        super( ZScoreDetector, self ).__init__()
        self.threshold = threshold
        self.window_size = window_size
        self.k = 0  # total signal_size
        self.g_mean_ = 0.0  # global mean
        self.s_ = 0.0  # for Welford's method. variance = s / (k + 1)
        self.window = deque(maxlen = window_size)
        self.z_score_ = np.nan
        self.window_mean_ = 0.0
        self.g_std_ = 0.0

    def update_residuals(self, new_signal_value):
        self._update_base_residuals(new_signal_value)
        x = new_signal_value
        self.window.append(x)

        # Calculate global statistics using welford's method
        oldm = self.g_mean_
        newm = oldm + (x - oldm) / (self.k + 1)
        s = self.s_ + (x - newm) * (x - oldm)

        g_mean_ = newm  # Global mean
        g_std = np.sqrt(s / (self.k+1))  # Global std

        w_mean = np.mean(self.window)  # Window mean
        w_std = np.std(self.window)  # Window std
        self.window_mean_ = w_mean

        std_diff = (g_std - w_std) / g_std
        SE = g_std / np.sqrt(self.window_size)

        mean_diff = (g_mean_ - w_mean) / g_mean_

        self.z_score_ = (w_mean - g_mean_) / SE
        self.g_mean_ = g_mean_
        self.g_std_ = g_std
        self.s_ = s
        self.k += 1

    def check_stopping_rules(self, new_signal_value):
        self.rules_triggered = False
        if np.absolute(self.z_score_) > self.threshold:
            #print("value:  ", new_signal_value)
            #print("zscore: ", np.absolute(self.z_score_))
            self.rules_triggered = True
            # self.k = 0  # total signal_size
            # self.g_mean_ = 0.0  # global mean
            # self.s_ = 0.0  # for Welford's method. variance = s / (k + 1)
            # self.z_score_ = np.nan
            # self.window_mean_ = 0.0
            # self.g_std_ = 0.0
