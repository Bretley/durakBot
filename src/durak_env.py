"""A Gym environment that mimics a game of Durak.

Contains the DurakEnv class, which is a child class of the gym.Env class.
Implements all of the functions necessary to play through a game of Durak and
train a machine learning model to play it.
"""

import gym
from gym import spaces
import logging

from card import Card, RANKS, SUITS, Cards
from player import Player
from strategy import Attack, Defense, S0, S1, S2

poducts = ['a', 'd', 's']
sums = ['done']
total_options = len(CARDS) * len(['a', 'd', 's']) + len(['done'])

options_dict = {}
total = 0
for c in CARDS:
    for p in products:
        options_dict[total] = (p, c)
        total += 1

options_dict[total] = ('done', None)


print(options_dict)


class DurakEnv(gym.Env):
    """The environment that represents a game of Durak.

    TODO more detail about Durak.

    Attributes:
        action_space: The set of available actions.
        observation_space: The set of variables in the environment.
    """

    def __init__(self):
        """Inits DurakEnv with default data.
        """

        metadata = {'render.modes': ['human']}
        del metadata

        super(DurakEnv, self).__init__()

        # Attack(x36 cards), Defend(x36 cards), Shed(x36 Cards), Stop Shedding, Take, Done
        self.action_space = spaces.Discrete(111)

        # 1 Discrete observation for now just to set it up
        self.observation_space = spaces.Discrete(1)
        self.game_started = False
        self.deck = None
        self.out_pile = []
        self.players = []
        self.turns = 0
        self.table = []
        self.ranks = {}
        self.attacker = 0
        self.attack_count = 0
        self.state = False
        self.dank = None
        self.table_card = None
        self.opponent = Player("Bot", S0())


        class AI:
            def __init__(self):
                self.hand = []
            def take(self, card):
                """
                Adds card to the player's hand

                Parameters
                ----------
                card : Card
                    The card to add to the hand
                """

                if card is not None:
                    self.hand.append(card)

            def take_table(self, cards):
                """
                Adds cards to the player's hand

                Parameters
                ----------
                cards : list(Card)
                    The list of cards to add to the player's hand
                """
                self.hand += cards

            def remove_card(self, card):
                self.hand.remove(card)

        self.ai = AI()

    def step(self, action):
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
        obs = None
        reward = 0
        done = True
        info = {}
        table = self.table

        if not self.game_started:
            for _ in range(6):
                self.opponent.take(self.deck.draw())
                self.ai.take(self.deck.draw())

            self.table_card = self.table.flip()
            self.dank = self.table_card.suit

            # Start state nonsense
            if True:  # AI attacks first
                self.state = "a"
                return obs, reward, done, info
            else:  # Bot attacks first
                atk = self.opponent.attack(self.table, self.ranks)
                if self.print_trace:
                    print('Opponent starts attack with ' + str(atk[1]))
                if atk[0] != Attack.play:
                    logging.error("Atk[0] != Attack.play, bot is attacking at start")

                self.table.append(atk[1])
                return obs, reward, done, info

        elif self.state == "a":
            if True:  # AI plays a card

                if True:  # AI plays a legal move
                    pass
                else:  # AI plays an illegal action
                    pass
            elif False:  # AI is done
                pass
        elif self.state == "d":
            if True:  # Bot 
                pass
        elif self.state == "s":
            pass

        del action

        return obs, reward, done, info

    def reset(self):
        """Resets the game to the starting state.

        TODO more detail about what gets reset.
        """

    def render(self, mode='human'):
        """Will not be used.
        """
