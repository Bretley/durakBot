"""
A module used to store classes related the the representation of a player

Classes
-------
Player
    The representation of a player
"""


class Player:
    """
    A class used to represent a Player

    Attributes
    ----------
    hand : list
        The list of cards in the player's hand
    num : int
        The Player's ID

    Methods
    -------
    take(card_list)
        Adds cards to the player's hand
    """

    def __init__(self, num):
        """
        Parameters
        ----------
        num : int
            The Player's ID
        """
        self.hand = []
        self.num = num

    def __str__(self):
        """
        Returns the player as a string
        """

        ret = "==" + str(self.num) + "==\n"
        ret += "hand:\n"
        for card in self.hand:
            ret += str(card) + '\n'
        return ret

    def take(self, card_list):
        """
        Adds a card to the player's hand

        Parameters
        ----------
        card_list : list
            The list of cards to add to the player's hand
        """

        for card in card_list:
            if card is not None:
                self.hand.append(card)
