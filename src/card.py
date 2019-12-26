"""A module used to store the Card class.

Represents a playing card from a Durak deck, which is a standard deck but with
the cards 2-5 removed.
"""

import functools
import itertools


class Card:
    """Represents a card object.

    Attributes
        rank: The value of a card, 6-A.
        suit: The suit of the card: Diamonds, Spades, Clubs, or Hearts.
    """

    def __init__(self, rank, suit):
        """Inits the Card with a rank and a suit.

        Args:
            rank: The rank of the card.
            suit: The suit of the card.
        """

        if rank not in RANKS:
            raise TypeError("Invalid rank {} for initialized card!".format(rank))
        if suit not in SUITS:
            raise TypeError("Invalid suit {} for initialized card!".format(suit))

        self.rank = rank
        self.suit = suit

    def __eq__(self, o):
        if not isinstance(0, Card):
            return False
        return self.rank == o.rank and self.suit == o.suit

    def __hash__(self):
        return hash(self.suit + self.rank)

    def __str__(self):
        return self.rank + ' of ' + self.suit


# Constants representing possible cards and attributes of cards.
RANKS = ['A', 'K', 'Q', 'J', '10', '9', '8', '7', '6']
SUITS = ['Diamonds', 'Spades', 'Clubs', 'Hearts']
CARDS = [Card(rank, suit) for rank, suit in itertools.product(RANKS, SUITS)]
RANK_NUM = {rank: index for index, rank in enumerate(reversed(RANKS))}
CARD_COMPARATORS = {}


def create_comparator(dank_suit):
    """Creates a comparator to compare two cards.

    Args:
        dank_suit: The suit of the dank card.

    Returns:
        A comparator function based on the dank suit.
    """

    def compare(card1, card2):
        """Compares two cards

        Args:
            card1: The first card to compare.
            card2: The second card to compare.

        Returns:
            -1 if the first card is smaller.
            0 if both cards are the same.
            1 if the first card is bigger.
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
    """Tells if the card matches the suit.

    Args
        card: The card to check.
        suit: The suit to check.

    Returns
        True if they are the same suit, false otherwise.
    """

    return card.suit == suit
