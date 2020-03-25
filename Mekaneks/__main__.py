from os import path

import pygame
import grid
import sys
import deckcardplayerclasses
import cardlib
import monster
import random
import time
import fonts
import messages
import high_scores

# initialize game engine and open a window
mainClock = pygame.time.Clock()
pygame.init()
window_width = 1200
window_height = 750
# window settings
display_size = (window_width, window_height)
screen = pygame.display.set_mode(display_size)
pygame.display.set_caption('Mechanum')

# main font (currently system default)


# sounds
pygame.mixer.pre_init(44100, 16, 2, 4096)  # frequency, size, channels, buffersize
pygame.mixer.init()
sound_dir = path.join(path.dirname(__file__), 'sounds')
MenuMusic = pygame.mixer.music.load(path.join(sound_dir, 'menu_music.wav'))

click = False

# todo check, are these being used?
left = 0
top = 0
width = 0
height = 0

# constant globals for universal card size
card_width = 1771
card_length = 2633
card_scale_factor = 0.08


def get_location(x, y):
    left = x
    top = y
    width = x + 62
    height = y + 62


mess_ = messages.Messages()

def display_score(score):
    button_play_msg = "Score: " + str(score)
    button_play_txt = fonts.score_font().render(button_play_msg, True, (255, 255, 255))
    screen.blit(button_play_txt, (150, 6))


def display_armor(armor):
    armor_image: object = pygame.image.load(
        'Images/armor.png')
    armor_image = pygame.transform.scale(armor_image, (400, 400))
    screen.blit(armor_image, [395, 100])
    black_background = pygame.Rect(543, 251, 100, 40)
    pygame.draw.rect(screen, (0, 0, 0), black_background)

    armor_msg = str(armor)
    armor_txt = fonts.armor_small_font().render(armor_msg, True, (255, 255, 255))
    arm_txt2 = fonts.armor_font().render("Armor", True, (255, 255, 255))
    screen.blit(armor_txt, (573, 255))
    screen.blit(arm_txt2, (523, 145))


def display_gold(gold):
    gold_image: object = pygame.image.load('Images/coins.png')
    gold_image = pygame.transform.scale(gold_image, (60, 60))
    screen.blit(gold_image, [480, 10])
    gold_msg = str(gold)
    gold_txt = fonts.coin_font().render(gold_msg, True, (255, 255, 255))
    screen.blit(gold_txt, (544, 24))


def display_draw_deck(deck_length):
    cardback_image: object = pygame.image.load('Images/cardback.png')
    cardback_image = pygame.transform.scale(cardback_image, (230, 345))
    screen.blit(cardback_image, [720, 70])
    black_background = pygame.Rect(782, 220, 110, 40)
    pygame.draw.rect(screen, (0, 0, 0), black_background)

    deck_msg = str(deck_length)
    deck_txt = fonts.display_deck_font().render(deck_msg, True, (255, 255, 255))
    screen.blit(deck_txt, (825, 226))
    draw_deck_txt = fonts.display_title_font().render("Draw Deck", True, (255, 255, 255))
    screen.blit(draw_deck_txt, (730, 40))

def display_discard_deck(deck_length):
    cardback_image: object = pygame.image.load('Images/cardback_red.png')
    cardback_image = pygame.transform.scale(cardback_image, (230, 345))
    screen.blit(cardback_image, [965, 70])
    black_background = pygame.Rect(1026, 220, 110, 40)
    pygame.draw.rect(screen, (0, 0, 0), black_background)

    deck_msg = str(deck_length)
    deck_txt = fonts.display_deck_font().render(deck_msg, True, (255, 255, 255))
    screen.blit(deck_txt, (1068, 226))
    draw_deck_txt = fonts.discard_deck_font().render("Discard Deck", True, (255, 255, 255))
    screen.blit(draw_deck_txt, (970, 40))


