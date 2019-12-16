"""
A module used to store classes related to the representation of a game

Classes
-------
Player
    The representation of a game
"""

from card import CARD_COMPARATORS, RANK_NUM
from deck import Deck
from player import Attack, Defense, Player


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
    cmp : CARD_COMPARATORS
        A card comparator function
    turns : int
        A count of turns that have passed
    table : list
        TODO(Bretley)
    attacker : int
        The player that is attacking

    Methods
    -------
    play()
        Begins and runs the game
    turn()
        Method reflecting a single turn
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
        self.cmp = CARD_COMPARATORS[self.dank]
        self.turns = 0
        self.table = []
        self.attacker = 0

        # FOR DEBUGGING
        # print('Table Card:')
        # print(self.table_card)

        # Check danks at start of round
        # Whoever has the lowest one goes first
        # Else we default to 0

        min_rank = 9
        min_start = None
        for player in self.players:
            # Give player dank suit knowledge
            player.dank = self.dank
            player.sort()
            for card in player.hand:
                if card.suit == self.dank and RANK_NUM[card.rank] < min_rank:
                    min_start = (player.num, card)
                    min_rank = RANK_NUM[card.rank]
        if min_start is not None:
            self.attacker = min_start[0]
        # FOR DEBUGGING
        # print(held_danks[0][0], held_danks[0][1])

    def play(self):
        """
        Begins and runs the game
        """
        while len(self.players) > 1:
            self.turn()
            self.turns += 1

            break

            # right to left removal of empty players

            # for p_num in range(-len(self.players), -1):
            #     if len(self.players[p_num]) == 0 and self.deck.is_empty():
            #         self.players.pop()

            # Probably shouldn't take over 100
            # if self.turns > 2:
            #     break
    def add_mod(self, a, b):
        """
        returns  a+ b mod number of players

        Parameters
        ----------
        a: int
        b: int
        """

        return (a + b) % len(self.players)

    def inc_attacker(self, i):
        """
        Updates the attacker value mod number of players

        Parameters
        ----------
        i: int
        """
        self.attacker = (self.attacker + i) % len(self.players)

    def turn(self):
        """
        Method reflecting a single turn

        General gist:
        Attacker attacks to + 1 % len(self.players):
            Play 1 card:
        Defender has 3 choices:
            Pass -> Can only be done if all cards on table match rank (i.e attack with 6 -> pass to next with 6 -> pass with 6)
                As soon as a non-6 is played cards can't be passed
            Defend -> Plays a card higher rank and same suit
            Take -> Takes up to 12 cards, gets skipped
                After that, the attackers can shed

        Back and forth
        Can't play more than min(6, len(defender.cars))
        Round is over when either a player runs out of cards
        """

        # Attack phase
        pass_to = self.add_mod(self.attacker, 2)
        attacker = self.players[self.attacker]
        defender = self.players[self.add_mod(self.attacker, 1)]
        table = []
        atk = attacker.attack(self.table)

        # It definitely does, this is to catch errors
        if atk[0] == Attack.play:
            pass

        table.append(atk[1])
        # FOR DEBUGGING
        print(self.dank)
        print(attacker)
        print("\n\n\n\n")
        print(defender)
        print(self.dank)
        print('Player ' + str(attacker.num) + ' Attacks with: ' + str(atk[1]))

        # Pass phase
        pass_count = 0
        while True:
            pass_is_legal = (len(self.players[pass_to]) >= len(table) + 1)
            defense = defender.defend(table, pass_is_legal, len(table))
            if defense[0] == Defense.pass_to:
                print('Player ' + str(defender.num) + ' Passes with: ' + str(defense[1][0]))
                pass_count += 1
                self.inc_attacker(1)
                attacker = self.players[self.attacker]
                defender = self.players[self.add_mod(self.attacker, 1)]

                # TODO(Bretley) Use attacker
                del attacker

                table += defense[1]
                continue

            if defense[0] == Defense.take:
                print('Player ' + str(defender.num) + ' takes ' + ', '.join([str(x) for x in table]))
                defender.take_table(table)
                self.inc_attacker(2)
                break

            if defense[0] == Defense.defend:
                print('Player ' + str(defender.num) + ' defends with ' + ', '.join([str(x) for x in defense[1]]))
                break

        if pass_count > 3:
            print("Bug in game.turn, pass_count > 3")

        # Defense phase
        attacker = self.players[self.attacker]
        atk = attacker.attack(table)
        if atk[0] == Attack.play:
            pass
        elif atk[0] == Attack.done:
            pass

        if pass_count > 3:
            print("Bug in game turn, pass_count > 3")


def main():
    """
    The main function for the game
    """
    game = Game(2)
    game.play()


if __name__ == "__main__":
    main()
