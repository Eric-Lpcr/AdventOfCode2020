from collections import namedtuple, Counter
from functools import reduce
from operator import itemgetter, add

Food = namedtuple('Food', 'ingredients allergens')


def resolve_possible_ingredients(allergenic):
    """Simplifies the list of several possible ingredients for each allergen to get a list of allergen ingredient
        allergenic[allergen]: set(ingredients) => allergenic[allergen]: ingredient
    """
    single_ingredients = set()
    changed = True
    while changed:
        changed = False
        for ingredients in allergenic.values():
            if len(ingredients) == 1:  # This one is already solved
                single_ingredients.update(ingredients)
            elif len(ingredients) > 1:
                ingredients.difference_update(single_ingredients)  # Remove already solved ingredients
                changed = True
    # Change dict of sets of one ingredient to a simpler dict allergen: ingredient
    solved_allergenic = {allergen: next(iter(ingredients)) for allergen, ingredients in allergenic.items()}
    return solved_allergenic


def find_allergenic_ingredients(foods):
    allergenic = dict()  # allergen: possible ingredient
    for food in foods:
        for allergen in food.allergens:
            if allergen not in allergenic:
                allergenic[allergen] = set(food.ingredients)
            else:
                allergenic[allergen] &= set(food.ingredients)

    allergenic = resolve_possible_ingredients(allergenic)
    return allergenic


def load_food_description(file_name):
    foods = []
    with open(file_name) as f:
        for line in f.readlines():
            ingredients, allergens = line.strip(')\n').split(' (contains ')
            foods.append(Food(ingredients.split(), allergens.split(', ')))
    return foods


def main():
    foods = load_food_description('input.txt')
    allergenic = find_allergenic_ingredients(foods)

    all_ingredients = Counter(reduce(add, map(itemgetter(0), foods)))
    n_times = sum(n for ingredient, n in all_ingredients.items() if ingredient not in allergenic.values())
    print(f"Part 1 - Non allergenic ingredients appear {n_times} times")

    dangerous_list = ','.join(dict(sorted(allergenic.items())).values())
    print(f'Part 2 - Canonical dangerous ingredient list is: {dangerous_list}')


if __name__ == '__main__':
    main()
