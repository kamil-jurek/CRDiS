from rules_miner import RulesMiner


# sequences = [
#         [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
#         [2, 2, 2, 3, 3, 3, 2, 2, 2, 4, 4, 4, 5, 5, 5, 5]
#         #['a','b','c','d','e','f'],
#     ]

# sequences = [['attr_1:2', 'attr_1:2', 'attr_1:2', 'attr_1:3', 'attr_1:3', 'attr_1:3', 'attr_1:1', 'attr_1:1', 'target'],
#            ['attr_2:4', 'attr_2:4', 'attr_2:4', 'attr_2:4', 'attr_2:4', 'attr_2:5', 'attr_2:5', 'attr_2:1', 'target'],
#            ['attr_2:1', 'attr_2:4', 'attr_2:4', 'attr_2:4', 'attr_2:5', 'attr_2:5', 'attr_2:5', 'attr_2:1', 'target'],
#            ['attr_3:1', 'attr_3:1', 'attr_3:1', 'attr_3:1', 'attr_3:1', 'attr_3:1', 'attr_3:1', 'attr_3:4', 'target'],
#            #['attr_1:1', 'attr_1:2', 'attr_1:2', 'attr_1:3', 'attr_1:3', 'attr_1:3', 'attr_1:3', 'attr_1:3', 'target'],
#            ]