def main_menu():
    pygame.mixer.music.play(-1)
    while True:
        # button texts
        # Fill black
        screen.fill((0, 0, 0))
        # button creations
        # text_play = font.render('Mechanum', True, (255, 255, 255))
        # screen.blit(text_play, (200, 100))
        # todo yell at chase to photoshop a background for the menu and the main game. Should feature a stylised 'mechanum' title
        # Rect(left pos, top pos, width, height)
        button_play = pygame.Rect(450, 150, 300, 100)
        button_highscores = pygame.Rect(450, 350, 300, 100)
        button_exit = pygame.Rect(450, 550, 300, 100)
        pygame.draw.rect(screen, (255, 0, 0), button_play)
        pygame.draw.rect(screen, (255, 0, 0), button_highscores)
        pygame.draw.rect(screen, (255, 0, 0), button_exit)
        pygame.draw.rect(screen, (255, 0, 0), button_play)
        # text for buttons
        button_play_msg = "PLAY"
        button_opt_msg = "Highscores"
        button_quit_msg = "Quit"
        button_play_txt = fonts.play_font().render(button_play_msg, True, (255, 255, 255))
        button_opt_txt = fonts.highscore_font().render(button_opt_msg, True, (255, 255, 255))
        button_quit_txt = fonts.quit_font().render(button_quit_msg, True, (255, 255, 255))
        screen.blit(button_play_txt, (537, 170))
        screen.blit(button_opt_txt, (465, 372))
        screen.blit(button_quit_txt, (537, 570))

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
        button_char1 = pygame.Rect(400, 200, 400, 100)
        button_char2 = pygame.Rect(400, 400, 400, 100)
        pygame.draw.rect(screen, (255, 0, 0), button_char1)
        pygame.draw.rect(screen, (255, 0, 0), button_char2)

        robby_disp = pygame.image.load("Images/Robby.png")
        robby_disp = pygame.transform.scale(robby_disp, (210, 270))
        screen.blit(robby_disp, (150, 40))

        doom_disp = pygame.image.load("Images/doomcopter.png")
        doom_disp = pygame.transform.scale(doom_disp, (210, 270))
        screen.blit(doom_disp, (840, 387))
        # text for buttons
        play_as_msg = "PLAY AS:"
        button_char1_msg = "Robby the Robot"
        button_char2_msg = "The Doomcopter"
        button_char1_txt = fonts.player_select_font().render(button_char1_msg, True, (255, 255, 255))
        button_char2_txt = fonts.player_select_font().render(button_char2_msg, True, (255, 255, 255))
        play_as_msg_txt = fonts.player_select_font().render(play_as_msg, True, (255, 255, 255))
        screen.blit(play_as_msg_txt, (490, 100))
        screen.blit(button_char1_txt, (430, 230))
        screen.blit(button_char2_txt, (434, 430))

        for event in pygame.event.get():
            mx, my = pygame.mouse.get_pos()
            click = False
            if event.type == pygame.QUIT:
                exit()
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


def displayplayer(player):
    x = grid.gridtocoordx(player.xcoord)
    y = grid.gridtocoordy(player.ycoord)
    playersprite = pygame.image.load(player.sprite)
    playersprite = pygame.transform.scale(playersprite, (67, 80))
    screen.blit(playersprite, (x, y))


def displaygoblin(goblinmonster):
    x = grid.gridtocoordx(goblinmonster.xcoord)
    y = grid.gridtocoordy(goblinmonster.ycoord)
    goblinsprite = pygame.image.load(goblinmonster.sprite)
    goblinsprite = pygame.transform.scale(goblinsprite, (67, 80))
    screen.blit(goblinsprite, (x, y))


