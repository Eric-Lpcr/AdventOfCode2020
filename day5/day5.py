def main():
    with open('input.txt') as f:
        boarding_passes = f.readlines()

    translation = str.maketrans('FBLR', '0101')
    sids = [int(sid.translate(translation), 2) for sid in boarding_passes]

    sid = max(sids)
    row = sid >> 3
    column = sid & 7
    print(f"Highest seat ID {sid}, row {row} column {column}")

    sids = sorted(sids)
    free_seats = [sids[i]-1 for i in range(1, len(sids)) if sids[i] - sids[i-1] > 1]
    print(f"Last free seat ID is {free_seats.pop()}")


if __name__ == '__main__':
    main()
