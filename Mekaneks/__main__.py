import pygame
import grid
import sys
import deckcardplayerclasses
import cardlib
import monster

# initialize game engine and open a window
mainClock = pygame.time.Clock()
pygame.init()
window_width = 600
window_height = 600
# window settings
display_size = (window_width, window_height)
screen = pygame.display.set_mode(display_size)
pygame.display.set_caption('Mechanum')

# main font (currently system default)
font = pygame.font.SysFont(None, 20)
small_button_font = pygame.font.SysFont(None, 12)

click = False

robot_image = pygame.image.load('/home/chase/PycharmProjects/mechanum/Mekaneks/Robby.png')
robot_image = pygame.transform.scale(robot_image, (62, 62))
goblin_image = pygame.image.load('/home/chase/PycharmProjects/mechanum/Mekaneks/goblinmonster.png')
goblin_image = pygame.transform.scale(goblin_image, (62, 62))


def robot(x, y):
    screen.blit(robot_image, (x, y))

def goblin(x, y):
    screen.blit(goblin_image, (x, y))

left = 0
top = 0
width = 0
height = 0


def get_location(x, y):
    left = x
    top = y
    width = x + 62
    height = y + 62


def main_menu():
    while True:
        # button texts
        text_play = font.render('Mechanum', True, (255, 255, 255))
        # screen.blit(text_play, (0,0))
        # Fill black
        screen.fill((0, 0, 0))
        # button creations
        # Rect(left pos, top pos, width, height)
        button_play = pygame.Rect(200, 200, 200, 50)
        button_options = pygame.Rect(200, 300, 200, 50)
        button_exit = pygame.Rect(200, 400, 200, 50)
        pygame.draw.rect(screen, (255, 0, 0), button_play)
        pygame.draw.rect(screen, (255, 0, 0), button_options)
        pygame.draw.rect(screen, (255, 0, 0), button_exit)
        pygame.draw.rect(screen, (255, 0, 0), button_play)
        # text for buttons
        button_play_msg = "Play"
        button_opt_msg = "Options"
        button_quit_msg = "Quit"
        button_play_txt = font.render(button_play_msg, True, (255, 255, 255))
        button_opt_txt = font.render(button_opt_msg, True, (255, 255, 255))
        button_quit_txt = font.render(button_quit_msg, True, (255, 255, 255))
        screen.blit(button_play_txt, (285, 220))
        screen.blit(button_opt_txt, (285, 320))
        screen.blit(button_quit_txt, (285, 420))

        for event in pygame.event.get():
            mx, my = pygame.mouse.get_pos()
            click = False
            if event.type == pygame.QUIT:
                exit()
            # event - left mousebutton clicked (button actions)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                click = True
                if button_play.collidepoint(mx, my):
                    if click:
                        game()
                if button_options.collidepoint(mx, my):
                    if click:
                        options()
                if button_exit.collidepoint(mx, my):
                    if click:
                        exit()
            # call exit function on Esc key
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit()
        pygame.display.update()
        mainClock.tick(60)


def playersetup(xplayer, yplayer):
    playerdrawdeck = deckcardplayerclasses.Deck(cardlib.startingcards())
    playerdrawdeck.shuffle()
    playerdiscarddeck = deckcardplayerclasses.Deck([])
    playertrashdeck = deckcardplayerclasses.Deck([])
    player = deckcardplayerclasses.Player(playerdrawdeck, playerdiscarddeck, playertrashdeck, xplayer, yplayer)
    return player


def playerturn(player):
    turn = 0  # player is able to play 2 cards before monsters act and before they redraw, hence the need for a loop.
    while turn < 2:
        # todo have player able to click card in hand, return index of card in player.hand
        # player.playcard(index)
        # todo if the player kills a monster, call cardlib.randcard and give the player the option to add card to deck
        turn = turn + 1

    if len(player.hand) < 3:
        while player.hand < 5:
            player.draw()


def isadjacent(object1, object2):
    xmod = 1
    while xmod > -2:  # todo change this to a for loop like a sane person (upon research this might be the best way)
        ymod = 1
        while ymod > -2:
            if (object1.xcoord == (object2.xcoord + xmod)) & (object2.ycoord == object2.ycoord):
                return True
            elif (object1.xcoord == object2.xcoord) & (object1.ycoord == (object2.ycoord + ymod)):
                return True
            ymod = ymod - 2
        xmod = xmod - 2
    return False


