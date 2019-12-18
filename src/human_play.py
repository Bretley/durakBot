from durak_env import DurakEnv, OPTIONS_DICT, CARD_TO_OBS


class HumanInterface:
    def __init__(self):
        self.hand = []
        self.table = []
        self.outs = []
        self.dank = None

    def parse_obs(self, obs):
        self.hand = []
        self.table = []
        self.outs = []
        self.table = []
        for index, location in enumerate(obs[0:-1]):
            if location == 1:
                self.table.append(OPTIONS_DICT[index])
            elif location == 2:
                self.hand.append(OPTIONS_DICT[index])
            elif location == 3:
                self.outs.append(OPTIONS_DICT[index])
            elif location == 4:
                self.dank = OPTIONS_DICT[index].suit

        if obs[-1] == 0:
            self.state = 'defending'
        elif obs[-1] == 1:
            self.state = "attacking"
        else:
            self.state = 'shedding'
        print(obs)

    def __str__(self):

        ret = 'You are currently ' + self.state + '\n'
        ret += ('Table: ' + ', '.join([str(x) for x in self.table])) + '\n'
        ret += 'Dank: ' + self.dank + '\n'
        ret += ('Hand: ' + ', '.join([str(i) + ': ' + str(x) for i, x in enumerate(self.hand)])) + '\n'
        ret += 'Out: ' + ', '.join([str(x) for i, x in enumerate(self.outs)]) + '\n'
        return ret

    def get_play(self):
        move = input('Move ->  ')
        if move == 'd':
            return 36
            # done
            pass
        elif move == 't':
            return 37
            # take
            pass
        else:
            try:
                card_index = int(move)
                if 0 <= card_index < len(self.hand):
                    g = CARD_TO_OBS[self.hand[card_index]]
                    print('Pl')
                    print('playing ' + str(OPTIONS_DICT[g]))
                    return g
            except:
                print('not a valid input')
                return self.get_play()


def main():
    h = HumanInterface()
    env = DurakEnv()
    env.reset()
    o, r, d, i = env.step(30)
    print(o)
    h.parse_obs(o)
    while not d:
        print(h)
        o, r, d, i = env.step(h.get_play())
        print(o)
        h.parse_obs(o)
        print('\t'*10 + str((d)))
        print('\t'*10 + 'reward: ' + str((r)))


if __name__ == '__main__':
    main()
