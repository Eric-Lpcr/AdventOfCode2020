class Position:
    def __init__(self, x=0, y=0):
        if isinstance(x, Position):
            self.x, self.y = x.x, x.y
        else:
            self.x, self.y = x, y

    def N(self, value):
        self.y += value

    def S(self, value):
        self.y -= value

    def E(self, value):
        self.x += value

    def W(self, value):
        self.x -= value

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def manhattan_distance_of(self, position):
        return abs(self.x - position.x) + abs(self.y - position.y)

    def __str__(self):
        return f'(x={self.x}, y={self.y})'


class Waypoint(Position):
    def __init__(self, x=0, y=0):
        Position.__init__(self, x, y)

    def L(self, rotation):
        if rotation == 90:
            self.x, self.y = -self.y, self.x
        elif rotation == 180:
            self.x, self.y = -self.x, -self.y
        else:
            self.R(90)

    def R(self, rotation):
        if rotation == 90:
            self.x, self.y = self.y, -self.x
        elif rotation == 180:
            self.x, self.y = -self.x, -self.y
        else:
            self.L(90)


class Ship:
    def __init__(self, position):
        self.position = Position(position)

    def execute(self, instructions):
        for instruction in instructions:
            action = instruction[0]
            value = int(instruction[1:])
            self.execute_action(action, value)

    def execute_action(self, action, value):
        pass

    def manhattan_distance_of(self, position):
        return self.position.manhattan_distance_of(position)


class Ship1(Ship):
    def __init__(self, position, route):
        Ship.__init__(self, position)
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
    def __init__(self, position, waypoint):
        Ship.__init__(self, position)
        self.waypoint = waypoint

    def execute_action(self, action, value):
        if action == 'F':
            self.F(value)
        else:
            getattr(self.waypoint, action)(value)

    def F(self, value):
        self.position.move(self.waypoint.x * value, self.waypoint.y * value)


NORTH, EAST, SOUTH, WEST = 0, 90, 180, 270


def main():
    with open('input.txt') as f:
        instructions = f.readlines()
    initial_position = Position(0, 0)
    route = EAST

    ship1 = Ship1(initial_position, route)
    ship1.execute(instructions)
    print(f'Got ship 1 at ({ship1.position}), '
          f'answer to part 1 is {ship1.manhattan_distance_of(initial_position)}')

    ship2 = Ship2(initial_position, Waypoint(10, 1))
    ship2.execute(instructions)
    print(f'Got ship 2 at ({ship2.position}), '
          f'answer to part 2 is {ship2.manhattan_distance_of(initial_position)}')


if __name__ == '__main__':
    main()
