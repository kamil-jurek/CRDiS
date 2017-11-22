import numpy as np
from detector import ChangeDetector

class StackZScoreDetector(ChangeDetector):
    def __init__(self, y, lag=30, threshold=1.0, influence=0.0):
        super( StackZScoreDetector, self ).__init__()
        self.y = np.asarray(y)
        self.lag = lag
        self.threshold = float(threshold)
        self.influence = influence
        self.itt = -1
        self.signals_ = np.zeros(len(y))
        self.filteredY_ = y
        self.avgFilter_ = [0]*len(y)
        self.stdFilter_ = [0]*len(y)
        # for i in np.arange(0, lag):
        #     self.avgFilter_[i] = np.mean(y[0:i])
        #     self.stdFilter_[i] = np.std(y[0:i])
        self.avgFilter_[lag - 1] = np.mean(y[0:lag])
        self.stdFilter_[lag - 1] = np.std(y[0:lag])
        self.rules_triggered = False
        self.is_after_lag = False

    def update_residuals(self, new_signal_value):
        self._update_base_residuals(new_signal_value)
        self.itt += 1

        if self.itt > self.lag:
            self.is_after_lag = True;

    def check_stopping_rules(self, new_signal_value):
        if self.is_after_lag:
            #print("1: ",np.abs(self.y[self.itt] - self.avgFilter_[self.itt-1]))
            #print("2: ",self.threshold * self.stdFilter_[self.itt-1])
            i = int(self.itt)
            filteredY = self.filteredY_
            avgFilter = self.avgFilter_
            stdFilter = self.stdFilter_
            threshold = self.threshold
            influence = self.influence
            lag = int(self.lag)
            y = self.y
            print(i)
            if np.abs(y[i] - avgFilter[i-1]) > threshold * stdFilter[i-1]:
                self.rules_triggered = True

                if y[i] > avgFilter[i-1]:
                    self.signals_[i] = 1
                else:
                    self.signals_[i] = -1

                self.filteredY_[i] = influence * y[i] + (1 - influence) * filteredY[i-1]
                self.avgFilter_[i] = np.mean(filteredY[(i-lag):i])
                self.stdFilter_[i] = np.std(filteredY[(i-lag):i])

            else:
                self.rules_triggered = False

                self.signals_[i] = 0

                self.filteredY_[i] = y[i]
                self.avgFilter_[i] = np.mean(filteredY[(i-lag):i])
                self.stdFilter_[i] = np.std(filteredY[(i-lag):i])
