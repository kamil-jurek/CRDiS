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

import numpy as np

class Rule(object):
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs
        self.rule_support = 0
        self.last_occurrence = -1
        self.occurrences = []
        self.lhs_support = 0
        self.generalized = False
        self.RHS_factor = 1.5

    def __repr__(self):
        generalized = " Generalized" if self.generalized else ""

        return(str(self.lhs) + " ==> " + str(self.rhs) +
               "\n\t# rule_support:\t" + str(self.rule_support) +
               "\n\t# lhs_support:\t" + str(self.lhs_support) +
               "\n\t# confidence:\t" + str(self.get_confidence()) +
               "\n\t# rule_score:\t" + str(self.get_rule_score()) +
               "\n\t# occurences:\t" + str(self.occurrences) + generalized)
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

    def increment_rule_support(self):
        self.rule_support += 1

    def set_last_occurence(self, last):
        self.last_occurrence = last

    def get_confidence(self):
        if self.lhs and self.rhs:
            return self.rule_support / self.lhs_support
        else:
            return 0

    def get_rule_score(self):
        if self.lhs and self.rhs:
            lhs_score = np.sum([lhs.len for lhs in self.lhs])
            rhs_score = self.rhs.len

            return self.rule_support  * self.get_confidence() *(lhs_score + rhs_score * self.RHS_factor)
        else:
            return 0