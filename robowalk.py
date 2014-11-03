__author__ = 'Jeka'

import math as ma
from numpy import matrix, array
import numpy as np


def sin(angle):
    return ma.sin(ma.radians(angle))


def cos(angle):
    return ma.cos(ma.radians(angle))


def fit_parabola(x, y):
    """Fits the equation "y = ax^2 + bx + c" given exactly 3 points as two
    lists or arrays of x & y coordinates"""
    A = np.zeros((3, 3), dtype=np.float)
    A[:, 0] = x ** 2
    A[:, 1] = x
    A[:, 2] = 1
    a, b, c = np.linalg.solve(A, y)
    return a, b, c


def fit_parabel(r, h):
    A = np.zeros((3, 3), dtype=np.float)
    x = np.array([-r, 0, r])
    y = np.array([0, h, 0])
    A[:, 0] = x ** 2
    A[:, 1] = x
    A[:, 2] = 1
    a, b, c = np.linalg.solve(A, y)
    return a, b, c


class Walk(object):
    modetext = ["Dreieck", "Recheck", "Parabel"]

    def __init__(self):
        self.__MODE_MIN = 0
        self.__MODE_MAX = 2
        self.__HIGHT_MIN = 0.1
        self.__HIGHT_MAX = 0.2

        self.__mode = 1
        self.__curmode = -1
        self.__initMode()

        self.__angle = 0
        self.setAngle(0)
        self.__curangle = -1

        self.__h = 1.
        self.__r = 1.

        self.__spu = 4
        self.__curspu = 0

        self.__list = []
        self.genList()

    def __initMode(self):
        self.__modemethode = [self.__gangDreieck,
                              self.__gangRechteck,
                              self.__gangParabel]

    def switchMode(self):
        if self.__mode >= 2:
            self.__mode = 0
        else:
            self.__mode += 1

    def setMode(self, mode=0):
        if self.__MODE_MAX >= mode:
            self.__mode = mode
        return Walk.modetext[self.__mode]

    def setAngle(self, angle):
        self.__angle = -angle

    def setSpu(self, spu):
        if spu > 0:
            self.__spu = spu

    def setHigh(self, h):
        self.__h = h


    def getStartPos(self):
        self.__list = []
        self.__list += [np.array([0, 0, 0])]
        self.__list += [np.array([0, 0, self.__h])]
        self.__curmode = -1
        return self.__list

    def getStandPos(self):
        self.__list = []
        self.__list += [np.array([0, 0, 0])]
        self.__list += [np.array([0, 0, 0])]
        self.__curmode = -1
        return self.__list

    def __gangDreieck(self):
        self.__list = []
        angle = self.__angle

        for i in range(self.__spu):
            self.__list += [array([[cos(angle) * self.__r],
                                   [sin(angle) * self.__r],
                                   [0]]) / self.__spu * (i + 1)]
        for i in range(self.__spu):
            self.__list += [array([[-cos(angle)] * self.__r,
                                   [-sin(angle)] * self.__r,
                                   [self.__h]]) / self.__spu + self.__list[len(self.__list) - 1]]
        for i in range(self.__spu):
            self.__list += [array([[-cos(angle)] * self.__r,
                                   [-sin(angle)] * self.__r,
                                   [-self.__h]]) / self.__spu + self.__list[len(self.__list) - 1]]
        for i in range(self.__spu):
            self.__list += [array([[cos(angle) * self.__r],
                                   [sin(angle) * self.__r],
                                   [0]]) / self.__spu + self.__list[len(self.__list) - 1]]

    def __gangRechteck(self):
        self.__list = []
        angle = self.__angle
        for i in range(self.__spu * 2):
            self.__list += [array([[cos(angle) * self.__r],
                                   [sin(angle) * self.__r],
                                   [0]]) / (self.__spu * 2) * (i + 1)]
        for i in range(self.__spu):
            self.__list += [array([[0], [0], [self.__h]]) / self.__spu + self.__list[len(self.__list) - 1]]
        for i in range(self.__spu * 2):
            self.__list += [array([[-cos(angle) * self.__r],
                                   [-sin(angle) * self.__r],
                                   [0]]) / self.__spu + self.__list[len(self.__list) - 1]]
        for i in range(self.__spu):
            self.__list += [array([[0], [0], [-self.__h]]) / self.__spu + self.__list[len(self.__list) - 1]]
        for i in range(self.__spu * 2):
            self.__list += [array([[cos(angle) * self.__r],
                                   [sin(angle) * self.__r],
                                   [0]]) / (self.__spu * 2) + self.__list[len(self.__list) - 1]]
        for i in self.__list:
            print(i)
        pass

    def __gangParabel(self):
        self.__list = []
        angle = self.__angle

        x = cos(angle) * self.__r
        y = sin(angle) * self.__r
        for i in range(1, self.__spu + 1):
            v = i / self.__spu
            self.__list += [array([[x], [y], [0]]) * v]

        for i in range(self.__spu - 1, -self.__spu - 1, -1):
            v = i/self.__spu
            x = cos(angle) * self.__r * v
            y = sin(angle) * self.__r * v
            a, b, c = fit_parabel(self.__r, self.__h)
            hyp = ma.sqrt(x**2+y**2)
            z = a*(hyp**2) + b*hyp + c
            self.__list += [array([[x], [y], [z]])]

        x = cos(angle) * self.__r
        y = sin(angle) * self.__r
        for i in range(-self.__spu + 1, 1):
            v = i / self.__spu
            self.__list += [array([[x], [y], [0]]) * v]

        for i in self.__list:
            print(i)
        pass

    def genList(self):
        if self.__mode != self.__curmode or self.__angle != self.__curangle or self.__spu != self.__curspu:
            self.__curmode = self.__mode
            self.__curangle = self.__angle
            self.__curspu = self.__spu
            self.__modemethode[self.__mode]()
        return self.__list

    def getList(self):
        return self.__list
