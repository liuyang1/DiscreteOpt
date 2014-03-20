from collections import Counter


def statDegree(edges):
    cnt = Counter()
    for i in edges:
        cnt.update(i)
    return cnt

def isLink(newnode, nodeset, edges):
    return any((newnode, n) in edges for n in nodeset) or any((n, newnode) in edges for n in nodeset)


def welchPowll(edges):
    degree = statDegree(edges)
    nodeN = len(degree.keys())
    colors = {}
    c = 0
    nodelist = [d[0] for d in degree.most_common()]
    for i in xrange(len(nodelist)):
        node = nodelist[i]
        if node in colors.keys():
            continue
        colors[node] = c
        nodeset = [node]
        for j in xrange(i + 1, len(nodelist)):
            newnode = nodelist[j]
            if not isLink(newnode, nodeset, edges):
                colors[newnode] = c
                nodeset.append(newnode)
        c += 1
    lst = sorted(colors.keys())
    ret = []
    for k in lst:
        ret.append(colors[k])
    return ret


def easyTest():
    edges = [[1, 2], [2, 5], [1, 5], [4, 5], [4, 3], [3, 2], [4, 6]]
    print welchPowll(edges)


if __name__ == "__main__":
    easyTest()
