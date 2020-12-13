from collections import Counter
from itertools import chain

from day11.matrix import Matrix


def count_los_neighbours(r, c, room, rows, columns, tolerance):
    neighbours = 0
    for dr, dc in neighbour_pattern:
        rs, cs = r, c
        # find first seat in line of sight
        while 0 <= rs + dr < rows and 0 <= cs + dc < columns:
            rs += dr
            cs += dc
            if room[rs][cs] == 'L':
                break  # no neighbour in this direction
            if room[rs][cs] == '#':
                neighbours += 1
                break  # found neighbour in this direction
        if neighbours >= tolerance:
            break  # no need to find more than tolerance
    return neighbours


def count_adjacent_neighbours(r, c, room, rows, columns, tolerance):
    neighbours = 0
    for dr, dc in neighbour_pattern:
        if 0 <= r + dr < rows and 0 <= c + dc < columns and room[r + dr][c + dc] == '#':
            neighbours += 1
            if neighbours >= tolerance:
                break  # no need to find more than tolerance
    return neighbours


def change_seat_status(seat, neighbours, max_tolerance):
    if seat == 'L' and neighbours == 0:
        return '#'
    elif seat == '#' and neighbours >= max_tolerance:
        return 'L'
    else:
        return seat


def print_waiting_area(waiting_area):
    for row in waiting_area:
        print(''.join(row))
    print()


def play_rule(waiting_area, count_neighbours, max_tolerance):
    rows = len(waiting_area)
    columns = len(waiting_area[0])
    changed = True
    while changed:
        next_state = []
        changed = False
        for r, row in enumerate(waiting_area):
            next_state.append(row.copy())
            for c, place in enumerate(row):
                if place != '.':
                    neighbours = count_neighbours(r, c, waiting_area, rows, columns, max_tolerance)
                    next_state[r][c] = change_seat_status(place, neighbours, max_tolerance)
                    if not changed and next_state[r][c] != place:
                        changed = True
        waiting_area = next_state
    return waiting_area


def main():
    with open('input.txt') as f:
        input_data = f.read().splitlines(keepends=False)

#     input_data = """L.LL.LL.LL
# LLLLLLL.LL
# L.L.L..L..
# LLLL.LL.LL
# L.LL.LL.LL
# L.LLLLL.LL
# ..L.L.....
# LLLLLLLLLL
# L.LLLLLL.L
# L.LLLLL.LL""".splitlines(keepends=False)

    waiting_area = Matrix([list(line) for line in input_data])

    rule1_state = play_rule(waiting_area, count_adjacent_neighbours, max_tolerance=4)
    counter = Counter(chain.from_iterable(rule1_state))
    print(f"Got {counter['#']} occupied seats")

    rule2_state = play_rule(waiting_area, count_los_neighbours, max_tolerance=5)
    counter = Counter(chain.from_iterable(rule2_state))
    print(f"Got {counter['#']} occupied seats")


if __name__ == '__main__':
    main()
