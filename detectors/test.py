from detector import ChangeDetector
from detector import OnlineSimulator
from cusum_detector import CusumDetector

det = CusumDetector(delta=0.005, lambd=5)
OnlineSimulator(det, [1,2,3,4]).run()
