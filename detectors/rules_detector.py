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

from detectors import detector
from change_point import ChangePoint
from rule_component import RuleComponent
from rule import Rule
from online_simulator import OnlineSimulator
from utils import *

class RulesDetector(object):
    def __init__(self, target_seq_index, window_size=0, round_to=100, type="all", combined=False):
        self.target_seq_index = target_seq_index
        self.round_to = round_to
        self.window_size = window_size
        self.type = type
        self.combined = combined

    def set_online_simulator(self, simulator):
        self.simulator = simulator

    def search_rules(self, seq_index, current_index):
        if(seq_index == self.target_seq_index and
           self.simulator.change_detectors[seq_index].is_change_detected is True and
           len(self.simulator.detected_change_points[seq_index]) > 1):

            prev_change_point_target = self.get_previous_change_point_in_target()
            pre_prev_change_point_target = self.get_pre_previuus_change_point_in_target()

            if self.window_size:
                window_begin = round_to(prev_change_point_target.at_, self.round_to) - self.window_size \
                    if pre_prev_change_point_target != None else 0
            else:
                window_begin = round_to(pre_prev_change_point_target.at_, self.round_to) \
                    if pre_prev_change_point_target != None else 0

            window_end = round_to(prev_change_point_target.at_, self.round_to)

            if self.type == "closed":
                self.generate_closed_rules(window_begin, window_end, current_index)

            elif self.type == "generate_discretized":
                self.generate_discretized_sequences(window_begin, window_end, current_index)

            elif self.type == "all":
                self.generate_all_rules(window_begin, window_end, current_index)

            elif self.type == "simple":
                self.generate_simple_rules(window_begin, window_end, current_index)
            
            else:
                print("ERROR - incorrect rules_detector type")

    def get_previous_change_point_in_target(self):
        prev_change_point = self.simulator.detected_change_points[self.target_seq_index][-2]
        return prev_change_point

    def get_pre_previuus_change_point_in_target(self):
        pre_prev_change_point = None
        if len(self.simulator.detected_change_points[self.target_seq_index]) > 2:
            pre_prev_change_point = self.simulator.detected_change_points[self.target_seq_index][-3]
        return pre_prev_change_point

    def generate_simple_rules(self, window_begin, window_end, current_index):
        generated_rules = [[] for i in range(len(self.simulator.sequences))]
        for seq_index, change_point_list in enumerate(self.simulator.detected_change_points):           
            lhs = []
            points_before_window, points_in_window, points_after_window = \
                self.get_change_points_in_window(seq_index, window_begin, window_end)

            # no change points in window
            if len(points_in_window) == 0:
                if round_to(window_end - window_begin, self.round_to):
                    lhs_elem = RuleComponent(-1, 
                                             points_before_window[-1].curr_value if len(points_before_window) > 0 else -1,
                                             self.simulator.sequences_names[seq_index],
                                             0)
                    lhs_elem.prev_value = points_before_window[-1].curr_value if len(points_before_window) > 0 else -1
                    lhs.append(lhs_elem)

            else:
                for point in points_in_window:
                    # print("inside window case")
                    if round_to(point.prev_value_len, self.round_to) > 0:
                        lhs_elem = RuleComponent(-1,
                                                 point.curr_value,
                                                 point.attr_name,
                                                 point.prev_value_percent)
                        lhs_elem.prev_value = point.prev_value
                        lhs.append(lhs_elem)
                    

            prev_target_cp = self.simulator.detected_change_points[self.target_seq_index][-2]
            rhs_elem = RuleComponent(prev_target_cp.curr_value,
                                     prev_target_cp.curr_value,
                                     prev_target_cp.attr_name,
                                     prev_target_cp.prev_value_percent)
            rhs_elem.prev_value = prev_target_cp.prev_value

            if len(lhs) > 0:
                self.update_discovered_lhss(seq_index, current_index, [lhs])
                self.generate_and_update_rules(seq_index, current_index,
                                               [lhs], [rhs_elem],
                                               generated_rules)               
       
    def generate_closed_rules(self, window_begin, window_end, current_index):
        combined_rule = []
        for seq_index, change_point_list in enumerate(self.simulator.detected_change_points):
            if seq_index == self.target_seq_index:
                continue

            lhs = []
            points_before_window, points_in_window, points_after_window = \
                self.get_change_points_in_window(seq_index, window_begin, window_end)

            # no change points in window
            if len(points_in_window) == 0:
                if round_to(window_end - window_begin, self.round_to):
                    lhs_elem = RuleComponent(round_to(window_end - window_begin, self.round_to),
                                           points_before_window[-1].curr_value if len(points_before_window) > 0 else -1,
                                           self.simulator.sequences_names[seq_index],
                                             0)
                    lhs.append(lhs_elem)

            else:
                first_point = points_in_window[0]
                skip_first_point = False
                if first_point.at_ - first_point.prev_value_len < window_begin:
                    # print("before window case")
                    if round_to(first_point.at_ - window_begin, self.round_to) > 0:
                        lhs_elem = RuleComponent(round_to(first_point.at_ - window_begin, self.round_to),
                                               first_point.prev_value,
                                               first_point.attr_name,
                                                 first_point.prev_value_percent)
                        lhs.append(lhs_elem)
                        skip_first_point = True

                for point in points_in_window[1:] if skip_first_point else points_in_window:
                    # print("inside window case")
                    if round_to(point.prev_value_len, self.round_to) > 0:
                        lhs_elem = RuleComponent(round_to(point.prev_value_len, self.round_to),
                                               point.prev_value,
                                               point.attr_name,
                                            point.prev_value_percent)
                        lhs.append(lhs_elem)

                last_point = points_in_window[-1]
                if last_point.at_ < window_end:
                    # print("after window case")
                    lhs_elem = RuleComponent(round_to(window_end - last_point.at_, self.round_to),
                                           last_point.curr_value,
                                           last_point.attr_name,
                                             last_point.prev_value_percent)
                    lhs.append(lhs_elem)

            rhs_elem = RuleComponent(
                round_to(self.simulator.detected_change_points[self.target_seq_index][-1].prev_value_len,
                         self.round_to),
                self.simulator.detected_change_points[self.target_seq_index][-1].prev_value,
                self.simulator.detected_change_points[self.target_seq_index][-1].attr_name,
                self.simulator.detected_change_points[self.target_seq_index][-1].prev_value_percent)
           
            if len(lhs) > 0:
                

                rule = Rule(lhs, rhs_elem)
                rule.occurrences.append(current_index)

                is_new_rule = True
                for r in self.simulator.rules_sets[seq_index]:
                    if r == rule:
                        is_new_rule = False
                        r.set_last_occurence(current_index)
                        r.increment_rule_support()
                        r.occurrences.append(current_index)
                        r.lhs_support = 1
                        combined_rule.append(r)
                        print("Rule already in set:", r)

                if is_new_rule:
                    rule.set_last_occurence(current_index)
                    rule.increment_rule_support()
                    rule.lhs_support = 1
                    # gen_rule = self.generalize_rule(seq_index, rule)
                    # if gen_rule != None:
                    #     gen_rule.set_last_occurence(current_index)
                    #     self.simulator.rules_sets[m].add(gen_rule)

                    self.simulator.rules_sets[seq_index].add(rule)
                    combined_rule.append(rule)
                    print("New rule:", rule)

        if len(combined_rule) > 0:
            print("Adding to combined rules")
            self.simulator.combined_rules.add(tuple(combined_rule))

    def generate_all_rules(self, window_begin, window_end, current_index):
        generated_rules = [[] for i in range(len(self.simulator.sequences))]
        
        for seq_index, change_point_list in enumerate(self.simulator.detected_change_points):
            # if seq_index == self.target_seq_index:
            #     continue

            generated_lhss = []
            generated_rhss = []
            points_before_window, points_in_window, points_after_window = \
                self.get_change_points_in_window(seq_index, window_begin, window_end)

            if not points_in_window:
                generated_lhss = self.generate_lhss_for_empty_window(seq_index, points_before_window, window_begin, window_end)
            else:
                generated_lhss = self.generate_lhss(points_in_window, window_begin, window_end)

            generated_rhss = self.generate_rhss()

            if generated_lhss:
                self.update_discovered_lhss(seq_index, current_index, generated_lhss)
                self.generate_and_update_rules(seq_index, current_index,
                                               generated_lhss, generated_rhss,
                                               generated_rules)

        if self.combined:
            combined_rule = []
            #[self.simulator.combined_rules.add((x,y,z)) if x.rhs == y.rhs and x.rhs == z.rhs
            # else None for x in generated_rules[0] for y in generated_rules[1] for z in generated_rules[2]]

            for seq_rules in generated_rules:
                if seq_rules:
                    combined_rule.append(seq_rules[-1])
                    # print("seq_rule:", seq_rules[-1])
                    # for gr in seq_rules:
                    #     print(gr)
                    # print("==============================================")

            if len(combined_rule) > 0:
                # print("Adding to combined rules")
                self.simulator.combined_rules.add(tuple(combined_rule))

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
        #generated_rules = [[] for i in range(len(self.simulator.sequences))]

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
        #return generated_rules

    def generalize_rule(self, seq_index, new_rule):
        for rule in self.simulator.rules_sets[seq_index]:

            gen_rule = Rule([], None)

            contains, generalized_rhs = rule.rhs.generalize(new_rule.rhs)
            if contains > 0:
                gen_rule.rhs = generalized_rhs
                for i in range(1, min(len(rule.lhs)+1, len(new_rule.lhs)+1)):
                    lhs_contains, generalized_lhs = rule.lhs[-i].generalize(new_rule.lhs[-i])
                    if lhs_contains > 0: # lhs can be generazlized
                        gen_rule.lhs.insert(0, generalized_lhs)
                    else:
                        break

            if (len(gen_rule.lhs) > 0 and gen_rule.rhs != None and
                gen_rule != new_rule and gen_rule != rule):
                print("== GENERALZED RULE ==")
                print("rule:     ", rule)
                print("new rule: ", new_rule)
                print("gen_rule: ", gen_rule)
                print()
                gen_rule.rule_support = rule.rule_support + new_rule.rule_support
                gen_rule.generalized = True
                return gen_rule
            else:
                return None

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

    def generate_discretized_sequences(self, window_begin, window_end, current_index):
        for seq_index, change_point_list in enumerate(self.simulator.detected_change_points):
            if seq_index == self.target_seq_index:
                continue

            lhs_x = []
            points_before_window, points_in_window, points_after_window = \
                self.get_change_points_in_window(seq_index, window_begin, window_end)

            # no change points in window
            if len(points_in_window) == 0:
                if round_to(window_end - window_begin, self.round_to):
                    x = round_to(window_end - window_begin, self.round_to)
                    if x > 0:
                        for lhs_len in range(0, x, self.round_to):
                            lhs_x.append(str(self.simulator.sequences_names[seq_index]) + ":" +
                                         str(points_before_window[-1].curr_value if len(points_before_window) > 0 else -1))

            else:
                first_point = points_in_window[0]
                skip_first_point = False
                if first_point.at_ - first_point.prev_value_len < window_begin:
                    # print("before window case")
                    if round_to(first_point.at_ - window_begin, self.round_to) > 0:
                        skip_first_point = True

                        x = round_to(first_point.at_ - window_begin, self.round_to)
                        if x > 0:
                            for lhs_len in range(0, x, self.round_to):
                                lhs_x.append(str(self.simulator.sequences_names[seq_index]) + ":" +
                                             str(first_point.prev_value))

                for point in points_in_window[1:] if skip_first_point else points_in_window:
                    # print("inside window case")
                    if round_to(point.prev_value_len, self.round_to) > 0:
                        x = round_to(point.prev_value_len, self.round_to)
                        if x > 0:
                            for lhs_len in range(0, x, self.round_to):
                                lhs_x.append(str(self.simulator.sequences_names[seq_index]) + ":" +
                                             str(point.prev_value))

                last_point = points_in_window[-1]
                if last_point.at_ < window_end:
                    # print("after window case")
                    x = round_to(window_end - last_point.at_, self.round_to)
                    if x > 0:
                        for lhs_len in range(0, x, self.round_to):
                            lhs_x.append(
                                str(self.simulator.sequences_names[seq_index]) + ":" + str(last_point.curr_value))

            if lhs_x:
                x = round_to(self.simulator.detected_change_points[self.target_seq_index][-1].prev_value_len, self.round_to)
                if x > 0:
                    for lhs_len in range(0, x, self.round_to):
                        lhs_x.append(
                            str(self.simulator.detected_change_points[self.target_seq_index][-1].attr_name) + ":" +
                            str(self.simulator.detected_change_points[self.target_seq_index][-1].prev_value))

                #print(lhs_x)
                self.simulator.discretized_sequences.append(lhs_x)