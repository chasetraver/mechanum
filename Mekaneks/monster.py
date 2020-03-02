import cardlib
import random
import pygame

class Monster:
    def __init__(self, hp):
        self.hp = hp
        self.isalive = 1
        self.sprite = pygame.image.load()

    def damage(self, amount):
        self.hp = self.hp - amount
        if self.hp <= 0:
            self.isalive = 0
            r = random.randint(1, 3)
            if r == 3:
                return cardlib.randomcard()
            # todo have player be able to select if they want to add returned card to deck or not.

