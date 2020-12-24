from itertools import chain


def initialise(labels, n_cups=None):
    """Returns a dict cup label -> following cup label"""
    labels = list(map(int, labels))
    n_labels = len(labels)
    if n_cups is None:
        n_cups = n_labels

    all_labels = chain(labels, range(n_labels + 1, n_cups + 1))
    following_cup = dict()  # key is cup label, value is the following label
    current_cup = cur = next(all_labels, None)
    while label := next(all_labels, None):
        following_cup[cur] = label
        cur = label
    following_cup[cur] = current_cup

    return following_cup, current_cup


def print_cups(following_cup, current_cup):
    print('cups:', end='')
    cur = current_cup
    for _ in range(len(following_cup)):
        if cur == current_cup:
            print(f' ({cur})', end='')
        else:
            print(f' {cur}', end='')
        cur = following_cup[cur]
    print()


def play(input_text, n_cups=None, n_times=10):
    following_cup, current_cup = initialise(input_text, n_cups)
    n_cups = len(following_cup)
    for n_move in range(n_times):
        # print(f'-- move {n_move + 1} --')
        # print_cups(following_cup, current_cup)
        pick = [pick1 := following_cup[current_cup],
                pick2 := following_cup[pick1],
                pick3 := following_cup[pick2]]
        # print(f'pick up: {", ".join(map(str, pick))}')
        following_cup[current_cup] = following_cup[pick3]

        destination = current_cup - 1 if current_cup > 1 else n_cups
        while destination in pick:
            destination = destination - 1 if destination > 1 else n_cups
        # print(f'destination: {destination}\n')

        following_cup[pick3] = following_cup[destination]
        following_cup[destination] = pick1

        current_cup = following_cup[current_cup]

    # print('-- final --')
    # print_cups(following_cup, current_cup)

    return following_cup, current_cup


def main():
    input_text = '916438275'
    # input_text = '389125467'  # example

    following_cup, current_cup = play(input_text, n_times=100)
    cup = 1
    cups = []
    while (cup := following_cup[cup]) != 1:
        cups.append(cup)
    end_labels = ''.join(map(str, cups))
    print(f"\nPart 1: labels on the cups are: {end_labels}\n")

    following_cup, current_cup = play(input_text, n_cups=1_000_000, n_times=10_000_000)
    result = following_cup[1] * following_cup[following_cup[1]]
    print(f"\nPart 2: product of labels after cup 1 is: {result}\n")


if __name__ == '__main__':
    main()
