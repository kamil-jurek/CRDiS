from __future__ import print_function

import sys
from collections import defaultdict
from heapq import heappop, heappush

results = []

def contains_sublist(db, sublst):
    counter = 0
    for j in range(len(db)):
        n = len(sublst)
        if any((sublst == db[j][i:i+n]) for i in range(len(db[j])-n+1)):
            counter += 1
    return counter

def frequent_rec(patt, mdb):
    results.append((len(mdb), patt))

    occurs = defaultdict(list)
    for (i, startpos) in mdb: #for each sequence
        seq = db[i]
        for j in range(startpos, len(seq)): # for each elem in seq from startPoint to end
            l = occurs[seq[j]]  # list of tuples, where [0] is seq index and [1] is elem index +1
            if len(l) == 0 or l[-1][0] != i:    #or last item in l(seq index) is diffrent than
                l.append((i, j + 1))

    for (c, newmdb) in occurs.items():
        if len(newmdb) >= minsup and contains_sublist(db, patt + [c]) ==len(newmdb):
            frequent_rec(patt + [c], newmdb)

#######################################################3
db = [
        [2, 2, 2, 2, 3, 3, 3, 3, 2, 2, 2, 2, 2, 4, 4, 4, 4, 5, 5, 5, 5, 5]
     ]


minsup = 1
gcd = 50

x = [(i, 0) for i in range(len(db))]
frequent_rec([], x)

freq_patterns = []
for (freq, patt) in results:
    freq_patterns.append(patt)

rules = []
for pattern in freq_patterns:
    for i in range(1,len(pattern)):
        lhs = pattern[0:i]
        rhs = pattern[i:len(pattern)]
        rule = str(str(lhs) + " ==> " + str(rhs))
        if rule not in rules:
            counter = 1
            lhs_short = ""
            rhs_short = ""
            for i in range(1,len(lhs)):
                if(i == 0):
                    lhs_short += str(gcd) + " * " + str(lhs[i] + "; ")

                elif lhs[i] == lhs[i-1]:
                    counter += 1
                else:
                    lhs_short += str(counter*gcd) + " * " + str(lhs[i-1]) + "; "
            lhs_short += str(counter*gcd) + " * " + str(lhs[-1]) +  " ===>"

            counter = 1
            for i in range(1,len(rhs)):
                if(i == 0):
                    rhs_short += str(gcd) + " * " + str(rhs[i] + "; ")

                elif rhs[i] == rhs[i-1]:
                    counter += 1
                else:
                    rhs_short += str(counter*gcd) + " * " + str(rhs[i-1]) + "; "
            rhs_short += str(counter*gcd) + " * " + str(rhs[-1])

            print(lhs_short, rhs_short)
            print(rule)
            print("--------------------")
            rules.append(rule)
