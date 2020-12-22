import re
from collections import Counter, namedtuple
from functools import reduce
from itertools import chain, groupby
from math import prod
from operator import add


def reverse(string):
    return ''.join(reversed(string))


N, E, S, W = 0, 1, 2, 3


class Tile:
    def __init__(self, tile_id, lines):
        self.id = tile_id
        self.lines = lines
        if self.lines:
            self.computed_borders = self._compute_borders()

    def __repr__(self):
        return str(self.id)

    def view(self):
        return '\n'.join(self.lines)

    def _compute_borders(self):
        """Returns an array of borders, indexed by directions N, E, S, W"""
        self.computed_borders = [self.lines[0],
                                 ''.join(line[-1] for line in self.lines),
                                 self.lines[-1],
                                 ''.join(line[0] for line in self.lines)]
        return self.computed_borders

    def borders(self):
        return self.computed_borders

    def flipped_borders(self):
        """Returns reversed borders"""
        return list(map(reverse, self.computed_borders))

    def border(self, direction):
        return self.computed_borders[direction]

    def flip_vertical(self):
        self.lines.reverse()
        self._compute_borders()

    def flip_horizontal(self):
        self.lines = list(map(reverse, self.lines))
        self._compute_borders()

    def rotate_cw(self):
        self.lines = [''.join(line[index] for line in reversed(self.lines))
                      for index in range(len(self.lines[0]))]
        self._compute_borders()

    def rotate_ccw(self):
        self.lines = [''.join(line[index] for line in self.lines)
                      for index in reversed(range(len(self.lines[0])))]
        self._compute_borders()

    def rotate_half(self):
        self.flip_vertical()
        self.flip_horizontal()

    def cropped(self):
        return Tile(self.id, [line[1:-1] for line in self.lines[1:-1]])

    def count_hashes(self):
        counter = Counter(''.join(self.lines))
        if '#' in counter:
            return counter['#']
        else:
            return 0


def find_corner_tiles(tiles):
    borders_index = {}  # border => set<tile_id>
    for tile in tiles.values():
        for border, flipped_border in zip(tile.borders(), tile.flipped_borders()):
            if border in borders_index:
                borders_index[border].add(tile.id)
            elif flipped_border in borders_index:
                borders_index[flipped_border].add(tile.id)
            else:
                borders_index[border] = {tile.id}

    edge_tiles = list(next(iter(tile_ids)) for tile_ids in borders_index.values() if len(tile_ids) == 1)
    edge_counter = Counter(edge_tiles)
    corner_tiles = list(tile_id for tile_id, count in edge_counter.items() if count == 2)
    return corner_tiles, borders_index


def reassemble_image(tiles):
    # find corners, pick one
    corner_tiles, borders_index = find_corner_tiles(tiles)
    image = [[]]  # matrix of tiles

    tile = tiles[corner_tiles.pop()]
    # tile = tiles[1951]
    # corner_tiles.remove(1951)

    # orient NW corner
    edge_borders = [border for border in borders_index if borders_index[border] == {tile.id}]
    while tile.border(N) not in edge_borders:
        if reverse(tile.border(N)) in edge_borders:
            tile.flip_horizontal()
        else:
            tile.rotate_ccw()
    if tile.border(W) not in edge_borders and reverse(tile.border(W)) not in edge_borders:
        tile.rotate_cw()

    image_y = 0
    image[image_y].append(tile)
    image_width = 1

    while len(corner_tiles) > 0:
        # build a line of tiles : first line stops at a corner, next ones stop at first line length (image_width)
        while (image_y == 0 and tile.id not in corner_tiles) or (len(image[image_y]) < image_width):
            connect_border = tile.border(E)
            if connect_border in borders_index:
                candidate_tile_id = next(iter(borders_index[connect_border] - {tile.id}))
            else:
                candidate_tile_id = next(iter(borders_index[reverse(connect_border)] - {tile.id}))
            candidate_tile = tiles[candidate_tile_id]
            # orient candidate tile
            while candidate_tile.border(W) != connect_border:
                if candidate_tile.border(W) == reverse(connect_border):
                    candidate_tile.flip_horizontal()
                else:
                    candidate_tile.rotate_cw()
            image[image_y].append(candidate_tile)
            if image_y == 0:
                image_width += 1
            tile = candidate_tile

        if tile.id in corner_tiles:
            corner_tiles.remove(tile.id)
            if len(corner_tiles) == 0:
                break

        # start next line, find first tile connected to previous line first tile
        tile = image[image_y][0]
        if tile.id in corner_tiles:
            corner_tiles.remove(tile.id)
            continue

        connect_border = tile.border(S)
        if connect_border in borders_index:
            candidate_tile_id = next(iter(borders_index[connect_border] - {tile.id}))
        else:
            candidate_tile_id = next(iter(borders_index[reverse(connect_border)] - {tile.id}))
        candidate_tile = tiles[candidate_tile_id]
        # orient candidate tile
        while candidate_tile.border(N) != connect_border:
            if candidate_tile.border(N) == reverse(connect_border):
                candidate_tile.flip_horizontal()
            else:
                candidate_tile.rotate_cw()
        image.append([])
        image_y += 1
        image[image_y].append(candidate_tile)
        tile = candidate_tile

    return image


