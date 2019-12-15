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
<<<<<<< HEAD
ranks = ['A', 'K', 'Q', 'J', '10', '9', '8', '7', '6']
rankNum = {rank: index for index, rank in enumerate(reversed(ranks))}
suits = ['Diamonds', 'Spades', 'Clubs', 'Hearts']
cards = list(itertools.product(ranks, suits))

""" returns a comparator for a given suit """
def createComparator(dank):
    def compare(x, y):
        if x.suit == dank and y.suit == dank:  # Both dank -> check rank
            if rankNum[x.rank] > rankNum[y.rank]:
                return 1
            elif rankNum[x.rank] < rankNum[y.rank]:
                return -1
            else:
                return 0

        elif x.suit != dank and y.suit != dank:  # both nondank -> check rank
            if rankNum[x.rank] > rankNum[y.rank]:
                return 1
            elif rankNum[x.rank] < rankNum[y.rank]:
                return -1
            else:
                return 0

        else:  # one must be dank and one must not
            return 1 if x.suit == dank else -1
    return compare


def minCard(cards, suit):
    minimum = 9
    lowestCard = None
    for card in cards:
        if card.suit == suit and rankNum[card.rank] < minimum:
            lowestCard = card
            minimum = rankNum[lowestCard.rank]
    return lowestCard
=======

RANKS = ['A', 'K', 'Q', 'J', '10', '9', '8', '7', '6']
SUITS = ['Diamonds', 'Spades', 'Clubs', 'Hearts']
CARDS = itertools.product(RANKS, SUITS)
>>>>>>> 56666cef58f394cb26187e1104c76f624ff2b38f


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
<<<<<<< HEAD
        self.cards = [Card(rank, suit) for rank, suit in cards]
        print(self.cards)
=======
        """
        """
        self.cards = [Card(rank, suit) for rank, suit in CARDS]
>>>>>>> 56666cef58f394cb26187e1104c76f624ff2b38f

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
