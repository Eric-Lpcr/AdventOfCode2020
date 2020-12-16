import re
from itertools import chain
from math import prod
from operator import itemgetter


class InclusiveRangeRule:
    def __init__(self, minimum, maximum):
        self.minimum = minimum
        self.maximum = maximum

    def __contains__(self, item):
        return self.minimum <= item <= self.maximum

    def validates(self, item):
        return item in self

    def __repr__(self):
        return f'{self.minimum}-{self.maximum}'


class RuleSet(list):
    def validates_values(self, values):
        """Returns True if all values in ticket are validated by at least one rule in rule set"""
        return all(self.validates_value(value) for value in values)

    def validates_value(self, value):
        """Returns True if at least one rule in rule set validates the value"""
        return any(rule.validates(value) for rule in self)


def read_data(filename):
    pattern = re.compile(r'([\w\s]+):(.*)')
    field = ''
    rules = dict()

    with open(filename) as f:
        for line in f.readlines():
            if match := pattern.match(line):
                field = match.group(1)
                if ranges := match.group(2):
                    rules[field] = RuleSet()
                    for rule in ranges.split(' or '):
                        m, n = rule.split('-', 1)
                        rules[field].append(InclusiveRangeRule(int(m), int(n)))
                else:
                    rules[field] = []
            elif line[0].isdigit():
                rules[field].append([int(s) for s in line.split(',')])
    my_ticket = rules.pop('your ticket').pop()
    nearby_tickets = rules.pop('nearby tickets')

    return rules, my_ticket, nearby_tickets


def sum_of_invalid_values(rules, tickets):
    """Solves part 1: find invalid values (the ones that no rule validates)"""
    all_rules = RuleSet(chain(*rules.values()))
    all_values = chain(*tickets)
    out_of_range_values = (value for value in all_values if not any(rule.validates(value) for rule in all_rules))
    return sum(out_of_range_values)


def filter_valid_tickets(rules, tickets):
    all_rules = RuleSet(chain(*rules.values()))
    return filter(lambda ticket: all_rules.validates_values(ticket), tickets)


def compute_possible_fields(rules, valid_nearby_tickets):
    """According to rules, find all possible fields for each column
        Returns a column indexed list of sets: possible_fields[column]: set(field)"""
    columns = len(valid_nearby_tickets[0])
    possible_fields = []  # list of fields having a rule which validates all ticket[column] values
    for column in range(columns):
        tickets_column = [ticket[column] for ticket in valid_nearby_tickets]
        possible_fields.append(
            set(field for field, rule_set in rules.items()
                if rule_set.validates_values(tickets_column)))

    return possible_fields


def resolve_possible_fields(possible_fields):
    """Simplifies the list of several possible fields for each column to get a list of column field
        possible_fields[column]: set(field) => possible_fields[column]: field
    """
    single_fields = set()
    changed = True
    while changed:
        changed = False
        for field_set in possible_fields:
            if len(field_set) == 1:  # This one is already solved
                single_fields.update(field_set)
            elif len(field_set) > 1:
                field_set.difference_update(single_fields)  # Remove already used fields from column possible fields
                changed = True
    # Change list of sets of one field to a simpler list of fields
    solved_fields = [next(iter(field_set)) for field_set in possible_fields]
    return solved_fields


def product_of_departure_fields(my_ticket, nearby_tickets, rules):
    """Solves part 2: according to rules, compute fields for each column of nearby_tickets and apply to my_my_ticket"""
    valid_nearby_tickets = list(filter_valid_tickets(rules, nearby_tickets))
    possible_fields = compute_possible_fields(rules, valid_nearby_tickets)
    solved_fields = resolve_possible_fields(possible_fields)

    departure_fields_indices = [i for i, field in enumerate(solved_fields) if field.startswith('departure')]
    departure_values = itemgetter(*departure_fields_indices)(my_ticket)

    return prod(departure_values)


def main():
    rules, my_ticket, nearby_tickets = read_data('input.txt')
    print(f'Part 1 : sum of out of range values is {sum_of_invalid_values(rules, nearby_tickets)}')
    print(f'Part 2 : product of departure values is {product_of_departure_fields(my_ticket, nearby_tickets, rules)}')


if __name__ == '__main__':
    main()
