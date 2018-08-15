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
                 round_to=100, predict_ratio=0.9, plot_change_detectors=False):

        self.sequences = sequences
        self.sequences_names = seqs_names
        self.change_detectors = change_detectors
        self.sequence_size = len(sequences[0])
        self.detected_change_points = [[] for i in range(len(self.sequences))]
        self.rounded_change_points = [[] for i in range(len(self.sequences))]
        self.rules_sets = [set() for i in range(len(self.sequences))]
        self.parameters_history = [defaultdict(list) for i in range(len(self.sequences))]
        self.rules_detector = rules_detector
        self.combined_rules = set()
        self.round_to = round_to
        self.predictor = SequencePredictor(self)
        self.lhs_sets = [set() for i in range(len(self.sequences))]
        self.discretized_sequences = []
        self.plot_change_detectors = plot_change_detectors
        self.predict_ratio = predict_ratio
        self.plot_parameters = False
        self.best_rules = []
        self.label_encoder = None
        self.random_subsequences = False

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

        for curr_index in range(0, self.sequence_size):
            for seq_index, seq in enumerate(self.sequences):
                detector = self.change_detectors[seq_index]

                value = seq[curr_index]
                res = detector.step(value)

                for k, v in res.items():
                    parameters_history[seq_index][k].append(v)

                if detector.is_change_detected is True:
                    self.add_change_point(curr_index, seq_index, detector, value)
                
                if curr_index == self.sequence_size - 1:
                    self.add_change_point_at_end(curr_index, seq_index, detector, value)    
                
                if curr_index == 0:
                    self.add_change_point_at_start(curr_index, seq_index, detector, value)

                if detect_rules:
                    self.rules_detector.search_rules(seq_index, curr_index)

                if predict_seq:
                    self.predictor.predict(curr_index, seq_index, detector)

                # no random subsequences
                # if (predict_seq and
                #    curr_index >= self.sequence_size * self.predict_ratio and
                #    seq_index == self.rules_detector.target_seq_index and
                #    detector.is_change_detected is True):
                #     self.predictor.predict_sequence_no_random(curr_index)
                

                # first_pred = True
                # if self.rules_detector:
                #     first_pred = True if self.predictor.predicted_rule == Rule(None, None) else False
                
                # if (predict_seq and curr_index >= self.sequence_size * self.predict_ratio):
                #     if first_pred:
                #         if seq_index == self.rules_detector.target_seq_index and detector.is_change_detected is True:
                #             self.predictor.predict_sequence(seq_index, curr_index)
                    
                #     elif curr_index % self.rules_detector.round_to == 0 and seq_index == 0:
                #         self.predictor.predict_sequence(seq_index, curr_index)

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

            plotcount = 1
            if self.plot_parameters:
                plotcount = 1 + len(parameters_history)

            fig, axes = plt.subplots(nrows=plotcount, ncols=1, sharex=True,
                                     figsize=(12, plotcount*3))

            if self.sequences_names[i].endswith('_code'):
                sequence = [int(x) for x in sequence]
                sequence = self.label_encoder.inverse_transform(sequence)
            
            # Plot the sequence
            if plotcount > 1:
                ax = axes[0]
            elif plotcount == 1:
                ax = axes

            ax.plot(sequence, 'b.', markersize=3, label="Actual values")
            ax.plot(sequence, 'b-', alpha=0.25)

            # Print predicted sequence
            if self.rules_detector and i == self.rules_detector.target_seq_index:
                ax.plot(self.predictor.predicted, 'r.', markersize=3, label="Predicted values")
                ax.legend(loc=2)

            ax.set_title(sequence_name)
            # ax.set_ylim(np.nanmin(sequence)-1,
            #             np.nanmax(sequence)+1)
            # ax.set_xlim(0, len(sequence))

            # xl = ax.get_xticks()
            # ticks = xl
            # ax.set_xticklabels(ticks)

            # Plot a horizontal line where the change_point is detected
            for change_point in detected_change_points:
                ax.axvline(change_point.at_, color='r', linestyle='--')

            if self.plot_parameters:
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
    
    def add_change_point(self, curr_index, seq_index, detector, value):
        prev_at = self.detected_change_points[seq_index][-1].at_ if len(self.detected_change_points[seq_index]) > 0 else 0
        prev_value_len = curr_index - prev_at
        change_point = ChangePoint(detector.previous_value,
                                    detector.current_value,
                                    curr_index,
                                    prev_value_len,
                                    self.sequences_names[seq_index],
                                    detector.percent)
        self.detected_change_points[seq_index][-1].curr_value_len = change_point.prev_value_len
        self.detected_change_points[seq_index][-1].curr_value_percent = change_point.prev_value_percent
        self.detected_change_points[seq_index].append(change_point)
        self.rounded_change_points[seq_index].append(change_point.get_rounded(self.round_to))

    def add_change_point_at_end(self, curr_index, seq_index, detector, value):                   
        detector.is_change_detected = True
        prev_at = self.detected_change_points[seq_index][-1].at_ if len(self.detected_change_points[seq_index]) > 0 else 0
        prev_value_len = curr_index - prev_at
        change_point = ChangePoint(detector.current_value,
                                   -1,
                                   curr_index,
                                   prev_value_len,
                                   self.sequences_names[seq_index],
                                   detector.percent)
        self.detected_change_points[seq_index][-1].curr_value_len = change_point.prev_value_len
        self.detected_change_points[seq_index][-1].curr_value_percent = change_point.prev_value_percent
        self.detected_change_points[seq_index].append(change_point)
        self.rounded_change_points[seq_index].append(change_point.get_rounded(self.round_to))

    def add_change_point_at_start(self, curr_index, seq_index, detector, value): 
        detector.is_change_detected = True
        change_point = ChangePoint(-1,
                                    value,
                                    curr_index,
                                    0,
                                    self.sequences_names[seq_index],
                                    detector.percent)
        self.detected_change_points[seq_index].append(change_point)
        self.rounded_change_points[seq_index].append(change_point.get_rounded(self.round_to))