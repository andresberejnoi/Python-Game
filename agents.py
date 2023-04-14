import pygame
import spritesheet
from config import *

class BaseAgent(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_group, image=None, spritesheet=None, animation_speed=None):
        super().__init__(groups)

        if image is None:
            self.image = spritesheet.get_image((0,0), scale=3)
        self.spritesheet = spritesheet

        #-- Rectangle and position elements
        self.rect = self.image.get_rect(center = pos)
        #self.rect = self.image.get_rect(topleft = pos)
        self.pos  = pygame.math.Vector2(self.rect.center)

        #-- Collision elements
        self.collision_group = collision_group
        self._hitbox_shrink_x_factor = 0.35
        self._hitbox_shrink_y_factor = 0.80
        self._hitbox_rect = self.rect.copy().inflate(-self.rect.width * self._hitbox_shrink_x_factor,  #make hitbox rect slightly smaller than image rect
                                                    -self.rect.height * self._hitbox_shrink_y_factor)
        
        self.test_rect = self.rect.copy().inflate(-self.rect.width * self._hitbox_shrink_x_factor,  #make hitbox rect slightly smaller than image rect
                                                  -self.rect.height * self._hitbox_shrink_y_factor)
        self.test_rect.bottom = self.rect.bottom

        #-- Motion and speed elements
        self.direction = pygame.math.Vector2()
        self.speed     = 3

        #-- Animation elements
        self._animation_speed  = animation_speed or 1
        self._animation_step   = 0
        self._idle_sprite_idx  = 0
        self._sprite_idx       = 0
        self._frame_idx        = 0
        self._sprites_sequence = self._extract_sprite_sequence(scale=3)

    @property
    def hitbox_rect(self):
        return self._hitbox_rect
    
    # @hitbox_rect.setter
    # def hitbox_rect(self, new_rect):


    def _extract_sprite_sequence(self, scale=3):
        if self.spritesheet:
            return self.spritesheet.get_all_sprites(scale=3)
        else:
            return []
        
    @property
    def frames_per_animation_step(self):
        return self._frames_per_animation_step
    
    @frames_per_animation_step.setter
    def frames_per_animation_step(self, new_val):
        if new_val < 1:
            pass#no change, use current value
        else:
            self._frames_per_animation_step = new_val


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

                    self.rect.centery = self.hitbox_rect.centery
                    self.pos.y        = self.hitbox_rect.centery


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
        if mouse_x_pos < self.pos.x:
            self.image = pygame.transform.flip(self.image, flip_x = True, flip_y=False,).convert_alpha()

class Player(BaseAgent):
    def __init__(self, pos, groups, collision_group, image=None, spritesheet=None, animation_speed=1):
        super().__init__(pos, groups, collision_group, image, spritesheet, animation_speed)

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

        self.test_rect.centerx = self.rect.centerx

        self.collision_calculation(direction='horizontal')

        #-- Update coordinates in VERTICAL direction
        self.pos.y += self.direction.y * self.speed
        self.hitbox_rect.centery = round(self.pos.y)
        self.rect.centery = self.hitbox_rect.centery


        self.test_rect.bottom = self.rect.bottom

        self.collision_calculation(direction='vertical')

        #-- Update sprite based on animation sequence
        self._animation_control()
        

    

        