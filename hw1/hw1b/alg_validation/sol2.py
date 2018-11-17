# -*- coding: utf-8 -*-
import time
import math


def find(row, ld, rd, p_num, level):
    global n, p, grid, upperlim, queen, maxPoints
    if level == n:
        # compare and return maxPoints
        if p_num <= 0:
            items = []
            for i in xrange(n):
                if queen[i] != -1:
                    items.append(grid[i][queen[i]])
            items.sort(reverse=True)
            maxTemp = 0
            for i in xrange(p):
                maxTemp += items[i]
            if maxTemp > maxPoints:
                maxPoints = maxTemp
    else:
        pos = upperlim & (~(row | ld | rd))
        while pos:
            po = pos & (~pos + 1)  # take the last 1
            pos = pos - po
            queen[level] = n - int(math.log(po, 2)) - 1  # costs a lot
            find(row | po, (ld | po) << 1, (rd | po) >> 1, p_num - 1, level + 1)
            queen[level] = -1
        if p_num <= n - level - 1:
            find(row, ld << 1, rd >> 1, p_num, level + 1)


def main():
    '''
    Using N-Queen bitwise variation (DFS) with tiny pruning to solve the problem.
    Time complexity: O(n^n).
    :return:
    '''
    global n, p, grid, upperlim, queen, maxPoints
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
            queen = [-1] * n
            upperlim = (1 << n) - 1
            find(0, 0, 0, p, 0)
        output.write(str(maxPoints))
        fp.close()
        output.close()
        print maxPoints


if __name__ == '__main__':
    start_time = time.time()
    main()
    print "%s seconds" % (time.time() - start_time)