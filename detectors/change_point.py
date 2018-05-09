class ChangePoint(object):
    def __init__(self, from_, to_, at_, prev_value_len_, attr_name_):
        self.prev_value = from_
        self.curr_value = to_
        self.at_ = at_
        self.prev_value_len = prev_value_len_
        self.attr_name = attr_name_

    def __repr__(self):
        return("(" + self.attr_name + " changed from:" + str(self.prev_value) + "(len= " + str(self.prev_value_len) + ") to:" + str(self.curr_value) + " at: " + str(self.at_) + ")")
