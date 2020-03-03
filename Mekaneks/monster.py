import cardlib
import random
import pygame

class Monster:
    def __init__(self, hp):
        self.hp = hp
        self.isalive = 1
        self.sprite = pygame.image.load('/Users/Benny/Desktop/School/Software Engineering/mechanum/Mekaneks/goblinmonster.png')

    def damage(self, amount):
        self.hp = self.hp - amount
        if self.hp <= 0:
            self.isalive = 0

