"""A module used to store classes related to the representation of a game

Mostly used for playing bots against each other and developing strategies.
"""

import logging
import sys

from card import CARD_COMPARATORS, RANK_NUM, RANKS
from deck import Deck
from player import Player
from strategy import Attack, Defense, S0, S1, S2


def pad_after(s):
    return s + ' '*(15-len(s))


class Game:
    """A class used to represent a game.

    Attributes:
        players: The list of players.
        table_card: The card on the table.
        dank: The suit of the trump card.
        cmp: A card comparator function.
        turns: A count of turns that have passed.
        table: The cards on the table.
        attacker: The player that is attacking.
    """

    def __init__(self, strategies, print_trace):
        """Inits Game with strategy and print trace data.

        visual:
            2
        1       3
            0

        Deal 6 to each
        Determine who has initial lowest dank (otherwise default to 0)

        Args:
            strategies: Contains the instantiated strategies for the players.
            print_trace: Whether or not to print a human readable trace.
        """
        self.print_trace = print_trace
        deck = Deck()
        deck.shuffle_deck()
        self.deck = deck
        self.out_pile = []

        if len(strategies) == 0:
            logging.error("Number of players is 0!")
            sys.exit()

        self.players = [Player(i, x) for i, x in enumerate(strategies)]
        for _ in range(6):
            for player in self.players:
                player.take(self.deck.draw())

        self.table_card = self.deck.flip()
        if self.table_card is None:
            logging.error("Table Card is None upon game instantiation!")
        # Determines Dank suit.
        self.dank = self.table_card.suit
        self.cmp = CARD_COMPARATORS[self.dank]
        self.turns = 0
        self.table = []
        self.attacker = 0

        logging.debug('Table Card:')
        logging.debug("%s", self.table_card)

        # Checks danks at start of round, whoever has the lowest one goes first, else we default to 0.
        min_rank = 9
        min_start = None
        for player in self.players:
            # Gives player dank suit knowledge.
            player.dank = self.dank
            player.sort()
            for card in player.hand:
                if card.suit == self.dank and RANK_NUM[card.rank] < min_rank:
                    min_start = (player.num, card)
                    min_rank = RANK_NUM[card.rank]
        if min_start is not None:
            self.attacker = min_start[0]

        self.game_started = False
        self.state = None

    def add_mod(self, start, offset):
        """Returns the player that is offset after the start/

        Args:
            start: The starting position.
            offset: The amount to offset by.

        Returns:
            The player that is offset after the start.
        """

        return (start + offset) % len(self.players)

    def get_players(self):
        """Returns players involved in a turn.

        Returns:
            The Attacker, the Defender, and the next Player.
        """

        attacker = self.players[self.attacker]
        defender = self.players[self.add_mod(self.attacker, 1)]
        next_player = self.players[self.add_mod(self.attacker, 2)]
        return attacker, defender, next_player

    def inc_attacker(self, increment):
        """Updates the attacker value mod number of players"

        Args:
            increment: The amount to increment by.
        """
        self.attacker = (self.attacker + increment) % len(self.players)

    def play(self):
        """Begins and runs the game.
        """
        while True:
            if self.print_trace:
                print('====== Turn ' + str(self.turns) + '===========')
                print('Dank: ' + self.dank, ' Deck: ' + str(len(self.deck)))
                self.print_hands()
            winning_player = self.turn2()
            if winning_player is not None:
                break
            self.turns += 1

        if winning_player is None:
            logging.error('ERROR: nobody has won')
        elif len(self.deck) > 0:
            logging.error('Someone has won with cards in the deck.')
            logging.error('Player ' + str(winning_player.num) + ' has won!')

        if self.print_trace:
            print('Player ' + str(winning_player.num) + ' has won!')

        return winning_player

    def step(self):
        """TODO(Bretley)
        """
        if self.state == 'Attack':
            pass
        elif self.state == 'Defend':
            pass
        elif self.state == 'Shed':
            pass
        pass

    def turn2(self):
        """Turn reflecting a guaranteed 2 person game.
        """

        # TODO(Bretley) is this what you wanted?
        ranks = RANKS.copy()
        # ENDTODO

        attacker, defender, next_player = self.get_players()
        table = []
        atk = attacker.attack(table, ranks)

        # It definitely does, this is to catch errors.
        if atk[0] != Attack.play:
            logging.error("Atk[0] != Attack.play, bot is attacking at start.")

        table.append(atk[1])

        logging.debug("%s", self.dank)
        logging.debug("%s", attacker)
        logging.debug("\n\n\n\n")
        logging.debug("%s", defender)
        logging.debug("%s", self.dank)

        # Pass phase.
        pass_count = 0
        attack_count = 0

        while True:
            pass_is_legal = (len(next_player) >= len(table) + 1)
            defense = defender.defend(table, pass_is_legal, len(table))
            if defense[0] == Defense.pass_to:
                if self.print_trace:
                    print('Player ' + str(defender.num) + ' Passes with: ' + str(defense[1][0]))
                pass_count += 1
                attack_count += 1
                self.inc_attacker(1)
                attacker, defender, next_player = self.get_players()
                table += defense[1]
                ranks.update({x.rank: 0 for x in defense[1]})
                continue

            if defense[0] == Defense.take:
                break

            if defense[0] == Defense.defend:
                if self.print_trace:
                    print('Player ' + str(defender.num) + ' defends with ' + ', '.join([str(x) for x in defense[1]]))
                table += defense[1]
                ranks.update({x.rank: 0 for x in defense[1]})
                break

        if pass_count > 3:
            logging.error("Bug in game.turn, pass_count > 3")

        # Defense phase.
        # Used to check for 2 passes in a row.
        attacker, defender, next_player = self.get_players()
        if defense[0] != Defense.take:
            while attack_count < 6 and len(defender) > 0 and len(attacker) > 0 and len(table) < 12:
                # Loops until table reaches 12 (fully attacked) or len(defender) == 0 (defender is out of cards).
                atk = attacker.attack(table, ranks)
                if atk[0] == Attack.play:
                    if self.print_trace:
                        print('Player ' + str(attacker.num) + ' Attacks with: ' + str(atk[1]))
                    attack_count += 1
                    # Defender must defend then try again until defender takes or player is done.
                    table.append(atk[1])
                    defense = defender.defend(table, False, 1)
                    if defense[0] == Defense.defend:
                        # Attack-defense continues until one gives up or cards have reached min(6, len(defender)).
                        table += defense[1]
                        ranks.update({x.rank: 0 for x in defense[1]})
                        if self.print_trace:
                            print('Player ' + str(defender.num) + ' defends with ' + ', '.join([str(x) for x in defense[1]]))
                        continue

                    if defense[0] == Defense.take:
                        # Break out and drop to shed phase
                        break

                elif atk[0] == Attack.done:

                    # TODO (Bretley) Add logic for other players to join in on the attack.
                    break

        # Shed phase.
        if defense[0] == Defense.take:
            shed = attacker.shed(table, min((6-attack_count, len(defender))), ranks)
            if self.print_trace:
                print('Player ' + str(attacker.num) + ' sheds: ' + ', '.join([str(x) for x in shed]))
            table += shed
            defender.take_table(table)
            if self.print_trace:
                print('Player : ' + str(defender.num) + ' picks up: ' + ', '.join([str(x) for x in table]))
            if len(table) > len(set(table)):
                logging.error('ERROR: Duplicates in the table')
                logging.error([str(x) for x in table])
        elif atk[0] == Attack.done or len(table) == 12:
            if self.print_trace:
                print('Player ' + str(attacker.num) + ' has ceased attack')
            self.out_pile += table
            if len(table) > len(set(table)):
                logging.error('ERROR: Duplicates in the table')
                logging.error([str(x) for x in table])
            pass

        elif len(attacker) == 0:
            # print( 'attacker')
            # print('Player ' + str(attacker.num) + ' has run out of cards')
            pass

        elif len(defender) == 0:
            # print( 'defender' )
            # print('Player ' + str(defender.num) + ' has run out of cards')
            pass
        else:
            logging.error([str(x) for x in table])
            logging.error('table size ' + str(len(table)))
            logging.error(str(len(attacker)))
            logging.error(str(len(defender)))
            logging.error('not a defense or done')
            logging.error(str(atk))
            logging.error(str(defense))
            # Success for defender.

        del table
        del ranks

        for player in self.players:
            if not player.verify_hand():
                logging.error("Player : " + str(player.num) + ' has duplicate cards')

        if len(self.out_pile) > len(set(self.out_pile)):
            logging.error('out pile has duplicates')

        # Draw: Win condition.
        # Player is definitely a winner if, after drawing, they have zero cards.
        # Attacker draws first, so if deck empties then defender wins.
        # Payer draws up to 6 cards.

        if len(attacker) < 6:
            for _ in range(6-len(attacker)):
                attacker.take(self.deck.draw())

        if len(attacker) == 0:
            return attacker
            # Attacker has won.

        if len(defender) < 6:
            for _ in range(6-len(defender)):
                defender.take(self.deck.draw())

        if len(defender) == 0:
            return defender
            # Defender has won.

        if defense[0] == Defense.take:
            self.inc_attacker(2)
        else:
            self.inc_attacker(1)

        return None

    def turn(self):
        """Method reflecting a single turn.

        General gist:
        Attacker attacks to + 1 % len(self.players):
            Play 1 card:
        Defender has 3 choices:
            Pass -> Can only be done if all cards on table match rank (i.e attack with 6 -> pass to next with 6 -> pass with 6).
                As soon as a non-6 is played cards can't be passed.
            Defend -> Plays a card higher rank and same suit.
            Take -> Takes up to 12 cards, gets skipped.
                After that, the attackers can shed.

        Back and forth.
        Can't play more than min(6, len(defender.cars)).
        Round is over when either a player runs out of cards.
        """
        pass

    def print_hands(self):
        """Prints the cards in both hands.
        """
        p1 = str(self.players[0]).split('\n')
        p2 = str(self.players[1]).split('\n')
        if len(p1) < len(p2):
            p1 += ['']*(len(p2) - len(p1))
        elif len(p2) < len(p1):
            p2 += ['']*(len(p1) - len(p2))
        out = '\n'.join([pad_after(x) + y for x, y in zip(p1, p2)])
        print(out)


def main():
    """The main function for the game.
    """
    turns = []
    s0_wins = 0
    s1_wins = 0
    s2_wins = 0
    num_games = pow(10, 4)
    for _ in range(num_games):
        game = Game([S1(), S2()], False)
        wp = game.play()
        turns.append(float(game.turns))
        if isinstance(wp.strategy, S0):
            s0_wins += 1
        elif isinstance(wp.strategy, S1):
            s1_wins += 1
        elif isinstance(wp.strategy, S2):
            s2_wins += 1

    print('Finished ' + str(num_games) + ' averaging ' + str(sum(turns)/len(turns)) + ' turns')
    print('s0 wins: ' + str(s0_wins))
    print('s1 wins: ' + str(s1_wins))
    print('s2 wins: ' + str(s2_wins))


if __name__ == "__main__":
    main()
