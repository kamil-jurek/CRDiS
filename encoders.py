from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
import category_encoders as ce

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
    integer_encoded = label_encoder.fit_transform(values)+1

    return integer_encoded
