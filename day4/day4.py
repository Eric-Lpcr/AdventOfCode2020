import re
from collections import namedtuple

hcl_pattern = re.compile('#[0-9a-z]{6}')
ecl_pattern = re.compile('amb|blu|brn|gry|grn|hzl|oth')
pid_pattern = re.compile('[0-9]{9}')
hgt_pattern = re.compile(r'(\d+)(cm|in)')


def check_height(hgt):
    match = hgt_pattern.fullmatch(hgt)
    if match:
        height = int(match.group(1))
        if match.group(2) == 'cm':
            return 150 <= height <= 193
        else:  # 'in'
            return 59 <= height <= 76
    return False


PassportRule = namedtuple("PassportRule", ['description', 'mandatory', 'check'])
passport_rules = {
    'byr': PassportRule("Birth Year", True, lambda byr: 1920 <= int(byr) <= 2002),
    'iyr': PassportRule("Issue Year", True, lambda iyr: 2010 <= int(iyr) <= 2020),
    'eyr': PassportRule("Expiration Year", True, lambda eyr: 2020 <= int(eyr) <= 2030),
    'hgt': PassportRule("Height", True, check_height),
    'hcl': PassportRule("Hair Color", True, lambda hcl: hcl_pattern.fullmatch(hcl)),
    'ecl': PassportRule("Eye Color", True, lambda ecl: ecl_pattern.fullmatch(ecl)),
    'pid': PassportRule("Passport ID", True, lambda pid: pid_pattern.fullmatch(pid)),
}


def main():
    with open('input.txt') as f:
        text = f.read()

    valid_passports1 = valid_passports2 = 0
    passports = text.split("\n" * 2)
    for passport in passports:
        fields = passport.split()
        if len(fields) >= 7:
            passport_data = dict()
            for field in fields:
                key, value = field.split(':')
                passport_data[key] = value

            if all([key in passport_data for key in passport_rules]):
                valid_passports1 += 1
                if all([rule.check(passport_data[key]) for key, rule in passport_rules.items()]):
                    valid_passports2 += 1

    print(f"Ignoring rules, found {valid_passports1} valid passports")
    print(f"Checking rules, found {valid_passports2} valid passports")


if __name__ == '__main__':
    main()
