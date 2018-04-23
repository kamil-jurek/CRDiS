from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
import category_encoders as ce
import numpy as np

label_encoder = None

def encode(data):
    #encoder = ce.BinaryEncoder( ) #obiecujacy
    encoder = ce.HelmertEncoder( ) #obiecujacy
    #encoder = ce.OrdinalEncoder( ) #simple but working

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