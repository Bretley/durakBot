"""A Gym environment that mimics a game of Durak.

Contains the DurakEnv class, which is a child class of the gym.Env class.
Implements all of the functions necessary to play through a game of Durak and
train a machine learning model to play it.
"""

import logging
from math import sqrt, atan


# pylint: disable=import-error
import gym
from gym import spaces

import numpy as np

from card import CARDS, RANK_NUM, Card
from player import Player
from strategy import Attack, Defense, S0
from deck import Deck

PRODUCTS = ['a', 'd', 's']
SUMS = ['done', 'take']
TOTAL_OPTIONS = len(CARDS) + len(['done', 'take'])

OPTIONS_DICT = {}
TOTAL = 0
for c in CARDS:
    OPTIONS_DICT[TOTAL] = c
    TOTAL += 1

OPTIONS_DICT[TOTAL] = ('done', None)
TOTAL += 1
OPTIONS_DICT[TOTAL] = ('take', None)
CARD_TO_OBS = {card: i for i, card in enumerate(CARDS)}
logging.debug("%s", OPTIONS_DICT)
logging.debug("%s", len(OPTIONS_DICT))
logging.debug("%s", OPTIONS_DICT[35])
logging.debug("%s", TOTAL_OPTIONS)
logging.debug("%s %s", 35, OPTIONS_DICT[35])
logging.debug("%s %s", 36, OPTIONS_DICT[36])
logging.debug("%s %s", 37, OPTIONS_DICT[37])

WIN = 10
LOSE = -2
ILLEGAL = -3


class Model:
    """Model is a wrapper for the AI hand.

        Attributes:
            hand: TODO(Bretley)
    """

    def __init__(self):
        """Inits Model.
        """
        self.hand = []

    def __len__(self):
        return len(self.hand)

    def take(self, card):
        """
        Adds card to the model's hand.

        Args:
            card: The card to add to the hand.
        """

        if card is not None:
            self.hand.append(card)

    def take_table(self, cards):
        """Adds cards to the model's hand.

        Args:
        cards: The list of cards to add to the model's hand.
        """
        self.hand += cards

    def remove_card(self, card):
        """Removes a card from the model's hand.

        Args:
            card: The card to remove from the model's hand.
        """
        self.hand.remove(card)


