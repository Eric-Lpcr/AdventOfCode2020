from itertools import count
from operator import mul


class Deck(list):
    def __init__(self, *args, **kwargs):
        super(Deck, self).__init__(*args, **kwargs)
        self.history = []

    def draw(self):
        return self.pop(0)

    def win(self, *cards):
        self += cards

    def __repr__(self):
        return ', '.join(map(str, self))

    def score(self):
        return sum(map(mul, self, reversed(range(1, len(self) + 1))))

    def historize(self):
        check = self.check_history()
        self.history.append(list(self))
        return check

    def check_history(self):
        return list(self) in self.history


def load_decks(file_name):
    decks = []
    with open(file_name) as f:
        for deck_text in f.read().split('\n\n'):
            cards = [int(line) for line in deck_text.splitlines()[1:]]
            decks.append(Deck(cards))
    return decks


def play_combat(deck1, deck2):
    n_round = 0
    while deck1 and deck2:
        n_round += 1
        debug_print(f'\n-- Round {n_round} --')
        debug_print(f"Player 1's deck: {deck1}")
        debug_print(f"Player 2's deck: {deck2}")

        card1, card2 = deck1.draw(), deck2.draw()
        debug_print(f"Player 1's plays: {card1}")
        debug_print(f"Player 2's plays: {card2}")

        if card1 > card2:
            debug_print("Player 1 wins the round!")
            deck1.win(card1, card2)
        else:
            debug_print("Player 2 wins the round!")
            deck2.win(card2, card1)

    print('== Post - game results ==')
    print(f"Player 1's deck: {deck1}")
    print(f"Player 2's deck: {deck2}")
    print()

    winner, winner_deck = (1, deck1) if deck1 else (2, deck2)
    return winner, winner_deck


game_number = count(1)


def play_recursive_combat(deck1, deck2):
    n_game = next(game_number)
    debug_print(f'\n=== Game {n_game} ===')

    n_round = 0
    while deck1 and deck2:
        n_round += 1
        debug_print(f'\n-- Round {n_round} (Game {n_game}) --')
        if deck1.historize() and deck2.historize():
            debug_print(f'Repeated decks, the winner of game {n_game} is player 1!')
            return 1, deck1

        debug_print(f"Player 1's deck: {deck1}")
        debug_print(f"Player 2's deck: {deck2}")
        card1, card2 = deck1.draw(), deck2.draw()
        debug_print(f"Player 1's plays: {card1}")
        debug_print(f"Player 2's plays: {card2}")
        if len(deck1) >= card1 and len(deck2) >= card2:
            debug_print(f'Playing a sub-game to determine the winner...')
            round_winner, _ = play_recursive_combat(Deck(list(deck1[:card1])), Deck(list(deck2[:card2])))
            debug_print(f'...anyway, back to game {n_game}.')
        else:
            round_winner = 1 if card1 > card2 else 2

        debug_print(f"Player {round_winner} wins round {n_round} of game {n_game}!")
        if round_winner == 1:
            deck1.win(card1, card2)
        else:
            deck2.win(card2, card1)

    winner, winner_deck = (1, deck1) if deck1 else (2, deck2)
    debug_print(f'The winner of game {n_game} is player {winner}!' '\n')

    if n_game == 1:
        print('== Post - game results ==')
        print(f"Player 1's deck: {deck1}")
        print(f"Player 2's deck: {deck2}")
        print()

    return winner, winner_deck


DEBUG = False


def debug_print(string=None, debug=DEBUG):
    if string is not None and debug:
        print(string)


def main():
    print("PART 1")
    deck1, deck2 = load_decks('input.txt')
    winner, winner_deck = play_combat(deck1, deck2)
    print(f"Part1 - Combat game, player {winner} won with score: {winner_deck.score()}")
    print()

    print("PART 2")
    deck1, deck2 = load_decks('input.txt')
    winner, winner_deck = play_recursive_combat(deck1, deck2)
    print(f"Part2 - Recursive combat game, , player {winner} won with score: {winner_deck.score()}")


if __name__ == '__main__':
    main()
