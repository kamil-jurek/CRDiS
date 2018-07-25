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

from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
import category_encoders as ce
import numpy as np

label_encoder = None

def encode(data):
    encoder = ce.HelmertEncoder()   # promising
    #encoder = ce.BinaryEncoder( )  # promising
    #encoder = ce.OrdinalEncoder( ) # simple but working
    #encoder = ce.polynomial.PolynomialEncoder()
    #encoder = ce.OneHotEncoder()
    #encoder = ce.BackwardDifferenceEncoder()
    #encoder = ce.HashingEncoder( )
    #encoder = ce.SumEncoder()
    encoder.fit(data, verbose=1)
    data = encoder.transform(data)
    data = data.values.tolist()

    #print(data[len(signal)-1])
    return data

def encode_int(data):
    values = np.array(data)
    label_encoder = LabelEncoder()
    label_encoder = label_encoder.fit(values)
    integer_encoded = label_encoder.transform(values)+1

    return integer_encoded

def invese_encode_int(data):
    integer_decoded = label_encoder.inverse_transform([0, 0, 1, 2])
    return integer_decoded