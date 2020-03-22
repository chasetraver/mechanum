from typing import Union

import pygame
from pygame.font import FontType
from pygame.ftfont import Font


def small_button_font():
    small_button: object = pygame.font.Font("Video Game Font.ttf", 8)
    return small_button


def play_font():
    play: object = pygame.font.Font("pixel_font.TTF", 60)
    return play


def highscore_font():
    highscore: Union[Font, FontType] = pygame.font.Font("pixel_font.TTF", 50)
    return highscore


def quit_font():
    quit = pygame.font.Font("pixel_font.TTF", 60)
    return quit


def player_select_font():
    player_select = pygame.font.Font("pixel_font.TTF", 40)
    return player_select


def play_as_font():
    play_as = pygame.font.Font("pixel_font.TTF", 60)
    return play_as


def back_font():
    back = pygame.font.Font("Video Game Font.ttf", 30)
    return back


def score_font():
    score = pygame.font.Font("pixel_font.TTF", 35)
    return score

def armor_font():
    armor = pygame.font.Font("Video Game Font.ttf", 40)
    return armor

def armor_small_font():
    armor_small = pygame.font.Font("Video Game Font.ttf", 25)
    return armor_small

def coin_font():
    coin = pygame.font.Font("Video Game Font.ttf", 40)
    return coin

def message_display_font():
    message = pygame.font.Font("Video Game Font.ttf", 11)
    return message
