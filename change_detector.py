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

        # Check
        if detector.has_started is True:
            raise Exception("Detector must be re-initialized.")

        # Run simulation
        residuals_history = defaultdict(list)
        for value in signal:
            # Step to get residuals and check stopping rules
            res = next(detector.step(value))

            # Store residual_history (for plotting only)
            for k, v in res.items():
                residuals_history[k].append(v)

            if detector.rules_triggered is True:
                self.stops.append(value)

        def dict_to_arrays(ddict):
            """Convenience func to bundle residuals into a dict"""
            new_dict = {}
            for k, v in ddict.items():
                new_dict[k] = np.array(v)
            return new_dict

        residuals_history = dict_to_arrays(residuals_history)
        self.residuals_history = residuals_history

        # Display results
        if plot is True:
            self.display_results(**kwargs)

        return detector.rules_triggered

    def display_results(self, signal_name='Signal', **kwargs):
        signal = self.signal
        detector = self.change_detector
        residuals_history = self.residuals_history
        """Print out the results of our experiment. """

        print("Residuals: {}".format(
            [res for res in residuals_history.keys()]
            ))

        # Print results
        if detector.rules_triggered is True:
            # Length of any residual array tells us when the rule was triggered
            some_res = next(iter(residuals_history.items()))
            #print(some_res)
            #print("residuals: ", residuals_history)
            print(self.stops)
            stop_point = len(some_res) - 1
            # Quick sanity check
            assert (stop_point > 0) & (stop_point <= len(signal))
            print("Change detected. Stopping Rule triggered at {}.\n".format(
                stop_point))
        else:
            stop_point = None
            print("Stopping rule not triggered.")

        # Generate axes to plot signal and residuals"""
        plotcount = 1 + len(residuals_history)
        fig, axes = plt.subplots(nrows=plotcount, ncols=1, sharex=True,
                                 figsize=(12, plotcount*3))

        # Plot the signal
        if plotcount > 1:
            ax = axes[0]
        elif plotcount == 1:
            ax = axes
        ax.plot(self.stops, 'o')
        ax.plot(signal, 'b.')
        ax.plot(signal, 'b-', alpha=0.15)
        ax.set_title(signal_name)

        # Scale signal
        ax.set_ylim(
            np.nanmin(signal)*.5,
            np.nanmax(signal)*1.5)
        ax.set_xlim(0, len(signal))

        # Plot a horizontal line where the stop_point is indicated
        if detector.rules_triggered is True:
            ax.vlines(x=stop_point, ymin=0, ymax=ax.get_ylim()[1],
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
            if stop_point is not None:
                ax.vlines(x=stop_point, ymin=0, ymax=ax.get_ylim()[1],
                          colors='r', linestyles='dotted')

        plt.show()

class MeanDetector(ChangeDetector):
    """
    Static Mean Detector

    Residuals:
        mean_: the mean of signal values seen so far
        diff_: the difference between new value and mean_

    Stopping Rule:
        Stop if diff_ exceeds some threshold percentage value.
        Default is 5%.
    """

    def __init__(self, threshold=0.05):
        super( MeanDetector, self ).__init__()

        # Save hyper-parameter(s)
        self.threshold = threshold

        # Required Attributes
        self.total_val = 0  # Used for calculating mean

        # new residuals(s)
        self.diff_ = np.nan

    def update_residuals(self, new_signal_value):
        self._update_base_residuals(new_signal_value)

        # Update attributes
        self.total_val += new_signal_value

        #Update residuals
        self.mean_ = self.total_val / self.signal_size
        self.diff_ = np.absolute(self.mean_ - new_signal_value)

    def check_stopping_rules(self, new_signal_value):
        #check if new value is more than % different from mean
        threshold_level = self.mean_ * self.threshold

        if self.diff_ > threshold_level:
            self.rules_triggered = True

from collections import deque

class ZScoreDetector(ChangeDetector):
    def __init__(self, window_size = 100, threshold=0.05):
        super( ZScoreDetector, self ).__init__()

        # hyper-parameters
        self.threshold = threshold
        self.window_size = window_size

        # Interim and calculated values
        self.k = 0  # total signal_size
        self.g_mean = 0.0  # global mean
        self.s = 0.0  # for Welford's method. variance = s / (k + 1)

        # This is the window
        self.window = deque(maxlen = window_size)

        # ... and, finally, our residuals
        self.z_score_ = np.nan
        self.z_array = []

    def update_residuals(self, new_signal_value):
        self._update_base_residuals(new_signal_value)
        x = new_signal_value

        # Add new value to local window (deque will
        #  automatically drop a value to maintain window size)
        self.window.append(x)

        """Calculate Statistics on global and local window """
        # Calculate global statistics using welford's method
        oldm = self.g_mean
        newm = oldm + (x - oldm) / (self.k + 1)
        s = self.s + (x - newm) * (x - oldm)

        g_mean = newm  # Global mean
        g_std = np.sqrt(s / (self.k+1))  # Global std

        # Calculate local statistics on the window
        #  We have all values stored for the window, so
        #  can use built-in numpy stats methods
        w_mean = np.mean(self.window)  # Window mean
        w_std = np.std(self.window)  # Window std

        """Calculate variables required for Zscore"""
        # Calculate SE, see formula above
        std_diff = (g_std - w_std) / g_std
        SE = g_std / np.sqrt(self.window_size)

        # Difference between the means
        mean_diff = (g_mean - w_mean) / g_mean

        # Z-score (residual)
        self.z_score_ = (w_mean - g_mean) / SE
        self.z_array.append(self.z_score_)

        # Store attributes
        self.g_mean = g_mean
        self.s = s

        # Update k (size of global window).
        #   This must be done at the end!
        self.k += 1

    def check_stopping_rules(self, new_signal_value):
        # Check stopping rule!
        if np.abs(self.z_score_) > self.threshold:
            self.rules_triggered = True
