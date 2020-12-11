from collections import Counter
from itertools import tee


def pairwise(iterable):
    """s -> (s0,s1), (s1,s2), (s2, s3), ..."""
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def differences(numbers):
    """s -> s1-s0, s2-s1, s3-s2, ..."""
    return (y - x for x, y in pairwise(numbers))


def count_adapter_chains(adapters_joltage):
    """Counts the number of chains which can produce output_joltage with adapters"""
    nb_chains = Counter()
    nb_chains[adapters_joltage[0]] = 1  # one chain to get to the first adapter input

    for adapter_ouput in adapters_joltage[1:]:
        # input to this adapter must be 1, 2 or 3 jolts less than its output
        # so the number of chains to get this output is the sum of the numbers of chains giving each possible input
        for delta_jolt in [1, 2, 3]:
            nb_chains[adapter_ouput] += nb_chains[adapter_ouput - delta_jolt]
    return nb_chains[adapters_joltage[-1]]


def main():
    with open('input.txt') as f:
        adapters_joltage = (int(line) for line in f.readlines())

    outlet_joltage = 0
    builtin_adapter_power = 3

    adapters_joltage = [outlet_joltage,  *sorted(adapters_joltage)]
    device_joltage = adapters_joltage[-1] + builtin_adapter_power
    adapters_joltage. append(device_joltage)

    distribution = Counter(differences(adapters_joltage))
    print(f"Got {distribution} adapters power distribution, answer is {distribution[1] * distribution[3]}")

    number_of_adapter_chains = count_adapter_chains(adapters_joltage)
    print(f"{number_of_adapter_chains} possible adapter chains to get {device_joltage} jolts for device")


if __name__ == '__main__':
    main()
