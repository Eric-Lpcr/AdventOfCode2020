from collections import Counter
from itertools import chain

NORTH = -1, 0
NORTHEAST = -1, 1
EAST = 0, 1
SOUTHEAST = 1, 1
SOUTH = 1, 0
SOUTHWEST = 1, -1
WEST = 0, -1
NORTHWEST = -1, -1

DIRECTIONS = [NORTH, NORTHEAST, EAST, SOUTHEAST, SOUTH, SOUTHWEST, WEST, NORTHWEST]


class Matrix:
    def __init__(self, data=None):
        if data is None:
            data = []
        self.data = data

    def rows(self):
        return len(self.data)

    def columns(self):
        if self.rows() > 0:
            return len(self.data[0])
        return 0

    def row(self, index):
        if 0 <= index < self.rows():
            return self.data[index]
        else:
            return self.__missing_row__(index)

    def column(self, index):
        if 0 <= index < self.columns():
            return [self[r, index] for r in range(self.rows())]
        else:
            return self.__missing_column__(index)

    def __getitem__(self, item):
        (r, c) = item
        if 0 <= r < self.rows() and 0 <= c < self.columns():
            return self.data[r][c]
        else:
            return self.__missing_value__(r, c)

    def get(self, r, c, default=None):
        try:
            return self[r, c]
        except IndexError:
            return default

    def get_diagonal(self, r, c):
        """Returns the diagonal (increasing rows and columns) containing value at (r,c)
         and the index of this value in the diagonal"""
        d1 = min(r, c)
        r1, c1 = r - d1, c - d1
        length = min(self.rows() - r1, self.columns() - c1)
        return [self[r1 + i, c1 + i] for i in range(length)], c - c1

    def get_cross_diagonal(self, r, c):
        """Returns the diagonal (decreasing rows and increasing columns) containing value at (r,c)
         and the index of this value in the diagonal"""
        d1 = min(self.rows() - 1 - r, c)
        r1, c1 = r + d1, c - d1
        length = min(r1 + 1, self.columns() - c1)
        return [self[r1 - i, c1 + i] for i in range(length)], c - c1

    def get_at(self, r, c, hops, direction, default=None):
        dr, dc = direction
        return self.get(r + dr * hops, c + dc * hops, default)

    def get_neighbours(self, r, c):
        """Returns the 8 neighbours of value at (r,c), clockwise from 12:00"""
        return [self.get(r + dr, c + dc, None) for dr, dc in DIRECTIONS]

    def append_row(self, row):
        if len(row) != self.rows() and self.rows() != 0:
            raise ValueError(f'row should be {self.rows()} long')
        self.data.append(row)

    def append_column(self, column):
        for index, val in enumerate(column):
            self.row(index).append(val)

    def __setitem__(self, item, value):
        (r, c) = item
        if 0 <= r < self.rows() and 0 <= c < self.columns():
            self.data[r][c] = value
        else:
            raise IndexError

    def __missing_row__(self, index):
        return [self.__missing_value__(index, c) for c in range(self.columns())]

    def __missing_column__(self, index):
        return [self.__missing_value__(r, index) for r in range(self.rows())]

    def __missing_value__(self, r, c):
        raise IndexError()

    def __str__(self):
        return "[" + "\n ".join(str(row) for row in self.data) + "]"

    def __copy__(self):
        return Matrix(self.data.copy())


if __name__ == '__main__':
    m = Matrix([[1, 2, 3],
                [4, 5, 6],
                [7, 8, 9]])
    print(m)

    print(m.rows(), m.columns())
    print(m.row(1))
    print(m.column(1))
    print(m[1, 1])

    print(m.get_neighbours(0, 0))
    print(m.get_cross_diagonal(2, 1))

    print(m.get_at(2, 0, 2, NORTHEAST))

    m[1, 1] = 0
    print(m)

    print(m.copy())
