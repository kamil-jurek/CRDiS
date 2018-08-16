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

class SimpleRulesGenerator(RulesGenerator):
    def __init__(self, target_seq_index, window_size=0, round_to=100, combined=False):
        super(SimpleRulesGenerator, self).__init__()
        self.target_seq_index = target_seq_index
        self.round_to = round_to
        self.window_size = window_size
        self.combined = combined
        self.simulator = None

    def generate_rules(self, window_begin, window_end, current_index):
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