# -*- coding: utf-8 -*-
'''
Created on Nov 16, 2018

@author: Zhuoran Dong

Version 3:
Take going into walls as a policy and update utilities after calculating new utilities.
'''
import time
import numpy as np
import copy


def main(num):
    global grid_size
    # Get pointers of input & output files.
    fp_in = open('./testcase_policies/policy' + str(num) + '.txt', 'r')
    fp_out = open('output.txt', 'w')
    policy_out = open('policy' + str(num) + '_print.txt', 'w')

    # Load parameters
    grid_size = int(fp_in.readline())
    car_num = int(fp_in.readline())
    obstacle_num = int(fp_in.readline())
    obstacles = []
    for i in xrange(obstacle_num):
        obstacles.append(map(int, fp_in.readline().split(',')[::-1]))
    cars = []
    for i in xrange(car_num):
        cars.append(map(int, fp_in.readline().split(',')[::-1]))
    ends = []
    for i in xrange(car_num):
        ends.append(map(int, fp_in.readline().split(',')[::-1]))

    # Initialize reward
    rewards = []
    reward = [[-1] * grid_size for _ in xrange(grid_size)]
    for o in obstacles:
        reward[o[0]][o[1]] -= 100
    for i in xrange(car_num):
        rewards.append(copy.deepcopy(reward))
        rewards[i][ends[i][0]][ends[i][1]] += 100

    # First part: generate policy for each car.
    policies = []
    for i in xrange(car_num):
        t_pos = ends[i]
        # Step 1: Initialize utility chart for car i.
        utility = copy.deepcopy(rewards[i])
        # Step 2: Initialize policy for car i.
        policy = [[[0, 0]] * grid_size for _ in xrange(grid_size)]
        policy[t_pos[0]][t_pos[1]] = [-1, -1]  # Terminal point.
        # Step 3: Generate the policy.
        policy = generate_policy(rewards[i], policy, utility, t_pos, 0.9, 0.1)
        policies.append(policy)
        policy_out.write('car ' + str(i) + '\n')
        print_policy(policy, policy_out)

    # Second part: simulation.
    ave_amounts = []
    for i in xrange(car_num):
        ave_amount = simulation(rewards[i], cars[i], ends[i], policies[i])
        fp_out.write(str(ave_amount) + '\n')
        ave_amounts.append(ave_amount)
    print ave_amounts

    fp_in.close()
    fp_out.close()
    policy_out.close()


def simulation(reward, car, end, policy):
    amount = 0
    for j in xrange(10):
        pos = copy.deepcopy(car)
        # Do not add the reward at start point!!!
        # amount += reward[pos[0]][pos[1]]
        np.random.seed(j)
        swerve = np.random.random_sample(1000000)
        k = 0
        while pos != end:
            move = copy.deepcopy(policy[pos[0]][pos[1]])
            if swerve[k] > 0.7:
                if swerve[k] > 0.8:
                    if swerve[k] > 0.9:
                        move = turn(pos, move, 180)
                    else:
                        move = turn(pos, move, 270)
                else:
                    move = turn(pos, move, 90)
            pos = move
            normalize_pos(pos)
            k += 1
            amount += reward[pos[0]][pos[1]]
    return amount // 10


def normalize_pos(pos):
    global grid_size
    if pos[0] < 0:
        pos[0] = 0
    if pos[0] == grid_size:
        pos[0] = grid_size - 1
    if pos[1] < 0:
        pos[1] = 0
    if pos[1] == grid_size:
        pos[1] = grid_size - 1


def turn(pos, move, degree):
    global grid_size

    if pos[1] == move[1]:
        if pos[0] > move[0]:
            if degree == 90:
                if pos[1] - 1 >= 0:
                    return [pos[0], pos[1] - 1]
                else:
                    return pos
            if degree == 180:
                if pos[0] + 1 < grid_size:
                    return [pos[0] + 1, pos[1]]
                else:
                    return pos
            if degree == 270:
                if pos[1] + 1 < grid_size:
                    return [pos[0], pos[1] + 1]
                else:
                    return pos
        else:
            if degree == 90:
                if pos[1] + 1 < grid_size:
                    return [pos[0], pos[1] + 1]
                else:
                    return pos
            if degree == 180:
                if pos[0] - 1 >= 0:
                    return [pos[0] - 1, pos[1]]
                else:
                    return pos
            if degree == 270:
                if pos[1] - 1 >= 0:
                    return [pos[0], pos[1] - 1]
                else:
                    return pos
    else:
        if pos[1] > move[1]:
            if degree == 90:
                if pos[0] + 1 < grid_size:
                    return [pos[0] + 1, pos[1]]
                else:
                    return pos
            if degree == 180:
                if pos[1] + 1 < grid_size:
                    return [pos[0], pos[1] + 1]
                else:
                    return pos
            if degree == 270:
                if pos[0] - 1 >= 0:
                    return [pos[0] - 1, pos[1]]
                else:
                    return pos
        else:
            if degree == 90:
                if pos[0] - 1 >= 0:
                    return [pos[0] - 1, pos[1]]
                else:
                    return pos
            if degree == 180:
                if pos[1] - 1 >= 0:
                    return [pos[0], pos[1] - 1]
                else:
                    return pos
            if degree == 270:
                if pos[0] + 1 < grid_size:
                    return [pos[0] + 1, pos[1]]
                else:
                    return pos


