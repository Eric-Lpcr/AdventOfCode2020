from functools import lru_cache
from itertools import count


@lru_cache
def compute_key_recurse(subject_number, loop_size):
    if loop_size == 0:
        return 1
    else:
        return compute_key_recurse(subject_number, loop_size - 1) * subject_number % 20201227


def reverse_engineer(key, subject_number=7):
    c = count(1)
    while loop_size := next(c):
        if compute_key_recurse(subject_number, loop_size) == key:
            break
    return loop_size


def compute_key(subject_number, loop_size):
    key = 1
    for _ in range(loop_size):
        key = key * subject_number % 20201227
    return key


def main():
    subject_number = 7

    card_public_key = 17115212
    door_public_key = 3667832

    # example
    # card_public_key = 5764801
    # door_public_key = 17807724

    card_loop_size = reverse_engineer(card_public_key, subject_number)
    print(f'Card secret loop size is {card_loop_size}')

    door_loop_size = reverse_engineer(door_public_key, subject_number)
    print(f'Door secret loop size is {door_loop_size}')

    card_encryption_key = compute_key(door_public_key, card_loop_size)
    print(f'Card encryption key is {card_encryption_key}')

    door_encryption_key = compute_key(card_public_key, door_loop_size)
    print(f'Door encryption key is {door_encryption_key}')


if __name__ == '__main__':
    main()

