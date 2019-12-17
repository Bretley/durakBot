"""A module used to store classes related the the representation of a player.
"""

from card import CARD_COMPARATORS


class Player:
    """A class used to represent a Player (simple bot).

    Attributes:
        hand: The list of cards in the player's hand.
        num : The Player's ID.
        dank: The suit of the Dank card.
        strategy: The strategy the bot uses.
    """

    def __init__(self, num, strategy):
        """Inits Player with an ID and strategy.

        Args:
            num: The Player's ID
            strategy: Class must implement shed, attack, and defend for the bot.
        """

        self.hand = []
        self.num = num
        self.dank = None
        self.strategy = strategy

    def __len__(self):
        return len(self.hand)

    def __str__(self):
        ret = "==" + str(self.num) + "==\n"
        ret += "hand:\n"
        for card in self.hand:
            ret += str(card) + '\n'
        return ret

    def verify_hand(self):
        """Method to ensure that the hand contains 0 duplicates
        """
        return len(self.hand) == len(set(self.hand))

    def attack(self, table, ranks):
        """Does an attack action.

        Args:
            table: The cards on the table.
            ranks: TODO(Bretley)

        Returns:
            The return of the strategy's attack.
        """
        return self.strategy.attack(self.hand, table, self.dank, ranks)

    def defend(self, table, pass_is_legal, cards_to_defend):
        """Does a defense action.

        Args:
            table: The cards on the table.
            pass_is_legal: Whether or not a pass is legal.
            cards_to_defend: The number of cards to defend against.

            Returns:
                The return of the strategy's defend.
        """
        return self.strategy.defend(self.hand, table, self.dank, pass_is_legal, cards_to_defend)

    def sort(self):
        """Sorts the player's hand
        """

        self.hand.sort(key=CARD_COMPARATORS[self.dank])

    def take(self, card):
        """Adds card to the player's hand.

        Args:
            card: The card to add to the hand.
        """

        if card is not None:
            self.hand.append(card)

        if self.dank is not None:
            # This might be more efficient than constantly iterating over hands over and over to find least valuable card.
            self.sort()

    def take_table(self, cards):
        """Adds cards to the player's hand

        Args:
            cards: The list of cards to add to the player's hand.
        """

        self.hand += cards
        self.sort()

    def shed(self, table, max_shed_allowed, ranks):
        """Sheds cards to the player's hand

        Args:
            table: The list of cards on the table.
            max_shed_allowed: The maximum amount of cards to shed.
            ranks: TODO(Bretley)

            Returns:
                The return of the strategy's shed.
            """
        return self.strategy.shed(self.hand, table, self.dank, max_shed_allowed, ranks)
