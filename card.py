"""
A module used to store the card class

Classes
-------
Card
    The representation of a card
"""

import functools
import itertools


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


RANKS = ['A', 'K', 'Q', 'J', '10', '9', '8', '7', '6']
SUITS = ['Diamonds', 'Spades', 'Clubs', 'Hearts']
CARDS = [Card(rank, suit) for rank, suit in itertools.product(RANKS, SUITS)]
RANK_NUM = {rank: index for index, rank in enumerate(reversed(RANKS))}
CARD_COMPARATORS = {}


def create_comparator(dank_suit):
    """
    Creates a comparator

    Parameters
    ----------
    dank_suit: Card.suit
        The suit of the dank card
    """

    def compare(card1, card2):
        """
        Compares two cards

        Parameters
        ----------
        card1: Card
            The first card to compare
        card2: Card
            The second card to compare
        """
        if (card1.suit == dank_suit and card2.suit == dank_suit) or (dank_suit not in (card1.suit, card2.suit)):
            if RANK_NUM[card1.rank] > RANK_NUM[card2.rank]:
                return 1

            if RANK_NUM[card1.rank] < RANK_NUM[card2.rank]:
                return -1

            return 0

        # Only one is a dank, if x then x > y else y > x
        return 1 if card1.suit == dank_suit else -1

    return compare


for dank in SUITS:
    CARD_COMPARATORS[dank] = functools.cmp_to_key(create_comparator(dank))


def suited(card, suit):
    """
    Tell if card matches suit

    Parameters
        ----------
        card: Card
            The card to check
        suit: Card.suit
            The suit to check
    """
    return card.suit == suit


def rank_matches(cards, rank):
    """
    Return all rank matches in a set of cards

    Parameters
        ----------
        cards: list
            A list of cards
        rank: int
            The rank to check for
    """
    return [card for card in cards if card.rank == rank]
