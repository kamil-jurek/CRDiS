import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict

class ChangeDetector(object):
    def __init__(self):
        self.rules_triggered = False
        self.has_started = False
        self.signal_size = 0

        # Residuals
        #   All attributes ending in underscore (_) are treated as
        #   residual values (for plotting, printing, etc)
        #   e.g. self.mean_ = np.nan
        pass

    def update_residuals(self, new_signal_value):
        self._update_base_residuals(new_signal_value)
        pass

    def check_stopping_rules(self, new_signal_value):
        pass

    @property
    def residuals_(self):
        return self._get_residual_dict()

    def _update_base_residuals(self, x):
        self.signal_size += 1

    def _get_residual_dict(self):
        residuals_dict = {}
        for k, v in self.__dict__.items():
            if k.endswith('_'):
                residuals_dict[k] = v

        return residuals_dict

    def _step(self, new_signal_value):
        self.has_started = True
        self.update_residuals(new_signal_value)
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

        #avgFilter = np.asarray(detector.avgFilter)
        #stdFilter = np.asarray(detector.stdFilter)
        #ax.plot(self.stops, 'o')
        ax.plot(signal, 'b.')
        ax.plot(signal, 'b-', alpha=0.15)
        #ax.plot(avgFilter, color="red", lw=2)
        #ax.plot(detector.g_mean_list, color="red", lw=2 )
        #ax.plot(detector.windows_mean_list, color="green", lw=2 )
        #ax.plot(avgFilter + detector.threshold * stdFilter,  color="green", lw=2)
        #ax.plot(avgFilter - detector.threshold * stdFilter, color="green", lw=2)
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
            #print("res:",res_name, res_values)
            ax = axes[ii+1]
            #[len(res_values)-1]
            ax.plot(res_values, 'g.', alpha=0.7)
            ax.set_title("Residual #{}: {}".format(ii+1, res_name))
            ax.set_ylim(
                np.nanmin(res_values)*0.5,
                np.nanmax(res_values)*1.5)
            for s in self.stops:
                print(s)
                ax.vlines(x=s, ymin=0, ymax=ax.get_ylim()[1],
                      colors='r', linestyles='dotted')

        plt.show()
