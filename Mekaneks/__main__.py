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
    playerxcoord = 0
    playerycoord = 0
    player = deckcardplayerclasses.Player(playerdrawdeck, playerdiscarddeck, playertrashdeck, playerxcoord, playerycoord)
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
    card_images = ['conveyorWheels.png', 'pointedStick.png', 'scrapArmor.png', 'stickLobber.png']
    card_width = 1771
    card_length = 2633
    card_scale_factor = 0.05
    card_scaled_width = int(card_scale_factor*card_width)
    card_scaled_length = int(card_scale_factor*card_length)

    while True:
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
        #conv_wheels_image, draw a transparent rectangle behind an image to be able to use collidepoint
        img_conv_wheels_surface = pygame.Rect(45, 415, card_scaled_width, card_scaled_length)
        pygame.draw.rect(screen, (0,0,0), img_conv_wheels_surface, 1)
        img_conv_wheels = pygame.image.load(card_images[0])
        img_conv_wheels = pygame.transform.scale(img_conv_wheels, (card_scaled_width, card_scaled_length))
        #pointed_stick_image
        img_pointed_stick_surface = pygame.Rect(195, 415, card_scaled_width, card_scaled_length)
        pygame.draw.rect(screen, (0,0,0), img_pointed_stick_surface, 1)
        img_pointed_stick = pygame.image.load(card_images[1])
        img_pointed_stick = pygame.transform.scale(img_pointed_stick, (card_scaled_width, card_scaled_length))
        #scrap_armor_image
        img_scrap_armor_surface = pygame.Rect(345, 415, card_scaled_width, card_scaled_length)
        pygame.draw.rect(screen, (0,0,0), img_scrap_armor_surface, 1)
        img_scrap_armor = pygame.image.load(card_images[2])
        img_scrap_armor = pygame.transform.scale(img_scrap_armor, (card_scaled_width, card_scaled_length))
        #stick_lobber_imaaage
        img_stick_lobber_surface = pygame.Rect(495, 415, card_scaled_width, card_scaled_length)
        pygame.draw.rect(screen, (0,0,0), img_stick_lobber_surface, 1)
        img_stick_lobber = pygame.image.load(card_images[3])
        img_stick_lobber = pygame.transform.scale(img_stick_lobber, (card_scaled_width, card_scaled_length))
        #blit images
        screen.blit(img_conv_wheels, (45,415))
        screen.blit(img_pointed_stick, (195,415))
        screen.blit(img_scrap_armor, (345,415))
        screen.blit(img_stick_lobber, (495,415))
        for event in pygame.event.get():
            mx, my = pygame.mouse.get_pos()
            click = False
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                click = True
                if img_conv_wheels_surface.collidepoint(mx, my):
                    if click:
                        #replace
                        exit()
                if img_pointed_stick_surface.collidepoint(mx, my):
                    if click:
                        exit()
                        #replace
                if img_scrap_armor_surface.collidepoint(mx, my):
                    if click:
                        #replace
                        exit()
                if img_stick_lobber_surface.collidepoint(mx, my):
                    if click:
                        #replace
                        exit()
                if button_conv_wheels.collidepoint(mx, my):
                    if click:
                        #replace
                        exit()
                if button_pointed_stick.collidepoint(mx, my):
                    if click:
                        #replace with move
                        exit()
                if button_scrap_armor.collidepoint(mx, my):
                    if click:
                        #replace with move
                        exit()
                if button_stick_lobber.collidepoint(mx, my):
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
        player1 = playersetup()
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
