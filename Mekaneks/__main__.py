import random
import sys
import time
from os import path

import pygame

import cardlib
import deckcardplayerclasses
import fonts
import grid
import messages
import monster

# initialize game engine and open a window
mainClock = pygame.time.Clock()
pygame.init()
window_width = 1200
window_height = 750
# window settings
display_size = (window_width, window_height)
screen = pygame.display.set_mode(display_size)
pygame.display.set_caption('Mechanum')
FPS = 60
white = (255, 255, 255)

# main font (currently system default)


# sounds
pygame.mixer.pre_init(44100, 16, 2, 4096)  # frequency, size, channels, buffersize
pygame.mixer.init()
sound_dir = path.join(path.dirname(__file__), 'Sounds')
MenuMusic = pygame.mixer.music.load(path.join(sound_dir, 'acid_music.wav'))     #A.C.I.D. - Intro the Breach OST
#music_playing = True        #Variable to toggle music on/off

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


def save_high_score(new_high_score):
    hs_file = "highscores.txt"
    hs_arr = read_scores(hs_file)
    hs_arr.sort()

    # Displaying text whether or not you made it to the top 10
    update_text = pygame.font.Font('Video Game Font.ttf', 20)
    updatedSurf, updatedRect = text_objects("Congrats, you made the top 10 in high scores!", update_text)
    updatedRect.center = ((window_width / 2), (window_height - (window_height / 6)))

    notUpdatedSurf, notUpdatedRect = text_objects("Sorry, you didn't make top 10 :(", update_text)
    notUpdatedRect.center = ((window_width / 2), (window_height - (window_height / 6)))

    # Checks to see if the new score is greater than the first (smallest) element in the array
    # If so, then lowest score is replaced with new high score
    if new_high_score > hs_arr[0]:
        screen.blit(updatedSurf, updatedRect)
        hs_arr.pop(0)
        hs_arr.append(new_high_score)
        hs_arr.sort()
        try:
            high_score_file = open(hs_file, "w")
            for element in range(10):
                temp_str = str(hs_arr[element])
                high_score_file.write(temp_str + "\n")
            high_score_file.close()
        except IOError:
            # Can't write to file
            print("Unable to write to file...")
    else:
        screen.blit(notUpdatedSurf, notUpdatedRect)


def create_game_over(score):
    # Update high scores if needed; need to call other function that saves score to file

    pygame.display.set_caption('GAME OVER')
    screen.fill((255, 0, 0))
    pygame.init()

    go_score = "Final Score: " + str(score)
    largeText = pygame.font.Font('Video Game Font.ttf', 50)
    textSurf, textRect = text_objects(go_score, largeText)
    textRect.center = ((window_width / 2), (window_height / 2))
    screen.blit(textSurf, textRect)

    go_msg = "Press any key to return to the main menu."
    medText = pygame.font.Font('Video Game Font.ttf', 20)
    textSurf2, textRect2 = text_objects(go_msg, medText)
    textRect2.center = ((window_width / 2), (window_height - (window_height / 4)))
    screen.blit(textSurf2, textRect2)

    # using the end score, check to see if the scores need to be updated; print if they were updated or not
    save_high_score(score)

    pygame.display.update()

    game_over = True
    while game_over:
        # time.clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                # Goes back to main menu
                game_over = False
                main_menu()


