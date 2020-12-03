from math import prod


def traverse_map(forrest_map, dx, dy, x=0, y=0):
    bottom = len(forrest_map)
    pattern_width = len(forrest_map[0])
    res = 0
    while y < bottom:
        if forrest_map[y][x] == '#':
            res += 1
        x += dx
        x %= pattern_width
        y += dy
    return res


def main():
    with open('input.txt') as f:
        input_text = f.read()

    debug_input_text = """..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#"""

    forrest_map = input_text.splitlines(keepends=False)
    del input_text

    # part 1
    dx = 3  # Right 3
    dy = 1  # Down 1
    res1 = traverse_map(forrest_map, dx, dy)
    print(f"Encountered {res1} trees")

    # part 2
    res2 = []
    for (dx, dy) in [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]:
        res2.append(traverse_map(forrest_map, dx, dy))
    print(f"Encountered {res2} trees, answer is {prod(res2)}")


if __name__ == '__main__':
    main()
