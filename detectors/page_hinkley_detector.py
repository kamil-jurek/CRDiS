import numpy as np
from detector import ChangeDetector

class PageHinkleyDetector(ChangeDetector):

    def __init__(self, delta=0.005, lambd=50, alpha=1 - 0.0001):
        super( PageHinkleyDetector, self ).__init__()
        self.delta = delta
        self.lambd = lambd
        self.alpha = alpha
        self.x_mean_ = 0
        self.sum_ = 0
        self.sum_min = 0
        self.num = 0
        self.rules_triggered = False

    def update(self, new_signal_value):
        super(PageHinkleyDetector, self).update(new_signal_value)
        self.num += 1
        x = new_signal_value
        #self.x_mean_ = (x + self.x_mean_ * (self.num - 1)) / self.num
        self.x_mean_ = self.x_mean_ + (x - self.x_mean_) / self.num
        self.sum_ = self.sum_ * self.alpha + x - self.x_mean_ - self.delta

    def check_stopping_rules(self, new_signal_value):
        self.rules_triggered = False
        if self.sum_ > self.lambd or self.sum_ < -self.lambd:
            self.rules_triggered = True
            self.num = 0
            self.x_mean_ = 0
            self.sum_ = 0
