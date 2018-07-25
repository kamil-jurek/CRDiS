# The MIT License
# Copyright (c) 2018 Kamil Jurek
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import math
import numpy as np
from detector import ChangeDetector

class DDMDetector(ChangeDetector):
    def __init__(self, lambd=5, delta=0.001):
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
        self.percent = 0
        self.subseq = []

    def update(self, new_value):
        super(DDMDetector, self).update(new_value)
 
        self.subseq.append(new_value)
        x = new_value
        self.mean_ = self.mean_ + (x - self.mean_) / self.sig_size
        self.sum_ = self.sum_ + x - self.mean_ - self.delta

        if np.abs(np.sum(self.sum_)) > self.lambd:
            prediction = 1
        else:
            prediction = 0

        self.prob_of_false = self.prob_of_false + (prediction - self.prob_of_false) / self.sig_size
        self.std_ = math.sqrt(self.prob_of_false * (1 - self.prob_of_false) / self.sig_size)
        self.sig_size += 1

        self.estimation = self.prob_of_false
        self.delay = 0

        if self.prob_of_false + self.std_ <= self.ps_min:
            self.p_min = self.prob_of_false
            self.s_min_ = self.std_
            self.ps_min = self.prob_of_false + self.std_

    def reset(self):
        self.prob_of_false = 1
        self.sig_size = 1
        self.std_ = 0
        self.p_min = math.inf
        self.ps_min = math.inf
        self.s_min_ = math.inf
        self.mean_ = 0
        self.sum_ = 0
        self.subseq = []

    def check_change(self, new_value):
        self.is_change_detected = False

        if self.prob_of_false + self.std_ > self.p_min + 2 * self.s_min_:
            self.is_change_detected = True
            self.previous_value = max(set(self.subseq), key=self.subseq.count)
            self.current_value = max(set(self.subseq[-1:]), key=self.subseq[-1:].count)
            self.percent = (self.subseq.count(self.previous_value) / len(self.subseq)) * 100
            
            if len(self.warning_zone) > 0:
                print(self.warning_zone)

            self.reset()

        if self.prob_of_false + self.std_ > self.p_min + 2.5 * self.s_min_:
            print("Warning", new_value)
            self.warning_zone.append(self.sig_size-1)
