"""
A module used to store the deck class

Classes
-------
Deck
    The representation of a deck
"""

from random import shuffle

from src.card import CARDS


class Deck:
    """
    A class used to represent a deck

    Attributes
    ----------
    cards : list(Card)
        The list of cards in the deck

    Methods
    -------
    draw()
        Takes a card from the top of the deck
    flip()
        Reveals the bottom card of the deck
    is_empty()
        Returns whether deck is empty
    shuffle_deck()
        Randomizes the order of the deck


    """

    def __init__(self):
        """
        """
        self.cards = CARDS.copy()

    def __len__(self):
        """
        Implements len function for Deck

        Returns
        -------
        int
            The amount of cards
        """
        return len(self.cards)

    def __str__(self):
        """
        Implements str function for Deck

        Returns
        -------
        str
            The deck as a string
        """
        return str([str(x) for x in self.cards])

    def draw(self):
        """
        Takes a card from the top of the deck

        Returns
        -------
        Card
            The top card or None if there is not a card in the deck
        """
        if not self.is_empty():
            return self.cards.pop()  # takes the -1th card by default
        return None

    def flip(self):
        """
        Reveals the bottom card of the deck

        Returns
        -------
        Card
            The bottom card in the deck or None if the deck is empty
        """
        if not self.is_empty():
            return self.cards[0]
        return None

    def is_empty(self):
        """
        Returns whether deck is empty

        Returns
        -------
        bool
            True if the deck is empty, False otherwise
        """
        return len(self.cards) == 0

    def shuffle_deck(self):
        """
        Randomizes the order of the deck
        """
        shuffle(self.cards)