def displaycards(player):
    handsize = len(player.hand)
    if handsize >= 1:
        button_card_0 = pygame.Rect(0, 721, 141, 25)
        pygame.draw.rect(screen, (128, 128, 128), button_card_0)
        button_0_msg = "Play %s" % player.hand[0].name
        button_0_txt = fonts.small_button_font().render(button_0_msg, True, (255, 255, 255))
        img_0 = pygame.image.load(player.hand[0].image)
        img_0 = pygame.transform.scale(img_0, (
            int(card_scale_factor * card_width), int(card_scale_factor * card_length)))
        screen.blit(img_0, (0, 508))
        screen.blit(button_0_txt, (2, 730))

    if handsize >= 2:
        button_card_1 = pygame.Rect(150, 721, 141, 25)
        pygame.draw.rect(screen, (128, 128, 128), button_card_1)
        button_1_msg = "Play %s" % player.hand[1].name
        button_1_txt = fonts.small_button_font().render(button_1_msg, True, (255, 255, 255))
        screen.blit(button_1_txt, (152, 730))
        img_1 = pygame.image.load(player.hand[1].image)
        img_1 = pygame.transform.scale(img_1, (
            int(card_scale_factor * card_width), int(card_scale_factor * card_length)))
        screen.blit(img_1, (150, 508))

    if handsize >= 3:
        button_card_2 = pygame.Rect(300, 721, 141, 25)
        pygame.draw.rect(screen, (128, 128, 128), button_card_2)
        button_2_msg = "Play %s" % player.hand[2].name
        button_2_txt = fonts.small_button_font().render(button_2_msg, True, (255, 255, 255))
        screen.blit(button_2_txt, (302, 730))
        img_2 = pygame.image.load(player.hand[2].image)
        img_2 = pygame.transform.scale(img_2, (
            int(card_scale_factor * card_width), int(card_scale_factor * card_length)))
        screen.blit(img_2, (300, 508))

    if handsize >= 4:
        button_card_3 = pygame.Rect(450, 721, 141, 25)
        pygame.draw.rect(screen, (128, 128, 128), button_card_3)
        button_3_msg = "Play %s" % player.hand[3].name
        button_3_txt = fonts.small_button_font().render(button_3_msg, True, (255, 255, 255))
        screen.blit(button_3_txt, (452, 730))
        img_3 = pygame.image.load(player.hand[3].image)
        img_3 = pygame.transform.scale(img_3, (
            int(card_scale_factor * card_width), int(card_scale_factor * card_length)))
        screen.blit(img_3, (450, 508))

    if handsize >= 5:
        button_card_4 = pygame.Rect(600, 721, 141, 25)
        pygame.draw.rect(screen, (128, 128, 128), button_card_4)
        button_4_msg = "Play %s" % player.hand[4].name
        button_4_txt = fonts.small_button_font().render(button_4_msg, True, (255, 255, 255))
        screen.blit(button_4_txt, (602, 730))
        img_4 = pygame.image.load(player.hand[4].image)
        img_4 = pygame.transform.scale(img_4, (
            int(card_scale_factor * card_width), int(card_scale_factor * card_length)))
        screen.blit(img_4, (600, 508))


