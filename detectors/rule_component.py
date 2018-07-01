
class RuleComponent(object):
    def __init__(self, len_, value_, attr_name_, percent_):
        self.len = len_
        self.value = value_
        self.attr_name_ = attr_name_
        self.percent = percent_

    def __repr__(self):
        return(str(self.attr_name_) + ": " + str(self.value) + "{"+ str(self.len) + "; " + str(self.percent) +"% " +"}")

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