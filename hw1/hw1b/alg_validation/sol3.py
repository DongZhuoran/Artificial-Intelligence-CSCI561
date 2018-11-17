# -*- coding: utf-8 -*-
import time
import math


def find(row, ld, rd, p_num, level, curSum):
    global n, p, grid, upperlim, police, maxPoints
    for r in xrange(level, n - p_num + 1):
        if p_num == 0:
            if curSum > maxPoints:
                maxPoints = curSum
        else:
            pos = upperlim & (~(row | ld | rd))
            while pos:
                po = pos & (~pos + 1)
                pos = pos - po
                police[level] = n - int(math.log(po, 2)) - 1
                curSum += grid[level][police[level]]
                find(row | po, (ld | po) << 1, (rd | po) >> 1, p_num - 1, r + 1, curSum)
                curSum -= grid[level][police[level]]
                police[level] = -1


def main():
    global n, p, grid, upperlim, police, maxPoints
    try:
        fp = open("input.txt", "r")
        output = open("output.txt", "w")
    except IOError:
        pass
    else:
        n = int(fp.readline())  # Length of one side of the grid
        p = int(fp.readline())  # Number of police
        s = int(fp.readline())  # Number of scooters, useless here

        # Initialize the grid with values.
        grid = [[0 for x in range(n)] for y in range(n)]
        for line in fp:
            coord = line.split(",")
            if len(coord) == 2:
                grid[int(coord[1])][int(coord[0])] += 1

        maxPoints = 0  # Record the max points the police can get in total.
        # If the number of police is 1, return the largest number in the grid
        if p == 1:
            for l in grid:
                maxPoints = max(maxPoints, max(l))
        else:
            police = [-1] * n
            upperlim = (1 << n) - 1
            find(0, 0, 0, p, 0, 0)
        output.write(str(maxPoints))
        fp.close()
        output.close()
        print maxPoints


if __name__ == '__main__':
    start_time = time.time()
    main()
    print "%s seconds" % (time.time() - start_time)