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

            generated_rules = set()
            prev_prev_change_point_target = self.simulator.detected_change_points[self.target_seq_index][-3] if len(self.simulator.detected_change_points[self.target_seq_index]) > 2 else None
            prev_change_point_target = self.simulator.detected_change_points[self.target_seq_index][-2]
            window_begin = round_to(prev_prev_change_point_target.at_, self.round_to) if prev_prev_change_point_target != None else 0
            window_end = round_to(prev_change_point_target.at_, self.round_to)

            for m, change_point_list in enumerate(self.simulator.detected_change_points):
                if m == self.target_seq_index:
                    continue

                lhss = []
                rhss = []
                points_before_window, points_in_window, points_after_window = self.get_change_points_in_window(m, window_begin, window_end)

                # no change points in window
                if len(points_in_window) == 0:
                    # print("no change points in window")
                    if round_to(window_end - window_begin, self.round_to):
                        lhs_elem_len = round_to(window_end - window_begin, self.round_to)
                        for lhs_len in range(self.round_to, lhs_elem_len, self.round_to):
                            lhs_elem = LHS_element(lhs_len,
                                                   points_before_window[-1].curr_value if len(points_before_window) > 0 else -1,
                                                   self.simulator.sequences_names[m])
                            lhss.append([lhs_elem])
                else :
                    last_point = points_in_window[-1]
                    if last_point.at_ < window_end:
                        # print("after window case")
                        lhs_elem_len = round_to(window_end - last_point.at_, self.round_to)
                        for lhs_len in range(self.round_to, lhs_elem_len+1, self.round_to):
                            lhs_elem = LHS_element(lhs_len,
                                                   last_point.curr_value,
                                                   last_point.attr_name)
                            lhss.append([lhs_elem])

                    for point_index in range(1, len(points_in_window)+1):
                        # print("inside window case")
                        prefix = lhss[-1]
                        # print("prefix:", prefix)
                        point = points_in_window[-point_index]
                        if round_to(point.prev_value_len, self.round_to) > 0:
                            lhs_elem_len = point.prev_value_len
                            for lhs_len in range(self.round_to, lhs_elem_len + 1, self.round_to):
                                lhs_elem = LHS_element(lhs_len,
                                                       point.prev_value,
                                                       point.attr_name)
                                lhss.append([lhs_elem]+prefix)

                last_target_change_point = self.simulator.detected_change_points[self.target_seq_index][-1]
                rhs_elem_len = round_to(last_target_change_point.prev_value_len, self.round_to)
                for rhs_len in range(self.round_to, rhs_elem_len+1, self.round_to):
                    rhs_elem = LHS_element(rhs_len,
                                          last_target_change_point.prev_value,
                                          last_target_change_point.attr_name)
                    rhss.append(rhs_elem)

                if len(lhss) > 0:
                    for rhs in rhss:
                        for lhs in lhss:
                            rule = Rule(lhs, rhs)
                            generated_rules.add(rule)

                            is_new_rule = True
                            for r in self.simulator.rules_sets[m]:
                                if r == rule:
                                    is_new_rule = False
                                    r.set_last_occurence(current_index)
                                    r.increment_occurrences()
                                    # print("Rule already in set:", r)

                            if is_new_rule:
                                rule.set_last_occurence(current_index)
                                rule.increment_occurrences()
                                self.simulator.rules_sets[m].add(rule)
                                # print("New rule:", rule)
            print("==============================================")
            for gr in generated_rules:
                print(gr)
            print("==============================================")

    def generalize_rule(self, seq_index, new_rule):
        #print()
        #print("generalization try")
        for rule in self.simulator.rules_sets[seq_index]:
            #print("rule:     ", rule)
            #print("new rule: ", new_rule)
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

            # if (rule.rhs.attr_name_ == new_rule.rhs.attr_name_ and
            #     rule.rhs.value == new_rule.rhs.value):
            #     gen_rule = Rule([], None)
            #     print("same rhs")
            #     if new_rule.rhs.len < rule.rhs.len: # new_rule is shorter / less specific, is part of rule
            #         print("new rule rhs shorter than rule")
            #         gen_rule.rhs = new_rule.rhs
            #         ##
            #         for i in range(1, max(len(rule.lhs) + 1, len(new_rule.lhs) + 1)):
            #             if i <= len(rule.lhs) and i <= len(new_rule.lhs):
            #                 if (rule.lhs[-i].attr_name_ == new_rule.lhs[-i].attr_name_ and
            #                         rule.lhs[-i].value == new_rule.lhs[-i].value):
            #                     print("lhs_elem are the same, i:", -i, rule.lhs[-i], new_rule.lhs[-i])
            #                     if new_rule.lhs[-i].len == rule.lhs[-i].len:
            #                         gen_rule.lhs.insert(0, new_rule.lhs[-i])
            #
            #                     elif new_rule.lhs[-i].len > rule.lhs[-i].len:  # new rule lhs_elem is longer, rule is part of it
            #                         gen_rule.lhs.insert(0, new_rule.lhs[-i])
            #                         rule.increment_occurrences()
            #                         break
            #                     else:
            #                         gen_rule.lhs.insert(0, new_rule.lhs[-i])  # new_rule lhs_elem is shorter, is part of rule
            #                         gen_rule.number_of_occurrences = rule.number_of_occurrences
            #                         break
            #
            #                 else:
            #                     print("lhs_elem are different, i:", -i, rule.lhs[-i], new_rule.lhs[-i])
            #                     if i == 1:
            #                         print("first lhs different not possible to generalize")
            #                     else:
            #                         print("")
            #                     break
            #             else:
            #                 print("i is greater")
            #                 if i > len(rule.lhs):
            #                     print("for rule     -- new_rule is longer, adding it, and increasining rule occ")
            #                     gen_rule.lhs.insert(0, new_rule.lhs[-i])
            #                     rule.increment_occurrences()
            #
            #                 if i > len(new_rule.lhs):
            #                     print("for new rule -- rule is longer")
            #                     gen_rule.lhs.insert(0, rule.lhs[-i])
            #         ##
            #         gen_rule.number_of_occurrences = rule.number_of_occurrences
            #
            #     elif new_rule.rhs.len > rule.rhs.len: # new_rule is longer / more specific, rule is part of it
            #         print("new rule rhs longer than rule")
            #         gen_rule.rhs = new_rule.rhs
            #         rule.increment_occurrences()
            #
            #     else:
            #         print("new rule rhs same size") #no need to change
            #         gen_rule.rhs = new_rule.rhs
            #         #self.generalize_lhs(rule, new_rule)




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