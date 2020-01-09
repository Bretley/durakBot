"""A Gym environment that mimics a game of Durak.

Contains the DurakEnv class, which is a child class of the gym.Env class.
Implements all of the functions necessary to play through a game of Durak and
train a machine learning model to play it.
"""

import logging
from math import atan

# pylint: disable=import-error
import gym
import numpy as np
from gym import spaces

from card import Card, CARDS, RANK_NUM, dank_float_order
from deck import Deck
from player import Player
from strategy import Attack, Defense, S0
from random import randrange

# logging.basicConfig(level=logging.INFO)

# Constants
PRODUCTS = ['a', 'd', 's']
SUMS = ['done', 'take']
TOTAL_OPTIONS = len(CARDS) + len(['done', 'take'])

OPTIONS_DICT = {}
TOTAL = 0
for c in CARDS:
    OPTIONS_DICT[TOTAL] = c
    TOTAL += 1

OPTIONS_DICT[TOTAL] = 'done'
TOTAL += 1
OPTIONS_DICT[TOTAL] = 'take'
CARD_TO_OBS = {card: i for i, card in enumerate(CARDS)}

logging.debug("%s", OPTIONS_DICT)
logging.debug("%s", len(OPTIONS_DICT))
logging.debug("%s", OPTIONS_DICT[35])
logging.debug("%s", TOTAL_OPTIONS)
logging.debug("%s %s", 35, OPTIONS_DICT[35])
logging.debug("%s %s", 36, OPTIONS_DICT[36])
logging.debug("%s %s", 37, OPTIONS_DICT[37])

WIN = 'W'
LOSE = 'L'
CONTINUE = 'C'


