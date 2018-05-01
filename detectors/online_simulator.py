import numpy as np
import matplotlib.pyplot as plt

from detectors import detector
from change_point import ChangePoint
from lhs_element import LHS_element
from rule import Rule
from collections import defaultdict

class OnlineSimulator(object):
    def __init__(self, rules_detector, change_detectors, sequences, seqs_names):
        self.sequences = sequences
        self.sequences_names = seqs_names
        self.change_detectors = change_detectors
        self.sequence_size = len(sequences[0])
        self.detected_change_points = [[] for i in range(len(self.sequences))]
        self.rules_sets = [set() for i in range(len(self.sequences))]
        self.parameters_history = [defaultdict(list) for i in range(len(self.sequences))]
        self.rules_detector = rules_detector
        self.combined_rules = []

        if rules_detector != None:
            self.rules_detector.set_online_simulator(self)

    def get_detected_changes(self):
        return self.detected_change_points

    def get_rules_sets(self):
        result = []
        for i, rs in enumerate(self.rules_sets):
            if i != self.rules_detector.target_seq_index:
                result.append(rs)
        return result

    def get_combined_rules(self):
        return self.combined_rules

    def run(self, plot=True, detect_rules=True, **kwargs):
        parameters_history = [defaultdict(list) for i in range(len(self.sequences))]

        for i in range(0, self.sequence_size):
            for j, seq in enumerate(self.sequences):
                detector = self.change_detectors[j]

                value = seq[i]
                res = detector.step(value)

                for k, v in res.items():
                    #print(k, v)
                    parameters_history[j][k].append(v)

                if detector.is_change_detected is True:
                    prev_at = self.detected_change_points[j][-1].at_ if len(self.detected_change_points[j]) > 0 else 0
                    prev_value_len = i - prev_at

                    change_point = ChangePoint(detector.previous_value, detector.current_value, i, prev_value_len, self.sequences_names[j])
                    self.detected_change_points[j].append(change_point)
                    #print(change_point)

                if i == self.sequence_size - 1:
                    detector.is_change_detected = True
                    prev_at = self.detected_change_points[j][-1].at_ if len(self.detected_change_points[j]) > 0 else 0
                    prev_value_len = i - prev_at
                    change_point = ChangePoint(detector.current_value, -1, i, prev_value_len, self.sequences_names[j])
                    self.detected_change_points[j].append(change_point)
                    #print(change_point)

                if i == 0:
                    detector.is_change_detected = True
                    change_point = ChangePoint(-1, value, i, 0, self.sequences_names[j])
                    self.detected_change_points[j].append(change_point)

                if detect_rules:
                    self.rules_detector.search_rules(j, i)


        def dict_to_arrays(ddict):
            new_dict = {}
            for k, v in ddict.items():
                new_dict[k] = np.array(v)
            return new_dict

        for i in range(0, len(self.sequences)):
            parameters_history[i] = dict_to_arrays(parameters_history[i])
            self.parameters_history[i] = parameters_history[i]

        if plot is True:
            self.display_results(**kwargs)

        return detector.is_change_detected

    def display_results(self, sequence_name='Sequence', **kwargs):
        for i in range(0, len(self.sequences)):
            sequence = self.sequences[i]
            detector = self.change_detectors[i]
            parameters_history = self.parameters_history[i]
            detected_change_points = self.detected_change_points[i]

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
            ticks = xl #- int(2/3 * len(sequence))

            ax.set_xticklabels(ticks)

            # Plot a horizontal line where the change_point is detected
            for change_point in detected_change_points:
                ax.vlines(x=change_point.at_, ymin=0, ymax=ax.get_ylim()[1],
                      colors='r', linestyles='dotted')

            # Plot each parameter
            for ii, (res_name, res_values) in enumerate(parameters_history.items()):
                ax = axes[ii+1]
                ax.plot(res_values, 'g.', alpha=0.7)
                ax.set_title("Parameter #{}: {}".format(ii+1, res_name))

                for change_poin in detected_change_points:
                    ax.vlines(x=change_poin.at_, ymin=0, ymax=ax.get_ylim()[1],
                          colors='r', linestyles='dotted')

        plt.show()