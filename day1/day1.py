import time


def sum_of_two(data, expected_sum=2020):
    for i, a in enumerate(data):
        b = expected_sum - a
        if b in data[i+1:]:  # find in remaining numbers only
            return a, b, a * b
    return None


def sum_of_two_v2(data, expected_sum=2020):
    # limitation : this algorithm doesn't ensure that solution is not made of two different numbers...
    # for example, a single 1010 would return a result with it and itself again.
    # solution is not guaranteed to be a strict combination of 2 among 200
    # It would need more code, but the event specification can be interpreted
    data_set = set(data)
    for a in data:
        b = expected_sum - a
        if b in data_set:  # optimized search with set: faster but duplicates data
            return a, b, a * b
    return None


def sum_of_three(data, expected_sum=2020):
    # same distinct element problem here: a and b are guaranteed to be different entries,
    # but c may be chosen as a or b
    pair_sum = dict()
    for i, a in enumerate(data):
        for b in data[i+1:]:  # pair_sum is half a matrix
            s = a + b
            if s <= expected_sum:  # no need for pairs exceeding expected_sum
                pair_sum[a+b] = (a, b)  # keep numbers giving the sum
    for c in data:
        s = expected_sum - c
        if s in pair_sum:  # optimized search with dict
            (a, b) = pair_sum[s]
            return a, b, c, a * b * c
    return None


def main():
    with open('input.txt') as f:
        data = [int(line) for line in f.readlines()]

    start_time = time.perf_counter()
    res = sum_of_two_v2(data)
    elapsed_time = time.perf_counter() - start_time
    print("Got", res, "in", elapsed_time, "s")

    start_time = time.perf_counter()
    res = sum_of_three(data)
    elapsed_time = time.perf_counter() - start_time
    print("Got", res, "in", elapsed_time, "s")


if __name__ == '__main__':
    main()
