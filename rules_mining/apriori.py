import numpy as np
from collections import defaultdict

class Rule(object):
    def __init__(self, lhs, rhs, conf, supp):
        self.lhs = lhs
        self.rhs = rhs
        self.conf = conf
        self.supp = supp

    def __repr__(self):
        return(str(self.lhs) + " ==> " + str(self.rhs) + "\tconf:" + str(self.conf)+ "\tsupp:"+ str(self.supp))

def createC1(data_set):
    candidate_seqs_1 = []
    for transaction in data_set:
        for item in transaction:
            if not [item] in candidate_seqs_1:
                candidate_seqs_1.append([item])
    return candidate_seqs_1

def contains(small, big):
    for i in range(len(big)-len(small)+1):
        for j in range(len(small)):
            if big[i+j] != small[j]:
                break
        else:
            return i, i+len(small)
    return False

def scanD(data_set, candidates_k, minSupport):
    ssCnt = {}
    for tid in data_set:
        for can in candidates_k:
            if contains(can, tid):
                if not tuple(can) in ssCnt:
                    ssCnt[tuple(can)] = 1
                else:
                    ssCnt[tuple(can)] += 1

    numItems = float(len(data_set))
    retList = []
    supportData = {}
    for key in ssCnt:
        support = ssCnt[key]/numItems
        #print(key, "\tsupp:", support)
        if support >= minSupport:
            retList.append(key)
        supportData[key] = support
    return retList, supportData



def aprioriGen(Lk, k): #creates candidates list
    retList = []
    lenLk = len(Lk)
    for i in range(lenLk):
        for j in range(lenLk):
            for k in Lk[j]:
                t = tuple([k])
                if Lk[i] + t not in retList:
                    retList.append(Lk[i] + t)
    return retList

def aprioriAlgo(dataSet, minSupport = 0.5):
    C1 = createC1(dataSet)
    D = dataSet
    L1, supportData = scanD(D, C1, minSupport)
    L = [L1]
    k = 2
    while (len(L[k-2]) > 0):
        Ck = aprioriGen(L[k-2], k)
        Lk, supK = scanD(D, Ck, minSupport)
        supportData.update(supK)
        L.append(Lk)
        k += 1
    return L, supportData

def generateRules(L, supportData, target, minConf=0.7):
    rulesList = []
    rulesDict = defaultdict(list)
    for i in range(1, len(L)):
        for freqSeq in L[i]:
            for j in range(1, len(freqSeq)):
                lhs = freqSeq[:j]
                rhs = freqSeq[j:]
                conf = supportData[freqSeq] / supportData[rhs]  # calc confidence
                print(conf)
                if conf >= minConf: # and rhs == (target,):
                    rule = Rule(lhs, rhs, conf, supportData[freqSeq])
                    attrName = getAttrName(lhs)

                    rulesDict[attrName].append(rule)
                    rulesList.append(rule)
                    #print(rule)


    return (rulesList, rulesDict)

def getAttrName(lhs):
    return (lhs[0].split(':')[0])

# dataSet = [[1, 1, 3, 4],
#             [2, 3, 5, 1, 1, 3],
#             [1, 1, 2, 3, 5,1],
#             ['a', 'b', 'c'],
#             ['a', 'b', 'c'],
#             ['a', 'b', 'c'],
#             [2, 5],
#             ['a', 'b', 'c']]

dataSet = [['attr_1(1->2)', 'attr_1(2->3)', 'attr_1(3->4)'],
        #    ['attr_2:4', 'attr_2:4', 'attr_2:4', 'attr_2:4', 'attr_2:4', 'attr_2:5', 'attr_2:5', 'attr_2:1', 'target'],
        #    #['attr_2:1', 'attr_2:4', 'attr_2:4', 'attr_2:4', 'attr_2:4', 'attr_2:5', 'attr_2:5', 'attr_2:5', 'target'],
        #    ['attr_3:1', 'attr_3:1', 'attr_3:1', 'attr_3:1', 'attr_3:1', 'attr_3:1', 'attr_3:1', 'attr_3:4', 'target'],
        #    #['attr_1:1', 'attr_1:2', 'attr_1:2', 'attr_1:3', 'attr_1:3', 'attr_1:3', 'attr_1:3', 'attr_1:3', 'target']
           ]

# # L, suppData = aprioriAlgo(dataSet, minSupport=0.1)
# # rules, rulesDict= generateRules(L,suppData, minConf=0.0)
target = 'attr_1(4){600}'
L, suppData = aprioriAlgo(dataSet, minSupport=0.0)
rules, rulesDict = generateRules(L,suppData, target, minConf=0.0)
#
for r in rules:
    print(r)

# for k, r in rulesDict.items():
#     r.sort(key=lambda t: len(t.lhs), reverse=True)
#     print(k, r[0])
#     print("------------------------------------")
#     for ru in r:
#         print(k, ru)
