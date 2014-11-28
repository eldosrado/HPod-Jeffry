__author__ = 'Jeka'

import matplotlib.pyplot as plt
from matplotlib.patches import Circle, PathPatch
from mpl_toolkits.mplot3d import Axes3D
import mpl_toolkits.mplot3d.art3d as art3d
import numpy as np
import threading
import time as tm
from copy import copy


class my3DFig_th(threading.Thread):
    lock = threading.Lock()

    def __init__(self, punkte_anzahl, circle_pos):
        threading.Thread.__init__(self)

        my3DFig_th.lock.acquire()
        # Setzt die anzahl der Punkte
        self.__p_anzahl = punkte_anzahl
        self.__p_color = ['k'] * punkte_anzahl

        self.__t_start = tm.time()
        self.__t_end = tm.time()
        self.__t_interval = 0.01
        self.__t_step = 0.15

        # Erstellt ein 2D Plot-Modell(Figur) und setze es zu einem 3D Plot-Modell(Figur)
        self.__fig = plt.figure()
        self.__ax = self.__fig.gca(projection='3d')

        # Erstelle eine Puffer-Koordinatenliste
        #self.__xyz = [[0 for o in range(self.__p_anzahl)] for i in range(3)] ## alt
        self.__xyz_reg_ziel = np.zeros((3, self.__p_anzahl)).tolist()

        self.__xyz_ziel = np.zeros((3, self.__p_anzahl)).tolist()
        self.__xyz_start = np.zeros((3, self.__p_anzahl)).tolist()
        self.__xyz_temp = np.zeros((3, self.__p_anzahl)).tolist()

        # Setze die Label und die Grenzen der Koordinatensystems
        self.set_xyzlablim()

        # Lässt das Programm weiterlaufen während das Plotfenster noch offen ist
        plt.ion()

        # Drehung um die z-Achse und der neuen horizontal zum Sichpunkt schauenden Achse
        self.__ax.view_init(elev=40., azim=45)

        # Erstellt die Punkte
        self.__newPoints = self.__ax.scatter(self.__xyz_ziel[0], self.__xyz_ziel[1], self.__xyz_ziel[2], c=self.__p_color)

        # Läst die Kreise erstellen wenn ihre Positionen verfügbar sind
        if circle_pos is not None:
            self.initCircle(circle_pos)
            for i in range(len(circle_pos)):
                self.setLegPos(i, circle_pos[i])
        # Zeigt das Plotfester an
        self.__fig.show()

        my3DFig_th.lock.release()

    def set_xyzlablim(self, llabel=None, llimit=None):
        if llabel is None:
            self.__ax.set_xlabel('x->')
            self.__ax.set_ylabel('y->')
            self.__ax.set_zlabel('^z')
        else:
            self.__ax.set_xlabel(llabel[0])
            self.__ax.set_ylabel(llabel[1])
            self.__ax.set_zlabel(llabel[2])

        if llimit is None:
            self.__ax.set_xlim3d(-5, 5)
            self.__ax.set_ylim3d(-5, 5)
            self.__ax.set_zlim3d(-1, 4)
        else:
            self.__ax.set_xlim3d(llimit[0])
            self.__ax.set_ylim3d(llimit[1])
            self.__ax.set_zlim3d(llimit[2])

    # Anzahl der Beine setzen
    def set_anzahl(self, n):
        self.__p_anzahl = n
        self.__p_color = ['b'] * n

    def initCircle(self, mlist):
        """
        Funktion sur berechnung und Positionierung der Kreise in dem 3D-Plot
        :param mlist: ?????
        """
        if len(mlist) != self.__p_anzahl:
            print("initCircle:Error: Länge stimmt nicht überein!")
        else:
            for i in mlist:
                circle = Circle((i[0], i[1]), 1, color="b", alpha=0.5)
                self.__ax.add_patch(circle)
                art3d.pathpatch_2d_to_3d(circle, z=i[2])
            plt.draw()

    def run(self):
        arrived = False
        while True:
            if tm.time() > self.__t_end and arrived is not True:
                self.__newPoints.remove()
                self.__newPoints = self.__ax.scatter(self.__xyz_ziel[0], self.__xyz_ziel[1], self.__xyz_ziel[2], c=self.__p_color)
                plt.draw()
                arrived = True
            elif tm.time() < self.__t_end and arrived is True:
                self.__t_start = tm.time()
                arrived = False

            if arrived is not True:
                t = (self.__t_end - self.__t_start) / self.__t_step
                for i in range(self.__p_anzahl):
                    for o in range(3):
                        self.__xyz_temp[o][i] = (self.__xyz_ziel[o][i] * t) + (1. - t) * self.__xyz_start[o][i]

                self.__newPoints.remove()
                #self.__ax.scatter(self.__xyz_temp[0], self.__xyz_temp[1], self.__xyz_temp[2], c=self.__p_color)
                self.__newPoints = self.__ax.scatter(self.__xyz_temp[0], self.__xyz_temp[1], self.__xyz_temp[2], c=self.__p_color)
                plt.draw()
            #tm.sleep(0.001)

    def update(self):
        my3DFig_th.lock.acquire()
        self.__xyz_start = copy(self.__xyz_temp)
        self.__xyz_ziel = copy(self.__xyz_reg_ziel)
        self.__t_end = tm.time() + self.__t_step
        my3DFig_th.lock.release()


    def setLegPos(self, nr, xyz):
        try:
            temp = xyz.tolist()
        except:
            temp = xyz

        if nr < len(self.__xyz_reg_ziel[0]):
            for i in range(3):
                self.__xyz_reg_ziel[i][nr] = temp[i]