class Model:
    """Model is a wrapper for the AI hand.

        Attributes:
            hand: The cards in the model's hand.
    """

    def __init__(self):
        """Inits Model.
        """

        self.hand = []

    def __len__(self):
        return len(self.hand)

    def take(self, card):
        """Adds card to the model's hand.

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


class DurakAdvEnv(gym.Env):
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

        super(DurakAdvEnv, self).__init__()

        # 36 Cards, Take, Done
        self.action_space = self.action_space = spaces.Box(low=np.array([0] * 38), high=np.array([1] * 38))

        # Bit vector of valid option
        self.attack_count = 1
        self.observation_space = spaces.MultiDiscrete([1] * 219)
        self.game_started = False
        self.deck = Deck()
        self.players = [Model(), Model()]
        self.state = None
        self.table_card = None
        self.dank = None
        self.table = []
        self.ranks = {}
        self.out_pile = []

    def gen_legal_moves(self):
        ret = np.zeros((1, 38))

        if self.state[0] == 'a':
            if len(self.table) != 0:
                ret[36] = 1
            for card in self.current_player().hand:
                if len(self.table) == 0 or card.rank in self.ranks:
                    ret[CARD_TO_OBS[card]] = 1

        elif self.state == 'd':
            ret[37] = 1
            for card in self.current_player().hand:
                # if legal card


        if self.state == 'd':
            ret[37] = 1
            for card in self.model.hand:
                if self.legal_defense(CARD_TO_OBS[card]):
                    ret[CARD_TO_OBS[card]] = 1

        # legal_shed called AFTER
        if self.state == 's':
            ret[36] = 1
            if self.first_shed:
                allowed_sheds = min(6 - self.attack_count, len(self.opponent))
                if allowed_sheds > 0:
                    for card in self.model.hand:
                        if card.rank in self.ranks:
                            ret[CARD_TO_OBS[card]] = 1
            else:
                if self.shed_so_far < self.allowed_to_shed:
                    for card in self.model.hand:
                        if card.rank in self.ranks:
                            ret[CARD_TO_OBS[card]] = 1

        return ret


    def gen_return(self, condition):
        """DOCSTRING
        """
        obs = []
        reward = 10 if condition == WIN else 0
        done = True if condition == WIN else False
        info = {'player': self.state[1]}
        return obs, reward, done, info

    def player_draw(self, index):
        player = self.players[index]
        if len(player) < 6:
            for _ in range(6 - len(player)):
                player.take(self.deck.draw())
        return len(player) == 0

    def step(self, action: list):
        """Steps through the environment
        """

        if not self.game_started:
            self.deck.shuffle_deck()
            for _ in range(6):
                self.players[0].take(self.deck.draw())
                self.players[1].take(self.deck.draw())

            self.state = ('a', randrange(0, 2))
            self.table_card = self.deck.flip()
            self.dank = self.table_card.suit
            return self.gen_return(CONTINUE)

        legal_moves = self.gen_legal_moves()

        filtered = np.multiply(np.array(legal_moves), np.abs(np.array(action) + .01))

        filtered_action = int(np.argmax(filtered))
        assert isinstance(filtered_action, int)
        move = OPTIONS_DICT[filtered_action]

        if self.state[0] == 'a':
            return self.handle_attack(move)
        elif self.state[0] == 'd':
            return self.handle_defense(move)
        elif self.state[0] == 's':
            return self.handle_shed(move)

    def current_player(self):
        return self.players[self.state[1]]

    def quick_win(self):
        return len(self.current_player()) == 0 and len(self.deck) == 0

    def add_attack(self, card):
        self.table.append(card)
        self.ranks[card.rank] = 0

    def handle_attack(self, move):
        if isinstance(move, Card):
            self.current_player().remove_card(move)
            self.add_attack(move)
            if self.quick_win():
                return self.gen_return(WIN)
            self.state = ('d', (self.state[1] + 1) % 2)
            return self.gen_return(CONTINUE)
        elif move == 'done':
            self.attack_count = 0
            self.out_pile += self.table
            self.table = []
            self.ranks = {}
            self.state = ('a', (self.state[1] + 1) % 2)
            return self.gen_return(CONTINUE)
        else:
            raise RuntimeError('Model has made move that is not card or done in attack')

    def handle_defense(self, move):
        if isinstance(move, Card):
            # if continue, different player different state
            self.current_player().remove_card(move)
            self.table.append(move)
            if self.quick_win():
                return self.gen_return(WIN)

            # check for a turn ending condition
            if len(self.players[0]) == 1 or len(self.players[1]) == 1 or self.attack_count == 6:
                # Turn is over
                if self.player_draw((self.state[1] + 1) % 2):
                    # Attacker win
                    pass

                if self.player_draw(self.state[1]):
                    # defender wins
                    pass

                # Turn was over with no winner, successful defense
                self.attack_count = 0
                self.out_pile += self.table
                self.table = []
                self.ranks = {}
                self.state = ('a', self.state[1])
                return self.gen_return(CONTINUE)

            # Turn is not over, other player gets to attack
            self.state = ('a', (self.state[1] + 1) % 2)
            return self.gen_return(CONTINUE)
        elif move == 'take':
            self.state = ('s', (self.state[1] + 1) % 2)
            return self.gen_return(CONTINUE)
        else:
            raise RuntimeError('Model has made move that is not card or take in defense')

    def handle_shed(self, move):
        if isinstance(move, Card):
            self.current_player().remove_card(move)
            self.table.append(move)
            self.attack_count += 1
            self.state = ('s', self.state[1])
        elif move == 'done':
            self.attack_count = 0
            self.players[(self.state[1] + 1) % 2].take_table(self.table)
            self.table = []
            self.ranks = {}
            if self.player_draw(self, self.state[1]):
                return self.gen_return(WIN)
            self.state = ('a', self.state[1])
            return self.gen_return(CONTINUE)
        else:
            raise RuntimeError('Model has made move that is not card or done in shed')



    def reset(self):
        """Resets the game to the starting state.
        """

    def render(self, mode='human'):
        """Will not be used.
        """
