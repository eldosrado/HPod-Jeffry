__author__ = 'Jeka'

import robot
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import mlab
import threading as th
from time import sleep, time
from vector import vector


def main():
    smode = "Enter = Abbruch\n" \
            "0 = Start/Stop\n" \
            "1 = set Winkel\n" \
            "2 = set Mode\n" \
            "3 = set StepsPerUnit\n"

    r = robot.Robot()
    t = th.Thread(target=r.wakeup)
    t.start()
    i = 1
    go = False
    while i >= 0:
        print(smode)
        try:
            i = int(input())
        except ValueError as e:
            r.stop()
            r.RobotSleep()
            exit()

        if i == 0:
            if go:
                r.stop()
                go = False
            else:
                r.start()
                go = True
        elif i == 1:
            print('Gib den neuen Winkel ein: ')
            temp = int(input())
            r.setAngel(temp)
        elif i == 2:
            print('0=Dreieck-Gang\n1=Rechteckgang\n2=Parabelgang\n')
            temp = int(input())
            r.setMode(temp)
        elif i == 3:
            print("Gib die genauigkeit der schritte an: ")
            temp = int(input())
            r.setSpu(temp)

if __name__ == '__main__':
    pass
    main()

"""
v = vector()
v2 = vector(5, 5, 5)
print(v2.length())
print(v2.length2())
"""
