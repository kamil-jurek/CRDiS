import numpy as np
import math
from detector import ChangeDetector

class EntropyDetector(ChangeDetector):
    def __init__(self, threshold=4):
        super( EntropyDetector, self ).__init__()
        self.entropy_ = 0
        self.threshold = threshold

    def update(self, new_signal_value):
        super(EntropyDetector, self).update(new_signal_value)
        x = new_signal_value

        self.p_x_ = float(self.signal.count(x)) / self.signal_size
        if self.p_x_ > 0:
           self.entropy_ += - self.p_x_ * math.log(self.p_x_, 2)

    def check_stopping_rules(self, new_signal_value):
        self.rules_triggered = False
        print("entropy:", self.entropy_)

        if self.entropy_ > self.threshold:
            self.rules_triggered = True
            self.entropy_ = 0
            self.signal = []
            self.signal_size = 0
