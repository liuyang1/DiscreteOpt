import networkx as nx
import sys
import matplotlib.pyplot as plt

def plotPath(points, path):
    for i in xrange(len(path)-1):
        pair = (points[path[i]], points[path[i+1]])
        pair = zip(*pair)
        plt.plot(pair[0], pair[1], color="blue")
    pair = (points[path[-1]], points[path[0]])
    pair = zip(*pair)
    plt.plot(pair[0], pair[1], label="$end$", color="blue", linewidth=3)

def plotPoints(points):
    points = zip(*points)
    plt.scatter(points[0], points[1])


def loadPoints(f):
    points = []
    first_line = f.readline()
    for line in f.readlines():
        p = [float(i) for i in line.split()]
        points.append((p[0], p[1]))
    return points


if __name__ == "__main__":
    f = open(sys.argv[1])
    points = loadPoints(f)
    f.close()
    print points
    plotPoints(points)
    import tsp
    path = tsp.greedyDfs(points)
    print path
    plotPath(points, path)
    plt.show()