def main_menu():
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.2)
    music_playing = True  # Variable to toggle music on/off

    while True:
        # button texts
        # Fill black
        screen.fill((0, 0, 0))
        # button creations
        # text_play = font.render('Mechanum', True, (255, 255, 255))
        # screen.blit(text_play, (200, 100))
        # Rect(left pos, top pos, width, height)
        button_play = pygame.Rect(450, 150, 300, 100)
        button_highscores = pygame.Rect(450, 350, 300, 100)
        button_exit = pygame.Rect(450, 550, 300, 100)
        button_tutorial = pygame.Rect(535, 275, 130, 25)
        button_mute = pygame.Rect(980, 10, 200, 25)

        pygame.draw.rect(screen, (255, 0, 0), button_play)
        pygame.draw.rect(screen, (255, 0, 0), button_highscores)
        pygame.draw.rect(screen, (255, 0, 0), button_exit)
        pygame.draw.rect(screen, (255, 0, 0), button_play)
        pygame.draw.rect(screen, (255, 255, 255), button_tutorial)
        pygame.draw.rect(screen, (255, 255, 255), button_mute)

        # text for buttons
        button_title_msg = "MECHANUM"
        button_play_msg = "PLAY"
        button_opt_msg = "Highscores"
        button_quit_msg = "Quit"
        button_tut_msg = "Tutorial"
        button_mute_msg = "Toggle Music"

        button_title_text = fonts.title_font().render(button_title_msg, True, (255, 255, 255))
        button_play_txt = fonts.play_font().render(button_play_msg, True, (255, 255, 255))
        button_opt_txt = fonts.highscore_font().render(button_opt_msg, True, (255, 255, 255))
        button_quit_txt = fonts.quit_font().render(button_quit_msg, True, (255, 255, 255))
        button_tut_txt = fonts.tut_font().render(button_tut_msg, True, (0, 0, 0))
        button_mute_txt = fonts.tut_font().render(button_mute_msg, True, (0, 0, 0))

        screen.blit(button_title_text, (410, 50))
        screen.blit(button_play_txt, (537, 170))
        screen.blit(button_opt_txt, (465, 372))
        screen.blit(button_quit_txt, (537, 570))
        screen.blit(button_tut_txt, (537, 280))
        screen.blit(button_mute_txt, (990, 15))

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
                if button_tutorial.collidepoint(mx, my):
                    if click:
                        xplayer = grid.rand_location()
                        yplayer = grid.rand_location()
                        player1 = playersetup(xplayer, yplayer, 1)
                        goblin = monster.Monster(0, 0, 0)
                        game_tutorial(player1, goblin)
                if button_mute.collidepoint(mx, my):
                    while(click):
                        if music_playing == True:
                            pygame.mixer.music.pause()
                            music_playing = False
                        else:
                            pygame.mixer.music.unpause()
                            music_playing = True
                        break

            # call exit function on Esc key
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit()
        pygame.display.update()
        mainClock.tick(60)


def characterscreen() -> object:

    character = 0
    difficulty = 0
    screen.fill((0, 0, 0))
    color1 = (0, 0, 0)
    color2 = (0, 0, 0)
    color3 = (0, 0, 0)
    color4 = (0, 0, 0)
    button_char1 = pygame.Rect(90, 255, 400, 100)
    button_char2 = pygame.Rect(90, 450, 400, 100)
    button_diff1 = pygame.Rect(720, 255, 400, 100)
    button_diff2 = pygame.Rect(720, 450, 400, 100)
    button_fill1 = pygame.Rect(92, 257, 396, 96)
    button_fill2 = pygame.Rect(92, 452, 396, 96)
    button_fill3 = pygame.Rect(722, 257, 396, 96)
    button_fill4 = pygame.Rect(722, 452, 396, 96)
    button_go = pygame.Rect(520, 360, 170, 100)

    pygame.draw.rect(screen, (255, 0, 0), button_char1)
    pygame.draw.rect(screen, (255, 0, 0), button_char2)
    pygame.draw.rect(screen, (255, 0, 0), button_diff1)
    pygame.draw.rect(screen, (255, 0, 0), button_diff2)

    robby_disp = pygame.image.load("Images/Robby.png")
    robby_disp = pygame.transform.scale(robby_disp, (134, 172))
    screen.blit(robby_disp, (40, 85))

    doom_disp = pygame.image.load("Images/doomcopter.png")
    doom_disp = pygame.transform.scale(doom_disp, (134, 172))
    screen.blit(doom_disp, (440, 550))

    # text for buttons
    play_as_msg = "SELECT YOUR CHARACTER:"
    difficulty_msg = "SELECT YOUR DIFFICULTY:"
    button_char1_msg = "Robby the Robot"
    button_char2_msg = "The Doomcopter"
    button_diff1_msg = "EASY"
    button_diff2_msg = "HARD"
    go_msg = "Play"

    button_char1_txt = fonts.player_select_font().render(button_char1_msg, True, (255, 255, 255))
    button_char2_txt = fonts.player_select_font().render(button_char2_msg, True, (255, 255, 255))
    play_as_msg_txt = fonts.player_select_font().render(play_as_msg, True, (255, 255, 255))
    difficulty_msg_txt = fonts.player_select_font().render(difficulty_msg, True, (255, 255, 255))
    button_diff1_txt = fonts.player_select_font().render(button_diff1_msg, True, (255, 255, 255))
    button_diff2_txt = fonts.player_select_font().render(button_diff2_msg, True, (255, 255, 255))
    go_txt = fonts.go_font().render(go_msg, True, (255, 255, 255))

    screen.blit(play_as_msg_txt, (60, 50))
    screen.blit(difficulty_msg_txt, (664, 50))

    pygame.draw.line(screen, (255, 255, 255), (window_width / 2, 0), (window_width / 2, 1000), 3)
    pygame.draw.rect(screen, (255, 0, 0), button_go)
    screen.blit(go_txt, (window_width / 2 - 73, window_height / 2 - 8))

    while True:
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
                        character = 1
                        color1 = (255, 0, 0)
                        color2 = (0, 0, 0)
                if button_char2.collidepoint(mx, my):
                    if click:
                        character = 2
                        color1 = (0, 0, 0)
                        color2 = (255, 0, 0)
                if button_diff1.collidepoint(mx, my):
                    if click:
                        difficulty = 1
                        color3 = (255, 0, 0)
                        color4 = (0, 0, 0)
                if button_diff2.collidepoint(mx, my):
                    if click:
                        difficulty = 2
                        color3 = (0, 0, 0)
                        color4 = (255, 0, 0)
                if button_go.collidepoint(mx, my):
                    if click:
                        if not character == 0:
                            if not difficulty == 0:
                                return character, difficulty

            # call exit function on Esc key
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit()

        pygame.draw.rect(screen, color1, button_fill1)
        pygame.draw.rect(screen, color2, button_fill2)
        pygame.draw.rect(screen, color3, button_fill3)
        pygame.draw.rect(screen, color4, button_fill4)
        screen.blit(button_char1_txt, (120, 285))
        screen.blit(button_char2_txt, (124, 480))
        screen.blit(button_diff1_txt, (875, 285))
        screen.blit(button_diff2_txt, (875, 480))
        pygame.display.update()


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


