import numpy as np

def createC1(dataSet):
    C1 = []
    for transaction in dataSet:
        for item in transaction:
            if not [item] in C1:
                C1.append([item])
    return C1

def contains(small, big):
    for i in range(len(big)-len(small)+1):
        for j in range(len(small)):
            if big[i+j] != small[j]:
                break
        else:
            return i, i+len(small)
    return False

def scanD(D, Ck, minSupport):
    ssCnt = {}
    for tid in D:
        for can in Ck:
            if contains(can, tid):
                if not tuple(can) in ssCnt:
                    ssCnt[tuple(can)] = 1
                else:
                    ssCnt[tuple(can)] += 1

    numItems = float(len(D))
    retList = []
    supportData = {}
    for key in ssCnt:
        support = ssCnt[key]/numItems
        print(key, "\tsupp:", support)
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

def apriori(dataSet, minSupport = 0.5):
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

def generateRules(L, supportData, minConf=0.7):
    rulesList = []
    for i in range(1, len(L)):
        for freqSeq in L[i]:
            for j in range(1, len(freqSeq)):
                lhs = freqSeq[:j]
                rhs = freqSeq[j:]
                conf = supportData[freqSeq] / supportData[rhs]  # calc confidence
                #print(('attr_4:5',))
                if conf >= minConf and rhs == ('attr_4:5',):
                    rule = (rhs, lhs, conf)
                    rulesList.append(rule)
                    print(lhs, "-->", rhs, "\tconf:", conf)

    return rulesList

# dataSet = [[1, 1, 3, 4],
#             [2, 3, 5, 1, 1, 3],
#             [1, 1, 2, 3, 5,1],
#             ['a', 'b', 'c'],
#             ['a', 'b', 'c'],
#             ['a', 'b', 'c'],
#             [2, 5],
#             ['a', 'b', 'c']]
dataSet = [['attr_1:2', 'attr_1:2', 'attr_1:2', 'attr_1:3', 'attr_1:3', 'attr_1:3', 'attr_1:3', 'attr_1:3', 'attr_4:5'],
           ['attr_2:4', 'attr_2:4', 'attr_2:4', 'attr_2:4', 'attr_2:4', 'attr_2:5', 'attr_2:5', 'attr_2:5', 'attr_4:5'],
           ['attr_3:1', 'attr_3:1', 'attr_3:1', 'attr_3:1', 'attr_3:1', 'attr_3:1', 'attr_3:1', 'attr_3:4', 'attr_4:5']]
L, suppData = apriori(dataSet, minSupport=0.1)
rules= generateRules(L,suppData, minConf=0.0)