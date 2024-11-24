import numpy as np
import math

type Color = tuple[int, int, int]

BLACK: Color = (0, 0, 0)
WHITE: Color = (255, 255, 255)
GREEN: Color = (0, 255, 0)
DARK_GREEN: Color = (0, 127, 0)
RED: Color = (255, 0, 0)
DARK_RED: Color = (127, 0, 0)
BLUE: Color = (0, 0, 255)


# Constants for easy understanding of the code
x = 0
y = 1


# Finds a perpendicular vector to a
# Input: 2d vector a
# Output: A vector b such that a*b = 0
def perpendicular(a):
    b = np.empty_like(a)
    b[0] = -a[1]
    b[1] = a[0]
    return b


# Normalizes the input vector a to have the magnitude c
def normalize(a, c):
    a = np.array(a)
    return c * a / np.linalg.norm(a)


# Rotates the 2d vector a by the angle beta clockwise.
def rotate(a, beta):
    theta = np.radians(beta)
    c, s = np.cos(theta), np.sin(theta)
    return np.array(((c, -s), (s, c))).dot(a)


# Calculates the distance and the point until an element is hit from the position p and direction a
def raycast(a, p, theMap):
    step = [0, 0]
    side = [0, 0]

    raydir = normalize(a, 1)
    deltaX = float("inf")
    deltaY = float("inf")
    if raydir[y] != 0:
        deltaY = math.sqrt(1 + raydir[x] ** 2 / raydir[y] ** 2)
    if raydir[x] != 0:
        deltaX = math.sqrt(1 + raydir[y] ** 2 / raydir[x] ** 2)

    delta = (deltaX, deltaY)
    aMap = [int(p[x]), int(p[y])]

    hit = False
    dist = 0.0

    if raydir[x] > 0:
        step[x] = 1
        side[x] = abs((aMap[x] + 1 - p[x]) * delta[x])
    elif raydir[x] < 0:
        step[x] = -1
        side[x] = abs((aMap[x] - p[x]) * delta[x])
    else:
        step[x] = 0
        side[x] = float("inf")

    if raydir[y] > 0:
        step[y] = 1
        side[y] = abs((aMap[y] + 1 - p[y]) * delta[y])
    elif raydir[y] < 0:
        step[y] = -1
        side[y] = abs((aMap[y] - p[y]) * delta[y])
    else:
        step[y] = 0
        side[y] = float("inf")

    while not hit:
        collision_side = "x"
        if side[x] < side[y]:
            collision_side = "x"
            dist += side[x]
            side[y] -= side[x]
            side[x] = abs(delta[x])
            aMap[x] += step[x]
        else:
            collision_side = "y"
            dist += side[y]
            aMap[y] += step[y]
            side[x] -= side[y]
            side[y] = abs(delta[y])

        if any([aMap[y] >= len(theMap), aMap[y] < 0, aMap[x] >= len(theMap[0]), aMap[x] < 0]):
            return None, None, None

        if theMap[aMap[y]][aMap[x]] > 0:
            hit = True
            point = p + raydir * dist

    return point, collision_side, (aMap[x], aMap[y])
