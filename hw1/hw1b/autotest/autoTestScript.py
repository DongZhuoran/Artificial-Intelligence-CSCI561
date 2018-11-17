# -*- coding: utf-8 -*-
import random
import os
import sol4


def main():
    num_cases = 10000
    num_pass = 0.0
    l = range(0, 10)
    l = [x * num_cases * 0.1 for x in l]
    for i in xrange(num_cases):
        if i in l:
            print float(i) / num_cases
        testCasesCreator()
        ret = sol4.main()
        os.system("hongyuSolution.py")
        fp = open("output.txt")
        ret2 = int(fp.readline())
        if ret == ret2:
            num_pass += 1
        else:
            print ret, ret2
            input("stop")
        fp.close()
    print "Similarity:", num_pass / num_cases * 100, "%"


def testCasesCreator():
    try:
        fp = open("input.txt", "w")
        fp2 = open("input_cmp.txt", "w")
    except IOError:
        pass
    else:
        n = random.randint(0, 15)  # length of grid
        p = random.randint(0, n)  # number of police
        s = random.randint(0, n * n)  # coord of scooters
        fp.writelines([str(n) + "\n", str(p) + "\n", str(s) + "\n"])
        fp2.writelines([str(n) + "\n", str(p) + "\n", str(s) + "\n"])
        for i in xrange(s * 12):
            x = random.randint(0, n - 1)
            y = random.randint(0, n - 1)
            fp.write(str(x) + "," + str(y) + "\n")
            fp2.write(str(x) + "," + str(y) + "\n")
        fp.close()
        fp2.close()


if __name__ == '__main__':
    main()