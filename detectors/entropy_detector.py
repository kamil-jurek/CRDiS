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

        for block in (self.signal[x:20+x] for x in range(self.signal_size-20)):
            self.entropy_ = self.entrop(block)

    def check_stopping_rules(self, new_signal_value):
        self.rules_triggered = False
        print("entropy:", self.entropy_)

        if self.entropy_ > self.threshold:
            self.rules_triggered = True
            #self.entropy_ = 0
            #self.signal = []
            #self.signal_size = 0
    def entrop(self, data):
        if not data:
            return 0

        entropy = 0
        for x in range(len(data)):
            p_x = float(data.count(x))/len(data)
            if p_x > 0:
                entropy += - p_x*math.log(p_x, 2)
        return entropy
