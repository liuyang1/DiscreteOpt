#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import numpy as np


def coloring(edges):
    print edges
    return range(0, len(edges) + 1)


def buildAdjMat(edges):
    n = max((max(e) for e in edges)) + 1
    mat = [[0 for i in xrange(n)] for j in xrange(n)]
    for e in edges:
        mat[e[0]][e[1]] = 1
        mat[e[1]][e[0]] = 1
    return np.matrix(mat)


def adjMatrixPower(mat, n):
    if n == 1:
        return mat
    if n % 2 == 0:
        mat = adjMatrixPower(mat, n / 2)
        return mat * mat
    else:
        return mat * adjMatrixPower(mat, n - 1)


def logicMatMul(a, b):
    n = a.shape[0]
    C = a * b
    c = np.zeros((n, n))
    for i in xrange(n):
        for j in xrange(n):
            if C[i, j] != 0:
                c[i, j] = 1
    return c


def logicMatAdd(a, b):
    n = a.shape[0]
    new = False
    for i in xrange(n):
        for j in xrange(n):
            if a[i, j] == 0 and b[i, j] != 0:
                new = True
                a[i, j] = 1
    return a, new


def adjMatrixAccu(mat, n):
    matN = mat
    acc = matN
    for i in xrange(1, n):
        matN = logicMatMul(matN, mat)
        acc, newer = logicMatAdd(acc, matN)
        if newer == False:
            break
    return acc


def connectSplit(edges):
    # 连通性分析代码
    # 没有实际作用
    mat = buildAdjMat(edges)
    n = mat.shape[0]
    con = adjMatrixAccu(mat, n)
    initflag = -1
    label = [initflag for i in xrange(n)]
    label[0] = 0
    cnt = 1
    start = 0
    while 1:
        for i in xrange(n):
            if con[start, i] == 1 and label[i] == initflag:
                label[i] = label[start]
                cnt += 1
            else:
                nextstart = i
        if cnt >= n - 1:
            break
        start = nextstart
        label[start] = start
    return label


def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    first_line = lines[0].split()
    node_count = int(first_line[0])
    edge_count = int(first_line[1])

    edges = []
    for i in range(1, edge_count + 1):
        line = lines[i]
        parts = line.split()
        edges.append((int(parts[0]), int(parts[1])))

    # build a trivial solution
    # every node has its own color
    # solution = range(0, node_count)
    import welch
    solution = welch.solve_it(edges)
    # solution = coloring(edges)

    # prepare the solution in the specified output format
    # output_data = str(node_count) + ' ' + str(0) + '\n'
    output_data = str(max(solution)+1) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution))

    return output_data


import sys

if __name__ == '__main__':
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        input_data_file = open(file_location, 'r')
        input_data = ''.join(input_data_file.readlines())
        input_data_file.close()
        print solve_it(input_data)
    else:
        print 'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/gc_4_1)'
