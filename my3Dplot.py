__author__ = 'Jeka'

import matplotlib.pyplot as plt
from matplotlib.patches import Circle, PathPatch
from mpl_toolkits.mplot3d import Axes3D
import mpl_toolkits.mplot3d.art3d as art3d
import time
import numpy as np



class my3DFig(object):
    def __init__(self, anzahl, zeroPos=None):
        """
        Plottet in einer 3D-Pespektive alles Fußposition und ihren Bodenkontakt
        :param anzahl: Anzahl der Füße
        :param zeroPos: Liste von Koordinaten wo der Bodenkontakt sein soll
        """
        # Definiert die anzahl der Beine
        self.__anzahl = anzahl

        # Erstellt ein 2D Plot-Modell(Figur)
        self.__fig = plt.figure()

        # Setzt es zu einem 3D Plot-Modell(Figur)
        self.__ax = self.__fig.gca(projection='3d')

        # Erstelle eine Puffer-Koordinatenliste
        self.__xyz = [np.zeros(anzahl), np.zeros(anzahl), np.zeros(anzahl)]

        # Setzt die Farbei für die Fuss-Punkte
        self.__color = ['k'] * self.__anzahl

        # Setze die Label und die Grenzen der Koordinatensystems
        self.set_xyzlablim()

        # Lässt das Programm weiterlaufen während das Plotfenster noch offen ist
        plt.ion()

        # Drehung um die z-Achse und der neuen horizontal zum Sichpunkt schauenden Achse
        self.__ax.view_init(elev=40., azim=45)

        # Erstellt
        self.__newPoints = self.__ax.scatter(self.__xyz[0], self.__xyz[1], self.__xyz[2], c=self.__color)

        # Läst die Kreise erstellen wenn ihre Positionen verfügbar sind
        if zeroPos is not None:
            self.initCircle(zeroPos)
            for i in range(len(zeroPos)):
                self.setLegPos(i, zeroPos[i])
        # Zeigt das Plotfester an
        self.__fig.show()

    def set_xyzlablim(self, llabel=None, llimit=None):
        """
        Setze die Label und die Grenzen der Koordinatensystems
        :param llabel: Eine String-Liste für x, y, z Koordinaten
        :param llimit: Liste von tupeln mit (a)minimas und (b)maximas für x,y,z Koordiantensystem
                        llimit=[[xa,xb],[ya,yb],[za,zb]]
        """
        if llabel is None:
            self.__ax.set_xlabel('x->')
            self.__ax.set_ylabel('y->')
            self.__ax.set_zlabel('^z')
        else:
            self.__ax.set_xlabel(llabel[0])
            self.__ax.set_ylabel(llabel[1])
            self.__ax.set_zlabel(llabel[2])

        if llimit is None:
            self.__ax.set_xlim3d(-4, 4)
            self.__ax.set_ylim3d(-4, 4)
            self.__ax.set_zlim3d(-3, 1)
        else:
            self.__ax.set_xlim3d(llimit[0])
            self.__ax.set_ylim3d(llimit[1])
            self.__ax.set_zlim3d(llimit[2])

    def setAnzahl(self, anzahl):
        """
        Setzt eine neue anzahl von Beinenspitzen(Punkten)
        :param anzahl: int -> neue Anzahl
        """
        self.__anzahl = anzahl
        self.__color = ['k'] * anzahl

    def initCircle(self, mlist):
        """
        Funktion sur berechnung und Positionierung der Kreise in dem 3D-Plot
        :param mlist: ?????
        """
        if len(mlist) != self.__anzahl:
            print("initCircle:Error: Länge stimmt nicht überein!")
        else:
            for i in mlist:
                circle = Circle((i[0], i[1]), 1, color="b", alpha=0.5)
                self.__ax.add_patch(circle)
                art3d.pathpatch_2d_to_3d(circle, z=i[2])
            plt.draw()

    def update(self):
        """
        Aktualisiere die Punkte auf der Anzeige
        """
        self.__newPoints.remove()
        self.__newPoints = self.__ax.scatter(self.__xyz[0], self.__xyz[1], self.__xyz[2], c=self.__color)
        plt.draw()

    def setLegPos(self, nr, mxyz):
        for i in range(3):
            self.__xyz[i][nr] = mxyz[i]
