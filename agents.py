import pygame
import spritesheet

class BaseAgent(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_group, image, spritesheet=None, animation_speed=None):
        super.__init__(groups)

        self.image = image
        self.spritesheet = spritesheet

        #-- Rectangle and position elements
        self.rect = self.image.get_rect(center = pos)
        self.pos  = pygame.math.Vector2(self.rect.center)

        #-- Collision elements
        self.collision_group = collision_group
        self._hitbox_shrink_x_factor = 0.15
        self._hitbox_shrink_y_factor = 0.80
        self.hitbox_rect = self.rect.copy().inflate(-self.rect.width * self._hitbox_shrink_x_factor,  #make hitbox rect slightly smaller than image rect
                                                    -self.rect.height * self._hitbox_shrink_y_factor)
        
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

    def _extract_sprite_sequence(self, scale=3):
        return self.spritesheet.get_all_sprites(scale=3)
    
    def collision_calculation(self, direction='horizontal'):
        for sprite in self.collision_group.sprites():
            pygame.draw.rect(screen, RED, sprite.hitbox_rect, 1)
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
