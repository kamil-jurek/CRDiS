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

from rule_component import RuleComponent
from rule import Rule
from utils import *

class RulesGenerator(object):
    def __init__(self):
            self.target_seq_index = 0
            self.round_to = 100
            self.window_size = 0
            self.combined = False
            self.simulator = None

    def set_online_simulator(self, simulator):
        self.simulator = simulator

    def search_rules(self, seq_index, current_index):
        if(seq_index == self.target_seq_index and
           self.simulator.change_detectors[self.target_seq_index].is_change_detected and
           len(self.simulator.detected_change_points[self.target_seq_index]) > 1):

            prev_change_point_target = self.get_previous_change_point_in_target()
            pre_prev_change_point_target = self.get_pre_previuus_change_point_in_target()

            if self.window_size:
                window_begin = round_to(prev_change_point_target.at_, self.round_to) - self.window_size \
                    if pre_prev_change_point_target != None else 0
            else:
                window_begin = round_to(pre_prev_change_point_target.at_, self.round_to) \
                    if pre_prev_change_point_target != None else 0

            window_end = round_to(prev_change_point_target.at_, self.round_to)

            self.generate_rules(window_begin, window_end, current_index)

    def generate_rules(self, window_begin, window_end, current_index):
        pass

    def get_previous_change_point_in_target(self):
        prev_change_point = self.simulator.detected_change_points[self.target_seq_index][-2]
        return prev_change_point

    def get_pre_previuus_change_point_in_target(self):
        pre_prev_change_point = None
        if len(self.simulator.detected_change_points[self.target_seq_index]) > 2:
            pre_prev_change_point = self.simulator.detected_change_points[self.target_seq_index][-3]
        return pre_prev_change_point

    def generate_lhss(self,points_in_window, window_begin, window_end):
        generated_lhss = []
        last_point = points_in_window[-1]
        if last_point.at_ <= window_end:
            lhs_elem_len = round_to(window_end - last_point.at_, self.round_to)
            for lhs_len in range(self.round_to, lhs_elem_len + 1, self.round_to):
                lhs_elem = RuleComponent(lhs_len,
                                         last_point.curr_value,
                                         last_point.attr_name,
                                         last_point.prev_value_percent)
                generated_lhss.append([lhs_elem])

        for point_index in range(1, len(points_in_window)):
            prefix = generated_lhss[-1] if generated_lhss else []
            point = points_in_window[-point_index]
            lhs_elem_len = round_to(point.prev_value_len, self.round_to)
            if lhs_elem_len > 0:
                for lhs_len in range(self.round_to, lhs_elem_len + 1, self.round_to):
                    lhs_elem = RuleComponent(lhs_len,
                                             point.prev_value,
                                             point.attr_name,
                                             point.prev_value_percent)
                    generated_lhss.append([lhs_elem] + prefix)

        first_point = points_in_window[0]
        if round_to(first_point.at_ - first_point.prev_value_len, self.round_to) <= window_begin:
            lhs_elem_len = round_to(first_point.at_ - window_begin, self.round_to)
            if lhs_elem_len >= 0:
                prefix = generated_lhss[-1] if generated_lhss else []
                for lhs_len in range(self.round_to, lhs_elem_len + 1, self.round_to):
                    lhs_elem = RuleComponent(lhs_len,
                                             first_point.prev_value,
                                             first_point.attr_name,
                                             first_point.prev_value_percent)
                    generated_lhss.append([lhs_elem] + prefix)
        return generated_lhss

    def generate_rhss(self):
        generated_rhss = []

        last_target_change_point = self.simulator.detected_change_points[self.target_seq_index][-1]
        rhs_elem_len = round_to(last_target_change_point.prev_value_len, self.round_to)
        for rhs_len in range(self.round_to, rhs_elem_len + 1, self.round_to):
            rhs_elem = RuleComponent(rhs_len,
                                     last_target_change_point.prev_value,
                                     last_target_change_point.attr_name,
                                     last_target_change_point.prev_value_percent)
            generated_rhss.append(rhs_elem)
        return generated_rhss

    def generate_lhss_for_empty_window(self, seq_index, points_before_window, window_begin, window_end):
        generated_lhss = []
        lhs_elem_len = round_to(window_end - window_begin, self.round_to)
        if lhs_elem_len > 0:
            for lhs_len in range(self.round_to, lhs_elem_len + 1, self.round_to):
                percent = (list(self.simulator.sequences[seq_index][window_begin:window_end]).count(
                    self.simulator.change_detectors[seq_index].current_value) / lhs_elem_len) * 100

                lhs_elem = RuleComponent(lhs_len,
                                         points_before_window[-1].curr_value if len(
                                             points_before_window) > 0 else np.nan,
                                         self.simulator.sequences_names[seq_index],
                                         points_before_window[-1].prev_value_percent if len(
                                             points_before_window) > 0 else percent)

                generated_lhss.append([lhs_elem])
        return generated_lhss

    def update_discovered_lhss(self, seq_index, current_index, generated_lhss):
        for lhs in generated_lhss:
            new_lhs = Rule(lhs, [])
            is_new_lhs = True

            for lhs in self.simulator.lhs_sets[seq_index]:
                if lhs == new_lhs:
                    is_new_lhs = False
                    lhs.set_last_occurence(current_index)
                    lhs.increment_rule_support()
                    lhs.occurrences.append(current_index)
                    

            if is_new_lhs:
                new_lhs.set_last_occurence(current_index)
                new_lhs.increment_rule_support()
                new_lhs.occurrences.append(current_index)
                self.simulator.lhs_sets[seq_index].add(new_lhs)

    def generate_and_update_rules(self, seq_index, current_index, generated_lhss, generated_rhss, generated_rules):
        for rhs in generated_rhss:
            for lhs in generated_lhss:
                new_rule = Rule(lhs, rhs)

                is_new_rule = True
                for rule in self.simulator.rules_sets[seq_index]:
                    if rule == new_rule:
                        is_new_rule = False
                        rule.set_last_occurence(current_index)
                        rule.increment_rule_support()
                        rule.occurrences.append(current_index)
                        rule.lhs_support = self.get_support_of(lhs, seq_index)
                        generated_rules[seq_index].append(rule)

                if is_new_rule:
                    new_rule.set_last_occurence(current_index)
                    new_rule.increment_rule_support()
                    new_rule.occurrences.append(current_index)
                    new_rule.lhs_support = self.get_support_of(lhs, seq_index)
                    self.simulator.rules_sets[seq_index].add(new_rule)
                    generated_rules[seq_index].append(new_rule)

    def get_change_points_in_window(self, seq_index, window_begin, window_end):
        points_in_window = []
        points_before_window = []
        points_after_window = []
        for change_point in self.simulator.detected_change_points[seq_index]:
            if round_to(change_point.at_, self.round_to) > window_begin:
                if round_to(change_point.at_, self.round_to) < window_end:
                    points_in_window.append(change_point)
                else:  # change point is after windows end
                    points_after_window.append(change_point)
            else:  # change point is before windows start
                points_before_window.append(change_point)
        return (points_before_window, points_in_window, points_after_window)

    def get_support_of(self, lhs, seq_index):
        for r in self.simulator.lhs_sets[seq_index]:
            if r == Rule(lhs, []):
                return r.rule_support