sequences = [['attr_1(1->2)', 'attr_1(2->3)', 'attr_1(3->4)']
    # ['attr_1:2.0', 'attr_1:2.0', 'attr_1:2.0', 'attr_1:3.0', 'attr_1:3.0', 'attr_1:3.0', 'attr_1:4.0', 'attr_1:4.0', 'attr_4:6.0', 'attr_4:6.0', 'attr_4:6.0', 'attr_4:6.0'],
    # ['attr_2:4.0', 'attr_2:4.0', 'attr_2:4.0', 'attr_2:4.0', 'attr_2:4.0', 'attr_2:5.0', 'attr_2:5.0', 'attr_2:1.0', 'attr_4:6.0', 'attr_4:6.0', 'attr_4:6.0', 'attr_4:6.0'],
    # ['attr_3:1.0', 'attr_3:1.0', 'attr_3:1.0', 'attr_3:1.0', 'attr_3:1.0', 'attr_3:1.0', 'attr_3:1.0', 'attr_3:4.0', 'attr_4:6.0', 'attr_4:6.0', 'attr_4:6.0', 'attr_4:6.0'],
    # ['attr_1:4.0', 'attr_1:4.0', 'attr_1:4.0', 'attr_1:4.0', 'attr_4:4.0', 'attr_4:4.0', 'attr_4:4.0'],
    # ['attr_2:1.0', 'attr_2:1.0', 'attr_2:1.0', 'attr_2:1.0', 'attr_4:4.0', 'attr_4:4.0', 'attr_4:4.0'],
    # ['attr_3:4.0', 'attr_3:4.0', 'attr_3:4.0', 'attr_3:4.0', 'attr_4:4.0', 'attr_4:4.0', 'attr_4:4.0'],
    # ['attr_1:2.0', 'attr_1:2.0', 'attr_1:4.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0'],
    # ['attr_2:1.0', 'attr_2:1.0', 'attr_2:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0'],
    # ['attr_3:2.0', 'attr_3:2.0', 'attr_3:2.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0'],
    # ['attr_1:2.0', 'attr_1:2.0', 'attr_1:2.0', 'attr_1:3.0', 'attr_1:3.0', 'attr_1:3.0', 'attr_1:4.0', 'attr_1:4.0', 'attr_4:6.0', 'attr_4:6.0', 'attr_4:6.0', 'attr_4:6.0', 'attr_4:6.0', 'attr_4:6.0', 'attr_4:6.0'],
    # ['attr_2:4.0', 'attr_2:4.0', 'attr_2:4.0', 'attr_2:4.0', 'attr_2:4.0', 'attr_2:5.0', 'attr_2:5.0', 'attr_2:1.0', 'attr_4:6.0', 'attr_4:6.0', 'attr_4:6.0', 'attr_4:6.0', 'attr_4:6.0', 'attr_4:6.0', 'attr_4:6.0'],
    # ['attr_3:1.0', 'attr_3:1.0', 'attr_3:1.0', 'attr_3:1.0', 'attr_3:1.0', 'attr_3:1.0', 'attr_3:1.0', 'attr_3:4.0', 'attr_4:6.0', 'attr_4:6.0', 'attr_4:6.0', 'attr_4:6.0', 'attr_4:6.0', 'attr_4:6.0', 'attr_4:6.0'],
    # ['attr_1:4.0', 'attr_1:4.0', 'attr_1:4.0', 'attr_1:4.0', 'attr_1:3.0', 'attr_1:3.0', 'attr_1:3.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0'],
    # ['attr_2:1.0', 'attr_2:1.0', 'attr_2:1.0', 'attr_2:1.0', 'attr_2:1.0', 'attr_2:2.0', 'attr_2:2.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0'],
    # ['attr_3:4.0', 'attr_3:4.0', 'attr_3:4.0', 'attr_3:2.0', 'attr_3:2.0', 'attr_3:2.0', 'attr_3:2.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0'],
    # ['attr_1:2.0', 'attr_1:2.0', 'attr_1:2.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0'],
    # ['attr_2:4.0', 'attr_2:4.0', 'attr_2:4.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0'],
    # ['attr_3:1.0', 'attr_3:1.0', 'attr_3:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0'],
    # ['attr_1:3.0', 'attr_1:3.0', 'attr_1:3.0', 'attr_1:4.0', 'attr_1:4.0', 'attr_4:6.0', 'attr_4:6.0', 'attr_4:6.0', 'attr_4:6.0'],
    # ['attr_2:4.0', 'attr_2:4.0', 'attr_2:5.0', 'attr_2:5.0', 'attr_2:1.0', 'attr_4:6.0', 'attr_4:6.0', 'attr_4:6.0', 'attr_4:6.0'],
    # ['attr_3:1.0', 'attr_3:1.0', 'attr_3:1.0', 'attr_3:1.0', 'attr_3:4.0', 'attr_4:6.0', 'attr_4:6.0', 'attr_4:6.0', 'attr_4:6.0'],
    # ['attr_1:4.0', 'attr_1:4.0', 'attr_1:4.0', 'attr_1:4.0', 'attr_4:3.0'],
    # ['attr_2:1.0', 'attr_2:1.0', 'attr_2:1.0', 'attr_2:1.0', 'attr_4:3.0'],
    # ['attr_3:4.0', 'attr_3:4.0', 'attr_3:4.0', 'attr_3:4.0', 'attr_4:3.0'],
    # ['attr_1:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0'],
    # ['attr_2:3.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0'],
    # ['attr_3:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0'],
    # ['attr_1:2.0', 'attr_1:2.0', 'attr_1:2.0', 'attr_1:3.0', 'attr_1:3.0', 'attr_1:3.0', 'attr_1:4.0', 'attr_1:4.0', 'attr_4:6.0', 'attr_4:6.0', 'attr_4:6.0', 'attr_4:6.0'],
    # ['attr_2:4.0', 'attr_2:4.0', 'attr_2:4.0', 'attr_2:4.0', 'attr_2:4.0', 'attr_2:5.0', 'attr_2:5.0', 'attr_2:1.0', 'attr_4:6.0', 'attr_4:6.0', 'attr_4:6.0', 'attr_4:6.0'],
    # ['attr_3:1.0', 'attr_3:1.0', 'attr_3:1.0', 'attr_3:1.0', 'attr_3:1.0', 'attr_3:1.0', 'attr_3:1.0', 'attr_3:4.0', 'attr_4:6.0', 'attr_4:6.0', 'attr_4:6.0', 'attr_4:6.0'],
    # ['attr_1:4.0', 'attr_1:4.0', 'attr_1:4.0', 'attr_1:4.0', 'attr_4:2.0', 'attr_4:2.0', 'attr_4:2.0'],
    # ['attr_2:1.0', 'attr_2:1.0', 'attr_2:1.0', 'attr_2:1.0', 'attr_4:2.0', 'attr_4:2.0', 'attr_4:2.0'],
    # ['attr_3:4.0', 'attr_3:4.0', 'attr_3:1.0', 'attr_3:1.0', 'attr_4:2.0', 'attr_4:2.0', 'attr_4:2.0'],
    # ['attr_1:4.0', 'attr_1:4.0', 'attr_1:2.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0'],
    # ['attr_2:5.0', 'attr_2:5.0', 'attr_2:4.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0'],
    # ['attr_3:4.0', 'attr_3:4.0', 'attr_3:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0'],
    # ['attr_1:2.0', 'attr_1:2.0', 'attr_1:3.0', 'attr_1:3.0', 'attr_1:3.0', 'attr_1:4.0', 'attr_1:4.0', 'attr_4:6.0', 'attr_4:6.0', 'attr_4:6.0', 'attr_4:6.0'],
    # ['attr_2:4.0', 'attr_2:4.0', 'attr_2:4.0', 'attr_2:4.0', 'attr_2:5.0', 'attr_2:5.0', 'attr_2:1.0', 'attr_4:6.0', 'attr_4:6.0', 'attr_4:6.0', 'attr_4:6.0'],
    # ['attr_3:1.0', 'attr_3:1.0', 'attr_3:1.0', 'attr_3:1.0', 'attr_3:1.0', 'attr_3:1.0', 'attr_3:4.0', 'attr_4:6.0', 'attr_4:6.0', 'attr_4:6.0', 'attr_4:6.0'],
    # ['attr_1:4.0', 'attr_1:4.0', 'attr_1:4.0', 'attr_1:4.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0'],
    # ['attr_2:1.0', 'attr_2:4.0', 'attr_2:4.0', 'attr_2:4.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0'],
    # ['attr_3:4.0', 'attr_3:4.0', 'attr_3:4.0', 'attr_3:4.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0'],
    # ['attr_1:3.0', 'attr_1:3.0', 'attr_1:3.0', 'attr_1:2.0', 'attr_1:2.0', 'attr_1:2.0', 'attr_1:3.0', 'attr_1:3.0', 'attr_1:3.0', 'attr_1:4.0', 'attr_1:4.0', 'attr_4:6.0', 'attr_4:6.0', 'attr_4:6.0', 'attr_4:6.0'],
    # ['attr_2:3.0', 'attr_2:3.0', 'attr_2:3.0', 'attr_2:4.0', 'attr_2:4.0', 'attr_2:4.0', 'attr_2:4.0', 'attr_2:4.0', 'attr_2:5.0', 'attr_2:5.0', 'attr_2:1.0', 'attr_4:6.0', 'attr_4:6.0', 'attr_4:6.0', 'attr_4:6.0'],
    # ['attr_3:2.0', 'attr_3:2.0', 'attr_3:2.0', 'attr_3:1.0', 'attr_3:1.0', 'attr_3:1.0', 'attr_3:1.0', 'attr_3:1.0', 'attr_3:1.0', 'attr_3:1.0', 'attr_3:4.0', 'attr_4:6.0', 'attr_4:6.0', 'attr_4:6.0', 'attr_4:6.0'],
    # ['attr_1:4.0', 'attr_1:4.0', 'attr_1:4.0', 'attr_1:4.0', 'attr_4:3.0', 'attr_4:3.0'],
    # ['attr_2:1.0', 'attr_2:1.0', 'attr_2:1.0', 'attr_2:1.0', 'attr_4:3.0', 'attr_4:3.0'],
    # ['attr_3:4.0', 'attr_3:4.0', 'attr_3:4.0', 'attr_3:4.0', 'attr_4:3.0', 'attr_4:3.0'],
    # ['attr_1:3.0', 'attr_1:3.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0'],
    # ['attr_2:5.0', 'attr_2:5.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0'],
    # ['attr_3:4.0', 'attr_3:4.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0'],
    # ['attr_1:2.0', 'attr_1:2.0', 'attr_1:2.0', 'attr_1:3.0', 'attr_1:3.0', 'attr_1:3.0', 'attr_1:4.0', 'attr_1:4.0', 'attr_4:6.0', 'attr_4:6.0', 'attr_4:6.0', 'attr_4:6.0', 'attr_4:6.0', 'attr_4:6.0'],
    # ['attr_2:4.0', 'attr_2:4.0', 'attr_2:4.0', 'attr_2:4.0', 'attr_2:4.0', 'attr_2:5.0', 'attr_2:5.0', 'attr_2:1.0', 'attr_4:6.0', 'attr_4:6.0', 'attr_4:6.0', 'attr_4:6.0', 'attr_4:6.0', 'attr_4:6.0'],
    # ['attr_3:1.0', 'attr_3:1.0', 'attr_3:1.0', 'attr_3:1.0', 'attr_3:1.0', 'attr_3:1.0', 'attr_3:1.0', 'attr_3:4.0', 'attr_4:6.0', 'attr_4:6.0', 'attr_4:6.0', 'attr_4:6.0', 'attr_4:6.0', 'attr_4:6.0'],
    # ['attr_1:4.0', 'attr_1:4.0', 'attr_1:4.0', 'attr_1:4.0', 'attr_1:2.0', 'attr_1:2.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0'],
    # ['attr_2:1.0', 'attr_2:1.0', 'attr_2:1.0', 'attr_2:1.0', 'attr_2:4.0', 'attr_2:4.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0'],
    # ['attr_3:4.0', 'attr_3:4.0', 'attr_3:4.0', 'attr_3:4.0', 'attr_3:5.0', 'attr_3:5.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0'],
    # ['attr_1:2.0', 'attr_1:2.0', 'attr_1:2.0', 'attr_1:3.0', 'attr_1:3.0', 'attr_1:3.0', 'attr_1:4.0', 'attr_1:4.0', 'attr_4:6.0', 'attr_4:6.0', 'attr_4:6.0', 'attr_4:6.0'],
    # ['attr_2:4.0', 'attr_2:4.0', 'attr_2:4.0', 'attr_2:4.0', 'attr_2:4.0', 'attr_2:5.0', 'attr_2:5.0', 'attr_2:1.0', 'attr_4:6.0', 'attr_4:6.0', 'attr_4:6.0', 'attr_4:6.0'],
    # ['attr_3:1.0', 'attr_3:1.0', 'attr_3:1.0', 'attr_3:1.0', 'attr_3:1.0', 'attr_3:1.0', 'attr_3:1.0', 'attr_3:4.0', 'attr_4:6.0', 'attr_4:6.0', 'attr_4:6.0', 'attr_4:6.0'],
    # ['attr_1:4.0', 'attr_1:4.0', 'attr_1:4.0', 'attr_1:4.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0'],
    # ['attr_2:1.0', 'attr_2:1.0', 'attr_2:1.0', 'attr_2:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0'],
    # ['attr_3:4.0', 'attr_3:4.0', 'attr_3:4.0', 'attr_3:4.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0'],
    # ['attr_1:3.0', 'attr_1:3.0', 'attr_1:3.0', 'attr_1:2.0', 'attr_1:2.0', 'attr_1:2.0', 'attr_1:3.0', 'attr_1:3.0', 'attr_1:3.0', 'attr_1:4.0', 'attr_1:4.0', 'attr_4:6.0', 'attr_4:6.0', 'attr_4:6.0', 'attr_4:6.0'],
    # ['attr_2:3.0', 'attr_2:3.0', 'attr_2:3.0', 'attr_2:4.0', 'attr_2:4.0', 'attr_2:4.0', 'attr_2:4.0', 'attr_2:4.0', 'attr_2:5.0', 'attr_2:5.0', 'attr_2:1.0', 'attr_4:6.0', 'attr_4:6.0', 'attr_4:6.0', 'attr_4:6.0'],
    # ['attr_3:1.0', 'attr_3:1.0', 'attr_3:1.0', 'attr_3:1.0', 'attr_3:1.0', 'attr_3:1.0', 'attr_3:1.0', 'attr_3:1.0', 'attr_3:1.0', 'attr_3:1.0', 'attr_3:4.0', 'attr_4:6.0', 'attr_4:6.0', 'attr_4:6.0', 'attr_4:6.0'],
    # ['attr_1:4.0', 'attr_1:4.0', 'attr_1:4.0', 'attr_1:4.0', 'attr_4:2.0', 'attr_4:2.0'],
    # ['attr_2:1.0', 'attr_2:1.0', 'attr_2:1.0', 'attr_2:1.0', 'attr_4:2.0', 'attr_4:2.0'],
    # ['attr_3:4.0', 'attr_3:4.0', 'attr_3:4.0', 'attr_3:4.0', 'attr_4:2.0', 'attr_4:2.0'],
    # ['attr_1:4.0', 'attr_1:4.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0'],
    # ['attr_2:4.0', 'attr_2:4.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0'],
    # ['attr_3:1.0', 'attr_3:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0', 'attr_4:1.0'],
    # ['attr_1:2.0', 'attr_1:2.0', 'attr_1:2.0', 'attr_1:3.0', 'attr_1:3.0', 'attr_1:3.0', 'attr_1:4.0', 'attr_1:4.0', 'attr_4:6.0', 'attr_4:6.0', 'attr_4:6.0', 'attr_4:6.0'],
    # ['attr_2:4.0', 'attr_2:4.0', 'attr_2:4.0', 'attr_2:4.0', 'attr_2:4.0', 'attr_2:5.0', 'attr_2:5.0', 'attr_2:1.0', 'attr_4:6.0', 'attr_4:6.0', 'attr_4:6.0', 'attr_4:6.0'],
    # ['attr_3:1.0', 'attr_3:1.0', 'attr_3:1.0', 'attr_3:1.0', 'attr_3:1.0', 'attr_3:1.0', 'attr_3:1.0', 'attr_3:4.0', 'attr_4:6.0', 'attr_4:6.0', 'attr_4:6.0', 'attr_4:6.0'],
    # ['attr_1:4.0', 'attr_1:4.0', 'attr_1:1.0', 'attr_1:1.0', 'attr_4:5.0'],
    # ['attr_2:1.0', 'attr_2:1.0', 'attr_2:1.0', 'attr_2:1.0', 'attr_4:5.0'],
    # ['attr_3:4.0', 'attr_3:4.0', 'attr_3:4.0', 'attr_3:4.0', 'attr_4:5.0']
]

max_window_size = 50
min_sup = 0
gcd = 100

rules_miner = RulesMiner(sequences, min_sup, max_window_size)
rules_miner.prefix_span()
rules = rules_miner.getRules()
[print(r) for r in rules]
rules_miner.print_rules()
