"""
A module used to store classes related the the representation of a player

Classes
-------
Player
    The representation of a player
"""

import enum

from card import *



class Player:
    """
    A class used to represent a Player (simple bot)

    Attributes
    ----------
    hand : list
        The list of cards in the player's hand
    num : int
        The Player's ID

    Methods
    -------
    take(card)
        Adds card to the player's hand
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

    def __str__(self):
        """
        Returns the player as a string
        """

        ret = "==" + str(self.num) + "==\n"
        ret += "hand:\n"
        for card in self.hand:
            ret += str(card) + '\n'
        return ret

    def sort(self):
        self.hand.sort(key=CARD_COMPARATORS[self.dank])

    def take_table(self, cards):
        self.hand += cards
        print( self.hand)
        self.sort()

    def take(self, card):
        if self.dank is not None:
            self.sort()
            # this might be more efficient than constantly 
            # iterating over hands over and over to find least valuable card
        """
        Adds a card to the player's hand

        Parameters
        ----------
        card: Card(rank, suit)
            The list of cards to add to the player's hand
        """
        if card is not None:
            self.hand.append(card)

    def __len__(self):
        """
        Implements len function for Player:
        """
        return len(self.hand)

    def defend(self, table, pass_is_legal, cards_to_defend):
        if pass_is_legal:
            matches = rank_matches(self.hand, table[-1].rank)
            if matches != []:
                self.hand.remove(matches[0])
                print( matches[0])
                return (Defense.pass_to, [matches[0]])
        
        if cards_to_defend > 1:  # came from pass, special logic
            defense = []
            for attack in table:
                current_defense = lowest_defense(attack, self.hand, self.dank)
                if current_defense is not None:
                    # Accumulate defense cards to send back
                    self.hand.remove(current_defense)
                    defense.append(current_defense)
                else:
                    # Put cards back in hand and signal defeat
                    for x in defense:
                        self.hand.append(x)
                    return (Defense.take, None)  # Don't need to sort because taking cards
            return (Defense.defend, defense)
        else:  # the last card played was a single attack, we can just use -1
            attack = table[-1]
            current_defense = lowest_defense(attack, self.hand, self.dank)
            print( 'defense logic')
            print( attack)
            print( self)
            print( current_defense)
            if current_defense is None:
                return (Defense.take, None)
            else:
                self.hand.remove(current_defense)
                return (Defense.defend, [current_defense])
        return (Defense.take, None)

    def attack(self, table):
        if len(table) == 0:
            return (Attack.play, self.hand.pop(0))
            # must play
        else:
            return (None, None)

        """
        Player's attack method when option to attack:
            MUST play first card, then can either match or allow other attacker 
            play one per method
            if pass then none ?
        """


def lowest_defense(attack, hand, dank):
    """
    returns lowest card that can defend or None
    Assumes sorted hand
    """
    low = RANK_NUM[attack.rank]
    if attack.suit == dank:  # Can only defend in dank suit
        for card in hand:
            rank = RANK_NUM[card.rank]
            if card.suit == dank and rank > low:
                return card
    else:  # Can defend with any dank or higher in same suit
        for card in hand:
            rank = RANK_NUM[card.rank]
            if (card.suit == attack.suit and rank > low) or card.suit == dank:
                return card 
        return None
                
class Defense(enum.Enum):
    pass_to = 0
    defend = 1
    take = 2


class Attack(enum.Enum):
    play = 0
    done = 1

