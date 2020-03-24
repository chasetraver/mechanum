import cardlib
import random
import pygame


class Monster:
    def __init__(self, maxhp, xcoord, ycoord):
        self.maxhp = maxhp
        self.hp = self.maxhp
        self.isalive = 1
        self.xcoord = xcoord
        self.attackpower = 1
        self.ycoord = ycoord
        self.sprite = 'Images/goblinmonster.png'

    def damage(self, amount):
        self.hp = self.hp - amount
        if self.hp <= 0:
            self.isalive = 0

