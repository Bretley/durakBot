"""
A module used to store classes related the the representation of a game

Classes
-------
Player
    The representation of a game
"""

from deck import Deck
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

    Methods
    -------
    temp_public_method()
        A method to be implemented later TODO
    temp_public_method_2()
        A method to be implemented later TODO
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

    def temp_public_method(self):
        """
        A method to be implemented later TODO
        """

    def temp_public_method_2(self):
        """
        A method to be implemented later TODO
        """


def main():
    """
    The main function for the game
    """
    game = Game(4)
    del game  # For now until we use something else with the game variable


if __name__ == "__main__":
    main()
