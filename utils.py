import math

def print_rules(rules_sets,support):
    print("---------------------------------------------------------------------------------------")
    for rules_set in rules_sets:
        #for rule in sorted(rules_set, key=lambda x: (x.number_of_occurrences, len(x.lhs), x.rhs.len, x.lhs[0].len), reverse=True):
        for rule in sorted(rules_set, key=lambda r: (r.get_rule_score()),reverse=True):
            if rule.number_of_occurrences >= support:
                print(rule)
                print("----------------------------------------------------------------------------------------")
        print("----------------------------------------------------------------------------------------")
    print()

def print_combined_rules(combined_rules, support):
    print("---------------------------------------------------------------------------------------")
    for combined_rule in sorted(combined_rules, key=lambda x: min(x[i].number_of_occurrences for i in range(len(x))), reverse=True):
        # print(combined_rule)
        nr_of_occu = min([combined_rule[i].number_of_occurrences for i in range(len(combined_rule))])
        if nr_of_occu >= support:
            for i, rule in enumerate(combined_rule):
                print(rule.lhs, rule.number_of_occurrences, rule.last_occurrence, rule.occurrences, "AND" if i < len(combined_rule)-1 else "")
            print(" ==>", )
            print(combined_rule[0].rhs)
            print("number of occurenes:", nr_of_occu)
            print("---------------------------------------------------------------------------------------")

def print_detected_change_points(detected_changes):
    print("---------------------------------------------------------------------------------------")
    for attr_detected_change in detected_changes:
        for point in attr_detected_change:
            print(point)
        print("---------------------------------------------------------------------------------------")
