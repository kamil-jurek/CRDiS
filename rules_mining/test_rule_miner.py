from rules_miner import RulesMiner


sequences = [
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        #[2, 2, 2, 3, 3, 3, 2, 2, 2, 4, 4, 4, 5, 5, 5, 5]
        #['a','b','c','d','e','f']
    ]

max_window_size = 8
min_sup = 1
gcd = 10

rules_miner = RulesMiner(sequences, min_sup, max_window_size)
rules_miner.prefix_span()
rules = rules_miner.getRules()
#[print(r) for r in rules]
rules_miner.print_rules()
