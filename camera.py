"""

Credits and Resources
---------------------

I followed a tutorial that helped me implement this camera
that follows the player and can zoom in and out.
Here is the link:
    * https://youtu.be/u7LPRqrzry8
"""

import pygame
from config import * 

class Camera(pygame.sprite.Group):
    def __init__(self, min_zoom=0.7, max_zoom=3):
        super().__init__()

        self.display_surface = pygame.display.get_surface()

        #-- camera offset to account for player motion and keep it always centered
        self.camera_offset      = pygame.math.Vector2()
        self.half_screen_width  = self.display_surface.get_size()[0] // 2
        self.half_screen_height = self.display_surface.get_size()[1] // 2

        #-- Zoom control
        self._zoom_level = 1
        self._min_zoom   = min_zoom
        self._max_zoom   = max_zoom
        self.internal_surface_size = (1500,1500)  #it will be used to zoom out. It should be big enough to contain the map and zoom out levels
        self.internal_surface = pygame.Surface(self.internal_surface_size, pygame.SRCALPHA)
        self.internal_rect    = self.internal_surface.get_rect(center = (self.half_screen_width, self.half_screen_height))
        self.internal_surface_size_vector = pygame.math.Vector2(self.internal_surface_size)
        self.internal_offset  = pygame.math.Vector2()
        self.internal_offset.x = self.internal_surface_size[0] // 2 - self.half_screen_width
        self.internal_offset.y = self.internal_surface_size[1] // 2 - self.half_screen_height

    @property
    def zoom_level(self):
        return self._zoom_level
    
    @zoom_level.setter
    def zoom_level(self, new_val):
        #new_val = current_zoom + delta_zoom
        if new_val >= self._min_zoom and new_val <= self._max_zoom:
            self._zoom_level = new_val
        
        elif new_val < self._min_zoom:
            self._zoom_level = self._min_zoom
        elif new_val > self._max_zoom:
            self._zoom_level = self._max_zoom

    def center_camera_on_target(self, target):
        self.camera_offset.x = target.rect.centerx - self.half_screen_width
        self.camera_offset.y = target.rect.centery - self.half_screen_height

    def custom_draw(self, player):
        self.center_camera_on_target(player)

        _sorted_sprites = self._sort_sprites(sort_target='hitbox')
        for sprite in _sorted_sprites:
            #-- draw bounding boxes, for debugging purposes
            #pygame.draw.rect(self.display_surface, RED, sprite.hitbox_rect, 1)
            #pygame.draw.rect(self.display_surface, DARKVIOLET, sprite.rect, 1)
            #pygame.draw.rect(self.display_surface, BLUE, sprite.test_rect, 1)

            offset_vector = sprite.rect.topleft - self.camera_offset
            self.display_surface.blit(sprite.image, offset_vector)

    def zoom_keys(self):
        keys_pressed = pygame.key.get_pressed()

        delta_zoom = 0
        if keys_pressed[pygame.K_q]:
            delta_zoom = 0.1

        elif keys_pressed[pygame.K_e]:
            delta_zoom = -0.1

        self.zoom_level += delta_zoom

    def custom_draw_with_zoom(self, player):
        self.center_camera_on_target(player)
        self.zoom_keys()
        self.internal_surface.fill(SCREEN_FILL)

        _sorted_sprites = self._sort_sprites('hitbox')
        for sprite in _sorted_sprites:
            offset_vector = sprite.rect.topleft - self.camera_offset + self.internal_offset
            self.internal_surface.blit(sprite.image, offset_vector)

        #-- Scale internal surface according to zoom level
        scaled_surface = pygame.transform.scale(self.internal_surface, self.internal_surface_size_vector * self.zoom_level)
        scaled_rect    = scaled_surface.get_rect(center = (self.half_screen_width, self.half_screen_height))

        #-- draw regular display onto zoom display
        self.display_surface.blit(scaled_surface, scaled_rect)


    def _sort_sprites(self, sort_target='hitbox'):
        if sort_target.lower() == 'hitbox':
            _sorted = sorted(self.sprites(), key = lambda sprite: sprite.hitbox_rect.top)
        
        elif sort_target.lower() == 'center':
            _sorted = sorted(self.sprites(), key = lambda sprite: sprite.rect.centery)

        return _sorted