import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict

class ChangeDetector(object):
    def __init__(self):
        self.is_change_detected = False
        self.sequence_size = 0
        self.sequence = []

    def update(self, new_value):
        self.sequence.append(new_value)
        self.sequence_size += 1

    def check_change(self, new_value):
        pass

    def get_parameters(self):
        parameters_dict = {}
        for k, v in self.__dict__.items():
            if k.endswith('_'):
                parameters_dict[k] = v

        return parameters_dict

    def step(self, new_value):
        self.update(new_value)
        self.check_change(new_value)

        return self.get_parameters()

class OnlineSimulator(object):
    def __init__(self, change_detector, sequence):
        self.sequence = sequence
        self.change_detector = change_detector
        self.sequence_size = len(sequence)
        self.detected_change_points = []

    def get_detected_changes(self):
        return self.detected_change_points

    def run(self, plot=True, **kwargs):
        sequence = self.sequence
        detector = self.change_detector

        parameters_history = defaultdict(list)

        for i, value in enumerate(sequence):
            res = detector.step(value)

            for k, v in res.items():
                parameters_history[k].append(v)

            if detector.is_change_detected is True:
                self.detected_change_points.append(i)

        def dict_to_arrays(ddict):
            new_dict = {}
            for k, v in ddict.items():
                new_dict[k] = np.array(v)
            return new_dict

        parameters_history = dict_to_arrays(parameters_history)
        self.parameters_history = parameters_history

        if plot is True:
            self.display_results(**kwargs)

        return detector.is_change_detected

    def display_results(self, sequence_name='Sequence', **kwargs):
        sequence = self.sequence
        detector = self.change_detector
        parameters_history = self.parameters_history

        plotcount = 1 + len(parameters_history)
        fig, axes = plt.subplots(nrows=plotcount, ncols=1, sharex=True,
                                 figsize=(12, plotcount*3))

        # Plot the sequence
        if plotcount > 1:
            ax = axes[0]
        elif plotcount == 1:
            ax = axes

        ax.plot(sequence, 'b.')
        ax.plot(sequence, 'b-', alpha=0.25)

        ax.set_title(sequence_name)

        ax.set_ylim(
            np.nanmin(sequence)*.5,
            np.nanmax(sequence)*1.5)
        ax.set_xlim(0, len(sequence))
        xl = ax.get_xticks()
        ticks = xl - int(2/3 * len(sequence))

        ax.set_xticklabels(ticks)

        # Plot a horizontal line where the change_point is detected
        for s in self.detected_change_points:
            ax.vlines(x=s, ymin=0, ymax=ax.get_ylim()[1],
                  colors='r', linestyles='dotted')

        # Plot each parameter
        for ii, (res_name, res_values) in enumerate(parameters_history.items()):
            ax = axes[ii+1]
            ax.plot(res_values, 'g.', alpha=0.7)
            ax.set_title("Parameter #{}: {}".format(ii+1, res_name))

            # ax.set_ylim(
            #     np.nanmin(res_values)*0.5,
            #     np.nanmax(res_values)*1.5)
            for p in self.detected_change_points:
                ax.vlines(x=p, ymin=0, ymax=ax.get_ylim()[1],
                      colors='r', linestyles='dotted')

        plt.show()
