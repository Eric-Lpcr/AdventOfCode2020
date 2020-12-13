class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

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


class ShipPosition(Position):
    def __init__(self, x, y, route):
        Position.__init__(self, x, y)
        self.route = route

    def execute(self, instructions):
        for instruction in instructions:
            action = instruction[0]
            value = int(instruction[1:])
            getattr(self, action)(value)

    def L(self, value):
        self.route = (self.route - value) % 360

    def R(self, value):
        self.route = (self.route + value) % 360

    def F(self, value):
        direction = "NESW"[self.route // 90]
        getattr(self, direction)(value)


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

    def execute(self, instructions):
        for instruction in instructions:
            action = instruction[0]
            value = int(instruction[1:])
            getattr(self, action)(value)


class ShipPosition2(Position):
    def __init__(self, x, y, waypoint):
        Position.__init__(self, x, y)
        self.waypoint = waypoint

    def execute(self, instructions):
        for instruction in instructions:
            action = instruction[0]
            value = int(instruction[1:])
            if action == "F":
                self.F(value)
            else:
                getattr(self.waypoint, action)(value)

    def F(self, value):
        self.x += self.waypoint.x * value
        self.y += self.waypoint.y * value


NORTH, EAST, SOUTH, WEST = 0, 90, 180, 270


def main():
    with open('input.txt') as f:
        instructions = f.readlines()
    x0 = y0 = 0
    route = EAST

    ship = ShipPosition(x0, y0, route)
    ship.execute(instructions)
    print(f"Got ship 1 at ({ship.x}, {ship.y}), "
          f"answer to part 1 is {ship.manhattan_distance_of(x0, y0)} ")

    ship2 = ShipPosition2(x0, y0, Waypoint(10, 1))
    ship2.execute(instructions)
    print(f"Got ship 2 at ({ship2.x}, {ship2.y}), "
          f"answer to part 2 is {ship2.manhattan_distance_of(x0, y0)} ")


if __name__ == '__main__':
    main()
