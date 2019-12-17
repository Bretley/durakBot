import gym
from gym import spaces


class DurakEnv(gym.Env):

    def __init__(self):
        metadata = {'render.modes': ['human']}
        super(DurakEnv, self).__init__()

        # 5 Base actions and 36 Cards
        self.action_space = spaces.Tuple([spaces.Discrete(5), spaces.Discrete(36)])

        # 1 Discrete observation for now just to set it up
        self.observation_space = spaces.Discrete(1)

    def step(self, action):
        obs = None
        reward = 0
        done = True
        info = {}
        return obs, reward, done, info

    def reset(self):
        pass

    def render(self, mode='human'):
        pass
