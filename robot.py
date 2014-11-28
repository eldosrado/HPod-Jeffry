import time as tm
from leg import *
import numpy as np
import math as ma
from gaitEngine import *


class Robot(object):
    def __init__(self):
        # Platzhalter für die Gangliste
        self.__list = []
        # Listenlänge
        self.__list_lenth = 0
        # Zyklus Zeit
        self.__steptime = 0.15

        self.__bein = Legs()
        self.__walk = GaitEngine()
        self.__go = False
        self.__wakeup = True

    # Sendet die Liste an die Beinpaare
    def __sendListToBein(self, i=0):
        for o in range(0, 6, 2):
            self.__bein.setPos(o, self.__list[i])

        alt = int(len(self.__list) / 2)
        if i >= len(self.__list) / 2:
            i -= alt
        else:
            i += alt
        for o in range(1, 6, 2):
            self.__bein.setPos(o, self.__list[i])

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
        self.__list = self.__walk.getStartPos()
        self.__sendListToBein()
        tm.sleep(1)
        self.__bein.activate()

    # Stellt sich wieder in die ausgangposition hin // Senkt alle Beine
    def __setStandPos(self):
        self.__list = self.__walk.getStandPos()
        self.__sendListToBein()
        tm.sleep(1)
        self.__bein.activate()

    # Führt den eigentlichen Gang aus
    def __move(self):
        firstHalf = True
        while self.__go:
            # Startezeit aufnehmen
            t_start = tm.time()
            cycle = 0
            self.__list, self.__list_lenth = self.__walk.genList()

            # Unterscheiden Welche Beingruppe sich oben befindet
            if firstHalf:
                start, stop = 0, int(self.__list_lenth/2)
                firstHalf = False
            else:
                start, stop = int(self.__list_lenth/2), self.__list_lenth
                firstHalf = True

            for i in range(start, stop):
                # Sendet die Beinliste
                self.__sendListToBein(i)
                # Zyklus inkrement
                cycle += 1
                # Berechnung der restlichen Zykluszeit
                t_sleep = (self.__steptime * cycle) - (tm.time() - t_start)

                if t_sleep > 0:
                    tm.sleep(t_sleep)
                # Broadcast zum start der Bewegung der Servos
                self.__bein.activate()

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
        self.__walk.setAngle(angel)
        print("Winkel gesetzt zu:", angel)

    # Setzt ein Gangmodus
    # 0 = Dreick
    # 1 = Rechteck
    # 2 = Parabel
    def setMode(self, mode):
        modetext = self.__walk.setMode(mode)
        print("Geheform gesetzt zu:", modetext)

    # Ändert den Gangmode zu dem Nächsten
    def switchMode(self):
        self.__walk.switchMode()

    # Setzt die Anzahl der zwischenpunkte bei der Gangbewegung
    def setSpu(self, spu):
        self.__walk.setSpu(spu)
        print("steps per unit gesetzt zu:", spu)

    # Beendet das komplete Roboterporgramm
    def RobotSleep(self):
        self.__wakeup = False
