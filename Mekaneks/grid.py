import pygame


def x_location(i):
    x = 0

    if 0 < i < 62:
        x = 0
    elif 62 < i < 124:
        x = 62
    elif 124 < i < 186:
        x = 124
    elif 186 < i < 248:
        x = 186
    elif 248 < i < 310:
        x = 248

    return x

def y_location(i):
    x = 0

    if 0 < i < 62:
        x = 0
    elif 62 < i < 124:
        x = 62
    elif 124 < i < 186:
        x = 124
    elif 186 < i < 248:
        x = 186
    elif 248 < i < 310:
        x = 248

    return x


def get_location(x, y):
    x_coor = xy_location(x)
    y_coor = xy_location(y)
    return x_coor, y_coor


def grid():
    grid_image: object = pygame.image.load(
        '/Users/Benny/Desktop/School/Software Engineering/mechanum/Mekaneks/gridBackground.png').convert()
    return grid_image
