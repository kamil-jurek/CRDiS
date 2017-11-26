import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict

class ChangeDetector(object):
    def __init__(self):
        self.rules_triggered = False
        self.signal_size = 0
        self.signal = []

    def update(self, new_signal_value):
        self.signal.append(new_signal_value)
        self.signal_size += 1

    def check_stopping_rules(self, new_signal_value):
        pass

    def get_parameters(self):
        parameters_dict = {}
        for k, v in self.__dict__.items():
            if k.endswith('_'):
                parameters_dict[k] = v

        return parameters_dict

    def step(self, new_signal_value):
        self.update(new_signal_value)
        self.check_stopping_rules(new_signal_value)

        return self.get_parameters()

    def __repr__(self):
        return "Change Detector(triggered={}, residuals={})".format(
            self.rules_triggered,
            self.parameters_
            )

class OnlineSimulator(object):
    def __init__(self, change_detector, signal):
        self.signal = signal
        self.change_detector = change_detector
        self.signal_size = len(signal)
        self.stops = []

    def get_detected_changes(self):
        return self.stops

    def run(self, plot=True, **kwargs):
        signal = self.signal
        detector = self.change_detector

        parameters_history = defaultdict(list)

        for i, value in enumerate(signal):
            res = detector.step(value)

            for k, v in res.items():
                parameters_history[k].append(v)

            if detector.rules_triggered is True:
                self.stops.append(i)

        def dict_to_arrays(ddict):
            new_dict = {}
            for k, v in ddict.items():
                new_dict[k] = np.array(v)
            return new_dict

        parameters_history = dict_to_arrays(parameters_history)
        self.parameters_history = parameters_history

        if plot is True:
            self.display_results(**kwargs)

        return detector.rules_triggered

    def display_results(self, signal_name='Signal', **kwargs):
        signal = self.signal
        detector = self.change_detector
        parameters_history = self.parameters_history

        plotcount = 1 + len(parameters_history)
        fig, axes = plt.subplots(nrows=plotcount, ncols=1, sharex=True,
                                 figsize=(12, plotcount*3))

        # Plot the signal
        if plotcount > 1:
            ax = axes[0]
        elif plotcount == 1:
            ax = axes

        ax.plot(signal, 'b.')
        ax.plot(signal, 'b-', alpha=0.15)

        ax.set_title(signal_name)

        ax.set_ylim(
            np.nanmin(signal)*.5,
            np.nanmax(signal)*1.5)
        ax.set_xlim(0, len(signal))
        xl = ax.get_xticks()
        ticks = xl - int(2/3 * len(signal))

        ax.set_xticklabels(ticks)

        # Plot a horizontal line where the stop_point is indicated
        for s in self.stops:
            ax.vlines(x=s, ymin=0, ymax=ax.get_ylim()[1],
                  colors='r', linestyles='dotted')

        # Plot each
        for ii, (res_name, res_values) in enumerate(parameters_history.items()):
            ax = axes[ii+1]
            ax.plot(res_values, 'g.', alpha=0.7)
            ax.set_title("Parameter #{}: {}".format(ii+1, res_name))

            # ax.set_ylim(
            #     np.nanmin(res_values)*0.5,
            #     np.nanmax(res_values)*1.5)
            for s in self.stops:
                ax.vlines(x=s, ymin=0, ymax=ax.get_ylim()[1],
                      colors='r', linestyles='dotted')

        plt.show()
