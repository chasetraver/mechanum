import pygame
import grid
import sys
import deckcardplayerclasses
import cardlib
import monster
import random

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

robot_image = pygame.image.load('Robby.png')
robot_image = pygame.transform.scale(robot_image, (62, 62))
goblin_image = pygame.image.load('goblinmonster.png')
goblin_image = pygame.transform.scale(goblin_image, (62, 62))


def robot(x, y):
    x = grid.gridtocoord(x)
    y = grid.gridtocoord(y)
    screen.blit(robot_image, (x, y))


def goblin(x, y):
    x = grid.gridtocoord(x)
    y = grid.gridtocoord(y)
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
    while len(player.hand) < 5:
        player.draw()
    return player


def possibleattack(player, _monster, attrange):
    for x in range(-attrange, attrange):
        if player.xcoord + x == _monster.xcoord:
            return True
        if player.ycoord + x == monster.ycoord:
            return True
    return False


def waitforclick():
    while not pygame.MOUSEBUTTONDOWN:
        pass
    return pygame.mouse.get_pos()


def playerturn(player, _monster, index):
    turn = 0  # player is able to play 2 cards before monsters act and before they redraw, hence the need for a loop.
    while turn < 2:
        # todo have player able to click card in hand, return index of card in player.hand

        assert not index == 6, "index error"
        playedcard = player.hand[index]
        if playedcard.move != 0:
            message_display("Select the space to move to")
            xclick, yclick = waitforclick()
            while not grid.valid_move(xclick, yclick, player.xcoord, player.ycoord, _monster.xcoord, _monster.ycoord,
                                playedcard.move, True):
                message_display("That is not a valid move, please select a space within %d spaces of Robby" %
                                playedcard.move)
            xclick = grid.coordtogrid(xclick)
            yclick = grid.coordtogrid(yclick)
            player.xcoord = xclick
            player.ycoord = yclick
        if playedcard.attrange != 0:
            if not possibleattack(player, _monster, playedcard.attrange):
                message_display("There is no possible attack target for that card")
                player.discard(index)
                return
            message_display("Select a space to attack")
            xclick, yclick = waitforclick()

            while not grid.valid_attack(xclick, yclick, player.xcoord, player.ycoord, _monster.xcoord, _monster.ycoord,
                                     playedcard.attrange, True):
                message_display("That is not a valid space to attack, please select a space within %d spaces of Robby" %
                                playedcard.attrange)
            _monster.damage(playedcard.damage)
            if not _monster.isalive:
                message_display("You attack and kill the monster! You earn 100 points!")
                player.score = player.score + 100
                randnum = random.randint(1, 3)
                if randnum == 3:
                    lootcard = cardlib.randomcard()
                    message_display("The monster has dropped a part! Would you like to add %s to your deck?" %
                                    lootcard.name)
                    validresponse = False
                    while not validresponse:
                        while not pygame.MOUSEBUTTONDOWN:
                            card_width = 1771
                            card_length = 2633
                            card_scale_factor = 0.05

                            img_lootcard = pygame.transform.scale(lootcard.image, (
                                int(card_scale_factor * card_width), int(card_scale_factor * card_length)))
                            screen.blit(img_lootcard, 325, 200)

                            button_yes = pygame.Rect(200, 200, 200, 50)
                            pygame.draw.rect(screen, (255, 0, 0), button_yes)
                            button_yes_msg = "YES"
                            button_yes_txt = font.render(button_yes_msg, True, (255, 255, 255))
                            screen.blit(button_yes_txt, (285, 220))
                            button_no = pygame.Rect(200, 300, 200, 50)
                            pygame.draw.rect(screen, (255, 0, 0), button_no)
                            button_no_msg = "NO"
                            button_no_txt = font.render(button_no_msg, True, (255, 255, 255))
                            screen.blit(button_no_txt, (285, 320))
                            pygame.display.update()
                        xmouse, ymouse = pygame.mouse.get_pos()
                        if button_yes.collidepoint(xmouse, ymouse):
                            playerchoice = True
                            validresponse = True
                        if button_no.collidepoint(xmouse, ymouse):
                            playerchoice = False
                            validresponse = True
                    if playerchoice:
                        player.addcard(lootcard)

            else:
                message_display("You attack the monster. It is weakened, but yet lives.")
        if playedcard.armor != 0:
            message_display("You gain %d armor" % playedcard.armor)
            player.armor = player.armor + playedcard.armor

        player.discard(index)
        turn = turn + 1

    if len(player.hand) < 3:
        while player.hand < 5:
            player.draw()


