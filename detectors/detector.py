import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict

class ChangeDetector(object):
    def __init__(self):
        self.is_change_detected = False
        self.sequence_size = 0
        self.sequence = []
        self.current_value = 0
        self.previous_value = 0

    def update(self, new_value):
        self.sequence.append(new_value)
        self.sequence_size += 1

    def check_change(self, new_value):
        pass

    def get_parameters(self):
        parameters_dict = {}
        for k, v in self.__dict__.items():
            if k.endswith('_'):
                parameters_dict[k] = v

        return parameters_dict

    def step(self, new_value):
        self.update(new_value)
        self.check_change(new_value)

        return self.get_parameters()

class OnlineSimulator(object):
    def __init__(self, change_detectors, sequences, seqs_names):
        self.sequences = sequences
        self.sequences_names = seqs_names
        self.change_detectors = change_detectors
        self.sequence_size = len(sequences[0])
        self.detected_change_points = [[] for i in range(len(self.sequences))]
        self.rules_sets = [set() for i in range(len(self.sequences))]
        self.parameters_history = [defaultdict(list) for i in range(len(self.sequences))]
        self.target_index = len(self.sequences) - 1

    def get_detected_changes(self):
        return self.detected_change_points

    def get_rules(self):
        return self.rules_sets

    def run(self, plot=True, detect_rules=True, **kwargs):
        parameters_history = [defaultdict(list) for i in range(len(self.sequences))]

        for i in range(0, self.sequence_size):
            for j, seq in enumerate(self.sequences):
                detector = self.change_detectors[j]

                value = seq[i]
                res = detector.step(value)

                for k, v in res.items():
                    #print(k, v)
                    parameters_history[j][k].append(v)

                if detector.is_change_detected is True:
                    prev_at = self.detected_change_points[j][-1].at_ if len(self.detected_change_points[j]) > 0 else 0
                    prev_value_len = i - prev_at

                    change_point = ChangePoint(detector.previous_value, detector.current_value, i, prev_value_len, self.sequences_names[j])
                    self.detected_change_points[j].append(change_point)
                    #print(change_point)

                if i == self.sequence_size - 1:
                    detector.is_change_detected = True
                    prev_at = self.detected_change_points[j][-1].at_ if len(self.detected_change_points[j]) > 0 else 0
                    prev_value_len = i - prev_at
                    change_point = ChangePoint(detector.current_value, -1, i, prev_value_len, self.sequences_names[j])
                    self.detected_change_points[j].append(change_point)
                    #print(change_point)

                # if i == 0:
                #     change_point = ChangePoint(-1, detector.curr_value, i, self.sequences_names[j])
                #     self.detected_change_points[j].append(change_point)
                #     print(self.sequences_names[j], "changed from:", change_point.prev_value, "to:", change_point.curr_value, "at: ",
                #           change_point.at_)


                if detect_rules:
                    #last seq - target
                    if j == len(self.sequences) - 1:
                        if detector.is_change_detected is True and len(self.detected_change_points[j]) > 1:
                            self.search_rules(i)


        def dict_to_arrays(ddict):
            new_dict = {}
            for k, v in ddict.items():
                new_dict[k] = np.array(v)
            return new_dict

        for i in range(0, len(self.sequences)):
            parameters_history[i] = dict_to_arrays(parameters_history[i])
            self.parameters_history[i] = parameters_history[i]

        if plot is True:
            self.display_results(**kwargs)

        return detector.is_change_detected

    def search_rules(self, current_index):
        prev_prev_change_point_target = self.detected_change_points[self.target_index][-3] if len(self.detected_change_points[self.target_index]) > 2 else None
        prev_change_point_target = self.detected_change_points[self.target_index][-2]
        window_begin = round_to_hundreds(prev_prev_change_point_target.at_) if prev_prev_change_point_target != None else 0
        window_end = round_to_hundreds(prev_change_point_target.at_)


        for m, change_point_list in enumerate(self.detected_change_points[:-1]):  # abandoning last seq, as it is target for now
            lhs = []
            points_before_window, points_in_window, points_after_window = self.get_change_points_in_window(m, window_begin, window_end)

            # no change points in window
            if len(points_in_window) == 0:
                lhs_elem = LHS_element(round_to_hundreds(window_end - window_begin),
                                       points_before_window[-1].curr_value,
                                       self.sequences_names[m])
                lhs.append(lhs_elem)

            else :
                first_point = points_in_window[0]
                skip_first_point = False
                if first_point.at_ - first_point.prev_value_len < window_begin:
                    #print("before window case")
                    lhs_elem = LHS_element(round_to_hundreds(first_point.at_ - window_begin),
                                           first_point.prev_value,
                                           first_point.attr_name)
                    lhs.append(lhs_elem)
                    skip_first_point = True

                for point in points_in_window[1:] if skip_first_point else points_in_window:
                    #print("inside window case")
                    lhs_elem = LHS_element(round_to_hundreds(point.prev_value_len),
                                           point.prev_value,
                                           point.attr_name)
                    lhs.append(lhs_elem)

                last_point = points_in_window[-1]
                if last_point.at_ < window_end:
                    #print("after window case")
                    lhs_elem = LHS_element(round_to_hundreds(window_end - last_point.at_),
                                           last_point.curr_value,
                                           last_point.attr_name)
                    lhs.append(lhs_elem)


            rhs_elem = LHS_element(round_to_hundreds(self.detected_change_points[self.target_index][-1].prev_value_len),
                                   self.detected_change_points[self.target_index][-1].prev_value,
                                   self.detected_change_points[self.target_index][-1].attr_name)
            rule = Rule(lhs, rhs_elem)

            is_new_rule = True
            for r in self.rules_sets[m]:
                if r == rule:
                    print("rule already in set")
                    is_new_rule = False
                    r.set_last_occurence(current_index)
                    r.increment_occurrences()
                    print(r)

            if is_new_rule:
                print("new rule")
                rule.set_last_occurence(current_index)
                rule.increment_occurrences()
                self.generalize_rule(m, rule)


                self.rules_sets[m].add(rule)
                print(rule)

    def display_results(self, sequence_name='Sequence', **kwargs):
        for i in range(0, len(self.sequences)):
            sequence = self.sequences[i]
            detector = self.change_detectors[i]
            parameters_history = self.parameters_history[i]
            detected_change_points = self.detected_change_points[i]

            plotcount = 1 + len(parameters_history)
            fig, axes = plt.subplots(nrows=plotcount, ncols=1, sharex=True,
                                     figsize=(12, plotcount*3))

            # Plot the sequence
            if plotcount > 1:
                ax = axes[0]
            elif plotcount == 1:
                ax = axes

            ax.plot(sequence, 'b.')
            ax.plot(sequence, 'b-', alpha=0.25)

            ax.set_title(sequence_name)

            ax.set_ylim(
                np.nanmin(sequence)*.5,
                np.nanmax(sequence)*1.5)
            ax.set_xlim(0, len(sequence))
            xl = ax.get_xticks()
            ticks = xl #- int(2/3 * len(sequence))

            ax.set_xticklabels(ticks)

            # Plot a horizontal line where the change_point is detected
            for change_point in detected_change_points:
                ax.vlines(x=change_point.at_, ymin=0, ymax=ax.get_ylim()[1],
                      colors='r', linestyles='dotted')

            # Plot each parameter
            for ii, (res_name, res_values) in enumerate(parameters_history.items()):
                ax = axes[ii+1]
                ax.plot(res_values, 'g.', alpha=0.7)
                ax.set_title("Parameter #{}: {}".format(ii+1, res_name))

                for change_poin in detected_change_points:
                    ax.vlines(x=change_poin.at_, ymin=0, ymax=ax.get_ylim()[1],
                          colors='r', linestyles='dotted')

        plt.show()

    def generalize_rule(self, seq_index, new_rule):
        print("generalization try")
        for rule in self.rules_sets[seq_index]:
            if rule.rhs == new_rule.rhs:
                for i in range(len(rule.lhs), 0):
                    if rule.lhs[i] == new_rule.lhs[i]:
                        print("lhs_elems are the same", rule.lhs[i], new_rule.lhs[i])
                    else:
                        print()

    def get_change_points_in_window(self, seq_index, window_begin, window_end):
        points_in_window = []
        points_before_window = []
        points_after_window = []
        for n, change_point in enumerate(self.detected_change_points[seq_index]):
            if round_to_hundreds(change_point.at_) > window_begin:
                if round_to_hundreds(change_point.at_) < window_end:
                    points_in_window.append(change_point)
                else: # change point is after windows end
                    points_after_window.append(change_point)
            else: # change point is before windows start
                points_before_window.append(change_point)
        return (points_before_window, points_in_window, points_after_window)

