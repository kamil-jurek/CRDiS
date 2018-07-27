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

import math
import numpy as np
import pandas as pd

def round_to(x, _round_to):
    return int(round(x / _round_to)) * _round_to

def print_separator():
    print("-----------------------------------------------------------------------------------------------------------")

def print_rules(rules_sets, support):
    print_separator()
    for rules_set in rules_sets:
        #for rule in sorted(rules_set, key=lambda x: (x.number_of_occurrences, len(x.lhs), x.rhs.len, x.lhs[0].len), reverse=True):
        for rule in sorted(rules_set, key=lambda r: (r.get_rule_score()),reverse=True):
            if rule.rule_support >= support:
                print(rule)
                print_separator()
        print_separator()
    print()

def print_best_rules(rules_sets):
    print_separator()
    for rules_set in rules_sets:
        best_rule = sorted(rules_set, key=lambda r: (r.get_rule_score()), reverse=True)[0]
        print(best_rule)
        print_separator()
    print()

def print_combined_rules(combined_rules, support):
    print_separator()
    for combined_rule in sorted(combined_rules, key=lambda x: min(x[i].rule_support for i in range(len(x))), reverse=True):
        # print(combined_rule)
        nr_of_occu = min([combined_rule[i].rule_support for i in range(len(combined_rule))])
        if nr_of_occu >= support:
            for i, rule in enumerate(combined_rule[:-1]):
                print(rule.lhs, "{supp:", rule.rule_support, "conf:", rule.get_confidence(), "} AND" if i < len(combined_rule)-1 else "}")
            print(" ==>", )
            print(combined_rule[0].rhs)
            print("number of occurenes:", nr_of_occu)
            print_separator()

def print_detected_change_points(detected_changes):
    print_separator()
    for attr_detected_change in detected_changes:
        for point in attr_detected_change:
            print(point)
        print_separator()


def evaluate_change_detectors(simulator, actual_change_points):
    for k in range(len(simulator.sequences)):
        detected_change_points = np.array(simulator.get_detected_changes())[k]
        detected_change_points = [x.at_ for x in detected_change_points]
        actual_change_points2 = list(actual_change_points)
        

        print("actual:",actual_change_points)
        print("detect:",detected_change_points)
        if len(detected_change_points) < len(actual_change_points):
            for i in range(len(actual_change_points)):
                if np.abs(detected_change_points[i] - actual_change_points[i]) > 305:
                    detected_change_points.insert(i, 0)
            actual_change_points2 = np.array(actual_change_points)
        
        elif len(detected_change_points) > len(actual_change_points):
            for i in range(len(detected_change_points)):
                if np.abs(detected_change_points[i] - actual_change_points2[i]) > 205:
                    actual_change_points2.insert(i, 0)
            actual_change_points2 = np.array(actual_change_points2)
        else:
            actual_change_points2 = np.array(actual_change_points)
        #actual_change_points2 = np.array(actual_change_points)
        print("====== ", simulator.sequences_names[k], " ===============================")
        print("Actual change points:   ", list(actual_change_points2))
        print("Detected change points: ", detected_change_points)

        delta = np.abs(actual_change_points2 - detected_change_points)

        print("Difference: ", delta)
        print("Errors sum: ", np.sum(delta))
        print("Errors avg: ", np.sum(delta) / len(detected_change_points))

        rmse = np.sqrt(((detected_change_points - actual_change_points2) ** 2).mean())
        print('Mean Squared Error: {}'.format(round(rmse, 5)))
        print("==============================================================================")

def generate_classical_dataset(detected_changes, discretization_step=100, save_csv=False):
    classical = [[] for i in range(len(detected_changes))]
    for j, seq_changes in enumerate(detected_changes):
        for point in seq_changes:
            for i in range(round_to(point.at_ - point.prev_value_len, discretization_step), round_to(point.at_ - discretization_step, discretization_step), discretization_step):
                classical[j].append(
                    str(str(point.attr_name) + ":" + str(point.prev_value) + "->" + str(point.prev_value)))
                print(point.attr_name, ":", point.prev_value, "->", point.prev_value)
            classical[j].append(str(str(point.attr_name) + ":" + str(point.prev_value) + "->" + str(point.curr_value)))
            print(point.attr_name, ":", point.prev_value, "->", point.curr_value)

    df = pd.DataFrame()
    df['attr_1'] = classical[0][1:-2]
    df['attr_2'] = classical[1][1:-2]
    df['attr_3'] = classical[2][1:-2]
    df['attr_4'] = classical[3][1:-2]

    if save_csv:
        df.to_csv('calssical_dataset.csv', sep=',')
    print(df)

def generate_discretized_sequence(change_points):
    sequences = [[] for i in range(len(change_points))]
    for k, attr_p in enumerate(change_points):
        attr_p = attr_p[1:]
        attr_name = attr_p[0].attr_name
        for i, p in enumerate(attr_p):
            prev = round_to(attr_p[i-1].at_,100) if i > 0 else 0

            if i < len(attr_p)-1:
                for j in range(prev, round_to(p.at_,100), 100):
                    elem = attr_name + ":" + str(p.prev_value)
                    sequences[k].append(elem)
    return sequences