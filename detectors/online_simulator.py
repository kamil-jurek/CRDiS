# The MIT License
# Copyright (c) 2018 Kamil Jurek
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import numpy as np
import matplotlib.pyplot as plt

from detectors import detector
from change_point import ChangePoint
from rule_component import RuleComponent
from rule import Rule
from prediction import Prediction
from sequence_predictor import SequencePredictor
from collections import defaultdict
from utils import *

class OnlineSimulator(object):
    def __init__(self, rules_detector, change_detectors, sequences, seqs_names,
                 predict_ratio=0.9, plot_change_detectors=False):

        self.sequences = sequences
        self.sequences_names = seqs_names
        self.change_detectors = change_detectors
        self.sequence_size = len(sequences[0])
        self.detected_change_points = [[] for i in range(len(self.sequences))]
        self.rules_sets = [set() for i in range(len(self.sequences))]
        self.parameters_history = [defaultdict(list) for i in range(len(self.sequences))]
        self.rules_detector = rules_detector
        self.combined_rules = set()
        self.round_to = 100
        self.predictor = SequencePredictor(self)
        self.lhs_sets = [set() for i in range(len(self.sequences))]
        self.discretized_sequences = []
        self.plot_change_detectors = plot_change_detectors
        self.predict_ratio = predict_ratio

        if rules_detector != None:
            self.rules_detector.set_online_simulator(self)

    def get_detected_changes(self):
        return self.detected_change_points

    def get_rules_sets(self):
        return self.rules_sets

    def get_combined_rules(self):
        return self.combined_rules

    def run(self, plot=True, detect_rules=True, predict_seq=False, **kwargs):
        parameters_history = [defaultdict(list) for i in range(len(self.sequences))]

        for i in range(0, self.sequence_size):
            for j, seq in enumerate(self.sequences):
                detector = self.change_detectors[j]

                value = seq[i]
                res = detector.step(value)

                for k, v in res.items():
                    parameters_history[j][k].append(v)

                if detector.is_change_detected is True:
                    prev_at = self.detected_change_points[j][-1].at_ if len(self.detected_change_points[j]) > 0 else 0
                    prev_value_len = i - prev_at

                    change_point = ChangePoint(detector.previous_value,
                                               detector.current_value,
                                               i,
                                               prev_value_len,
                                               self.sequences_names[j],
                                               detector.percent)
                    self.detected_change_points[j].append(change_point)

                if i == self.sequence_size - 1:
                    detector.is_change_detected = True
                    prev_at = self.detected_change_points[j][-1].at_ if len(self.detected_change_points[j]) > 0 else 0
                    prev_value_len = i - prev_at
                    change_point = ChangePoint(detector.current_value,
                                               -1,
                                               i,
                                               prev_value_len,
                                               self.sequences_names[j],
                                               detector.percent)
                    self.detected_change_points[j].append(change_point)

                if i == 0:
                    detector.is_change_detected = True
                    change_point = ChangePoint(-1,
                                               value,
                                               i,
                                               0,
                                               self.sequences_names[j],
                                               detector.percent)
                    self.detected_change_points[j].append(change_point)

                if detect_rules:
                    self.rules_detector.search_rules(j, i)

                if(predict_seq and
                   i >= self.sequence_size*self.predict_ratio and
                   i % self.rules_detector.round_to == 0):
                    self.predictor.predict_sequence(j, i)


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

    def display_results(self, sequence_name='Sequence ', **kwargs):
        for i in range(0, len(self.sequences)):
            sequence = self.sequences[i]
            detector = self.change_detectors[i]
            parameters_history = self.parameters_history[i]
            detected_change_points = self.detected_change_points[i]
            sequence_name = 'Sequence ' + self.sequences_names[i]

            plotcount = 1 + len(parameters_history)
            fig, axes = plt.subplots(nrows=plotcount, ncols=1, sharex=True,
                                     figsize=(12, plotcount*3))

            # Plot the sequence
            if plotcount > 1:
                ax = axes[0]
            elif plotcount == 1:
                ax = axes

            ax.plot(sequence, 'b.', markersize=3)
            ax.plot(sequence, 'b-', alpha=0.25)

            # Print predicted sequence
            if self.rules_detector and i == self.rules_detector.target_seq_index:
                ax.plot(self.predictor.predicted, 'r', linewidth=3.0)

            ax.set_title(sequence_name)
            ax.set_ylim(np.nanmin(sequence)-1,
                        np.nanmax(sequence)+1)
            ax.set_xlim(0, len(sequence))

            xl = ax.get_xticks()
            ticks = xl
            ax.set_xticklabels(ticks)

            # Plot a horizontal line where the change_point is detected
            for change_point in detected_change_points:
                ax.axvline(change_point.at_, color='r', linestyle='--')

            # Plot each parameter
            for ii, (res_name, res_values) in enumerate(parameters_history.items()):
                ax = axes[ii+1]
                ax.plot(res_values, '-', alpha=0.7)
                ax.set_title("Parameter #{}: {}".format(ii+1, res_name))

                for change_point in detected_change_points:
                    ax.axvline(change_point.at_, color='r', linestyle='--')

        if self.plot_change_detectors:
            plotcount = len(self.sequences)
            fig, axes = plt.subplots(nrows=plotcount, ncols=1, sharex=True,
                                     figsize=(12, plotcount * 3))

            if plotcount > 1:
                ax = axes[0]
            elif plotcount == 1:
                ax = axes

            for k in range(0, len(self.sequences)):
                print("k:",k)
                ax = axes[k]
                sequence1 = self.sequences[k]
                ax.plot(sequence1, 'b.', markersize=3)
                ax.plot(sequence1, 'b-', alpha=0.25)
                # ax.plot(res_values, '-', alpha=0.7)
                ax.set_title("Detector {}".format(self.sequences_names[k]))

                ax.set_ylim(np.nanmin(self.sequences[k]) - 1,
                            np.nanmax(self.sequences[k]) + 1)
                ax.set_xlim(0, len(self.sequences[k]))
                xl = ax.get_xticks()
                ticks = xl
                ax.set_xticklabels(ticks)

                for change_point in self.detected_change_points[k]:
                    ax.axvline(change_point.at_, color='r', linestyle='--')