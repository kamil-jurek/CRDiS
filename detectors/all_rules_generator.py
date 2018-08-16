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

class AllRulesGenerator(RulesGenerator):
    def __init__(self, target_seq_index, window_size=0, round_to=100, combined=False):
        super(AllRulesGenerator, self).__init__()
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