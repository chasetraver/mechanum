import pygame
from random import seed
from random import randint

seed(randint(0, 10))


def coordtogridx(i):
    if 2 < i < 92:
        return 12
    elif 93 < i < 183:
        return 105
    elif 184 < i < 275:
        return 198
    elif 277 < i < 368:
        return 291
    elif 369 < i < 459:
        return 384

def coordtogridy(i):
    if 49 < i < 138:
        return 52
    elif 140 < i < 229:
        return 145
    elif 232 < i < 322:
        return 238
    elif 325 < i < 415:
        return 331
    elif 417 < i < 507:
        return 424


def get_location(x: object, y: object) -> object:
    x_coor = coordtogridx(x)
    y_coor = coordtogridy(y)
    return x_coor, y_coor


    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:  # ESC makes the game quit
                    exit()
def grid():
    grid_image: object = pygame.image.load(
        'Images/gridBackground.png').convert()
    grid_image = pygame.transform.scale(grid_image, (460, 460))
    return grid_image


def rand_location():
    value = randint(0, 4)
    return value


def gridtocoordx(i):
    if i == 0:
        return 12
    elif i == 1:
        return 105
    elif i == 2:
        return 198
    elif i == 3:
        return 291
    else:
        return 384

def gridtocoordy(i):
    if i == 0:
        return 52
    elif i == 1:
        return 145
    elif i == 2:
        return 238
    elif i == 3:
        return 331
    else:
        return 424


def valid_move(clickx, clicky, playerx, playery, goblinx, gobliny, move):
    # i is the number of moves the user is allowed to make
    # x_r, y_r are the coordinates of the robot
    # x_g, y_g are the coordinates of the goblin
    # x and y are the coordinates of the click (pygame.mouse.get_pos())
    # j == False means it is the computer's turn, j == True means it is the player's turn
    x_temp = 0  # The x distance the user is trying to click away from current position
    y_temp = 0  # The y distance the user is trying to click away from current position

    clickx, clicky = get_location(clickx, clicky)
    if clickx == playerx and clicky == playery:  # If trying to move where the robot is
        return False
    elif clickx == goblinx and clicky == gobliny:  # If trying to move where goblin is
        return False
    if True:
        if clickx > playerx:
            x_temp = clickx - playerx
        else:
            x_temp = playerx - clickx
        if clicky > playery:
            y_temp = clicky - playery
        else:
            y_temp = playery - clicky

    #this logic doesnt make sense to me.
    #if x_temp > 0 and y_temp > 0:
        #return False
    if x_temp > move:
        return False
    elif y_temp > move:
        return False
    elif (x_temp + y_temp) > move:
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