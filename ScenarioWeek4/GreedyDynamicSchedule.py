from ScenarioWeek4 import *

rob = robots()
number_of_robots = len(rob)

polygons = polygon()

print("number of robots: {number_of_robots}".format(number_of_robots=number_of_robots))

infinity = 1000000000000000000

from ScenarioWeek4 import AStar

modifiedEdges = {}


class Robot:
    def __init__(self, x, y, status):
        self.x = x
        self.y = y
        self.status = status
        self.closest = -1
        self.distanceAcquiredSinceLastJump = 0
        self.remainingDistance = infinity
        self.intermediatePoints = [[x, y]]
        self.jParam = 0
        self.path = []
        self.closestNeighbours = []
        self.visited = False


def distance(a, b):
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


def new_distance(route):
    total_distance = 0
    for i in range(0, len(route) - 1):
        total_distance += distance(route[i], route[i + 1])
    return total_distance


def shortestDistance(firstRobot, secondRobot, shapeList):
    """
    :param firstRobot:
    :param secondRobot:
    :param shapeList:
    :return: float
    """

    a = AStar.Node(firstRobot.x, firstRobot.y)
    b = AStar.Node(secondRobot.x, secondRobot.y)

    route = AStar.a_star(a, b)
    modifiedEdges[(a.x, a.y, b.x, b.y)] = route
    return new_distance(route)


def greedy_dynamic_schedule():
    r = []
    r.append(Robot(rob[0][0], rob[0][1], True))
    # make copy of robots
    for r1 in rob[1:]:
        r.append(Robot(r1[0], r1[1], False))

    targetList = []
    targetList.append([0, -1])
    counter = 0

    for i in range(0, number_of_robots):
        for j in range(0, number_of_robots):
            if i != j:
                r[i].closestNeighbours.append((r[j], shortestDistance(r[i], r[j], polygons)))
                r[j].jParam = j
        r[i].closestNeighbours.sort(key=lambda x: x[1])

    print("***()()()***")

    for x in range(1, number_of_robots):  # fill in target list
        print("{cu}: waiting...".format(cu=counter))

        for i in range(0, number_of_robots):

            if r[i].status:
                r[i].closest = -1
                r[i].remainingDistance = infinity
                for bot in r[i].closestNeighbours:
                    if bot[0].status is False:
                        d = bot[1] - r[i].distanceAcquiredSinceLastJump
                        if d < r[i].remainingDistance:
                            r[i].remainingDistance = d
                            r[i].closest = bot[0].jParam

        # see which robot will reach target first
        nextRobotToReachTarget = -1
        d = infinity

        for i in range(0, number_of_robots):
            if r[i].status and r[i].remainingDistance < d:
                d = r[i].remainingDistance
                nextRobotToReachTarget = i

        if d == infinity:
            break

        # update acquired distance for all awake robots
        for i in range(0, number_of_robots):
            if r[i].status:
                r[i].distanceAcquiredSinceLastJump += d

        # reset robot that made jump
        r[nextRobotToReachTarget].distanceAcquiredSinceLastJump = 0
        r[nextRobotToReachTarget].x = r[r[nextRobotToReachTarget].closest].x
        r[nextRobotToReachTarget].y = r[r[nextRobotToReachTarget].closest].y

        # add the two robots to target list in numerical order
        if r[nextRobotToReachTarget].closest < nextRobotToReachTarget:
            targetList.append([r[nextRobotToReachTarget].closest, -1])
            targetList.append([nextRobotToReachTarget, -1])
        else:
            targetList.append([nextRobotToReachTarget, -1])
            targetList.append([r[nextRobotToReachTarget].closest, -1])

        # update newly awakened robot
        r[r[nextRobotToReachTarget].closest].status = True

        # update target list
        updated = False
        for i in range(0, len(targetList)):
            if targetList[i][0] == nextRobotToReachTarget and targetList[i][1] == -1 and updated is False:
                targetList[i][1] = r[nextRobotToReachTarget].closest
                updated = True
        counter += 1

    s = []

    for i in range(0, len(targetList)):
        s.append(targetList[i][1])

    return s


def start():
    print("starting")
    # schedule = constantSchedule()
    schedule = greedy_dynamic_schedule()
    # print(schedule)
    # print(rob[1:])

    idleRobots = []

    for r1 in rob:
        idleRobots.append(Robot(r1[0], r1[1], False))

    idleRobots[0].status = True

    while schedule is not []:

        if schedule == []:
            break

        num, counter = 0, 0
        for robotx in idleRobots:
            if robotx.status:
                num += 1

        for robotX in idleRobots:

            if schedule == []:
                break

            if robotX.status is True:

                if counter >= num:
                    break

                counter += 1

                if schedule[0] == -1:
                    robotX.status = False
                    # print("stopping robot: {x}, {y} : status: {s}".format(x=robotX.x,
                    #                                                       y=robotX.y,
                    #                                                       s=robotX.status))

                else:
                    robotX.intermediatePoints.append(rob[schedule[0]])
                    idleRobots[schedule[0]].status = True
                    # print("starting robot: {x}, {y} : status: {s}".format(x=idleRobots[schedule[0]].x,
                    #                                                       y=idleRobots[schedule[0]].y,
                    #                                                       s=idleRobots[schedule[0]].status))
                schedule.remove(schedule[0])
                # print("*****_____*****")

    print("------")

    for bot in idleRobots:
        for i in range(0, len(bot.intermediatePoints) - 1):
            a = (bot.intermediatePoints[i][0], bot.intermediatePoints[i][1], bot.intermediatePoints[i + 1][0],
                 bot.intermediatePoints[i + 1][1])
            if a in modifiedEdges:
                counter = 1
                for j in range(i + 1, len(modifiedEdges[a])):

                    if counter == len(modifiedEdges[a]) - 1:
                        break

                    bot.intermediatePoints.insert(j , [modifiedEdges[a][counter][0], modifiedEdges[a][counter][1]])
                    counter += 1

    outputString = ""
    for bott in idleRobots:
        if len(bott.intermediatePoints) <= 1:
            pass
        else:
            for interPoint in bott.intermediatePoints:
                if interPoint == bott.intermediatePoints[-1]:
                    outputString += "({x},{y})".format(x=float(interPoint[0]), y=float(interPoint[1]))
                else:
                    outputString += "({x},{y}),".format(x=float(interPoint[0]), y=float(interPoint[1]))
            outputString += ";"

    print(outputString)


def GenerateCycle():
    r = []
    r.append(Robot(rob[0][0], rob[0][1], True))
    # make copy of robots
    for r1 in rob[1:]:
        r.append(Robot(r1[0], r1[1], False))

    outputString = ""
    outputStrign2 = ""

    for i in range(0, len(r) - 1):
        nodeA = AStar.Node(r[i].x, r[i].y)
        nodeB = AStar.Node(r[i + 1].x, r[i + 1].y)
        isFirst = True
        for node in AStar.a_star(nodeA, nodeB):

            if isFirst:
                isFirst = False
                continue

            if [node[0], node[1]] in rob:
                outputString += "({x},{y}),".format(x=node[0], y=node[1])
                outputStrign2 += "[{x},{y}],".format(x=node[0], y=node[1])
            else:
                outputString += "({x:.24},{y:.24}),".format(x=node[0], y=node[1])
                outputStrign2 += "[{x:.24},{y:.24}],".format(x=node[0], y=node[1])

    print(outputString)
    print(outputStrign2)
