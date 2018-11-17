# -*- coding: utf-8 -*-
import time


def isCompatible(row, col):
    global police
    for i in xrange(n):
        if (police[i] != -1 and
                (police[i] - col == i - row or police[i] - col == row - i)):
            return False
    return True


def find(p_num, curSum, start):
    '''
    Args:
        p_num: Number of non-put police
        curSum: Current sum of points
    '''
    global n, p, grid_sorted, maxPoints, police, police_col
    if p_num == 0:
        # compare and return maxPoints
        if curSum > maxPoints:
            maxPoints = curSum
    else:
        for head in xrange(start, n*n - p_num + 1):
            latterSum = 0
            for i in xrange(head, head + p_num):
                latterSum += grid_sorted[i][1]
            if curSum + latterSum > maxPoints and \
                    grid_sorted[head][1] > (maxPoints - curSum) / p_num:
                row = grid_sorted[head][0][0]
                col = grid_sorted[head][0][1]
                if police[row] == -1 and police_col[col] == -1 and isCompatible(row, col):
                    police[row] = col
                    police_col[col] = 1
                    find(p_num - 1, curSum + grid_sorted[head][1], head + 1)
                    police[row] = -1
                    police_col[col] = -1
            else:
                break


def main():
    global n, p, grid_sorted, maxPoints, police, police_col
    try:
        fp = open("input.txt", "r")
        # output = open("output.txt", "w")
    except IOError:
        pass
    else:
        n = int(fp.readline())
        p = int(fp.readline())
        s = int(fp.readline())

        # Initialize the grid with values.
        grid = [[0 for x in range(n)] for y in range(n)]
        for line in fp:
            coord = line.split(",")
            if len(coord) == 2:
                grid[int(coord[1])][int(coord[0])] += 1
        # Create grid_sorted and sort
        grid_sorted = [0] * (n * n)
        for x in xrange(n):
            for y in xrange(n):
                grid_sorted[x * n + y] = ((x, y), grid[x][y])
        grid_sorted.sort(key=lambda l: l[1], reverse=True)
        maxPoints = 0  # Record the max points the police can get in total.
        police = [-1] * n
        police_col = [-1] * n  # A trade-off between time and space
        find(p, 0, 0)
        # output.write(str(maxPoints))
        fp.close()
        # output.close()
        # print maxPoints
        return maxPoints


if __name__ == '__main__':
    start_time = time.time()
    main()
    print "%s seconds" % (time.time() - start_time)