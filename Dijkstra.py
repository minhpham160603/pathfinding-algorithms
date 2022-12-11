import math
import matplotlib.pyplot as plt


class Node:
    def __init__(self, index, x, y, distance=math.inf, parent_node = None):
        self.index = index
        self.x = x
        self.y = y
        self.distance = distance
        self.parent = parent_node

    def __lt__(self, other_node):
        return self.distance < other_node.distance

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

def createMap(h, w):
    return [[0]*w for _ in range(h)]

def getMotion():
     # dx, dy, cost
    motion = [[1, 0, 1],
                [0, 1, 1],
                [-1, 0, 1],
                [0, -1, 1],
                [-1, -1, math.sqrt(2)],
                [-1, 1, math.sqrt(2)],
                [1, -1, math.sqrt(2)],
                [1, 1, math.sqrt(2)]]

    return motion

def getIndex(x, y, map):
    return y*len(map[0]) + x

def Dijkstra(start_position, goal_position, map, ox, oy):
    w, h = len(map[0]), len(map)
    plt.plot(w, h)
    plt.plot(ox, oy, ".k")
    plt.plot([start_position[0]], [start_position[1]], "og")
    plt.plot([goal_position[0]], [goal_position[1]], "xb")

    open_set, closed_set = {}, {}
    start_id = getIndex(start_position[0], start_position[1], map)

    open_set[start_id] = Node(start_id, start_position[0], start_position[1], 0)

    while len(open_set):
        current_id = min(open_set, key=lambda i: open_set[i].distance)
        current = open_set[current_id]

        plt.plot(current.x, current.y, "xc")

        del open_set[current_id]
        closed_set[current_id] = current

        if (current.x, current.y) == goal_position:
            print("Find goal!")
            break

        motion = getMotion()
        for dx, dy, dist in motion:
            x, y = current.x + dx, current.y + dy
            if 0 <= x < w and 0 <= y < h and map[y][x] == 0:
                new_id = getIndex(x, y, map)
                node = Node(new_id, x, y, current.distance + dist, current)
                if new_id in closed_set:
                    continue

                if new_id not in open_set:
                    open_set[new_id] = node

                else:
                    if current.distance + dist < open_set[new_id].distance:
                        open_set[new_id].distance = current.distance + dist
                        open_set[new_id].parent = current

    path = findFinalPath(closed_set, goal_position, map)
    rx, ry = [p.x for p in path], [p.y for p in path]
    plt.plot(rx, ry, "-r")
    plt.pause(0.01)
    plt.show()
    

def findFinalPath(closed_set, goal_position, map):
    current_node = closed_set[getIndex(goal_position[0], goal_position[1], map)]
    path = []
    while current_node:
        path.append(current_node)
        current_node = current_node.parent
    path.reverse()
    return path

def addVerticalWalls(map, x, y_start, y_end, ox, oy):
    for i in range(y_start, y_end):
        map[i][x] = 1
        ox.append(x)
        oy.append(i)

def test():
    map = createMap(50, 50)
    ox, oy = [], []
    addVerticalWalls(map, 20, 0, 40, ox, oy)
    Dijkstra((1, 1), (40, 10), map, ox, oy)

test()