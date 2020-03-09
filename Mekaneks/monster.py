import cardlib


class Monster:
    def __init__(self, hp):
        self.hp = hp
        self.isalive = 1

    def damage(self, amount):
        self.hp = self.hp - amount
        if self.hp <= 0:
            self.isalive = 0
            return cardlib.randomcard()
            # todo have player be able to select if they want to add returned card to deck or not.

