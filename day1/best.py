# https://github.com/mdumke/aoc2020/blob/main/day01/main.py
import math
from itertools import combinations


def sum_to(target: int, n: int, values: [int]) -> [int]:
    """return the n values that sum to target"""
    for group in combinations(values, n):
        if sum(group) == target:
            return group


print('part 1:', math.prod(sum_to(2020, 2, values)))


# unknown source

def solution(target, n, data):
    return next(math.prod(c) for c in combinations(data, n) if sum(c) == target)
