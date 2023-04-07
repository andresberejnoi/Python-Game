import pygame
import agents
import objects
import spritesheet
import random
import os


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group, image) -> None:
        super().__init__(group)
        self.pos = pos
        self.image = image

        self.rect = self.image.get_rect(center=pos)
        self.direction = pygame.math.Vector2()
        self.speed = 3

    def input(self):
        keys_pressed = pygame.key.get_pressed()

        if keys_pressed[pygame.K_a]:
            self.direction.x = -1
        elif keys_pressed[pygame.K_d]:
            self.direction.x = 1
        else:
            self.direction.x = 0

        if keys_pressed[pygame.K_w]:
            self.direction.y = -1
        elif keys_pressed[pygame.K_s]:
            self.direction.y = 1 
        else:
            self.direction.y = 0

    def update(self):
        self.input()
        self.rect.center += self.direction * self.speed


class Rock(pygame.sprite.Sprite):
    def __init__(self, pos, group, image):
        super().__init__(group)
        self.pos = pos

        #self.image = pygame.image.load(os.path.join(graphics_folder, "rock.png")).convert_alpha()
        self.image = image
        self.rect =  self.image.get_rect(topleft = pos)


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

        #-- camera offset to account for player motion and keep it always centered
        self.camera_offset      = pygame.math.Vector2()
        self.half_screen_width  = self.display_surface.get_size()[0] // 2
        self.half_screen_height = self.display_surface.get_size()[1] // 2
    
    def center_camera_on_target(self, target):
        self.camera_offset.x = target.rect.centerx - self.half_screen_width
        self.camera_offset.y = target.rect.centery - self.half_screen_height

    def custom_draw(self, player):
        
        self.center_camera_on_target(player)
        
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):  #sort sprites by their y-position
            offset_vector = sprite.rect.topleft - self.camera_offset
            self.display_surface.blit(sprite.image, offset_vector) 

#=======================
WHITE = (255, 255, 255)
BLACK = (  0,   0,   0)

#=======================
graphics_folder = "sprites"
pygame.init()
clock = pygame.time.Clock()
FPS   = 60

#========================
#
SCREEN_WIDTH  = 960
SCREEN_HEIGHT = 540 
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#========================
#-- Load Spritesheet
_player_spritesheet_img  = pygame.image.load(os.path.join(graphics_folder, "human_regular_hair.png")).convert_alpha()
_rock_spritesheet_img    = pygame.image.load(os.path.join(graphics_folder,"rock.png")).convert_alpha()

player_spritesheet = spritesheet.SpriteSheet(_player_spritesheet_img, single_width=20, single_height=20)
rock_spritesheet   = spritesheet.SpriteSheet(_rock_spritesheet_img, single_width=25, single_height=25)

#
camera_group = CameraGroup()

player_sprite = player_spritesheet.get_image((0,0), scale=3)
rock_sprite   = rock_spritesheet.get_image((0,0), scale=3, chromakey=WHITE)
player = Player((0,0), camera_group, image=player_sprite)

for i in range(20):
    rand_x = random.randint(0,1300)
    rand_y = random.randint(0,1300)
    Rock((rand_x, rand_y), camera_group, image=rock_sprite)

#========================
# MAIN LOOP
keep_running = True
while keep_running:
    screen.fill((100,200,100))
    clock.tick(FPS)

    # handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            keep_running = False

    #screen.blit(player_sprite, (0,0))

    camera_group.update()
    camera_group.custom_draw(player)

    pygame.display.update()

pygame.quit()
