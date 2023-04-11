"""

Credits and Resources
---------------------

I followed a tutorial that helped me implement a camera
that follows the player and can zoom in and out.
Here is the link:
    * https://youtu.be/u7LPRqrzry8
"""

import pygame
import agents
import objects
import spritesheet
import random
import os


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group, image, sprite_sheet=None, animation_speed=None,) -> None:
        super().__init__(group)
        #self.pos = pos
        self.image = image
        self.sprite_sheet = sprite_sheet   #contains a SpriteSheet object with different frames for animation

        self.rect = self.image.get_rect(center=pos)
        self.direction = pygame.math.Vector2()
        self.speed = 3

        #-- Variables that control animation
        self._animation_step     = 0
        self._sprite_idx         = 0
        self._animation_speed    = animation_speed or 2
        self._frame_idx          = 0
        self._standing_image_idx = 0   #index for default image when character is not moving
        self.sprites_sequence    = self._extract_sprite_sequence(scale=3)
        #self._frames_per_animation_step = 

    def _extract_sprite_sequence(self, scale=3):
        return self.sprite_sheet.get_all_sprites(scale=3)

    def keyboard_input(self):
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

    def update(self, events=None):
        self.keyboard_input()
        self.rect.center += self.direction * self.speed


        frames_per_animation_step = 5 // self._animation_speed
        if frames_per_animation_step < 1:
            frames_per_animation_step = 5

        full_cycle_frames = frames_per_animation_step * len(self.sprites_sequence)
        

        #self._animation_step += 1
        full_cycle_frames = FPS // self._animation_speed

        full_cycle_frames += full_cycle_frames % len(self.sprites_sequence)  #make sure that there are always enough frames in a cycle for all sprites 
        
        assert(full_cycle_frames >= len(self.sprites_sequence))
        assert(full_cycle_frames % len(self.sprites_sequence) == 0)

        frames_per_animation_step = full_cycle_frames // len(self.sprites_sequence)
        
        #-- check if player is currently standing still
        if self.direction.y == 0 and self.direction.x == 0:
            self.image = self.sprites_sequence[self._standing_image_idx]
            self._animation_step = 0

        else:
            # if self._animation_step % frames_per_animation_step:
            #     pass
            # self._sprite_idx = (self._sprite_idx + 1) % len(self.sprites_sequence)  #make sure sprite index is never greater than total available sprites, so they can cycle through
            try:
                print(f"Full Cycle Frames:{full_cycle_frames}\n",
                      f"Animation Step: {self._animation_step}\n",
                      f"Frames per animation step: {frames_per_animation_step}\n", 
                      f"Sprite Index: {self._sprite_idx}\n")
                
                self._sprite_idx = self._animation_step // frames_per_animation_step
                self.image = self.sprites_sequence[self._sprite_idx]

            except IndexError:
                print("ERROR WITH SPRITE_INDEX OUT OF BOUNDS!\n")


            self._animation_step = (self._animation_step + 1) % full_cycle_frames   #animation step will always stay within the allowed frames per cycle



class Rock(pygame.sprite.Sprite):
    def __init__(self, pos, group, image):
        super().__init__(group)
        #self.pos = pos

        #self.image = pygame.image.load(os.path.join(graphics_folder, "rock.png")).convert_alpha()
        self.image = image
        self.rect =  self.image.get_rect(topleft = pos)

    def update(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                if self.rect.collidepoint(event.pos):
                    self.is_clicked()
    
    def is_clicked(self):
        print(f"Rock {self} was clicked!")


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

        #-- camera offset to account for player motion and keep it always centered
        self.camera_offset      = pygame.math.Vector2()
        self.half_screen_width  = self.display_surface.get_size()[0] // 2
        self.half_screen_height = self.display_surface.get_size()[1] // 2

        #-- Zoom control
        self.zoom_level = 1
        self.internal_surface_size = (1500,1500)  #it will be used to zoom out. It should be big enough to contain the map and zoom out levels
        self.internal_surface = pygame.Surface(self.internal_surface_size, pygame.SRCALPHA)
        self.internal_rect    = self.internal_surface.get_rect(center = (self.half_screen_width, self.half_screen_height))
        self.internal_surface_size_vector = pygame.math.Vector2(self.internal_surface_size)
        self.internal_offset  = pygame.math.Vector2()
        self.internal_offset.x = self.internal_surface_size[0] // 2 - self.half_screen_width
        self.internal_offset.y = self.internal_surface_size[1] // 2 - self.half_screen_height

    def center_camera_on_target(self, target):
        self.camera_offset.x = target.rect.centerx - self.half_screen_width
        self.camera_offset.y = target.rect.centery - self.half_screen_height

    @staticmethod
    def zoom_guard(current_zoom, delta_zoom, min_zoom = 0.7, max_zoom = 3):
        '''Make sure zoom levels always stay within min and max values. Take original value and return a new value within parameters.'''

        new_zoom = current_zoom + delta_zoom
        if new_zoom >= min_zoom and new_zoom <= max_zoom:
            return new_zoom
        
        if new_zoom < min_zoom:
            return min_zoom
        elif new_zoom > max_zoom:
            return max_zoom
            
    def set_zoom_level(self, new_zoom):
        self.zoom_level = new_zoom

    def zoom_keys(self):
        keys_pressed = pygame.key.get_pressed()

        if keys_pressed[pygame.K_q]:
            delta_zoom = 0.1
            #self.zoom_level = max(4, self.zoom_level + delta_zoom)
            safe_zoom = self.zoom_guard(self.zoom_level, delta_zoom, min_zoom=0.7, max_zoom=3)
            self.set_zoom_level(safe_zoom)

        elif keys_pressed[pygame.K_e]:
            delta_zoom = -0.1
            #self.zoom_level = max(0.5, self.zoom_level + delta_zoom)
            safe_zoom = self.zoom_guard(self.zoom_level, delta_zoom, min_zoom=0.7, max_zoom=3)
            self.set_zoom_level(safe_zoom)

    def custom_draw(self, player):

        self.center_camera_on_target(player)
        self.zoom_keys()
        
        self.internal_surface.fill(SCREEN_FILL)

        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):  #sort sprites by their y-position
            offset_vector = sprite.rect.topleft - self.camera_offset + self.internal_offset
            self.internal_surface.blit(sprite.image, offset_vector) 
            pygame.draw.rect(self.internal_surface, RED, [0,0, sprite.rect.w, sprite.rect.h])

        scaled_surface = pygame.transform.scale(self.internal_surface, self.internal_surface_size_vector * self.zoom_level)
        scaled_rect    = scaled_surface.get_rect(center = (self.half_screen_width, self.half_screen_height))

        #-- draw regular display onto zoom display
        self.display_surface.blit(scaled_surface, scaled_rect)

    def BACKUP_custom_draw(self, player):
        '''custom draw containing only the code to keep player centered and dynamic depth drawing. No zoom here.'''

        self.center_camera_on_target(player)
        self.zoom_keys()
        
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):  #sort sprites by their y-position
            offset_vector = sprite.rect.topleft - self.camera_offset
            self.display_surface.blit(sprite.image, offset_vector) 

