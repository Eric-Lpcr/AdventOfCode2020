from math import prod
from operator import add, mul
import re

operators = {'+': add, '*': mul}


def tokenize(expression):
    tokens = []
    for token in re.findall(r'\d+|[+*()]', expression):
        if token.isdigit():
            tokens.append(int(token))
        elif token in operators:
            tokens.append(operators[token])
        else:
            tokens.append(token)
    return tokens


def compute1(tokens):
    res = tokens[0]
    current_op = None
    for token in tokens[1:]:
        if token in operators.values():
            current_op = token
        else:
            res = current_op(res, token)
    return res


def compute2(tokens):
    sums = []
    current_sum = []
    for token in tokens:
        if token == mul:
            sums.append(compute1(current_sum))
            current_sum = []
        else:
            current_sum.append(token)
    sums.append(compute1(current_sum))
    return prod(sums)


def evaluate(expression, compute=compute1):
    tokens = tokenize(expression)
    expr_stack = []
    current_expr = []
    for token in tokens:
        if token == '(':
            expr_stack.append(current_expr)
            current_expr = []
        elif token == ')':
            sub_result = compute(current_expr)
            current_expr = expr_stack.pop()
            current_expr.append(sub_result)
        else:
            current_expr.append(token)
    return compute(current_expr)


def main():
    with open('input.txt') as f:
        expressions = f.readlines()

    res1 = sum(evaluate(expression) for expression in expressions)
    print(f'Part 1 sum of results is {res1}')

    res2 = sum(evaluate(expression, compute=compute2) for expression in expressions)
    print(f'Part 2 sum of results is {res2}')


if __name__ == '__main__':
    main()

    # expressions = '''1 + 2 * 3 + 4 * 5 + 6
    # 1 + (2 * 3) + (4 * (5 + 6))
    # 2 * 3 + (4 * 5)
    # 5 + (8 * 3 + 9 + 3 * 4 * 3)
    # 5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))
    # ((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2'''.splitlines()


