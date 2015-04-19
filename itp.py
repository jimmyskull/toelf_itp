# -*- coding: utf-8 -*-
# Copyright © 2015, Paulo Urio.
from math import ceil, floor
import numpy as np
from scipy import optimize

# Score → correct questions
Q1 = lambda x: ceil((x - 31) / (68 - 31) * 50)
Q2 = lambda x: ceil((x - 31) / (68 - 31) * 40)
Q3 = lambda x: ceil((x - 31) / (67 - 31) * 50)

# Correct questions → score
N1 = lambda x: floor(x / 50 * (68 - 31) + 31)
N2 = lambda x: floor(x / 40 * (68 - 31) + 31)
N3 = lambda x: floor(x / 50 * (67 - 31) + 31)

# Obs: x == N1(Q1(x))

# Separated score → total score
N = lambda a, b, c: (a + b + c - 31 * 3) * (677-310) / (68+68+67-31*3) + 310
NQ = lambda a, b, c: N(N1(a), N2(b), N3(c))
QN = lambda a, b, c: np.array([Q1(a), Q2(b), Q3(c)])

TARGET = 628 # The minimum for proficiency is 627
def f(x):
    return abs(TARGET - N(*x))

def TOEFL_iTP(n1, n2, n3):
    print('Section 1: {} points, {}/50 ({} missed)'.format(n1, Q1(n1), 50-Q1(n1)))
    print('Section 2: {} points, {}/40 ({} missed)'.format(n2, Q2(n2), 40-Q2(n2)))
    print('Section 3: {} points, {}/50 ({} missed)'.format(n3, Q3(n3), 50-Q3(n3)))
    print('Total: {}/677\n'.format(floor(N(n1, n2, n3))))
    parameters = np.array([n1, n2, n3])
    bounds = ((31, 68), (31, 68), (31, 67))
    r = optimize.minimize(f, parameters, method = 'SLSQP', bounds=bounds,\
            options={'disp': True, 'eps': 1.0})
    print('\nYour result:', QN(*parameters))
    print('Optimized  :', QN(*r.x))
    print('How many more questions you would have to get correct:\n ' + \
            'Section 1: {}\n Section 2: {}\n Section 3: {}\n'.format(\
                *(QN(*r.x) - QN(*parameters))))
    print('And then you’d get a score of {}'.format(NQ(*QN(*r.x))))

TOEFL_iTP(n1=64, n2=63, n3=57)

