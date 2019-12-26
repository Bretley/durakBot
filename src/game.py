"""A module used to store classes related to the representation of a game.

Mostly used for playing bots against each other and developing strategies.
"""

import logging

from card import CARD_COMPARATORS, RANK_NUM
from deck import Deck
from player import Player
from strategy import Attack, Defense, S0, S1, S2


def pad_after(input_str):
    """Pads a string with extra spaces.

        Args:
            input_str: The string to pad.

        Returns:
            A padded string.
        """
    return input_str + ' ' * (15 - len(input_str))


class Game:
    """Represents a game.

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

        Deal 6 to each.
        Determine who has initial lowest dank. (otherwise default to 0)

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
            raise RuntimeError("Number of players is 0!")

        self.players = [Player(i, x) for i, x in enumerate(strategies)]
        for _ in range(6):
            for player in self.players:
                player.take(self.deck.draw())

        self.table_card = self.deck.flip()
        if self.table_card is None:
            raise RuntimeError("Table Card is None upon game instantiation!")
        # Determines Dank suit.
        self.dank = self.table_card.suit
        self.cmp = CARD_COMPARATORS[self.dank]
        self.turns = 0
        self.table = []
        self.attacker = 0

        logging.info('Table Card:')
        logging.info("%s", self.table_card)

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
        """Returns the player that is offset after the start.

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
        """Updates the attacker value mod number of players.

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
            raise RuntimeError('ERROR: nobody has won')
        if len(self.deck) > 0:
            logging.debug('Player %s has won!', str(winning_player.num))
            raise RuntimeError('Someone has won with cards in the deck.')

        if self.print_trace:
            print('Player ' + str(winning_player.num) + ' has won!')

        return winning_player

    def turn2(self):
        """Turn reflecting a guaranteed 2 person game.
        """

        ranks = {}

        attacker, defender, next_player = self.get_players()
        table = []
        atk = attacker.attack(table, ranks)

        # It definitely does, this is to catch errors.
        if atk[0] != Attack.play:
            raise RuntimeError("Atk[0] != Attack.play, bot is attacking at start.")

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
            raise RuntimeError("Bug in game.turn, pass_count > 3")

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
                        # Break out and drop to shed phase.
                        break

                elif atk[0] == Attack.done:

                    # TODO (Bretley) Add logic for other players to join in on the attack.
                    break

        # Shed phase.
        if defense[0] == Defense.take:
            shed = attacker.shed(table, min((6 - attack_count, len(defender))), ranks)
            if self.print_trace:
                print('Player ' + str(attacker.num) + ' sheds: ' + ', '.join([str(x) for x in shed]))
            table += shed
            defender.take_table(table)
            if self.print_trace:
                print('Player : ' + str(defender.num) + ' picks up: ' + ', '.join([str(x) for x in table]))
            if len(table) > len(set(table)):
                logging.debug([str(x) for x in table])
                raise RuntimeError('ERROR: Duplicates in the table')
        elif atk[0] == Attack.done or len(table) == 12:
            if self.print_trace:
                print('Player ' + str(attacker.num) + ' has ceased attack')
            self.out_pile += table
            if len(table) > len(set(table)):
                logging.debug([str(x) for x in table])
                raise RuntimeError('ERROR: Duplicates in the table')

        elif len(attacker) == 0:
            logging.info('attacker')
            if self.print_trace:
                print('Player ' + str(attacker.num) + ' has run out of cards')

        elif len(defender) == 0:
            logging.info('defender')
            if self.print_trace:
                print('Player ' + str(defender.num) + ' has run out of cards')
        else:
            logging.debug([str(x) for x in table])
            logging.debug('table size %s', str(len(table)))
            logging.debug(str(len(attacker)))
            logging.debug(str(len(defender)))
            logging.debug(str(atk))
            logging.debug(str(defense))
            raise RuntimeError("Not a defense or done.")

        del table
        del ranks

        for player in self.players:
            if not player.verify_hand():
                raise RuntimeError("Player {} has duplicate cards".format(str(player.num)))

        if len(self.out_pile) > len(set(self.out_pile)):
            raise RuntimeError('Out pile has duplicates.')

        # Draw: Win condition.
        # Player is definitely a winner if, after drawing, they have zero cards.
        # Attacker draws first, so if deck empties then defender wins.
        # Payer draws up to 6 cards.

        if len(attacker) < 6:
            for _ in range(6 - len(attacker)):
                attacker.take(self.deck.draw())

        if len(attacker) == 0:
            # Attacker has won.
            return attacker

        if len(defender) < 6:
            for _ in range(6 - len(defender)):
                defender.take(self.deck.draw())

        if len(defender) == 0:
            # Defender has won.
            return defender

        if defense[0] == Defense.take:
            self.inc_attacker(2)
        else:
            self.inc_attacker(1)

        return None

    def print_hands(self):
        """Prints the cards in both hands.
        """

        player1 = str(self.players[0]).split('\n')
        player2 = str(self.players[1]).split('\n')
        if len(player1) < len(player2):
            player1 += [''] * (len(player2) - len(player1))
        elif len(player2) < len(player1):
            player2 += [''] * (len(player1) - len(player2))
        out = '\n'.join([pad_after(x) + y for x, y in zip(player1, player2)])
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
        game_instance = game.play()
        turns.append(float(game.turns))
        if isinstance(game_instance.strategy, S0):
            s0_wins += 1
        elif isinstance(game_instance.strategy, S1):
            s1_wins += 1
        elif isinstance(game_instance.strategy, S2):
            s2_wins += 1

    print('Finished ' + str(num_games) + ' averaging ' + str(sum(turns) / len(turns)) + ' turns')
    print('s0 wins: ' + str(s0_wins))
    print('s1 wins: ' + str(s1_wins))
    print('s2 wins: ' + str(s2_wins))


if __name__ == "__main__":
    main()
