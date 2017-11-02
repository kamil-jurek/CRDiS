import zscore as zs
import numpy as np
import pylab
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('sequences/sequence_2017_11_01-21:24:04.csv')

y = df['attr_1']
# Data
# y = np.array([1,1,1.1,1,0.9,1,1,1.1,1,0.9,1,1.1,1,1,0.9,1,1,1.1,1,1,1,1,1.1,0.9,1,1.1,1,1,0.9,
#        1,1.1,1,1,1.1,1,0.8,0.9,1,1.2,0.9,1,1,1.1,1.2,1,1.5,1,3,2,5,3,2,1,1,1,0.9,1,1,3,
#        2.6,4,3,3.2,2,1,1,0.8,4,4,2,2.5,1,1,1])

# Settings: lag = 30, threshold = 5, influence = 0
lag = 30
threshold = 1.5
influence = 0.5

# Run algo with settings from above
result = zs.thresholding_algo(y, lag=lag, threshold=threshold, influence=influence)
#print(result)

# Plot result
plt.subplot(211)
plt.plot(np.arange(1, len(y)+1), y)

plt.plot(np.arange(1, len(y)+1),
           result["avgFilter"], color="cyan", lw=2)

plt.plot(np.arange(1, len(y)+1),
           result["avgFilter"] + threshold * result["stdFilter"], color="green", lw=2)

plt.plot(np.arange(1, len(y)+1),
           result["avgFilter"] - threshold * result["stdFilter"], color="green", lw=2)

plt.subplot(212)
plt.step(np.arange(1, len(y)+1), result["signals"], color="red", lw=2)
plt.ylim(-1.5, 1.5)
plt.show()
