import numpy as np
import scipy as sp
from scipy import signal
from statistics import mode
from detector import ChangeDetector

class PageHinkleyDetector(ChangeDetector):

    def __init__(self, delta=0.005, lambd=50, alpha=1 - 0.0001):
        super( PageHinkleyDetector, self ).__init__()
        self.delta = delta
        self.lambd = lambd
        self.alpha = alpha
        self.mean_ = 0
        self.sum_ = 0
        self.n = 0
        self.subseq = []
        self.is_change_detected = False

    def update(self, new_value):
        super(PageHinkleyDetector, self).update(new_value)
        self.subseq.append(new_value)
        self.n += 1
        self.mean_ = self.mean_ + (new_value - self.mean_) / self.n
        self.sum_ = self.sum_ * self.alpha + new_value - self.mean_ - self.delta

    def check_change(self, new_value):
        self.is_change_detected = False
        if np.abs(self.sum_) > self.lambd:
            self.previous_value = mode(self.subseq)
            self.current_value = mode(self.subseq[-9:])
            self.is_change_detected = True
            self.reset()

    def reset(self):
        self.n = 0
        self.subseq = []
        self.mean_ = 0
        self.sum_ = 0