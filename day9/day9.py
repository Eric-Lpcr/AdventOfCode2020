from itertools import combinations, islice, accumulate


def is_a_sum_of_two(number, numbers):
    """Checks whether number is the sum of two distinct ones taken from numbers"""
    return number in [sum(c) for c in combinations(numbers, 2)]


def find_sum_sequence(number, numbers):
    """Returns a sequence of at least two numbers summing up to number"""
    found_seq = None
    i = 0
    while i < len(numbers) and not found_seq:
        sum_up = list(accumulate(numbers[i:]))
        if number in sum_up[1:]:  # Consider sum of at least *two* numbers
            index = sum_up.index(number)  # index+1 is the number of accumulated values in sum_up
            found_seq = numbers[i:i+index+1]
        i += 1
    return found_seq


def main():
    with open('input.txt') as f:
        port_output = (int(line) for line in f.readlines())

    preamble_length = 25
    stack = list(islice(port_output, preamble_length + 1))  # stack contains preamble and next number to be tested

    while is_a_sum_of_two(stack[-1], stack[-preamble_length-1:-1]):
        stack.append(next(port_output))  # Should trap IterationError in case there is no invalid number...
    first_invalid_number = stack.pop()
    print(f"First invalid number is {first_invalid_number}")

    seq = find_sum_sequence(first_invalid_number, stack)
    if seq:
        print(f"Sequence sum giving this number is {seq}, answer is {min(seq) + max(seq)}")
    else:
        print(f"Can't find sequence")


if __name__ == '__main__':
    main()