def choosecards(player, goblin):
    handsize = len(player.hand)
    currentmessage = "Choose a card to play this turn."
    while True:
        if handsize >= 1:
            button_card_0 = pygame.Rect(0, 700, 141, 40)
            pygame.draw.rect(screen, (128, 128, 128), button_card_0)
            button_0_msg = "Play %s" % player.hand[0].name
            button_0_txt = fonts.small_button_font().render(button_0_msg, True, (255, 255, 255))
            img_0 = pygame.image.load(player.hand[0].image)
            img_0 = pygame.transform.scale(img_0, (
                int(card_scale_factor * card_width), int(card_scale_factor * card_length)))
            screen.blit(img_0, (0, 485))
            screen.blit(button_0_txt, (8, 715))

        if handsize >= 2:
            button_card_1 = pygame.Rect(150, 700, 141, 40)
            pygame.draw.rect(screen, (128, 128, 128), button_card_1)
            button_1_msg = "Play %s" % player.hand[1].name
            button_1_txt = fonts.small_button_font().render(button_1_msg, True, (255, 255, 255))
            screen.blit(button_1_txt, (156, 715))
            img_1 = pygame.image.load(player.hand[1].image)
            img_1 = pygame.transform.scale(img_1, (
                int(card_scale_factor * card_width), int(card_scale_factor * card_length)))
            screen.blit(img_1, (150, 485))

        if handsize >= 3:
            button_card_2 = pygame.Rect(300, 700, 141, 40)
            pygame.draw.rect(screen, (128, 128, 128), button_card_2)
            button_2_msg = "Play %s" % player.hand[2].name
            button_2_txt = fonts.small_button_font().render(button_2_msg, True, (255, 255, 255))
            screen.blit(button_2_txt, (304, 715))
            img_2 = pygame.image.load(player.hand[2].image)
            img_2 = pygame.transform.scale(img_2, (
                int(card_scale_factor * card_width), int(card_scale_factor * card_length)))
            screen.blit(img_2, (300, 485))

        if handsize >= 4:
            button_card_3 = pygame.Rect(450, 700, 141, 40)
            pygame.draw.rect(screen, (128, 128, 128), button_card_3)
            button_3_msg = "Play %s" % player.hand[3].name
            button_3_txt = fonts.small_button_font().render(button_3_msg, True, (255, 255, 255))
            screen.blit(button_3_txt, (455, 715))
            img_3 = pygame.image.load(player.hand[3].image)
            img_3 = pygame.transform.scale(img_3, (
                int(card_scale_factor * card_width), int(card_scale_factor * card_length)))
            screen.blit(img_3, (450, 485))

        if handsize >= 5:
            button_card_4 = pygame.Rect(600, 700, 141, 40)
            pygame.draw.rect(screen, (128, 128, 128), button_card_4)
            button_4_msg = "Play %s" % player.hand[4].name
            button_4_txt = fonts.small_button_font().render(button_4_msg, True, (255, 255, 255))
            screen.blit(button_4_txt, (603, 715))
            img_4 = pygame.image.load(player.hand[4].image)
            img_4 = pygame.transform.scale(img_4, (
                int(card_scale_factor * card_width), int(card_scale_factor * card_length)))
            screen.blit(img_4, (600, 485))

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
                                return 0
                    if handsize >= 2:
                        if button_card_1.collidepoint(mx, my):
                            if click:
                                return 1
                    if handsize >= 3:
                        if button_card_2.collidepoint(mx, my):
                            if click:
                                return 2
                    if handsize >= 4:
                        if button_card_3.collidepoint(mx, my):
                            if click:
                                return 3
                    if handsize >= 5:
                        if button_card_4.collidepoint(mx, my):
                            if click:
                                return 4
        displayboard(player, goblin, currentmessage)
        pass


def displayboard(player, goblin, currentmessage):
    screen.fill((0, 0, 0))
    # displays grid
    screen.blit(grid.grid(), [0, 47])
    displayplayer(player)
    display_score(player.score)
    display_armor(player.armor)
    display_gold(player.gold)
    display_draw_deck(len(player.drawdeck.cards))
    display_discard_deck(len(player.discarddeck.cards))
    displaycards(player)
    displaygoblin(goblin)

    message_display(currentmessage)  # todo update message_display to have a log of previous messages as well
    pygame.display.flip()


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
    # todo fix bug where attack misses if target is to the right of player, or above (might be fixed now)
    for possibletarget in range(0, attrange + 1):
        if player.xcoord + possibletarget == _monster.xcoord and player.ycoord == _monster.ycoord:
            return True
        elif player.ycoord + possibletarget == _monster.ycoord and player.xcoord == _monster.xcoord:
            return True
        elif player.xcoord - possibletarget == _monster.xcoord and player.ycoord == _monster.ycoord:
            return True
        elif player.ycoord - possibletarget == _monster.ycoord and player.xcoord == _monster.xcoord:
            return True

    return False


