import numpy as np
import scipy as sp
from scipy import integrate
import matplotlib.pyplot as plt
import math

class drawLightCurve(object):
    #RelativeRadius is the radius of the planet divided by the radius of the star
    def __init__(self, pointsNum,TotalTime,period,RelativeRadius,duration,depth,firstTransitTime):
        changeTime = duration*0.5*(RelativeRadius/(1+RelativeRadius))
        self.pointsNum = pointsNum
        # self.TotalTime = TotalTime
        self.TotalTime = 1
        self.period = period/TotalTime
        self.duration = duration/TotalTime
        self.changeTime = changeTime/TotalTime
        self.RelativeRadius = RelativeRadius
        self.firstTransitTime = firstTransitTime/TotalTime
        # self.periodNum = float(TotalTime)/period
        self.x = np.linspace(0, 1, self.pointsNum)
        self.baseLine = np.ones(self.pointsNum)*math.pi *1**2
    
    def calc(self):
        self.transitLine = self.baseLine
        # self.durPoints = int(self.duration/self.TotalTime*self.pointsNum)
        #Calculate all the transit times
        self.transitTime = [self.firstTransitTime]
        while self.transitTime[-1] < self.TotalTime:
            self.transitTime.append(self.transitTime[-1]+self.period)
        self.transitTime = self.transitTime[:-1]

        for index,point in enumerate(self.transitLine):
            for transitTime in self.transitTime:
                if abs((index/self.pointsNum) - transitTime) < self.duration:
                    if abs(self.duration - abs((index/self.pointsNum) - transitTime)) < self.changeTime:
                        #TODO:Need to transform the l to arc length.
                        l = 1 - (abs(self.duration - abs((index/self.pointsNum) - transitTime)))/self.changeTime
                        # self.transitLine[index] = self.calcChange(2*self.RelativeRadius*l + 1 - self.RelativeRadius)
                        self.transitLine[index] = self.quad(2*self.RelativeRadius*l + 1 - self.RelativeRadius)
                    else:
                        self.transitLine[index] = math.pi*(1**2 - self.RelativeRadius**2)
                    break

    def calcChange(self,af):
        # af = 0.51
        r = self.RelativeRadius
        R = 1
        assert R > r
        assert af >= (R-r) and af <= (R+r)
        Ia1 = af - r
        Ib1 = abs((R ** 2 - r ** 2 + af ** 2) / (2 * af))
        print('af',af)
        print('Ib1',Ib1)
        print('asin',math.asin(Ib1 / abs(R)))

        Ia2 = Ib1
        Ib2 = R

        Ss1b = R ** 2 * math.asin(Ib1 / abs(R)) + Ib1 * math.sqrt(R ** 2 - Ib1 ** 2)
        Ss1a = R ** 2 * math.asin(Ia1 / abs(R)) + Ia1 * math.sqrt(R ** 2 - Ia1 ** 2)
        Ss1 = Ss1b - Ss1a
        
        Ss2b = r ** 2 * math.asin((Ib2 - af) / abs(r)) + (Ib2 - af) * math.sqrt(2 * af * Ib2 + r ** 2 - Ib2 ** 2 - af **2)
        Ss2a = r ** 2 * math.asin((Ia2 - af) / abs(r)) + (Ia2 - af) * math.sqrt(2 * af * Ia2 + r ** 2 - Ia2 ** 2 - af **2)
        Ss2 = Ss2b - Ss2a
        Ss = Ss1 + Ss2
        return math.pi *R**2 - Ss
    
    def normalize(self):
        self.transitLine = self.transitLine - np.min(self.transitLine)
        self.transitLine = self.transitLine/np.max(self.transitLine)

    def quad_single(self,x,af,type):
        r = self.RelativeRadius
        R = 1
        assert R > r
        assert af >= (R-r) and af <= (R+r)
        if(type == 'Ss1'):
            return 2 * (math.sqrt(r ** 2 - (x - af) ** 2))
        elif(type == 'Ss2'):
            return 2 * (math.sqrt(R ** 2 - x ** 2))
        # Ss1 = 2 * (math.sqrt(r ** 2 - (x - af) ** 2))#, x, Ia1, Ib1);
        # Ss2 = 2 * (math.sqrt(R ** 2 - x ** 2))#, x), Ia2, Ib2);
        # return [Ss1,Ss2]
    
    def quad(self,af):
        r = self.RelativeRadius
        R = 1
        Ia1 = af - r
        Ib1 = abs((R ** 2 - r ** 2 + af ** 2) / (2 * af))
        Ia2 = Ib1
        Ib2 = R
        Ss1 = sp.integrate.quad(self.quad_single,Ia1,Ib1,args = (af,'Ss1'))
        Ss2 = sp.integrate.quad(self.quad_single,Ia2,Ib2,args = (af,'Ss2'))
        return math.pi *R**2 - (Ss1[0] + Ss2[0])

if __name__ == '__main__':
    curve = drawLightCurve(pointsNum = 2000,period = 10,duration = 1,firstTransitTime = 1.5,TotalTime = 3,RelativeRadius=0.9)
    curve.calc()
    curve.normalize()

    plt.figure()
    # plt.plot(curve.transitLine)
    plt.plot(curve.transitLine,'b.',markersize = 1)

    # for transitTime in curve.transitTime:
    #     plt.axvline(x = transitTime*curve.pointsNum,color = 'r')
    plt.show()