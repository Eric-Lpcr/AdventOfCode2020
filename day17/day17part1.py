from itertools import product, repeat
from collections import namedtuple

Coord = namedtuple('Coord', 'x y z')

study_pattern = set(Coord(*p) for p in product([-1, 0, 1], repeat=3))
neighbor_pattern = study_pattern - {Coord(0, 0, 0)}


def print_3d_pocket(pocket):
    if len(pocket) == 0:
        print('empty pocket')
        return

    cubes = iter(pocket)
    min_x, min_y, min_z = next(cubes)
    max_x, max_y, max_z = min_x, min_y, min_z
    for cube in cubes:
        min_x = min(min_x, cube.x)
        min_y = min(min_y, cube.y)
        min_z = min(min_z, cube.z)
        max_x = max(max_x, cube.x)
        max_y = max(max_y, cube.y)
        max_z = max(max_z, cube.z)

    def from_to(i, j):
        return range(i, j + 1)

    for z in from_to(min_z, max_z):
        print(f'z={z}')
        for y in from_to(min_y, max_y):
            for x in from_to(min_x, max_x):
                if is_cube_active_at(Coord(x, y, z), pocket):
                    print('#', end='')
                else:
                    print('.', end='')
            print()
        print()


def offset(coord, rel_coord):
    return Coord(*(c1 + c2 for c1, c2 in zip(coord, rel_coord)))


def neighbors(coord, pattern):
    return (offset(coord, p) for p in pattern)


def is_cube_active_at(cube_coord, pocket):
    return cube_coord in pocket


def neighbors_status(cube_coord, pocket, activity):
    return (p for p in neighbors(cube_coord, neighbor_pattern)
            if is_cube_active_at(p, pocket) == activity)


def count_active_neighbors(coord, pocket):
    return len(list(neighbors_status(coord, pocket, True)))


def evolve(cube_coord, pocket, new_pocket):
    n = count_active_neighbors(cube_coord, pocket)
    if is_cube_active_at(cube_coord, pocket):
        if 2 <= n <= 3:
            new_pocket.add(cube_coord)
    else:
        if n == 3:
            new_pocket.add(cube_coord)


def cycle(pocket, times):
    new_pocket = set()
    for _ in range(times):
        evolving_cubes = set()
        for active_cube_coord in pocket:
            evolving_cubes.update(neighbors(active_cube_coord, study_pattern))
        new_pocket = set()
        for cube_coord in evolving_cubes:
            evolve(cube_coord, pocket, new_pocket)
        pocket = new_pocket
    return new_pocket


def main():
    input_text = '''......##
####.#..
.##....#
.##.#..#
........
.#.#.###
#.##....
####.#..'''

#     input_text = '''.#.
# ..#
# ###'''

    pocket = set()
    for y, line in enumerate(input_text.splitlines()):
        for x, cube_activity in enumerate(line):
            if cube_activity == '#':
                pocket.add(Coord(x, y, z=0))
    # print_pocket(pocket)

    new_pocket = cycle(pocket, times=6)
    print(f"Got {len(new_pocket)} active cube")


if __name__ == '__main__':
    main()
