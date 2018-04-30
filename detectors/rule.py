
class Rule(object):
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs
        self.number_of_occurrences = 0
        self.last_occurrence = -1
        self.generalized = False

    def __repr__(self):
        generalized = " Generalized" if self.generalized else ""
        return(str(self.lhs) + " ==> " + str(self.rhs) + " |\t\t nr_of_occurences:" + str(self.number_of_occurrences) + " last_occurence:" + str(self.last_occurrence) + generalized)
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