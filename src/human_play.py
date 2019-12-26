"""A module used to simulate Model interaction as a human.
"""

from durak_env import CARD_TO_OBS, DurakEnv, OPTIONS_DICT


class HumanInterface:
    """A class used to represent a human interactable way version of the
    information the model receives.

        Attributes:
            hand: The cards in the player's hand.
            table: The cards on the table.
            outs: The cards in the out pile.
            dank: The dank card.
            def_card: The card to defend against.
            state: The state of gameplay.
        """

    def __init__(self):
        """Inits HumanInterface.
        """
        self.hand = []
        self.table = []
        self.outs = []
        self.dank = None
        self.def_card = None
        self.state = None

    def __str__(self):
        ret = 'You are currently ' + self.state + '\n'
        ret += ('Table: ' + ', '.join([str(x) for x in self.table])) + '\n'
        ret += 'Dank: ' + self.dank + '\n'
        ret += ('Hand: ' + ', '.join([str(i) + ': ' + str(x) for i, x in enumerate(self.hand)])) + '\n'
        ret += 'Out: ' + ', '.join([str(x) for i, x in enumerate(self.outs)]) + '\n'
        ret += 'Last defense card: ' + str(self.def_card) + '\n'
        return ret

    def parse_obs(self, obs):
        """Parses the observations into a human readable structure.

        Args:
            obs: The observations to parse.
        """
        self.hand = []
        self.table = []
        self.outs = []
        self.table = []
        self.def_card = None
        for index, location in enumerate(obs[0:-2]):
            if location == 1:
                self.table.append(OPTIONS_DICT[index])
            elif location == 2:
                self.hand.append(OPTIONS_DICT[index])
            elif location == 3:
                self.outs.append(OPTIONS_DICT[index])
            elif location == 4:
                self.dank = OPTIONS_DICT[index].suit

        if obs[-2] == 0:
            self.state = 'defending'
            self.def_card = OPTIONS_DICT[obs[-1]]
        elif obs[-2] == 1:
            self.state = "attacking"
        else:
            self.state = 'shedding'
        print(obs)

    def get_play(self):
        """Gets the input from the human to decide what to play.

        Returns:
            A number representing an action in the action space.
        """
        move = input('Move ->  ')
        if move == 'd':
            return 36

        if move == 't':
            return 37

        try:
            card_index = int(move)
            if 0 <= card_index < len(self.hand):
                card = CARD_TO_OBS[self.hand[card_index]]
                print('Pl')
                print('playing ' + str(OPTIONS_DICT[card]))
                return card
            print('not a valid input')
            return self.get_play()
        except IndexError:
            print('not a valid input')
            return self.get_play()


def main():
    """The main function that runs.
    """

    human_inter = HumanInterface()
    env = DurakEnv()
    env.reset()
    obs, reward, done, info = env.step(31)
    print(obs)
    human_inter.parse_obs(obs)
    while not done:
        print(human_inter)
        obs, reward, done, info = env.step(human_inter.get_play())
        print(obs)
        human_inter.parse_obs(obs)
        print('\t' * 10 + str(done))
        print('\t' * 10 + 'reward: ' + str(reward))
    del info


if __name__ == '__main__':
    main()
