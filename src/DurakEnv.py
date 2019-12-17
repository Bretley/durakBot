import gym
from gym import spaces


class DurakEnv(gym.Env):

    def __init__(self):
        super(DurakEnv, self).__init__()

        # 1 Discrete action for now just to set it up
        self.action_space = spaces.Discrete(1)

        # 1 Discrete observation for now just to set it up
        self.observation_space = spaces.Discrete(1)

    def step(self, action):
        pass

    def reset(self):
        pass

    def render(self, mode='human'):
        pass
