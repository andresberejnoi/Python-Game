import pygame
import spritesheet
from config import *
from base_sprite import PrimordialSprite

#class BaseAgent(pygame.sprite.Sprite):
class BaseAgent(PrimordialSprite):
    def __init__(self, pos, groups, collision_group, image = None, spritesheet = None, animation_speed = None, hitbox_shrink_factor = (0.3, 0.85), **kwargs):
        super().__init__(pos=pos, 
                         groups=groups, 
                         image=image, 
                         spritesheet=spritesheet, 
                         animation_speed=animation_speed, 
                         hitbox_shrink_factor=hitbox_shrink_factor, 
                         **kwargs)

        #-- Collision elements
        self.collision_group = collision_group
        
        #-- Motion and speed elements
        self.direction = pygame.math.Vector2()
        self.speed     = kwargs.get('speed', 3)


    def collision_calculation(self, direction='horizontal'):
        for sprite in self.collision_group.sprites():
            if sprite.hitbox_rect.colliderect(self.hitbox_rect):
                if direction == 'horizontal':
                    if self.direction.x < 0:   #player was moving right to left
                        self.hitbox_rect.left = sprite.hitbox_rect.right

                    elif self.direction.x > 0:  #player was moving left to right
                        self.hitbox_rect.right = sprite.hitbox_rect.left

                    self.rect.centerx = self.hitbox_rect.centerx
                    self.pos.x        = self.hitbox_rect.centerx

                elif direction == 'vertical':
                    if self.direction.y < 0: #player was moving from bottom to top
                        self.hitbox_rect.top = sprite.hitbox_rect.bottom 

                    elif self.direction.y > 0: #player was moving from top to bottom
                        self.hitbox_rect.bottom = sprite.hitbox_rect.top

                    self.rect.centery = self.hitbox_rect.bottom - self.rect.height // 2
                    self.pos.y        = self.hitbox_rect.bottom - self.rect.height // 2

    def _animation_control(self):
       
        self.frames_per_animation_step = 4 // self._animation_speed
        full_cycle_frames = self.frames_per_animation_step * len(self._sprites_sequence)

        #-- check if player is currently standing still
        if self.direction.y == 0 and self.direction.x == 0:
            self.image = self._sprites_sequence[self._idle_sprite_idx]
            self._animation_step = 0
        
        else:
            self._sprite_idx = self._animation_step // self.frames_per_animation_step
            self.image = self._sprites_sequence[self._sprite_idx]
            self._animation_step = (self._animation_step + 1) % full_cycle_frames

        #-- keep character sprite facing the mouse x position
        mouse_x_pos = pygame.mouse.get_pos()[0]
        if mouse_x_pos < pygame.display.get_window_size()[0] // 2:
            self.image = pygame.transform.flip(self.image, flip_x = True, flip_y=False,).convert_alpha()


class Player(BaseAgent):
    def __init__(self, pos, groups, collision_group, image=None, spritesheet=None, animation_speed=1, **kwargs):
        super().__init__(pos=pos, 
                         groups=groups, 
                         collision_group=collision_group, 
                         image=image, spritesheet=spritesheet, 
                         animation_speed=animation_speed,   
                         **kwargs)

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

        #-- Update coordinates in HORIZONTAL direction
        self.pos.x += self.direction.x * self.speed
        self.hitbox_rect.centerx = round(self.pos.x)
        self.rect.centerx = self.hitbox_rect.centerx

        self.collision_calculation(direction='horizontal')

        #-- Update coordinates in VERTICAL direction
        self.pos.y += self.direction.y * self.speed
        self.rect.centery = round(self.pos.y)
        self.hitbox_rect.bottom = self.rect.bottom

        self.collision_calculation(direction='vertical')

        #-- Update sprite based on animation sequence
        self._animation_control()
        

    

        