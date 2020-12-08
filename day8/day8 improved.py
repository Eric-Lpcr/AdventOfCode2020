from types import SimpleNamespace


# Couldn't resist a bit of OOP (I'm coming from C++/Java ;) when I saw execute(program) and repair(program)
# Could even write 'program' instead of 'self', but the latter is recommended
# Program is a list (of Instructions)
class Program(list):
    def __init__(self, instructions):
        # which builds like a list
        list.__init__(self, instructions)

    def execute(self):
        executed_instructions = set()
        accumulator = pointer = 0
        while pointer < len(self):  # Program is a list...
            if pointer in executed_instructions:
                return 'Halted on infinite loop', accumulator
            executed_instructions.add(pointer)
            instruction = self[pointer]  # Program is a list...
            if instruction.op == 'acc':
                accumulator += instruction.param
            elif instruction.op == 'jmp':
                pointer += instruction.param
                continue
            elif instruction.op == 'nop':
                pass
            else:
                raise ValueError(f'Unknown operation {instruction.op} at {pointer}')
            pointer += 1
        return 'Ended', accumulator

    flip_instruction = {'jmp': 'nop', 'nop': 'jmp'}

    def repair(self):
        status, accumulator = None, 0  # oneliner for dual initialisation, usually I don't like, but the tuple is the return value
        for instruction in filter(lambda i: i.op in self.flip_instruction, self):  # iterate only on modifiable instructions
            # no need for pointer here, as instruction is an object, it can be modified directly and program is modified
            original_op = instruction.op
            instruction.op = self.flip_instruction[instruction.op]
            status, accumulator = self.execute()
            if status == 'Ended':
                break
            instruction.op = original_op
        return status, accumulator


def main():
    with open('input.txt') as f:
        # SimpleNameSpace to get .op and .param notation
        # Not always need brackets around "x for x in iterable" => Generator
        # The list is program itself
        program = Program(SimpleNamespace(op=o, param=int(p)) for o, p in
                          # Double comprehension, parenthesis works in place of brackets:
                          # it gives a Generator and avoids creating a list
                          (line.split() for line in f.read().splitlines(keepends=False)))

    status, accumulator = program.execute()
    print(f"Got program status -{status}- with accumulator = {accumulator}")

    status, accumulator = program.repair()
    if status == 'Ended':
        print(f"Modified program ended with accumulator = {accumulator}")
    else:
        print("No program correction found")


if __name__ == '__main__':
    main()
