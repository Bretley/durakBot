"""
A module used to store the card class

Classes
-------
Card
    The representation of a card
"""

import functools
import itertools
import logging


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

    def __hash__(self):
        return hash(self.suit + self.rank)
    
    def __init__(self, rank, suit):
        """
        """
        if rank not in RANKS:
            logging.error("Invalid rank %s for initialized card!", rank)
        if suit not in SUITS:
            logging.error("Invalid suit %s for initialized card!", suit)

        self.rank = rank
        self.suit = suit

    def __str__(self):
        """
        Implements str function for Card

        Returns
        -------
        str
            The card as a string
        """
        return self.rank + ' of ' + self.suit

    def __eq__(self, o):
        return self.rank == o.rank and self.suit == o.suit


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
    dank_suit : Card.suit
        The suit of the dank card

    Returns
        -------
        function
            A comparator function
    """

    def compare(card1, card2):
        """
        Compares two cards

        Parameters
        ----------
        card1 : Card
            The first card to compare
        card2 : Card
            The second card to compare

        Returns
        -------
        int
            -1 if the first card is smaller
            0 if they are the same
            1 if the first card is bigger
        """
        if (card1.suit == dank_suit and card2.suit == dank_suit) or (dank_suit not in (card1.suit, card2.suit)):
            if RANK_NUM[card1.rank] > RANK_NUM[card2.rank]:
                return 1

            if RANK_NUM[card1.rank] < RANK_NUM[card2.rank]:
                return -1

            return 0

        # Only one is a dank, if card1 then card1 > card2 else card2 > card1
        return 1 if card1.suit == dank_suit else -1

    return compare


for dank in SUITS:
    CARD_COMPARATORS[dank] = functools.cmp_to_key(create_comparator(dank))


def suited(card, suit):
    """
    Tell if card matches suit

    Parameters
        ----------
        card : Card
            The card to check
        suit : Card.suit
            The suit to check

    Returns
    -------
    bool
        True if they are the same suit, false otherwise
    """
    return card.suit == suit


def rank_matches(cards, rank):
    """
    Return all rank matches in a set of cards

    Parameters
        ----------
        cards : list(Card)
            A list of cards
        rank : int
            The rank to check for

    Returns
    -------
    list
        The list of cards that match the rank
    """
    return [card for card in cards if card.rank == rank]