def playerturn(goblinmonster, player, difficulty):
    currentmessage = ""
    index = choosecards(player, goblinmonster)

    playedcard = player.hand[index]
    if playedcard.move == 99:
        player.cleanup = True
    elif playedcard.move != 0:
        move = playedcard.move
        direction = ""
        validinput = False
        message_display("Select the direction to move in")
        currentmessage = "using the arrow keys"
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
                message_display("You attack and kill the monster!")
                currentmessage = "You earn 100 points and %d gold!" % droppedgold
                player.gold = player.gold + droppedgold
                player.score = player.score + 100
                spawngoblin(goblinmonster, player)
                if difficulty == 1:
                    player.loot = cardlib.randomcard()
                else:
                    randnum = random.randint(1, 3)
                    if randnum == 3:
                        player.loot = cardlib.randomcard()
                player.cleanup = True
                displayboard(player, goblinmonster, currentmessage)

            else:
                message_display("The monster survives your attack.")
                currentmessage = "The monster has %d health left" % goblinmonster.hp
                displayboard(player, goblinmonster, currentmessage)
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

        if (len(player.hand)) < 2:
            drawcount = 0
            while (len(player.hand)) < 5:
                drawcount = drawcount + 1
                player.draw()
            currentmessage = "You draw %d cards." % drawcount
            displayboard(player, goblinmonster, currentmessage)

        player.turn = player.turn + 1
        return
    pass


def playerloot(player):
    while True:

        addprompt = "The monster has dropped a part!"
        addprompt2 = "Would you like to add %s to your deck?" % player.loot.name
        screen.fill((0, 0, 0))
        button_option1 = pygame.Rect(400, 200, 400, 100)
        button_option2 = pygame.Rect(400, 400, 400, 100)
        pygame.draw.rect(screen, (255, 0, 0), button_option1)
        pygame.draw.rect(screen, (255, 0, 0), button_option2)
        addprompt = fonts.message_display_font().render(addprompt, True, (255, 255, 255))
        addprompt2 = fonts.message_display_font().render(addprompt2, True, (255, 255, 255))
        lootcard = pygame.image.load(player.loot.image)
        lootcard = pygame.transform.scale(lootcard, (210, 270))
        screen.blit(lootcard, (150, 40))

        # text for buttons
        button_option1_msg = "Yes"
        button_option2_msg = "No"
        button_option1_txt = fonts.play_font().render(button_option1_msg, True, (255, 255, 255))
        button_option2_txt = fonts.play_font().render(button_option2_msg, True, (255, 255, 255))
        screen.blit(addprompt, (490, 100))
        screen.blit(addprompt2, (490, 140))
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
                        player.addcard(player.loot)
                        player.loot = None
                        return
                if button_option2.collidepoint(mx, my):
                    if click:
                        player.loot = None
                        return
            # call exit function on Esc key
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit()


