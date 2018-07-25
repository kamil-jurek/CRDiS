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

import sys;
sys.path.append('./detectors/')
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import encoders as en
from detector import ChangeDetector
from online_simulator import OnlineSimulator
from geometric_moving_average_detector import GeometricMovingAverageDetector
from rules_detector import RulesDetector
from utils import *

#Numerical data
df = pd.read_csv('sequences/sequence_2017_11_28-18.07.57.csv')
seq = np.array(df['attr_1'])

detector = GeometricMovingAverageDetector(threshold=0.75)
simulator = OnlineSimulator(None,
                            [detector],
                            [seq],
                            ['attr_1'])

simulator.run(plot=True, detect_rules=False)

detected_change_points = simulator.get_detected_changes()
print_detected_change_points(detected_change_points)

plt.show()