import numpy as np
from detector import ChangeDetector

class MeanDetector(ChangeDetector):

    def __init__(self, threshold=0.05):
        super( MeanDetector, self ).__init__()
        self.threshold = threshold
        self.total_val = 0
        self.diff_ = np.nan
        self.n = 0

    def update(self, new_value):
        super(MeanDetector, self).update(new_value)
        self.total_val += new_value
        self.n += 1
        self.mean_ = self.total_val / self.n
        self.diff_ = np.absolute(self.mean_ - new_value)

    def check_stopping_rules(self, new_value):
        threshold_level = self.mean_ * self.threshold
        self.rules_triggered = False

        if self.diff_ > threshold_level:
            self.rules_triggered = True
            self.total_val = 0
            self.n = 0
            self.mean_ = 0
            self.diff_ = 0