def generate_policy(reward, policy, utility, end, gamma=0.9, epsilon=0.1):
    global grid_size
    # Stop condition.
    error = epsilon * (1 - gamma) / gamma
    # The maximum change in the utility of any state.
    delta = 0
    while True:
        new_utility = [[99] * grid_size for _ in xrange(grid_size)]
        for i in xrange(grid_size):
            for j in xrange(grid_size):
                if [i, j] == end:
                    continue
                util_val = utility_calculator(reward, policy, utility, [i, j], gamma)
                delta = max(delta, abs(util_val - utility[i][j]))
                new_utility[i][j] = util_val
        if delta >= error:
            delta = 0
            utility = new_utility
        else:
            break
    # print np.array(utility)
    return policy
    # return update_policy(policy, utility)


def utility_calculator(reward, policy, utility, pos, gamma):
    north = utility[pos[0]][pos[1] - 1] if pos[1] - 1 >= 0 else utility[pos[0]][pos[1]]
    south = utility[pos[0]][pos[1] + 1] if pos[1] + 1 < grid_size else utility[pos[0]][pos[1]]
    east = utility[pos[0] + 1][pos[1]] if pos[0] + 1 < grid_size else utility[pos[0]][pos[1]]
    west = utility[pos[0] - 1][pos[1]] if pos[0] - 1 >= 0 else utility[pos[0]][pos[1]]

    d = 0
    eu_max = north
    if eu_max < south:
        d = 1
        eu_max = south
    if eu_max < east:
        d = 2
        eu_max = east
    if eu_max < west:
        d = 3
        eu_max = west

    eu = 0
    p1 = 0.7
    p2 = 0.1
    if d == 0:
        eu = p1 * north + p2 * (south + east + west)
        policy[pos[0]][pos[1]] = [pos[0], pos[1] - 1]
    elif d == 1:
        eu = p1 * south + p2 * (north + east + west)
        policy[pos[0]][pos[1]] = [pos[0], pos[1] + 1]
    elif d == 2:
        eu = p1 * east + p2 * (north + south + west)
        policy[pos[0]][pos[1]] = [pos[0] + 1, pos[1]]
    elif d == 3:
        eu = p1 * west + p2 * (north + south + east)
        policy[pos[0]][pos[1]] = [pos[0] - 1, pos[1]]
    eu = reward[pos[0]][pos[1]] + gamma * eu
    return eu


def update_policy(policy, utility):
    for i in xrange(grid_size):
        for j in xrange(grid_size):
            # Avoid terminal node.
            if policy[i][j][0] == -1:
                continue
            max_val = -200
            pos = []
            if i - 1 >= 0 and utility[i - 1][j] > max_val:
                max_val = utility[i - 1][j]
                pos = [i - 1, j]
            if i + 1 < grid_size and utility[i + 1][j] > max_val:
                max_val = utility[i + 1][j]
                pos = [i + 1, j]
            if j + 1 < grid_size and utility[i][j + 1] > max_val:
                max_val = utility[i][j + 1]
                pos = [i, j + 1]
            if j - 1 >= 0 and utility[i][j - 1] > max_val:
                max_val = utility[i][j - 1]
                pos = [i, j - 1]
            policy[i][j] = pos
    return policy


def print_policy(policy, out):
    p_print = [['T'] * grid_size for _ in xrange(grid_size)]
    for i in xrange(grid_size):
        for j in xrange(grid_size):
            if policy[i][j][0] == -1 and policy[i][j][1] == -1:
                out.write('T ')
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
            out.write(n + ' ')
        out.write('\n')
    out.write('\n')
    print np.array(p_print)


if __name__ == '__main__':
	for i in xrange(3):
		main(i)