def monsterturn(_monster, player, p_score):
    # checks each space adjacent to monster. If player is there, player is damaged, otherwise the monster moves closer.
    if isadjacent(_monster, player):
        for i in range(0, _monster.attackpower):
            if player.armor > 0:
                message_display("Your armor protected you from 1 damage!")
                player.damage(1, p_score)
            else:
                lostcard = player.damage(1, p_score)
                if player.isalive:
                    message_display("The monster broke your %s!" % lostcard.name)
                else:
                    currentmessage = "The monster broke your robot!"
                    displayboard(player, _monster, currentmessage)
                    time.sleep(4)

    else:
        message_display("The monster moves closer.")
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
    currentmessage = ""


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
    goblinmonster.hp = goblinmonster.maxhp
    message_display("The monsters have %d hp" % goblinmonster.hp)
    if goblinmonster.maxhp % 3 == 0:
        goblinmonster.attackpower = goblinmonster.attackpower + 1
        if goblinmonster.attackpower < 5:
            goblinmonster.sprite = cardlib.sprites[goblinmonster.attackpower - 1]
        message_display("The monsters have %d atk" % goblinmonster.attackpower)


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

def tut_message(text):
    white = (255, 255, 255)
    black = (0, 0, 0)

    border1 = pygame.Rect(746, 485, 2, 265)
    border2 = pygame.Rect(746, 485, 480, 2)
    pygame.draw.rect(screen, white, border1)
    pygame.draw.rect(screen, white, border2)

    mess_.new_tutorial_message(text)
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


