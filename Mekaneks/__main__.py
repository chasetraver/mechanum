import pygame
import grid
import sys

# initialize game engine and open a window
mainClock = pygame.time.Clock()
pygame.init()
window_width = 600
window_height = 600
# window settings
display_size = (window_width, window_height)
screen = pygame.display.set_mode(display_size)
pygame.display.set_caption('Mekaneks')

#main font (currently system default)
font = pygame.font.SysFont(None, 20)

click = False

def main_menu():
    while True:
        #button texts
        text_play = font.render('Mechaneks', True, (255,255,255))
        #screen.blit(text_play, (0,0))
        #Fill black
        screen.fill((0,0,0))
        #button creations
        button_play = pygame.Rect(200, 200, 200, 50)
        button_options = pygame.Rect(200, 300, 200, 50)
        button_exit = pygame.Rect(200, 400, 200, 50)
        pygame.draw.rect(screen, (255,0,0), button_play)
        pygame.draw.rect(screen, (255,0,0), button_options)
        pygame.draw.rect(screen, (255,0,0), button_exit)
        pygame.draw.rect(screen, (255,0,0), button_play)

        for event in pygame.event.get():
            mx, my = pygame.mouse.get_pos()
            click = False
            if event.type == pygame.QUIT:
                exit()
            #event - left mousebutton clicked (button actions)
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
            #call exit function on Esc key
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit()
        pygame.display.update()
        mainClock.tick(60)

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
        #Print the grid to the screen
        screen.blit(grid.grid(), [0, 0])
        pygame.display.flip()
        pygame.display.update()
        mainClock.tick(60)

def options():
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
        #Print the grid to the screen
        screen.blit(grid.grid(), [0, 0])
        pygame.display.flip()
        pygame.display.update()
        mainClock.tick(60)

def exit():
    pygame.quit()
    sys.exit()

main_menu()