import pygame
import agents
import objects
import spritesheet
from config import *

#==================================
#-- Initialize Pygame
pygame.init()

#-- Setup the display
screen = pygame.display.set_mode((SCREEN_PARAMS['width'], SCREEN_PARAMS['height']))
pygame.display.set_caption("Prototype Survival Game")

#-- Setup the clock
clock = pygame.time.Clock()


#==================================
#----------MAIN GAME LOOP----------
keep_running = True

while keep_running:
    screen.fill(SCREEN_FILL)
    clock.tick(FPS)

    #-- handle events
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            keep_running = False

    
    #-- Update display at the end of each loop
    pygame.display.update()

pygame.quit()