def isadjacent(object1, object2):
   #loops through all orthagonally adjacent squares of an object2 to determine if object 1 is adjacent
    xmod = 1
    while xmod > -2:
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
    #checks each space adjacent to monster. If player is there, player is damaged, otherwise the monster moves closer.
    if isadjacent(_monster, player):
        if player.armor > 0:
            message_display("The monster attacked you, but your armor protected you!")
            player.damage(1)
        else:
            lostcard = player.damage(1)
            if player.isalive:
                message_display("The monster attacked you and broke your %s!" % lostcard.name)

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
                # assert True, "monster/player coord move error. Monsterx: %a, Monstery: %b, Playerx: %c, Playery: %d" % \
                             # (_monster.xcoord, _monster.ycoord, player.xcoord, player.ycoord)
                pass

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

    xrobby = grid.rand_location()
    yrobby = grid.rand_location()

    xgoblin = grid.rand_location()
    ygoblin = grid.rand_location()
    player1 = playersetup(xrobby, yrobby)

    if xrobby == xgoblin and yrobby == ygoblin:
        while xrobby == xgoblin and yrobby == ygoblin:
            xgoblin = grid.rand_location()
            ygoblin = grid.rand_location()

    goblinmonster = monster.Monster(1, xgoblin, ygoblin)
    currentmessage = ""
    while player1.isalive:

        screen.fill((0, 0, 0))

        card_width = 1771
        card_length = 2633
        card_scale_factor = 0.05

        handsize = len(player1.hand)
        assert handsize <= 5
        index = 6

        if handsize >= 1:
            button_card_0 = pygame.Rect(45, 550, 90, 25)
            pygame.draw.rect(screen, (128, 128, 128), button_card_0)
            button_0_msg = "Play %s" % player1.hand[0].name
            button_0_txt = small_button_font.render(button_0_msg, True, (255, 255, 255))
            img_0 = pygame.image.load(player1.hand[0].image)
            img_0 = pygame.transform.scale(img_0, (
            int(card_scale_factor * card_width), int(card_scale_factor * card_length)))
            screen.blit(img_0, (45, 415))
            screen.blit(button_0_txt, (50, 557))

        if handsize >= 2:
            button_card_1 = pygame.Rect(195, 550, 90, 25)
            pygame.draw.rect(screen, (128, 128, 128), button_card_1)
            button_1_msg = "Play %s" % player1.hand[1].name
            button_1_txt = small_button_font.render(button_1_msg, True, (255, 255, 255))
            screen.blit(button_1_txt, (200, 557))
            img_1 = pygame.image.load(player1.hand[1].image)
            img_1 = pygame.transform.scale(img_1, (
                int(card_scale_factor * card_width), int(card_scale_factor * card_length)))
            screen.blit(img_1, (195, 415))

        if handsize >= 3:
            button_card_2 = pygame.Rect(345, 550, 90, 25)
            pygame.draw.rect(screen, (128, 128, 128), button_card_2)
            button_2_msg = "Play %s" % player1.hand[2].name
            button_2_txt = small_button_font.render(button_2_msg, True, (255, 255, 255))
            screen.blit(button_2_txt, (350, 557))
            img_2 = pygame.image.load(player1.hand[2].image)
            img_2 = pygame.transform.scale(img_2, (
                int(card_scale_factor * card_width), int(card_scale_factor * card_length)))
            screen.blit(img_2, (345, 415))

        if handsize >= 4:
            button_card_3 = pygame.Rect(495, 550, 90, 25)
            pygame.draw.rect(screen, (128, 128, 128), button_card_3)
            button_3_msg = "Play %s" % player1.hand[3].name
            button_3_txt = small_button_font.render(button_3_msg, True, (255, 255, 255))
            screen.blit(button_3_txt, (500, 557))
            img_3 = pygame.image.load(player1.hand[3].image)
            img_3 = pygame.transform.scale(img_3, (
                int(card_scale_factor * card_width), int(card_scale_factor * card_length)))
            screen.blit(img_3, (495, 415))

        if handsize >= 5:
            button_card_4 = pygame.Rect(420, 340, 90, 25)
            pygame.draw.rect(screen, (128, 128, 128), button_card_4)
            button_4_msg = "Play %s" % player1.hand[4].name
            button_4_txt = small_button_font.render(button_4_msg, True, (255, 255, 255))
            screen.blit(button_4_txt, (425,345))
            img_4 = pygame.image.load(player1.hand[4].image)
            img_4 = pygame.transform.scale(img_4, (
                int(card_scale_factor * card_width), int(card_scale_factor * card_length)))
            screen.blit(img_4, (420, 200))

        for event in pygame.event.get():
            mx, my = pygame.mouse.get_pos()
            click = False
            if event.type == pygame.QUIT:
                exit()
            if True:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    click = True
                    if button_card_0.collidepoint(mx, my):
                        if click:
                            index = 0
                    if button_card_1.collidepoint(mx, my):
                        if click:
                            index = 1
                    if button_card_2.collidepoint(mx, my):
                        if click:
                            index = 2
                    if button_card_3.collidepoint(mx, my):
                        if click:
                            index = 3
                    if button_card_4.collidepoint(mx, my):
                        if click:
                            index = 4

        # Print the grid to the screen
        message_display(currentmessage)
        screen.blit(grid.grid(), [0, 0])
        robot(xrobby, yrobby)
        goblin(xgoblin, ygoblin)


        pygame.display.flip()
        pygame.display.update()
        mainClock.tick(60)

        playerwent = False
        if not index == 6:
            playerturn(player1, goblinmonster, index)
            playerwent = True
        if playerwent == True:
            monsterturn(goblinmonster, player1)
#todo add game over screen and display player1.score

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