def isadjacent(player, _monster):
    if player.xcoord + 1 == _monster.xcoord and player.ycoord == _monster.ycoord:
        return True
    elif player.ycoord + 1 == _monster.ycoord and player.xcoord == _monster.xcoord:
        return True
    elif player.xcoord - 1 == _monster.xcoord and player.ycoord == _monster.ycoord:
        return True
    elif player.ycoord - 1 == _monster.ycoord and player.xcoord == _monster.xcoord:
        return True

    return False


def playermove(player, goblin, amount, direction):
    if direction == "down":
        destination = player.ycoord + amount
        if destination > 4:
            destination = 4
        for spacemoved in range(player.ycoord, destination):
            if goblin.ycoord == spacemoved + 1 and goblin.xcoord == player.xcoord:
                destination = spacemoved
                break
        player.ycoord = destination

    # todo fix bug where I couldnt move up when I was at coordinates (2,2), same issue from (3,2). (Might be fixed now)
    elif direction == "up":
        destination = player.ycoord - amount
        if destination < 0:
            destination = 0
        for spacemoved in range(player.ycoord, destination, -1):
            if goblin.ycoord == spacemoved - 1 and goblin.xcoord == player.xcoord:
                destination = spacemoved
                break
        player.ycoord = destination

    elif direction == "right":
        destination = player.xcoord + amount
        if destination > 4:
            destination = 4
        for spacemoved in range(player.xcoord, destination):
            if goblin.xcoord == spacemoved + 1 and goblin.ycoord == player.ycoord:
                destination = spacemoved
                break
        player.xcoord = destination


    elif direction == "left":
        destination = player.xcoord - amount
        if destination < 0:
            destination = 0
        for spacemoved in range(player.xcoord, destination, -1):
            if goblin.xcoord == spacemoved - 1 and goblin.ycoord == player.ycoord:
                destination = spacemoved
                break
        player.xcoord = destination


def playerturn(goblinmonster, player):
    currentmessage = ""
    index = choosecards(player, goblinmonster)
    displayboard(player, goblinmonster, currentmessage)

    playedcard = player.hand[index]
    if playedcard.move == 99:
        player.cleanup = True
    elif playedcard.move != 0:
        move = playedcard.move
        direction = ""
        validinput = False
        currentmessage = "Select the direction to move in"
        displayboard(player, goblinmonster, currentmessage)
        currentmessage = "using the arrow keys"
        displayboard(player, goblinmonster, currentmessage)
        while True:
            displayboard(player, goblinmonster, currentmessage)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        direction = "up"
                        validinput = True
                    elif event.key == pygame.K_DOWN:
                        direction = "down"
                        validinput = True
                    elif event.key == pygame.K_LEFT:
                        direction = "left"
                        validinput = True
                    elif event.key == pygame.K_RIGHT:
                        direction = "right"
                        validinput = True
                    else:
                        currentmessage = "that is not a valid key, please try again"
            if validinput:
                break
        playermove(player, goblinmonster, move, direction)
        player.cleanup = True
        displayboard(player, goblinmonster, currentmessage)

    if playedcard.attrange != 0:
        if not possibleattack(player, goblinmonster, playedcard.attrange):
            currentmessage = "There is no possible attack target"
            displayboard(player, goblinmonster, currentmessage)
            player.cleanup = True

        else:
            goblinmonster.damage(playedcard.damage)
            if not goblinmonster.isalive:
                randnum = random.randint(5, 10)
                droppedgold = randnum
                currentmessage = "You attack and kill the monster!"
                displayboard(player, goblinmonster, currentmessage)
                currentmessage = "You earn 100 points and %d gold!" % droppedgold
                displayboard(player, goblinmonster, currentmessage)
                player.gold = player.gold + droppedgold
                player.score = player.score + 100
                spawngoblin(goblinmonster, player)
                randnum = random.randint(1, 3)
                if randnum == 3:
                    player.loot = cardlib.randomcard()
                player.cleanup = True
                displayboard(player, goblinmonster, currentmessage)

            else:
                currentmessage = "The monster survives your attack."
                displayboard(player, goblinmonster, currentmessage)
                currentmessage = "The monster has %d health left" % goblinmonster.hp
                player.cleanup = True

    if playedcard.armor != 0:
        currentmessage = "You gain %d armor" % playedcard.armor
        player.armor = player.armor + playedcard.armor
        displayboard(player, goblinmonster, currentmessage)
        player.cleanup = True

    if player.cleanup:
        player.cleanup = False
        player.discard(index)
        currentmessage = "%s has been discarded." % playedcard.name
        displayboard(player, goblinmonster, currentmessage)
        displaycards(player)

        if (len(player.hand)) < 2:
            drawcount = 0
            while (len(player.hand)) < 5:
                drawcount = drawcount + 1
                player.draw()
            displayboard(player, goblinmonster, currentmessage)
            currentmessage = "You draw %d cards." % drawcount
            displayboard(player, goblinmonster, currentmessage)
            displaycards(player)

        player.turn = player.turn + 1
        return
    pass


