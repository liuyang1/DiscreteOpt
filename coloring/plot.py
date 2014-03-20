import networkx as nx
import sys
import matplotlib.pyplot as plt


def addEdges(g, edges):
    for e in edges:
        g.add_edge(e[0], e[1])
    return g


def plotEdges(edges):
    G = nx.Graph()
    G = addEdges(G, edges)
    nx.draw(G)
    plt.show()


def loadEdges(f):
    edges = []
    first_line = f.readline()
    for line in f.readlines():
        p = [int(i) for i in line.split()]
        edges.append((p[0], p[1]))
    return edges


if __name__ == "__main__":
    f = open(sys.argv[1])
    edges = loadEdges(f)
    f.close()
    plotEdges(edges)
