"""
A module used to store classes related to the representation of a game

Classes
-------
Player
    The representation of a game
"""

from deck import *
from card import *
from player import *


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
        for card_num in range(6):
            for player in self.players:
                player.take(deck.draw())

        self.table_card = deck.flip()
        self.dank = self.table_card.suit  # Determine Dank suit
        self.cmp = CARD_COMPARATORS[self.dank]
        self.turns = 0
        self.table = []
        self.attacker = 0
        # print('Table Card:')
        # print(self.table_card)

        # check danks at start of round
        # whoever has the lowest one goes first
        # else we default to 0
        min_rank = 9
        min_start = None
        for player in self.players:
            player.dank = self.dank  # give player dank suit knowledge
            player.sort()
            for card in player.hand:
                if card.suit == self.dank and RANK_NUM[card.rank] < min_rank:
                    min_start = (player.num, card)
                    min_rank = RANK_NUM[card.rank]
        if min_start is not None:
            self.attacker = min_start[0]
        # print(held_danks[0][0], held_danks[0][1])



    def turn(self):
        """
        method reflecting a single turn
        """
        """
        General gist:
        attacker attacks to + 1 % len(self.players):
            play 1 card:
        defender has 3 choices:
            pass -> Can only be done if all cards on table match rank
                (i.e attack with 6 -> pass to next with 6 -> pass with 6)
                as soon as a non-6 is played cards can't be passed
            defend -> plays a card higher rank and same suit
            take -> takes up to 12 cards, gets skipped
                after that, the attackers can shed


        back and forth
        can't play more than min(6, len(defender.cars))
        round is over when either a player runs out of cards 
        """

        # Attack phase
        pass_to = (self.attacker + 2) % len(self.players)
        attacker = self.players[self.attacker]
        defender = self.players[(self.attacker + 1) % len(self.players)]
        table = []
        atk = attacker.attack(self.table)
        if atk[0] == Attack.play:  # it definitely does, this is to catch errors
            pass

        table.append(atk[1])
        print( self.dank)
        print(attacker)
        print()
        print()
        print()
        print()
        print()
        print(defender)
        print( self.dank)
        print('Player ' + str(attacker.num) + ' Attacks with: ' + str(atk[1]))

        # pass phase
        pass_count = 0
        while True:
            pass_is_legal = (len(self.players[pass_to]) >= len(table) + 1)
            defense = defender.defend(table, pass_is_legal, len(table))
            if defense[0] == Defense.pass_to:
                print( 'Player ' + str(defender.num) + ' Passes with: ' + str(defense[1][0]))
                pass_count += 1
                self.attacker = (self.attacker + 1) % len(self.players)
                attacker = self.players[self.attacker]
                defender = self.players[(self.attacker + 1) % len(self.players)]
                table += defense[1]
                continue
            elif defense[0] == Defense.take:
                print( 'Player ' + str(defender.num) + ' takes ' + ', '.join([str(x) for x in table]))
                defender.take_table(table)
                self.attacker = (self.attacker + 2) % len(self.players)
                break
            elif defense[0] == Defense.defend:
                print('Player ' + str(defender.num) + ' defends with ' + 
                        ', '.join([str(x) for x in defense[1]]))
                break

        if pass_count > 3:
            print( "Bug in game.turn, pass_count > 3")

        # Defense phase
        attacker = self.players[self.attacker]
        atk = attacker.attack(table)
        if atk[0] == Attack.play:
            pass
        elif atk[0] == Attack.done:
            pass



    def play(self):
        """
        Begins and runs the game
        """
        while len(self.players) > 1:
            self.turn()
            self.turns += 1

            break

            # right to left removal of empty players
            for p_num in range(-len(self.players), -1):
                if len(self.players[p_num]) == 0 and self.deck.isEmpty():
                    self.players.pop()

            if self.turns > 2:  # Probably shouldn't take over 100
                break


def main():
    """
    The main function for the game
    """
    g = Game(2)
    g.play()
    # for x in range(pow(10, 5)):
        # game = Game(4)
    # del g  # For now until we use something else with the game variable


if __name__ == "__main__":
    main()
