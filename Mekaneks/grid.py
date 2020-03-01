import pygame


def xy_location(i):
    x = 0

    if 0 < i < 63:
        x = 0
    elif 64 < i < 127:
        x = 64
    elif 128 < i < 190:
        x = 128
    elif 191 < i < 255:
        x = 191
    elif 255 < i < 316:
        x = 255
    return x


def get_location(x: object, y: object) -> object:
    x_coor = xy_location(x)
    y_coor = xy_location(y)
    return x_coor, y_coor


def grid():
    grid_image: object = pygame.image.load(
        '/Users/Benny/Desktop/School/Software Engineering/mechanum/Mekaneks/gridBackground.png').convert()
    return grid_image
