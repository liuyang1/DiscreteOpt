#-*- encoding=utf8 -*-
import copy
import sys


def removeOneClq(clq):
    """对于一个团,去除其中一个,得到其对应的补集.所有的补集的列表,就是本函数返回
    例如(1,2,3) -> [(1, 2) (2,3) (1,3)]
    """
    ret = []
    for i in clq:
        l = copy.deepcopy(clq)
        l.remove(i)
        ret.append(l)
    return ret


def addOneClq(clq, setRet):
    ret = []
    for i in setRet:
        l = copy.deepcopy(clq)
        l.append(i)
        ret.append(l)
    return ret


def complete(comp, clq):
    """如果一个团补,是一个团的补
    例如 (1,2) 是 (1, 2, 3) 的补
    然后返回3,
    不是补的话,否则返回None
    """
    c = None
    for i in clq:
        if i not in comp:
            if c is not None:
                return None
            c = i
    return c


def mergeclique(clqlst):
    newclqlst = []
    for clq in clqlst:
        # print "dive in ",clq
        compltementLst = removeOneClq(clq)
        if len(compltementLst) == 0:
            return None
        firstflag = True
        for comp in compltementLst:
            tmp = set()
            for clq1 in clqlst:
                ret = complete(comp, clq1)
                if ret:
                    tmp.add(ret)
            if firstflag:
                firstflag = False
                cc = tmp
            cc = set([x for x in cc if x in tmp])
        if len(cc) == 0:
            continue
        newclq = addOneClq(clq, cc)
        newclq = [i for i in newclq if isUp(i)]
        newclqlst.extend(newclq)
    return newclqlst


def isUp(lst):
    for i in xrange(1, len(lst)):
        if lst[i - 1] > lst[i]:
            return False
    return True

def statDegree(edges):
    from collections import Counter
    cnt = Counter()
    for i in edges:
        cnt.update(i)
    return cnt

def filterDegree(clqLst, degreeCnt, maxClqN):
    def isGtDegree(clq):
        return all(degreeCnt[i] >= maxClqN for i in clq)
    return filter(isGtDegree, clqLst)


def clique(edges):
    degreeCnt = statDegree(edges)
    clqLst = edges
    maxClqN = 2
    while 1:
        l0 = len(clqLst)
        clqLst = filterDegree(clqLst, degreeCnt, maxClqN + 1)
        print "filter...", 1 - len(clqLst) / (l0 + 0.0)
        print maxClqN, " to check ", len(clqLst)
        clqLst = mergeclique(clqLst)
        if len(clqLst) == 0:
            break
        maxClqN += 1
        if len(clqLst) == 0 or len(clqLst) < len(clqLst[0]) + 1:
            break
    print "final: ",maxClqN
    return maxClqN


def easyTest():
    edges = [[1, 2], [2, 5], [1, 5], [4, 5], [4, 3], [3, 2], [4, 6]]
    clique(edges)


def complexTest():
    # clique FOUR
    # edges = [[1,2], [2,5], [1,5], [4,5], [4,3], [3,2], [4,6], [1,7], [5,7], [2,7]]
    # clique THREE
    edges = [[1, 2], [2, 5], [1, 5], [4, 5], [4, 3],
             [3, 2], [4, 6], [1, 7], [5, 7], [4, 7], [6, 7]]
    clique(edges)


if __name__ == "__main__":
    "test case"
    easyTest()
    complexTest()
