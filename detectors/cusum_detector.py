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
        self.p_x_ = 0

    def update(self, new_signal_value):
        super(CusumDetector, self).update(new_signal_value)
        x = new_signal_value
        self.n += 1
        self.mean_ = self.mean_ + (x - self.mean_) / self.n;
        self.sum_ = self.sum_ + x - self.mean_ - self.delta;

        #self.p_x_ = float(data.count(chr(x)))/len(data)
        #if self.p_x > 0:
        #    self.entropy += - self.p_x_*math.log(self.p_x_, 2)


    def check_stopping_rules(self, new_signal_value):
        self.rules_triggered = False
        print("sum:", np.sum(self.sum_))
        if np.abs(np.sum(self.sum_)) > self.lambd:
            self.rules_triggered = True
            self.n = 0
            self.sum_ = 0
            self.mean_ = 0
