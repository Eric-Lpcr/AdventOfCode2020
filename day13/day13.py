from itertools import count
from math import prod, gcd


def main():
    with open('input.txt') as f:
        from_time = int(f.readline())
        bus_table = f.readline().split(',')

    # from_time = 939
    # x = 'x'
    # bus_table = [7, 13, x, x, 59, x, 31, 19]

    # Part 1
    busses = [int(bus) for bus in bus_table if bus != 'x']
    departures = [(bus, (from_time // bus + 1) * bus) for bus in busses]
    next_bus, next_departure = min(departures, key=lambda d: d[1])

    print(f'Next bus departure is bus {next_bus} at {next_departure}, '
          f'answer is {next_bus * (next_departure - from_time)}')

    # Part 2
    busses = [(int(bus), offset) for offset, bus in enumerate(bus_table) if bus != 'x']

    """
    for each bus:
    (time + offset[i]) % bus[i] = 0
    <=> time % bus[i] = -offset[i] % bus[i]
    <=> time === -offset[i] % bus[i] [mod bus[i]] # === means is congruent to
    
    https://fr.wikipedia.org/wiki/Congruence_lin%C3%A9aire#M%C3%A9thode_des_substitutions_successives
    https://fracademic.com/dic.nsf/frwiki/1626206#Syst.C3.A8me_de_congruences_d.27entiers
    
    This method works because bus numbers (mods) are prime numbers ...
    For each i, x === ri mod mi
    p = m1 * m2 * m3 ...
    ni = p / mi
    ki such as ei = ki * ni === 1 [mod ni] 
    
    x = sum (ri * ei) mod p
    
    r is offset, m is bus
    """

    m = [bus for bus, offset in busses]
    r = [-offset % bus for bus, offset in busses]

    # # example from algorithm links
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

    time_of_first_bus = x

    # # This was a brute force algorithm...which doesn't work on the problem input
    # max_bus, max_bus_offset = max(busses, key=lambda e: e[0])
    # for multiplier in count(1):
    #     if multiplier % 100000 == 0: print(multiplier)
    #     time_of_first_bus = max_bus * multiplier - max_bus_offset
    #     if all((time_of_first_bus + offset) % bus == 0 for bus, offset in busses):
    #         break

    print(f'Earliest timestamp for all busses one minute offset departure is {time_of_first_bus}')


if __name__ == '__main__':
    main()
