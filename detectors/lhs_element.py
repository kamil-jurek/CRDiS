
class LHS_element(object):
    def __init__(self, len_, value_, attr_name_):
        self.len = len_
        self.value = value_
        self.attr_name_ = attr_name_

    def __repr__(self):
        return(str(self.attr_name_) + ": " + str(self.value) + "{"+ str(self.len) + "}" )

    def __eq__(self, other):
        if isinstance(other, LHS_element):
            return ((self.len == other.len) and (self.value == other.value) and (self.attr_name_ == other.attr_name_))
        else:
            return False

    def __ne__(self, other):
        return (not self.__eq__(other))

    def __hash__(self):
        return hash(self.__repr__())