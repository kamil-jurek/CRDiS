import numpy as np
from detector import ChangeDetector

class CusumDetector(ChangeDetector):

    def __init__(self, delta=0.005, lambd=50):
        super( CusumDetector, self ).__init__()
        self.delta = delta
        self.lambd = lambd
        self.mean_ = 0
        self.sum_ = 0
        self.n = 0

    def update(self, new_value):
        super(CusumDetector, self).update(new_value)
        x = new_value
        self.n += 1
        self.mean_ = self.mean_ + (x - self.mean_) / self.n;
        self.sum_ = self.sum_ + x - self.mean_ - self.delta;

    def check_stopping_rules(self, new_value):
        self.rules_triggered = False
        if np.abs(np.sum(self.sum_)) > self.lambd:
            self.rules_triggered = True
            self.n = 0
            self.sum_ = 0
            self.mean_ = 0
