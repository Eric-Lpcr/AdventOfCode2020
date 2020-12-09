from itertools import combinations, islice, accumulate


def is_a_sum_of_two(number, numbers):
    """Checks whether number is the sum of two distinct ones taken from numbers"""
    return number in (sum(c) for c in combinations(numbers, 2))


def find_first_invalid(numbers, n):
    """Returns the first item in numbers which is not the sum of two among its n previous ones"""
    stack = list(islice(numbers, n))
    for number in numbers:
        if not is_a_sum_of_two(number, stack[-n:]):
            return number, stack
        stack.append(number)
    return None, stack


def find_sum_sequence(number, numbers):
    """Returns a sequence of at least two numbers summing up to number"""
    found_seq = None
    i = 0
    while i < len(numbers)-1 and not found_seq:
        sums = list(accumulate(numbers[i:]))
        try:
            index = sums.index(number)  # index+1 is the number of accumulated values in sums
            if index > 1:  # Consider sum of at least *two* numbers
                found_seq = numbers[i:i+index+1]
        except ValueError:  # number is not in sums
            pass
        i += 1
    return found_seq


def main():
    with open('input.txt') as f:
        port_output = (int(line) for line in f.readlines())  # generator: no need to read all input
    preamble_length = 25

    first_invalid_number, stack = find_first_invalid(port_output, preamble_length)
    print(f"First invalid number is {first_invalid_number}")

    seq = find_sum_sequence(first_invalid_number, stack)
    if seq:
        print(f"Sequence sum giving this number is {seq}, answer is {min(seq) + max(seq)}")
    else:
        print(f"Can't find sequence")


if __name__ == '__main__':
    main()
