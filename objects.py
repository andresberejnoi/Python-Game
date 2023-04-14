import pygame
from config import *

class BaseObject(pygame.sprite.Sprite):
    def __init__(self, pos, groups, image, spritesheet = None, animation_speed = 1):
        super().__init__(groups)

        self.image = image or pygame.Surface((50,50))
        self.spritesheet = spritesheet

        #-- Rectangle and position elements
        self.rect = self.image.get_rect(center = pos)
        self.pos  = pygame.math.Vector2(self.rect.center)

        #-- Collision elements
        self._hitbox_shrink_x_factor = 0.15
        self._hitbox_shrink_y_factor = 0.80
        self.hitbox_rect = self.rect.copy().inflate(-self.rect.width * self._hitbox_shrink_x_factor,  #make hitbox rect slightly smaller than image rect
                                                    -self.rect.height * self._hitbox_shrink_y_factor)

        self.test_rect = self.rect.copy().inflate(-self.rect.width * self._hitbox_shrink_x_factor,  #make hitbox rect slightly smaller than image rect
                                                  -self.rect.height * self._hitbox_shrink_y_factor)
        self.test_rect.bottom = self.rect.bottom

class Rock(BaseObject):
    def __init__(self, pos, groups, image, spritesheet=None, animation_speed=1):
        super().__init__(pos, groups, image, spritesheet, animation_speed)

        