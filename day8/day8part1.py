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

    executed_instructions = set()
    pointer = 0
    accumulator = 0
    while True:
        op, param = program[pointer].split()
        param = int(param)
        if pointer in executed_instructions:
            break
        executed_instructions.add(pointer)
        if op == 'acc':
            accumulator += param
            pointer += 1
        elif op == 'jmp':
            pointer += param
        elif op == 'nop':
            pointer += 1

    print(f"Got accumulator = {accumulator}")


if __name__ == '__main__':
    main()
