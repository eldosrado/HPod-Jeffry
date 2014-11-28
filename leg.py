__author__ = 'Jeka'
import my3Dplot as mPlt
from numpy import array


class Leg(object):
    anzahl = 0

    def __init__(self, offset=array([0, 0, 0])):
        self.nr = Leg.anzahl
        #print(self.nr)
        Leg.anzahl += 1

        self.Pos = array([0, 0, 0])
        self.Offset = array([0, 0, 0])
        self.setOff(offset)
        self.Pos = offset

    def getNr(self):
        return self.nr

    def setOff(self, offset=array([0, 0, 0])):
        self.Offset = offset
        self._legPos()

    def setPos(self, Plot3D=None, pos=array([0, 0, 0])):
        self.Pos = pos
        self._legPos(Plot3D)

    def _legPos(self, Plot3D=None):
        self.legPos = self.Pos + self.Offset
        if Plot3D is not None:
            Plot3D.setLegPos(self.nr, self.legPos)

    def getPos(self):
        return self.legPos

    def getPosAsList(self):
        return self.legPos.tolist()

    def activate(self):
        print(self.nr, "Bein ->", self.Pos)

    def __str__(self):
        return 'leg%d %2f %2d %2d' % (self.nr, self.Pos[0, 0], self.Pos[1, 0], self.Pos[2, 0])


class Legs(object):
    def __init__(self):
        self.__plot = True
        self.leg = []
        offset = [array([3, -2, -1]),
                  array([0, -3, -1]),
                  array([-3, -2, -1]),
                  array([-3, 2, -1]),
                  array([0, 3, -1]),
                  array([3, 2, -1])]

        if self.__plot:
            debug = False
            if not debug:
                self.P3D = mPlt.my3DFig(6, offset)
            else:
                self.P3D = mPlt.my3DFig_th(6, offset)
                self.P3D.start()

        for i in range(6):
            self.leg.append(Leg(offset[i]))

    def setPos(self, nr, pos, speed = 0):
        """
        Übergebe einem Bein(nr) eine neue Positzion
        :param nr: Nummer des Bein von 0 bis 5
        :param pos: neue Position in eine 1x3 array x,y,z
        """
        if self.__plot:
            self.leg[nr].setPos(Plot3D=self.P3D, pos=pos)

        self.leg[nr].setPos(pos=pos)

    def activate(self):
        if self.__plot: self.P3D.update()
        temp = ""
        stringarray = ["+ ",
                       "x ",
                       "y ",
                       "z "]
        for i in self.leg:
            stringarray[0] += " B%d   " % i.getNr()
            for o in range(1, 4):
                stringarray[o] += "%5.2f " % i.getPosAsList()[o-1]
        for s in stringarray:
            temp += s + "\n"
        return temp

    def __str__(self):
        temp = ""
        stringarray = ["+ ",
                       "x ",
                       "y ",
                       "z "]
        for i in self.leg:
            stringarray[0] += " B%d   " % i.getNr()
            for o in range(1, 4):
                stringarray[o] += "%5.2f " % i.getPosAsList()[o-1]
        for s in stringarray:
            temp += s + "\n"
        return temp
