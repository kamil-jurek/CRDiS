class Prediction(object):
    def __init__(self, rhs, lhs, rule, nr):
        self.lhs = lhs
        self.rhs = rhs
        self.rule = rule
        self.number_of_occurrences = nr

    def __repr__(self):      
        return(str(self.lhs) + " ==> " + str(self.rhs) + "\t| nr_of_occurences:" + str(self.number_of_occurrences) +
               " | rule_score:" + str(self.get_prediction_score()))
               
    def get_prediction_score(self):
        return self.number_of_occurrences * self.rule.get_rule_score()