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

class ChangeDetector(object):
    def __init__(self):
        self.is_change_detected = False
        self.sequence_size = 0
        self.sequence = []
        self.current_value = 0
        self.previous_value = 0

    def update(self, new_value):
        self.sequence.append(new_value)
        self.sequence_size += 1

    def check_change(self, new_value):
        pass

    def get_parameters(self):
        parameters_dict = {}
        for k, v in self.__dict__.items():
            if k.endswith('_'):
                parameters_dict[k] = v

        return parameters_dict

    def step(self, new_value):
        self.update(new_value)
        self.check_change(new_value)

        return self.get_parameters()

