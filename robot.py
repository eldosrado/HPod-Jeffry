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
        # self.bein = legs()
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
        self.__sendListToBein(l)
        tm.sleep(self.steptime)

    def __move(self):
        """
        Fängt an die die gesetzte Richtung zu gehen
        """
        #tdynam = tm.time()
        while self.__go:
            #tdl = []
            tstart = tm.time()
            self.list = self.walk.genList()
            for i in range(len(self.list)):
                self.__sendListToBein(i)
                #tdl += [tm.time()-tdynam]
                td = (self.steptime * (i + 1)) - (tm.time() - tstart)
                if td > 0:
                    tm.sleep(td)
                else:
                    pass
                    print(td, " Sekunden überschritten!!!")
                #tdynam = tm.time()
                self.bein.activate()
            #self.steptime = max(tdl) * 1.5

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
