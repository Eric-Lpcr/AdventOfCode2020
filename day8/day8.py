
def execute(program):
    executed_instructions = set()
    pointer = 0
    accumulator = 0
    while True:
        if pointer >= len(program):
            return 'Ended', accumulator
        op, param = program[pointer].split()
        param = int(param)
        if pointer in executed_instructions:
            return 'Infinite loop', accumulator
        executed_instructions.add(pointer)
        if op == 'acc':
            accumulator += param
            pointer += 1
        elif op == 'jmp':
            pointer += param
        elif op == 'nop':
            pointer += 1


def main():
    with open('input.txt') as f:
        program = f.readlines()

#     program = '''nop +0
# acc +1
# jmp +4
# acc +3
# jmp -3
# acc -99
# acc +1
# jmp -4
# acc +6'''.splitlines(False)

    status, accumulator = execute(program)
    print(f"Got program status -{status}- with accumulator = {accumulator}")

    flip_instruction = {'jmp': 'nop', 'nop': 'jmp'}
    status = None
    for pointer, instruction in enumerate(program):
        op, param = instruction.split()
        if op in flip_instruction:
            program[pointer] = flip_instruction[op] + ' ' + param
            status, accumulator = execute(program)
            if status == 'Ended':
                break
            program[pointer] = instruction

    if status == 'Ended':
        print(f"Modified program ended with accumulator = {accumulator}")
    else:
        print("No program correction found")


if __name__ == '__main__':
    main()
