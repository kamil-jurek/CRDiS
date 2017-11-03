import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict

class ChangeDetector(object):
    """
    A change detection algorithm.

    The algorithm calculates residuals and updates them for each new value
    passed. Residuals are checked against stopping rules at each change,
    yielding either True or False, accordingly.
    """

    def __init__(self):
        self.rules_triggered = False
        self.has_started = False
        # Interim and calculated values
        self.signal_size = 0

        # Residuals
        #   All attributes ending in underscore (_) are treated as
        #   residual values (for plotting, printing, etc)
        #   e.g. self.mean_ = np.nan
        pass

    def update_residuals(self, new_signal_value):
        """
        Updates residuals.
        Override this method when writing your own change detector based on
        this class.
        """
        self._update_base_residuals(new_signal_value)
        # Update your residuals here
        pass

    def check_stopping_rules(self, new_signal_value):
        """
        Check Stopping Rules.
        Override this method when writing your own change detector based on
        this class
        """
        # Implemente your stopping rules here
        # Set self.rules_triggered to True when triggered
        pass

    """
    Internal methods
    -------------------
    leave the following methods alone. You should only need to override or edit
    above this line in order to implement your own change detector.
    """

    @property
    def residuals_(self):
        return self._get_residual_dict()

    def _update_base_residuals(self, x):
        """
        Input
         x: scalar, float.
            is the new signal value obtained for this step.
        Base residuals
         k: int
            the total signal size seen so far.
            TEMP: Currently called signal_size for clarity
        """
        # We'll always use these
        self.signal_size += 1

    def _get_residual_dict(self):
        """create a dictionary of residuals to return.
        Inclues all class and instance variables ending in '_'
        """
        residuals_dict = {}
        for k, v in self.__dict__.items():
            if k.endswith('_'):
                residuals_dict[k] = v

        return residuals_dict

    def _step(self, new_signal_value):
        """Internal method to "step", digest one new signal point."""
        self.has_started = True

        # Update residuals
        self.update_residuals(new_signal_value)

        # Compare residuals to stopping_rules
        self.check_stopping_rules(new_signal_value)

        yield self._get_residual_dict()

    def step(self, new_signal_value):
        return self._step(new_signal_value)

    def __repr__(self):
        return "Change Detector(triggered={}, residuals={})".format(
            self.rules_triggered,
            self.residuals_
            )


class OnlineSimulator(object):
    def __init__(self, change_detector, signal):
        self.signal = signal
        self.change_detector = change_detector
        self.signal_size = len(signal)
        self.stops = []

    def run(self, plot=True, **kwargs):
        signal = self.signal
        detector = self.change_detector

        if detector.has_started is True:
            raise Exception("Detector must be re-initialized.")

        residuals_history = defaultdict(list)

        for i, value in enumerate(signal):
            res = next(detector.step(value))

            for k, v in res.items():
                residuals_history[k].append(v)

            if detector.rules_triggered is True:
                self.stops.append(i)

        def dict_to_arrays(ddict):
            new_dict = {}
            for k, v in ddict.items():
                new_dict[k] = np.array(v)
            return new_dict

        residuals_history = dict_to_arrays(residuals_history)
        self.residuals_history = residuals_history

        if plot is True:
            self.display_results(**kwargs)

        return detector.rules_triggered

    def display_results(self, signal_name='Signal', **kwargs):
        signal = self.signal
        detector = self.change_detector
        residuals_history = self.residuals_history

        # if detector.rules_triggered is True:
        #     some_res = next(iter(residuals_history.items()))
        #     #print(some_res)
        #     #print("residuals: ", residuals_history)
        #     #print("stops: ", self.stops)
        #     stop_point = len(some_res) - 1
        # else:
        #     stop_point = None
        #     print("Stopping rule not triggered.")

        # Generate axes to plot signal and residuals"""
        plotcount = 1 + len(residuals_history)
        fig, axes = plt.subplots(nrows=plotcount, ncols=1, sharex=True,
                                 figsize=(12, plotcount*3))

        # Plot the signal
        if plotcount > 1:
            ax = axes[0]
        elif plotcount == 1:
            ax = axes

        avgFilter = np.asarray(detector.avgFilter)
        stdFilter = np.asarray(detector.stdFilter)
        #ax.plot(self.stops, 'o')
        ax.plot(signal, 'b.')
        ax.plot(signal, 'b-', alpha=0.15)
        ax.plot(avgFilter, color="red", lw=2)
        ax.plot(avgFilter + detector.threshold * stdFilter,  color="green", lw=2)
        ax.plot(avgFilter - detector.threshold * stdFilter, color="green", lw=2)
        ax.set_title(signal_name)

        # Scale signal
        ax.set_ylim(
            np.nanmin(signal)*.5,
            np.nanmax(signal)*1.5)
        ax.set_xlim(0, len(signal))

        # Plot a horizontal line where the stop_point is indicated
        if detector.rules_triggered is True:
            for s in self.stops:
                ax.vlines(x=s, ymin=0, ymax=ax.get_ylim()[1],
                      colors='r', linestyles='dotted')

        # Plot each residual
        for ii, (res_name, res_values) in enumerate(
                residuals_history.items()):
            ax = axes[ii+1]
            ax.plot(res_values, 'g.', alpha=0.7)
            ax.set_title("Residual #{}: {}".format(ii+1, res_name))
            ax.set_ylim(
                np.nanmin(res_values)*0.5,
                np.nanmax(res_values)*1.5)
            for s in self.stops:
                ax.vlines(x=s, ymin=0, ymax=ax.get_ylim()[1],
                      colors='r', linestyles='dotted')

        plt.show()

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

