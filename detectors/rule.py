import numpy as np

class Rule(object):
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs
        self.number_of_occurrences = 0
        self.last_occurrence = -1
        self.occurrences = []
        self.support = 0
        self.generalized = False

    def __repr__(self):
        generalized = " Generalized" if self.generalized else ""
        return(str(self.lhs) + " ==> " + str(self.rhs) + "\n\t| nr_of_occurences:" + str(self.number_of_occurrences) +
               " | support:" + str(self.support) +  " | confidence:" + str(self.number_of_occurrences/self.support) +
               " | rule_score:" + str(self.get_rule_score()) + " | last_occurence:" + str(self.last_occurrence) + " | occurences:" + str(self.occurrences) + generalized)
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

    def get_rule_score(self):
        if self.lhs and self.rhs:
            lhs_score = np.sum([lhs.len for lhs in self.lhs])
            rhs_score = self.rhs.len

            return self.number_of_occurrences * (lhs_score + rhs_score)
        else:
            return 0