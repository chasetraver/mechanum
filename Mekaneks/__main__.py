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

click = False


def main_menu():
    while True:
        # button texts
        text_play = font.render('Mechaneks', True, (255,255,255))
        # screen.blit(text_play, (0,0))
        # Fill black
        screen.fill((0,0,0))
        # button creations
        button_play = pygame.Rect(200, 200, 200, 50)
        button_options = pygame.Rect(200, 300, 200, 50)
        button_exit = pygame.Rect(200, 400, 200, 50)
        pygame.draw.rect(screen, (255,0,0), button_play)
        pygame.draw.rect(screen, (255,0,0), button_options)
        pygame.draw.rect(screen, (255,0,0), button_exit)
        pygame.draw.rect(screen, (255,0,0), button_play)
        button_play_msg = "Play"
        button_opt_msg = "Options"
        button_quit_msg = "Quit"
        button_play_txt = font.render(button_play_msg, True, (255,255,255))
        button_opt_txt = font.render(button_opt_msg, True, (255,255,255))
        button_quit_txt = font.render(button_quit_msg, True, (255,255,255))
        screen.blit(button_play_txt, (285,220))
        screen.blit(button_opt_txt, (285,320))
        screen.blit(button_quit_txt, (285,420))

        for event in pygame.event.get():
            mx, my = pygame.mouse.get_pos()
            click = False
            if event.type == pygame.QUIT:
                exit()
            # event - left mousebutton clicked (button actions)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                click = True
                if button_play.collidepoint(mx,my):
                    if click:
                        game()
                if button_options.collidepoint(mx,my):
                    if click:
                        options()
                if button_exit.collidepoint(mx,my):
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
    turn = 0 # player is able to play 2 cards before monsters act and before they redraw, hence the need for a loop.
    while turn < 2:
        # todo have player able to click card in hand, return index of card in player.hand
        player.playcard(index)
        turn = turn + 1
    if len(player.hand) < 3:
        while player.hand < 5:
            player.draw()

def monsterturn(turncount, player):
    # todo if there is no monster on the grid, spawn a monster in a random space
    if turncount % 3 == 0: # could be every 2 monster turns instead of 3. Playtest? Might not matter.
        #todo spawn a monster
    #todo for each monster:
    #todo if adjacent to the player:
    player.damage(1)
    #todo else the monster moves 1 space closer to the player

def game():
    running = True
    while running:
        screen.fill((0,0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit()
        # Print the grid to the screen
        screen.blit(grid.grid(), [0, 0])
        pygame.display.flip()
        pygame.display.update()
        mainClock.tick(60)
        player1 = playersetup()
        turncount = 0
        while player1.isalive == 1:
            playerturn(player1)
            monsterturn(turncount, player1)

def options():
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
        pygame.display.flip()
        pygame.display.update()
        mainClock.tick(60)


def exit():
    pygame.quit()
    sys.exit()


main_menu()