#! /usr/bin/env python
#! -*-encoding=utf8 -*-
import math
import random
import multiprocessing

import geo
import plot


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


def deCrossMutation(pts, mat, path):
    def deCross(path):
        shift = path[1:] + path[:1]
        pairlist = zip(*(path, shift))
        for i,(pt0, pt1) in enumerate(pairlist):
            for j,(pt2, pt3) in enumerate(pairlist):
                if abs(i-j) <= 1:
                    continue
                if pt0 == pt2 or pt0 == pt3 or pt1 == pt2 or pt1 == pt3:
                    continue
                if geo.isCross(pts[pt0], pts[pt1], pts[pt2], pts[pt3]):
                    l0 = mat[pt0][pt1] + mat[pt2][pt3]
                    l1 = mat[pt0][pt3] + mat[pt1][pt2]
                    # print "decross ", pt0, pt1, pt2, pt3, l0 - l1
                    newpath = path[0:i+1] + path[j:i:-1] + path[j+1:]
                    return True, newpath
        return False, path
    while 1:
        flag, path = deCross(path)
        if flag == False:
            return path


def redraw(p, pts, path):
    if p != None:
        p.terminate()
    p = multiprocessing.Process(target=plot.plotThread, args=(pts, path))
    p.start()
    return p


def greedyDfs2(pts):
    mat = distMat(pts)
    p, mv, mp = None, None, None
    for begin in xrange(len(pts)):
        path = [begin]
        while(len(path) < len(pts)):
            start = path[-1]
            end = path[0]
            totest = [x for x in xrange(len(pts)) if x not in path]
            if len(path) / (len(pts)+0.0) < 0.7:
                m = min(totest, key=lambda x: mat[x][start])
            else:
                m = min(totest, key=lambda x: mat[x][start] - mat[x][end])
            path.append(m)
        path = deCrossMutation(pts, mat, path)
        v = distPath(mat, path)
        if mv == None or mv > v:
            mv, mp = v, path
            p = redraw(p, pts, path)
        print begin, v, mv
    return mp

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


def allPerm(pts):
    import itertools
    path = range(1, len(pts))
    m = 100000000
    mat = distMat(pts)
    for i in itertools.permutations(path):
        p = list(i) + [0]
        # v = distPath(mat, p)
        v = 0
        shift = p[1:] + p[:1]
        pairlist = zip(*(p, shift))
        for x in pairlist:
            v += mat[x[0]][x[1]]
            if v > m:
                v = m + 1
                break
        if v < m:
            m, ret = v, p
            print m, ret
    return ret


def randDeCross(pts):
    mat = distMat(pts)
    path = range(len(pts))
    p = None
    mv, mp = None, None
    for i in xrange(100):
        random.shuffle(path)
        path = deCrossMutation(pts, mat, path)
        v = distPath(mat, path)
        if mv == None or v < mv:
            mv, mp = v, path
            print i, mv
            p = redraw(p, pts, path)
    return mp


tsp = greedyDfs2
