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
pygame.display.set_caption('Mekaneks')

# main font (currently system default)
font = pygame.font.SysFont(None, 20)
small_button_font = pygame.font.SysFont(None, 12)

click = False

robot_image = pygame.image.load('Robby.png')
robot_image = pygame.transform.scale(robot_image, (62, 62))


def robot(x, y):
    screen.blit(robot_image, (x, y))


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
        text_play = font.render('Mechaneks', True, (255, 255, 255))
        # screen.blit(text_play, (0,0))
        # Fill black
        screen.fill((0, 0, 0))
        # button creations
        #Rect(left pos, top pos, width, height)
        button_play = pygame.Rect(200, 200, 200, 50)
        button_options = pygame.Rect(200, 300, 200, 50)
        button_exit = pygame.Rect(200, 400, 200, 50)
        pygame.draw.rect(screen, (255, 0, 0), button_play)
        pygame.draw.rect(screen, (255, 0, 0), button_options)
        pygame.draw.rect(screen, (255, 0, 0), button_exit)
        pygame.draw.rect(screen, (255, 0, 0), button_play)
        #text for buttons
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


def playersetup():
    playerdrawdeck = deckcardplayerclasses.Deck(cardlib.startingcards())
    playerdrawdeck.shuffle()
    playerdiscarddeck = deckcardplayerclasses.Deck([])
    playertrashdeck = deckcardplayerclasses.Deck([])
    player = deckcardplayerclasses.Player(playerdrawdeck, playerdiscarddeck, playertrashdeck)
    return player


def playerturn(player):
    turn = 0  # player is able to play 2 cards before monsters act and before they redraw, hence the need for a loop.
    while turn < 2:
        # todo have player able to click card in hand, return index of card in player.hand
        # player.playcard(index)
        # todo if the player kills a monster, call cardlib.randcard and give the player the option to add card to deck
        turn = turn + 1


# if len(player.hand) < 3:
# while player.hand < 5:
# player.draw()

# def monsterturn(turncount, player):
# todo if there is no monster on the grid, spawn a monster in a random space
# if turncount % 3 == 0: # could be every 2 monster turns instead of 3. Playtest? Might not matter.
# todo spawn a monster
# todo for each monster:
# todo if adjacent to the player:
# player.damage(1)
# todo else the monster moves 1 space closer to the player



def game():
    
    x = 0
    y = 0

    mx, my = pygame.mouse.get_pos()
    click = False
    running = True
    while running:
        screen.fill((0, 0, 0))
        button_conv_wheels = pygame.Rect(50, 550, 75, 25)
        button_pointed_stick = pygame.Rect(200, 550, 75, 25)
        button_scrap_armor = pygame.Rect(350, 550, 75, 25)
        button_stick_lobber = pygame.Rect(500, 550, 75 , 25)
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
        #img_conv_wheels = pygame.image.load(r'conveyorWheels.png')
        #img_pointed_stick = pygame.image.load(r'pointedStick.png')
        #img_scrap_armor = pygame.image.load(r'scrapArmor.png')
        #img_stick_lobber = pygame.image.load(r'stickLobber.png')
        #screen.blit(img_conv_wheels, (0,0))
        #screen.blit(img_pointed_stick, (0,150))
        #screen.blit(img_scrap_armor, (0,300))
        #screen.blit(img_stick_lobber, (0,400))
        #pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                click = True
                if button_conv_wheels.collidepoint(mx, my):
                    if click:
                        #replace with move
                        exit()
                if button_pointed_stick.collidepoint(mx, my):
                    if click:
                        #replace with move
                        exit()
                if button_scrap_armor(mx, my):
                    if click:
                        #replace with move
                        exit()
                if button_scrap_armor(mx, my):
                    if click:
                        #replace with move
                        exit()
            if event.type == pygame.MOUSEBUTTONUP:
                x_temp, y_temp = pygame.mouse.get_pos()
                x_temp, y_temp = grid.get_location(x_temp, y_temp)
                if x_temp <= 316:
                    if y_temp <= 316:
                        x = x_temp
                        y = y_temp

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit()
        # Print the grid to the screen

        screen.blit(grid.grid(), [0, 0])
        robot(x, y)

        pygame.display.flip()
        pygame.display.update()
        # mainClock.tick(60)
        # player1 = playersetup()
        # turncount = 0
        # while player1.isalive == 1:
        # playerturn(player1)
        # monsterturn(turncount, player1)


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
