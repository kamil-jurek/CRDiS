import numpy as np
from detector import ChangeDetector

class GeometricMovingAverageDetector(ChangeDetector):

    def __init__(self, threshold=0.05):
        super(GeometricMovingAverageDetector, self).__init__()
        self.threshold = threshold
        self.total_val = 0
        self.diff_ = np.nan
        self.n = 0
        self.previous_value = -1
        self.current_value = -1
        self.subseq = []
        self.percent = 0

    def update(self, new_value):
        super(GeometricMovingAverageDetector, self).update(new_value)
        self.subseq.append(new_value)
        self.total_val += new_value
        self.n += 1
        self.mean_ = self.total_val / self.n
        self.diff_ = np.absolute(self.mean_ - new_value)
        #print(self.diff_)


    def reset(self):
        self.total_val = 0
        self.n = 0
        self.mean_ = 0
        self.diff_ = 0
        self.subseq = []

    def check_change(self, new_value):
        threshold_level = self.mean_ * self.threshold
        self.is_change_detected = False
        #print("diff:", self.diff_)
        #print("threshold_level:", threshold_level)
        if self.diff_ > threshold_level:
            #print(self.diff_)
            self.is_change_detected = True
            self.previous_value = max(set(self.subseq), key=self.subseq.count)
            self.current_value = max(set(self.subseq[-1:]), key=self.subseq[-1:].count)
            self.percent = (self.subseq.count(self.previous_value) / len(self.subseq)) * 100
            self.reset()
