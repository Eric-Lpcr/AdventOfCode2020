import re
from itertools import zip_longest


class Computer:
    def __init__(self):
        self.memory = dict()
        self.bitmask = ''
        self.bitmask_X1 = self.bitmask_X0 = 0

    def set_mask(self, mask):
        self.bitmask = mask
        self.bitmask_X1 = int(mask.replace('X', '1'), base=2)
        self.bitmask_X0 = int(mask.replace('X', '0'), base=2)

    mask_pattern = re.compile(r'mask\s*=\s*([X01]+)')
    mem_pattern = re.compile(r'mem\[(\d+)]\s*=\s*(\d+)')

    def execute(self, program):
        for instruction in program:
            if match := self.mask_pattern.match(instruction):
                self.set_mask(match.group(1))
            elif match := self.mem_pattern.match(instruction):
                self.set_memory(int(match.group(1)), int(match.group(2)))
            else:
                raise SyntaxError('Erroneous instruction')
        return sum(self.memory.values())

    def set_memory(self, address, value):
        self.memory[address] = value


class ComputerV1(Computer):
    def decode_value(self, value):
        return value & self.bitmask_X1 | self.bitmask_X0

    def set_memory(self, address, value):
        self.memory[address] = self.decode_value(value)


class ComputerV2(Computer):
    def __init__(self):
        Computer.__init__(self)
        self.floating_masks = []

    def set_mask(self, mask):
        Computer.set_mask(self, mask)
        floating_bits_positions = [i for i, c in enumerate(reversed(mask)) if c == 'X']
        xs = list(range(2**len(floating_bits_positions)))  # all combinations of floating bits
        # Need to put them at their right place, inserting zeroes
        ys = []
        for i in range(len(floating_bits_positions)):
            ys = [y | (x >> i & 1) << floating_bits_positions[i] for x, y in zip_longest(xs, ys, fillvalue=0)]
        self.floating_masks = ys

    def decode_address(self, address):
        address |= self.bitmask_X1
        return [address ^ mask for mask in self.floating_masks]

    def set_memory(self, address, value):
        for an_address in self.decode_address(address):
            self.memory[an_address] = value


def main():
    with open('input.txt') as f:
        program = f.readlines()

    computer = ComputerV1()
    memory_sum = computer.execute(program)
    print(f'With decode chip V1, got sum of memory values = {memory_sum}')

    computer = ComputerV2()
    memory_sum = computer.execute(program)
    print(f'With decode chip V2, got sum of memory values = {memory_sum}')


if __name__ == '__main__':
    main()

# Test program for part 1
#     program = '''mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
# mem[8] = 11
# mem[7] = 101
# mem[8] = 0'''.splitlines()

# Test program for part 2
#     program = '''mask = 000000000000000000000000000000X1001X
# mem[42] = 100
# mask = 00000000000000000000000000000000X0XX
# mem[26] = 1
# '''.splitlines()
