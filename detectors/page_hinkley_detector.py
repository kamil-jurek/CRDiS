import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
from scipy import signal
from detector import ChangeDetector

class PageHinkleyDetector(ChangeDetector):

    def __init__(self, delta=0.005, lambd=50, alpha=1 - 0.0001):
        super( PageHinkleyDetector, self ).__init__()
        self.delta = delta
        self.lambd = lambd
        self.alpha = alpha
        self.x_mean_ = 0
        self.sum_ = 0
        self.n = 0
        self.sig = []
        self.signa = []
        self.rules_triggered = False

    def update(self, new_signal_value):
        super(PageHinkleyDetector, self).update(new_signal_value)
        self.sig.append(new_signal_value)
        self.signa.append(new_signal_value)
        self.n += 1
        if self.n % 10 == 0:
            self.sig = sp.signal.medfilt(self.sig,5).tolist()
            self.signa = sp.signal.medfilt(self.signa,5).tolist()

        x = np.mean(new_signal_value)
        self.x_mean_ = self.x_mean_ + (x - self.x_mean_) / self.n
        self.x_mean_ = np.mean(self.sig)
        self.sum_ = self.sum_ * self.alpha + x - self.x_mean_ - self.delta

    def check_stopping_rules(self, new_signal_value):
        self.rules_triggered = False
        if self.n % 5 == 0 and np.abs(self.sum_) > self.lambd:
            self.rules_triggered = True
            plt.plot(self.sig)
            self.n = 0
            self.x_mean_ = 0
            self.sum_ = 0
            self.sig = []
