import numpy
import math
from adwin_win_list import AdWinList
from detector import ChangeDetector

class AdwinDetector(ChangeDetector):
    def __init__(self, delta = 0.01):
        super( AdwinDetector, self ).__init__()
        self.MINTCLOCK = 1.0
        self.MINLENGTHWINDOW = 5
        self.DELTA = delta
        self.MAXBUCKETS = 5
        self.bucketList = AdWinList(self.MAXBUCKETS)
        self.mintTime=0.0;
        self.mintClock=self.MINTCLOCK;
        self.mdblError=0.0;
        self.mdblWidth=0.0;
        self.lastBucketRow=0;
        self.sum_ = 0.0;
        self.W_ = 0.0;
        self.var = 0.0;
        self.bucketNumber=0;
        self.est_ = 0
        self.rules_triggered = False

    def getEstimation(self):
        if self.W_ > 0:
            return self.sum_ / float(self.W_);
        else:
            return 0;

    def update(self, new_signal_value):
        super(AdwinDetector, self).update(new_signal_value)
        self.insertElement(new_signal_value)
        self.compressBuckets()
        self.est_ = self.getEstimation()

        #return self.checkDrift()

    def check_stopping_rules(self, new_signal_value):
        self.rules_triggered = False
        if self.checkDrift():
            self.rules_triggered = True
            self.bucketList = AdWinList(self.MAXBUCKETS)
            self.mintTime=0.0;
            self.mintClock=self.MINTCLOCK;
            self.mdblError=0.0;
            self.mdblWidth=0.0;
            self.lastBucketRow=0;
            self.sum_ = 0.0;
            self.W_ = 0.0;
            self.var = 0.0;
            self.bucketNumber=0;
            self.est_ = 0

    def printInfo(self):
        it = self.bucketList.tail
        if it is None:
            print("It None")

        i = self.lastBucketRow

        while True:
            for k in range(it.size-1, -1, -1):
                print(str(i)+" ["+str(it.sum[k])+" de "+str(self.bucketSize(i))+"],")

            print()
            it = it.prev
            i -= 1
            if it is None:
                break;

    def length(self):
        return self.W_

    def insertElement(self, value):
        self.W_ +=1
        self.bucketList.head.addBack(float(value), 0.0)
        self.bucketNumber += 1

        if self.W_ > 1:
            self.var += (self.W_-1) * (value-self.sum_/(self.W_-1)) * (value-self.sum_/(self.W_-1))/self.W_

        self.sum_ += value

    def compressBuckets(self):
        i = 0
        cont = 0

        cursor = self.bucketList.head
        nextNode = None

        while True:
            k = cursor.size
            if k == self.MAXBUCKETS+1:
                nextNode = cursor.next
                if nextNode is None:
                    self.bucketList.addToTail()
                    nextNode = cursor.next
                    self.lastBucketRow += 1
                n1 = self.bucketSize(i)
                n2 = self.bucketSize(i)
                u1 = cursor.sum[0]/n1
                u2 = cursor.sum[1]/n2
                incVariance = n1*n2*(u1-u2)*(u1-u2)/(n1+n2)
                nextNode.addBack(cursor.sum[0]+cursor.sum[1], cursor.variance[0]+cursor.variance[1]+incVariance)
                self.bucketNumber -= 1
                cursor.dropFront(2)
                if nextNode.size <= self.MAXBUCKETS:
                    break
            else:
                break
            cursor = cursor.next
            i += 1
            if cursor is None:
                break

    def checkDrift(self):
        change = False
        quit = False
        it = None

        self.mintTime += 1

        if self.mintTime % self.mintClock == 0 and self.W_ > self.MINLENGTHWINDOW:
            blnTalla = True

            while blnTalla:
                blnTalla = False
                quit = False
                n0 = 0.0
                n1 = float(self.W_)
                u0 = 0.0
                u1 = float(self.sum_)
                it = self.bucketList.tail
                i = self.lastBucketRow

                while True:
                    for k in range(it.size):
                        if i == 0 and k == it.size-1:
                            quit = True
                            break
                        n0 += self.bucketSize(i)
                        n1 -= self.bucketSize(i)
                        u0 += it.sum[k]
                        u1 -= it.sum[k]
                        mintMinWinLength = 5
                        if n0 >= mintMinWinLength and n1 >= mintMinWinLength and self.cutExpression(n0, n1, u0, u1):
                            blnTalla = True
                            change = True
                            if self.W_ > 0:
                                self.deleteElement()
                                quit = True
                                break
                    it = it.prev
                    i -= 1
                    if quit or it is None:
                        break
        return change;

    def deleteElement(self):
        node = self.bucketList.tail
        n1 = self.bucketSize(self.lastBucketRow)
        self.W_ -= n1
        self.sum_ -= node.sum[0]
        u1 = node.sum[0]/n1
        incVariance = float(node.variance[0]+n1*self.W_*(u1-self.sum_/self.W_)*(u1-self.sum_/self.W_))/(float(n1+self.W_))
        self.var -= incVariance
        node.dropFront()
        self.bucketNumber -= 1
        if node.size == 0:
            self.bucketList.removeFromTail()
            self.lastBucketRow -= 1

    def cutExpression(self, N0, N1, u0, u1):
        n0 = float(N0)
        n1 = float(N1)
        n = float(self.W_)
        diff = float(u0/n0) - float(u1/n1)

        v = self.var/self.W_
        dd = math.log(2.0*math.log(n)/self.DELTA)

        mintMinWinLength = 5
        m = (float(1/((n0-mintMinWinLength+1))))+(float(1/((n1-mintMinWinLength+1))))
        eps = math.sqrt(2*m*v*dd)+float(2/3*dd*m)

        if math.fabs(diff) > eps:
            return True
        else:
            return False

    def bucketSize(self, Row):
        return int(math.pow(2,Row));
