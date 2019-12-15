import itertools
from random import shuffle
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


class Deck:
    def __init__(self):
        self.cards = [Card(rank, suit) for rank, suit in cards]
        print(self.cards)

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
