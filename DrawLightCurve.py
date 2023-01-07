import numpy as np
import scipy as sp
from scipy import integrate
import matplotlib.pyplot as plt
import math

class drawLightCurve(object):
    #RelativeRadius is the radius of the planet divided by the radius of the star
    def __init__(self, pointsNum,TotalTime,period,RelativeRadius,duration,firstTransitTime):
        changeTime = duration*(RelativeRadius/(1+RelativeRadius))
        self.pointsNum = pointsNum
        # self.TotalTime = TotalTime
        self.TotalTime = 1
        self.period = period/TotalTime
        self.duration = duration/TotalTime
        self.changeTime = changeTime/TotalTime
        # print(self.changeTime)
        self.realTimeLine = np.linspace(0, TotalTime, self.pointsNum)
        self.RelativeRadius = RelativeRadius
        self.firstTransitTime = firstTransitTime/TotalTime
        # self.periodNum = float(TotalTime)/period
        self.x = np.linspace(0, 1, self.pointsNum)
        self.baseLine = np.ones(self.pointsNum)*math.pi *1**2
    
    def calc(self):
        self.transitLine = self.baseLine
        self.transitTime = [self.firstTransitTime]
        while self.transitTime[-1] < self.TotalTime:
            self.transitTime.append(self.transitTime[-1]+self.period)
        self.transitTime = self.transitTime[:-1]

        for index,point in enumerate(self.transitLine):
            for transitTime in self.transitTime:
                if abs((index/self.pointsNum) - transitTime) < self.duration/2:
                    time = (index/self.pointsNum)
                    if time < transitTime:
                        l = abs(((time - (transitTime - self.duration/2))/self.changeTime))
                    else:
                        l = abs(((time - (transitTime + self.duration/2))/self.changeTime))                
                    if l < 1:
                        #TODO:Need to transform the l to arc length.
                        self.transitLine[index] = self.quad(-2*self.RelativeRadius*l + 1 + self.RelativeRadius)
                    else:
                        self.transitLine[index] = math.pi*(1**2 - self.RelativeRadius**2)
                    break
    
    def normalize(self):
        self.transitLine = self.transitLine - np.min(self.transitLine)
        self.transitLine = self.transitLine/np.max(self.transitLine)

    def quad_single(self,x,af,type):
        r = self.RelativeRadius
        R = 1
        assert R > r
        try:
            assert af >= (R-r) and af <= (R+r)
        except:
            print('af',af)
            print('R',R)
            print('r',r)
            print('R-r',R-r)
            print('R+r',R+r)
            exit()
        if(type == 'Ss1'):
            return 2 * (math.sqrt(r ** 2 - (x - af) ** 2))
        elif(type == 'Ss2'):
            return 2 * (math.sqrt(R ** 2 - x ** 2))
    
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
    
    def addNoise(self,noiseLevel):
        self.transitLine()

if __name__ == '__main__':
    curve = drawLightCurve(pointsNum = 2000,period = 3,duration = 1,firstTransitTime = 1.5,TotalTime = 5,RelativeRadius=0.2)
    curve.calc()
    # curve.normalize()
    
    # plt.figure()
    # plt.plot(curve.realTimeLine,curve.transitLine,'b.',markersize = 1)
    dir = './npData/'
    np.save(dir+'realTimeLine',curve.realTimeLine)
    # for transitTime in curve.transitTime:
    #     plt.axvline(x = transitTime*curve.pointsNum,color = 'r')
    # plt.show()