#=======================
WHITE = (255, 255, 255)
BLACK = (  0,   0,   0)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)

SCREEN_FILL = (100,200,100)

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
pygame.display.set_caption("Prototype Survival Game")

#========================
#-- Load Spritesheet
# _player_spritesheet_img  = pygame.image.load(os.path.join(graphics_folder, "human_regular_hair.png")).convert_alpha()
# _rock_spritesheet_img    = pygame.image.load(os.path.join(graphics_folder,"rock.png")).convert_alpha()

player_spritesheet = spritesheet.SpriteSheet.load_from_file(os.path.join(graphics_folder, "human_regular_hair.png"),
                                                            single_width=20,
                                                            single_height=20)

rock_spritesheet = spritesheet.SpriteSheet.load_from_file(os.path.join(graphics_folder, "rock.png"),
                                                            single_width=25,
                                                            single_height=25)
# player_spritesheet = spritesheet.SpriteSheet(_player_spritesheet_img, single_width=20, single_height=20)
# rock_spritesheet   = spritesheet.SpriteSheet(_rock_spritesheet_img, single_width=25, single_height=25)

#
camera_group = CameraGroup()

player_sprite = player_spritesheet.get_image((2,0), scale=3, chromakey=BLACK)
rock_sprite   = rock_spritesheet.get_image((0,0), scale=6, chromakey=WHITE)
player = Player((0,0), camera_group, image=player_sprite, sprite_sheet=player_spritesheet)



frame_0 = player_spritesheet.get_image((0,0), scale=3)
frame_1 = player_spritesheet.get_image((1,0), scale=3)
frame_2 = player_spritesheet.get_image((2,0), scale=3)

rock_list = []
for i in range(5):
    rand_x = random.randint(0,1300)
    rand_y = random.randint(0,1300)
    rock_list.append(Rock((rand_x, rand_y), camera_group, image=rock_sprite))

#========================
# MAIN LOOP
keep_running = True
while keep_running:
    screen.fill(SCREEN_FILL)
    clock.tick(FPS)

    # handle events
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            keep_running = False

        # detect zoom from mousewheel
        elif event.type == pygame.MOUSEWHEEL:
            #camera_group.zoom_level += event.y * 0.03
            safe_zoom = camera_group.zoom_guard(camera_group.zoom_level, event.y * 0.1, min_zoom=0.7, max_zoom=3)
            camera_group.set_zoom_level(safe_zoom)
            #event.y = 0   

        elif event.type == pygame.MOUSEBUTTONUP: # and event.button == 1:   #if left click was pressed
            print(event)
            for rock in rock_list:
                print("Rock:", rock.rect.center)
                if rock.rect.collidepoint(event.pos):
                    print("rock has been clicked!!")
                    rock.kill() 

        # if pygame.mouse.get_pressed() == (True, False, False):    #left click was pressed
        #     mouse_pos = pygame.mouse.get_pos()
        #     for rock in rock_list:
        #         if rock.rect.collidepoint(mouse_pos):
        #             rock.kill()

    screen.blit(frame_0, (300,300))
    screen.blit(frame_1, (350,350))
    screen.blit(frame_2, (400,400))

    camera_group.update(events)
    camera_group.custom_draw(player)

    pygame.display.update()

pygame.quit()
