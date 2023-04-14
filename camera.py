import pygame
from config import * 

class Camera(pygame.sprite.Group):
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

    def custom_draw(self, player):
        self.center_camera_on_target(player)
        #self.zoom_keys()

        _sorted_sprites = self._sort_sprites(sort_target='hitbox')
        #for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
        for sprite in _sorted_sprites:
            pygame.draw.rect(self.display_surface, RED, sprite.hitbox_rect, 1)
            pygame.draw.rect(self.display_surface, DARKVIOLET, sprite.rect, 1)
            #pygame.draw.rect(self.display_surface, BLUE, sprite.test_rect, 1)
            self.display_surface.blit(sprite.image, sprite.rect)

    def _sort_sprites(self, sort_target='hitbox'):
        if sort_target.lower() == 'hitbox':
            _sorted = sorted(self.sprites(), key = lambda sprite: sprite.hitbox_rect.top)
        
        elif sort_target.lower() == 'center':
            _sorted = sorted(self.sprites(), key = lambda sprite: sprite.rect.centery)

        return _sorted