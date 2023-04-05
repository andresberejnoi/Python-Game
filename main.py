'''Some of the code was adapted from these tutorials:
        * https://www.youtube.com/watch?v=OAH8K5lVYOU&ab_channel=CodingWithRuss
        * https://www.youtube.com/watch?v=sVbFS9qEl4Y&ab_channel=ScriptLineStudios
'''
import pygame
import sys

import agents


pygame.init()

clock = pygame.time.Clock()
FPS   = 60


#-- Define Window Size and Create Screen
SCREEN_WIDTH  = 960
SCREEN_HEIGHT = 540 

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Prototype Survival Game")

#-- Define the player object
player = agents.Player(screen=screen)

#-- Main loop
keep_running = True

while keep_running:
    screen.fill((100,200,100))
    clock.tick(FPS)

    # handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            keep_running = False
            #sys.quit()

    #-- collect pressed keys and check if motion was used
    keys_pressed = pygame.key.get_pressed()

    if keys_pressed[pygame.K_a]:
        print(chr(pygame.K_a)) 
    if keys_pressed[pygame.K_d]:
        print(chr(pygame.K_d)) 
    if keys_pressed[pygame.K_w]:
        print(chr(pygame.K_w)) 
    if keys_pressed[pygame.K_s]:
        print(chr(pygame.K_s))

    #-- Handle camera updates

    #-- draw the playr
    player.update(screen)

    pygame.display.update()

pygame.quit()