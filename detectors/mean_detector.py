import numpy as np
from change_detector import ChangeDetector

class MeanDetector(ChangeDetector):

    def __init__(self, threshold=0.05):
        super( MeanDetector, self ).__init__()
        self.threshold = threshold
        self.total_val = 0
        self.diff_ = np.nan

    def update_residuals(self, new_signal_value):
        self._update_base_residuals(new_signal_value)
        self.total_val += new_signal_value
        self.mean_ = self.total_val / self.signal_size
        self.diff_ = np.absolute(self.mean_ - new_signal_value)

    def check_stopping_rules(self, new_signal_value):
        threshold_level = self.mean_ * self.threshold
        self.rules_triggered = False

        if self.diff_ > threshold_level:
            self.rules_triggered = True
            self.total_val = 0
            self.signal_size = 0
