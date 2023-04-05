'''
Some of the code was adapted from these tutorials:
    * https://www.youtube.com/watch?v=OAH8K5lVYOU&ab_channel=CodingWithRuss
    * https://www.youtube.com/watch?v=sVbFS9qEl4Y&ab_channel=ScriptLineStudios

I read the answers to the following StackOverflow question to get a better idea of how to implement a 
camera system:
https://stackoverflow.com/questions/67526781/trying-to-make-screen-center-to-player-in-pygame-simple-2d-platformer
'''
import pygame
import sys

import agents
import objects


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

#-- Random objects for testing
objects = [objects.Rock(screen) for i in range(10)]

#-- CAMERA SETUP
camera = pygame.math.Vector2((0,0))

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
    # in the main loop: adjust the camera position to center the player
    camera.x = player.x - SCREEN_WIDTH / 2
    camera.y = player.y - SCREEN_HEIGHT / 2
    
    #-- draw the playr
    player.update(screen)

    for item in objects:
        item.update(screen)

    pygame.display.update()

pygame.quit()