def playerloot(player):
    screen.fill((0, 0, 0))
    while True:

        addprompt = "The monster has dropped a part! Would you like to add %s to your deck?" % player.loot.name
        screen.fill((0, 0, 0))
        button_option1 = pygame.Rect(400, 200, 400, 100)
        button_option2 = pygame.Rect(400, 400, 400, 100)
        pygame.draw.rect(screen, (255, 0, 0), button_option1)
        pygame.draw.rect(screen, (255, 0, 0), button_option2)
        addprompt = fonts.play_font().render(addprompt, True, (255, 255, 255))
        lootcard = pygame.image.load(player.loot.image)
        lootcard = pygame.transform.scale(lootcard, (210, 270))
        screen.blit(lootcard, (150, 40))

        # text for buttons
        button_option1_msg = "Yes"
        button_option2_msg = "No"
        button_option1_txt = player_select_font.render(button_option1_msg, True, (255, 255, 255))
        button_option2_txt = player_select_font.render(button_option2_msg, True, (255, 255, 255))
        screen.blit(addprompt, (490, 100))
        screen.blit(button_option1_txt, (430, 230))
        screen.blit(button_option2_txt, (434, 430))

        pygame.display.flip()

        for event in pygame.event.get():
            mx, my = pygame.mouse.get_pos()
            click = False
            if event.type == pygame.QUIT:
                exit()
            # event - left mousebutton clicked (button actions)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                click = True
                if button_option1.collidepoint(mx, my):
                    if click:
                        player.loot = None
                        player.addcard(player.loot)
                        return
                if button_option2.collidepoint(mx, my):
                    if click:
                        player.loot = None
                        return
            # call exit function on Esc key
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit()


def monsterturn(_monster, player):
    # checks each space adjacent to monster. If player is there, player is damaged, otherwise the monster moves closer.
    if isadjacent(_monster, player):
        if player.armor > 0:
            currentmessage = "The monster attacked you, but your armor protected you!"
            player.damage(1)
            displayboard(player, _monster, currentmessage)
        else:
            lostcard = player.damage(1)
            if player.isalive:
                currentmessage = "The monster attacked you and broke your %s!" % lostcard.name
                displayboard(player, _monster, currentmessage)
            else:
                currentmessage = "The monster attacked you and broke your robot! \nGAME OVER! \n Your score was: %d" % \
                                 player.score
                displayboard(player, _monster, currentmessage)
                time.sleep(4)

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
    goblinmonster.maxhp = goblinmonster.maxhp + 1


