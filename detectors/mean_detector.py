import numpy as np
from detector import ChangeDetector

class MeanDetector(ChangeDetector):

    def __init__(self, threshold=0.05):
        super( MeanDetector, self ).__init__()
        self.threshold = threshold
        self.total_val = 0
        self.diff_ = np.nan
        self.n = 0
        self.previous_value = -1
        self.current_value = -1
        self.subseq = []

    def update(self, new_value):
        super(MeanDetector, self).update(new_value)
        self.subseq.append(new_value)
        self.total_val += new_value
        self.n += 1
        self.mean_ = self.total_val / self.n
        self.diff_ = np.absolute(self.mean_ - new_value)

    def reset(self):
        self.total_val = 0
        self.n = 0
        self.mean_ = 0
        self.diff_ = 0
        self.subseq = []

    def check_stopping_rules(self, new_value):
        threshold_level = self.mean_ * self.threshold
        self.rules_triggered = False

        if self.diff_ > threshold_level:
            self.rules_triggered = True
            self.previous_value = max(set(self.subseq), key=self.subseq.count)
            self.current_value = max(set(self.subseq[-1:]), key=self.subseq[-1:].count)
            self.reset()
