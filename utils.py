def print_rules(rules_sets):
    print("---------------------------------------------------------------------------------------")
    for rules_set in rules_sets:
        for rule in sorted(rules_set, key=lambda x: x.number_of_occurrences, reverse=True):
            print(rule)
        print("----------------------------------------------------------------------------------------")
    print()

def print_combined_rules(combined_rules):
    print("---------------------------------------------------------------------------------------")
    for combined_rule in combined_rules:
        # print(combined_rule)
        for i, rule in enumerate(combined_rule):
            print(rule.lhs, "AND" if i < len(combined_rule)-1 else "")
        print(" ==>", )
        print(combined_rule[0].rhs)
        print()