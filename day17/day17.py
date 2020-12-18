""" Conway hypercubes """

from itertools import product, repeat
from collections import namedtuple


class Pocket(set):
    def __init__(self, n_dims):
        super().__init__()
        self.n_dims = n_dims
        self.Coord = namedtuple('Coord', list('xyzwabcdefghijklmnopqrstuv'[:n_dims]),
                                defaults=tuple(repeat(0, n_dims)))
        self.neighbor_pattern = set(self.Coord(*c) for c in product([-1, 0, 1], repeat=n_dims)) - {self.Coord()}

    def load(self, input_text):
        for y, line in enumerate(input_text.splitlines()):
            self.update(self.Coord(x, y) for x, active in enumerate(line) if active == '#')

    def is_cube_active_at(self, coord):
        return coord in self

    def offset(self, coord, rel_coord):
        return self.Coord(*map(sum, zip(coord, rel_coord)))

    def neighbors(self, coord):
        return (self.offset(coord, p) for p in self.neighbor_pattern)

    def count_active_neighbors(self, coord):
        active_neighbors = self.intersection(self.neighbors(coord))
        return len(list(active_neighbors))

    def cycle_cube(self, coord, target_pocket):
        n = self.count_active_neighbors(coord)
        active = self.is_cube_active_at(coord)
        if (active and 2 <= n <= 3) or (not active and n == 3):
            target_pocket.add(coord)  # set it active

    def cycle(self, times):
        new_pocket = source_pocket = self
        for _ in range(times):
            evolving_cubes = set()
            for active_cube_coord in source_pocket:
                evolving_cubes.add(active_cube_coord)
                evolving_cubes.update(source_pocket.neighbors(active_cube_coord))
            new_pocket = Pocket(source_pocket.n_dims)
            for coord in evolving_cubes:
                source_pocket.cycle_cube(coord, new_pocket)
            source_pocket = new_pocket
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

    test_input_text = '''.#.
..#
###'''

    for n_dims in [3, 4]:
        pocket = Pocket(n_dims)
        pocket.load(input_text)
        new_pocket = pocket.cycle(times=6)
        print(f"Got {len(new_pocket)} active cube with {n_dims}-D pocket ")


if __name__ == '__main__':
    main()


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
                if pocket.is_cube_active_at(pocket.Coord(x, y, z)):
                    print('#', end='')
                else:
                    print('.', end='')
            print()
        print()
