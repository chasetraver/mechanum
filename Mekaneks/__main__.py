import pygame
import grid

# initialize game engine
pygame.init()

window_width = 600
window_height = 600

# Open a window
display_size = (window_width, window_height)
screen = pygame.display.set_mode(display_size)

# Set title to the window
pygame.display.set_caption('Mekaneks')

gameExit = False

while not gameExit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameExit = True

    # Print the grid to the screen
    screen.blit(grid.grid(), [0, 0])

    pygame.display.flip()
