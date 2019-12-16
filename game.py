"""
A module used to store classes related to the representation of a game

Classes
-------
Player
    The representation of a game
"""

import sys

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
        The cards on the table
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
        deck.shuffle_deck()

        self.players = [Player(x) for x in range(num_players)]
        for _ in range(6):
            for player in self.players:
                player.take(deck.draw())

        self.table_card = deck.flip()
        if self.table_card is None:
            # TODO
            sys.exit()
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

    def draw(self):
        """
        Handles the logic of giving players cards in the right order
        Attacker first, then attacker + 2, then defender, then defender + 2
        """
        # if len(self.players) == 2:
            # # Attacker then defender
            # a, d, n = self.get_players()
            # if self.deck.is_empty():

            # for _ in range(6-len(a)):
                # a.take(self.deck.draw())
        # else:
            # pass

    def play(self):
        """
        Begins and runs the game
        """
        while len(self.players) > 1:
            self.turn()
            # self.draw()
            self.turns += 1

            if self.turns > 100:
                break


            # right to left removal of empty players

            # for p_num in range(-len(self.players), -1):
            #     if len(self.players[p_num]) == 0 and self.deck.is_empty():
            #         self.players.pop()

            # Probably shouldn't take over 100
            # if self.turns > 2:
            #     break

    def get_players(self):
        """
        Returns players involved in a turn

        Returns
        -------
        Player, Player, Player
            The Attacker, the Defender, and the next Player
        """
        attacker = self.players[self.attacker]
        defender = self.players[self.add_mod(self.attacker, 1)]
        next_player = self.players[self.add_mod(self.attacker, 2)]
        return attacker, defender, next_player

    def add_mod(self, start, offset):
        """
        Returns the player that is offset after the start

        Parameters
        ----------
        start: int
            The starting position
        offset: int
            The amount to offset by

        Returns
        -------
        int
            The player that is offset after the start
        """

        return (start + offset) % len(self.players)

    def inc_attacker(self, increment):
        """
        Updates the attacker value mod number of players

        Parameters
        ----------
        increment: int
            The amount to increment by
        """
        self.attacker = (self.attacker + increment) % len(self.players)

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
        attacker, defender, next_player = self.get_players()
        table = []
        atk = attacker.attack(self.table)

        # It definitely does, this is to catch errors
        if atk[0] == Attack.play:
            pass

        table.append(atk[1])
        # FOR DEBUGGING
        # print(self.dank
        # print(attacker)
        # print("\n\n\n\n")
        # print(defender)
        # print(self.dank)
        print('Player ' + str(attacker.num) + ' Attacks with: ' + str(atk[1]))

        attacker = None

        # Pass phase
        pass_count = 0
        attack_count = 0
        defense = None
        while True:
            pass_is_legal = (len(next_player) >= len(table) + 1)
            defense = defender.defend(table, pass_is_legal, len(table))
            if defense[0] == Defense.pass_to:
                print('Player ' + str(defender.num) + ' Passes with: ' + str(defense[1][0]))
                pass_count += 1
                attack_count += 1
                self.inc_attacker(1)
                attacker, defender, next_player = self.get_players()

                table += defense[1]
                continue

            if defense[0] == Defense.take:
                print('Player ' + str(defender.num) + ' takes ' + ', '.join([str(x) for x in table]))
                defender.take_table(table)
                table = []
                self.inc_attacker(2)
                attacker, defender, next_player = self.get_players()
                break

            if defense[0] == Defense.defend:
                print('Player ' + str(defender.num) + ' defends with ' + ', '.join([str(x) for x in defense[1]]))
                break

        if pass_count > 3:
            print("Bug in game.turn, pass_count > 3")

        # Defense phase
        lastMove = None # used to check for 2 passes in a row
        attacker, defender, next_player = self.get_players()
        while attack_count < 6 and len(defender) > 0 and defense[1] != Defense.take:
            # Loop until table reaches 12 (fully attacked)
            # or len(defender) == 0 (defender is out of cards) 
            atk = attacker.attack(table)
            if atk[0] == Attack.play:
                print('Player ' + str(attacker.num) + ' Attacks with: ' + str(atk[1]))
                attack_count += 1
                # defender must defend then try again until defender takes or
                # player is done
                table.append(atk[1])
                defense = defender.defend(table, False, len(table))
                if defense[0] == Defense.defend:
                    # Attack-defense continues until one gives up or cards have
                    # reached min(6, len(defender))
                    table += defense[1]
                    print('Player ' + str(defender.num) + ' defends with ' + ', '.join([str(x) for x in defense[1]]))
                    continue
                elif defense[0] == Defense.take:
                    # Defender has to take cards
                    # move to shed then draw
                    print('Player ' + str(defender.num) + ' takes ' + ', '.join([str(x) for x in table]))
                    defender.take_table(table)
                    table = []
                    break

            elif atk[0] == Attack.done:
                print( 'Player ' + str(attacker.num) + ' has ceased attack')
                if len(self.players) == 2:
                    break
                else:
                    # TODO (Bretley)
                    # Add logic for other players to join in on the attack
                    break

            # shed phase
            if defense[0] == Defense.take:
                table += attacker.shed()
                defender.take_table(table)
                print( 'defender picks up shed')
                table = []
            else:
                pass
                # success for attacker
        return

def main():
    """
    The main function for the game
    """
    for i in range(pow(10,5)):
        game = Game(2)
        game.play()
        break


if __name__ == "__main__":
    main()
