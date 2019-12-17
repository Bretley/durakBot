"""Contains various strategies for bots to employ.

The Strategy class is an interface for for the various strategies.
All strategies need an attack, defense, and shed.
"""

import enum
import logging

from card import RANK_NUM


def rank_matches(cards, rank):
    """Return all rank matches in a set of cards.

    Args:
        cards: A list of cards.
        rank: The rank to check for.

    Returns:
        The list of cards that match the rank.
    """

    return [card for card in cards if card.rank == rank]


def lowest_defense(attack, hand, dank):
    """Returns lowest card that can defend or None.

    Assumes sorted hand.

    Args:
        attack: The card to attack with
        hand: The list of cards in the hand
        dank: The suit of the dank card

    Returns:
        The lowest card that can defend or None if there is not a valid card
    """

    low = RANK_NUM[attack.rank]
    # Can only defend in dank suit.
    if attack.suit == dank:
        for card in hand:
            rank = RANK_NUM[card.rank]
            if card.suit == dank and rank > low:
                return card

    # Can defend with any dank or higher in same suit.
    else:
        for card in hand:
            rank = RANK_NUM[card.rank]
            if (card.suit == attack.suit and rank > low) or card.suit == dank:
                return card

    return None


class Defense(enum.Enum):
    """A class used to enumerate defense actions.
    """
    pass_to = 0
    defend = 1
    take = 2


class Attack(enum.Enum):
    """A class used to enumerate attack actions.
    """
    play = 0
    done = 1


class Strategy:
    """An interface for strategies.
    """

    def __init__(self):
        """Inits Strategy.
        """

    def attack(self, hand, table, dank, ranks):
        """An attack turn.

        Args:
            hand: The list of cards in the player's hand.
            table: The cards on the table.
            dank: The suit of the Dank card.
            ranks: TODO(Bretley)
        """

    def defend(self, hand, table, dank, pass_is_legal, cards_to_defend):
        """A defense turn.

        Args:
            hand: The list of cards in the player's hand.
            table: The cards on the table.
            dank: The suit of the Dank card.
            pass_is_legal: Whether or not a pass is legal.
            cards_to_defend: The number of cards to defend against.
        """

    def shed(self, hand, table, dank, max_shed_allowed, ranks):
        """A shed turn.

        Args:
            hand: The list of cards in the player's hand.
            table: The cards on the table.
            dank: The suit of the Dank card.
            max_shed_allowed: The maximum amount of cards to shed.
            ranks: TODO(Bretley)
        """


class S0(Strategy):
    """TODO(Bretley)
    """

    def attack(self, hand, table, dank, ranks):
        """TODO(Bretley)

        Args:
            hand: The list of cards in the player's hand.
            table: The cards on the table.
            dank: The suit of the Dank card.
            ranks: TODO(Bretley)

        Returns:
            TODO(Bretley)
        """

        if len(table) == 0:
            return Attack.play, hand.pop(0)
            # Must play, 1st attack.

        # Default bot logic: play lowest first, don't pass to other player until out of matches.
        # Assumes sorted hand.
        matches = [card for card in hand if card.rank in ranks]
        if matches:
            hand.remove(matches[0])
            return Attack.play, matches[0]

        return Attack.done, None

    def defend(self, hand, table, dank, pass_is_legal, cards_to_defend):
        """TODO(Bretley)

        Args:
            hand: The list of cards in the player's hand.
            table: The cards on the table.
            dank: The suit of the Dank card.
            pass_is_legal: Whether or not a pass is legal.
            cards_to_defend: The number of cards to defend against.

        Returns:
            TODO(Bretley)
        """

        if pass_is_legal:
            matches = rank_matches(hand, table[-1].rank)
            if matches:
                hand.remove(matches[0])
                return Defense.pass_to, [matches[0]]

        # Came from pass, special logic.
        if cards_to_defend > 1:
            defense = []
            for attack in table:
                current_defense = lowest_defense(attack, hand, dank)
                if current_defense is not None:
                    # Accumulate defense cards to send back.
                    hand.remove(current_defense)
                    defense.append(current_defense)
                else:
                    # Put cards back in hand and signal defeat.
                    for card in defense:
                        hand.append(card)
                    # Don't need to sort because taking cards.

                    return Defense.take, None
            return Defense.defend, defense

        attack = table[-1]
        current_defense = lowest_defense(attack, hand, dank)

        logging.debug('Defense Logic:')
        logging.debug("%s", attack)
        logging.debug("%s", self)
        logging.debug("%s", current_defense)

        if current_defense is None:
            return Defense.take, None

        hand.remove(current_defense)
        return Defense.defend, [current_defense]

    def shed(self, hand, table, dank, max_shed_allowed, ranks):
        """TODO(Bretley)

        Args:
            hand: The list of cards in the player's hand.
            table: The cards on the table.
            dank: The suit of the Dank card.
            max_shed_allowed: The maximum amount of cards to shed.
            ranks: TODO(Bretley)

        Returns:
            A list of cards to shed.
        """

        if max_shed_allowed == 0:
            return []

        card_list = []
        for card in hand:
            if len(card_list) < max_shed_allowed and card.rank in ranks:
                card_list.append(card)
        for card in card_list:
            hand.remove(card)

        return card_list


