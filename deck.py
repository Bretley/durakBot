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

from card import *



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
        self.cards = [card for card in CARDS]

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
            return self.cards.pop()  # takes the -1th card by default
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

    def isEmpty(self):
        """
        Returns whether deck is empty
        """
        return len(self.cards) > 0



# for i in range(1, pow(10,7)):
#     d = Deck()
# runs in ~4.6s
