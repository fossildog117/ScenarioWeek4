import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
import ScenarioWeek4
import itertools

polygonArray = ScenarioWeek4.polygon()

"""
This is used to draw graphs
"""

def polygonEdges():
    polygonEdgeArray = []
    for shape in polygonArray:
        edges = []
        for i in range(-1, len(shape) - 1):
            edges.append([ScenarioWeek4.Coordinate(False, shape[i][0], shape[i][1]), ScenarioWeek4.Coordinate(False, shape[i + 1][0], shape[i + 1][1])])
        polygonEdgeArray.append(edges)
    return polygonEdgeArray


edges = polygonEdges()

def plotRobots(plt):
    x, y = [], []
    coordinates = []
    points = ScenarioWeek4.robots()
    for robot in points:
        x.append(robot[0])
        y.append(robot[1])
        coordinates.append(ScenarioWeek4.Coordinate(True, robot[0], robot[1]))

    plt.scatter(x[1:], y[1:])
    plt.scatter(x[0:1], y[0:1], color="r")


def plotOutcome(plt):
    colours = ['m','g','r','c','b','y','k']
    cou = 0
    # max
    # 3 node
    # arr1 = [[[1.7611158486517908,-7.747711347622252],[-0.7986697892720992,2.802929857341768],[4.570302341941199,6.133961454352471],[4.545065131048604,7.011566783399479]]]
    arr1 = [[[0.0,1.0],[2.0,0.0],[3.0,2.0],[4.0,4.0],[3.0,5.0]],[[2.0,0.0],[9.0,0.0]],[[9.0,0.0],[8.0,1.0],[6.0,2.0]]]
    for arr in arr1:
        for i in range(0, len(arr) - 1):
            # print([[arr[i][0], arr[i][1]], [arr[i + 1][0], arr[i + 1][1]]])
            plt.plot([arr[i][0], arr[i + 1][0]], [arr[i][1], arr[i + 1][1]], color=colours[cou])
        if cou == len(colours) - 1:
            cou = 0
        else:
            cou += 1


def printLines(polygons, plt):
    for p in polygons:
        x = []
        y = []
        for coordinate in p:
            x.append(coordinate[0])
            y.append(coordinate[1])

        plt.scatter(x, y, color="orange")


fig, ax = plt.subplots()
patches = []
N = 5

plotRobots(ax)
printLines(polygonArray, ax)
plotOutcome(ax)

for i in ScenarioWeek4.polygon():
    polygon = Polygon(np.array(i), True)
    patches.append(polygon)

p = PatchCollection(patches, cmap=matplotlib.cm.jet, alpha=0.4)

colors = 100 * np.random.rand(len(patches))
p.set_array(np.array(colors))

ax.add_collection(p)
plt.show()
