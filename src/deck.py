"""A module used to store the Deck class.

Represents a deck of cards for a game of Durak.
"""

from random import shuffle

from card import CARDS


class Deck:
    """A class used to represent a deck of cards.

    Attributes:
        cards: The list of cards in the deck
    """

    def __init__(self):
        """Inits Deck.
        """

        self.cards = CARDS.copy()

    def __len__(self):
        return len(self.cards)

    def __str__(self):
        return str([str(x) for x in self.cards])

    def draw(self):
        """Takes a card from the top of the deck.

        Returns:
            The top card or None if there is not a card in the deck
        """

        if not self.is_empty():
            return self.cards.pop()  # takes the -1th card by default
        return None

    def flip(self):
        """Reveals the bottom card of the deck.

        Returns:
            The bottom card in the deck or None if the deck is empty
        """

        if not self.is_empty():
            return self.cards[0]
        return None

    def is_empty(self):
        """Returns whether the deck is empty.

        Returns:
            True if the deck is empty, False otherwise
        """
        return len(self.cards) == 0

    def shuffle_deck(self):
        """ Randomizes the order of the deck
        """
        shuffle(self.cards)
