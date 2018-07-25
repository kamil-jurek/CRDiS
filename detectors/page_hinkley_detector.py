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
        self.percent = 0

    def update(self, new_value):
        super(PageHinkleyDetector, self).update(new_value)
        self.subseq.append(new_value)
        self.n += 1
        self.mean_ = self.mean_ + (new_value - self.mean_) / self.n
        self.sum_ = self.sum_ * self.alpha + new_value - self.mean_ - self.delta

    def reset(self):
        self.n = 0
        self.subseq = []
        self.mean_ = 0
        self.sum_ = 0

    def check_change(self, new_value):
        self.is_change_detected = False

        if np.abs(self.sum_) > self.lambd:
            self.is_change_detected = True
            self.previous_value = max(set(self.subseq), key=self.subseq.count)
            self.current_value = max(set(self.subseq[-1:]), key=self.subseq[-1:].count)
            self.percent = (self.subseq.count(self.previous_value) / len(self.subseq)) * 100
            self.reset()