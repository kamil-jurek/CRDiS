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

class ChangePoint(object):
    def __init__(self, from_, to_, at_, prev_value_len_, attr_name_, percent_):
        self.prev_value = from_
        self.curr_value = to_
        self.at_ = at_
        self.prev_value_len = prev_value_len_
        self.attr_name = attr_name_
        self.percent = percent_

    def __repr__(self):
        return(self.attr_name + " changed from: " + str(self.prev_value) +
               " to: " + str(self.curr_value) + " at: " + str(self.at_) +
               " prev_value_len: " + str(self.prev_value_len) +
               " prev_value_percent: " + str(self.percent) +"%")
