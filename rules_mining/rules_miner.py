import sys
from collections import defaultdict
from heapq import heappop, heappush

def contains_sublist(db, sublst):
    counter = 0
    for j in range(len(db)):
        n = len(sublst)
        if any((sublst == db[j][i:i+n]) for i in range(len(db[j])-n+1)):
            counter += 1
    return counter

class RulesMiner(object):

    def __init__(self, sequences, min_sup=1, max_window_size=10):
        self.sequences = sequences
        self.min_sup = min_sup
        self.max_window_size = max_window_size
        self.frequent_seqs = []
        self.rules = []
        self.gcd = 100

        self.x = [(i, 0) for i in range(len(self.sequences))]

    def prefix_span(self, patt=[], mdb=None):
        if mdb is None:
            mdb = self.x

        self.frequent_seqs.append((len(mdb), patt))
        occurs = defaultdict(list)

        for (i, startpos) in mdb: #for each sequence
            seq = self.sequences[i]
            for j in range(startpos, len(seq)):     # for each elem in seq from startPoint to end
                l = occurs[seq[j]]                  # list of tuples, where [0] is seq index and [1] is elem index +1
                if len(l) == 0 or l[-1][0] != i:    # or last item in l(seq index) is diffrent than current seq index
                    l.append((i, j + 1))

        for (c, newmdb) in occurs.items():
            if (len(newmdb) >= self.min_sup and
                len(patt) < self.max_window_size and
                contains_sublist(self.sequences, patt + [c]) == len(newmdb)):
                self.prefix_span(patt + [c], newmdb)

    def get_frequent_sequnces(self):
        return self.frequent_seqs

    def getRules(self):
        for (freq, pattern) in self.frequent_seqs:
            for i in range(1, len(pattern)):
                lhs = pattern[0:i]
                rhs = pattern[i:len(pattern)]
                rule = str(str(lhs) + " ==> " + str(rhs))
                if rule not in self.rules:
                    self.rules.append((lhs, rhs, freq))

        return self.rules

    def print_rules(self):
        for rule in sorted(self.rules, key=lambda r: r[2],reverse=True):
            lhs = rule[0]
            rhs = rule[1]

            is_rhs_target = True
            for elem in rhs:
                if elem.split(":")[0] != "attr_4":
                    is_rhs_target = False
                    break
            for elem in lhs:
                if elem.split(":")[0] == "attr_4":
                    is_rhs_target = False
                    break

            if is_rhs_target:

                counter = 1
                lhs_short = ""
                for i in range(1, len(lhs)):
                    if(i == 0):
                        lhs_short +=  str(lhs[i] + "{" + str(gcd) + "} ")

                    elif lhs[i] == lhs[i-1]:
                        counter += 1
                    else:
                        lhs_short += str(lhs[i-1]) + "{" + str(counter*self.gcd) + "} "
                        counter = 1

                lhs_short += str(lhs[-1]) + "{" + str(counter*self.gcd) + "}"

                counter = 1
                rhs_short = ""
                for i in range(1, len(rhs)):
                    if(i == 0):
                        rhs_short += str(rhs[i] + "{" + str(gcd)+ "} ")

                    elif rhs[i] == rhs[i-1]:
                        counter += 1
                    else:
                        rhs_short += str(rhs[i-1]) + "{" + str(counter*self.gcd) +"} "

                rhs_short += str(rhs[-1]) + "{" +str(counter*self.gcd)+ "} "

                print(lhs_short, "==>", rhs_short, "\tSupp:", rule[2])
                print(rule[0], "==>", rule[1], "\tSup:", rule[2])
                #print(rule)
                print("-----------------------------------------------------")
