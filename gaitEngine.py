__author__ = 'Jeka'

import math as ma
from numpy import matrix, array
import numpy as np
import vector


# nur zur abkürzung in der Berechnungsmethode erstellt
def sin(angle):
    return ma.sin(ma.radians(angle))


# nur zur abkürzung in der Berechnungsmethode erstellt
def cos(angle):
    return ma.cos(ma.radians(angle))


# Berechnet die a,b,c Werte einer Parabelfunktion y = ax^2 + bx + c aus einer an der Y-Achse gespiegelten Parabel
# wobei b immer 0 ist. 
def fit_parabel(r, h):
    A = np.zeros((3, 3), dtype=np.float)
    x = np.array([-r, 0, r])
    y = np.array([0, h, 0])
    A[:, 0] = x ** 2
    A[:, 1] = x
    A[:, 2] = 1
    a, b, c = np.linalg.solve(A, y)
    return a, b, c


class GaitEngine(object):
    modetext = ["Dreieck", "Recheck", "Parabel"]

    def __init__(self):
        # Ein paar Standartparameter
        self.__MODE_MIN = 0
        self.__MODE_MAX = 2
        self.__HIGHT_MIN = 0.1
        self.__HIGHT_MAX = 0.2

        # Variable zur Erkennung für Änderungen
        self.__changes = True

        self.__mode = 2
        # Setzte die Adresse für die Gangart
        self.__modemethode = [self.__gangDreieck,
                              self.__gangRechteck,
                              self.__gangParabel]

        self.__angle = 0
        self.setAngle(0)
        self.__curangle = -1

        self.__h = 1.
        self.__r = 1.

        self.__spu = 4

        self.__list = []
        self.genList()

    def switchMode(self):
        if self.__mode > self.__MODE_MAX:
            self.__mode = 0
        else:
            self.__mode += 1
        self.__changes = True

    def setMode(self, mode=0):
        if self.__MODE_MAX >= mode:
            self.__mode = mode
        self.__changes = True
        return GaitEngine.modetext[self.__mode]

    def setAngle(self, angle):
        self.__angle = -angle
        self.__changes = True

    # Setze Stepps per Unit
    def setSpu(self, spu):
        if spu > 0:
            self.__spu = spu
        self.__changes = True

    # Erhöhe die Fushebehöhe
    def incHight(self, diff=0.5):
        self.__h += diff
        self.__changes = True

    # Verringere die Fußhebehöhe
    def decHight(self, diff=0.5):
        self.__h -= diff
        self.__changes = True

    # Setze der Fußhebehöhe ein bestimmten wert
    def setHigh(self, h):
        self.__h = h
        self.__changes = True

    # Erstellt eine Liste für von der der Roboter dann starten kann zu gehen
    def getStartPos(self):
        self.__list = []
        self.__list += [np.array([0, 0, 0])]
        self.__list += [np.array([0, 0, self.__h])]
        self.__changes = True
        return self.__list

    # Erstellt einel Liste mit allen Fußpositionen auf dem Boden
    def getStandPos(self):
        self.__list = []
        self.__list += [np.array([0, 0, 0])]
        self.__list += [np.array([0, 0, 0])]
        self.__changes = True
        return self.__list

    # Erstellt eine Gangliste mit Dreieckbewegung
    def __gangDreieck(self):
        self.__list = []
        angle = self.__angle

        x = cos(angle) * self.__r
        y = sin(angle) * self.__r
        for i in range(1, self.__spu + 1):
            v = i / self.__spu
            self.__list += [array([x, y, 0]) * v]

        for i in range(self.__spu - 1, -1, -1):
            v = i / self.__spu
            x = cos(angle) * self.__r * v
            y = sin(angle) * self.__r * v
            hyp = ma.sqrt(x**2 + y**2)
            z = (1 - hyp / self.__r) * self.__h
            self.__list += [array([x, y, z])]

        for i in range(-1, -self.__spu - 1, -1):
            v = i / self.__spu
            x = cos(angle) * self.__r * v
            y = sin(angle) * self.__r * v
            hyp = ma.sqrt(x**2 + y**2)
            z = (1 - hyp / self.__r) * self.__h
            self.__list += [array([x, y, z])]

        x = cos(angle) * self.__r
        y = sin(angle) * self.__r
        for i in range(-self.__spu + 1, 1):
            v = i / self.__spu
            self.__list += [array([x, y, 0]) * v]

    def __gangRechteck(self):
        self.__list = []
        angle = self.__angle

        # Anfang: Bodenkontakt
        # Bewegung nach hinten (Vorwärtsbewegung)
        x = cos(angle) * self.__r
        y = sin(angle) * self.__r
        for i in range(1, self.__spu * 2 + 1):
            v = i / self.__spu / 2
            self.__list += [array([x, y, 0]) * v]

        # Bein anheben
        for i in range(self.__spu):
            v = (i+1) / self.__spu
            z = self.__h * v
            self.__list += [array([x, y, z])]

        # Bein in der Luft nach vorne bewegen
        z = self.__h
        for i in range(self.__spu - 1, -self.__spu - 1, -1):
            v = i/self.__spu
            x = cos(angle) * self.__r * v
            y = sin(angle) * self.__r * v
            self.__list += [array([x, y, z])]

        # Bein absetzen
        x = -cos(angle) * self.__r
        y = -sin(angle) * self.__r
        for i in range(self.__spu - 1, -1, -1):
            v = i / self.__spu
            z = self.__h * v
            self.__list += [array([x, y, z])]

        # Bein zur Startposition bewegen
        x = cos(angle) * self.__r
        y = sin(angle) * self.__r
        for i in range(-self.__spu * 2 + 1, 1):
            v = i / self.__spu / 2
            self.__list += [array([x, y, 0]) * v]

    def __gangParabel(self):
        self.__list = list()
        angle = self.__angle

        x = cos(angle) * self.__r
        y = sin(angle) * self.__r
        for i in range(1, self.__spu + 1):
            v = i / self.__spu
            self.__list += [array([x, y, 0]) * v]

        for i in range(self.__spu - 1, -self.__spu - 1, -1):
            v = i/self.__spu
            x = cos(angle) * self.__r * v
            y = sin(angle) * self.__r * v
            a, b, c = fit_parabel(self.__r, self.__h)
            hyp = ma.sqrt(x**2+y**2)
            z = a*(hyp**2) + b*hyp + c
            self.__list += [array([x, y, z])]

        x = cos(angle) * self.__r
        y = sin(angle) * self.__r
        for i in range(-self.__spu + 1, 1):
            v = i / self.__spu
            self.__list += [array([x, y, 0]) * v]

    def genList(self):
        if self.__changes:
            self.__changes = False
            self.__modemethode[self.__mode]()
        return self.__list, len(self.__list)

    def getList(self):
        return self.__list
