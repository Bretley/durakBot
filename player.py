"""
A module used to store classes related the the representation of a player

Classes
-------
Player
    The representation of a player
Attack
    Enum for attacking
Defense
    Enum for defending
"""



import logging

from card import CARD_COMPARATORS

from strategy import S0, S1


class Player:
    """
    A class used to represent a Player (simple bot)

    Attributes
    ----------
    hand : list(Card)
        The list of cards in the player's hand
    num : int
        The Player's ID
    dank : Card.suit
        The suit of the Dank card

    Methods
    -------
    attack(table)
        Does an attack action
    defend(table, pass_is_legal, cards_to_defend)
        Does a defense action
    sort()
        Sort's the player's hand
    take(card)
        Adds card to the player's hand
    take_table(cards)
        Adds cards to the player's hand
    shed(table, max_shed_allowed)
        Sheds cards to the player's hand
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
        self.dank = None
        if num == 0:
            self.strategy =S0()
        else:
            self.strategy = S1()

    def __len__(self):
        """
        Implements len function for Player

        Returns
        -------
        int
            The number of cards in the hand
        """
        return len(self.hand)

    def __str__(self):
        """
        Implements str function for Player

        Returns
        -------
        str
            The player as a string
        """

        ret = "==" + str(self.num) + "==\n"
        ret += "hand:\n"
        for card in self.hand:
            ret += str(card) + '\n'
        return ret

    def verify_hand(self):
        """
        Method to ensure that the hand contains 0 duplicates
        """
        return len(self.hand) == len(set(self.hand))

    def attack(self, table):
        return self.strategy.attack(self.hand, table, self.dank)
        """
        Does an attack action
        ----------
        table : Table
            The cards on the table

        Returns
        -------
        Attack, Card
            An Attack enum, the card to be removed
        """

    def defend(self, table, pass_is_legal, cards_to_defend):
        return self.strategy.defend(self.hand, table, self.dank, pass_is_legal, cards_to_defend)
        """
        Does a defense action

        Parameters
        ----------
        table : list(Card)
            The cards on the table
        pass_is_legal : bool
            Whether or not a pass is legal
        cards_to_defend : int
            The number of cards to defend against

        Returns
        -------
        Defense, list
            A Defense enum, a list of Cards
        """

    def sort(self):
        """
        Sort's the player's hand
        """

        self.hand.sort(key=CARD_COMPARATORS[self.dank])

    def take(self, card):
        """
        Adds card to the player's hand

        Parameters
        ----------
        card : Card
            The card to add to the hand
        """


        if card is not None:
            self.hand.append(card)

        if self.dank is not None:
            # This might be more efficient than constantly iterating over 
            # hands over and over to find least valuable card
            self.sort()

    def take_table(self, cards):
        """
        Adds cards to the player's hand

        Parameters
        ----------
        cards : list(Card)
            The list of cards to add to the player's hand
        """

        self.hand += cards
        self.sort()

    def shed(self, table, max_shed_allowed):
        return self.strategy.shed(self.hand, table, self.dank, max_shed_allowed)
        """
        Sheds cards to the player's hand

        Parameters
        ----------
        table : list(Card)
            The list of cards on the table
        max_shed_allowed : int
            The maximum amount of cards to shed

        Returns
        -------
        list
            A list of Cards
        """



