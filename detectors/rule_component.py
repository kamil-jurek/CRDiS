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

class RuleComponent(object):
    def __init__(self, len_, value_, attr_name_, percent_):
        self.len = len_
        self.value = value_
        self.attr_name_ = attr_name_
        self.percent = percent_
        self.prev_value = None

    
    def __repr__(self):
        if self.prev_value:
            return(str(self.attr_name_) + "(" + str(self.prev_value) + "->" + str(self.value) + ")")
        else:
            return(str(self.attr_name_) + "(" + str(self.value) + "){"+ str(self.len) + "; " + "{0:.0f}".format(self.percent) + "%" +"}")

    def __eq__(self, other):
        if isinstance(other, RuleComponent):
            return ((self.len == other.len) and (self.value == other.value) and (self.attr_name_ == other.attr_name_))
        else:
            return False

    def __ne__(self, other):
        return (not self.__eq__(other))

    def __hash__(self):
        return hash(self.__repr__())

    def generalize(self, other):
        generalized_lhs_elem = RuleComponent(None, None, None, 0)
        contains = 0
        if (self.attr_name_ == other.attr_name_ and
            self.value == other.value):
            generalized_lhs_elem.attr_name_ = self.attr_name_
            generalized_lhs_elem.value = self.value

            if self.len >= other.len:
                generalized_lhs_elem.len = other.len
                contains = 1
            else:
                generalized_lhs_elem.len = self.len
                contains = 2

        return (contains, generalized_lhs_elem)