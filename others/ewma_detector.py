import numpy as np
import math
from detector import ChangeDetector

class EWMADetector(ChangeDetector):

    def __init__(self, lambd=0.2):
        super( EWMADetector, self ).__init__()
        self.m_n = 1.0
        self.m_s_um = 0.0
        self.m_p_ = 0.0
        self.m_s_ = 0.0
        self.z_t_ = 0.0
        self.lambda_ = lambd

    def update(self, new_value):
        super(EWMADetector, self).update(new_value)
        self.m_s_um += new_value
        self.m_p_ = self.m_s_um / self.m_n
        self.m_s_ = math.sqrt(self.m_p_ * (1.0 - self.m_p_) * self.lambda_ * (1.0 - math.pow(1.0 - self.lambda_, 2.0 * self.m_n)) / (2.0 - self.lambda_))
        self.m_n += 1

        self.z_t_ += self.lambda_ * (new_value - self.z_t_)
        self.L_t_ = 3.97 - 6.56 * self.m_p_ + 48.73 * math.pow(self.m_p_, 3) - 330.13 * math.pow(self.m_p_,5) + 848.18 * math.pow(self.m_p_, 7)

    def check_change(self, new_value):
        self.is_change_detected = False
        if self.z_t_ > self.m_p_ + self.L_t_ * self.m_s_:
            self.is_change_detected = True
            self.reset()

    def reset(self):
        self.m_n = 1.0
        self.m_s_um = 0.0
        self.m_p_ = 0.0
        self.m_s_ = 0.0
        self.z_t_ = 0.0