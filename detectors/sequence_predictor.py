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

    def predict_sequence(self, seq_index, curr_elem_index):
        # if seq_index == self.simulator.rules_detector.target_seq_index:
        #     return

        if seq_index != 0:
            return

        print("---START Predict sequence ", "seq_index:", seq_index, "curr_elem_index:", curr_elem_index)
        window_end = round_to(curr_elem_index, self.simulator.round_to)
        window_begin = window_end - self.PREDICT_WIN_SIZE

        points_before_window, points_in_window, points_after_window = \
            self.get_change_points_in_window(seq_index, window_begin, window_end)

        lhss = []
        self.generate_lhss(lhss,seq_index,window_begin,window_end,points_in_window,points_before_window,points_after_window)

        predictions = []
        # print("-----------------------------------------------------------------------------------------------")
        # print("All LHS:")
        for lhs in lhss:
            # print(lhs)
            self.get_predictions_by_lhs(seq_index, lhs, predictions)

        predictions_dict = {}
        for pred in predictions:
            # print("Prediction:  ", pred)
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

        # print("==========================================================")
        # print("best_rule:")
        # print(best_rule)
        # print("==========================================================")

        if best_rule:
            # new better than current or current rule
            print("best_rule.get_rule_score():", best_rule.get_rule_score())
            print("")
            if best_rule.get_rule_score() > self.predicted_rule.get_rule_score() or self.predicted_len <= curr_elem_index:
                if self.predicted == []:
                    predicted_seq = [-1 for i in range(curr_elem_index)]
                    for i in range(100):
                        predicted_seq.append(best_rule.rhs.value)

                    self.predicted = predicted_seq

                else:
                    self.predicted = self.predicted + [best_rule.rhs.value for i in range(100)]

                print("======================================================")
                print("curr_elem_index:", curr_elem_index)
                print("best_rule.rhs.value:", best_rule.rhs.value)
                print("predicting ", best_rule.rhs.value, "for 100 next elems")
                print(best_rule)
                print(curr_elem_index, len(self.predicted))
                print("self.predicted_len:", self.predicted_len)
                print("======================================================")

                self.predicted_len = curr_elem_index + best_rule.rhs.len
                self.predicted_rule = best_rule

            else:
                if self.predicted == []:
                    predicted_seq = [-1 for i in range(curr_elem_index)]
                    for i in range(100):
                        predicted_seq.append(self.predicted_rule.rhs.value)
                    self.predicted = predicted_seq

                else:
                    self.predicted = self.predicted + [self.predicted_rule.rhs.value for i in range(100)]
                print("======================================================")
                print("curr_elem_index:", curr_elem_index)
                print("self.predicted_rule.rhs.value:", self.predicted_rule.rhs.value)
                print("predicting ", self.predicted_rule.rhs.value, "for 100 next elems")
                print(self.predicted_rule)
                print(curr_elem_index, len(self.predicted))
                print("self.predicted_len:", self.predicted_len)
                print("======================================================")
        else:
            self.predicted = self.predicted + [-1 for i in range(100)]
            # prediction_list = []
            # for k, predictions_list in predictions.items():
            #     # for p in predictions_list:
            #     # print("\t", p.lhs, "==>", p.rhs, " nr:", p.number_of_occurrences, p.rule.number_of_occurrences, p.rule.get_rule_score())
            #
            #     # print("-----------------------------------------------------------------------------------------------")
            #     pred = predictions_list[-1]
            #     # print("\tPossible Best Prediction: ", pred.lhs, "==>", pred.rhs,
            #     #       " nrOfPredOcc:", pred.number_of_occurrences,
            #     #       " nrOfRuleOcc:", pred.rule.number_of_occurrences,
            #     #       " ruleScore:", pred.rule.get_rule_score(),
            #     #       " predScore:", pred.get_prediction_score())
            #
            #     # adding the best prediction for each RHS
            #     prediction_list.append(pred)
            #     # print("-----------------------------------------------------------------------------------------------")
            #
            # if prediction_list:
            #     # geting best possible prediction
            #
            #     # if prediction_list[-1][1].get_rule_score() >= self.predicted_rule.get_rule_score():
            #     prediction = sorted(prediction_list, key=lambda p: (p.get_prediction_score()), reverse=True)[0]
            #     if (prediction.get_prediction_score() > (
            #     self.predictions[-1].get_prediction_score() if self.predictions else 0) or
            #             curr_elem_index >= self.predicted_len):  # curr_elem_index >= self.predicted_len:
            #         print("Best prediction:", prediction)
            #         print("In index ", curr_elem_index, "predicting", prediction.lhs, "==>", k,
            #               "nr of rules supporting:", prediction.number_of_occurrences,
            #               "because of rule:\n", prediction.rule)
            #
            #         self.predicted_rule = prediction.rule
            #
            #         lhs_seq = []
            #         for lhs_elem in prediction.rule.lhs:
            #             for elem in range(lhs_elem.len):
            #                 lhs_seq.append(lhs_elem.value)
            #
            #         if len(lhs_seq) >= self.MIN_LHS_LEN:
            #             print("Adding new prediction")
            #             self.predictions.append(prediction)
            #             predicted_seq = [-1 for i in range(curr_elem_index)]  # -len(lhs_seq))] + lhs_seq
            #             for i in range(k.len):
            #                 predicted_seq.append(k.value)
            #
            #             if self.predicted == []:
            #                 self.predicted = predicted_seq
            #
            #             print("curr_elem_index:", curr_elem_index)
            #             print("k.value:", k.value)
            #             self.predicted = self.predicted[:curr_elem_index] + [k.value for i in range(k.len)]
            #             self.predicted_len = curr_elem_index + k.len
            #
            #             # if curr_elem_index <= self.predicted_len:
            #             #     self.predicted.remove(self.predicted[-1]) if self.predicted else None
            #             #     self.predicted.append(predicted_seq)
            #             # else:
            #             # self.predicted.append(predicted_seq)
            #             # self.predicted_len = curr_elem_index+k.len
        print("---END Predict sequence ", "seq_index:", seq_index, "curr_elem_index:", curr_elem_index)
        print("========================================================================================")

    def generate_lhss(self, lhss, seq_index, window_begin, window_end, points_in_window, points_before_window, points_after_window):
        if not points_in_window:
            lhs_elem_len = round_to(window_end - window_begin, self.simulator.round_to)
            if lhs_elem_len > 0:
                for lhs_len in range(self.simulator.round_to, lhs_elem_len, self.simulator.round_to):
                    lhs_elem = RuleComponent(lhs_len,
                                             points_before_window[-1].curr_value if len(
                                                 points_before_window) > 0 else np.nan,
                                             self.sequences_names[seq_index])
                    lhss.append([lhs_elem])
        else:
            last_point = points_in_window[-1]
            if last_point.at_ <= window_end:
                lhs_elem_len = round_to(window_end - last_point.at_, self.simulator.round_to)
                for lhs_len in range(self.simulator.round_to, lhs_elem_len + 1, self.simulator.round_to):
                    lhs_elem = RuleComponent(lhs_len,
                                             last_point.curr_value,
                                             last_point.attr_name,
                                             last_point.percent)
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
                                                 point.percent)

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
