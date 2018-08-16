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
from rules_generator import RulesGenerator
from rule_component import RuleComponent
from utils import *

class ClosedRulesGenerator(RulesGenerator):
    def __init__(self, target_seq_index, window_size=0, round_to=100, combined=False):
        super(ClosedRulesGenerator, self).__init__()
        self.target_seq_index = target_seq_index
        self.round_to = round_to
        self.window_size = window_size
        self.combined = combined
        self.simulator = None

    def generate_rules(self, window_begin, window_end, current_index):
        generated_rules = [[] for i in range(len(self.simulator.sequences))]
        
        for seq_index, change_point_list in enumerate(self.simulator.detected_change_points):
            # if seq_index == self.target_seq_index:
            #     continue

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
                         round_to(self.simulator.detected_change_points[self.target_seq_index][-1].prev_value_len, self.round_to),
                         self.simulator.detected_change_points[self.target_seq_index][-1].prev_value,
                         self.simulator.detected_change_points[self.target_seq_index][-1].attr_name,
                         self.simulator.detected_change_points[self.target_seq_index][-1].prev_value_percent)
           
            if len(lhs) > 0:
                self.update_discovered_lhss(seq_index, current_index, [lhs])
                self.generate_and_update_rules(seq_index, current_index,
                                                [lhs], [rhs_elem],
                                                generated_rules)   
            
        if self.combined:
            combined_rule = []
            for seq_rules in generated_rules:
                if seq_rules:
                    combined_rule.append(seq_rules[-1])

            if len(combined_rule) > 0:
                # print("Adding to combined rules")
                self.simulator.combined_rules.add(tuple(combined_rule))