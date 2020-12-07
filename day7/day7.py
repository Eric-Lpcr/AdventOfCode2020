from collections import namedtuple


class BagRules(dict):
    def __getitem__(self, bag_description):
        if bag_description in self:
            return dict.__getitem__(self, bag_description)
        else:
            o = BagRule(bag_description)
            self[bag_description] = o
            return o


class BagRule:
    def __init__(self, bag_description):
        self.bag_description = bag_description
        self.contents = []
        self.containers = []

    def __str__(self):
        return self.bag_description

    def get_all_containers(self):
        containers = set(self.containers)
        for container in self.containers:
            containers |= container.get_all_containers()
        return containers

    def get_nb_contents(self):
        nb_contents = 0
        for content in self.contents:
            nb_contents += content.number + content.number * content.bag_rule.get_nb_contents()
        return nb_contents


BagContent = namedtuple('BagContent', ['number', 'bag_rule'])


def main():
    with open('input.txt') as f:
        bag_rules_text = f.readlines()

#     bag_rules_text = """light red bags contain 1 bright white bag, 2 muted yellow bags.
# dark orange bags contain 3 bright white bags, 4 muted yellow bags.
# bright white bags contain 1 shiny gold bag.
# muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
# shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
# dark olive bags contain 3 faded blue bags, 4 dotted black bags.
# vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
# faded blue bags contain no other bags.
# dotted black bags contain no other bags.""".splitlines()

    bag_rules = BagRules()

    for bag_rule_text in bag_rules_text:
        bag_description, bag_contents_text = bag_rule_text.strip('.\n').split(' bags contain ')
        if bag_contents_text != 'no other bags':
            for bag_content_text in bag_contents_text.split(', '):
                bag_content = bag_content_text.split()
                bag_content_nb = int(bag_content[0])
                bag_content_description = ' '.join(bag_content[1:-1])
                bag_rules[bag_description].contents\
                    .append(BagContent(bag_content_nb, bag_rules[bag_content_description]))
                bag_rules[bag_content_description].containers.append(bag_rules[bag_description])

    containers = bag_rules['shiny gold'].get_all_containers()
    print(f"Got {len(containers)} possible containers for shiny gold bag")

    nb_of_bags = bag_rules['shiny gold'].get_nb_contents()
    print(f"Shiny gold bag contains {nb_of_bags} other bags")


if __name__ == '__main__':
    main()
