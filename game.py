from deck import Deck
from player import Player


class Game:
    def __init__(self, numPlayers):
        """ visual:
            2
        1       3
            0
        """
        """
            Deal 6 to each
            Determine who has initial lowest dank (otherwise default to 0)
        """
        d = Deck()
        d.shuffle()
        self.players = [Player(x) for x in range(numPlayers)]
        for cardNum in range(6):
            for p in self.players:
                p.take(d.draw())

        self.tableCard = d.flip()
        self.dank = self.tableCard.suit  # Determine Dank suit
        print('Table Card:')
        print(self.tableCard)
        for p in self.players:
            print(p)


g = Game(4)
