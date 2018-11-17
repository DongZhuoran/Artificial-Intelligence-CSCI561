# -*- coding: utf-8 -*-
import time


def isAvailable(row, col):
    global grid
    for i in xrange(row):
        if (queen[i] != -1 and
                (queen[i] == col or queen[i] - col == i - row or queen[i] - col == row - i)):
            return False
    return True


def find(row, p_num):
    global n, p, grid, queen, maxPoints
    if row == n:
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
                # print items, queen
            # print maxTemp
    else:
        for col in xrange(n):
            # print isAvailable(row, col)
            if isAvailable(row, col):
                queen[row] = col
                find(row + 1, p_num - 1)
                queen[row] = -1
        if p_num <= n - row - 1:
            find(row + 1, p_num)
        # print queen


def main():
    '''
        Using N-Queen variation (DFS) with tiny pruning to solve the problem.
        Time complexity: O(n^n).
        :return:
        '''
    global n, p, grid, queen, maxPoints
    try:
        fp = open("input.txt", "r")
        output = open("output.txt", "w")
    except IOError:
        pass
    else:
        n = int(fp.readline())
        p = int(fp.readline())
        s = int(fp.readline())
        grid = [[0 for x in range(n)] for y in range(n)]
        for line in fp:
            coord = line.split(",")
            if len(coord) == 2:
                grid[int(coord[1])][int(coord[0])] += 1
        maxPoints = 0
        queen = [-1] * n
        find(0, p)
        output.write(str(maxPoints))
        fp.close()
        output.close()
        print maxPoints


if __name__ == '__main__':
    start_time = time.time()
    main()
    print "%s seconds" % (time.time() - start_time)