#######################################################################################################################


class my3DFig(object):
    def __init__(self, anzahl, zeroPos=None):
        """
        Plottet in einer 3D-Pespektive alles Fußposition und ihren Bodenkontakt
        :param anzahl: Anzahl der Füße
        :param zeroPos: Liste von Koordinaten wo der Bodenkontakt sein soll
        """
        # Definiert die anzahl der
        self.__anzahl = None
        self.setAnzahl(anzahl)

        # Erstellt ein 2D Plot-Modell(Figur)
        self.__fig = plt.figure()


        # Setzt es zu einem 3D Plot-Modell(Figur)
        self.__ax = self.__fig.gca(projection='3d')


        # Erstelle eine Puffer-Koordinatenliste
        self.__xyz = [[0 for o in range(anzahl)] for i in range(3)]

        # Setzt die Farbei für die Fuss-Punkte
        self.__color = ['k'] * anzahl

        # Setze die Label und die Grenzen der Koordinatensystems
        self.set_xyzlablim()

        # Lässt das Programm weiterlaufen während das Plotfenster noch offen ist
        plt.ion()

        # Drehung um die z-Achse und der neuen horizontal zum Sichpunkt schauenden Achse
        self.__ax.view_init(elev=40., azim=45)

        # Erstellt die Punkte
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
            self.__ax.set_xlim3d(-5, 5)
            self.__ax.set_ylim3d(-5, 5)
            self.__ax.set_zlim3d(-1, 4)
        else:
            self.__ax.set_xlim3d(llimit[0])
            self.__ax.set_ylim3d(llimit[1])
            self.__ax.set_zlim3d(llimit[2])

    # Anzahl der Beine setzen
    def setAnzahl(self, anzahl):
        """
        Setzt eine neue anzahl von Beinenspitzen(Punkten)
        :param anzahl: int -> neue Anzahl
        """
        self.__anzahl = anzahl
        self.__color = ['b'] * anzahl

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
        # print("__xyz", self.__xyz)
        self.__newPoints = self.__ax.scatter(self.__xyz[0], self.__xyz[1], self.__xyz[2], c=self.__color)
        plt.draw()

    def setLegPos(self, nr, mxyz):
        try:
            temp = mxyz.tolist()
        except:
            temp = mxyz

        if nr < len(self.__xyz[0]):
            for i in range(3): self.__xyz[i][nr] = temp[i]



