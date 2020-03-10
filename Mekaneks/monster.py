import cardlib
import random
import pygame

class Monster:
    def __init__(self, hp, xcoord, ycoord):
        self.hp = hp
        self.isalive = 1
        self.xcoord = xcoord
        self.ycoord = ycoord
<<<<<<< HEAD
        self.sprite = pygame.image.load('Images/goblinmonster.png')
=======
        self.sprite = ('/home/chase/PycharmProjects/mechanum/Mekaneks/goblinmonster.png')
>>>>>>> 48a2f1974b2b20ac62f23d9b4ba5e46dd518325e

    def damage(self, amount):
        self.hp = self.hp - amount
        if self.hp <= 0:
            self.isalive = 0

