import pygame

class PrimordialSprite(pygame.sprite.Sprite):
    def __init__(self, pos, groups, image=None, spritesheet=None, animation_speed=None, can_collide=True):
        super().__init__(groups)

        if image is None:
            if spritesheet is not None:
                self.image = spritesheet.get_image((0,0), scale=3)
            else:
                raise #placeholder until I decide best course of action here
        else:
            self.image = image
        self.spritesheet = spritesheet

        #-- Rectangle and position elements
        self.rect = self.image.get_rect(center = pos)
        #self.rect = self.image.get_rect(topleft = pos)
        self.pos  = pygame.math.Vector2(self.rect.center)

        #-- Collision elements
        self._hitbox_shrink_x_factor = 0.35
        self._hitbox_shrink_y_factor = 0.80
        self._hitbox_rect = self.rect.copy().inflate(-self.rect.width * self._hitbox_shrink_x_factor,  #make hitbox rect slightly smaller than image rect
                                                    -self.rect.height * self._hitbox_shrink_y_factor)
        
        self.test_rect = self.rect.copy().inflate(-self.rect.width * self._hitbox_shrink_x_factor,  #make hitbox rect slightly smaller than image rect
                                                  -self.rect.height * self._hitbox_shrink_y_factor)
        self.test_rect.bottom = self.rect.bottom

        #-- Animation elements
        self._animation_speed  = animation_speed or 1
        self._animation_step   = 0
        self._idle_sprite_idx  = 0
        self._sprite_idx       = 0
        self._frame_idx        = 0
        self._sprites_sequence = self._extract_sprite_sequence(scale=3)

    def _extract_sprite_sequence(self, scale=3):
        if self.spritesheet:
            return self.spritesheet.get_all_sprites(scale=scale)
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


