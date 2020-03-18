import pygame
import grid
import sys
import deckcardplayerclasses
import cardlib
import monster
import random
import time
import high_scores

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

robot_image = pygame.image.load('Images/Robby.png')
robot_image = pygame.transform.scale(robot_image, (62, 62))
goblin_image = pygame.image.load('Images/goblinmonster.png')
goblin_image = pygame.transform.scale(goblin_image, (62, 62))


def displayplayer(player):
    x = grid.gridtocoord(player.xcoord)
    y = grid.gridtocoord(player.ycoord)
    playersprite = pygame.image.load(player.sprite)
    playersprite = pygame.transform.scale(playersprite, (62, 62))
    screen.blit(playersprite, (x, y))


def displaygoblin(goblinmonster):
    x = grid.gridtocoord(goblinmonster.xcoord)
    y = grid.gridtocoord(goblinmonster.ycoord)
    goblinsprite = pygame.image.load(goblinmonster.sprite)
    goblinsprite = pygame.transform.scale(goblinsprite, (62, 62))
    screen.blit(goblinsprite, (x, y))

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
        # Fill black
        screen.fill((0, 0, 0))
        # button creations
        #text_play = font.render('Mechanum', True, (255, 255, 255))
        #screen.blit(text_play, (200, 100))
    #todo yell at chase to photoshop a background for the menu and the main game. Should feature a stylised 'mechanum' title
        # Rect(left pos, top pos, width, height)
        button_play = pygame.Rect(200, 200, 200, 50)
        button_highscores = pygame.Rect(200, 300, 200, 50)
        button_exit = pygame.Rect(200, 400, 200, 50)
        pygame.draw.rect(screen, (255, 0, 0), button_play)
        pygame.draw.rect(screen, (255, 0, 0), button_highscores)
        pygame.draw.rect(screen, (255, 0, 0), button_exit)
        pygame.draw.rect(screen, (255, 0, 0), button_play)
        # text for buttons
        button_play_msg = "Play"
        button_opt_msg = "High Scores"
        button_quit_msg = "Quit"
        button_play_txt = font.render(button_play_msg, True, (255, 255, 255))
        button_opt_txt = font.render(button_opt_msg, True, (255, 255, 255))
        button_quit_txt = font.render(button_quit_msg, True, (255, 255, 255))
        screen.blit(button_play_txt, (285, 220))
        screen.blit(button_opt_txt, (265, 320))
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
                if button_highscores.collidepoint(mx, my):
                    if click:
                        highscores()
                if button_exit.collidepoint(mx, my):
                    if click:
                        exit()
            # call exit function on Esc key
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit()
        pygame.display.update()
        mainClock.tick(60)


def characterscreen():
    while True:
        screen.fill((0, 0, 0))
        button_char1 = pygame.Rect(200, 200, 200, 50)
        button_char2 = pygame.Rect(200, 300, 200, 50)
        pygame.draw.rect(screen, (255, 0, 0), button_char1)
        pygame.draw.rect(screen, (255, 0, 0), button_char2)
        # text for buttons
        button_char1_msg = "Select 'Robby the Robot'"
        button_char2_msg = "Select 'The Doomcopter'"
        button_char1_txt = font.render(button_char1_msg, True, (255, 255, 255))
        button_char2_txt = font.render(button_char2_msg, True, (255, 255, 255))
        screen.blit(button_char1_txt, (285, 220))
        screen.blit(button_char2_txt, (265, 320))

        for event in pygame.event.get():
            mx, my = pygame.mouse.get_pos()
            click = False
            # event - left mousebutton clicked (button actions)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                click = True
                if button_char1.collidepoint(mx, my):
                    if click:
                        return 1
                if button_char2.collidepoint(mx, my):
                    if click:
                        return 2
            # call exit function on Esc key
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit()
        pygame.display.update()
        mainClock.tick(60)


def playersetup(xplayer, yplayer, playercharacterchoice):
    playerdrawdeck = deckcardplayerclasses.Deck(cardlib.startingcards(playercharacterchoice))
    playerdrawdeck.shuffle()
    playerdiscarddeck = deckcardplayerclasses.Deck([])
    playertrashdeck = deckcardplayerclasses.Deck([])
    player = deckcardplayerclasses.Player(playerdrawdeck, playerdiscarddeck, playertrashdeck, xplayer, yplayer,
                                          playercharacterchoice)
    while len(player.hand) < 5:
        player.draw()
    return player


def possibleattack(player, _monster, attrange):
    for x in range(-attrange, attrange):
        if player.xcoord + x == _monster.xcoord:
            return True
        if player.ycoord + x == _monster.ycoord:
            return True
    return False


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
        elif _monster.ycoord > player.ycoord:
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


def spawngoblin(goblinmonster, player):
    xgoblin = grid.rand_location()
    ygoblin = grid.rand_location()

    while xgoblin == player.xcoord and ygoblin == player.ycoord:
        xgoblin = grid.rand_location()
        ygoblin = grid.rand_location()

    goblinmonster.xcoord = xgoblin
    goblinmonster.ycoord = ygoblin
    goblinmonster.isalive = True
    goblinmonster.hp = goblinmonster.hp + 1

def message_display(text):
    white = (255, 255, 255)
    black = (0, 0, 0)
    font = pygame.font.Font('freesansbold.ttf', 15)
    text = font.render(text, True, white, black)
    textRect = text.get_rect()
    textRect.center = (300, 350)
    screen.blit(text, textRect)


