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
SUMS = ['done', 'take']
TOTAL_OPTIONS = len(CARDS) * len(['a', 'd', 's']) + len(['done','take'])


OPTIONS_DICT = {}
TOTAL = 0
for p in PRODUCTS:
    for c in CARDS:
        OPTIONS_DICT[TOTAL] = (p, c)
        TOTAL += 1

OPTIONS_DICT[TOTAL] = ('done', None)
TOTAL += 1
OPTIONS_DICT[TOTAL] = ('take', None)
print(OPTIONS_DICT[35])
print(TOTAL_OPTIONS)
print(71, OPTIONS_DICT[71])
print(72, OPTIONS_DICT[72])
print(108, OPTIONS_DICT[108])



class DurakEnv(gym.Env):
    """The environment that represents a game of Durak.

    Durak is a Russian/Slavic/Eastern European card game that
    exists somewhere in between War and Euchre. Rounds are played with
    attackers and defenders, the first to go out wins, and the trump 'dank'
    suit matters. It's a good blend of mechanics, strategy, and luck.

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
        self.state = None
        self.dank = None
        self.table_card = None
        self.opponent = Player("Bot", S0())
        self.print_trace = True
        self.first_shed = None

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

        self.model = Model()

    def legal_shed(self, move):
        """

        Parameters
        ----------
        move: int

        Returns
        -------
            Whether or not the shed is legal
            'Done' is always a legal shed
            Shed card is legal if card is in hand and rank matches table

        """
        if self.first_shed:  # first shed state of the round
            self.first_shed = False
            self.allowed_to_shed = min(6-self.atack_count, len(opp))
            self.shed_so_far = 0
        if move == 108:
            self.first_shed  = True
            self.allowed_to_shed = -1
            return True
        elif 71 < move < 108:  # Shed action or done
            _, card = OPTIONS_DICT[move]
            if card in self.model.hand and card.rank in self.ranks and self.shed_so_far < self.allowed_to_shed:
                self.first_shed = False
            return True

        return False

    def legal_attack(self, move):
        """

        Parameters
        ----------
        move: int

        Returns
        -------
            Whether or not attack is legal
            Attack is legal if:
            move < 36 or 108
            card matches ranks in table
            card is in hand
        """
        if move < 36:  # (Attack, Card)
            _, card = OPTIONS_DICT[move]
            if card in self.model.hand and card.rank in self.ranks:
                return True
        elif move == 108: # ('done', None)
            if len(self.table) > 0:
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
        move, card = OPTIONS_DICT[action]
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
                self.state = "a"
                return obs, reward, done, info
            else:  # Bot attacks first
                atk = self.opponent.attack(self.table, self.ranks)
                if self.print_trace:
                    print('Opponent starts attack with ' + str(atk[1]))
                if atk[0] != Attack.play:
                    logging.error("Atk[0] != Attack.play, bot is attacking at start")

                self.table.append(atk[1])
                self.ranks[atk[1].rank] = 0
                del atk
                return obs, reward, done, info

        elif self.state == 'a':
            if self.legal_attack(action):
                if move == 'a':  # AI plays a card
                    self.model.remove_card(card)
                    self.table.append(card)
                    self.ranks[card.rank] = 0
                    self.attack_count += 1
                    defense = self.opponent.defend(self.table, False, 1)
                    if defense[0] == Defense.defend:
                        self.table += defense
                        # Check for end of turn conditions
                        if len(self.table) == 12 or len(self.model) == 0 or len(self.opponent) == 0:
                            # Turn is over, reset table
                            self.attack_count = 0
                            self.out_pile += self.table
                            self.table = []
                            self.ranks = {}
                            # Model will be defending next turn
                            self.state = 'd'
                            # Bot attacks table
                            atk = self.opponent.attack(self.table, self.ranks)
                            if atk[0] != Attack.play:
                                logging.error('Opponent is not attacking on first attack')
                                return None, None, True, None
                            self.table.append(atk[1])
                            self.ranks[atk[1].rank] = 0
                            self.attack_count += 1
                        else:  # Turn is not over, Model is attacking again
                            self.state = 'a'
                            return None, None, None, None
                    elif defense[0] == Defense.take:
                        self.state = 's'  # Model will be shedding in next step
                        if self.print_trace:
                            print('Opponent has chosen to take')
                        return None, None, None, None
                    else:
                        logging.error('opponent has passed cards')
                        return None, None, True, None
                    del defense
                elif move == 'done':  # AI is done in attack context
                    self.attack_count = 0
                    self.out_pile += self.table
                    self.table = []
                    self.ranks = {}
                    # Model will be defending next turn
                    self.state = 'd'
                    # Bot attacks table
                    atk = self.opponent.attack(self.table, self.ranks)
                    if atk[0] != Attack.play:
                        logging.error('Opponent is not attacking on first attack')
                        return None, None, True, None
                    self.table.append(atk[1])
                    self.ranks[atk[1].rank] = 0
                    self.attack_count += 1
                    return None, None, None, None
                else:
                    logging.error('legal_attack true but not a or move')
            else:  # Punish and end
                return None, -1, True, None
        # Defend state logic
        elif self.state == "d":
            if True:  # Bot has already attacked
                pass

        # Shed state logic
        elif self.state == "s":
            if self.legal_shed(action):
                if move == 's':
                    # Shed 1 card -> return to shed
                    self.model.remove_card(card)
                    self.table.append(card)
                    self.ranks[card.rank] = 0
                    self.state = 's'
                elif move == 'done':
                    # done -> attack
                    self.first_shed = True
                    self.opponent.take_table(self.table)
                    self.table = []
                    self.ranks = {}
                    self.state = 'a'
                else:
                    logging.error('legal_shed true but not s or done')
            else:  # Return and punish
                return None, None, True, None
            pass

        del action

        return obs, reward, done, info

    def reset(self):
        """Resets the game to the starting state.

        TODO more detail about what gets reset.
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
        self.model = Model()

    def render(self, mode='human'):
        """Will not be used.
        """
