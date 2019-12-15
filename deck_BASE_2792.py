import itertools
from random import shuffle
ranks = ['A', 'K', 'Q', 'J', '10', '9', '8', '7', '6']
suits = ['Diamonds', 'Spades', 'Clubs', 'Hearts']
cards = itertools.product(ranks, suits)


class Deck:
    def __init__(self):
        self.cards = [Card(rank, suit) for rank, suit in cards]

    def shuffle(self):
        shuffle(self.cards)

    def draw(self):
        if len(self.cards) > 0:
            return [self.cards.pop()]  # takes the -1th card by default
        else:
            return None

    def __str__(self):
        return str([str(x) for x in self.cards])

    def __len__(self):
        return len(self.deck)

    def flip(self):
        return self.cards[0]


class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        return self.rank + ' of ' + self.suit


"""
for i in range(1, pow(10,7)):
    d = Deck()
runs in ~4.6s
"""
