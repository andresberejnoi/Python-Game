import pygame
from config import *
from base_sprite import PrimordialSprite

#class BaseObject(pygame.sprite.Sprite):
class BaseObject(PrimordialSprite):
    def __init__(self, pos, groups, image=None, spritesheet = None, animation_speed = 1, **kwargs):
        super().__init__(pos=pos, 
                         groups=groups, 
                         image=image, 
                         spritesheet = spritesheet, 
                         animation_speed = animation_speed, 
                         **kwargs)


class Rock(BaseObject):
    def __init__(self, pos, groups, image=None, spritesheet=None, animation_speed=1, **kwargs):
        super().__init__(pos=pos, 
                         groups=groups, 
                         image=image, 
                         spritesheet=spritesheet, 
                         animation_speed=animation_speed, 
                         hitbox_shrink_factor=(0.35,0.85), 
                         **kwargs)
        
    def update(self, events=None):
        if events is not None:
            for event in events:
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:   #if left click was pressed
                    print(event)
                    if self.hitbox_rect.collidepoint(event.pos):
                        print("rock has been clicked!!")
                        self.kill() 

        