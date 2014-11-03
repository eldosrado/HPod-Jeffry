__author__ = 'Jeka'
import my3Dplot as mPlt
from numpy import matrix


class Leg(object):
    anzahl = 0

    def __init__(self, offset=matrix([[0], [0], [0]])):
        self.nr = Leg.anzahl
        #print(self.nr)
        Leg.anzahl += 1

        self.Pos = matrix([[0], [0], [0]])
        self.Offset = matrix([[0], [0], [0]])
        self.setOff(offset)
        self.Pos = offset

    def setOff(self, offset=matrix([[0], [0], [0]])):
        self.Offset = offset
        self._legPos()

    def setPos(self, Plot3D=None, pos=matrix([[0], [0], [0]])):
        self.Pos = pos
        self._legPos(Plot3D)

    def _legPos(self, Plot3D=None):
        self.legPos = self.Pos + self.Offset
        if Plot3D is not None:
            Plot3D.setLegPos(self.nr, self.legPos)
            # mPlt.setLegPos(self.nr, self.legPos)

    def getPos(self):
        return self.legPos

    def activate(self):
        print(self.nr, "Bein ->", self.Pos)

    def __str__(self):
        return 'leg%d %2f %2d %2d' % (self.nr, self.Pos[0, 0], self.Pos[1, 0], self.Pos[2, 0])


class Legs(object):
    def __init__(self):
        self.leg = []
        offset = [matrix([[3], [-2], [-1]]),
                  matrix([[0], [-3], [-1]]),
                  matrix([[-3], [-2], [-1]]),
                  matrix([[-3], [2], [-1]]),
                  matrix([[0], [3], [-1]]),
                  matrix([[3], [2], [-1]])]

        self.P3D = mPlt.my3DFig(6, offset)
        for i in range(6):
            self.leg.append(Leg(offset[i]))

    def setPos(self, nr, pos):
        """
        Übergebe einem Bein(nr) eine neue Positzion
        :param nr: Nummer des Bein von 0 bis 5
        :param pos: neue Position in eine 1x3 Matrix x,y,z
        """
        self.leg[nr].setPos(Plot3D=self.P3D, pos=pos)

    def activate(self):
        self.P3D.update()

    def __str__(self):
        string = ""
        for i in range(6):
            string += "%4d" % i
        string += "\n"
        for o in range(3):
            for i in range(6):
                string += "%4.1f" % self.leg[i].getPos()[o, 0]
            string += "\n"
        return string