def build_image(tiles):
    """rebuild the full image, cropping borders"""
    image_tiles = reassemble_image(tiles)
    image = Tile(None, [])
    for row in image_tiles:
        image.lines += list(reduce(add, tiles_lines) for tiles_lines in zip(*(tile.cropped().lines for tile in row)))
    return image


FindReplaceRE = namedtuple('FindReplaceRE', 'find match replace')


def create_re(pattern):
    re_pattern = []
    for line in pattern:
        tokens = [''.join(g) for _, g in groupby(line)]
        match = ''.join(map(lambda g: '(.{' + str(len(g)) + '})' if g.startswith(' ') else '(' + g + ')',
                            tokens))
        # uses (?= look ahead for finditer to match overlapping occurrences
        find = '(?=' + match + ')'
        # keep dot groups in place with \digit
        replace = ''.join(map(lambda t: '\\' + str(t[0] + 1) if t[1].startswith(' ') else t[1].replace('#', 'O'),
                              enumerate(tokens)))
        re_pattern.append(FindReplaceRE(find, match, replace))
    return re_pattern


def highlight_pattern(image, re_pattern):

    n_monsters = 0
    for i in range(len(image.lines) - len(re_pattern)):
        for m in re.finditer(re_pattern[0].find, image.lines[i]):
            pos = m.start()
            multiline_match = True
            for j in range(1, len(re_pattern)):
                multiline_match &= re.match(re_pattern[j].find, image.lines[i + j][pos:]) is not None
                if not multiline_match:
                    break

            if multiline_match:
                for j in range(len(re_pattern)):
                    image.lines[i + j] = image.lines[i + j][:pos] + re.sub(re_pattern[j].match,
                                                                           re_pattern[j].replace,
                                                                           image.lines[i + j][pos:],
                                                                           count=1)
                n_monsters += 1
    return n_monsters


def load_tiles(file_name):
    tiles = {}
    with open(file_name) as f:
        for tile_text in f.read().split('\n\n'):
            tile_desc, *tile_lines = tile_text.splitlines()
            tile_id = int(tile_desc.strip(':')[5:])
            tiles[tile_id] = Tile(tile_id, tile_lines)
    return tiles


def main():
    tiles = load_tiles('input.txt')

    # Part 1
    corner_tiles, _ = find_corner_tiles(tiles)
    print(f'Corner tiles are {corner_tiles}')
    print(f'Part 1: corner tiles id product is {prod(corner_tiles)}')

    image = build_image(tiles)

    pattern = ['                  # ',
               '#    ##    ##    ###',
               ' #  #  #  #  #  #   ']
    re_pattern = create_re(pattern)

    # Part 1
    # do at most 4 rotations, 1 flip, 4 rotations to scan all possible images
    op_counter = 1
    while (n_monsters := highlight_pattern(image, re_pattern)) == 0:
        image.rotate_cw()
        op_counter += 1
        if op_counter == 4:
            image.flip_vertical()
        elif op_counter == 8:
            break

    print('\n', image.view(), '\n')
    print(f"Part 2: found {n_monsters} monster{'s' if n_monsters > 1 else ''}, "
          f"habitat's water roughness is {image.count_hashes()}")


def test():
    tile = Tile(0, ['abc', 'def', 'ghi'])

    print(tile.view(), '\n')
    print(tile.borders(), '\n')
    for _ in range(4):
        tile.rotate_cw()
        print(tile.view(), '\n')

    tile.rotate_half()
    print(tile.view(), '\n')


if __name__ == '__main__':
    main()
    # test()