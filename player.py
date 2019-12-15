class Player:
    def __init__(self, num):
        self.hand = []
        self.num = num

    def take(self, cards):
        for card in cards:
            if card is not None:
                self.hand.append(card)

    def __str__(self):
        ret = "==" + str(self.num) + "==\n"
        ret += "hand:\n"
        for card in self.hand:
            ret += str(card) + '\n'
        return ret