class ChangePoint(object):
    def __init__(self, from_, to_, at_, prev_value_len_, attr_name_):
        self.prev_value = from_
        self.curr_value = to_
        self.at_ = at_
        self.prev_value_len = prev_value_len_
        self.attr_name = attr_name_

    def __repr__(self):
        return("(" + self.attr_name + " changed from:" + str(self.prev_value) + "(len= " + str(self.prev_value_len) + ") to:" + str(self.curr_value) + " at: " + str(self.at_) + ")")

class LHS_element(object):
    def __init__(self, len_, value_, attr_name_):
        self.len = len_
        self.value = value_
        self.attr_name_ = attr_name_

    def __repr__(self):
        return(str(self.attr_name_) + ": " + str(self.value) + "{"+ str(self.len) + "}" )

    def __eq__(self, other):
        if isinstance(other, LHS_element):
            return ((self.len == other.len) and (self.value == other.value) and (self.attr_name_ == other.attr_name_))
        else:
            return False

    def __ne__(self, other):
        return (not self.__eq__(other))

    def __hash__(self):
        return hash(self.__repr__())


class Rule(object):
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs
        self.number_of_occurrences = 0
        self.last_occurrence = -1


    def __repr__(self):
        return(str(self.lhs) + " ==> " + str(self.rhs) + " | nr_of_occurences:" + str(self.number_of_occurrences) + " last_occurence:" + str(self.last_occurrence))
        #  + "nr:" + str(self.number_of_occurrences) + " lastOcc:" + str(self.last_occurrence)

    def __eq__(self, other):
        if isinstance(other, Rule):
            return ((self.lhs == other.lhs) and (self.rhs == other.rhs))
        else:
            return False

    def __ne__(self, other):
        return (not self.__eq__(other))

    def __hash__(self):
        return hash(str(self.lhs) + " ==> " + str(self.rhs))

    def increment_occurrences(self):
        self.number_of_occurrences += 1

    def set_last_occurence(self, last):
        self.last_occurrence = last

def round_to_hundreds(x):
    return int(round(x / 100.0)) * 100