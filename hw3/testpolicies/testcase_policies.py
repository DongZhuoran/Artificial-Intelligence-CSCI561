# -*- coding: utf-8 -*-


def main(num, fp_res):
    global grid_size, car_num
    fp_in = open('./testcase_policies/policy' + str(num) + '.txt', 'r')
    fp_out = open('./testcase_policies/policy' + str(num) + '_print.txt', 'w')

    # Load parameters
    grid_size = int(fp_in.readline())
    car_num = int(fp_in.readline())
    for i in xrange(car_num):
        policy = [[[-1, -1]] * grid_size for _ in xrange(grid_size)]
        for j in xrange(grid_size * grid_size):
            poses = fp_in.readline().strip().split(':')
            if poses[1] == ' None':
                continue
            ps = map(int, poses[0].replace('(', '').replace(')', '').split(',')[::-1])
            pt = map(int, poses[1].replace('(', '').replace(')', '').split(',')[::-1])
            policy[ps[0]][ps[1]] = [ps[0] + pt[0], ps[1] + pt[1]]
        fp_out.write('car ' + str(i) + '\n')
        print_policy(policy, fp_out)

    fp_in.close()
    fp_out.close()

    policy_compare(num, fp_res)


def policy_compare(num, fp_res):
    global grid_size, car_num
    fp_p1 = open('./testcase_policies/policy' + str(num) + '_print.txt', 'r')
    fp_p2 = open('./policy' + str(num) + '_print.txt', 'r')

    fp_res.write('case ' + str(num) + '\n')
    for i in xrange(car_num):
        fp_p1.readline()
        fp_p2.readline()
        for j in xrange(grid_size):
            l1 = fp_p1.readline().strip().split(' ')
            l2 = fp_p2.readline().strip().split(' ')
            for k in xrange(grid_size):
                if l1[k] != l2[k]:
                    fp_res.write('car ' + str(i) + ' line ' + str(j) + '\n')
                    print 'car ' + str(i)
        fp_p1.readline()
        fp_p2.readline()
    fp_res.write("\n")

    fp_p1.close()
    fp_p2.close()


def print_policy(policy, out):
    global grid_size
    p_print = [['T'] * grid_size for _ in xrange(grid_size)]
    for i in xrange(grid_size):
        for j in xrange(grid_size):
            if policy[i][j][0] == -1 and policy[i][j][1] == -1:
                out.write("T ")
                continue
            n = ''
            if policy[i][j][0] < i:
                n = '^'
            if policy[i][j][0] > i:
                n = 'v'
            if policy[i][j][1] > j:
                n = '>'
            if policy[i][j][1] < j:
                n = '<'
            p_print[i][j] = n
            out.write(n + " ")
        out.write('\n')
    out.write('\n')
    # print np.array(p_print)


if __name__ == '__main__':
    fp_res = open('./result.txt', 'w')
    for i in xrange(3):
        main(i, fp_res)
    fp_res.close()