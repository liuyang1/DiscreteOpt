#! /usr/bin/env python
#! -*-encoding=utf8 -*-
import math


def distance(pt0, pt1):
    return math.sqrt((pt0[0] - pt1[0]) ** 2 + (pt0[1] - pt1[1]) ** 2)


def distMat(pts):
    return [[distance(i, j) for i in pts] for j in pts]


def distPath(mat, path):
    shift = path[1:] + path[:1]
    pairlist = zip(*(path, shift))
    return sum(map(lambda x: mat[x[0]][x[1]], pairlist))


def mst(pts):
# TODO:
# 这个实现的效率非常之低,只有O(n^3)
    mat = distMat(pts)
    _, idx0, idx1 = min(min((val, idx0, idx1) for idx1, val in enumerate(vec) if val > 0.1)
                        for idx0, vec in enumerate(mat))
    f = [idx0, idx1]
    p = [(idx0, idx1)]
    while len(f) < len(mat):
        _, idx0, idx1 = min(min((val, idx0, idx1) for idx1, val in enumerate(vec) if idx1 not in f)
                            for idx0, vec in enumerate(mat) if idx0 in f)
        # print idx0, idx1, len(f), len(mat)
        f.append(idx1)
        p.append((idx0, idx1))
    return p


def greedyDfs2(pts):
    mat = distMat(pts)
    pathlst = []
    for begin in xrange(len(pts)):
        path = [begin]
        while(len(path) < len(pts)):
            start = path[-1]
            end = path[0]
            totest = [x for x in xrange(len(pts)) if x not in path]
            if 2 * len(path) < len(pts):
                m = min(totest, key=lambda x: mat[x][start])
            else:
                m = min(totest, key=lambda x: mat[x][start] - mat[x][end])
            path.append(m)
        pathlst.append(path)
    return min(pathlst, key=lambda x: distPath(mat, x))

tsp = greedyDfs2
