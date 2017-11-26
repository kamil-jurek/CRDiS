import numpy as np
import math
from detector import ChangeDetector

class EntropyDetector(ChangeDetector):
    def __init__(self, threshold=4):
        super( EntropyDetector, self ).__init__()
        self.entropy_ = 0
        self.oldEntropy = 0
        self.threshold = threshold
        self.freqList = {}
        self.sum_ = 0

    def update(self, new_signal_value):
        super(EntropyDetector, self).update(new_signal_value)
        x = new_signal_value

        if x in self.freqList:
            self.freqList[x] += 1
        else:
            self.freqList[x] = 1

        self.oldEntropy = self.entropy_
        for f in self.freqList:
            p_x = float(self.signal.count(x))/self.signal_size
            print(p_x)
            if p_x > 0:
                self.entropy_ += - p_x * math.log(p_x, 2)
        #print(self.entropy_)
        self.sum_ = self.sum_ + self.entropy_ - self.oldEntropy;

    def check_stopping_rules(self, new_signal_value):
        self.rules_triggered = False
        #print("entropy:", self.entropy_)

        #if self.entropy_ > self.threshold:
        if np.abs(self.sum_) > self.threshold:
            self.rules_triggered = True
            self.entropy_ = 0
            self.signal = []
            self.signal_size = 0
            self.freqList = {}
            self.sum_ = 0

    def entrop(self, data):
        entropy = 0
        for x in range(len(data)):
            p_x = float(data.count(x))/len(data)
            if p_x > 0:
                entropy += - p_x*math.log(p_x, 2)
        return entropy
