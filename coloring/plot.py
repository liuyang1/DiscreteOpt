import networkx as nx
import sys
import matplotlib.pyplot as plt


def addEdges(g, edges):
    for e in edges:
        g.add_edge(e[0], e[1])
    return g


def plotEdges(edges, iscolor=False):
    G = nx.Graph()
    G = addEdges(G, edges)
    if iscolor:
        import welch
        ret = welch.solve_it(edges)
        print zip(range(len(ret)), ret)
        m = max(ret) + 0.0
        val = [i/m for i in ret]
        val_map = zip(range(len(ret)), val)
        nx.draw(G, cmap = plt.get_cmap('jet'), node_color = val)
    else:
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
    plotEdges(edges, True)
