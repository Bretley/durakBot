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

import enum
import logging

from card import CARD_COMPARATORS, rank_matches, RANK_NUM


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

    def attack(self, table):
        """
        Does an attack action

        Parameters
        ----------
        table : Table
            The cards on the table

        Returns
        -------
        Attack, Card
            An Attack enum, the card to be removed
        """

        if len(table) == 0:
            return Attack.play, self.hand.pop(0)
            # Must play, 1st attack

        # Default bot logic: play lowest first, don't pass to other player until out of matches
        # Assumes sorted hand
        matches = [card for card in self.hand if rank_in_table(card, table)]
        if matches:
            self.hand.remove(matches[0])
            return Attack.play, matches[0]

        return Attack.done, None

        # Player's attack method when option to attack:
        #     MUST play first card, then can either match or allow other attacker
        #     play one per method
        #     if pass then none ?

    def defend(self, table, pass_is_legal, cards_to_defend):
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

        if pass_is_legal:
            matches = rank_matches(self.hand, table[-1].rank)
            if matches:
                self.hand.remove(matches[0])
                return Defense.pass_to, [matches[0]]

        # Came from pass, special logic
        if cards_to_defend > 1:
            defense = []
            for attack in table:
                current_defense = lowest_defense(attack, self.hand, self.dank)
                if current_defense is not None:
                    # Accumulate defense cards to send back
                    self.hand.remove(current_defense)
                    defense.append(current_defense)
                else:
                    # Put cards back in hand and signal defeat
                    for card in defense:
                        self.hand.append(card)
                    # Don't need to sort because taking cards

                    return Defense.take, None
            return Defense.defend, defense

        attack = table[-1]
        current_defense = lowest_defense(attack, self.hand, self.dank)

        logging.debug('Defense Logic:')
        logging.debug("%s", attack)
        logging.debug("%s", self)
        logging.debug("%s", current_defense)

        if current_defense is None:
            return Defense.take, None

        self.hand.remove(current_defense)
        return Defense.defend, [current_defense]

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

        if self.dank is not None:
            # This might be more efficient than constantly iterating over hands over and over to find least valuable card
            self.sort()

        if card is not None:
            self.hand.append(card)

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

        if max_shed_allowed == 0:
            return []

        card_list = []
        for card in self.hand:
            if card.suit != self.dank and len(card_list) < max_shed_allowed and rank_in_table(card, table):
                card_list.append(card)
        return card_list


def lowest_defense(attack, hand, dank):
    """
    Returns lowest card that can defend or None
    Assumes sorted hand

    Parameters
    ----------
    attack : Card
        The card to attack with
    hand : list(Card)
        The list of cards in the hand
    dank : Card.suit
        The suit of the dank card

    Returns
    -------
    Card
        The lowest card that can defend or None if there is not a valid card
    """
    low = RANK_NUM[attack.rank]
    # Can only defend in dank suit
    if attack.suit == dank:
        for card in hand:
            rank = RANK_NUM[card.rank]
            if card.suit == dank and rank > low:
                return card

    # Can defend with any dank or higher in same suit
    else:
        for card in hand:
            rank = RANK_NUM[card.rank]
            if (card.suit == attack.suit and rank > low) or card.suit == dank:
                return card

    return None


def rank_in_table(card, table):
    """
    Returns True if a card in the hand matches one in the table by rank

    Parameters
    ------
    card : Card
        The Card to match
    table : List(Card)
        The list of Cards on the table

    Returns
    -------
    bool
        True if a card in the hand matches one in the table by rank, False otherwise
    """
    return any(card.rank == x.rank for x in table)


class Defense(enum.Enum):
    """
    A class used to enumerate defense actions
    """
    pass_to = 0
    defend = 1
    take = 2


class Attack(enum.Enum):
    """
    A class used to enumerate attack actions
    """
    play = 0
    done = 1