def monsterturn(_monster, player):
    #checks each space adjacent to monster. If player is there, player is damaged.
    if isadjacent(_monster, player):
        player.damage(1)
    else:
        if _monster.ycoord < player.ycoord:
            _monster.ycoord = _monster.ycoord + 1
        elif monster.ycoord > player.ycoord:
            _monster.ycoord = _monster.ycoord - 1
        elif _monster.ycoord == player.ycoord:
            if _monster.xcoord < player.xcoord:
                _monster.xcoord = _monster.xcoord + 1
            elif _monster.xcoord > player.xcoord:
                _monster.xcoord = _monster.xcoord - 1
            else:
                assert True, "monster/player coord move error. Monsterx: %a, Monstery: %b, Playerx: %c, Playery: %d" % \
                             (_monster.xcoord, _monster.ycoord, player.xcoord, player.ycoord)
        goblin(_monster.xcoord, _monster.ycoord)


def message_display(text):
    white = (255, 255, 255)
    black = (0, 0, 0)
    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render(text, True, white, black)
    textRect = text.get_rect()
    textRect.center = (100, 350)
    screen.blit(text, textRect)


def game():
    xgoblin = 0
    ygoblin = 0
    playerscore = 0
    card_width = 1771
    card_length = 2633
    card_scale_factor = 0.05
    beginning = True            # If it's at the beginning of the game, Robby and Goblin will get randomly assigned spaces

    xrobby = grid.rand_location()
    yrobby = grid.rand_location()
    xrobby = grid.set_coor(xrobby)
    yrobby = grid.set_coor(yrobby)

    player1 = playersetup(xrobby, yrobby)

    while True:

        screen.fill((0, 0, 0))
        button_conv_wheels = pygame.Rect(50, 550, 75, 25)
        button_pointed_stick = pygame.Rect(200, 550, 75, 25)
        button_scrap_armor = pygame.Rect(350, 550, 75, 25)
        button_stick_lobber = pygame.Rect(500, 550, 75, 25)
        pygame.draw.rect(screen, (128, 128, 128), button_conv_wheels)
        pygame.draw.rect(screen, (128, 128, 128), button_pointed_stick)
        pygame.draw.rect(screen, (128, 128, 128), button_scrap_armor)
        pygame.draw.rect(screen, (128, 128, 128), button_stick_lobber)
        button_conv_wheels_msg = "conveyor wheels"
        button_pointed_stick_msg = "pointed stick"
        button_scrap_armor_msg = "scrap armor"
        button_stick_lobber_msg = "stick lobber"
        button_conv_wheels_txt = small_button_font.render(button_conv_wheels_msg, True, (255, 255, 255))
        button_pointed_stick_txt = small_button_font.render(button_pointed_stick_msg, True, (255, 255, 255))
        button_scrap_armor_txt = small_button_font.render(button_scrap_armor_msg, True, (255, 255, 255))
        button_stick_lobber_txt = small_button_font.render(button_stick_lobber_msg, True, (255, 255, 255))
        screen.blit(button_conv_wheels_txt, (55, 557))
        screen.blit(button_pointed_stick_txt, (212, 557))
        screen.blit(button_scrap_armor_txt, (365, 557))
        screen.blit(button_stick_lobber_txt, (517, 557))
        img_conv_wheels = pygame.image.load(
            '/home/chase/PycharmProjects/mechanum/Mekaneks/conveyorWheels.png')
        img_conv_wheels = pygame.transform.scale(img_conv_wheels, (
            int(card_scale_factor * card_width), int(card_scale_factor * card_length)))
        img_pointed_stick = pygame.image.load(
            '/home/chase/PycharmProjects/mechanum/Mekaneks/pointedStick.png')
        img_pointed_stick = pygame.transform.scale(img_pointed_stick, (
            int(card_scale_factor * card_width), int(card_scale_factor * card_length)))
        img_scrap_armor = pygame.image.load(
            '/home/chase/PycharmProjects/mechanum/Mekaneks/scrapArmor.png')
        img_scrap_armor = pygame.transform.scale(img_scrap_armor, (
            int(card_scale_factor * card_width), int(card_scale_factor * card_length)))
        img_stick_lobber = pygame.image.load(
            '/home/chase/PycharmProjects/mechanum/Mekaneks/sticklobber.png')
        img_stick_lobber = pygame.transform.scale(img_stick_lobber, (
            int(card_scale_factor * card_width), int(card_scale_factor * card_length)))
        screen.blit(img_conv_wheels, (45, 415))
        screen.blit(img_pointed_stick, (195, 415))
        screen.blit(img_scrap_armor, (345, 415))
        screen.blit(img_stick_lobber, (495, 415))

        for event in pygame.event.get():
            mx, my = pygame.mouse.get_pos()
            click = False
            if event.type == pygame.QUIT:
                exit()
            if beginning == False:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    click = True
                    if button_conv_wheels.collidepoint(mx, my):
                            if click:

                                for event in pygame.event.get():
                                    message_display('Move 1')
                                    if event.type == pygame.MOUSEBUTTONUP:
                                        x_temp, y_temp = pygame.mouse.get_pos()
                                        if 0 <= x_temp <= 316 and 0 <= y_temp <= 316:
                                            x_temp, y_temp = grid.get_location(x_temp, y_temp)
                                            xrobby = x_temp
                                            yrobby = y_temp



                        #exit()
                    if button_pointed_stick.collidepoint(mx, my):
                        if click:
                            #todo have it wait for another click to get space coordinates...?
                            message_display("Click the space you want to attack")
                            if grid.valid_attack(xcoord,ycoord,player1.xcoord,player1.ycoord,goblinmonster.xcoord,
                                                 goblinmonster.ycoord,1, playerturn):
                                playerscore = playerscore + 100
                                xgoblin = grid.rand_location()
                                ygoblin = grid.rand_location()
                                if player1.xcoord == xgoblin and player1.ycoord == ygoblin:
                                    while xrobby == xgoblin and yrobby == ygoblin:
                                        xgoblin = grid.rand_location()
                                        ygoblin = grid.rand_location()

                                xgoblin = grid.gridtocoord(xgoblin)
                                ygoblin = grid.gridtocoord(ygoblin)

                                goblin(xgoblin, ygoblin)

                                #todo double check this spawns the goblin properly
                    if button_scrap_armor.collidepoint(mx, my):
                        if click:
                            player1.armor = player1.armor + 1
                    if button_stick_lobber.collidepoint(mx, my):
                        if click:
                            if grid.valid_attack(xcoord, ycoord, player1.xcoord, player1.ycoord, goblinmonster.xcoord,
                                                 goblinmonster.ycoord, 2, playerturn):
                                playerscore = playerscore + 100
                                xgoblin = grid.rand_location()
                                ygoblin = grid.rand_location()
                                if player1.xcoord == xgoblin and player1.ycoord == ygoblin:
                                    while xrobby == xgoblin and yrobby == ygoblin:
                                        xgoblin = grid.rand_location()
                                        ygoblin = grid.rand_location()

                                xgoblin = grid.set_coor(xgoblin)
                                ygoblin = grid.set_coor(ygoblin)

                                goblin(xgoblin, ygoblin)
                                newgoblin = monster.Monster(1, xgoblin, ygoblin)


            elif beginning == True:

                xgoblin = grid.rand_location()
                ygoblin = grid.rand_location()
                if xrobby == xgoblin and yrobby == ygoblin:
                    while xrobby == xgoblin and yrobby == ygoblin:
                        xgoblin = grid.rand_location()
                        ygoblin = grid.rand_location()

                xgoblin = grid.set_coor(xgoblin)
                ygoblin = grid.set_coor(ygoblin)

                beginning = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # ESC makes the game quit
                    exit()
        # Print the grid to the screen

        screen.blit(grid.grid(), [0, 0])
        robot(xrobby, yrobby)
        goblin(xgoblin, ygoblin)
        goblinmonster = monster.Monster(1, xgoblin, ygoblin)

        pygame.display.flip()
        pygame.display.update()
        mainClock.tick(60)

        while player1.isalive:
            playerturn(player1)
            monsterturn(goblinmonster, player1)


def options():
    x = 0
    y = 0
    running = True
    while running:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit()
        # Print the grid to the screen
        screen.blit(grid.grid(), [0, 0])
        robot(x, y)
        pygame.display.flip()
        pygame.display.update()
        mainClock.tick(60)


def exit():
    pygame.quit()
    sys.exit()


main_menu()
