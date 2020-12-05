def main():
    with open('input.txt') as f:
        boarding_passes = f.readlines()

    # translate to binary number, then to decimal
    translation = str.maketrans('FBLR', '0101')
    sids = [int(sid.translate(translation), 2) for sid in boarding_passes]

    sid = max(sids)
    row = sid >> 3  # remove first three bits XXXXXXX---
    column = sid & 7  # consider only first three bits -------XXX
    print(f"Highest seat ID {sid}, row {row} column {column}")

    sids = sorted(sids)
    # Free seat is where the interval between two occupied seats is more than 1
    free_seats = [sids[i]-1 for i in range(1, len(sids)) if sids[i] - sids[i-1] > 1]
    print(f"Last free seat ID is {free_seats.pop()}")


if __name__ == '__main__':
    main()
