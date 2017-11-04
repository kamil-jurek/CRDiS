import math
import numpy as np
from change_detector import ChangeDetector

class DDMDetector(ChangeDetector):

    def __init__(self, m_p=1, m_n=1, m_s=0):
        super( DDMDetector, self ).__init__()
        self.m_p_ = m_p
        self.m_n = m_n
        self.m_s_ = m_s
        self.m_pmin = 9999
        self.m_psmin = 9999
        self.m_smin_ = 9999
        self.rules_triggered = False

    def update_residuals(self, new_signal_value):
        self._update_base_residuals(new_signal_value)
        if self.rules_triggered:
            self.m_p_ = 1
            self.m_n = 1
            self.m_s_ = 0
            self.m_pmin = 9999
            self.m_psmin = 9999
            self.m_smin_ = 9999

        prediction = new_signal_value % 2
        print(prediction)
        self.m_p_ = self.m_p_ + (prediction - self.m_p_) / self.m_n;
        self.m_s_ = math.sqrt(self.m_p_ * (1 - self.m_p_) / self.m_n);
        self.m_n += 1

        self.estimation = self.m_p_;
        self.delay = 0;

        if self.m_p_ + self.m_s_ <= self.m_psmin:
            self.m_pmin = self.m_p_;
            self.m_smin_ = self.m_s_;
            self.m_psmin = self.m_p_ + self.m_s_;


    def check_stopping_rules(self, new_signal_value):
        x = new_signal_value

        self.rules_triggered = False
        if self.m_p_ + self.m_s_ > self.m_pmin + 2 * self.m_smin_:
            self.rules_triggered = True