def game():
    characterselect = characterscreen()
    xplayer = grid.rand_location()
    yplayer = grid.rand_location()


    player1 = playersetup(xplayer, yplayer, characterselect)

    goblinmonster = monster.Monster(0, 0, 0)
    spawngoblin(goblinmonster, player1)
    currentmessage = "Defeat the Goblins! Choose a card to get started!"

    emptycard = deckcardplayerclasses.Card("", 0, 0, 0, 0, "")
    playedcard = emptycard
    loot = False
    playerwent = 0
    lootcard = emptycard
    playercleanup = False

    while player1.isalive:

        screen.fill((0, 0, 0))

        card_width = 1771
        card_length = 2633
        card_scale_factor = 0.05

        handsize = len(player1.hand)
        index = None

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

                    if handsize >= 1:
                        if button_card_0.collidepoint(mx, my):
                            if click:
                                index = 0
                    if handsize >= 2:
                        if button_card_1.collidepoint(mx, my):
                            if click:
                                index = 1
                    if handsize >= 3:
                        if button_card_2.collidepoint(mx, my):
                            if click:
                                index = 2
                    if handsize >= 4:
                        if button_card_3.collidepoint(mx, my):
                            if click:
                                index = 3
                    if handsize >= 5:
                        if button_card_4.collidepoint(mx, my):
                            if click:
                                index = 4

        # Print the grid to the screen
        message_display(currentmessage)
        screen.blit(grid.grid(), [0, 0])

        displayplayer(player1)
        displaygoblin(goblinmonster)

        if not index == None:
            playedcard = player1.hand[index]
            if playedcard.move == 99:
                playercleanup = True
            elif playedcard.move != 0:
                currentmessage = "Select the space to move to"
                for event in pygame.event.get():
                    xclick, yclick = pygame.mouse.get_pos()
                    click = False
                    if event.type == pygame.QUIT:
                        exit()
                    if True:
                        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                            click = True
                    if click:
                        if not grid.valid_move(xclick, yclick, player1.xcoord, player1.ycoord, goblinmonster.xcoord,
                                          goblinmonster.ycoord,
                                          playedcard.move, True):
                            currentmessage = ("That is not a valid move, please select a space within %d spaces of Robby" %
                                        playedcard.move)
                        else:
                            xclick = grid.coordtogrid(xclick)
                            yclick = grid.coordtogrid(yclick)
                            player1.xcoord = xclick
                            player1.ycoord = yclick
                            playercleanup = True

            if playedcard.attrange != 0:
                if not possibleattack(player1, goblinmonster, playedcard.attrange):
                    currentmessage = "There is no possible attack target for that card"
                    playercleanup = True

                currentmessage = "Select a space to attack"
                for event in pygame.event.get():
                    xclick, yclick = pygame.mouse.get_pos()
                    click = False
                    if event.type == pygame.QUIT:
                        exit()
                    if True:
                        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                            click = True
                if click:
                    if not grid.valid_attack(xclick, yclick, player1.xcoord, player1.ycoord, goblinmonster.xcoord,
                                            goblinmonster.ycoord,
                                            playedcard.attrange, True):
                        currentmessage = "That is not a valid space to attack, please select a space within %d spaces of Robby" % playedcard.attrange

                    else: goblinmonster.damage(playedcard.damage)
                    if not goblinmonster.isalive:
                        currentmessage = "You attack and kill the monster! You earn 100 points!"
                        player1.score = player1.score + 100
                        spawngoblin(goblinmonster, player1)
                        randnum = random.randint(1, 3)
                        if randnum == 3:
                            loot = True
                            lootcard = cardlib.randomcard()
                            player1.discard(index)
                            playedcard = emptycard
                            index = None


                    else:
                        currentmessage = "You attack the monster. It is weakened, but yet lives."
                        playercleanup = True
            if playedcard.armor != 0:
                currentmessage = "You gain %d armor" % playedcard.armor
                player1.armor = player1.armor + playedcard.armor
                playercleanup = True


            if (len(player1.hand)) < 3:
                while (len(player1.hand)) < 6:
                    player1.draw()
        if loot:
            message_display("The monster has dropped a part! Would you like to add %s to your deck?" %
                            lootcard.name)
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
                loot = False
                playerwent = playerwent + 1
            if button_no.collidepoint(xmouse, ymouse):
                playerchoice = False
                loot = False
                playerwent = playerwent + 1
            if playerchoice:
                player1.addcard(lootcard)

        if playercleanup:
            playercleanup = False
            player1.discard(index)
            playedcard = emptycard
            index = None
            playerwent = playerwent + 1

        if playerwent == 2:
            monsterturn(goblinmonster, player1)
            playerwent = 0

        pygame.display.flip()
        pygame.display.update()
        mainClock.tick(2)


#todo add game over screen and display player1.score

white = (255,255,255)
def text_objects(text, font):
    textSurface = font.render(text, True, white)
    return textSurface, textSurface.get_rect()

def highscore_display(text, i):
    height = window_height/10
    largeText = pygame.font.Font('freesansbold.ttf',30)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((window_width/2),(height+(i*50)))
    screen.blit(TextSurf, TextRect)

    #pygame.display.update()



def read_scores(filename):
    with open(filename) as f:
        return [int(x) for x in f]


def highscores():
    black = (0, 0, 0)
    white = (255, 255, 255)
    red = (255, 0, 0)
    arr = read_scores('highscores.txt')
    running = True
    scoresdisplayed = False
    while running:
        screen.fill(black)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit()

        highscore_display("Top 10 High Scores:", 0)
        for i in range(10):
            temp_string = str(arr[i])
            temp_string = str(i + 1) + ". " + temp_string
            highscore_display(temp_string, i + 1)

        if scoresdisplayed == False:
            pygame.display.flip()
            pygame.display.update()
            displayed = True

        mainClock.tick(60)
def exit():
    pygame.quit()
    sys.exit()


main_menu()
