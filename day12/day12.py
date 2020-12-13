class Position:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def N(self, value):
        self.y += value

    def S(self, value):
        self.y -= value

    def E(self, value):
        self.x += value

    def W(self, value):
        self.x -= value

    def manhattan_distance_of(self, x, y):
        return abs(self.x - x) + abs (self.y - y)

    def __str__(self):
        return f'(x={self.x}, y={self.y})'


class Waypoint(Position):
    def __init__(self, x, y):
        Position.__init__(self, x, y)

    def L(self, rotation):
        times = rotation // 90
        for _ in range(times):
            self.x, self.y = -self.y, self.x

    def R(self, rotation):
        times = rotation // 90
        for _ in range(times):
            self.x, self.y = self.y, -self.x


class Ship:
    def __init__(self, x, y):
        self.position = Position(x, y)

    def execute(self, instructions):
        for instruction in instructions:
            action = instruction[0]
            value = int(instruction[1:])
            self.execute_action(action, value)

    def execute_action(self, action, value):
        pass

    def manhattan_distance_of(self, x, y):
        return self.position.manhattan_distance_of(x, y)


class Ship1(Ship):
    def __init__(self, x, y, route):
        Ship.__init__(self, x, y)
        self.route = route

    def execute_action(self, action, value):
        if action in 'NSEW':
            getattr(self.position, action)(value)
        else:
            getattr(self, action)(value)

    def L(self, value):
        self.route = (self.route - value) % 360

    def R(self, value):
        self.route = (self.route + value) % 360

    def F(self, value):
        direction = 'NESW'[self.route // 90]
        getattr(self.position, direction)(value)


class Ship2(Ship):
    def __init__(self, x, y, waypoint):
        Ship.__init__(self, x, y)
        self.waypoint = waypoint

    def execute_action(self, action, value):
        if action == 'F':
            self.F(value)
        else:
            getattr(self.waypoint, action)(value)

    def F(self, value):
        self.position.x += self.waypoint.x * value
        self.position.y += self.waypoint.y * value


NORTH, EAST, SOUTH, WEST = 0, 90, 180, 270


def main():
    with open('input.txt') as f:
        instructions = f.readlines()
    x0 = y0 = 0
    route = EAST

    ship1 = Ship1(x0, y0, route)
    ship1.execute(instructions)
    print(f'Got ship 1 at ({ship1.position}), '
          f'answer to part 1 is {ship1.manhattan_distance_of(x0, y0)}')

    ship2 = Ship2(x0, y0, Waypoint(10, 1))
    ship2.execute(instructions)
    print(f'Got ship 2 at ({ship2.position}), '
          f'answer to part 2 is {ship2.manhattan_distance_of(x0, y0)}')


if __name__ == '__main__':
    main()
