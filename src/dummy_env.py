"""A Gym environment that mimics a game of Durak.

Contains the DurakEnv class, which is a child class of the gym.Env class.
Implements all of the functions necessary to play through a game of Durak and
train a machine learning model to play it.
"""

import logging

# pylint: disable=import-error
import gym
import numpy as np
from gym import spaces

from card import CARDS
from game import Game
from strategy import S0, S1, S2, StratAI

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

WIN = 10
LOSE = 0
ILLEGAL = -3


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


class DurakEnvDummy(gym.Env):
    """The environment that represents a game of Durak.

    """

    def __init__(self):
        """Inits DurakEnv.
        """

        super(DurakEnvDummy, self).__init__()

        # 36 Cards, Take, Done
        self.action_space = spaces.Box(low=np.array([0, 0]), high=np.array([1, 1]))

        # Bit vector of valid option
        self.observation_space = spaces.Discrete(1)

    def step(self, action):
        """The main function for the game.
        """

        turns = []
        s0_wins = 1
        s1_wins = 0
        s2_wins = 0
        ai_wins = 1
        num_games = pow(10, 3)
        action_list = list(action)
        if action_list[0] < 0 or action_list[0] > 1 or action_list[1] < 0 or action_list[1] > 1:
            return [1], 0, True, None
        for _ in range(num_games):

            game = Game([StratAI(action_list[0], action_list[1]), S0()], False)
            game_instance = game.play()

            turns.append(float(game.turns))
            if isinstance(game_instance.strategy, S0):
                s0_wins += 1
            elif isinstance(game_instance.strategy, S1):
                s1_wins += 1
            elif isinstance(game_instance.strategy, S2):
                s2_wins += 1
            elif isinstance(game_instance.strategy, StratAI):
                ai_wins += 1

        print('Finished ' + str(num_games) + ' averaging ' + str(sum(turns) / len(turns)) + ' turns')
        print('s0 wins: ' + str(s0_wins))
        print('s1 wins: ' + str(s1_wins))
        print('s2 wins: ' + str(s2_wins))
        print('ai_wins: ' + str(ai_wins))
        print('ai_ratio: ' + str(float(ai_wins) / s0_wins))

        return [1], (float(ai_wins) / s0_wins), True, None

    def reset(self):
        """Resets the game to the starting state.
        """

    def render(self, mode='human'):
        """Will not be used.
        """