def message_display(text: object) -> object:
    white = (255, 255, 255)
    black = (0, 0, 0)

    border1 = pygame.Rect(746, 485, 2, 265)
    border2 = pygame.Rect(746, 485, 480, 2)
    pygame.draw.rect(screen, white, border1)
    pygame.draw.rect(screen, white, border2)




    mess_.new_message(text)
    message1, message2, message3, message4, message5 = mess_.get_messages()
    text1 = fonts.message_display_font().render(message1, True, white, black)
    text2 = fonts.message_display_font().render(message2, True, white, black)
    text3 = fonts.message_display_font().render(message3, True, white, black)
    text4 = fonts.message_display_font().render(message4, True, white, black)
    text5 = fonts.message_display_font().render(message5, True, white, black)

    textRect1 = text1.get_rect()
    textRect2 = text2.get_rect()
    textRect3 = text3.get_rect()
    textRect4 = text4.get_rect()
    textRect5 = text5.get_rect()

    textRect1.center = (960, 518)
    textRect2.center = (960, 571)
    textRect3.center = (960, 624)
    textRect4.center = (960, 677)
    textRect5.center = (960, 730)

    assert isinstance(screen, object)
    screen.blit(text1, textRect1)
    screen.blit(text2, textRect2)
    screen.blit(text3, textRect3)
    screen.blit(text4, textRect4)
    screen.blit(text5, textRect5)

    pygame.display.flip()


def shopphase(player):
    shopnotdoneyet = True
    if shopnotdoneyet:
        return

    screen.fill((0, 0, 0))
    shopcard1 = cardlib.randomcard()
    shopcard2 = cardlib.randomcard()
    shopcard3 = cardlib.randomcard()
    shopcard4 = cardlib.randomcard()
    shopcard5 = cardlib.randomcard()
    shopcard6 = cardlib.randomcard()
    shopcard7 = cardlib.randomcard()
    shopcard8 = cardlib.randomcard()
    shopcard9 = cardlib.randomcard()
    shopcard10 = cardlib.randomcard()
    while True:
        # todo display 10 cards using their respective images
        displayimage1 = shopcard1.image
        displayimage2 = shopcard2.image
        displayimage3 = shopcard3.image
        displayimage4 = shopcard4.image
        displayimage5 = shopcard5.image
        displayimage6 = shopcard6.image
        displayimage7 = shopcard7.image
        displayimage8 = shopcard8.image
        displayimage9 = shopcard9.image
        displayimage10 = shopcard10.image
        # todo display buttons below the cards that say "purchase x" where x is the card's cost
        card1cost = shopcard1.cost
        card2cost = shopcard2.cost
        card3cost = shopcard3.cost
        card4cost = shopcard4.cost
        card5cost = shopcard5.cost
        card6cost = shopcard6.cost
        card7cost = shopcard7.cost
        card8cost = shopcard8.cost
        card9cost = shopcard9.cost
        card10cost = shopcard10.cost
        # todo when the button is clicked, if the player has enough money, lose that much money and gain the card, and
        # todo replace the card in the shop with a different, random card.
        # todo Also send a message the player adds that card to their discard deck
        if player.gold < shopcard.cost:
            player.gold = player.gold - shopcard.cost
            player.discarddeck.addcard(shopcard)
            shopcard = cardlib.randomcard()
            message_display("You have purchased %s and added it to your discard deck.") % shopcard.name

        else:
            message_display("you do not have enough gold to purchase that card.")

        # todo there should also be a button that, when clicked, runs the following code
        removedcard = removecard(player)
        removed = False
        for card in player.drawdeck:
            if removedcard == card.name:
                player.drawdeck.remove(card)
                removed = True
                break
        if not removed:
            for card in player.discarddeck:
                if removedcard == card.name:
                    player.discarddeck.remove(card)
                    removed = True
                    break
        if not removed:
            for card in player.hand:
                if removedcard == card.name:
                    player.hand.remove(card)
                    removed = True
                    break


        # todo there should be another button that, when clicked, allows for the player to exit the shop
        if False:
            # change to button click, this should bring the player right back to the game function.
            return
        # todo the player's current gold amount should also be displayed at the top of the screen, preferably in yellow.
        playergoldfordisplay = player.gold
        pygame.display.flip()

    pass


