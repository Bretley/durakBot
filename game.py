"""
A module used to store classes related to the representation of a game

Classes
-------
Player
    The representation of a game
"""

from deck import Deck, create_card_comparator, Card
from player import Player


class Game:
    """
    A class used to represent a game

    Attributes
    ----------
    players : list
        The list of players
    table_card : Card
        The card on the table
    dank: Card.suit
        The suit of the trump card
    """

    def __init__(self, num_players):
        """
        visual:
            2
        1       3
            0

        Deal 6 to each
        Determine who has initial lowest dank (otherwise default to 0)

        Parameters
        ----------
        num_players : int
            The number of players
        """
        deck = Deck()
        deck.shuffle()

        self.players = [Player(x) for x in range(num_players)]
        for _ in range(6):
            for player in self.players:
                player.take(deck.draw())

        self.table_card = deck.flip()
        self.dank = self.table_card.suit  # Determine Dank suit
        print('Table Card:')
        print(self.table_card)
        for player in self.players:
            print(player)

    def play(self):
        """
        Begins and runs the game
        """
        pass


def main():
    """
    The main function for the game
    """
    game = Game(4)
    d = Deck()
    x = sorted(d.cards, key=create_card_comparator('Diamonds'), reverse=True)
    for card in x:
        print(card)
    del game  # For now until we use something else with the game variable


if __name__ == "__main__":
    main()
