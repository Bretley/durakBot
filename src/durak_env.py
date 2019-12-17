"""A Gym environment that mimics a game of Durak.

Contains the DurakEnv class, which is a child class of the gym.Env class.
Implements all of the functions necessary to play through a game of Durak and
train a machine learning model to play it.
"""

# TODO Figure this out.
# pylint: disable=import-error
import gym
from gym import spaces


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

    # TODO Remove once self use.
    # pylint: disable=no-self-use
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

        del action

        obs = None
        reward = 0
        done = True
        info = {}
        return obs, reward, done, info

    def reset(self):
        """Resets the game to the starting state.

        TODO more detail about what gets reset.
        """

    def render(self, mode='human'):
        """Will not be used.
        """
