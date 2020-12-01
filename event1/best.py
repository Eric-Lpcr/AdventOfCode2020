# https://github.com/mdumke/aoc2020/blob/main/day01/main.py

from itertools import combinations


def sum_to(target: int, n: int, values: [int]) -> [int]:
    """return the n values that sum to target"""
    for group in combinations(values, n):
        if sum(group) == target:
            return group
