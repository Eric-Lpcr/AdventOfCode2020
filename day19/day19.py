def match_rule(message, rules, rule_index):
    current_rule = rules[rule_index]
    if isinstance(current_rule, str):
        return message.startswith(current_rule), len(current_rule)
    else:
        rule_match = False
        pos = 0
        for alt_group in current_rule:
            group_match = True
            pos = 0
            for alt_rule in alt_group:
                match, consumed = match_rule(message[pos:], rules, alt_rule)
                if not match:
                    group_match = False
                    break
                pos += consumed
            if group_match:
                rule_match = True
                break
        return rule_match, pos


def full_match_rule(message, rules):
    match, consumed = match_rule(message, rules, rule_index=0)
    return match and consumed == len(message)


def match_part2(message, rules):
    """For part 2,
    rule 0 : 8 11
    <=>  0: (42 | 42 8) (42 31 | 42 11 31)
    <=>  0: 42+ 42{n} 31{n}
    <=> 0: 42{m} 31{n} with m>n>=1 (at least 42 42 31, m=2 and n=1)
    """
    match42, consumed = match_rule(message, rules, 42)
    pos = 0
    m = 0
    while match42:
        m += 1
        pos += consumed

        # try to end with rule 31
        pos31 = pos
        n = 0
        match31, consumed = match_rule(message[pos31:], rules, 31)
        while match31:
            n += 1
            pos31 += consumed
            if m > n >= 1 and pos31 == len(message):
                return True
            else:
                match31, consumed = match_rule(message[pos31:], rules, 31)

        match42, consumed = match_rule(message[pos:], rules, 42)
    return False


def decode_rule(rule_line, rules):
    index, rule_def = rule_line.split(': ')
    if rule_def.startswith('"'):
        rules[int(index)] = rule_def[1]
    else:
        alts = rule_def.split(' | ')
        rules[int(index)] = [list(map(int, alt.split())) for alt in alts]


def load_rules(rule_lines):
    rules = {}
    for rule_line in rule_lines:
        decode_rule(rule_line, rules)
    return rules


def main():
    with open('input.txt') as f:
        rule_lines, messages = tuple(part.splitlines() for part in f.read().split('\n\n'))
    rules = load_rules(rule_lines)

    res = sum(full_match_rule(message, rules) for message in messages)
    print(f"Part 1: got {res} valid messages")

    decode_rule('8: 42 | 42 8', rules)
    decode_rule('11: 42 31 | 42 11 31', rules)
    res = sum(match_part2(message, rules) for message in messages)
    print(f"Part 2: got {res} valid messages")


def test1():
    rule_lines = '''0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"'''.splitlines()

    rules = load_rules(rule_lines)

    messages = '''ababbb
bababa
abbbab
aaabbb
aaaabbb'''.splitlines()

    matching_messages = list(message for message in messages if full_match_rule(message, rules))
    print(matching_messages)
    print(len(matching_messages))


def test2():
    rule_lines = '''42: 9 14 | 10 1
9: 14 27 | 1 26
10: 23 14 | 28 1
1: "a"
11: 42 31
5: 1 14 | 15 1
19: 14 1 | 14 14
12: 24 14 | 19 1
16: 15 1 | 14 14
31: 14 17 | 1 13
6: 14 14 | 1 14
2: 1 24 | 14 4
0: 8 11
13: 14 3 | 1 12
15: 1 | 14
17: 14 2 | 1 7
23: 25 1 | 22 14
28: 16 1
4: 1 1
20: 14 14 | 1 15
3: 5 14 | 16 1
27: 1 6 | 14 18
14: "b"
21: 14 1 | 1 14
25: 1 1 | 1 14
22: 14 14
8: 42
26: 14 22 | 1 20
18: 15 15
7: 14 5 | 1 21
24: 14 1'''.splitlines()

    rules = load_rules(rule_lines)
    decode_rule('8: 42 | 42 8', rules)
    decode_rule('11: 42 31 | 42 11 31', rules)

    messages = '''abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa
bbabbbbaabaabba
babbbbaabbbbbabbbbbbaabaaabaaa
aaabbbbbbaaaabaababaabababbabaaabbababababaaa
bbbbbbbaaaabbbbaaabbabaaa
bbbababbbbaaaaaaaabbababaaababaabab
ababaaaaaabaaab
ababaaaaabbbaba
baabbaaaabbaaaababbaababb
abbbbabbbbaaaababbbbbbaaaababb
aaaaabbaabaaaaababaa
aaaabbaaaabbaaa
aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
babaaabbbaaabaababbaabababaaab
aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba'''.splitlines()

    matching_messages = list(message for message in messages if match_part2(message, rules))
    print(matching_messages)
    print(len(matching_messages))


def test3():
    rule_lines = '''0: 2
2: 3 | 2 3
3: "a"'''.splitlines()

    rules = load_rules(rule_lines)

    messages = '''a
aa
aaa
aaaa
aaaaa'''.splitlines()

    matching_messages = list(message for message in messages if full_match_rule(message, rules))
    print(matching_messages)
    print(len(matching_messages))


if __name__ == '__main__':
    main()
    # test1()
    # test2()
    # test3()
