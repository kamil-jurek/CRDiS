from detectors import detector
from change_point import ChangePoint
from lhs_element import LHS_element
from rule import Rule
from online_simulator import OnlineSimulator

class RulesDetector(object):
    def __init__(self, target_seq_index,round_to=100):
        self.target_seq_index = target_seq_index
        self.round_to = round_to

    def set_online_simulator(self, sim):
        self.simulator = sim

    def search_rules(self, seq_index, current_index):
        if (seq_index == self.target_seq_index and
            self.simulator.change_detectors[seq_index].is_change_detected is True and
            len(self.simulator.detected_change_points[seq_index]) > 1):

            prev_prev_change_point_target = self.simulator.detected_change_points[self.target_seq_index][-3] if len(self.simulator.detected_change_points[self.target_seq_index]) > 2 else None
            prev_change_point_target = self.simulator.detected_change_points[self.target_seq_index][-2]
            window_begin = round_to(prev_prev_change_point_target.at_, self.round_to) if prev_prev_change_point_target != None else 0
            window_end = round_to(prev_change_point_target.at_, self.round_to)

            combined_rule = []
            for m, change_point_list in enumerate(self.simulator.detected_change_points):
                if m == self.target_seq_index:
                    continue

                lhs = []
                points_before_window, points_in_window, points_after_window = self.get_change_points_in_window(m, window_begin, window_end)

                # no change points in window
                if len(points_in_window) == 0:
                    # print("no change points in window")
                    if round_to(window_end - window_begin, self.round_to):
                        lhs_elem = LHS_element(round_to(window_end - window_begin, self.round_to),
                                               points_before_window[-1].curr_value if len(points_before_window) > 0 else -1,
                                               self.simulator.sequences_names[m])
                        lhs.append(lhs_elem)

                else :
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


                rhs_elem = LHS_element(round_to(self.simulator.detected_change_points[self.target_seq_index][-1].prev_value_len, self.round_to),
                                       self.simulator.detected_change_points[self.target_seq_index][-1].prev_value,
                                       self.simulator.detected_change_points[self.target_seq_index][-1].attr_name)

                if len(lhs) > 0:
                    rule = Rule(lhs, rhs_elem)

                    is_new_rule = True
                    for r in self.simulator.rules_sets[m]:
                        if r == rule:
                            is_new_rule = False
                            r.set_last_occurence(current_index)
                            r.increment_occurrences()
                            combined_rule.append(rule)
                            print("Rule already in set:", r)

                    if is_new_rule:
                        rule.set_last_occurence(current_index)
                        rule.increment_occurrences()
                        gen_rule = self.generalize_rule(m, rule)
                        if gen_rule != None:
                            gen_rule.set_last_occurence(current_index)
                            # self.simulator.rules_sets[m].add(gen_rule)

                        self.simulator.rules_sets[m].add(rule)
                        combined_rule.append(rule)
                        print("New rule:", rule)

            if len(combined_rule) > 0:
                print("Adding to combined rules")
                self.simulator.combined_rules.append(combined_rule)

    def generalize_rule(self, seq_index, new_rule):
        for rule in self.simulator.rules_sets[seq_index]:
            # print("rule:     ", rule)
            # print("new rule: ", new_rule)
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

            if len(gen_rule.lhs) > 0 and gen_rule.rhs != None:
                print("gen_rule:", gen_rule)
                gen_rule.number_of_occurrences = rule.number_of_occurrences + new_rule.number_of_occurrences
                gen_rule.generalized = True
                return gen_rule
            else:
                return None

    def generalize_lhs(self, rule, new_rule):
        print("rule:     ", rule)
        print("new rule: ", new_rule)
        for i in range(1, max(len(rule.lhs)+1, len(new_rule.lhs)+1)):
            print("i:", i)
            if i <= len(rule.lhs) and i <= len(new_rule.lhs):
                if rule.lhs[-i] == new_rule.lhs[-i]:
                    print("lhs_elem are the same, i:", -i, rule.lhs[-i], new_rule.lhs[-i])

                else:
                    print("lhs_elem are different, i:", -i, rule.lhs[-i], new_rule.lhs[-i])
                    break
            else:
                print("i is greater")
                if i > len(rule.lhs):
                    print("for rule     -- new_rule is longer, adding it, and increasining rule occ")
                    rule.increment_occurrences()

                if i > len(new_rule.lhs):
                    print("for new rule -- rule is longer")

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