class S1(Strategy):
    """TODO(Bretley)

    Identical to S0 except:
        does not shed danks
        does not pass if it requires a dank to do so
    """

    def attack(self, hand, table, dank, ranks):
        """TODO(Bretley)

        Args:
            hand: The list of cards in the player's hand.
            table: The cards on the table.
            dank: The suit of the Dank card.
            ranks: TODO(Bretley)

        Returns:
            TODO(Bretley)
        """

        if len(table) == 0:
            return Attack.play, hand.pop(0)
            # Must play, 1st attack.

        # Default bot logic: play lowest first, don't pass to other player until out of matches.
        # Assumes sorted hand.
        matches = [card for card in hand if card.rank in ranks]
        if matches:
            hand.remove(matches[0])
            return Attack.play, matches[0]

        return Attack.done, None

    def defend(self, hand, table, dank, pass_is_legal, cards_to_defend):
        """TODO(Bretley)

        Args:
            hand: The list of cards in the player's hand.
            table: The cards on the table.
            dank: The suit of the Dank card.
            pass_is_legal: Whether or not a pass is legal.
            cards_to_defend: The number of cards to defend against.

        Returns:
            TODO(Bretley)
        """

        if pass_is_legal:
            matches = rank_matches(hand, table[-1].rank)
            if matches and matches[0].suit != dank:
                hand.remove(matches[0])
                return Defense.pass_to, [matches[0]]

        # Came from pass, special logic.
        if cards_to_defend > 1:
            defense = []
            for attack in table:
                current_defense = lowest_defense(attack, hand, dank)
                if current_defense is not None:
                    # Accumulate defense cards to send back.
                    hand.remove(current_defense)
                    defense.append(current_defense)
                else:
                    # Put cards back in hand and signal defeat.
                    for card in defense:
                        hand.append(card)
                    # Don't need to sort because taking cards.

                    return Defense.take, None
            return Defense.defend, defense

        attack = table[-1]
        current_defense = lowest_defense(attack, hand, dank)

        logging.debug('Defense Logic:')
        logging.debug("%s", attack)
        logging.debug("%s", self)
        logging.debug("%s", current_defense)

        if current_defense is None:
            return Defense.take, None

        hand.remove(current_defense)
        return Defense.defend, [current_defense]

    def shed(self, hand, table, dank, max_shed_allowed, ranks):
        """TODO(Bretley)

        Args:
            hand: The list of cards in the player's hand.
            table: The cards on the table.
            dank: The suit of the Dank card.
            max_shed_allowed: The maximum amount of cards to shed.
            ranks: TODO(Bretley)

        Returns:
            A list of cards to shed.
        """

        if max_shed_allowed == 0:
            return []

        card_list = []
        for card in hand:
            if card.suit != dank and len(card_list) < max_shed_allowed and card.rank in ranks:
                card_list.append(card)
        for card in card_list:
            hand.remove(card)

        return card_list


class S2(Strategy):
    """TODO(Bretley)

    Identical to S0 except:
        does not shed danks
        does not shed if card rank > 10
        does not pass if it requires a dank to do so
    """

    def attack(self, hand, table, dank, ranks):
        """TODO(Bretley)

        Args:
            hand: The list of cards in the player's hand.
            table: The cards on the table.
            dank: The suit of the Dank card.
            ranks: TODO(Bretley)

        Returns:
            TODO(Bretley)
        """

        if len(table) == 0:
            return Attack.play, hand.pop(0)
            # Must play, 1st attack.

        # Default bot logic: play lowest first, don't pass to other player until out of matches.
        # Assumes sorted hand.
        matches = [card for card in hand if card.rank in ranks]
        if matches:
            hand.remove(matches[0])
            return Attack.play, matches[0]

        return Attack.done, None

    def defend(self, hand, table, dank, pass_is_legal, cards_to_defend):
        """TODO(Bretley)

        Args:
            hand: The list of cards in the player's hand.
            table: The cards on the table.
            dank: The suit of the Dank card.
            pass_is_legal: Whether or not a pass is legal.
            cards_to_defend: The number of cards to defend against.

        Returns:
            TODO(Bretley)
        """

        if pass_is_legal:
            matches = rank_matches(hand, table[-1].rank)
            if matches and matches[0].suit != dank:
                hand.remove(matches[0])
                return Defense.pass_to, [matches[0]]

        # Came from pass, special logic.
        if cards_to_defend > 1:
            defense = []
            for attack in table:
                current_defense = lowest_defense(attack, hand, dank)
                if current_defense is not None:
                    # Accumulate defense cards to send back.
                    hand.remove(current_defense)
                    defense.append(current_defense)
                else:
                    # Put cards back in hand and signal defeat.
                    for card in defense:
                        hand.append(card)
                    # Don't need to sort because taking cards.

                    return Defense.take, None
            return Defense.defend, defense

        attack = table[-1]
        current_defense = lowest_defense(attack, hand, dank)

        logging.debug('Defense Logic:')
        logging.debug("%s", attack)
        logging.debug("%s", self)
        logging.debug("%s", current_defense)

        if current_defense is None:
            return Defense.take, None

        hand.remove(current_defense)
        return Defense.defend, [current_defense]

    def shed(self, hand, table, dank, max_shed_allowed, ranks):
        """TODO(Bretley)

        Args:
            hand: The list of cards in the player's hand.
            table: The cards on the table.
            dank: The suit of the Dank card.
            max_shed_allowed: The maximum amount of cards to shed.
            ranks: TODO(Bretley)

        Returns:
            A list of cards to shed.
        """

        if max_shed_allowed == 0:
            return []

        card_list = []
        for card in hand:
            if card.suit != dank and len(card_list) < max_shed_allowed and (
                    card.rank in ranks and RANK_NUM[card.rank] < RANK_NUM['J']):
                card_list.append(card)
        for card in card_list:
            hand.remove(card)

        return card_list