def shopphase(player):
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

    # first message to be displayed, overwritten when other cards are purchased.
    log_msg = "Purchase a card!"

    while True:
        screen.fill((0, 0, 0))
        # Display card images
        displayimage1 = shopcard1.image
        img_shop_card1 = pygame.image.load(displayimage1)
        img_shop_card1 = pygame.transform.scale(img_shop_card1, (
            int(card_scale_factor * card_width), int(card_scale_factor * card_length)))
        screen.blit(img_shop_card1, (125, 100))
        displayimage2 = shopcard2.image
        img_shop_card2 = pygame.image.load(displayimage2)
        img_shop_card2 = pygame.transform.scale(img_shop_card2, (
            int(card_scale_factor * card_width), int(card_scale_factor * card_length)))
        screen.blit(img_shop_card2, (325, 100))
        displayimage3 = shopcard3.image
        img_shop_card3 = pygame.image.load(displayimage3)
        img_shop_card3 = pygame.transform.scale(img_shop_card3, (
            int(card_scale_factor * card_width), int(card_scale_factor * card_length)))
        screen.blit(img_shop_card3, (525, 100))
        displayimage4 = shopcard4.image
        img_shop_card4 = pygame.image.load(displayimage4)
        img_shop_card4 = pygame.transform.scale(img_shop_card4, (
            int(card_scale_factor * card_width), int(card_scale_factor * card_length)))
        screen.blit(img_shop_card4, (725, 100))
        displayimage5 = shopcard5.image
        img_shop_card5 = pygame.image.load(displayimage5)
        img_shop_card5 = pygame.transform.scale(img_shop_card5, (
            int(card_scale_factor * card_width), int(card_scale_factor * card_length)))
        screen.blit(img_shop_card5, (925, 100))
        displayimage6 = shopcard6.image
        img_shop_card6 = pygame.image.load(displayimage6)
        img_shop_card6 = pygame.transform.scale(img_shop_card6, (
            int(card_scale_factor * card_width), int(card_scale_factor * card_length)))
        screen.blit(img_shop_card6, (125, 400))
        displayimage7 = shopcard7.image
        img_shop_card7 = pygame.image.load(displayimage7)
        img_shop_card7 = pygame.transform.scale(img_shop_card7, (
            int(card_scale_factor * card_width), int(card_scale_factor * card_length)))
        screen.blit(img_shop_card7, (325, 400))
        displayimage8 = shopcard8.image
        img_shop_card8 = pygame.image.load(displayimage8)
        img_shop_card8 = pygame.transform.scale(img_shop_card8, (
            int(card_scale_factor * card_width), int(card_scale_factor * card_length)))
        screen.blit(img_shop_card8, (525, 400))
        displayimage9 = shopcard9.image
        img_shop_card9 = pygame.image.load(displayimage9)
        img_shop_card9 = pygame.transform.scale(img_shop_card9, (
            int(card_scale_factor * card_width), int(card_scale_factor * card_length)))
        screen.blit(img_shop_card9, (725, 400))
        displayimage10 = shopcard10.image
        img_shop_card10 = pygame.image.load(displayimage10)
        img_shop_card10 = pygame.transform.scale(img_shop_card10, (
            int(card_scale_factor * card_width), int(card_scale_factor * card_length)))
        screen.blit(img_shop_card10, (925, 400))

        # Display costs
        card1cost = shopcard1.cost
        button_purchase_card1 = pygame.Rect(125, 335, 145, 30)
        pygame.draw.rect(screen, (128, 128, 128), button_purchase_card1)
        msg_card1_price = "Purchase for %s" % card1cost
        card1_price_txt = fonts.small_button_font().render(msg_card1_price, True, (255, 255, 255))
        screen.blit(card1_price_txt, (125, 345))
        card2cost = shopcard2.cost
        button_purchase_card2 = pygame.Rect(325, 335, 145, 30)
        pygame.draw.rect(screen, (128, 128, 128), button_purchase_card2)
        msg_card2_price = "Purchase for %s" % card2cost
        card2_price_txt = fonts.small_button_font().render(msg_card2_price, True, (255, 255, 255))
        screen.blit(card2_price_txt, (325, 345))
        card3cost = shopcard3.cost
        button_purchase_card3 = pygame.Rect(525, 335, 145, 30)
        pygame.draw.rect(screen, (128, 128, 128), button_purchase_card3)
        msg_card3_price = "Purchase for %s" % card3cost
        card3_price_txt = fonts.small_button_font().render(msg_card3_price, True, (255, 255, 255))
        screen.blit(card3_price_txt, (525, 345))
        card4cost = shopcard4.cost
        button_purchase_card4 = pygame.Rect(725, 335, 145, 30)
        pygame.draw.rect(screen, (128, 128, 128), button_purchase_card4)
        msg_card4_price = "Purchase for %s" % card4cost
        card4_price_txt = fonts.small_button_font().render(msg_card4_price, True, (255, 255, 255))
        screen.blit(card4_price_txt, (725, 345))
        card5cost = shopcard5.cost
        button_purchase_card5 = pygame.Rect(925, 335, 145, 30)
        pygame.draw.rect(screen, (128, 128, 128), button_purchase_card5)
        msg_card5_price = "Purchase for %s" % card5cost
        card5_price_txt = fonts.small_button_font().render(msg_card5_price, True, (255, 255, 255))
        screen.blit(card5_price_txt, (925, 345))

        # 2nd row of cards
        card6cost = shopcard6.cost
        button_purchase_card6 = pygame.Rect(125, 635, 145, 30)
        pygame.draw.rect(screen, (128, 128, 128), button_purchase_card6)
        msg_card6_price = "Purchase for %s" % card6cost
        card6_price_txt = fonts.small_button_font().render(msg_card6_price, True, (255, 255, 255))
        screen.blit(card6_price_txt, (125, 645))
        card7cost = shopcard7.cost
        button_purchase_card7 = pygame.Rect(325, 635, 145, 30)
        pygame.draw.rect(screen, (128, 128, 128), button_purchase_card7)
        msg_card7_price = "Purchase for %s" % card7cost
        card7_price_txt = fonts.small_button_font().render(msg_card7_price, True, (255, 255, 255))
        screen.blit(card7_price_txt, (325, 645))
        card8cost = shopcard8.cost
        button_purchase_card8 = pygame.Rect(525, 635, 145, 30)
        pygame.draw.rect(screen, (128, 128, 128), button_purchase_card8)
        msg_card8_price = "Purchase for %s" % card8cost
        card8_price_txt = fonts.small_button_font().render(msg_card8_price, True, (255, 255, 255))
        screen.blit(card8_price_txt, (525, 645))
        card9cost = shopcard9.cost
        button_purchase_card9 = pygame.Rect(725, 635, 145, 30)
        pygame.draw.rect(screen, (128, 128, 128), button_purchase_card9)
        msg_card9_price = "Purchase for %s" % card9cost
        card9_price_txt = fonts.small_button_font().render(msg_card9_price, True, (255, 255, 255))
        screen.blit(card9_price_txt, (725, 645))
        card10cost = shopcard10.cost
        button_purchase_card10 = pygame.Rect(925, 635, 145, 30)
        pygame.draw.rect(screen, (128, 128, 128), button_purchase_card10)
        msg_card10_price = "Purchase for %s" % card10cost
        card10_price_txt = fonts.small_button_font().render(msg_card10_price, True, (255, 255, 255))
        screen.blit(card10_price_txt, (925, 645))

        # todo add remove card button for sprint 3
        # button_discard = pygame.Rect(800, 20, 275, 50)
        # pygame.draw.rect(screen, (0, 0, 255), button_discard)
        # msg_discard = "Remove a card here for 5 gold"
        # discard_txt = fonts.small_button_font().render(msg_discard, True, (255, 255, 255))
        # screen.blit(discard_txt, (820, 45))
        # todo when the button is clicked, if the player has enough money, lose that much money and gain the card, and
        # todo replace the card in the shop with a different, random card.
        # todo Also send a message the player adds that card to their discard deck

        # Go back message
        button_0_msg = "Press Esc to exit the shop"
        button_back_txt = fonts.small_button_font().render(button_0_msg, True, (255, 255, 255))
        screen.blit(button_back_txt, (800, 730))

        # Purchase display log
        log_txt = fonts.small_button_font().render(log_msg, True, (255, 255, 255))
        screen.blit(log_txt, (300, 730))

        for event in pygame.event.get():
            mx, my = pygame.mouse.get_pos()
            click = False
            # card purchase event
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if button_purchase_card1.collidepoint(mx, my):
                    # buy card 1(not done)
                    if player.gold >= shopcard1.cost:
                        player.gold = player.gold - shopcard1.cost
                        player.addcard(shopcard1)
                        log_msg = ("%s has been added to your discard deck.") % shopcard1.name
                        shopcard1 = cardlib.randomcard()
                    else:
                        log_msg = "You do not have enough gold to purchase that card."
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if button_purchase_card2.collidepoint(mx, my):
                    if player.gold >= shopcard2.cost:
                        player.gold = player.gold - shopcard2.cost
                        player.addcard(shopcard2)
                        log_msg = ("%s has been added to your discard deck.") % shopcard1.name
                        shopcard2 = cardlib.randomcard()
                    else:
                        log_msg = "You do not have enough gold to purchase that card."

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if button_purchase_card3.collidepoint(mx, my):
                    if player.gold >= shopcard3.cost:
                        player.gold = player.gold - shopcard1.cost
                        player.addcard(shopcard3)
                        log_msg = ("%s has been added to your discard deck.") % shopcard3.name
                        shopcard3 = cardlib.randomcard()
                    else:
                        log_msg = "You do not have enough gold to purchase that card."

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if button_purchase_card4.collidepoint(mx, my):
                    if player.gold >= shopcard4.cost:
                        player.gold = player.gold - shopcard4.cost
                        player.addcard(shopcard4)
                        log_msg = ("%s has been added to your discard deck.") % shopcard1.name
                        shopcard4 = cardlib.randomcard()
                    else:
                        log_msg = "You do not have enough gold to purchase that card."

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if button_purchase_card5.collidepoint(mx, my):
                    if player.gold >= shopcard5.cost:
                        player.gold = player.gold - shopcard5.cost
                        player.addcard(shopcard5)
                        log_msg = ("%s has been added to your discard deck.") % shopcard5.name
                        shopcard5 = cardlib.randomcard()
                    else:
                        log_msg = "You do not have enough gold to purchase that card."

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if button_purchase_card6.collidepoint(mx, my):
                    if player.gold >= shopcard6.cost:
                        player.gold = player.gold - shopcard6.cost
                        player.addcard(shopcard6)
                        log_msg = ("%s has been added to your discard deck.") % shopcard6.name
                        shopcard6 = cardlib.randomcard()
                    else:
                        log_msg = "You do not have enough gold to purchase that card."

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if button_purchase_card7.collidepoint(mx, my):
                    if player.gold >= shopcard7.cost:
                        player.gold = player.gold - shopcard7.cost
                        player.addcard(shopcard7)
                        log_msg = ("%s has been added to your discard deck.") % shopcard7.name
                        shopcard7 = cardlib.randomcard()
                    else:
                        log_msg = "You do not have enough gold to purchase that card."

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if button_purchase_card8.collidepoint(mx, my):
                    if player.gold >= shopcard8.cost:
                        player.gold = player.gold - shopcard8.cost
                        player.addcard(shopcard8)
                        log_msg = ("%s has been added to your discard deck.") % shopcard8.name
                        shopcard8 = cardlib.randomcard()
                    else:
                        log_msg = "You do not have enough gold to purchase that card."

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if button_purchase_card9.collidepoint(mx, my):
                    if player.gold >= shopcard9.cost:
                        player.gold = player.gold - shopcard9.cost
                        player.addcard(shopcard9)
                        log_msg = ("%s has been added to your discard deck.") % shopcard9.name
                        shopcard9 = cardlib.randomcard()
                    else:
                        log_msg = "You do not have enough gold to purchase that card."

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if button_purchase_card10.collidepoint(mx, my):
                    if player.gold >= shopcard10.cost:
                        player.gold = player.gold - shopcard10.cost
                        player.addcard(shopcard10)
                        log_msg = ("%s has been added to your discard deck.") % shopcard10.name
                        shopcard10 = cardlib.randomcard()
                    else:
                        log_msg = "You do not have enough gold to purchase that card."

            if event.type == pygame.QUIT:
                running = False
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Exit Shop here
                    return

        # Showing gold amount
        display_score(player.score)
        display_gold(player.gold)
        pygame.display.flip()


