def play_game(starting_numbers, turns):
    spoken = dict()
    number = 0
    for turn, number in enumerate(starting_numbers):
        spoken[number] = turn + 1
    previous_number = number
    for turn in range(len(starting_numbers)+1, turns+1):
        if previous_number in spoken:
            number = turn - 1 - spoken[previous_number]
        else:
            number = 0
        spoken[previous_number] = turn - 1
        previous_number = number
    return number


def main():
    starting_numbers = [0, 13, 16, 17, 1, 10, 6]

    end_number = play_game(starting_numbers, 2020)
    print(f'Part 1 game gives {end_number}')

    end_number = play_game(starting_numbers, 30000000)
    print(f'Part 2 game gives {end_number}')


if __name__ == '__main__':
    main()

# Test for part 1
#     starting_numbers = [0, 3, 6]
