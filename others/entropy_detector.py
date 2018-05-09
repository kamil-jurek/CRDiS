import numpy as np
import scipy as scp
import math
from detector import ChangeDetector
from collections import deque
from collections import Counter
from statistics import mode

class EntropyDetector(ChangeDetector):
    def __init__(self, threshold=4, window_size = 5):
        super( EntropyDetector, self ).__init__()
        self.entropy_ = 0
        self.oldEntropy = 0
        self.threshold = threshold
        self.freqList = {}
        self.sum_ = 0
        self.kl_ = 0
        self.kl_window_ = 0
        self.window = deque(maxlen = window_size)
        self.window_size = window_size
        self.w2g_ = 0
        self.sig = []
        self.sigSize = 0

    def update(self, new_signal_value):
        super(EntropyDetector, self).update(new_signal_value)
        x = new_signal_value
        self.window.append(x)
        self.sig.append(x)
        self.sigSize += 1

        if x in self.freqList:
            self.freqList[x] += 1
        else:
            self.freqList[x] = 1

        #self.entropy_ = scp.stats.entropy(self.sig)
        # self.oldEntropy = self.entropy_
        # for f in self.freqList:
        #     p_x = float(self.signal.count(x))/self.signal_size
        #     #print(p_x)
        #     if p_x > 0:
        #         self.entropy_ += - p_x * math.log(p_x, 2)
        # #print(self.entropy_)
        # self.sum_ = self.sum_ + self.entropy_ - self.oldEntropy;
        ##############
        freqList2={}
        for i in self.window:
            if i in freqList2:
                freqList2[i] += 1
            else:
                freqList2[1] = 1

        qkw = [v/self.window_size for k, v in freqList2.items()]
        print(qkw)
        #qkw = [0.1 for i in np.arange(len(self.window))]
        #print(qkw)
        #self.kl_window_ = scp.stats.entropy(self.window)

        #mod = mode(self.sig)
        # qk = [self.freqList[self.sig[i]] / self.sigSize for i in np.arange(self.sigSize)]
        # print(qk)
        # #qk = [0.1 for i in np.arange(self.sigSize)]
        # #
        # # for i in np.arange(self.sigSize):
        # #     if self.sig[i] == mod:
        # #         qk[i] = 0.9
        #self.kl_ = scp.stats.entropy(qk)
        #
        self.w2g_ =  scp.stats.entropy(qkw)
        #print(self.kl_)

        # if self.sigSize % 100 == 0:
        #     print(self.freqList)
        qk = [v/self.sigSize for k, v in self.freqList.items()]
        #qk = [self.freqList[self.sig[i]] / self.sigSize for i in np.arange(self.sigSize)]
        print(qk, '\n')
        self.kl_ = scp.stats.entropy(qk)


    def check_stopping_rules(self, new_signal_value):
        self.rules_triggered = False
        #print("entropy:", self.entropy_)

        #if self.entropy_ > self.threshold:
        # if self.kl_ > 0.5:
        #    self.is_change_detected = True
        #    self.sigSize = 0
        #    self.sig = []
        #    self.freqList = {}
        #     self.entropy_ = 0
        #     self.sig = []
        #     self.sigSize = 0
        #     self.window = []


    def entrop(self, data):
        entropy = 0
        for x in range(len(data)):
            p_x = float(data.count(x))/len(data)
            if p_x > 0:
                entropy += - p_x*math.log(p_x, 2)
        return entropy
