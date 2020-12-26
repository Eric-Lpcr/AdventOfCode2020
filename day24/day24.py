import re
from functools import reduce
from operator import add, itemgetter


class Coord3:
    __slots__ = ['x', 'y', 'z']

    def __init__(self, x=0, y=0, z=0):
        self.x, self.y, self.z = x, y, z

    def __add__(self, other):
        return Coord3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f'({self.x}, {self.y}, {self.z})'

    def __hash__(self):
        return self.x * 31 + self.y * 37 + self.z * 41

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z


(BLACK, WHITE) = (True, False)


class Floor(set):
    neighbor_pattern = {
        'e': Coord3(1, -1, 0),
        'se': Coord3(0, -1, 1),
        'sw': Coord3(-1, 0, 1),
        'w': Coord3(-1, 1, 0),
        'nw': Coord3(0, 1, -1),
        'ne': Coord3(1, 0, -1),
    }  # https://www.redblobgames.com/grids/hexagons/#coordinates

    def color(self, tile, color=None):
        if color is not None:
            if color is BLACK:
                self.add(tile)
            elif tile in self:
                self.remove(tile)
            return color
        return BLACK if tile in self else WHITE

    @property
    def n_black_tiles(self):
        return len(self)

    def flip(self, tile):
        if tile in self:
            self.remove(tile)
        else:
            self.add(tile)

    def neighbors(self, tile):
        return (tile + rel for rel in self.neighbor_pattern.values())

    def count_black_neighbors(self, tile):
        black_neighbors = self.intersection(self.neighbors(tile))
        return len(list(black_neighbors))

    def update_tile(self, tile, next_day_floor):
        n = self.count_black_neighbors(tile)
        color = self.color(tile)
        if (color == BLACK and not (n == 0 or n > 2)) or (color == WHITE and n == 2):
            next_day_floor.add(tile)  # set it black

    def cycle(self, times):
        new_floor = None
        source_floor = self
        for t in range(1, times + 1):
            evolving_tiles = set()
            for black_tile in source_floor:
                evolving_tiles.add(black_tile)
                evolving_tiles.update(source_floor.neighbors(black_tile))
            new_floor = Floor()
            for tile in evolving_tiles:
                source_floor.update_tile(tile, new_floor)
            source_floor = new_floor
            print(f'Day {t}: {source_floor.n_black_tiles}')
        return new_floor

    instruction_regexp = re.compile('|'.join(neighbor_pattern.keys()))

    def tile_at(self, direction_path):
        directions = self.instruction_regexp.findall(direction_path)
        moves = itemgetter(*directions)(self.neighbor_pattern)
        return reduce(add, moves)


def main():
    floor = Floor()

    with open('input.txt') as f:
        for directions in f.readlines():
            floor.flip(floor.tile_at(directions))
    n_days = 100
    next_floor = floor.cycle(times=n_days)

    print(f"Initial floor has {floor.n_black_tiles} black tiles")
    print(f"After {n_days} days, floor has {next_floor.n_black_tiles} black tiles")


if __name__ == '__main__':
    main()
