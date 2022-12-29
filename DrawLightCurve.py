import numpy as np
import matplotlib.pyplot as plt

class drawLightCurve(object):
    def __init__(self, pointsNum,TotalTime,period,RelativeRadii,duration,changeTime,depth,firstTransitTime):
        self.pointsNum = pointsNum
        # self.TotalTime = TotalTime
        self.TotalTime = 1
        self.period = period/TotalTime
        self.duration = duration/TotalTime
        self.changeTime = changeTime/TotalTime
        self.RelativeRadii = RelativeRadii
        self.depth = depth
        self.firstTransitTime = firstTransitTime/TotalTime
        # self.periodNum = float(TotalTime)/period
        self.x = np.linspace(0, 1, self.pointsNum)
        self.baseline = np.zeros(self.pointsNum)
    
    def calc(self):
        self.transitLine = self.baseline
        # self.durPoints = int(self.duration/self.TotalTime*self.pointsNum)
        
        #Calculate all the transit times
        self.transitTime = [self.firstTransitTime]
        while self.transitTime[-1] < self.TotalTime:
            self.transitTime.append(self.transitTime[-1]+self.period)
        self.transitTime = self.transitTime[:-1]
        print(self.transitTime)

        for index,point in enumerate(self.transitLine):
            for transitTime in self.transitTime:
                if abs((index/self.pointsNum) - transitTime) < self.duration:
                    if abs(self.duration - abs((index/self.pointsNum) - transitTime)) < self.changeTime:

                        self.transitLine[index] = self.depth*((abs(self.duration - abs((index/self.pointsNum) - transitTime)))/self.changeTime)
                    else:
                        self.transitLine[index] = self.depth
                    break
    def draw(self):
        plt.figure()
        # plt.plot(self.baseline,'.')
        plt.plot(self.transitLine,'b.',markersize = 2)
        # plt.plot(self.transitLine)

        # for transitTime in self.transitTime:
        #     plt.axvline(x = transitTime*self.pointsNum,color = 'r')
        plt.show()

if __name__ == '__main__':
    curve = drawLightCurve(pointsNum = 500,period = 7,duration = 0.5,changeTime=0.3,depth = -1,firstTransitTime = 1,TotalTime = 27,RelativeRadii=0.1)
    curve.calc()
    curve.draw()