class DurakEnv(gym.Env):
    """The environment that represents a game of Durak.

    Durak is a Russian/Slavic/Eastern European card game that
    exists somewhere in between War and Euchre. Rounds are played with
    attackers and defenders, the first to go out wins, and the trump 'dank'
    suit matters. It's a good blend of mechanics, strategy, and luck.

    Attributes:
        action_space: The set of available actions.
        observation_space: The set of variables in the environment.
        game_started: Whether or not the game has been started.
        deck: Deck object containing cards.
        out_pile: List of cards that are out of the game.
        players: The number of players.
        turns: The number of turns taken so far.
        table: The cards on the current attack/defense.
        ranks: Hash table of ranks of cards in table.
        attack_count: Count of attacks this turn.
        state: String representing the state of the game DFA.
        dank: String representing the dank suit.
        table_card: Card at the bottom of the deck.
        opponent: Bot that plays against the Model.
        print_trace: Whether or not to print trace of the game.
        first_shed: True if first shed of the turn, false otherwise.
        shed_so_far: Number of cards shed so far.
        allowed_to_shed: Total number of cards the Model could shed.
        model: Model object wrapper, mostly manages Model's hand.
    """

    def __init__(self):
        """Inits DurakEnv.
        """

        metadata = {'render.modes': ['human']}
        del metadata

        super(DurakEnv, self).__init__()

        # x36 Cards, Take, Done
        self.action_space = spaces.Discrete(38)

        # 1 Discrete observation for now just to set it up
        self.observation_space = spaces.Box(low=np.array([0] * 37), high=np.array(([4] * 36) + [2]), dtype=int)

        self.game_started = False
        self.deck = Deck()
        self.out_pile = []
        self.players = []
        self.turns = 0
        self.table = []
        self.ranks = {}
        self.attack_count = 0
        self.state = None
        self.dank = None
        self.table_card = None
        self.opponent = Player("Bot", S0())
        self.print_trace = False
        self.first_shed = True
        self.shed_so_far = None
        self.allowed_to_shed = None
        self.model = Model()
        self.legal_moves = 0.
        self.successful_attacks = 0.
        self.successful_defenses = 0.
        self.takes = 0.

    def add_attack(self, card: Card):
        """

        Args:
            card: Card to be added to the table

        Returns
        -------
            None

        """
        self.table.append(card)
        self.ranks[card.rank] = 0
        self.attack_count += 1

    def clear_table(self):
        """Method to clean up variables related to the table

        Returns
        -------
            None

        """
        self.out_pile += self.table
        self.table = []
        self.ranks = {}
        self.attack_count = 0

    def player_draw(self, player):
        """ players draw and report win condition

        Args:
            player: Model or Player

        Returns:
            True if player is out of cards after draw
            False otherwise

        """

        if len(player) < 6:
            for _ in range(6 - len(player)):
                player.take(self.deck.draw())
            if len(player) == 0:
                return True

        return False

    def legal_defense(self, move):
        """Determines whether a defense is a legal action or not.

        Args:
            move: The defense to check.

        Returns:
            True if defense is legal.
            Defense is legal if it is higher rank same suit,or any dank,
            or higher dank in the case that a dank was played.

        """

        if move == 109:
            # Take is always legal in defense.
            return True

        if move < 36:
            # Made a defense move.
            card = OPTIONS_DICT[move]
            # Defend against attack.
            attack = self.table[-1]
            if card in self.model.hand:
                if card.suit == attack.suit and RANK_NUM[card.rank] > RANK_NUM[attack.rank]:
                    # Higher in same suit, dank or non.
                    return True

                if attack.suit != self.dank and card.suit == self.dank:
                    # Or defense is dank suit and attack is not.
                    return True
        return False

    def legal_shed(self, move):
        """Determines whether a shed is a legal action or not.

        Args:
            move: The attack to check.

        Returns:
            Whether or not the shed is legal.
            'Done' is always a legal shed.
            Shed card is legal if card is in hand and rank matches table.

        """

        # First shed state of the round.
        if self.first_shed:
            self.first_shed = False
            self.allowed_to_shed = min(6 - self.attack_count, len(self.opponent))
            self.shed_so_far = 0
        # done is always legal during a shed
        if move == 36:
            self.first_shed = True
            self.allowed_to_shed = -1
            return True

        # Shed action or done.
        if move < 36:

            card = OPTIONS_DICT[move]
            if card in self.model.hand and card.rank in self.ranks and self.shed_so_far < self.allowed_to_shed:
                self.first_shed = False
            return True

        return False

    def legal_attack(self, move):
        """Determines whether an attack is a legal action or not.

        Args:
            move: The attack to check.

        Returns:
            Attack is legal if:
            Move < 36 or 108.
            Card matches ranks in table.
            Card is in hand.
        """

        # has chosen to play a card
        if move < 36:
            card = OPTIONS_DICT[move]
            if card in self.model.hand and card.rank in self.ranks:
                return True
        # 'done'
        elif move == 36:
            if len(self.table) != 0:
                return True
        return False

    def step(self, action: int):
        """Proceeds through a single step in the game.

        Goes from one state of the game to the next based on the input action
        that it receives and returns relevant information. TODO more detail.

        Args:
            action: The action to take on this step.
        Returns:
            A gym.space that represents the current state of the game.
            A float that represents the fitness of this genome.
            A bool that represents whether or not the game is done.
            A list that contains additional information that may be useful.
        """

        logging.debug("%s", action)
        logging.debug('f')
        move = OPTIONS_DICT[action]
        logging.debug("%s", move)

        if not self.game_started:
            self.game_started = True
            self.deck.shuffle_deck()
            for _ in range(6):  # Deal cards
                self.opponent.take(self.deck.draw())
                self.model.take(self.deck.draw())

            self.table_card = self.deck.flip()
            self.dank = self.table_card.suit

            # Start state nonsense.

            # AI attacks first.
            if int(action) % 2 == 0:
                self.state = "a"
                logging.info('Model attacks first')
                return self.gen_obs(), self.gen_score(), False, None

            logging.info('bot attacks first')
            # Bot attacks first.
            atk = self.opponent.attack(self.table, self.ranks)

            if self.print_trace:
                print('Opponent starts attack with ' + str(atk[1]))

            if atk[0] != Attack.play:
                raise RuntimeError("Atk[0] != Attack.play, bot is attacking at start.")

            self.add_attack(atk[1])
            self.state = 'd'
            del atk
            return self.gen_obs(), self.gen_score(), False, None

        if self.state == 'a':
            logging.info('state a')
            if self.legal_attack(action):
                self.legal_moves += 1
                logging.info('legal card action')
                # AI plays a card.
                if isinstance(move, Card):
                    self.model.remove_card(move)
                    self.add_attack(move)
                    defense = self.opponent.defend(self.table, False, 1)
                    # Both players still have cards or drawing potential
                    if defense[0] == Defense.defend:
                        self.table += defense
                        # Check for end of turn conditions.
                        if len(self.table) == 12 or len(self.model) == 0 or len(self.opponent) == 0:
                            # Turn is over, reset table.
                            self.clear_table()

                            # Draw cards, attacker then defender
                            if self.player_draw(self.model):
                                # TODO: Model wins on attack
                                return self.gen_obs(), self.gen_score() + WIN, True, None

                            if self.player_draw(self.opponent):
                                # TODO:  Bot wins defending in attack phase
                                return self.gen_obs(), self.gen_score() + LOSE, True, None

                            # Bot attacks table.
                            atk = self.opponent.attack(self.table, self.ranks)
                            # Model will be defending next turn.
                            self.state = 'd'

                            if atk[0] != Attack.play:
                                raise RuntimeError('Opponent is not attacking on first attack.')
                            self.add_attack(atk[1])
                            return self.gen_obs(), self.gen_score(), False, None
                        # Turn is not over, Model is attacking again
                        self.state = 'a'
                        return self.gen_obs, self.gen_score(), False, None
                    if defense[0] == Defense.take:
                        self.state = 's'  # Model will be shedding in next step
                        # if self.print_trace:
                        # 'Opponent has chosen to take'
                        self.successful_attacks += 1
                        return self.gen_obs(), self.gen_score(), False, None
                    raise RuntimeError('Opponent has passed cards')
                if move == 'done':  # AI is done in attack context
                    self.clear_table()
                    # Bot attacks table
                    atk = self.opponent.attack(self.table, self.ranks)
                    if atk[0] != Attack.play:
                        raise RuntimeError('Opponent is not attacking on first attack.')
                    self.add_attack(atk[1])
                    # Model will be defending next turn
                    self.state = 'd'
                    return self.gen_obs(), self.gen_score(), False, None
                raise RuntimeError('Legal_attack true but not attack or move.')
            # Punish and end.
            return self.gen_obs(), self.gen_score() + ILLEGAL, True, None
        # Defend state logic.
        if self.state == "d":
            logging.info('state d')
            self.legal_moves += 1
            # Bot has already attacked.
            if self.legal_defense(action):
                if isinstance(move, Card):
                    self.table.append(move)
                    self.model.remove_card(move)
                    if len(self.table) == 12 or len(self.model) == 0 or len(self.opponent) == 0:
                        # Turn is over
                        self.clear_table()
                        # Draw cards, attacker (opponent) then defender (model)
                        if self.player_draw(self.opponent):
                            # TODO:  Bot wins defending in attack phase
                            return self.gen_obs(), self.gen_score() + LOSE, True, None
                        if self.player_draw(self.model):
                            # TODO: Model wins on attack
                            return self.gen_obs(), self.gen_score() + WIN, True, None
                        # if game hasn't ended, the turn is over and the bot successfully defends
                        self.state = "a"
                        return self.gen_obs(), self.gen_score(), False, None

                    atk = self.opponent.attack(self.table, self.ranks)
                    if atk[0] == Attack.play:
                        self.add_attack(atk[1])
                        self.state = "d"
                        return self.gen_obs(), self.gen_score(), False, None

                    if atk[0] == Attack.done:
                        self.clear_table()
                        # Players get to draw, attacker first.
                        # It shouldn't be possible for a win condition here
                        if self.player_draw(self.opponent):
                            raise RuntimeError('Win condition in defense phase:\nOpponent has won after ceasing attack.')

                        if self.player_draw(self.model):
                            raise RuntimeError('Win condition in defense phase:\nModel has won after ceasing attack.')

                        self.successful_defenses += 1
                        self.state = 'a'
                    else:
                        raise RuntimeError('In defense phase, opponent has not chosen play or done.')

                elif move == 'take':
                    # Bot gets to shed
                    self.takes += 1
                    shed = self.opponent.shed(self.table, min((6 - self.attack_count, len(self.model))), self.ranks)
                    if self.print_trace:
                        print("opponent sheds: " + ", ".join([str(x) for x in shed]))

                    if self.player_draw(self.opponent):
                        # TODO: opponent has won on their shed
                        return self.gen_obs(), self.gen_score() + LOSE, True, None

                    self.table += shed
                    self.model.take_table(self.table)
                    # self.table = [] before clear table to prevent out pile duplicate
                    self.table = []
                    self.clear_table()

                    # get Bot Attack
                    atk = self.opponent.attack(self.table, self.ranks)
                    if atk[0] != Attack.play:
                        raise RuntimeError('opponent is not attacking on first attack')
                    self.add_attack(atk[1])
                    # Model will be defending next turn
                    self.state = 'd'
                    return self.gen_obs(), self.gen_score(), False, None
                else:
                    raise RuntimeError('legal_defense true but not defense or take: move = {}'.format(str(move)))
            else:
                # Return and punish.
                return self.gen_obs(), self.gen_score() + ILLEGAL, True, None

        # Shed state logic.
        elif self.state == "s":
            logging.info('state s')
            if self.legal_shed(action):
                self.legal_moves += 1
                if isinstance(move, Card):
                    # Shed 1 card -> return to shed.
                    self.model.remove_card(move)
                    self.add_attack(move)
                    self.state = 's'
                elif move == 'done':
                    # Done -> attack.
                    self.first_shed = True
                    self.opponent.take_table(self.table)

                    # self.table = [] before clear table to prevent duplicates in out pile
                    self.table = []
                    self.clear_table()
                    self.state = 'a'

                    # check win condition / draw
                    # opponent shouldn't have to draw here
                    if self.player_draw(self.model):
                        # TODO: Model has won by shedding last cards
                        return self.gen_obs(), self.gen_score() + WIN, True, None
                    return self.gen_obs(), self.gen_score(), False, None

                else:
                    raise RuntimeError('legal_shed true but not shed or done')
            # Return and punish.
            else:
                return self.gen_obs(), self.gen_score() + ILLEGAL, True, None

        logging.info("%s", self.state)

        return self.gen_obs(), self.gen_score(), False, None

    def gen_obs(self):
        """

        -------
        Returns an observation based on game state
            0 unknown
            1 on table
            2 in hand
            3 in out pile

        """

        ret = [0] * 36
        # 1 if on table
        for card in self.table:
            ret[CARD_TO_OBS[card]] = 1
        # 2 if in hand
        for card in self.model.hand:
            ret[CARD_TO_OBS[card]] = 2

        # 3 if in out pile
        for card in self.out_pile:
            ret[CARD_TO_OBS[card]] = 3

        ret[CARD_TO_OBS[self.table_card]] = 4

        if self.state == "d":
            ret[-1] = 0
        elif self.state == "a":
            ret[-1] = 1
        else:
            ret[-1] = 2

        return np.array(ret)

    def gen_score(self):
        """TODO
        """
        # base reward for not messing up
        legal_moves_reward = 2 * 5 * atan(self.legal_moves)/3.1415
        # ratio of bot making opponent take vs opponent making bot take
        attack_success_reward = sqrt(self.successful_attacks/(self.takes+1)) - 0.8
        taking_reward = 2/3.1415 * 3.5 * atan(4-self.takes)
        return legal_moves_reward + attack_success_reward + taking_reward

    def reset(self):
        """Resets the game to the starting state.
        """
        self.game_started = False
        self.deck = Deck()
        self.out_pile = []
        self.players = []
        self.turns = 0
        self.table = []
        self.ranks = {}
        self.attack_count = 0
        self.state = None
        self.dank = None
        self.table_card = None
        self.opponent = Player("Bot", S0())
        self.first_shed = True
        self.shed_so_far = None
        self.allowed_to_shed = None
        self.model = Model()
        self.legal_moves = 0.
        self.successful_attacks = 0.
        self.successful_defenses = 0.
        self.takes = 0.

    def render(self, mode='human'):
        """Will not be used.
        """
