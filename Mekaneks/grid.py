import pygame
from random import seed
from random import randint

seed(randint(0, 10))


def coordtogrid(i):

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
    x_coor = coordtogrid(x)
    y_coor = coordtogrid(y)
    return x_coor, y_coor


    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:  # ESC makes the game quit
                    exit()
def grid():
    grid_image: object = pygame.image.load(
        'gridBackground.png').convert()
    return grid_image


def rand_location():
    value = randint(0, 4)
    return value


def gridtocoord(i):
    if i == 0:
        return 0
    elif i == 1:
        return 64
    elif i == 2:
        return 128
    elif i == 3:
        return 191
    else:
        return 255


def valid_move(x, y, xr, yr, xg, yg, i, j):
    # i is the number of moves the user is allowed to make
    # x_r, y_r are the coordinates of the robot
    # x_g, y_g are the coordinates of the goblin
    # x and y are the coordinates of the click (pygame.mouse.get_pos())
    # j == False means it is the computer's turn, j == True means it is the player's turn
    x_temp = 0  # The x distance the user is trying to click away from current position
    y_temp = 0  # The y distance the user is trying to click away from current position

    x, y = get_location(x, y)
    if x == xr and y == yr:  # If trying to move where the robot is
        return False
    elif x == xg and y == yg:  # If trying to move where goblin is
        return False
    if j:
        if x > xr:
            x_temp = x - xr
        else:
            x_temp = xr - x
        if y > yr:
            y_temp = y - yr
        else:
            y_temp = yr - y
    else:
        if x > xr:
            x_temp = x - xg
        else:
            x_temp = xg - x
        if y > yg:
            y_temp = y - yg
        else:
            y_temp = yg - y

    if x_temp > 0 and y_temp > 0:
        return False
    elif x_temp > i:
        return False
    elif y_temp > i:
        return False
    elif (x_temp + y_temp) > i:
        return False
    else:
        return True


def in_range(xr, yr, xg, yg, i):
    # i is the range alloted
    x = 0
    y = 0
    if xr > xg:
        x = xr - xg
    else:
        x = xg - xr
    if yr > yg:
        y = yr - yg
    else:
        y = yg - yr

    if x > i and y > i:
        return False
    else:
        return True


def valid_attack(x, y, xr, yr, xg, yg, i, j):
    # x and y are coordinates of the click
    # xr and yr are the coordinates of the robot
    # xg and yg are the coordinates of the goblin
    # i is the range
    # j is True for the player's turn, False for the CPU's turn
    x, y = get_location(x, y)

    if not in_range(xr, yr, xg, yg, i):
        return False

    if j:
        if x == xg and y == yg:
            return True
        else:
            return False
    else:
        if x == xr and y == yr:
            return True
        else:
            return False