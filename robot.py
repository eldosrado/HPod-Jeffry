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
        self.__list_length = 0
        # Zyklus Zeit
        self.__steptime = 0.15

        self.__plot = True
        self.__legs = []
        offset = [array([3, -2, -1]),
                  array([0, -3, -1]),
                  array([-3, -2, -1]),
                  array([-3, 2, -1]),
                  array([0, 3, -1]),
                  array([3, 2, -1])]

        ##### Hilfsmittel zur Darsellung der Beine >>>>>
        if self.__plot:
            debug = True
            if not debug:
                self.P3D = mPlt.my3DFig(6, offset)
            else:
                self.P3D = mPlt.my3DFig_th(6, offset)
                self.P3D.start()

        for i in range(6):
            self.__legs.append(Leg(offset[i]))
        # <<<<<<<<

        self.__gait = GaitEngine()
        self.__go = False
        self.__wakeup = True

    # Sendet die Liste an die Beinpaare
    def __sendListToBein(self, step=0):
        """ Sendet aus eine Positions-Liste an die zwei Bein-Gruppen

        :param step: Positions-Listen index
        """
        for o in range(0, 6, 2):
            self.__legs[o].setPos(pos=self.__list[step], Plot3D=self.P3D)

        half_l = int(len(self.__list) / 2)
        for o in range(1, 6, 2):
            self.__legs[o].setPos(pos=self.__list[step - half_l], Plot3D=self.P3D)

    # Roboters Hauptschleife
    def wakeup(self):
        """ Hauptschleife von der Roboter_Klasse

        """
        self.__setStandPos()
        while self.__wakeup:
            if self.__go:
                self.__setGoPos()
                self.__move()
                self.__setStandPos()

    # Beretet sich vor um loszugehen // Hebt eine Beingruppe an
    def __setGoPos(self):
        """ Bereitet sich zum loszugehen vor // Hebt eine Beingruppe an

        """
        self.__list = self.__gait.getStartPos()
        self.__sendListToBein()
        tm.sleep(1)
        Leg.activate(self.P3D)

    # Stellt sich wieder in die ausgangposition hin // Senkt alle Beine
    def __setStandPos(self):
        """ Stellt sich wieder in die ausgangposition hin // Senkt alle Beine

        """
        self.__list = self.__gait.getStandPos()
        self.__sendListToBein()
        tm.sleep(1)
        Leg.activate(self.P3D)

    # gibt eine Listen von Beinpositionen zurück
    def get_allLegPos(self):
        """ gibt alle Beinpositionen zurück

        :return: gibt eine Listen von Beinpositionen zurück
        """
        return [self.__legs[i].getPos() for i in range(6)]

    # Führt den eigentlichen Gang aus
    def __move(self):
        """ Führt den eigentlichen Gang aus

        """
        firstHalf = True
        t_temp = tm.time()
        while self.__go:
            # Startezeit aufnehmen
            self.__list = self.__gait.genList()
            self.__list_length = len(self.__list)

            # Unterscheiden Welche Beingruppe sich oben befindet
            if firstHalf:
                start, stop = 0, int(self.__list_length/2)
                firstHalf = False
            else:
                start, stop = int(self.__list_length/2), self.__list_length
                firstHalf = True

            for i in range(start, stop):
                # Sendet die Beinliste
                self.__sendListToBein(i)

                # Berechnung der restlichen Zykluszeit
                # schlaf_zeit = soll_zeit            -  ist_zeit
                t_sleep = (self.__steptime + t_temp) - tm.time()

                if t_sleep > 0:
                    tm.sleep(t_sleep)
                t_temp = tm.time()
                # Broadcast zum start der Bewegung der Servos
                Leg.activate(self.P3D)

    # Methode um den Roboter wieder stillstehen zu lassen
    def stop(self):
        """ Methode um den Roboter wieder stillstehen zu lassen

        """
        print('stop move')
        self.__go = False

    # Startet den Gehvorgang
    def start(self):
        """ Startet den Gehvorgang

        """
        print('start move')
        self.__go = True

    # Winkel in welche richtung der Roboter sich bewegen soll
    def setAngle(self, angle):
        """ Winkel in welche richtung der Roboter sich bewegen soll

        :param angle: Winkel der Gangrichtung (0°=>Gradeaus)
        """
        self.__gait.setAngle(angle)
        print("Winkel gesetzt zu:", angle)

    # Setzt ein Gangmodus
    # 0 = Dreick
    # 1 = Rechteck
    # 2 = Parabel
    def setMode(self, mode):
        """ Setzt ein Gangmodus
        0 = Dreick
        1 = Rechteck
        2 = Parabel

        :param mode: zum setzen des Gangart
        """
        modetext = self.__gait.setMode(mode)
        print("Geheform gesetzt zu:", modetext)

    # Ändert den Gangmode zu dem Nächsten
    def switchMode(self):
        """ Ändert den Gangmode zu dem Nächsten

        """
        self.__gait.switchMode()

    # Setzt die Anzahl der zwischenpunkte bei der Gangbewegung
    def setSpu(self, spu):
        """ Setzt die Anzahl der zwischenpunkte von einem Extrempunkt zum nächsten Extrempunkt
        1=> minimale Punkteanzah

        :param spu: Setzt die Anzahl der zwischenpunkte bei der Gangbewegung
        """
        self.__gait.setSpu(spu)
        print("steps per unit gesetzt zu:", spu)

    # Beendet das komplete Roboterporgramm
    def RobotSleep(self):
        """ Beendet das komplete Roboterporgramm

        """
        self.__go = False
        self.__wakeup = False
