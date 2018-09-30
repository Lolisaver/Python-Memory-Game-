from random import shuffle

class Deck():
    def __init__(self, shoe_size=1,
                suits=["S","C","H","D"],
                ranks = range(13),
                values = range(13)):
        self.cards = []
        self.suits = suits
        self.ranks = ranks
        self.values = values

        for i in range(shoe_size):
            for suit in suits:
                for rank in ranks:
                    self.cards.append({'suit':suit, 'rank':str(rank+1), 'value':values[rank]+1})

        shuffle(self.cards)

    def __len__(self):
        return len(self.cards)

    def draw(self, amount=1):
        deal = self.cards[-1 : -(amount+1) : -1]
        self.cards = self.cards[: -amount]

        # only return the card and not the list if it's only one
        return deal[0] if amount==1 else deal

    def generator(self):
        while True:
            yield self.cards.pop()

    def reshuffle(self):
        shuffle(self.cards)

    def isEmpty(self):
        return len(self.cards)==0

    def rebuild(self):
        self.__init__(1,self.suits,self.ranks,self.values)

if __name__ == "__main__":
    SK = SquareKing()
    SK.game()