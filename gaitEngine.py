__author__ = 'Jeka'

import math as ma
from numpy import matrix, array
import numpy as np
from vector import vector
from copy import copy


# nur zur abkürzung in der Berechnungsmethode erstellt
def sin(angle):
    """ Berechnet ein Sinus-Wert

    :param angle: Winkel in Grad
    """
    return ma.sin(ma.radians(angle))


# nur zur abkürzung in der Berechnungsmethode erstellt
def cos(angle):
    """ Berechnet ein Cosinus-Wert

    :param angle: Winkel in Grad
    """
    return ma.cos(ma.radians(angle))


# Berechnet die a,b,c Werte einer Parabelfunktion y = ax^2 + bx + c aus einer an der Y-Achse gespiegelten Parabel
# wobei b immer 0 ist. 
def fit_parabel(r, h):
    """ Berechnet aus aus Höhe und posetiver Nullstelle eine Parabel

    :param r: posetive Nullstelle der Parabel
    :param h: Höhe der Parabel
    :return: a,b,c aus der Formel ax^2 + bx + c
    """
    A = np.zeros((3, 3), dtype=np.float)
    x = np.array([-r, 0, r])
    y = np.array([0, h, 0])
    A[:, 0] = x ** 2
    A[:, 1] = x
    A[:, 2] = 1
    a, b, c = np.linalg.solve(A, y)
    return a, b, c


