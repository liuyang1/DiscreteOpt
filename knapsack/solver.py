#!/usr/bin/python
# -*- coding: utf-8 -*-

import copy
from collections import namedtuple
Item = namedtuple("Item", ['index', 'value', 'weight'])

def greedy(items, capacity):
    value, weight = 0, 0
    taken = [0] * len(items)
    for item in items:
        print item
        if weight + item.weight <= capacity:
            value += item.value
            weight += item.weight
            taken[item.index] = 1
    return value, weight, taken

def backtrace(tbl, item):
    newtbl = copy.deepcopy(tbl)
    for j in xrange(0, len(newtbl)):
        t = newtbl[j] + item.value
        if j + item.weight < len(newtbl) and t == newtbl[j+item.weight]:
            newtbl[j+item.weight] = max(newtbl[j+item.weight] - item.value,newtbl[j + item.weight-1])
    return newtbl

def dynProgramming(items, capacity):
    tbl = [0 for i in xrange(capacity + 1)]
    taken = [0] * len(items)
    for i in xrange(0, len(items)):
        for j in reversed(xrange(capacity+1)):
            if j-items[i].weight < 0:
                break
            t = tbl[j-items[i].weight] + items[i].value
            if items[i].weight <= j:
                tbl[j] = max(t, tbl[j])
    value = tbl[-1]
    j = capacity
    weight = 0
    for i in reversed(xrange(len(items))):
        newtbl = backtrace(tbl, items[i])
        if tbl[j] > newtbl[j]:
            taken[i] = 1
            j -= items[i].weight
            weight += items[i].weight
        tbl = newtbl
    return value, 0, taken


def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])

    items = []

    for i in range(1, item_count+1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i-1, int(parts[0]), int(parts[1])))

    # a trivial greedy algorithm for filling the knapsack
    # it takes items in-order until the knapsack is full
    value, weight, taken = dynProgramming(items, capacity)
    # value, weight, taken = greedy(items, capacity)

    # prepare the solution in the specified output format
    output_data = str(value) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, taken))
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
        print 'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)'

