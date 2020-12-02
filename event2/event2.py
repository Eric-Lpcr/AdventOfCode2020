def password_is_valid_rule1(line):
    minimum, maximum, letter, password = line.replace('-', ' ').replace(':', ' ').split()
    return int(minimum) <= password.count(letter) <= int(maximum)


def password_is_valid_rule2(line):
    pos1, pos2, letter, password = line.replace('-', ' ').replace(':', ' ').split()
    return (password[int(pos1)-1] == letter) != (password[int(pos2)-1] == letter)  # != for bool is an xor


def main():
    res_rule1 = res_rule2 = 0
    with open('input.txt') as f:
        for line in f.readlines():
            if password_is_valid_rule1(line):
                res_rule1 += 1
            if password_is_valid_rule2(line):
                res_rule2 += 1

    print("Got", res_rule1, "valid passwords according to rule 1")
    print("Got", res_rule2, "valid passwords according to rule 2")


if __name__ == '__main__':
    main()
