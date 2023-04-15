import pygame
import agents
from objects import Rock
from sound import SoundMaster
import spritesheet
from camera import Camera
from config import *


import os

#==================================
#-- Initialize Pygame
pygame.mixer.pre_init(44100, size=-16, channels=2, buffer=512)
pygame.init()
pygame.mixer.init()

#-- Set cursor image
pygame.mouse.set_cursor(*pygame.cursors.broken_x)

#-- Setup the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Prototype Survival Game")

#-- Setup the clock
clock = pygame.time.Clock()

#==================================
#-- Groups
camera_group    = Camera()  #pygame.sprite.Group()
collision_group = pygame.sprite.Group()

#==================================
#-- Sound Section
sound_master = SoundMaster()
sound_files  = ['walking_gravel.ogg']
for sound in sound_files:
    sound_master.add_sound('player_walking', sound)

sound_walking = pygame.mixer.Sound(os.path.join(SOUNDS_FOLDER, 'walking_gravel.ogg'))

print(sound_master.sounds)
#==================================
#-- Preparing sprites and related stuff
player_spritesheet = spritesheet.SpriteSheet.load_from_file(os.path.join(GRAPHICS_FOLDER, "human_regular_hair.png"),
                                                            single_width=20,
                                                            single_height=20,
                                                            num_cols=3)

rock_spritesheet = spritesheet.SpriteSheet.load_from_file(os.path.join(GRAPHICS_FOLDER, "rock.png"),
                                                          single_width=25,
                                                          single_height=25)

#img_rock = rock_spritesheet.get_image((0,0), scale=2, chromakey=WHITE)

#==================================
#-- Initialize player, agents, and objects
player = agents.Player(
    pos             = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2), 
    groups          = camera_group, 
    collision_group = collision_group, 
    spritesheet     = player_spritesheet,
    sprite_scale    = 2,
    speed           = 3,

    sound_master    = sound_master,
)

rock_locations = [
    (400, 150),
    (700, 100),
    (500, 400),
    (150, 450),
    (256, 256),
]

rocks = []
for pos in rock_locations:
    rock = Rock(
        pos=pos, 
        groups=[camera_group, collision_group], 
        spritesheet=rock_spritesheet, 
        sprite_scale=3,
        sprite_chromakey=WHITE
    )
    rocks.append(rock)

#==========================================
#--------------MAIN GAME LOOP--------------
keep_running = True

while keep_running:
    screen.fill(SCREEN_FILL)
    clock.tick(FPS)

    #===========================
    #-- handle events
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            keep_running = False

        # detect zoom from mousewheel
        elif event.type == pygame.MOUSEWHEEL:
            camera_group.zoom_level += event.y * 0.03

        elif event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d]:
                sound_walking.play()
        
        elif event.type == pygame.KEYUP:
            if event.key in [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d]:
                sound_walking.stop()
    #===========================
    #-- Display
    #screen.blit(player.image, player.pos, player.rect)
    camera_group.update()
    #camera_group.custom_draw(player)
    camera_group.custom_draw_with_zoom(player)
    
    #===========================
    #-- Update display at the end of each loop
    pygame.display.update()

pygame.quit()