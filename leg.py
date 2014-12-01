__author__ = 'Jeka'
import my3Dplot as mPlt
from numpy import array


class Leg(object):
    anzahl = 0
    M3P = None

    def __init__(self, offset=array([0, 0, 0])):
        self.__nr = Leg.anzahl
        Leg.anzahl += 1

        self.__pos_offset = offset
        self.__pos = offset
        self.__legPos = None
        self.__calc_legPos()

    def getNr(self):
        return self.__nr

    def setOff(self, offset=array([0, 0, 0])):
        self.__pos_offset = offset
        self.__calc_legPos()

    def setPos(self, pos=array([0, 0, 0]), Plot3D=None, speed=0.15):
        self.__pos = pos
        self.__calc_legPos(Plot3D)

    def __calc_legPos(self, Plot3D=None, speed=0.15):
        self.__legPos = self.__pos + self.__pos_offset
        if Plot3D is not None:
            Plot3D.setLegPos(self.__nr, self.__legPos)

    def getPos(self):
        return self.__legPos

    def getPosAsList(self):
        return self.__legPos.tolist()

    @staticmethod
    def activate(my3DPlot=None):
        if Leg.M3P is not None:
            Leg.M3P.update()
        elif my3DPlot is not None:
            my3DPlot.update()
