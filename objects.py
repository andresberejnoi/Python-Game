import pygame
import random 

class BaseObject(pygame.sprite.Sprite):
    def __init__(self, screen, width=50, height=50, color=(140,140,255)) -> None:
        super().__init__()

        min_x_border = width  / 2
        min_y_border = height / 2

        self.x = random.randint(min_x_border, screen.get_width() - min_x_border)
        self.y = random.randint(min_y_border, screen.get_height() - min_y_border)

        self.width  = width
        self.height = height
        self.color  = color


    def update(self, screen):
        rect_bounds = (self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, self.color, rect_bounds)

class Rock(BaseObject):
    def __init__(self, screen, width=50, height=50, color=(200, 200, 180)) -> None:
        super().__init__(screen, width, height, color)