from collections import deque

class ZScoreDetector(ChangeDetector):
    def __init__(self, window_size = 100, threshold=0.05):
        super( ZScoreDetector, self ).__init__()
        self.threshold = threshold
        self.window_size = window_size
        self.k = 0  # total signal_size
        self.g_mean = 0.0  # global mean
        self.s = 0.0  # for Welford's method. variance = s / (k + 1)
        self.window = deque(maxlen = window_size)
        self.z_score_ = np.nan
        self.z_array = []
        self.mymean = []

    def update_residuals(self, new_signal_value):
        self._update_base_residuals(new_signal_value)
        x = new_signal_value
        self.window.append(x)

        # Calculate global statistics using welford's method
        oldm = self.g_mean
        newm = oldm + (x - oldm) / (self.k + 1)
        s = self.s + (x - newm) * (x - oldm)

        g_mean = newm  # Global mean
        g_std = np.sqrt(s / (self.k+1))  # Global std

        w_mean = np.mean(self.window)  # Window mean
        w_std = np.std(self.window)  # Window std

        std_diff = (g_std - w_std) / g_std
        SE = g_std / np.sqrt(self.window_size)

        mean_diff = (g_mean - w_mean) / g_mean
        self.mymean.append(newm)
        self.z_score_ = (w_mean - g_mean) / SE
        self.z_array.append(self.z_score_)
        self.g_mean = g_mean
        self.s = s
        self.k += 1

    def check_stopping_rules(self, new_signal_value):
        self.rules_triggered = False
        if np.absolute(self.z_score_) > self.threshold:
            #print("value:  ", new_signal_value)
            #print("zscore: ", np.absolute(self.z_score_))
            self.rules_triggered = True

class MyZScoreDetector(ChangeDetector):
    def __init__(self, y, lag=30, threshold=1.0, influence=0.0):
        super( MyZScoreDetector, self ).__init__()
        self.y = y
        self.lag = lag
        self.threshold = float(threshold)
        self.influence = influence
        self.itt = -1
        self.signals = np.zeros(len(y))
        self.filteredY = np.array(y)
        self.avgFilter = [0]*len(y)
        self.stdFilter = [0]*len(y)
        for i in np.arange(0, lag):
            self.avgFilter[i] = np.mean(y[0:i])
            self.stdFilter[i] = np.std(y[0:i])
        self.avgFilter[lag - 1] = np.mean(y[0:lag])
        self.stdFilter[lag - 1] = np.std(y[0:lag])
        self.rules_triggered = False

    def update_residuals(self, new_signal_value):
        self._update_base_residuals(new_signal_value)
        self.itt += 1

    def check_stopping_rules(self, new_signal_value):
        if self.itt > self.lag:
            print("1: ",np.abs(self.y[self.itt] - self.avgFilter[self.itt-1]))
            print("2: ",self.threshold * self.stdFilter[self.itt-1])
            if np.abs(self.y[self.itt] - self.avgFilter[self.itt-1]) > self.threshold * self.stdFilter[self.itt-1]:
                self.rules_triggered = True

                self.filteredY[self.itt] = self.influence * self.y[self.itt] + (1 - self.influence) * self.filteredY[self.itt-1]
                self.avgFilter[self.itt] = np.mean(self.filteredY[(self.itt-self.lag):self.itt])
                self.stdFilter[self.itt] = np.std(self.filteredY[(self.itt-self.lag):self.itt])
            else:
                self.rules_triggered = False
                self.filteredY[self.itt] = self.y[self.itt]
                self.avgFilter[self.itt] = np.mean(self.filteredY[(self.itt-self.lag):self.itt])
                self.stdFilter[self.itt] = np.std(self.filteredY[(self.itt-self.lag):self.itt])