'''
             #todo move this up
            discard button event
             if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                click = True
                if button_discard.collidepoint(mx, my):
                    if click:
                        removedcard = removecard(player)
                        removed = False
                        for card in player.drawdeck:
                            if removedcard == card.name:
                                player.drawdeck.remove(card)
                                removed = True
                        if not removed:
                            for card in player.discarddeck:
                                if removedcard == card.name:
                                    player.discarddeck.remove(card)
                                    removed = True
                        if not removed:
                            for card in player.hand:
                                if removedcard == card.name:
                                    player.hand.remove(card)
                                    removed = True
   '''


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
    # todo for each card in uniquecards, display it on the screen, to a max of 15. If you don't think 15 will fit, 10 is fine
    # todo each card should also have a button underneath it that, when clicked, returns card.name
    pass


def game_tutorial(player: object, goblin: object) -> object:
    stage = 1
    running = True

    while not stage == 10:
        screen.fill((0, 0, 0))
    # explain message box
        if stage == 1:
            tut_message("Welcome to MEKANEKS")
            pygame.display.flip()
    # explain grid and character
        if stage == 2:
            screen.blit(grid.grid(), [0, 47])
            displayplayer(player)
            tut_message("This is your grid with your character")
            tut_message("Your job is to move around and attack.")
            tut_message("Goal: survive as long as you can.")
            pygame.display.flip()
    # explain monsters
        if stage == 3:
            screen.blit(grid.grid(), [0, 47])
            displayplayer(player)
            displaygoblin(goblin)
            tut_message("The monster will chase you.")
            tut_message("Stay alive for as you can.")
            tut_message("Kill the monster or be killed.")
            tut_message("Kill one and a stronger one appears.")
            pygame.display.flip()
    # explain coins
        if stage == 4:
            screen.blit(grid.grid(), [0, 47])
            displayplayer(player)
            displaygoblin(goblin)
            display_gold(player.gold)
            tut_message("Kill monsters to get coins and cards.")
            tut_message("You can buy cards in the shop.")
            tut_message("Build the best deck you can!")
            pygame.display.flip()
    # explain scores
        if stage == 5:
            screen.blit(grid.grid(), [0, 47])
            displayplayer(player)
            displaygoblin(goblin)
            display_gold(player.gold)
            display_score(player.score)
            tut_message("Your score is above the grid.")
            tut_message("Each monster is worth 100 points")
            pygame.display.flip()
    # explain armor
        if stage == 6:
            screen.blit(grid.grid(), [0, 47])
            displayplayer(player)
            displaygoblin(goblin)
            display_gold(player.gold)
            display_score(player.score)
            display_armor(player.armor)
            tut_message("Monster attacks break your cards.")
            tut_message("Armor prevents damage.")
            tut_message("Get armor from armor cards.")
            tut_message("If you don't have 5 cards left, you lose!")
            pygame.display.flip()
    # explain hand
        if stage == 7:
            screen.blit(grid.grid(), [0, 47])
            displayplayer(player)
            displaygoblin(goblin)
            display_gold(player.gold)
            display_score(player.score)
            display_armor(player.armor)
            displaycards(player)
            tut_message("Each turn you can play a card.")
            tut_message("Using them, you can move, attack,")
            tut_message("or gain armor.")
            tut_message("The button below the card will play it.")
            pygame.display.flip()
    # explain drawdeck & discard
        if stage == 8:
            screen.blit(grid.grid(), [0, 47])
            displayplayer(player)
            displaygoblin(goblin)
            display_gold(player.gold)
            display_score(player.score)
            display_armor(player.armor)
            displaycards(player)
            display_draw_deck(len(player.drawdeck.cards))
            display_discard_deck(len(player.discarddeck.cards))
            tut_message("Used cards go to the discard.")
            tut_message("New cards from the draw deck.")
            tut_message("If the draw deck is empty,")
            tut_message("the discard deck is shuffled in.")
            pygame.display.flip()
        if stage == 9:
            screen.blit(grid.grid(), [0, 47])
            displayplayer(player)
            displaygoblin(goblin)
            display_gold(player.gold)
            display_score(player.score)
            display_armor(player.armor)
            displaycards(player)
            display_draw_deck(len(player.drawdeck.cards))
            display_discard_deck(len(player.discarddeck.cards))
            tut_message("You're ready to play!")
            tut_message(" ")
            tut_message("  ")
            tut_message("   ")
            pygame.display.flip()



        for event in pygame.event.get():
            click = False
            if event.type == pygame.QUIT:
                running = False
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
                if click:
                    stage = stage + 1
    # todo explain shop


