import numpy as np
from detector import ChangeDetector
from collections import deque

class RILL(ChangeDetector):

    def __init__(self):
        super( RILL, self ).__init__()
        self.window_size = 10
        self.sw = deque(maxlen = self.window_size)
        self.rules = []

    def update(self, new_signal_value):
        super(RILL, self).update(new_signal_value)

        x = new_signal_value
        self.sw.append(x)
        sw = list(self.sw)
        for i in range(1, len(sw)):
            rhs = sw[:i]
            lhs = sw[i:]
            rule = (rhs, lhs+[x])

            positive_coverage = self.is_positive_coverage(rule)

            if positive_coverage == False:
                generalization = self.generalize(rule)

            if positive_coverage == False and generalization == False:
                self.rules.append(rule)
                print(rule)


    def check_stopping_rules(self, new_signal_value):
        #print()
        #print("check_stopping_rules")
        return

    def is_positive_coverage(self, rule):
        if rule in self.rules:
            return True

        return False

    def generalize(self, e):

        return False
