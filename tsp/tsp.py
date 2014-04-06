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

def connect(lines, pt):
    l0 = [x for x, y in lines if y == pt]
    l1 = [y for x, y in lines if x == pt]
    return l0 + l1


def preorderWalk(tree, root=None):
    if root == None:
        root = tree[0][0]
    lst = []
    queue = [root]
    passed = []
    while 1:
        try:
            n = queue.pop()
        except:
            break
        passed.append(n)
        l = connect(tree, n)
        nl = [i for i in l if i not in passed]
        queue.extend(nl)
    return passed


def approxTSP(pts):
# 实现了构建最小生成树,然后得到近似解的算法,但是结果太差了.
# 还不如贪心算法的结果
    lines = mst(pts)
    ptlist = [preorderWalk(lines, r) for r in xrange(len(pts))]
    mat = distMat(pts)
    pt = min(ptlist, key=lambda x: distPath(mat, x))
    return pt


tsp = greedyDfs2