def game():

    characterselect, difficulty = characterscreen()
    xplayer = grid.rand_location()
    yplayer = grid.rand_location()

    player1 = playersetup(xplayer, yplayer, characterselect)

    goblinmonster = monster.Monster(0, 0, 0)
    spawngoblin(goblinmonster, player1)
    displayplayer(player1)
    displaygoblin(goblinmonster)
    currentmessage = "Use the cards to kill the goblins!"
    turncount = 0
    if difficulty == 1:
        shopturns = 5
    else:
        shopturns = 10
    while player1.isalive:
        turncount = turncount + 1
        shopcountdown = shopturns - turncount % shopturns
        if shopcountdown == shopturns:
            currentmessage = "The shop will open this round!"
        else:
            currentmessage = ("%d rounds until the shop opens!" % shopcountdown)
        displayboard(player1, goblinmonster, currentmessage)
        currentmessage = ""
        if player1.turn < 2:
            playerturn(goblinmonster, player1, difficulty)
            if player1.loot != None:
                playerloot(player1)

        if player1.turn >= 2:
            monsterturn(goblinmonster, player1, player1.score)
            player1.turn = 0
            displayboard(player1, goblinmonster, currentmessage)

        if shopcountdown == shopturns:
            shopphase(player1)
        mainClock.tick(60)

        # game over screen in progress
    create_game_over(player1.score)


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


# This reads the high scores text file and saves the integers into an array
def read_scores(filename):
    with open(filename) as f:
        return [int(x) for x in f]  # Converts them to integers before storing in array


def highscores():
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
        arr.sort(reverse=True)
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
