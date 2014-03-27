import math


def distance(pt0, pt1):
    return math.sqrt((pt0[0] - pt1[0]) ** 2 + (pt0[1] - pt1[1]) ** 2)


def distMat(pts):
    return [[distance(i, j) for i in pts] for j in pts]


def greedyDfs(pts):
    mat = distMat(pts)
    path = [0]
    dist = 0
    while(len(path) < len(pts)):
        start = pts[path[-1]]
        totest = [x for x in xrange(len(pts)) if x not in path]
        m = min(totest, key=lambda x: distance(pts[x], start))
        path.append(m)
    return path
