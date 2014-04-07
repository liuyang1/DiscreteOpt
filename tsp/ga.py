#! -*-encoding=utf8-*-
import sys
import multiprocessing
import heapq
import random
import matplotlib.pyplot as plt
import thread
import copy

import tsp
import plot
import geo


class Unit():

    def __init__(self, mat, points):
        self.mat = mat
        self.points = points
        self.size = len(mat)
        self.seq = range(1, self.size)
        random.shuffle(self.seq)
        self.seq.append(0)
        self.judgeVal = None

    def Singlemutation(self):
# 逆转变异算子
        p0 = random.randint(0, self.size - 1)
        p1 = random.randint(0, self.size - 1)
        if p0 != p1:
            self.seq[p0], self.seq[p1] = self.seq[p1], self.seq[p0]
        self.judgeVal = None
        return self

    def bigMutation(self, n=4):
        plst = [random.randint(0, self.size - 1) for i in xrange(n)]
        v0 = self.seq[plst[0]]
        for i in xrange(n - 1):
            self.seq[plst[i]] = self.seq[plst[i + 1]]
        self.seq[plst[-1]] = v0
        self.judgeVal = None
        return self

    def deCrossMutation(self):
# 检查是否存在相交的线段,然后去除相交,这样可以必然得到较好的变异结果
        shift = self.seq[1:] + self.seq[:1]
        pairlist = zip(*(self.seq, shift))
        points = self.points
        flag = False
        for i in xrange(len(pairlist)):
            pair0 = pairlist[i]
            pt0, pt1 = points[pair0[0]], points[pair0[1]]
            for j in xrange(len(pairlist)):
                if abs(i-j) <= 1:
                    continue
                pair1 = pairlist[j]
                pt2, pt3 = points[pair1[0]], points[pair1[1]]
                if geo.isCross(pt0, pt1, pt2, pt3):
                    flag = True
                    muta = [pair0[0], pair0[1], pair1[0], pair1[1]]
                    break
            if flag:
                break
        if flag:
            random.shuffle(muta)
            ii = 0
            for i in xrange(len(self.seq)):
                if self.seq[i] in muta:
                    try:
                        self.seq[i] = muta[ii]
                    except IndexError:
                        break
                    ii += 1
            self.judgeVal = None
            return self
        else:
            return self.bigMutation()
    mutation = bigMutation

    def SingleCross(self, u):
# 单点交叉法
        p = random.randint(0, self.size - 1)
        c = [i for i in u.seq[p:] if i in self.seq[p:]]
        o = [i for i in self.seq[p:] if i not in u.seq[p:]]
        newUnit = Unit(self.mat, self.points)
        newUnit.seq = self.seq[0:p] + o + c
        newUnit.judgeVal = None
        return newUnit

    def newcross(self, u):
        p = random.randint(0, self.size - 1)
        c = [i for i in u.seq[p:] if i in self.seq[p:]]
        newUnit = Unit(self.mat, self.points)
        newUnit.seq = copy.deepcopy(self.seq)
        ii = 0
        for i in xrange(p, len(self.seq)):
            if newUnit.seq[i] in c:
                try:
                    newUnit.seq[i] = c[ii]
                except IndexError:
                    break
                ii += 1
        return newUnit
    cross = newcross


    def select(self, thresh):
        v = self.judge()
        if v <= thresh:
            return True
        else:
            return (v / thresh - 1.0) < random.random()

    def judge(self):
        if self.judgeVal == None:
            self.judgeVal = tsp.distPath(self.mat, self.seq)
        return self.judgeVal

    def display(self):
        for i in xrange(5):
            print self.seq[i],
        print


class GA():

    def __init__(self, mat, points):
        self.groupsize = 80
        self.group = [Unit(mat, points) for i in xrange(self.groupsize)]

    def loop(self):
        gen = 0
        m = 300000
        m = m * m
        p = None
        cnt = 0
        while 1:
            print "gen ", gen,
            g = [u for u in self.group if u.select(m)]
            g0 = heapq.nsmallest(
                self.groupsize / 2, g, key=lambda x: x.judge())
            m0 = g0[0].judge()
            g = [u0.cross(u1) for u1 in g for u0 in g]
            g = [u.mutation() for u in g]
            g = heapq.nsmallest(self.groupsize / 2, g, key=lambda x: x.judge())
            m1 = g[0].judge()
            m = min(m0, m1)
            print "%.4f %.4f" % (m, m / m0),
            g = g0 + g
            self.group = g
            gen += 1
            if m != m0:
                cnt = 0
                if p != None:
                    p.terminate()
                p = multiprocessing.Process(
                    target=plot.plotThread, args=(pts, g[0].seq))
                p.start()
            else:
                cnt += 1
            print cnt
            if cnt == 20:
                break
        p.terminate()
        return g[0].seq


def ga(points):
    mat = tsp.distMat(points)
    ga = GA(mat,points)
    ga.loop()

if __name__ == "__main__":
    fn = sys.argv[1] if len(sys.argv) >=2 else "data/tsp_51_1"
    f = open(fn)
    pts = plot.loadPoints(f)
    f.close()
    print "running main"
    ga(pts)
