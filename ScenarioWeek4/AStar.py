from ScenarioWeek4 import GreedyDynamicSchedule as gs
from ScenarioWeek4 import *

import copy


nodeList = {}
robots = gs.rob
polygons = gs.polygons
infinity = 1000000


class Node(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.children = []

    def distance(self, other):
        return decimal.Decimal(math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2))


def createNodeList():
    nodeArray = {}

    for polygon in polygons:
        for i in range(-1, len(polygon) - 1):
            # arr = [polygon[i][0], polygon[i][1], polygon[i + 1][0], polygon[i + 1][1]]
            # if node exists add

            p1 = (polygon[i][0], polygon[i][1])
            p2 = (polygon[i + 1][0], polygon[i + 1][1])

            if p1 not in nodeArray:
                nodeArray[p1] = Node(polygon[i][0], polygon[i][1])

            if p2 not in nodeArray:
                nodeArray[p2] = Node(polygon[i + 1][0], polygon[i + 1][1])

            # nodeArray[p1].children.append(p2)
            # nodeArray[p2].children.append(p1)

        # for node in polygon():
        #     p = Node(node[0], node[1])
        #     nodeArray[(node[0], node[1])] = p

    return nodeArray


def additionalPoints(nodeList):
    # print("****")
    counter = 0
    seenNodes = {}

    for node in nodeList:
        print("{count}: Working on node {x},{y}".format(count=counter, x=node[0], y=node[1]))
        a1 = Coordinate(False, nodeList[node].x, nodeList[node].y)

        for node1 in nodeList:
            if node1 in seenNodes:
                if seenNodes[node1] > 3:
                    continue
            if node1 is not node:
                if node1 not in nodeList[node].children:
                    a2 = Coordinate(False, nodeList[node1].x, nodeList[node1].y)
                    intersections = 0
                    for polygon in polygons:
                        if [a1.x, a1.y] in polygon and [a2.x, a2.y] in polygon:
                            # check if adjacent
                            # print("Passing....")
                            # print([[a1.x, a1.y] , [a2.x, a2.y]])
                            # print(polygon)
                            # print("****************")
                            intersections += 1
                            break
                        else:
                            for i in range(-1, len(polygon) - 1):
                                b1 = Coordinate(False, polygon[i][0], polygon[i][1])
                                b2 = Coordinate(False, polygon[i + 1][0], polygon[i + 1][1])
                                if (b1.x == a1.x and b1.y == a1.y or b1.x == a2.x and b1.y == a2.y) or (
                                                    b2.x == a1.x and b2.y == a1.y or b2.x == a2.x and b2.y == a2.y):
                                    continue
                                if intersect(a1, a2, b1, b2):
                                    # print([a1.x, a1.y, a2.x, a2.y, b1.x, b1.y, b2.x, b2.y])
                                    intersections += 10
                                    break

                    # print("?????????????")
                    if intersections == 0:
                        # print("Adding : {a}".format(a=[a1.x, a1.y, a2.x, a2.y, b1.x, b1.y, b2.x, b2.y]))
                        if node not in seenNodes:
                            seenNodes[node] = 0
                        if node1 not in seenNodes:
                            seenNodes[node1] = 0
                        seenNodes[node] += 1
                        seenNodes[node1] += 1
                        nodeList[node].children.append(node1)
                        nodeList[node1].children.append(node)

    return nodeList



def lowestHeuristic(openSet, heuristicMap):
    lowest = infinity
    currentNode = (0, 0)

    for heuristic in heuristicMap:
        if heuristic in openSet:
            if heuristicMap[heuristic] < lowest:
                lowest = heuristicMap[heuristic]
                currentNode = heuristic
    return currentNode


def a_star(start, end):

    # set of evaluated nodes
    closedSet = {}

    # set of currently discovered nodes that have node been evaluated
    openSet = {(start.x, start.y): start}

    cameFrom = {}
    g_score = {}
    f_score = {}
    heuristicMap = {}

    for node in nodeList:
        g_score[node] = infinity
        f_score[node] = infinity
        heuristicMap[node] = end.distance(nodeList[node])

    g_score[(start.x, start.y)] = 0
    f_score[(start.x, start.y)] = heuristicMap[(start.x, start.y)]

    while len(openSet) > 0:

        current = lowestHeuristic(openSet, heuristicMap)
        if current[0] == end.x and current[1] == end.y:
            return reconstruct_path(cameFrom, current)

        closedSet[current] = openSet[current]
        openSet.pop(current)
        for neighbour in nodeList[current].children:
            if neighbour in closedSet:
                continue

            # distance between start and neighbour
            g = g_score[current] + nodeList[neighbour].distance(nodeList[current])

            if neighbour not in openSet:
                openSet[neighbour] = nodeList[neighbour]

            elif g > g_score[neighbour]:
                continue

            cameFrom[neighbour] = current
            g_score[neighbour] = g
            f_score[neighbour] = g_score[neighbour] + heuristicMap[neighbour]

    return 0


def reconstruct_path(cameFrom, current):
    # print(cameFrom)
    total_path = [current]
    while current in cameFrom:
        current = cameFrom[current]
        total_path.append(current)
    return list(reversed(total_path))


print("Creating node list")
nodeList = createNodeList()
# for value in nodeList:
#     print(value)
#     print(nodeList[value].children)
for robo in robots:
    nodeList[(robo[0], robo[1])] = Node(robo[0], robo[1])
print("Generating graph")
nodeList = additionalPoints(nodeList)
print("-----")
for value in nodeList:
    print(value)
    print(nodeList[value].children)

outString = ""

for value in nodeList:
    outString += "["
    for node in nodeList[value].children:
        if nodeList[value].children[-1] is node:
            outString += "[{x},{y}],[{x2},{y2}]".format(x=value[0], y=value[1], x2=node[0], y2=node[1])
        else:
            outString += "[{x},{y}],[{x2},{y2}],".format(x=value[0],y=value[1],x2=node[0],y2=node[1])
    outString += "],"
print(outString)
