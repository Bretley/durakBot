"""
A module used to store classes related to the functioning of a deck

Classes
-------
Deck
    The representation of a deck
Card
    The representation of a card
"""

import itertools

from random import shuffle

import functools

RANKS = ['A', 'K', 'Q', 'J', '10', '9', '8', '7', '6']
SUITS = ['Diamonds', 'Spades', 'Clubs', 'Hearts']
CARDS = list(itertools.product(RANKS, SUITS))
RANK_NUM = {rank: index for index, rank in enumerate(reversed(RANKS))}


class Deck:
    """
    A class used to represent a deck

    Attributes
    ----------
    cards : list
        The list of cards in the deck

    Methods
    -------
    draw()
        Takes a card from the top of the deck
    flip()
        Reveals the top card of the deck
    shuffle()
        Randomizes the order of the deck


    """

    def __init__(self):
        """
        """
        self.cards = [Card(rank, suit) for rank, suit in CARDS]

    def __len__(self):
        """
        Returns the amount of cards in the deck
        """
        return len(self.cards)

    def __str__(self):
        """
        Returns the deck as a string
        """
        return str([str(x) for x in self.cards])

    def draw(self):
        """
        Takes a card from the top of the deck
        """
        if len(self.cards) > 0:
            return [self.cards.pop()]  # takes the -1th card by default

        return None

    def flip(self):
        """
        Reveals the top card of the deck
        """
        return self.cards[0]

    def shuffle(self):
        """
        Randomizes the order of the deck
        """
        shuffle(self.cards)


def create_card_comparator(dank):
    """
    Returns a comparator that orders cards depending on the dank suit
    comparator will be wrapped as key arg to sorted and list.sort
    """
    def compare(x, y):
        if x.suit == dank and y.suit == dank:
            if RANK_NUM[x.rank] > RANK_NUM[y.rank]:
                return 1
            elif RANK_NUM[x.rank] < RANK_NUM[y.rank]:
                return -1
            else:
                return 0
        elif x.suit != dank and y.suit != dank:
            if RANK_NUM[x.rank] > RANK_NUM[y.rank]:
                return 1
            elif RANK_NUM[x.rank] < RANK_NUM[y.rank]:
                return -1
            else:
                return 0
        else:  # Only one is a dank, if x then x > y else y > x
            return 1 if x.suit == dank else -1
    return functools.cmp_to_key(compare)


class Card:
    """
    A class used to represent a card

    Attributes
    ----------
    rank : str
        The value of a card
    suit : str
        The Suit of the card
    """

    def __init__(self, rank, suit):
        """
        """
        self.rank = rank
        self.suit = suit

    def __str__(self):
        """
        Returns the card as a string
        """
        return self.rank + ' of ' + self.suit

# for i in range(1, pow(10,7)):
#     d = Deck()
# runs in ~4.6s
