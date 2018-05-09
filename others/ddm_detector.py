import math
import numpy as np
from detector import ChangeDetector

class DDMDetector(ChangeDetector):

    def __init__(self, lambd=5):
        super( DDMDetector, self ).__init__()
        self.prob_of_false = 1
        self.sig_size = 1
        self.std_ = 0
        self.p_min = math.inf
        self.ps_min = math.inf
        self.s_min_ = math.inf
        self.is_change_detected = False
        self.mean_ = 0
        self.sum_ = 0
        self.lambd = lambd
        self.delta = 0.005
        self.warning_zone = []

    def update(self, new_signal_value):
        super(DDMDetector, self).update(new_signal_value)
        if self.is_change_detected:
            self.prob_of_false = 1
            self.sig_size = 1
            self.std_ = 0
            self.p_min = math.inf
            self.ps_min = math.inf
            self.s_min_ = math.inf
            self.mean_ = 0
            self.sum_ = 0

        x = new_signal_value
        self.mean_ = self.mean_ + (x - self.mean_) / self.sig_size;
        self.sum_ = self.sum_ + x - self.mean_ - self.delta;

        if np.abs(np.sum(self.sum_)) > self.lambd:
            prediction = 1
        else:
            prediction = 0

        self.prob_of_false = self.prob_of_false + (prediction - self.prob_of_false) / self.sig_size;
        self.std_ = math.sqrt(self.prob_of_false * (1 - self.prob_of_false) / self.sig_size);
        self.sig_size += 1

        self.estimation = self.prob_of_false;
        self.delay = 0;

        if self.prob_of_false + self.std_ <= self.ps_min:
            self.p_min = self.prob_of_false;
            self.s_min_ = self.std_;
            self.ps_min = self.prob_of_false + self.std_;


    def check_change(self, new_signal_value):
        x = new_signal_value
        self.is_change_detected = False
        #print("p+s=",self.prob_of_false + self.std_)
        if self.prob_of_false + self.std_ > self.p_min + 2 * self.s_min_:
            self.is_change_detected = True
            if len(self.warning_zone) > 0:
                print(self.warning_zone)
        if self.prob_of_false + self.std_ > self.p_min + 2.5 * self.s_min_:
            print("Warning", new_signal_value)
            self.warning_zone.append(self.sig_size-1)
