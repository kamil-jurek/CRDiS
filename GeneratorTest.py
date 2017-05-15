import SequenceGenerator
import matplotlib.pyplot as plt
import numpy

args = [1, 2, 3, 4, 5, 6]
args_op = ['eq','eq','eq','eq','eq','eq']
args_prob = [0.1, 0.8, 1.0, 0.6, 0.5, 0.93]
args_len = [100, 50, 30, 20, 10, 50]

seq = [SequenceGenerator.generateSequence(args,
                                          args[i],
                                          args_op[i],
                                          args_prob[i],
                                          args_len[i]) for i in range(len(args))]

print seq
[plt.plot(seq[i],'ro', color=numpy.random.rand(3,1)) for i in range(len(args))]
plt.show()

[SequenceGenerator.testSequence(seq[i], args[i], args_prob[i]) for i in range(len(args))]
