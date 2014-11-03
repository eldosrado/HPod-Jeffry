__author__ = 'Jeka'

import robot
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import mlab
import threading as th
from time import sleep, time


def main():
    smode = "0 = Exit\n" \
            "1 = set Winkel\n" \
            "2 = set Mode\n" \
            "3 = set StepsPerUnit\n"

    r = robot.Robot()
    t = th.Thread(target=r.go)
    t.start()
    i = 1
    #go = False
    while i >= 0:
        print(smode)
        try:
            i = int(input())
        except ValueError as e:
            print(e)
            r.stop()
            exit()
        """
        if i == 0:
            if go:
                r.stop()
                go = False
                print(go)
            else:
                #tgo = th.Thread(target=r.go)
                t.start()
                go = True
                print(go)
        """
        if i == 1:
            print('Gib den neuen Winkel ein: ')
            temp = int(input())
            r.setAngel(temp)
        elif i == 2:
            print('0=Dreieck-Gang\n1=Rechteckgang\n')
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
    ths = []
    for i in range(10):
        t = th.Thread(target=test, args=(i,))
        ths += [t]
        t.start()
    """
