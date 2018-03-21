import math
import sys
import numpy as np
from detector import ChangeDetector

class DDMDetector(ChangeDetector):

    def __init__(self, lambd=5):
        super( DDMDetector, self ).__init__()
        self.sig_size = 1

        self.p_ = 1
        self.s_ = 0
        self.p_min_ = sys.maxsize
        self.s_min_ = sys.maxsize

        self.is_change_detected = False
        self.warning_zone = []

    def update(self, new_value):
        super(DDMDetector, self).update(new_value)
        self.sig_size += 1

        self.p_ -= self.p_ / self.sig_size
        self.s_ = math.sqrt(self.p_ * (1 - self.p_) / self.sig_size)

        if self.p_ + self.s_ < self.p_min_ + self.s_min_:
            self.p_min_ = self.p_
            self.s_min_ = self.s_

        # x = new_signal_value
        # self.mean_ = self.mean_ + (x - self.mean_) / self.sig_size;
        # self.sum_ = self.sum_ + x - self.mean_ - self.delta;
        #
        # if np.abs(np.sum(self.sum_)) > self.lambd:
        #     prediction = 1
        # else:
        #     prediction = 0
        #
        # self.prob_of_false = self.prob_of_false + (prediction - self.prob_of_false) / self.sig_size;
        # self.std_ = math.sqrt(self.prob_of_false * (1 - self.prob_of_false) / self.sig_size);
        # self.sig_size += 1
        #
        # self.estimation = self.prob_of_false;
        # self.delay = 0;
        #
        # if self.prob_of_false + self.std_ <= self.ps_min:
        #     self.p_min = self.prob_of_false;
        #     self.s_min_ = self.std_;
        #     self.ps_min = self.prob_of_false + self.std_;


    def check_change(self, new_value):
        self.is_change_detected = False

        current_level = self.p_ + self.s_
        warning_level = self.p_min_ + 2 * self.s_min_
        drift_level = self.p_min_ + 3 * self.s_min_

        if current_level >= warning_level:
            print("Warning", new_value)
            self.warning_zone.append(self.sig_size-1)
            if len(self.warning_zone) > 0:
                print(self.warning_zone)

        if current_level >= drift_level:
            self.is_change_detected = True
        # x = new_signal_value
        # self.is_change_detected = False
        # #print("p+s=",self.prob_of_false + self.std_)
        # if self.prob_of_false + self.std_ > self.p_min + 2 * self.s_min_:
        #     self.is_change_detected = True
        #     if len(self.warning_zone) > 0:
        #         print(self.warning_zone)
        #     self.reset()
        # if self.prob_of_false + self.std_ > self.p_min + 2.5 * self.s_min_:
        #     print("Warning", new_signal_value)
        #     self.warning_zone.append(self.sig_size-1)

    def reset(self):
        self.prob_of_false = 1
        self.sig_size = 1
        self.std_ = 0
        self.p_min = math.inf
        self.ps_min = math.inf
        self.s_min_ = math.inf
