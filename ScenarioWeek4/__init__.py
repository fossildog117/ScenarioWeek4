import math
import re

import numpy as np

import matplotlib.pyplot as plt
import matplotlib
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
import decimal

inf = 1000000000000000

class Coordinate(object):
    def __init__(self, isRobot, x_coordinate, y_coordinate):
        self.isRobot = isRobot
        self.x = x_coordinate
        self.y = y_coordinate


def polygon():
    output = []
    with open('input.txt') as f:
        for line in f:
            inputLine = line.replace(" ", "").split(':')[1].split('#')
            try:
                for poly in inputLine[1].split(';'):
                    values = []
                    for item in re.split('\),\(|\)|\(', poly)[1:-1]:
                        pair = item.split(',')
                        values.append([float(pair[0]), float(pair[1])])
                    output.append(values)
            except:
                print("----")
    return output


def robots():
    output = []

    with open('input.txt') as f:
        for line in f:
            inputLine = line.replace(" ", "").split(':')[1].split('#')
            for item in re.split('\),\(|\)|\(', inputLine[0])[1:-1]:
                pair = item.split(',')
                output.append([float(pair[0]), float(pair[1])])

    return output


def distance(x1, y1, x2, y2):
    x3 = x1 - x2
    y3 = y1 - y2
    return math.sqrt((x3 * x3) + (y3 * y3))


def __perp(a):
    b = np.empty_like(a)
    b[0] = -a[1]
    b[1] = a[0]
    return b


def __isBetween(a, b, c):
    crossproduct = abs((c.y - a.y) * (b.x - a.x) - (c.x - a.x) * (b.y - a.y))

    if crossproduct > 0.00000001:
        return False   # (or != 0 if using integers)

    dotproduct = (c.x - a.x) * (b.x - a.x) + (c.y - a.y)*(b.y - a.y)
    if dotproduct < 0:
        return False

    squaredlengthba = (b.x - a.x)*(b.x - a.x) + (b.y - a.y)*(b.y - a.y)
    if dotproduct > squaredlengthba:
        return False

    return True

def intersect(coordinateA1, coordinateA2, coordinateB1, coordinateB2):

    a1 = np.array([coordinateA1.x, coordinateA1.y])
    a2 = np.array([coordinateA2.x, coordinateA2.y])
    b1 = np.array([coordinateB1.x, coordinateB1.y])
    b2 = np.array([coordinateB2.x, coordinateB2.y])

    # print([a1,a2,b1,b2])
    # print("------------")

    da = a2 - a1
    db = b2 - b1
    dp = a1 - b1
    dap = __perp(da)
    denom = np.dot(dap, db)

    if denom == 0:
        return False

    num = np.dot(dap, dp)
    x, y = (num / denom) * db + b1
    c = Coordinate(False, x, y)

    if __isBetween(coordinateA1, coordinateA2, c) and __isBetween(coordinateB2, coordinateB1, c):
        return True

    return False


a1 = Coordinate(True, 6, 2)
a2 = Coordinate(True, 1, 4)
b1 = Coordinate(True, 4, 1)
b2 = Coordinate(True, 4, 4)

print (intersect(a1, a2, b1, b2))


