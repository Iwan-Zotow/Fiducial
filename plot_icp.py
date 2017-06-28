#%%
import sys
import matplotlib.pyplot as plt
import numpy as np

def readICP(fname):
    """
    read ICP file and return IC ow and iw
    """

    if fname is None:
        return None

    with open(fname) as f:
        # RU
        line = f.readline().rstrip('\n')

        # Outer cup
        line = f.readline().rstrip('\n')

        # Inner cup
        line = f.readline().rstrip('\n')

        # nof points in the inner wall
        line = f.readline().rstrip('\n')
        niw = int(line)

        riw = list()
        ziw = list()
        # inner wall
        for k in range(niw):
            line = f.readline().rstrip('\n')
            s = line.split(' ')
            s = [x for x in s if x] # remove empty lines
            ziw.append(float(s[0]))
            riw.append(float(s[1]))

        # nof points in the outer wall
        line = f.readline().rstrip('\n')
        now = int(line)

        row = list()
        zow = list()
        # outer wall
        for k in range(now):
            line = f.readline().rstrip('\n')
            s = line.split(' ')
            s = [x for x in s if x] # remove empty lines
            zow.append(float(s[0]))
            row.append(float(s[1]))

        return (ziw, riw, zow, row)

    return None

ziwO, riwO, zowO, rowO = readICP("D:/Ceres/Resource/PlanEngine/R8/Cup/R8O1IS01.icp")
#ziwO, riwO, zowO, rowO = readICP("R8O1IS02.icp")

l_innerO, = plt.plot(ziwO, riwO, label="innerO")
l_outerO, = plt.plot(zowO, rowO, label="outerO")

ziwN, riwN, zowN, rowN = readICP("R8O1IS01.icp")

l_innerN, = plt.plot(ziwN, riwN, label="innerN")
l_outerN, = plt.plot(zowN, rowN, label="outerN")

plt.legend([l_innerO, l_outerO, l_innerN, l_outerN], ['InnerO', 'OuterO', 'InnerN', 'OuterN'])

plt.show()
