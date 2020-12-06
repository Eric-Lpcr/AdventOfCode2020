from collections import Counter


def main():
    with open('input.txt') as f:
        text = f.read()

    positive_answers = 0
    groups = text.split("\n" * 2)
    for group in groups:
        positive_answers += len(set(group.replace("\n", "")))

    print(f"Total number of positive answers: {positive_answers}")

    shared_positive_answers = 0
    for group in groups:
        counts = Counter(group)
        nb_of_forms = counts["\n"] + 1
        del counts["\n"]
        shared_positive_answers += len([count for answer, count in counts.items() if count == nb_of_forms])

    print(f"Total number of shared positive answers: {shared_positive_answers}")


if __name__ == '__main__':
    main()
