# Symbolic data
df = pd.read_csv('sequences/sequence_2017_11_22-19.35.27.csv')
seq = np.array(df['day_of_week'])
label = ['Fri', 'Mon', 'Sat', 'Sun', 'Thu', 'Tue', 'Wed']
le = preprocessing.LabelEncoder()
le.fit(label)
seq = le.transform(seq) +1