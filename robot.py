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
        self.walk = Walk()
        self.__go = False
        self.__wakeup = True

    # Sendet die Liste an die Beinpaare
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

    # Roboters Hauptschleife
    def wakeup(self):
        self.__setStandPos()
        while self.__wakeup:
            if self.__go:
                self.__setGoPos()
                self.__move()
                self.__setStandPos()

    # Aufmethoden zum Gehen
    def go(self):
        self.__setGoPos()
        self.__move()
        self.__setStandPos()

    # Beretet sich vor um loszugehen // Hebt eine Beingruppe an
    def __setGoPos(self):
        self.list = self.walk.getStartPos()
        self.__sendListToBein()
        tm.sleep(1)
        self.bein.activate()

    # Stellt sich wieder in die ausgangposition hin // Senkt alle Beine
    def __setStandPos(self):
        self.list = self.walk.getStandPos()
        self.__sendListToBein()
        tm.sleep(1)
        self.bein.activate()

    # Führt den eigentlichen Gang aus
    def __move(self):
        firstHalf = True
        while self.__go:
            tstart = tm.time()
            steps = 0
            self.list = self.walk.genList()

            # Unterscheiden Welche Beingruppe sich oben befindet
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
                    print(td, " Sekunden überschritten!!!")
                self.bein.activate()

    # Methode um den Roboter wieder stillstehen zu lassen
    def stop(self):
        print('stop move')
        self.__go = False

    # Startet den Gehvorgang
    def start(self):
        print('start move')
        self.__go = True

    # Winkel in welche richtung der Roboter sich bewegen soll
    def setAngel(self, angel):
        self.walk.setAngle(angel)
        print("Winkel gesetzt zu:", angel)

    # Setzt ein Gangmodus
    # 0 = Dreick
    # 1 = Rechteck
    # 2 = Parabel
    def setMode(self, mode):
        modetext = self.walk.setMode(mode)
        print("Geheform gesetzt zu:", modetext)

    # Ändert den Gangmode zu dem Nächsten
    def switchMode(self):
        self.walk.switchMode()

    # Setzt die Anzahl der zwischenpunkte bei der Gangbewegung
    def setSpu(self, spu):
        self.walk.setSpu(spu)
        print("steps per unit gesetzt zu:", spu)

    # Beendet das komplete Roboterporgramm
    def RobotSleep(self):
        self.__wakeup = False