class GaitEngine(object):
    """
    Objekt zur Berechnung der Fußpunkte für die verschiedenen Gangarten
    """
    modetext = ["Dreieck", "Recheck", "Parabel"]

    def __init__(self):
        # Variable zur Erkennung für Änderungen
        self.__changes = True

        self.__mode = 2
        # Setzte die Adresse für die Gangart
        self.__modemethode = [self.__gangDreieck,
                              self.__gangRechteck,
                              self.__gangParabel]

        # Ein paar Standartparameter
        self.__MODE_MIN = 0
        self.__MODE_MAX = len(self.__modemethode)

        self.__angle = 0
        self.setAngle(0)
        #self.__curangle = -1

        self.__h = 1.
        self.__r = 1.

        self.__spu = 4

        self.__list = []
        #self.genList()

    def switchMode(self):
        """
        Schaltet aufs Nächste Gangart um
        """
        if self.__mode >= self.__MODE_MAX:
            self.__mode = 0
        else:
            self.__mode += 1
        self.__changes = True

    def setMode(self, mode):
        """
        Stellt eine bestimmte Gangart fest
        0 = Dreiecksgang
        1 = Rechteckgang
        2 = Parabelgang
        :param mode: Gangart zum setzen
        """
        if self.__MODE_MAX >= mode:
            self.__mode = mode
        self.__changes = True
        return GaitEngine.modetext[self.__mode]

    def setAngle(self, angle):
        """
        Winkel in welche richtung der Roboter sich bewegen soll
        :param angle: Winkel der Gangrichtung (0°=>Gradeaus)
        """
        self.__angle = -angle
        self.__changes = True

    # Setze Stepps per Unit
    def setSpu(self, spu):
        """
        Setzt die Anzahl der zwischenpunkte von einem Extrempunkt zum nächsten Extrempunkt
        1=> minimale Punkteanzahl

        :param spu: Setzt die Anzahl der zwischenpunkte bei der Gangbewegung
        """
        if spu > 0:
            self.__spu = spu
            self.__changes = True

    # Erhöhe die Fushebehöhe
    def incHight(self, diff=0.5):
        """
        Erhöt die Gang-Bein-Hebe-Höhe
        :param diff: Wert um welchen das Bein erhöt werden soll
        :return:
        """
        self.__h += diff
        self.__changes = True

    # Verringere die Fußhebehöhe
    def decHight(self, diff=0.5):
        """
        Vermindert die Gang-Bein-Hebe-Höhe
        :param diff: Wert um welchen das Bein gesenkt werden soll
        :return:
        """
        if self.__h - diff > 0:
            self.__h -= diff
            self.__changes = True

    # Setze der Fußhebehöhe ein bestimmten wert
    def setHigh(self, h):
        """
        Setze der Fußhebehöhe ein bestimmten wert
        :param h: Setzt ein bestimmten Höhe
        """
        self.__h = h
        self.__changes = True

    # Erstellt eine Liste mit den StartPositionen, jeweils für A und für B
    def getStartPos(self):
        """
        Erstellt eine Liste mit den StartPositionen, jeweils für BeinGruppe A und für B
        :return: Gibt eine Liste mit den StartPositionen, jeweils für BeinGruppe A und für B zurück
        """
        self.__list = []
        self.__list += [np.array([0, 0, 0])]
        self.__list += [np.array([0, 0, self.__h])]
        self.__changes = True
        return self.__list

    # Erstellt einel Liste mit allen Fußpositionen auf dem Boden
    def getStandPos(self):
        """
        Erstellt einel Liste mit allen Fußpositionen auf dem Boden
        :return:
        """
        self.__list = []
        self.__list += [np.array([0, 0, 0])]
        self.__list += [np.array([0, 0, 0])]
        self.__changes = True
        return self.__list

    # Erstellung der Gangpunkte für den Dreiecksgang
    def __gangDreieck_vec(self):
        liste = [vector()]
        angle = self.__angle

        x = cos(angle) * self.__r
        y = sin(angle) * self.__r
        z = self.__h

        # Nochmal der gleiche Code aber etwas verkürztz
        ######
        # Liste mit aus allen benötigten Vektoren
        vecs = [vector(x, y, 0),
                vector(-x, -y, z),
                vector(-x, -y, -z),
                vector(x, y, 0)]

        for v in vecs:
            vec = v / self.__spu
            [liste.append(vec + liste[-1]) for i in range(self.__spu)]

        self.__list = copy(liste[1:])

    # Code zur Erstellung der Gangpunkte für den Dreiecksgang
    def __gangDreieck(self):
        liste = [array([0., 0., 0.])]
        angle = self.__angle

        x = cos(angle) * self.__r
        y = sin(angle) * self.__r
        z = self.__h

        # Liste mit allen benötigten Vektoren
        vecs = [array([x, y, 0]),
                array([-x, -y, z]),
                array([-x, -y, -z]),
                array([x, y, 0])]

        for v in vecs:
            vec = v / self.__spu
            [liste.append(vec + liste[-1]) for i in range(self.__spu)]

        self.__list = copy(liste[1:])

    # Code zur Erstellung der Gangpunkte für den Rechteckgang
    def __gangRechteck(self):
        liste = [array([0., 0., 0.])]
        angle = self.__angle

        x = cos(angle) * self.__r
        y = sin(angle) * self.__r
        z = self.__h

        vec_ground = array([x, y, 0.])
        vecs = [array([0., 0., z]),
                array([-x, -y, 0.]),
                array([-x, -y, 0.]),
                array([0., 0., -z])]

        # Listenerstellung der Gangpositionen vom x=y=z=0 bei Bodenkontakt
        [liste.append((vec_ground / (self.__spu * 2)) + liste[-1]) for i in range(self.__spu * 2)]

        # Listenerstellung der Gangpositionen ohne Bodenkontakt
        for v in vecs:
            vec = v / self.__spu
            [liste.append(vec + liste[-1]) for i in range(self.__spu)]

        # Listenerstellung der Gangpositionen zur Position x=y=z=0 bei Bodenkontakt
        [liste.append((vec_ground / (self.__spu * 2)) + liste[-1]) for i in range(self.__spu * 2)]

        self.__list = copy(liste[1:])

    # Code zur Erstellung der Gangpunkte für den Parabelgang
    def __gangParabel(self):
        liste = [array([0., 0., 0.])]
        angle = self.__angle

        x_max = cos(angle) * self.__r
        y_max = sin(angle) * self.__r

        vec = array([x_max, y_max, 0]) / self.__spu
        [liste.append(vec + liste[-1]) for i in range(self.__spu)]

        for i in range(self.__spu - 1, -self.__spu - 1, -1):
            v = i/self.__spu
            x = x_max * v
            y = y_max * v
            a, b, c = fit_parabel(self.__r, self.__h)
            hyp = ma.sqrt(x**2+y**2)
            z = a*(hyp**2) + b*hyp + c
            liste.append(array([x, y, z]))

        [liste.append(vec + liste[-1]) for i in range(self.__spu)]

        self.__list = copy(liste[1:])

    def genList(self):
        if self.__changes:
            self.__changes = False
            self.__modemethode[self.__mode]()
        return self.__list