def removecard(player):
    uniquecards = deckcardplayerclasses.Deck()

    for card in player.drawdeck:
        for uniquecard in uniquecards:
            if card == uniquecard:
                break
            else:
                uniquecards.addcard(card)

    for card in player.discarddeck:
        for uniquecard in uniquecards:
            if card == uniquecard:
                break
            else:
                uniquecards.addcard(card)

    for card in player.hand:
        for uniquecard in uniquecards:
            if card == uniquecard:
                break
            else:
                uniquecards.addcard(card)

    totalcards = len(uniquecards)
    #todo for each card in uniquecards, display it on the screen, to a max of 15. If you don't think 15 will fit, 10 is fine
    #todo each card should also have a button underneath it that, when clicked, returns card.name
    pass


def game():
    characterselect = characterscreen()
    xplayer = grid.rand_location()
    yplayer = grid.rand_location()

    player1 = playersetup(xplayer, yplayer, characterselect)

    goblinmonster = monster.Monster(0, 0, 0)
    spawngoblin(goblinmonster, player1)
    displayplayer(player1)
    displaygoblin(goblinmonster)
    currentmessage = "Use the cards to kill the goblins!"
    turncount = 0
    while player1.isalive:

        screen.fill((0, 0, 0))
        displayboard(player1, goblinmonster, currentmessage)
        currentmessage = ""
        if player1.turn < 2:
            playerturn(goblinmonster, player1)
            displayboard(player1, goblinmonster, currentmessage)
            if player1.loot != None:
                playerloot(player1)

        if player1.turn >= 2:
            monsterturn(goblinmonster, player1)
            player1.turn = 0
            displayboard(player1, goblinmonster, currentmessage)

        turncount = turncount + 1

        if turncount % 10 == 0:
            shopphase(player1)
        mainClock.tick(60)
    while True:
        # game over screen in progress
        screen.fill((255, 0, 0))
        pygame.display.flip()


# todo add game over screen and display player1.score

white = (255, 255, 255)


def text_objects(text, font):
    textSurface = font.render(text, True, white)
    return textSurface, textSurface.get_rect()


def highscore_display(text, i):
    height = window_height / 10
    largeText = pygame.font.Font('pixel_font.TTF', 30)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((window_width / 2), (height + (i * 50)))
    screen.blit(TextSurf, TextRect)

    # pygame.display.update()


def read_scores(filename):
    with open(filename) as f:
        return [int(x) for x in f]


def highscores():
    # todo add a button that when clicked, returns back to main menu.
    black = (0, 0, 0)
    white = (255, 255, 255)
    red = (255, 0, 0)
    arr = read_scores('highscores.txt')

    running = True
    scoresdisplayed = False
    while running:
        screen.fill(black)
        button_back = pygame.Rect(50, 50, 150, 50)
        pygame.draw.rect(screen, (255, 0, 0), button_back)
        button_back_msg = "BACK"
        button_back_txt = fonts.back_font().render(button_back_msg, True, (255, 255, 255))
        screen.blit(button_back_txt, (68, 61))
        for event in pygame.event.get():
            mx, my = pygame.mouse.get_pos()
            click = False
            if event.type == pygame.QUIT:
                running = False
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                click = True
                if button_back.collidepoint(mx, my):
                    if click:
                        main_menu()

        highscore_display("Top 10 High Scores:", 0)
        for i in range(10):
            temp_string = str(arr[i])
            temp_string = str(i + 1) + ". " + temp_string
            highscore_display(temp_string, i + 1)

        if scoresdisplayed == False:
            pygame.display.flip()
            displayed = True

        mainClock.tick(60)


def exit():
    pygame.quit()
    sys.exit()


main_menu()
