import time as tm
from leg import *
import numpy as np
import math as ma
from robowalk import *


class Robot(object):
    def __init__(self):
        self.list = []
        self.steptime = 0.15
        self.status = 0
        self.bein = Legs()
        self.bein.activate()
        self.walk = Walk()
        self.__go = True

    def __sendListToBein(self, i=0):
        for o in range(0, 6, 2):
            self.bein.setPos(o, self.list[i])

        alt = int(len(self.list) / 2)
        if i >= len(self.list) / 2:
            i -= alt
        else:
            i += alt
        for o in range(1, 6, 2):
            self.bein.setPos(o, self.list[i])

    def go(self):
        self.__setGoPos()
        self.__move()
        self.__setStandPos()
    
    def __setGoPos(self):
        self.list = self.walk.getStartPos()
        self.__sendListToBein()
        tm.sleep(self.steptime)

    def __setStandPos(self):
        self.list = self.walk.getStandPos()
        self.__sendListToBein()
        tm.sleep(self.steptime)

    def __move(self):
        """
        Fängt an die die gesetzte Richtung zu gehen
        """
        firstHalf = True
        while self.__go:
            tstart = tm.time()
            steps = 0
            self.list = self.walk.genList()

            if firstHalf:
                start, stop = 0, int(len(self.list)/2)
                firstHalf = False
            else:
                start, stop = int(len(self.list)/2), len(self.list)
                firstHalf = True

            for i in range(start, stop):
                self.__sendListToBein(i)
                steps += 1
                td = (self.steptime * steps) - (tm.time() - tstart)
                if td > 0:
                    tm.sleep(td)
                else:
                    pass
                    print(td, " Sekunden überschritten!!!")
                self.bein.activate()

    def stop(self):
        print('stop')
        self.__go = False

    def setAngel(self, angel):
        self.walk.setAngle(angel)
        print("Winkel gesetzt zu:", angel)

    def setMode(self, mode):
        modetext = self.walk.setMode(mode)
        print("Geheform gesetzt zu:", modetext)

    def setSpu(self, spu):
        self.walk.setSpu(spu)
        print("steps per unit gesetzt zu:", spu)
