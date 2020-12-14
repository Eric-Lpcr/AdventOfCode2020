from itertools import count
from math import prod, gcd


def find_next_bus(busses, from_time):
    departures = [(bus, (from_time // bus + 1) * bus) for bus in busses]
    next_bus, next_departure = min(departures, key=lambda d: d[1])
    return next_bus, next_departure


def solve_congruence_equations(r, m):
    """Returns p, x where x is congruent to 0 modulo p
    and x is congruent to r[i] modulo m[i] for each (m[i], r[i]) in parameters m, r
    m numbers shall be prime"""

    # https://fr.wikipedia.org/wiki/Congruence_lin%C3%A9aire#M%C3%A9thode_des_substitutions_successives
    # https://fracademic.com/dic.nsf/frwiki/1626206#Syst.C3.A8me_de_congruences_d.27entiers
    #
    # For each i, x === ri mod mi
    # p = m1 * m2 * m3 ...
    # ni = p / mi
    # ki such as ei = ki * ni === 1 [mod ni]
    # x = sum (ri * ei) mod p
    #
    # example from algorithm links, gives 23 [mod 105]
    # m = [3, 5, 7]
    # r = [2, 3, 2]

    p = prod(m)
    n = [p // mi for mi in m]
    k = [1] * len(n)
    for i in range(len(k)):
        while k[i] * n[i] % m[i] != 1:
            k[i] += 1
    e = [ki * ni for ki, ni in zip(k, n)]
    x = sum(ri * ei for ri, ei in zip(r, e)) % p
    return x, p


def brute_solve(busses):
    # This was a brute force algorithm...which doesn't work on the problem input
    # Although it's a bit optimized to iterate with the less frequent bus
    max_bus, max_bus_offset = max(busses, key=lambda e: e[0])
    time_of_first_bus = 0
    for multiplier in count(1):
        if multiplier % 100000 == 0: print(multiplier)
        time_of_first_bus = max_bus * multiplier - max_bus_offset
        if all((time_of_first_bus + offset) % bus == 0 for bus, offset in busses):
            break
    return time_of_first_bus


def main():
    with open('input.txt') as f:
        from_time = int(f.readline())
        bus_table = f.readline().split(',')

    # from_time = 939
    # x = 'x'
    # bus_table = [7, 13, x, x, 59, x, 31, 19]

    # Part 1
    busses = [int(bus) for bus in bus_table if bus != 'x']
    next_bus, next_departure = find_next_bus(busses, from_time)

    print(f'Next bus departure is bus {next_bus} at {next_departure}, '
          f'answer is {next_bus * (next_departure - from_time)}')

    # Part 2
    busses = [(int(bus), offset) for offset, bus in enumerate(bus_table) if bus != 'x']
    # time_of_first_bus = brute_solve(busses, time_of_first_bus)

    # Congruence equations
    # for each bus:
    # (time + offset[i]) % bus[i] = 0
    # <=> time % bus[i] = -offset[i] % bus[i]
    # <=> time === -offset[i] % bus[i] [mod bus[i]] # === means is congruent to
    # r is -offset [mod bus], m is bus id
    m = [bus for bus, offset in busses]
    r = [-offset % bus for bus, offset in busses]
    # This method works because bus numbers (mods) are prime numbers ...
    time_of_first_bus, _ = solve_congruence_equations(r, m)

    print(f'Earliest timestamp for all busses one minute offset departure is {time_of_first_bus}')


if __name__ == '__main__':
    main()
