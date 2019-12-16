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


def create_comparator(dank):
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
    return compare


for dank in SUITS:
    CARD_COMPARATORS[dank] = functools.cmp_to_key(create_comparator(dank))


def suited(card, suit):
    """
    tell if card matches suit
    """
    return card.suit == suit


def rank_matches(cards, rank):
    """
    return all rank matches in a set of cards
    """
    return [card for card in cards if card.rank == rank]
