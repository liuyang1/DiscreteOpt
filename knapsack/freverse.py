import sys


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "input file name as param"
        sys.exit()
    fi = open(sys.argv[1])
    for line in reversed(fi.readlines()):
        print line.strip()
    fi.close()
