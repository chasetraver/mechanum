import cardlib
import random
import pygame

class Monster:
    def __init__(self, hp, xcoord, ycoord):
        self.hp = hp
        self.isalive = 1
        self.xcoord = xcoord
        self.ycoord = ycoord
        self.sprite = pygame.image.load('/home/chase/PycharmProjects/mechanum/Mekaneks/goblinmonster.png')

    def damage(self, amount):
        self.hp = self.hp - amount
        if self.hp <= 0:
            self.isalive = 0

