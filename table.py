"""
A module used to store classes related the the representation of a table state

Classes
-------
Table
    The representation of a table
"""


class Table:
    """
    A class used to represent a table

    Attributes
    ----------
    attacks : list(Card)
        The list of Cards in the attack pile
    defense : list(Card)
        The list of Cards in the defend pile

    Methods
    -------
    add_attack(card)
        Adds a card to the attack pile
    add_defense(card)
        Adds a card to the defense pile
    """

    def __init__(self):
        """
        """
        self.attacks = []
        self.defense = []

    def add_attack(self, card):
        """
        Adds a card to the attack pile

        Parameters
        ----------
        card : Card
            The card to add to the pile
        """
        self.attacks.append(card)

    def add_defense(self, card):
        """
        Adds a card to the defense pile

        Parameters
        ----------
        card : Card
            The card to add to the pile
        """
        self.defense.append(card)
