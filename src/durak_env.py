"""A Gym environment that mimics a game of Durak.

Contains the DurakEnv class, which is a child class of the gym.Env class.
Implements all of the functions necessary to play through a game of Durak and
train a machine learning model to play it.
"""

# TODO Figure this out.
# pylint: disable=import-error
import gym
from gym import spaces
import logging

from card import Card, RANKS, SUITS, CARDS
from player import Player
from strategy import Attack, Defense, S0, S1, S2
from deck import Deck

PRODUCTS = ['a', 'd', 's']
SUMS = ['done']
TOTAL_OPTIONS = len(CARDS) * len(['a', 'd', 's']) + len(['done'])


OPTIONS_DICT = {}
TOTAL = 0
for p in PRODUCTS:
    for c in CARDS:
        OPTIONS_DICT[TOTAL] = (p, c)
        TOTAL += 1

OPTIONS_DICT[TOTAL] = ('done', None)
print(OPTIONS_DICT[35])
print(TOTAL_OPTIONS)
print(OPTIONS_DICT[TOTAL_OPTIONS-1])



class DurakEnv(gym.Env):
    """The environment that represents a game of Durak.

    TODO more detail about Durak.

    Attributes:
        action_space: The set of available actions.
        observation_space: The set of variables in the environment.
        game_started: Boolean
        deck: Deck object containing cards
        out_pile: List of cards that are out of the game
        players: number of players
        turns: number of turns so far
        table: cards on the current attack/defense
        ranks: hash table of ranks of cards in table
        attack_count: count of attacks this turn
        state: String representing the state of the game dfa
        dank: string representing dank suit
        table_card: card at the bottom of the deck
        opponent: Bot that plays against the Model
        model: Model object wrapper, mostly manages Model's hand
    """

    def __init__(self):
        """Inits DurakEnv.
        """

        metadata = {'render.modes': ['human']}
        del metadata

        super(DurakEnv, self).__init__()

        # Attack(x36 cards), Defend(x36 cards), Shed(x36 Cards), Take, Done
        self.action_space = spaces.Discrete(110)

        # 1 Discrete observation for now just to set it up
        self.observation_space = spaces.Discrete(1)

        self.game_started = False
        self.deck = Deck()
        self.out_pile = []
        self.players = []
        self.turns = 0
        self.table = []
        self.ranks = {}
        self.attack_count = 0
        self.state = False
        self.dank = None
        self.table_card = None
        self.opponent = Player("Bot", S0())
        self.print_trace = True

        class Model:
            """
                Model is a wrapper for the AI hand

                Attributes:
                    hand: TODO
            """

            def __init__(self):
                """Inits Model.
                """
                self.hand = []

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

        self.model = Model()

    def legal_attack(self, attack):
        """

        Parameters
        ----------
        attack: int

        Returns
        -------
            Attack is legal if:
            action < 36 or 108
            card matches ranks in table
            card is in hand
        """
        if attack < 36:
            move, card = OPTIONS_DICT[attack]
            if card in self.model.hand and card.rank in self.ranks:
                return True
        elif attack == 108:
            if len(self.table) != 0:
                return True
        return False



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
        print(action)
        m_type, card = OPTIONS_DICT[action]
        obs = None
        reward = 0
        done = False
        info = {}

        if not self.game_started:
            self.deck.shuffle_deck()
            for _ in range(6):  # Deal cards
                self.opponent.take(self.deck.draw())
                self.model.take(self.deck.draw())

            self.table_card = self.deck.flip()
            self.dank = self.table_card.suit

            # Start state nonsense

            if int(action) % 2 == 0:  # AI attacks first
                print('int works')
                self.state = "a"
                return obs, reward, done, info
            else:  # Bot attacks first
                atk = self.opponent.attack(self.table, self.ranks)
                if self.print_trace:
                    print('Opponent starts attack with ' + str(atk[1]))
                if atk[0] != Attack.play:
                    logging.error("Atk[0] != Attack.play, bot is attacking at start")

                self.table.append(atk[1])
                self.ranks.update({atk[1].rank:0})
                return obs, reward, done, info

        elif self.state == 'a':
            if m_type == 'a':  # AI plays a card
                if self.legal_attack(action):
                    self.model.remove_card(card)
                    self.table.append(card)
                    self.ranks[card.rank] = 0
                else:
                    # punish and return
                    pass
            elif m_type == 'd':  # AI is done
                pass
            else:  # Punish and end
                return None, -1, True, None
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
