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

from utils import *

class ChangePoint(object):
    def __init__(self, prev_value, curr_value, at, prev_value_len, attr_name, prev_value_percent):
        self.attr_name = attr_name
        self.prev_value = prev_value
        self.curr_value = curr_value
        self.at_ = at
        self.prev_value_len = prev_value_len
        self.prev_value_percent = prev_value_percent
        self.curr_value_len = -1
        self.curr_value_percent = -1

    def __repr__(self):
        return(self.attr_name + " at: " + str(round_to(self.at_, 60)) + "\t" + 
                str(self.prev_value) + "{" + str(self.prev_value_len) + "}" + " -> " + str(self.curr_value) +
                "{" + str(self.curr_value_len) + "}")
                
    def get_rounded(self, round_to_):
        rounded_cp = ChangePoint(self.prev_value,
                                 self.curr_value,
                                 round_to(self.at_, round_to_),
                                 round_to(self.prev_value_len, round_to_),
                                 self.attr_name,
                                 self.prev_value_percent)
        rounded_cp.curr_value_len = round_to(self.curr_value_len, round_to_)
        rounded_cp.curr_value_percent = self.curr_value_percent


