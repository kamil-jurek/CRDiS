from detectors import detector
from change_point import ChangePoint
from lhs_element import LHS_element
from rule import Rule
from online_simulator import OnlineSimulator

class RulesDetector(object):
    def __init__(self, target_seq_index, window_size=0,round_to=100):
        self.target_seq_index = target_seq_index
        self.round_to = round_to
        self.window_size = window_size

    def set_online_simulator(self, sim):
        self.simulator = sim

    def search_rules(self, seq_index, current_index):
        if (seq_index == self.target_seq_index and
            self.simulator.change_detectors[seq_index].is_change_detected is True and
            len(self.simulator.detected_change_points[seq_index]) > 1):

            prev_prev_change_point_target = self.simulator.detected_change_points[self.target_seq_index][-3] if len(self.simulator.detected_change_points[self.target_seq_index]) > 2 else None
            prev_change_point_target = self.simulator.detected_change_points[self.target_seq_index][-2]
            if self.window_size > 0:
                window_begin = round_to(prev_change_point_target.at_, self.round_to) - self.window_size if prev_prev_change_point_target != None else 0
            else:
                window_begin = round_to(prev_prev_change_point_target.at_, self.round_to) if prev_prev_change_point_target != None else 0
            window_end = round_to(prev_change_point_target.at_, self.round_to)

            #self.generate_closed_rules(window_begin, window_end, current_index)
            self.generate_all_rules(window_begin, window_end, current_index)

    def generate_closed_rules(self, window_begin, window_end, current_index):
        combined_rule = []
        for seq_index, change_point_list in enumerate(self.simulator.detected_change_points):
            if seq_index == self.target_seq_index:
                continue

            lhs = []
            points_before_window, points_in_window, points_after_window = self.get_change_points_in_window(seq_index, window_begin, window_end)

            # no change points in window
            if len(points_in_window) == 0:
                if round_to(window_end - window_begin, self.round_to):
                    lhs_elem = LHS_element(round_to(window_end - window_begin, self.round_to),
                                           points_before_window[-1].curr_value if len(points_before_window) > 0 else -1,
                                           self.simulator.sequences_names[seq_index])
                    lhs.append(lhs_elem)

            else:
                first_point = points_in_window[0]
                skip_first_point = False
                if first_point.at_ - first_point.prev_value_len < window_begin:
                    # print("before window case")
                    if round_to(first_point.at_ - window_begin, self.round_to) > 0:
                        lhs_elem = LHS_element(round_to(first_point.at_ - window_begin, self.round_to),
                                               first_point.prev_value,
                                               first_point.attr_name)
                        lhs.append(lhs_elem)
                        skip_first_point = True

                for point in points_in_window[1:] if skip_first_point else points_in_window:
                    # print("inside window case")
                    if round_to(point.prev_value_len, self.round_to) > 0:
                        lhs_elem = LHS_element(round_to(point.prev_value_len, self.round_to),
                                               point.prev_value,
                                               point.attr_name)
                        lhs.append(lhs_elem)

                last_point = points_in_window[-1]
                if last_point.at_ < window_end:
                    # print("after window case")
                    lhs_elem = LHS_element(round_to(window_end - last_point.at_, self.round_to),
                                           last_point.curr_value,
                                           last_point.attr_name)
                    lhs.append(lhs_elem)

            rhs_elem = LHS_element(
                round_to(self.simulator.detected_change_points[self.target_seq_index][-1].prev_value_len,
                         self.round_to),
                self.simulator.detected_change_points[self.target_seq_index][-1].prev_value,
                self.simulator.detected_change_points[self.target_seq_index][-1].attr_name)

            if len(lhs) > 0:
                rule = Rule(lhs, rhs_elem)
                rule.occurrences.append(current_index)

                is_new_rule = True
                for r in self.simulator.rules_sets[seq_index]:
                    if r == rule:
                        is_new_rule = False
                        r.set_last_occurence(current_index)
                        r.increment_occurrences()
                        r.occurrences.append(current_index)
                        combined_rule.append(rule)
                        print("Rule already in set:", r)

                if is_new_rule:
                    rule.set_last_occurence(current_index)
                    rule.increment_occurrences()
                    gen_rule = self.generalize_rule(seq_index, rule)
                    if gen_rule != None:
                        gen_rule.set_last_occurence(current_index)
                    #     self.simulator.rules_sets[m].add(gen_rule)

                    self.simulator.rules_sets[seq_index].add(rule)
                    combined_rule.append(rule)
                    print("New rule:", rule)

        if len(combined_rule) > 0:
            print("Adding to combined rules")
            self.simulator.combined_rules.append(combined_rule)

    def generate_all_rules(self, window_begin, window_end, current_index):
        generated_rules = [[] for i in range(len(self.simulator.detected_change_points))]
        combined_rule = []
        for seq_index, change_point_list in enumerate(self.simulator.detected_change_points):
            if seq_index == self.target_seq_index:
                continue

            lhss = []
            rhss = []
            points_before_window, points_in_window, points_after_window = self.get_change_points_in_window(seq_index, window_begin, window_end)

            # no change points in window
            if len(points_in_window) == 0:
                # print("no change points in window")
                if round_to(window_end - window_begin, self.round_to):
                    lhs_elem_len = round_to(window_end - window_begin, self.round_to)
                    for lhs_len in range(self.round_to, lhs_elem_len, self.round_to):
                        lhs_elem = LHS_element(lhs_len,
                                               points_before_window[-1].curr_value if len(
                                                   points_before_window) > 0 else -1,
                                               self.simulator.sequences_names[seq_index])
                        lhss.append([lhs_elem])
            else:
                last_point = points_in_window[-1]
                if last_point.at_ < window_end:
                    # print("after window case")
                    lhs_elem_len = round_to(window_end - last_point.at_, self.round_to)
                    for lhs_len in range(self.round_to, lhs_elem_len + 1, self.round_to):
                        lhs_elem = LHS_element(lhs_len,
                                               last_point.curr_value,
                                               last_point.attr_name)
                        lhss.append([lhs_elem])

                for point_index in range(1, len(points_in_window) + 1):
                    # print("inside window case")
                    prefix = lhss[-1]
                    # print("prefix:", prefix)
                    point = points_in_window[-point_index]
                    if round_to(point.prev_value_len, self.round_to) > 0:
                        lhs_elem_len = round_to(point.prev_value_len, self.round_to)
                        for lhs_len in range(self.round_to, lhs_elem_len + 1, self.round_to):
                            lhs_elem = LHS_element(lhs_len,
                                                   point.prev_value,
                                                   point.attr_name)
                            lhss.append([lhs_elem] + prefix)

            last_target_change_point = self.simulator.detected_change_points[self.target_seq_index][-1]
            rhs_elem_len = round_to(last_target_change_point.prev_value_len, self.round_to)
            for rhs_len in range(self.round_to, rhs_elem_len + 1, self.round_to):
                rhs_elem = LHS_element(rhs_len,
                                       last_target_change_point.prev_value,
                                       last_target_change_point.attr_name)
                rhss.append(rhs_elem)

            if len(lhss) > 0:
                for rhs in rhss:
                    for lhs in lhss:
                        rule = Rule(lhs, rhs)
                        rule.occurrences.append(current_index)

                        is_new_rule = True
                        for r in self.simulator.rules_sets[seq_index]:
                            if r == rule:
                                is_new_rule = False
                                r.set_last_occurence(current_index)
                                r.increment_occurrences()
                                r.occurrences.append(current_index)
                                #print("Rule already in set:", r)

                        if is_new_rule:
                            rule.set_last_occurence(current_index)
                            rule.increment_occurrences()
                            self.simulator.rules_sets[seq_index].add(rule)
                            #print("New rule:", rule)

                        generated_rules[seq_index].append(rule)

        print("==============================================")
        for seq_rules in generated_rules:
            if seq_rules:
                print(seq_rules)
                combined_rule.append(seq_rules[-1])
                for gr in seq_rules:
                    print(gr)
                print("==============================================")
        if len(combined_rule) > 0:
            print("Adding to combined rules")
            self.simulator.combined_rules.append(combined_rule)

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
                gen_rule.number_of_occurrences = rule.number_of_occurrences + new_rule.number_of_occurrences
                gen_rule.generalized = True
                return gen_rule
            else:
                return None

    def get_change_points_in_window(self, seq_index, window_begin, window_end):
        points_in_window = []
        points_before_window = []
        points_after_window = []
        for n, change_point in enumerate(self.simulator.detected_change_points[seq_index]):
            if round_to(change_point.at_, self.round_to) > window_begin:
                if round_to(change_point.at_, self.round_to) < window_end:
                    points_in_window.append(change_point)
                else:  # change point is after windows end
                    points_after_window.append(change_point)
            else:  # change point is before windows start
                points_before_window.append(change_point)
        return (points_before_window, points_in_window, points_after_window)

def round_to(x, _to):
    return int(round(x / _to)) * _to