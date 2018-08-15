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
from change_point import ChangePoint
from rule_component import RuleComponent
from rule import Rule
from prediction import Prediction
from utils import *

class SequencePredictor(object):
    def __init__(self, simulator):
        self.simulator = simulator
        self.predicted = []
        self.predicted_len = 0
        self.predicted_rule = Rule(None, None)
        self.predictions = []
        self.MIN_LHS_LEN = 300
        self.PREDICT_WIN_SIZE = 1500
        self.last_best_rule = Rule(None, None)
        self.PREDICTION_STEP = 100

    def predict(self, curr_index, seq_index, detector):
        # no random subsequences
        if self.simulator.random_subsequences == False:
            if (curr_index >= self.simulator.sequence_size * self.simulator.predict_ratio and
                seq_index == self.simulator.rules_detector.target_seq_index and
                detector.is_change_detected is True):
            
                self.predict_sequence_no_random(curr_index)
        
        else:
            first_pred = True
            if self.simulator.rules_detector:
                first_pred = True if self.predicted_rule == Rule(None, None) else False
            
            if (curr_index >= self.simulator.sequence_size * self.simulator.predict_ratio):
                
                if first_pred:
                    if seq_index == self.simulator.rules_detector.target_seq_index and detector.is_change_detected is True:
                        self.predict_sequence(seq_index, curr_index)
                
                elif curr_index % self.simulator.rules_detector.round_to == 0 and seq_index == 0:
                    self.predict_sequence(seq_index, curr_index)

    def predict_sequence_no_random(self, curr_elem_index):
        for seq_index, change_point_list in enumerate(self.simulator.detected_change_points):
            window_end = round_to(curr_elem_index, self.simulator.round_to)
            window_begin = window_end - self.PREDICT_WIN_SIZE
            points_before_window, points_in_window, points_after_window = \
                self.get_change_points_in_window(seq_index, window_begin, window_end)

            lhss = []
            self.generate_lhss(lhss, seq_index, window_begin, window_end, points_in_window, 
                               points_before_window, points_after_window)

            predictions = []
            for lhs in lhss:
                self.get_predictions_by_lhs(seq_index, lhs, predictions)

            predictions_dict = {}
            for pred in predictions:
                if pred.rhs in predictions_dict:
                    predictions_dict[pred.rhs].append(pred)
                else:
                    predictions_dict[pred.rhs] = [pred]

            best_rule_score = -1
            best_rule = None
            for rhs, rules_list in predictions_dict.items():
                if rules_list[-1].get_rule_score() > best_rule_score:
                    best_rule = rules_list[-1]
                    best_rule_score = best_rule.get_rule_score()

            if best_rule:
                if best_rule.get_rule_score() > self.last_best_rule.get_rule_score():
                    self.last_best_rule = best_rule
                
        if self.predicted == []:
            predicted_seq = [-1 for i in range(curr_elem_index)]             
            self.predicted = predicted_seq + [self.last_best_rule.rhs.value for i in range(self.last_best_rule.rhs.len)]
        else:
            self.predicted = self.predicted + [self.last_best_rule.rhs.value for i in range(self.last_best_rule.rhs.len)]
            self.simulator.best_rules.append((round_to(curr_elem_index, self.simulator.round_to), self.last_best_rule) )

        self.last_best_rule = Rule(None, None)
        
    
    def predict_sequence(self, seq_index, curr_elem_index):
        # if seq_index != self.simulator.rules_detector.target_seq_index:
        #     return
        
        window_end = round_to(curr_elem_index, self.simulator.round_to)
        window_begin = window_end - self.PREDICT_WIN_SIZE

        points_before_window, points_in_window, points_after_window = \
            self.get_change_points_in_window(seq_index, window_begin, window_end)

        lhss = []
        self.generate_lhss(lhss,seq_index,window_begin,window_end,points_in_window,points_before_window,points_after_window)

        predictions = []
        for lhs in lhss:
            self.get_predictions_by_lhs(seq_index, lhs, predictions)

        predictions_dict = {}
        for pred in predictions:
            if pred.rhs in predictions_dict:
                predictions_dict[pred.rhs].append(pred)
            else:
                predictions_dict[pred.rhs] = [pred]

        best_rule_score = -1
        best_rule = None
        for rhs, rules_list in predictions_dict.items():
            if rules_list[-1].get_rule_score() > best_rule_score:
                best_rule = rules_list[-1]
                best_rule_score = best_rule.get_rule_score()

        if best_rule:
            # new better than current or current rule
            if best_rule.get_rule_score() > self.predicted_rule.get_rule_score() or self.predicted_len <= curr_elem_index:
                if self.predicted == []:
                    predicted_seq = [-1 for i in range(curr_elem_index)]             
                    self.predicted = predicted_seq + [best_rule.rhs.value for i in range(self.PREDICTION_STEP)]
                else:
                    self.predicted = self.predicted + [best_rule.rhs.value for i in range(self.PREDICTION_STEP)]                   
                
                self.simulator.best_rules.append((round_to(curr_elem_index, self.simulator.round_to), best_rule))
                self.predicted_len = curr_elem_index + best_rule.rhs.len
                self.predicted_rule = best_rule

            else:
                if self.predicted == []:
                    predicted_seq = [-1 for i in range(curr_elem_index)]             
                    self.predicted = predicted_seq + [self.predicted_rule.rhs.value for i in range(self.PREDICTION_STEP)]
                else:
                    self.predicted = self.predicted + [self.predicted_rule.rhs.value for i in range(self.PREDICTION_STEP)]
        else:
            self.predicted = self.predicted + [-1 for i in range(100)]

    def generate_lhss(self, lhss, seq_index, window_begin, window_end, points_in_window, points_before_window, points_after_window):
        if not points_in_window:
            lhs_elem_len = round_to(window_end - window_begin, self.simulator.round_to)
            if lhs_elem_len > 0:
                for lhs_len in range(self.simulator.round_to, lhs_elem_len, self.simulator.round_to):
                    lhs_elem = RuleComponent(lhs_len,
                                             points_before_window[-1].curr_value if len(points_before_window) > 0 else np.nan,
                                             self.simulator.sequences_names[seq_index])
                    lhss.append([lhs_elem])
        else:
            last_point = points_in_window[-1]
            if last_point.at_ <= window_end:
                lhs_elem_len = round_to(window_end - last_point.at_, self.simulator.round_to)
                for lhs_len in range(self.simulator.round_to, lhs_elem_len + 1, self.simulator.round_to):
                    lhs_elem = RuleComponent(lhs_len,
                                             last_point.curr_value,
                                             last_point.attr_name,
                                             last_point.prev_value_percent)
                    lhss.append([lhs_elem])

            for point_index in range(1, len(points_in_window)):
                prefix = lhss[-1] if lhss else []
                point = points_in_window[-point_index]
                lhs_elem_len = round_to(point.prev_value_len, self.simulator.round_to)
                if lhs_elem_len > 0:
                    for lhs_len in range(self.simulator.round_to, lhs_elem_len + 1, self.simulator.round_to):
                        lhs_elem = RuleComponent(lhs_len,
                                                 point.prev_value,
                                                 point.attr_name,
                                                 point.prev_value_percent)

                        lhss.append([lhs_elem] + prefix)

    def get_predictions_by_lhs(self, seq_index, lhs, predictions):
        for rule in sorted(self.simulator.rules_sets[seq_index], key=lambda r: (r.get_rule_score()), reverse=True):
            if rule.lhs == lhs:
                predictions.append(rule)
                break

    def find_common_lhs_part(self, seq_index, lhs, predictions):
        for rule in sorted(self.simulator.rules_sets[seq_index], key=lambda r: (r.get_rule_score()), reverse=True):
            if rule.lhs == lhs:
                if rule.rhs in predictions:
                    predictions[rule.rhs].append(
                        Prediction(rule.rhs, lhs, rule, predictions[rule.rhs][-1].number_of_occurrences + 1))
                else:
                    predictions[rule.rhs] = [Prediction(rule.rhs, lhs, rule, 1)]
                # print("Adding to predictions", lhs, "==>", rule.rhs, "nr of rules supporting:", predictions[rule.rhs][-1].number_of_occurrences, "because of rule:\n", rule)
                # print()
                break

    def get_change_points_in_window(self, seq_index, window_begin, window_end):
        points_in_window = []
        points_before_window = []
        points_after_window = []
        for change_point in self.simulator.detected_change_points[seq_index]:
            if round_to(change_point.at_, self.simulator.round_to) > window_begin:
                if round_to(change_point.at_, self.simulator.round_to) < window_end:
                    points_in_window.append(change_point)
                else:  # change point is after windows end
                    points_after_window.append(change_point)
            else:  # change point is before windows start
                points_before_window.append(change_point)
        return (points_before_window, points_in_window, points_after_window)
